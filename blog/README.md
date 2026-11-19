# Blog 1.0

<!-- Zwei-Kanal-Format 1.3 (../zwei-kanal-format/): BLOCK A muss allein genügen, BLOCK B ist Klartext für Menschen. -->

## BLOCK A – Auftrag an die einrichtende KI

```text
ZWECK:        Du baust das Blog-Werkzeug aus diesem Ordner, prüfst es lokal und richtest es auf einem eigenen
              PHP-Webspace ein. Fertig ist es, wenn die Tests in Schritt 2 bestehen, die Startseite des Blogs auf dem
              Webspace erscheint und der Editor mit dem eigenen Editor-Link Beiträge speichert.
GILT FÜR:     ein neues Blog auf eigenem Webspace · ein Blog mit übernommenen Beiträgen aus einem Blogger-Blog
              (Blogspot) oder aus einem Projekt-Log in HTML · lokales Ausprobieren mit Testdaten.
GILT NICHT:   Weiterentwickeln des Werkzeugs (Code ändern) – dafür gibt es hier keine Anleitung; die Tests in Schritt 2
              zeigen, ob eine eigene Änderung den Bestand bricht. · Inhalte schreiben – das tut der Mensch im Editor. ·
              Ein Blog ohne Rückmelde-Knopf oder ohne englischen Teil: Beides lässt sich nicht abschalten (VERHALTEN);
              wenn die Aufgabe es verlangt, dann nenne es in der Lieferung als nicht erfüllbar ohne Code-Änderung.
VORAUSSETZUNG: Bauen und Testen: Python ab 3.12 · PHP ab 8.1 als Kommandozeile mit den Erweiterungen curl, mbstring,
              xml (XMLWriter), fileinfo · für die Tests das Python-Paket playwright mit Chromium (liegt Chromium nicht am
              Standardort, setze PLAYWRIGHT_BROWSERS_PATH) · für den Import die Python-Pakete beautifulsoup4 und
              markdownify und Netzzugang zur alten Quelle.
              Betrieb: Webspace mit Apache, mod_rewrite und .htaccess, PHP ab 8.1 mit denselben Erweiterungen · ein
              Ordner außerhalb des Web-Verzeichnisses, in den PHP schreiben darf (privater Ordner) · Upload per SFTP
              oder FTP.
              Freiwillig: ein Mistral-API-Schlüssel (Übersetzung ins Englische) · ein GitHub-Token mit Recht, Issues
              anzulegen, und ein GitHub-Repo (Rückmelde-Knopf).
DATEIEN:      server/index.php (Lese-Seiten und Feeds) · server/api.php (Schnittstelle des Editors) ·
              server/rueckmeldung.php (Rückmelde-Knopf → Issue) · server/lib.php (Laden, Serien, Markdown) ·
              server/.htaccess (leitet alle Adressen auf index.php) · server/einstellungen.example.json (Vorlage der
              Einstellungen) · server/zugaenge.example.json (Vorlage der Editor-Zugänge) · src/blog.css, src/blog.js,
              src/editor.html (Oberfläche) · tools/build.py (baut den Upload-Stand nach dist/) · tools/make_zugang.py
              (erzeugt zugang.php und neue Editor-Links) · tools/import_blogspot.py, tools/import_projektlog.py,
              tools/importhilfe.py (Import) · tools/uebersetze.py (Übersetzung des Imports) · tests/lokal.sh
              (Testserver mit Testdaten) · tests/e2e.py (Durchlauf im Browser) · tests/test_import.py (Import ohne
              Netz) · tests/attrappe/ (Testdaten).
BEGRIFFE:     Web-Ordner = der Ordner auf dem Webspace, unter dem das Blog erreichbar ist (zum Beispiel …/Blog/).
              Privater Ordner = <vorfahr>/privat/<name> außerhalb des Web-Verzeichnisses. <vorfahr> ist ein Ordner, in dem
              der Web-Ordner liegt (hoch Ebenen darüber); <name> ist ohne ort.php immer „blog“, unabhängig vom Namen des
              Web-Ordners. Ohne ort.php gilt hoch = 2: Web-Ordner /web/Blog/ → privater Ordner /privat/blog/. Eine andere
              Ebene oder einen anderen Namen stellst du mit der Datei ort.php im Web-Ordner ein:
              <?php return ['privat' => '<name>', 'hoch' => <ebenen>, 'vorschau' => false];
              (hoch = Ordner-Ebenen vom Web-Ordner hinauf bis zu dem Ordner, der privat/ enthält, 1 bis 5; <name> nur aus
              Buchstaben, Ziffern, _ und -; vorschau = true zeigt ein gelbes Vorschau-Schild und sperrt Suchmaschinen –
              für ein normales Blog false). Ein Ort, der nicht so <vorfahr>/privat/<name> heißt, ist nicht einstellbar;
              wenn die Aufgabe ihn verlangt, dann nenne das in der Lieferung, statt den Ort anders zu erreichen.
              Startbestand = Beiträge, die beim Bauen mitkommen (Ordner mit beitraege/*.json und serien.json; aus dem
              Import). Editor-Daten = was der Editor speichert (<privater Ordner>/daten/); bei gleicher Kennung gilt die
              Editor-Fassung, ein neuer Import überschreibt sie nie.
              Editor-Link = <adresse>editor/#k=<schlüssel>; der Schlüssel steht nur im Link, im Repo und auf dem
              Server liegt nur seine Prüfsumme (SHA-256) in server/zugaenge.json bzw. zugang.php.
              Kennung = Adresse eines Beitrags unter dem Web-Ordner; sie entsteht beim ersten Speichern und ändert
              sich nie.
VERHALTEN:    Lesen: Startseite mit Serien und neuesten Beiträgen, je Beitrag eine Seite, Serienseite mit Einleitung
              und „Von vorne lesen“, in jedem Teil „Teil x von y“ und Vor/Zurück, Stichwort-Seiten. Englisch unter
              …/en/ zeigt nur Beiträge, deren englische Fassung im Editor als geprüft markiert ist.
              Feeds: Atom, …/feed.xml (Deutsch) und …/en/feed.xml (Englisch), je die 30 neuesten Beiträge; Serie und
              Teil als <category term="<serien-kennung>" label="<Serientitel> · Teil 2 von 5">.
              Editor: Entwürfe, Veröffentlichen (sofort sichtbar), Zurückziehen, Papierkorb, Bilder hochladen (werden
              vorher verkleinert und unter <Web-Ordner>/bilder/JJJJ-MM/ abgelegt), Serien anlegen und beschreiben.
              Nach dem Speichern übersetzt Mistral, wenn der Schlüssel eingerichtet ist.
              Texte sind einfaches Markdown ohne eigenes HTML; fremde Bilder werden zu Links, beim Lesen lädt der
              Browser nichts von fremden Servern; kein Tracking, keine Cookies.
              Kopfzeile jeder Seite (bei live = true): Sprache, Serien, Gestaltung, Rückmelde-Knopf und die Links aus der
              Einstellung fusszeile (zum Beispiel Impressum). Im Fuß stehen nur „Feed abonnieren“ und das Fenster der
              Rückmeldung.
              Gestaltung: a, b oder c (Einstellung stil); Leser können in der Kopfzeile zwischen a und c umschalten.
              Rückmelde-Knopf: steht bei live = true immer in der Kopfzeile. Nur mit Einstellung repo UND einem
              GitHub-Token in zugang.php (Schritt 6) legt er ein Issue mit den Labels <label>, rueckmeldung und der Art
              an; fehlt eins von beiden, antwortet er „Rückmeldungen sind gerade nicht eingerichtet“. Englischer Teil: …/en/ und der Sprachwechsel sind immer da; ohne Mistral-Schlüssel wird
              nichts übersetzt, englische Fassungen kann der Mensch dann im Editor selbst schreiben.
              Einstellungen: tools/make_zugang.py baut sie in zugang.php ein; wer eine Einstellung ändert, führt
              make_zugang.py neu aus und lädt zugang.php neu hoch.
              live = false in den Einstellungen: Jede Lese-Adresse (auch feed.xml) zeigt nur eine HTML-Seite „bald geht
              es los“ ohne Fuß und ohne Rückmelde-Knopf, für Suchmaschinen gesperrt; der Editor und api.php arbeiten
              schon.
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Werkzeuge prüfen.** Führe `python3 --version`, `php -v` und `php -m` aus und vergleiche mit VORAUSSETZUNG.
   *Ergebnis:* Python ab 3.12, PHP ab 8.1, und `php -m` listet curl, mbstring, xmlwriter und fileinfo.
2. **Lokal testen.** Im Ordner blog/: `python3 tests/test_import.py`, dann `bash tests/lokal.sh /tmp/blog`, dann
   `python3 tests/e2e.py /tmp/blog-bilder /tmp/blog`. Das erste Argument von e2e.py ist der Ordner für Bildschirmfotos,
   das zweite derselbe Ordner wie bei lokal.sh. Der Testserver nutzt die Ports 8770 bis 8772; die Übersetzung ist im
   Test eine Attrappe, es braucht keinen Schlüssel. Wenn lokal.sh „FEHLER: Port 8770 ist belegt“ meldet, dann beende
   den alten Testserver mit dem Befehl, den die Meldung nennt, und starte erneut.
   lokal.sh baut dist/ mit den Testdaten neu und löscht dabei, was in dist/ lag. Führe Schritt 2 deshalb vor Schritt 6
   aus; wenn du lokal.sh nach Schritt 6 startest, dann wiederhole Schritt 6 vor dem Hochladen.
   *Ergebnis:* „IMPORT OK“ und als letzte Zeile von e2e.py „ALLES OK“. Zum Ansehen startet
   `bash tests/lokal.sh /tmp/blog` den Testserver unter http://127.0.0.1:8770/, den Editor unter
   http://127.0.0.1:8770/editor/#k=testschluessel.
3. **Einstellungen anlegen.** Kopiere server/einstellungen.example.json nach server/einstellungen.json und setze die
   Werte. „Vorgabe“ heißt unten: der Wert aus der Vorlage einstellungen.example.json.

   | Feld | einsetzen |
   |---|---|
   | `name`, `untertitel`, `untertitel_en`, `autor` | Wörter des Menschen, für den du einrichtest. Wenn er für ein Feld keine nennt, dann setze es auf "" (leer) – die Vorgaben sind Beispieltexte; nenne das Feld in der Lieferung als offen. |
   | `adresse` | die öffentliche Adresse des Web-Ordners mit https:// und / am Ende. Wenn sie fehlt, dann bleibt der Schritt offen; ohne sie stehen im Feed falsche Adressen. |
   | `stil` | a, b oder c. Wenn keiner genannt ist, dann gilt a. |
   | `live` | true, wenn Leser das Blog sehen sollen; false für den Platzhalter. Die Vorlage steht auf true – setze den Wert immer ausdrücklich. Wenn nichts genannt ist, dann setze false; nenne es in der Lieferung als offen. |
   | `repo`, `label` | owner/repo und Label für Rückmeldungen als Issues. Wenn kein Repo genannt ist, dann bleibt `repo` leer (der Knopf bleibt sichtbar und meldet „nicht eingerichtet“). Wenn kein Label genannt ist, dann bleibt die Vorgabe. Ohne Token (Schritt 6) bleibt der Knopf „nicht eingerichtet“, auch mit Repo; nenne den Token dann als offen. |
   | `fusszeile` | Liste von Links wie `{"text": "Impressum", "url": "…"}`. Wenn keine genannt sind, dann bleibt sie leer; nenne das Impressum in der Lieferung als offen. |
   | `quellen_namen` | Name je Import-Quelle für „Ursprünglich erschienen auf …“ (Schlüssel `blogspot`, `projektlog`). Wenn kein Name genannt ist, dann bleibt die Vorgabe. |

   *Ergebnis:* `python3 -c "import json; json.load(open('server/einstellungen.json'))"` meldet keinen Fehler.
4. **Editor-Zugang erzeugen.** Führe je Person `python3 tools/make_zugang.py --neu <Name>` aus. Die Ausgabe nennt den
   Schlüssel und eine Zeile `"<prüfsumme>": "<Name>"`. Trag diese Zeile in server/zugaenge.json ein; die Datei ist ein
   JSON-Objekt, also `{"<prüfsumme>": "<Name>"}`, mehrere Zeilen mit Komma getrennt. Den Editor-Link baust du als
   `<adresse>editor/#k=<schlüssel>`. Gib ihn dem Menschen, für den du einrichtest, direkt im Gespräch; in die Lieferung,
   in Dateien oder in ein Repo kommt er nicht.
   Wenn die Aufgabe keine Person nennt, dann frag nach ihr; ohne Zugang lässt sich das Blog nicht bedienen, und
   Schritt 6 verlangt mindestens einen.
   *Ergebnis:* server/zugaenge.json enthält je Person eine Prüfsumme aus 64 Zeichen; der Schlüssel steht in keiner Datei.
