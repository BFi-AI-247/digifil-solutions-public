# Kapsel web-feeds 0.4.0

Fremde Quellen und eigene Feeds.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt wie ein Web-Werkzeug fremde Feeds holt und eigene Inhalte als Feed anbietet.
GILT FÜR:     Rezept web
BRAUCHT:      Kapseln kern · web-server-php
```

### REGELN
- 1 Ein Werkzeug hat keine freie Suche im Netz. Fremde Feeds holt nur der Server, und nur aus einer festen Liste
  erlaubter Quellen. Er puffert die Antwort
  (z. B. 10 Minuten), repariert falsch kodierte Zeichen und liefert ein einheitliches JSON.
- 2 Eigene Inhalte bietet das Werkzeug als Atom-Feed an (`feed.xml`), mit `<link rel="alternate">` in jeder Seite.
- Grund: Keine offene Weiterleitung; die Oberfläche sieht immer dieselbe Form.
- Test: Quelle außerhalb der Liste ergibt einen Fehler; ein Feed mit falschen Zeichen kommt repariert an.
- Stand: erprobt.

### WAHL UND LEHREN
- Lehre: Fremde Feeds kommen mit falsch kodierten Zeichen; ohne Reparatur auf dem Server zeigt jede Oberfläche
  Zeichensalat (Regel 1).

## BLOCK B – für Menschen

Fremde Feeds holt nur der Server aus einer festen Liste; eigene Inhalte gibt es als Atom-Feed.
