# Example: a test report in the Two-Channel Format

<!-- Invented example for template-test-report.md. Club, persons, files, commit and all numbers are made up. The example
     continues the order from example-order.md. It contains a deviation and a step that was not checked on purpose, so
     that all fields occur. BLOCK A is English, BLOCK B German. -->

Situation: The AI "Build_1" has built the filter for past events (see `example-order.md`). The chairwoman of the club tried
it out on the club computer by a test guide and reported the results to the AI "Test_1". Test_1 writes the report and files
it as `testprotokolle/2026-11-05_calendar-filter.md`.

---

# Testprotokoll Event Calendar – Filter for Past Events – 2026-11-05

## BLOCK A – for AIs

```text
TEMPLATE:     Test report template 1.1 (Two-Channel Format, application 3)
FROM:         Test_1
DATE:         2026-11-05, 11:02 Europe/Berlin (measured)
STATE:        Branch feature/41-old-events, commit 3f9a2c1 (preview by Build_1 from the order ED-041).
GUIDE:        Test guide "Calendar filter" by Editor_2 (ED-043), steps 1 to 6.
CONDUCTED:    By the chairwoman of the club on 2026-11-05 around 09:30 on the club computer (Windows, browser) with the
              preview of the branch.
SOURCE:       Message by Editor_2 (ED-044) with the results of the chairwoman. I collected nothing myself.
READ:         The test guide ED-043, the message ED-044, the order ED-041 and, in the branch, the function loadEvents()
              in web/calendar.js.
RULES:        No company data: file names, paths, server names, article and branch numbers do not stand in the report,
              counts do. · No image tests: no screenshot, no image comparison; what could only be seen in the image
              stands under NOT TESTED. · Remedies only as a proposal, no building.
ENVIRONMENT:  Club computer, Windows, browser with time zone Europe/Berlin. Test data: 20 events, 3 of them without end
              date. Test day: 2026-11-05. Further details not reported.

RESULT PER STEP (step · expected · seen · judgment):
  1 Open the calendar · 14 visible events (20 events, 6 of them ended before the test day) · "15 events" ·
    deviates (DEV-1)
  2 Look for an event that ended yesterday · not visible · "not found" · ok
  3 Look for an event that ends today · visible · "visible, line 4" · ok
  4 Look for an event without end date that began yesterday · not visible (rule from ED-041: counts until the end of
    the start day) · "visible" · deviates (DEV-1)
  5 Compare the data source · 20 entries before and after · ticked off, no note · ok
  6 Reload the page shortly after midnight · change of day by Europe/Berlin · not reported ·
    not checked (the test ran around 09:30; the midnight sample was not possible)

RECALCULATED:
  20 events minus 6 ended before the test day = 14 expected. Seen 15, so 1 event too many. That fits exactly one event
  without end date that began yesterday (step 4). The other 2 events without end date begin today or later and are
  rightly visible.

DEVIATIONS (per finding):
  DEV-1 (steps 1 and 4) An event without end date stays visible although its start day is over.
    Cause: evidenced – in loadEvents() stands the comparison "end date before today". With an empty end date the
      comparison is never true, the event is not hidden. The order ED-041 demands the start date for this case.
    Consequence: Events without end date appear in the calendar until someone enters an end date. In the test data set
      this concerns 1 of 20 events.
    Proposal: With an empty end date take the start date for the comparison and add a test case. This is an order to
      Build_1, not part of this report.

VERDICT:      passed with conditions – The filter hides ended events and leaves the data source unchanged; only the
              special case "event without end date" is wrong.
NOT TESTED:
  - The change of day at midnight (step 6): the test ran in the morning.
  - The display on a mobile device: that would be an image test and is excluded.
OPEN:
  1. Fix of DEV-1: the operator decides whether Build_1 gets the order (recommendation: yes, the change is small).
  2. Midnight sample (step 6): the chairwoman repeats it as soon as DEV-1 is fixed, or the operator waives it.
```

## BLOCK B – für den Betreiber

Ergebnis: Der Filter für vergangene Termine funktioniert bis auf einen Sonderfall: bestanden mit Auflagen.
Abweichungen: Ein Termin ohne eingetragenes Enddatum bleibt im Kalender stehen, auch wenn sein Tag vorbei ist (1 von 20
Testterminen).
Nicht getestet: der Tageswechsel um Mitternacht und die Darstellung auf dem Handy.
Zu entscheiden: ob der Fehler behoben wird (Empfehlung: ja, der Aufwand ist klein) und ob die Mitternachtsprobe
wiederholt wird.

Test_1 · #001 · K0 · 2026-11-05 11:02 Europe/Berlin (measured)
