# Vorlage: Anleitung im Zwei-Kanal-Format (Anwendung 2)

Kopiere den Inhalt des Blocks in eine neue Datei (zum Beispiel `README.md`) und ersetze alle `<…>`. Ein Hinweis hinter
`←` nennt die Bedingung für ein Feld oder eine Zeile: Lösche sie, wenn die Bedingung nicht zutrifft, und lösche in jedem
Fall den Hinweis. Beispiel: `beispiel-readme.md`.

````markdown
# <Name> <Version>

## BLOCK A – Auftrag an die einrichtende KI

```text
ZWECK:        <Was am Ende steht, in ein bis drei Sätzen, prüfbar.>
GILT FÜR:     <Wofür die Anleitung gedacht ist.>
GILT NICHT:   <Wofür nicht, und wo das stattdessen steht.>
VORAUSSETZUNG: <Sprache und Version, Zugriffe, Dienste, die vorher da sein müssen.>
DATEIEN:      <datei> (<wozu>) · <datei> (<wozu>) · …
BEGRIFFE:     <Begriff> = <genaue Bedeutung, wie die Schritte ihn verwenden>.   ← wenn ein Begriff mehrere Deutungen zulässt
VERHALTEN:    <Wie das Werkzeug sich heute verhält, je Funktion eine prüfbare Aussage.>   ← bei Werkzeugen, die laufen
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **<Kurzname>.** <Was genau zu tun ist: welche Datei, welche Stelle, welcher Wert.>
   *Ergebnis:* <Befehl oder Beobachtung, die zeigt, dass der Schritt gelang.>
2. **<Kurzname>.** <…> Wo etwas einzusetzen ist:

   | Platzhalter | einsetzen |
   |---|---|
   | `<…>` | <Quelle des Werts>. Wenn der Auftrag keinen Wert nennt, dann gilt die Vorgabe <Wert>; nenne sie in der Lieferung als offen. |
   | `<…>` | <Quelle des Werts>. Wenn der Wert fehlt, dann bleibt er offen, und der Schritt wartet.   ← für Adressaten, Veröffentlichung, Löschen und Zugangsdaten; dort gibt es nie eine Vorgabe |

   *Ergebnis:* <…>

```text
PRÜFUNG:      <Was am Ende alles bestätigt: ein Befehl oder die Ergebnisse der Schritte, die zusammen gelten.>
FAIL-MODE:    <Wenn ein Schritt nicht geht, dann …. Wenn nur eine Angabe fehlt, dann ….>
NICHT TUN:    <Je Grenze erst, was richtig ist, dann was die KI lässt.>   ← wenn es Grenzen gibt, die kein Schritt nennt
LIEFERUNG:    <angelegte und geänderte Dateien> · <Ergebnis jeder Prüfung> · offene Punkte ·
              jede Stelle, an der diese Anleitung nicht reichte, mit Zitat.
REFERENZ:     <Wo Einzelheiten stehen.>   ← wenn nötig
```

---

## BLOCK B – für Menschen

<Ein echter Vorfall oder ein Beispiel, das zeigt, welches Problem das hier löst.>

<Was es tut – so lang, wie ein Mensch zum Verstehen braucht, und kürzer als Block A.>

## Was du im Alltag tust

<Was der Mensch selbst tut, wenn es läuft, und woran er erkennt, ob es geklappt hat.>
````
