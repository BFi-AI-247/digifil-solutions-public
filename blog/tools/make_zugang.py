#!/usr/bin/env python3
"""Erzeugt zugang.php für den privaten Ordner des Blogs (außerhalb des Web-Ordners, nicht abrufbar).

Enthält
- die Schlüssel aus den Umgebungsvariablen MISTRAL_API_KEY (Übersetzung) und BLOG_GITHUB_TOKEN (Rückmeldungen als Issues), beide optional,
- die Prüfsummen (SHA-256) der persönlichen Editor-Links aus server/zugaenge.json,
- die Einstellungen aus server/einstellungen.json.

Vorlagen: server/*.example.json.
Einen neuen Editor-Zugang erzeugen:  python3 tools/make_zugang.py --neu <Name>
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
    if v is None: return "null"
    if isinstance(v, (int, float)): return repr(v)
    if isinstance(v, str): return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"
    if isinstance(v, list): return "[" + ", ".join(php(x) for x in v) + "]"
    if isinstance(v, dict): return "[" + ", ".join(f"{php(str(k))} => {php(x)}" for k, x in v.items()) + "]"
    raise TypeError(type(v))


def lade(name):
    f = hier / "server" / name
    if not f.exists():
        f = hier / "server" / name.replace(".json", ".example.json")
        print(f"Hinweis: server/{name} fehlt – nehme die Vorlage {f.name}", file=sys.stderr)
    return json.loads(f.read_text(encoding="utf-8"))


if len(sys.argv) == 3 and sys.argv[1] == "--neu":
    k = secrets.token_urlsafe(18)
    print(f"Schlüssel für {sys.argv[2]}: {k}")
    print(f"In server/zugaenge.json eintragen:  \"{hashlib.sha256(k.encode()).hexdigest()}\": \"{sys.argv[2]}\"")
    print(f"Persönlicher Editor-Link:  https://<deine-seite>/<pfad>/editor/#k={k}")
    sys.exit(0)

einst = lade("einstellungen.json")
assert einst.get("stil", "a") in ("a", "b", "c"), "einstellungen.json: stil muss a, b oder c sein"
if einst.get("repo"):
    assert re.fullmatch(r"[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+", einst["repo"]), "einstellungen.json: repo als owner/repo"
if einst.get("adresse"):
    assert re.fullmatch(r"https?://\S+/", einst["adresse"]), "einstellungen.json: adresse mit https:// und / am Ende"
zugaenge = lade("zugaenge.json")
for h, n in zugaenge.items():
    assert re.fullmatch(r"[0-9a-f]{64}", h) and re.fullmatch(r"[\w .-]{1,40}", n), f"zugaenge.json: Eintrag {n!r} fehlerhaft"

werte = {"mistral": schluessel("MISTRAL_API_KEY"), "gh": schluessel("BLOG_GITHUB_TOKEN"), "zugaenge": zugaenge, "einstellungen": einst}
out = Path(sys.argv[1] if len(sys.argv) > 1 else "zugang.php")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("<?php\n// automatisch erzeugt beim Upload – nicht bearbeiten\nreturn " + php(werte) + ";\n", encoding="utf-8")
print("zugang.php geschrieben:", ", ".join(f"{k} {'ja' if werte[k] else 'fehlt'}" for k in ("mistral", "gh")),
      f"· {len(zugaenge)} Editor-Zugänge · „{einst.get('name', 'Blog')}“")
