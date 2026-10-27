#!/usr/bin/env python3
"""Rauchtest für Blattwerk – Pflicht vor jedem Push und im Upload-Workflow.

Aufruf:  python3 tests/smoke.py dist/index.html [--bilder ORDNER]
Lädt die gebaute Seite in Chromium (Playwright), spielt die wichtigsten Abläufe durch
und endet mit „OK“. Mit --bilder entstehen Bildschirmfotos (iPad quer, iPad hochkant).
"""
import argparse
import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

fehler = []


def pruefe(bedingung, text):
    print(("  ok   " if bedingung else "  FEHLER ") + text)
    if not bedingung:
        fehler.append(text)


async def main(datei: str, bilder: str | None) -> int:
    url = pathlib.Path(datei).resolve().as_uri()
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1180, "height": 820}, has_touch=True)
        pg = await ctx.new_page()
        js_fehler = []
        pg.on("pageerror", lambda e: js_fehler.append(str(e)))
        # Schriften liegen online unter <pfad>/fonts/ – lokal (file://) fehlen sie, das ist kein Fehler
        pg.on("console", lambda m: js_fehler.append(m.text) if m.type == "error" and "ERR_FILE_NOT_FOUND" not in m.text else None)
        await pg.goto(url)
        await pg.wait_for_timeout(700)

        print("Beispielblatt")
        pruefe(await pg.locator(".page").count() == 1, "eine Seite")
        pruefe(await pg.locator(".item.lineatur").count() == 4, "vier Lineaturen")
        pruefe(await pg.locator(".item.number").count() == 4, "vier Nummern")
        nums = await pg.evaluate("[...document.querySelectorAll('.item.number .num')].map(n=>n.textContent).join(',')")
        pruefe(nums == "1,2,3,4", "Nummern 1–4 in Lesereihenfolge")
        pruefe(await pg.locator(".page .cell").count() == 7, "Kopfzeile mit sieben Feldern")

        print("Bearbeiten")
        box = await pg.locator(".item.lineatur").first.bounding_box()
        await pg.mouse.click(box["x"] + 50, box["y"] + 10)
        pruefe(await pg.locator(".selbox").count() == 1, "Lineatur auswählbar")
        await pg.mouse.move(box["x"] + 50, box["y"] + 10)
        await pg.mouse.down()
        await pg.mouse.move(box["x"] + 90, box["y"] + 40, steps=6)
        await pg.mouse.up()
        moved = await pg.evaluate("document.querySelector('.item.lineatur').style.left")
        pruefe(moved != "45mm", "Lineatur verschiebbar")
        await pg.click("#btnUndo")
        back = await pg.evaluate("document.querySelector('.item.lineatur').style.left")
        pruefe(back == "45mm", "Rückgängig stellt die Lage wieder her")
        await pg.keyboard.press("Escape")
        await pg.tap("[data-add=L2]")
        await pg.wait_for_timeout(150)
        pruefe(await pg.locator(".item.lineatur").count() == 5, "Lineatur aus der Leiste hinzugefügt")
        await pg.keyboard.press("Escape")
        await pg.get_by_text("Punkte-Spalte einfügen").click()
        pruefe(await pg.locator(".pts").count() == 4, "Punkte-Spalte mit vier Feldern")
        await pg.locator(".pts").first.click()
        await pg.locator('.stepper button[aria-label="Punkte mehr"]').click()
        await pg.locator('.stepper button[aria-label="Punkte mehr"]').click()
        pruefe("/ 1" in await pg.locator(".pts").first.inner_text(), "Punkte je Block einstellbar")
        await pg.keyboard.press("Escape")
        await pg.click("#btnAddPage")
        pruefe(await pg.locator(".page").count() == 2, "neue Seite")
        await pg.click("#btnUndo")
        pruefe(await pg.locator(".page").count() == 1, "neue Seite rückgängig")

        print("Hineinschreiben (#1)")
        await pg.keyboard.press("Escape")
        await pg.evaluate("document.getElementById('desk').scrollTo(0,0)")
        lb = await pg.locator(".item.lineatur").first.bounding_box()
        await pg.mouse.click(lb["x"] + 60, lb["y"] + 8)
        await pg.mouse.click(lb["x"] + 60, lb["y"] + 8)
        await pg.wait_for_timeout(100)
        pruefe(await pg.locator(".item.lineatur.editing").count() == 1, "Lineatur: zweimal antippen startet das Schreiben")
        await pg.keyboard.type("Haus")
        await pg.keyboard.press("Enter")
        await pg.keyboard.type("Maus")
        await pg.keyboard.press("Escape")
        zeilen = await pg.evaluate("[...document.querySelector('.item.lineatur').querySelectorAll('.lrow')].map(r=>r.textContent)")
        pruefe(zeilen[:2] == ["Haus", "Maus"], "Lineatur: Text steht in Zeile 1 und 2")
        await pg.click("#btnUndo")
        zeilen = await pg.evaluate("[...document.querySelector('.item.lineatur').querySelectorAll('.lrow')].map(r=>r.textContent)")
        pruefe(zeilen[:2] == ["", ""], "Lineatur: Rückgängig nimmt das Geschriebene in einem Schritt zurück")
        await pg.click("#btnRedo")
        await pg.keyboard.press("Escape")
        await pg.tap("[data-add=karo]")
        await pg.wait_for_timeout(600)
        await pg.locator(".item.karo").first.scroll_into_view_if_needed()
        kb = await pg.locator(".item.karo").first.bounding_box()
        await pg.mouse.click(kb["x"] + 40, kb["y"] + 25)
        await pg.wait_for_timeout(100)
        pruefe(await pg.locator(".item.karo.editing").count() == 1, "Kästchen: Antippen startet das Schreiben")
        await pg.keyboard.type("12+3")
        await pg.click("#btnUnder")
        await pg.keyboard.press("Backspace")
        zeichen = await pg.evaluate("[...document.querySelectorAll('.item.karo text')].map(t=>t.textContent).join('')")
        pruefe(zeichen == "12+", "Kästchen: ein Zeichen je Kästchen, Löschtaste nimmt das letzte weg")
        pruefe(await pg.locator(".item.karo .kunder").count() == 1, "Kästchen: Zeile unterstreichen")
        await pg.keyboard.press("Escape")
        await pg.keyboard.press("Escape")
        pruefe(await pg.locator(".item.karo .kcur").count() == 0, "Kästchen: Schreibmarke verschwindet nach dem Schreiben")

        print("Tabelle (#2)")
        await pg.tap("[data-add=table]")
        await pg.wait_for_timeout(600)
        tab = pg.locator(".item.table").first
        await tab.scroll_into_view_if_needed()
        pruefe(await pg.locator(".item.table td").count() == 6, "Tabelle mit 2 Zeilen und 3 Spalten eingefügt")
        tb = await tab.bounding_box()
        await pg.mouse.click(tb["x"] + 30, tb["y"] + 12)
        await pg.wait_for_timeout(150)
        pruefe(await pg.locator(".item.table.editing").count() == 1, "Tabelle: Antippen startet das Schreiben")
        await pg.keyboard.type("Hund")
        await pg.keyboard.press("Tab")
        await pg.keyboard.type("Katze und noch viel mehr Text, damit die Zeile höher wird")
        h0 = await pg.evaluate("parseFloat(document.querySelector('.item.table').style.height)")
        pruefe(h0 > 19, "Tabelle: Zeile wächst mit dem Text")
        await pg.get_by_role("button", name="Zeile darunter").click()
        await pg.wait_for_timeout(100)
        pruefe(await pg.locator(".item.table td").count() == 9, "Tabelle: Zeile einfügen")

        print("Tabelle unterstreichen (#3)")
        await pg.click("#btnCellUnder")
        await pg.wait_for_timeout(100)
        pruefe(await pg.locator(".item.table td.under").count() == 1, "Tabelle: eine Zelle unterstreichen")
        z00 = pg.locator('.item.table td[data-r="0"][data-c="0"]')
        await z00.click(modifiers=["Shift"])
        await pg.wait_for_timeout(100)
        pruefe(await pg.locator(".item.table td.insel").count() == 4, "Tabelle: Umschalt+Klick wählt mehrere Zellen")
        await pg.click("#btnCellUnder")
        await pg.wait_for_timeout(100)
        pruefe(await pg.locator(".item.table td.under").count() == 4, "Tabelle: Auswahl unterstreichen")
        await pg.get_by_role("button", name="Nur diese eine Zelle").click()
        await pg.click("#btnCellExtend")
        await pg.locator('.item.table td[data-r="2"][data-c="2"]').tap()
        await pg.wait_for_timeout(100)
        pruefe(await pg.locator(".item.table td.insel").count() == 9, "Tabelle: „Bis zu einer Zelle auswählen“ per Antippen")
        a20 = await pg.locator('.item.table td[data-r="2"][data-c="0"]').bounding_box()
        a22 = await pg.locator('.item.table td[data-r="2"][data-c="2"]').bounding_box()
        await pg.mouse.move(a20["x"] + 5, a20["y"] + 5)
        await pg.mouse.down()
        await pg.mouse.move(a22["x"] + 5, a22["y"] + 5, steps=6)
        await pg.mouse.up()
        await pg.wait_for_timeout(100)
        pruefe(await pg.locator(".item.table td.insel").count() == 3, "Tabelle: Auswahl mit der Maus aufziehen")
        await pg.click("#btnCellUnder")
        await pg.wait_for_timeout(100)
        pruefe(await pg.locator(".item.table td.under").count() == 7, "Tabelle: aufgezogene Auswahl unterstreichen")
        await pg.click("#btnUndo")
        await pg.wait_for_timeout(100)
        pruefe(await pg.locator(".item.table td.under").count() == 4, "Tabelle: Rückgängig nimmt den Strich zurück")
        await pg.click("#btnRedo")
        await pg.wait_for_timeout(100)
        tab2 = await pg.locator(".item.table").first.bounding_box()
        await pg.mouse.click(tab2["x"] + 30, tab2["y"] + 12)
        await pg.mouse.click(tab2["x"] + 30, tab2["y"] + 12)
        await pg.wait_for_timeout(100)
        await pg.keyboard.press("Escape")
        await pg.keyboard.press("Escape")
        zellen = await pg.evaluate("[...document.querySelectorAll('.item.table td')].map(t=>t.textContent)")
        pruefe(zellen[0] == "Hund" and zellen[1].startswith("Katze"), "Tabelle: Text steht in den Zellen")
        pruefe(await pg.locator(".item.table td[contenteditable=true]").count() == 0, "Tabelle: Schreiben endet mit Escape")

        if bilder:
            out = pathlib.Path(bilder)
            out.mkdir(parents=True, exist_ok=True)
            await pg.evaluate("document.getElementById('desk').scrollTo(0,0)")
            await pg.screenshot(path=str(out / "ipad-quer.png"))

        print("Drucken")
        await pg.emulate_media(media="print")
        pdf = await pg.pdf(format="A4", print_background=True, prefer_css_page_size=True)
        await pg.emulate_media(media="screen")
        pruefe(pdf.count(b"/Type /Page") - pdf.count(b"/Type /Pages") == 1, "Druck ergibt genau eine A4-Seite")

        if bilder:
            ctx2 = await b.new_context(viewport={"width": 820, "height": 1180}, has_touch=True)
            p2 = await ctx2.new_page()
            await p2.goto(url)
            await p2.wait_for_timeout(600)
            await p2.screenshot(path=str(pathlib.Path(bilder) / "ipad-hochkant.png"))

        pruefe(not js_fehler, "keine Skriptfehler" + ("" if not js_fehler else ": " + "; ".join(js_fehler[:3])))
        await b.close()
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("datei")
    ap.add_argument("--bilder")
    a = ap.parse_args()
    asyncio.run(main(a.datei, a.bilder))
    if fehler:
        print(f"FEHLER: {len(fehler)} Prüfung(en) nicht bestanden")
        sys.exit(1)
    print("OK")
