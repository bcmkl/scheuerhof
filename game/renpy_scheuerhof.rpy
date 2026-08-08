# ============================================================
#   VISUAL NOVEL: DER FLUCH VON SCHEUERHOF — VERSION 0.8
#   Komplettes Script mit erweitertem Jesuiten-Hintergrund
# ============================================================
# ------------------------------------------------------------
# Charaktere
# ------------------------------------------------------------
define l = Character("Lina", color="#c8e6ff")
define k = Character("Kai", color="#ffd27f")
define m = Character("Mira", color="#ffb3c6")
define h = Character("Hüter", color="#d1c4e9")

# ------------------------------------------------------------
# Hintergrundbilder (Szenen)
# ------------------------------------------------------------
# Zuordnung aller im Skript verwendeten "scene"-Namen zu den
# vorhandenen Dateien in img/. "black" ist ein Renpy-Built-in
# und braucht keine eigene Datei.
#
# Wiederverwendete Platzhalter (kein eigenes Artwork vorhanden):
#   - bolzplatz_night_close  -> gleiches Bild wie bolzplatz_night
#   - sanatorium_ruine_close -> gleiches Bild wie sanatorium_ruine
#   - kapelle_vision_dark    -> gleiches Bild wie kapelle_vision
#   - kapelle_zerfall        -> gleiches Bild wie kapelle_vision
#
# Hinweis: Linas Traum (label lina_dream) beschreibt inhaltlich eine
# Kapelle mit Kerzen, nicht den Waldweg - daher nutzt die Szene dort
# "kapelle_vision_dark" statt eines (nicht vorhandenen) Waldweg-Blur-Bilds.
#
# Alle Hintergrundbilder haben unterschiedliche Original-Auflösungen und
# passen nicht 1:1 zur virtuellen Bildschirmgröße (1280x720). bg() skaliert
# jedes Bild automatisch auf volle Bildschirmgröße (mit Beschnitt an den
# Rändern, Seitenverhältnis bleibt erhalten) - kein Bild wird mehr in
# Originalgröße/klein am Bildschirmrand angezeigt.
init python:
    def bg(path):
        return Transform(path, xysize=(config.screen_width, config.screen_height), fit="cover")

    # Eigener Kanal für loopende Umgebungsgeräusche (Lagerfeuer, Wind, Tropfen...),
    # getrennt von "music" (Szenen-Themes) und "sound" (einmalige Stinger).
    renpy.music.register_channel("ambience", mixer="sfx", loop=True)

image bolzplatz_night = bg("img/sportplatz_01.png")
image bolzplatz_night_close = bg("img/sportplatz_01.png")

image waldweg_dusk = bg("img/waldweg_01.png")
image waldweg_dusk_close = bg("img/waldweg_dusk_close.png")

image sanatorium_ruine = bg("img/ruine_01.png")
image sanatorium_ruine_close = bg("img/ruine_01.png")

image kapelle_vision = bg("img/kapelle_01.png")
image kapelle_vision_dark = bg("img/kapelle_01.png")
image kapelle_zerfall = bg("img/kapelle_01.png")

image krankensaal_vision = bg("img/sanatorium_01.png")

image pockenstation = bg("img/pockenstation_01.png")

image scheuerhof_real = bg("img/ruine_01.png")

image grundiss_hof_vision = bg("img/familie_gundiss_01.png")
image gasthaus_sommerfrische_vision = bg("img/gasthaus_01.png")
image erholungsheim_vision = bg("img/erholungsheim_01.png")

# investoren_verfall_vision braucht kein neues Bild - ruine_01.png (verwildertes,
# verfallenes Gebäude) passt inhaltlich schon perfekt zu gescheiterten Investoren.
image investoren_verfall_vision = bg("img/ruine_01.png")

image archiv_vision = bg("img/archiv_01.png")
image siedlung_vision = bg("img/siedlung_vision_01.png")
image siedlung_brunnen = bg("img/siedlung_brunnen_01.png")
image wald_kosmisch = bg("img/wald_kosmisch_01.png")

# Epilog-Enden
image epilog_newspaper = bg("img/epilog01.png")
image epilog_forest = bg("img/epilog_04.png")
image epilog_shooting_center = bg("img/epilog_5.png")

# ------------------------------------------------------------
# Charakterportraits (Emotionen)
# ------------------------------------------------------------
# Werden nur in Szenen eingeblendet, deren Hintergrundbild die
# drei Jugendlichen NICHT bereits selbst zeigt (Visionen, Kapelle,
# Archiv, Siedlung, kosmischer Wald, Ritual). Bei Lagerfeuer,
# Waldweg, Ruine-Außenansicht und den Epilog-Bildern sind Lina,
# Kai und Mira schon Teil der Illustration - dort bleibt es beim
# reinen Hintergrund ohne Portrait-Overlay.
#
# Die Portrait-Dateien sind alle quadratisch (512x512), der Bildschirm ist
# aber 1280x720. char_left/char_center/char_right skalieren jedes Portrait
# einheitlich auf 420x420 und positionieren es überlappungsfrei nebeneinander
# am unteren Bildschirmrand - ersetzen die eingebauten "left"/"center"/"right"
# Transforms, die keine Größenanpassung vornehmen.
transform char_left:
    xanchor 0.0
    xpos 0.02
    yanchor 1.0
    ypos 1.0
    xysize (420, 420)
    fit "contain"

transform char_center:
    xanchor 0.5
    xpos 0.5
    yanchor 1.0
    ypos 1.0
    xysize (420, 420)
    fit "contain"

transform char_right:
    xanchor 1.0
    xpos 0.98
    yanchor 1.0
    ypos 1.0
    xysize (420, 420)
    fit "contain"

image lina neutral = "img/lina_neutral.png"
image lina ruhig = "img/lina_ruhig.png"
image lina nachdenklich = "img/lina_nachdenklich.png"
image lina angespannt = "img/lina_angespannt.png"
image lina entschlossen = "img/lina_entschlossen.png"
image lina erschrocken = "img/lina_erschrocken.png"
image lina fasziniert = "img/lina_fasziniert.png"
image lina hopeful = "img/lina_hopeful.png"
image lina konzentriert = "img/lina_konzentriert.png"
image lina laechelnd = "img/lina_laechelnd.png"
image lina misstrauisch = "img/lina_misstrauisch.png"
image lina muede = "img/lina_muede.png"
image lina nervoes = "img/lina_nervoes.png"
image lina traurig = "img/lina_traurig.png"
image lina ueberrascht = "img/lina_ueberrascht.png"

image kai neutral = "img/kai_neutral.png"
image kai ruhig = "img/kai_ruhig.png"
image kai nachdenklich = "img/kai_nachdenklich.png"
image kai angespannt = "img/kai_angespannt.png"
image kai entschlossen = "img/kai_entschlossen.png"
image kai erschrocken = "img/kai_erschrocken.png"
image kai fasziniert = "img/kai_fasziniert.png"
image kai hopeful = "img/kai_hopeful.png"
image kai konzentriert = "img/kai_konzentriert.png"
image kai laechelnd = "img/kai_laechelnd.png"
image kai misstrauisch = "img/kai_misstrauisch.png"
image kai muede = "img/kai_muede.png"
image kai nervoes = "img/kai_nervoes.png"
image kai traurig = "img/kai_traurig.png"
image kai ueberrascht = "img/kai_ueberrascht.png"

