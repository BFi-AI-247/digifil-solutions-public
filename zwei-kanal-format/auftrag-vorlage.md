# Vorlage: Auftrag im Zwei-Kanal-Format 1.1 (Anwendung 1)

<!-- Kopieren, alle Platzhalter in spitzen Klammern ersetzen, diesen Kommentar löschen. Alle zehn Felder von Block A sind Pflicht („keine“ ist ein
     Wert). Block A muss allein genügen; was nicht in Block B darf, steht in konzept.md (Anwendung 1). Erklärung der Felder:
     konzept.md, Anwendung 1. Beispiel: beispiel-auftrag.md. Trägt der Transportweg (die Kopfzeilen einer als Datei abgelegten
     Nachricht) schon ein gemessenes Datum und die RUN-ID, dürfen DATUM und RUN-ID in Block A „siehe Kopf“ lauten.
     Die Quittung unten ist nicht Teil des Auftrags; der Empfänger antwortet in dieser Form. -->

```text
BLOCK A
VON: <Kennung des Absenders, z. B. Redaktion_2 – Rolle und Nummer>
AN: <Kennung des Empfängers, z. B. Bau_1>
DATUM: <JJJJ-MM-TT, HH:MM Zeitzone> (gemessen | Kontextangabe, nicht gemessen)
RUN-ID: <Kürzel des Absenders>-<fortlaufende Nummer>
AUFTRAG: <Die Handlung in einem Satz.>
PARAMETER:
- <Datei, Pfad, Wert, Frist – alles, was der Empfänger zum Ausführen braucht, je Zeile ein Punkt.>
- <…>
LEITPLANKEN: <Begrenzungen, die der Empfänger kennt, oder ausgeschrieben – oder „keine“. Nie leer lassen.>
FAIL-MODE: <Was der Empfänger tut, wenn ein Teil nicht geht: abbrechen, melden, was genau; nicht improvisieren.>
REQUIRE-ACK: <Was zurückkommt – mindestens RUN-ID und Stand der Ausführung; dazu alles, was der Absender prüfen will.>
ESKALATION: <Wann und an wen, wenn der Empfänger blockiert ist.>

BLOCK B
<Hintergrund, Motivation, Einordnung – höchstens drei Absätze, in ganzen Sätzen, für einen Menschen ohne Fachwissen.
 Nichts aus der Liste „Was nicht in Block B darf“ (konzept.md). Wird es länger: eigene Datei, die Block A unter PARAMETER
 mit Zweck nennt.>
```

## Quittung (formlos, kein Auftrag – Antwort des Empfängers, nicht mitschicken)

```text
<RUN-ID> · Quittung
Empfangen: <JJJJ-MM-TT, HH:MM Zeitzone> (gemessen)
Stand: <erledigt | teilweise | nicht begonnen> – <ein Satz>
Abweichungen: <keine | welche Regel oder welcher Umstand welchem Feld entgegenstand>
Beleg: <Datei, Commit, Protokollzeile>
```
