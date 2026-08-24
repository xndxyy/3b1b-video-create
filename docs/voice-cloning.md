# Voice Cloning — VoxCPM2 (generic)

VoxCPM2 generates natural speech from text using a short reference voice `.wav`. This repo uses it for narration.

## Prerequisites

- A CUDA GPU and the VoxCPM2 package importable (`from voxcpm import VoxCPM`).
- A **reference voice** `.wav` of the speaker you want to clone. This is private — supply it via `.env` (`REFERENCE_VOICE_WAV`). The repo never ships it.

## Core call

```python
import numpy as np, soundfile as sf
from voxcpm import VoxCPM

model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, device="cuda")
sr = model.tts_model.sample_rate

def say(text: str) -> np.ndarray:
    return model.generate(
        text=text,
        reference_wav_path=REFERENCE_VOICE_WAV,
        cfg_value=2.5,
        inference_timesteps=15,
    )

# Long text MUST be split into <280-char segments, generated one at a time,
# then concatenated. Concatenating raw segment arrays avoids cross-segment artifacts.
wavs = [say(seg) for seg in SEGMENTS]
full = np.concatenate(wavs)
sf.write("voiceover.wav", full, sr)
```

## Operational rules

- **<280 chars per segment.** Above this VoxCPM2 OOMs on consumer GPUs.
- **cfg_value 2.5** and **inference_timesteps 15** are good defaults; raise timesteps for quality, lower for speed.
- **Concatenate the numpy arrays**, not the files, then write once.
- Print per-segment durations — `assemble.py` consumes these for scene timing.
- Keep segments at sentence/clause boundaries so the concatenated audio sounds natural.

## Reference implementation

`templates/gen_voice.py` is the ready-to-run, env-driven version. It:
- loads `SEGMENTS` from the chapter config,
- generates each, writes `seg_NN.wav` + `voiceover.wav`,
- prints a cumulative timing table for `assemble.py`.
