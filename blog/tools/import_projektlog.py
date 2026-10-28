#!/usr/bin/env python3
"""Übernimmt ausgewählte Einträge aus einem Projekt-Log (HTML-Seiten mit Überschriften „Log 12 — Titel“) als Serie.

Nur Einträge, deren Kopfzeile den eingestellten Autor nennt, werden übernommen – mit dem eigenen Text:
Anmerkungen anderer (z. B. „Kommentar …“, „Anmerkung der Redaktion …“) werden abgeschnitten.
Die alte Nummer bleibt als Herkunft erhalten („ursprünglich Log 21“).

Aufruf: python3 tools/import_projektlog.py [startbestand-ordner]
Einstellungen: <startbestand>/quellen.json → "projektlog": {
    "seiten": ["https://…/blog.html", …], "autor_muster": "Name", "quelle_name": "projektlog",
    "serie": {"id": "…", "titel": "…", "einleitung": "…"},
    "abschneiden_ab": ["Kommentar", …], "weglassen": ["Von …:", …], "nur_nummern": [],   (leer = alle des Autors)
    "kennung_praefix": "log" }   → Adresse z. B. …/log-21-ein-bemerkenswerter-tag/
"""
import json, re, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
sys.path.insert(0, str(Path(__file__).resolve().parent))
from importhilfe import alte_uebersetzung, hole, html_zu_markdown, lade_json, schreibe_json, slug, stopp
from bs4 import BeautifulSoup, Tag

ziel = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "startbestand")
q = lade_json(ziel / "quellen.json", {}).get("projektlog")
if not q: stopp("quellen.json hat keinen Abschnitt „projektlog“")
KOPF = re.compile(r"^\s*Log\s+(\d{1,4})\s*[—–-]\s*(.+?)\s*$")
MONATE = {m: i + 1 for i, m in enumerate(["januar", "februar", "märz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember"])}
abschneiden = [s.lower() for s in q.get("abschneiden_ab", [])]
weglassen = [s.lower() for s in q.get("weglassen", [])]
muster = q.get("autor_muster", "")
nur = set(q.get("nur_nummern") or [])
quelle_name = q.get("quelle_name", "projektlog")
s_cfg = q.get("serie") or {}
sid = s_cfg.get("id") or "projekt-log"


def hat_kopf(t):
    """Enthält dieses Element (oder ist es) eine Log-Überschrift?"""
    koepfe = ([t] if re.match(r"^h[1-4]$", t.name or "") else []) + t.find_all(re.compile(r"^h[1-4]$"))
    return any(KOPF.match(re.sub(r"\s+", " ", x.get_text(" ", strip=True))) for x in koepfe)


def anfang(tag):
    return re.sub(r"^[\s*_#]+", "", tag.get_text(" ", strip=True)).lower()


def zeitpunkt(meta):
    m = re.search(r"(\d{1,2})\.\s*([A-Za-zäöüÄÖÜ]+)\s+(\d{4})", meta)
    if not m or m[2].lower() not in MONATE: return None
    u = re.search(r"(?:um|ca\.)\s+(\d{1,2}):(\d{2})", meta)
    d = datetime(int(m[3]), MONATE[m[2].lower()], int(m[1]), int(u[1]) if u else 12, int(u[2]) if u else 0, tzinfo=ZoneInfo("Europe/Berlin"))
    return d.isoformat()


def autor(meta, teile):
    m = re.search(r"Eintrag von\s+(.+?)(?:\s+um\s+\d|$)", meta) or re.search(r"Projekt\s*-?\s*Log\s*·\s*([^,·]+),\s*veröffentlicht", meta)
    if m: return m[1].strip()
    for t in [x for x in teile if isinstance(x, Tag)][:2]:  # ältere Einträge: erste Zeile „Von Name:“
        v = re.fullmatch(r"\s*Von\s+(.{1,40}?)\s*:\s*", t.get_text(" ", strip=True))
        if v: return v[1]
    return ""


def titel_ohne_datum(t):
    """„20. September 2026, ca. 07:09 Uhr — Titel“ → „Titel“ (ältere Einträge tragen das Datum im Titel)"""
    return re.sub(r"^\d{1,2}\.\s*[A-Za-zäöüÄÖÜ]+\s+\d{4}(,?\s*(ca\.|um)?\s*\d{1,2}:\d{2}\s*Uhr)?\s*[—–-]\s*", "", t).strip() or t


