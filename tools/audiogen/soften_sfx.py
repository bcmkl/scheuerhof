# -*- coding: utf-8 -*-
"""
Entschärft schrille Soundeffekte von "Der Fluch von Scheuerhof".

    python tools/audiogen/soften_sfx.py --dry-run    # nur messen und vorschlagen
    python tools/audiogen/soften_sfx.py              # anwenden

Hintergrund: Die SFX stammen aus AudioLDM2 und sind bandbegrenzt (oberhalb
von rund 7 kHz ist nichts mehr). Ihre Energie sitzt dadurch oft fast
vollständig im Bereich 2-8 kHz - genau dort, wo das Gehör am
empfindlichsten ist. Das klingt dünn und stechend, obwohl der Pegel
harmlos aussieht. Zwei Dateien lagen zusätzlich über 0 dBFS.

Dazu kommt ein zweites, hörbareres Problem: Der Vokoder von AudioLDM2 legt
in viele Dateien einen schmalen Dauerton um 6,25 kHz, der 36 bis 42 dB über
seiner Umgebung steht - bei den Endlosschleifen (Waldnacht, Lagerfeuer)
pfeift der die ganze Zeit mit. Solche Töne werden gezielt ausgenotcht.

Nur oberhalb von 4,5 kHz: Darunter sind schmale Spitzen meist gewollt - die
Glocke in sfx_bell_distant hat dort ihre Obertöne, und die soll sie behalten.

Was das Skript macht, je Datei aus der Messung abgeleitet:

0. Schmale Störtöne über 4,5 kHz mit hoher Güte absenken. Treten drei oder
   mehr davon als Kamm auf - typisch für den Vokoder -, wird stattdessen das
   ganze Band darüber abgeschnitten: Bei einem Herzschlag oder einem
   Flüstern steht dort kein Nutzsignal, das man erhalten müsste. Wo die
   Grenze liegt, bestimmt die Datei selbst (99 % ihrer Energie bleiben
   erhalten), nicht ein fester Wert.

1. Glockenfilter auf das lauteste Terzband zwischen 2 und 8 kHz. Das nimmt
   dem Klang die Spitze, ohne ihn dumpf zu machen.
2. Sanftes Höhenband ab 5 kHz absenken, wenn dort überdurchschnittlich viel
   Energie liegt.
3. Tiefpass bei 7,5 kHz - oberhalb liegt ohnehin nur Encoder-Rauschen.
4. Die Lautheit (RMS) wieder auf den Ausgangswert bringen, gedeckelt durch
   einen Spitzenpegel von -3 dBFS. Bewusst RMS und nicht Spitzenwert: Wer
   eine herausstechende Frequenz wegnimmt und danach den Spitzenwert
   wiederherstellt, macht die Datei insgesamt lauter - das würde die
   Mischung des Spiels verschieben. Übersteuerte Dateien werden über den
   Deckel automatisch leiser, was bei genau den schrillsten hilft.

Die Originale werden nach tools/audiogen/sfx_original/ gesichert. Ein
zweiter Lauf arbeitet wieder auf dieser Sicherung, verarbeitet also nie
doppelt - Parameter lassen sich damit gefahrlos nachjustieren.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

HIER = Path(__file__).resolve().parent
PROJEKT = HIER.parents[1]
SFX_DIR = PROJEKT / "game" / "audio" / "sfx"
SICHERUNG = HIER / "sfx_original"

SR = 48000
ZIEL_PEAK_DB = -3.0

# Terzbänder im Schärfebereich, in denen nach der Spitze gesucht wird.
SCHAERFE_BAENDER = [(2000, 2500), (2500, 3150), (3150, 4000),
                    (4000, 5000), (5000, 6300), (6300, 8000)]

# Ab diesem Energieanteil in 2-8 kHz gilt eine Datei als behandlungsbedürftig.
SCHWELLE_SCHAERFE = 0.35

# Störtonsuche: nur oberhalb dieser Grenze, darunter sind schmale Spitzen
# in der Regel gewollter Klang (Glocke, Signalton).
TON_AB_HZ = 4500
TON_BIS_HZ = 8000
# Wie weit ein Ton über seiner geglätteten Umgebung stehen muss, um als
# Artefakt zu gelten. 20 dB trennt die Vokoder-Pfeiftöne (36-44 dB) sicher
# von normalen Klangspitzen.
TON_SCHWELLE_DB = 20.0
TON_MAX_ABSENKUNG = 18.0
# Zusätzlich muss der Ton überhaupt hörbar sein: Ein Pfeifton 60 dB unter
# dem Hauptsignal sticht zwar aus seiner Umgebung heraus, hört aber niemand.
TON_HOERBAR_UNTER_MAX_DB = 40.0


def lade(pfad):
    roh = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(pfad), "-ac", "1", "-ar", str(SR),
         "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(roh, dtype=np.float32)


def finde_stoertoene(x):
    """Schmale, stehende Töne im Artefaktbereich finden."""
    n = 16384
    if x.size < n * 2:
        return []
    bloecke = [np.abs(np.fft.rfft(x[i:i + n] * np.hanning(n))) ** 2
               for i in range(0, len(x) - n, n // 2)]
    P = np.mean(bloecke, axis=0)
    f = np.fft.rfftfreq(n, 1 / SR)
    Pl = 10 * np.log10(P + 1e-20)
    hoerbar = Pl.max() - TON_HOERBAR_UNTER_MAX_DB
    bin_hz = SR / n
    fenster = int(500 / bin_hz)       # +/- 500 Hz Umgebung
    kern = int(40 / bin_hz)           # der Ton selbst zählt nicht als Umgebung

    # Referenz ist der Median der Leistung in der Umgebung, nicht deren
    # logarithmischer Mittelwert: Über den Logarithmus gemittelt ziehen
    # einzelne Nullstellen die Referenz massiv nach unten, und dann sieht
    # jeder gewöhnliche Buckel wie ein 40-dB-Pfeifton aus.
    toene = []
    idx = np.where((f >= TON_AB_HZ) & (f <= TON_BIS_HZ))[0]
    for i in idx:
        if Pl[i] < hoerbar:
            continue
        lo, hi = max(0, i - fenster), min(len(P), i + fenster)
        umgebung = np.concatenate([P[lo:max(lo, i - kern)], P[min(hi, i + kern):hi]])
        if umgebung.size < 10:
            continue
        ueberschuss = 10 * np.log10(P[i] / (np.median(umgebung) + 1e-20))
        if ueberschuss > TON_SCHWELLE_DB and P[i] == P[max(0, i - kern):i + kern].max():
            toene.append((float(f[i]), float(ueberschuss)))

    # Nur die deutlichsten, und keine Dubletten dicht beieinander
    toene.sort(key=lambda t: -t[1])
    gewaehlt = []
    for hz, db in toene:
        if all(abs(hz - g[0]) > 150 for g in gewaehlt):
            gewaehlt.append((hz, db))
        if len(gewaehlt) == 4:
            break
    return sorted(gewaehlt)


def messe(pfad):
    x = lade(pfad)
    if x.size < 4096:
        return None
    n = 4096
    fenster = np.hanning(n)
    bloecke = [np.abs(np.fft.rfft(x[i:i + n] * fenster)) ** 2
               for i in range(0, len(x) - n, n // 2)]
    P = np.mean(bloecke, axis=0)
    f = np.fft.rfftfreq(n, 1 / SR)
    ges = P.sum() + 1e-20

    def anteil(lo, hi):
        return float(P[(f >= lo) & (f < hi)].sum() / ges)

    # Pegel des Artefaktbereichs, bezogen auf die stärkste Stelle der Datei.
    # Das ist das Maß, das dem Höreindruck entspricht - die reine Anzahl
    # erkannter Spitzen sagt nach dem Filtern wenig aus, weil auch stark
    # abgesenkte Reste rechnerisch noch aus ihrer Umgebung herausragen.
    artefaktband = float(10 * np.log10(
        P[(f >= TON_AB_HZ) & (f <= TON_BIS_HZ)].sum() / (P.max() + 1e-20) + 1e-20))

    baender = [(lo, hi, anteil(lo, hi)) for lo, hi in SCHAERFE_BAENDER]
    lo, hi, stark = max(baender, key=lambda b: b[2])
    mittel = float(np.mean([b[2] for b in baender]))
    # Frequenz, unterhalb derer 99 % der Energie liegen - alles darüber
    # ist für diese Datei entbehrlich.
    kum = np.cumsum(P) / (P.sum() + 1e-20)
    f99 = float(f[int(np.searchsorted(kum, 0.99))])

    return dict(
        stoertoene=finde_stoertoene(x),
        artefaktband=artefaktband,
        f99=f99,
        rms_db=float(20 * np.log10(np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-20)),
        schaerfe=anteil(2000, 8000),
        ueber5k=anteil(5000, 8000),
        spitzenband=(lo + hi) / 2,
        spitzenband_ueberschuss=stark / (mittel + 1e-9),
        peak_db=float(20 * np.log10(np.abs(x).max() + 1e-20)),
    )


def kette(m, schwelle=SCHWELLE_SCHAERFE):
    """Leitet die Filterkette aus der Messung ab. Leer = nichts zu tun."""
    filter_ = []

    # Störtöne zuerst - sonst hebt das Nachziehen der Lautheit sie mit an.
    toene = m["stoertoene"]
    kamm_grenze = None
    if len(toene) >= 3:
        # Kamm: abschneiden statt einzeln notchen. Die Grenze liegt unter dem
        # tiefsten Störton, aber nie unter dem, was die Datei an Nutzsignal
        # braucht (99-Prozent-Grenze), und nie unter 2,5 kHz.
        kamm_grenze = max(2500.0, min(toene[0][0] - 200.0, m["f99"]))
        filter_.append("lowpass=f=%d:p=2" % int(kamm_grenze))
        filter_.append("lowpass=f=%d:p=2" % int(kamm_grenze))
    else:
        for hz, ueberschuss in toene:
            gain = -min(TON_MAX_ABSENKUNG, ueberschuss - 6.0)
            filter_.append("equalizer=f=%d:t=q:w=30:g=%.1f" % (int(hz), gain))

    if m["schaerfe"] >= schwelle:
        # Je deutlicher ein Band heraussticht, desto tiefer die Glocke -
        # gedeckelt, damit nichts dumpf wird.
        ueberschuss = m["spitzenband_ueberschuss"]
        gain = -min(8.0, max(3.0, 3.0 * ueberschuss))
        filter_.append("equalizer=f=%d:t=q:w=1.2:g=%.1f"
                       % (int(m["spitzenband"]), gain))

        if m["ueber5k"] > 0.25 and kamm_grenze is None:
            filter_.append("highshelf=f=5000:g=-3.5")

        if kamm_grenze is None:
            filter_.append("lowpass=f=7500")

    return filter_


def verarbeite(pfad, filter_, rms_db):
    """Filtert und stellt den Ausgangspegel wieder her (gedeckelt bei -3 dBFS)."""
    ziel = SFX_DIR / pfad.name
    with_filter = ",".join(filter_) if filter_ else "anull"

    tmp = ziel.with_suffix(".tmp.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(pfad),
                    "-af", with_filter, str(tmp)], check=True)

    x = lade(tmp)
    neuer_peak = float(20 * np.log10(np.abs(x).max() + 1e-20))
    neuer_rms = float(20 * np.log10(np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-20))
    # So viel anheben, dass die Lautheit wieder stimmt - aber nur so weit,
    # wie der Spitzenpegel es zulässt.
    anhebung = min(rms_db - neuer_rms, ZIEL_PEAK_DB - neuer_peak)

    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp),
                    "-af", "volume=%.2fdB" % anhebung,
                    "-ac", "2", "-c:a", "vorbis", "-strict", "-2", "-q:a", "5",
                    str(ziel)], check=True)
    tmp.unlink(missing_ok=True)
    return anhebung


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--dry-run", action="store_true",
                    help="nur messen und zeigen, was passieren würde")
    ap.add_argument("--schwelle", type=float, default=SCHWELLE_SCHAERFE,
                    help="Energieanteil in 2-8 kHz, ab dem gefiltert wird")
    args = ap.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg fehlt.")

    SICHERUNG.mkdir(parents=True, exist_ok=True)
    dateien = sorted(SFX_DIR.glob("*.ogg"))
    if not dateien:
        sys.exit("Keine SFX in %s" % SFX_DIR)

    print("%-26s %8s %8s %9s  %s" % ("Datei", "2-8kHz", "Peak dB", "Störton", "Behandlung"))
    print("-" * 96)

    behandelt = 0
    for datei in dateien:
        # Immer vom Original ausgehen, nie vom schon behandelten Stand.
        quelle = SICHERUNG / datei.name
        if not quelle.exists():
            shutil.copy2(datei, quelle)

        m = messe(quelle)
        if m is None:
            continue
        filter_ = kette(m, args.schwelle)

        if not filter_ and m["peak_db"] <= ZIEL_PEAK_DB + 0.5:
            print("%-26s %7.1f%% %8.1f %9s  unverändert"
                  % (datei.name, 100 * m["schaerfe"], m["peak_db"], "-"))
            continue

        beschreibung = ("Lautheit erhalten, Spitze gedeckelt auf %.0f dBFS" % ZIEL_PEAK_DB
                        if m["peak_db"] > ZIEL_PEAK_DB else "Lautheit erhalten")
        if filter_:
            beschreibung = "; ".join(filter_) + "; " + beschreibung

        if args.dry_run:
            print("%-26s %7.1f%% %8.1f %9s  %s"
                  % (datei.name, 100 * m["schaerfe"], m["peak_db"],
                     ("%.0fHz" % m["stoertoene"][0][0]) if m["stoertoene"] else "-",
                     beschreibung))
        else:
            verarbeite(quelle, filter_, m["rms_db"])
            neu = messe(datei)

            # Nachkorrektur: Wird eine dominante Frequenz weggenommen, hebt
            # die anschließende Lautheitskorrektur alles Übrige an - auch den
            # oberen Bereich, den wir gerade beruhigen wollten. Dann kommt ein
            # sanftes Höhenband dazu und die Datei wird noch einmal erzeugt.
            if neu["artefaktband"] > m["artefaktband"] + 1.0:
                filter_ = [f for f in filter_ if not f.startswith("highshelf")]
                filter_.append("highshelf=f=4500:g=-4")
                verarbeite(quelle, filter_, m["rms_db"])
                neu = messe(datei)
            print("%-26s %7.1f%% %8.1f %9s  -> 2-8kHz %.1f%%, Artefaktband %+.1f dB, RMS %+.1f dB"
                  % (datei.name, 100 * m["schaerfe"], m["peak_db"],
                     ("%.0fHz" % m["stoertoene"][0][0]) if m["stoertoene"] else "-",
                     100 * neu["schaerfe"],
                     neu["artefaktband"] - m["artefaktband"],
                     neu["rms_db"] - m["rms_db"]))
        behandelt += 1

    print("\n%d von %d Dateien %s. Originale liegen in %s"
          % (behandelt, len(dateien),
             "würden behandelt" if args.dry_run else "behandelt",
             SICHERUNG.relative_to(PROJEKT)))


if __name__ == "__main__":
    main()
