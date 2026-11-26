# Template: test report in the Two-Channel Format (application 3) – version 1.1

Version 1.1 of 2026-11-26 (version 1.0 of 2026-11-23 was German; 1.1 has English field names and words, the content is the
same). The version of the template stands in the field `TEMPLATE` of every report; if the template changes, the field
names the version the report was written by. Reports written by 1.0 stay valid as they are (they are history, not
errors). Example: `example-test-report.md`.

A test report records what a test of a tool showed. Several AIs write reports on different tools. The operator and every AI
must be able to read them side by side. Therefore all reports have the same file form, the same fields in the same
order and the same words of judgment.

Copy the content of the block below into a new file and replace all `<…>`. A note after `←` names the condition for a
field or a line: delete it if the condition does not apply, and always delete the note. Do not invent additional
fields. What fits no field goes under DEVIATIONS or OPEN. BLOCK B stays German (operator 25.11.2026 21:40).

## File and title

- Create the file in your own write area: `testprotokolle/<YYYY-MM-DD>_<test>.md`. `<YYYY-MM-DD>` is the day of the test.
  `<test>` is a short name of lowercase letters, digits and hyphens.
- The title reads exactly `# Testprotokoll <tool> – <test> – <YYYY-MM-DD>`.
- One test, one report. If the same test is repeated later, then create a new report. You do not change the old one.
- If the body that presents the result to the operator is not your reader, then send it BLOCK B as a message of its own as well.

## Words that every test report uses in the same way

| Word | Meaning |
|---|---|
| ok | What was seen matches what was expected, and the source proves it. |
| deviates | What was seen differs from what was expected. Every deviation gets a number `DEV-<n>` under DEVIATIONS. |
| not checked | The step was not carried out, not reported, or dropped because its condition did not occur. The reason stands in brackets. |
| evidenced | The statement stands in a source you have read. The source stands next to it. |
| ⟦interpretation⟧ | An assumption you have not checked. An interpretation stands only in the report, never as a fact. |
| passed | No step that the guide demands deviates. |
| passed with conditions | The purpose of the test is reached, but at least one step deviates or stayed open. Every condition stands under OPEN. |
| failed | The purpose of the test is missed: a step that the purpose demands deviates or failed. |

## Writing rules

- "Seen" is taken word for word from the source. If the source only reports that a step is ticked off, then write
  "ticked off, no note" and judge ok. Do not invent a wording.
- Recalculate what can be recalculated (sums, shares, times) and write it under RECALCULATED. Calculate only with values
  from the source.
- For every cause, say whether it is evidenced or an ⟦interpretation⟧.
- Only propose remedies. A test report builds and changes nothing.
- BLOCK B has at most eight lines of plain language, built as the template shows. BLOCK B contains no characters in
  backticks, no file names and no abbreviation without an explaining sentence. If BLOCK B says something other than
  BLOCK A, then BLOCK A applies.

````markdown
# Testprotokoll <tool> – <test> – <YYYY-MM-DD>

## BLOCK A – for AIs

```text
TEMPLATE:     Test report template 1.1 (Two-Channel Format, application 3)
FROM:         <ID of the author from role and number, e.g. Test_1>
DATE:         <YYYY-MM-DD, HH:MM zone> (measured | context statement, not measured)
STATE:        <What was tested: version, commit or build. If the build of the sample is not reported, then write
              "not reported" and name the state that the results prove at least, as ⟦interpretation⟧.>
GUIDE:        <Where the test guide is that the test followed, and which steps it has.>
CONDUCTED:    <Who carried out the test, when, where and with what. This is the time of the test, not the time of writing.>
SOURCE:       <collected myself | the message or file the results come from. If you collected nothing yourself, then write:
              "I collected nothing myself.">
READ:         <What you read for the assessment: guide, messages, code.>
RULES:        No company data: file names, paths, server names, article and branch numbers do not stand in the report,
              counts do. · No image tests: no screenshot, no image comparison; what could only be seen in the image
              stands under NOT TESTED. · Remedies only as a proposal, no building. · <further rule of this test>   ← if the client names a further rule
ENVIRONMENT:  <Machine, operating system, runtime, place of the data (counts only). Further details not reported.>

RESULT PER STEP (step · expected · seen · judgment):
  1 <name of the step> · <expected> · <seen, word for word> · ok | deviates (DEV-<n>) | not checked (<reason>)
  2 <…>

RECALCULATED:
  <What you recalculated from the values of the source, and whether it is right.>   ← if the report holds numbers that can be recalculated

DEVIATIONS (per finding):
  DEV-<n> (step <no.>) <What deviates, in one sentence.>
    Cause: evidenced – <source> | ⟦interpretation⟧ <assumption>, not checked
    Consequence: <What the deviation means for the use of the tool.>
    Proposal: <What would be done, without doing it.>
  None reported.   ← instead of the findings, if no step deviates

VERDICT:      passed | passed with conditions | failed – <one sentence with the reason>
NOT TESTED:
  - <What this test does not cover, and why not.>
OPEN:
  1. <What is still missing or to be decided – and who decides it.>
```

## BLOCK B – für den Betreiber

Ergebnis: <Das Ergebnis in einem Satz, in Klartext.>
Abweichungen: <Was abweicht, in ein bis drei Zeilen. Wenn nichts abweicht: „keine".>
Nicht getestet: <Was dieser Test nicht abdeckt, in einer Zeile.>
Zu entscheiden: <Was nur der Betreiber entscheiden kann, mit der Empfehlung. Wenn nichts: „nichts".>

<Signature line of your rules: ID · counter · time (measured)>   ← if your rules demand a signature
````

## Finishing the report

Before you file it, check: every step of the guide has a judgment · every deviation has a number, a cause and a
proposal · VERDICT uses one of the three words · `grep -n '<' <file>` shows no placeholder any more · BLOCK B has at most
eight lines.
