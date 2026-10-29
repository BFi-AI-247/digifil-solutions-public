#!/usr/bin/env python3
"""Prüft die Import-Werkzeuge offline mit nachgebauten Quellen (tests/attrappe/import). Endet mit „IMPORT OK“."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

HIER = Path(__file__).resolve().parent.parent
fehler = []
def pruefe(bed, text):
    print(("  ok  " if bed else "  FEHLER  ") + text)
    if not bed: fehler.append(text)

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp); q = tmp / "quellen"; shutil.copytree(HIER / "tests/attrappe/import", q)
    for f in q.glob("*.json"): f.write_text(f.read_text().replace("@HIER@", str(q)))
    sb = tmp / "startbestand"; sb.mkdir()
    (sb / "quellen.json").write_text(json.dumps({
        "blogspot": {"adresse": "https://altes-blog.example/", "beitraege_datei": str(q / "blogger-beitraege.json"), "seiten_datei": str(q / "blogger-seiten.json")},
        "projektlog": {"seiten": [str(q / "log.html"), str(q / "archiv.html")], "autor_muster": "Testautor", "quelle_name": "projektlog",
                       "kennung_praefix": "test-log", "serie": {"id": "test-projekt-log", "titel": "Test – Projekt-Log", "einleitung": "Meine Einträge."},
                       "abschneiden_ab": ["Kommentar PM", "Anmerkung der Redaktion", "Ältere Einträge", "Zuletzt aktiv"], "weglassen": ["Von Testautor:", "Geändert am"]}}, ensure_ascii=False))
    for w in ("import_blogspot.py", "import_projektlog.py"):
        r = subprocess.run([sys.executable, str(HIER / "tools" / w), str(sb)], capture_output=True, text=True)
        pruefe(r.returncode == 0, f"{w} läuft durch" + ("" if r.returncode == 0 else ": " + r.stderr[-400:]))
    b = {p.stem: json.loads(p.read_text()) for p in (sb / "beitraege").glob("*.json")}
    s = {x["id"]: x for x in json.loads((sb / "serien.json").read_text())["serien"]}
    print("   Beiträge:", sorted(b))
    pruefe("gamechanger-oder-endgame" in b and b["gamechanger-oder-endgame"]["serie"] == "gedanken-zu-ki", "Serie aus dem Titel erkannt, Nummer aus dem Titel entfernt")
    pruefe(b.get("sprache-und-worte", {}).get("serie") == "gedanken-zu-ki", "„Gedanken zur KI“ landet in derselben Serie")
    pruefe(b.get("kein-social-media-das-geht-auch", {}).get("serie") is None, "Beitrag ohne Nummer bleibt Einzelbeitrag")
    t = b["gamechanger-oder-endgame"]["text"]
    pruefe("**Gamechanger**" in t and "\n\nZweiter Absatz" in t, "HTML → Markdown mit Absätzen")
    pruefe("![](bilder/import/gamechanger-oder-endgame-1.png)" in t and (sb / "bilder/import/gamechanger-oder-endgame-1.png").exists(), "Bild (große Fassung) übernommen und lokal verlinkt")
    pruefe("https://altes-blog.example/p/x.html" in t, "Relative Links werden absolut")
    pruefe("Erster Post" not in b["sprache-und-worte"]["text"] and "about:invalid" not in b["sprache-und-worte"]["text"], "Alte Serien-Navigation entfernt")
    pruefe("[meinen Beitrag zum Gamechanger](beitrag:gamechanger-oder-endgame)" in b["sprache-und-worte"]["text"], "Link auf alten Beitrag zeigt auf den neuen")
    pruefe(b["gamechanger-oder-endgame"]["datum"] == "2024-12-28T10:10:00+01:00", f"Datum in deutscher Zeit ({b['gamechanger-oder-endgame']['datum']})")
    pruefe("Eingebettetes Video" in b["sprache-und-worte"]["text"] and "- Grok" in b["sprache-und-worte"]["text"], "Einbettung wird Link, Liste bleibt Liste")
    pruefe("Ein Jahr ist vergangen." in b["kein-social-media-das-geht-auch"]["text"].split("\n\n")[1], "Doppelte Zeilenumbrüche werden Absätze")
    pruefe(s["gedanken-zu-ki"]["einleitung"] == "Meine Gedanken zur KI, Teil für Teil.", "Serien-Einleitung aus der Seite „Serie: …“ ohne Teile-Liste")
    pruefe(b["gamechanger-oder-endgame"]["herkunft"]["bezeichnung"] == "Gedanken zu KI (5)", "Alte Nummer bleibt als Herkunft")
    logs = {k: v for k, v in b.items() if k.startswith("test-log-")}
    pruefe(sorted(logs) == ["test-log-16-die-domain", "test-log-2-der-anfang", "test-log-22-fertig-sort-of"], f"Nur eigene Log-Einträge übernommen ({sorted(logs)})")
    l22 = logs.get("test-log-22-fertig-sort-of", {})
    pruefe("Wofür eigentlich?" in l22.get("text", "") and "Kommentar" not in l22.get("text", ""), "Kommentar der Agenten abgeschnitten")
    l16 = logs.get("test-log-16-die-domain", {}).get("text", "")
    pruefe(l16.startswith("Seit heute") and "Anmerkung" not in l16 and "Archiv" not in l16, "„Von …:“ weggelassen, Anmerkung und Archiv-Hinweis abgeschnitten")
    pruefe(l22.get("datum") == "2026-10-05T06:34:00+02:00", f"Datum mit Uhrzeit aus der Kopfzeile ({l22.get('datum')})")
    pruefe(l22.get("herkunft", {}).get("url", "").endswith("log.html#log-22"), "Herkunft mit Anker")
    pruefe(s.get("test-projekt-log", {}).get("titel") == "Test – Projekt-Log", "Serie für den Projekt-Log angelegt")
    # zweiter Lauf: gleiches Ergebnis, keine Dubletten
    for w in ("import_blogspot.py", "import_projektlog.py"): subprocess.run([sys.executable, str(HIER / "tools" / w), str(sb)], capture_output=True)
    pruefe(len(list((sb / "beitraege").glob("*.json"))) == len(b), "Zweiter Import erzeugt keine Dubletten")
    r = subprocess.run([sys.executable, str(HIER / "tools/build.py"), "--startbestand", str(sb)], capture_output=True, text=True)
    pruefe(r.returncode == 0, "Import-Ergebnis besteht die Prüfung in build.py" + ("" if r.returncode == 0 else ": " + r.stdout[-300:]))

print()
if fehler: print(f"{len(fehler)} FEHLER"); sys.exit(1)
print("IMPORT OK")
