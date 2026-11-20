# Kapsel web-daten 0.4.0

Daten eines Web-Werkzeugs: im Browser oder im privaten Ordner.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt wo und wie ein Web-Werkzeug Daten hält, ohne Datenbank.
GILT FÜR:     Rezept web
BRAUCHT:      Kapseln kern · web-aufbau
```

### REGELN
- 1 Zwei Wege (W1): im Browser oder im privaten Ordner auf dem Server.
- 2 Im Browser: `localStorage` mit einem Präfix je Werkzeug (die Vorschau mit eigenem Präfix) für kleine Stände,
  IndexedDB für Dokumente. Jeder Zugriff steht in `try/catch`. Der Nutzer kann alles als Datei sichern und wieder laden;
  für den Wechsel des Geräts gibt es einen Übertragungs-Code ohne Server.
- 3 Auf dem Server: JSON-Dateien im privaten Ordner. Schreiben unter einer Sperre (`flock`), erst in eine `.tmp`, dann
  `rename`. Ein Protokoll als `.jsonl`, eine Zeile je Änderung, nur anhängen. Löschen heißt Papierkorb, wiederherstellbar.
- 4 Eine Auslieferung (Workflow nach Kapsel web-auslieferung) lädt nie Daten in den privaten Ordner, außer der Zugangsdatei
  (Kapsel web-zugang); vorhandene Daten überschreibt sie nie. Das Wiederherstellen aus der Sicherung (Kapsel web-sicherung) ist ein eigener
  Schritt, den ein Mensch auslöst.
- 6 Jede Speicherung zählt einen Stand (`stand` + 1). Ändern zwei Personen gleichzeitig, dann gewinnt die letzte; das
  Protokoll zeigt beide. Empfehlung (unbelegt): Die Oberfläche schickt den gelesenen Stand mit; weicht er ab, dann
  antwortet der Server mit 409 und die Oberfläche lädt neu.
- 5 Ein neues Format liest alte Daten weiter. Die Reihenfolge einer Liste, an der etwas hängt (z. B. ein Tagesplan),
  änderst du nie; du ersetzt an gleicher Stelle oder hängst hinten an.
- Grund: Kein Datenbankserver; Dateien lassen sich sichern und von Hand prüfen.
- Falle: Zwei gleichzeitige Speichervorgänge ohne Sperre löschen einen davon.
- Test: zwei gleichzeitige Schreibvorgänge im lokalen Test; Laden einer alten Datei aus `tests/attrappe/`.
- Stand: erprobt.

### WAHL UND LEHREN
- W1 Daten im Browser (kein Server, kein Konto, Sicherung durch den Nutzer) oder im privaten Ordner (mehrere Nutzer
  teilen Daten, Sicherung nach Kapsel web-sicherung). Empfehlung: im Browser, wenn nur eine Person die Daten braucht.
- Lehre: Die Reihenfolge einer Lösungsliste ist der Tagesplan; umsortieren hätte alle früheren Tage geändert (Regel 5).
- Lehre: Ein neuer Import überschreibt nie, was jemand im Editor bearbeitet hat; bearbeitete Inhalte werden eine eigene
  Fassung.

## BLOCK B – für Menschen

Daten bleiben beim Nutzer im Browser oder in einem geschützten Ordner auf dem Webspace, nie im Repo.
