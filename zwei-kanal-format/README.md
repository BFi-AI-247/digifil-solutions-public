# Zwei-Kanal-Format 1.1

*AI-to-AI-and-Human-Messages: ein Text, zwei Leser – Block A für die KI, die handelt, Block B für den Menschen.*

<!-- Diese Anleitung ist selbst im Zwei-Kanal-Format geschrieben (konzept.md, Anwendung 2): BLOCK A muss allein genügen,
     BLOCK B ist Klartext für Menschen. -->

## BLOCK A – Auftrag an die schreibende KI

```text
ZWECK:        Einen Text im Zwei-Kanal-Format schreiben: Block A enthält alles, was der Empfänger zum Handeln braucht,
              Block B erklärt Menschen in Klartext, wozu das Ganze gut ist. Ergebnis: Der Empfänger kann allein mit
              Block A richtig handeln.
GILT FÜR:     (1) Aufträge eines Agenten an einen anderen, die etwas bewirken (Dateien, Abläufe, Begrenzungen).
              (2) Anleitungen (README), nach denen eine KI etwas einrichtet oder benutzt.
GILT NICHT:   Quittungen und kurze Rückfragen – die bleiben kurz und formlos. Aufträge ohne Wirkung, mit einem Empfänger
              in einem Strang (einer Unterhaltung) und ohne Begrenzung dürfen Klartext bleiben (konzept.md, Anwendung 1, „Wann“).
VORAUSSETZUNG: Zum Schreiben: keine, die sechs Dateien dieses Ordners genügen. Für Schritt 5 (Blindtest einer Anleitung):
              eine frische KI oder eine neue Sitzung ohne Verlauf; ist beides nicht möglich, siehe Schritt 5.
DATEIEN:      konzept.md (Grundsatz, Felder beider Anwendungen, Schreibregeln, Prüfungen, Herkunft) ·
              auftrag-vorlage.md (Vorlage für Anwendung 1) · readme-vorlage.md (Vorlage für Anwendung 2) ·
              beispiel-auftrag.md (ein vollständiger, erfundener Auftrag) · beispiel-readme.md (eine vollständige,
              erfundene Anleitung) · README.md (diese Datei).
BEGRIFFE:     Ausführungsrelevant = alles, ohne das der Empfänger anders oder falsch handeln würde: Fristen, Pfade, Werte,
              Schwellen, Freigaben, Beteiligte, Verweise.
              Begrenzung = eine Grenze, die der Empfänger kennt und nicht überschreiten darf (im Feld LEITPLANKEN).
              Blindtest = eine frische KI ohne Vorwissen bekommt nur Block A und einen erfundenen Auftrag und meldet,
              wo sie raten musste (konzept.md, „Prüfungen“).
              Betreiber = der Mensch, dem das Vorhaben gehört; Auftraggeber = wer den konkreten Auftrag gibt;
              Instanz = eine laufende KI mit Kennung (konzept.md, „Drei Begriffe“).
```

### SCHRITTE (in dieser Reihenfolge; jeder Schritt hat ein prüfbares Ergebnis)

1. **Anwendung wählen.** Ist der Text eine Nachricht an einen Agenten, die etwas bewirkt: Anwendung 1, Vorlage
   `auftrag-vorlage.md`. Ist er eine Anleitung, die dauerhaft im Repo liegt: Anwendung 2, Vorlage `readme-vorlage.md`.
   *Ergebnis:* Die Vorlage ist kopiert; ihre Felder stehen in der Reihenfolge aus `konzept.md`.
2. **Block A füllen.** Jedes Pflichtfeld füllen, in ganzen Sätzen mit Verb – bei Aufträgen alle zehn Felder der Vorlage, bei
   Anleitungen die Felder mit „ja“ in der Tabelle in `konzept.md`. Jeder Schritt einer Anleitung nennt
   Datei, Stelle und Wert und endet mit *Ergebnis:*. Was nur im Code steht (Dateiname, Ablageort, das Wort für eine Rolle
   im Code), auch hier nennen. Dieselbe Sache überall mit demselben Wort bezeichnen. Listenfelder dürfen Punkte mit „·“ trennen,
   jeder Punkt eine vollständige Aussage. Nur bei Anleitungen: Wo ein Wert offen sein kann, Vorgabe daneben und „in der
   Lieferung als offen nennen“. Nur bei Aufträgen: LEITPLANKEN und ESKALATION ausdrücklich füllen („keine“ ist ein Wert);
   REQUIRE-ACK mindestens RUN-ID und Stand; hast du selbst eine Angabe nicht: nicht raten – vor dem Abschicken beschaffen oder
   in PARAMETER als `offen: … – vor dem Handeln beim Absender erfragen` schreiben, nie in Block B verstecken (was der
   Empfänger dann tut: konzept.md, „Wenn der Verfasser eine Angabe nicht hat“).
   *Ergebnis:* `grep -n '<' <datei>` zeigt nur noch absichtliche Zeichen (z. B. in Befehlen), keine Platzhalter.
