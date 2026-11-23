# Vorlage: Testprotokoll im Zwei-Kanal-Format (Anwendung 3) – Fassung 1.0

Fassung 1.0 vom 2026-11-23. Die Fassung der Vorlage steht im Feld `VORLAGE` jedes Protokolls; ändert sich die Vorlage, dann
steht dort die Fassung, nach der das Protokoll geschrieben wurde. Beispiel: `beispiel-testprotokoll.md`.

Ein Testprotokoll hält fest, was ein Test an einem Werkzeug ergeben hat. Mehrere KIs schreiben Protokolle zu verschiedenen
Werkzeugen. Der Betreiber und jede KI sollen sie nebeneinander lesen können. Deshalb haben alle Protokolle dieselbe
Dateiform, dieselben Felder in derselben Reihenfolge und dieselben Urteilswörter.

Kopiere den Inhalt des Blocks unten in eine neue Datei und ersetze alle `<…>`. Ein Hinweis hinter `←` nennt die Bedingung
für ein Feld oder eine Zeile: Lösche sie, wenn die Bedingung nicht zutrifft, und lösche in jedem Fall den Hinweis.
Erfinde keine zusätzlichen Felder. Was in kein Feld passt, steht unter ABWEICHUNGEN oder OFFEN.

## Datei und Titel

- Lege die Datei im eigenen Schreibbereich an: `testprotokolle/<JJJJ-MM-TT>_<test>.md`. `<JJJJ-MM-TT>` ist der Tag der
  Durchführung. `<test>` ist ein kurzer Name aus Kleinbuchstaben, Ziffern und Bindestrichen.
- Der Titel lautet genau `# Testprotokoll <Werkzeug> – <Test> – <JJJJ-MM-TT>`.
- Ein Test, ein Protokoll. Wenn derselbe Test später wiederholt wird, dann lege ein neues Protokoll an. Das alte änderst
  du nicht.
- Wenn die Stelle, die dem Betreiber das Ergebnis vorlegt, nicht dein Leser ist, dann sende ihr zusätzlich Block B als
  eigene Nachricht.

## Wörter, die jedes Testprotokoll gleich benutzt

| Wort | Bedeutung |
|---|---|
| ok | Das Gesehene entspricht dem Erwarteten, und die Quelle belegt es. |
| abweichend | Das Gesehene weicht vom Erwarteten ab. Jede Abweichung bekommt eine Nummer `AB-<n>` unter ABWEICHUNGEN. |
| nicht geprüft | Der Schritt wurde nicht ausgeführt, nicht gemeldet oder entfiel, weil seine Bedingung nicht eintrat. Der Grund steht in Klammern. |
| belegt | Die Angabe steht in einer Quelle, die du gelesen hast. Die Quelle steht dabei. |
| ⟦Deutung⟧ | Eine Annahme, die du nicht geprüft hast. Eine Deutung steht nur im Protokoll, nie als Tatsache. |
| bestanden | Kein Schritt weicht ab, den die Anleitung verlangt. |
| bestanden mit Auflagen | Der Zweck des Tests ist erreicht, aber mindestens ein Schritt weicht ab oder blieb offen. Jede Auflage steht unter OFFEN. |
| nicht bestanden | Der Zweck des Tests ist verfehlt: Ein Schritt, den der Zweck verlangt, weicht ab oder ist gescheitert. |

## Schreibregeln

- „Gesehen“ ist wörtlich aus der Quelle übernommen. Wenn die Quelle nur meldet, dass ein Schritt abgehakt ist, dann
  schreib „abgehakt, keine Notiz“ und urteile ok. Erfinde keinen Wortlaut.
- Rechne nach, was sich nachrechnen lässt (Summen, Anteile, Zeiten), und schreib es unter NACHGERECHNET. Rechne nur mit
  Werten aus der Quelle.
- Nenne bei jeder Ursache, ob sie belegt ist oder eine ⟦Deutung⟧.
- Schlag Abhilfen nur vor. Ein Testprotokoll baut und ändert nichts.
- Block B hat höchstens acht Zeilen Klartext, nach dem Aufbau der Vorlage. Block B enthält keine Zeichen in Backticks,
  keine Dateinamen und kein Kürzel ohne erklärenden Satz. Wenn Block B etwas anderes sagt als Block A, dann gilt Block A.