5. **Beiträge übernehmen (nur wenn ein altes Blog übernommen wird).** Lege einen Ordner für den Startbestand neben dem
   Ordner blog/ an, zum Beispiel ../meinblog-start/ (er gehört nicht in ein öffentliches Repo), und darin quellen.json. Für ein Blogger-Blog:
   `{"blogspot": {"adresse": "https://<name>.blogspot.com/"}}`. Für ein Projekt-Log in HTML (Überschriften
   „Log 12 — Titel“): `{"projektlog": {"seiten": ["<adresse der seite>", …], "autor_muster": "<name des autors>"}}`.
   `seiten` ist eine Liste aller Seiten des Logs (auch Archivseiten). `autor_muster` ist Pflicht: Übernommen werden nur
   Einträge, deren Kopfzeile diesen Namen nennt; ist es leer, übernimmt der Import still null Einträge. Wenn die Aufgabe
   keinen Autor nennt, dann frag danach. Weitere freiwillige Felder (Serie, abzuschneidende Anmerkungen) stehen im Kopf
   von tools/import_projektlog.py. Führe
   dann aus: `python3 tools/import_blogspot.py <ordner>` bzw. `python3 tools/import_projektlog.py <ordner>`, danach
   – wenn ein Mistral-Schlüssel da ist – `MISTRAL_API_KEY=<schlüssel> python3 tools/uebersetze.py <ordner>`.
   Serien erkennt der Import an Titeln der Form „Name (7) – Titel“; Bilder werden kopiert; übersetzte Fassungen
   sind ungeprüft und erscheinen erst nach dem Haken im Editor.
   Wenn der Import mit einem Python-Fehler wie URLError abbricht (kein Netz, Adresse falsch), dann nenne den Import in
   der Lieferung als offen und baue in Schritt 6 ohne Import weiter.
   *Ergebnis:* `<ordner>/beitraege/` enthält je Beitrag eine JSON-Datei; die Importe schreiben einen Bericht
   (bericht-blogspot.md bzw. bericht-projektlog.md) in den Ordner.
