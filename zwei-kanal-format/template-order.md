# Template: order in the Two-Channel Format (application 1)

<!-- Copy the block and replace all placeholders in angle brackets. Every field of BLOCK A is filled. A note after ← names
     the condition for a line: delete the line if it does not apply, and always delete the note. Delete this comment.
     BLOCK B stays German (operator 25.11.2026 21:40). Example: example-order.md. -->

```text
BLOCK A
FROM: <ID of the sender from role and number, e.g. Editor_2>
TO: <ID of the receiver, e.g. Build_1>
DATE: <YYYY-MM-DD, HH:MM zone> (measured | context statement, not measured)
RUN-ID: <short name of the sender>-<running number>
ORDER: <The action in one sentence.>
PARAMETERS:
- <File, path, value, deadline – everything the receiver needs to carry it out, one item per line.>
- <Where the format is (folder or file).>   ← if the receiver has to write in the format itself
- <File with the background and what the receiver reads it for.>   ← if BLOCK B would be longer than three paragraphs
- open: <missing detail> – <what the receiver does with it>   ← if you lack a detail
GUARDRAILS: <For each limit first what is right, then what the receiver leaves – written out or as an ID from a catalogue
  that sender and receiver both have. Without a limit: "none".>
FAIL-MODE: <What the receiver does if a part does not work.>
REQUIRE-ACK: <What comes back: at least the RUN-ID and the state of the execution, plus everything the sender wants to check.>
ESCALATION: <Who decides if the receiver cannot go on, and how to reach him – only for blockers that only the named person
  can solve. Questions come with the receipt. Without: "none".>

BLOCK B
<Hintergrund, Motivation, Einordnung für einen Menschen ohne Fachwissen, in höchstens drei Absätzen.>
```

## Receipt (the receiver's answer; do not send it along with the order)

```text
<RUN-ID> · Receipt
Received: <YYYY-MM-DD, HH:MM zone> (measured)
State: <done | partly | not started> – <one sentence>
Deviations: <none | which circumstance stood against which field>
Questions: <none | questions to the sender>
Evidence: <file, commit, log line>
```
