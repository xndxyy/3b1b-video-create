# Production Workflow

End-to-end pipeline for one chapter video. Each step is a concrete action, not a suggestion.

## Phase 0 — Setup (once per machine)

1. Install Manim: `pip install manim` (Community edition).
2. Install VoxCPM2 venv and place `voxcpm/` importable; set `VOXCPM_PATH` in `.env`.
3. Install ffmpeg (on PATH) and Whisper (`pip install openai-whisper` or faster-whisper).
4. (Optional) Install HyperFrames / Remotion for web-style segments.
5. Put your own reference voice `.wav` somewhere local; set `REFERENCE_VOICE_WAV` in `.env`.
6. Obtain the textbook PDF locally; set `TEXTBOOK_PDF` in `.env`.

## Phase 1 — Source extraction

- Read the target chapter from `TEXTBOOK_PDF`.
- List every section, formula, Python snippet, figure, and exercise.
- Mark: mandatory concepts, nice-to-have highlights, likely animation moments.

## Phase 2 — Script (run the skill order, or follow `skill-recipes.md`)

1. **brainstorming** — pick mandatory vs highlight concepts; rough scene list.
2. **writing-fragments** — dump the book's definitions/examples/derivations as raw material.
3. **writing-shape** — turn fragments into prose narration (paragraphs, 50–100 chars each).
4. **humanizer-zh** — remove AI texture; make it sound like a real educator narrating.
5. **manim-video / hyperframes** — adjust rhythm; write animation cues inline as `[动画]` notes.

Output: `script.md`. Must meet the word-count floor in `AGENTS.md`. No bullet lists.

## Phase 3 — Segment & voice

- Split `script.md` narration into segments where each `<280` Chinese characters.
- Put them in `templates/gen_voice.py`'s `SEGMENTS` list.
- Run inside the VoxCPM2 venv:
  ```bash
  python gen_voice.py
  ```
- Produces `seg_NN.wav` + `voiceover.wav` and prints per-segment timing.

## Phase 4 — Animation

- Two routes:
  - **Manim** (`scenes_template.py`): one `Scene` class per beat; render with
    `manim render -qm scenes.py SceneName`; outputs land in `media/videos/.../1080p30/`.
  - **HyperFrames**: author `index.html` composition; `npx hyperframes render`.
- Time each scene to its audio segment duration (from Phase 3 timing log).
- Keep the 3B1B palette from `AGENTS.md`. Dark `#111111` canvas, ≤3 strong colors.

## Phase 5 — Assembly

- `templates/assemble.py` reads `seg_*.wav` durations, maps scenes→segments, pads/trims
  each rendered clip to match audio, concatenates, then muxes `voiceover.wav`.
- Output: `<chapter>_3B1B风格.mp4`.
- Run: `python assemble.py`

## Phase 6 — Verify

- `ffprobe` the final file for duration + stream integrity.
- Spot-check audio/video sync at scene boundaries.
- If a scene is missing, `assemble.py` falls back to a blank `#111111` clip (no crash).

## Checklist before committing

- [ ] No absolute personal paths in any committed file.
- [ ] `.env` and media are git-ignored.
- [ ] `script.md` meets word minimum.
- [ ] Final video plays and is in sync.
