# Prompt-Liste für die automatische Musik-/SFX-Generierung von
# "Der Fluch von Scheuerhof". Abgeleitet aus den Szenen in
# game/renpy_scheuerhof.rpy (Orte, Stimmung, Tageszeit).
#
# name    -> Dateiname ohne Endung (landet als .ogg in game/audio/music bzw. sfx)
# prompt  -> Text-Prompt für MusicGen / AudioGen (bewusst auf Englisch,
#            die Modelle wurden überwiegend auf englischen Beschreibungen trainiert)
# duration -> Länge in Sekunden

MUSIC = [
    ("theme_bolzplatz_intro", "warm summer evening acoustic guitar with soft ambient pad, nostalgic teenage friendship theme, campfire, crickets in background, gentle melancholy, instrumental, no vocals, loopable", 30),
    ("theme_waldweg_dusk", "unsettling forest ambience at dusk, slow dark drone, creaking branches, wind, rising tension, minor key strings, instrumental, no vocals, loopable", 30),
    ("theme_sanatorium_ruine", "abandoned sanatorium horror ambience, dissonant strings, decayed out of tune piano, distant dripping water, sparse and eerie, instrumental, no vocals, loopable", 30),
    ("theme_kapelle_vision", "dark chapel vision, ghostly choir pads, low organ drone, flickering candle atmosphere, sacred but corrupted, unsettling, instrumental, no vocals, loopable", 30),
    ("theme_krankensaal_vision", "historic hospital ward horror ambience, sparse metallic drone, clinical dread, slow heartbeat pulse underneath, instrumental, no vocals, loopable", 30),
    ("theme_pockenstation", "grim historic plague ward, somber low strings, muffled distant bells, slow oppressive tempo, instrumental, no vocals, loopable", 30),
    ("theme_scheuerhof_real", "old decayed barn and farmhouse theme, rural gothic horror, sparse detuned guitar, ominous low drone, main location theme, instrumental, no vocals, loopable", 30),
    ("theme_grundiss_hof_vision", "early 20th century family farm vision, folk instrumentation, nostalgic but tense undertone, instrumental, no vocals, loopable", 30),
    ("theme_gasthaus_vision", "old countryside inn, faded warmth, nostalgic accordion and piano, bittersweet, slightly haunted, instrumental, no vocals, loopable", 30),
    ("theme_erholungsheim_vision", "recovery home sanatorium vision, gentle but unsettling piano, fragile hope tinged with dread, instrumental, no vocals, loopable", 30),
    ("theme_investoren_verfall", "decayed abandoned investment ruins, hollow industrial drone, ironic decay of greed, cold and empty, instrumental, no vocals, loopable", 30),
    ("theme_archiv_vision", "mystery archive investigation theme, tense minimal strings, subtle rhythmic pulse for suspense, instrumental, no vocals, loopable", 30),
    ("theme_siedlung_vision", "abandoned rural settlement ambience, isolated wind, distant well echo, folk horror undertone, instrumental, no vocals, loopable", 30),
    ("theme_wald_kosmisch", "cosmic surreal forest, ethereal ambient drone, shimmering high tones, dreamlike and otherworldly, instrumental, no vocals, loopable", 30),
    ("theme_epilog_newspaper", "bittersweet resolution theme, quiet piano melody, calm closure after tension, instrumental, no vocals", 30),
    ("theme_epilog_forest", "hopeful forest epilogue, warm strings, gentle resolution, soft nature undertone, instrumental, no vocals", 30),
    ("theme_epilog_shooting_center", "ambiguous dark epilogue, tense unresolved low drone, quiet lingering dread, instrumental, no vocals", 30),
]

SFX = [
    ("sfx_ui_select", "soft short UI click sound, clean and subtle, user interface", 3),
    ("sfx_ui_notification", "soft magical chime notification sound, subtle and short", 3),
    ("sfx_footsteps_gravel", "slow footsteps walking on gravel path outdoors", 4),
    ("sfx_door_creak", "old wooden door creaking open slowly, horror atmosphere", 4),
    ("sfx_wind_gust", "cold eerie wind gust through trees", 5),
    ("sfx_water_drip", "water dripping echo in an abandoned building, horror ambience", 5),
    ("sfx_whisper_ghostly", "faint ghostly unintelligible whisper, horror", 4),
    ("sfx_heartbeat_tense", "slow tense human heartbeat, horror tension build", 5),
    ("sfx_page_turn", "old book page turning, paper rustle, archive room", 3),
    ("sfx_bell_distant", "distant church bell tolling once, muffled and ominous", 4),
    ("sfx_well_echo", "small stone falling into a deep stone well, echo", 4),
    ("sfx_jumpscare_stinger", "sudden sharp dissonant horror orchestral stinger hit", 3),
    ("sfx_campfire_crackle", "campfire crackling, warm outdoor night ambience", 5),
    ("sfx_forest_night", "gentle calm nighttime forest ambience, soft wind through leaves, quiet and smooth, no insects, no hiss, atmospheric", 12),
]
