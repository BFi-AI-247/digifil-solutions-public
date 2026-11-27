# Two-Channel Format 1.4

*AI-to-AI-and-Human-Messages: one text, two readers – BLOCK A for the AI that acts, BLOCK B for the human.*

**Status of this folder (2026-11-26).** This is version 1.4 of the format; it replaces version 1.3, which was German. The files have English names since this version.

## BLOCK A – order to the AI that writes

```text
PURPOSE:      You write a text in the Two-Channel Format. BLOCK A holds everything the receiver needs to act. BLOCK B
              explains to humans in plain language what the text is for. The aim is reached when the receiver can act
              correctly with BLOCK A alone.
APPLIES TO:   Orders from one AI to another that make something happen · guides by which an AI sets up or uses something ·
              test reports that several AIs write in the same form so that their results can be read side by side.
DOES NOT APPLY TO: Receipts and short questions stay short plain text. Whether a text must be in the format is laid down by
              the rules you work under. This format only lays down what the text then looks like.
PREREQUISITES: The eight files of this folder are enough for writing. For step 5 you need a fresh AI or a new session without history.
FILES:        README.md (this guide) · concept.md (principle and origin: why the format is as it is) ·
              template-order.md (form of an order and its receipt) · template-guide.md (form of a guide) ·
              template-test-report.md (form of a test report) · example-order.md (a finished, invented order) ·
              example-guide.md (a finished, invented guide) · example-test-report.md (a finished, invented test report).
TERMS:        Receiver = the AI that acts after the text.
              Relevant for execution = everything without which the receiver would act differently or wrongly: deadlines,
              paths, values, thresholds, approvals, parties, references.
              Limit = something the receiver leaves. Orders name limits in the field GUARDRAILS, guides in the field DO NOT.
              Fresh AI = an AI that knows neither the text nor the project.
              Guess place = a place where the fresh AI had to guess.
              Language = BLOCK A is English, BLOCK B is German (operator 25.11.2026 21:40); the operator's words and quotes
              stay in the language they were said in.
```

### STEPS (in this order; every step has a checkable result)

1. **Choose the template.** If the text is a message to another AI that makes something happen, then copy
   `template-order.md`. If the text is a guide that stays in a repo for good, then copy `template-guide.md`. If the text
   reports on a test, then copy `template-test-report.md`. Leave the names and the order of the fields as they are.
   *Result:* The copy holds the fields of the template in the same order.
2. **Fill BLOCK A.** Replace every placeholder; the placeholder says what belongs into the field. Write like this:
   - Write whole sentences with a verb.
   - Name the condition before the action: "If X, then do Y."
   - For every limit name first what is right, then what the receiver leaves: "Write only on branch X. You do not touch main."
   - In every step of a guide name the file, the place and the value.
   - Name also what otherwise stands only in the code: file names, storage places and the word with which the code names a role.
   - Name the same thing with the same word everywhere.
   - Separate the items of a list field with "·" or one per line. Every item is a complete statement.

   *Result:* `grep -n '<' <file>` shows only intended characters and no placeholder.
3. **The two test questions.** Ask of every sentence in BLOCK B: "Is this actually an instruction?" If yes, then move it
   to BLOCK A. Then ask: "Could the receiver act correctly without BLOCK B?" If no, then add to BLOCK A what is missing.
   *Result:* Everything relevant for execution stands in BLOCK A.
4. **Write BLOCK B.** Write in German for a person without special knowledge: whole sentences, no function, file or
   field names, every abbreviation explained. Follow the build that the template shows for BLOCK B.
   *Result:* BLOCK B holds no characters in backticks and no abbreviation without an explaining sentence.
5. **Blind test (guides only).** Give a fresh AI only BLOCK A and a small, invented sample task that fits APPLIES TO. Let
   it carry out the steps and name every guess place. Fix every guess place in BLOCK A or in the code. Repeat the test
   with another sample task until it finds only trifles. If you have no fresh AI, then take the same AI in a new session
   without history and say so in the delivery. If that is not possible either, then mark the guide in the delivery as
   "ungeprüft (Blindtest offen)".
   *Result:* The last blind test found no real gap. Sample task, guess places and fix lie where the project keeps its
   tests, and the delivery names the place.

```text
CHECK:        The results of steps 2, 3 and 4 apply together. For a guide the result of step 5 applies in addition.
FAIL-MODE:    If something relevant for execution fits no field, then take it up as an item of its own in PARAMETERS or as a
              step of its own in BLOCK A. If you lack a detail that you cannot get, then write it in BLOCK A as "open: …"
              with what the receiver does with it, and name it in the delivery.
DELIVERY:     the text · the result of the two test questions · for guides every blind test with its finding · open
              details · every place where this guide was not enough, with quote.
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
derselben Form schreiben; seit Fassung 1.4 ist das Testprotokoll eine feste Vorlage wie die beiden anderen. Ob eine
Anleitung taugt, zeigt ein Blindtest: Eine KI, die nichts davon kennt, richtet damit etwas ein und schreibt auf, wo sie
raten musste. Bei der ersten Anleitung waren es beim ersten Versuch 22 Stellen, beim dritten noch 11, darunter eine echte
Lücke, die dann behoben wurde; der vierte Versuch fand nur noch Kleinigkeiten.

Seit Fassung 1.4 ist Block A englisch; Block B bleibt deutsch.

## Was du im Alltag tust

Lies nur den zweiten Teil. Verstehst du danach nicht, wozu das Ganze gut ist und was du selbst tun musst, ist der Text nicht
fertig – sag es einfach. Den ersten Teil prüft der Blindtest, nicht du.
Stand: 2026-11-26