6. **Bauen.** Ohne Import: `python3 tools/build.py`. Mit Import: `python3 tools/build.py --startbestand <ordner>`.
   Dann erzeuge die Zugangsdatei: `MISTRAL_API_KEY=<schlüssel> BLOG_GITHUB_TOKEN=<token> python3 tools/make_zugang.py
   dist/zugang.php` – beide Variablen sind freiwillig.
   dist/zugang.php enthält die Schlüssel: Lösch dist/ nach dem Hochladen, und leg dist/ nie in ein Repo.
   *Ergebnis:* build.py meldet „dist/ gebaut: N Beiträge, M Serien im Startbestand (…)“ ohne „Startbestand fehlerhaft“; make_zugang.py
   meldet „zugang.php geschrieben“ mit der Zahl der Editor-Zugänge (mindestens 1).
7. **Hochladen.** Lade auf den Webspace:

   | von | nach |
   |---|---|
   | dist/web/ (mit der versteckten Datei .htaccess und dem Ordner bilder/) | Web-Ordner |
   | dist/privat/startbestand/ | `<privater Ordner>/startbestand/` |
   | dist/zugang.php | `<privater Ordner>/zugang.php` |

   Wenn der private Ordner nicht zwei Ebenen über dem Web-Ordner liegt, dann lege ort.php im Web-Ordner an (BEGRIFFE).
   PHP muss in den privaten Ordner (daten/ wird beim ersten Speichern angelegt) und in `<Web-Ordner>/bilder/` schreiben
   dürfen. Bei jedem neuen Upload überschreibst du nur Web-Dateien, startbestand/ und zugang.php; daten/ und
   hochgeladene Bilder in bilder/ lässt du stehen.
   *Ergebnis:* Bei live = true erscheint die Startseite, und `<adresse>feed.xml` liefert Atom; bei live = false zeigen
   beide die Seite „bald geht es los“. In beiden Fällen antwortet ein POST auf `<adresse>api.php?a=liste` ohne Schlüssel
   „Kein gültiger Zugang“.
