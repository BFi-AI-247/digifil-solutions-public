# Blindtest von TECH-STACK.md

Verfahren nach dem Zwei-Kanal-Format, Fassung 1.3, README Schritt 5: Eine KI, die weder die Datei noch das Projekt
kennt, bekommt nur Block A und eine erfundene Probeaufgabe. Sie beschreibt, was sie nach der Anleitung tun würde, und
nennt jede Stelle, an der sie raten musste. Echte Lücken werden in Block A behoben; dann folgt eine neue Runde mit einer
anderen Probeaufgabe, bis nur noch Kleinigkeiten bleiben.

Prüfende KI: je Runde eine neue Instanz desselben Modells wie die schreibende KI, ohne Verlauf und ohne Zugriff auf
andere Dateien. Das ist im Sinne des Formats eine „neue Sitzung derselben KI“, der schwächere Ersatz für eine fremde KI,
weil dasselbe Modell dieselben Lücken übersehen kann.

| Runde | Datum | Probeaufgabe (Kurzform) | Echte Lücken | Kleinigkeiten | Datei |
|---|---|---|---|---|---|
| 1 | 2026-11-18 | Werkzeug „Muster“: Ordner, Port, Laufzeit, Start, Manifest, Token-Ablage | 6 (5 Ratestellen, Zeilenenden) | 6 | runde1.md |
| 2 | 2026-11-18 | Werkzeug „Zaehler“: Datenbank, Austauschdatei, täglicher Lauf, Protokoll, Schutz, Beenden im Import | 3 | 9 | runde2.md |
| 3 | 2026-11-18 | Werkzeug „Notiz“: Oberfläche, Ablage als Dateien, Rückmeldungen, Installation und Updates ohne Steuerpult, Tests ohne Netz | 3 | 6 | runde3.md |
| 4 | 2026-11-18 | Werkzeug „Kurs“: SQL Server lesend, lokale Ablage, Befehl ohne Oberfläche, Eintrag in ein vorhandenes Steuerpult | 1 | 9 | runde4.md |
| 5 | 2026-11-18 | Werkzeug „Etikett“: ohne Steuerpult und ohne GitHub, Austauschdatei mit neuem Feld, Beenden, Rückmeldungen | 9 (5 davon im offenen Bereich ohne GitHub) | 22 | runde5.md |
| 6 | 2026-11-18 | Werkzeug „Lager“: langer Import, Abbruch, Beenden während eines Auftrags, täglicher Lauf, Protokolle, Issues, privates Repo ohne Steuerpult | 12 | 36 | runde6.md |
| 7 | 2026-11-18 | wie Runde 6 (Bestätigung) | 6 | 27 | runde7.md |
| 8 | 2026-11-18 | Werkzeug „Bericht“: Austauschdateien lesen, neue Version beim Lieferer, Tabelle für den Menschen, Steuerpult vorhanden – Prüflesung mit Vorwissen durch ein anderes Modell (GLM 5.3), kein Blindtest | 2 | 9 | runde8.md |

Beobachtung nach Runde 7: Jede neue Probeaufgabe berührt Bereiche, die vorher keine berührt hat, und findet dort neue
echte Lücken (6 · 3 · 3 · 1 · 9 · 12). Die Wiederholung derselben Aufgabe in Runde 7 fand keine der in Runde 6
behobenen Lücken wieder, aber 6 neue, tiefer liegende. Das Abbruchkriterium des Formats („nur noch Kleinigkeiten“)
ist bei dieser Breite bisher nicht erreicht.

Nach Runde 8: Runde 8 lief mit einem anderen Modell und war keine Blindprüfung (die Prüferin kannte die ganze Datei,
Entscheid des Betreibers). Ihre Zahlen sind mit den Runden 1–7 nicht vergleichbar.

Blindtest der README (tech-stack/README.md): einmal, auf Wort des Betreibers – readme-runde1.md (2026-11-18; 3 echte
Lücken, 15 Kleinigkeiten, alle echten Lücken behoben).
