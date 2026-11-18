# Prüflesung Runde 8 – 2026-11-18 (kein Blindtest)

- Stand der Datei: TECH-STACK.md 0.2, Commit 7637d35.
- Prüfende KI: eine Instanz eines anderen Modells (GLM 5.3, über Mistral betrieben). Auf Entscheid des Betreibers las sie die ganze
  Datei vor der Probeaufgabe; die Runde ist daher eine Prüflesung mit Vorwissen, kein Blindtest. Zahl und Einstufung
  der Ratestellen sind mit den Runden 1–7 nicht vergleichbar.
- Quelle: Bericht der prüfenden KI im Postfach der pflegenden Rolle (nicht öffentlich), hier gekürzt; die Spalte
  „Behebung“ ist von der pflegenden Rolle.
- Probeaufgabe (wörtlich): „Ein neues Werkzeug „Bericht“ liest die Austauschdateien eines anderen Werkzeugs, rechnet daraus Kennzahlen in einer eigenen Datenbank und zeigt sie in der Oberfläche; auf Knopfdruck legt es eine Tabelle als Datei für den Menschen ab. Es soll dieselbe Laufzeit nutzen wie die anderen Werkzeuge. Auf dem Rechner gibt es ein Steuerpult. Plane Laufzeit und Pakete, Port und Start, das Lesen der Austauschdateien (auch wenn der Lieferer eine neue Version einführt), die Datenbank, die Oberfläche, das Log, Updates, die Version und die Tests.“
- Ergebnis: 11 Ratestellen (2 echte Lücken, 9 Kleinigkeiten), 5 ausdrücklich offene Stellen mit Vorgehen, 5
  Widersprüche oder Lücken. Eingearbeitet in TECH-STACK.md 0.3.

| Nr. | Stelle (gekürzt) | Was unklar war | Einstufung (Prüferin) | Behebung |
|---|---|---|---|---|
| R1 | 10.6 | Woher der Bau den Austauschordner nimmt | Kleinigkeit | 10.6: den Ordner nennt der Auftrag oder der Mensch; beide Werkzeuge tragen denselben Wert ein |
| R2 | 10.4, 10.5 | Wohin der Leser eine unbekannte Version meldet und welchen Stand er solange hat | echte Lücke | 10.4: Satz nicht einlesen, gelesene und erwartete Version in Log und Oberfläche melden, Daten bleiben auf dem letzten Stand |
| R3 | Baustein 10 | Keine Vorgabe für eine Datei an den Menschen | echte Lücke | 10.8 neu: eigener Unterordner unter `Data/`, je Lauf mit Zeitstempel, nie überschreiben, bleibt auf dem Zielrechner |
| R4 | GILT NICHT | Format der Datei, erneuter Knopfdruck | Kleinigkeit | 10.8: Format nennt der Auftrag; nie überschreiben |
| R5 | Probeaufgabe, 8.4 | Wann Lesen und Rechnen laufen | Kleinigkeit | unverändert: Fachlogik |
| R6 | 2.1 | Welcher freie Port | Kleinigkeit | unverändert |
| R7 | 1.3, 1.9 | Welches Werkzeug das Referenz-Archiv liefert | Kleinigkeit | unverändert: nennt der Auftrag (1.9) |
| R8 | 2.3, 2.5, 3.2 | Welche Adresse der Browser aufruft | Kleinigkeit | 2.2: `http://localhost:<port>/` |
| R9 | 2.4 | Umfang des Fingerabdrucks `build` | Kleinigkeit | 2.4: `VERSION` und `<paket>/`, `Web/`, `Sql/`, 12 Zeichen |
| R10 | 8.1 | Ist „Tabelle ablegen“ auch ein Schalter | Kleinigkeit | unverändert |
| R11 | 10.5 | Version des Vertrags oder des Werkzeugs | Kleinigkeit | 10.5: `version` ist eine ganze Zahl, getrennt von `VERSION` |

Ausdrücklich offen, mit Vorgehen: Abbruch auf Knopfdruck (5.5) · Rückfrage vor dem Stopp, Stand von Baustein 2 ·
Aufgabenplanung (8.4) · Aufbewahrung alter Sätze (10.6) · Ablage ohne GitHub (Baustein 6).

Widersprüche und Lücken:
1. W6 („Empfehlung“) gegen 2.4 und 8.2 (Pflicht) → W6: Die Sperrdatei für schreibende Werkzeuge ist keine Wahl.
2. 2.2 (nur 127.0.0.1) gegen 3.2 (Host `[::1]` erlaubt), Aufrufadresse fehlt → 2.2 nennt `http://localhost:<port>/`,
   3.2 vermerkt, dass `[::1]` nur als Kopf erlaubt ist.
3. 10.5 gegen 12.4 (Version des Vertrags oder des Werkzeugs) → 10.5 trennt beide.
4. Keine Vorgabe für Ausgaben an den Menschen → 10.8 (mit R3).
5. 1.9: starlette 1.7.0 und uvicorn 0.54.0 wirken unplausibel → am Archiv selbst geprüft: alle 18 Fassungen, SHA-256,
   Dateizahl und Größe stimmen; unverändert.
