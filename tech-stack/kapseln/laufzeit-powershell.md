# Kapsel laufzeit-powershell 0.4.0

Windows PowerShell 5.1 als Laufzeit, ohne Python, und wie die gemeinsamen Kapseln in PowerShell gebaut werden.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt Laufzeit, Start, Server, Zeichenkodierung, Hintergrundarbeit und Tests eines lokalen Werkzeugs in
              Windows PowerShell 5.1.
GILT FÜR:     Rezept lokal-powershell.
BRAUCHT:      Kapseln kern · lokal-server
```

### REGELN
- 1 Nimm `powershell.exe` aus Windows PowerShell 5.1, nicht stillschweigend `pwsh.exe`, und keine Syntax oder Parameter,
  die erst PowerShell 7 kennt (z. B. kein `ForEach-Object -Parallel`, kein vorausgesetztes ThreadJob-Modul). Prüf beim
  Start `$PSVersionTable.PSVersion`, `$PSVersionTable.PSEdition`, `[Environment]::Is64BitProcess` und
  `$ExecutionContext.SessionState.LanguageMode`; Soll ist Desktop/5.1/x64/FullLanguage. Eine Abweichung meldest du vor
  jeder Verarbeitung.
- 2 Nimm die Klassen des .NET Framework, die Windows mitbringt. Zur Laufzeit wird kein Modul, Paketmanager oder Browser
  nachgeladen; eine zusätzliche Bibliothek liegt im Werkzeug und steht mit Version, Herkunft, Lizenz und Prüfsumme in
  `ABHAENGIGKEITEN.md`. Eine Datenbank wie SQLite gehört nicht zu dieser Laufzeit; braucht ein Werkzeug eine, dann ist
  das eine eigene Kapsel oder das Rezept lokal-python.
- 3 Ordner zusätzlich zu Kapsel lokal-server: `<Name>.cmd` (Start mit Konsole) · `<Name>.vbs` (wahlweise, ohne Konsole) ·
  `App/<Name>.ps1` (Einstieg, Parameter) · `App/Version.psd1` (Produkt und Version; gelesen mit
  `Import-PowerShellDataFile`) · `App/Modules/` (je Aufgabe ein Modul: Server, Daten, Aufträge, Log, wahlweise mehr).
  Den Werkzeugordner nimmt das Skript aus `$PSScriptRoot`; Pfade mit `Join-Path`, Dateinamen von außen mit
  `-LiteralPath`.
- 4 `<Name>.cmd` wechselt mit `cd /d "%~dp0"` in seinen Ordner und startet den festen Pfad von Windows PowerShell mit
  `-NoProfile -STA -File App\<Name>.ps1` und reicht die Argumente weiter. `-ExecutionPolicy Bypass` nur für diesen
  Prozess und nur, wenn die Umgebung den Weg zulässt; nie eine Richtlinie dauerhaft ändern. Gruppenrichtlinien,
  AppLocker, WDAC und der eingeschränkte Sprachmodus werden dadurch nicht aufgehoben.
- 5 `<Name>.vbs` ist nur Komfort: VBScript ist abgekündigt und kann fehlen oder gesperrt sein. Die `.cmd` bleibt immer
  nutzbar; die README verspricht keinen unsichtbaren Start.
- 6 Server: `System.Net.HttpListener` mit genau dem Präfix `http://127.0.0.1:<port>/`; der Browser öffnet genau diese
  Adresse (`localhost` passt nicht zum Präfix). Den Start prüfst du ohne Administratorrechte. Scheitert die Registrierung
  an Rechten, dann meldest du Fehlercode und Schritt; URL-Reservierungen, Firewall und Rechte änderst du nie selbst. Ein
  selbst gebauter HTTP-Parser als Ausweg ist nicht vorgesehen.
- 7 Sitzungstoken: 32 Byte aus `System.Security.Cryptography.RandomNumberGenerator`, nie `Get-Random` oder eine GUID.
  Vergleich nach Prüfung von Format und Länge Byte für Byte mit gleichbleibender Laufzeit (eigene Schleife), nie ein
  Textvergleich, der von Kultur oder Groß- und Kleinschreibung abhängt.
- 8 Eine Instanz: `[IO.File]::Open('Data\instance.lock', 'OpenOrCreate', 'ReadWrite', 'None')` und das Handle bis zum
  Ende halten (Kapsel lokal-server).
