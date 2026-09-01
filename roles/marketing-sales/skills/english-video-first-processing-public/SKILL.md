---
name: english-video-first-processing-public
description: "Build a tightly synced SRT subtitle file from a spoken video or audio recording, using silence anchored segment windows so the timing cannot drift in the second half. Optionally denoises the audio track first. Works with whatever transcription tooling the user already has (a speech to text MCP, a CLI, a hosted API, or an existing transcript) because the user declares the toolchain at the start and the skill adapts. Accepts a per project glossary so proper nouns, product names and habitual filler words are corrected consistently. Use when someone asks for subtitles, captions, an SRT, a transcript with timecodes, or says their captions drift out of sync partway through a recording. Does not burn subtitles into the video."
---

# Video to synced SRT

Produces one `.srt` file from a spoken recording, plus an optional denoised audio
or video track.

The whole point of this skill is a single design decision: **the recording is cut
into short silence bounded windows, and every window is transcribed on its own
known start and end time.** Timing comes from the window, never from a word
matching cursor running the length of the file. That is why the second half stays
in sync when a whole file transcription would have drifted.

This works no matter which transcription engine the user has, and it repairs the
common failure of accented or filler heavy speech regardless of vendor.

**Runs standalone.** No other skill is required. No account, no API key and no
paid tier is assumed. The only hard requirement is `ffmpeg` and `ffprobe` on the
PATH, plus Python 3.8 or newer.

---

## Step 0. Ask what tooling the user has. Do this first, always.

This is the one thing the skill cannot work out on its own, and getting it wrong
wastes the whole run. Ask before touching the file.

Ask two questions in a single message:

> 1. How should I turn speech into text? Tell me the tool, or say you have none.
> 2. Do you want the audio cleaned up first, and if so with what?

Offer these as the menu. Take whatever the user names, even if it is not listed.

### Transcription modes, best first

| Mode | The user has | What you do |
|---|---|---|
| `mcp` | A speech to text tool connected to this session | Call it once per segment file with the segment's path. Use whatever parameter names that tool actually exposes. Prefer options that return the text directly rather than writing files |
| `cli` | A local command, for example a whisper build, a vendor CLI, or their own script | Run it once per segment, capture stdout or the file it writes. Ask for the exact command line once, then reuse it |
| `api` | A hosted endpoint plus a key already in their environment | Post each segment file. Never ask the user to paste a key into the chat, read it from the environment variable they name |
| `transcript` | A script, caption file or transcript that already matches the recording | Skip transcription. Split the supplied text across the segments by proportion of characters, then let the user correct the segment boundaries |
| `none` | Nothing at all | Say plainly that text cannot be produced without a transcription engine. Offer the **timing skeleton**: a valid SRT with correct in and out times and a placeholder line per cue, which the user fills in by hand. This is genuinely useful and it is the honest floor |

Whatever the user names, the pipeline below does not change. Only the call in
step 5 changes.

### Denoise modes, best first

| Mode | The user has | What you do |
|---|---|---|
| `mcp` or `api` | An audio isolation or noise removal tool | Run it on the extracted audio. Most of them attenuate speech by roughly 3 to 4 dB, so if you remux the result back into a video, boost by about 1.4x and check by ear. Ask the user to confirm the loudness rather than assuming the constant |
| `ffmpeg` | Nothing beyond ffmpeg | `ffmpeg -i in.mp3 -af "afftdn=nf=-25,highpass=f=80" out.mp3`. Modest but free and always available |
| `none` | Wants to skip it | Skip it. Denoising helps segmentation slightly on noisy rooms and is optional everywhere else |

**Always segment and transcribe the same audio file.** If you denoised, every
later step uses the denoised file. Mixing the two shifts every timestamp.

---

## Step 1. Check the toolchain and read the input

```bash
command -v ffmpeg ffprobe || echo "MISSING"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "<input>"
```

If `ffmpeg` or `ffprobe` is missing, stop and say so in one line. Do not print
install instructions for the user's operating system unless they ask; a setup
walkthrough they did not request is a support burden, not help.

Record the duration. Step 7 needs it.

---

## Step 2. Extract the audio

```bash
ffmpeg -y -loglevel error -i "<input>" -vn -c:a libmp3lame -b:a 128k "<work>/audio.mp3"
```

