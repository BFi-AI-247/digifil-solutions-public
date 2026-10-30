Stand: 2026-10-30d

# Zwei-Kanal-Format 1.1 – Konzept

*AI-to-AI-and-Human-Messages: ein Text, zwei Leser – Block A für die KI, die handelt, Block B für den Menschen.*

Dieser Ordner ist die vollständige, eigenständige Fassung des Formats. Er besteht aus: `README.md` (Anleitung, wie man
einen Text im Format schreibt), `konzept.md` (diese Datei: Grundsatz, beide Anwendungen, Schreibregeln, Prüfungen),
`auftrag-vorlage.md` (Vorlage für Aufträge), `readme-vorlage.md` (Vorlage für Anleitungen), `beispiel-auftrag.md` und
`beispiel-readme.md` (je ein vollständiges, erfundenes Beispiel).

Ein Text, nach dem eine KI (oder ein Mensch) handeln soll, besteht aus zwei getrennten Blöcken:

- **Block A – Ausführungskanal:** alles, was zum Handeln nötig ist, in festen Feldern.
- **Block B – Mensch-Kanal:** Hintergrund, Motivation, Einordnung. Nie eine Anweisung.

Das Format gilt für zwei Arten von Texten: **Aufträge** (eine Nachricht von einem Agenten an einen anderen, Anwendung 1)
und **Anleitungen** (eine README, nach der eine KI etwas einrichtet oder benutzt, Anwendung 2). Der Grundsatz ist derselbe,
die Felder sind verschieden.

## Drei Begriffe

Drei Wörter, die überall gleich gemeint sind: **Betreiber** ist der Mensch, dem das Vorhaben gehört; er gibt Aufträge,
erteilt Freigaben und ist die letzte Instanz bei Fragen (in den Zitaten unten dasselbe Wort). **Auftraggeber** ist, wer den
konkreten Auftrag gibt – der Betreiber selbst oder ein Agent in seinem Auftrag. **Instanz** ist eine laufende KI mit einer
Kennung, die in ihren Texten steht (zum Beispiel „Bau_1“).

## Grundsatz (beide Anwendungen)

Die Zitate in diesem Abschnitt stammen aus der Auftragsform einer KI-Agentur (Fassung 1.0, September/Oktober 2026), in der
das Format entstand. Sie sind wörtlich übernommen.

**Trennregel.**
> „**Block B darf niemals Informationen enthalten, die für die Ausführung notwendig sind — alles Ausführungsrelevante gehört zwingend in Block A.**“

**Zwei Prüffragen vor dem Abschicken.**
> 1. „Ist dieser Kontext-Satz eigentlich eine Anweisung? → nach A verschieben.“
> 2. „Könnte der Empfänger den Auftrag korrekt ausführen, wenn Block B weg wäre?“ — Nein → Inhalt fehlt in A.

**Vorrang der Regeln.**
> „Das Format SCHICHTET die Kommunikation zusätzlich; es suspendiert, ersetzt oder lockert KEINE Regel. Widerspricht ein Block-A-Feld dem Kanon, ist das Feld falsch, nicht der Kanon.“

„Kanon“ meint hier das Regelwerk, nach dem der Empfänger arbeitet. Das Format ist eine Form für Texte, keine Erlaubnis:
Ein Auftrag im richtigen Format darf nichts, was die Regeln des Empfängers verbieten.

**Warum überhaupt.**
> „Mehrdeutigkeit entsteht bei Wirkung, nicht bei Wortzahl; das Format schichtet nur, wo Fehlinterpretation Schaden anrichten könnte (Doppelausführung, Format-Drift).“

**Block B ist Klartext.** Block B muss ein Mensch ohne Fachwissen verstehen: keine Funktions-, Datei- oder Feldnamen, keine
Abkürzungen ohne Erklärung, ganze Sätze. Prüffrage: *Weiß ein Leser nach Block B, wozu das Ganze gut ist und was er selbst
tun muss – ohne Block A gelesen zu haben?*
Anlass: Der Betreiber, für den die erste Anleitung in diesem Format geschrieben wurde, fand deren Block B „Kauderwelsch“ –
eine Tabelle aus Regelkürzeln und Funktionsnamen.

---

## Anwendung 1: Aufträge zwischen Agenten

Vorlage: `auftrag-vorlage.md`. Beispiel: `beispiel-auftrag.md`.

**Wann.** Zitat:
> „Ein Auftrag darf im Klartext bleiben, wenn ALLE drei Bedingungen erfüllt sind: keine Bestands-/Job-Berührung · keine Leitplanken-Relevanz · ein Empfänger, ein Strang. Quittierungen sind KEINE Aufträge — sie bleiben immer im kurzen Format.“

