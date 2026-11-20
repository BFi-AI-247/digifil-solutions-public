# Kapsel web-ki 0.4.0

KI-Anbindung über den Server.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt KI-Aufrufe aus einem Web-Werkzeug: nur über den Server, nur als Vorschlag.
GILT FÜR:     Rezept web
BRAUCHT:      Kapseln kern · web-server-php · web-zugang
```

### REGELN
- 1 KI-Aufrufe gehen nur über den Server; die Schlüssel stehen in `zugang.php`. Wenn mehrere Anbieter möglich sind,
  dann wählt der Nutzer; fehlt ein Schlüssel, dann sagt der Server „nicht eingerichtet“ (503).
- 2 Die KI macht nur Vorschläge. Ausgeführt wird erst, wenn der Mensch „Übernehmen“ drückt.
- 3 Antworten der KI liest das Werkzeug tolerant: Es sucht das erwartete JSON auch in umgebendem Text und meldet, was
  es nicht lesen konnte, statt abzubrechen (Stand: gebaut, als eigene Sammlung von Lesern für PHP, JavaScript und
  Python).
- 4 Im Test ersetzt eine Attrappe die KI (Umgebungsvariable, die auf einen Ordner mit festen Antworten zeigt).
- 5 Ohne eigenen Schlüssel keine KI-Funktion für Fremde; eine Ausnahme gibt nur der Auftrag.
- Grund: Kosten und Fehler der KI bleiben beim Menschen sichtbar und umkehrbar.
- Test: Durchlauf mit Attrappe; Anfrage ohne Schlüssel ergibt 503.
- Stand: erprobt (Regeln 1, 2, 4) · gebaut (Regel 3).

### WAHL UND LEHREN
- W4 KI-Anbieter: Claude oder Mistral, wählbar (Regel 1).

## BLOCK B – für Menschen

Die KI macht Vorschläge; übernommen wird erst, was der Mensch bestätigt.
