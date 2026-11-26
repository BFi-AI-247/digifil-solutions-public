# Two-Channel Format – concept

Version 1.4 of 2026-11-26. English; quotes and words of the operator stay German, as they were said. This file is the translation of version 1.3 (German) with the changes of 1.4 (see "Versions").

The Two-Channel Format is a tool. It lays down how a text is built that an AI is to act on. What an AI may and must do is
laid down by the rules it works under; the format replaces and loosens none of them.

How to write a text in the format stands in `README.md`. What the fields look like stands in `template-order.md`,
`template-guide.md` and `template-test-report.md`. Here stands why the format is as it is.

## Principle

The quotes come from the order form of an AI agency (version 1.0, September/October 2026) in which the format arose.
They are taken over word for word.

**Separation rule.**
> „**Block B darf niemals Informationen enthalten, die für die Ausführung notwendig sind — alles Ausführungsrelevante gehört zwingend in Block A.**“

This is how a text in the format is read: BLOCK A applies, BLOCK B explains. BLOCK B holds no instruction to the receiver;
what the human does himself may stand there. If BLOCK B says something other than BLOCK A, then BLOCK A applies, and the
sentence in BLOCK B is a fault of the text.

**What does not belong in BLOCK B.**
> „Block B darf enthalten: Hintergrund, Motivation, Einordnung, Betreiber-Zitate. Block B darf NICHT: Fristen, Datei-Pfade, Schwellen, Freigaben, Namen/Beteiligte, Verweise auf frühere Punkte.“

The yardstick is the separation rule. A detail that the receiver needs to act stands in BLOCK A; BLOCK B may repeat it for
explanation. A number that only tells a story („beim ersten Versuch 22 Stellen“) may stand in BLOCK B alone.

**Two test questions.**
> 1. „Ist dieser Kontext-Satz eigentlich eine Anweisung? → nach A verschieben.“
> 2. „Könnte der Empfänger den Auftrag korrekt ausführen, wenn Block B weg wäre?“ — Nein → Inhalt fehlt in A.

The questions are the separation rule as a test. They are asked in `README.md`, step 3.

**Why at all.**
> „Mehrdeutigkeit entsteht bei Wirkung, nicht bei Wortzahl; das Format schichtet nur, wo Fehlinterpretation Schaden anrichten könnte (Doppelausführung, Format-Drift).“

**BLOCK B is plain language.** Test: *Does a reader know after BLOCK B what the whole is for and what he has to do himself –
without having read BLOCK A?* Origin: The operator, for whom the first guide in this format was written, found its BLOCK B
„Kauderwelsch“ – a table of rule abbreviations and function names.

**BLOCK B not too terse** (operator 25.11.2026 16:35): „Im Zwei-Kanal-Format, bitte Block B nicht zu knapp. Der ist häufig echt überschaubar. ;)“ –
"at most three paragraphs" is a limit, not a target.

## Three terms

**Operator** is the human who owns the undertaking (the same word in the quotes). **Client** is who gives the concrete
order – the operator himself or an AI on his behalf. **Instance** is a running AI with an ID made of role and number (for
example "Build_1").

## Language (new in 1.4)

BLOCK A, the field names, the words of judgment, the notes in the templates, the examples' BLOCK A and these concept
files are English: a machine loads them. BLOCK B is German: the human reads it. Decided by the operator on 25.11.2026: BLOCK A English, BLOCK B German.

Field names of an order, old (German, version 1.3) → new: VON → FROM · AN → TO · DATUM → DATE · RUN-ID → RUN-ID ·
AUFTRAG → ORDER · PARAMETER → PARAMETERS · LEITPLANKEN → GUARDRAILS · FAIL-MODE → FAIL-MODE · REQUIRE-ACK → REQUIRE-ACK ·
ESKALATION → ESCALATION. Receipt: Quittung → Receipt · Empfangen → Received · Stand → State · Abweichungen → Deviations ·
Fragen → Questions · Beleg → Evidence. Guide: ZWECK → PURPOSE · GILT FÜR → APPLIES TO · GILT NICHT → DOES NOT APPLY TO ·
VORAUSSETZUNG → PREREQUISITES · DATEIEN → FILES · BEGRIFFE → TERMS · VERHALTEN → BEHAVIOUR · SCHRITTE → STEPS · PRÜFUNG →
CHECK · NICHT TUN → DO NOT · LIEFERUNG → DELIVERY · REFERENZ → REFERENCE. Test report: see the table in
`template-test-report.md`; its words ok / abweichend / nicht geprüft / belegt / ⟦Deutung⟧ / bestanden / bestanden mit
Auflagen / nicht bestanden are now ok / deviates / not checked / evidenced / ⟦interpretation⟧ / passed / passed with
conditions / failed. The value of DATE is written "(measured | context statement, not measured)".
The title of a test report and the four lines of its BLOCK B stay German (they are for the operator).

