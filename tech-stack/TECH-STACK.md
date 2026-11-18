# Tech-Stack für lokale Werkzeuge 0.3.1

## BLOCK A – Auftrag an die bauende KI

```text
ZWECK:        Du baust ein neues lokales Werkzeug und entscheidest die Grundlagen nicht neu: Laufzeit, Start, Port,
              Webserver, Oberfläche, Daten, Ablage (GitHub empfohlen), Zugangsschlüssel, Befehle ohne Oberfläche,
              Log, Schnittstellen, Tests und Arbeitsweise stehen hier als Vorgabe. Das Ziel ist erreicht, wenn
              das Werkzeug die Schritte des Startpakets mit ihren Ergebnissen erfüllt und jede Abweichung in
              ANNAHMEN.md steht.
GILT FÜR:     Ein KI-Bau-Chat beginnt ein neues Werkzeug, das auf einem Windows-Rechner läuft und seine Oberfläche im
              Browser zeigt · ein Bau-Chat prüft, ob ein bestehendes Werkzeug der Vorgabe folgt.
GILT NICHT:   Websites und Dienste auf einem Server · die Fachlogik eines Werkzeugs (die steht in seinem Auftrag) ·
              was eine KI-Rolle darf (das steht in ihrer Rollendatei und im Regelwerk, Baustein 12).
VORAUSSETZUNG: Rahmen auf dem Zielrechner: Windows 11 ohne Administratorrechte · auf dem Rechner wird nichts
              installiert · Oberfläche im Browser auf localhost, je Werkzeug ein eigener Port · ein Benutzer je Rechner
              · später übernehmen andere Anwender das Werkzeug, deren Pfade sich ändern können (Pfade nur in Config/).
              Ablage: GitHub ist empfohlen. Wenn GitHub nicht verfügbar ist, dann nimm je nach Verfügbarkeit
              Knowledge (Projektwissen der KI), SharePoint oder lokale Dateien (Baustein 6).
              Bauumgebung: Python 3.13 oder 3.14 mit pytest, Node.js und Chrome oder Chromium für Klickabläufe,
              git. Die Laufzeit auf dem Zielrechner ist Python 3.14 (Baustein 1).
DATEIEN:      TECH-STACK.md (diese Vorgabe) · BELEGE.md (je Vorgabe die Stelle, an der sie schon funktioniert, mit
              Datei, Zeile und Commit; nicht Teil der öffentlichen Fassung) · blindtest/ (Probeaufgaben und Befunde
              der Blindtests dieser Datei).
BEGRIFFE:     Werkzeug = ein lokales Programm mit eigenem Ordner, eigenem Port und Oberfläche im Browser.
              Zielrechner = der Windows-Rechner, auf dem das Werkzeug läuft. Bauumgebung = die Umgebung der bauenden
              KI, meist Linux, ohne Windows und oft ohne Netz.
              Installationsordner = der Ordner des Werkzeugs auf dem Zielrechner.
              Steuerpult = ein Werkzeug, das andere Werkzeuge anzeigt, startet, stoppt und aktualisiert.
              Sitzungstoken = Schlüssel der Oberfläche für POST-Anfragen, bei jedem Start neu. Zugangsschlüssel = das
              Token für GitHub. Das sind zwei verschiedene Dinge.
              Auftrag (im Werkzeug) = eine längere Verarbeitung im Hintergrund, z. B. ein Import.
              Log = das Tageslog des Werkzeugs (Baustein 9); es bleibt auf dem Rechner. Protokolle = was das Werkzeug
              nach GitHub sendet (6.1); sie enthalten nie Firmendaten.
              Firmendaten = Kassen-, Preis-, Kurs-, Bestands-, Mengen-, Umsatz-, Filial- und Personendaten sowie
              echte Server- und Datenbanknamen. Sie bleiben auf dem Zielrechner (Config/, Data/, Logs/ und der
              Austauschordner nach 10.6) und stehen nie im Repo, in Issues, Protokollen oder Beispielen.
              Stand eines Bausteins: erprobt = beim Menschen am Zielrechner gelaufen · gebaut = nur in der
              Bauumgebung getestet · offen = noch nirgends gebaut. „offen“ an einer Vorgabe heißt: hier nicht geregelt;
              dann gilt FAIL-MODE.
              Nummern wie 3.2 = Vorgabe 2 in Baustein 3; BELEGE.md führt dieselben Nummern. Fassungen anderer
              Dokumente stehen immer als „Fassung 1.3“.
              Platzhalter: <werkzeug> = Ordnername des Werkzeugs in Kleinbuchstaben (z. B. muster) · <paket> = sein
              Python-Paket, gleich <werkzeug> · <Name> = derselbe Name mit großem Anfangsbuchstaben (Muster) für
              Startdateien, Kopf X-<Name>-Token und Ziele in Windows · <fassung> = Python-Fassung (z. B. 3.14.7).
```

### SCHRITTE (Startpaket; in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Absicht und Rolle.** Lass Absicht, Auftrag und Grenzen als Datei ins Repo schreiben und eine Rolle mit Kennung
   anlegen (Baustein 12). Ohne Rolle schreibst du nicht ins Repo.
   *Ergebnis:* Auftrag und Rollendatei liegen im Repo; die Rollendatei nennt den Ordner des Werkzeugs.
2. **Ordner und Port.** Lege den Ordner `<werkzeug>/` an mit `<paket>/` (Python), `Web/`, `tests/`, `Tools/`,
   `laufzeit/`, `Config/` (Vorlagen der Einstellungen, im Manifest mit `nur_wenn_fehlt`) und `.gitattributes`. Die
   Einstellungen stehen in `Config/<werkzeug>.config.json` (UTF-8 ohne BOM); fehlt die Datei, dann legt das Werkzeug
   sie aus einer Vorlage im Paket an.
   `Data/` und `Logs/` legt das Werkzeug beim Start an, `Backup/` das Update; im Repo stehen dort höchstens leere
   Platzhalterdateien. Wähle den Port nach 2.1.
   *Ergebnis:* Der Port steht in `PORTS.md` des Repos und als Standard in `<paket>/__init__.py`.
3. **Laufzeit und Start.** Lege Archiv, `<Name>.cmd`, `<Name>.vbs` und `LAUFZEIT.md` nach Baustein 1 an. Dieser
   Schritt ist der erste Sperrpunkt (11.7): das riskanteste Paket zuerst. Für den Starttest legt der Mensch Archiv und
   Startdateien von Hand in einen leeren Installationsordner; Hol- und Update-Skript entstehen erst in Schritt 7. Leg
   dazu ein kleinstes `<paket>/` an (`__init__.py` mit `VERSION`, `__main__.py` gibt sie aus), damit der erste Start
   über die `.cmd` die Laufzeit entpackt und ohne Fehler endet.
   *Ergebnis:* Der Mensch meldet vom Zielrechner die Ausgabe des Starttests aus 1.8 ohne Fehler.
4. **Server.** Baue `<paket>/__main__.py` (Port, zweiter Start, Schalter) und `<paket>/web.py` (Vorprüfung,
   Sicherheitsköpfe, `/api/status`, `/api/shutdown`) nach den Bausteinen 2, 3 und 8.
   *Ergebnis:* Tests für fremden Host, falsches Sitzungstoken, Methode OPTIONS und falschen Content-Type sind grün.
5. **Oberfläche.** Baue `Web/` nach Baustein 4.
   *Ergebnis:* Ein Klickablauf im Headless-Chrome läuft ohne Fehler in der Konsole.
6. **Daten und Log.** Baue nach den Bausteinen 5 und 9.
   *Ergebnis:* Ein Test schreibt ein erfundenes Token ins Log, und die Logdatei enthält es nicht.
