# Vorlage: Anleitung im Zwei-Kanal-Format 1.2 (Anwendung 2)

Kopiere den Inhalt des Blocks unten in eine neue Datei (zum Beispiel `README.md`), ersetze alle `<…>`, lösche Felder ohne
Inhalt („wenn nötig“) und die Kommentare. Erklärung der Felder: `konzept.md`, Anwendung 2. Beispiel: `beispiel-readme.md`.
Der Block ist ein Codeblock, damit die Platzhalter in spitzen Klammern hier sichtbar bleiben.

````markdown
# <Name> <Version>

<!-- Zwei-Kanal-Format 1.2, Anwendung 2. BLOCK A enthält alles, was zum Ausführen nötig ist, und muss allein genügen.
     BLOCK B ist für Menschen, in Klartext, und enthält nichts Ausführungsrelevantes. Diesen Kommentar löschen. -->

## BLOCK A – Auftrag an die einrichtende KI

```text
ZWECK:        <Was am Ende steht, ein bis drei Sätze, prüfbar.>
GILT FÜR:     <Wofür die Anleitung gedacht ist.>
GILT NICHT:   <Was nicht – und wo es stattdessen steht.>
VORAUSSETZUNG: <Sprache/Version, Zugriffe, Dienste, die vorher da sein müssen.>
DATEIEN:      <datei> (<wozu>) · <datei> (<wozu>) · …
BEGRIFFE:     <Begriff> = <genaue Bedeutung, wie die Schritte ihn verwenden>.   ← wenn nötig
VERHALTEN:    <Wie das Werkzeug sich heute verhält, je Funktion eine prüfbare Aussage.>   ← bei Werkzeugen, die laufen
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **<Kurzname>.** <Was genau zu tun ist: welche Datei, welche Stelle, welcher Wert. Ganze Sätze.>
   *Ergebnis:* <Befehl oder Beobachtung, die zeigt, dass der Schritt gelang.>
2. **<Kurzname>.** <…> Wo etwas einzusetzen ist:

   | Platzhalter | einsetzen |
   |---|---|
   | `<…>` | <Quelle des Werts>; sonst <Vorgabe> (in der Lieferung als offen nennen) – für Empfänger, Veröffentlichung, Löschen und Zugangsdaten keine Vorgabe: offen lassen, der Schritt wartet |

   *Ergebnis:* <…>

```text
PRÜFUNG:      <Was am Ende alles bestätigt: ein Befehl oder die Ergebnisse der Schritte, die zusammen gelten müssen.>
FAIL-MODE:    Ein Schritt geht nicht: nicht improvisieren, abbrechen und melden, welcher Schritt mit welchem Befund
              scheiterte. Teilerfolg ausdrücklich als Teilerfolg melden. Fehlt nur eine Angabe: die Vorgabe aus dem
              Schritt nehmen und sie in der Lieferung als offen nennen. <Projektspezifisches ergänzen.>
NICHT TUN:    <Was ausdrücklich verboten ist.>
LIEFERUNG:    angelegte/geänderte Dateien · Ergebnis jeder Prüfung · offene Punkte ·
              jede Stelle, an der diese Anleitung nicht reichte (mit Zitat).
REFERENZ:     <Wo Einzelheiten stehen.>   ← wenn nötig
```

---

## BLOCK B – für Menschen

<!-- Klartext: keine Funktions-, Datei- oder Feldnamen, keine Abkürzungen ohne Erklärung, ganze Sätze.
     Prüffrage: Weiß ein Leser nach diesem Block, wozu das Ganze gut ist und was er selbst tun muss – ohne Block A? -->

<Ein echter Vorfall oder ein Beispiel, das zeigt, welches Problem das hier löst.>

<Was es tut, in zwei, drei Absätzen – kürzer als Block A.>

## Was du im Alltag tust

<Was der Mensch selbst tut, wenn es läuft – und woran er erkennt, ob es geklappt hat.>
````
