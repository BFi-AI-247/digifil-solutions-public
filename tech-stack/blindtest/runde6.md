# Blindtest Runde 6 – 2026-11-18

- Stand der Datei: Block A nach Runde 5 (474 Zeilen), Commit a97fb20.
- Prüfende KI: neue Instanz, nur Block A, kein weiterer Zugriff.
- Probeaufgabe (wörtlich): „Ein neues Werkzeug „Lager“ liest täglich CSV-Dateien aus einem Ordner in eine eigene Datenbank ein; ein Import kann mehrere Minuten dauern. Die Oberfläche zeigt Auswertungen. Auf Knopfdruck sendet das Werkzeug Protokolle an GitHub, und Rückmeldungen gehen als Issues ein. Es gibt kein Steuerpult; GitHub ist verfügbar, das Repo ist privat. Plane Laufzeit und Start, den Import samt Abbruch und erneutem Lauf, das Beenden während eines Imports, den täglichen Lauf, die Protokolle, den Zugangsschlüssel, Erstinstallation und Updates, die Version und die Tests.“
- Ergebnis: Die KI konnte die Aufgabe planen und jede Angabe einer Vorgabe zuordnen; 48 Ratestellen (12 echte
  Lücken, 36 Kleinigkeiten) und 15 Widersprüche oder Lücken. Die Probeaufgabe ging tiefer als die früheren
  (langer Import, Beenden während eines Auftrags, täglicher Lauf). Die echten Lücken sind behoben oder als offen bzw.
  als unbelegte Empfehlung gekennzeichnet.

| Nr. | Stelle (gekürzt) | Was unklar war | Einstufung (Prüfer) | Behebung |
|---|---|---|---|---|
| R1 | 1.3 | Gibt es schon ein Werkzeug mit Archiv | Kleinigkeit | unverändert: steht im Auftrag |
| R2 | 1.3/1.4 | Distribution ohne die Grundausstattung | Kleinigkeit | unverändert |
| R3 | 1.4 | Weitere Pakete erlaubt | Kleinigkeit | unverändert: Grundausstattung gilt |
| R4 | 2.1 | Inhalt von `PORTS.md` unbekannt | Kleinigkeit | unverändert |
| R5 | 2.3/2.4 | Reihenfolge Verbindungsprobe und Sperrdatei | Kleinigkeit | 2.3: mit Sperrdatei zuerst 2.4, der Fingerabdruck entscheidet |
| R6 | 2.4/2.6 | Ablösung bei anderem Fingerabdruck während eines Auftrags | echte Lücke | 2.4: Empfehlung (unbelegt) – nicht ablösen, melden, Rückgabe 1 |
| R7 | 2.4/2.5 | Sperrdatei bei sauberem Ende löschen | Kleinigkeit | unverändert |
| R8 | 3.1/5.1 | Wo Schreib-Thread und Listener starten | Kleinigkeit | unverändert |
| R9 | 5.5 | Abbruch durch den Menschen | echte Lücke | 5.5: ausdrücklich offen; ein neuer Lauf setzt nach Beenden oder Absturz fort |
| R10 | 5.5 | Commit nach 1 s mitten in einer Datei | echte Lücke | 5.5: Commit nur zwischen zwei Dateien; SHA-256 in derselben Transaktion wie die Zeilen |
| R11 | 5.5 | Ort der SHA-256, Name der Datenbank | Kleinigkeit | unverändert: Fachlogik |
| R12 | 5.2 | Langer Import im einzigen Schreib-Thread | Kleinigkeit | unverändert |
| R13 | 2.6/2.5 | Feld und Werte des Auftragszustands | echte Lücke | 2.6: Feld `state_key`, Wert `processing`, sonst z. B. `ready` |
| R14 | BEGRIFFE, Baustein 10 | Eingangsordner, halb geschriebene Fremddateien | echte Lücke | 10.7 neu: nur lesen, Ordner gewählt oder in `Config/`; Erkennung halb geschriebener Dateien offen |
| R15 | 2.6 | Wie `--stop` bei laufendem Auftrag fragt | echte Lücke | 2.6: Knopf „Beenden“ fragt; `--stop` nur mit Zusatzschalter (Empfehlung, unbelegt) |
| R16 | 2.5 | Hartes Ende nach 0,3 s | Kleinigkeit | unverändert: 5.5 setzt fort |
| R17 | 8.2 | Lauf ohne Oberfläche stoppen | Kleinigkeit | unverändert: verwaiste Sperre (2.4) |
| R18 | 8.1/8.4 | Name des Schalters | Kleinigkeit | unverändert: Fachlogik |
| R19 | 8.4 | Fester `pythonw`-Pfad veraltet nach einem Laufzeit-Update | echte Lücke | 8.4: Aufgabe ruft `<Name>.cmd --<befehl>` (Empfehlung, unbelegt) |
| R20 | 8.4 | Arbeitsordner der Aufgabe | echte Lücke | 8.4: „Starten in“ = Installationsordner |
| R21 | 8.4 | Rückgabe 1 ohne Bedingung | Kleinigkeit | 8.4: bei einem Fehler |
| R22 | 8.2/8.4 | Tageslauf während eines Imports, Zeitgrenze | Kleinigkeit | unverändert |
| R23 | 9.2 | Zwei Prozesse schreiben dieselbe Tagesdatei | Kleinigkeit | unverändert |
| R24 | 6.1 | Eigenes Protokoll-Repo, leeres Repo | Kleinigkeit | unverändert |
| R25 | 6.1 | Format des Technik-Protokolls | echte Lücke | 6.1: Dateiname, Zeilenformat, feste Ereignisse und was nie hineinkommt |
| R26 | 6.1 | Weitere Dateien der Positivliste | Kleinigkeit | unverändert |
| R27 | 6.1 | Ref-Vorschub scheitert, Zeitzone | Kleinigkeit | unverändert |
| R28 | 6.4 | „Sichtbare Fehler“ können Firmendaten tragen | echte Lücke | 6.4: Version, Browser, Zustand, Fehlerart; keine Meldungstexte mit Pfaden oder Firmendaten |
| R29 | 6.4 | Issue-Repo, Label | Kleinigkeit | unverändert |
| R30 | 7.3/7.2 | Ein Feld und eine Route, aber zwei Ziele | echte Lücke | 7.3: eigenes Feld und eigene Routen für den Protokoll-Schlüssel |
| R31 | 6.5 | Gegen welches Repo „Zugang prüfen“ prüft | Kleinigkeit | unverändert |
| R32 | Schritt 3/7 | Starttest vor dem Hol-Skript | echte Lücke | Schritt 3: der Mensch legt Archiv und Startdateien von Hand ab |
| R33 | 6.3 | Quelle der Skripte | Kleinigkeit | unverändert |
| R34 | 6.3 | Ort der Skripte, Hol-Skript im Manifest | Kleinigkeit | unverändert |
| R35 | 6.3 | Allgemeiner Ablauf gegen Update-Skript | Kleinigkeit | 6.3: „Ablauf beim Steuerpult“ |
| R36 | 6.3 | „Sperrdatei lebt“ bei neuer PID | Kleinigkeit | unverändert: 2.4 |
| R37 | 6.3 | Bestätigung des Plans | Kleinigkeit | unverändert |
| R38 | 6.3/5.3 | Sicherung vor Migration, Aufbewahrung | Kleinigkeit | unverändert |
| R39 | 6.3/1.7 | Hol-Skript erneut als Update | Kleinigkeit | unverändert |
| R40 | 1.7 | Reihenfolge bei mehreren Archiven | Kleinigkeit | unverändert: das Update lässt eines übrig |
| R41 | Baustein 1 | Archivgröße und GitHub-Grenze | Kleinigkeit | unverändert |
| R42 | 12.4 | „Jede Änderung erhöht sie“ | Kleinigkeit | 12.4: eine der beiden Stellen |
| R43 | 6.3/2.4 | Felder des Manifests, Umfang von `build` | Kleinigkeit | unverändert |
| R44 | Schritt 7/11.5 | Hol-Skript in der Bauumgebung nicht prüfbar | Kleinigkeit | Schritt 7: Testhelfer in Python; Hol-Skript am Zielrechner |
| R45 | 11.7/12.2 | Riskantestes Paket bei fester Reihenfolge | Kleinigkeit | Schritt 3 nennt es |
| R46 | Schritt 1, 12.1 | Quellen im Blindtest nicht lesbar | Kleinigkeit | unverändert: Folge des Verfahrens |
| R47 | Baustein 6 | Bedeutung der Reihenfolge | Kleinigkeit | unverändert |
| R48 | BEGRIFFE/Baustein 9 | Firmendaten im Tageslog | Kleinigkeit | BEGRIFFE: Log und Protokolle getrennt |

