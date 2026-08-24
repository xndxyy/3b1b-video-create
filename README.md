# Deep Learning — 3Blue1Brown Style Video Course

> A reproducible pipeline for turning a textbook (《深度学习入门：基于Python的理论与实现》by 斋藤康毅 / "Deep Learning from Scratch") into 3Blue1Brown-style explainer videos: long-form narrative script → cloned-voice narration → math/geometry animation → ffmpeg assembly.

This repository is **self-contained and privacy-safe**. All absolute paths, machine-specific config, and voice-clone references have been replaced with placeholders (`<PROJECT_ROOT>`, `<REFERENCE_VOICE_WAV>`, etc.). Nothing here points back to the original author's machine.

---

## What's inside

```
deep-learning-3b1b-video/
├── README.md              ← You are here. Start here.
├── AGENTS.md              ← Operating manual for the AI agent (Codex / Claude / etc.)
├── .env.example           ← Copy to .env and fill in your local paths & model refs
├── .gitignore             ← Excludes media, voice clones, venvs, large binaries
├── LICENSE                ← MIT
├── docs/
│   ├── workflow.md            ← Full step-by-step production pipeline
│   ├── 3b1b-style-guide.md    ← Visual language: colors, motion, composition
│   ├── voice-cloning.md       ← VoxCPM2 narration generation (generic)
│   ├── skill-recipes.md       ← Summarized skill workflows (khazix-writer, hyperframes, manim-video)
│   └── ffmpeg-cookbook.md     ← Assembly / concat / pad patterns
├── templates/
│   ├── gen_voice.py           ← Voice generation script (env-driven, no hard paths)
│   ├── assemble.py            ← Final ffmpeg assembly (auto timing from segments)
│   └── scenes_template.py     ← Manim animation template (generic, from a worked example)
└── samples/
    └── ch02_perceptron_script.md  ← A finished example script (Chapter 2: Perceptron)
```

## Tech stack

| Purpose | Tool | Notes |
|---------|------|-------|
| Math / geometry animation | **Manim Community** | `pip install manim` (tested on 0.20.1). Alternative: HyperFrames (HTML/CSS/JS). |
| Web / packaging animation | **HyperFrames** | HTML-based video composition; good for title cards, dynamic text, transitions. |
| Narration (voice clone) | **VoxCPM2** | `openbmb/VoxCPM2`, runs on CUDA GPU. Needs a reference `.wav` of the target voice. |
| Speech recognition | **Whisper** | Optional; for timestamp alignment if you re-record. |
| Final assembly | **ffmpeg** | Any recent build (8.x tested). |
| Web-style wrappers (optional) | **Remotion** | For intro/outro, cover, lower-thirds. |

All tools are installed locally by the user. This repo ships **code + workflow**, not binaries.

## Quick start (for the AI agent)

When a user asks you to "make a video for chapter N", follow `docs/workflow.md`. In short:

1. Read the textbook chapter → extract core concepts.
2. Write the script with the **khazix-writer** persona + **3B1B** visual style (see `docs/skill-recipes.md` and `docs/3b1b-style-guide.md`). Target word counts are in `AGENTS.md`.
3. Split the narration into `<280`-char Chinese segments; generate audio with `templates/gen_voice.py` (driven by `<REFERENCE_VOICE_WAV>`).
4. Build animations (Manim `scenes_template.py` or HyperFrames) timed to the audio.
5. Assemble with `templates/assemble.py` + ffmpeg.

See `samples/ch02_perceptron_script.md` for a finished reference.

## Privacy notes

- No personal names, home-directory paths, or private voice files are committed.
- Voice cloning requires the user to supply their **own** reference audio at runtime via `.env` (`REFERENCE_VOICE_WAV`). The repo never ships voice data.
- Large media (`*.mp4`, `*.wav`, `voiceover*`, `seg_*.wav`) is git-ignored by default.

## License

MIT — do whatever you want with the pipeline and scripts. The textbook content itself belongs to its publisher; this repo contains only original scripts and tooling.
