# assets/

Shared, non-private assets for the video project.

Recommended contents (all user-supplied, git-ignored if large):
- `fonts/` — e.g. a CJK font (Microsoft YaHei / Noto Sans CJK) and a mono font (Consolas / JetBrains Mono) for code & formulas.
- `voices/` — **DO NOT COMMIT.** Your reference voice `.wav` goes here locally; it is git-ignored. Point `REFERENCE_VOICE_WAV` in `.env` at it.
- `bgm/` — optional background music ( royalty-free only ).

This folder is intentionally empty in the repo. Populate it on your own machine; nothing here is required to understand the pipeline.
