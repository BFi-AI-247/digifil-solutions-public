#!/usr/bin/env python3
"""Baut Blattwerk aus src/ zusammen.

dist/index.html     – vollständige Seite (ohne Google-Server)
dist/vorschau.html  – dieselbe Seite als Vorschau-Fassung (eigener Browser-Speicher)
dist/artifact.html  – Vorschau-Fassung für Claude (Fragment, Schriften über Google Fonts)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DIST = ROOT / "dist"

TITLE = "Blattwerk"
GOOGLE_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Andika:ital,wght@0,400;0,700;1,400&'
    'family=Lexend:wght@400;500;600&display=swap">'
)


def read(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")


VERSION = (SRC / "VERSION").read_text(encoding="utf-8").strip()


def parts(env: str, stage: str = "live") -> str:
    db = "blattwerk2-vorschau" if stage == "vorschau" else "blattwerk2"
    return (
        f"<style>\n{read('styles.css')}\n</style>\n"
        f"{read('body.html')}\n"
        f"<script>window.BLATT_ENV = '{env}'; window.BLATT_STAGE = '{stage}'; window.BLATT_DB = '{db}'; window.BLATT_VERSION = '{VERSION}';</script>\n"
        f"<script>\n{read('core.js')}\n</script>\n"
        f"<script>\n{read('app.js')}\n</script>\n"
    )


def page(stage: str, font_link: str) -> str:
    if stage == "vorschau":
        font_link = font_link.replace('href="fonts/', 'href="../fonts/')
    title = TITLE + (" Vorschau" if stage == "vorschau" else "")
    return (
        "<!doctype html>\n<html lang=\"de\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
        "<meta name=\"robots\" content=\"noindex,nofollow\">\n"
        "<meta name=\"apple-mobile-web-app-capable\" content=\"yes\">\n"
        f"<title>{title}</title>\n{font_link}\n</head>\n<body>\n{parts('web', stage)}</body>\n</html>\n"
    )


def main() -> None:
    DIST.mkdir(exist_ok=True)
    # Schriften liegen selbst gehostet unter <pfad>/fonts/ (Datenschutz: keine Google-Anfragen)
    local_fonts = (SRC / "fonts" / "fonts.css").exists()
    font_link = '<link rel="stylesheet" href="fonts/fonts.css">' if local_fonts else ""
    (DIST / "index.html").write_text(page("live", font_link), encoding="utf-8")
    (DIST / "vorschau.html").write_text(page("vorschau", font_link), encoding="utf-8")
    if local_fonts:
        import shutil
        shutil.copytree(SRC / "fonts", DIST / "fonts", dirs_exist_ok=True)
    artifact = (
        f"<title>{TITLE}</title>\n<meta name=\"claude:viewport-fit-sides\" content=\"cover\">\n"
        f"{GOOGLE_FONTS}\n{parts('artifact')}"
    )
    (DIST / "artifact.html").write_text(artifact, encoding="utf-8")
    print("gebaut: index.html, vorschau.html, artifact.html (v" + VERSION + ")")


if __name__ == "__main__":
    main()
