#!/usr/bin/env python3
"""Durchlauf-Test des Blogs gegen den lokalen Testserver (tests/lokal.sh) – Lesen, Serien, Feeds, Editor, Vorschau.

Aufruf:  bash tests/lokal.sh /tmp/blog && python3 tests/e2e.py /tmp/blog-bilder [/tmp/blog]
Endet mit „ALLES OK“. Bildschirmfotos (Handy 390×844, hell und dunkel, Entwürfe A/B/C) landen im angegebenen Ordner.
"""
import json, os, subprocess, sys, time, urllib.error, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
from playwright.sync_api import sync_playwright

PORT = int(os.environ.get("BLOG_TESTPORT", "8770"))          # lokal.sh mit demselben Port starten; Vorschau und Start-Test: PORT+1, PORT+2
BASIS = f"http://127.0.0.1:{PORT}/"
B2, B3 = f"http://127.0.0.1:{PORT + 1}/", f"http://127.0.0.1:{PORT + 2}/"
BILDER = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/blog-bilder"); BILDER.mkdir(parents=True, exist_ok=True)
ARBEIT = Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/blog")
HIER = Path(__file__).resolve().parent.parent
fehler = []


def pruefe(bed, text):
    print(("  ok  " if bed else "  FEHLER  ") + text)
    if not bed: fehler.append(text)


