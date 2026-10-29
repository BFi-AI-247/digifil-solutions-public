#!/usr/bin/env python3
"""Übersetzt Beiträge und Serien-Einleitungen im Startbestand ins Englische (Mistral).

Nur was noch keine Übersetzung hat oder deren deutscher Text sich seitdem geändert hat. Ergebnis ist immer
„nicht geprüft“ – sichtbar wird Englisch erst, wenn im Editor der Haken „geprüft“ gesetzt ist.
Aufruf: MISTRAL_API_KEY=… python3 tools/uebersetze.py [startbestand-ordner]   (ohne Schlüssel: nichts zu tun, Hinweis)
"""
import json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from importhilfe import de_stand, lade_json, schreibe_json

ziel = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "startbestand")
SCHLUESSEL = os.environ.get("MISTRAL_API_KEY", "").strip()
MODELL = "mistral-large-latest"
# gleiche Anweisung wie UEBERSETZ_ANWEISUNG in server/api.php
ANWEISUNG = ("Du übersetzt Texte eines persönlichen Blogs vom Deutschen ins Englische. Bleib nah am Ton des Autors (persönlich, "
             "nachdenklich, gern mit Witz), schreib natürliches Englisch statt wörtlicher Übersetzung. Behalte die Markdown-Formatierung exakt bei "
             "(Absätze, Überschriften, Listen, **fett**, *kursiv*, Links [Text](Adresse) und Bilder ![Text](Adresse) – Adressen nie ändern). "
             "Eigennamen, Produktnamen und Zitate in anderen Sprachen bleiben, wie sie sind. Füge nichts hinzu und lass nichts weg. "
             'Antworte NUR mit JSON: {"titel": "…", "text": "…"}.')


def frage(titel, text):
    body = json.dumps({"model": MODELL, "temperature": 0.2, "max_tokens": 8000, "response_format": {"type": "json_object"},
                       "messages": [{"role": "system", "content": ANWEISUNG}, {"role": "user", "content": json.dumps({"titel": titel, "text": text}, ensure_ascii=False)}]}).encode()
    for versuch in range(4):
        try:
            req = urllib.request.Request("https://api.mistral.ai/v1/chat/completions", data=body,
                                         headers={"Content-Type": "application/json", "Authorization": "Bearer " + SCHLUESSEL})
            with urllib.request.urlopen(req, timeout=180) as r:
                t = json.loads(r.read())["choices"][0]["message"]["content"]
            t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t.strip())
            j = json.loads(t)
            if isinstance(j.get("titel"), str) and isinstance(j.get("text"), str): return j
        except (urllib.error.URLError, json.JSONDecodeError, KeyError, TimeoutError) as e:
            print(f"    Versuch {versuch + 1}: {e.__class__.__name__}", file=sys.stderr)
        time.sleep(5 * (versuch + 1))
    return None


if not SCHLUESSEL:
    print("::notice::MISTRAL_API_KEY fehlt – keine Übersetzung im Import. Im Editor geht „Übersetzen lassen“ trotzdem, wenn der Schlüssel dort eingerichtet ist.")
    sys.exit(0)
fertig = offen = 0
for p in sorted((ziel / "beitraege").glob("*.json")):
    b = json.loads(p.read_text(encoding="utf-8"))
    stand = de_stand(b["titel"], b["text"])
    if b.get("en", {}).get("stand") == stand and b["en"].get("text"): continue
    print("übersetze:", b["id"])
    j = frage(b["titel"], b["text"])
    if not j: offen += 1; print("    ⚠ nicht geklappt – bleibt ohne Englisch"); continue
    b["en"] = {"titel": j["titel"].strip()[:200], "text": j["text"].strip(), "geprueft": False, "stand": stand}
    schreibe_json(p, b); fertig += 1
sf = ziel / "serien.json"
d = lade_json(sf, {"serien": []})
for s in d["serien"]:
    stand = de_stand(s["titel"], s.get("einleitung", ""))
    if s.get("en", {}).get("stand") == stand and s["en"].get("titel"): continue
    print("übersetze Serie:", s["id"])
    j = frage(s["titel"], s.get("einleitung", "") or "-")
    if not j: offen += 1; continue
    s["en"] = {"titel": j["titel"].strip()[:120], "einleitung": "" if j["text"].strip() in ("-", "") else j["text"].strip(), "geprueft": False, "stand": stand}
    fertig += 1
schreibe_json(sf, d)
print(f"{fertig} übersetzt, {offen} nicht geklappt.")