In eigenen Worten: Ändert der Auftrag etwas (Dateien, einen laufenden Ablauf, eine Begrenzung) oder richtet er sich an mehr
als einen Empfänger, kommt er ins Format. Eine Rückfrage, eine Quittung oder ein Hinweis ohne Wirkung bleibt formlos.

**Felder von Block A.** Zitat:
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

Das Zitat zeigt die Herkunft; die gültige Form ist die Vorlage `auftrag-vorlage.md`. Sie weicht vom Zitat so ab:
- VON und AN tragen die Kennung der Instanz („Redaktion_2“: Rolle und Nummer in einem Wort).
- Datum als `JJJJ-MM-TT, HH:MM` mit Zeitzone. Konnte die Zeit nicht gemessen werden, steht sie mit dem Vermerk
  „Kontextangabe, nicht gemessen“ statt „Stempel unsicher“ („Betreiber-Wahrnehmung“ im Zitat meint die Uhrzeit, die der
  Betreiber auf seinem Gerät sieht).
- RUN-ID als Kürzel des Absenders plus fortlaufende Nummer („RED-041“).
- DATUM und RUN-ID dürfen „siehe Kopf“ lauten, wenn der Transportweg beides trägt (unten).
- LEITPLANKEN dürfen ausgeschrieben sein, wenn es keinen gemeinsamen Katalog gibt (unten).

**Alle zehn Felder sind Pflicht.** LEITPLANKEN und ESKALATION dürfen „keine“ lauten, aber nie fehlen; REQUIRE-ACK enthält
mindestens RUN-ID und Stand.

Erläuterung der Felder, die Erklärung brauchen:
- **DATUM** ist die gemessene Systemzeit des Absenders, nie eine Erinnerung oder ein Wert aus einer Vorlage; geht Messen
  nicht, steht die beste Angabe mit dem Vermerk „Kontextangabe, nicht gemessen“. Trägt der
  Transportweg bereits ein gemessenes Datum und die RUN-ID – etwa die Kopfzeilen (Nummer, Von, Datum, RUN-ID) einer
  Nachricht, die als Datei abgelegt wird –, dürfen die Felder DATUM und RUN-ID in Block A darauf verweisen („siehe Kopf“);
  eine Angabe steht genau einmal.
- **LEITPLANKEN** sind Begrenzungen, die der Empfänger kennt (etwa „kein Löschen“, „keine Veröffentlichung“). Gibt es bei
  Absender und Empfänger keinen gemeinsamen Katalog solcher Begrenzungen, stehen sie hier ausgeschrieben; „keine“ ist
  ausdrücklich zu schreiben, nicht wegzulassen.
- **REQUIRE-ACK** ist die Bestellung der Quittung: Der Absender sagt, was er zurückbekommen will. Mindestens die RUN-ID
  und den Stand der Ausführung – sonst kann niemand abgleichen, ob der Auftrag schon bearbeitet wurde.

**Was nicht in Block B darf.** Zitat:
> „Block B darf enthalten: Hintergrund, Motivation, Einordnung, Betreiber-Zitate. Block B darf NICHT: Fristen, Datei-Pfade, Schwellen, Freigaben, Namen/Beteiligte, Verweise auf frühere Punkte.“

Diese Liste gilt für beide Anwendungen und steht nur hier; Anleitung und Vorlagen verweisen auf sie. Maßstab ist die
Trennregel: verboten ist, was der Empfänger zum Handeln braucht. Eine Zahl, die er zum Handeln braucht, steht in Block A
(und darf in Block B zur Erklärung wiederholt werden); eine Zahl, die nur erzählt („beim ersten Versuch 22 Stellen“), darf
allein in Block B stehen.

**Wenn der Verfasser eine Angabe nicht hat.** Wer einen Auftrag schreibt und eine Angabe nicht kennt (einen Wert, einen Pfad,
eine Frist), rät nicht und lässt die Lücke nicht in Block B verschwinden. Entweder er beschafft die Angabe vor dem
Abschicken beim Betreiber, oder er schreibt sie in PARAMETER als offen: `offen: <Angabe> – vor dem Handeln beim Absender erfragen`. Der Empfänger führt den Teil des Auftrags, der die offene Angabe braucht, nicht aus: Er fragt auf dem Weg aus
ESKALATION beim Absender nach, erledigt den Rest und meldet in der Quittung `teilweise – wartet auf <Angabe>`. Er setzt
keine eigene Vorgabe ein; das dürfen nur Anleitungen, die eine Vorgabe ausdrücklich nennen (Anwendung 2).

**Quittung.** Zitat:
> „Der Empfänger zitiert die Auftrags-Nummer am Anfang seiner Quittierung — nur mit Rückbezug kann abgleichen, ob der Auftrag schon bearbeitet wurde (auch über einen Instanz-Wechsel hinweg).“