def hole(pfad, daten=None, kopf=None, basis=BASIS):
    req = urllib.request.Request(basis + pfad, data=json.dumps(daten).encode() if daten is not None else None,
                                 headers={"Content-Type": "application/json", **(kopf or {})}, method="POST" if daten is not None else "GET")
    class KeinFolgen(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    try:
        r = urllib.request.build_opener(KeinFolgen).open(req, timeout=10)
        return r.status, r.read().decode(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(), dict(e.headers)


print("Lesen")
s, t, _ = hole("")
pruefe(s == 200 and t.count('class="karte"') == 4, "Startseite zeigt 4 veröffentlichte Beiträge")
pruefe("Noch geheim" not in t, "Entwurf erscheint nicht")
pruefe("3 Teile" in t and "Leere Serie" not in t, "Serien-Kasten: Garten mit 3 Teilen, leere Serie ausgeblendet")
s, t, _ = hole("der-kompost/")
pruefe("Teil 2 von 3" in t, "Beitrag kennt seinen Platz in der Serie")
pruefe('href="/tomaten-im-oktober/"' in t and 'href="/schnecken/"' in t, "Vor/Zurück zeigen auf Teil 1 und 3")
pruefe("<li>Kaffeesatz</li>" in t and "<em>Gold</em>" in t, "Markdown: Liste und Kursiv")
s, t, _ = hole("tomaten-im-oktober/")
pruefe('<img src="/bilder/import/testbild.png"' in t, "Eigenes Bild wird eingebunden")
pruefe('rel="noopener"' in t and "Altes Blog" in t, "Fremder Link mit noopener, Hinweis auf alte Quelle")
pruefe('hreflang="en"' in t, "Geprüfte englische Fassung ist verlinkt")
pruefe('<a href="/tomaten-im-oktober/">den Tomaten</a>' in hole("ein-buch/")[1], "Interner Link beitrag:… zeigt auf den Beitrag")
s, t, _ = hole("serie/gedanken-zum-garten/")
pruefe(s == 200 and "Von vorne lesen" in t and t.count("<li>") >= 3 and "Gemüsebeet" in t, "Serienseite mit Einleitung, Von vorne lesen, 3 Teilen")
s, t, _ = hole("stichwort/garten/")
pruefe(s == 200 and t.count('class="karte"') == 2, "Stichwort-Seite zeigt 2 Beiträge")
pruefe(hole("noch-geheim/")[0] == 404 and hole("gibt-es-nicht/")[0] == 404, "Entwurf und Unbekanntes geben 404")
s, t, _ = hole("<script>/")
pruefe(s == 404 and "<script>" not in t, "Seltsame Adressen werden nicht ausgegeben")

print("Englisch")
s, t, _ = hole("en/")
pruefe(s == 200 and t.count('class="karte"') == 1 and "Tomatoes in October" in t, "en/ zeigt nur die geprüfte Übersetzung")
s, t, h = hole("en/der-kompost/")
pruefe(s == 302 and h.get("Location", "").endswith("/der-kompost/"), "Ungeprüftes Englisch leitet auf Deutsch um")
s, t, _ = hole("en/tomaten-im-oktober/")
pruefe("Part 1 of 1" in t and "Thoughts on the Garden" in t, "Englische Serien-Zählung nur über geprüfte Teile")

print("Feeds")
ns = {"a": "http://www.w3.org/2005/Atom"}
s, t, h = hole("feed.xml")
f = ET.fromstring(t)
eintraege = f.findall("a:entry", ns)
pruefe(s == 200 and "atom" in h.get("Content-Type", ""), "Feed liefert Atom")
pruefe(len(eintraege) == 4, f"Feed DE hat 4 Einträge ({len(eintraege)})")
labels = [c.get("label") for e in eintraege for c in e.findall("a:category", ns) if c.get("label")]
pruefe("Gedanken zum Garten · Teil 2 von 3" in labels, "Serie und Teil stehen als Kategorie im Feed")
inhalt = " ".join(e.find("a:content", ns).text or "" for e in eintraege)
pruefe('src="http://127.0.0.1:8770/bilder/import/testbild.png"' in inhalt, "Bilder im Feed mit voller Adresse")
s, t, _ = hole("en/feed.xml")
pruefe(len(ET.fromstring(t).findall("a:entry", ns)) == 1, "Feed EN hat nur den geprüften Beitrag")

print("Schutz")
pruefe(hole("api.php?a=liste", {})[0] == 401, "Editor-Schnittstelle ohne Schlüssel: 401")
pruefe(hole("api.php?a=liste", {}, {"X-Blog-Schluessel": "falsch"})[0] == 401, "falscher Schlüssel: 401")
s, t, _ = hole("rueckmeldung.php", {"text": "Hallo Test", "art": "fehler"})
pruefe(s == 503 and "nicht eingerichtet" in t, "Rückmeldung ohne GitHub-Schlüssel meldet sich verständlich")
pruefe(hole("lib.php")[0] in (403, 404, 200) and "<?php" not in hole("lib.php")[1], "lib.php gibt keinen Quelltext preis")

print("Editor")
with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={"width": 390, "height": 844}, locale="de-DE", color_scheme="light")
    pg = ctx.new_page()
    pg.on("dialog", lambda d: d.accept())
    pg.goto(BASIS + "editor/#k=testschluessel")
    pg.wait_for_selector(".liste li")
    pruefe(pg.locator(".liste li").count() == 5, "Editor listet alle 5 Beiträge (mit Entwurf)")
    pg.screenshot(path=str(BILDER / "editor-liste.png"))
    pg.click("#neu")
    pg.fill("#titel", "Der erste Frost")
    pg.select_option("#serie", "gedanken-zum-garten")
    pruefe(pg.get_attribute("#datum", "type") == "date" and pg.get_attribute("#zeit", "type") == "time", "Editor: Datum und Zeit als eigene Wähler")
    pruefe(pg.evaluate("document.querySelector('#serie').getBoundingClientRect().top === document.querySelector('#datum').getBoundingClientRect().top"), "Editor: Serie, Datum und Zeit in einer Zeile")
    pg.fill("#stichwoerter", "gar")
    pruefe(pg.locator("#sw-vorschlaege button[data-w=Garten]").count() == 1, "Editor: schlägt schon verwendete Stichwörter vor")
    pg.click("#sw-vorschlaege button[data-w=Garten]")
    pruefe(pg.input_value("#stichwoerter") == "Garten, ", "Editor: Vorschlag antippen übernimmt das Stichwort")
    pg.screenshot(path=str(BILDER / "editor-kopf.png"))
    pg.fill("#stichwoerter", "Garten, Winter")
    pg.fill("#zeit", "00:01")
    pg.fill("#text", "Heute Nacht kam der **Frost**.\n\nDie Dahlien sind hin.")
    pg.click("#speichern")
    pg.wait_for_function("document.querySelector('#en-titel') && document.querySelector('#en-titel').value.startsWith('[EN]')", timeout=8000)
    pruefe(pg.input_value("#en-titel") == "[EN] Der erste Frost", "Nach dem Speichern wird automatisch übersetzt")
    gespeichert = json.loads((ARBEIT / "privat/daten/beitraege/der-erste-frost.json").read_text())["datum"]
    pruefe(pg.evaluate(f"(function(d){{return d.getHours()===0&&d.getMinutes()===1}})(new Date({json.dumps(gespeichert)}))"), "Editor: gewählte Zeit wird gespeichert")
    pg.screenshot(path=str(BILDER / "editor-beitrag.png"), full_page=True)
    pg.check("#en-geprueft")
    pg.click("#speichern"); pg.wait_for_timeout(500)
    pg.click("#veroeff"); pg.wait_for_selector("#zurueckziehen", timeout=8000)
    s, t, _ = hole("der-erste-frost/")
    pruefe(s == 200 and "Teil 4 von 4" in t and "<strong>Frost</strong>" in t, "Veröffentlichter Beitrag ist sofort online, als Teil 4 von 4")
    s, t, _ = hole("en/der-erste-frost/")
    pruefe(s == 200 and "[EN] Der erste Frost" in t, "Geprüftes Englisch erscheint unter en/")
    pruefe(len(ET.fromstring(hole("feed.xml")[1]).findall("a:entry", ns)) == 5, "Neuer Beitrag steht im Feed")
    # importierten Beitrag bearbeiten: eigene Fassung, Startbestand bleibt
    pg.click("#zurueck"); pg.wait_for_selector(".liste li")
    pg.click(".liste li:has-text('Schnecken')")
    pg.wait_for_selector("#text")
    pruefe("Übernommen aus" in pg.inner_text("main"), "Editor zeigt Hinweis bei importiertem Beitrag")
    pg.fill("#text", "Die Schnecken waren wieder da.")
    pg.click("#speichern"); pg.wait_for_timeout(800)
    eigen = ARBEIT / "privat/daten/beitraege/schnecken.json"
    alt = ARBEIT / "privat/startbestand/beitraege/schnecken.json"
    pruefe(eigen.exists() and "wieder da" in eigen.read_text() and "Geduld" in alt.read_text(), "Bearbeitung landet als eigene Fassung, Import unangetastet")
    pruefe("wieder da" in hole("schnecken/")[1], "Bearbeitete Fassung ist online")
    # Serien-Ansicht
    pg.click("#zurueck"); pg.wait_for_selector("#serien-knopf"); pg.click("#serien-knopf")
    pg.wait_for_selector(".s-titel")
    pruefe(pg.locator(".kasten").count() == 2, "Serien-Ansicht zeigt beide Serien")
    ctx.close()

    print("Lese-Seiten: Bildschirmfotos")
    for schema in ("light", "dark"):
        c = br.new_context(viewport={"width": 390, "height": 844}, locale="de-DE", color_scheme=schema, device_scale_factor=2)
        q = c.new_page()
        zu_breit = []
        for stil in "abc":
            for pfad, name in (("", "start"), ("der-kompost/", "beitrag"), ("serie/gedanken-zum-garten/", "serie")):
                q.set_viewport_size({"width": 390, "height": 844})
                q.goto(BASIS + pfad)
                q.evaluate(f"document.documentElement.dataset.stil='{stil}'")
                q.screenshot(path=str(BILDER / f"{name}-{stil}-{schema}.png"))
                q.set_viewport_size({"width": 360, "height": 780})
                w = q.evaluate("document.documentElement.scrollWidth")
                if w > 360: zu_breit.append(f"{name}/{stil}: {w}px")
        q.set_viewport_size({"width": 390, "height": 844})
        q.goto(BASIS); q.evaluate("localStorage.removeItem('blog-stil')"); q.goto(BASIS)
        pruefe(q.locator(".stilwahl button").count() == 2 and q.locator(".stilwahl button[data-s=b]").count() == 0, f"Leser: Umschalter Kaffeehaus/digifil im Fuß ({schema})")
        q.click(".stilwahl button[data-s=c]"); q.goto(BASIS + "der-kompost/")
        hell = q.evaluate("(function(){var m=getComputedStyle(document.body).backgroundColor.match(/\\d+/g).map(Number);return m[0]+m[1]+m[2]>384})()")
        pruefe(q.evaluate("document.documentElement.dataset.stil") == "c" and hell == (schema == "light"), f"Leser: digifil bleibt gewählt und folgt dem Gerät ({schema})")
        pruefe("serif" in q.evaluate("getComputedStyle(document.querySelector('.text')).fontFamily") and "sans-serif" not in q.evaluate("getComputedStyle(document.querySelector('.text')).fontFamily"), f"digifil: Text mit Serifen ({schema})")
        q.evaluate("localStorage.removeItem('blog-stil')")
        pruefe(not zu_breit, f"Keine waagerechte Scrollleiste bei 360 px, alle Seiten und Entwürfe ({schema})" + (": " + ", ".join(zu_breit) if zu_breit else ""))
        c.close()
    br.close()

print("Vorschau")
W2 = Path(str(ARBEIT) + "-vorschau")
subprocess.run(["bash", str(HIER / "tests/lokal.sh"), str(W2), str(PORT + 1)], env={**os.environ, "BLOG_VORSCHAU": "1"}, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.5)
s, t, h = hole("", basis=B2)
pruefe("vorschau-schild" in t and "noindex" in t and "noindex" in h.get("X-Robots-Tag", ""), "Vorschau: Schild und nicht in Suchmaschinen")
with sync_playwright() as p:
    br = p.chromium.launch(); q = br.new_page(viewport={"width": 390, "height": 844})
    q.goto(B2 + "der-kompost/"); q.click(".vorschau-schild button[data-s=b]")
    q.goto(B2)
    pruefe(q.evaluate("document.documentElement.dataset.stil") == "b", "Vorschau: gewählter Entwurf bleibt beim Weiterklicken")
    q.screenshot(path=str(BILDER / "vorschau-schild.png")); br.close()
subprocess.run(["bash", "-c", f"for p in $(ps -C php -o pid=,args= | grep {PORT + 1} | awk '{{print $1}}'); do kill $p; done"])

print("Vor dem Start")
W3 = Path(str(ARBEIT) + "-start")
subprocess.run(["bash", str(HIER / "tests/lokal.sh"), str(W3), str(PORT + 2)], env={**os.environ, "BLOG_LIVE": "0"}, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.5)
s, t, h = hole("", basis=B3)
pruefe("bald geht es los" in t and "Tomaten" not in t and "noindex" in h.get("X-Robots-Tag", ""), "Ohne „live“: Leser sehen nur den Platzhalter")
pruefe("Tomaten" not in hole("feed.xml", basis=B3)[1], "Ohne „live“: Feed verrät nichts")
s, t, _ = hole("api.php?a=liste", {}, {"X-Blog-Schluessel": "testschluessel"}, basis=B3)
pruefe(s == 200 and "tomaten-im-oktober" in t, "Ohne „live“: Editor arbeitet schon mit den Daten")
subprocess.run(["bash", "-c", f"for p in $(ps -C php -o pid=,args= | grep {PORT + 2} | awk '{{print $1}}'); do kill $p; done"])

# Testserver von lokal.sh wieder beenden, damit der nächste Lauf einen freien Port findet
subprocess.run(["bash", "-c", f"for p in $(ps -C php -o pid=,args= | grep {PORT} | awk '{{print $1}}'); do kill $p; done"])

print()
if fehler:
    print(f"{len(fehler)} FEHLER:\n  - " + "\n  - ".join(fehler)); sys.exit(1)
print("ALLES OK")
