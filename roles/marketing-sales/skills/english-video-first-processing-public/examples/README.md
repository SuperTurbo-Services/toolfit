# Examples

**Everything in this folder is synthetic.** It was written to show the shape of
each file, not to represent a real recording, a real company or a real
transcription result. `ExampleCorp` is not a company.

| File | What it shows |
|---|---|
| `glossary.example.json` | The shape of a project glossary. Copy it, replace every value with your own proper nouns and habitual fillers, pass it to `build_srt.py --glossary` |
| `sample.transcripts.json` | The shape of the step 5 output: a JSON list of strings, one per window, in manifest order, with `""` for a silent window |

The sample transcript deliberately includes the edge cases worth testing: an
empty string for a silent window, a multi word filler (`All right`) that would
strand a lone `All` if single word stripping ran first, a doubled word
(`And and`), a bracketed stage direction, and two product names that a speech to
text engine commonly mishears.
