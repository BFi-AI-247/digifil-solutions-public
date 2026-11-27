#!/usr/bin/env python3
"""Durchlauf gegen den lokalen Testserver (tests/lokal.sh): Laden, Foto auslesen, speichern, Statistik,
KI-Vorschlag übernehmen, löschen, im Verlauf wiederherstellen. Bildschirmfotos nach <ordner>."""
import io, sys
from pathlib import Path
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/"
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "shots"); OUT.mkdir(parents=True, exist_ok=True)
fehler = []

# Attrappe der GitHub-Schnittstelle (DOKO_GITHUB_API in tests/lokal.sh): lehnt jeden Schlüssel ab wie ein abgelaufener (#65)
import json as _json, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
class _GH(BaseHTTPRequestHandler):
    def _nein(self):
        b = _json.dumps({"message": "Bad credentials", "documentation_url": "https://docs.github.com/rest"}).encode()
        self.send_response(401); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self): self.rfile.read(int(self.headers.get("Content-Length", 0))); self._nein()
    def do_GET(self): self._nein()
    def log_message(self, *a): pass
threading.Thread(target=HTTPServer(("127.0.0.1", 8766), _GH).serve_forever, daemon=True).start()

def foto():
    im = Image.new("RGB", (1200, 1600), "white"); d = ImageDraw.Draw(im)
    for i in range(22): d.line([(60, 100 + i * 65), (1140, 100 + i * 65)], fill="#99a")
    d.text((80, 40), "K   R   B   S", fill="black")
    b = io.BytesIO(); im.save(b, "JPEG"); p = OUT / "zettel.jpg"; p.write_bytes(b.getvalue()); return p

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pg.on("pageerror", lambda e: fehler.append(f"JS: {e}"))
    dialoge, ablehnen = [], {"plaetze": False}
    def _dialog(d):
        dialoge.append(d.message)
        if d.type == "prompt": d.accept("Test-Löschung")
        elif ablehnen["plaetze"] and "andere Plätze" in d.message: d.dismiss()
        else: d.accept()
    pg.on("dialog", _dialog)
    kl0 = lambda sel: pg.eval_on_selector(sel, "e => e.className")
    pg.goto(URL + "#k=testschluessel"); pg.wait_for_selector("#hallo:has-text('Hallo Clara')")
    assert "204 Abende" in pg.inner_text("#hallo"), pg.inner_text("#hallo")
    assert "#k=" not in pg.url, "Schlüssel bleibt in der Adresse"
    pg.screenshot(path=OUT / "1-erfassen.png", full_page=True)
    # Foto auslesen
    pg.set_input_files("#foto", str(foto()))
    pg.wait_for_selector("#auslesen:not([disabled])")
    w0 = pg.evaluate("document.querySelector('#foto-vorschau').naturalWidth")
    pg.click("#drehen"); pg.wait_for_function(f"document.querySelector('#foto-vorschau').naturalWidth !== {w0} && document.querySelector('#foto-vorschau').complete")
    pg.click("#auslesen")
    pg.wait_for_selector("#e-ok"); pg.wait_for_timeout(300)
    assert pg.input_value("#e-datum") == "2026-10-25"
    assert pg.input_value("#e-ort") == "bei Anna + essen", pg.input_value("#e-ort")
    pl = {s: pg.input_value(f'[data-platz="{s}"]') for s in ["Anna", "Ben", "Clara", "David"]}
    assert pl == {"Anna": "2", "Ben": "1", "Clara": "4", "David": "3"}, pl
    assert "Unsicher:" not in pg.inner_text("#entwurf"), "Unsicher-Hinweis doppelt (steht schon als Farbe in der Tabelle)"
    assert "Ohne Pflichtsolo: Clara" in pg.inner_text("#entwurf"), pg.inner_text("#entwurf")[:600]
    assert pg.input_value('[data-sitz="0"]') == "David"
    # Spalten der Spielzeilen in Sitzordnung (#70): wie die KI sie von links nach rechts gelesen hat, nicht in der Reihenfolge der Einstellungen.
    # #67 (Bürotest des Betreibers 27.11.): eine Reihenfolge, die vom Zettel – oben je Spalte Name (wählbar), gelesene Überschrift,
    # Endstand und Platz; keine eigenen Zeilen „Sitzordnung“, „Plätze“, „Endstand“. Die KI liefert nach Position, die App ordnet die Namen zu
    # (Attrappe: „Bn“ ist nicht erkannt → Ben geraten und markiert; die Spalte „Spiel“ in den Spalten der KI wird übergangen).
    kopf = lambda: pg.evaluate("[...document.querySelectorAll('#entwurf table.spiele thead th[data-kopf]')].map(e => e.dataset.kopf)")
    kopftext = lambda: pg.evaluate("[...document.querySelectorAll('#entwurf table.spiele thead th[data-kopf]')].map(e => e.textContent)")
    zeile0 = lambda: pg.evaluate("[...document.querySelectorAll('#entwurf tr[data-zeile=\"0\"] [data-sp]')].map(e => e.dataset.s + '=' + e.value)")
    namen0 = lambda: [x.split("=")[0] for x in zeile0()]
    zahlen0 = lambda: [x.split("=")[1] for x in zeile0()]
    oben = lambda: pg.evaluate("[...document.querySelectorAll('#entwurf [data-kopfzelle]')].map(z => [z.querySelector('[data-sitz]').value, z.querySelector('[data-end]').dataset.end, z.querySelector('[data-end]').value, z.querySelector('[data-platz]').dataset.platz, z.querySelector('[data-platz]').value])")
    assert kopf() == ["David", "Anna", "Ben", "Clara"], kopf()
    assert namen0() == ["David", "Anna", "Ben", "Clara"], zeile0()
    if pg.locator("#entwurf [data-kopfzelle]").count() != 4: fehler.append(f"Prüfmaske (#67): {pg.locator('#entwurf [data-kopfzelle]').count()} Spaltenköpfe statt 4")
    if pg.evaluate("[...document.querySelectorAll('#entwurf [data-platz], #entwurf [data-end]')].filter(e => !e.closest('[data-kopfzelle]')).length"): fehler.append("Prüfmaske (#67): Plätze oder Endstand noch in eigener Zeile mit Namen")
    o0 = oben()
    if [x[0] for x in o0] != ["David", "Anna", "Ben", "Clara"] or any(x[0] != x[1] or x[0] != x[3] for x in o0): fehler.append(f"Prüfmaske (#67): Spaltenköpfe oben passen nicht zur Tabelle: {o0}")
    gel = pg.evaluate("[...document.querySelectorAll('#entwurf [data-kopfzelle] .gelesen')].map(e => e.textContent)")
    if gel != ["Zettel: D", "Zettel: A", "Zettel: Bn", "Zettel: C"]: fehler.append(f"Prüfmaske (#67): gelesene Überschriften {gel}")
    if "z-niedrig" not in kl0('[data-sitz="2"]') or "z-niedrig" in kl0('[data-sitz="0"]'): fehler.append("Prüfmaske (#67): nicht erkannte Überschrift nicht markiert")
    if "Spalte 3: Überschrift „Bn“ nicht erkannt" not in pg.inner_text("#entwurf"): fehler.append("Prüfmaske (#67): Hinweis zur nicht erkannten Überschrift fehlt")
    v0 = zahlen0()
    assert pg.input_value('[data-solo="16"]') == "Anna|p", pg.input_value('[data-solo="16"]')
    # Namen oben ändern: ein Feld reicht – steht der Name schon über einer anderen Spalte, tauschen die beiden; alles andere bleibt in der Spalte
    pg.select_option('[data-sitz="0"]', "Anna"); pg.wait_for_timeout(100)
    o1 = oben()
    if kopf() != ["Anna", "David", "Ben", "Clara"] or kopftext() != ["Ann", "Dav", "Ben", "Cla"]: fehler.append(f"Name oben (#67): Spaltenköpfe {kopf()} {kopftext()}")
    if [x[0] for x in o1] != ["Anna", "David", "Ben", "Clara"] or any(x[0] != x[1] or x[0] != x[3] for x in o1): fehler.append(f"Name oben (#67): Spalten oben {o1}")
    if [(x[2], x[4]) for x in o1] != [(x[2], x[4]) for x in o0]: fehler.append(f"Name oben (#67): Endstand oder Platz sind gewandert {o1} statt {o0}")
    if zahlen0() != v0: fehler.append(f"Name oben (#67): Zahlen sind gewandert {zeile0()} statt {v0}")
    if namen0() != ["Anna", "David", "Ben", "Clara"]: fehler.append(f"Name oben (#67): Spalten gehören nicht den neuen Namen {zeile0()}")
    if pg.input_value('[data-solo="16"]') != "David|p": fehler.append(f"Name oben (#67): Solo der Spalte nicht mitgewechselt: {pg.input_value('[data-solo=\"16\"]')}")
    if "Tabelle stimmt" not in pg.inner_text("#e-pruef"): fehler.append("Name oben (#67): nach dem Umbenennen geht die Tabelle nicht mehr auf: " + pg.inner_text("#e-pruef")[:200])
    if "Anna 7,50" not in pg.inner_text("#e-kasse") or "David 5,00" not in pg.inner_text("#e-kasse"): fehler.append("Name oben (#67): Kasse folgt dem Platz der Spalte nicht: " + pg.inner_text("#e-kasse"))
    pg.evaluate("document.querySelector('#entwurf details').open = true"); pg.wait_for_timeout(2500)
    pg.evaluate("document.querySelector('nav.unten').style.visibility = 'hidden'"); pg.locator("#entwurf .karte").screenshot(path=OUT / "10-spalten-bleiben.png"); pg.evaluate("document.querySelector('nav.unten').style.visibility = ''")
    pg.select_option('[data-sitz="0"]', "David"); pg.wait_for_timeout(100)
    assert kopf() == ["David", "Anna", "Ben", "Clara"] and zahlen0() == v0 and namen0() == ["David", "Anna", "Ben", "Clara"], zeile0()
    assert oben() == o0 and pg.input_value('[data-solo="16"]') == "Anna|p", oben()
    # Prüfen wie ein Sudoku (#38): Farben je Sicherheit, blau = bestätigt, grasgrün = folgt logisch, Widerspruch nur als Vorschlag
    assert pg.evaluate("typeof window.aufloesen") == "function", "aufloesen nicht freigelegt"
    pg.evaluate("document.querySelector('#entwurf details').open = true")
    kl = lambda sel: pg.eval_on_selector(sel, "e => e.className")
    assert "z-niedrig" in kl('[data-sp="6"][data-s="Clara"]'), kl('[data-sp="6"][data-s="Clara"]')
    assert "z-mittel" in kl('[data-sp="2"][data-s="Anna"]') and "z-hoch" in kl('[data-sp="0"][data-s="Ben"]')
    assert "Tabelle stimmt" in pg.inner_text("#e-pruef"), pg.inner_text("#e-pruef")[:300]
    def drueck(sel):
        pg.eval_on_selector(sel, "e => e.scrollIntoView({block: 'center'})")  # nicht unter der Navigation unten
        bb = pg.locator(sel).bounding_box()
        pg.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2); pg.mouse.down(); pg.wait_for_timeout(700); pg.mouse.up(); pg.wait_for_timeout(150)
    # drei Werte einer Zeile bestätigen → der vierte folgt logisch (grasgrün)
    for s in ["Ben", "Clara", "David"]: drueck(f'[data-sp="1"][data-s="{s}"]')
    assert "z-blau" in kl('[data-sp="1"][data-s="Ben"]'), kl('[data-sp="1"][data-s="Ben"]')
    assert "z-gruen" in kl('[data-sp="1"][data-s="Anna"]'), kl('[data-sp="1"][data-s="Anna"]')
    # Widerspruch: bestätigter Wert passt nicht zum gelesenen → rot, nur Vorschlag
    pg.fill('[data-sp="0"][data-s="Ben"]', "5"); pg.dispatch_event('[data-sp="0"][data-s="Ben"]', "change")
    for s in ["Clara", "David"]: drueck(f'[data-sp="0"][data-s="{s}"]')
    assert "z-rot" in kl('[data-sp="0"][data-s="Anna"]'), kl('[data-sp="0"][data-s="Anna"]')
    assert pg.input_value('[data-sp="0"][data-s="Anna"]') == "-4", "gelesener Wert wurde ersetzt"
    t = pg.inner_text("#e-pruef"); assert "Gelesen ≠ logisch" in t and "logisch -5" in t, t[:300]
    pg.click('[data-nimm="0|Anna"]'); pg.wait_for_timeout(150)
    assert "z-blau" in kl('[data-sp="0"][data-s="Anna"]') and pg.input_value('[data-sp="0"][data-s="Anna"]') == "-5"
    # zurück auf den Zettel: Ben 4, Anna −4 → wieder stimmig
    pg.fill('[data-sp="0"][data-s="Ben"]', "4"); pg.dispatch_event('[data-sp="0"][data-s="Ben"]', "change")
    pg.fill('[data-sp="0"][data-s="Anna"]', "-4"); pg.dispatch_event('[data-sp="0"][data-s="Anna"]', "change")
    assert "Tabelle stimmt" in pg.inner_text("#e-pruef"), pg.inner_text("#e-pruef")[:300]
    # Endstand verstellen → Gesamtprüfung meldet es
    pg.fill('[data-end="Anna"]', "9"); pg.dispatch_event('[data-end="Anna"]', "change")
    assert "aus den Spielen ergibt sich 4" in pg.inner_text("#e-pruef"), pg.inner_text("#e-pruef")[:300]
    pg.fill('[data-end="Anna"]', "4"); pg.dispatch_event('[data-end="Anna"]', "change")
    assert "Tabelle stimmt" in pg.inner_text("#e-pruef")
    # alle sicheren auf einmal bestätigen
    pg.click("#e-hell-ok"); pg.wait_for_timeout(150)
    assert "z-blau" in kl('[data-sp="5"][data-s="Ben"]') and "z-blau" not in kl('[data-sp="6"][data-s="Clara"]')
    pg.evaluate("document.querySelector('#entwurf details').open = true"); pg.screenshot(path=OUT / "2-entwurf.png", full_page=True)
    # Spalte „Spiel“ in der Prüfmaske (#66): von der App gerechnet (Unterschied zur Zeile darüber), nicht zum Tippen,
    # Solos als Paar wie „3/-1“; ohne Scrollbalken bei 360–412 px; gespeichert wird der gerechnete Wert
    if pg.locator("td[data-spielwert]").count() != 20: fehler.append(f"Prüfmaske: {pg.locator('td[data-spielwert]').count()} Felder Spiel statt 20")
    if pg.locator("input[data-spielwert], td[data-spielwert] input").count(): fehler.append("Prüfmaske (#66): Spalte Spiel ist noch zum Tippen")
    spw = lambda i: (pg.text_content(f'td[data-spielwert="{i}"]') or "").strip()
    for i, w in [(0, "4"), (5, "1"), (12, "2"), (16, "6/-2"), (17, "9/-3"), (18, "3/-1"), (19, "6/-2")]:
        if spw(i) != w: fehler.append(f"Prüfmaske (#66): Spiel {i + 1} zeigt „{spw(i)}“ statt „{w}“")
    if pg.locator("td.spiel-falsch").count(): fehler.append(f"Prüfmaske (#66): {pg.locator('td.spiel-falsch').count()} Spielwerte rot, obwohl alles aufgeht")
    lauf = pg.evaluate("""window.spielwerte({spieler: ['A','B','C','D'], format: 'laufend', zeilen: [
        {werte: {A: 1, B: 1, C: -1, D: -1}}, {werte: {A: 7, B: -1, C: -3, D: -3}, solo: 'A'}, {werte: {A: 8, B: -4, C: -2, D: -2}, solo: 'B'},
        {werte: {A: 8, B: -4, C: -2, D: -2}}, {werte: {A: 8, B: -4, C: -2, D: 0}}, {werte: {A: '', B: -4, C: -2, D: 0}}]})""")
    soll = [("1", 1, False), ("6/-2", 2, False), ("-3/1", 1, False), ("0", 0, False), ("2", None, True), ("", None, False)]
    if [(r["text"], r["wert"], r["falsch"]) for r in lauf] != soll: fehler.append(f"spielwerte (#66, laufende Summe): {lauf}")
    for b in (360, 390, 412):
        pg.set_viewport_size({"width": b, "height": 844})
        w, c = pg.evaluate("(() => { const e = document.querySelector('#entwurf .rollen'); return [e.scrollWidth, e.clientWidth]; })()")
        if w > c: fehler.append(f"Prüfmaske bei {b} px zu breit: {w}/{c}")
    pg.set_viewport_size({"width": 390, "height": 844})
    # Spiel streichen (#69): ✕ je Zeile, gestrichen = grau und durchgestrichen, Prüfung ohne die Zeile, zurückholen mit nochmal ✕
    if pg.locator("[data-streich]").count() != 20: fehler.append(f"Prüfmaske: {pg.locator('[data-streich]').count()} Knöpfe ✕ statt 20")
    pg.eval_on_selector('[data-streich="1"]', "e => e.scrollIntoView({block: 'center'})"); pg.click('[data-streich="1"]'); pg.wait_for_timeout(150)
    assert "gestrichen" in kl('tr[data-zeile="1"]'), kl('tr[data-zeile="1"]')
    assert pg.is_disabled('[data-sp="1"][data-s="Anna"]'), "gestrichene Zeile noch änderbar"
    t = pg.inner_text("#e-pruef")
    assert "Gestrichen: Spiel 2" in t and "aus den Spielen ergibt sich 1" in t, t[:400]   # Anna 4 − 3: Endstand passt ohne Spiel 2 nicht mehr
    pg.wait_for_timeout(2500); pg.evaluate("document.querySelector('nav.unten').style.visibility = 'hidden'"); pg.locator("#entwurf .karte").screenshot(path=OUT / "8-gestrichen.png"); pg.evaluate("document.querySelector('nav.unten').style.visibility = ''")   # ohne Hinweis-Blase und Navigation
    pg.click('[data-streich="1"]'); pg.wait_for_timeout(150)
    assert "gestrichen" not in kl('tr[data-zeile="1"]') and "Tabelle stimmt" in pg.inner_text("#e-pruef"), pg.inner_text("#e-pruef")[:300]
    # Zeile, die nicht aufgeht (#70): neu geprüft beim Ändern, nur markiert (Nummer rot), Speichern bleibt möglich
    pg.fill('[data-sp="3"][data-s="Ben"]', "2"); pg.dispatch_event('[data-sp="3"][data-s="Ben"]', "change")
    assert "zeile-falsch" in kl('tr[data-zeile="3"]') and "Spiel 4 ergibt zusammen 4 statt 0" in pg.inner_text("#e-pruef"), pg.inner_text("#e-pruef")[:300]
    if "spiel-falsch" not in kl('td[data-spielwert="3"]'): fehler.append("Prüfmaske (#66): Spielwert einer Zeile, die nicht aufgeht, ist nicht rot")
    pg.evaluate("document.querySelector('nav.unten').style.visibility = 'hidden'"); pg.locator("#entwurf .karte").screenshot(path=OUT / "9-zeile-falsch.png"); pg.evaluate("document.querySelector('nav.unten').style.visibility = ''")
    pg.fill('[data-sp="3"][data-s="Ben"]', "-2"); pg.dispatch_event('[data-sp="3"][data-s="Ben"]', "change")
    assert "zeile-falsch" not in kl('tr[data-zeile="3"]') and "spiel-falsch" not in kl('td[data-spielwert="3"]')
    # Plätze aus den Zeilen (#70): andere Plätze eingetragen → Nachfrage, „Abbrechen“ speichert nicht
    assert pg.evaluate("window.plaetzeAusZeilen({spieler:['A','B'],format:'laufend',spiele:[{werte:{A:1,B:-1}},{werte:{A:3,B:-3}}],plaetze:{A:1,B:2}})") is None
    assert pg.evaluate("window.plaetzeAusZeilen({spieler:['A','B'],format:'laufend',spiele:[{werte:{A:2,B:2}}],plaetze:{A:2,B:1}})") is None, "Gleichstand (Stechen) darf nicht warnen"
    assert "andere Plätze" in (pg.evaluate("window.plaetzeAusZeilen({spieler:['A','B'],format:'einzeln',spiele:[{werte:{A:1,B:-1}},{werte:{A:3,B:-3}}],plaetze:{A:2,B:1}})") or "")
    pg.select_option('[data-platz="Ben"]', "2"); pg.select_option('[data-platz="Anna"]', "1")
    ablehnen["plaetze"] = True; n0 = len(dialoge)
    pg.click("#e-ok"); pg.wait_for_timeout(400)
    if not any("andere Plätze" in m for m in dialoge[n0:]): fehler.append(f"Keine Nachfrage bei falschen Plätzen: {dialoge[n0:]}")
    if not pg.locator("#e-ok").count(): fehler.append("Nach „Abbrechen“ trotzdem gespeichert")
    ablehnen["plaetze"] = False
    pg.select_option('[data-platz="Ben"]', "1"); pg.select_option('[data-platz="Anna"]', "2")
    n0 = len(dialoge)
    pg.click("#e-ok"); pg.wait_for_selector("#s-abende.an")
    if any("andere Plätze" in m for m in dialoge[n0:]): fehler.append("Nachfrage, obwohl die Plätze passen")
    pg.wait_for_selector(".abend >> text=25.10.2026")
    assert "205" in pg.inner_text(".abend >> nth=0")
    pg.screenshot(path=OUT / "3-abende.png")
    # Details
    pg.click(".abend >> nth=0"); pg.wait_for_selector("#d-weg"); pg.wait_for_timeout(400)
    pg.click("#dlg summary"); t = pg.inner_text("#dlg")
    for w in ["Sitzordnung David → Anna → Ben → Clara", "Pflichtsolo David", "Lustsolo Anna", "Pflichtsolo Anna"]:
        if w not in t: fehler.append(f"Abend-Ansicht ohne: {w}")
    pg.screenshot(path=OUT / "4-abend.png", full_page=False); pg.click("[data-zu]")
    # Statistik
    pg.click("nav.unten button[data-s=statistik]"); pg.select_option("#stat-jahr", "2026")
    t = pg.inner_text("#s-statistik"); assert "2026: 14 Abende" in t and "Details aus den Zetteln · 1 Abend" in t and "mit einzelnen Spielen" not in t, t[:400]
    pg.screenshot(path=OUT / "5-statistik.png", full_page=True)
    pg.select_option("#stat-jahr", "2025"); pg.check('#stat-seit')
    assert "Seit 2025: 29 Abende" in pg.inner_text("#stat"), pg.inner_text("#stat")[:120]
    pg.uncheck('#stat-seit'); assert "2025: 15 Abende" in pg.inner_text("#stat")
    # KI
    pg.click("nav.unten button[data-s=fragen]"); pg.fill("#ki-text", "Am 9.10. war Ben Erster")
    pg.click("#ki-senden"); pg.wait_for_selector("[data-v]")
    t = pg.inner_text("#s-fragen")
    if pg.locator("[data-v]").count() != 2: fehler.append(f"KI: {pg.locator('[data-v]').count()} Vorschläge statt 2 (unbekannter Abend / falsches Datum nicht weggelassen)")
    for w in ["2 Vorschläge passten nicht", "Noch ist nichts geändert"]:
        if w not in t: fehler.append(f"KI-Antwort ohne: {w}")
    pg.click("[data-v='1:0']"); pg.wait_for_selector("text=✓ übernommen")
    pg.click("[data-v='1:1']"); pg.wait_for_timeout(500)
    pg.screenshot(path=OUT / "6-ki.png", full_page=True)
    # Rückmeldung, die GitHub ablehnt: Grund und Text landen im Protokoll, ohne Schlüssel (#65)
    pg.fill("#fb-text", "Test: Rückmeldung bei abgelehntem Schlüssel"); pg.click("#fb-senden")
    pg.wait_for_selector("text=Der Grund steht im Verlauf unter Protokoll")
    # Löschen
    pg.click("nav.unten button[data-s=abende]"); pg.click(".abend >> nth=0"); pg.wait_for_selector("#d-weg"); pg.click("#d-weg")
    pg.wait_for_timeout(700); assert "204 Abende" in pg.inner_text("#hallo"), pg.inner_text("#hallo")
    # #67: Antwort mit kleinen Formfehlern wird ausgebessert, falsches Jahr gibt einen Hinweis (ohne das Datum zu ändern)
    import urllib.request, json as _jj
    b = io.BytesIO(); Image.new("RGB", (400, 300), "white").save(b, "JPEG", comment=b"DOKO-TEST-KAPUTT")
    rand = "----dokotest"; koerper = (f"--{rand}\r\nContent-Disposition: form-data; name=\"foto\"; filename=\"z.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n").encode() + b.getvalue() + f"\r\n--{rand}--\r\n".encode()
    rq = urllib.request.Request(URL + "api.php?a=auslesen", data=koerper, headers={"Content-Type": f"multipart/form-data; boundary={rand}", "X-Doko-Schluessel": "testschluessel"})
    ent = _jj.loads(urllib.request.urlopen(rq).read())["entwurf"]; h = " | ".join(ent["hinweise"])
    if len(ent["spiele"]) != 20: fehler.append(f"Ausbessern (#67): {len(ent['spiele'])} Spiele statt 20")
    if ent["datum"] != "2016-10-25": fehler.append(f"Ausbessern (#67): Datum geändert auf {ent['datum']} (soll bleiben wie gelesen)")
    for w in ["Datum: gelesen 25.10.2016", "Gemeint ist wohl der 25.10.2026", "Antwort der KI ausgebessert: überzähliges Komma entfernt", "Pluszeichen vor Zahlen entfernt"]:
        if w not in h: fehler.append(f"Ausbessern (#67): Hinweis fehlt: {w} – {h[:300]}")
    # Verlauf
    pg.goto(URL + "verlauf.html"); pg.wait_for_selector("[data-zurueck]")
    t = pg.inner_text("main")
    if "20 Spiele erkannt (beim zweiten Versuch; 1. Versuch: abgeschnitten)" not in t: fehler.append("Verlauf ohne: zweiter Versuch nach abgeschnittener Antwort (#67)")
    for w in ["1. Versuch: abgeschnitten – Ende fehlt) · Anfang:", " · Ende: ", "(ausgebessert: überzähliges Komma entfernt"]:
        if w not in t: fehler.append(f"Verlauf ohne: {w} (#67)")
    for w in ["Abend erfasst", "Vorschlag aus dem KI-Feld", "Termin eingetragen", "Papierkorb gelegt", "fragte"]:
        if w not in t: fehler.append(f"Verlauf ohne: {w}")
    for w in ["Rückmeldung nicht abgelegt – GitHub antwortete mit 401: Bad credentials", "Test: Rückmeldung bei abgelehntem Schlüssel"]:
        if w not in t: fehler.append(f"Verlauf ohne: {w}")
    if "testgh" in t: fehler.append("Verlauf zeigt den GitHub-Schlüssel")
    pg.screenshot(path=OUT / "7-verlauf.png", full_page=True)
    pg.click("[data-zurueck]"); pg.wait_for_selector("#papierkorb >> text=Leer.")
    # Downloads
    assert "Zuletzt gesichert am 25.10.2026" in pg.inner_text("#sicherung"), pg.inner_text("#sicherung")
    with pg.expect_download() as dl: pg.click("#dl-excel")
    xp = OUT / "export.xlsx"; dl.value.save_as(xp)
    import openpyxl
    wb = openpyxl.load_workbook(xp); ws = wb["Dokoergebnisse"]
    if ws["C4"].value.date().isoformat() != "2015-01-26" or ws["D4"].value != 4: fehler.append(f"Excel: erste Zeile falsch {ws['C4'].value} {ws['D4'].value}")
    werte = [[c.value for c in r] for r in ws.iter_rows()]
    if not any(r[1] == "Gesamt" for r in werte): fehler.append("Excel: keine Gesamt-Zeile")
    if wb["Spiele"].max_row != 21: fehler.append(f"Excel: Spiele-Blatt hat {wb['Spiele'].max_row} Zeilen")
    wb2 = openpyxl.load_workbook(xp, data_only=True)
    g = [r for r in wb2["Dokoergebnisse"].iter_rows(values_only=True) if r[1] == "Gesamt"][0]
    if g[0] != 205: fehler.append(f"Excel: Gesamt {g[0]}")
    with pg.expect_download() as dl: pg.click("#dl-json")
    jp = OUT / "export.json"; dl.value.save_as(jp)
    import json as _j
    if len(_j.loads(jp.read_text())["abende"]) != 205: fehler.append("JSON: Anzahl Abende")
    _sp = [a for a in _j.loads(jp.read_text())["abende"] if a.get("spiele")]
    if not _sp or _sp[0]["spiele"][16].get("wert") != 2 or _sp[0]["spiele"][0].get("wert") != 4: fehler.append(f"Gerechneter Spielwert nicht gespeichert (#66): {[_sp[0]['spiele'][i] for i in (0, 16)] if _sp else None}")
    pg.goto(URL); pg.wait_for_selector("#hallo:has-text('205 Abende')")
    # Eigene Farbe
    pg.click("#meine-farbe"); pg.click('.muster button[data-c="#d94c3d"]'); pg.click("#f-ok"); pg.wait_for_timeout(800)
    pg.click("nav.unten button[data-s=abende]")
    bg = pg.eval_on_selector('.chip[data-p="Clara"]', "e => getComputedStyle(e).backgroundColor")
    assert bg == "rgb(217, 76, 61)", bg
    # Statistik: Namen oben und unten in der Personenfarbe, ohne Scrollbalken bei 360–412 px
    pg.click("nav.unten button[data-s=statistik]"); pg.select_option("#stat-jahr", "2026")
    for sel in ['#stat .chip[data-p="Clara"]', '#stat-details .chip[data-p="Clara"]']:
        bg = pg.eval_on_selector(sel, "e => getComputedStyle(e).backgroundColor")
        if bg != "rgb(217, 76, 61)": fehler.append(f"Statistik {sel}: Farbe {bg}")
    for b in (360, 390, 412):
        pg.set_viewport_size({"width": b, "height": 844})
        m = pg.evaluate("['#stat', '#stat-details'].map(s => { const e = document.querySelector(s + ' .rollen'); return s + ' ' + e.scrollWidth + '/' + e.clientWidth; })")
        for x in m:
            w, c = map(int, x.split()[1].split("/"))
            if w > c: fehler.append(f"Statistik bei {b} px zu breit: {x}")
        if b == 390: pg.screenshot(path=OUT / "5b-statistik-farben.png", full_page=True)
    pg.set_viewport_size({"width": 390, "height": 844})
    # Personenwechsel per Link wird gemeldet; ohne gültigen Schlüssel gesperrt
    pg.goto("about:blank"); pg.goto(URL + "#k=falsch"); pg.wait_for_selector("text=Kein Zugang")
    assert pg.evaluate("localStorage.getItem('doko-k')") is None, "falscher Schlüssel bleibt gespeichert"
    pg.goto("about:blank"); pg.goto(URL); pg.wait_for_selector("text=Kein Zugang")
    pg.goto("about:blank"); pg.goto(URL + "#k=testschluessel"); pg.wait_for_selector("#hallo:has-text('Hallo Clara')")
    pg.click("#meine-farbe"); pg.click("#f-ab"); pg.wait_for_selector("text=Kein Zugang")
    pg.goto("about:blank"); pg.goto(URL + "#k=testschluessel"); pg.wait_for_selector("#hallo:has-text('Hallo Clara')")
    # Dunkel
    pg.emulate_media(color_scheme="dark"); pg.click("nav.unten button[data-s=abende]"); pg.screenshot(path=OUT / "8-dunkel.png")
    br.close()

print("\n".join(fehler) if fehler else "ALLES OK")
sys.exit(1 if fehler else 0)
