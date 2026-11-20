# Ordner tech-stack – Einstieg (Fassung 0.4.1)

## BLOCK A – für die lesende KI

```text
ZWECK:        Dieser Text führt in den Ordner tech-stack/ ein: was in ihm liegt, wer die Dateien wie benutzt und wie
              Rezepte und Kapseln gepflegt werden. Das Ziel ist erreicht, wenn ein Leser allein mit diesem Text weiß,
              welche Datei er wem gibt und wohin Befunde gehen.
GILT FÜR:     Menschen und KI-Instanzen, die ein neues Werkzeug bauen lassen, ein bestehendes prüfen lassen oder die
              Bauvorgabe pflegen.
GILT NICHT:   Die Regeln selbst (stehen in den Kapseln; dieser Text wiederholt sie nicht) · die Belege (belege/; nicht
              öffentlich) · das Verfahren der Prüflesungen (blindtest/README.md).
VORAUSSETZUNG: Lesezugriff auf diesen Ordner (belege/ nur für die pflegende Rolle; in einer öffentlichen Fassung fehlt
              er). Wer ein Werkzeug bauen lassen will, braucht eine bauende KI und einen Auftrag für sie.
DATEIEN:      README.md (dieser Einstieg) · rezepte/ (je Art von Werkzeug eine Liste von Kapseln mit Schritten:
              lokal-python.md, lokal-powershell.md, web.md) · kapseln/ (je Aufgabe eine Datei, die sie ganz regelt;
              kern.md gilt immer) · belege/ (Beleg je Regel; nicht öffentlich) · TECH-STACK.md und TECH-STACK-2.md
              (Wegweiser für alte Verweise) · blindtest/ (Prüflesungen der Fassungen bis 0.3).
BEGRIFFE:     Repo = die Ablage eines Werkzeugs; das muss kein GitHub-Repo sein (kapseln/kern.md). Rezept, Kapsel und
              Stand: siehe kapseln/kern.md. Pflegende Rolle = die Rolle, die diesen Ordner führt;
              welche das ist, steht in der Rollendatei des Projekts. Gibt es keine, dann ist es der Mensch, der diesen
              Ordner verantwortet.
```

### SCHRITTE (Schritt 1 oder 2, je nach Fall; Schritt 3, wenn etwas auffällt; Schritt 4 nur für die pflegende Rolle)

1. **Neues Werkzeug bauen lassen.** Wähl das Rezept: `rezepte/lokal-python.md` für ein Werkzeug auf dem eigenen Rechner
   mit Python, `rezepte/lokal-powershell.md` für eines nur mit Windows-Bordmitteln (wahlweise mit Outlook),
   `rezepte/web.md` für ein Web-Werkzeug. Gib der bauenden KI das Rezept, den Ordner `kapseln/` und den Auftrag,
   sonst nichts aus diesem Ordner.
   *Ergebnis:* Der Bau nennt Rezept und gewählte Kapseln und beginnt mit dem ersten Schritt des Rezepts.
2. **Bestehendes Werkzeug prüfen lassen.** Gib einer prüfenden KI das passende Rezept, `kapseln/` und das Werkzeug.
   *Ergebnis:* Die Prüfung nennt je Kapsel, ob das Werkzeug ihr folgt.
3. **Befunde melden.** Ein Fehler im Werkzeug geht an die KI, die es baut, oder als Issue an dessen Repo. Nur eine
   Regel, die nicht reicht oder auf dem Zielsystem nicht passt, geht an die pflegende Rolle: Ein Mensch sagt es ihr im
   Chat, eine KI schreibt eine Nachricht in ihr Postfach. Nenn Kapsel und Nummer der Regel (z. B. lokal-server, Regel 5)
   und was geschah. Bis zur Antwort gilt die geltende Fassung; die Abweichung steht in der ANNAHMEN.md des Werkzeugs.
   *Ergebnis:* Der Befund liegt bei der pflegenden Rolle. Sie antwortet mit einer neuen Fassung der Kapsel oder mit
   einer Ablehnung samt Grund.
4. **Pflegen.** Jede Kapsel hat ihre eigene Fassung (dritte Stelle Berichtigung, zweite neue Regel); ein Rezept nennt
   nur Kapseln. Eine neue Fähigkeit wird eine neue Kapsel mit Zweck, Voraussetzungen, Ein- und Ausgabe, Wirkung nach
   außen, Fehlerweg, Test und Herkunft; sie bekommt erst nach einer Prüfung einen höheren Stand. Verweise nennen immer
   eine ganze Kapsel, nie einen Teil eines anderen Dokuments. Jede neue Regel braucht einen Beleg in belege/ im selben
   Commit.
   *Ergebnis:* Kapsel, Rezept und Beleg passen zusammen; die Fassung ist erhöht.

```text
PRÜFUNG:      Ein Leser beantwortet nach diesem Text: was liegt in diesem Ordner, wem gebe ich welche Datei, wohin
              gehen Befunde. Die Antworten stehen hier oder in den benannten Dateien.
FAIL-MODE:    Wenn dieser Text eine Frage nicht beantwortet, dann steht sie in kapseln/kern.md; fehlt sie auch dort,
              dann gilt der FAIL-MODE der Kapsel kern.
NICHT TUN:    Diese README ersetzt kein Rezept. · Gib belege/ nicht weiter; er ist nicht öffentlich. · Gib nie
              Zugangsschlüssel oder Firmendaten mit. · Ändere Kapseln und Rezepte nicht selbst; Befunde gehen an die
              pflegende Rolle.
LIEFERUNG:    Dieser Text legt nichts an und ändert nichts. Wer ihm folgt, nennt in seiner eigenen Lieferung die
              weitergegebenen Dateien und jede Stelle, an der dieser Text nicht reichte, mit Zitat.
REFERENZ:     rezepte/ · kapseln/ · blindtest/README.md (Prüflesungen).
```

---

## BLOCK B – für Menschen

Mehrere kleine Hilfsprogramme sind hier nacheinander entstanden, jedes in einem eigenen Gespräch mit einer künstlichen
Intelligenz – für den eigenen Rechner in Python oder PowerShell, für das Netz als Web-Werkzeug. Immer wieder wurden
dieselben Grundfragen neu beantwortet, und manche Fehler passierten mehrfach.

Dieser Ordner sammelt die bewährten Antworten in Kapseln: Jede Kapsel regelt eine Aufgabe ganz, etwa den kleinen
Webserver, das Log oder die Mail-Entwürfe in Outlook. Was alle Werkzeuge gemeinsam haben, steht in der Kapsel kern. Ein
Rezept sagt, welche Kapseln ein Werkzeug einer Art braucht. Eine nicht öffentliche Belegliste zeigt, woher jede Regel
stammt und ob sie schon auf einem echten Rechner gelaufen ist.

## Was du im Alltag tust

Willst du ein neues Hilfsprogramm bauen lassen, gib dem Bau-Gespräch das passende Rezept und den Ordner mit den Kapseln
und schreib dazu, was das Programm tun soll. Am Ende nennt dir die Intelligenz für jede Kapsel, ob sie schon am echten
Rechner gelaufen ist, nur gebaut und getestet oder noch offen. Selbst prüfen musst du nur die Proben am eigenen Rechner
oder in der Vorschau. Passt eine Regel nicht, sag es der Rolle, die den Ordner pflegt.
