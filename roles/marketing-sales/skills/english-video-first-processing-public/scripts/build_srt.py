#!/usr/bin/env python3
"""Build an SRT from a segment manifest plus one transcript per segment.

Timing comes from each segment's known (start, end) in the source recording,
never from a word-matching cursor run across the whole file. That is what stops
the second half drifting.

Inputs:
  --manifest     segments.json written by segment_audio.py
  --transcripts  JSON list[str], one entry per manifest segment, same order.
                 A silent segment is "" and must still be present.
  --output       path to write the .srt (required, no default)
  --glossary     optional JSON with project-specific cleaning rules

Glossary shape, every key optional:
  {
    "corrections":    {"<regex>": "<replacement>"},
    "grammar":        {"<regex>": "<replacement>"},
    "fillers_multi":  ["all right", "so yeah"],
    "fillers_single": ["um", "uh"],
    "protect":        ["DeepSeek", "PostgreSQL"]
  }

Nothing project-specific is built in. The defaults below are limited to cleanups
that are safe for any English recording.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


# --------------------------------------------------------------------------
# Universally safe defaults. Anything project-specific belongs in a glossary.
# --------------------------------------------------------------------------

DEFAULT_CORRECTIONS = {
    r"\(\s*click(?:s)?\s*\)": "",
    r"\(\s*clicks? (?:mouse|tongue)\s*\)": "",
    r"\(\s*(?:laughs?|coughs?|sighs?|inaudible|music)\s*\)": "",
    r"\[\s*(?:laughs?|coughs?|sighs?|inaudible|music)\s*\]": "",
}

DEFAULT_FILLERS_MULTI = ["you know", "i mean", "sort of", "kind of"]
DEFAULT_FILLERS_SINGLE = ["um", "uh", "erm", "uhm", "hmm"]

DEFAULT_GRAMMAR = {
    r"\b(\w+)\s+\1\b": r"\1",       # doubled word: "and and" -> "and"
    r"\s+([.,?!;:])": r"\1",
    r",\s*,": ",",
    r"\s{2,}": " ",
    r"^\s*[,.]\s*": "",
    r"[-–—]\s*$": "",
}

# Words a cue may not end on. Pronouns are deliberately allowed: they are
# frequently the object of the clause and reading fine at a line break.
DANGLERS = set("""
the a an to of in on at by for with from into onto upon about over under
your my our their his her its
is are was were be been being am have has had do does did
will would could should can may might must shall
this that these those
as or and but so if because when while which who whom whose what how than
much many more most few less fewer several such very quite
""".split())

CONNECTORS = [" and then ", " because ", " which ", " when ", " while ",
              " if ", " so that ", " so ", " but ", " or ", " and ", " then "]


def load_glossary(path):
    g = {"corrections": {}, "grammar": {}, "fillers_multi": [],
         "fillers_single": [], "protect": []}
    if not path:
        return g
    p = Path(path)
    if not p.is_file():
        sys.exit(f"glossary not found: {path}")
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"glossary is not valid JSON: {e}")
    if not isinstance(raw, dict):
        sys.exit("glossary must be a JSON object")
    for key in g:
        if key in raw:
            g[key] = raw[key]
    for key in ("corrections", "grammar"):
        for pattern in g[key]:
            try:
                re.compile(pattern)
            except re.error as e:
                sys.exit(f"glossary {key} has an invalid regex {pattern!r}: {e}")
    return g


def build_cleaner(gloss):
    corrections = dict(DEFAULT_CORRECTIONS)
    corrections.update(gloss["corrections"])

    # Multi-word fillers ALWAYS run before single-word ones. Otherwise stripping
    # "right" out of "all right" strands a lone "All".
    multi = list(gloss["fillers_multi"]) + list(DEFAULT_FILLERS_MULTI)
    multi.sort(key=len, reverse=True)
    single = list(gloss["fillers_single"]) + list(DEFAULT_FILLERS_SINGLE)

    filler_patterns = [r"\b" + re.escape(f) + r"\b[,.]?\s*" for f in multi]
    filler_patterns += [r"\b" + re.escape(f) + r"\b[,.]?\s*" for f in single]

    grammar = dict(gloss["grammar"])
    grammar.update(DEFAULT_GRAMMAR)  # structural repairs run last

    def clean(text):
        out = text or ""
        for pat, rep in corrections.items():
            out = re.sub(pat, rep, out, flags=re.IGNORECASE)
        for pat in filler_patterns:
            out = re.sub(pat, " ", out, flags=re.IGNORECASE)
        for pat, rep in grammar.items():
            out = re.sub(pat, rep, out, flags=re.IGNORECASE)
        out = re.sub(r"\s+([.,?!;:])", r"\1", out)
        out = re.sub(r"\s{2,}", " ", out)
        return out.strip()

    return clean


def split_sentence(s, mx, protect):
    if len(s) <= mx:
        return [s]

    mid = len(s) // 2
    best = None
    for con in CONNECTORS:
        for m in re.finditer(re.escape(con), s, flags=re.IGNORECASE):
            p = m.start()
            left, right = s[:p].strip(), s[p + len(con):].strip()
            if not left or not right:
                continue
            score = abs(p - mid)
            if best is None or score < best[0]:
                best = (score, left, con.strip() + " " + right)
    if best:
        return split_sentence(best[1], mx, protect) + split_sentence(best[2], mx, protect)

    commas = [m.start() for m in re.finditer(r",", s)]
    if commas:
        bp = min(commas, key=lambda p: abs(p - mid))
        left, right = s[:bp].strip(), s[bp + 1:].strip()
        if left and right:
            return split_sentence(left, mx, protect) + split_sentence(right, mx, protect)

    words = s.split()
    if len(words) <= 1:
        return [s]

    # Character offset of the start of each word, for the protect check.
    offsets, cursor = [], 0
    for w in words:
        offsets.append(cursor)
        cursor += len(w) + 1

    def breaks_protected(i):
        """True if splitting before word i would cut a protected phrase."""
        cut = offsets[i]
        for term in protect:
            for m in re.finditer(re.escape(term), s, flags=re.IGNORECASE):
                if m.start() < cut < m.end():
                    return True
        return False

    target = len(s) // 2
    for i in sorted(range(1, len(words)), key=lambda i: abs(offsets[i] - target)):
        if words[i - 1].lower().strip(".,!?;:") in DANGLERS:
            continue
        if breaks_protected(i):
            continue
        left, right = " ".join(words[:i]), " ".join(words[i:])
        if max(len(left), len(right)) <= mx * 1.4:
            return split_sentence(left, mx, protect) + split_sentence(right, mx, protect)

    i = len(words) // 2
    return (split_sentence(" ".join(words[:i]), mx, protect)
            + split_sentence(" ".join(words[i:]), mx, protect))


def chunk_text(text, mx, protect):
    chunks = []
    for sentence in re.split(r"(?<=[.?!])\s+", text):
        sentence = sentence.strip()
        if sentence:
            chunks.extend(split_sentence(sentence, mx, protect))

    stripped = []
    for c in chunks:
        c = re.sub(r"[.,?!;:]", " ", c)
        c = re.sub(r"\s{2,}", " ", c).strip()
        if c:
            stripped.append(c)

    merged = []
    for c in stripped:
        if (merged and (len(c) <= 8 or len(merged[-1]) <= 8)
                and len(merged[-1]) + 1 + len(c) <= mx):
            merged[-1] += " " + c
        else:
            merged.append(c)

    # A connector or comma split can still leave a dangling word at the end of a
    # cue. Push any trailing dangler onto the next cue where it fits. Runs to a
    # fixed point because moving one word can expose another behind it.
    for _ in range(4):
        moved = False
        for i in range(len(merged) - 1):
            words = merged[i].split()
            if len(words) < 2:
                continue
            if words[-1].lower() not in DANGLERS:
                continue
            if len(words[-1]) + 1 + len(merged[i + 1]) > mx:
                continue
            merged[i] = " ".join(words[:-1])
            merged[i + 1] = words[-1] + " " + merged[i + 1]
            moved = True
        if not moved:
            break
    return [c for c in merged if c]


def srt_time(t):
    t = max(t, 0.0)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        t, ms = t + 1, 0
    return f"{int(t)//3600:02d}:{(int(t)//60)%60:02d}:{int(t)%60:02d},{ms:03d}"


def leading_silence(seg_path, threshold=0.35, max_skip=2.0):
    """Seconds of silence at the very start of this slice, else 0."""
    if not shutil.which("ffmpeg"):
        return 0.0
    proc = subprocess.run(
        ["ffmpeg", "-i", str(seg_path),
         "-af", "silencedetect=noise=-30dB:d=0.2", "-f", "null", "-"],
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
    for s, e in zip(starts, ends):
        if s < threshold:
            return min(e, max_skip)
    return 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--transcripts", required=True)
    ap.add_argument("--output", required=True,
                    help="where to write the .srt. Required: nothing is written anywhere else.")
    ap.add_argument("--glossary", default=None)
    ap.add_argument("--max-chars", type=int, default=55)
    ap.add_argument("--min-dwell", type=float, default=0.6)
    ap.add_argument("--max-dwell", type=float, default=6.0)
    ap.add_argument("--no-silence-skip", action="store_true",
                    help="do not re-probe each slice for leading silence")
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    transcripts = json.loads(Path(args.transcripts).read_text(encoding="utf-8"))

    if not isinstance(transcripts, list):
        sys.exit("--transcripts must be a JSON list of strings")
    if len(manifest) != len(transcripts):
        sys.exit(
            f"length mismatch: manifest has {len(manifest)} segments, "
            f"transcripts has {len(transcripts)}. A silent segment must be \"\", "
            f"not omitted, or every cue after it lands on the wrong window."
        )

    gloss = load_glossary(args.glossary)
    clean = build_cleaner(gloss)
    protect = list(gloss["protect"])

    entries = []
    for seg, raw in zip(manifest, transcripts):
        if not (raw or "").strip():
            continue
        seg_start = float(seg["start"])
        seg_end = float(seg["end"])
        if not args.no_silence_skip and seg.get("path"):
            lead = leading_silence(seg["path"])
            if lead > 0.05:
                seg_start += lead
        if seg_end - seg_start < 0.2:
            seg_start = float(seg["start"])

        chunks = chunk_text(clean(raw), args.max_chars, protect)
        if not chunks:
            continue

        total = sum(len(c) for c in chunks) or 1
        usable = max(seg_end - seg_start - 0.05, 0.5)
        cursor = seg_start + 0.05
        for c in chunks:
            dur = min(max(usable * len(c) / total, args.min_dwell), args.max_dwell)
            start = cursor
            end = min(seg_end - 0.02, start + dur)
            if end - start < 0.5:
                end = start + 0.5
            entries.append([start, end, c])
            cursor = end + 0.02

    entries.sort(key=lambda e: e[0])
    for i in range(len(entries) - 1):
        if entries[i][1] > entries[i + 1][0] - 0.02:
            entries[i][1] = max(entries[i][0] + 0.45, entries[i + 1][0] - 0.02)

    out_path = Path(args.output)
    if out_path.parent and not out_path.parent.exists():
        sys.exit(f"output directory does not exist: {out_path.parent}. "
                 f"This skill does not create folders.")

    lines = []
    for idx, (start, end, text) in enumerate(entries, 1):
        lines += [str(idx), f"{srt_time(start)} --> {srt_time(end)}", text, ""]
    out_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {out_path} ({len(entries)} cues from {len(manifest)} windows)")


if __name__ == "__main__":
    main()
