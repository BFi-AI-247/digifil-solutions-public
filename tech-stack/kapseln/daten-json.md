# Kapsel daten-json 0.4.0

Daten eines lokalen Werkzeugs als JSON-Dateien: sicher ersetzen, Verläufe anhängen, gleichzeitige Änderungen erkennen.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt JSON-Dateien als Datenhaltung für überschaubare Bestände.
GILT FÜR:     Rezepte lokal-python und lokal-powershell (dort der Standard).
BRAUCHT:      Kapseln kern · lokal-befehle
```

### REGELN
- 1 JSON-Dateien für überschaubare Bestände, UTF-8 ohne BOM; Verläufe als JSON-Zeilen (`.jsonl`), nur anhängen. Jeder
  Datensatz trägt Formatkennung, Version des Schemas und eine Revision.
- 2 Alle Änderungen gehen durch einen Schreiber; Lesen, Ändern und Schreiben derselben Datei stehen unter einer Sperre.
  Eine gleichzeitige Änderung mit veralteter Revision wird abgewiesen (409).
- 3 Ersetzen: Schreib die neue Fassung ganz in eine eindeutig benannte `.tmp` im selben Ordner, schließ und prüf sie, dann
  ersetze die alte atomar (wie, sagt die Laufzeit-Kapsel); für die erste Anlage umbenennen ohne Überschreiben. Bei einem
  Fehler bleibt die alte Fassung gültig.
- 4 Mehrere Dateien werden durch nacheinander Umbenennen nicht zu einer Einheit. Gehören sie zusammen, dann schreib sie
  in einen neuen, vollständigen Generationsordner mit Manifest und Prüfsummen und schalte ihn erst über einen atomar
  ersetzten Zeiger frei; Leser nehmen nur freigeschaltete Generationen. Oder ein einziger Schnappschuss hält alles, was
  zusammen geändert wird.
- 5 Importe: Vor dem Import ein SHA-256 der Eingabe, zusammen mit Art des Imports und Fassung des Lesers; diese Kennung
  steht im selben Schnappschuss wie die Daten. Eine Wiederholung liefert den vorhandenen Stand; eine neue Fassung des
  Lesers ist eine bewusste Neuverarbeitung. Fachliche Schlüssel nennt der Auftrag.
- 6 Fehlerhafte Dateien und Datensätze bekommen einen nachvollziehbaren Fehlerstatus. Eine Änderung des Schemas braucht
  Sicherung, Prüfung und Rückweg; ein unbekanntes neueres Format wird nie still gedeutet. Rohdaten, aktueller Stand,
  Verlauf und Exporte für Menschen liegen getrennt.
- Grund: Dateien brauchen keinen Dienst und lassen sich von Hand prüfen; atomares Ersetzen lässt nie eine halbe Datei
  zurück.
- Fallen: Unter Windows scheitert das Ersetzen, wenn ein anderer Thread die Datei gerade offen hat. Eine gemeinsame `.tmp`
  für mehrere Schreiber verliert Einträge.
- Test: Abbruch vor und nach dem Ersetzen · gesperrte Datei · zwei Schreiber · kaputtes JSON · Wiederholung eines Imports
  · Wechsel des Schemas; die Dateioperationen werden unter Windows tatsächlich geprüft.
- Stand: Regeln 1–3 gebaut (Python); Regeln 4–6 Empfehlung (unbelegt); PowerShell offen.
- Lehre: Eine Datei wurde ohne Sperre gelesen, geändert und ersetzt, mit gemeinsamer `.tmp`; Einträge können verloren
  gehen, und das Ersetzen scheitert unter Windows (Regeln 2, 3).

## BLOCK B – für Menschen

Kleinere Datenbestände liegen als lesbare Dateien im Werkzeugordner. Eine neue Fassung ersetzt die alte erst, wenn sie
vollständig geschrieben ist.
