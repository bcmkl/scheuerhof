"""
Generiert Soundeffekte für 'Der Fluch von Scheuerhof' via AudioLDM2
(cvssp/audioldm2, über die diffusers-Bibliothek).

Nutzung:
    source .venv/bin/activate
    python generate_sfx.py

Ergebnis: eine .wav-Datei je Eintrag in prompts.SFX, abgelegt in
../../game/audio/sfx/. Anschließend mit convert_to_ogg.sh nach .ogg wandeln.
"""
import time
from pathlib import Path

import scipy.io.wavfile
import torch
from diffusers import AudioLDM2Pipeline

from prompts import SFX

OUT_DIR = Path(__file__).resolve().parents[2] / "game" / "audio" / "sfx"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEVICE = "cpu"  # robuster für unbeaufsichtigten Batch-Lauf, siehe generate_music.py
MODEL_ID = "cvssp/audioldm2"
NUM_INFERENCE_STEPS = 100


def main():
    print(f"Lade {MODEL_ID} ...")
    pipe = AudioLDM2Pipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float32)
    pipe = pipe.to(DEVICE)

    for i, (name, prompt, duration) in enumerate(SFX, 1):
        out_path = OUT_DIR / f"{name}.wav"
        if out_path.exists():
            print(f"[{i}/{len(SFX)}] {name}: existiert bereits, übersprungen")
            continue

        print(f"[{i}/{len(SFX)}] Generiere '{name}' ({duration}s) ...")
        t0 = time.time()
        audio = pipe(
            prompt,
            num_inference_steps=NUM_INFERENCE_STEPS,
            audio_length_in_s=duration,
        ).audios[0]

        scipy.io.wavfile.write(out_path, 16000, audio)
        print(f"    -> {out_path.name} in {time.time() - t0:.1f}s")

    print("SFX-Batch fertig.")


if __name__ == "__main__":
    main()
