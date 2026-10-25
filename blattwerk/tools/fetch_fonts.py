#!/usr/bin/env python3
"""Lädt die Schriften Andika und Lexend (SIL Open Font License) einmalig herunter,
damit die Website sie selbst ausliefert und keine Anfragen an Google gehen.
Ergebnis: src/fonts/fonts.css und die .woff2-Dateien. Läuft beim Upload in GitHub Actions.
"""
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "src" / "fonts"
CSS_URL = (
    "https://fonts.googleapis.com/css2?family=Andika:ital,wght@0,400;0,700;1,400"
    "&family=Lexend:wght@400;500;600&display=swap"
)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main() -> None:
    try:
        css = get(CSS_URL).decode("utf-8")
    except Exception as e:  # ohne Schriften läuft die Seite mit Systemschrift weiter
        print(f"Schriften nicht geladen ({e}); Seite nutzt Systemschriften.")
        return
    blocks = re.findall(r"/\* ([\w-]+) \*/\s*(@font-face\s*{[^}]*})", css)
    keep = [b for subset, b in blocks if subset in ("latin", "latin-ext")]
    if not keep:
        print("Keine passenden Schriftblöcke gefunden.")
        return
    FONTS.mkdir(parents=True, exist_ok=True)
    out = []
    for i, block in enumerate(keep):
        url = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
        name = f"font-{i:02d}.woff2"
        (FONTS / name).write_bytes(get(url))
        out.append(block.replace(url, name))
    (FONTS / "fonts.css").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{len(out)} Schriftdateien gespeichert.")


if __name__ == "__main__":
    sys.exit(main())
