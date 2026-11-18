# Blindtest Runde 7 – 2026-11-18

- Stand der Datei: Block A nach Runde 6 (493 Zeilen), Commit 3835443.
- Prüfende KI: neue Instanz, nur Block A, kein weiterer Zugriff.
- Probeaufgabe: dieselbe wie in Runde 6 (Bestätigungsrunde), wörtlich: „Ein neues Werkzeug „Lager“ liest täglich CSV-Dateien aus einem Ordner in eine eigene Datenbank ein; ein Import kann mehrere Minuten dauern. Die Oberfläche zeigt Auswertungen. Auf Knopfdruck sendet das Werkzeug Protokolle an GitHub, und Rückmeldungen gehen als Issues ein. Es gibt kein Steuerpult; GitHub ist verfügbar, das Repo ist privat. Plane Laufzeit und Start, den Import samt Abbruch und erneutem Lauf, das Beenden während eines Imports, den täglichen Lauf, die Protokolle, den Zugangsschlüssel, Erstinstallation und Updates, die Version und die Tests.“
- Abweichung im Verfahren: Die prüfende KI sollte Stellen, die die Vorgabe ausdrücklich „offen“ nennt und für die sie
  ein Vorgehen angibt, getrennt aufzählen statt als Ratestellen. Der Plan war auf 40 Zeilen begrenzt.
- Ergebnis: 33 Ratestellen (6 echte Lücken, 27 Kleinigkeiten), 5 ausdrücklich offene Stellen mit Vorgehen,
  16 Widersprüche oder Lücken. Keine der 12 echten Lücken aus Runde 6 kam wieder; die prüfende KI folgte den neuen
  Vorgaben. Die neuen echten Lücken liegen tiefer. Sie sind behoben oder als unbelegte Empfehlung gekennzeichnet.

| Nr. | Stelle (gekürzt) | Was unklar war | Einstufung (Prüfer) | Behebung |
|---|---|---|---|---|
| R1 | 1.3 | Gibt es schon ein Werkzeug mit Archiv | Kleinigkeit | unverändert |
| R2 | Schritt 3, 1.5 | Im Starttest fehlt das Paket; die `.cmd` endet mit Fehler | Kleinigkeit | Schritt 3: kleinstes Paket mit `VERSION` |
| R3 | 1.5 | Fassung aus dem Archivnamen ohne Sprungmarken | Kleinigkeit | unverändert |
| R4 | 2.1 | `PORTS.md` über mehrere Repos | Kleinigkeit | unverändert |
| R5 | 2.4 | Sperre mit `kommandozeile` und neu vergebener PID blockiert den Start | echte Lücke | 2.4: Empfehlung (unbelegt) – Startzeit des Prozesses gegen `started_at` |
| R6 | 2.4 | Gleicher Fingerabdruck ohne Prüfung von `produkt` | Kleinigkeit | 2.4: `produkt` wie in 2.3 |
| R7 | 2.4, 8.2 | Rückgabewert bei „arbeitet gerade ohne Oberfläche“ | Kleinigkeit | 2.4: Rückgabe 1 |
| R8 | 2.5, 2.6 | Weitere Felder des Auftragszustands, Route zum Start | Kleinigkeit | unverändert: Fachlogik |
| R9 | 2.5, 5.5 | Import-Thread beim Ende nach 0,3 s | Kleinigkeit | Fallen in Baustein 2 an 5.5 angeglichen |
| R10 | 2.6 | Name des Zusatzschalters zu `--stop` | Kleinigkeit | unverändert |
| R11 | 5.2, 5.5 | Langer Import gegen Schreib-Thread mit Warteschlange; volle Warteschlange | echte Lücke | 5.2: Import ist ein Auftrag; „läuft bereits“; 503 bei voller Warteschlange |
| R12 | 5.5 | Gleicher Name, neuer Inhalt | Kleinigkeit | unverändert: Fachlogik |
| R13 | BEGRIFFE, 2.1 | Name und Format der Einstellungsdatei | Kleinigkeit | Schritt 2: `Config/<werkzeug>.config.json`, Vorlage im Paket |
| R14 | 10.7 | Ordnerwahl im Browser | Kleinigkeit | unverändert |
| R15 | 6.1 | Protokoll-Repo: wer, wo eingestellt, getrennt? | echte Lücke | 6.1: eigenes Repo, Standard im Code, Änderung in `Config/`, Standard aus dem Auftrag |
| R16 | 6.1, BEGRIFFE | Feste Felder der Ereignisse; sind Zählwerte Mengendaten? | echte Lücke | 6.1: Felder je Ereignis; Zählwerte für Dateien und Zeilen sind keine Mengendaten |
| R17 | 6.1 | Positivliste, Branch, Routen, abgelehnter Ref-Vorschub | Kleinigkeit | unverändert |
| R18 | 6.5, 7.3 | „Zugang prüfen“ für den Protokoll-Schlüssel | Kleinigkeit | unverändert |
| R19 | 6.4 | Privates Repo: Anwender ohne Zugang | echte Lücke | 6.4: Mensch braucht Zugang, die README sagt das |
| R20 | 6.3 | Quelle der Skripte, Rechte des Schlüssels | Kleinigkeit | unverändert |
| R21 | 6.3 | „Neben dem Werkzeug“ gegen Pfade im Manifest | Kleinigkeit | 6.3: in der Wurzel des Werkzeugordners |
| R22 | 6.3 | Altes Manifest für den Abraum | Kleinigkeit | 6.3: angewendetes Manifest bleibt im Werkzeugordner |
| R23 | 6.3 | Gilt der Ablauf auch für das Update-Skript | Kleinigkeit | 6.3: ja, wie beim Steuerpult |
| R24 | 6.3, 8.4 | Täglicher Lauf mitten im Update | echte Lücke | 6.3: Empfehlung (unbelegt) – Sperre mit `kommandozeile` für die Dauer des Updates |
| R25 | 6.3 | Spiegel legt Dateien ab, die das Manifest nie abräumt | Kleinigkeit | unverändert |
| R26 | 6.3 | Inhalt der Felder `stand`, `erzeugt`, `hinweis` | Kleinigkeit | unverändert |
| R27 | 2.4 | Umfang von `build` | Kleinigkeit | unverändert |
| R28 | 8.2 | Wartet der Befehl über die API | Kleinigkeit | unverändert |
| R29 | 8.4 | Konsolenfenster der `.cmd`, nur bei Anmeldung | Kleinigkeit | 8.4: Konsolenfenster hinzunehmen |
| R30 | 8.4, 9.2 | Zweiter Log-Schreiber | Kleinigkeit | unverändert |
| R31 | 12.4 | Erste Stelle der Version | Kleinigkeit | unverändert |
| R32 | Test in Baustein 6, 11.5 | PowerShell-Störfälle in der Bauumgebung | Kleinigkeit | Test in Baustein 6: 11.5, Störfälle am Zielrechner |
| R33 | Schritt 1 | Ort der Rollendatei | Kleinigkeit | unverändert: Kanon |

