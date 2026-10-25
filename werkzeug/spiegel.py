#!/usr/bin/env python3
"""Spiegel: übernimmt freigegebene Code-Ordner aus einem privaten Repo in dieses öffentliche Repo.

Aufruf (im Workflow des privaten Repos):
    python3 spiegel.py <konfig.json> <privates-repo> <oeffentliches-repo>

Die Konfiguration (z. B. .github/oeffentlich.json im privaten Repo):
{
  "eintraege": [
    {"von": "doko-idstein", "nach": "doko-block",
     "ordner": ["src", "server", "tools", "tests"],
     "ohne": ["server/zugaenge.json", "server/einstellungen.json", "tools/*.xlsx"]}
  ],
  "verboten": ["Name1", "Name2", "meine-domain.de"],
  "ausnahmen": {"doko-block/tools/quellen.py": ["Name1 Nachname"]}
}

"ausnahmen" erlaubt je Zieldatei bestimmte Begriffe oder Wendungen (z. B. eine Quellenangabe, die zufällig
einen verbotenen Vornamen enthält). Sie werden vor der Prüfung aus der Zeile entfernt; alles andere wird weiter geprüft.

Ablauf je Eintrag: Zielordner <nach>/<ordner> wird geleert und aus <von>/<ordner> neu befüllt
(ohne die Muster in "ohne" und ohne __pycache__). Andere Dateien im Ziel (README, beispiele/ …)
bleiben unberührt. Danach prüft das Skript alle Textdateien der Zielordner auf verbotene Begriffe
und typische Schlüssel. Findet es etwas, endet es mit Fehler – dann wird nichts veröffentlicht.
"""
import fnmatch
import json
import re
import shutil
import sys
from pathlib import Path

SCHLUESSEL = [
    r"sk-ant-[A-Za-z0-9_\-]{10,}", r"ghp_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"AKIA[0-9A-Z]{16}", r"xox[bap]-[A-Za-z0-9\-]{10,}",
]
BINAER = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".woff", ".woff2", ".ttf", ".otf", ".pdf", ".zip", ".xlsx"}


def ausgeschlossen(rel: str, muster: list[str]) -> bool:
    teile = rel.split("/")
    if "__pycache__" in teile or rel.endswith(".pyc"):
        return True
    return any(fnmatch.fnmatch(rel, m) or rel == m.rstrip("/") or rel.startswith(m.rstrip("/") + "/") for m in muster)


def kopiere(quelle: Path, ziel: Path, eintrag: dict) -> list[Path]:
    von, nach = quelle / eintrag["von"], ziel / eintrag["nach"]
    ohne = eintrag.get("ohne", [])
    geschrieben = []
    for ordner in eintrag["ordner"]:
        q, z = von / ordner, nach / ordner
        if not q.is_dir():
            sys.exit(f"Quelle fehlt: {q}")
        if z.exists():
            shutil.rmtree(z)
        for datei in sorted(q.rglob("*")):
            if not datei.is_file():
                continue
            rel = datei.relative_to(von).as_posix()
            if ausgeschlossen(rel, ohne):
                continue
            neu = nach / rel
            neu.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(datei, neu)
            geschrieben.append(neu)
    return geschrieben


def pruefe(dateien: list[Path], verboten: list[str], basis: Path, ausnahmen: dict | None = None) -> list[str]:
    muster = [(w, re.compile(r"(?<![\w])" + re.escape(w) + r"(?![\w])", re.IGNORECASE)) for w in verboten if w.strip()]
    muster += [("Schlüssel", re.compile(s)) for s in SCHLUESSEL]
    funde = []
    for d in dateien:
        if d.suffix.lower() in BINAER:
            continue
        try:
            text = d.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = d.relative_to(basis).as_posix()
        erlaubt = [re.compile(r"(?<![\w])" + re.escape(a) + r"(?![\w])", re.IGNORECASE)
                   for a in sorted((ausnahmen or {}).get(rel, []), key=len, reverse=True)]
        for nr, zeile in enumerate(text.splitlines(), 1):
            for rx in erlaubt:
                zeile = rx.sub(" ", zeile)
            for name, rx in muster:
                if rx.search(zeile):
                    funde.append(f"{d.relative_to(basis)}:{nr}: „{name}“")
    return funde


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    konfig = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    quelle, ziel = Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    alle = []
    for e in konfig["eintraege"]:
        neu = kopiere(quelle, ziel, e)
        print(f"{e['von']} → {e['nach']}: {len(neu)} Dateien")
        alle += neu
    funde = pruefe(alle, konfig.get("verboten", []), ziel, konfig.get("ausnahmen"))
    if funde:
        print("\nNICHT veröffentlicht – verbotene Begriffe oder Schlüssel gefunden:")
        print("\n".join("  " + f for f in funde[:50]))
        if len(funde) > 50:
            print(f"  … und {len(funde) - 50} weitere")
        sys.exit(1)
    print("Prüfung OK – keine verbotenen Begriffe, keine Schlüssel.")


if __name__ == "__main__":
    main()
