# Templates

Copy these into a per-chapter working folder (e.g. `ch03_neural_network/`) and adapt.

| File | Purpose |
|------|---------|
| `gen_voice.py` | Generate cloned-voice narration. Fill `SEGMENTS` (<280 chars each), set `.env`, run in VoxCPM2 venv. Outputs `seg_NN.wav` + `voiceover.wav`. |
| `assemble.py` | Final ffmpeg assembly. Maps scenes→segments, pads/trims clips, concatenates, muxes audio. Set `SCENE_SEGMENTS` + `.env`. |
| `scenes_template.py` | *(see samples/ for a full worked example)* Start from `samples/ch02_perceptron_scenes.py` — a complete Chapter 2 Manim animation using the 3B1B palette. |

## Per-chapter folder convention

```
<PROJECT_ROOT>/
└── chNN_topic/
    ├── script.md          ← narration (meets word minimum in AGENTS.md)
    ├── gen_voice.py       ← copy of template, SEGMENTS filled
    ├── scenes.py          ← Manim scenes (or HyperFrames index.html)
    ├── assemble.py        ← copy of template, SCENE_SEGMENTS set
    ├── seg_*.wav          ← generated (git-ignored)
    ├── voiceover.wav      ← generated (git-ignored)
    └── media/             ← Manim render output (git-ignored)
```

All paths come from `.env` / `<PROJECT_ROOT>`; never hardcode personal directories.
