Stand: 2026-10-30a

# Zwei-Kanal-Format

*AI-to-AI-and-Human-Messages: ein Text, zwei Leser – Block A für die KI, die handelt, Block B für den Menschen.*

> Verweise auf `../kanon_01_single_agent/`, `../kanon_02_multi_agent/`, `../arbeit/` und `../quelle/` führen in den nicht öffentlichen Teil des Kanons.

Ein Text, nach dem eine KI (oder ein Mensch) handeln soll, besteht aus zwei getrennten Blöcken:

- **Block A – Ausführungskanal:** alles, was zum Handeln nötig ist, in festen Feldern.
- **Block B – Mensch-Kanal:** Hintergrund, Motivation, Einordnung. Nie eine Anweisung.

Das Format gilt für zwei Arten von Texten: **Aufträge** (eine Nachricht von einem Agenten an einen anderen, Anwendung 1)
und **Anleitungen** (eine README, nach der eine KI etwas einrichtet, Anwendung 2). Der Grundsatz ist derselbe, die Felder
sind verschieden.

## Grundsatz (beide Anwendungen)

**Trennregel.** Quelle wörtlich:
> „**Block B darf niemals Informationen enthalten, die für die Ausführung notwendig sind — alles Ausführungsrelevante gehört zwingend in Block A.**“
> (`../quelle/kanon-export/v3/tools/auftragsformat.md`, Abschnitt „Block B — Mensch-Kanal (Trennregel)“)

**Zwei Prüffragen vor dem Abschicken.** Quelle wörtlich:
> „1. „Ist dieser Kontext-Satz eigentlich eine Anweisung? → nach A verschieben."
> 2. „Könnte der Empfänger den Auftrag korrekt ausführen, wenn Block B weg wäre?" — Nein → Inhalt fehlt in A.“
> (ebenda)

**Kanon-Vorrang.** Quelle wörtlich:
> „Das Format SCHICHTET die Kommunikation zusätzlich; es suspendiert, ersetzt oder lockert KEINE Regel. Widerspricht ein Block-A-Feld dem Kanon, ist das Feld falsch, nicht der Kanon.“
> (ebenda, Abschnitt „Mechanik-Regeln“)

**Warum überhaupt.** Quelle wörtlich:
> „Mehrdeutigkeit entsteht bei Wirkung, nicht bei Wortzahl; das Format schichtet nur, wo Fehlinterpretation Schaden anrichten könnte (Doppelausführung, Format-Drift).“
> (ebenda, Abschnitt „Grundsatz“)

**Neu für beide (28.10.2026): Block B ist Klartext.** Block B muss ein Mensch ohne Fachwissen verstehen: keine Funktions-,
Datei- oder Feldnamen, keine Abkürzungen ohne Erklärung, ganze Sätze. Prüffrage: *Weiß ein Leser nach Block B, wozu das
Ganze gut ist und was er selbst tun muss – ohne Block A gelesen zu haben?*
Anlass: Der Betreiber fand Block B der Basis-Anleitung „Kauderwelsch“ – eine Tabelle aus Regelkürzeln und Funktionsnamen.

---

## Anwendung 1: Aufträge zwischen Agenten

Übernommen aus `../quelle/kanon-export/Konzept-2_20261002/ZweiKanal_Kanon.md` (Export-Fassung 1.0) und
`../quelle/kanon-export/v3/tools/auftragsformat.md`; im Produkt als Regel T6 in `../kanon_02_multi_agent/regeln-team.md`, Vorlage in
`../kanon_02_multi_agent/vorlagen.md`, Prüfung im Code mit `auftrag_pruefen` (`../kanon_02_multi_agent/kanon_team.py`).

**Wann.** Quelle wörtlich (`ZweiKanal_Kanon.md`, Schritt 1):
> „Ein Auftrag darf im Klartext bleiben, wenn ALLE drei Bedingungen erfüllt sind: keine Bestands-/Job-Berührung · keine Leitplanken-Relevanz · ein Empfänger, ein Strang. Quittierungen sind KEINE Aufträge — sie bleiben immer im kurzen Format.“

