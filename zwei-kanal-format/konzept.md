Stand: 2026-11-17

# Zwei-Kanal-Format – Konzept

Das Zwei-Kanal-Format ist ein Werkzeug. Es legt fest, wie ein Text gebaut ist, nach dem eine KI handeln soll. Was eine KI
darf und muss, regelt das Regelwerk, nach dem sie arbeitet; das Format ersetzt und lockert davon nichts.

Wie man einen Text im Format schreibt, steht in `README.md`. Wie die Felder aussehen, steht in `auftrag-vorlage.md` und
`readme-vorlage.md`. Hier steht, warum das Format so ist.

## Grundsatz

Die Zitate stammen aus der Auftragsform einer KI-Agentur (Fassung 1.0, September/Oktober 2026), in der das Format
entstand. Sie sind wörtlich übernommen.

**Trennregel.**
> „**Block B darf niemals Informationen enthalten, die für die Ausführung notwendig sind — alles Ausführungsrelevante gehört zwingend in Block A.**“

So wird ein Text im Format gelesen: Block A gilt, Block B erklärt. Block B enthält keine Anweisung an den Empfänger; was
der Mensch selbst tut, darf dort stehen. Wenn Block B etwas anderes sagt als Block A, dann gilt Block A, und der Satz in
Block B ist ein Fehler im Text.

**Was nicht in Block B gehört.**
> „Block B darf enthalten: Hintergrund, Motivation, Einordnung, Betreiber-Zitate. Block B darf NICHT: Fristen, Datei-Pfade, Schwellen, Freigaben, Namen/Beteiligte, Verweise auf frühere Punkte.“

Maßstab ist die Trennregel. Eine Angabe, die der Empfänger zum Handeln braucht, steht in Block A; Block B darf sie zur
Erklärung wiederholen. Eine Zahl, die nur erzählt („beim ersten Versuch 22 Stellen“), darf allein in Block B stehen.

**Zwei Prüffragen.**
> 1. „Ist dieser Kontext-Satz eigentlich eine Anweisung? → nach A verschieben.“
> 2. „Könnte der Empfänger den Auftrag korrekt ausführen, wenn Block B weg wäre?“ — Nein → Inhalt fehlt in A.

Die Fragen sind die Trennregel als Probe. Gestellt werden sie in `README.md`, Schritt 3.

**Warum überhaupt.**
> „Mehrdeutigkeit entsteht bei Wirkung, nicht bei Wortzahl; das Format schichtet nur, wo Fehlinterpretation Schaden anrichten könnte (Doppelausführung, Format-Drift).“

**Block B ist Klartext.** Probe: *Weiß ein Leser nach Block B, wozu das Ganze gut ist und was er selbst tun muss – ohne
Block A gelesen zu haben?* Anlass: Der Betreiber, für den die erste Anleitung in diesem Format geschrieben wurde, fand
deren Block B „Kauderwelsch“ – eine Tabelle aus Regelkürzeln und Funktionsnamen.

## Drei Begriffe

**Betreiber** ist der Mensch, dem das Vorhaben gehört (in den Zitaten dasselbe Wort). **Auftraggeber** ist, wer den
konkreten Auftrag gibt – der Betreiber selbst oder eine KI in seinem Auftrag. **Instanz** ist eine laufende KI mit einer
Kennung aus Rolle und Nummer (zum Beispiel „Bau_1“).

## Anwendung 1: Aufträge

Form: `auftrag-vorlage.md`. Beispiel: `beispiel-auftrag.md`. Warum die Vorlage so ist:

- **DATUM und RUN-ID stehen immer in Block A,** auch wenn der Transportweg beides schon trägt. Anlass: Blindtest
  16.11.2026 – Block A wurde ohne den Kopf der Nachricht weitergegeben, Datum und RUN-ID fehlten.
- **ESKALATION ist für Blocker, Rückfragen kommen mit der Quittung.** Anlass: Blindtest 16.11.2026 – Fragen in
  REQUIRE-ACK und Eskalation an den Betreiber im selben Auftrag; die Leser wussten nicht, wohin.
- **PARAMETER nennt, wo das Format steht,** wenn der Empfänger selbst im Format schreiben soll. Anlass: Blindtest
  16.11.2026 – zwei von vier Lesern wussten nicht, was in Block B gehört.
- **Die Quittung beginnt mit der RUN-ID.** Zitat:
  > „Der Empfänger zitiert die Auftrags-Nummer am Anfang seiner Quittierung — nur mit Rückbezug kann abgleichen, ob der Auftrag schon bearbeitet wurde (auch über einen Instanz-Wechsel hinweg).“
- **Block B hat höchstens drei Absätze;** Längeres steht in einer eigenen Datei. Zitat:
  > „Nachrichten-Kerne bleiben kurz; Substanz (Konzepte, Begründungen, Rohfassungen) wird als eigene Datei in der Wissens-Ablage hinterlegt und mit Lese-Auslöser referenziert (Zweck + entscheidungsrelevante Abschnitte).“

## Anwendung 2: Anleitungen