Widersprüche und Lücken:
1. Schritt 3 vor Schritt 7; feste Reihenfolge gegen „riskantestes zuerst“ → Schritt 3 (mit R32, R45).
2. 8.4 gegen 1.5 und 1.7 → 8.4 (mit R19–R21).
3. 5.5 in sich → 5.5 (mit R10).
4. Abbruch und Zustandsformat fehlen → 5.5 offen, 2.6 Feld (mit R9, R13).
5. 2.4 gegen 2.6; 2.3 gegen 2.4 → 2.4 Empfehlung, 2.3 Verweis (mit R5, R6).
6. 7.3 gegen 7.2 → 7.3 (mit R30).
7. 6.4 gegen NICHT TUN → 6.4 (mit R28).
8. Begriff „Protokoll“ doppelt → BEGRIFFE: Log und Protokolle; Baustein 9 heißt „Log mit Schwärzung“.
9. Begriff „Auftrag“ dreifach → 5.2: „Schreibvorgänge“; der Auftrag an die KI bleibt durch BEGRIFFE abgegrenzt.
10. 6.3 Ablauf gegen Update-Skript → „Ablauf beim Steuerpult“.
11. Ergebnis Schritt 7 in der Bauumgebung nicht prüfbar → Schritt 7 (mit R44).
12. Fremde Eingangsdateien → 10.7 (mit R14).
13. 1.3 gegen 1.4 → unverändert (Kleinigkeit).
14. Technik-Protokoll ohne Format → 6.1 (mit R25).
15. Kleinere Lücken (R17, R38–R40, R42, R43, R47) → nur R42 geändert.
