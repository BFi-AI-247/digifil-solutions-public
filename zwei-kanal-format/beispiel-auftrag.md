# Beispiel: ein Auftrag im Zwei-Kanal-Format 1.2

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
- Datei: web/kalender.js, Funktion termineLaden(); dort nach dem Laden filtern, nicht in der Datenquelle löschen.
- „Heute“ ist der Kalendertag in der Zeitzone Europe/Berlin, nicht die Weltzeit.
- Termine ohne Enddatum gelten bis zum Ende ihres Startdatums.
- Test: tests/kalender.test.js um einen Fall „gestern beendet → nicht sichtbar“ und einen Fall „heute → sichtbar“ ergänzen.
- Arbeitszweig: feature/41-alte-termine. Kein Merge nach main; die Freigabe kommt vom Betreiber.
- Frist: Vorschau bis 2026-11-04, 18:00 Europe/Berlin.
LEITPLANKEN: keine Änderung an der Datenquelle (data/termine.json) · kein Löschen von Terminen · kein Push nach main.
FAIL-MODE: Lässt sich das Enddatum nicht eindeutig lesen (gemischte Formate in data/termine.json): abbrechen, die
  betroffenen Einträge mit Zeilennummer melden, nichts raten.
REQUIRE-ACK: RUN-ID RED-041 · Stand · Name des Arbeitszweigs und Commit · Ausgabe des Tests · jede Stelle, an der dieser
  Auftrag nicht reichte (mit Zitat).
ESKALATION: Bei Widerspruch zu einer Regel des Baus oder bei Unklarheit zur Zeitzone: nicht ausführen, Nachricht an
  Redaktion_2 mit der Frage.

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
Abweichungen: keine. Hinweis: drei Einträge in data/termine.json haben kein Enddatum; sie gelten nach deiner Regel
  bis zum Ende des Starttags – das war ausreichend beschrieben, nichts geraten.
Beleg: Commit 3f9a2c1 auf feature/41-alte-termine; Testausgabe „12 passed“.
```

## Was dieses Beispiel zeigt

- Block A nennt Datei, Funktion, Zeitzone, Zweig, Frist und Testfälle – alles, ohne das der Bau anders handeln könnte.
- Block B erzählt den Anlass und was danach anders ist, in zwei Absätzen, ohne eine einzige Angabe, die der Bau braucht –
  auch Freigabe und Vorschau stehen nur in Block A. Die Probe: Streicht man Block B, kann Bau_1 trotzdem richtig handeln.
- Ein Auftrag hat keinen Abschnitt „Was du im Alltag tust“; den gibt es nur in Anleitungen.
- LEITPLANKEN steht ausgeschrieben, weil Redaktion und Bau keinen gemeinsamen Katalog haben.
- Die Quittung beginnt mit der RUN-ID und sagt ausdrücklich, dass nichts geraten wurde.
