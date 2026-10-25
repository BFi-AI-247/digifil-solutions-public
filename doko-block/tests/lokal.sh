#!/bin/bash
# Startet einen lokalen Testserver: tests/lokal.sh <arbeitsordner>  → http://127.0.0.1:8765/
set -e
H="$(cd "$(dirname "$0")/.." && pwd)"; W="${1:?Arbeitsordner}"
rm -rf "$W"; mkdir -p "$W/web" "$W/privat" "$W/attrappe"
python3 "$H/tools/build.py" >/dev/null
cp "$H"/dist/*.html "$H"/server/api.php "$H"/server/manifest.webmanifest "$H"/src/icon-*.png "$W/web/"
cp "$H/tests/attrappe/altdaten.json" "$W/privat/"
cp "$H"/tests/attrappe/*.json "$W/attrappe/"
python3 - "$W/privat/zugang.php" <<'P'
import hashlib,sys
h=hashlib.sha256(b"testschluessel").hexdigest()
open(sys.argv[1],"w").write(f"<?php return ['anthropic'=>'x','mistral'=>'x','gh'=>'','zugaenge'=>['{h}'=>'Clara'],'einstellungen'=>['runde'=>'Testrunde']];")
P
cd "$W/web" && DOKO_PRIVAT="$W/privat" DOKO_KI_ATTRAPPE="$W/attrappe" php -S 127.0.0.1:8765 >"$W/server.log" 2>&1 &
sleep 1; echo "läuft: http://127.0.0.1:8765/#k=testschluessel"