bericht = ["## Projekt-Log", ""]
eintraege = []
for seite in q.get("seiten", []):
    soup = BeautifulSoup(hole(seite), "html.parser")
    for h in soup.find_all(re.compile(r"^h[1-4]$")):
        kopf = re.sub(r"\s+", " ", h.get_text(" ", strip=True)).replace("Septem ber", "September")
        k = KOPF.match(kopf)
        if not k: continue
        # Inhalt: Geschwister bis zur nächsten Log-Überschrift (oder bis zum Ende des umschließenden Blocks)
        teile = []
        for sib in h.next_siblings:
            if isinstance(sib, Tag) and hat_kopf(sib):
                break
            if isinstance(sib, Tag) and sib.name in ("footer", "hr") and teile: break
            teile.append(sib)
        tags = [t for t in teile if isinstance(t, Tag)]
        meta_tag = next((t for t in tags[:3] if re.search(r"Projekt\s*-?\s*Log\s*·", t.get_text(" ", strip=True)) and re.search(r"\d{4}", t.get_text())), None)
        meta = meta_tag.get_text(" ", strip=True) if meta_tag else ""
        if not re.search(r"\d{4}", meta): meta = k[2]  # ältere Einträge: Datum steht im Titel
        eintraege.append({"nr": int(k[1]), "titel": titel_ohne_datum(k[2]), "meta": meta, "autor": autor(meta, teile), "seite": seite, "anker": h.get("id"),
                          "teile": [t for t in teile if t is not meta_tag]})

bilder = ziel / "bilder" / "import"; bilder.mkdir(parents=True, exist_ok=True)
for p in (ziel / "beitraege").glob("*.json") if (ziel / "beitraege").exists() else []:
    if json.loads(p.read_text(encoding="utf-8")).get("herkunft", {}).get("quelle") == quelle_name: p.unlink()
ids = {p.stem for p in (ziel / "beitraege").glob("*.json")} if (ziel / "beitraege").exists() else set()
gesehen, neu = set(), []
for e in sorted(eintraege, key=lambda x: x["nr"]):
    if e["nr"] in gesehen: continue
    gesehen.add(e["nr"])
    eigen = (muster and muster.lower() in e["autor"].lower()) and (not nur or e["nr"] in nur)
    bericht.append(f"- Log {e['nr']} „{e['titel']}“ – Autor: {e['autor'] or 'unbekannt'} → " + ("**übernommen**" if eigen else "bleibt drüben"))
    if not eigen: continue
    html, abgeschnitten = [], []
    for t in e["teile"]:
        if isinstance(t, Tag):
            a = anfang(t)
            if any(a.startswith(x) for x in abschneiden): abgeschnitten.append(a[:60]); break
            if any(a.startswith(x) for x in weglassen) and len(a) < 200: continue
        html.append(str(t))
    if abgeschnitten: bericht.append(f"    abgeschnitten ab: „{abgeschnitten[0]}…“")
    bid = f"{slug(q.get('kennung_praefix', 'log'), 20)}-{e['nr']}-" + slug(e["titel"], 60)
    while bid in ids: bid += "-2"
    ids.add(bid)
    datum = zeitpunkt(e["meta"])
    if not datum: bericht.append(f"    ⚠ Datum nicht erkannt in „{e['meta'][:80]}“ – bitte im Editor setzen"); datum = "2026-01-01T12:00:00+01:00"
    url = e["seite"] + (f"#{e['anker']}" if e["anker"] else "")
    text = html_zu_markdown("".join(html), e["seite"], bid, bilder, "bilder/import", bericht)
    b = {"id": bid, "status": "veroeffentlicht", "datum": datum, "titel": e["titel"], "text": text, "serie": sid, "reihe": e["nr"], "stichwoerter": s_cfg.get("stichwoerter", []),
         "herkunft": {"quelle": quelle_name, "url": url, "titel": f"Log {e['nr']} — {e['titel']}", "nr": e["nr"], "bezeichnung": f"Log {e['nr']}"}}
    b["en"] = alte_uebersetzung(ziel, b)
    neu.append(b)
    schreibe_json(ziel / "beitraege" / f"{bid}.json", b)

serien = lade_json(ziel / "serien.json", {"serien": []})["serien"]
alt = next((s for s in serien if s["id"] == sid), None)
s_neu = {"id": sid, "titel": s_cfg.get("titel", "Projekt-Log"), "einleitung": s_cfg.get("einleitung", ""), "quelle": quelle_name,
         "en": (alt or {}).get("en") or {"titel": "", "einleitung": "", "geprueft": False, "stand": ""}}
serien = [s for s in serien if s["id"] != sid] + ([s_neu] if neu else [])
schreibe_json(ziel / "serien.json", {"serien": serien})
if not eintraege: bericht.append("⚠ Keine Log-Einträge gefunden – Aufbau der Seite geändert?")
(ziel / "bericht-projektlog.md").write_text("\n".join(bericht) + "\n", encoding="utf-8")
print("\n".join(bericht))
print(f"\n{len(eintraege)} Einträge gefunden, {len(neu)} übernommen.")
