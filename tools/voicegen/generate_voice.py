# -*- coding: utf-8 -*-
"""
Erzeugt die deutsche Sprachausgabe für "Der Fluch von Scheuerhof".

Nutzung:
    # 1. Zeilenliste aus Ren'Py exportieren (schreibt dialogue.tab ins Projekt):
    /pfad/zum/renpy-8.5.3-sdk/renpy.sh . dialogue None

    # 2. Stimmen erzeugen (Piper lädt fehlende Modelle selbst nach):
    source tools/voicegen/.venv/bin/activate
    python tools/voicegen/generate_voice.py

Ergebnis: je Dialogzeile eine Datei game/audio/voice/<translate-id>.opus.
Ren'Py bindet sie über config.auto_voice in game/voice.rpy automatisch ein -
im Skript selbst muss dafür keine einzige Zeile geändert werden.

Setup des venv (einmalig):
    python3 -m venv tools/voicegen/.venv
    tools/voicegen/.venv/bin/pip install piper-tts

Backends:
    piper (Standard) - lokale ONNX-Modelle, CC-BY-lizenzierte deutsche Stimmen
    say              - macOS-Systemstimmen, ohne Installation, nur als schnelle
                       Vorschau gedacht (Apple-Stimmen sind nicht zur
                       Weitergabe in eigenen Produkten lizenziert)

Stimmzuordnung, Tempo und Aussprache-Regeln stehen in voices.py.
"""
import argparse
import csv
import os
import shutil
import subprocess
import sys
import tempfile
import time
import wave
from pathlib import Path

from voices import (
    AUSGABE_BITRATE,
    AUSGABE_FORMAT,
    AUSGABE_SAMPLERATE,
    SPRECHER,
    ist_sprechbar,
    normalisiere,
)

HIER = Path(__file__).resolve().parent
PROJEKT = HIER.parents[1]
OUT_DIR = PROJEKT / "game" / "audio" / "voice"
MODELL_DIR = HIER / ".voices"
DIALOG_DATEI = PROJEKT / "dialogue.tab"


def lies_zeilen(pfad):
    """Liest den Ren'Py-Dialogexport: Identifier, Sprecher, Text."""
    with open(pfad, encoding="utf-8") as f:
        for reihe in csv.DictReader(f, delimiter="\t"):
            ident = (reihe.get("Identifier") or "").strip()
            sprecher = (reihe.get("Character") or "").strip()
            text = (reihe.get("Dialogue") or "").strip()
            if ident and text:
                yield ident, sprecher, text


def nach_opus(wav_pfad, ziel):
    """WAV -> Opus mono, auf einheitliche Lautheit gebracht.

    loudnorm (EBU R128) macht zweierlei: Es gleicht die fünf Stimmmodelle
    aneinander an - die haben von Haus aus deutlich unterschiedliche Pegel -
    und lässt 1,5 dB Luft nach oben. Ohne diesen Kopfraum liefert Piper
    Dateien mit Spitzen bei 0 dBFS, die der Opus-Encoder übersteuert.
    """
    ziel.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(wav_pfad),
            "-af", "loudnorm=I=-18:TP=-1.5:LRA=11",
            "-ac", "1",
            "-ar", str(AUSGABE_SAMPLERATE),
            "-c:a", "libopus",
            "-b:a", AUSGABE_BITRATE,
            str(ziel),
        ],
        check=True,
    )


class PiperBackend:
    """Lädt je Sprecher ein Modell, einmal, und behält es im Speicher."""

    name = "piper"

    def __init__(self):
        from piper import PiperVoice, SynthesisConfig

        self._PiperVoice = PiperVoice
        self._SynthesisConfig = SynthesisConfig
        self._geladen = {}
        MODELL_DIR.mkdir(parents=True, exist_ok=True)

    def _voice(self, kuerzel):
        if kuerzel not in self._geladen:
            modell = SPRECHER[kuerzel]["piper"]
            pfad = MODELL_DIR / (modell + ".onnx")
            if not pfad.exists():
                print("  lade Modell %s ..." % modell)
                subprocess.run(
                    [sys.executable, "-m", "piper.download_voices", modell,
                     "--data-dir", str(MODELL_DIR)],
                    check=True,
                )
            self._geladen[kuerzel] = self._PiperVoice.load(str(pfad))
        return self._geladen[kuerzel]

    def synthese(self, kuerzel, text, wav_pfad):
        cfg = SPRECHER[kuerzel]
        syn = self._SynthesisConfig(
            length_scale=cfg.get("length_scale"),
            noise_scale=cfg.get("noise_scale"),
            noise_w_scale=cfg.get("noise_w_scale"),
        )
        with wave.open(str(wav_pfad), "wb") as f:
            self._voice(kuerzel).synthesize_wav(text, f, syn_config=syn)


