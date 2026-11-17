# Beispiel: ein Auftrag im Zwei-Kanal-Format

<!-- Erfundenes Beispiel zu auftrag-vorlage.md. Verein, Personen, Dateien und Zeiten sind ausgedacht. -->

Situation: Ein Verein betreibt eine kleine Website mit einem Veranstaltungskalender. Zwei KI-Instanzen arbeiten daran:
„Redaktion_2“ pflegt die Texte, „Bau_1“ ändert den Code. Die Redaktion hat bemerkt, dass der Kalender vergangene
Termine weiter anzeigt, und beauftragt den Bau.

```text
BLOCK A
VON: Redaktion_2
AN: Bau_1
DATUM: 2026-11-03, 09:14 Europe/Berlin (gemessen)
RUN-ID: RED-041
AUFTRAG: Blende im Veranstaltungskalender alle Termine aus, deren Enddatum vor dem heutigen Tag liegt.
PARAMETER:
- Filtere in der Datei web/kalender.js in der Funktion termineLaden() nach dem Laden.
- „Heute“ ist der Kalendertag in der Zeitzone Europe/Berlin, nicht die Weltzeit.
- Ein Termin ohne Enddatum gilt bis zum Ende seines Startdatums.
- Ergänze in tests/kalender.test.js zwei Fälle: „gestern beendet → nicht sichtbar“ und „heute → sichtbar“.
- Liefere die Vorschau bis 2026-11-04, 18:00 Europe/Berlin.
LEITPLANKEN: Filtere nur die Anzeige. Die Datenquelle data/termine.json änderst du nicht, und du löschst keinen Termin. ·
  Schreib nur auf den Zweig feature/41-alte-termine. Main fasst du nicht an; die Freigabe für main gibt der Betreiber.
FAIL-MODE: Wenn sich ein Enddatum in data/termine.json nicht eindeutig lesen lässt, dann brich ab und melde die
  betroffenen Einträge mit Zeilennummer.
REQUIRE-ACK: RUN-ID RED-041 · Stand · Name des Zweigs und Commit · Ausgabe des Tests · Rückfragen · jede Stelle, an der
  dieser Auftrag nicht reichte, mit Zitat.
ESKALATION: Wenn dir ein Zugriffsrecht auf das Repo fehlt, dann frag den Betreiber im Chat; nur er vergibt Rechte.

BLOCK B
Auf der Startseite des Vereins stehen seit Wochen Veranstaltungen, die längst vorbei sind. Zwei Mitglieder haben sich
gemeldet, weil sie dachten, der Herbstmarkt finde noch einmal statt. Das wirkt ungepflegt und kostet Vertrauen.

Die Termine sollen deshalb von selbst verschwinden, sobald sie vorbei sind – ohne dass jemand sie von Hand löscht. Die
alten Einträge bleiben erhalten, nur sichtbar sind sie nicht mehr.
```

## Die Quittung dazu

```text
RED-041 · Quittung
Empfangen: 2026-11-03, 09:20 Europe/Berlin (gemessen)
Stand: erledigt – Filter in termineLaden(), zwei Tests ergänzt, Vorschau auf feature/41-alte-termine.
Abweichungen: keine. Drei Einträge in data/termine.json haben kein Enddatum; sie gelten nach deiner Regel bis zum Ende
  des Starttags.
Fragen: keine
Beleg: Commit 3f9a2c1 auf feature/41-alte-termine; Testausgabe „12 passed“.
```
