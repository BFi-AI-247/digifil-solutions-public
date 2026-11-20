# Kapsel lokal-befehle 0.4.0

Aufträge im Hintergrund, Befehle ohne Oberfläche und tägliche Läufe eines lokalen Werkzeugs.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt, wie lange Arbeit neben dem Server läuft und wie jede Funktion auch ohne Oberfläche geht.
GILT FÜR:     Rezepte lokal-python und lokal-powershell.
BRAUCHT:      Kapseln kern · lokal-server · lokal-log
```

### REGELN
- 1 Lange Arbeit läuft getrennt von der Annahme der Anfragen; der Server bleibt dabei antwortfähig. Es gibt genau einen
  Schreiber für Daten mit einer begrenzten Warteschlange von Aufträgen (z. B. 32 bis 64); ist sie voll, dann antwortet
  die Route mit 503. Läuft derselbe Auftrag schon, dann meldet die Route das. Ein Auftrag hat Kennung, Art, Schlüssel
  gegen Wiederholung, Beginn, Ende, Fortschritt und Zustand (`queued`, `running`, `succeeded`, `failed`, `cancelled`,
  `uncertain`). Jeder Fehler eines Auftrags steht im Log.
- 2 Zwischen Ausführungskontexten gehen nur geprüfte Datenobjekte, nie Verbindungen zur Anfrage oder COM-Objekte.
- 3 Nach einem Neustart werden zuvor laufende Aufträge abgeglichen oder als `uncertain` gemeldet; sie gelten nicht von
  selbst als erledigt oder gescheitert. Eine Zeitüberschreitung bei einer Wirkung nach außen kann „unklar“ heißen; so
  etwas wird nie blind wiederholt.
- 4 Jede Funktion gibt es auch als Schalter am selben Einstieg, z. B. `<Name>.cmd --status`. Die Rückgabe folgt
  Kapsel lokal-server (0, 1, 2). Die Ausgabe ist ein Ergebnis als JSON; Diagnosen gehen getrennt nach stderr oder ins
  Log. Zugangsschlüssel und Mailinhalte nimmt kein Schalter entgegen; größere Eingaben kommen über eine Datei.
- 5 Läuft eine Instanz, dann geht der Befehl über ihre API, denn sie ist der eine Schreiber: über dieselben Routen, mit
  denen die Oberfläche den Auftrag startet und seinen Zustand abfragt. Sonst arbeitet der Befehl selbst und hält so
  lange die Sperre mit `kommandozeile: true` und Port 0 (Kapsel lokal-server). Ein Werkzeug, dessen Befehle schreiben,
  führt deshalb immer die Sperre.
- 6 Beim Start per Doppelklick ohne Konsole gehen Ausgaben in eine Logdatei und Fehler zusätzlich in ein Meldungsfenster.
  Ein Lauf mit dem Schalter eines täglichen Laufs zeigt nie eines: Der Einstieg wertet diese Schalter aus, bevor er den
  Start ohne Konsole einrichtet.
- 7 Tägliche Läufe startet die Windows-Aufgabenplanung im Konto des Benutzers. Empfehlung (unbelegt): Die Aufgabe ruft
  `<Name>.cmd --<befehl>` auf, „Starten in“ ist der Installationsordner, damit die Startdatei auch nach einem Update die
  aktuelle Laufzeit findet; ein fester Pfad zu einer Laufzeit veraltet. Bei einem Fehler schreibt der Lauf den Grund ins
  Log und endet mit Rückgabe 1. Das Konsolenfenster der `.cmd` ist hinzunehmen. Die Aufgabe legt der Mensch nach der
  README an; das Werkzeug ändert die Aufgabenplanung nie ohne Auftrag.
- Grund: Was auch ohne Oberfläche geht, lässt sich planen und von einer KI prüfen; ein Schreiber verhindert Konflikte.
- Test: Status während eines Auftrags · volle Warteschlange · Befehl neben laufender Oberfläche · Neustart mit
  unklarem Auftrag.
- Stand: Python: Warteschlange und Prüfbefehle erprobt, Befehle für tägliche Läufe gebaut, Aufgabenplanung offen,
  Zustände `cancelled`/`uncertain` und Regel 3 Empfehlung (unbelegt). PowerShell: Hintergrundarbeit in Runspaces hat ein
  Vorbild (Belege); der Rest ist offen.
- Lehre: Fehler eines Auftrags standen nur im Auftragsdatensatz, nicht im Log (Regel 1).

## BLOCK B – für Menschen

Lange Verarbeitungen laufen im Hintergrund, und die Oberfläche bleibt bedienbar. Alles, was die Oberfläche kann, geht
auch als Befehl – so lässt es sich jeden Morgen von Windows starten.