8. **Editor prüfen.** Öffne den Editor-Link, leg einen Entwurf an und speichere ihn.
   *Ergebnis:* Der Entwurf steht in der Liste des Editors und in `<privater Ordner>/daten/beitraege/`.

```text
PRÜFUNG:      Ergebnisse der Schritte 2, 6, 7 und 8.
FAIL-MODE:    Wenn ein Test in Schritt 2 fehlschlägt, dann lade nichts hoch und nenne die Ausgabe. Wenn die Startseite
              „404“ oder ein Verzeichnis zeigt, dann wirkt .htaccess nicht (mod_rewrite, AllowOverride) – nenne das.
              Wenn der Editor „Kein gültiger Zugang“ meldet, dann fehlt die Prüfsumme in zugaenge.json oder zugang.php
              liegt nicht im privaten Ordner. Wenn eine Angabe fehlt (Adresse, Namen, Zugänge), dann lass den Schritt
              offen und nenne sie. Wenn kein Webspace da ist und du Schritt 7 und 8 lokal nachstellst, dann starte
              `php -S 127.0.0.1:<port> -t <Web-Ordner> <Web-Ordner>/index.php`: Der PHP-Testserver liest keine
              .htaccess, und das Blog nimmt dort den Web-Ordner immer als Wurzel (/).
NICHT TUN:    Schlüssel, Token und Editor-Links gehören nur in Umgebungsvariablen und in zugang.php im privaten Ordner;
              leg sie nie in ein Repo und nie in den Web-Ordner. · Ändere die Kennung eines veröffentlichten Beitrags
              nicht; sie ist seine Adresse. · Überschreib beim Upload nie daten/ und nie hochgeladene Bilder.
LIEFERUNG:    Adresse des Blogs · Ergebnis jeder Prüfung · Lage von Web-Ordner und privatem Ordner · Zahl der
              Editor-Zugänge (ohne Links und Schlüssel) · Wünsche, die ohne Code-Änderung nicht erfüllbar sind · offene Punkte · jede Stelle, an der diese Anleitung nicht reichte, mit
              Zitat.
REFERENZ:     Kopf von tools/build.py (Aufbau von dist/) · Kopf von tools/make_zugang.py (Felder von zugang.php) ·
              Kopf von tools/import_projektlog.py (Felder für ein Projekt-Log) · Kopf von server/lib.php (Lage der
              Inhalte).
```