- 9 Zeichenkodierung: `.ps1`, `.psm1` und `.psd1` sind UTF-8 mit BOM (reines ASCII nur als bewusste Ausnahme in
  `ANNAHMEN.md`); `.cmd` und `.vbs` bleiben ASCII mit CRLF; Markdown, Webdateien, JSON und Logs sind UTF-8 ohne BOM.
  Maschinenlesbare Dateien liest und schreibst du mit .NET-Methoden und fester Kodierung, nie über die wechselnden
  Standards von `Out-File`, `Set-Content`, `>` oder `Export-Csv`. HTTP sendet UTF-8-Bytes mit richtigem Content-Type und
  der Zahl der Bytes, nicht der Zeichen.
- 10 JSON über `ConvertTo-Json` mit bewusst gesetzter Tiefe, aus Objekten mit festen Feldern (nie COM-Objekte oder
  beliebige .NET-Objekte). Listen bleiben bei null, einem oder vielen Elementen ein Array. Zeiten nach ISO 8601 mit
  Zeitzone, innen UTC; die Ortszeit zeigt erst die Oberfläche. Ein Weg über ASCII-JSON mit numerischen HTML-Entities ist
  eine Ausnahme bei nachgewiesenem Bedarf, kein Standard.
  Bestehende Dateien ersetzt du mit `[IO.File]::Replace` und Sicherungsdatei, die erste Anlage mit `[IO.File]::Move`
  (Kapsel daten-json).
- 11 Hintergrundarbeit: in einem begrenzten Runspace-Pool; zwischen Runspaces gehen nur geprüfte Daten, nie
  `HttpListenerContext` oder COM-Objekte (Kapsel lokal-befehle).
- 12 Befehle als Parameter des Einstiegs, z. B. `-Status`, `-Import -SourcePath <ordner>`, `-Export`, `-Stop`,
  `-SelfTest`; die `.cmd` reicht sie weiter (Kapsel lokal-befehle).
- 13 Manifest: `Tools/Erzeuge-Manifest.ps1` erzeugt und prüft es; weder dafür noch für das Werkzeug wird Python
  vorausgesetzt (Kapsel lokal-updates).
- 14 Tests: `tests/Run-Tests.ps1` für Windows PowerShell 5.1 mit einfachen eigenen Prüffunktionen oder einer mitgelieferten,
  festgelegten Pester-Fassung; keine unbekannte Pester-Installation, keine Python-Laufzeit auf dem Zielrechner. Werkzeuge
  der Bauumgebung sind davon getrennt (Kapsel lokal-tests).
- 15 Pflichtdateien zusätzlich zu Kapsel kern: `AUFTRAG.md` · `ABHAENGIGKEITEN.md` (Windows-Laufzeit und wahlweise
  Teile) · `PRUEFBERICHT.md` · `components.manifest.json`. Ein Laufzeit-Archiv gibt es in diesem Rezept nicht.
- Grund: Windows PowerShell 5.1 ist auf jedem Windows-Rechner vorhanden; ohne Python bleibt das Werkzeug dort lauffähig,
  wo nichts mitgebracht werden darf.
- Fallen (Fachwissen, nicht belegt, außer BOM): Ohne BOM liest Windows PowerShell 5.1 Umlaute im Skript falsch. `ConvertTo-Json` kürzt ab Tiefe 2 still und
  macht aus einer Liste mit einem Element ein einzelnes Objekt. `HttpListener` nimmt nur Anfragen an, deren Host zum
  Präfix passt; Fehler, die HTTP.sys selbst erzeugt, tragen nicht die eigenen Sicherheitsköpfe.
- Test: Start aus fremdem Arbeitsverzeichnis, mit Leerzeichen und Umlauten im Pfad, aus verschobenem Ordner; Prüfsummen
  nach dem Entpacken unverändert; Parser-Prüfung aller Skripte unter 5.1.
- Stand: Vorbilder in bestehenden PowerShell-Werkzeugen für Regeln 3, 6, 8, 9, 11 und 13 (Belege); die Kapsel als
  Ganzes ist offen bis zum ersten Bau nach ihr. Regel 7 Empfehlung (unbelegt).

## BLOCK B – für Menschen

PowerShell ist auf jedem Windows-Rechner schon da. Ein Werkzeug nach dieser Kapsel braucht deshalb nichts Zusätzliches
und startet über eine `.cmd`-Datei im Werkzeugordner.
