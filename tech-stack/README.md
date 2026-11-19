# Ordner tech-stack – Einstieg

## BLOCK A – für die lesende KI

```text
ZWECK:        Dieser Text führt in den Ordner tech-stack/ ein: was in ihm liegt, wer die Dateien wie benutzt und wie
              die Bauvorgabe gepflegt wird. Das Ziel ist erreicht, wenn ein Leser allein mit diesem Text weiß, welche
              Datei er wem gibt und wohin Befunde gehen.
GILT FÜR:     Menschen und KI-Instanzen, die ein neues lokales Werkzeug bauen lassen, ein bestehendes prüfen lassen
              oder die Bauvorgabe pflegen.
GILT NICHT:   Die Bauvorgabe selbst mit ihren Bausteinen und Grenzen (steht in TECH-STACK.md; dieser Text wiederholt
              sie nicht) · die Belege je Vorgabe (stehen in BELEGE.md; nicht öffentlich) · das Verfahren der
              Prüflesungen (steht in blindtest/README.md).
VORAUSSETZUNG: Lesezugriff auf diesen Ordner (BELEGE.md nur für die pflegende Rolle; in einer öffentlichen Fassung
              fehlt sie). Wer ein Werkzeug bauen lassen will, braucht eine bauende KI und einen Auftrag für sie.
DATEIEN:      README.md (dieser Einstieg) · TECH-STACK.md (Bauvorgabe für lokale Werkzeuge in zwei Blöcken; die
              Fassung steht in der Überschrift) · TECH-STACK-2.md (Bauvorgabe für Web-Werkzeuge, ebenso) · BELEGE.md
              und BELEGE-2.md (Beleg je Vorgabe; nicht öffentlich) · blindtest/
              (Verfahren und Berichte der Prüflesungen der Bauvorgabe).
BEGRIFFE:     pflegende Rolle = die Rolle, die TECH-STACK.md führt; welche das ist, steht in der Rollendatei des
              Projekts. Gibt es keine, dann ist es der Mensch, der diesen Ordner verantwortet.
```

### SCHRITTE (Schritt 1 oder 2, je nach Fall; Schritt 3, wenn etwas auffällt; jeder Schritt hat ein prüfbares Ergebnis)

1. **Neues Werkzeug bauen lassen.** Gib einer bauenden KI die passende Bauvorgabe – TECH-STACK.md für ein Werkzeug auf
   dem eigenen Rechner, TECH-STACK-2.md für ein Web-Werkzeug – und den Auftrag für das Werkzeug, sonst nichts aus
   diesem Ordner. Die KI arbeitet danach das Startpaket dieser Bauvorgabe ab.
   *Ergebnis:* Der Bau nennt das Startpaket der Bauvorgabe als Grundlage und beginnt mit dessen erstem Schritt.
2. **Bestehendes Werkzeug prüfen lassen.** Gib einer prüfenden KI die Datei TECH-STACK.md und das Werkzeug, das zu
   prüfen ist. Die KI gleicht das Werkzeug mit den Bausteinen der Datei ab.
   *Ergebnis:* Die Prüfung nennt je Baustein, ob das Werkzeug der Vorgabe folgt.
3. **Befunde melden.** Ein Fehler im Werkzeug geht an die KI, die das Werkzeug baut, oder als Issue an dessen Repo.
   Nur eine Regel der Bauvorgabe, die nicht reicht oder am Zielrechner nicht passt, geht an die pflegende Rolle: Ein
   Mensch sagt es ihr im Chat, eine KI schreibt eine Nachricht in ihr Postfach. Nenn die Nummer der Vorgabe (z. B.
   2.4) und was geschah. Bis zur Antwort baut die KI nach der geltenden Fassung und trägt die Abweichung in die
   ANNAHMEN.md des Werkzeugs ein (FAIL-MODE in TECH-STACK.md).
   *Ergebnis:* Der Befund liegt bei der pflegenden Rolle. Sie antwortet mit einer neuen Fassung, die die Änderung
   nennt, oder mit einer Ablehnung samt Grund.

```text
PRÜFUNG:      Ein Leser beantwortet nach diesem Text: was liegt in diesem Ordner, wem gebe ich welche Datei, wohin
              gehen Befunde. Die Antworten stehen hier oder in den benannten Dateien.
FAIL-MODE:    Wenn dieser Text eine Frage nicht beantwortet, dann steht sie in TECH-STACK.md; fehlt sie auch dort,
              dann gilt der Weg, den die Bauvorgabe für Lücken vorsieht.
NICHT TUN:    Die bauende KI bekommt TECH-STACK.md; diese README ersetzt die Bauvorgabe nicht. · Gib BELEGE.md nicht
              weiter; sie ist nicht öffentlich. · Gib nie Zugangsschlüssel oder Firmendaten mit; was dafür gilt, steht
              in TECH-STACK.md. · Ändere TECH-STACK.md nicht selbst; Befunde gehen an die pflegende Rolle.
LIEFERUNG:    Dieser Text legt nichts an und ändert nichts. Wer ihm folgt, nennt in seiner eigenen Lieferung die
              weitergegebenen Dateien und jede Stelle, an der dieser Text nicht reichte, mit Zitat.
REFERENZ:     TECH-STACK.md in diesem Ordner (Vorgaben, Bausteine, Pflege) · blindtest/README.md (Prüflesungen).
```

---

## BLOCK B – für Menschen

Mehrere kleine Hilfsprogramme für den eigenen Rechner sind hier nacheinander entstanden, jedes in einem eigenen
Gespräch mit einer künstlichen Intelligenz. Immer wieder wurden dieselben Grundfragen neu beantwortet: Wie kommt ein
Programm ohne Installation auf den Rechner? Wie startet es? Wo liegt der Zugangsschlüssel? Manche Fehler passierten
mehrfach, weil jede Runde von vorn anfing.

Dieser Ordner sammelt die bewährten Antworten an einem Ort. Eine Bauvorgabe legt fest, was jedes Hilfsprogramm
mitbringen muss. Eine nicht öffentliche Belegliste zeigt, woher jede Vorgabe stammt und ob sie schon auf einem echten
Rechner gelaufen ist. Ein Unterordner sammelt die Berichte der Prüfungen, in denen jeweils eine neue Intelligenz die
Vorgabe mit einer erfundenen Aufgabe auf Lücken prüfte.

## Was du im Alltag tust

Willst du ein neues Hilfsprogramm bauen lassen, gib dem Bau-Gespräch die Bauvorgabe aus diesem Ordner und schreib dazu,
was das Programm tun soll. Am Ende nennt dir die Intelligenz für jeden Baustein, ob er schon am echten Rechner gelaufen
ist, nur gebaut und getestet oder noch offen. Selbst prüfen musst du nur die Proben am eigenen Rechner: starten,
stoppen, aktualisieren. Geht im Programm etwas schief, sag es dem Bau-Gespräch. Passt eine Regel der Bauvorgabe nicht,
sag es der Rolle, die sie pflegt; sie entscheidet, ob die Bauvorgabe eine neue Fassung bekommt.
