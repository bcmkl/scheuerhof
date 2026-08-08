# Der Fluch von Scheuerhof

Eine deutschsprachige Ren'Py Visual Novel über den Scheuerhof im Wald von Nohn (Saarland) - ein Mystery-Horror-Coming-of-Age über drei Jugendliche, einen jahrhundertealten Hüter und die reale Geschichte eines Ortes, der seit dem 17. Jahrhundert immer wieder neu genutzt, verkauft und vergessen wurde.

Die Handlung verwebt frei erfundene Ereignisse mit realer Lokalgeschichte des Scheuerhofs (Jesuiten-Gut ab 1643, Zwangsversteigerung 1905, Gasthaus "zur Sommerfrische", Lungensanatorium, Pockenstation, mehrere gescheiterte Investorenprojekte). Namen real belegter Personen und Firmen aus dieser Zeit wurden **aus Pietätsgründen fiktionalisiert**, um keine Persönlichkeitsrechte zu verletzen - reale Orte (Nohn, Wehingen, Bethingen, Tünsdorf, Perl a.d. Mosel) blieben erhalten.

Erhältlich auf Deutsch (Original), Englisch, Französisch und Luxemburgisch.

## Setup

Dieses Repository enthält nur den Projektquellcode - nicht die Ren'Py-Engine selbst.

1. [Ren'Py SDK 8.5.3](https://www.renpy.org/latest.html) herunterladen und neben (oder außerhalb) dieses Repos entpacken.
2. Über den Ren'Py-Launcher dieses Repo-Verzeichnis als Projekt öffnen (es muss einen `game/`-Unterordner enthalten).
3. "Launch Project" zum Testen, "Build & Distribute" zum Erstellen von Distributionen.

Icons (`icon.icns`, `icon.ico`) liegen bereits im Projekt-Root und werden automatisch eingebunden.

## Plattform-Status

Fertige Builds gibt es unter [Releases](../../releases):

- **macOS / Windows** - fertig gebaut, direkt spielbar.
- **Web (HTML5)** - fertig gebaut. Zum Selbst-Hosten den Inhalt der zip auf einen Webserver legen (die progressive-download-Dateien brauchen keinen speziellen Server, ein einfacher statischer Host reicht).
- **Android** - noch nicht gebaut. Braucht einmalig das Android SDK/NDK (über den Ren'Py-Launcher: Android-Reiter → "Install SDK", inkl. Lizenz-Akzeptierung und Signierschlüssel).
- **iOS** - nicht automatisierbar ohne volles Xcode (nicht nur Command Line Tools) und ein Apple-Developer-Konto zum Signieren. Ren'Py erzeugt dafür nur ein Xcode-Projekt (`renios`), das dann manuell in Xcode gebaut/signiert werden muss.

## Audio-Tooling

`tools/audiogen/` enthält die Skripte, mit denen die Hintergrundmusik und Soundeffekte lokal generiert wurden (siehe Abschnitt "Credits & Lizenzen" unten). Die Python-Umgebungen selbst sind nicht Teil des Repos (siehe `.gitignore`); Setup-Hinweise stehen in den Skript-Headern:

- `generate_music.py` - MusicGen (transformers)
- `generate_sfx.py` / `regen_one_sfx.py` - AudioLDM2 (diffusers)
- `convert_to_ogg.sh` - WAV → OGG Vorbis Konvertierung für Ren'Py
- `prompts.py` - alle verwendeten Text-Prompts, editierbar für Neugenerierung

## Credits & Lizenzen

- **Story & Konzept:** Michael Klein, ergänzt mit Unterstützung von Claude Code
- **Programmierung:** umgesetzt mit Unterstützung von Claude Code
- **Bilder:** lokal generiert mit FLUX.2 [klein] (Black Forest Labs)
- **Musik:** lokal generiert mit [MusicGen](https://huggingface.co/facebook/musicgen-small) (Meta, Modellgewichte unter CC-BY-NC 4.0)
- **Soundeffekte:** lokal generiert mit [AudioLDM2](https://huggingface.co/cvssp/audioldm2) (Modellgewichte unter CC-BY-NC-SA 4.0)

**Hinweis zu den KI-Modell-Lizenzen:** MusicGen und AudioLDM2 sind für nicht-kommerzielle Nutzung lizenziert - passend zu diesem Projekt, das als kostenloses Fan-/Hobby-Projekt gedacht ist. Bei einer eventuellen kommerziellen Nutzung müsste die Musik/SFX vorher durch lizenzkonforme Alternativen ersetzt werden. FLUX.2 [klein] existiert in einer 4B-Variante (Apache 2.0, kommerziell nutzbar) und einer 9B-Variante (nicht-kommerzielle Lizenz) - für dieses Projekt spielt das aktuell keine Rolle, da es nicht kommerziell vertrieben wird.

## Lizenz

Der **Code** (Ren'Py-Engine-Struktur, `screens.rpy`, `options.rpy`, die Tooling-Skripte in `tools/audiogen/`) steht unter der MIT-Lizenz, siehe [LICENSE](LICENSE).

Das gilt **nicht** für die kreativen Inhalte: Story, Dialoge, Charaktere und Handlung von "Der Fluch von Scheuerhof" (eingebettet in `game/renpy_scheuerhof.rpy` und die Übersetzungen in `game/tl/`), die Bilder in `game/img/` und `game/gui/`, sowie die Musik/Soundeffekte in `game/audio/`. Diese bleiben © Michael Klein, alle Rechte vorbehalten.
