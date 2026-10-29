#!/bin/bash
# Startet einen lokalen Testserver mit Testdaten: tests/lokal.sh <arbeitsordner> [port]  → http://127.0.0.1:8770/
# Bricht mit Fehler ab, wenn der Port schon belegt ist oder der Server nicht antwortet (dann steht der Grund in <arbeitsordner>/server.log).
set -e
H="$(cd "$(dirname "$0")/.." && pwd)"; W="${1:?Arbeitsordner}"; PORT="${2:-${BLOG_TESTPORT:-8770}}"
if python3 -c "import socket,sys; s=socket.socket(); sys.exit(0 if s.connect_ex(('127.0.0.1',$PORT))==0 else 1)"; then
  echo "FEHLER: Port $PORT ist belegt – läuft noch ein alter Testserver? Beenden: for p in \$(ps -C php -o pid=,args= | grep $PORT | awk '{print \$1}'); do kill \$p; done" >&2
  exit 1
fi
rm -rf "$W"; mkdir -p "$W"
python3 "$H/tools/build.py" --startbestand "$H/tests/attrappe/startbestand" >/dev/null
cp -r "$H/dist/web" "$W/web"; cp -r "$H/dist/privat" "$W/privat"
LIVE="${BLOG_LIVE:-1}"
python3 - "$W/privat/zugang.php" "$LIVE" <<'P'
import hashlib,sys
h=hashlib.sha256(b"testschluessel").hexdigest()
open(sys.argv[1],"w").write("<?php return ['mistral'=>'x','gh'=>'','zugaenge'=>['"+h+"'=>'Testautorin'],'einstellungen'=>['live'=>"+("true" if sys.argv[2]=="1" else "false")+",'name'=>'Testblog','untertitel'=>'Nur zum Testen.','autor'=>'Testautorin','stil'=>'a','quellen_namen'=>['blogspot'=>'Altes Blog']]];")
P
cd "$W/web"
BLOG_PRIVAT="$W/privat" BLOG_KI_ATTRAPPE=1 BLOG_VORSCHAU="${BLOG_VORSCHAU:-0}" php -S 127.0.0.1:$PORT index.php >"$W/server.log" 2>&1 &
for i in $(seq 1 30); do
  python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:$PORT/', timeout=1)" 2>/dev/null && break
  sleep 0.2
  [ "$i" = 30 ] && { echo "FEHLER: Testserver antwortet nicht – siehe $W/server.log:" >&2; tail -5 "$W/server.log" >&2; exit 1; }
done
echo "läuft: http://127.0.0.1:$PORT/  ·  Editor: http://127.0.0.1:$PORT/editor/#k=testschluessel"