image mira neutral = "img/mira_neutral.png"
image mira ruhig = "img/mira_ruhig.png"
image mira nachdenklich = "img/mira_nachdenklich.png"
image mira angespannt = "img/mira_angespannt.png"
image mira entschlossen = "img/mira_entschlossen.png"
image mira erschrocken = "img/mira_erschrocken.png"
image mira fasziniert = "img/mira_fasziniert.png"
image mira hopeful = "img/mira_hopeful.png"
image mira konzentriert = "img/mira_konzentriert.png"
image mira laechelnd = "img/mira_laechelnd.png"
image mira misstrauisch = "img/mira_misstrauisch.png"
image mira muede = "img/mira_muede.png"
image mira nervoes = "img/mira_nervoes.png"
image mira traurig = "img/mira_traurig.png"
image mira ueberrascht = "img/mira_ueberrascht.png"

# ------------------------------------------------------------
# Globale Variablen & Flags
# ------------------------------------------------------------
default trust_lina = 0
default trust_kai = 0
default trust_mira = 0

default saw_all_visions = False
default confronted_huter = False
default protected_forest = False
default lina_sensitive = False
default kai_burden = False
default mira_chronistin = False

default seen_kai_memory = False
default seen_mira_memory = False
default seen_lina_dream = False

# ------------------------------------------------------------
# Intro
# ------------------------------------------------------------
label start:
    scene bolzplatz_night
    with fade
    play music "audio/music/theme_bolzplatz_intro.ogg" loop fadein 1.0
    play ambience "audio/sfx/sfx_campfire_crackle.ogg"

    "Später Sommerabend am Sportplatz von Nohn. Die Luft ist noch warm, das Gras riecht nach Staub und Grillkohle."

    "Lina, Kai und Mira sitzen am Lagerfeuer, so wie an den meisten Freitagen seit der neunten Klasse."

    m "Halt still, Kai, ich will dich mit der Kamera einfangen, bevor's dunkel und unscharf wird."
    k "Alles an mir sieht komisch aus, Mira. Verschwendete Mühe."
    l "Stimmt nicht. Im Halbdunkel bist du fast erträglich."
    k "Danke. Sehr aufbauend."

    "Mira dreht die Kamera zu Lina. Lina hält die Hand davor."

    l "Nicht mich. Ich seh heute nicht gut aus."
    m "Du siehst nie schlecht aus. Du versteckst dich nur gern."

    "Ein kurzer Blick zwischen den beiden. Nichts Großes. Aber genug, dass es Kai auffällt."

    k "Seit wann sammelst du eigentlich Fotos von uns wie Beweisstücke?"
    m "Seit mir aufgefallen ist, dass sich keiner von euch an irgendwas erinnert, wenn ich's nicht festhalte."

    "Irgendwo bellt ein Hund. Zwei Straßen weiter lacht jemand zu laut über einen Lautsprecher. Ein ganz gewöhnlicher Abend."

    k "Wisst ihr noch, letztes Jahr, als Basti hier eingepennt ist und wir ihm mit Kreide 'ich liebe Montage' auf die Stirn geschrieben haben?"
    l "Das war episch."
    m "Das war fies. Ich hab natürlich Fotos."

    "Sie lachen. Für ein paar Sekunden ist es einfach nur ein guter Abend."

    "Dann knistert das Feuer unruhig auf. Für einen Moment wirken die Schatten der drei etwas länger, als sie sein sollten."

    l "Das Feuer klingt… anders. Als würde es zuhören."
    k "Du klingst wie mein Opa, wenn er über den Scheuerhof geredet hat."

    "Kai lacht kurz auf. Es klingt nicht ganz echt."

    k "Ist im Winter gestorben. Falls ich das noch nicht erwähnt hab."
    m "Kai…"
    k "Passt schon. Du konntest ja nicht fragen, wenn ich's nie gesagt hab."

    "Er wirft ein Stück Holz ins Feuer. Etwas zu hart. Funken stieben hoch."

    k "Bis zum Schluss hat er vom Scheuerhof geredet. Ich dachte, es wären die Medikamente. Jetzt bin ich nicht mehr sicher."

    m "Ich mach ein Foto. Vielleicht sieht man etwas, das wir nicht sehen."

    menu:
        "Wie reagiert Lina?"

        "Sie vertraut ihrem Gefühl.":
            $ trust_lina += 1
            $ lina_sensitive = True
            l "Seit Tagen höre ich ein Flüstern. Nicht laut. Eher wie ein Gedanke, der nicht meiner ist."
        "Sie spielt es runter.":
            l "Schon gut. Ich bin nur müde."

    k "Mein Opa sagte: Der Scheuerhof sei ein Ort, der nie das sein wollte, was Menschen aus ihm gemacht haben."
    m "Meine Oma sprach von einem 'Hüter'. Etwas, das die Jesuiten gebunden haben, bevor man sie vertrieb."

    "Ein Funken springt aus dem Feuer. Für einen Moment sieht Lina darin eine Kutte. Ein Gesicht ohne Augen."

    menu:
        "Erzählt Kai mehr über seinen Opa?"

        "Ja, er öffnet sich.":
            $ trust_kai += 1
            $ kai_burden = True
            jump kai_opa_memory
        "Nein, er bleibt vage.":
            k "Er hat viel gesehen. Zu viel. Er mochte nicht darüber reden."
            jump pfad_der_stille


# ------------------------------------------------------------
# Optionale Vertiefung nach Kapitel 1 — Kai + Opa Rückblende
# ------------------------------------------------------------
label kai_opa_memory:
    scene bolzplatz_night_close
    with dissolve

    k "Er war Sanitäter. Hat Leute gesehen, die hier gearbeitet haben."
    k "Er sagte, nachts habe man Schritte im alten Jesuitenflügel gehört."
    k "Obwohl der seit 1773 nicht mehr existiert. Seit die Jesuiten vertrieben wurden."

    "Kai sieht ins Feuer. Sein Gesicht wirkt älter."

    k "Er hat mir einmal gesagt: 'Der Ort will nicht vergessen werden. Und er straft jeden, der es versucht.'"

    $ seen_kai_memory = True

    jump pfad_der_stille


# ------------------------------------------------------------
# Kapitel 2 — Pfad der Stille
# ------------------------------------------------------------
label pfad_der_stille:
    scene waldweg_dusk
    with fade
    play music "audio/music/theme_waldweg_dusk.ogg" loop fadein 1.0
    play ambience "audio/sfx/sfx_forest_night.ogg"

    "Der Pfad zwischen Nohn und Dreisbach ist alt. Älter als die Dörfer. Älter als die Geschichten."

    m "Hier sollen die Jesuiten ihre Prozessionen gemacht haben. Ein Brunnen, der nie austrocknete."
    k "Mein Opa meinte, der Brunnen sei 'nicht von dieser Welt' gewesen."
    l "Ich spüre etwas. Wie Druck im Kopf. Als würde der Wald mich mustern."

    scene waldweg_dusk_close
    with dissolve

    show lina angespannt at char_left
    show kai angespannt at char_center
    show mira konzentriert at char_right

    k "Hey. Alles okay?"
    l "Keine Ahnung. Es fühlt sich an, als würde mich jemand ansehen. Aber da ist niemand."

    show kai nachdenklich
    k "Wenn's dir zu viel wird, sag's. Wir müssen hier nicht durch."
    show lina hopeful
    l "Nein. Ich will wissen, was das ist. Ich will nicht mehr denken, ich bild mir das nur ein."

    show mira nachdenklich
    m "Du bildest dir gar nichts ein. Ich glaub dir."

    "Kai sagt nichts. Aber er bleibt näher bei Lina als sonst."

    menu:
        "Linas innerer Monolog"

        "Sie hört hin.":
            $ trust_lina += 1
            $ lina_sensitive = True
            show lina fasziniert
            l "Es ist, als würde jemand meinen Namen denken. Nicht sprechen. Denken."
        "Sie verdrängt es.":
            show lina muede
            l "Ich rede mir das ein. Es ist nur Stille."

    show lina angespannt
    show kai angespannt
    show mira angespannt
    "Die Geräusche des Dorfes sind verschwunden. Nur der Wald bleibt."

    jump lina_dream


