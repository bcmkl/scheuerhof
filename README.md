# Der Fluch von Scheuerhof

Eine deutschsprachige Ren'Py Visual Novel über den Scheuerhof im Wald von Nohn (Saarland) - ein Mystery-Horror-Coming-of-Age über drei Jugendliche, einen jahrhundertealten Hüter und die reale Geschichte eines Ortes, der seit dem 17. Jahrhundert immer wieder neu genutzt, verkauft und vergessen wurde.

Die Handlung verwebt frei erfundene Ereignisse mit realer Lokalgeschichte des Scheuerhofs (Jesuiten-Gut ab 1643, Zwangsversteigerung 1905, Gasthaus "zur Sommerfrische", Lungensanatorium, Pockenstation, mehrere gescheiterte Investorenprojekte). Namen real belegter Personen und Firmen aus dieser Zeit wurden **aus Pietätsgründen fiktionalisiert**, um keine Persönlichkeitsrechte zu verletzen - reale Orte (Nohn, Wehingen, Bethingen, Tünsdorf, Perl a.d. Mosel) blieben erhalten.

Erhältlich auf Deutsch (Original), Englisch, Französisch und Luxemburgisch. Die deutsche Fassung ist vollständig vertont.

## Direkt im Browser spielen

**▶ [Jetzt im Browser spielen](https://bcmkl.github.io/scheuerhof/)** - keine Installation, keine Downloads.

Die Web-Fassung läuft auf GitHub Pages, inklusive der deutschen Sprachausgabe.
Bilder und Ton werden während des Spielens nachgeladen, der erste Bildschirm ist
deshalb schnell da. Wer lieber lokal spielt, findet Windows- und macOS-Pakete
unter [Releases](../../releases).

## Setup

Dieses Repository enthält nur den Projektquellcode - nicht die Ren'Py-Engine selbst.

1. [Ren'Py SDK 8.5.3](https://www.renpy.org/latest.html) herunterladen und neben (oder außerhalb) dieses Repos entpacken.
2. Über den Ren'Py-Launcher dieses Repo-Verzeichnis als Projekt öffnen (es muss einen `game/`-Unterordner enthalten).
3. "Launch Project" zum Testen, "Build & Distribute" zum Erstellen von Distributionen.

Icons (`icon.icns`, `icon.ico`) liegen bereits im Projekt-Root und werden automatisch eingebunden.

## Plattform-Status

Fertige Builds gibt es unter [Releases](../../releases):

- **macOS / Windows** - fertig gebaut, direkt spielbar.
- **Web (HTML5)** - fertig gebaut und unter [bcmkl.github.io/scheuerhof](https://bcmkl.github.io/scheuerhof/) veröffentlicht. Der Build liegt im Branch `gh-pages`; neu erzeugen und hochladen lässt er sich mit `tools/deploy_web_pages.sh <sdk-pfad> --build`. Zum Selbst-Hosten reicht ein einfacher statischer Webserver.
- **Android** - noch nicht gebaut. Braucht einmalig das Android SDK/NDK (über den Ren'Py-Launcher: Android-Reiter → "Install SDK", inkl. Lizenz-Akzeptierung und Signierschlüssel).
- **iOS** - nicht automatisierbar ohne volles Xcode (nicht nur Command Line Tools) und ein Apple-Developer-Konto zum Signieren. Ren'Py erzeugt dafür nur ein Xcode-Projekt (`renios`), das dann manuell in Xcode gebaut/signiert werden muss.

## Audio-Tooling

`tools/audiogen/` enthält die Skripte, mit denen die Hintergrundmusik und Soundeffekte lokal generiert wurden (siehe Abschnitt "Credits & Lizenzen" unten). Die Python-Umgebungen selbst sind nicht Teil des Repos (siehe `.gitignore`); Setup-Hinweise stehen in den Skript-Headern:

- `generate_music.py` - MusicGen (transformers)
- `generate_sfx.py` / `regen_one_sfx.py` - AudioLDM2 (diffusers)
- `convert_to_ogg.sh` - WAV → OGG Vorbis Konvertierung für Ren'Py
- `prompts.py` - alle verwendeten Text-Prompts, editierbar für Neugenerierung
- `soften_sfx.py` - nimmt fertigen Soundeffekten die Schärfe

### Schärfe aus den Soundeffekten nehmen

Die von AudioLDM2 erzeugten Effekte sind auf 16 kHz bandbegrenzt und legen
ihre Energie deshalb oft fast vollständig in den Bereich 2-8 kHz, in dem das
Gehör am empfindlichsten ist. Dazu kommen schmale Kunsttöne des Vokoders
(9 bis 26 Hz breite Sinusspitzen zwischen 4,5 und 6,5 kHz). Beides zusammen
klingt stechend, obwohl der Pegel harmlos aussieht.

```sh
python tools/audiogen/soften_sfx.py --dry-run   # messen und Vorschlag zeigen
python tools/audiogen/soften_sfx.py             # anwenden
```

Das Skript misst jede Datei und leitet die Behandlung daraus ab: Glockenfilter
auf das schärfste Terzband, Notch oder Bandbegrenzung gegen die Kunsttöne,
Spitzenpegel auf höchstens -3 dBFS. Die **Lautheit bleibt erhalten** (RMS ±0 dB),
damit sich die Mischung des Spiels nicht verschiebt - Ausnahme sind die
Dateien, die vorher über 0 dBFS lagen und dadurch leiser werden.

Die Originale liegen unter `tools/audiogen/sfx_original/` (nicht Teil des
Builds, `tools/**` ist in `options.rpy` ausgeschlossen). Ein erneuter Lauf
arbeitet immer auf dieser Sicherung, verarbeitet also nie doppelt.

Ergebnis des bisherigen Laufs: 11 von 14 Effekten behandelt, drei waren
unauffällig. Deutlichste Verbesserungen im Kunstton-Bereich: Türknarren
-14,8 dB, Herzschlag -11,8 dB, UI-Klick -9,0 dB. Der Anteil im Schärfebereich
2-8 kHz sank z.B. beim Herzschlag von 40,5 % auf 11,7 %, beim Türknarren von
29,3 % auf 2,0 %. `sfx_whisper_ghostly` ist ein Sonderfall: Die Datei besteht
praktisch nur aus einem Sinuston bei 2,3 kHz - sie wurde um 7,9 dB leiser
gemacht, sinnvoll reparieren lässt sie sich nur durch Neugenerierung (der
Prompt in `prompts.py` ist dafür bereits überarbeitet).

## Sprachausgabe (deutsch)

Alle 344 Dialogzeilen der deutschen Fassung sind vertont - lokal erzeugt mit
[Piper](https://github.com/OHF-Voice/piper1-gpl) (ONNX, läuft auf der CPU),
je Figur eine eigene Stimme:

| Figur | Stimme | Besonderheit |
| --- | --- | --- |
| Erzähler | `de_DE-thorsten-medium` | ruhiges Grundtempo |
| Lina | `de_DE-kerstin-low` | |
| Kai | `de_DE-karlsson-low` | |
| Mira | `de_DE-eva_k-x_low` | |
| Hüter | `de_DE-pavoque-low` | deutlich langsamer, gleichmäßiger |

Eingebunden ist das über `config.auto_voice` in [game/voice.rpy](game/voice.rpy):
Ren'Py sucht zu jeder Dialogzeile eine Datei, die nach der Translate-ID der
Zeile benannt ist - dieselben IDs, die auch die Übersetzungen in `game/tl/`
verwenden. Im Skript selbst steht deshalb **kein einziges** `voice`-Statement,
und fehlende Dateien führen nicht zum Fehler, sondern nur zu einer stummen
Zeile. Vertont ist nur Deutsch; in den übrigen Sprachen bleibt es still.

Erzeugen und prüfen:

```sh
python3 -m venv tools/voicegen/.venv
tools/voicegen/.venv/bin/pip install piper-tts faster-whisper

/pfad/zum/renpy-8.5.3-sdk/renpy.sh . dialogue None     # dialogue.tab erzeugen
tools/voicegen/.venv/bin/python tools/voicegen/generate_voice.py
tools/voicegen/.venv/bin/python tools/voicegen/check_voice.py --asr
```

- `voices.py` - Stimmzuordnung, Sprechtempo und Aussprache-Regeln. Hier steht
  auch die Textaufbereitung: Jahreszahlen werden ausgeschrieben (1773 →
  "siebzehnhundertdreiundsiebzig" statt der Kardinalzahl), Datumsangaben als
  Ordinalzahl, Ren'Py-Texttags und Versalien entfernt.
- `generate_voice.py` - Synthese, Lautheitsangleichung (EBU R128, -18 LUFS) und
  Ausgabe als Opus mono. Vorhandene Dateien werden übersprungen, neue
  Dialogzeilen also einfach nachgeneriert.
- `check_voice.py` - Prüfung auf drei Ebenen: Vollständigkeit gegen
  `dialogue.tab`, Audio-Plausibilität (Länge im Verhältnis zur Zeichenzahl,
  Stille, Übersteuerung) und mit `--asr` ein echter Verständlichkeitstest:
  Whisper erkennt die erzeugten Dateien wieder in Text zurück, verglichen wird
  über die Wortfehlerrate, aufgeschlüsselt nach Stimme.

Gemessener Stand (`check_voice.py --asr`, Whisper `small`, alle 342 Dateien):
mittlere Wortfehlerrate **10,7 %**, keine Auffälligkeiten bei Länge, Stille oder
Übersteuerung. Je Stimme: Hüter 7,5 %, Kai 8,8 %, Erzähler 11,4 %, Mira 12,0 %,
Lina 16,5 %. Die Rate ist bei sehr kurzen Zeilen ("Kai...", "Das war episch.")
naturgemäß hoch, weil der Erkenner dort keinen Kontext hat - als Vergleichsmaß
zwischen den Stimmen taugt sie trotzdem. Welche Alternativen gegengetestet und
warum verworfen wurden, steht als Kommentar in `tools/voicegen/voices.py`.

Die Sprachdateien liegen als Opus mono (24 kbit/s) in `game/audio/voice/` -
zusammen rund 5 MB für gut 40 Minuten Sprache. Für den Web-Build sind sie in
`progressive_download.txt` als `voice` eingetragen und werden damit erst bei
Bedarf nachgeladen.

**Lizenzhinweis zu den Stimmen:** Der Thorsten-Voice-Datensatz steht unter CC0;
die übrigen vier Stimmen stammen aus dem M-AILABS-Datensatz, der auf
gemeinfreien LibriVox-Aufnahmen beruht. Die genauen Angaben je Stimme stehen in
den Model Cards unter
[huggingface.co/rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices)
und sollten vor einer kommerziellen Nutzung geprüft werden - wie bei Musik und
Soundeffekten ist dieses Projekt als kostenloses Hobbyprojekt gedacht.

## Credits & Lizenzen

- **Story & Konzept:** Michael Klein, ergänzt mit Unterstützung von Claude Code
- **Programmierung:** umgesetzt mit Unterstützung von Claude Code
- **Bilder:** lokal generiert mit FLUX.2 [klein] (Black Forest Labs)
- **Musik:** lokal generiert mit [MusicGen](https://huggingface.co/facebook/musicgen-small) (Meta, Modellgewichte unter CC-BY-NC 4.0)
- **Soundeffekte:** lokal generiert mit [AudioLDM2](https://huggingface.co/cvssp/audioldm2) (Modellgewichte unter CC-BY-NC-SA 4.0)
- **Sprachausgabe:** lokal generiert mit [Piper](https://github.com/OHF-Voice/piper1-gpl) (Stimmen aus Thorsten-Voice und M-AILABS)

**Hinweis zu den KI-Modell-Lizenzen:** MusicGen und AudioLDM2 sind für nicht-kommerzielle Nutzung lizenziert - passend zu diesem Projekt, das als kostenloses Fan-/Hobby-Projekt gedacht ist. Bei einer eventuellen kommerziellen Nutzung müsste die Musik/SFX vorher durch lizenzkonforme Alternativen ersetzt werden. FLUX.2 [klein] existiert in einer 4B-Variante (Apache 2.0, kommerziell nutzbar) und einer 9B-Variante (nicht-kommerzielle Lizenz) - für dieses Projekt spielt das aktuell keine Rolle, da es nicht kommerziell vertrieben wird.

## Lizenz

Der **Code** (Ren'Py-Engine-Struktur, `screens.rpy`, `options.rpy`, die Tooling-Skripte in `tools/audiogen/`) steht unter der MIT-Lizenz, siehe [LICENSE](LICENSE).

Das gilt **nicht** für die kreativen Inhalte: Story, Dialoge, Charaktere und Handlung von "Der Fluch von Scheuerhof" (eingebettet in `game/renpy_scheuerhof.rpy` und die Übersetzungen in `game/tl/`), die Bilder in `game/img/` und `game/gui/`, sowie die Musik/Soundeffekte in `game/audio/`. Diese bleiben © Michael Klein, alle Rechte vorbehalten.
