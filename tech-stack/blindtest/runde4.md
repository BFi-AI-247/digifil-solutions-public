# Blindtest Runde 4 – 2026-11-18

- Stand der Datei: Block A nach Runde 3 (450 Zeilen), nicht einzeln committet; die Änderungen der Runden 3 und 4 gehen
  in einen gemeinsamen Commit.
- Prüfende KI: neue Instanz, nur Block A, kein weiterer Zugriff.
- Probeaufgabe (Kurzform; der genaue Wortlaut wurde nicht abgelegt): Ein neues Werkzeug „Kurs“ liest Tageswerte aus
  einer SQL-Server-Datenbank, nur lesend, legt sie lokal ab und hat einen Befehl ohne Oberfläche für den täglichen
  Lauf. Auf dem Rechner gibt es schon ein Steuerpult. Plane Verbindung, Ablage, Befehl, Eintrag ins Steuerpult,
  Updates und Zugang.
- Ergebnis: Die KI konnte die Aufgabe lösen und jede Angabe einer Vorgabe zuordnen; 10 Ratestellen (1 echte Lücke,
  9 Kleinigkeiten) und 5 Widersprüche oder Lücken. Alle sind behoben oder begründet unverändert.

| Nr. | Stelle (gekürzt) | Was unklar war | Einstufung | Behebung |
|---|---|---|---|---|
| R1 | Firmendaten | Kurse fehlten in der Aufzählung | Kleinigkeit | BEGRIFFE nennt Kurs-Daten |
| R2 | Sperrdatei | Ob ein Befehl ohne Oberfläche sie führt | Kleinigkeit | 2.4 nennt schreibende Befehle ohne Oberfläche (8.2) |
| R3 | Befehl bei laufender Instanz | Welche Route der Befehl nimmt | Kleinigkeit | 8.2: dieselben Routen wie die Oberfläche (Start und Zustand) |
| R4 | Steuerpult vorhanden | Wie das Werkzeug eingetragen wird und wessen Schlüssel die Updates holt | echte Lücke | Schritt 7 und 6.3: Eintrag nach der Anleitung des Steuerpults, typische Felder; den Schlüssel hält das Steuerpult |
| R5 | Baustein 7 | Ob das Werkzeug einen Schlüssel braucht, wenn das Steuerpult aktualisiert | Kleinigkeit | Schritt 7: Baustein 7 nur, wenn das Werkzeug selbst GitHub anspricht |
| R6 | PORTS.md | Welche Datei gilt, wenn Werkzeuge in mehreren Repos liegen | Kleinigkeit | unverändert: Empfehlung je Repo; 2.3 fängt einen belegten Port beim Start ab |
| R7 | Beispiel in 8.1 | Welcher Interpreter gemeint ist | Kleinigkeit | 8.1: Beispiel `<Name>.cmd --status`, die `.cmd` reicht die Schalter weiter |
| R8 | 8.1 gegen 7.4 | Ob der Schlüssel als Schalter kommen darf | Kleinigkeit | 8.1: Ausnahme mit Verweis auf 7.4 |
| R9 | Servernamen | Wo Server- und Datenbankname stehen | Kleinigkeit | BEGRIFFE und 5.6: nur in `Config/` auf dem Zielrechner |
| R10 | 12.1 | Die Vorlage der README war nur in 12.3 genannt | Kleinigkeit | 12.1 nennt `readme-vorlage.md` und `auftrag-vorlage.md` |

Widersprüche und Lücken:
- Bauumgebung Python 3.13 gegen Laufzeit 3.14 → VORAUSSETZUNG nennt beide getrennt.
- 4.6 als Pflicht gegen „Bau davon nur, was das Werkzeug braucht“ (Baustein 6) → 4.6: „Wahlweise“.
- 10.5 „vorher abgestimmt“ ohne Weg → schriftlich im Repo, mit der Rolle oder dem Menschen, der den Leser baut.
- 5.6 nannte die TLS-Einstellungen nicht → `TrustServerCertificate=yes`, beim Treiber 18 zusätzlich `Encrypt=no`.
- 2.4 gegen 8.2 (Sperrdatei) → mit R2 behoben.
