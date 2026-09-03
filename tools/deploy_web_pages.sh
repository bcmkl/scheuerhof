#!/usr/bin/env bash
# Stellt den Web-Build von "Der Fluch von Scheuerhof" auf GitHub Pages bereit.
#
#   tools/deploy_web_pages.sh /pfad/zum/renpy-8.5.3-sdk [--build]
#
# --build erzeugt den Web-Build vorher neu; ohne die Option wird der
# vorhandene Ordner scheuerhof-<version>-dists/ verwendet.
#
# Wichtig: Der Web-Build entsteht mit dem Unterbefehl "web_build" des
# Launchers, nicht mit "distribute --package web" - letzterer erzeugt ein
# ganz anderes Paket (Quellen statt wasm-Laufzeit).
#
# Der Inhalt landet im verwaisten Branch gh-pages und ist danach unter
#   https://<user>.github.io/<repo>/
# spielbar. Die Quellen auf main bleiben unberührt.
set -euo pipefail

SDK="${1:?Pfad zum RenPy-SDK angeben (z.B. ./renpy-8.5.3-sdk)}"
BUILD="${2:-}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERSION="$(grep -oE 'define build\.version = "[^"]+"' game/options.rpy | cut -d'"' -f2)"
SITE="scheuerhof-${VERSION}-dists"
WORKTREE="$ROOT/.gh-pages-worktree"

if [ "$BUILD" = "--build" ] || [ ! -f "$SITE/index.html" ]; then
    echo "==> Web-Build für Version ${VERSION}"
    "$SDK/renpy.sh" "$SDK/launcher" web_build . --dest "$SITE"
fi

[ -f "$SITE/index.html" ] || { echo "Kein Web-Build in $SITE/"; exit 1; }

cleanup() { git worktree remove --force "$WORKTREE" 2>/dev/null || true; }
trap cleanup EXIT

echo "==> Schreibe Branch gh-pages"
# Bewusst jedes Mal ein frischer verwaister Commit statt einer Fortschreibung:
# Ein Web-Build wiegt rund 90 MB, und die landen bei jedem Release komplett neu
# im Baum. Ohne Historie bleibt im Repository immer nur der aktuelle Stand
# liegen, statt mit jeder Version ein weiteres Build-Paket anzusammeln.
git worktree add --force --detach "$WORKTREE"
cd "$WORKTREE"
git checkout -q --orphan gh-pages
git rm -rqf . 2>/dev/null || true
cp -R "$ROOT/$SITE/." .
# Ohne .nojekyll unterschlägt GitHub Pages Dateien und Ordner mit Unterstrich.
touch .nojekyll
git add -A
git commit -q -m "Web-Build ${VERSION} für GitHub Pages"
git push -q --force origin gh-pages
cd "$ROOT"

echo "==> Fertig."
echo "    Pages einmalig aktivieren, falls noch nicht geschehen:"
echo "    gh api -X POST repos/OWNER/REPO/pages -f source[branch]=gh-pages -f source[path]=/"
