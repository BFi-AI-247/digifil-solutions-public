#!/usr/bin/env python3
"""Baut Digiwort aus src/game.html und den Wortlisten in data/.

Ergebnis in dist/:
  index.html     Live-Fassung (<adresse>)
  vorschau.html  Vorschau (<adresse>vorschau/) – eigener Spielstand, gelbes Schild

Einstellungen (Umgebungsvariablen, alle optional):
  DW_ADRESSE     öffentliche Adresse des Spiels, z. B. https://example.org/digiwort/ – steht im geteilten Ergebnis;
                 Rückmeldungen und Besuchszähler laufen nur auf diesem Host (leer: auf jedem Webserver)
  DW_BETREIBER   Name im Rückmelde-Dialog („… liest jede Rückmeldung.“)
  DW_HEIMAT      Webseite des Betreibers, z. B. https://example.org/ – Link unten auf der Seite und unter „Über Digiwort“
  DW_QUELLCODE   Adresse des Quellcodes, z. B. https://github.com/<name>/<repo>/tree/main/digiwort – unter „Über Digiwort“
  artifact.html  nur der Seiteninhalt, ohne <head> (für die Vorschau im Claude-Chat)

Aufruf: python3 tools/build.py
"""
import base64
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, DATA, DIST = ROOT / "src", ROOT / "data", ROOT / "dist"
ABSTAND = 365  # kleinster Abstand in Tagen, bis ein Lösungswort wiederkommen darf
OK = {5: re.compile(r"^[A-ZÄÖÜ]{5}$"), 6: re.compile(r"^[A-ZÄÖÜ]{6}$")}


def liste(name: str, n: int) -> list[str]:
    woerter = [w.strip() for w in (DATA / name).read_text(encoding="utf-8").splitlines() if w.strip() and not w.startswith("#")]
    falsch = [w for w in woerter if not OK[n].match(w)]
    if falsch:
        sys.exit(f"{name}: ungültige Einträge (nur Großbuchstaben A–Z, Ä, Ö, Ü; Länge {n}): {falsch[:10]}")
    if name.startswith("loesungen"):
        # Tagesplan: Zeile n = Tag n. Eine Lösungsliste darf hinten als Kopie angehängt werden (nächste Runde),
        # ein Wort darf aber frühestens nach ABSTAND Tagen wiederkommen.
        zuletzt, zu_frueh = {}, []
        for i, w in enumerate(woerter):
            if w in zuletzt and i - zuletzt[w] < ABSTAND:
                zu_frueh.append(f"{w} (Zeile {zuletzt[w] + 1} und {i + 1})")
            zuletzt[w] = i
        if zu_frueh:
            sys.exit(f"{name}: Wort kommt früher als nach {ABSTAND} Tagen wieder: {zu_frueh[:10]}")
        return woerter
    doppelt = {w for w in woerter if woerter.count(w) > 1} if len(woerter) < 3000 else set()
    if doppelt:
        sys.exit(f"{name}: doppelte Einträge: {sorted(doppelt)[:10]}")
    return woerter


# Manifest nicht für Samsung Internet: dessen „Installieren“ baut eine eigene App-Hülle (WebAPK) für eine alte
# Android-Version, die Google Play Protect als „Unsichere App“ blockiert. Ohne Manifest legt Samsung Internet
# eine normale Verknüpfung auf den Startbildschirm. Chrome und andere Browser bekommen das Manifest wie bisher.
MANIFEST = ('<script>if(!/SamsungBrowser/i.test(navigator.userAgent)){var m=document.createElement("link");'
            'm.rel="manifest";m.href="manifest.webmanifest";document.head.appendChild(m);}</script>')


def main() -> None:
    version = (SRC / "VERSION").read_text().strip()
    core = (SRC / "game.html").read_text(encoding="utf-8")
    adresse = os.environ.get("DW_ADRESSE", "").strip()
    if adresse and not re.fullmatch(r"https?://[A-Za-z0-9.\-]+(:\d+)?/[A-Za-z0-9_\-/]*", adresse):
        sys.exit("DW_ADRESSE bitte als volle Adresse mit / am Ende, z. B. https://example.org/digiwort/")
    betreiber = os.environ.get("DW_BETREIBER", "").strip()[:40]
    leser = f"{betreiber} liest jede Rückmeldung." if betreiber else "Jede Rückmeldung wird gelesen."
    for zeichen in "<>&\"'`$\\":
        if zeichen in betreiber:
            sys.exit("DW_BETREIBER: bitte nur einen einfachen Namen")
    links = {}
    for k in ("DW_HEIMAT", "DW_QUELLCODE"):
        v = os.environ.get(k, "").strip()
        if v and not re.fullmatch(r"https://[A-Za-z0-9.\-]+(:\d+)?(/[A-Za-z0-9_.\-/]*)?", v):
            sys.exit(f"{k} bitte als volle https-Adresse, z. B. https://example.org/")
        links[k] = v
    core = core.replace("__HEIMAT__", links["DW_HEIMAT"]).replace("__QUELLCODE__", links["DW_QUELLCODE"])
    core = core.replace("__ADRESSE__", adresse).replace("__LESER__", leser)
    for n in (5, 6):
        sol = liste(f"loesungen{n}.txt", n)
        erl = liste(f"erlaubt{n}.txt", n)
        s = set(sol)
        core = core.replace(f"__SOL{n}__", "".join(sol)).replace(f"__GUE{n}__", "".join(w for w in erl if w not in s))
        print(f"{n} Buchstaben: {len(sol)} Lösungen, {len(set(erl) | s)} erlaubte Wörter")
    i180 = base64.b64encode((SRC / "icon-180.png").read_bytes()).decode()
    cut = core.index("</style>") + len("</style>")
    DIST.mkdir(exist_ok=True)
    for name, fassung in (("index", "live"), ("vorschau", "vorschau")):
        page = core.replace("__VERSION__", version).replace("__FASSUNG__", fassung)
        if fassung == "vorschau":
            page = page.replace("<title>Digiwort</title>", "<title>Digiwort · Vorschau</title>", 1)
        head = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#141a24">
<meta name="description" content="Digiwort – deutsches Wortspiel: Finde das Wort mit fünf oder sechs Buchstaben in sechs Versuchen. Jeden Tag neu.">
{'<meta name="robots" content="noindex,nofollow">' if fassung == "vorschau" else ''}
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Digiwort">
<link rel="apple-touch-icon" href="data:image/png;base64,{i180}">
<link rel="icon" type="image/png" href="data:image/png;base64,{i180}">
{'' if fassung == "vorschau" else MANIFEST}
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}[hidden]{{display:none!important}}</style>
"""
        full = head + page[:cut] + "\n</head>\n<body>\n" + page[cut:] + "\n</body>\n</html>\n"
        (DIST / f"{name}.html").write_text(full, encoding="utf-8")
    (DIST / "artifact.html").write_text(core.replace("__VERSION__", version).replace("__FASSUNG__", "test"), encoding="utf-8")
    print(f"gebaut: Fassung {version} → dist/index.html, dist/vorschau.html")


if __name__ == "__main__":
    main()
