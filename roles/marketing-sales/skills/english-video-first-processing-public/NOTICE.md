# Notice

## This work

Copyright 2026 SuperTurbo. Licensed under the PolyForm Noncommercial License
1.0.0. See `LICENSE` for terms and `COMMERCIAL.md` for commercial licensing.

Required Notice: Copyright 2026 SuperTurbo

## Third party material

**None.** No third party code, prose, templates or assets are included in this
skill.

Two design ideas were adopted independently after surveying the field, and
neither involved copying any protected expression:

- Presenting every external dependency as a tiered mode with a graceful fallback,
  rather than naming one tool and failing without it. This is a widely used
  pattern in agent skills; the implementation and wording here are original.
- Holding project specific configuration in a user supplied file rather than
  hardcoding it, so one install serves many projects. Also a general pattern;
  the glossary schema, the code and the documentation here are original.

Approach and method are not protected by copyright. Expression is, and none was
taken.

## Runtime dependencies not distributed here

- **FFmpeg** (`ffmpeg`, `ffprobe`). Required, not bundled. The user must already
  have it. FFmpeg is licensed LGPL 2.1 or later, with some builds GPL. Because
  this skill only invokes the binaries the user already installed and does not
  link against or redistribute them, no FFmpeg obligation attaches to this skill.
- **Python 3.8 or newer.** Standard library only. No third party packages are
  imported, installed or required.

## Verification

Facts in this skill that concern the outside world are limited to FFmpeg filter
names and flags (`silencedetect`, `afftdn`, `highpass`, `subtitles`), all of
which are long standing and stable. Verified against the FFmpeg filters
documentation on 25 August 2026. Re-check if a run reports an unknown filter.
