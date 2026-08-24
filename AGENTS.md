# AGENTS.md — Operating Manual for the Video Agent

You are helping a user produce 3Blue1Brown-style educational videos from a deep-learning textbook. This file is your standing instructions. Read it fully before starting any chapter.

## Project

Turn 《深度学习入门：基于Python的理论与实现》(斋藤康毅, "Deep Learning from Scratch") into a series of explainer videos. Each chapter = one video. Style reference: 3Blue1Brown (dark canvas, geometric math animation, calm narration). Narration uses a cloned voice via VoxCPM2.

A finished **example** (Chapter 2: Perceptron) ships in `samples/ch02_perceptron_script.md` — use it as the quality bar.

## Hard rules

1. **Never hardcode personal paths.** Use env vars / `<PROJECT_ROOT>` / `.env`. Paths to secrets, voice files, and venvs come from `.env`, never from memory.
2. **Never commit** `*.wav`, `*.mp4`, `voiceover*`, `seg_*.wav`, `.env`, venvs, or the textbook PDF. `.gitignore` already covers these.
3. **Word counts are a floor, not a ceiling.** Under the minimum = rejected. Over = fine.
4. **No bullet-list scripts.** Scripts are prose paragraphs (50–100 chars each), 3B1B-narrative rhythm.
5. **Split narration into `<280`-char Chinese segments** before TTS (VoxCPM2 OOMs above that).

## Script writing workflow (run in this order, per chapter)

```
1. Extract chapter concepts from the source PDF (raw material).
2. brainstorming — decide which concepts are mandatory, which are highlights, scene breakdown.
3. writing-fragments — collect the book's key definitions, examples, derivations as raw material.
4. writing-shape — shape fragments into full prose narration (paragraphs, not bullets).
5. humanizer-zh — strip AI traces, make it natural (3B1B narration voice).
6. manim-video (or hyperframes) — adjust rhythm to animation possibilities, write animation cues.
7. Split into <280-char SEGMENTS for VoxCPM2.
```

If the user has the `khazix-writer`, `humanizer-zh`, `manim-video`, `hyperframes` skills installed, use them. If not, `docs/skill-recipes.md` summarizes the equivalent workflow so you can still execute it.

## Per-chapter word-count targets (minimums)

| Chapter type | Min duration | Min words | Max words |
|--------------|--------------|-----------|-----------|
| Ch02 Perceptron (baseline) | 12 min | 3500 | unlimited |
| Simple (ch03/06) | 8–10 min | 3000 | unlimited |
| Complex (ch04/05/07) | 10–12 min | 3500 | unlimited |
| Summary (ch08) | 6–8 min | 2500 | unlimited |

Cover every section, every formula derivation, every Python implementation, every figure, every exercise the book has. Prefer a 30-min deep video over a 3-min summary.

## Production pipeline (per chapter)

```
1. Read PDF chapter → extract concepts.
2. Pick a visual preset: clean / texture / cinematic.
3. Write script per the workflow above (paragraph form, meet word minimum).
4. Generate narration with VoxCPM2 (templates/gen_voice.py), split <280 chars.
5. Build math/geometry animation (Manim scenes_template.py) or HyperFrames.
6. Assemble with ffmpeg (templates/assemble.py).
7. Whisper timestamp alignment (optional, only if re-recording).
```

## 3B1B color scheme (use these, not random colors)

```python
BG      = "#111111"   # canvas background (not pure black)
BLUE    = "#58C4DD"   # primary concept / neuron / main curve
GOLD    = "#F0AC5F"   # key conclusion / highlighted path
GREEN   = "#83C167"   # correct / activated / pass
RED_C   = "#FC6255"   # error / limit / counter-example
PURPLE  = "#9A72AC"   # hidden layer / intermediate variable
TEAL    = "#5CD0B3"   # auxiliary concept / data flow
YELLOW  = "#FFFF00"   # rare strong emphasis
GREY_E  = "#222222"   # dark panels / weak background
GREY_D  = "#444444"   # grid / faint outline
GREY    = "#888888"   # connectors / secondary elements
LIGHT   = "#BBBBBB"   # axes / secondary text
WHITE   = "#DDDDDD"   # primary text (not pure white)
```

Texture rules: background `#111111`/`#171717` with faint `GREY_E` panels; text `GREY_A/#DDDDDD`, secondary `GREY_B/#BBBBBB`; connectors `GREY_C/#888888` at 0.35–0.7 alpha; ≤3 strong colors on screen; add subtle glow/stroke to key objects rather than raising saturation.

## Voice generation (VoxCPM2)

```python
from voxcpm import VoxCPM
model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, device="cuda")
wav = model.generate(
    text="<segment under 280 chars>",
    reference_wav_path="<REFERENCE_VOICE_WAV>",  # user supplies their own voice .wav
    cfg_value=2.5,
    inference_timesteps=15,
)
# concatenate segment numpy arrays → voiceover.wav
```

`templates/gen_voice.py` is the ready-to-run, env-driven version. It reads `SEGMENTS` (list of strings), writes `seg_NN.wav` + `voiceover.wav`.

## Adding a new chapter

1. Create `<PROJECT_ROOT>/chNN_topic/` (e.g. `ch03_neural_network/`).
2. Drop in `script.md`, `gen_voice.py` (copy template, set SEGMENTS), `scenes.py` (copy template, build scenes), `assemble.py`.
3. Run `gen_voice.py` in the VoxCPM2 venv.
4. `manim render -qm scenes.py SceneName` per scene.
5. Run `assemble.py` to concatenate.

## Constraints / gotchas

- VoxCPM2 single segment must stay `<280` chars (CUDA OOM otherwise).
- Manim crop filter can't use dynamic `t` (w/h evaluated once at init).
- ffmpeg concat requires `setsar=1` uniform SAR on all fragments.
- Prefer `filter_complex concat` re-encode over stream copy for mixed sources.
- The textbook PDF is **not** shipped in this repo; the user provides it locally.