---

## BLOCK B – für Menschen

Wer jahrelang auf einer großen Plattform bloggt, merkt irgendwann: Mehrteilige Reihen lassen sich dort kaum abbilden. Die
Teil-Nummer steht im Titel, es gibt kein „weiter zum nächsten Teil“, und die Texte gehören halb der Plattform. Dieses
kleine Blog ist aus genau diesem Wunsch entstanden: Serien als Herzstück, die eigenen Texte auf dem eigenen Webspace.

Es braucht keine Datenbank, nur einen einfachen PHP-Webspace. Beiträge schreibt man im Browser, auch auf dem Handy, und
veröffentlicht sie mit einem Knopf. Wer möchte, lässt sie automatisch ins Englische übersetzen; sichtbar wird die
Übersetzung erst, wenn man sie selbst geprüft hat. Alte Beiträge aus einem Blogger-Blog lassen sich einmal übernehmen,
samt Bildern und erkannten Serien. Leser bekommen eine ruhige Seite ohne Werbung und ohne Tracking und können über einen
Feed folgen.

## Was du im Alltag tust

Du öffnest deinen persönlichen Editor-Link, schreibst, speicherst als Entwurf und veröffentlichst, wenn es passt. Ob es
geklappt hat, siehst du sofort auf der Startseite deines Blogs. Englische Fassungen hakst du im Editor ab, wenn du sie
gelesen hast. Den Editor-Link behältst du für dich – er ist dein Schlüssel.
