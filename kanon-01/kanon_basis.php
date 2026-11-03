<?php
// Kanon 01 Single Agent – Prüfbausteine für KI-Aufrufe in PHP. Eigene Auswahl für Endpunkte (kein vollständiges Gegenstück zu kanon_basis.py):
// Regelstand, Pflichtfelder, Marker, Zahlen, Sperrliste, Behauptungen, bekannte IDs, Zeit, Laufprotokoll, Beleg.
// Erfahrungen (B24, B25) gibt es nur in Python.
// Herkunft: Kanon 01 Single Agent (kanon/kanon_01_single_agent, Regeln in regeln.md).
// Grundsatz: Was nur im Prompt steht, lenkt. Was hier geprüft wird, gilt.
// In Projekten als Kopie einbinden und NICHT dort ändern. Änderungen nur an der Quelle, dann neu kopieren.
declare(strict_types=1);

if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }

const KANON_BASIS_VERSION = '1.1.2';

/** Vergleichsform: geschützte Leerzeichen zu Leerzeichen, Leerraum zusammengefasst. */
function kanon_norm(string $t): string {
    if (class_exists('Normalizer')) $t = \Normalizer::normalize($t, \Normalizer::FORM_C) ?: $t;
    $t = str_replace(["\u{00A0}", "\r\n"], [' ', "\n"], $t);
    return trim((string)preg_replace('/\s+/u', ' ', $t));
}

/** B1: Regelstand aus einem Regeltext lesen („Regelstand: 2026-10-27a“ oder Kanon-Kopf „STATUS: … · Regelstand: kanon_01 3.1 (…)“). null = keine Zeile. */
function kanon_regelstand(string $regeln): ?string {
    return preg_match('/^(?:STATUS:[^\n]*?· )?Regelstand:\s*([^\n(·]+?)\s*(?:\(|·|$)/mu', $regeln, $m) ? $m[1] : null;
}

/** B1: Hat das Modell den Regelstand wörtlich bestätigt? */
function kanon_regelstand_ok($antwort, string $stand, string $feld = 'regelstand'): bool {
    return is_array($antwort) && trim((string)($antwort[$feld] ?? '')) === $stand;
}

/** B16: Pflichtfelder und Typen prüfen. $felder = ['name' => 'string'|'array'|'bool'|'int'|'string?' ...]. Leere Liste = gültig. */
function kanon_pflichtfelder($antwort, array $felder): array {
    if (!is_array($antwort)) return ['Antwort ist kein JSON-Objekt'];
    $fehler = [];
    foreach ($felder as $k => $typ) {
        $optional = str_ends_with($typ, '?'); $typ = rtrim($typ, '?');
        if (!array_key_exists($k, $antwort)) { if (!$optional) $fehler[] = "Pflichtfeld „{$k}“ fehlt"; continue; }
        $v = $antwort[$k];
        $ok = match ($typ) { 'string' => is_string($v), 'array' => is_array($v), 'bool' => is_bool($v), 'int' => is_int($v), default => true };
        if (!$ok) $fehler[] = "Feld „{$k}“ hat den falschen Typ";
    }
    return $fehler;
}

/** B6: offene Vorschlags- oder Unsicher-Marker im Text. */
function kanon_marker_offen(string $text, string $muster = '⟦\s*Vorschlag'): array {
    preg_match_all('/' . $muster . '[^⟧]*⟧?/u', $text, $m);
    return $m[0];
}

/** B7: Zahlen im Text, die in keinem Beleg vorkommen (Listen-Nummern am Zeilenanfang zählen nicht). */
function kanon_zahlen_ohne_beleg(string $neu, array $belege): array {
    $muster = '/(?<![\w.,])\d+(?:[.,]\d+)*(?!\d)/u';
    $vorrat = [];
    foreach ($belege as $b) { preg_match_all($muster, (string)$b, $m); foreach ($m[0] as $z) $vorrat[$z] = true; }
    $text = (string)preg_replace('/^\s*\d+\.\s/mu', ' ', $neu);
    preg_match_all($muster, $text, $m);
    $fehlt = [];
    foreach ($m[0] as $z) if (!isset($vorrat[$z]) && !in_array($z, $fehlt, true)) $fehlt[] = $z;
    return $fehlt;
}

