# Blindtest Runde 5 – 2026-11-18

- Stand der Datei: Block A nach Runde 4 (460 Zeilen), Commit c9d5b71.
- Prüfende KI: neue Instanz, nur Block A, kein weiterer Zugriff.
- Probeaufgabe (wörtlich): „Ein neues Werkzeug „Etikett“ erzeugt aus einer Liste, die der Mensch in der Oberfläche pflegt, eine Austauschdatei, die ein anderes Werkzeug liest. Auf dem Rechner gibt es kein Steuerpult, und GitHub ist für dieses Werkzeug nicht verfügbar; Ablage und Updates gehen über einen freigegebenen Ordner. Nach einigen Wochen bekommt die Austauschdatei ein neues Feld. Plane Port, Start und Beenden, die Ablage der Liste, die Austauschdatei und ihre Änderung, das Protokoll, Verteilung und Updates ohne GitHub, Rückmeldungen und die Tests.“
- Ergebnis: Die KI konnte die Aufgabe planen und jede Angabe einer Vorgabe zuordnen; 31 Ratestellen (9 echte Lücken,
  22 Kleinigkeiten) und 12 Widersprüche oder Lücken. Fünf der echten Lücken liegen im Bereich „ohne GitHub“, den
  Baustein 6 als offen führt; sie sind jetzt dort als offene Punkte genannt (Entscheidung nach FAIL-MODE). Ob dieser
  Bereich als Empfehlung ausgearbeitet wird, entscheidet der Betreiber. Die übrigen echten Lücken sind behoben.

| Nr. | Stelle (gekürzt) | Was unklar war | Einstufung (Prüfer) | Behebung |
|---|---|---|---|---|
| R1 | Repo ohne GitHub | Was „das Repo“ ist und wer es hält | echte Lücke | Baustein 6: als offener Punkt genannt |
| R2 | Freigegebener Ordner | „Lokale Dateien“ oder „SharePoint“ | Kleinigkeit | Baustein 6: offen |
| R3 | Fester Stand ohne Commit | Festlegen und Prüfen ohne Commit und Git-Blob-SHA | echte Lücke | Baustein 6: als offener Punkt genannt |
| R4 | Weg in die Freigabe | Wie die Dateien aus der Bauumgebung dorthin kommen | echte Lücke | Baustein 6: offen (Ort von Repo und Pflichtdateien) |
| R5 | Hol-Skript ohne GitHub | Woher es im leeren Ordner die Quelle kennt | echte Lücke | Baustein 6: als offener Punkt genannt |
| R6 | Update-Skript ohne GitHub | Woher es die Quelle liest | Kleinigkeit | Baustein 6: offen |
| R7 | Beenden ohne Steuerpult | Kein Knopf und kein Schalter genannt | echte Lücke | 2.5: Knopf „Beenden“ und Schalter `--stop`, beide über `/api/shutdown` |
| R8 | Sperrdatei | Ob der Export als schreibender Befehl zählt | Kleinigkeit | 2.4: jedes Werkzeug, das Daten schreibt |
| R9 | Port | Einträge anderer Werkzeuge nicht einsehbar | Kleinigkeit | unverändert: `PORTS.md` im Repo, 2.3 fängt Belegung ab |
| R10 | Liste als JSON oder SQLite | „Kleine Datenmengen“ nicht beziffert | Kleinigkeit | unverändert: Fachentscheidung des Werkzeugs |
| R11 | Etiketten-Inhalte | Ob sie Firmendaten sind | echte Lücke | BEGRIFFE: Preisdaten zählen dazu; sie bleiben auf dem Zielrechner |
| R12 | Ort der Austauschdatei | Freigabe oder lokal | echte Lücke | BEGRIFFE: Firmendaten bleiben auf dem Zielrechner, auch im Austauschordner (10.6) |
| R13 | Werte der Pflichtfelder | `version` als Ganzzahl, `filter` | Kleinigkeit | unverändert: Vertrag des Werkzeugs (10.1) |
| R14 | Auslöser des Exports | Knopf, Änderung oder täglicher Lauf | Kleinigkeit | unverändert: Fachlogik |
| R15 | Wechsel auf die neue Version | Reihenfolge der Updates von Lieferer und Leser | echte Lücke | 10.5: Empfehlung (unbelegt) – erst der Leser, dann der Lieferer |
| R16 | Neues Feld | Schlüssel oben oder Spalte | Kleinigkeit | unverändert: beides ist ein neues Feld (10.5) |
| R17 | Alte Sätze | Aufbewahrung | Kleinigkeit | unverändert: in 10.6 als offen geführt |
| R18 | Protokolle senden | Ohne GitHub nicht beschrieben | Kleinigkeit | unverändert: Baustein 6, nur bauen, was gebraucht wird |
| R19 | Tageslogs | Wann sie gelöscht werden | Kleinigkeit | unverändert |
| R20 | Rückmeldungen ohne GitHub | Kein Ersatz für Issues | echte Lücke | Baustein 6: als offener Punkt genannt; 12.1 „wenn das Werkzeug welche annimmt“ |
| R21 | Körpergrenze | Nur 4 KB für Steuerbefehle genannt | Kleinigkeit | 3.5: feste Grenze je Route, für Daten nach Bedarf |
| R22 | Feld für den Zustand der Aufträge | Name und Werte | Kleinigkeit | unverändert: Beispiel in 2.6 |
| R23 | Eigenes Werkzeug erkennen | Woran die Probe es erkennt | Kleinigkeit | 2.3: `produkt` in `GET /api/status` |
| R24 | Felder des Manifests, Stempel | Inhalt von `stand`, `erzeugt`, `hinweis` | Kleinigkeit | unverändert |
| R25 | Laufzeit-Archiv ohne GitHub | Herkunft | Kleinigkeit | unverändert: 1.3 (byte-gleich übernehmen) |
| R26 | Updatetest | Nur „nachgebautes GitHub“ genannt | Kleinigkeit | Baustein 6: offen |
| R27 | „Sperrdatei lebt“ | PID neu vergeben | Kleinigkeit | unverändert: Prüfreihenfolge in 2.4 |
| R28 | Vorlagen ohne GitHub | Zugriff auf das öffentliche Repo | Kleinigkeit | unverändert: „ohne GitHub“ betrifft das Werkzeug, nicht die Bau-KI |
| R29 | Hol-Skript als Spiegel | Ganzer Ordner oder nur Manifest | Kleinigkeit | unverändert: 6.3 (wie ein Spiegel) |
| R30 | Version beim neuen Feld | Zweite oder dritte Stelle | Kleinigkeit | 10.5: zweite Stelle (12.4) |
| R31 | Starttest | Prüft Pakete, die das Werkzeug nicht braucht | Kleinigkeit | unverändert: Starttest prüft das Archiv |

