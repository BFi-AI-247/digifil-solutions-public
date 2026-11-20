# Kapsel lokal-oberflaeche 0.4.0

Die Oberfläche eines lokalen Werkzeugs im Browser: HTML, CSS, JavaScript, ohne Internet.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt Aufbau und Verhalten der Oberfläche unter `Web/`.
GILT FÜR:     Rezepte lokal-python und lokal-powershell.
BRAUCHT:      Kapseln kern · lokal-server
```

### REGELN
- 1 Schreib die Oberfläche in HTML, CSS und JavaScript im Ordner `Web/`, getrennte Dateien, ohne Build-Schritt auf dem
  Zielsystem und ohne Datei aus dem Internet; alle Bibliotheken liegen im Werkzeug. Mehrere Skripte bindest du als
  ES-Module ein (`<script type="module">`), ein einzelnes mit `defer`; keine Skripte im HTML selbst.
- 2 Setz Texte vom Server oder von außen nur mit `textContent` ein. Wo HTML nötig ist, baust du es aus festen Elementen
  und maskierten Werten; frei eingegebenes HTML geht durch eine Bereinigung mit Positivliste. Eine Zeichenkodierung wie
  `&#...;` ersetzt keine Bereinigung.
- 3 Frag den Zustand im Takt ab, im Leerlauf alle 5 s, während eines langen Vorgangs jede Sekunde; nie zwei Abfragen
  übereinander.
- 4 Jede POST-Anfrage schickt das Sitzungstoken und `Content-Type: application/json` (Kapsel lokal-server). Während
  einer Anfrage ist der Knopf gesperrt; der Server schützt dieselbe Aktion zusätzlich gegen Wiederholung. Die
  Oberfläche zeigt „angenommen“ und „fertig“ getrennt; eine abgebrochene Verbindung heißt nicht, dass nichts geschah.
- 5 Zeig Zustand, Fortschritt, letzte erfolgreiche Verarbeitung und verständliche Fehler. Suche und Filter ändern nur die
  Anzeige, nie still gespeicherte Daten.
- 6 Wahlweise: Stile als eigene CSS-Dateien zum Umschalten; Sprachen als eine Textdatei je Sprache; ein Knopf
  „Rückmeldung“ (Kapsel rueckmeldungen); ein Knopf „Beenden“ (Kapsel lokal-server).
- Grund: Ohne Build-Schritt und ohne Internet läuft die Oberfläche auf jedem Zielrechner und bleibt prüfbar.
- Fallen: Eine Fehlermeldung mit HTML darin, über `innerHTML` gesetzt, wird ausgeführt. Ein Doppelklick startet sonst
  zwei Aufträge.
- Test: reine Logik mit `node --test` (Dateien `*.test.mjs`); Klickabläufe im Headless-Chrome (Kapsel lokal-tests);
  Konsole ohne Fehler; Betrieb ohne Internet; HTML als Eingabewert; Doppelklick; Neuladen während eines Auftrags.
- Stand: Regeln 1–3 und 6 erprobt (Python) · Regeln 4 und 5 Empfehlung (unbelegt) bis auf Sitzungstoken und Content-Type
  (erprobt).

### WAHL
- W1 Fremde Texte: `textContent` (Empfehlung) oder `innerHTML` mit Escape-Funktion.

## BLOCK B – für Menschen

Die Oberfläche ist eine Webseite, die nur aus dem Werkzeugordner kommt. Sie läuft ohne Internet und zeigt immer, was
gerade passiert.
