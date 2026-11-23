# Zwei-Kanal-Format 1.3

*AI-to-AI-and-Human-Messages: ein Text, zwei Leser – Block A für die KI, die handelt, Block B für den Menschen.*

## BLOCK A – Auftrag an die schreibende KI

```text
ZWECK:        Du schreibst einen Text im Zwei-Kanal-Format. Block A enthält alles, was der Empfänger zum Handeln braucht.
              Block B erklärt Menschen in Klartext, wozu der Text gut ist. Das Ziel ist erreicht, wenn der Empfänger
              allein mit Block A richtig handeln kann.
GILT FÜR:     Aufträge von einer KI an eine andere, die etwas bewirken · Anleitungen, nach denen eine KI etwas
              einrichtet oder benutzt · Testprotokolle, die mehrere KIs in derselben Form schreiben, damit sich ihre
              Ergebnisse nebeneinander lesen lassen.
GILT NICHT:   Quittungen und kurze Rückfragen bleiben kurzer Klartext. Ob ein Text im Format stehen muss, legt das
              Regelwerk fest, nach dem du arbeitest. Dieses Format legt nur fest, wie der Text dann aussieht.
VORAUSSETZUNG: Zum Schreiben genügen die acht Dateien dieses Ordners. Für Schritt 5 brauchst du eine frische KI oder
              eine neue Sitzung ohne Verlauf.
DATEIEN:      README.md (diese Anleitung) · konzept.md (Grundsatz und Herkunft: warum das Format so ist) ·
              auftrag-vorlage.md (Form eines Auftrags und seiner Quittung) · readme-vorlage.md (Form einer Anleitung) ·
              testprotokoll-vorlage.md (Form eines Testprotokolls) · beispiel-auftrag.md (ein fertiger, erfundener
              Auftrag) · beispiel-readme.md (eine fertige, erfundene Anleitung) · beispiel-testprotokoll.md (ein
              fertiges, erfundenes Testprotokoll).
BEGRIFFE:     Empfänger = die KI, die nach dem Text handelt.
              Ausführungsrelevant = alles, ohne das der Empfänger anders oder falsch handeln würde: Fristen, Pfade,
              Werte, Schwellen, Freigaben, Beteiligte, Verweise.
              Grenze = etwas, das der Empfänger lässt. Aufträge nennen Grenzen im Feld LEITPLANKEN, Anleitungen im
              Feld NICHT TUN.
              Frische KI = eine KI, die weder den Text noch das Projekt kennt.
              Ratestelle = eine Stelle, an der die frische KI raten musste.
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Vorlage wählen.** Wenn der Text eine Nachricht an eine andere KI ist, die etwas bewirkt, dann kopiere
   `auftrag-vorlage.md`. Wenn der Text eine Anleitung ist, die dauerhaft im Repo liegt, dann kopiere `readme-vorlage.md`.
   Wenn der Text über einen Test berichtet, dann kopiere `testprotokoll-vorlage.md`.
   Namen und Reihenfolge der Felder lässt du, wie sie sind.
   *Ergebnis:* Die Kopie enthält die Felder der Vorlage in derselben Reihenfolge.
2. **Block A füllen.** Ersetze jeden Platzhalter; der Platzhalter sagt, was in das Feld gehört. Schreib so:
   - Schreib ganze Sätze mit Verb.
   - Nenne die Bedingung vor der Handlung: „Wenn X, dann tu Y.“
   - Nenne bei jeder Grenze zuerst, was richtig ist, und dann, was der Empfänger lässt: „Schreib nur auf Branch X.
     Main fasst du nicht an.“
   - Nenne in jedem Schritt einer Anleitung die Datei, die Stelle und den Wert.
   - Nenne auch, was sonst nur im Code steht: Dateinamen, Ablageorte und das Wort, mit dem der Code eine Rolle
     bezeichnet.
   - Bezeichne dieselbe Sache überall mit demselben Wort.
   - Trenne die Punkte eines Listenfelds mit „·“ oder je Zeile. Jeder Punkt ist eine vollständige Aussage.

   *Ergebnis:* `grep -n '<' <datei>` zeigt nur noch absichtliche Zeichen und keinen Platzhalter.
3. **Die zwei Prüffragen.** Frag jeden Satz in Block B: „Ist das eigentlich eine Anweisung?“ Wenn ja, dann verschiebe
   ihn nach Block A. Frag danach: „Könnte der Empfänger ohne Block B richtig handeln?“ Wenn nein, dann ergänze in
   Block A, was fehlt.
   *Ergebnis:* Alles Ausführungsrelevante steht in Block A.
4. **Block B schreiben.** Schreib für einen Menschen ohne Fachwissen: ganze Sätze, keine Funktions-, Datei- oder
   Feldnamen, jede Abkürzung erklärt. Folge dem Aufbau, den die Vorlage für Block B zeigt.
   *Ergebnis:* Block B enthält keine Zeichen in Backticks und kein Kürzel ohne erklärenden Satz.
5. **Blindtest (nur bei Anleitungen).** Gib einer frischen KI nur Block A und eine kleine, erfundene Probeaufgabe, die
   zu GILT FÜR passt. Lass sie die Schritte ausführen und jede Ratestelle nennen. Behebe jede Ratestelle in Block A
   oder im Code. Wiederhole den Test mit einer anderen Probeaufgabe, bis er nur noch Kleinigkeiten findet. Wenn du
   keine frische KI hast, dann nimm dieselbe KI in einer neuen Sitzung ohne Verlauf und nenne das in der Lieferung.
   Wenn auch das nicht geht, dann kennzeichne die Anleitung in der Lieferung als „ungeprüft (Blindtest offen)“.
   *Ergebnis:* Der letzte Blindtest fand keine echte Lücke. Probeaufgabe, Ratestellen und Behebung liegen dort, wo das
   Projekt seine Prüfungen aufbewahrt, und die Lieferung nennt den Ort.

```text
PRÜFUNG:      Die Ergebnisse der Schritte 2, 3 und 4 gelten zusammen. Bei einer Anleitung gilt zusätzlich das Ergebnis
              von Schritt 5.
