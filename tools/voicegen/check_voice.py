# -*- coding: utf-8 -*-
"""
Prüft die erzeugte Sprachausgabe von "Der Fluch von Scheuerhof".

    python tools/voicegen/check_voice.py            # Vollständigkeit + Audio
    python tools/voicegen/check_voice.py --diff     # zeigt die Textaufbereitung
    python tools/voicegen/check_voice.py --asr      # Verständlichkeitstest

Drei Prüfebenen:

1. Vollständigkeit - hat jede Dialogzeile aus dialogue.tab eine Datei, und
   gibt es Dateien ohne zugehörige Zeile (verwaiste Reste nach Textänderungen)?

2. Audio-Plausibilität - Länge im Verhältnis zur Zeichenzahl (abgeschnittene
   oder ins Leere gelaufene Synthesen fallen so auf), Stille, Übersteuerung.

3. Verständlichkeit (--asr) - die erzeugten Dateien werden mit Whisper wieder
   in Text zurückverwandelt und mit der Vorlage verglichen. Das misst, ob ein
   Mensch die Zeile verstehen würde, statt nur, ob eine Datei existiert.
   Braucht: pip install faster-whisper
"""
import argparse
import csv
import difflib
import re
import subprocess
import sys
from pathlib import Path

from voices import AUSGABE_FORMAT, SPRECHER, ist_sprechbar, normalisiere

HIER = Path(__file__).resolve().parent
PROJEKT = HIER.parents[1]
VOICE_DIR = PROJEKT / "game" / "audio" / "voice"
DIALOG_DATEI = PROJEKT / "dialogue.tab"

# Sprechtempo-Fenster in Zeichen pro Sekunde. Deutlich darüber heißt meist:
# ein Teil des Textes fehlt. Deutlich darunter: die Synthese hat sich
# irgendwo verhakt und Stille angehängt.
ZEICHEN_PRO_SEK_MIN = 8.0
ZEICHEN_PRO_SEK_MAX = 30.0
MIN_DAUER = 0.4

# Sehr kurze Zeilen ("Kai...", "Wer sind die?") haben anteilig so viel
# Ein- und Ausschwingen, dass die Tempomessung dort nichts aussagt -
# darunter wird nur noch auf Stille und Übersteuerung geprüft.
MIN_ZEICHEN_FUER_TEMPO = 25


def lies_zeilen(pfad):
    with open(pfad, encoding="utf-8") as f:
        for reihe in csv.DictReader(f, delimiter="\t"):
            ident = (reihe.get("Identifier") or "").strip()
            text = (reihe.get("Dialogue") or "").strip()
            if ident and text:
                yield ident, (reihe.get("Character") or "").strip(), text


def ffprobe_dauer(pfad):
    aus = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(pfad)],
        capture_output=True, text=True, check=True,
    )
    return float(aus.stdout.strip())


def lautstaerke(pfad):
    """(mittlere, maximale) Lautstärke in dBFS via ffmpeg volumedetect."""
    aus = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(pfad), "-af", "volumedetect",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    mittel = re.search(r"mean_volume:\s*(-?[\d.]+) dB", aus.stderr)
    maximal = re.search(r"max_volume:\s*(-?[\d.]+) dB", aus.stderr)
    return (float(mittel.group(1)) if mittel else None,
            float(maximal.group(1)) if maximal else None)


