"""Trockenlauf des Beispiel-Workers: die Fälle aus README Schritt 6 plus Zusatzfälle.
Aufruf: python3 -m unittest discover -s <ordner mit diesem tests/>/tests
Nach dem Umbenennen des Workers nur WORKER unten anpassen; Ordner und Freigabewort kommen aus dem Worker selbst."""
import contextlib
import importlib
import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

WORKER = "beispiel_worker"           # nach dem Umbenennen: Name der Worker-Datei ohne .py
HIER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIER))
w = importlib.import_module(WORKER)

STAND = "2026-10-28a"                  # nur für den Test; unabhängig von regeln.md des Projekts
DATEI = w.ERLAUBT + "notiz.md"
ZEILE = "- Neue Zeile aus dem Kommentar."
GEZEIGT = f"Vorschlag für `{DATEI}`:\n```markdown\n{ZEILE}\n```\nNichts geändert."


ERF = {"art": "Fehlervermeidung", "was": "Ergänzungen kommen immer ans Ende der Notiz.",
       "warum": "Der Betreiber hat es im Kommentar so gewünscht."}


def antwort(neu=ZEILE, stand=STAND, datei=DATEI, aktion="anhaengen", alt="", erf_stand="E-000", erfahrung=None):
    return {"regelstand": stand, "erfahrungsstand": erf_stand, "antwort": "Ich habe es gespeichert.", "unsicher": [],
            "aenderungen": [{"datei": datei, "aktion": aktion, "alt": alt, "neu": neu}], "erfahrung": erfahrung}