# ------------------------------------------------------------
# Kapitel 3 — Linas Traum
# ------------------------------------------------------------
label lina_dream:
    scene kapelle_vision_dark
    with dissolve
    play music "audio/music/theme_kapelle_vision.ogg" loop fadein 1.0
    stop ambience fadeout 1.0

    show lina traurig at char_center

    "In der Nacht träumt Lina von einer Kapelle, die nicht existiert."

    "Kerzen. Stein. Ein Mann in einer Kutte. Kein Gesicht. Nur eine Leere, die sie ansieht."

    h "Du hörst mich. Mehr als die anderen."
    show lina nervoes
    l "Wer bist du?"
    h "Ich bin der Wille des Ortes. Der Schatten der Geschichte."

    show lina erschrocken
    play sound "audio/sfx/sfx_whisper_ghostly.ogg"
    "Lina schreckt auf. Der Wald ist still. Aber das Flüstern bleibt."

    hide lina
    with dissolve

    $ seen_lina_dream = True

    jump ruine


# ------------------------------------------------------------
# Kapitel 4 — Ruine des Sanatoriums
# ------------------------------------------------------------
label ruine:
    scene sanatorium_ruine
    with fade
    play music "audio/music/theme_sanatorium_ruine.ogg" loop fadein 1.0
    play ambience "audio/sfx/sfx_water_drip.ogg"

    show lina neutral at char_left
    show kai nachdenklich at char_center
    show mira konzentriert at char_right

    "Der Scheuerhof liegt wie ein verwundetes Tier im Wald. Die Mauern sind überwuchert, aber sie wirken nicht tot."

    "Kai bleibt kurz stehen. Nur eine Sekunde zu lange."

    show kai angespannt
    k "Wir müssen da nicht rein, oder?"
    show mira entschlossen
    m "Wir müssen. Ich hab die Kamera extra für sowas mitgenommen."
    show lina nachdenklich
    l "Seit wann hast du Angst vor altem Gemäuer?"
    show kai nachdenklich
    k "Seit mein Opa gesagt hat, ich soll nie wieder herkommen."

    "Er sagt es wie einen Scherz. Aber er meint es nicht so."

    show kai nachdenklich
    k "Mein Opa hat gesagt, manche Patienten hätten nachts geschrien, weil sie 'den Mann im Habit' gesehen hätten."
    m "Ich mache ein Foto."

    show mira erschrocken
    play sound "audio/sfx/sfx_jumpscare_stinger.ogg"
    "Mira drückt ab. Das Foto zeigt eine Gestalt. Groß. Kutte. Kein Gesicht."

    m "Das… das kann nicht sein."
    show lina ruhig
    l "Doch. Ich habe ihn im Feuer gesehen. Und im Traum."

    show mira nervoes
    "Miras Hände zittern um die Kamera. Sie lässt sie trotzdem nicht los."

    show lina ruhig
    l "Zeig's mir nicht nochmal. Ich glaub dir auch so."

    menu:
        "Wie reagiert Kai?"

        "Er macht einen Witz.":
            show kai laechelnd
            k "Vielleicht ist das nur ein Bug in der Kamera. Oder ein Schatten."
        "Er nimmt es ernst.":
            $ trust_kai += 1
            show kai entschlossen
            k "Das ist der Hüter. Genau so hat mein Opa ihn beschrieben."

    show lina angespannt
    show mira angespannt
    "Die Luft wird schwerer. Der Boden wird warm, als würde etwas darunter atmen."

    menu:
        "Mira erinnert sich an ihre Oma?"

        "Ja, sie erzählt.":
            $ trust_mira += 1
            $ mira_chronistin = True
            jump mira_oma_story
        "Nein, sie schweigt.":
            jump kapelle


# ------------------------------------------------------------
# Kapitel 5 — Mira + Oma Rückblende
# ------------------------------------------------------------
label mira_oma_story:
    scene sanatorium_ruine_close
    with dissolve

    show lina neutral at char_left
    show kai neutral at char_center
    show mira nachdenklich at char_right

    m "Meine Oma war im Ferienheim hier angestellt."
    show mira angespannt
    m "Sie sagte, nachts sei jemand durch die Flure gegangen, obwohl alle Türen abgeschlossen waren."
    show mira nervoes
    m "Sie nannte ihn 'den Mann ohne Augen'."

    show lina ruhig
    l "Deine Oma hat dir das erzählt? Nicht deine Eltern?"
    show mira laechelnd
    m "Meine Eltern reden nicht über sowas. Oma schon. Deshalb hab ich ihr geglaubt."

    "Mira hält die Kamera fester. Ihre Hände zittern."

    show mira traurig
    m "Sie hat mir gesagt: 'Wenn du ihn siehst, dann sieht er dich auch.'"

    show kai nachdenklich
    k "Und du machst trotzdem Fotos."
    show mira entschlossen
    m "Gerade deshalb."

    $ seen_mira_memory = True

    jump kapelle


# ============================================================
#   TEIL 2 — Kapitel 6–10
# ============================================================

# ------------------------------------------------------------
# Kapitel 6 — Erste Kapellen-Vision
# ------------------------------------------------------------
label kapelle:
    scene kapelle_vision
    with fade
    play music "audio/music/theme_kapelle_vision.ogg" loop fadein 1.0
    play sound "audio/sfx/sfx_bell_distant.ogg"

    show lina fasziniert at char_left
    show kai fasziniert at char_center
    show mira fasziniert at char_right

    "Die Jesuiten-Kapelle existiert nicht mehr. Und doch stehen sie darin."

    "Kerzen brennen. Die Luft riecht nach Weihrauch und feuchtem Stein. Die Geometrie des Raumes ist falsch."

    h "Ihr seid nicht die Ersten, die den Pfad der Stille betreten."
    show lina misstrauisch
    l "Wer bist du?"
    h "Ich bin das, was die Jesuiten gebunden haben, als sie vertrieben wurden."

    menu:
        "Wie reagiert Lina?"

        "Sie stellt sich ihm.":
            $ trust_lina += 1
            show lina entschlossen
            l "Warum zeigst du uns das? Was willst du von uns?"
            h "Ich habe Jahrhunderte gewartet. Ich bin müde."
        "Sie schweigt.":
            show lina angespannt
            l "…"
            h "Schweigen ist auch eine Antwort."

    "Die Kapelle flackert. Als wäre sie nur ein Gedanke."

    jump huter_monolog


# ------------------------------------------------------------
# Kapitel 7 — Der Hüter-Monolog (Erste Offenbarung)
# ------------------------------------------------------------
label huter_monolog:
    scene kapelle_vision_dark
    with dissolve

    show lina nachdenklich at char_left
    show kai misstrauisch at char_center
    show mira fasziniert at char_right

    h "Ich bin nicht Mensch. Ich bin nicht Geist. Ich bin Erinnerung."
    h "Ich bin der Wille eines Ortes, der nicht vergessen werden will."

    h "Als die Jesuiten gingen, ließen sie mich zurück. Gebunden. Namenlos."

    menu:
        "Wie reagieren die drei?"

        "Sie hören zu.":
            $ trust_lina += 1
            $ trust_mira += 1
            show lina fasziniert
            l "Wenn du Erinnerung bist… was passiert, wenn niemand mehr von dir weiß?"
            h "Dann werde ich laut."
        "Sie lehnen es ab.":
            show kai entschlossen
            k "Das ist Wahnsinn. Wir halluzinieren."
            h "Ihr könnt gehen. Aber ich bleibe."

    "Die Kapelle beginnt zu zerfallen. Stein wird zu Staub."

    jump krankensaal