class SayBackend:
    """macOS-Systemstimmen - keine Installation, aber nur für Vorschauen."""

    name = "say"

    def synthese(self, kuerzel, text, wav_pfad):
        cfg = SPRECHER[kuerzel]
        aiff = wav_pfad.with_suffix(".aiff")
        subprocess.run(
            ["say", "-v", cfg["say"], "-r", str(cfg["say_rate"]),
             "-o", str(aiff), text],
            check=True,
        )
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(aiff), str(wav_pfad)],
            check=True,
        )
        aiff.unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--backend", choices=["piper", "say"], default="piper")
    ap.add_argument("--dialogue", default=str(DIALOG_DATEI),
                    help="Pfad zur dialogue.tab aus dem Ren'Py-Export")
    ap.add_argument("--out", default=str(OUT_DIR))
    ap.add_argument("--limit", type=int, default=0,
                    help="nur die ersten N Zeilen (für Probeläufe)")
    ap.add_argument("--speaker", action="append", default=None,
                    help="nur diese Sprecherkürzel, z.B. --speaker h "
                         "(Erzähler ist das leere Kürzel: --speaker '')")
    ap.add_argument("--force", action="store_true",
                    help="vorhandene Dateien überschreiben")
    args = ap.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg fehlt - z.B. mit 'brew install ffmpeg' nachinstallieren.")

    dialog = Path(args.dialogue)
    if not dialog.exists():
        sys.exit("%s fehlt. Erst exportieren:\n"
                 "  renpy.sh . dialogue None" % dialog)

    out = Path(args.out)
    zeilen = list(lies_zeilen(dialog))
    if args.speaker is not None:
        zeilen = [z for z in zeilen if z[1] in args.speaker]
    if args.limit:
        zeilen = zeilen[: args.limit]

    unbekannt = sorted({s for _, s, _ in zeilen if s not in SPRECHER})
    if unbekannt:
        sys.exit("Unbekannte Sprecherkürzel in dialogue.tab: %s\n"
                 "In voices.py ergänzen." % ", ".join(repr(u) for u in unbekannt))

    backend = PiperBackend() if args.backend == "piper" else SayBackend()
    print("Backend: %s | %d Zeilen | Ziel: %s"
          % (backend.name, len(zeilen), out))

    erzeugt = uebersprungen = stumm = 0
    start = time.time()

    with tempfile.TemporaryDirectory() as tmp:
        wav_pfad = Path(tmp) / "zeile.wav"

        for i, (ident, sprecher, text) in enumerate(zeilen, 1):
            ziel = out / ("%s.%s" % (ident, AUSGABE_FORMAT))
            if ziel.exists() and not args.force:
                uebersprungen += 1
                continue

            if not ist_sprechbar(text):
                # Zeile ohne Wort (z.B. nur "..."): bleibt absichtlich stumm.
                stumm += 1
                continue

            gesprochen = normalisiere(text)

            backend.synthese(sprecher, gesprochen, wav_pfad)
            nach_opus(wav_pfad, ziel)
            erzeugt += 1

            print("[%3d/%3d] %-8s %s%s"
                  % (i, len(zeilen), SPRECHER[sprecher]["name"],
                     gesprochen[:58], "..." if len(gesprochen) > 58 else ""))

    dauer = time.time() - start
    groesse = sum(p.stat().st_size for p in out.glob("*." + AUSGABE_FORMAT))
    print("\nFertig: %d erzeugt, %d schon vorhanden, %d absichtlich stumm, %.1fs"
          % (erzeugt, uebersprungen, stumm, dauer))
    print("Bestand: %d Dateien, %.1f MB in %s"
          % (len(list(out.glob("*." + AUSGABE_FORMAT))), groesse / 1e6, out))
    print("\nPrüfen mit: python tools/voicegen/check_voice.py")


if __name__ == "__main__":
    main()
