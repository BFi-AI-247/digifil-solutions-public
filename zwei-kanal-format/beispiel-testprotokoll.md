# Beispiel: ein Testprotokoll im Zwei-Kanal-Format

<!-- Erfundenes Beispiel zu testprotokoll-vorlage.md. Verein, Personen, Dateien, Commit und alle Zahlen sind ausgedacht.
     Das Beispiel setzt den Auftrag aus beispiel-auftrag.md fort. Es enthält absichtlich eine Abweichung und einen
     Schritt, der nicht geprüft wurde, damit alle Felder vorkommen. -->

Situation: Die KI „Bau_1“ hat den Filter für vergangene Termine gebaut (siehe `beispiel-auftrag.md`). Die Vorsitzende des
Vereins hat ihn am Vereinsrechner nach einer Testanleitung ausprobiert und die Ergebnisse an die KI „Test_1“ gemeldet. Test_1
schreibt das Protokoll und legt es unter `testprotokolle/2026-11-05_kalender-filter.md` ab.

---

# Testprotokoll Veranstaltungskalender – Filter vergangener Termine – 2026-11-05

## BLOCK A – für KIs

```text
VORLAGE:      Testprotokoll-Vorlage 1.0 (Zwei-Kanal-Format, Anwendung 3)
VON:          Test_1
DATUM:        2026-11-05, 11:02 Europe/Berlin (gemessen)
STAND:        Zweig feature/41-alte-termine, Commit 3f9a2c1 (Vorschau von Bau_1 aus dem Auftrag RED-041).
ANLEITUNG:    Testanleitung „Kalender-Filter“ von Redaktion_2 (RED-043), Schritte 1 bis 6.
DURCHGEFÜHRT: Von der Vorsitzenden des Vereins am 2026-11-05 gegen 09:30 am Vereinsrechner (Windows, Browser) mit der
              Vorschau des Zweigs.
QUELLE:       Nachricht von Redaktion_2 (RED-044) mit den Ergebnissen der Vorsitzenden. Ich habe nichts selbst erhoben.
GELESEN:      Die Testanleitung RED-043, die Nachricht RED-044, den Auftrag RED-041 und im Zweig die Funktion
              termineLaden() in web/kalender.js.
REGELN:       Keine Firmendaten: Dateinamen, Pfade, Servernamen, Artikel- und Filialnummern stehen nicht im Protokoll,
              Zählwerte schon. · Keine Bildtests: kein Screenshot, kein Bildvergleich; was nur am Bild zu sehen wäre,
              steht unter NICHT GEPRÜFT. · Abhilfen nur als Vorschlag, kein Bau.
UMGEBUNG:     Vereinsrechner, Windows, Browser mit Zeitzone Europe/Berlin. Testdaten: 20 Termine, davon 3 ohne
              Enddatum. Testtag: 2026-11-05. Weitere Angaben nicht gemeldet.

ERGEBNIS JE SCHRITT (Schritt · erwartet · gesehen · Urteil):
  1 Kalender öffnen · 14 sichtbare Termine (20 Termine, 6 davon vor dem Testtag beendet) · „15 Termine“ ·
    abweichend (AB-1)
  2 Termin suchen, der gestern endete · nicht sichtbar · „nicht gefunden“ · ok
  3 Termin suchen, der heute endet · sichtbar · „sichtbar, Zeile 4“ · ok
  4 Termin ohne Enddatum suchen, der gestern begann · nicht sichtbar (Regel aus RED-041: gilt bis zum Ende des
    Starttags) · „sichtbar“ · abweichend (AB-1)
  5 Datenquelle vergleichen · 20 Einträge vorher und nachher · abgehakt, keine Notiz · ok
  6 Seite kurz nach Mitternacht neu laden · Tageswechsel nach Europe/Berlin · nicht gemeldet ·
    nicht geprüft (Test lief gegen 09:30; die Mitternachtsprobe war nicht möglich)

NACHGERECHNET:
  20 Termine minus 6 vor dem Testtag beendete = 14 erwartet. Gesehen 15, also 1 Termin zu viel. Das passt zu genau einem
  Termin ohne Enddatum, der gestern begann (Schritt 4). Die anderen 2 Termine ohne Enddatum beginnen heute oder später
  und sind zu Recht sichtbar.

ABWEICHUNGEN (je Befund):
  AB-1 (Schritte 1 und 4) Ein Termin ohne Enddatum bleibt sichtbar, obwohl sein Starttag vorbei ist.
    Ursache: belegt – in termineLaden() steht der Vergleich „Enddatum vor heute“. Bei leerem Enddatum ist der Vergleich
      nie wahr, der Termin wird nicht ausgeblendet. Der Auftrag RED-041 verlangt dafür das Startdatum.
    Folge: Termine ohne Enddatum erscheinen im Kalender, bis jemand ein Enddatum einträgt. Im Testdatensatz betrifft das
      1 von 20 Terminen.
    Vorschlag: Bei leerem Enddatum das Startdatum für den Vergleich nehmen und dazu einen Testfall ergänzen. Das ist ein
      Auftrag an Bau_1, kein Teil dieses Protokolls.

BEWERTUNG:    bestanden mit Auflagen – Der Filter blendet beendete Termine aus und lässt die Datenquelle unverändert; nur der
              Sonderfall „Termin ohne Enddatum“ ist falsch.
NICHT GEPRÜFT:
  - Der Tageswechsel um Mitternacht (Schritt 6): Der Test lief am Vormittag.
  - Die Darstellung auf einem Mobilgerät: Das wäre ein Bildtest und ist ausgeschlossen.
OFFEN:
  1. Behebung von AB-1: Der Betreiber entscheidet, ob Bau_1 sie beauftragt bekommt (Empfehlung: ja, die Änderung ist
     klein).
  2. Mitternachtsprobe (Schritt 6): Die Vorsitzende wiederholt sie, sobald AB-1 behoben ist, oder der Betreiber
     verzichtet darauf.
```

## BLOCK B – für den Betreiber

Ergebnis: Der Filter für vergangene Termine funktioniert bis auf einen Sonderfall: bestanden mit Auflagen.
Abweichungen: Ein Termin ohne eingetragenes Enddatum bleibt im Kalender stehen, auch wenn sein Tag vorbei ist (1 von 20
Testterminen).
Nicht getestet: der Tageswechsel um Mitternacht und die Darstellung auf dem Handy.
Zu entscheiden: ob der Fehler behoben wird (Empfehlung: ja, der Aufwand ist klein) und ob die Mitternachtsprobe
wiederholt wird.

Test_1 · #001 · K0 · 2026-11-05 11:02 Europe/Berlin (gemessen)
