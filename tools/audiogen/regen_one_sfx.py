"""
Regeneriert genau eine einzelne SFX-Datei (per Name aus prompts.SFX) neu,
ohne den kompletten Batch anzufassen. Nutzung:

    source .venv-sfx/bin/activate
    python regen_one_sfx.py sfx_forest_night
"""
import sys
from pathlib import Path

import scipy.io.wavfile
import torch
from diffusers import AudioLDM2Pipeline

from prompts import SFX

OUT_DIR = Path(__file__).resolve().parents[2] / "game" / "audio" / "sfx"
DEVICE = "cpu"
MODEL_ID = "cvssp/audioldm2"
NUM_INFERENCE_STEPS = 150

name_to_regen = sys.argv[1]
entry = next((e for e in SFX if e[0] == name_to_regen), None)
if entry is None:
    raise SystemExit(f"Kein Eintrag '{name_to_regen}' in prompts.SFX gefunden.")

name, prompt, duration = entry
print(f"Lade {MODEL_ID} ...")
pipe = AudioLDM2Pipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float32).to(DEVICE)

print(f"Generiere '{name}' ({duration}s) mit Prompt: {prompt!r}")
audio = pipe(prompt, num_inference_steps=NUM_INFERENCE_STEPS, audio_length_in_s=duration).audios[0]

out_path = OUT_DIR / f"{name}.wav"
scipy.io.wavfile.write(out_path, 16000, audio)
print(f"-> {out_path}")