3. **Die zwei Prüffragen.** Jeden Satz in Block B fragen: „Ist das eigentlich eine Anweisung?“ – ja → nach Block A. Dann:
   „Könnte der Empfänger ohne Block B korrekt ausführen?“ – nein → in Block A fehlt etwas.
   *Ergebnis:* Block B enthält nichts aus der Liste „Was nicht in Block B darf“ in `konzept.md` (Anwendung 1); eine Zahl nur,
   wenn der Empfänger sie nicht zum Handeln braucht.
4. **Block B in Klartext.** Einstieg mit einem echten Vorfall oder Beispiel; dann, was es tut; bei Anleitungen zusätzlich der
   Abschnitt „Was du im Alltag tust“. Keine Funktions-, Datei- oder Feldnamen, keine Abkürzungen ohne Erklärung. Bei Aufträgen
   höchstens drei Absätze; Längeres in eine eigene Datei, die Block A mit Zweck nennt.
   *Ergebnis:* Block B enthält keine Zeichen in `Backticks` und keine Kürzel ohne erklärenden Satz.
5. **Blindtest (jede Anleitung, Anwendung 2).** Eine frische KI – ohne die Anleitung und das Projekt zu kennen – bekommt nur
   Block A und einen erfundenen, kleinen Auftrag, der zu GILT FÜR passt. Ihre Liste der geratenen Stellen in Block A (oder im
   Code) beheben. Mit einem anderen erfundenen Auftrag wiederholen, bis nur noch Kleinigkeiten kommen. Gibt es keine frische KI:
   dieselbe KI in einer neuen Sitzung ohne Verlauf, und das in der Lieferung so nennen. Geht auch das nicht: Schritt auslassen
   und die Anleitung in der Lieferung als „ungeprüft (Blindtest offen)“ kennzeichnen.
   *Ergebnis:* Der letzte Blindtest fand keine echte Lücke; Auftrag, Ratestellen und Behebung sind dort abgelegt, wo das
   Projekt seine Prüfungen aufbewahrt, und die Lieferung nennt den Ort.

```text
PRÜFUNG:      Die drei Ergebnisse zusammen: Schritt 3 (beide Prüffragen) · Schritt 4 (Block B ohne Backticks) · bei Anleitungen
              Schritt 5 (kein Blindtest-Befund mit echter Lücke).
FAIL-MODE:    Lässt sich etwas Ausführungsrelevantes nicht in ein Feld bringen: als eigenen Schritt in Block A aufnehmen,
              nie in Block B. Fehlt dir beim Ausführen dieser Anleitung eine Angabe, die nur der Auftraggeber kennt: nicht
              raten, als offen in die Lieferung. (Schreibst du selbst einen Auftrag und dir fehlt eine Angabe: Schritt 2.)
NICHT TUN:    Anweisungen in Block B · Stichwort-Telegramm in Block A · Block B aus Funktionsnamen und Kürzeln ·
              Regeln des Empfängers durch das Format lockern (Vorrang der Regeln, konzept.md).
LIEFERUNG:    der Text · Ergebnis der Prüffragen · bei Anleitungen die Blindtest-Läufe mit Befund ·
              jede Stelle, an der diese Anleitung nicht reichte (mit Zitat).
REFERENZ:     konzept.md (Zitate der Herkunft, Felder, Prüfungen) · beispiel-auftrag.md und beispiel-readme.md (fertige Texte).
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
noch 11, darunter eine echte Lücke, die dann behoben wurde; der vierte Versuch fand nur noch Kleinigkeiten.

## Was du im Alltag tust

Lies nur den zweiten Teil. Verstehst du danach nicht, wozu das Ganze gut ist und was du selbst tun musst, ist der Text nicht
fertig – sag es einfach. Den ersten Teil prüft der Blindtest, nicht du.
