# Blindtest der README – 2026-11-18 (einziger, auf Wort des Betreibers)

- Stand der Datei: tech-stack/README.md wie in Commit 279b6c4 (66 Zeilen).
- Prüfende KI: neue Instanz, nur die README; die Dateien, auf die sie verweist, hatte sie nicht.
- Probeaufgabe (wörtlich): „Ein Mensch gibt dir nur diese README eines Ordners und sagt: „Ich will mir ein kleines Werkzeug für meinen Rechner bauen lassen, das Termine aus einer Datei liest und anzeigt. Was gebe ich der bauenden KI, was gebe ich ihr nicht, und was tue ich, wenn mir später auffällt, dass eine Regel nicht passt? Und was liegt in diesem Ordner überhaupt?““
- Ergebnis: Die Prüferin beantwortete, was im Ordner liegt und wem welche Datei gegeben wird; wohin Befunde gehen,
  nur teilweise (PRÜFUNG der README: „teilweise“). 18 Ratestellen (3 echte Lücken, 15 Kleinigkeiten), 6 Widersprüche.
  Alle echten Lücken und Widersprüche sind behoben. Eine zweite Runde gibt es nicht (Betreiber: „nur einen
  Blindtest“).

| Nr. | Stelle (gekürzt) | Was unklar war | Einstufung (Prüferin) | Behebung |
|---|---|---|---|---|
| R1 | Schritt 3, NICHT TUN, Block B | Wer die pflegende Rolle ist und auf welchem Weg man meldet | echte Lücke | BEGRIFFE „pflegende Rolle“ (Rollendatei des Projekts, sonst der verantwortliche Mensch); Schritt 3: Mensch im Chat, KI ins Postfach |
| R2 | Schritt 3 gegen Block B | Wohin ein Fehler im Werkzeug geht und wohin eine Regel, die nicht passt | echte Lücke | Schritt 3 und Block B trennen: Werkzeugfehler an die bauende KI oder als Issue, Regeln an die pflegende Rolle |
| R3 | Schritt 3 | Was bis zur neuen Fassung gilt | echte Lücke | Schritt 3: nach der geltenden Fassung bauen, Abweichung in ANNAHMEN.md des Werkzeugs |
| R4 | Schritt 3, Ergebnis | „Ort und Wortlaut“ wovon | Kleinigkeit | Schritt 3: Nummer der Vorgabe und was geschah |
| R5 | Schritt 1, Block B | Form des Auftrags, Beispieldatei | Kleinigkeit | unverändert: Sache des Auftrags |
| R6 | NICHT TUN | Was außer BELEGE.md nicht weitergegeben wird | Kleinigkeit | NICHT TUN: nie Zugangsschlüssel oder Firmendaten |
| R7 | NICHT TUN | Geht die README auch an die bauende KI | Kleinigkeit | NICHT TUN: die bauende KI bekommt TECH-STACK.md; die README ersetzt sie nicht |
| R8 | DATEIEN, Schritt 1 | Geht blindtest/ an die bauende KI | Kleinigkeit | Schritt 1: „sonst nichts aus diesem Ordner“ |
| R9 | GILT FÜR | Was „lokal“ heißt | Kleinigkeit | unverändert: steht in TECH-STACK.md (GILT FÜR) |
| R10 | SCHRITTE | Reihenfolge, obwohl sich 1 und 2 ausschließen | Kleinigkeit | Überschrift: Schritt 1 oder 2 je nach Fall, Schritt 3 bei Bedarf |
| R11 | Block B | Statusmeldung und Proben nicht in Block A | Kleinigkeit | unverändert: stehen in TECH-STACK.md |
| R12 | Schritt 3 gegen Block B | „Zielrechner“ und „eigener Rechner“ | Kleinigkeit | unverändert |
| R13 | VORAUSSETZUNG | Wer BELEGE.md lesen darf | Kleinigkeit | VORAUSSETZUNG: nur die pflegende Rolle; fehlt in einer öffentlichen Fassung |
| R14 | Überschrift Block A | „einrichtende KI“ | Kleinigkeit | „für die lesende KI“ |
| R15 | LIEFERUNG | Lieferung eines Menschen | Kleinigkeit | unverändert |
| R16 | Schritt 3 | Wer entscheidet | Kleinigkeit | Schritt 3: die pflegende Rolle antwortet |
| R17 | FAIL-MODE | Welcher Weg für Lücken | Kleinigkeit | unverändert: FAIL-MODE in TECH-STACK.md; Schritt 3 verweist darauf |
| R18 | DATEIEN | README fehlt in der Liste | Kleinigkeit | DATEIEN nennt README.md |

Widersprüche:
1. Block A „Auftrag an die einrichtende KI“ gegen LIEFERUNG („legt nichts an“) → Überschrift „für die lesende KI“.
2. „in dieser Reihenfolge“, obwohl sich Schritt 1 und 2 ausschließen → Überschrift der SCHRITTE.
3. Schritt 3 „nach der Entscheidung“ gegen „neue Fassung“ immer → Ergebnis: neue Fassung oder Ablehnung mit Grund;
   Block B: die Rolle entscheidet.
4. Schritt 3 (nur Regeln) gegen Block B („Passt etwas nicht“) → beide trennen Werkzeugfehler und Regeln.
5. NICHT TUN „nicht nach diesem Text allein“ gegen Schritt 1 → NICHT TUN: die README ersetzt die Bauvorgabe nicht.
6. VORAUSSETZUNG „Lesezugriff“ gegen BELEGE.md „nicht öffentlich“ → VORAUSSETZUNG nennt die Ausnahme.
