#!/usr/bin/env bash
# Wandelt alle generierten .wav-Dateien in game/audio/{music,sfx} nach .ogg
# (Ren'Py-Standardformat) und löscht danach die .wav-Originale.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

for dir in "$ROOT/game/audio/music" "$ROOT/game/audio/sfx"; do
    for wav in "$dir"/*.wav; do
        [ -e "$wav" ] || continue
        ogg="${wav%.wav}.ogg"
        ffmpeg -y -loglevel error -i "$wav" -ac 2 -c:a vorbis -strict -2 -q:a 5 "$ogg"
        rm "$wav"
        echo "-> $(basename "$ogg")"
    done
done