# ------------------------------------------------------------
# Kapitel 8 — Krankensaal-Vision
# ------------------------------------------------------------
label krankensaal:
    scene krankensaal_vision
    with fade
    play music "audio/music/theme_krankensaal_vision.ogg" loop fadein 1.0
    play ambience "audio/sfx/sfx_water_drip.ogg"

    show lina angespannt at char_left
    show kai muede at char_center
    show mira nachdenklich at char_right

    play sound "audio/sfx/sfx_whisper_ghostly.ogg"
    "Betten. Schatten. Flüstern. Patienten ohne Gesichter."

    "Ein Arzt spricht mit einer unsichtbaren Gestalt. Seine Stimme ist brüchig."

    "Eine Krankenschwester schreibt in ihr Tagebuch: 'Der Ort will nicht, dass wir hier sind.'"

    m "Meine Oma hat von Nächten erzählt, in denen niemand schlafen konnte."
    k "Mein Opa sagte, der Ort wolle nicht, dass Menschen hier bleiben."

    h "Ich bin nicht der Fluch. Ich bin nur sein Werkzeug. Der Fluch liegt im Boden. In den Steinen. In der Geschichte."

    menu:
        "Konfrontieren sie den Hüter?"

        "Ja, Lina stellt sich ihm.":
            $ confronted_huter = True
            show lina entschlossen
            l "Dann hör auf. Lass den Ort los."
            h "Ich kann nicht. Ich bin gebunden. Aber ihr könnt entscheiden, ob ich allein bleibe."
        "Nein, sie weichen zurück.":
            show lina nervoes
            l "Wir sollten gehen."
            h "Ihr könnt gehen. Aber ihr nehmt mich mit, ob ihr wollt oder nicht."

    jump pockenstation


# ------------------------------------------------------------
# Kapitel 9 — Pockenstation
# ------------------------------------------------------------
label pockenstation:
    scene pockenstation
    with fade
    play music "audio/music/theme_pockenstation.ogg" loop fadein 1.0
    stop ambience fadeout 1.0

    show lina angespannt at char_left
    show kai angespannt at char_center
    show mira konzentriert at char_right

    "Der Betonblock steht kalt und feucht im Wald. Die Stille ist schwer wie Wasser."

    k "Die haben das 1970 gebaut. Für Pockenfälle. Aber eröffnet wurde sie nie - die Pocken waren so gut wie besiegt, bevor der erste Patient herkam."
    h "So steht es in euren Akten. Vielleicht stimmt es sogar."

    show kai misstrauisch
    k "Was soll das heißen?"
    h "Nur, dass ich froh war, als sie die Pläne wieder einstampften. Manche Orte sollten leer bleiben."

    menu:
        "Wie reagiert Mira?"

        "Sie will alles dokumentieren.":
            $ trust_mira += 1
            $ mira_chronistin = True
            show mira entschlossen
            m "Wenn wir deine Geschichte erzählen, bist du nicht mehr allein."
            h "Erzählen ist Macht. Ihr müsst vorsichtig sein, wem ihr sie gebt."
        "Sie hat Angst vor den Bildern.":
            show mira nervoes
            m "Manche Dinge wollen vergessen werden."
            h "Vergessen ist auch eine Entscheidung. Aber ich werde mich wehren."

    show lina erschrocken
    show kai erschrocken
    show mira erschrocken
    "Ein dumpfer Schlag hallt durch den Beton. Niemand weiß, woher er kommt."

    jump archiv


# ------------------------------------------------------------
# Kapitel 10 — Archiv der Jesuiten (Vision)
# ------------------------------------------------------------
label archiv:
    scene archiv_vision
    with fade
    play music "audio/music/theme_archiv_vision.ogg" loop fadein 1.0

    show lina fasziniert at char_left
    show kai konzentriert at char_center
    show mira fasziniert at char_right

    "Ein Archiv, das nie existiert hat. Regale, die sich bewegen. Bücher, die flüstern."

    "Pergamente blättern sich selbst um. Schatten wirken wie Hände."

    h "Die Jesuiten wollten den Ort schützen. Nicht beherrschen."

    h "Ich war ein Wächter. Kein Fluch."

    show lina nachdenklich
    l "Was ist passiert?"
    h "Vergessen. Vergessen ist schlimmer als Tod."

    play sound "audio/sfx/sfx_page_turn.ogg"
    "Ein Buch fällt aus dem Regal. Es öffnet sich. Darin: ein Name."

    show mira ueberrascht
    m "Das ist… dein Name?"
    h "Der Name, den ich hatte, bevor ich gebunden wurde."

    menu:
        "Wer hebt das Buch auf?"

        "Lina.":
            $ trust_lina += 1
            show lina entschlossen
            l "Ich werde dich nicht vergessen."
            h "Dann bin ich nicht allein."
        "Kai.":
            $ trust_kai += 1
            show kai entschlossen
            k "Wenn das hier echt ist… dann müssen wir etwas tun."
            h "Mut ist Erinnerung."
        "Mira.":
            $ trust_mira += 1
            show mira entschlossen
            m "Ich dokumentiere es. Damit es nicht verloren geht."
            h "Du bist meine Chronistin."

    "Das Archiv beginnt zu brennen — aber rückwärts. Die Flammen ziehen sich zurück."

    jump jesuiten_block_1


# ------------------------------------------------------------
# Jesuiten-Block 1 — Vertiefung der historischen Hintergründe
# ------------------------------------------------------------
label jesuiten_block_1:
    scene archiv_vision
    with fade

    show lina nachdenklich at char_left
    show kai nachdenklich at char_center
    show mira nachdenklich at char_right

    "Ein weiteres Buch fällt aus dem Regal. Es öffnet sich selbst, als würde es atmen."

    h "Die Jesuiten kamen nicht als Eroberer. Sie kamen als Heiler."
    h "Sie errichteten eine Kapelle, einen Garten und einen Brunnen, der nie versiegte."

    h "Sie bemerkten Lichter im Wald. Stimmen, die nicht menschlich waren."
    h "Mehrere Mönche träumten denselben Traum — von einer Siedlung, die längst verschwunden war."

    h "Sie schrieben: 'Dieser Ort hat einen Willen.'"

    show mira fasziniert
    m "Aber die Jesuiten waren doch nicht die Ersten hier."
    h "Nein. Vor uns war ein Mann namens Bockenheim. Er hat diesen Hof erst gebaut - 1629, auf brachliegendem Land, das man Scheuren nannte."

    h "Ein Dorf war das einmal. Aber es war schon tot, lange bevor er kam."

    show kai nachdenklich
    k "Und davor?"
    h "Davor war es römisch. Ein Speicher, ein 'Horreum', sagten sie. Daher der Name - Scheuern, Scheuerhof. Getreide, Heu, Proviant. Immer schon ein Ort, an dem man etwas aufbewahrte."

    h "Auch der Name trug das weiter. Ein Heisso von Horreum saß hier im zwölften Jahrhundert. Später ein Pfarrer, Johannes de Horreo. Der Ort hat seinen lateinischen Namen nie ganz losgelassen."

    h "1643 kaufte uns Bockenheims Witwe den Hof ab. Zweitausend Reichstaler und zwei Fuder Wein."

    jump jesuiten_dokument


# ------------------------------------------------------------
# In-Game Jesuiten-Dokument (Chronik-Auszug)
# ------------------------------------------------------------
label jesuiten_dokument:
    scene archiv_vision
    with dissolve

    show lina nachdenklich at char_left
    show kai nachdenklich at char_center
    show mira fasziniert at char_right

    play sound "audio/sfx/sfx_page_turn.ogg"
    "Ein Pergament liegt auf einem Pult. Die Schrift ist alt, aber lesbar."

    "»Anno Domini 1673. Wir, die Brüder der Gesellschaft Jesu, haben am Orte Scheuerhof eine kleine Kapelle errichtet.«"

    "»Der Brunnen spendet Wasser ohne Unterlass. Die Leute sagen, er sei ein Wunder. Wir sagen, er sei ein Zeichen.«"

    "»In den Nächten sehen wir Lichter im Walde. Wir hören Stimmen, die nicht von Menschen stammen.«"

    "»Wir halten fest: Dieser Ort hat einen Willen. Möge Gott uns lehren, ihn zu verstehen.«"

    m "Das ist… eine echte Chronik. Oder etwas, das sich so anfühlt."
    show lina nachdenklich
    l "Es macht alles… schwerer. Aber auch klarer."
    show kai entschlossen
    k "Sie wussten, dass hier etwas ist. Und sie sind trotzdem geblieben."

    jump siedlung