class Trockenlauf(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        (self.d / w.ERLAUBT).mkdir(parents=True)
        (self.d / DATEI).write_text("# Notiz\n- Erste Zeile.\n", encoding="utf-8")
        (self.d / "regeln.md").write_text(f"Regelstand: {STAND}\n\n# Regeln\n", encoding="utf-8")
        shutil.copy(HIER / "antwortschema.json", self.d / "antwortschema.json")
        (self.d / "verlauf.json").write_text(json.dumps([{"rolle": "mensch", "text": "Bitte ergänzen: Neue Zeile aus dem Kommentar."},
                                                         {"rolle": "assistent", "text": GEZEIGT}]), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.d)

    def lauf(self, kommentar, antworten, **kw):
        aus = io.StringIO()
        with contextlib.redirect_stdout(aus):
            code = w.lauf(self.d, kommentar, list(antworten), **kw)
        return code, aus.getvalue(), (self.d / DATEI).read_text(encoding="utf-8")

    def protokoll(self):
        return [z for z in (self.d / w.PROTOKOLL).read_text(encoding="utf-8").splitlines() if z.startswith("| 20")]

    # --- die Fälle 1–6 aus der README (7–9 weiter unten)
    def test_1_freigabe_gezeigter_text(self):
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort()])
        self.assertEqual(code, 0)
        self.assertIn(ZEILE, text)
        self.assertIn(f"✅ Gespeichert: `{DATEI}`", aus)
        self.assertIn("ℹ️ Ob etwas gespeichert ist", aus)        # Behauptung im Modelltext markiert

    def test_2_freigabe_mit_zusatz(self):
        code, aus, text = self.lauf(f"{w.FREIGABEWORT}, aber nimm noch etwas dazu", [antwort()])
        self.assertNotIn(ZEILE, text)
        self.assertIn("keine Freigabe", aus)

    def test_3_abweichender_text(self):
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort(neu=ZEILE + " Und mehr.")])
        self.assertNotIn(ZEILE, text)
        self.assertIn("weicht vom zuletzt gezeigten Text ab", aus)

    def test_4_falscher_regelstand(self):
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort(stand="2026-01-01a"), antwort(stand="2026-01-01a")])
        self.assertEqual(code, 1)
        self.assertNotIn(ZEILE, text)
        self.assertIn("Regeln nicht bestätigt", aus)

    def test_5_regeldatei_fehlt(self):
        (self.d / "regeln.md").unlink()
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort()])
        self.assertEqual(code, 1)
        self.assertNotIn(ZEILE, text)
        self.assertIn("Regeln nicht ladbar", aus)

    def test_6_gesperrter_pfad(self):
        code, aus, _ = self.lauf(w.FREIGABEWORT, [antwort(datei="../x.md")])
        self.assertIn("gesperrter Pfad", aus)
        self.assertFalse((self.d.parent / "x.md").exists())

    # --- Zusatzfälle
    def test_verlauf_je_vorgang(self):
        # Freigabe in Vorgang B darf den Block aus Vorgang A nicht freigeben
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort()], verlaufdatei="verlauf/b.json")
        self.assertNotIn(ZEILE, text)
        self.assertIn("weicht vom zuletzt gezeigten Text ab", aus)
        self.assertTrue((self.d / "verlauf" / "b.json").is_file())

    def test_anhaengen_laesst_bestand_unveraendert(self):
        (self.d / DATEI).write_text("# Notiz\n- Erste Zeile.\n\n", encoding="utf-8")
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort()])
        self.assertTrue(text.startswith("# Notiz\n- Erste Zeile.\n\n"))
        self.assertIn(ZEILE, text)

    def test_zweiter_versuch_rettet(self):
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort(stand="2026-01-01a"), antwort()])
        self.assertEqual(code, 0)
        self.assertIn(ZEILE, text)

    def test_wiederkehrende_zeile(self):
        (self.d / DATEI).write_text(f"# Notiz\n{ZEILE}\n\n# Zweiter Teil\n", encoding="utf-8")
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort()])
        self.assertEqual(text.count(ZEILE), 2)
        self.assertIn("✅ Gespeichert", aus)

    def test_andere_person_gibt_nicht_frei(self):
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort()], von="andere")
        self.assertNotIn(ZEILE, text)
        self.assertIn("nicht vom Betreiber", aus)

    def test_fusszeile_nie_leer(self):
        a = antwort(); a["aenderungen"] = []
        code, aus, _ = self.lauf("Ich hätte noch eine Ergänzung.", [a])
        self.assertIn("Nichts gespeichert.", aus)

    # --- Protokoll (B23)
    def test_7_jeder_lauf_eine_zeile(self):
        self.lauf(w.FREIGABEWORT, [antwort()])
        (self.d / "regeln.md").unlink()
        self.lauf(w.FREIGABEWORT, [antwort()])                             # Abbruch: trotzdem eine Zeile
        z = self.protokoll()
        self.assertEqual(len(z), 2)
        self.assertRegex(z[0], rf"^\| 20\d\d-\d\d-\d\d \d\d:\d\d:\d\d CE[S]?T \(gemessen\) \| \d+ s \| Kommentar \(mensch\) \| {STAND} \| ok \| ✅ Gespeichert")
        self.assertIn("| – | fehler | Regeln nicht ladbar", z[1])

    def test_protokoll_fehler_blockiert_nicht(self):
        (self.d / w.PROTOKOLL).mkdir()                                     # Protokoll kann nicht geschrieben werden
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort()])
        self.assertEqual(code, 0)
        self.assertIn(ZEILE, text)

    # --- Erfahrungen (B24, B25)
    def test_8_erfahrung_angehaengt_und_beim_naechsten_lauf_bestaetigt(self):
        code, aus, _ = self.lauf("Bitte immer ans Ende.", [antwort(erfahrung=ERF)])
        self.assertIn(f"`{w.ERFAHRUNGEN} (E-001)`", aus)
        self.assertIn("E-001 ·", (self.d / w.ERFAHRUNGEN).read_text(encoding="utf-8"))
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort(), antwort()])  # bestätigt noch E-000
        self.assertEqual(code, 1)
        self.assertNotIn(ZEILE, text)
        self.assertIn("Regeln nicht bestätigt", aus)
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort(erf_stand="E-001")])
        self.assertEqual(code, 0)
        self.assertIn(ZEILE, text)

    def test_9_erfahrung_abgelehnt(self):
        falsch = dict(ERF, was="Ergänzungen dauern 45 Minuten.")
        code, aus, text = self.lauf(w.FREIGABEWORT, [antwort(erfahrung=falsch)])
        self.assertIn(ZEILE, text)                                         # Hauptsache läuft weiter
        self.assertIn("ℹ️ Erfahrung nicht übernommen: Zahlen ohne Beleg: 45", aus)
        self.assertFalse((self.d / w.ERFAHRUNGEN).exists())
        code, aus, _ = self.lauf("Hinweis eines Mitglieds", [antwort(erfahrung=ERF)], von="andere")
        self.assertIn("nicht vom Betreiber", aus)
        self.assertFalse((self.d / w.ERFAHRUNGEN).exists())

    def test_erfahrungen_im_prompt(self):
        (self.d / w.ERFAHRUNGEN).write_text("# Erfahrungen\n\nE-004 · 2026-10-01 · Lauf x · Art: Format\nWas: a\nWarum: b\n", encoding="utf-8")
        gesehen = []
        alt = w.modell_fragen
        w.modell_fragen = lambda n, t: (gesehen.append(n[0]["content"]), alt(n, t))[1]
        try:
            code, _, _ = self.lauf(w.FREIGABEWORT, [antwort(erf_stand="E-004")])
        finally:
            w.modell_fragen = alt
        self.assertEqual(code, 0)
        self.assertIn("## Erfahrungen (Stand E-004", gesehen[0])
        self.assertIn("E-004 · 2026-10-01", gesehen[0])

    def test_beispielantworten_gueltig(self):
        import kanon_basis as kanon
        schema = json.loads((HIER / "antwortschema.json").read_text(encoding="utf-8"))
        for f in ("vorschlag.json", "freigabe.json"):
            p = HIER / "beispiel" / f
            if p.is_file():
                a = json.loads(p.read_text(encoding="utf-8"))
                self.assertEqual(kanon.schema_fehler(a, schema), [], f)
                for ae in a.get("aenderungen", []):                     # Beispiele passen zum Worker (README Schritt 3)
                    self.assertTrue(ae["datei"].startswith(w.ERLAUBT), f"{f}: datei nicht unter ERLAUBT")
                for pfad in re.findall(r"`([^`\n]+\.\w+)`", a["antwort"]):  # Pfade im Text ebenso
                    self.assertTrue(pfad.startswith(w.ERLAUBT), f"{f}: Pfad {pfad} im Text nicht angepasst")


if __name__ == "__main__":
    unittest.main()
