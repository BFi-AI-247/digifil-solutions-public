# Example: a guide in the Two-Channel Format

<!-- Invented example for template-guide.md. The tool "Event Reminder" does not exist; file names and commands are made up,
     but as concrete as a real guide would have to name them. BLOCK A is English, BLOCK B German. -->

---

# Event Reminder 1.2

## BLOCK A – order to the AI that sets it up

```text
PURPOSE:      Every morning at the set time the Event Reminder sends an e-mail with the events of the day from a
              calendar file. It is set up when the test run produces an e-mail to the test address and the log holds a
              line with "ok".
APPLIES TO:   An AI sets up the reminder for a club or a family on a Linux machine.
DOES NOT APPLY TO: The person keeps the events in the calendar file himself. The reminder has no other way of sending than e-mail.
PREREQUISITES: Python 3.10 or newer · an e-mail account with SMTP access (server, port, user, password) · write access
              in the folder where the reminder lies · cron or a comparable scheduler.
FILES:        reminder.py (reads the calendar file, builds the e-mail, sends it) · settings.json (address, sender, test
              address, SMTP access, time, time zone; template settings.example.json) · events.csv (the events, one line
              per event: date;time;title) · reminder.log (one line per run, is created) · test_reminder.py (test run
              with test data, sends only to the test address).
TERMS:        Event of the day = every line in events.csv whose date equals the calendar day of the run in the time zone
              from settings.json. Test address = field "test_to" in settings.json.
BEHAVIOUR:    Without events on the day no e-mail is sent, but a log line is written ("ok, 0 events"). A faulty line in
              events.csv (wrong date format) is skipped and named in the log; the run does not stop because of it. The
              password stands only in settings.json, never in the log.
```

### STEPS (in this order; every step has a checkable result)

1. **Create the settings.** Copy `settings.example.json` to `settings.json` and fill the fields:

   | Placeholder | insert |
   |---|---|
   | `"to"` | the address from the order that the e-mail goes to. If it is missing, then leave the field empty and name it in the delivery as open; step 4 waits. |
   | `"from"` | the sender address of the e-mail account |
   | `"test_to"` | an address that the client reads. If it is missing, then stop the step and report it as open. |
   | `"smtp"` | server, port, user and password from the order. If something is missing, then stop the step and report it as open. |
   | `"time"` | the time from the order. If the order names none, then the default `"07:00"` applies; name it in the delivery as open. |
   | `"timezone"` | the time zone from the order. If the order names none, then the default `"Europe/Berlin"` applies; name it in the delivery as open. |

   *Result:* `python3 -c "import json; json.load(open('settings.json'))"` prints no error.
2. **Check the events.** `events.csv` holds `YYYY-MM-DD;HH:MM;title` per line; the first line is the heading.
   If the file is missing, then create one with the heading and one test event for today.
   *Result:* `head -2 events.csv` shows the heading and a valid line.
3. **Test run.** Run `python3 test_reminder.py`.
   *Result:* The output ends with "TEST OK"; at the test address there is an e-mail with the test event;
   `tail -1 reminder.log` begins with today's date and contains "ok".
4. **Set the schedule.** If the client has seen the test e-mail from step 3 and said "fine", and the field `"to"` is
   filled, then create a line in cron:
   `<minute> <hour> * * * cd <folder of the reminder> && python3 reminder.py`. Take minute and hour from the field
   `"time"` and replace the folder with the absolute path. Until then name the step in the delivery as
   "waiting for confirmation".
   *Result:* `crontab -l` shows the line with time and path.

```text
CHECK:        The results of step 3 and, after the confirmation, of step 4 apply together.
FAIL-MODE:    If a step does not work, then stop and report which step failed with which finding.
              If the test run sends nothing, then report the SMTP details as uncertain and stay with this account.
              If only a detail is missing, then the line of the field in step 1 applies.
DO NOT:       The password stands only in settings.json; do not write it into another file or into the delivery. ·
              In events.csv create at most the test line from step 2; do not change the rest of the content. · Set the
              time from step 1 and no other. · Until the client confirms, send only to the test address; nothing goes to
              real addresses before.
DELIVERY:     settings.json without the password line · output of step 3 · the cron line · open items ·
              every place where this guide was not enough, with quote.
```

---

## BLOCK B – für Menschen

Ein Verein hatte einen Kalender auf der Website, aber die Vorstandsmitglieder schauten nicht jeden Tag hinein – und so
stand beim Sommerfest niemand pünktlich am Grill. Der Event Reminder löst das auf die einfachste Art: Jeden Morgen kommt
eine E-Mail mit dem, was heute ansteht. Gibt es nichts, kommt auch keine E-Mail.

Die Termine pflegst du in einer einfachen Tabelle, eine Zeile je Termin. Das Programm liest sie, schreibt die E-Mail und
hält in einem Protokoll fest, dass es gelaufen ist. Eine fehlerhafte Zeile bringt nicht alles zum Stehen; sie wird
übersprungen und im Protokoll erwähnt, damit du sie findest.

## Was du im Alltag tust

Neue Termine trägst du in die Tabelle ein, alte lässt du einfach stehen. Kommt an einem Tag mit Terminen keine E-Mail,
schau ins Protokoll: Dort steht, ob das Programm gelaufen ist und was es gefunden hat. Mehr ist nicht zu tun.