Die Quittung selbst ist kein Auftrag und bleibt formlos: RUN-ID zuerst, dann Empfangen (Zeit, gemessen), Stand (erledigt,
teilweise, nicht begonnen), Abweichungen, Beleg (Datei, Commit, Protokollzeile). Trägt der Transportweg die RUN-ID in der Kopfzeile oder ein Feld
„Antwort auf“, erfüllt das den Rückbezug.

**Substanz auslagern.** Zitat:
> „Nachrichten-Kerne bleiben kurz; Substanz (Konzepte, Begründungen, Rohfassungen) wird als eigene Datei in der Wissens-Ablage hinterlegt und mit Lese-Auslöser referenziert (Zweck + entscheidungsrelevante Abschnitte).“

Schwelle für Aufträge: Block B hat höchstens drei Absätze. Was länger wird, ist Substanz und gehört in eine eigene Datei;
Block A nennt sie mit Lese-Auslöser (Zweck der Datei und was der Leser darin entscheidet). Für Anleitungen (Anwendung 2)
gilt diese Zahl nicht – dort ist Block B so lang, wie ein Mensch zum Verstehen braucht, und bleibt trotzdem kürzer als Block A.

---

## Anwendung 2: Anleitungen (README)

Vorlage: `readme-vorlage.md`. Beispiel: `beispiel-readme.md`. Die Anleitung dieses Ordners (`README.md`) ist selbst in
dieser Form geschrieben.

Diese Anwendung ist eine Erweiterung vom 28.10.2026; die Agentur-Fassung kannte das Format nur für Aufträge. Anlass:
Der Betreiber las die erste Anleitung eines Werkzeugs und fand sie nichtssagend („Tw. drei Wort Anweisungen, die für mich
viel Interpretationspielraum lassen“), dazu: „welcher Mensch liest denn noch Readme. Das liest doch auch alles KI. Für mich
ein Fall für das Zwei-Kanal-Verfahren.“

**Was anders ist als beim Auftrag.** Eine README ist kein einmaliger Auftrag, sondern liegt dauerhaft da und wird von
vielen gelesen. Deshalb entfallen VON, AN, DATUM und RUN-ID; an ihre Stelle tritt die Version im Titel. Aus AUFTRAG wird
ZWECK, aus PARAMETER werden VORAUSSETZUNG und DATEIEN, aus LEITPLANKEN wird NICHT TUN, aus REQUIRE-ACK wird LIEFERUNG.
FAIL-MODE bleibt und enthält die Eskalation.

**Felder von Block A** (Reihenfolge fest):

| Feld | Inhalt | Pflicht |
|---|---|---|
| ZWECK | Was am Ende steht, in ein bis drei Sätzen; prüfbar formuliert | ja |
| GILT FÜR / GILT NICHT | Wofür die Anleitung gedacht ist; was nicht, mit Verweis, wo es stattdessen steht | ja |
| VORAUSSETZUNG | Was vorher da sein muss (Sprache, Version, Zugriff, Dienste) | ja |
| DATEIEN | Jede Datei des Ordners mit einem Halbsatz, wozu sie dient | ja |
| BEGRIFFE | Jeder Begriff, den die Schritte verwenden und der mehr als eine Deutung zulässt | wenn nötig |
| VERHALTEN | Wie das Werkzeug sich heute verhält, als prüfbare Aussagen – für jede KI, die Fragen dazu beantwortet oder Änderungen plant. Anlass: Eine KI, die Rückmeldungen zu einem Werkzeug beantwortet, soll „so ist es heute“ aus der README sagen können, ohne den Code zu lesen | bei Werkzeugen, die laufen |
| SCHRITTE | Nummeriert, in fester Reihenfolge; jeder mit *Ergebnis:* – einem Befehl oder einer Beobachtung, die zeigt, dass der Schritt gelang. Wo etwas auszufüllen ist: Tabelle Platzhalter → einsetzen, mit Vorgabe, wenn der Auftrag nichts sagt | ja |
| PRÜFUNG | Was am Ende alles bestätigt: ein Befehl – oder die Liste der Ergebnisse aus den Schritten, die zusammen gelten müssen | ja |
| FAIL-MODE | Was tun, wenn ein Schritt nicht geht; was tun, wenn nur eine Angabe fehlt | ja |
| NICHT TUN | Was ausdrücklich verboten ist | ja |
| LIEFERUNG | Was die einrichtende KI am Ende zurückmeldet – immer mit „jede Stelle, an der diese Anleitung nicht reichte (mit Zitat)“ | ja |
| REFERENZ | Wo die Einzelheiten stehen (Regeln, Herkunft) | wenn nötig |

**Schreibregeln für Block A** (beide Anwendungen).
- Ganze Sätze mit Verb, kein Stichwort-Telegramm. Anlass: „drei Wort Anweisungen“ (Betreiber, 28.10.2026).
- Listenfelder (PARAMETER, LEITPLANKEN, DATEIEN, NICHT TUN, LIEFERUNG) dürfen ihre Punkte mit „·“ oder je Zeile trennen;
  jeder Punkt ist dann eine vollständige Aussage oder eine Datei mit einem Halbsatz, wozu sie dient.
