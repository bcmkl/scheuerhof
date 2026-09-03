# -*- coding: utf-8 -*-
"""
Stimmzuordnung und Textaufbereitung für die deutsche Sprachausgabe von
"Der Fluch von Scheuerhof".

Gleiches Schema wie tools/audiogen/prompts.py: Diese Datei enthält alles,
was man zum Nachjustieren ändern will (Stimmen, Tempo, Aussprache-Regeln),
die eigentliche Generierung steckt in generate_voice.py.

Sprecherkürzel entsprechen den Character-Objekten in game/renpy_scheuerhof.rpy:

    ""  Erzähler (Zeilen ohne Sprecher)
    l   Lina
    k   Kai
    m   Mira
    h   Hüter

Engine: Piper (https://github.com/OHF-Voice/piper1-gpl), lokal auf der CPU,
ONNX-Modelle von HuggingFace. Die deutschen Stimmen stammen aus dem
Thorsten-Voice-Datensatz bzw. den M-AILABS-Sprechern und stehen unter
CC-BY 4.0 bzw. gemeinfreien Lizenzen - anders als die macOS-Systemstimmen
(Backend "say", nur als schneller Vorschau-Fallback gedacht).
"""

# ---------------------------------------------------------------
# Stimmen
# ---------------------------------------------------------------
# Die Zuordnung ist gemessen, nicht geraten. Mit check_voice.py --asr
# (Whisper "small", Wortfehlerrate gegen die Vorlage) ergab sich über alle
# 342 Dateien im Mittel 10,7 %, je Stimme:
#
#   Hüter    (pavoque-low)     7,5 %
#   Kai      (karlsson-low)    8,8 %
#   Erzähler (thorsten-medium) 11,4 %
#   Mira     (eva_k-x_low)     12,0 %
#   Lina     (kerstin-low)     16,5 %
#
# Lina liegt am schlechtesten, ist aber schon die beste verfügbare Option.
# Gegengetestet und verworfen (gleiche 30-39 Zeilen, gleiches Verfahren):
#
#   Lina:     ramona-low 26,0 % / mls-medium 80,0 % gegen kerstin-low 24,9 %
#             (mls ist mehrsprecherfähig; Sprecher 0 ist unbrauchbar)
#   Erzähler: thorsten-high 7,9 % gegen thorsten-medium 7,4 % - das doppelt
#             so große Modell bringt nichts
#   Lina, andere Sprechparameter bei gleichem Modell:
#             1.12/0.55/0.7 -> 21,4 %, 1.05/0.45/0.6 -> 18,4 %
#             gegen die hier eingestellten 1.00/0.667/0.8 -> 17,0 %
#
# Kurze Zeilen ("Kai...") treiben die Rate nach oben, weil der Erkenner
# keinen Kontext hat - als Vergleich zwischen Stimmen taugt sie trotzdem.
# piper        -> Modellname (wird bei Bedarf nach .voices/ geladen)
# length_scale -> Sprechtempo, >1 = langsamer, <1 = schneller
# noise_scale / noise_w_scale -> Variabilität der Betonung
# say          -> macOS-Systemstimme für das Fallback-Backend
# say_rate     -> Wörter pro Minute für das Fallback-Backend

SPRECHER = {
    "": dict(
        name="Erzähler",
        piper="de_DE-thorsten-medium",
        length_scale=1.05,
        noise_scale=0.55,
        noise_w_scale=0.7,
        say="Anna",
        say_rate=170,
    ),
    "l": dict(
        name="Lina",
        piper="de_DE-kerstin-low",
        length_scale=1.0,
        noise_scale=0.667,
        noise_w_scale=0.8,
        say="Sandy",
        say_rate=180,
    ),
    "k": dict(
        name="Kai",
        piper="de_DE-karlsson-low",
        length_scale=0.97,
        noise_scale=0.667,
        noise_w_scale=0.8,
        say="Reed",
        say_rate=185,
    ),
    "m": dict(
        name="Mira",
        piper="de_DE-eva_k-x_low",
        length_scale=1.0,
        noise_scale=0.667,
        noise_w_scale=0.8,
        say="Shelley",
        say_rate=180,
    ),
    "h": dict(
        # Der Hüter spricht langsamer und gleichmäßiger als alle anderen -
        # er ist seit dem 17. Jahrhundert an diesen Ort gebunden.
        name="Hüter",
        piper="de_DE-pavoque-low",
        length_scale=1.22,
        noise_scale=0.5,
        noise_w_scale=0.6,
        say="Grandpa",
        say_rate=140,
    ),
}

# ---------------------------------------------------------------
# Ausgabeformat
# ---------------------------------------------------------------
# Opus mono statt Ogg Vorbis: Sprache ist bei 24 kbit/s in Opus noch klar
# verständlich, das komplette Skript passt so in wenige MB - wichtig für
# den Web-Build (progressive download). Ren'Py und der Web-Build (wasm)
# haben beide einen Opus-Decoder an Bord.
AUSGABE_FORMAT = "opus"
AUSGABE_BITRATE = "24k"
AUSGABE_SAMPLERATE = 24000

