#!/usr/bin/env python3
"""Structural check on a generated SRT, plus a speech-onset comparison.

Structure passing is NOT sync passing. This catches malformed output and an
obviously late first cue. Confirming that the words on screen match the words
spoken still requires listening at roughly 10%, 50% and 90% of the duration.

Usage:
  python3 check_srt.py --srt subs.srt [--audio audio.mp3] [--max-chars 55]
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

TS = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})")


def parse(path):
    cues, block = [], []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip() == "":
            if block:
                cues.append(block)
                block = []
        else:
            block.append(line)
    if block:
        cues.append(block)

    out = []
    for b in cues:
        m = next((TS.match(l) for l in b if TS.match(l)), None)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        text = [l for l in b if not TS.match(l) and not l.strip().isdigit()]
        out.append((start, end, text))
    return out


def first_speech(audio):
    """Seconds until the first non-silent audio, or None if unknown."""
    if not audio or not shutil.which("ffmpeg") or not Path(audio).is_file():
        return None
    proc = subprocess.run(
        ["ffmpeg", "-i", str(audio),
         "-af", "silencedetect=noise=-30dB:d=0.3", "-f", "null", "-"],
        capture_output=True, text=True)
    starts, ends = [], []
    for line in proc.stderr.splitlines():
        m = re.search(r"silence_start: (-?[\d.]+)", line)
        if m:
            starts.append(float(m.group(1)))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m:
            ends.append(float(m.group(1)))
    for s, e in zip(starts, ends):
        if s <= 0.1:
            return e
    return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--audio", default=None)
    ap.add_argument("--max-chars", type=int, default=55)
    ap.add_argument("--min-dwell", type=float, default=0.5)
    ap.add_argument("--max-dwell", type=float, default=6.5)
    args = ap.parse_args()

    cues = parse(args.srt)
    if not cues:
        sys.exit("no cues parsed. The file is empty or not valid SRT.")

    problems = []
    for i, (start, end, text) in enumerate(cues, 1):
        if end <= start:
            problems.append(f"cue {i}: end is not after start")
        dur = end - start
        if dur < args.min_dwell:
            problems.append(f"cue {i}: dwell {dur:.2f}s is under {args.min_dwell}s")
        if dur > args.max_dwell:
            problems.append(f"cue {i}: dwell {dur:.2f}s is over {args.max_dwell}s")
        if len(text) > 1:
            problems.append(f"cue {i}: {len(text)} lines, expected 1")
        for line in text:
            if len(line) > args.max_chars:
                problems.append(f"cue {i}: {len(line)} chars, over {args.max_chars}")
        if i < len(cues) and end > cues[i][0]:
            problems.append(f"cue {i}: overlaps cue {i + 1}")

    onset = first_speech(args.audio)
    if onset is not None:
        gap = cues[0][0] - onset
        note = f"first speech at {onset:.2f}s, first cue at {cues[0][0]:.2f}s (gap {gap:+.2f}s)"
        if abs(gap) > 1.5:
            problems.append(f"first cue is {gap:+.2f}s from first speech, over 1.5s")
        print(note)

    print(f"{len(cues)} cues, {cues[0][0]:.2f}s to {cues[-1][1]:.2f}s")
    if problems:
        print(f"\n{len(problems)} structural problem(s):")
        for p in problems[:40]:
            print(f"  - {p}")
        if len(problems) > 40:
            print(f"  ... and {len(problems) - 40} more")
        sys.exit(1)

    print("structure OK")
    print("NOT yet verified: that the words on screen match the words spoken.")
    print("Listen at 10%, 50% and 90% of the duration before calling this done.")


if __name__ == "__main__":
    main()
