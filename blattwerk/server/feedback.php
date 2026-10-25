<?php
// Blattwerk – Rückmeldungen: legt Issues im eingestellten Repo an (POST) und listet die bisherigen (GET).
// Nur für angemeldete Geräte. Der GitHub-Schlüssel liegt in <privat>/blattwerk/zugang.php (Feld 'gh').
declare(strict_types=1);
require __DIR__ . '/lib.php';
bw_header();

$z = bw_zugang();
if (!$z || !bw_gueltig($z)) { bw_json(401, ['fehler' => 'Bitte zuerst anmelden.']); exit; }
$gh = (string)($z['gh'] ?? '');
if ($gh === '' || BW_REPO === '') { bw_json(503, ['fehler' => 'Rückmeldungen sind noch nicht eingerichtet.']); exit; }

$ARTEN = ['fehler' => 'Fehler', 'wunsch' => 'Wunsch', 'frage' => 'Frage'];

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    [$st, $liste] = bw_github('GET', '/repos/' . BW_REPO . '/issues?labels=rueckmeldung&state=all&per_page=30&sort=created&direction=desc', null, $gh);
    if ($st !== 200 || !is_array($liste)) { bw_json(502, ['fehler' => 'Die Liste ließ sich gerade nicht laden.']); exit; }
    $out = [];
    foreach ($liste as $i) {
        if (isset($i['pull_request'])) continue;
        $labels = array_map(fn($l) => $l['name'], $i['labels'] ?? []);
        $status = 'Eingegangen';
        if (in_array(bw_einstellung('label_rueckfrage'), $labels, true)) $status = 'Rückfrage';
        if (in_array('vorschau', $labels, true)) $status = 'In der Vorschau';
        if (in_array('live', $labels, true) || ($i['state'] ?? '') === 'closed') $status = 'Erledigt';
        $out[] = ['nr' => $i['number'], 'titel' => preg_replace('/^Rückmeldung:\s*/u', '', (string)$i['title']), 'status' => $status, 'datum' => substr((string)$i['created_at'], 0, 10)];
    }
    bw_json(200, ['liste' => $out]);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { bw_json(405, ['fehler' => 'Nicht erlaubt.']); exit; }

$roh = file_get_contents('php://input', false, null, 0, 300000);
$d = json_decode((string)$roh, true);
if (!is_array($d)) { bw_json(400, ['fehler' => 'Die Rückmeldung kam unvollständig an.']); exit; }
$text = trim((string)($d['text'] ?? ''));
if (mb_strlen($text) < 3) { bw_json(400, ['fehler' => 'Bitte schreib ein paar Worte dazu.']); exit; }
$text = mb_substr($text, 0, 5000);
$art = array_key_exists((string)($d['art'] ?? ''), $ARTEN) ? (string)$d['art'] : 'wunsch';

// höchstens eine Rückmeldung alle 20 Sekunden
$marke = bw_privat() . '/feedback-zeit.txt';
if (is_file($marke) && time() - (int)@filemtime($marke) < 20) { bw_json(429, ['fehler' => 'Bitte einen kleinen Moment warten und dann noch einmal senden.']); exit; }
@touch($marke);

$zeilen = preg_split('/\R/u', $text);
$titel = 'Rückmeldung: ' . mb_substr(trim($zeilen[0]), 0, 70);
$zitat = implode("\n", array_map(fn($z) => '> ' . $z, $zeilen));
$meta = function ($k) use ($d) { return str_replace(['|', "\n"], ['/', ' '], mb_substr(trim((string)($d[$k] ?? '')), 0, 200)); };
$body = "**Art:** {$ARTEN[$art]}\n\n{$zitat}\n\n---\n\n| | |\n|---|---|\n" .
    '| Fassung | ' . $meta('fassung') . " |\n| Gerät | " . $meta('geraet') . " |\n| Bildschirm | " . $meta('bildschirm') . " |\n| Blatt | " . $meta('blatt') . " |\n";
$blatt = $d['blattDatei'] ?? null;
if (is_array($blatt)) {
    $json = json_encode($blatt, JSON_UNESCAPED_UNICODE);
    if (is_string($json) && strlen($json) < 55000) {
        $body .= "\n<details><summary>Blatt als Datei (zum Nachbauen, ohne Bilder)</summary>\n\n```json\n{$json}\n```\n</details>\n";
    } else {
        $body .= "\n_Das Blatt war zu groß, um es mitzuschicken._\n";
    }
}
$body .= "\n_Gesendet aus Blattwerk über den Rückmelde-Knopf._";

[$st, $issue] = bw_github('POST', '/repos/' . BW_REPO . '/issues', ['title' => $titel, 'body' => $body, 'labels' => ['rueckmeldung', $art]], $gh);
if ($st !== 201 || !is_array($issue)) { bw_json(502, ['fehler' => 'Senden hat gerade nicht geklappt. Bitte später noch einmal versuchen.']); exit; }
bw_json(201, ['nr' => $issue['number']]);