## Application 1: orders

Form: `template-order.md`. Example: `example-order.md`. Why the template is as it is:

- **DATE and RUN-ID always stand in BLOCK A,** even if the transport already carries both. Origin: blind test 16.11.2026 –
  BLOCK A was passed on without the head of the message, date and RUN-ID were missing.
- **ESCALATION is for blockers, questions come with the receipt.** Origin: blind test 16.11.2026 – questions in
  REQUIRE-ACK and an escalation to the operator in the same order; the readers did not know where to turn.
- **PARAMETERS names where the format is,** if the receiver has to write in the format itself. Origin: blind test
  16.11.2026 – two of four readers did not know what belongs in BLOCK B.
- **The receipt begins with the RUN-ID.** Quote:
  > „Der Empfänger zitiert die Auftrags-Nummer am Anfang seiner Quittierung — nur mit Rückbezug kann abgleichen, ob der Auftrag schon bearbeitet wurde (auch über einen Instanz-Wechsel hinweg).“
- **BLOCK B has at most three paragraphs;** anything longer stands in a file of its own. Quote:
  > „Nachrichten-Kerne bleiben kurz; Substanz (Konzepte, Begründungen, Rohfassungen) wird als eigene Datei in der Wissens-Ablage hinterlegt und mit Lese-Auslöser referenziert (Zweck + entscheidungsrelevante Abschnitte).“

## Application 2: guides

Form: `template-guide.md`. Example: `example-guide.md`. `README.md` is written like this too.

This application is an extension of 28.10.2026; the agency version knew the format only for orders. Origin: The operator
read the first guide of a tool and found it empty („Tw. drei Wort Anweisungen, die für mich viel Interpretationspielraum
lassen“), and added: „welcher Mensch liest denn noch Readme. Das liest doch auch alles KI. Für mich ein Fall für das
Zwei-Kanal-Verfahren.“

A guide lies there for good and is read by many. Therefore the version in the title takes the place of FROM, TO, DATE and
RUN-ID. ORDER becomes PURPOSE, PARAMETERS become PREREQUISITES and FILES, GUARDRAILS become DO NOT, REQUIRE-ACK becomes
DELIVERY; FAIL-MODE holds the escalation. BLOCK B is as long as a human needs to understand and stays shorter than BLOCK A.

BEHAVIOUR exists so that an AI answering feedback on a tool can say "this is how it is today" from the guide, without
reading the code.

## Application 3: test reports

Form: `template-test-report.md` (version 1.1 of 2026-11-26; 1.0 of 2026-11-23 was German). Example:
`example-test-report.md`.

This application is an extension of 23.11.2026. Origin: The operator had several tools tested on the company computer
and several AIs write one report each. He demanded that the reports can be read together and named the Two-Channel
Format as a help. The first three reports arose by a common frame; the template builds on it and turns the frame into
fixed fields.

**Decided (operator 25.11.2026 21:41):** „testprotokoll soll eine vorlage
werden“ – the answer to the question that stood here in 1.3 („Ob die Ergänzung eine neue Fassung des Formats wird,
entscheidet der Betreiber.“). The test report is a fixed template of the format, next to the template of orders and the
template of guides; the format is 1.4.

A test report is a report, not an order: The reader is not to carry anything out but to trust the result and go on
working with it. BLOCK A therefore carries everything needed for that: state, source, steps with judgment, deviations
with cause, verdict and what stayed open. BLOCK B is for the operator and has at most eight lines. The separation rule
applies unchanged.

Why the template is as it is:

- **The head stands as fields in BLOCK A** (`TEMPLATE`, `FROM`, `DATE`, `STATE`, `GUIDE`, `CONDUCTED`, `SOURCE`, `READ`). In the
  frame it stood as a list before BLOCK A. If only BLOCK A is passed on, state and source are missing then – the same
  origin as DATE and RUN-ID in application 1.
- **`CONDUCTED` and `DATE` are two fields:** The time of the test is not the time of writing.
- **`SOURCE` says whether the author collected the data himself.** Origin: A report relied on results that the operator
  had only ticked off; the author had collected nothing himself and did not want to invent a wording. The template names
  for this the formula "ticked off, no note" and the sentence "I collected nothing myself."
- **Three words of judgment per step (ok, deviates, not checked) and three verdicts (passed, passed with conditions,
  failed), each with a fixed meaning.** Without a fixed meaning every author would read the words differently, and the
  reports could not be read side by side.
- **Causes are evidenced or an ⟦interpretation⟧.** The first reports already separated the two; the template makes it a
  duty, because a guessed reason in the dress of a fact is worse than a gap.
- **`RECALCULATED` has a field of its own.** The first reports recalculated sums and shares; in the field of its own every
  reader finds which numbers are checked.
