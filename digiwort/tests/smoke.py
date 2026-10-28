#!/usr/bin/env python3
"""Rauchtest für Digiwort – Pflicht vor jedem Push und im Upload-Workflow.

Aufruf:  python3 tests/smoke.py dist/index.html [--bilder ORDNER]
Prüft die Färbelogik, spielt in Chromium (Playwright) die wichtigsten Abläufe durch
und endet mit „OK“. Mit --bilder entstehen Bildschirmfotos (Handy, hell und dunkel).
"""
import os
import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright

fehler = []


def pruefe(bedingung, text):
    print(("  ok   " if bedingung else "  FEHLER ") + text)
    if not bedingung:
        fehler.append(text)


# Lösung, Versuch, erwartete Farben (G = grün, Y = gelb, - = grau)
FAERBUNG = [
    ("HALLO", "LALLE", "-GGG-"), ("SPASS", "SASSE", "GYYG-"), ("ESSEN", "SEEEE", "YY-G-"),
    ("ÄRGER", "ARGER", "-GGGG"), ("KATZE", "KATZE", "GGGGG"), ("STERN", "NETTE", "YYY--"),
    ("ABBAU", "BABBA", "YYG-Y"), ("MÜLLE", "LULLE", "--GGG"), ("TEEEE", "ETTTT", "YY---"),
    ("GRÖSSE", "LASSEN", "--YGY-"), ("STRESS", "SESSEL", "GYYY--"), ("GRÖSSE", "GRÖSSE", "GGGGGG"),
]


def tippe(pg, wort):
    for ch in wort.lower():
        pg.evaluate("k=>document.dispatchEvent(new KeyboardEvent('keydown',{key:k}))", ch)
    pg.keyboard.press("Enter")