# ============================================================
#   TEIL 3 — Kapitel 11–14 + Enden
# ============================================================

# ------------------------------------------------------------
# Kapitel 11 — Untergegangene Siedlung (Zeitsprung)
# ------------------------------------------------------------
label siedlung:
    scene siedlung_vision
    with fade
    play music "audio/music/theme_siedlung_vision.ogg" loop fadein 1.0

    show lina ueberrascht at char_left
    show kai misstrauisch at char_center
    show mira fasziniert at char_right

    "Die Welt verändert sich. Der Wald wird heller, aber nicht freundlicher."

    "Sie stehen in einer Siedlung, die seit Jahrhunderten nicht mehr existiert."

    "Häuser aus Holz und Stein. Menschen, die sich bewegen, aber nicht sprechen. Als wären sie Erinnerungen, keine Lebenden."

    m "Das ist… das muss der alte Scheuerhof sein. Vor dem Kloster. Vor allem."

    h "Scheuren. So hieß dieser Ort, bevor er einen Hof trug. Ein eigenes Dorf, mit eigenem Bann."

    show kai misstrauisch
    k "Was ist aus ihm geworden?"
    h "Nichts Dramatisches. Kein Feuer, kein Krieg. Es ist einfach... verschwunden. Als die Herzöge hundert Jahre später ihre Steuerlisten zählten, stand Scheuren nicht mehr darauf. Niemand hat aufgeschrieben, warum."

    "Ein Kind bleibt stehen. Es sieht Lina an. Seine Augen sind schwarz wie Tinte."

    show lina erschrocken
    l "Es… es kennt mich."
    k "Das ist unmöglich."

    h "Erinnerungen kennen jeden, der sie berührt."

    "Das Kind hebt die Hand. Es zeigt auf den Brunnen."

    scene siedlung_brunnen
    with dissolve
    play sound "audio/sfx/sfx_well_echo.ogg"

    show lina erschrocken at char_left
    show kai misstrauisch at char_center
    show mira fasziniert at char_right

    "Der Brunnen enthält kein Wasser. Er enthält Licht. Flüssiges Licht."

    show mira nervoes
    m "Das ist nicht natürlich."
    h "Das ist der Ursprung. Der Ort war nie normal. Er war immer wach."

    menu:
        "Wer nähert sich dem Brunnen?"

        "Lina.":
            $ trust_lina += 1
            show lina fasziniert
            l "Ich… ich fühle etwas. Als würde mich jemand rufen."
        "Kai.":
            $ trust_kai += 1
            show kai entschlossen
            k "Wenn das hier echt ist, müssen wir wissen, was es bedeutet."
        "Mira.":
            $ trust_mira += 1
            show mira entschlossen
            m "Ich muss das festhalten. Es ist wichtig."

    "Das Licht pulsiert. Der Brunnen beginnt zu flüstern."

    h "Vergessen hat diese Siedlung getötet. Nicht Krieg. Nicht Krankheit. Vergessen."

    jump wald_wille


# ------------------------------------------------------------
# Kapitel 12 — Wille des Waldes (Kosmischer Horror)
# ------------------------------------------------------------
label wald_wille:
    scene wald_kosmisch
    with fade
    play music "audio/music/theme_wald_kosmisch.ogg" loop fadein 1.0

    show lina angespannt at char_left
    show kai angespannt at char_center
    show mira erschrocken at char_right

    "Der Wald ist nicht mehr der Wald. Die Bäume bewegen sich leicht, als würden sie atmen."

    "Wurzeln wirken wie Adern. Das Licht kommt aus keiner Richtung. Geräusche klingen rückwärts."

    l "Das ist… falsch."
    k "Das ist nicht mehr unser Wald."
    m "Ich… ich glaube, der Wald sieht uns."

    h "Der Wald ist Teil von mir. Teil des Ortes. Teil des Fluchs."

    h "Er will nicht zerstört werden. Er will nicht bebaut werden. Er will nicht vergessen werden."

    menu:
        "Wie reagieren die drei?"

        "Sie hören zu.":
            $ trust_lina += 1
            $ trust_mira += 1
            show lina nachdenklich
            l "Wenn der Wald ein Wille ist… dann ist er nicht böse. Nur… lebendig."
            h "Lebendig genug, um zu leiden."
        "Sie lehnen es ab.":
            show kai misstrauisch
            k "Das ist zu viel. Das ist nicht real."
            h "Real ist, was erinnert wird."

    "Ein Baum neigt sich. Nicht durch Wind. Durch Absicht."

    h "Ihr müsst entscheiden, ob ich allein bleibe."

    jump jesuiten_block_2


# ------------------------------------------------------------
# Jesuiten-Block 2 — Die Nacht der Bindung
# ------------------------------------------------------------
label jesuiten_block_2:
    scene kapelle_vision_dark
    with fade
    play music "audio/music/theme_kapelle_vision.ogg" loop fadein 1.0

    show lina nachdenklich at char_left
    show kai nachdenklich at char_center
    show mira nachdenklich at char_right

    h "Ich war ein Mönch. Pater Amandus Dreisbach."
    h "Ich hörte den Wald. Den Brunnen. Die Siedlung, die längst verschwunden war."

    h "Als die Jesuiten vertrieben wurden, wollten sie mich mitnehmen."
    h "Aber ich war zu tief mit dem Ort verbunden."

    h "Sie banden mich. Nicht mit Ketten. Mit Gebeten. Mit Erinnerung."
    h "Sie ließen mich zurück. Und sie nahmen meinen Namen mit."

    jump ritual_bindung


# ------------------------------------------------------------
# Ritual-Kapitel — Die Bindung als Vision
# ------------------------------------------------------------
label ritual_bindung:
    scene kapelle_zerfall
    with dissolve

    show lina fasziniert at char_left
    show kai fasziniert at char_center
    show mira fasziniert at char_right

    "Die Kapelle ist voll. Jesuiten in dunklen Gewändern. Kerzen flackern. Der Wald drückt gegen die Mauern."

    "Pater Amandus kniet vor dem Altar. Seine Hände zittern."

    "Ein älterer Jesuit spricht: 'Bruder Amandus, du bist der Einzige, der den Ort hört. Wenn wir gehen, bleibt er zurück.'"

    "Amandus flüstert: 'Dann bleibe ich auch.'"

    "Sie legen ihm die Hände auf. Sie sprechen Gebete. Lateinische Worte, die wie Ketten klingen."

    "Der Wald antwortet. Ein dumpfes Grollen. Die Mauern atmen."

    h "Ich habe zugestimmt. Ich habe mich binden lassen. Ich dachte, es sei ein Dienst."

    "Die Kerzen verlöschen. Nur der Brunnen leuchtet."

    "Als die Jesuiten gehen, bleibt Amandus zurück. Allein. Gebunden. Namenlos."

    jump hueter_name