Widersprüche und Lücken:
1. Sitzungstoken: 7.4 „nie in einer Antwort“ gegen 2.5 und 3.3; NICHT TUN nannte nur dauerhafte Ablagen → 7.4 und
   NICHT TUN: Das Sitzungstoken lebt nur im Speicher und steht nur in der Oberfläche und in `/api/status`.
2. Firmendaten „nur in Config/ und Data/“ gegen Austauschordner und Logs → BEGRIFFE: bleiben auf dem Zielrechner.
3. ZWECK „Ablage bei GitHub“ gegen „Empfehlung“ → ZWECK: „Ablage (GitHub empfohlen)“; Baustein 6 nennt die offenen
   Punkte ohne GitHub.
4. Repo ohne GitHub nicht bestimmt → Baustein 6: offener Punkt.
5. Beenden ohne Steuerpult → 2.5 (mit R7).
6. Kein Übergang beim Versionswechsel → 10.5 (mit R15).
7. Sperrdatei: 2.4 und W6 gegen 8.1 und 8.2 → 2.4 und W6: jedes Werkzeug, das Daten schreibt.
8. „Pfade nur in Config/“ gegen Hol-Skript im leeren Ordner → Baustein 6: offener Punkt (Quelle von Hol- und
   Update-Skript); mit GitHub nennt der Auftrag Besitzer und Repo.
9. Hol-Skript als Spiegel bringt Dateien außerhalb des Manifests mit → unverändert; so belegt, Kleinigkeit.
10. 12.1 „Rückmeldungen als Issues“ gegen 4.6 „wahlweise“ → 12.1: „wenn das Werkzeug welche annimmt“.
11. Meldungsfenster 8.3 gegen 8.4 → 8.3: Läufe mit dem Schalter eines täglichen Laufs zeigen keines.
12. Stand eintragen: Schritt 8 ohne „offen“ und ohne Ort → Schritt 8 nennt README oder ANNAHMEN.md und „offen“.
