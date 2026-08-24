# ffmpeg Cookbook

Recipes used by `templates/assemble.py`. All use the system `ffmpeg`/`ffprobe`.

## 1. Get media duration

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 file.mp4
```

## 2. Pad a short clip by holding its last frame (no stutter)

```bash
ffmpeg -y -i src.mp4 -vf "tpad=stop_mode=clone:stop_duration=DELTA,setsar=1" -t TARGET -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p -an out.mp4
```

## 3. Trim a long clip (no slow-mo)

```bash
ffmpeg -y -i src.mp4 -t TARGET -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p -an out.mp4
```

## 4. Blank placeholder (dark canvas) of duration D

```bash
ffmpeg -y -f lavfi -i "color=c=#111111:s=1920x1080:r=30:d=D" -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p -an blank.mp4
```

## 5. Concatenate many clips (re-encode, uniform SAR)

```bash
ffmpeg -y -i c0.mp4 -i c1.mp4 -i c2.mp4 \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]" \
  -map "[outv]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p video_only.mp4
```

> All inputs must have `setsar=1` (uniform Sample Aspect Ratio) or concat desyncs.

## 6. Mux voiceover + video

```bash
ffmpeg -y -i video_only.mp4 -i voiceover.wav -c:v copy -c:a aac -b:a 192k -shortest final.mp4
```

## 7. Verify

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 final.mp4
```

## Gotchas

- `filter_complex concat` re-encodes; use it for mixed sources (never stream-copy when SAR/codecs differ).
- Always `-an` on intermediate clips (audio handled at mux step).
- `tpad` holds the *last* frame — smooth for math diagrams, but avoid on moving content.
