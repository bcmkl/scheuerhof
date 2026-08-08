"""
Generiert Hintergrundmusik für 'Der Fluch von Scheuerhof' via MusicGen
(facebook/musicgen-small, über die transformers-Bibliothek).

Nutzung:
    source .venv/bin/activate
    python generate_music.py

Ergebnis: eine .wav-Datei je Eintrag in prompts.MUSIC, abgelegt in
../../game/audio/music/. Anschließend mit convert_to_ogg.sh nach .ogg wandeln.
"""
import time
from pathlib import Path

import scipy.io.wavfile
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

from prompts import MUSIC

OUT_DIR = Path(__file__).resolve().parents[2] / "game" / "audio" / "music"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# CPU statt MPS: robuster für einen langen unbeaufsichtigten Batch-Lauf.
# MPS ist bei manchen Operationen in älteren torch-Versionen lückenhaft
# und würde den Batch mitten im Lauf abbrechen.
DEVICE = "cpu"
MODEL_ID = "facebook/musicgen-small"
TOKENS_PER_SECOND = 50  # Framerate des MusicGen-Codebooks


def main():
    print(f"Lade {MODEL_ID} ...")
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = MusicgenForConditionalGeneration.from_pretrained(MODEL_ID).to(DEVICE)
    sampling_rate = model.config.audio_encoder.sampling_rate

    for i, (name, prompt, duration) in enumerate(MUSIC, 1):
        out_path = OUT_DIR / f"{name}.wav"
        if out_path.exists():
            print(f"[{i}/{len(MUSIC)}] {name}: existiert bereits, übersprungen")
            continue

        print(f"[{i}/{len(MUSIC)}] Generiere '{name}' ({duration}s) ...")
        t0 = time.time()
        inputs = processor(text=[prompt], padding=True, return_tensors="pt").to(DEVICE)
        max_new_tokens = int(duration * TOKENS_PER_SECOND)
        with torch.no_grad():
            audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, guidance_scale=3.0)

        audio = audio_values[0, 0].cpu().numpy()
        scipy.io.wavfile.write(out_path, sampling_rate, audio)
        print(f"    -> {out_path.name} in {time.time() - t0:.1f}s")

    print("Musik-Batch fertig.")


if __name__ == "__main__":
    main()
