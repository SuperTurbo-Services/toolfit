# Pre-flight checklist

Walk this before telling the user a run is finished. Every line here corresponds
to a failure that has actually happened.

## Step 0, toolchain declared
- [ ] The user was asked how speech becomes text, and answered
- [ ] The user was asked whether to denoise, and answered
- [ ] Neither was assumed from what happens to be installed

## Step 1, inputs
- [ ] `ffmpeg` and `ffprobe` are on PATH
- [ ] The input file exists and `ffprobe` returned a duration
- [ ] The output path was supplied by the user and its parent folder exists

## Steps 2 to 4, audio and windows
- [ ] Audio extracted
- [ ] If denoised, the denoised file is what steps 4, 5 and 6 all use
- [ ] `segment_audio.py` ran and reported a window count
- [ ] Window count looks sane: roughly 20 to 30 for a 3 to 5 minute recording.
      Two or three windows for a long recording means `--silence-db` is wrong

## Step 5, transcription
- [ ] Each window was transcribed **on its own**, never the whole file
- [ ] `transcripts.json` is a JSON list of strings
- [ ] Its length equals the manifest length
- [ ] Silent windows are `""`, not omitted
- [ ] Order matches the manifest exactly

## Step 6, the SRT
- [ ] A project glossary was offered, and used if the user supplied proper nouns
- [ ] `build_srt.py` ran with `--output` pointing where the user asked
- [ ] The script created no folders

## Step 7, verification
- [ ] `check_srt.py` ran and reported structure OK
- [ ] The first cue is within about 1.5s of the first speech
- [ ] Listened at roughly 10%, 50% and 90%: the cue on screen matches the words
- [ ] If any drifted over 1.5s, re-ran step 4 with `--min-seg 4 --max-seg 10`
- [ ] The result of these checks was reported to the user, including failures

## Step 8, delivery
- [ ] The `.srt` was handed over at the path the user named
- [ ] The user was told which transcription mode was used and how many windows
- [ ] Nothing was written into the user's project folder that they did not ask for
- [ ] Scratch files are in a temp area, not beside their video
