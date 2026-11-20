# Kapsel lokal-log 0.4.0

Das Tageslog eines lokalen Werkzeugs, mit Schwärzung von Geheimnissen.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt Log, Schwärzung und Fehlermeldungen; das Log bleibt auf dem Rechner.
GILT FÜR:     Rezepte lokal-python und lokal-powershell.
BRAUCHT:      Kapsel kern
```

### REGELN
- 1 Eine Tagesdatei `Logs/<werkzeug>_JJJJMMTT.log`, UTF-8 ohne BOM, eine Zeile je Meldung mit Zeit (ISO), Stufe,
  Ereignis und, wo es eine gibt, Auftragskennung; Zeilenumbrüche einer Meldung werden zu „ | “ in derselben Zeile.
- 2 Genau ein Schreiber: Alle Teile geben ihre Meldungen an ihn ab (wie, sagt die Laufzeit-Kapsel).
- 3 Schwärze vor dem Schreiben die ganze Zeile samt Fehlerdetails: bekannte Geheimnisse wörtlich (Sitzungstoken,
  Zugangsschlüssel) und Muster (`Authorization`, `X-…-Token`, `"token":`, `ghp_…`, `github_pat_…`, Zugangsdaten in
  Adressen, `password=` und ähnliche). Dasselbe gilt für Fehlerantworten: Sie nennen einen verständlichen Grund und eine
  Kennung; die Details bleiben geschwärzt im Log.
- 4 Regelmäßige Abfragen kommen nur bei Fehlern ins Log; jeder Fehler eines Auftrags kommt hinein.
- 5 Kein Mitschnitt der Konsole und keine ungefilterte Fehlersuche als Standard-Log. Inhalte von Nachrichten und Listen
  von Empfängern kommen nicht pauschal ins Log; braucht das Werkzeug eine solche Historie, dann ist sie ein eigener
  Datenbestand mit eigener Regel für Zugriff und Aufbewahrung.
- 6 Ein Fehler beim Schreiben des Logs verschwindet nie still (kein leerer `catch`); ein nicht schreibbarer Logordner
  ergibt eine sichtbare Meldung.
- 7 Getrennt davon steht das Technik-Protokoll zum Senden (Kapsel github-backend); das Tageslog wird nie gesendet.
- Grund: Das Log ist der erste Weg, einen Fehler am Zielrechner zu sehen; es darf nichts verraten.
- Test: ein erfundenes Token in Meldung, Fehlerdetails und Kopf; die Logdatei enthält es nicht · nicht schreibbarer
  Logordner.
- Stand: Python: Regeln 1–4 und 7 erprobt; Regeln 5 und 6 Empfehlung (unbelegt). PowerShell: offen.

## BLOCK B – für Menschen

Das Werkzeug schreibt jeden Tag eine Logdatei auf deinem Rechner. Schlüssel und Passwörter werden vorher unkenntlich
gemacht, damit du die Datei gefahrlos weitergeben kannst.
