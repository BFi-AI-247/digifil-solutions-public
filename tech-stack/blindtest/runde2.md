# Blindtest Runde 2 – 2026-11-18

- Stand der Datei: Block A nach Runde 1 (416 Zeilen), Commit e096be0 vor den Änderungen dieser Runde.
- Prüfende KI: neue Instanz, nur Block A, kein weiterer Zugriff.
- Probeaufgabe: „Ein neues Werkzeug ‚Zaehler‘ liest jeden Tag eine CSV-Datei mit Stückzahlen aus einem Ordner,
  speichert sie in einer Datenbank und erzeugt einmal am Tag eine Austauschdatei, die ein anderes Werkzeug liest. Es
  soll auf Knopfdruck Protokolle ohne Firmendaten nach GitHub senden. Plane Daten, Austauschdatei, täglichen Lauf,
  Protokoll, Schutz des Servers und das Beenden während eines laufenden Imports.“
- Ergebnis: Die KI konnte die Aufgabe lösen und jede Angabe einer Vorgabe zuordnen; 12 Ratestellen (3 echte Lücken,
  9 Kleinigkeiten) und 6 Widersprüche oder Lücken. Alle sind behoben oder als offen gekennzeichnet.

| Nr. | Stelle (gekürzt) | Was unklar war | Einstufung | Behebung |
|---|---|---|---|---|
| R1 | Sperrdatei mit Platzhalter name | Platzhalter nicht erklärt (auch beim Log) | Kleinigkeit | 2.4 und 9.1 nehmen den Platzhalter für den Werkzeugordner |
| R2 | Token aus dem Status | Status nannte kein Feld für das Sitzungstoken | echte Lücke | 2.5 nennt die Felder und warum das Token dort stehen darf; W10 |
| R3 | Sperre mit freiem Port ersetzen | Ein Lauf ohne Oberfläche hat Port 0 und gälte immer als verwaist | echte Lücke | 2.4: feste Reihenfolge der Prüfungen, Lauf ohne Oberfläche zuerst |
| R4 | wer fragt vor dem Beenden | Aufrufer oder Server | echte Lücke | 2.6: Das Werkzeug beendet immer, der Aufrufer fragt; Update wartet |
| R5 | Import je Gruppe | Was eine Gruppe ist | Kleinigkeit | 5.5: Commit spätestens nach etwa 1 s; Überspringen über SHA-256 |
| R6 | Positivliste beim Senden | Ob das Tageslog dazugehört | Kleinigkeit | 6.1: nie |
| R7 | defekte Datei | Ab wann eine Datei defekt ist | Kleinigkeit | 6.1 nennt die Bedingung |
| R8 | Aufgabenplanung | Wer die Aufgabe anlegt | Kleinigkeit | 8.4: der Mensch nach der README (unbelegt, offen) |
| R9 | Meldungsfenster | Nachts wartet ein Fenster | Kleinigkeit | 8.3 nur beim Doppelklick; 8.4 ohne Fenster |
| R10 | Firmendaten | Ob Stückzahlen dazugehören | Kleinigkeit | BEGRIFFE: Mengen und Umsätze ergänzt |
| R11 | Austausch lokal | Ablageort und Aufräumen | Kleinigkeit | 10.6: Ort aus Config; Aufbewahrung offen |
| R12 | Content-Type | Mit Zusatz charset erlaubt? | Kleinigkeit | 3.2: beginnt mit application/json |

Widersprüche und Lücken:
- Status ohne Token gegen Ablösung über das Token (2.4, 2.5) → mit R2 behoben.
- Port 0 der Sperre gegen „Port frei → verwaist“ (2.4, 8.2) → mit R3 behoben.
- „endet nach 0,3 s“ gegen „fragt vorher nach“ (2.5, 2.6) → mit R4 behoben.
- Zu großer Körper ohne Statuscode und Platz in der Reihenfolge (3.5) → 3.5: 400 in der Route.
- Host [::1] erlaubt, Bindung nur an 127.0.0.1 (2.2, 3.2) → unschädlich, unverändert.
- Die zwei Teile, die die Aufgabe am meisten brauchte, sind offen (8.4 Aufgabenplanung, Rückfrage vor dem Stopp) →
  bleiben offen; die Vorgabe sagt jetzt, wie sie aussehen sollen.
