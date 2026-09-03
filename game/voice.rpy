# ============================================================
#   SPRACHAUSGABE (deutsch)
# ============================================================
# Die Dialogzeilen sind vollständig vertont. Eingebunden wird das über
# config.auto_voice: Ren'Py sucht zu jeder Say-Zeile eine Datei, die nach
# der Translate-ID der Zeile benannt ist - dieselbe ID, die auch die
# Übersetzungen in game/tl/ verwenden. Im Skript selbst steht deshalb
# kein einziges voice-Statement.
#
# Erzeugt mit tools/voicegen/ (Piper, lokal auf der CPU). Stimmen,
# Sprechtempo und Aussprache-Regeln stehen in tools/voicegen/voices.py,
# die erwarteten Dateinamen ergeben sich aus dem Ren'Py-Dialogexport:
#
#     renpy.sh . dialogue None        -> dialogue.tab
#     python tools/voicegen/generate_voice.py
#     python tools/voicegen/check_voice.py --asr
#
# Fehlt eine Datei, spielt Ren'Py die Zeile einfach stumm ab: 00voice.rpy
# prüft vor dem Abspielen mit renpy.loadable(). Neue oder geänderte
# Dialogzeilen bekommen also eine neue ID und bleiben so lange still, bis
# sie nachgeneriert werden - kaputt geht dabei nichts.

init python:

    # Nur die deutsche Fassung ist vertont. Für die Übersetzungen gäbe es
    # noch keine Sprachdateien; ohne diese Abfrage würde Ren'Py in einer
    # anderen Sprache die deutschen Aufnahmen abspielen.
    #
    # Achtung: Deutsch ist hier nicht "keine Sprache gewählt". Das Projekt
    # setzt config.default_language = "german" (siehe options.rpy), also
    # steht _preferences.language auch im Original auf "german" - eine
    # Abfrage auf None allein würde die Vertonung nie abspielen.
    VERTONTE_SPRACHEN = (None, "german")

    def scheuerhof_auto_voice(tlid):
        if _preferences.language not in VERTONTE_SPRACHEN:
            return None
        return "voice/%s.opus" % tlid

    config.auto_voice = scheuerhof_auto_voice

# Der Sprachlautstärke-Regler wird über config.has_voice in options.rpy
# eingeblendet. Das Absenken der Musik während gesprochener Zeilen macht
# Ren'Py von sich aus (config.emphasize_audio_channels steht dort schon
# auf ["voice"]).
