#!/usr/bin/env python3
"""Erzeugt zugang.php für <privat>/doko-block (außerhalb des Web-Ordners, nicht abrufbar).

Enthält
- die API-Schlüssel aus den Umgebungsvariablen ANTHROPIC_API_KEY, MISTRAL_API_KEY, DOKO_GITHUB_TOKEN (alle optional),
- die Prüfsummen (SHA-256) der persönlichen Zugangs-Links aus server/zugaenge.json,
- die Einstellungen der Runde aus server/einstellungen.json.

Beide JSON-Dateien sind nicht im Repo (siehe .gitignore); Vorlagen: *.example.json.
Einen neuen Zugang erzeugt:  python3 tools/make_zugang.py --neu Anna
"""
import hashlib, json, os, re, secrets, sys
from pathlib import Path

hier = Path(__file__).resolve().parent.parent


def schluessel(name):
    v = os.environ.get(name, "").strip()
    if v and not re.fullmatch(r"[A-Za-z0-9_\-]+", v):
        sys.exit(f"{name} enthält unerwartete Zeichen.")
    return v


def php(v):
    """Python-Wert → PHP-Literal (Strings sicher maskiert)."""
    if isinstance(v, bool): return "true" if v else "false"
    if isinstance(v, (int, float)): return repr(v)
    if isinstance(v, str): return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"
    if isinstance(v, list): return "[" + ", ".join(php(x) for x in v) + "]"
    if isinstance(v, dict): return "[" + ", ".join(f"{php(str(k))} => {php(x)}" for k, x in v.items()) + "]"
    raise TypeError(type(v))


def lade(name):
    f = hier / "server" / name
    if not f.exists():
        sys.exit(f"server/{name} fehlt – Vorlage: server/{name.replace('.json', '.example.json')}")
    return json.loads(f.read_text(encoding="utf-8"))


if len(sys.argv) == 3 and sys.argv[1] == "--neu":
    k = secrets.token_urlsafe(18)
    print(f"Schlüssel für {sys.argv[2]}: {k}")
    print(f"In server/zugaenge.json eintragen:  \"{hashlib.sha256(k.encode()).hexdigest()}\": \"{sys.argv[2]}\"")
    print(f"Persönlicher Link:  https://<deine-seite>/<pfad>/#k={k}")
    sys.exit(0)

einst = lade("einstellungen.json")
spieler = einst.get("spieler", [])
assert isinstance(spieler, list) and len(spieler) == 4 and all(re.fullmatch(r"\w{1,20}", s) for s in spieler), \
    "einstellungen.json: genau vier Spieler-Namen (Buchstaben/Ziffern) angeben"
for n, c in (einst.get("farben") or {}).items():
    assert n in spieler and re.fullmatch(r"#[0-9a-fA-F]{6}", c), f"einstellungen.json: Farbe für {n} fehlerhaft"
if einst.get("repo"):
    assert re.fullmatch(r"[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+", einst["repo"]), "einstellungen.json: repo als owner/repo"

zugaenge = lade("zugaenge.json")
for h, n in zugaenge.items():
    assert re.fullmatch(r"[0-9a-f]{64}", h) and n in spieler, f"zugaenge.json: {n} ist kein Spieler der Runde"

werte = {"anthropic": schluessel("ANTHROPIC_API_KEY"), "mistral": schluessel("MISTRAL_API_KEY"), "gh": schluessel("DOKO_GITHUB_TOKEN"),
         "zugaenge": zugaenge, "einstellungen": einst}
out = Path(sys.argv[1] if len(sys.argv) > 1 else "zugang.php")
out.write_text("<?php\n// automatisch erzeugt beim Upload – nicht bearbeiten\nreturn " + php(werte) + ";\n", encoding="utf-8")
print("zugang.php geschrieben:", ", ".join(f"{k} {'ja' if werte[k] else 'fehlt'}" for k in ("anthropic", "mistral", "gh")),
      f"· {len(zugaenge)} Zugänge · Runde „{einst.get('runde', 'Doko-Runde')}“")