- **`RULES` names three requirements:** no company data (counts yes), no image tests and remedies only as a proposal. The
  first two are requirements of the operator of 23.11.2026 (image tests cost tokens, and tokens are scarce); the third
  comes from the frame.
- **BLOCK B has four fixed lines** (Ergebnis, Abweichungen, Nicht getestet, Zu entscheiden) and does not address the
  operator, so that all reports sound the same.
- **One test, one report.** A repeated test gets a new report; the old one stays unchanged and proves the earlier state.

## Origins of the way of writing

The way of writing stands in `README.md`, step 2, and in the templates. Here stands for each point where it comes from.

- **Whole sentences with a verb:** the „drei Wort Anweisungen“ from the origin of application 2.
- **Condition before action:** blind test 16.11.2026 – „scheitert tkinter: Rückfallweg …“ left open who decides;
  "if tkinter fails, then take …" did not. (After ASD-STE100, Simplified Technical English.)
- **First what is right, then the limit:** wish of the operator of 16.11.2026; „einfach nur Verbote“ had been felt as bad.
- **What stands only in the code:** A blind test found the storage place of a blocklist only in the code.
- **The same word for the same thing:** A blind test found two words for the same term – one on the command line, one in
  the code – and did not know whether both mean the same.
- **No default for addressees, publication, deletion and credentials:** external opinion of 30.10.2026.
- **Blind test:** Whoever writes a text does not see his own gaps. A new session of the same AI is the weaker substitute,
  because its model may overlook the same gaps.

## Origin

The format arose in September and October 2026 in the rules of an AI agency that built and ran a website with several AI
instances; the quotes come from its order form (version 1.0). Application 2, the plain language in BLOCK B, the threshold
for BLOCK B and the blind test are decisions of the operator, who publishes this folder, of 28 to 30 October 2026.

The fields of an order in the agency version. Quote:
```text
VON: <Absender-Instanz>
AN: <Empfänger-Instanz>
DATUM: <TT.MM.JJJJ, HH:MM> (Zeitzone, Systemzeit gemessen — PFLICHTFELD;
  bei Abweichung > 2 Min zur Betreiber-Wahrnehmung: Vermerk „Stempel unsicher"
  statt stiller Abweichung)
RUN-ID: <fortlaufende Auftrags-Nummer>
AUFTRAG: <Handlung in einem Satz>
PARAMETER: <Dateien, Pfade, Werte, Fristen — alles Ausführungsrelevante>
LEITPLANKEN: <Begrenzungs-IDs aus dem Katalog oder „keine">
FAIL-MODE: <Verhalten bei Teilmisserfolg>
REQUIRE-ACK: <was der Empfänger zurückmeldet — IMMER zu füllen,
  mindestens RUN-ID + Ausführungsstand>
ESKALATION: <wann/an wen bei Blockern>
```

The template is valid. It differs in this way: FROM and TO carry the ID of the instance; the date stands as YYYY-MM-DD with
zone and the note "measured" or "context statement, not measured"; the RUN-ID consists of the short name of the sender and
a running number; GUARDRAILS may be written out.

## Versions

- **1.0** (28.10.2026) was part of the operator's rules and referred into them.
- **1.1** (30.10.2026) is the first that is completely readable without the other rules.
- **1.2** (30.10.2026) added four rules for the receiver after an external opinion.
- **1.3** (17.11.2026) makes the format a pure tool. What the receiver does with gaps, contradictions and doubled orders,
  when a text must be in the format and that rules come before the format, no longer stands here but in the rules the
  receiver works under. Two points of the way of writing are new: "condition before action" (after ASD-STE100, Simplified
  Technical English) and "first what is right, then the limit". New are also the line "Fragen" in the receipt and the note in
  PARAMETER where the format is; ESKALATION applies only to blockers. "siehe Kopf" is dropped. Every detail stands in one
  place only. Version 1.2 stays retrievable in the history of the repo.
- **Application 3** (23.11.2026) added the template for test reports (version 1.0) and an example. Fields, way of writing
  and wording of applications 1 and 2 stayed unchanged; the format stayed 1.3.
- **1.4** (2026-11-26) – decisions of the operator of 25.11.2026: (1) the test report is a fixed template of the format (template version 1.1: field names and words English, content as in 1.0); (2) BLOCK A, the field names and the notes are English, BLOCK B stays German; (3) the files have English names. Wording of applications 1 to 3 otherwise unchanged.

## Open

- Requests and findings in the inbox use fields of their own; the format knows only order,
  guide and test report. Whether it needs a form for them is open.
- Test report template 1.1: the blind test with fresh AIs (reviewer and user test)
  was not done in this run (a run starts no agent); the text is marked "ungeprüft (Blindtest offen)".
