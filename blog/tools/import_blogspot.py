#!/usr/bin/env python3
"""Einmaliger Umzug eines Blogger-/Blogspot-Blogs in den Startbestand.

Liest Beiträge und Seiten über den öffentlichen Blogger-Feed (JSON), wandelt sie in Markdown, holt die Bilder
und erkennt Serien an Titeln der Form „Serienname (7) – Titel des Teils“. Serien-Einleitungen kommen aus
Seiten mit dem Titel „Serie: Serienname“ (Text ohne die Liste der Teile). Beiträge ohne Nummer bleiben Einzelbeiträge.

Aufruf: python3 tools/import_blogspot.py [startbestand-ordner]
Einstellungen: <startbestand>/quellen.json → "blogspot": {"adresse": "https://….blogspot.com/"}
               (im Test statt Adresse: "beitraege_datei" und "seiten_datei" mit Blogger-JSON)
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from importhilfe import alte_uebersetzung, berlin, hole, html_zu_markdown, lade_json, schreibe_json, slug, stopp
import json
from bs4 import BeautifulSoup

ziel = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "startbestand")
q = lade_json(ziel / "quellen.json", {}).get("blogspot")
if not q: stopp("quellen.json hat keinen Abschnitt „blogspot“")
adresse = q.get("adresse", "").rstrip("/") + "/"
SERIE = re.compile(r"^\s*(?P<name>.+?)\s*\((?P<nr>\d{1,3})\)\s*[-–—:]\s*(?P<titel>.+?)\s*$")

def feed(art, datei):
    if q.get(datei): return json.loads(hole(q[datei]))
    return json.loads(hole(f"{adresse}feeds/{art}/default?alt=json&max-results=500"))

bericht = ["## Blogspot", f"Quelle: {adresse}", ""]
roh = feed("posts", "beitraege_datei").get("feed", {}).get("entry", [])
seiten = feed("pages", "seiten_datei").get("feed", {}).get("entry", [])
if not roh: stopp("keine Beiträge im Feed gefunden")

bilder = ziel / "bilder" / "import"; bilder.mkdir(parents=True, exist_ok=True)
serien_alt = {s["id"]: s for s in lade_json(ziel / "serien.json", {"serien": []})["serien"]}
serien = {k: v for k, v in serien_alt.items() if v.get("quelle") != "blogspot"}
beitraege, ids = [], set()
for p in (ziel / "beitraege").glob("*.json") if (ziel / "beitraege").exists() else []:
    if json.loads(p.read_text(encoding="utf-8")).get("herkunft", {}).get("quelle") == "blogspot": p.unlink()  # sauber neu importieren
    else: ids.add(p.stem)

NAV = re.compile(r"(Erster|Vorheriger|Voriger|Nächster|Naechster|Letzter|Folgender)\s+(Post|Beitrag|Teil)", re.I)
def norm(u): return re.sub(r"^https?://", "", u.split("?")[0].split("#")[0]).rstrip("/").lower()
kennung = {}  # alte Adresse → neue Kennung (für Links zwischen Beiträgen)
for e in sorted(roh, key=lambda x: x["published"]["$t"]):
    t = e["title"]["$t"].strip(); m = SERIE.match(t)
    bid = slug(m["titel"].strip() if m else t); n = 2
    while bid in ids or bid in kennung.values(): bid = f"{slug(m['titel'].strip() if m else t, 75)}-{n}"; n += 1
    kennung[norm(next((l["href"] for l in e.get("link", []) if l.get("rel") == "alternate"), ""))] = bid

def vorbereiten(html):
    """Alte Serien-Navigation („Erster Post“, „Vorheriger Post …“) entfernen – das Blog baut sie selbst; Links auf alte Beiträge umbiegen."""
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a"):
        k = kennung.get(norm(a.get("href") or ""))
        if k: a["href"] = "beitrag:" + k
    for el in soup.find_all(["p", "div", "span", "b", "i"]):
        txt = el.get_text(" ", strip=True)
        if not txt or len(txt) > 200 or not NAV.search(txt): continue
        linktext = sum(len(a.get_text(" ", strip=True)) for a in el.find_all("a"))
        if linktext / len(txt) > 0.3: el.decompose()   # Zeile besteht im Wesentlichen aus Navigations-Links
    return str(soup)

for e in sorted(roh, key=lambda x: x["published"]["$t"]):
    titel_roh = e["title"]["$t"].strip()
    link = next((l["href"] for l in e.get("link", []) if l.get("rel") == "alternate"), adresse)
    m = SERIE.match(titel_roh)
    serie, nr, titel = None, None, titel_roh
    if m:
        name = re.sub(r"\bzur\b", "zu", m["name"].strip())  # „Gedanken zur KI“ und „Gedanken zu KI“ sind dieselbe Serie
        serie, nr, titel = slug(name, 60), int(m["nr"]), m["titel"].strip()
        serien.setdefault(serie, {"id": serie, "titel": name, "einleitung": "", "quelle": "blogspot",
                                  "en": {"titel": "", "einleitung": "", "geprueft": False, "stand": ""}})
    bid = kennung[norm(link)]
    ids.add(bid)
    bericht.append(f"- **{titel}** ({e['published']['$t'][:10]}) → `{bid}`" + (f" · Serie „{serien[serie]['titel']}“, ursprünglich Nr. {nr}" if serie else " · Einzelbeitrag"))
    text = html_zu_markdown(vorbereiten(e.get("content", {}).get("$t", "")), link, bid, bilder, "bilder/import", bericht)
    labels = [c["term"] for c in e.get("category", []) if c.get("term")]
    b = {"id": bid, "status": "veroeffentlicht", "datum": berlin(e["published"]["$t"]), "titel": titel, "text": text, "serie": serie, "reihe": nr,
         "stichwoerter": [l for l in labels if slug(l, 60) != serie],
         "herkunft": {"quelle": "blogspot", "url": link, "titel": titel_roh, **({"nr": nr, "bezeichnung": f"{serien[serie]['titel']} ({nr})"} if serie else {})}}
    b["en"] = alte_uebersetzung(ziel, b)
    beitraege.append(b)

# Serien-Einleitungen aus den Seiten „Serie: …“
for s in seiten:
    t = s["title"]["$t"].strip()
    m = re.match(r"^\s*Serie\s*:\s*(.+)$", t, re.I)
    if not m: continue
    sid = slug(re.sub(r"\bzur\b", "zu", m[1].strip()), 60)
    if sid not in serien: bericht.append(f"- ⚠ Seite „{t}“ passt zu keiner Serie"); continue
    soup = BeautifulSoup(s.get("content", {}).get("$t", ""), "html.parser")
    for liste in soup.find_all(["ul", "ol"]): liste.decompose()          # die Liste der Teile baut das Blog selbst
    for a in soup.find_all("a"):
        if adresse.split("//")[-1].rstrip("/") in (a.get("href") or ""): a.decompose()
    text = html_zu_markdown(str(soup), adresse, "serie-" + sid, bilder, "bilder/import", bericht)
    # nur echte Sätze ohne Links (Linklisten zu Teilen, PDFs usw. baut das Blog selbst bzw. gehören in die Beiträge)
    text = "\n\n".join(z for z in text.split("\n\n") if len(z.strip()) > 30 and "](" not in z)
    if text:
        serien[sid]["einleitung"] = text
        bericht.append(f"- Einleitung für Serie „{serien[sid]['titel']}“ aus der Seite „{t}“ übernommen")
    else:
        bericht.append(f"- Seite „{t}“ enthält keinen Einleitungstext (nur Links) – Einleitung bitte im Editor schreiben")

# Reihenfolge prüfen: automatische Teil-Nummer (nach Datum) gegen die alte Nummer im Titel
for sid, s in serien.items():
    teile = [b for b in beitraege if b["serie"] == sid]
    if not teile or s.get("quelle") != "blogspot": continue
    alt = [b["herkunft"].get("nr") for b in sorted(teile, key=lambda x: x["datum"])]
    bericht.append(f"- Serie „{s['titel']}“: {len(teile)} Teile, alte Nummern {alt}" +
                   ("" if alt == list(range(alt[0], alt[0] + len(alt))) else " ⚠ Nummern weichen von der Datumsfolge ab – im Blog gilt die alte Nummer als Reihenfolge (Feld „reihe“)"))

for b in beitraege: schreibe_json(ziel / "beitraege" / f"{b['id']}.json", b)
schreibe_json(ziel / "serien.json", {"serien": list(serien.values())})
(ziel / "bericht-blogspot.md").write_text("\n".join(bericht) + "\n", encoding="utf-8")
print("\n".join(bericht))
print(f"\n{len(beitraege)} Beiträge, {sum(1 for s in serien.values() if s.get('quelle') == 'blogspot')} Serien aus Blogspot übernommen.")
