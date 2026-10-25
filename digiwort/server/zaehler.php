<?php
// Digiwort – Besuchszähler. Zählt nur Anzahlen pro Tag (Europe/Berlin), keine IP, kein Cookie, nichts Persönliches.
// POST = ein Besuch (das Spiel schickt höchstens einen pro Tag und Gerät), GET = nur lesen.
// Antwort: {"heute":n,"woche":n,"total":n}  ·  Daten: <privat>/digiwort/zaehler.json
declare(strict_types=1);
date_default_timezone_set('Europe/Berlin');
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

$m = $_SERVER['REQUEST_METHOD'];
if ($m !== 'GET' && $m !== 'POST') { http_response_code(405); echo '{}'; exit; }
$herkunft = (string)($_SERVER['HTTP_ORIGIN'] ?? '');
$hostHier = (string)preg_replace('/:\d+$/', '', (string)($_SERVER['HTTP_HOST'] ?? ''));
$hostHer = parse_url($herkunft, PHP_URL_HOST);
$zaehlen = $m === 'POST' && ($herkunft === '' || (is_string($hostHer) && strcasecmp($hostHer, $hostHier) === 0) || getenv('DW_PRIVAT'));

$ort = @include __DIR__ . '/ort.php'; // optional: <?php return ['privat' => 'name'];
$ordner = getenv('DW_PRIVAT') ?: __DIR__ . '/../../privat/' . ((is_array($ort) && preg_match('/^[A-Za-z0-9_-]+$/', (string)($ort['privat'] ?? ''))) ? $ort['privat'] : 'digiwort');
@mkdir($ordner, 0700, true);
$fh = @fopen($ordner . '/zaehler.json', 'c+');
if (!$fh) { http_response_code(503); echo '{}'; exit; }
flock($fh, $zaehlen ? LOCK_EX : LOCK_SH);
$d = json_decode((string)stream_get_contents($fh), true);
if (!is_array($d)) $d = ['total' => 0, 'tage' => []];
$heute = date('Y-m-d');
if ($zaehlen) {
    $d['total'] = (int)($d['total'] ?? 0) + 1;
    $d['tage'][$heute] = (int)($d['tage'][$heute] ?? 0) + 1;
    krsort($d['tage']);
    $d['tage'] = array_slice($d['tage'], 0, 400, true); // gut ein Jahr Tageswerte reicht
    ftruncate($fh, 0); rewind($fh); fwrite($fh, json_encode($d)); fflush($fh);
}
flock($fh, LOCK_UN); fclose($fh);

$woche = 0;
for ($i = 0; $i < 7; $i++) $woche += (int)($d['tage'][date('Y-m-d', strtotime("-$i day"))] ?? 0);
echo json_encode(['heute' => (int)($d['tage'][$heute] ?? 0), 'woche' => $woche, 'total' => (int)($d['total'] ?? 0)]);