7. **Verteilung und Zugang.** Lege `Tools/erzeuge_manifest.py` und `components.manifest.json` an (6.3). Wenn es ein
   Steuerpult gibt, das das Werkzeug aufnehmen kann, dann trag es dort mit Update-Art Manifest ein; ein Hol-Skript
   brauchst du dann nicht. Wie eingetragen wird, sagt die Anleitung des Steuerpults; typisch sind Name,
   Installationsordner, Port, Quelle (Besitzer, Repo, Branch, Ordner im Repo) und Update-Art. Den Zugangsschlüssel für
   diese Updates hält das Steuerpult, nicht das Werkzeug. Wenn das Steuerpult das Werkzeug nicht aufnehmen kann, dann
   melde das dem Menschen und bau bis dahin ein Hol-Skript (6.3). Ohne Steuerpult baust du das Hol-Skript für die
   Erstinstallation und ein Update-Skript (6.3). Baustein 7 baust du nur, wenn das Werkzeug selbst GitHub anspricht.
   *Ergebnis:* `python3 <werkzeug>/Tools/erzeuge_manifest.py --pruefen` meldet Gleichstand; in der Bauumgebung startet
   eine Installation nur aus dem Manifest (mit einem Testhelfer in Python) in einem leeren Ordner. Den Lauf des
   Hol-Skripts in einen leeren Ordner prüft der Mensch am Zielrechner (Schritt 8).
8. **Probe am Zielrechner.** Der Mensch installiert, startet, stoppt und aktualisiert das Werkzeug.
   *Ergebnis:* Der Mensch bestätigt Start, Stopp und Update; du trägst jeden Baustein in README oder ANNAHMEN.md als
   „erprobt“, „gebaut“ oder „offen“ ein (PRÜFUNG).
9. **Pflichtdateien und Blindtest.** Schreib die Pflichtdateien nach 12.3 und lass die README blind testen.
   *Ergebnis:* Der letzte Blindtest der README findet keine echte Lücke.

### BAUSTEINE

Jeder Baustein nennt Vorgabe, Grund, Fallen, Test und Stand. Was hier fehlt, entscheidest du selbst und schreibst es in
ANNAHMEN.md. Eine Empfehlung ohne Beleg ist als „unbelegt“ gekennzeichnet.

**Baustein 1 – Laufzeit: Python 3.14 im Werkzeugordner**
- 1.1 Leg die Laufzeit als ein Archiv in den Werkzeugordner: `laufzeit/python-<fassung>-win64.zip`, eine vollständige
  Python-Laufzeit mit allen Paketen in `Lib/site-packages`. Auf dem Rechner wird nichts installiert.
- 1.2 Gib jedem Werkzeug eine eigene Kopie der Laufzeit. Teile keine Laufzeit zwischen Werkzeugen.
- 1.3 Herkunft: Wenn es schon ein Werkzeug mit dem Referenz-Archiv aus 1.9 gibt, dann kopiere dessen Archiv byte-gleich
  (gleicher SHA-256).
  Wenn nicht, dann besorgt der Mensch einmal eine portable Python-Distribution mit allen Paketen (bewährt: WinPython,
  64 Bit); du packst ihren Inhalt ungeändert in das Zip, Dateien sortiert, mit festem Zeitstempel, damit dieselben
  Dateien dieselbe Prüfsumme ergeben. Schreib SHA-256, Größe, Herkunft und Paketliste in `LAUFZEIT.md`.
- 1.4 Grundausstattung: fastapi, starlette, uvicorn, pydantic, pyodbc; aus der Standardbibliothek sqlite3 und tkinter
  (Fassungen in 1.9).
