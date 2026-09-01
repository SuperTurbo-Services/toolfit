# Step 0 in detail: matching the pipeline to what the user already has

Read this when the user's answer to "how should I turn speech into text" is not
one of the obvious cases, or when a mode needs wiring up.

The pipeline never changes. Only the call inside step 5 changes. Everything
before and after it is identical in every mode.

---

## The question to ask

Ask both parts at once, in plain language, before touching the file:

> To build the subtitles I need two things from you.
>
> **1. A way to turn speech into text.** That could be a transcription tool
> connected to this session, a command line tool on your machine, a hosted API
> whose key is already in your environment, or a transcript you already have.
> If you have none of those, say so and I will still build the timings.
>
> **2. Whether to clean up the audio first,** and with what. If you are not sure,
> I can do a modest pass with ffmpeg, or skip it.

Do not guess. Do not probe the environment and assume. A wrong assumption here
costs the whole run.

---

## Transcription modes

### `mcp` — a connected speech to text tool

The strongest option when it exists, because it needs no local install.

- Call it **once per segment file**, passing that segment's `path` from the
  manifest. Never pass the full recording.
- Use whatever parameter names the tool actually exposes. Tool schemas differ
  and change; read the schema rather than assuming a field name.
- Prefer options that return text to you directly over ones that write files.
  Files mean a second read and a cleanup step.
- Set the language explicitly if the tool accepts it. Auto detection on a six
  second window is much less reliable than on a whole file.
- Batch about 8 concurrent calls. More tends to hit rate limits and the retries
  cost more than the parallelism saved.

### `cli` — a local command

Ask for the exact command once, then reuse it for every segment. For example:

```bash
<their-command> "<segment-path>" > "<work>/seg_001.txt"
```

Some CLI transcribers write a file next to the input instead of printing to
stdout. Establish which on the first segment, then loop.

If the user's CLI is a Whisper build, this skill still helps: feeding it six to
fifteen second windows with known boundaries removes the long range drift that
whole file Whisper suffers from. Windowing is the fix, not the vendor.

### `api` — a hosted endpoint

- **Never ask the user to paste a key into the chat.** Ask which environment
  variable holds it and read it at run time.
- Post one segment per request.
- Handle a failed segment by retrying once, then recording `""` for it and
  telling the user which window failed. A missing entry breaks the manifest
  alignment; an empty string does not.

### `transcript` — text the user already has

Useful when the user has a script they read from, or captions from another tool
that are accurate in wording but wrong in timing.

1. Clean the supplied text of speaker labels and existing timecodes.
2. Split it across the windows in proportion to each window's duration.
3. Show the user the first three and last three windows with their assigned text
   and ask them to correct the boundaries. Proportional splitting drifts wherever
   speaking pace changes, and the user can see that instantly.

This mode is a good fit for scripted content and a poor one for improvised
speech.

### `none` — no transcription available

Say so plainly, in one sentence, and offer the **timing skeleton**: a valid SRT
with correct in and out times and a `TYPE HERE` placeholder on every cue.

```bash
python3 -c "
import json,sys
m=json.load(open(sys.argv[1]))
json.dump(['TYPE HERE' for _ in m], open(sys.argv[2],'w'))
" "<work>/segments.json" "<work>/transcripts.json"
```

Then run step 6 as normal. The user gets a file with every cue already timed to
their speech, and types over the placeholders in any subtitle editor. That is a
real saving over starting from an empty file, and it is honest about what it is.

Do not offer to install a transcription engine on their machine. A setup they
did not ask for is a support burden.

---

## Denoise modes

### A connected or hosted audio cleanup tool

Run it on the extracted audio, then use its output everywhere downstream.

Most speech isolation models attenuate the voice while removing the noise floor,
commonly by around 3 to 4 dB. If you are muxing the cleaned audio back into a
video, a gain of roughly 1.4x usually restores the perceived loudness. **Treat
that as a starting point and ask the user to confirm by ear**, because it varies
by model, by version and by how loud the original was. Too much gain clips.

### ffmpeg only

```bash
ffmpeg -y -loglevel error -i in.mp3 -af "afftdn=nf=-25,highpass=f=80" out.mp3
```

`afftdn` is an adaptive noise reducer and `highpass` removes rumble below the
speaking range. Modest, free, available everywhere, and it will not damage
speech at these settings.

For a stronger pass on a consistently noisy recording, raise the noise floor
estimate: `afftdn=nf=-20`. Listen before accepting it; aggressive settings make
speech sound underwater.

### Skip

Perfectly reasonable. Denoising mainly helps silence detection in a noisy room.
On a clean recording it changes nothing about the subtitles.

---

## The rule that survives every mode

**Segment and transcribe the same file.** If you denoised, the segmenter, the
transcriber and the leading silence check all run on the denoised audio. Mixing
the raw and cleaned versions shifts every timestamp by however much the cleanup
trimmed, and the error is invisible until someone watches the video.
