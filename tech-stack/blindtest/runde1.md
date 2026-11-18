# Blindtest Runde 1 – 2026-11-18

- Stand der Datei: TECH-STACK.md 0.1, Block A (385 Zeilen), Commit ff1cf4e.
- Prüfende KI: neue Instanz, nur Block A, kein weiterer Zugriff.
- Probeaufgabe: „Lege ein neues Werkzeug ‚Muster‘ an: Ordner, Port, Laufzeit, Start, Manifest, Token-Ablage.“
- Ergebnis: Die KI konnte die Aufgabe in den Grundzügen lösen; 11 Ratestellen (5 echte Lücken, 6 Kleinigkeiten) und
  7 Widersprüche oder Lücken (davon die Zeilenenden als echte Lücke eingestuft). Alle sind behoben.

| Nr. | Stelle (gekürzt) | Was unklar war | Einstufung | Behebung |
|---|---|---|---|---|
| R1 | Ordner mit Paket | Wie Ordner-, Paket-, Datei- und Kopfnamen zusammenhängen; Name des Platzhalters in der Startseite | Kleinigkeit | BEGRIFFE: Platzhalter; 3.3 nennt den Platzhalter |
| R2 | Portliste des Repos | Datei und Ort der Liste | echte Lücke | 2.1 und Schritt 2: PORTS.md in der Wurzel, anlegen, wenn sie fehlt |
| R3 | Archiv unverändert und reproduzierbar | Woher das Archiv kommt; kopieren oder neu bauen | echte Lücke | 1.3: byte-gleich kopieren oder einmal beschaffen und packen |
| R4 | Ordner der entpackten Laufzeit | Liegt er in laufzeit oder im Werkzeugordner | Kleinigkeit | 1.5: im Werkzeugordner neben laufzeit |
| R5 | Aufruf mit -m | Arbeitsordner nicht festgelegt | Kleinigkeit | 1.5 und 1.6: Wechsel in den eigenen Ordner |
| R6 | Ordner in Schritt 2 | Config, Data, Logs, Backup fehlten dort | Kleinigkeit | Schritt 2 nennt sie und wer sie anlegt |
| R7 | Manifest | Aufbau, Bezug der Pfade, Umfang | echte Lücke | 6.3: Aufbau, Pfade, was nicht dazugehört, Kennzeichen |
| R8 | Steuerpult oder Hol-Skript | Wann welcher Installer; zwei Prüfwege | echte Lücke | Schritt 7 und 6.3: Steuerpult mit Manifest, sonst Hol-Skript als Spiegel |
| R9 | Oberfläche zeigt nur ja/nein | Wer legt den Schlüssel ab | echte Lücke | 7.3 neu: Feld in der Oberfläche, zwei Routen |
| R10 | eigenes Ziel ohne Rückfall | Name des Ziels | Kleinigkeit | 7.2 nennt das Ziel |
| R11 | Version im Paket | Datei oder Konstante | Kleinigkeit | 12.4: Konstante in der Paketdatei |

Widersprüche und Lücken:
- „unverändert“ gegen „Dateien sortiert“ (1.3) → 1.3 neu: Inhalt ungeändert, das Zip wird reproduzierbar gepackt.
- Nummer 1.3 gegen Fassung 1.3 (12.1) → BEGRIFFE: Fassungen stehen als „Fassung 1.3“; 12.1 angepasst.
- Ohne Archiv kein FastAPI in der Bauumgebung (11.1) → 11.1 verweist auf 1.3.
- Zwei Prüfwege beim Update (6.3) → 6.3 nennt Spiegel mit Blob-SHA und Manifest mit SHA-256 getrennt.
- Zwei Archive in laufzeit (1.5, 1.7) → an der Quelle geprüft: Spiegel löscht nichts, die Startdatei nimmt den letzten
  Treffer; 1.7 empfiehlt deshalb die Update-Art Manifest.
- Unbelegte Empfehlung ohne Regel → FAIL-MODE: wie eine Vorgabe befolgen.
- Zeilenenden: Mit eol=crlf liegen die Startdateien im Repo trotzdem mit LF und kommen so beim Update an → an der
  Quelle geprüft (git ls-files --eol: i/lf); so laufen sie bereits am Zielrechner. Baustein 1, Fallen, sagt das jetzt.