# ------------------------------------------------------------
# Name des Hüters — Offenbarung
# ------------------------------------------------------------
label hueter_name:
    scene archiv_vision
    with dissolve
    play music "audio/music/theme_archiv_vision.ogg" loop fadein 1.0
    play sound "audio/sfx/sfx_page_turn.ogg"

    show lina nachdenklich at char_left
    show kai nachdenklich at char_center
    show mira ueberrascht at char_right

    "Ein Pergament fällt aus dem Regal. Ein Name steht darauf."

    m "Amandus… Dreisbach."
    l "Das ist dein Name."
    h "Es war mein Name. Bevor ich vergessen wurde."

    jump sakularisation


# ------------------------------------------------------------
# Zeitkapsel 0 — Napoleons Säkularisation (1802)
# ------------------------------------------------------------
label sakularisation:
    scene kapelle_zerfall
    with fade
    play music "audio/music/theme_kapelle_vision.ogg" loop fadein 1.0

    show lina fasziniert at char_left
    show kai fasziniert at char_center
    show mira fasziniert at char_right

    "Fast dreißig Jahre sind vergangen. Die Kutten sind verblasst. Der Altar ist nur noch ein Steinhaufen mit Erinnerung."

    h "1802. Napoleons Verwaltung kommt. Sie nennen es Säkularisation."

    "Männer in fremden Uniformen vermessen das Land. Sie sprechen eine Sprache, die der Wald nicht kennt."

    show kai nachdenklich
    k "Aber... die Jesuiten waren doch schon 1773 weg."
    h "Die Jesuiten, ja. Aber die Kirche hatte das Land noch. Ein paar Brüder vom Bistum. Genug, dass hier noch gebetet wurde."

    "Ein Offizier liest ein Dekret vor. Niemand hier versteht jedes Wort. Aber alle verstehen die Bedeutung."

    h "Sie haben den letzten geweihten Stein genommen. Danach war ich nicht mehr Diener einer Kirche. Nur noch... übrig."

    menu:
        "Wie reagiert Mira?"

        "Das erklärt, warum die Kapelle nie wieder aufgebaut wurde.":
            show mira nachdenklich
            m "Das erklärt, warum die Kapelle nie wieder aufgebaut wurde."
            h "Niemand baut etwas wieder auf, das dem Staat gehört. Es wurde verkauft. Wie Ackerland."
        "Wer hat das Land dann bekommen?":
            $ trust_mira += 1
            show mira konzentriert
            m "Wer hat das Land dann bekommen?"
            h "Bauern. Menschen, die nicht wussten, was sie gekauft hatten. Nur, dass es billig war."

    "Der Wald schluckt die letzten lateinischen Worte. Was bleibt, ist nur noch Erde."

    jump hofakte_1905


# ------------------------------------------------------------
# Zeitkapsel 1 — Die Versteigerungsakte (1904/1905)
# ------------------------------------------------------------
# Basiert auf einem realen Zeitungsfund (Versteigerungsanzeige
# "Hofgut Scheuerhof", Perl a.d. Mosel, 29. Mai 1905) sowie einer
# Hofchronik, die den vorausgehenden Großbrand von 1904 belegt. Die
# echten Orte (Nohn, Wehingen, Bethingen, Tünsdorf, Perl a.d. Mosel)
# wurden übernommen, die genannten Personen fiktionalisiert.
label hofakte_1905:
    scene grundiss_hof_vision
    with dissolve
    play music "audio/music/theme_grundiss_hof_vision.ogg" loop fadein 1.0

    show lina nachdenklich at char_left
    show kai nachdenklich at char_center
    show mira fasziniert at char_right

    "Fast ein Jahrhundert vergeht in wenigen Atemzügen. Pächter kommen, Pächter gehen. Namen, die niemand mehr kennt."

    h "Nach der Säkularisation ersteigerte ein Herr Dysing das Land. Seine Tochter heiratete nach Metz. Die Familie de Musiel besaß den Hof über hundert Jahre, ohne je hier zu leben. Nur zur Jagd kamen sie. Sonst verwaltete ihn eine Familie für sie."

    "1904. Ein Feuer frisst sich durch die Wirtschaftsgebäude. Rauch steht tagelang über dem Tal."

    show mira erschrocken
    m "Ein Brand?"
    h "Die Scheunen, die Ställe - alles Asche. Was blieb, war eine Schuld, die niemand zahlen konnte."

    play sound "audio/sfx/sfx_page_turn.ogg"
    "Ein vergilbtes Zeitungsblatt schwebt zwischen den Jahren."

    "»Versteigerung des Hofgutes Scheuerhof.«"

    "»Am Mittwoch, den 7. Juni 1905, vormittags 11 Uhr, werden die sämtlichen, zur Zeit noch zum Hofgut Scheuerhof gehörenden Ländereien — Äcker, Wiesen und Wälder auf den Bännen von Nohn, Wehingen, Bethingen und Tünsdorf — nebst sämtlichen Gebäulichkeiten, bestehend aus großem Wohnhaus, Scheunen, Stallungen und Bering, in der Wirtschaft der Witwe Hoffmann zu Wehingen öffentlich gegen ausgedehnten Zahlungsrückstand versteigert.«"

    "»Wegen Besichtigung wende man sich an Herrn Nikolaus Reiffers in Wehingen. Nähere Auskunft erteilt Herr Heinrich Rausch in Diedenhofen.«"

    "»Perl a.d. Mosel, den 29. Mai 1905. Der Königliche Notar, Franz Duren.«"

    show mira ueberrascht
    m "Das ist… eine echte Versteigerungsakte. Kein Sanatorium. Kein Kloster. Nur ein Hof, der abbrennt und verkauft wird."

    show lina traurig
    l "So fängt es also an. Nicht mit einem Fluch. Mit einem Feuer und einer unbezahlten Rechnung."

    h "Manchmal ist das dasselbe."

    "Erst vier Jahre später, 1909, findet sich endlich ein Käufer, der bleibt."

    "Das Zeitungsblatt löst sich auf wie Rauch. Die Jahreszahlen springen weiter."

    jump gasthaus_sommerfrische


# ------------------------------------------------------------
# Zeitkapsel 2 — Gasthaus zur Sommerfrische (ab 1920)
# ------------------------------------------------------------
label gasthaus_sommerfrische:
    scene gasthaus_sommerfrische_vision
    with dissolve
    play music "audio/music/theme_gasthaus_vision.ogg" loop fadein 1.0

    show lina fasziniert at char_left
    show kai laechelnd at char_center
    show mira fasziniert at char_right

    "1920. Der Hof ist verschwunden. An seiner Stelle: ein gepflegtes Gasthaus. Ein Garten. Eine Voliere voller Vögel."

    h "Nikolaus Berens hat das Land 1909 ersteigert. Aber erst Jahre später macht seine Familie daraus, was ihr hier seht."

    h "Das war die schönste Zeit."

    m "Es sieht... friedlich aus."
    h "Menschen kamen wegen der Stille. Nicht, um sie zu füllen. Nur, um in ihr zu sitzen."

    "Kinder füttern Rehe in einem kleinen Gehege. Ein Kellner trägt Kaffee über den Kiesweg. Irgendwo singt jemand."

    show kai fasziniert
    k "Und du warst... glücklich?"
    h "Ich weiß nicht, ob ich glücklich sein kann. Aber ich war nicht allein. Die Gäste kannten meinen Namen nicht. Aber sie haben den Ort geachtet."

    menu:
        "Was fragt Mira?"

        "Warum ist das vorbei?":
            show mira nachdenklich
            m "Warum ist das vorbei?"
            h "Nichts Gutes bleibt, wenn niemand es festhält. Das habt ihr doch schon gelernt."
        "Hast du ihnen geholfen?":
            $ trust_mira += 1
            show mira fasziniert
            m "Hast du ihnen irgendwie geholfen?"
            h "Ein wenig. Der Brunnen war nie leer. Vielleicht war das kein Zufall."

    "Das Bild verblasst wie eine alte Fotografie, die zu lange in der Sonne lag."

    jump grundiss_hof