Form: `readme-vorlage.md`. Beispiel: `beispiel-readme.md`. Auch `README.md` ist so geschrieben.

Diese Anwendung ist eine Erweiterung vom 28.10.2026; die Agentur-Fassung kannte das Format nur für Aufträge. Anlass:
Der Betreiber las die erste Anleitung eines Werkzeugs und fand sie nichtssagend („Tw. drei Wort Anweisungen, die für mich
viel Interpretationspielraum lassen“), dazu: „welcher Mensch liest denn noch Readme. Das liest doch auch alles KI. Für mich
ein Fall für das Zwei-Kanal-Verfahren.“

Eine Anleitung liegt dauerhaft da und wird von vielen gelesen. Deshalb tritt an die Stelle von VON, AN, DATUM und RUN-ID
die Version im Titel. Aus AUFTRAG wird ZWECK, aus PARAMETER werden VORAUSSETZUNG und DATEIEN, aus LEITPLANKEN wird
NICHT TUN, aus REQUIRE-ACK wird LIEFERUNG; FAIL-MODE enthält die Eskalation. Block B ist so lang, wie ein Mensch zum
Verstehen braucht, und bleibt kürzer als Block A.

VERHALTEN gibt es, damit eine KI, die Rückmeldungen zu einem Werkzeug beantwortet, „so ist es heute“ aus der Anleitung
sagen kann, ohne den Code zu lesen.

## Anlässe der Schreibweise

Die Schreibweise steht in `README.md`, Schritt 2, und in den Vorlagen. Hier steht je Punkt, woher er kommt.

- **Ganze Sätze mit Verb:** die „drei Wort Anweisungen“ aus dem Anlass zu Anwendung 2.
- **Bedingung vor Handlung:** Blindtest 16.11.2026 – „scheitert tkinter: Rückfallweg …“ ließ offen, wer entscheidet;
  „Wenn tkinter scheitert, dann nimm …“ nicht.
- **Erst das Richtige, dann die Grenze:** Wunsch des Betreibers vom 16.11.2026; „einfach nur Verbote“ waren als schlecht
  wahrgenommen worden.
- **Was nur im Code steht:** Ein Blindtest fand den Ablageort einer Sperrliste nur im Code.
- **Dasselbe Wort für dieselbe Sache:** Ein Blindtest fand für denselben Begriff zwei Wörter – eines auf der
  Kommandozeile, eines im Code – und wusste nicht, ob beide dasselbe meinen.
- **Keine Vorgabe für Adressaten, Veröffentlichung, Löschen und Zugangsdaten:** externes Gutachten vom 30.10.2026.
- **Blindtest:** Wer einen Text schreibt, sieht die eigenen Lücken nicht. Eine neue Sitzung derselben KI ist der
  schwächere Ersatz, weil ihr Modell dieselben Lücken übersehen kann.

## Herkunft

Das Format entstand im September und Oktober 2026 im Regelwerk einer KI-Agentur, die mit mehreren KI-Instanzen eine
Website baute und betrieb; die Zitate stammen aus deren Auftragsform (Fassung 1.0). Anwendung 2, der Klartext in
Block B, die Schwelle für Block B und der Blindtest sind Entscheidungen des Betreibers, der diesen Ordner herausgibt,
vom 28. bis 30. Oktober 2026.

Die Felder eines Auftrags in der Agentur-Fassung. Zitat:
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

Gültig ist die Vorlage. Sie weicht so ab: VON und AN tragen die Kennung der Instanz; das Datum steht als JJJJ-MM-TT mit
Zeitzone und dem Vermerk „gemessen“ oder „Kontextangabe, nicht gemessen“; die RUN-ID besteht aus dem Kürzel des
Absenders und einer fortlaufenden Nummer; LEITPLANKEN dürfen ausgeschrieben sein.

Fassungen:

- **1.0** (28.10.2026) war Teil des Regelwerks des Betreibers und verwies hinein.
- **1.1** (30.10.2026) ist die erste, die ohne das übrige Regelwerk vollständig lesbar ist.
- **1.2** (30.10.2026) ergänzte nach einem externen Gutachten vier Regeln für den Empfänger.
- **1.3** (17.11.2026) macht das Format zum reinen Werkzeug. Was der Empfänger bei Lücken, Widersprüchen und doppelten
  Aufträgen tut, wann ein Text ins Format muss und dass Regeln vor dem Format gelten, steht nicht mehr hier, sondern im
  Regelwerk, nach dem der Empfänger arbeitet. Neu sind zwei Punkte der Schreibweise: „Bedingung vor Handlung“ (nach
  ASD-STE100, Simplified Technical English) und „erst das Richtige, dann die Grenze“. Neu sind außerdem die Zeile
  „Fragen“ in der Quittung und der Hinweis in PARAMETER, wo das Format steht; ESKALATION gilt nur noch für Blocker.
  „siehe Kopf“ entfällt. Jede Angabe steht nur noch an einer Stelle. Fassung 1.2 bleibt in der Historie des Repos
  abrufbar.
