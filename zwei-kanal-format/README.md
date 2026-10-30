# Zwei-Kanal-Format 1.0

*AI-to-AI-and-Human-Messages: ein Text, zwei Leser – Block A für die KI, die handelt, Block B für den Menschen.*

> Verweise auf `../kanon_01_single_agent/`, `../kanon_02_multi_agent/`, `../arbeit/` und `../quelle/` führen in den nicht öffentlichen Teil des Kanons.

<!-- Zwei-Kanal-Format (konzept.md, Anwendung 2): BLOCK A muss allein genügen, BLOCK B ist Klartext für Menschen. -->

## BLOCK A – Auftrag an die schreibende KI

```text
ZWECK:        Einen Text im Zwei-Kanal-Format schreiben: Block A enthält alles, was der Empfänger zum Handeln braucht,
              Block B erklärt Menschen in Klartext, wozu das Ganze gut ist. Ergebnis: Der Empfänger kann allein mit
              Block A richtig handeln.
GILT FÜR:     (1) Aufträge eines Agenten an einen anderen, die etwas bewirken (Dateien, Abläufe, Leitplanken).
              (2) Anleitungen (README), nach denen eine KI etwas einrichtet oder benutzt.
GILT NICHT:   Quittungen und kurze Rückfragen – die bleiben kurz und formlos. Aufträge ohne Wirkung, mit einem Empfänger
              und ohne Leitplanke dürfen Klartext bleiben (konzept.md, Anwendung 1, „Wann“).
VORAUSSETZUNG: keine.
DATEIEN:      konzept.md (Grundsatz, Felder beider Anwendungen, Schreibregeln, Blindtest, mit Quellen) ·
              readme-vorlage.md (Vorlage für Anwendung 2) · für Anwendung 1: ../kanon_02_multi_agent/vorlagen.md §1 (Vorlage) und
              ../kanon_02_multi_agent/kanon_team.py auftrag_pruefen (Prüfung im Code)
BEGRIFFE:     Ausführungsrelevant = alles, ohne das der Empfänger anders oder falsch handeln würde: Fristen, Pfade, Werte,
              Schwellen, Freigaben, Beteiligte, Verweise.
              Blindtest = eine frische KI ohne Vorwissen bekommt nur Block A und einen erfundenen Auftrag und meldet,
              wo sie raten musste.
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Anwendung wählen.** Ist der Text eine Nachricht an einen Agenten, die etwas bewirkt: Anwendung 1, Vorlage
   `../kanon_02_multi_agent/vorlagen.md` §1. Ist er eine Anleitung, die dauerhaft im Repo liegt: Anwendung 2, Vorlage `readme-vorlage.md`.
   *Ergebnis:* Die Vorlage ist kopiert; ihre Felder stehen in der Reihenfolge aus `konzept.md`.
2. **Block A füllen.** Jedes Pflichtfeld aus `konzept.md` füllen, in ganzen Sätzen mit Verb. Jeder Schritt einer Anleitung nennt
   Datei, Stelle und Wert und endet mit *Ergebnis:*. Was nur im Code steht (Dateiname, Ablageort, Rollenwort), auch hier nennen.
   Dieselbe Sache überall mit demselben Wort bezeichnen. Wo ein Wert offen sein kann: Vorgabe daneben und „in der Lieferung als
   offen nennen“.
   *Ergebnis:* `grep -n '<' <datei>` zeigt nur noch absichtliche Zeichen (z. B. in Befehlen), keine Platzhalter.
3. **Die zwei Prüffragen.** Jeden Satz in Block B fragen: „Ist das eigentlich eine Anweisung?“ – ja → nach Block A. Dann:
   „Könnte der Empfänger ohne Block B korrekt ausführen?“ – nein → in Block A fehlt etwas.
   *Ergebnis:* Block B enthält keine Frist, keinen Pfad, keinen Wert, keine Freigabe.
4. **Block B in Klartext.** Einstieg mit einem echten Vorfall oder Beispiel; dann, was es tut; dann „Was du im Alltag tust“.
   Keine Funktions-, Datei- oder Feldnamen, keine Abkürzungen ohne Erklärung. Regellisten nach Themen, je mit „warum“ und ob
   das Programm es prüft oder es nur eine Bitte an das Modell ist.
   *Ergebnis:* Block B enthält keine Zeichen in `Backticks` und keine Regelkürzel ohne erklärenden Satz.
5. **Blindtest (nur Anwendung 2, und nur wenn die Anleitung etwas einrichtet).** Eine frische KI bekommt nur Block A und einen
   erfundenen, kleinen Auftrag, der zum GILT FÜR passt. Ihre Liste der geratenen Stellen in Block A (oder im Code) beheben.
   Mit einem anderen erfundenen Auftrag wiederholen, bis nur noch Kleinigkeiten kommen.
   *Ergebnis:* Der letzte Blindtest fand keine echte Lücke; die Läufe stehen mit Befund in der Arbeitsablage des Projekts.

```text
PRÜFUNG:      Schritt 3 bestanden (beide Prüffragen) · Schritt 4 bestanden (Block B ohne Backticks) · bei Anleitungen
              Schritt 5 ohne echte Lücke.
FAIL-MODE:    Lässt sich etwas Ausführungsrelevantes nicht in ein Feld bringen: als eigenen Schritt in Block A aufnehmen,
              nie in Block B. Fehlt eine Angabe, die nur der Betreiber kennt: nicht raten, als offen in die Lieferung.
NICHT TUN:    Anweisungen in Block B · Stichwort-Telegramm in Block A · Block B aus Funktionsnamen und Kürzeln ·
              Regeln anderer Kanon-Teile durch das Format lockern (Kanon-Vorrang).
LIEFERUNG:    der Text · Ergebnis der Prüffragen · bei Anleitungen die Blindtest-Läufe mit Befund ·
              jede Stelle, an der diese Anleitung nicht reichte (mit Zitat).
REFERENZ:     konzept.md (Quellen wörtlich) · Beispiel einer fertigen Anleitung: ../kanon_01_single_agent/README.md
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

Ursprünglich galt das nur für Aufträge zwischen KI-Agenten. Seit Oktober 2026 gilt es auch für Anleitungen, denn auch die
lesen heute meist KIs. Ob eine Anleitung taugt, zeigt ein Blindtest: Eine KI, die nichts davon kennt, richtet damit etwas
ein und schreibt auf, wo sie raten musste. Bei der ersten Anleitung waren es beim ersten Versuch 22 Stellen, beim dritten
nur noch Kleinigkeiten und eine echte Lücke, die dann behoben wurde.

## Was du im Alltag tust

Lies nur den zweiten Teil. Verstehst du danach nicht, wozu das Ganze gut ist und was du selbst tun musst, ist der Text nicht
fertig – sag es einfach. Den ersten Teil prüft der Blindtest, nicht du.