# ------------------------------------------------------------
# Zeitkapsel 3 — Familie Grundiss (1933–1949)
# ------------------------------------------------------------
label grundiss_hof:
    scene grundiss_hof_vision
    with fade
    play music "audio/music/theme_grundiss_hof_vision.ogg" loop fadein 1.0

    show lina fasziniert at char_left
    show kai fasziniert at char_center
    show mira fasziniert at char_right

    "1933. Das Gasthaus ist verschwunden. Stattdessen: ein Bauernhof. Hühner. Ein Pflug. Rauch aus einem Schornstein."

    h "Berens hat verkauft. Die Gästezahlen wurden dünner, die Zeiten schlechter. Ein Diplom-Landwirt namens Grundiss übernahm - mit seiner Frau Martha."

    "Ein Mann führt ein Pferd über den Hof. Ein Junge läuft ihm hinterher, ein Holzgewehr in der Hand."

    m "Wer sind die?"
    h "Die Familie Grundiss. Sie haben den Hof bestellt, ohne zu wissen, was unter ihm liegt."

    show kai nachdenklich
    k "Und du? Was hast du gemacht?"
    h "Nichts. Zum ersten Mal seit Langem: nichts. Ich habe zugesehen, wie sie die Erde bestellt haben. Es hat sich... richtig angefühlt."

    "Grundiss wollte den Hof vergrößern, Land von den Wehinger Bauern dazukaufen. Ein neues Gesetz der Machthaber verbot es ihm."

    menu:
        "Wie reagiert Lina auf diese ruhige Seite des Hüters?"

        "Sie ist erleichtert.":
            $ trust_lina += 1
            show lina hopeful
            l "Dann bist du nicht nur... das, was wir in der Kapelle gesehen haben."
            h "Ich bin vieles. Aber am ruhigsten bin ich, wenn niemand versucht, mich zu besitzen oder zu erklären."
        "Sie bleibt misstrauisch.":
            show lina misstrauisch
            l "Oder du hast einfach gewartet."
            h "Vielleicht. Warten kann auch Frieden sein."

    "Krieg kommt über das Land. Der Junge wird älter. Man sieht ihn in Uniform, geht zur Tür hinaus. Der Hof bleibt zurück."

    show mira traurig
    m "Wohin geht er?"
    h "Weg. Die meisten gehen irgendwann weg. Reimar Grundiss wurde Soldat. Er kam nie wirklich zurück."

    "Das Bild wird blasser. Die Jahreszahlen springen vorwärts."

    jump erholungsheim_sanatorium


# ------------------------------------------------------------
# Zeitkapsel 4 — Erholungsheim & Umbau zum Sanatorium (1950/1955)
# ------------------------------------------------------------
label erholungsheim_sanatorium:
    scene erholungsheim_vision
    with dissolve
    play music "audio/music/theme_erholungsheim_vision.ogg" loop fadein 1.0

    show lina nachdenklich at char_left
    show kai nachdenklich at char_center
    show mira ueberrascht at char_right

    "1950. Die Kreissparkasse Saarbrücken übernimmt das Haus als Erholungsheim für ihre Angestellten."

    h "Wieder Menschen, die einfach nur atmen wollten. Ein paar Wochen im Grünen."

    m "Moment. War das... war das nicht das Ferienheim, von dem meine Oma erzählt hat?"
    h "Ja. Ich erinnere mich an sie. Sie hat nie geschrien, als sie mich gespürt hat. Nur genickt. Als würde sie verstehen."

    "Mira sagt nichts. Aber ihre Hand zittert nicht mehr vor Angst. Nur vor Rührung."

    "Fünf Jahre später verändert sich das Haus wieder. Neue Schilder. Weiße Kittel. Betten in Reihen."

    show kai angespannt
    k "Das haben wir schon gesehen."
    h "Ja. Das Lungensanatorium. Ich habe es euch früher gezeigt, bevor ihr wusstet, wer ich bin."

    show lina angespannt
    l "War das der Anfang vom Ende?"
    h "Nein. Der Anfang vom Ende kam später. Als niemand mehr fragte, was hier war. Nur noch, was hier sein könnte."

    jump investoren_verfall


# ------------------------------------------------------------
# Zeitkapsel 5 — Verfall & gescheiterte Investoren (1980er–2000er)
# ------------------------------------------------------------
label investoren_verfall:
    scene investoren_verfall_vision
    with fade
    play music "audio/music/theme_investoren_verfall.ogg" loop fadein 1.0

    show lina angespannt at char_left
    show kai misstrauisch at char_center
    show mira traurig at char_right

    "1980. Das Sanatorium schließt. Die Geräte werden abtransportiert. Der Garten verwildert."

    "1986. Das Land bietet den Komplex zum Kauf an - 8,3 Millionen Mark. Eine Pflegegesellschaft will hier einen Bauernhof für psychisch Kranke einrichten. Ihr Angebot: eine Million. Der Deal platzt."

    h "Dann kamen die Pläne. Jahr für Jahr neue."

    "1988. Ein Hotelkomplex mit Sport- und Erholungszentrum, 250 neue Arbeitsplätze versprochen. Der Gemeinderat diskutiert. Naturschützer protestieren. Am Ende: nichts. 'Der Flop des Jahres', schreibt die Zeitung."

    show kai misstrauisch
    k "Und dann?"
    h "1990. Gerüchte über ein Manager-Zentrum mit Golfplatz. Gleichzeitig Gerüchte über ein Asylbewerberheim. Beides verschwindet wieder, bevor es echt wird."

    "Ein rostiges Bauschild kippt im Wind. 'Ferienanlage Scheuerhof - Eröffnung demnächst' steht darauf. Demnächst war vor zwanzig Jahren."

    menu:
        "Wie reagiert Mira?"

        "Hast du das getan?":
            show mira misstrauisch
            m "Hast du das getan? Sie alle vertrieben?"
            h "Ich habe niemanden vertrieben. Ich habe nur nie etwas gegeben, das sich verkaufen ließ. Das war offenbar genug."
        "Vielleicht war es einfach Pech.":
            show mira nachdenklich
            m "Vielleicht war es einfach Pech. Nicht jedes Projekt scheitert wegen... dir."
            h "Vielleicht. Aber ich habe aufgehört, mir das zu wünschen."

    show lina traurig
    show kai traurig
    show mira traurig
    "Niemand hier wollte je wissen, was der Ort war. Nur, was er werden könnte."

    h "Und jetzt wollt ihr wissen, was er war. Das ist... neu."

    $ saw_all_visions = True

    jump huter_bruch


# ------------------------------------------------------------
# Kapitel 13 — Der Hüter bricht (Tragödie)
# ------------------------------------------------------------
label huter_bruch:
    scene kapelle_zerfall
    with fade
    play music "audio/music/theme_kapelle_vision.ogg" loop fadein 1.0

    show lina traurig at char_left
    show kai traurig at char_center
    show mira traurig at char_right

    "Die Kapelle erscheint erneut. Aber sie zerfällt. Kerzen brennen rückwärts. Schatten lösen sich."

    h "Ihr habt jetzt alles gesehen. Die guten Jahre. Die schlechten. Und das, was übrig bleibt, wenn niemand mehr fragt."

    h "Ich war ein Mönch. Ich hatte einen Namen. Ich hatte ein Leben."

    h "Als die Jesuiten gingen, ließen sie mich zurück. Gebunden. Namenlos. Vergessen."

    l "Du bist… du bist nicht böse."
    h "Ich bin müde."

    "Der Hüter zeigt seine wahre Form. Kein Gesicht. Kein Körper. Nur Erinnerung, die Gestalt angenommen hat."

    h "Ich will nicht vergessen werden."

    menu:
        "Wie reagieren die drei?"

        "Sie versprechen, ihn zu erinnern.":
            $ trust_lina += 1
            $ trust_mira += 1
            show lina entschlossen
            l "Wir werden dich nicht vergessen."
            h "Dann bin ich nicht allein."
        "Sie schweigen.":
            l "…"
            h "Schweigen ist der erste Schritt zum Vergessen."

    jump entscheidung