Ausdrücklich offen, mit Vorgehen (keine Ratestellen): Abbruch auf Knopfdruck (5.5) · halb geschriebene Dateien (10.7)
· Rückfrage vor dem Stopp, Stand von Baustein 2 · Aufgabenplanung (8.4) · Aufbewahrung alter Sätze (10.6) und Ablage
ohne GitHub (Baustein 6).

Widersprüche und Lücken:
1. Schritt 3 gegen 1.5 und Schritt 4 (Paket fehlt im Starttest) → Schritt 3 (mit R2).
2. 2.4: `kommandozeile` vor der Portprüfung; `produkt` fehlt → 2.4 (mit R5, R6).
3. 5.2 gegen 5.5 → 5.2 (mit R11).
4. Falle in Baustein 2 („halber Stand“) gegen 5.5 → Falle angeglichen.
5. Zwei Bedeutungen von „offen“ → BEGRIFFE und FAIL-MODE.
6. 6.3 Update-Skript: Ablauf, Manifest-Kopie, Ort → 6.3 (mit R21–R23).
7. Spiegel gegen Manifest-Update → unverändert (Kleinigkeit, wie Runde 5).
8. Test in Baustein 6 gegen 11.5 → Test ergänzt (mit R32).
9. 6.3 gegen 8.4 → 6.3 Empfehlung (mit R24).
10. 6.1 und BEGRIFFE → 6.1 (mit R15, R16).
11. 6.4 gegen VORAUSSETZUNG (privates Repo) → 6.4 (mit R19).
12. 8.4 gegen 8.3 und 1.5 (Konsole), zwei Log-Schreiber → Konsole in 8.4; Log-Schreiber unverändert.
13. 10.7 und `Config/` ohne Format → Schritt 2 (mit R13); Ordnerwahl unverändert.
14. Bedeutung der Reihenfolge in Baustein 6 → „Reihenfolge nach Nutzen“.
15. `PORTS.md` nur je Repo → unverändert.
16. 12.2 höchstens drei Rückfragen → unverändert (Regel des Kanons).
