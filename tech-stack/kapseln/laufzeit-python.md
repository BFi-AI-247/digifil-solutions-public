# Kapsel laufzeit-python 0.4.0

Python 3.14 im Werkzeugordner, ohne Installation, und wie die gemeinsamen Kapseln in Python gebaut werden.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt Laufzeit, Start, Server-Rahmen und Bauumgebung eines lokalen Werkzeugs in Python.
GILT FÜR:     Rezept lokal-python.
BRAUCHT:      Kapseln kern · lokal-server
BEGRIFFE:     <paket> = Python-Paket des Werkzeugs, gleich <werkzeug> · <fassung> = Python-Fassung (z. B. 3.14.7).
```

### REGELN
- 1 Leg die Laufzeit als ein Archiv in den Werkzeugordner: `laufzeit/python-<fassung>-win64.zip`, eine vollständige
  Python-Laufzeit mit allen Paketen in `Lib/site-packages`. Auf dem Rechner wird nichts installiert. Jedes Werkzeug hat
  seine eigene Kopie; teile keine Laufzeit zwischen Werkzeugen.
- 2 Herkunft: Gibt es schon ein Werkzeug mit dem Referenz-Archiv aus Regel 7, dann kopiere dessen Archiv byte-gleich
  (gleicher SHA-256). Wenn nicht, dann besorgt der Mensch einmal eine portable Python-Distribution mit allen Paketen
  (bewährt: WinPython, 64 Bit); du packst ihren Inhalt ungeändert in das Zip, Dateien sortiert, mit festem Zeitstempel.
  SHA-256, Größe, Herkunft und Paketliste stehen in `LAUFZEIT.md`.
- 3 Grundausstattung: fastapi, starlette, uvicorn, pydantic, pyodbc; aus der Standardbibliothek sqlite3 und tkinter.
- 4 `<Name>.cmd` startet mit Konsole. Es wechselt zuerst in seinen eigenen Ordner (`cd /d "%~dp0"`) und sucht
  `laufzeit\python-*-win64.zip`. Fehlt im Werkzeugordner der Ordner `python-<fassung>-win64\`, dann entpackt es nach
  `python-<fassung>-win64.tmp\` (erst `tar`, sonst `Expand-Archive`) und benennt erst nach Erfolg um. Danach ruft es
  `python-<fassung>-win64\python.exe -E -s -X utf8 -m <paket>` auf und reicht Schalter weiter. `<Name>.vbs` setzt seinen
  Ordner als Arbeitsordner und startet ohne Konsole `python-<fassung>-win64\pythonw.exe -E -s -X utf8 -m <paket>`; ist
  die Laufzeit noch nicht entpackt, dann startet es die `.cmd` mit sichtbarer Konsole. Beide bleiben reines ASCII, ohne
  Sprungmarken.
- 5 Eine neue Fassung bringt ein Archiv mit neuem Namen. Die Update-Art Manifest räumt das alte Archiv ab; der alte
  entpackte Ordner bleibt als Rückweg liegen. Die Update-Art Spiegel löscht nichts, dann lägen zwei Archive in
  `laufzeit\`; gib Werkzeugen mit Laufzeit deshalb die Update-Art Manifest (Kapsel lokal-updates).
- 6 Starttest am Zielrechner: `python.exe -c "import sys,sqlite3,fastapi,uvicorn,pyodbc,tkinter"` im entpackten Ordner und
  `Get-FileHash .\laufzeit\python-<fassung>-win64.zip -Algorithm SHA256` gegen `LAUFZEIT.md`.
- 7 Referenz-Laufzeit (Stand dieser Kapsel):
  · Archiv `python-3.14.7-win64.zip`, SHA-256 `c1364d10327ae129121d9485f043303e17a6eb5f41cec99f9ff463e25164dfed`,
    17.416.341 Byte; entpackt 49.726.397 Byte in 1.369 Dateien; oberste Ebene `python.exe`, `pythonw.exe`, `Lib/`,
    `DLLs/` usw. Python 3.14.7, 64 Bit, aus WinPython WPy64-31470, ungeändert gepackt.
  · 18 Pakete in `Lib/site-packages`: annotated-doc 0.0.5 · annotated-types 0.8.0 · anyio 4.15.1 · click 8.5.0 ·
    colorama 0.4.6 · et_xmlfile 2.0.0 · fastapi 0.142.2 · h11 0.16.0 · idna 3.20 · openpyxl 3.1.5 ·
    opentelemetry-api 1.45.1 · pydantic 2.13.5 · pydantic_core 2.46.5 (für Windows kompiliert) · pyodbc 5.3.0 (für
    Windows kompiliert) · starlette 1.7.0 · typing_extensions 4.16.0 · typing-inspection 0.4.4 · uvicorn 0.54.0.
    Pakete, die ein Werkzeug nicht braucht, bleiben drin; ein ungeändertes Archiv ist leichter zu prüfen.
  · SQLite steckt in der Laufzeit (`sqlite3` mit `DLLs/sqlite3.dll`, SQLite 3.53.1); ein eigenes SQLite gibt es nicht.
    tkinter ebenso (Tcl/Tk 9.0).
  · Das Archiv liegt nicht bei dieser Kapsel: Jedes Werkzeug führt seine eigene Kopie, und ein Archiv bliebe für immer in
    der Git-Historie. Welches Werkzeug es byte-gleich liefert, nennt der Auftrag. Eine neuere Fassung nur auf Anweisung;
    dann bekommt diese Kapsel eine neue Referenz.
  · Nicht beizulegen: der ODBC-Treiber für SQL Server (gehört zum Rechner, Kapsel sqlserver) · Node.js und Chrome (nur
    Bauumgebung).
- 8 Ordner zusätzlich zu Kapsel lokal-server: `<paket>/`, `laufzeit/`, `.gitattributes` (`.cmd`, `.vbs`, `.ps1` mit
  `text eol=crlf`, das Archiv `binary`). Version als Konstante `VERSION` in `<paket>/__init__.py`, der Standard-Port
  ebenda. `build` über `VERSION`, `<paket>/`, `Web/` und `Sql/` (sortiert, ohne `__pycache__`).
- 9 Server: FastAPI mit uvicorn, `host="127.0.0.1"`, `access_log=False`, `log_config=None`, `lifespan="off"`, ohne
  Doku-Routen (`docs_url=None`, `redoc_url=None`, `openapi_url=None`). Die Prüfungen aus Kapsel lokal-server stehen in
  einer Middleware vor dem Routing. Sitzungstoken mit `secrets.token_hex(16)`, verglichen als Bytes mit
  `hmac.compare_digest`. Der Browser öffnet `http://localhost:<port>/`. Blockierende Arbeit (Dateien, Netz, Datenbank)
  läuft nicht in der Ereignisschleife, sondern über `run_in_threadpool` oder einen eigenen Leser-Pool.