# ------------------------------------------------------------
# Kapitel 14 — Erweiterte Entscheidung
# ------------------------------------------------------------
label entscheidung:
    scene scheuerhof_real
    with fade
    play music "audio/music/theme_scheuerhof_real.ogg" loop fadein 1.0

    show lina entschlossen at char_left
    show kai entschlossen at char_center
    show mira entschlossen at char_right

    "Sie stehen wieder im realen Scheuerhof. Die Ruine ist still. Der Wald ist wach."

    h "Ihr kennt meine Geschichte. Ihr kennt meinen Namen."
    h "Jetzt müsst ihr entscheiden, ob ich allein bleibe."

    menu:
        "Was tun sie?"

        "Schweigen — den Ort vergessen lassen.":
            jump ending_bad

        "Veröffentlichen — die Welt soll es wissen.":
            jump ending_alternative

        "Bewahren — die Geschichte schützen, den Ort schützen.":
            jump ending_true

        "Verraten — Lina vergisst seinen Namen absichtlich.":
            jump ending_hidden


# ------------------------------------------------------------
# ENDING — Alternative Ending
# ------------------------------------------------------------
label ending_alternative:
    scene epilog_newspaper
    with fade
    play music "audio/music/theme_epilog_newspaper.ogg" loop fadein 1.0
    play sound "audio/sfx/sfx_page_turn.ogg"

    "Ein Zeitungsartikel über das geplante Schießzentrum. Daneben ein Bericht über die Geschichte des Scheuerhofs."

    m "Wir haben alles veröffentlicht. Fotos, Berichte, Aussagen."
    k "Die Leute reden jetzt darüber. Aber sie reden auch über 'Entwicklung'."
    l "Der Hüter ist nicht mehr allein. Aber der Ort ist nicht mehr geschützt."

    "Der Wald flüstert. Nicht wütend. Aber unruhig."

    stop music fadeout 3.0
    stop ambience fadeout 3.0

    scene black
    with Dissolve(2.5)

    pause 1.5

    "ENDE — Die Wahrheit ans Licht"

    pause 2.5

    return


# ------------------------------------------------------------
# ENDING — True Ending
# ------------------------------------------------------------
label ending_true:
    scene epilog_forest
    with fade
    play music "audio/music/theme_epilog_forest.ogg" loop fadein 1.0

    "Kein Schießzentrum. Stattdessen ein kleiner Beitrag über 'geschützte historische Orte'."

    m "Wir haben die Geschichte erzählt. Aber nicht laut. Nur den richtigen Menschen."
    k "Die Gemeinde hat beschlossen, hier nichts mehr zu bauen."
    l "Der Hüter ist nicht mehr allein. Und der Ort bleibt, was er ist."

    if saw_all_visions and confronted_huter and trust_lina >= 2 and trust_mira >= 2 and trust_kai >= 1:
        "Sie haben den Hüter verstanden. Sie haben den Ort geschützt. Das ist das wahre Ende."
    else:
        "Sie haben viel getan. Aber etwas bleibt ungesagt."

    "Der Wald atmet. Zum ersten Mal wirkt er ruhig."

    stop music fadeout 3.0
    stop ambience fadeout 3.0

    scene black
    with Dissolve(2.5)

    pause 1.5

    "ENDE — Der Hüter ist nicht mehr allein"

    pause 2.5

    return


# ------------------------------------------------------------
# ENDING — Bad Ending
# ------------------------------------------------------------
label ending_bad:
    scene epilog_shooting_center
    with fade
    play music "audio/music/theme_epilog_shooting_center.ogg" loop fadein 1.0

    "Ein moderner Jagd- und Freizeitpark am Rand des Waldes. Schießbahnen. Eine Wurftaubenanlage. Ein Hotel mit über hundert Zimmern."

    "Die Waldkron Freizeit GmbH hat investiert - rund 22 Millionen Euro. Geschäftsführer Werner Kalscheuer nennt es einen 'Themenpark für Tourismus, Sport und Jagd'. 160 neue Arbeitsplätze, verspricht die Presse."

    m "Wir hätten etwas tun sollen."
    k "Wir haben nichts getan."
    l "Der Hüter ist allein. Und der Fluch wird sich einen neuen Weg suchen."

    play sound "audio/sfx/sfx_footsteps_gravel.ogg"
    "In der Nacht hört man wieder Schritte im Wald. Stimmen im Beton. Flüstern in den Mauern."

    "Das ist kein Ende. Das ist ein Anfang."

    stop music fadeout 3.0
    stop ambience fadeout 3.0

    scene black
    with Dissolve(2.5)

    pause 1.5

    "ENDE — Ein neuer Anfang"

    pause 2.5

    return


# ------------------------------------------------------------
# ENDING — Hidden Ending (Der Verrat)
# ------------------------------------------------------------
label ending_hidden:
    scene kapelle_vision_dark
    with fade
    play music "audio/music/theme_kapelle_vision.ogg" loop fadein 1.0

    show lina traurig at char_center

    "Die Kapelle erscheint ein letztes Mal. Lina steht allein vor dem Hüter."

    h "Du bist die Einzige, die mich hört."
    show lina entschlossen
    l "Und genau deshalb… muss ich dich vergessen."

    "Der Hüter zerfällt. Nicht in Staub. In Stille."

    "Der Wald verstummt. Der Ort wird normal. Aber etwas fehlt."

    "Lina spürt eine Leere. Als hätte sie einen Teil von sich selbst geopfert."

    "Manchmal ist das Ende eines Fluchs der Beginn einer Leere."

    stop music fadeout 3.0
    stop ambience fadeout 3.0

    scene black
    with Dissolve(2.5)

    pause 1.5

    "ENDE — Der Verrat"

    pause 2.5

    return


# ------------------------------------------------------------
# Optionales Glossar (nicht verlinkt, kann später eingebaut werden)
# ------------------------------------------------------------
label glossar:
    scene black
    with fade
    stop music fadeout 1.0
    stop ambience fadeout 1.0

    "GLOSSAR — BEGRIFFE UND HINTERGRÜNDE"

    "Jesuiten: katholischer Orden, bekannt für Bildung, Seelsorge und Missionsarbeit. Der Orden wurde 1773 päpstlich aufgelöst."
    "Säkularisation: 1802 unter napoleonischer Verwaltung eingezogenes und verkauftes Kirchenland - endgültiges Ende jeder religiösen Nutzung des Scheuerhofs."
    "Scheuerhof: historischer Ort im Wald, genutzt als Siedlung, Kloster, Bauernhof, Gasthaus, Erholungsheim, Sanatorium, Pockenstation."
    "Hüter: gebundene Erinnerung des Ortes, entstanden aus Pater Amandus Dreisbach."
    "Familie Grundiss: bewirtschaftete den Hof im 19. Jahrhundert. Sohn Reimar Grundiss wurde später Oberstleutnant."
    "Gasthaus zur Sommerfrische: ab 1909 betriebenes Erholungsgasthaus mit Park, Voliere und Tiergehege."
    "Erholungsheim der Kreissparkasse Saarbrücken: ab 1950 genutzt als Erholungsheim für Angestellte, ab 1955 zum Lungensanatorium umgebaut."
    "Pockenstation: 1970 errichteter, isolierter Betonbau zur Behandlung von Pockenfällen - wurde nie in Betrieb genommen, heute Ruine im Wald."
    "Pfad der Stille: Weg zwischen Nohn und Dreisbach, aufgeladen mit Geschichte und Ritualen."

    return