**Felder von Block A.** Quelle wörtlich (`auftragsformat.md`, Abschnitt „Block A — Ausführungskanal (Felder)“):
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

**Was nicht in Block B darf.** Quelle wörtlich (`auftragsformat.md`):
> „Block B darf enthalten: Hintergrund, Motivation, Einordnung, Betreiber-Zitate. Block B darf NICHT: Fristen, Datei-Pfade, Schwellen, Freigaben, Namen/Beteiligte, Verweise auf frühere Punkte.“

**Quittung.** Quelle wörtlich (`auftragsformat.md`, „Mechanik-Regeln“):
> „Der Empfänger zitiert die Auftrags-Nummer am Anfang seiner Quittierung — nur mit Rückbezug kann abgleichen, ob der Auftrag schon bearbeitet wurde (auch über einen Instanz-Wechsel hinweg).“

Im Postfach-Kopf (claude_1/post/README.md) steht die RUN-ID als Kopffeld und „Antwort auf“ nennt die Datei; das erfüllt die Regel.
Ebenso ersetzt das Kopffeld „Datum/Uhrzeit (gemessen)“ das Feld DATUM in Block A – ein Datum steht genau einmal (Kanon 01 B34).

**Substanz auslagern.** Quelle wörtlich (ebenda):
> „Nachrichten-Kerne bleiben kurz; Substanz (Konzepte, Begründungen, Rohfassungen) wird als eigene Datei in der Wissens-Ablage hinterlegt und mit Lese-Auslöser referenziert (Zweck + entscheidungsrelevante Abschnitte).“

Schwelle (seit 2026-10-30, nach Review R036): Block B hat höchstens drei Absätze. Was länger wird, ist Substanz und geht in
eine eigene Datei mit Lese-Auslöser in Block A (Zweck und was der Leser dort entscheidet).

---

## Anwendung 2: Anleitungen (README) – Erweiterung vom 28.10.2026

Nicht aus der Quelle, sondern neu: Die Quelle kennt das Format nur für Aufträge. Anlass: Der Betreiber las die erste
Basis-Anleitung und fand sie nichtssagend („Tw. drei Wort Anweisungen, die für mich viel Interpretationspielraum lassen“),
dazu: „welcher Mensch liest denn noch Readme. Das liest doch auch alles KI. Für mich ein Fall für das Zwei-Kanal-Verfahren.“

**Was anders ist als beim Auftrag.** Eine README ist kein einmaliger Auftrag, sondern liegt dauerhaft da und wird von
vielen gelesen. Deshalb entfallen VON, AN, DATUM und RUN-ID; an ihre Stelle tritt die Version im Titel. Aus AUFTRAG wird
ZWECK, aus PARAMETER werden VORAUSSETZUNG und DATEIEN, aus LEITPLANKEN wird NICHT TUN, aus REQUIRE-ACK wird LIEFERUNG.
FAIL-MODE bleibt und enthält die Eskalation.

**Felder von Block A** (Reihenfolge fest; Vorlage: `readme-vorlage.md`):

