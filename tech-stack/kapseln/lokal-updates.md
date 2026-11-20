# Kapsel lokal-updates 0.4.0

Paket, Manifest, Erstinstallation und Update eines lokalen Werkzeugs, mit Sicherung und Rückweg.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt, wie ein Werkzeug auf den Rechner kommt und aktualisiert wird, ohne gemischten oder halben Stand.
GILT FÜR:     Rezepte lokal-python und lokal-powershell.
BRAUCHT:      Kapseln kern · lokal-server; für den Bezug über GitHub zusätzlich windows-zugang (Schlüssel)
BEGRIFFE:     Installationsordner = der Ordner des Werkzeugs auf dem Zielrechner. Manifest = `components.manifest.json`.
              Update-Art Spiegel = der ganze Ordner eines Branches · Update-Art Manifest = die Dateien aus dem Manifest.
```

### REGELN
- 1 Manifest: oben `produkt`, `stand`, `erzeugt`, `hinweis` und `komponenten`; je Komponente (z. B. `programm`,
  `laufzeit`, `doku`) eine Liste `dateien`; je Datei `pfad` (relativ zum Werkzeugordner, mit `/`) und `sha256`,
  wahlweise `nur_wenn_fehlt: true` (Vorlagen in `Config/`) oder `nur_pruefen: true` (wird nie geladen, nur verglichen).
  Nicht ins Manifest: das Manifest selbst, `tests/`, `Tools/`, Punktdateien, `Data/`, `Logs/`, `Backup/`.
- 2 Das Manifest erzeugt ein Skript in `Tools/` mit einer Prüfung auf Gleichstand, nie die Hand. Die Prüfsummen gelten für
  genau die Bytes, die ausgeliefert werden: im Repo über die Fassung im Git-Index (`git show :<pfad>`), nicht über die
  ausgecheckte Datei; in einem ZIP nach der endgültigen Kodierung und den Zeilenenden. Dateien und Manifest gehen in
  denselben Commit; danach ändert sich das Paket nicht mehr ohne neue Prüfsummen.
- 3 Bezugswege: ein lokales Paket (ZIP mit Werkzeugordner und Manifest) ist der Grundweg; GitHub, SharePoint oder ein
  Steuerpult sind wahlweise. Jeder Weg legt vor dem Laden einen unveränderlichen Stand fest. Bei GitHub:
  `GET /repos/{owner}/{repo}/branches/{branch}` liefert `commit.sha`; jede Datei des Laufs kommt von genau diesem Commit
  (`raw.githubusercontent.com/{owner}/{repo}/{sha}/…`, Rückfall contents-API mit `ref={sha}`), nie über den
  Branch-Namen. Eine Prüfsumme zeigt Gleichheit, nicht Vertrauen; die Quelle muss feststehen.
- 4 Plan: Zeig vor jeder Änderung einen Plan je Datei: neu, geändert, gleich, behalten, Abraum, Warnung. Ein Plan gilt
  einmal und höchstens 1 h.
- 5 Ablauf: Produkt prüfen · Werkzeug geordnet beenden, nicht während eines Auftrags (Kapsel lokal-server) · alle
  Dateien nach `Backup/<stempel>.neu/` laden oder entpacken und prüfen · die zu ersetzenden Dateien nach
  `Backup/<stempel>/` sichern · ersetzen, jede Aktion vorher in einem Journal vermerken und bei einem Fehler rückwärts
  zurücknehmen · Werkzeug starten und warten, bis die erwartete Version im Status antwortet. Ein Abbruch während des
  Ladens lässt alles, wie es war. Verwirf absolute Pfade, `..`, doppelte Ziele, Verknüpfungen und unter Windows
  kollidierende Namen; begrenze Größe und Zahl der Dateien.
- 6 `Config/` legt das Update nur an, wenn es fehlt. `Data/`, `Logs/` und `Backup/` fasst es nie an. Abgeräumt wird nur,
  was im alten Manifest stand und im neuen fehlt; die Update-Art Spiegel löscht nichts (Liste und Git-Blob-SHA je Datei
  aus `GET /repos/{owner}/{repo}/git/trees/{sha}?recursive=1`). Ein neues Datenformat wird eigens gesichert und
  übertragen; ein Rückweg im Code ist kein Rückweg der Daten.
- 7 Selbst-Update: Wer aktualisiert (Steuerpult oder Update-Skript), verarbeitet seine eigene Datei zuerst. Ein
  Steuerpult ersetzt sie und startet sich als neuer Prozess ohne Fenster neu; ein Update-Skript endet nach seiner
  Erneuerung mit der Bitte, es erneut zu starten. Nie mit gemischtem Stand weitermachen.
- 8 Mit Steuerpult: Das Werkzeug wird nach der Anleitung des Steuerpults eingetragen (typisch Name, Installationsordner,
  Port, Quelle, Update-Art); den Zugangsschlüssel für die Updates hält das Steuerpult, nicht das Werkzeug. Kann das
  Steuerpult das Werkzeug nicht aufnehmen, dann meldest du das und baust bis dahin Regel 9.
- 9 Ohne Steuerpult: Ein Hol-Skript in PowerShell (`Hole-<Name>.ps1`) für die Erstinstallation – der Mensch legt es in
  einen leeren Installationsordner und ruft dort `powershell -ExecutionPolicy Bypass -File .\Hole-<Name>.ps1` auf; es
  arbeitet wie ein Spiegel, behält `Config/` und fragt den Schlüssel verdeckt nur für den eigenen Lauf ab (Kapsel
  windows-zugang). Dazu ein Update-Skript `Update-<Name>.ps1` in der Wurzel des Werkzeugordners nach der Update-Art
  Manifest (Regeln 4–7). Es legt das angewendete Manifest als `components.manifest.json` im Werkzeugordner ab; daraus
  räumt das nächste Update ab, ohne diese Kopie räumt es nichts ab. Es bricht ab, solange das Werkzeug auf seinem Port
  lauscht oder seine Sperre gehalten wird (Rückgabe 2); der Mensch beendet das Werkzeug vorher und startet es danach.
  Empfehlung (unbelegt): Für seine Dauer hält es selbst die Sperre mit `kommandozeile: true`, damit kein täglicher Lauf
  dazwischen startet.
- Grund: Ein fester Stand verhindert gemischte oder alte Dateien (Adressen über den Branch-Namen können eine Zeit lang
  zwischengespeicherte alte Dateien liefern); Sicherung und Journal verhindern ein halbes Update.
- Fallen: Ein Updater, der seine eigene Datei nicht verarbeitet, erneuert sich nie und kann eine neue Laufzeit nicht
  bringen. „Neu gestartet“ zu melden, ohne auf eine Antwort zu warten, täuscht. Der Kurzaufruf `.\<Skript>.ps1`
  scheitert an der Ausführungsrichtlinie.
- Test: nachgebaute Quelle mit Störfällen (Prüfsumme falsch, Datei fehlt, Abbruch, Ziel gesperrt, Fehler beim
  Ersetzen) · Installation aus dem Manifest in einen leeren Ordner · zweites „Prüfen“ ergibt nichts zu tun ·
  Selbst-Update · Einstellungen bleiben unverändert. Skripte für Windows prüft der Mensch auf dem Zielrechner.
- Stand: Steuerpult mit Sicherung, Abbruch und Selbst-Update erprobt; Update-Skript ohne Steuerpult erprobt (frühere
  Fassung); Manifest mit Erzeuger erprobt (Python, PowerShell); lokales ZIP als Grundweg und Größengrenzen offen.

### WAHL UND LEHREN
- W1 Update-Weg: ein Steuerpult für alle Werkzeuge (Empfehlung, wenn eines vorhanden ist) oder je Werkzeug ein eigenes
  Update-Skript (Regel 9).
- Lehre: Ein Updater verarbeitete seine eigene Datei nie und erneuerte sich deshalb nicht (Regel 7).
- Lehre: „Neu gestartet“ wurde gemeldet, ohne zu prüfen, ob das Werkzeug antwortet (Regel 5).
- Lehre: Der Kurzaufruf `.\<Skript>.ps1` scheiterte an der Ausführungsrichtlinie (Regel 9).
- Vorsorge, keine Lehre: Adressen über den Branch-Namen können eine Zeit lang alte Dateien liefern (Regel 3).

## BLOCK B – für Menschen

Ein Update zeigt dir erst, was sich ändert, sichert den alten Stand und nimmt ihn bei einem Fehler zurück. Deine
Einstellungen und Daten fasst es nicht an.
