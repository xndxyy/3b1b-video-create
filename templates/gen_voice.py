# -*- coding: utf-8 -*-
"""
Voice generation template (VoxCPM2).

Privacy-safe: no hardcoded personal paths. Configure via .env (see .env.example):
  VOXCPM_PATH        — folder containing the voxcpm/ package
  REFERENCE_VOICE_WAV— your own reference voice .wav (never committed)
  DEVICE             — cuda / cpu

Usage:
  1. Fill SEGMENTS with your narration, each < 280 Chinese chars.
  2. Run inside the VoxCPM2 venv:  python gen_voice.py
  3. Produces seg_NN.wav + voiceover.wav and a timing table for assemble.py.
"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import numpy as np
import soundfile as sf
from dotenv import load_dotenv

load_dotenv()

# Make the VoxCPM2 package importable (set VOXCPM_PATH in .env)
VOXCPM_PATH = os.environ.get("VOXCPM_PATH", "")
if VOXCPM_PATH and VOXCPM_PATH not in sys.path:
    sys.path.insert(0, VOXCPM_PATH)

REF_AUDIO = os.environ["REFERENCE_VOICE_WAV"]   # must be set in .env
DEVICE = os.environ.get("DEVICE", "cuda")

# ---------------------------------------------------------------------------
# >>> REPLACE this with your chapter's narration. Each item < 280 Chinese chars.
# >>> Below is a trimmed sample from the Chapter 2 Perceptron video.
SEGMENTS = [
    "我想跟你聊一个挺老的东西。一九五七年。那一年人类第一次让一台机器学会看。",
    "它叫Mark一感知机，一台占满整个房间的庞然大物。电路板上布满了旋钮和电线，看起来更像一台外星设备。",
    "但就是这么个大家伙，做了一件当时所有人都觉得不可思议的事——它能从一堆随机信号里，自己学出规律来。",
    "它背后的数学原理简单到可以写在一张餐巾纸上，而这就是今天所有深度学习、所有大模型、所有AI故事的最底层。感知机。",
    # ... (continue with the rest of your chapter's narration) ...
]
# ---------------------------------------------------------------------------

print(f"Total segments: {len(SEGMENTS)}")
print(f"Total chars: {sum(len(s) for s in SEGMENTS)}")
for i, s in enumerate(SEGMENTS):
    print(f"  [{i+1:2d}] {len(s):3d} chars  {s[:30]}...")

print("\nLoading VoxCPM2...")
from voxcpm import VoxCPM
model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, device=DEVICE)
sr = model.tts_model.sample_rate

all_wavs, all_durs = [], []
for i, text in enumerate(SEGMENTS):
    print(f"\n[{i+1}/{len(SEGMENTS)}] ({len(text)} chars) {text[:35]}...")
    wav = model.generate(
        text=text,
        reference_wav_path=REF_AUDIO,
        cfg_value=2.5,
        inference_timesteps=15,
    )
    all_wavs.append(wav)
    dur = len(wav) / sr
    all_durs.append(dur)
    sf.write(f"seg_{i:02d}.wav", wav, sr)
    print(f"  -> {dur:.2f}s")

full = np.concatenate(all_wavs)
sf.write("voiceover.wav", full, sr)
total = len(full) / sr
print(f"\n=== Done ===\nvoiceover.wav = {total:.2f}s at {sr}Hz")

cum = 0.0
print("Cumulative timing:")
for i, d in enumerate(all_durs):
    cum += d
    print(f"  seg_{i:02d}.wav: {cum-d:6.2f}s -> {cum:6.2f}s  ({d:5.2f}s)")
