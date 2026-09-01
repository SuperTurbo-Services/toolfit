# Video to synced SRT

Turns a spoken video or audio recording into one `.srt` subtitle file whose
timing does not drift.

## The problem it solves

Feed a whole recording to a transcription engine and ask for subtitles, and the
first minute usually looks fine. Somewhere in the middle the cues start arriving
early or late, and by the end they can be several seconds out. This happens most
on accented speech, filler heavy speech, and recordings with long pauses, and it
happens across engines.

The cause is that a whole file pass places every word on one long timeline, so a
small error early compounds all the way down.

This skill cuts the recording into six to fifteen second windows at natural
silence boundaries first, transcribes each window on its own, and anchors that
window's subtitles to its own known start and end. An error inside one window
stays inside that window. Nothing accumulates.

## What you need

- **FFmpeg**, providing `ffmpeg` and `ffprobe` on your PATH. Required.
- **Python 3.8 or newer.** Standard library only, nothing to install.
- **A way to turn speech into text.** The skill asks you what you have at the
  start and adapts. A connected transcription tool, a command line tool, a hosted
  API, or a transcript you already hold all work. See below for the case where
  you have none.

There is no account to create, no API key this skill holds, and no other skill it
depends on.

## What you get

- `<name>.srt`, a sidecar subtitle file: single line cues, at most 55 characters,
  punctuation stripped for on screen readability, no cue ending on a dangling
  word.
- Optionally a denoised audio or video track, if you asked for one.

Subtitles are **not** burned into the video. A sidecar stays editable, uploads to
any platform, and can be translated later. Burning in is one `ffmpeg` command
when you want it.

## Using it

Say something like:

> Make subtitles for `demo.mp4` and put the SRT next to it.

The skill will ask you two questions before it starts: how to turn speech into
text, and whether to clean the audio first. Answer those and it runs.

### The glossary is worth two minutes

Copy `examples/glossary.example.json`, put your product names, people's names and
your own habitual filler words in it, and pass it with `--glossary`. Every
transcription engine mishears proper nouns, and the glossary fixes each one
once instead of every run. This is the difference between a file you use and a
file you retype.

## If you have no transcription engine at all

The skill says so plainly and offers a **timing skeleton**: a valid SRT with
every cue already timed to your speech and a placeholder where the words go. You
type over the placeholders in any subtitle editor. That is much faster than
starting from an empty file, and it is the honest floor rather than a failure.

## What it does not do

- It does not burn subtitles into video.
- It does not translate.
- It does not write a social post, a title, or a thumbnail. Those are separate
  jobs and this skill stays out of them.
- It does not create folders. You give it an output path that already exists, and
  that is the only place it writes. Scratch files go to a temp directory.

## Licence

**PolyForm Noncommercial License 1.0.0.** Free forever for personal use, study,
hobby projects, and for charities, schools, universities, public research bodies
and government institutions. Commercial use needs a licence from SuperTurbo. See
`COMMERCIAL.md`.

This is not an OSI approved open source licence, and that is deliberate.
