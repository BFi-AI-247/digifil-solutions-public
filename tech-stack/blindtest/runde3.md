# Blindtest Runde 3 – 2026-11-18

- Stand der Datei: Block A nach Runde 2 (436 Zeilen), Commit 2ba08dd vor den Änderungen dieser Runde.
- Prüfende KI: neue Instanz, nur Block A, kein weiterer Zugriff.
- Probeaufgabe: „Ein neues Werkzeug ‚Notiz‘ hat nur eine Oberfläche, in der man Notizen schreibt; es speichert sie als
  Dateien, hat einen Knopf für Rückmeldungen und wird ohne Steuerpult installiert und aktualisiert. Plane die
  Oberfläche, die Ablage der Notizen, Rückmeldungen, Erstinstallation und Updates, die Version bei einer Änderung, die
  Tests in einer Bauumgebung ohne Netz und die Pflichtdateien.“
- Ergebnis: Die KI konnte die Aufgabe lösen und jede Angabe einer Vorgabe zuordnen; 9 Ratestellen (3 echte Lücken,
  6 Kleinigkeiten) und 5 Widersprüche oder Lücken. Alle sind behoben.

| Nr. | Stelle (gekürzt) | Was unklar war | Einstufung | Behebung |
|---|---|---|---|---|
| R1 | Issue anlegen oder öffnen | Per Schnittstelle mit Schlüssel oder im Browser | echte Lücke | 4.6 und 6.4: Browser-Seite mit vorbelegtem Text, ohne Schlüssel |
| R2 | Updates durch das Werkzeug selbst | Wie ein Werkzeug ohne Steuerpult aktualisiert wird | echte Lücke | 6.3: Update-Skript neben dem Werkzeug, mit Regeln; W3 angepasst |
| R3 | JSON-Dateien | Eine Datei je Notiz oder eine gesamt | Kleinigkeit | unverändert: Fachlogik des Werkzeugs |
| R4 | Version | Startwert | Kleinigkeit | 12.4: Beginn bei 0.1.0 |
| R5 | Hol-Skript | Data fehlte in der Aufzählung | Kleinigkeit | 6.3 nennt Data |
| R6 | Hol-Skript | Zielordner und wie das Skript auf den Rechner kommt | Kleinigkeit | 6.3: leerer Ordner, Herkunft des Skripts, Schlüssel bei privatem Repo |
| R7 | Pakete aus dem Archiv | Das Archiv ist für Windows, die Bauumgebung Linux | echte Lücke | an der Quelle geprüft: pydantic_core und pyodbc sind für Windows kompiliert; 11.1 nimmt nur reine Pakete aus dem Archiv |
| R8 | README im Zwei-Kanal-Format | Format nur über Verweis | Kleinigkeit | 12.3 nennt Vorlage und Aufbau |
| R9 | Reihenfolge bei GitHub | Ob Protokolle Pflicht sind | Kleinigkeit | Baustein 6: nur bauen, was das Werkzeug braucht |

Widersprüche und Lücken:
- „legt an“ gegen „öffnet“ beim Issue → mit R1 behoben.
- Empfehlung Update-Art Manifest gegen Hol-Skript als Spiegel; Schritt 7 prüfte nur die Installation aus dem Manifest
  → Hol-Skript nur für die Erstinstallation, Updates über Steuerpult oder Update-Skript (Manifest); Schritt 7 prüft
  auch das Hol-Skript.
- W3 empfiehlt ein Steuerpult, das es nicht immer gibt → W3: „wenn eines vorhanden ist“.
- Sperrdatei Pflicht für Befehle ohne Oberfläche (8.2) gegen nur bei langen Schreibaufträgen (2.4) → 8.2: Wer ohne
  Oberfläche schreibt, führt sie immer.
- Firmendaten in Issues ohne Vorschau → 6.4: vorbelegt werden nur technische Angaben; der Mensch sendet selbst.
