#!/usr/bin/env python3
"""Baut den Upload-Stand nach dist/ und prüft den Startbestand.

dist/web/     → Web-Ordner (index.php, api.php, rueckmeldung.php, lib.php, .htaccess, blog.css, blog.js, editor/index.html, bilder/…)
dist/privat/  → privater Ordner (startbestand/beitraege/*.json, startbestand/serien.json); zugang.php kommt beim Upload dazu
Aufruf: python3 tools/build.py [--startbestand <ordner>]   (Vorgabe: startbestand/, im Test tests/attrappe/startbestand)
"""
import json, re, shutil, sys
from pathlib import Path

hier = Path(__file__).resolve().parent.parent
quelle = hier / "startbestand"
if "--startbestand" in sys.argv:
    quelle = Path(sys.argv[sys.argv.index("--startbestand") + 1]).resolve()
dist = hier / "dist"
shutil.rmtree(dist, ignore_errors=True)
web, privat = dist / "web", dist / "privat"
(web / "editor").mkdir(parents=True)
for f in ["index.php", "api.php", "rueckmeldung.php", "lib.php", ".htaccess"]:
    shutil.copy(hier / "server" / f, web / f)
shutil.copy(hier / "src" / "blog.css", web / "blog.css")
shutil.copy(hier / "src" / "blog.js", web / "blog.js")
shutil.copy(hier / "src" / "editor.html", web / "editor" / "index.html")

fehler = []
ids = set()
serien = {}
sb = privat / "startbestand"
(sb / "beitraege").mkdir(parents=True)
sf = quelle / "serien.json"
if sf.exists():
    d = json.loads(sf.read_text(encoding="utf-8"))
    for s in d.get("serien", []):
        if not re.fullmatch(r"[a-z0-9-]{1,60}", s.get("id", "")): fehler.append(f"Serie mit ungültiger id: {s.get('id')!r}")
        serien[s["id"]] = s
    shutil.copy(sf, sb / "serien.json")
for f in sorted((quelle / "beitraege").glob("*.json")) if (quelle / "beitraege").exists() else []:
    b = json.loads(f.read_text(encoding="utf-8"))
    i = b.get("id", "")
    if not re.fullmatch(r"[a-z0-9-]{1,90}", i): fehler.append(f"{f.name}: ungültige id {i!r}")
    if i in ids: fehler.append(f"{f.name}: id {i} doppelt")
    if f.stem != i: fehler.append(f"{f.name}: Dateiname passt nicht zur id {i}")
    if b.get("serie") and b["serie"] not in serien: fehler.append(f"{f.name}: Serie {b['serie']} fehlt in serien.json")
    if not b.get("titel") or not b.get("text"): fehler.append(f"{f.name}: Titel oder Text fehlt")
    for bild in re.findall(r"!\[[^\]]*\]\(([^)\s]+)", b.get("text", "")):
        if not bild.startswith("http") and not (quelle / bild).exists(): fehler.append(f"{f.name}: Bild fehlt {bild}")
    ids.add(i)
    shutil.copy(f, sb / "beitraege" / f.name)
if (quelle / "bilder").exists():
    shutil.copytree(quelle / "bilder", web / "bilder", dirs_exist_ok=True)
else:
    (web / "bilder").mkdir()
if fehler:
    print("Startbestand fehlerhaft:\n  " + "\n  ".join(fehler)); sys.exit(1)
print(f"dist/ gebaut: {len(ids)} Beiträge, {len(serien)} Serien im Startbestand ({quelle.relative_to(hier) if quelle.is_relative_to(hier) else quelle})")
