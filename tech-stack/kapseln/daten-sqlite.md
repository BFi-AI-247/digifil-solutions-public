# Kapsel daten-sqlite 0.4.0

Daten eines lokalen Werkzeugs in SQLite: ein Schreiber, Schema-Versionen, Importe, die nach einem Abbruch fortsetzen.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt SQLite als Datenhaltung eines lokalen Werkzeugs.
GILT FÜR:     Rezept lokal-python, wenn das Werkzeug mehr Daten hat, als JSON-Dateien tragen (Kapsel daten-json).
BRAUCHT:      Kapseln kern · lokal-befehle · laufzeit-python
```

### REGELN
- 1 SQLite über `sqlite3`: Der Schreiber setzt `PRAGMA journal_mode=WAL`, `busy_timeout=5000` und `foreign_keys=ON`.
  Leser öffnen mit `?mode=ro` und legen nie eine Datei an.
- 2 Genau ein Schreib-Thread mit begrenzter Warteschlange (Kapsel lokal-befehle); Routen lesen parallel. Ein Import ist
  ein Auftrag und läuft darin von Anfang bis Ende.
- 3 Schema-Versionen als Dateien `NNN_beschreibung.sql`, in Namensreihenfolge, je Datei eine Transaktion mit Eintrag in
  der Tabelle `schema_version`. Vor einer Änderung des Schemas wird gesichert; ein unbekanntes neueres Schema liest das
  Werkzeug nicht.
- 4 Die Statusabfrage läuft ohne `PRAGMA integrity_check`; diese Prüfung gibt es nur auf Knopfdruck. Im Leerlauf läuft
  `PRAGMA wal_checkpoint(PASSIVE)`.
- 5 Ein Import über viele Dateien setzt je Datei einen `SAVEPOINT`; ein Fehler kostet dann nur diese Datei. Committet wird
  nur zwischen zwei Dateien, sobald die laufende Gruppe etwa 1 s alt ist. Der SHA-256 einer Datei steht in derselben
  Transaktion wie ihre Zeilen; bereits eingelesene Dateien erkennt der Import daran und überspringt sie. So setzt ein
  neuer Lauf nach einem Abbruch (Beenden, Absturz) dort fort, wo der letzte Commit war; das Ende einer Datei ist die
  sichere Grenze für einen kontrollierten Stopp (Kapsel lokal-server). Einen Abbruch auf Knopfdruck sieht diese Kapsel
  nicht vor (offen).
- Grund: SQLite braucht keinen Dienst; ein Schreiber verhindert Sperrkonflikte.
- Fallen: Eine Statusabfrage, die bei jedem Aufruf `integrity_check` ausführte, antwortete nach 28 s mit Fehler 500
  (Ursache aus dem Code abgeleitet).
- Test: echte SQLite-Dateien im Temp-Ordner; Abbruch mitten im Import und Fortsetzen.
- Stand: erprobt; Sicherung vor Schemaänderung und sichere Grenze für den Stopp Empfehlung (unbelegt).
- Lehre: `integrity_check` lief bei jeder Statusabfrage (Regel 4).

## BLOCK B – für Menschen

Für größere Datenmengen nimmt ein Python-Werkzeug SQLite, eine Datenbank in einer einzigen Datei. Ein abgebrochener
Import macht beim nächsten Mal dort weiter, wo er stand.