If the input is already audio, use it directly.

`<work>` is a scratch directory. Put it in the system temp area, never inside the
user's project folder, unless the user asked for intermediates to be kept.

---

## Step 3. Denoise, if the user asked for it

Run the mode chosen in step 0. Keep the output path and use it for everything
after this point.

---

## Step 4. Cut the audio into silence bounded windows

```bash
python3 "${SKILL_DIR}/scripts/segment_audio.py" \
  --audio "<work>/audio.mp3" \
  --out-dir "<work>/segments" \
  --manifest "<work>/segments.json"
```

The script finds silences with `silencedetect`, then greedily groups the speech
between them into windows of 6 to 15 seconds. Each window becomes a sliced mp3
plus a manifest entry holding its true `start` and `end` in the original
recording.

A 3 to 5 minute recording usually yields 20 to 30 windows.

Tuning, only when step 7 shows drift:

| Flag | Default | Raise or lower when |
|---|---|---|
| `--min-seg` / `--max-seg` | 6.0 / 15.0 | Drop to `4` and `10` for fast or run on speech. Raise for slow, well paced delivery |
| `--silence-db` | -30 | Lower to `-35` or `-40` in a noisy room, where -30 mistakes room tone for speech. Raise to `-25` for a very quiet recording |
| `--silence-dur` | 0.4 | Lower to `0.25` when the speaker barely pauses |

---

## Step 5. Transcribe every window separately

For each entry in `segments.json`, transcribe **that segment file only**, using
the mode chosen in step 0. Do not send the whole recording. Sending the whole
file is the failure this skill exists to prevent.

Where the tool supports concurrency, batch about 8 at a time.

Collect the results into `<work>/transcripts.json`, a JSON list of strings, one
per manifest entry, **in manifest order**, each stripped of leading and trailing
whitespace. A window with no speech is an empty string, not a dropped entry. The
list length must equal the manifest length; `build_srt.py` refuses to run
otherwise, on purpose.

---

## Step 6. Build the SRT

```bash
python3 "${SKILL_DIR}/scripts/build_srt.py" \
  --manifest "<work>/segments.json" \
  --transcripts "<work>/transcripts.json" \
  --output "<output-path>/<name>.srt" \
  --glossary "<glossary.json>"
```

`--output` is required and there is no default. Write only where the user named.

`--glossary` is optional and is what makes this reusable across projects. Without
it the script applies a small set of universally safe cleanups only. See
**Step 6a**.

What the script does per window:

1. **Skips leading silence.** Re-runs `silencedetect` on the slice; if a silence
   starts within 0.35s of the window start, moves the start to that silence's end.
   Without this the first cue fires during a breath or a mouse click.
2. **Cleans the text** through three ordered layers: term corrections, filler
   removal, then grammar and spacing repair. Multi word fillers are always
   stripped before single word ones, otherwise stripping `right` out of
   `all right` strands a lone `All`.
3. **Chunks into single lines** of at most 55 characters. Splits on sentence
   enders first, then the connector nearest the middle, then a comma, then a word
   boundary. Never splits inside a word. A chunk may not end on an article,
   preposition, auxiliary or connector.
4. **Distributes time inside the window** in proportion to character count,
   clamped to a minimum dwell of 0.6s and a maximum of 6s, then caps any overlap
   against the next cue.

### Step 6a. The glossary

Copy `examples/glossary.example.json`, fill it in for this project, and pass it
with `--glossary`. Every field is optional.

```json
{
  "corrections":  { "\\bdeep sea\\b": "DeepSeek" },
  "fillers_multi": ["all right", "so yeah"],
  "fillers_single": ["um", "uh"],
  "grammar":      { "\\bAnd and\\b": "And" },
  "protect":      ["DeepSeek", "PostgreSQL"]
}
```

- **`corrections`** and **`grammar`** are regular expression to replacement maps,
  applied case insensitively. Corrections run first. This is where a speech to
  text engine's mishearing of a product name gets fixed once and for all.
- **`fillers_multi`** must contain every multi word filler, and it is applied
  before `fillers_single`. Order matters and the script enforces it.
- **`protect`** is a list of terms the chunker will never split across two lines.

