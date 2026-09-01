#!/usr/bin/env python3
"""Cut an audio file into 6 to 15 second windows at silence boundaries.

Writes one sliced mp3 per window plus a manifest the agent reads to drive
per-window transcription. Each manifest entry carries the window's true start
and end in the source recording, and those become the subtitle timings.

Usage:
  python3 segment_audio.py \
    --audio /path/to/audio.mp3 \
    --out-dir /path/to/segments \
    --manifest /path/to/segments.json \
    [--min-seg 6.0] [--max-seg 15.0] [--silence-db -30] [--silence-dur 0.4]

Tuning: lower --min-seg/--max-seg to 4/10 for fast speech; lower --silence-db to
-35 or -40 in a noisy room; lower --silence-dur to 0.25 when the speaker barely
pauses.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def require_tools():
    missing = [t for t in ("ffmpeg", "ffprobe") if not shutil.which(t)]
    if missing:
        sys.exit(f"required tool(s) not on PATH: {', '.join(missing)}")


def find_silences(audio_path, db, dur):
    proc = subprocess.run(
        ["ffmpeg", "-i", str(audio_path),
         "-af", f"silencedetect=noise={db}dB:d={dur}",
         "-f", "null", "-"],
        capture_output=True, text=True
    )
    starts, ends = [], []
    for line in proc.stderr.splitlines():
        m = re.search(r"silence_start: (-?[\d.]+)", line)
        if m:
            starts.append(float(m.group(1)))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m:
            ends.append(float(m.group(1)))
    return sorted(zip(starts, ends))


def total_duration(audio_path):
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
        capture_output=True, text=True
    )
    try:
        return float(proc.stdout.strip())
    except ValueError:
        sys.exit(f"could not read a duration from {audio_path}. Is it a media file?")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--min-seg", type=float, default=6.0)
    ap.add_argument("--max-seg", type=float, default=15.0)
    ap.add_argument("--silence-db", type=int, default=-30)
    ap.add_argument("--silence-dur", type=float, default=0.4)
    args = ap.parse_args()

    require_tools()

    audio = Path(args.audio).resolve()
    if not audio.is_file():
        sys.exit(f"audio not found: {audio}")
    if args.min_seg >= args.max_seg:
        sys.exit("--min-seg must be smaller than --max-seg")

    out_dir = Path(args.out_dir).resolve()
    manifest_path = Path(args.manifest).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    total = total_duration(audio)
    silences = find_silences(audio, args.silence_db, args.silence_dur)

    # Candidate cut points: the start, the end of every silence, and the end.
    cuts = [0.0]
    for _, end in silences:
        if end - cuts[-1] > 0.5:
            cuts.append(end)
    if total - cuts[-1] > 0.2:
        cuts.append(total)

    segments = []
    seg_start = cuts[0]
    for c in cuts[1:]:
        if c - seg_start < args.min_seg:
            continue
        if c - seg_start <= args.max_seg:
            segments.append((seg_start, c))
            seg_start = c
        else:
            best = None
            for prev in cuts:
                if seg_start + args.min_seg <= prev <= seg_start + args.max_seg:
                    best = prev
            if best is None:
                best = seg_start + args.max_seg
            segments.append((seg_start, best))
            seg_start = best
    if seg_start < total - 0.1:
        segments.append((seg_start, total))

    if not segments:
        sys.exit("no segments produced. The file may be silent, or --silence-db "
                 "may be set so that the whole recording reads as silence.")

    manifest = []
    for i, (a, b) in enumerate(segments):
        path = out_dir / f"seg_{i + 1:03d}.mp3"
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", f"{a:.3f}", "-i", str(audio),
            "-t", f"{b - a:.3f}",
            "-c:a", "libmp3lame", "-b:a", "128k", str(path)
        ], check=True)
        manifest.append({
            "idx": i + 1,
            "start": round(a, 3),
            "end": round(b, 3),
            "duration": round(b - a, 3),
            "path": str(path),
        })

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    longest = max(s["duration"] for s in manifest)
    print(f"wrote {len(manifest)} windows to {out_dir} (longest {longest:.1f}s)")
    print(f"manifest: {manifest_path}")
    print(f"transcribe each window separately, then emit {len(manifest)} strings "
          f"in this order (\"\" for silent windows)")


if __name__ == "__main__":
    main()