````markdown
# Testprotokoll <Werkzeug> – <Test> – <JJJJ-MM-TT>

## BLOCK A – für KIs

```text
VORLAGE:      Testprotokoll-Vorlage 1.0 (Zwei-Kanal-Format, Anwendung 3)
VON:          <Kennung des Verfassers aus Rolle und Nummer, z. B. Test_1>
DATUM:        <JJJJ-MM-TT, HH:MM Zeitzone> (gemessen | Kontextangabe, nicht gemessen)
STAND:        <Was getestet wurde: Version, Commit oder Build. Wenn der Build der Probe nicht gemeldet ist, dann schreib
              „nicht gemeldet“ und nenne den Stand, den die Ergebnisse mindestens belegen, als ⟦Deutung⟧.>
ANLEITUNG:    <Wo die Testanleitung steht, nach der getestet wurde, und welche Schritte sie hat.>
DURCHGEFÜHRT: <Wer den Test wann, wo und womit ausgeführt hat. Das ist die Zeit des Tests, nicht die Zeit des Schreibens.>
QUELLE:       <selbst erhoben | die Nachricht oder Datei, aus der die Ergebnisse stammen. Wenn du nichts selbst erhoben
              hast, dann schreib: „Ich habe nichts selbst erhoben.“>
GELESEN:      <Was du für die Bewertung gelesen hast: Anleitung, Nachrichten, Code.>
REGELN:       Keine Firmendaten: Dateinamen, Pfade, Servernamen, Artikel- und Filialnummern stehen nicht im Protokoll,
              Zählwerte schon. · Keine Bildtests: kein Screenshot, kein Bildvergleich; was nur am Bild zu sehen wäre,
              steht unter NICHT GEPRÜFT. · Abhilfen nur als Vorschlag, kein Bau. · <weitere Regel dieses Tests>   ← wenn der Auftraggeber eine weitere Regel nennt
UMGEBUNG:     <Rechner, Betriebssystem, Laufzeit, Lage der Daten (nur Zählwerte). Weitere Angaben nicht gemeldet.>

ERGEBNIS JE SCHRITT (Schritt · erwartet · gesehen · Urteil):
  1 <Name des Schritts> · <erwartet> · <gesehen, wörtlich> · ok | abweichend (AB-<n>) | nicht geprüft (<Grund>)
  2 <…>

NACHGERECHNET:
  <Was du aus den Werten der Quelle nachgerechnet hast und ob es stimmt.>   ← wenn das Protokoll Zahlen enthält, die sich nachrechnen lassen

ABWEICHUNGEN (je Befund):
  AB-<n> (Schritt <Nr>) <Was weicht ab, in einem Satz.>
    Ursache: belegt – <Quelle> | ⟦Deutung⟧ <Annahme>, nicht geprüft
    Folge: <Was die Abweichung für die Benutzung des Werkzeugs bedeutet.>
    Vorschlag: <Was zu tun wäre, ohne es zu tun.>
  Keine gemeldet.   ← statt der Befunde, wenn kein Schritt abweicht

BEWERTUNG:    bestanden | bestanden mit Auflagen | nicht bestanden – <ein Satz mit dem Grund>
NICHT GEPRÜFT:
  - <Was dieser Test nicht abdeckt, und warum nicht.>
OFFEN:
  1. <Was noch fehlt oder zu entscheiden ist – und wer es entscheidet.>
```

## BLOCK B – für den Betreiber

Ergebnis: <Das Ergebnis in einem Satz, in Klartext.>
Abweichungen: <Was abweicht, in ein bis drei Zeilen. Wenn nichts abweicht: „keine“.>
Nicht getestet: <Was dieser Test nicht abdeckt, in einer Zeile.>
Zu entscheiden: <Was nur der Betreiber entscheiden kann, mit der Empfehlung. Wenn nichts: „nichts“.>

<Signaturzeile deines Regelwerks: Kennung · Zähler · Zeit (gemessen)>   ← wenn dein Regelwerk eine Signatur verlangt
````

## Das Protokoll abschließen

Prüfe vor dem Ablegen: Jeder Schritt der Anleitung hat ein Urteil · jede Abweichung hat eine Nummer, eine Ursache und
einen Vorschlag · BEWERTUNG nutzt eines der drei Wörter · `grep -n '<' <datei>` zeigt keinen Platzhalter mehr · Block B
hat höchstens acht Zeilen.