- 1.5 `<Name>.cmd` startet mit Konsole. Es wechselt zuerst in seinen eigenen Ordner (`cd /d "%~dp0"`) und sucht
  `laufzeit\python-*-win64.zip`. Wenn im Werkzeugordner (neben `laufzeit\`) der Ordner `python-<fassung>-win64\` fehlt,
  dann entpackt es nach `python-<fassung>-win64.tmp\` (erst `tar`, sonst `Expand-Archive`) und benennt erst nach
  Erfolg um. Danach ruft es `python-<fassung>-win64\python.exe -E -s -X utf8 -m <paket>` auf.
- 1.6 `<Name>.vbs` setzt seinen Ordner als Arbeitsordner und startet ohne Konsole
  `python-<fassung>-win64\pythonw.exe -E -s -X utf8 -m <paket>`. Wenn die Laufzeit noch nicht entpackt ist, dann
  startet es die `.cmd` mit sichtbarer Konsole.
- 1.7 Eine neue Fassung bringt ein Archiv mit neuem Namen. Das Update mit Update-Art Manifest räumt das alte Archiv
  ab (6.3); der alte entpackte Ordner bleibt als Rückweg liegen. Die Update-Art Spiegel löscht nichts; dann lägen zwei
  Archive in `laufzeit\`, und die Startdatei nähme das letzte, das ihre Suche findet. Gib Werkzeugen mit Laufzeit
  deshalb die Update-Art Manifest (Empfehlung).
- 1.8 Starttest am Zielrechner: `python.exe -c "import sys,sqlite3,fastapi,uvicorn,pyodbc,tkinter"` im entpackten Ordner
  und `Get-FileHash .\laufzeit\python-<fassung>-win64.zip -Algorithm SHA256` gegen `LAUFZEIT.md`.
- 1.9 Referenz-Laufzeit (Stand dieser Datei):
  · Archiv `python-3.14.7-win64.zip`, SHA-256 `c1364d10327ae129121d9485f043303e17a6eb5f41cec99f9ff463e25164dfed`,
    17.416.341 Byte; entpackt 49.726.397 Byte in 1.369 Dateien. Inhalt auf oberster Ebene: `python.exe`,
    `pythonw.exe`, `Lib/`, `DLLs/` usw.
  · Python 3.14.7, 64 Bit, aus WinPython WPy64-31470, ungeändert gepackt.
  · 18 Pakete in `Lib/site-packages`: annotated-doc 0.0.5 · annotated-types 0.8.0 · anyio 4.15.1 · click 8.5.0 ·
    colorama 0.4.6 · et_xmlfile 2.0.0 · fastapi 0.142.2 · h11 0.16.0 · idna 3.20 · openpyxl 3.1.5 ·
    opentelemetry-api 1.45.1 · pydantic 2.13.5 · pydantic_core 2.46.5 (für Windows kompiliert) · pyodbc 5.3.0 (für
    Windows kompiliert) · starlette 1.7.0 · typing_extensions 4.16.0 · typing-inspection 0.4.4 · uvicorn 0.54.0.
    Pakete, die ein Werkzeug nicht braucht, bleiben drin; ein ungeändertes Archiv ist leichter zu prüfen.
  · SQLite steckt in der Laufzeit: das Modul `sqlite3` der Standardbibliothek mit `DLLs/sqlite3.dll` (SQLite 3.53.1).
    Ein eigenes SQLite gibt es nicht. tkinter ebenso (`Lib/tkinter`, `DLLs/_tkinter.pyd`, Tcl/Tk 9.0).
  · Versionen beim Starttest (1.8): Python 3.14.7, SQLite 3.53.1, fastapi 0.142.2, uvicorn 0.54.0, pyodbc 5.3.0;
    tkinter lädt.
  · Bezug: Das Archiv liegt nicht bei dieser Datei, denn jedes Werkzeug führt seine eigene Kopie (1.2), und ein Archiv
    bliebe für immer in der Git-Historie. Welches Werkzeug es byte-gleich liefert, nennt der Auftrag. Eine neuere
    Fassung nimmst du nur auf Anweisung; dann bekommt diese Datei eine neue Referenz.
  · Nicht in der Laufzeit und nicht beizulegen: der ODBC-Treiber für SQL Server (er gehört zum Rechner, nicht zum
    Werkzeug; die Treiberfolge in 5.6 nimmt den besten vorhandenen) · Node.js und Chrome (nur in der Bauumgebung,
    11.4).
- Grund: Ohne Administratorrechte gibt es keine Installation. `-E -s` schließt Python-Umgebungsvariablen und Pakete
  des Benutzers aus; `-X utf8` hält Umlaute stabil.
- Fallen: Der erste Start entpackt rund 50 MB und dauert länger. `.cmd`, `.vbs` und `.ps1` bleiben reines ASCII; in
  `.gitattributes` bekommen sie `text eol=crlf`, das Archiv `binary`. Git speichert die Startdateien trotzdem mit LF,
  und Update und Hol-Skript liefern genau diese Fassung; `eol=crlf` wirkt nur beim Auschecken. Mit LF laufen sie am
  Zielrechner (erprobt). Halte sie deshalb einfach und ohne Sprungmarken (`goto`, `call :marke`), wie die Vorbilder;
  dass Sprungmarken mit LF scheitern können, ist Fachwissen, nicht belegt.
- Test: In der Bauumgebung prüft ein Test den Text der Startdateien; ausführen lassen sie sich nur am Zielrechner (1.8).
- Stand: erprobt.

**Baustein 2 – Start, Stopp, eine Instanz, Port**
- 2.1 Gib jedem Werkzeug einen festen Port. Reihenfolge: Schalter `--port`, sonst die Einstellung in `Config/`, sonst
  der Standard im Code. Empfehlung (unbelegt): Alle Werkzeuge nehmen Ports aus einem eigenen Bereich, z. B. 8700–8799,
  jeder Port nur einmal. Die Datei `PORTS.md` in der Wurzel des Repos führt eine Zeile je Werkzeug und Port; wenn sie
  fehlt, dann leg sie an. Häufig belegte Ports wie 8000 und 8080 meidest du.
- 2.2 Der Server bindet nur an 127.0.0.1. Im Browser öffnet das Werkzeug `http://localhost:<port>/` (so erprobt).
- 2.3 Zweiter Start: Prüf mit einer Verbindungsprobe (`connect_ex` auf 127.0.0.1), ob der Port belegt ist. Wenn dort
  das eigene Werkzeug antwortet (`produkt` in `GET /api/status`), dann öffne nur den Browser und beende mit
  Rückgabe 0. Wenn dort etwas anderes lauscht, dann melde „Port belegt“ mit dem Vorschlag `--port <port+1>` und
  beende mit Rückgabe 1. Ein Werkzeug mit Sperrdatei prüft vorher nach 2.4; dort entscheidet der Fingerabdruck.
- 2.4 Ein Werkzeug, das Daten schreibt, führt zusätzlich die Sperrdatei (jede Funktion gibt es auch ohne Oberfläche,
  8.1, 8.2): `Data/<werkzeug>.lock` (UTF-8 ohne BOM) mit `pid`, `port`, `started_at`, `version` und `build`.
  `build` ist ein Fingerabdruck (SHA-256, die ersten 12 Zeichen) über `VERSION` und die Programmdateien (`<paket>/`,
  `Web/`, `Sql/`; sortiert, mit relativem Pfad, ohne `__pycache__`). Beim Start prüfst du in dieser Reihenfolge:
  · Lebt die PID nicht, dann ist die Sperre verwaist: ersetzen, Warnung ins Log, starten.
  · Trägt die Sperre den Eintrag `kommandozeile` (Lauf ohne Oberfläche, Port 0, 8.2), dann startest du nicht und
    meldest „arbeitet gerade ohne Oberfläche“; Rückgabe 1. Empfehlung (unbelegt): Ist der Prozess mit dieser PID
    später gestartet als `started_at`, dann ist die Sperre verwaist (die PID wurde neu vergeben).
  · Ist ihr Port frei, dann gehört die PID einem fremden Prozess: Sperre ersetzen, Warnung, starten.
  · Gleicher Fingerabdruck (und `produkt` wie in 2.3): nur den Browser öffnen. Anderer Fingerabdruck: die alte Instanz
    über ihre API ablösen (`sitzungstoken` aus `/api/status`, dann `POST /api/shutdown`), auf ihr Ende warten, dann
    starten. Empfehlung (unbelegt): Läuft dort ein Auftrag (2.6), dann löst du nicht ab, sondern meldest es und beendest
    mit Rückgabe 1.
- 2.5 Jedes Werkzeug bringt drei Dinge mit, damit ein Steuerpult es verwalten kann: eine Startdatei ohne Konsole
  (`<Name>.vbs`) · `GET /api/status` mit den Feldern `produkt`, `version`, `pid`, `port`, `sitzungstoken` und dem
  Zustand der Aufträge · `POST /api/shutdown`, geschützt wie jede POST-Anfrage (3.2), Antwort `{"ok":true}`, danach
  endet der Server nach rund 0,3 s. Ohne Steuerpult beendet der Mensch das Werkzeug über einen Knopf „Beenden“ in
  der Oberfläche oder den Schalter `--stop` (8.1); beide gehen über `POST /api/shutdown`. Das Sitzungstoken darf in
  `/api/status` stehen: Eine fremde Webseite kann die Antwort nicht lesen, solange die Host-Prüfung aus 3.2 greift;
  ein lokales Programm braucht es zum Beenden.
- 2.6 Während ein Auftrag läuft, meldet `/api/status` das im Feld `state_key` mit dem Wert `processing` (sonst z. B.
  `ready`). Das Werkzeug selbst beendet sich auf `POST /api/shutdown` immer; fragen muss der Aufrufer. Ein
  Steuerpult liest deshalb vorher `/api/status`: Läuft ein Auftrag, dann fragt es den Menschen, bevor es beendet, und
  ein Update startet erst nach dem Auftrag. Ebenso fragt der Knopf „Beenden“ (2.5) nach. Empfehlung (unbelegt): Der
  Schalter `--stop` beendet bei laufendem Auftrag nur mit einem ausdrücklichen Zusatzschalter, sonst meldet er den
  Auftrag und endet mit Rückgabe 1.
- Grund: Zwei Instanzen schreiben gegeneinander; ein Steuerpult braucht feste Wege für Start, Zustand und Stopp.
- Fallen: Windows vergibt Prozessnummern neu – eine Sperrdatei mit fremder lebender PID darf den Start nicht
  blockieren. Eine Bind-Probe meldet einen eben beendeten Server noch Sekunden als belegt. Ein Stopp mitten im Import
  hinterlässt Daten bis zum letzten Commit; erst der nächste Lauf vervollständigt sie (5.5).
- Test: zweiter Start bei laufendem Werkzeug; Sperrdatei mit fremder PID und freiem Port; Status während eines
  nachgestellten Auftrags.
- Stand: Ablösung, Start und Stopp erprobt; Verbindungsprobe und Zustand „processing“ gebaut; Rückfrage vor dem Stopp
  während eines Auftrags offen.

**Baustein 3 – Webserver: FastAPI und uvicorn, nur auf 127.0.0.1**
- 3.1 Nimm FastAPI mit uvicorn: `host="127.0.0.1"`, `access_log=False`, `log_config=None`, `lifespan="off"`; ohne
  Doku-Routen (`docs_url=None`, `redoc_url=None`, `openapi_url=None`).
- 3.2 Prüf jede Anfrage in einer Middleware vor dem Routing, in dieser Reihenfolge:
  Host-Kopf ist `localhost`, `127.0.0.1` oder `[::1]` mit dem eigenen Port, sonst 400 (`[::1]` ist nur als Kopf
  erlaubt; der Server lauscht nicht an ::1, 2.2) ·
  Absender ist Loopback (eine IPv4-Adresse in IPv6 vorher auflösen), sonst 403 ·
  Methode ist GET oder POST, sonst 405 ·
  bei POST trägt der Kopf `X-<Name>-Token` das Sitzungstoken, verglichen als Bytes mit `hmac.compare_digest`, sonst 403 ·
  bei POST beginnt `Content-Type` mit `application/json` (ein Zusatz wie `; charset=utf-8` ist erlaubt), sonst 415.
- 3.3 Erzeuge das Sitzungstoken bei jedem Start neu (`secrets.token_hex(16)`). Die Oberfläche bekommt es über den
  Platzhalter `{{SITZUNGSTOKEN}}` in `index.html`, den der Server beim Ausliefern ersetzt. Es ist nie der
  Zugangsschlüssel zu GitHub.
- 3.4 Setz auf jede Antwort, auch auf Fehler: `Cache-Control: no-store` · `X-Content-Type-Options: nosniff` ·
  `X-Frame-Options: DENY` · `Referrer-Policy: no-referrer` ·
  `Content-Security-Policy: default-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'`.
- 3.5 Liefere statische Dateien nur aus `Web/`: erlaubte Zeichen, kein `%`, kein `\`, kein Nullbyte, keine Segmente
  `.` oder `..` und keine versteckten Dateien, nur feste Endungen; den Pfad mit `resolve()` und `is_relative_to()` prüfen.
  Begrenze den Körper von POST-Anfragen mit einer festen Grenze je Route (z. B. 4 KB für Steuerbefehle; für Daten so
  groß, wie das Werkzeug braucht); ist er zu groß, dann antwortet die Route mit 400.
- 3.6 Blockierende Arbeit (Dateien, Netz, Datenbank) läuft nicht in der Ereignisschleife, sondern über
  `run_in_threadpool` oder einen eigenen Leser-Pool.
- Grund: Eine fremde Webseite im selben Browser kann über DNS-Rebinding Anfragen an localhost schicken; Host-Prüfung,
  Sitzungstoken und Content-Type schließen das aus.
- Fallen: Ohne Host-Prüfung nimmt uvicorn jeden Host an. Ein Vergleich als `str` wirft bei Nicht-ASCII einen Fehler,
  die Antwort wird 500 und verliert die Sicherheitsköpfe.
- Test: rohe Anfragen mit fremdem Host, Token mit Umlaut, OPTIONS, falschem Content-Type und Pfaden mit `%2e%2e`.
- Stand: Host-Prüfung erprobt (fremder Host ergab 400); die übrigen Prüfungen gebaut.

**Baustein 4 – Oberfläche: HTML, CSS, JavaScript**
- 4.1 Schreib die Oberfläche in HTML, CSS und JavaScript im Ordner `Web/`, ohne Build-Schritt und ohne Datei aus dem
  Internet. Mehrere Skripte bindest du als ES-Module ein (`<script type="module">`), ein einzelnes mit `defer`.
- 4.2 Setz Texte vom Server oder von außen nur mit `textContent` ein. Wo HTML nötig ist, geht jeder Wert durch eine
  Escape-Funktion.
- 4.3 Frag den Zustand im Takt ab, z. B. alle 5 s, während eines langen Vorgangs jede Sekunde.
- 4.4 Jede POST-Anfrage schickt das Sitzungstoken (3.3) und `Content-Type: application/json`.
- 4.5 Wahlweise: Stile als eigene CSS-Dateien zum Umschalten; Sprachen als eine Textdatei je Sprache.
- 4.6 Wahlweise öffnet ein Knopf „Rückmeldung“ im Browser die Seite für ein neues Issue (6.4).
- Grund: Ohne Build-Schritt und ohne Internet läuft die Oberfläche auf jedem Zielrechner und bleibt prüfbar.
- Fallen: Eine Fehlermeldung mit HTML darin, über `innerHTML` gesetzt, wird ausgeführt.
- Test: reine Logik mit `node --test` (Dateien `*.test.mjs`); Klickabläufe im Headless-Chrome über das
  DevTools-Protokoll; Konsole ohne Fehler.
- Stand: erprobt.

**Baustein 5 – Daten: SQLite, SQL Server lesend, JSON-Dateien**
- 5.1 SQLite über `sqlite3`: Der Schreiber setzt `PRAGMA journal_mode=WAL`, `busy_timeout=5000` und `foreign_keys=ON`.
  Leser öffnen mit `?mode=ro` und legen nie eine Datei an.
- 5.2 Genau ein Schreib-Thread mit begrenzter Warteschlange von Aufträgen (z. B. 64); Routen lesen parallel. Ein
  Import ist ein Auftrag und läuft darin von Anfang bis Ende. Läuft derselbe Auftrag schon, dann meldet die Route das;
  ist die Warteschlange voll, dann antwortet sie mit 503. Jeder Fehler eines Auftrags steht im Log.
- 5.3 Schema-Versionen als Dateien `NNN_beschreibung.sql`, in Namensreihenfolge, je Datei eine Transaktion mit
  Eintrag in der Tabelle `schema_version`.
- 5.4 Die Statusabfrage läuft ohne `PRAGMA integrity_check`; diese Prüfung gibt es nur auf Knopfdruck. Im Leerlauf
  läuft `PRAGMA wal_checkpoint(PASSIVE)`.
- 5.5 Ein Import über viele Dateien setzt je Datei einen `SAVEPOINT`; ein Fehler kostet dann nur diese Datei.
  Committet wird nur zwischen zwei Dateien, sobald die laufende Gruppe etwa 1 s alt ist. Der SHA-256 einer Datei steht
  in derselben Transaktion wie ihre Zeilen; bereits eingelesene Dateien erkennt der Import daran und überspringt sie.
  So setzt ein neuer Lauf nach einem Abbruch (Beenden, Absturz) dort fort, wo der letzte Commit war. Einen Abbruch auf
  Knopfdruck sieht diese Vorgabe nicht vor (offen).
- 5.6 SQL Server nur lesend über `pyodbc` mit Windows-Anmeldung (`Trusted_Connection=yes`); kein Kennwort in einer
  Datei. Treiber in dieser Reihenfolge: „ODBC Driver 18 for SQL Server“, „ODBC Driver 17 for SQL Server“, „SQL Server
  Native Client 11.0“, „SQL Server“. Wenn ein Treiber fehlt oder TLS scheitert, dann nimm den nächsten. Setz
  `TrustServerCertificate=yes`, beim Treiber 18 zusätzlich `Encrypt=no`. Setz Zeitgrenzen für Anmeldung und Abfrage;
  die Abfrage läuft in einem eigenen Thread. Server- und Datenbankname stehen nur in `Config/` auf dem Zielrechner.
- 5.7 JSON-Dateien für kleine Datenmengen: UTF-8 ohne BOM · ersetzen über `.tmp` und `os.replace` · Verläufe als
  JSON-Zeilen nur anhängen · eine gleichzeitige Änderung mit Revisionsnummer abweisen (409). Wenn mehrere Threads
  dieselbe Datei ändern können, dann schützt eine Sperre Lesen, Ändern und Schreiben, und jede `.tmp` hat einen
  eindeutigen Namen.
- 5.8 Ordner im Werkzeug: `Config/` (Einstellungen; ein Update legt nur Fehlendes an) · `Data/` (Daten; kein Update
  fasst sie an) · `Logs/` · `Backup/`.
- Grund: SQLite braucht keinen Dienst; ein Schreiber verhindert Sperrkonflikte; die Windows-Anmeldung hält Kennwörter
  aus Dateien.
- Fallen: Eine Statusabfrage, die bei jedem Aufruf `integrity_check` ausführte, antwortete nach 28 s mit Fehler 500
  (Ursache aus dem Code abgeleitet). Unter Windows scheitert `os.replace`,
  wenn ein anderer Thread die Datei gerade offen hat. Der Treiber „SQL Server“ liefert Datumsspalten als Text.
- Test: echte SQLite-Dateien im Temp-Ordner; SQL Server über eine Attrappe (11.3); zwei Threads schreiben gleichzeitig.
- Stand: SQLite und SQL Server erprobt; JSON-Dateien gebaut.

**Baustein 6 – GitHub als Backend**
GitHub ist die Empfehlung, keine Bedingung. Wenn GitHub nicht verfügbar ist, dann nimm Knowledge, SharePoint oder
lokale Dateien; die Regeln aus 6.3 (fester Stand, Prüfsumme, Sicherung) gelten dort genauso (offen: dafür ist noch
nichts gebaut). Offen ist dann vor allem: wo Repo, Pflichtdateien und Verträge liegen · wie ein Stand ohne Commit
festgelegt und ohne Git-Blob-SHA geprüft wird · woher Hol- und Update-Skript ihre Quelle kennen · wohin Rückmeldungen
gehen. Das entscheidest du nach FAIL-MODE und nennst es in der Lieferung. Firmendaten gehen nie nach GitHub. Die
Reihenfolge nach Nutzen: Protokolle, Austausch, Updates, Issues. Bau davon nur, was das Werkzeug braucht; ein
Werkzeug ohne Bedarf an Protokollen braucht 6.1 nicht.
- 6.1 Protokolle: Auf Knopfdruck legt das Werkzeug Protokolle ohne Firmendaten als einen Commit in einem Protokoll-Repo
  ab, Ordner `protokolle/<werkzeug>/<JJJJ-MM-TT_HHMM>/`. Das Protokoll-Repo ist ein eigenes Repo, nicht das des
  Werkzeugs; Besitzer, Repo, Branch und Ordner haben einen Standard im Code und lassen sich in `Config/` (Abschnitt
  `protokolle`) ändern. Den Standard nennt der Auftrag. Es gilt eine Positivliste von Dateien und Feldern, kein
  Suchfilter. Vor dem Senden zeigt eine Vorschau jede Datei mit Inhalt. Der Schlüssel dafür hat Schreibrecht nur auf das
  Protokoll-Repo und ein eigenes Ziel ohne Rückfall (7.2). Gesendet wird über die Git-Data-API: Baum mit `base_tree`,
  Commit, Ref vorschieben ohne `force`. Für das Senden schreibt das Werkzeug ein Technik-Protokoll
  `Logs/technik_JJJJMMTT.log` (UTF-8 ohne BOM, LF), eine Zeile je Ereignis: Zeit, dann `ereignis=<name>` und
  `schluessel=wert`-Paare. Feste Ereignisse mit festen Feldern: `start` (Format, Version, Build, Port, Python, PID) ·
  `ende` (Version, Build, Dauer) · `job` (Auftrag, Ergebnis `ok`, `nicht_ok` oder `fehler`, Dauer, wahlweise Zahl der
  Dateien gefunden/eingelesen/übersprungen/fehlerhaft, Zahl der Zeilen, Fehlerart, Quelle `server` oder
  `kommandozeile`). Zahlen von Dateien und Zeilen sind technische Zählwerte, keine Mengendaten. Nie: Pfade, Datei- oder
  Servernamen, Meldungstexte oder Firmendaten; jeder Wert gegen ein Muster geprüft; was nicht passt, ergibt eine
  Zeile `ereignis=defekt`. Eine Datei ist defekt, wenn eine Zeile `ereignis=defekt` lautet oder eine Zeile nicht dem
  Muster entspricht; sie wird nicht gesendet. Das Tageslog (9.1) gehört nie zu den gesendeten Dateien.
- 6.2 Austausch über GitHub nur ohne Firmendaten: Einstellungen, Vorlagen, Nachrichten zwischen KIs. Firmendaten
  tauschen Werkzeuge lokal über Austauschdateien aus (Baustein 10).
- 6.3 Updates:
  · Leg den Stand fest: `GET /repos/{owner}/{repo}/branches/{branch}` liefert `commit.sha`. Jede Datei des Laufs kommt
    von genau diesem Commit (`raw.githubusercontent.com/{owner}/{repo}/{sha}/…`, Rückfall contents-API mit
    `ref={sha}`), nie über den Branch-Namen.
  · Zeig einen Plan je Datei: neu, geändert, gleich, behalten, Abraum, Warnung. Ein Plan gilt einmal und höchstens 1 h.
  · Ablauf beim Steuerpult: Werkzeug stoppen (nicht während eines Auftrags, 2.6) · alle Dateien nach
    `Backup/<stempel>.neu/` laden und prüfen · die zu ersetzenden Dateien nach `Backup/<stempel>/` sichern · ersetzen,
    jede Aktion vorher vermerken und bei einem Fehler rückwärts zurücknehmen · Werkzeug starten und warten, bis es
    antwortet. Ein Abbruch während des Ladens lässt alles, wie es war.
  · `Config/` legt das Update nur an, wenn es fehlt. `Data/`, `Logs/`, `Backup/` und die entpackte Laufzeit fasst es
    nie an. Das Laufzeit-Archiv legt es nur ab; entpackt wird beim nächsten Start (1.5).
  · Zwei Arten mit je eigenem Prüfweg: Spiegel = der ganze Ordner eines Branches; die Liste und die Git-Blob-SHA je
    Datei liefert `GET /repos/{owner}/{repo}/git/trees/{sha}?recursive=1`; nichts wird gelöscht · Manifest = die
    Dateien aus `components.manifest.json`, geprüft über SHA-256; abgeräumt wird nur, was im alten Manifest stand und
    im neuen fehlt.
  · Aufbau des Manifests: oben die Felder `produkt`, `stand`, `erzeugt`, `hinweis` und `komponenten`; je Komponente
    (z. B. `programm`, `laufzeit`, `doku`) eine Liste `dateien`; je Datei `pfad` und `sha256`, wahlweise
    `nur_wenn_fehlt: true` oder `nur_pruefen: true`.
    Pfade relativ zum Werkzeugordner mit `/`. SHA-256 über die Fassung im Git-Index (`git show :<pfad>`), nicht über
    die ausgecheckte Datei. Nicht ins Manifest: das Manifest selbst, `tests/`, `Tools/`, Punktdateien, `Data/`, `Logs/`.
    `nur_wenn_fehlt` für Vorlagen in `Config/`; `nur_pruefen` für Dateien, die das Update nie lädt, nur vergleicht.
  · Das Manifest erzeugt ein Skript (`Tools/erzeuge_manifest.py`, nach `git add`, mit `--pruefen`), nie die Hand;
    Dateien und Manifest gehen in denselben Commit.
  · Ein Steuerpult aktualisiert auch sich selbst: Dateien ersetzen, dann als neuer Prozess ohne Fenster neu starten.
  · Werkzeuge unter einem Steuerpult: Eingetragen werden sie nach dessen Anleitung (Schritt 7); ihre Updates holt das
    Steuerpult mit seinem eigenen Zugangsschlüssel.
  · Erstinstallation ohne Steuerpult mit einem Hol-Skript in PowerShell (`Hole-<Name>.ps1`). Der Mensch legt einen
    leeren Installationsordner an, legt das Skript hinein (aus dem Repo oder vom Auftraggeber) und ruft dort
    `powershell -ExecutionPolicy Bypass -File .\Hole-<Name>.ps1` auf. Es arbeitet wie ein Spiegel: legt den Commit fest,
    prüft jede Datei über die Git-Blob-SHA, behält `Config/`, fasst `Data/`, `Logs/` und `Backup/` nicht an und fragt
    den Zugangsschlüssel verdeckt nur für den eigenen Lauf ab (7.4); bei einem privaten Repo ist er nötig.
  · Updates ohne Steuerpult: ein Update-Skript in PowerShell in der Wurzel des Werkzeugordners (`Update-<Name>.ps1`)
    nach den Regeln der Update-Art Manifest; Plan, Laden nach `Backup/<stempel>.neu/`, Sicherung und Rücknahme gelten
    wie beim Steuerpult. Das angewendete Manifest legt es danach als `components.manifest.json` im Werkzeugordner ab;
    daraus räumt das nächste Update ab, ohne diese Kopie räumt es nichts ab. Es bricht ab, solange das Werkzeug auf
    seinem Port lauscht oder seine Sperrdatei lebt; der Mensch beendet das Werkzeug vorher und startet es danach. Das
    Skript steht selbst im Manifest, verarbeitet sich zuerst und endet nach einer Selbsterneuerung mit der Bitte, es
    erneut zu starten. Den Schlüssel fragt es verdeckt ab, nie als Parameter (7.4). Empfehlung (unbelegt): Für seine
    Dauer hält es die Sperrdatei mit `kommandozeile` (2.4), damit kein täglicher Lauf (8.4) dazwischen startet.
- 6.4 Issues: Ein Knopf „Rückmeldung“ öffnet im Browser die Seite `https://github.com/{owner}/{repo}/issues/new`
  mit vorbelegtem Titel, Label und Text (Version, Browser, Zustand, Fehlerart). Der Mensch ergänzt und sendet selbst;
  das Werkzeug braucht dafür keinen Schlüssel. Vorbelegt werden nur technische Angaben; Meldungstexte, die Pfade,
  Datei- oder Servernamen oder Firmendaten enthalten können, gehören nicht dazu. Bei einem
  privaten Repo braucht der Mensch dort Zugang; die README sagt das. Wahlweise beantwortet ein Workflow
  (Issue-Assistent) das Issue.
- 6.5 „Zugang prüfen“: `GET /repos/{owner}/{repo}`; die Meldung trennt Token fehlt · Token falsch oder abgelaufen · kein
  Zugriff auf das Repo · Abrufgrenze · Netz. Der Kopf lautet `Authorization: Bearer <token>`; bei einer Umleitung auf
  einen anderen Host fällt er weg.
- Grund: Ein fester Commit verhindert gemischte oder alte Stände (Adressen über den Branch-Namen können eine Zeit lang
  zwischengespeicherte alte Dateien liefern); Sicherung und Rückfall verhindern ein halbes Update.
- Fallen: Ein Updater, der seine eigene Datei nicht verarbeitet, erneuert sich nie und kann eine neue Laufzeit nicht
  bringen. „Neu gestartet“ zu melden, ohne auf eine Antwort zu warten, täuscht.
- Test: nachgebautes GitHub mit Störfällen (Prüfsumme falsch, Abbruch, Fehler beim Ersetzen); Installation aus dem
  Manifest in einen leeren Ordner; zweites „Prüfen“ ergibt nichts zu tun. Für Hol- und Update-Skript in PowerShell
  gilt 11.5; ihre Störfälle prüft der Mensch am Zielrechner.
- Stand: Updates über das Steuerpult, Sicherung, Abbruch, Selbst-Update und Protokolle erprobt; Update-Skript ohne
  Steuerpult erprobt (frühere Fassung, ohne die Laufzeit); Issues gebaut; Knowledge, SharePoint und lokale Dateien als
  Ablage offen.

**Baustein 7 – Zugangsschlüssel in Windows**
- 7.1 Leg den Zugangsschlüssel in der Windows-Anmeldeinformationsverwaltung ab: `advapi32` mit `CredWriteW`,
  `CredReadW` und `CredDeleteW` über `ctypes`, Typ generisch, Persistenz lokal (nur dieser Benutzer auf diesem Rechner),
  Ziel `<Name>/GitHub`, Inhalt als UTF-16LE. Überschreib den Puffer nach dem Schreiben mit Nullen.
- 7.2 Rückfall: die Umgebungsvariable `GITHUB_TOKEN`. Ein Schlüssel mit Schreibrecht (6.1) hat ein eigenes Ziel
  `<Name>/GitHub-Protokolle` und keinen Rückfall.
- 7.3 Ablegen: Der Mensch fügt den Schlüssel in der Oberfläche in ein Feld „Zugang zu GitHub“ ein und klickt „In
  Windows speichern“ (`POST /api/zugang/token`); löschen geht über `POST /api/zugang/loeschen`. Danach zeigt die
  Oberfläche nur „vorhanden ja/nein“ und die Quelle, nie den Schlüssel. Der Schreib-Schlüssel für Protokolle (7.2)
  hat ein eigenes Feld und eigene Routen: `POST /api/protokolle/token` und `POST /api/protokolle/token/loeschen`.
  Ein Werkzeug baut nur die Felder, deren Schlüssel es braucht.
- 7.4 Der Schlüssel steht nie in einer Datei, einer Antwort, einem Log, einem Chat oder auf der Befehlszeile. Ein
  Hol-Skript fragt ihn verdeckt ab (`Read-Host -AsSecureString`), legt ihn nicht ab, hat keinen Parameter dafür und
  leert am Ende seine Variablen. Das Sitzungstoken lebt nur im Speicher des Werkzeugs; außer in der Oberfläche (3.3)
  und in `/api/status` (2.5) steht es nirgends, auch nicht in einer Datei, einem Log oder einem Chat. Wenn es in einen
  Chat geraten ist, dann starte das Werkzeug neu.
- Grund: Windows PowerShell 5.1 schreibt jede eingetippte Befehlszeile im Klartext in eine Verlaufsdatei. Eine
  Umgebungsvariable gilt nur im Fenster, in dem sie gesetzt wurde; ein Start per Doppelklick sieht sie nicht.
- Test: In der Bauumgebung prüft ein Test die Größe der `ctypes`-Strukturen für x64; am Zielrechner sucht der Mensch
  den Schlüssel im Installationsordner (0 Treffer).
- Stand: erprobt.

**Baustein 8 – Ohne Oberfläche: Befehle und tägliche Läufe**
- 8.1 Jede Funktion gibt es auch als Schalter am selben Einstieg, z. B. `<Name>.cmd --status` (die `.cmd` reicht
  Schalter an `python.exe -E -s -X utf8 -m <paket>` weiter). Rückgabe 0 heißt in Ordnung, 1 heißt Fehler. Ausnahme:
  Den Zugangsschlüssel nimmt kein Schalter entgegen (7.4).
- 8.2 Wenn eine Instanz läuft, dann geht der Befehl über ihre API, denn sie ist der eine Schreiber: über dieselben
  Routen, mit denen die Oberfläche den Auftrag startet und seinen Zustand abfragt. Sonst arbeitet der
  Befehl selbst und hält so lange die Sperrdatei (2.4) mit Eintrag `kommandozeile` und Port 0. Ein Werkzeug, dessen
  Befehle ohne Oberfläche schreiben, führt deshalb immer die Sperrdatei.
- 8.3 Beim Start per Doppelklick ohne Konsole (`pythonw.exe`, ohne Schalter) gehen Ausgaben in eine Logdatei und
  Fehler zusätzlich in ein Meldungsfenster. Ein Lauf mit dem Schalter eines täglichen Laufs (8.4) zeigt nie eines: Der
  Einstieg wertet diese Schalter aus, bevor er den Start ohne Konsole einrichtet.
- 8.4 Tägliche Läufe startet die Windows-Aufgabenplanung im Konto des Benutzers. Empfehlung (unbelegt): Die Aufgabe
  ruft `<Name>.cmd --<befehl>` auf, „Starten in“ ist der Installationsordner; die `.cmd` findet die aktuelle Laufzeit
  auch nach einem Update (1.5, 1.7). Ein fester Pfad zu `python-<fassung>-win64\pythonw.exe` veraltet mit der
  nächsten Fassung. Ein solcher Lauf zeigt kein Meldungsfenster; bei einem Fehler schreibt er den Grund ins Log und
  endet mit Rückgabe 1. Das Konsolenfenster der `.cmd` ist dabei hinzunehmen. Die Aufgabe legt der Mensch nach der
  README des Werkzeugs an (offen: in Python noch nicht gebaut und nicht erprobt).
- Grund: Was auch ohne Oberfläche geht, lässt sich planen und von einer KI prüfen.
- Stand: Prüfbefehle erprobt; Befehle für tägliche Läufe gebaut; Aufgabenplanung offen.

**Baustein 9 – Log mit Schwärzung**
- 9.1 Eine Tagesdatei `Logs/<werkzeug>_JJJJMMTT.log`, UTF-8 ohne BOM, eine Zeile je Meldung mit Zeit und Stufe;
  Zeilenumbrüche einer Meldung werden zu „ | “ in derselben Zeile.
- 9.2 Genau ein Schreiber: Alle Threads geben über einen `QueueHandler` ab, ein `QueueListener` schreibt.
- 9.3 Schwärze vor dem Schreiben die ganze Zeile samt Traceback: bekannte Geheimnisse wörtlich (Sitzungstoken,
  Zugangsschlüssel) und Muster (`Authorization`, `X-…-Token`, `"token":`, `ghp_…`, `github_pat_…`, Zugangsdaten in
  Adressen, `password=` und ähnliche).
- 9.4 Regelmäßige Abfragen kommen nur bei Fehlern ins Log; jeder Fehler eines Auftrags kommt hinein.
- 9.5 Getrennt davon steht das Technik-Protokoll zum Senden (6.1).
- Grund: Das Log ist der erste Weg, einen Fehler am Zielrechner zu sehen; es darf nichts verraten.
- Stand: erprobt.

**Baustein 10 – Schnittstellen: Austauschdateien mit Version**
- 10.1 Werkzeuge tauschen Daten lokal über JSON-Dateien aus. Der Vertrag steht als eigene Markdown-Datei mit Nummer der
  Version im Repo des liefernden Werkzeugs.
- 10.2 Jede Datei trägt `format`, `version`, `table`, `exported_at`, `filter`, `columns`, `rows` und `row_count`; sie
  heißt `<art>_<JJJJMMTT-hhmmss>.json`.
- 10.3 Ein Exportlauf: Alle Dateien tragen denselben Zeitstempel und dasselbe `exported_at`. Erst entstehen alle als
  `.tmp`, dann werden alle umbenannt. Wenn der Lauf abbricht, dann entsteht keine `.json`, und die `.tmp` werden
  entfernt.
- 10.4 Der Leser nimmt den jüngsten vollständigen Satz und prüft `format`, `version`, `table`, `row_count` und das
  gleiche `exported_at`. Eine unbekannte Version deutet er nicht: Er liest den Satz nicht ein, meldet gelesene und
  erwartete Version in Log und Oberfläche, und seine Daten bleiben auf dem zuletzt gelesenen Stand. `.tmp` zählt
  nicht. Er liest nur.
- 10.5 Ein neues Feld bedeutet eine neue Version des Vertrags: Das Feld `version` ist eine ganze Zahl und zählt getrennt
  von `VERSION` des Werkzeugs (12.4). Der Vertrag wird vorher mit dem Leser abgestimmt: schriftlich im
  Repo, mit der Rolle oder dem Menschen, der den Leser baut. Empfehlung (unbelegt): Zuerst lernt der Leser die neue
  Version und liest die alte weiter, dann schreibt der Lieferer die neue; so fällt beim Update keiner aus. Beim
  Lieferer steigt zudem die zweite Stelle von `VERSION` (12.4).
- 10.6 Der Ablageort ist eine Einstellung in `Config/` beider Werkzeuge; der Lieferer schreibt dorthin, der Leser liest
  dort. Den Ordner nennt der Auftrag oder der Mensch; beide Werkzeuge tragen denselben Wert ein. Wie lange alte Sätze
  liegen bleiben, ist offen.
- 10.7 Dateien von außen (z. B. ein CSV-Eingang) liest das Werkzeug nur, aus einem Ordner, den der Mensch in der
  Oberfläche wählt oder der in `Config/` steht; sie bleiben auf dem Zielrechner. Wie das Werkzeug halb geschriebene
  Dateien erkennt, ist offen.
- 10.8 Dateien für den Menschen (z. B. eine Tabelle auf Knopfdruck) legt das Werkzeug in einen eigenen Unterordner unter
  `Data/`, je Lauf ein Ordner mit Zeitstempel (z. B. `Data/Export/<art>-JJJJMMTT-hhmmss/`). Eine vorhandene Datei
  überschreibt es nie. Die Dateien bleiben auf dem Zielrechner; das Format nennt der Auftrag.
- Grund: So lesen zwei Werkzeuge nie einen halben oder gemischten Stand, und Firmendaten bleiben auf dem Rechner.
- Stand: Export erprobt; Leser gebaut.

**Baustein 11 – Bauumgebung und Tests**
- 11.1 Die Bauumgebung hat meist kein Windows und kein Netz. Reine Python-Pakete, die ihr fehlen (z. B. fastapi und
  annotated_doc), nimmst du aus dem Laufzeit-Archiv (in einen Ordner außerhalb des Repos entpacken, in `sys.path`),
  nicht aus dem Internet. Kompilierte Pakete im Archiv (pydantic_core, pyodbc) sind für Windows gebaut und laufen
  unter Linux nicht; dafür nimmst du die Fassungen der Bauumgebung oder eine Attrappe (11.3) und nennst den Teil „nur
  unter Windows geprüft“. Wenn es noch kein Archiv gibt, dann beschafft der Mensch es zuerst (1.3).
- 11.2 Teste mit pytest gegen einen echten uvicorn auf 127.0.0.1 an einem freien Port (`urllib`), mit echten
  SQLite-Dateien im Temp-Ordner.
- 11.3 Ersetze Windows-APIs durch Attrappen: Größen der `ctypes`-Strukturen für x64 · SQL Server durch eine
  pyodbc-Attrappe auf SQLite · andere Werkzeuge durch nachgebaute Prozesse.
- 11.4 Klickabläufe laufen mit Node im Headless-Chrome über das DevTools-Protokoll und warten höchstens 15 s auf einen
  neuen Zustand.
- 11.5 `.cmd`, `.vbs` und `.ps1` laufen ohne Windows nicht. Ihr Test prüft den Text; die Lieferung nennt sie „unter
  Windows ungeprüft“.
- 11.6 Jede Änderung im Verhalten bekommt einen Test, der ohne sie fehlschlägt. Ein Test prüft das Manifest gegen den
  Git-Index.
- 11.7 Bau das riskanteste Paket zuerst. Erst wenn der Mensch es am Zielrechner sieht (Sperrpunkt), geht der Bau
  weiter. „Statisch geprüft“ schließt nichts ab.
- 11.8 Der Testordner heißt `tests/`. Windows unterscheidet Groß- und Kleinschreibung nicht; `Tests/` und `tests/` wären
  ein Ordner.
- Stand: erprobt.

**Baustein 12 – Arbeitsweise und Pflichtdateien (Best Practice)**
- 12.1 Arbeite nach dem öffentlichen Repo digifil-solutions-public: Regeln für KI-Instanzen in `kanon-01/`
  (Single Agent, Fassung 3.1), Aufträge und Anleitungen im Format `zwei-kanal-format/` (Fassung 1.3, mit den
  Vorlagen `readme-vorlage.md` und `auftrag-vorlage.md`), Bauweise im README, Abschnitt „Gemeinsame Bauweise“
  (Geheimes nie im Repo, Rückmeldungen als Issues, wenn das Werkzeug welche annimmt).
- 12.2 Ablauf (Intent-Driven Development): Der Mensch nennt Bedarf und Grund · eine KI schlägt vor und stellt höchstens
  drei Rückfragen, jede mit Empfehlung · der Mensch entscheidet, seine Worte kommen wörtlich in den Auftrag · Auftrag
  als Datei · Rolle mit Grenzen · Bau in Paketen, das riskanteste zuerst, Sperrpunkt am Zielrechner · Zwischenstand ·
  Review durch eine zweite KI mit Datei und Zeile · Abnahme am echten System. Keine KI prüft ihre eigene Arbeit; was
  gelten soll, steht als Datei im Repo.
- 12.3 Pflichtdateien je Werkzeug: `README.md` (Anleitung im Zwei-Kanal-Format nach `readme-vorlage.md` (12.1):
  Block A für die KI, Block B für Menschen, mit Blindtest) · `ARCHITEKTUR.md` ·
  `ANNAHMEN.md` (jede Festlegung mit Nummer, keine stillen Entscheidungen) · `EINSCHRAENKUNGEN.md` · `LAUFZEIT.md` ·
  `components.manifest.json` mit Erzeuger · `tests/`.
- 12.4 Version: die Konstante `VERSION` in `<paket>/__init__.py` und die Überschrift der README, beginnend bei 0.1.0.
  Die dritte Stelle zählt Behebungen, die zweite neue Funktionen; jede Änderung erhöht eine der beiden.
- 12.5 Ein Werkzeug = ein Ordner. Die Bau-KI schreibt nur dort und prüft vor jedem Commit mit `git status`, dass nichts
  anderes dabei ist.
- Stand: erprobt.

### WAHLMÖGLICHKEITEN (Vorschlag, nicht entschieden)

Bestehende Werkzeuge lösen diese Punkte verschieden. Bis der Betreiber entscheidet, gilt die Empfehlung.
- W1 Server-Rahmen: FastAPI (Empfehlung) oder reines Starlette.
- W2 Kopf zu GitHub: `Authorization: Bearer` (Empfehlung) oder `Authorization: token`. GitHub nimmt beide an.
- W3 Update-Weg: ein Steuerpult für alle Werkzeuge (Empfehlung, wenn eines vorhanden ist) oder je Werkzeug ein eigenes
  PowerShell-Skript (6.3, Updates ohne Steuerpult).
- W4 Schutz der POST-Anfragen: Sitzungstoken je Start (Empfehlung) oder ein fester Kopf wie `X-<Name>: 1`, der nur über
  die Vorabfrage des Browsers schützt.
- W5 Sicherheitsköpfe: voller Satz auf jeder Antwort (3.4, Empfehlung) oder nur `no-store` und `nosniff` auf
  statischen Dateien.
- W6 Eine Instanz: Verbindungsprobe (Empfehlung) oder Bind-Probe. Die Sperrdatei für jedes Werkzeug, das Daten
  schreibt, ist keine Wahl (2.4, 8.2).
- W7 Ordnernamen: `Config/`, `Data/`, `Logs/` (Empfehlung) oder ein Ordner `Daten/` mit `Konfig/` und `Logs/`.
- W8 FastAPI in der Bauumgebung: aus dem Laufzeit-Archiv (Empfehlung) oder aus einem Paketvorrat (Wheelhouse).
- W9 Fremde Texte in der Oberfläche: `textContent` (Empfehlung) oder `innerHTML` mit Escape-Funktion.
- W10 Feldname des Sitzungstokens in `/api/status`: `sitzungstoken` (Empfehlung) oder `token`.

### LEHREN (Fehler, die schon passiert sind, und die Vorgabe, die sie verhindert)

- L1 Der Server prüfte den Host-Kopf nicht; eine fremde Webseite hätte das Sitzungstoken lesen und Befehle auslösen
  können. → 3.2
- L2 Das Sitzungstoken wurde als `str` verglichen; ein Umlaut ergab 500 ohne Sicherheitsköpfe. → 3.2, 3.4
- L3 Ein Updater verarbeitete seine eigene Datei nie und erneuerte sich deshalb nicht; eine neue Laufzeit konnte so
  nicht ankommen. → 6.3 (Selbst-Update, Test)
- L4 Ein Hol-Skript nahm den Zugangsschlüssel als Parameter; PowerShell 5.1 speicherte ihn im Verlauf. → 7.4
- L5 Eine Installation lief mit 404, weil der Schlüssel im Konsolenfenster fehlte. → 7.1, 6.5
- L6 Ein Sitzungstoken geriet in einen Chat; das Werkzeug musste neu starten. → 7.4
- L7 Eine Sperrdatei mit wiederverwendeter Prozessnummer blockierte den Start. → 2.4
- L8 Eine Bind-Probe meldete einen eben beendeten Server noch über 10 s als belegt. → 2.3
- L9 Ein Stopp von außen hätte einen 33 Minuten langen Import mittendrin abgebrochen. → 2.6
- L10 Eine Datei wurde ohne Sperre gelesen, geändert und ersetzt, mit gemeinsamer `.tmp`; Einträge können verloren
  gehen, und `os.replace` scheitert unter Windows. → 5.7
- L11 „Neu gestartet“ wurde gemeldet, ohne zu prüfen, ob das Werkzeug antwortet. → 6.3
- L12 Fehler eines Auftrags standen nur im Auftragsdatensatz, nicht im Log. → 5.2, 9.4
- L13 `integrity_check` lief bei jeder Statusabfrage; eine Antwort kam nach 28 s mit Fehler 500. → 5.4
- L14 Der Kurzaufruf `.\<Skript>.ps1` scheiterte an der Ausführungsrichtlinie. → 6.3 (Aufruf mit `-ExecutionPolicy Bypass`)
- L15 `Tests/` und `tests/` sind unter Windows derselbe Ordner. → 11.8
- L16 Die Version blieb nach einem Paket unverändert. → 12.4
- Vorsorge, keine Lehre: Adressen über den Branch-Namen können eine Zeit lang alte Dateien liefern. → 6.3

```text
PRÜFUNG:      Die Ergebnisse der Schritte 1 bis 9 gelten zusammen. Jeder Baustein des Werkzeugs steht in seiner
              README oder ANNAHMEN.md als erprobt, gebaut oder offen.
FAIL-MODE:    Wenn eine Vorgabe am Zielrechner nicht funktioniert, dann bau die nächstbeste Lösung, schreib sie in
              ANNAHMEN.md und melde den Fund an die Rolle, die diese Datei führt (PFLEGE). Wenn ein Baustein oder eine
              Vorgabe hier „offen“ ist, dann entscheide selbst, schreib die Entscheidung in ANNAHMEN.md und nenne sie in
              der Lieferung. Wenn eine Wahlmöglichkeit (W1–W10) deinen Bau betrifft, dann nimm die Empfehlung und nenne
              sie. Eine Empfehlung mit dem Vermerk „unbelegt“ befolgst du wie eine Vorgabe; wenn sie nicht passt, dann
              gilt dasselbe wie oben (ANNAHMEN.md).
NICHT TUN:    Firmendaten stehen nur auf dem Zielrechner; in Repo, Issues, Protokollen und Beispielen stehen nur
              erfundene Werte. · Zugangsschlüssel liegen nur in der Windows-Anmeldeinformationsverwaltung oder
              in GITHUB_TOKEN, das Sitzungstoken nur im Speicher (7.4); in Dateien, Logs, Chats und Befehlszeilen
              schreibst du sie nicht. · Das Werkzeug installiert
              nichts und lädt zur Laufzeit nur aus der gewählten Ablage (Baustein 6). · Von dieser Vorgabe weichst du
              nur mit Eintrag in ANNAHMEN.md ab, nie still.
LIEFERUNG:    Liste der Bausteine mit Stand (erprobt, gebaut, offen) · Port · Abweichungen mit Nummer aus ANNAHMEN.md ·
              Ergebnis der Schritte 1 bis 9 · Dateien für Windows als „unter Windows ungeprüft“, bis der Mensch sie
              gesehen hat · jede Stelle, an der diese Vorgabe nicht reichte, mit Zitat.
REFERENZ:     digifil-solutions-public: kanon-01/, zwei-kanal-format/, README.md (Gemeinsame Bauweise) ·
              BELEGE.md in diesem Ordner (nicht öffentlich): je Vorgabe Datei, Zeile und Commit des Vorbilds.
PFLEGE:       Wenn ein Werkzeug einen Baustein anders löst oder ein neuer Fehler passiert, dann meldet die bauende
              Rolle das an die Rolle, die diese Datei führt. Die Datei bekommt dann eine neue Version (dritte Stelle:
              Berichtigung, zweite: neuer Baustein oder neue Vorgabe), BELEGE.md wird im selben Commit nachgezogen.
```

---

## BLOCK B – für Menschen

In kurzer Zeit sind mehrere kleine Werkzeuge entstanden, jedes in einem eigenen KI-Chat. Jedes hat dieselben
Grundfragen neu beantwortet: wie Python ohne Installation auf den Rechner kommt, wie man ein Werkzeug startet und
aktualisiert, wo der Zugangsschlüssel liegt. Manche Fehler sind dabei mehrfach passiert, etwa ein Schlüssel, der in
einer Textdatei von Windows landete, oder ein Server, der Anfragen von fremden Webseiten annahm.

Diese Datei sammelt die bewährten Antworten an einer Stelle. Wer das nächste Werkzeug baut, fängt hier an: Python 3.14
im Werkzeugordner, ein eigener Port, ein kleiner Webserver nur für den eigenen Rechner, eine Oberfläche im Browser,
SQLite für Daten und GitHub als Ablage für Aktualisierungen, Protokolle und Rückmeldungen. Zu jeder Vorgabe steht, ob
sie schon auf einem echten Rechner gelaufen ist, und welche Fehler sie verhindert.

Wo die bestehenden Werkzeuge verschiedene Wege gehen, nennt die Datei die Möglichkeiten mit einer Empfehlung. Darüber
entscheidest du; bis dahin gilt die Empfehlung.

## Was du im Alltag tust

Wenn du ein neues Werkzeug bauen lassen willst, gib dem Bau-Chat diese Datei mit. Er meldet dir am Ende je Baustein, ob
er erprobt, gebaut oder offen ist, und welche Abweichungen er gewählt hat. Prüfen musst du nur die Proben am eigenen
Rechner: Start, Stopp und Aktualisierung.