/** B14: gesperrte Begriffe als ganze Wörter, ohne Groß/Klein. */
function kanon_sperrtreffer(string $text, array $woerter): array {
    $t = [];
    foreach ($woerter as $w) {
        $w = trim((string)$w); if ($w === '') continue;
        if (str_starts_with($w, 're:')) { $r = @preg_match('/' . str_replace('/', '\/', substr($w, 3)) . '/iu', $text); $hit = ($r !== 0); } // ungültig (false) sperrt
        elseif (str_ends_with($w, '*')) { $hit = preg_match('/(?<!\w)' . preg_quote(substr($w, 0, -1), '/') . '/iu', $text) === 1; }
        else { $hit = preg_match('/(?<!\w)' . preg_quote($w, '/') . '(?!\w)/iu', $text) === 1; }
        if ($hit) $t[] = $w;
    }
    return $t;
}

/** B5: Erfolgsbehauptungen des Modells („wurde gespeichert“, „ich habe gelöscht“). Erfolg meldet nur der Code. */
function kanon_behauptungen(string $text): array {
    $v = '(gespeichert|gepusht|committet|geschlossen|hochgeladen|gelöscht|geändert|übernommen|eingetragen|hinzugefügt|ergänzt|erledigt|live)';
    preg_match_all('/\b(ich\s+habe\s+(?:\S+\s+){0,4}' . $v . '|(ist|wurde|sind|wurden|habe\s+ich)\s+(jetzt\s+|nun\s+)?' . $v . ')\b/iu', $text, $m);
    return $m[0];
}

/** B10/B12: Nur Kennungen behalten, die es wirklich gibt („Nicht vorhanden“ ist eine Behauptung). */
function kanon_bekannt(?string $id, array $bekannte): bool {
    return $id !== null && $id !== '' && in_array($id, $bekannte, true);
}

/** Gemessene Zeit mit echter Zeitzone (nie fester Versatz). */
function kanon_jetzt(string $zone = 'Europe/Berlin'): string {
    return (new DateTimeImmutable('now', new DateTimeZone($zone)))->format(DATE_ATOM);
}

/** B23: genau eine Zeile je Lauf ans Protokoll (Markdown-Tabelle) anhängen; legt die Datei mit Kopf an.
 *  $ergebnis: 'ok' | 'fehler'. Nebenpflicht: Aufrufer fängt Fehler ab (B17). Gibt false zurück, wenn es nicht ging. */
function kanon_laufzeile(string $pfad, DateTimeImmutable $start, DateTimeImmutable $ende, string $ausloeser,
                         string $regelstand, string $ergebnis, string $grund, string $titel = 'Laufprotokoll'): bool {
    if (!in_array($ergebnis, ['ok', 'fehler'], true)) return false;
    $zelle = function (string $t, int $n = 200): string {
        $t = trim(str_replace('|', '/', (string)preg_replace('/\s+/u', ' ', $t)));
        if ($t === '') return '–';
        return mb_strlen($t) > $n ? mb_substr($t, 0, $n - 1) . '…' : $t;
    };
    $s = max(0, $ende->getTimestamp() - $start->getTimestamp());
    $dauer = $s < 120 ? "$s s" : round($s / 60) . ' min';
    $zeile = '| ' . $start->format('Y-m-d H:i:s T') . ' (gemessen) | ' . $dauer . ' | ' . $zelle($ausloeser, 80) . ' | '
           . $zelle($regelstand, 40) . " | $ergebnis | " . $zelle($grund) . " |\n";
    $vorher = is_file($pfad) ? (string)file_get_contents($pfad) : null;
    $basis = $vorher ?? "# $titel\n\nEine Zeile je Lauf, geschrieben vom Programm. Nur anhängen.\n\n"
           . "| Start | Dauer | Auslöser | Regelstand | Ergebnis | Grund |\n|---|---|---|---|---|---|\n";
    if ($basis !== '' && substr($basis, -1) !== "\n") $basis .= "\n";
    if (@file_put_contents($pfad, $basis . $zeile, LOCK_EX) === false) return false;
    $neu = (string)file_get_contents($pfad);
    return str_starts_with($neu, $vorher ?? '') && str_ends_with($neu, $zeile);
}

/** B21: Beleg zu einer KI-Antwort (für Protokoll oder Antwort an die Oberfläche). */
function kanon_beleg(string $regelstand, string $modell, bool $bestaetigt, array $befunde = []): array {
    return ['regelstand' => $regelstand, 'bestaetigt' => $bestaetigt, 'modell' => $modell . ' (Konfiguration)',
            'zeit' => kanon_jetzt(), 'befunde' => array_values($befunde), 'kanon' => KANON_BASIS_VERSION];
}