- Jeder Schritt sagt, *welche* Datei, *welche* Stelle, *welcher* Wert. „Anpassen“ ohne Ziel ist kein Schritt.
- Lässt ein Platzhalter Raum, steht die Vorgabe daneben („sonst …“) und der Satz „in der Lieferung als offen nennen“.
- Was nur im Code steht (Dateiname, Ablageort, das Wort, mit dem der Code eine Rolle bezeichnet), steht auch in Block A. Anlass: Ein Blindtest fand den Ablageort
  einer Sperrliste nur im Code.
- Dieselbe Sache hat überall dasselbe Wort. Anlass: Ein Blindtest fand für denselben Begriff zwei Wörter – eines auf der
  Kommandozeile, eines im Code – und wusste nicht, ob beide dasselbe meinen.

**Schreibregeln für Block B.** Klartext (siehe Grundsatz). Gut bewährt: ein echter Vorfall als Einstieg, dann was das Ding
tut, dann was der Mensch im Alltag selbst tut. Regellisten nach Themen, je mit „warum“ und ob das Programm es prüft oder es
nur eine Bitte an das Modell ist.

---

## Prüfungen

**Die zwei Prüffragen** (beide Anwendungen) stehen im Grundsatz. Sie werden vor jedem Abschicken gestellt, Satz für Satz
in Block B.

**Blindtest – die Prüfung für Block A jeder Anleitung (Anwendung 2).** Eine frische KI ohne Vorwissen – eine, die weder
die Anleitung noch das Projekt kennt – bekommt **nur Block A** und einen kleinen, erfundenen Auftrag, der zu GILT FÜR passt
(„richte damit einen Vereins-Assistenten ein“, „beantworte damit drei Fragen zum Werkzeug“). Sie arbeitet die Schritte ab
und liefert, was LIEFERUNG verlangt – vor allem die Liste der Stellen, an denen sie raten musste. Jede Stelle wird in Block A
(oder im Code) behoben; dann folgt der nächste Blindtest mit einem anderen erfundenen Auftrag. Fertig ist Block A, wenn ein
Blindtest nur noch Kleinigkeiten findet und keine echte Lücke. Auftrag, Liste der Ratestellen und Behebung werden
aufbewahrt, wo das Projekt seine Prüfungen ablegt, und in der Lieferung genannt.
Steht keine frische KI zur Verfügung, ist der Ersatz dieselbe KI in einer neuen Sitzung ohne Verlauf, nur mit Block A und
dem Auftrag. Das ist schwächer, weil ihr Modell dieselben Lücken übersehen kann; die Lieferung nennt den Ersatz als solchen.
Ist auch das nicht möglich, wird die Anleitung ohne Blindtest ausgeliefert und in der Lieferung als „ungeprüft (Blindtest
offen)“ gekennzeichnet; der Auftraggeber entscheidet, wer ihn nachholt.
Erfahrungswerte aus der ersten Anleitung, die so geprüft wurde (Oktober 2026, die Anleitung eines Prüfwerkzeugs mit einer
Sperrliste für Wörter, die nie in Dateien stehen dürfen): Blindtest 1 fand 22 Stellen, Blindtest 2 fand 18 kleinere und
einen Fehler im Code, Blindtest 3 fand 11, darunter eine echte Lücke (die Sperrliste fing Kontonummern nicht), die behoben
wurde; Blindtest 4 fand nur noch Kleinigkeiten.

**Gutachter-Test und Anwender-Test – die Prüfung für eine Veröffentlichung des Formats selbst.** Eine frische KI bekommt
nur diesen Ordner und den Auftrag, ihn als Veröffentlichung zu begutachten (Verweise, Widersprüche, Interna). Eine zweite
frische KI schreibt mit dem Ordner einen erfundenen Auftrag und eine erfundene README und meldet, wo sie raten musste.
Beide Tests ohne echte Lücke: der Ordner ist fertig.

---

## Herkunft

Das Format entstand im September und Oktober 2026 im Regelwerk einer KI-Agentur, die mit mehreren KI-Instanzen eine
Website baute und betrieb; die Zitate oben stammen aus deren Auftragsform (Fassung 1.0). Anwendung 2, die Klartext-Regel
für Block B, die Schwelle für Block B und der Blindtest sind Entscheidungen des Betreibers, der diesen Ordner herausgibt,
vom 28. bis 30. Oktober 2026. Fassung 1.0 (28.10.2026) war Teil seines Regelwerks und verwies hinein; Fassung 1.1
(30.10.2026) ist die erste, die ohne das übrige Regelwerk vollständig lesbar ist.
