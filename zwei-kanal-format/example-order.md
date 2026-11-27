# Example: an order in the Two-Channel Format

<!-- Invented example for template-order.md. Club, persons, files and times are made up. BLOCK A is English, BLOCK B German. -->

Situation: A club runs a small website with an event calendar. Two AI instances work on it: "Editor_2" looks after the
texts, "Build_1" changes the code. The editor has noticed that the calendar keeps showing past events and orders the build.

```text
BLOCK A
FROM: Editor_2
TO: Build_1
DATE: 2026-11-03, 09:14 Europe/Berlin (measured)
RUN-ID: ED-041
ORDER: Hide in the event calendar all events whose end date is before today.
PARAMETERS:
- Filter in the file web/calendar.js, in the function loadEvents(), after loading.
- "Today" is the calendar day in the time zone Europe/Berlin, not universal time.
- An event without an end date counts until the end of its start date.
- Add two cases in tests/calendar.test.js: "ended yesterday → not visible" and "today → visible".
- Deliver the preview by 2026-11-04, 18:00 Europe/Berlin.
GUARDRAILS: Filter the display only. Do not change the data source data/events.json, and do not delete any event. ·
  Write only on the branch feature/41-old-events. Do not touch main; the operator gives the approval for main.
FAIL-MODE: If an end date in data/events.json cannot be read clearly, then stop and report the affected entries with
  the line number.
REQUIRE-ACK: RUN-ID ED-041 · state · name of the branch and commit · output of the test · questions · every place where
  this order was not enough, with quote.
ESCALATION: If you lack an access right to the repo, then ask the operator in the chat; only he grants rights.

BLOCK B
Auf der Startseite des Vereins stehen seit Wochen Veranstaltungen, die längst vorbei sind. Zwei Mitglieder haben sich
gemeldet, weil sie dachten, der Herbstmarkt finde noch einmal statt. Das wirkt ungepflegt und kostet Vertrauen.

Die Termine sollen deshalb von selbst verschwinden, sobald sie vorbei sind – ohne dass jemand sie von Hand löscht. Die
alten Einträge bleiben erhalten, nur sichtbar sind sie nicht mehr.
```

## The receipt

```text
ED-041 · Receipt
Received: 2026-11-03, 09:20 Europe/Berlin (measured)
State: done – filter in loadEvents(), two tests added, preview on feature/41-old-events.
Deviations: none. Three entries in data/events.json have no end date; by your rule they count until the end of the
  start day.
Questions: none
Evidence: commit 3f9a2c1 on feature/41-old-events; test output "12 passed".
```