- 10 Eine Instanz, bis die Sperre des Betriebssystems gebaut ist: Sperrdatei `Data/<werkzeug>.lock` (UTF-8 ohne BOM) mit
  `pid`, `port`, `started_at`, `version` und `build`. Beim Start in dieser Reihenfolge: Lebt die PID nicht, dann ist die
  Sperre verwaist (ersetzen, Warnung, starten) · trägt sie `kommandozeile`, dann nicht starten, melden · ist ihr Port
  frei, dann gehört die PID einem fremden Prozess (ersetzen, Warnung, starten) · gleicher `build`: nur den Browser
  öffnen · anderer `build`: ablösen nach Kapsel lokal-server. Empfehlung (unbelegt): Ist der Prozess mit dieser PID
  später gestartet als `started_at`, dann ist die Sperre verwaist. Weg zur Sperre des Betriebssystems (unbelegt): die
  Datei über `ctypes` mit `CreateFileW` ohne Freigabe öffnen und das Handle bis zum Ende halten.
- 11 Log mit einem Schreiber: Alle Threads geben über einen `QueueHandler` ab, ein `QueueListener` schreibt (Kapsel
  lokal-log). JSON-Dateien ersetzt du mit `os.replace` (Kapsel daten-json). Windows-Anmeldeinformationen über `ctypes`
  (Kapsel windows-zugang). Ohne Konsole (`pythonw.exe`) gehen Ausgaben ins Log, Fehler zusätzlich in ein
  Meldungsfenster (Kapsel lokal-befehle).
- 12 Manifest: `Tools/erzeuge_manifest.py` nach `git add`, mit `--pruefen` (Kapsel lokal-updates).
- 13 Bauumgebung: Reine Python-Pakete, die ihr fehlen (z. B. fastapi und annotated_doc), nimmst du aus dem
  Laufzeit-Archiv (in einen Ordner außerhalb des Repos entpacken, in `sys.path`), nicht aus dem Internet. Kompilierte
  Pakete im Archiv (pydantic_core, pyodbc) laufen unter Linux nicht; dafür nimmst du die Fassungen der Bauumgebung oder
  eine Attrappe und nennst den Teil „nur unter Windows geprüft“. Fehlt das Archiv, dann beschafft der Mensch es zuerst
  (Regel 2). Tests mit pytest gegen einen echten uvicorn auf 127.0.0.1 an einem freien Port (`urllib`); SQL Server über
  eine pyodbc-Attrappe auf SQLite.
- 14 Pflichtdatei zusätzlich zu Kapsel kern: `LAUFZEIT.md`.
- Grund: Ohne Administratorrechte gibt es keine Installation. `-E -s` schließt Python-Umgebungsvariablen und Pakete des
  Benutzers aus; `-X utf8` hält Umlaute stabil.
- Fallen: Der erste Start entpackt rund 50 MB und dauert länger. Git speichert die Startdateien trotz `eol=crlf` mit LF,
  und Update und Hol-Skript liefern genau diese Fassung; mit LF laufen sie (erprobt). Dass Sprungmarken mit LF scheitern
  können, ist Fachwissen, nicht belegt. Ohne Host-Prüfung nimmt uvicorn jeden Host an.
- Test: In der Bauumgebung prüft ein Test den Text der Startdateien; ausführen lassen sie sich nur am Zielrechner
  (Regel 6).
- Stand: erprobt, außer Regel 10 Satz 3 und 4 (unbelegt).

### WAHL
- W1 Server-Rahmen: FastAPI (Empfehlung) oder reines Starlette.
- W2 FastAPI in der Bauumgebung: aus dem Laufzeit-Archiv (Empfehlung) oder aus einem Paketvorrat (Wheelhouse).

## BLOCK B – für Menschen

Python kommt als Archiv im Werkzeugordner mit und wird beim ersten Start ausgepackt; auf dem Rechner wird nichts
installiert. Jedes Werkzeug hat seine eigene Kopie.