# ---------------------------------------------------------------
# Textaufbereitung
# ---------------------------------------------------------------
# Der Phonemizer (espeak-ng) liest manches anders vor, als ein deutscher
# Erzähler es täte. Hier steht, was vor der Synthese ersetzt wird.
# check_voice.py zeigt mit --diff an, welche Zeilen davon betroffen sind.

import re

# Feste Ersetzungen, Reihenfolge zählt. Kleinschreibung beachten!
ERSETZUNGEN = [
    ("…", "..."),
    ("—", " - "),
    ("–", " - "),
    ("»", ""),
    ("«", ""),
    ("„", ""),
    ("“", ""),
    ("”", ""),
    ("Scheuerhof", "Scheuer-Hof"),      # sonst "Scheuerhoff" mit hartem f
    ("Pockenstation", "Pocken-Station"),
    ("Kreissparkasse", "Kreis-Sparkasse"),
    ("Bolzplatz", "Bolz-Platz"),
]

_EINER = ["null", "ein", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun",
          "zehn", "elf", "zwölf", "dreizehn", "vierzehn", "fünfzehn", "sechzehn",
          "siebzehn", "achtzehn", "neunzehn"]
_ZEHNER = ["", "", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig",
           "siebzig", "achtzig", "neunzig"]
_ORDINAL = {
    1: "ersten", 2: "zweiten", 3: "dritten", 4: "vierten", 5: "fünften", 6: "sechsten",
    7: "siebten", 8: "achten", 9: "neunten", 10: "zehnten", 11: "elften", 12: "zwölften",
    13: "dreizehnten", 14: "vierzehnten", 15: "fünfzehnten", 16: "sechzehnten",
    17: "siebzehnten", 18: "achtzehnten", 19: "neunzehnten", 20: "zwanzigsten",
    21: "einundzwanzigsten", 22: "zweiundzwanzigsten", 23: "dreiundzwanzigsten",
    24: "vierundzwanzigsten", 25: "fünfundzwanzigsten", 26: "sechsundzwanzigsten",
    27: "siebenundzwanzigsten", 28: "achtundzwanzigsten", 29: "neunundzwanzigsten",
    30: "dreißigsten", 31: "einunddreißigsten",
}
_MONATE = ("Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|"
           "November|Dezember")


def _zahlwort(n):
    """Deutsche Zahlwörter für 0-999."""
    if n < 20:
        return _EINER[n]
    if n < 100:
        zehner, einer = divmod(n, 10)
        if einer:
            return "%sund%s" % (_EINER[einer], _ZEHNER[zehner])
        return _ZEHNER[zehner]
    hundert, rest = divmod(n, 100)
    wort = ("hundert" if hundert == 1 else _EINER[hundert] + "hundert")
    return wort + (_zahlwort(rest) if rest else "")


def _jahreszahl(n):
    """1773 -> 'siebzehnhundertdreiundsiebzig' statt 'eintausendsiebenhundert...'.

    Deutsche Jahreszahlen bis 1999 werden in Hundertern gesprochen; espeak-ng
    macht daraus sonst die Kardinalzahl, was beim Hören sofort auffällt.
    """
    if 1100 <= n <= 1999:
        hundert, rest = divmod(n, 100)
        wort = _zahlwort(hundert) + "hundert"
        return wort + (_zahlwort(rest) if rest else "")
    if 2000 <= n <= 2099:
        rest = n - 2000
        return "zweitausend" + (_zahlwort(rest) if rest else "")
    return None


def normalisiere(text):
    """Bereitet eine Dialogzeile für die Synthese auf."""
    # Ren'Py-Texttags und Variableneinsetzungen entfernen
    text = re.sub(r"\{[^}]*\}", "", text)
    text = re.sub(r"\[([^\]]*)\]", r"\1", text)

    for alt, neu in ERSETZUNGEN:
        text = text.replace(alt, neu)

    # "den 7. Juni" -> "den siebten Juni"
    def _ordinal(m):
        tag = int(m.group(1))
        return _ORDINAL.get(tag, m.group(1) + ".") + " " + m.group(2)

    text = re.sub(r"\b(\d{1,2})\.\s+(%s)\b" % _MONATE, _ordinal, text)

    # Jahreszahlen ausschreiben
    def _jahr(m):
        wort = _jahreszahl(int(m.group(0)))
        return wort if wort else m.group(0)

    text = re.sub(r"\b\d{4}\b", _jahr, text)

    # VERSALIEN werden sonst teils buchstabiert
    text = re.sub(r"\b[A-ZÄÖÜ]{3,}\b", lambda m: m.group(0).capitalize(), text)

    # Reste aufräumen
    text = text.replace("'", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def ist_sprechbar(text):
    """False für Zeilen, die nach der Aufbereitung kein Wort mehr enthalten.

    Im Skript gibt es Zeilen, die nur aus Auslassungspunkten bestehen - eine
    Figur schweigt. Dafür gibt es bewusst keine Sprachdatei: Ren'Py spielt die
    Zeile dann stumm, was genau das Gewollte ist. (Piper erzeugt für solche
    Eingaben gar keine Audiodaten.)
    """
    return bool(re.search(r"[A-Za-zÄÖÜäöüß]", normalisiere(text)))
