# -*- coding: utf-8 -*-
"""
Final assembly template (ffmpeg).

Privacy-safe: no hardcoded personal paths. Configure via .env:
  FFMPEG, FFPROBE  — executables (default "ffmpeg"/"ffprobe")
  PROJECT_ROOT     — chapter working directory (where seg_*.wav live)

Behavior:
  - Reads each seg_NN.wav duration via ffprobe.
  - Maps scenes -> segment index ranges (SCENE_SEGMENTS).
  - For each scene, trims/pads the rendered Manim clip to match the audio.
  - Missing animation -> blank #111111 clip (safe fallback).
  - Concatenates all clips, then muxes voiceover.wav.

Usage:
  python assemble.py
"""
import subprocess, os, glob
from dotenv import load_dotenv

load_dotenv()

ROOT = os.environ.get("PROJECT_ROOT", ".")
os.chdir(ROOT)
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
FFPROBE = os.environ.get("FFPROBE", "ffprobe")
MEDIA = os.environ.get("MEDIA_DIR", "media/videos/scenes/1080p30")
FINAL_NAME = os.environ.get("FINAL_NAME", "chapter_3b1b.mp4")

# Scene -> segment index ranges (0-based). Adjust per chapter.
SCENE_SEGMENTS = {
    "S1_ColdOpen":    [0, 1, 2, 3],
    "S2_Bio":         [4, 5, 6, 7],
    "S3_Structure":   [8, 9, 10, 11],
    "S4_Bias":        [12, 13, 14, 15],
    "S5_LogicGates":  [16, 17, 18, 19, 20],
    # ... extend to match your SEGMENTS ...
}

BG = "#111111"


def get_duration(path):
    p = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True,
    )
    return float(p.stdout.strip())


print("=== Reading segment durations ===")
seg_durs = []
max_id = max(max(v) for v in SCENE_SEGMENTS.values())
for i in range(max_id + 1):
    f = f"seg_{i:02d}.wav"
    if os.path.exists(f):
        d = get_duration(f)
        seg_durs.append(d)
        print(f"  {f}: {d:.2f}s")
    else:
        print(f"  {f}: MISSING")
        seg_durs.append(0.0)

print("\n=== Scene MAPPING ===")
MAPPING = []
cum = 0.0
for scene, seg_ids in SCENE_SEGMENTS.items():
    start = cum
    for sid in seg_ids:
        cum += seg_durs[sid]
    end = cum
    MAPPING.append((scene, start, end))
    print(f"  {scene}: {start:.2f}s -> {end:.2f}s  ({end-start:.2f}s)")

total_audio = cum
print(f"\nTotal audio: {total_audio:.2f}s")

print("\n=== Adjusting scene durations ===")
seg_files = []
for i, (scene, a_start, a_end) in enumerate(MAPPING):
    target_dur = a_end - a_start
    src = os.path.join(MEDIA, f"{scene}.mp4")
    out = f"_clip_{i:02d}.mp4"

    if not os.path.exists(src):
        print(f"  [{i}] {scene}: MISSING animation, using blank")
        blank = f"_blank_{i:02d}.mp4"
        subprocess.run([FFMPEG, "-y", "-f", "lavfi",
                        "-i", f"color=c={BG}:s=1920x1080:r=30:d={target_dur}",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                        "-pix_fmt", "yuv420p", "-an", blank], capture_output=True)
        seg_files.append(blank)
        continue

    src_dur = get_duration(src)
    print(f"  [{i}] {scene}: src={src_dur:.1f}s, target={target_dur:.1f}s")
    if abs(src_dur - target_dur) < 0.3:
        cmd = [FFMPEG, "-y", "-i", src, "-t", str(target_dur),
               "-c:v", "libx264", "-preset", "fast", "-crf", "20",
               "-pix_fmt", "yuv420p", "-an", out]
    elif src_dur < target_dur:
        pad = target_dur - src_dur
        vf = f"tpad=stop_mode=clone:stop_duration={pad},setsar=1"
        cmd = [FFMPEG, "-y", "-i", src, "-vf", vf, "-t", str(target_dur),
               "-c:v", "libx264", "-preset", "fast", "-crf", "20",
               "-pix_fmt", "yuv420p", "-an", out]
    else:
        cmd = [FFMPEG, "-y", "-i", src, "-t", str(target_dur),
               "-c:v", "libx264", "-preset", "fast", "-crf", "20",
               "-pix_fmt", "yuv420p", "-an", out]
    subprocess.run(cmd, capture_output=True)
    seg_files.append(out)

print("\n=== Concat ===")
inputs, filter_parts = [], []
for i, f in enumerate(seg_files):
    if not os.path.exists(f):
        blank = f"_blank_{i:02d}.mp4"
        subprocess.run([FFMPEG, "-y", "-f", "lavfi",
                        "-i", f"color=c={BG}:s=1920x1080:r=30:d=2",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", blank],
                       capture_output=True)
        f = blank
    inputs.extend(["-i", f])
    filter_parts.append(f"[{i}:v]")

filter_str = "".join(filter_parts) + f"concat=n={len(seg_files)}:v=1:a=0[outv]"
r = subprocess.run([FFMPEG, "-y"] + inputs + [
    "-filter_complex", filter_str, "-map", "[outv]",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-pix_fmt", "yuv420p", "_video_only.mp4"], capture_output=True)
if r.returncode != 0:
    print(f"  CONCAT ERR: {r.stderr.decode('utf-8','replace')[-300:]}")

print("\n=== Merge audio+video ===")
r = subprocess.run([FFMPEG, "-y",
    "-i", "_video_only.mp4", "-i", "voiceover.wav",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
    FINAL_NAME], capture_output=True)
if r.returncode != 0:
    print(f"  MERGE ERR: {r.stderr.decode('utf-8','replace')[-300:]}")

if os.path.exists(FINAL_NAME) and os.path.getsize(FINAL_NAME) > 1000:
    dur = get_duration(FINAL_NAME)
    sz = os.path.getsize(FINAL_NAME) / 1024 / 1024
    print(f"\nDone! {FINAL_NAME} = {dur:.1f}s, {sz:.1f}MB")
else:
    print("\nERROR: Final file not created")

for f in seg_files + ["_video_only.mp4"] + glob.glob("_blank_*.mp4"):
    if os.path.exists(f):
        os.remove(f)
print("Cleaned up temp files")