Ask the user for their proper nouns before the first run. It takes one question
and it is the difference between a usable file and one they retype.

The script's own built in defaults are limited to `um`, `uh`, `you know`,
doubled words, stray bracketed stage directions and whitespace repair. Nothing
project specific is baked in, by design.

---

## Step 7. Check three timecodes before saying it is done

```bash
python3 "${SKILL_DIR}/scripts/check_srt.py" --srt "<output>.srt" --audio "<work>/audio.mp3"
```

The script reports structural problems: cues out of order, overlaps, zero length
or over long dwells, lines over the character limit, and the gap between the
recording's first detected speech and the first cue.

Structure passing is not sync passing. **Listen at three points**, roughly 10%,
50% and 90% of the duration, and confirm the cue on screen matches the words
spoken. If any is out by more than about 1.5 seconds, re-run step 4 with
`--min-seg 4 --max-seg 10` and rebuild. Report what you checked and what you
found; do not claim sync you did not verify.

---

## Step 8. Deliver

Walk `references/workflow_checklist.md` first. Every line on it is a failure that
has actually happened.

Hand over the `.srt`, and the denoised media if one was produced. Say which
transcription mode was used, how many windows were cut, and the result of the
three spot checks.

The SRT is a sidecar file. It is not burned into the video, which keeps it
editable, uploadable to any platform and translatable later. If the user wants it
burned in, that is a separate one line `ffmpeg` step they can run themselves:

```bash
ffmpeg -i in.mp4 -vf "subtitles=subs.srt" -c:a copy out.mp4
```

---

## Rules that must not be broken

These exist because each one is a real failure that was observed and fixed.

1. **Never transcribe the whole file for timing.** Whole file transcription plus
   proportional placement compounds small errors into seconds by the second half.
   Every timestamp comes from a window's known start and end.
2. **Segment and transcribe the same audio.** If you denoised, everything
   downstream uses the denoised file.
3. **Skip leading silence per window.** 0.35s tolerance, or the first cue fires
   during a breath.
4. **Multi word fillers before single word fillers.** Always.
5. **Every correction is case insensitive.** A mis-heard product name appears
   capitalised at the start of a sentence and lowercase inside one.
6. **One line, 55 characters maximum.** Two line cues force the reader off the
   picture.
7. **A window with no speech is an empty string, not a missing entry.** The
   manifest and the transcript list must stay the same length and the same order.
8. **The SRT is the deliverable, not a burned in video.**
9. **Do not claim sync you did not check.** Step 7 is not optional and its result
   is reported, including when it fails.
10. **Write only where the user named.** No folder scaffolding, no default output
    location, no intermediates inside their project.

## Known failure modes and their fixes

| Symptom | Cause | Fix |
|---|---|---|
| Second half drifts | Whole file transcription was used | Re-run from step 4. This is the failure the skill exists for |
| First cue fires during silence | Leading silence skip did not trigger | Lower `--silence-dur` to `0.25` in step 4 |
| A product name is wrong everywhere | No glossary, or the pattern was not case insensitive | Add it to `corrections` in the glossary |
| A stray `All` or `So` sits alone in a cue | A multi word filler was listed in `fillers_single` | Move it to `fillers_multi` |
| A subtitle sits on screen through a long pause | Window contained one short line and a long silence | Already capped at 6s. Lower `--max-seg` if it persists |
| Cue splits a product name across two lines | Term not protected | Add it to `protect` in the glossary |
| Manifest and transcript length mismatch | A silent window was dropped instead of returned empty | Re-run step 5, emitting `""` for silent windows |

## Files

| File | What it is |
|---|---|
| `scripts/segment_audio.py` | Step 4. Silence detection and window slicing |
| `scripts/build_srt.py` | Step 6. Cleaning, chunking, timing, SRT writing |
| `scripts/check_srt.py` | Step 7. Structural validation and speech onset check |
| `references/toolchain.md` | Step 0 in detail. Worked examples of each mode |
| `references/workflow_checklist.md` | Before step 8. Walk it before saying a run is done |
| `examples/glossary.example.json` | Step 6a. Copy and fill in |
| `examples/sample.transcripts.json` | Synthetic example of the step 5 output shape |
| `examples/README.md` | What the synthetic examples cover and why |