| Feld | Inhalt | Pflicht |
|---|---|---|
| ZWECK | Was am Ende steht, in ein bis drei Sätzen; prüfbar formuliert | ja |
| GILT FÜR / GILT NICHT | Wofür die Anleitung gedacht ist; was nicht, mit Verweis, wo es stattdessen steht | ja |
| VORAUSSETZUNG | Was vorher da sein muss (Sprache, Version, Zugriff, Dienste) | ja |
| DATEIEN | Jede Datei des Ordners mit einem Halbsatz, wozu sie dient | ja |
| BEGRIFFE | Jeder Begriff, den die Schritte verwenden und der mehr als eine Deutung zulässt | wenn nötig |
| VERHALTEN | Wie das Werkzeug sich heute verhält, als prüfbare Aussagen – für jede KI, die Fragen dazu beantwortet oder Änderungen plant. Anlass: Entwurf der Blog-README (28.10.2026) – der Issue-Assistent soll „so ist es heute“ aus der README sagen können | bei Produkten |
| SCHRITTE | Nummeriert, in fester Reihenfolge; jeder mit *Ergebnis:* – einem Befehl oder einer Beobachtung, die zeigt, dass der Schritt gelang. Wo etwas auszufüllen ist: Tabelle Platzhalter → einsetzen, mit Vorgabe, wenn der Auftrag nichts sagt | ja |
| PRÜFUNG | Der eine Befehl oder Test, der am Ende alles bestätigt | ja |
| FAIL-MODE | Was tun, wenn ein Schritt nicht geht; was tun, wenn nur eine Angabe fehlt | ja |
| NICHT TUN | Was ausdrücklich verboten ist | ja |
| LIEFERUNG | Was die einrichtende KI am Ende zurückmeldet – immer mit „jede Stelle, an der diese Anleitung nicht reichte (mit Zitat)“ | ja |
| REFERENZ | Wo die Einzelheiten stehen (Regeln, Herkunft) | wenn nötig |

**Schreibregeln für Block A.**
- Ganze Sätze mit Verb, kein Stichwort-Telegramm. Anlass: „drei Wort Anweisungen“ (Betreiber, 28.10.2026).
- Jeder Schritt sagt, *welche* Datei, *welche* Stelle, *welcher* Wert. „Anpassen“ ohne Ziel ist kein Schritt.
- Lässt ein Platzhalter Raum, steht die Vorgabe daneben („sonst …“) und der Satz „in der Lieferung als offen nennen“.
- Was nur im Code steht (Dateiname, Ablageort, Rollenwort), steht auch in Block A. Anlass: Blindtest 3 fand den Ablageort
  der Sperrliste nur im Code.
- Dieselbe Sache hat überall dasselbe Wort. Anlass: Blindtest 3 – `betreiber` auf der Kommandozeile, `mensch` im Code.

**Schreibregeln für Block B.** Klartext (siehe Grundsatz). Gut bewährt: ein echter Vorfall als Einstieg, dann was das Ding
tut, dann was der Mensch im Alltag selbst tut. Regellisten nach Themen, je mit „warum“ und ob das Programm es prüft oder es
nur eine Bitte an das Modell ist.

**Blindtest – die Prüfung für Block A.** Eine frische KI ohne Vorwissen bekommt **nur Block A** und einen kleinen,
erfundenen Auftrag („richte damit einen Vereins-Assistenten ein“). Sie arbeitet die Schritte ab und liefert, was LIEFERUNG
verlangt – vor allem die Liste der Stellen, an denen sie raten musste. Jede Stelle wird in Block A (oder im Code) behoben;
dann folgt der nächste Blindtest mit einem anderen erfundenen Auftrag. Fertig ist Block A, wenn ein Blindtest nur noch
Kleinigkeiten findet und keine echte Lücke.
Belegt an der Anleitung von Kanon 01 Single Agent (damals „Basis“, `../kanon_01_single_agent/README.md`, Oktober 2026): Blindtest 1 fand 22 Stellen, Blindtest 2 fand 18 kleinere
und einen Fehler im Code, Blindtest 3 fand 11, darunter eine echte Lücke (Kontonummern wurden nicht gesperrt). Einzelheiten:
`../arbeit/anschluss.md`.

---

## Herkunft

- `../quelle/kanon-export/Konzept-2_20261002/ZweiKanal_Kanon.md` – Verfahrens-Datei, Export-Fassung 1.0
- `../quelle/kanon-export/v3/tools/auftragsformat.md` – Skillbook, Pilot-Verankerung 27.09.2026
- `../quelle/kanon-export/v4/framework-kern.md` – Kurzfassung im Kern
- Anwendung 2, Klartext-Regel für Block B und Blindtest: Entscheidungen des Betreibers vom 28.10.2026