FAIL-MODE:    Wenn etwas Ausführungsrelevantes in kein Feld passt, dann nimm es als eigenen Punkt in PARAMETER oder als
              eigenen Schritt in Block A auf. Wenn dir eine Angabe fehlt, die du nicht beschaffen kannst, dann schreib
              sie in Block A als „offen: …“ mit dem, was der Empfänger damit tut, und nenne sie in der Lieferung.
LIEFERUNG:    der Text · das Ergebnis der zwei Prüffragen · bei Anleitungen jeder Blindtest mit Befund · offene
              Angaben · jede Stelle, an der diese Anleitung nicht reichte, mit Zitat.
```

---

## BLOCK B – für Menschen

Wenn eine KI einen Text bekommt, nach dem sie handeln soll, liest sie alles darin als möglichen Auftrag – auch eine
nebenbei erwähnte Frist in einem erklärenden Absatz. Umgekehrt fehlt ihr oft genau das, was der Schreiber für
selbstverständlich hielt. In der Agentur, aus der dieses Format stammt, sollte es genau das verhindern: doppelt erledigte
Aufträge und Texte, die von Mal zu Mal etwas anders aussehen.

Das Zwei-Kanal-Format trennt deshalb jeden solchen Text in zwei Teile. Der erste Teil ist für den, der handelt: feste
Felder, vollständig, nichts zwischen den Zeilen. Der zweite Teil ist für Menschen: warum es das gibt, was es löst –
in normaler Sprache. Die Probe ist einfach: Streicht man den zweiten Teil, muss der Empfänger trotzdem richtig handeln
können.

Das Format ist ein Werkzeug. Es sagt, wie ein solcher Text gebaut ist. Was eine KI darf und was sie lassen muss, steht
in den Regeln, nach denen sie arbeitet, nicht hier.

Ursprünglich galt das nur für Aufträge zwischen KI-Agenten. Seit Oktober 2026 gilt es auch für Anleitungen, denn auch die
lesen heute meist KIs. Seit November 2026 gilt es außerdem für Testprotokolle, damit mehrere KIs ihre Berichte in
derselben Form schreiben. Ob eine Anleitung taugt, zeigt ein Blindtest: Eine KI, die nichts davon kennt, richtet damit etwas
ein und schreibt auf, wo sie raten musste. Bei der ersten Anleitung waren es beim ersten Versuch 22 Stellen, beim dritten
noch 11, darunter eine echte Lücke, die dann behoben wurde; der vierte Versuch fand nur noch Kleinigkeiten.

## Was du im Alltag tust

Lies nur den zweiten Teil. Verstehst du danach nicht, wozu das Ganze gut ist und was du selbst tun musst, ist der Text nicht
fertig – sag es einfach. Den ersten Teil prüft der Blindtest, nicht du.
