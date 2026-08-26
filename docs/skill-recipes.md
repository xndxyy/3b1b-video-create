# 脚本与动画写作方法

本文件将常用的脚本写作和动画制作方法整理为可直接执行的规则。它们既可手工使用，也可作为 AI 辅助写作时的输入规范。

## khazix-writer (narrative voice)

Persona: "an informed regular person seriously chatting about something that fascinated them." Used for the prose narration tone.

Rules to emulate:
- Open from a **specific, present-moment scene**, never a grand "In today's AI era…" intro.
- Chat rhythm: short and long sentences mixed; commas for spoken pauses; one-line paragraphs for emphasis.
- Use first person freely ("I think", "I got stuck here"). Embrace imperfection.
- No banned constructs: avoid 冒号 `：` → use comma; avoid 破折号 `——`; avoid double quotes `""` → use `「」` or none; avoid "说白了 / 意味着 / 本质上 / 换句话说 / 综上所述".
- No bullet lists for the main body; transition with spoken phrases ("回到这个", "说到这").
- Land a concrete example / persona, then zoom to a larger cultural/philosophical frame at the end.
- Self-check 4 layers: hard rules → style consistency → content depth → "does this sound like a human?".

## brainstorming

Before writing: clarify intent, audience, must-cover concepts, highlights, and a rough scene breakdown. Output a short plan, not prose.

## writing-fragments

Collect heterogeneous raw material: definitions, vignettes, sharp sentences, half-thoughts from the source. Append to a single raw-material doc. Goal = accumulate substance before structure.

## writing-shape

Take the raw material and shape it into an article through a conversational session: draft candidate openings, grow paragraph by paragraph, argue about format (lists/tables/callouts) at each step. Output = connected prose.

## humanizer-zh

Strip AI-writing tells from Chinese text: exaggerated symbolism, promotional language, shallow "-ing" analysis, vague attribution, dash overuse, three-part formulas, AI vocab, negation parallelism, excessive connectors. Rewrite to sound native and natural.

## manim-video

Pipeline for Manim Community math animation (3B1B style). Key moves:
- `Scene` per beat; `self.play(...)` for transforms; `always_redraw` for labels that track objects.
- Use the `3B1B-style-guide.md` palette.
- Render: `manim render -qm scenes.py SceneName` → `media/videos/.../1080p30/`.
- Crop filter can't use dynamic `t`; precompute sizes.
- Time each scene to its audio segment.

## hyperframes

HTML/CSS/JS video composition. Good for title cards, dynamic captions, lower-thirds, transitions, audio-reactive visuals.
- Author `index.html` with `window.__hfSeek`/timeline hooks for deterministic preview/render.
- `npx hyperframes render` to export.
- Use when the segment is web-style rather than pure math.

## Recommended order per chapter

`brainstorming → writing-fragments → writing-shape → humanizer-zh → manim-video (or hyperframes)`