def wortfehlerrate(soll, ist):
    """Levenshtein auf Wortebene, normiert - 0.0 = identisch."""
    a = re.findall(r"\w+", soll.lower())
    b = re.findall(r"\w+", ist.lower())
    if not a:
        return 0.0
    zaehler = difflib.SequenceMatcher(a=a, b=b)
    treffer = sum(block.size for block in zaehler.get_matching_blocks())
    return max(0.0, 1.0 - treffer / len(a))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--dialogue", default=str(DIALOG_DATEI))
    ap.add_argument("--voice-dir", default=str(VOICE_DIR))
    ap.add_argument("--diff", action="store_true",
                    help="zeigt, welche Zeilen die Textaufbereitung verändert")
    ap.add_argument("--asr", action="store_true",
                    help="Verständlichkeitstest per Whisper-Rückerkennung")
    ap.add_argument("--asr-modell", default="small",
                    help="Whisper-Modell: tiny/base/small/medium (Standard: small)")
    ap.add_argument("--asr-limit", type=int, default=0,
                    help="nur N zufällige Zeilen zurückerkennen (0 = alle)")
    ap.add_argument("--wer-schwelle", type=float, default=0.25,
                    help="ab dieser Wortfehlerrate gilt eine Zeile als auffällig")
    args = ap.parse_args()

    voice_dir = Path(args.voice_dir)
    zeilen = list(lies_zeilen(Path(args.dialogue)))
    vorhanden = {p.stem: p for p in voice_dir.glob("*." + AUSGABE_FORMAT)}
    probleme = 0

    # --- 1. Vollständigkeit -------------------------------------------------
    stumm = [(i, s, t) for i, s, t in zeilen if not ist_sprechbar(t)]
    stumme_ids = {i for i, _, _ in stumm}
    fehlend = [(i, s, t) for i, s, t in zeilen
               if i not in vorhanden and i not in stumme_ids]
    verwaist = sorted(set(vorhanden) - {i for i, _, _ in zeilen})

    print("=" * 66)
    print("1. VOLLSTÄNDIGKEIT")
    print("=" * 66)
    print("Dialogzeilen: %d | Sprachdateien: %d" % (len(zeilen), len(vorhanden)))
    if fehlend:
        probleme += len(fehlend)
        print("\nOhne Sprachdatei: %d" % len(fehlend))
        for ident, sprecher, text in fehlend[:10]:
            print("  %-22s %-8s %s" % (ident, SPRECHER.get(sprecher, {}).get("name", sprecher), text[:50]))
        if len(fehlend) > 10:
            print("  ... und %d weitere" % (len(fehlend) - 10))
    if verwaist:
        print("\nVerwaiste Dateien (Zeile im Skript geändert/entfernt): %d" % len(verwaist))
        for ident in verwaist[:10]:
            print("  %s" % ident)
    if stumm:
        print("\nAbsichtlich stumm (Zeile ohne Wort, z.B. nur \"...\"): %d" % len(stumm))
        for ident, _, text in stumm:
            print("  %-22s %s" % (ident, text))
    if not fehlend and not verwaist:
        print("\nVollständig, keine verwaisten Dateien.")

    # --- 2. Audio-Plausibilität --------------------------------------------
    print()
    print("=" * 66)
    print("2. AUDIO-PLAUSIBILITÄT")
    print("=" * 66)
    auffaellig = []
    gesamtdauer = 0.0
    for ident, sprecher, text in zeilen:
        pfad = vorhanden.get(ident)
        if not pfad:
            continue
        dauer = ffprobe_dauer(pfad)
        gesamtdauer += dauer
        zeichen = len(normalisiere(text))
        tempo = zeichen / dauer if dauer else 0
        tempo_pruefbar = zeichen >= MIN_ZEICHEN_FUER_TEMPO
        if dauer < MIN_DAUER:
            auffaellig.append((ident, "sehr kurz (%.2fs)" % dauer, text))
        elif tempo_pruefbar and tempo > ZEICHEN_PRO_SEK_MAX:
            auffaellig.append((ident, "zu schnell/unvollständig (%.1f Z/s)" % tempo, text))
        elif tempo_pruefbar and tempo < ZEICHEN_PRO_SEK_MIN:
            auffaellig.append((ident, "auffällig langsam (%.1f Z/s)" % tempo, text))
        else:
            mittel, maximal = lautstaerke(pfad)
            if mittel is not None and mittel < -45:
                auffaellig.append((ident, "nahezu still (%.1f dB)" % mittel, text))
            elif maximal is not None and maximal >= -0.1:
                auffaellig.append((ident, "übersteuert (%.1f dB)" % maximal, text))

    print("Gesamtlaufzeit: %d:%02d min | Ø %.1f s pro Zeile"
          % (gesamtdauer // 60, gesamtdauer % 60,
             gesamtdauer / max(1, len(vorhanden))))
    if auffaellig:
        probleme += len(auffaellig)
        print("\nAuffällig: %d" % len(auffaellig))
        for ident, grund, text in auffaellig[:15]:
            print("  %-22s %-32s %s" % (ident, grund, text[:40]))
    else:
        print("Keine auffälligen Dateien.")

    # --- Textaufbereitung ---------------------------------------------------
    if args.diff:
        print()
        print("=" * 66)
        print("TEXTAUFBEREITUNG (Vorlage -> gesprochen)")
        print("=" * 66)
        geaendert = 0
        for ident, _, text in zeilen:
            neu = normalisiere(text)
            if neu != text.strip():
                geaendert += 1
                print("  %s\n    alt: %s\n    neu: %s" % (ident, text[:90], neu[:90]))
        print("\n%d von %d Zeilen werden vor der Synthese angepasst." % (geaendert, len(zeilen)))

    # --- 3. Verständlichkeit ------------------------------------------------
    if args.asr:
        print()
        print("=" * 66)
        print("3. VERSTÄNDLICHKEIT (Whisper-Rückerkennung)")
        print("=" * 66)
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            sys.exit("faster-whisper fehlt:\n"
                     "  tools/voicegen/.venv/bin/pip install faster-whisper")

        pruefzeilen = [(i, s, t) for i, s, t in zeilen if i in vorhanden]
        if args.asr_limit:
            import random
            random.seed(42)
            pruefzeilen = random.sample(pruefzeilen, min(args.asr_limit, len(pruefzeilen)))

        print("Modell: %s | %d Zeilen\n" % (args.asr_modell, len(pruefzeilen)))
        modell = WhisperModel(args.asr_modell, device="cpu", compute_type="int8")

        raten, schlechte = [], []
        for nr, (ident, sprecher, text) in enumerate(pruefzeilen, 1):
            segmente, _ = modell.transcribe(str(vorhanden[ident]), language="de",
                                            beam_size=5)
            erkannt = " ".join(s.text for s in segmente).strip()
            soll = normalisiere(text)
            wer = wortfehlerrate(soll, erkannt)
            raten.append(wer)
            if wer > args.wer_schwelle:
                schlechte.append((ident, sprecher, wer, soll, erkannt))
            if nr % 25 == 0:
                print("  ... %d/%d geprüft" % (nr, len(pruefzeilen)))

        schnitt = sum(raten) / len(raten) if raten else 0
        print("\nMittlere Wortfehlerrate: %.1f %%  (0 %% = wortgleich erkannt)"
              % (schnitt * 100))
        print("Zeilen über Schwelle (%.0f %%): %d von %d"
              % (args.wer_schwelle * 100, len(schlechte), len(pruefzeilen)))

        # Nach Sprecher aufschlüsseln - so sieht man, ob eine Stimme
        # grundsätzlich schlechter zu verstehen ist als die anderen.
        je_sprecher = {}
        for (_, sprecher, _), wer in zip(pruefzeilen, raten):
            je_sprecher.setdefault(sprecher, []).append(wer)
        print("\nnach Stimme:")
        for sprecher, werte in sorted(je_sprecher.items(),
                                      key=lambda kv: -sum(kv[1]) / max(1, len(kv[1]))):
            print("  %-10s %5.1f %%  (%d Zeilen, Stimme: %s)"
                  % (SPRECHER[sprecher]["name"],
                     100 * sum(werte) / max(1, len(werte)), len(werte),
                     SPRECHER[sprecher]["piper"]))

        if schlechte:
            print("\nAuffällige Zeilen:")
            for ident, sprecher, wer, soll, erkannt in schlechte[:12]:
                print("  %s  %-8s  %.0f %%" % (ident, SPRECHER[sprecher]["name"], wer * 100))
                print("     Vorlage: %s" % soll[:88])
                print("     Erkannt: %s" % erkannt[:88])
        probleme += len(schlechte)

    print()
    print("=" * 66)
    print("Auffälligkeiten insgesamt: %d" % probleme)
    return 0


if __name__ == "__main__":
    sys.exit(main())