def main(datei: str, bilder: str | None) -> int:
    url = pathlib.Path(datei).resolve().as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 390, "height": 800}, device_scale_factor=2)
        pg = ctx.new_page()
        js = []
        pg.on("pageerror", lambda e: js.append(str(e)))
        pg.on("console", lambda m: js.append(m.text) if m.type == "error" and "manifest" not in m.text.lower()
              and "ERR_FILE_NOT_FOUND" not in m.text else None)
        pg.goto(url)
        pg.wait_for_timeout(400)

        print("Färbelogik")
        for sol, g, soll in FAERBUNG:
            ist = pg.evaluate("([g,s])=>score(g,s).map(x=>({ok:'G',near:'Y',off:'-'})[x]).join('')", [g, sol])
            pruefe(ist == soll, f"{sol} / {g} → {ist}" + ("" if ist == soll else f" (erwartet {soll})"))

        print("Wortlisten")
        n5, n6 = pg.evaluate("[SOL[5].length, SOL[6].length]")
        pruefe(n5 > 1000 and n6 > 1000, f"genug Lösungswörter ({n5} / {n6})")
        pruefe(pg.evaluate("SOL[5].every(w=>VALID[5].has(w)&&[...w].length===5)&&SOL[6].every(w=>VALID[6].has(w)&&[...w].length===6)"),
               "alle Lösungen sind erlaubte Wörter der richtigen Länge")
        pruefe(pg.evaluate("VALID[5].has('SPASS')&&VALID[5].has('ÄRGER')&&VALID[6].has('GRÖSSE')&&!VALID[5].has('XYZQW')"),
               "Stichproben (SPASS, ÄRGER, GRÖSSE ja, XYZQW nein)")
        pruefe(pg.evaluate("dayIndex(new Date(2026,9,25,0,1))===0&&dayIndex(new Date(2026,9,26,23,59))===1&&dayIndex(new Date(2027,2,30))===156"),
               "Tageszählung inkl. Zeitumstellung")

        print("Spielen")
        pg.keyboard.press("Escape")
        tippe(pg, "xyzqw")
        pg.wait_for_timeout(150)
        pruefe("Kein gültiges Wort" in pg.inner_text("#toasts"), "ungültiges Wort wird abgelehnt")
        for _ in range(5):
            pg.keyboard.press("Backspace")
        sol = pg.evaluate("game.sol")
        versuch = "HABEN" if sol != "HABEN" else "TISCH"
        tippe(pg, versuch)
        pg.wait_for_timeout(1700)
        pruefe(pg.locator(".board .row").first.locator(".tile.ok, .tile.near, .tile.off").count() == 5, "Versuch wird gefärbt")
        pruefe(pg.locator(".k.ok, .k.near, .k.off").count() > 0, "Tastatur färbt sich mit")
        pg.click("#l6")
        pg.wait_for_timeout(200)
        pruefe(pg.locator(".board .row").first.locator(".tile").count() == 6, "6-Buchstaben-Modus")
        tippe(pg, "größe")
        pg.wait_for_timeout(1900)
        pruefe(pg.evaluate("game.guesses[0]") == "GRÖSSE", "ß wird zu SS (GRÖSSE)")
        pg.click("#mEndless")
        pg.wait_for_timeout(200)
        pruefe("Endlos" in pg.inner_text("#sub"), "Endlos-Modus")
        pg.click("#mDaily"); pg.click("#l5")
        pg.wait_for_timeout(200)
        pruefe(pg.evaluate("game.guesses.length") == 1, "Spielstand bleibt beim Wechseln erhalten")

        print("Teilen")
        t = pg.evaluate("shareText()")
        adresse = os.environ.get("DW_ADRESSE", "").strip()
        pruefe((t.rstrip().endswith(adresse) if adresse else "http" not in t) and not any(ch in t.split("\n\n")[1] for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ"),
               "geteilter Text: nur Farbfelder" + (", Link zur Seite am Ende" if adresse else ", ohne Link (DW_ADRESSE leer)"))
        print("Links")
        heim, code = os.environ.get("DW_HEIMAT", "").strip(), os.environ.get("DW_QUELLCODE", "").strip()
        pruefe(pg.evaluate("[...document.querySelectorAll('#visits a')].map(a=>a.href).join()") == heim, "Fußzeile: Link zur Webseite" if heim else "Fußzeile: kein Link (DW_HEIMAT leer)")
        pruefe(pg.evaluate("$('ueberCode').hidden ? '' : $('codeLink').href") == code, "Über Digiwort: Link zum Quellcode" if code else "Über Digiwort: ohne Quellcode-Link (DW_QUELLCODE leer)")
        print("Statistik und Übertragung")
        pg.click("#bStats")
        pruefe(pg.is_visible("#dStats"), "Statistik öffnet")
        pg.click("#bExport")
        code = pg.input_value("#exportCode")
        pruefe(code.startswith("DIGIWORT-"), "Code wird erstellt")
        pg2 = ctx.new_page()
        pg2.on("pageerror", lambda e: js.append(str(e)))
        pg2.goto(url)
        pg2.evaluate("localStorage.clear()")
        pg2.reload(); pg2.wait_for_timeout(300); pg2.keyboard.press("Escape")
        pg2.click("#bStats"); pg2.click("#bImportOpen")
        pg2.fill("#importCode", "Quatsch"); pg2.click("#bImport")
        pruefe("kein Digiwort-Code" in pg2.inner_text("#importMsg"), "falscher Code wird abgefangen")
        pg2.fill("#importCode", code); pg2.click("#bImport"); pg2.click("#bImport")
        pg2.wait_for_timeout(300)
        pruefe(pg2.evaluate("game.guesses.length") == 1, "Code überträgt den Spielstand")
        pg2.close()
        pg.keyboard.press("Escape")

        print("Rückmeldung")
        pg.click("#bFb")
        pruefe(pg.is_visible("#dFb"), "Rückmelde-Dialog öffnet")
        pruefe(pg.get_attribute("#fbArt [data-a=sonstiges]", "aria-pressed") == "true" and pg.evaluate("fbArt") == "sonstiges",
               "„Sonstiges“ ist vorausgewählt")
        pg.click("#fbArt [data-a=wort-fehlt]")
        pruefe("nicht angenommen" in pg.inner_text("#fbLabel"), "Art wählbar")
        pg.click("#bFbSend")
        pruefe("ein paar Worte" in pg.inner_text("#fbMsg"), "leere Rückmeldung wird abgefangen")
        pg.keyboard.press("Escape")

        if bilder:
            out = pathlib.Path(bilder); out.mkdir(parents=True, exist_ok=True)
            pg.screenshot(path=str(out / "handy-dunkel.png"))
            pg.evaluate("document.documentElement.setAttribute('data-look','light')")
            pg.screenshot(path=str(out / "handy-hell.png"))

        print("Statistik nur nach Rundenende")
        pg.click("#mDaily"); pg.click("#l6"); pg.wait_for_timeout(200)
        if pg.evaluate("game.status") == "play":
            tippe(pg, pg.evaluate("game.sol"))
            pg.wait_for_timeout(3600)
            pruefe(pg.is_visible("#dStats"), "Statistik öffnet nach dem Lösen")
            pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
        pg.click("#l5"); pg.wait_for_timeout(200); pg.click("#l6"); pg.wait_for_timeout(700)
        pruefe(pg.evaluate("game.status") != "play" and not pg.is_visible("#dStats"), "Wechsel auf fertiges Rätsel öffnet keine Statistik")
        pg.reload(); pg.wait_for_timeout(900)
        pruefe(not pg.is_visible("#dStats"), "Start mit fertigem Rätsel öffnet keine Statistik")

        pruefe(not js, "keine JavaScript-Fehler" + (f": {js[:3]}" if js else ""))
        b.close()
    print("FEHLER: " + "; ".join(fehler) if fehler else "OK")
    return 1 if fehler else 0


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("datei")
    a.add_argument("--bilder")
    x = a.parse_args()
    sys.exit(main(x.datei, x.bilder))
