<?php
// Blog – Schnittstelle für den Editor (nur mit persönlichem Schlüssel im Header X-Blog-Schluessel).
// Aktionen (?a=…): liste, hole, speichern, status, serie, uebersetzen, bild, vorschau
// Gespeichert wird in <privat>/daten/ (Beiträge je Datei, serien.json). Der Startbestand wird nie verändert:
// wer einen importierten Beitrag bearbeitet, legt eine eigene Fassung gleicher id in daten/ an.
// Übersetzen: Mistral (Schlüssel in zugang.php). Englisch ist erst sichtbar, wenn im Editor „geprüft“ gesetzt ist.
declare(strict_types=1);
require __DIR__ . '/lib.php';

const BLOG_MISTRAL_MODELL = 'mistral-large-latest';
const BLOG_RESERVIERT = ['en', 'de', 'serie', 'serien', 'stichwort', 'editor', 'vorschau', 'bilder', 'feed', 'api', 'index'];
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');
header('X-Robots-Tag: noindex');

$schluessel = (string)($_SERVER['HTTP_X_BLOG_SCHLUESSEL'] ?? '');
$ICH = (zugang()['zugaenge'] ?? [])[hash('sha256', $schluessel)] ?? null;
if ($schluessel === '' || $ICH === null) json_antwort(401, ['fehler' => 'Kein gültiger Zugang. Bitte den persönlichen Editor-Link öffnen.']);
if ($_SERVER['REQUEST_METHOD'] !== 'POST') json_antwort(405, ['fehler' => 'Nicht erlaubt.']);

function eingabe(): array {
    static $d = null;
    if ($d === null) { $d = json_decode((string)file_get_contents('php://input', false, null, 0, 2_000_000), true); if (!is_array($d)) $d = []; }
    return $d;
}
function protokoll(string $art, string $text): void {
    global $ICH;
    @mkdir(privat(), 0700, true);
    file_put_contents(privat() . '/protokoll.jsonl', json_encode(['zeit' => date('c'), 'wer' => $ICH, 'art' => $art, 'text' => $text], JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
}
function sperre(): mixed { @mkdir(privat(), 0700, true); $s = fopen(privat() . '/.sperre', 'c'); flock($s, LOCK_EX); return $s; }
function speichere_beitrag(array $b): void {
    unset($b['quelle_ordner']);
    schreibe_json(privat() . '/daten/beitraege/' . $b['id'] . '.json', $b);
}
function speichere_serien(array $serien): void { schreibe_json(privat() . '/daten/serien.json', ['serien' => array_values($serien)]); }
function kurz_info(array $b): array {
    return ['id' => $b['id'], 'titel' => $b['titel'], 'datum' => $b['datum'], 'status' => $b['status'], 'serie' => $b['serie'],
        'stichwoerter' => $b['stichwoerter'], 'import' => ($b['quelle_ordner'] ?? '') === 'startbestand', 'herkunft' => $b['herkunft']['quelle'] ?? null,
        'en' => ['geprueft' => (bool)$b['en']['geprueft'], 'da' => trim((string)$b['en']['text']) !== '', 'veraltet' => $b['en']['stand'] !== '' && $b['en']['stand'] !== de_stand($b)]];
}

// ---------- KI ----------
function mistral(string $system, string $frage, int $max = 6000): string {
    if ($attrappe = getenv('BLOG_KI_ATTRAPPE')) { // lokale Tests: einfache, vorhersehbare „Übersetzung“
        return json_encode(['titel' => '[EN] ' . (json_decode($frage, true)['titel'] ?? ''), 'text' => '[EN] ' . (json_decode($frage, true)['text'] ?? '')], JSON_UNESCAPED_UNICODE);
    }
    $k = (string)(zugang()['mistral'] ?? '');
    if ($k === '') json_antwort(503, ['fehler' => 'Die Übersetzung ist nicht eingerichtet (Mistral-Schlüssel fehlt).']);
    $ch = curl_init('https://api.mistral.ai/v1/chat/completions');
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 150, CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json', 'Authorization: Bearer ' . $k],
        CURLOPT_POSTFIELDS => json_encode(['model' => BLOG_MISTRAL_MODELL, 'max_tokens' => $max, 'temperature' => 0.2,
            'response_format' => ['type' => 'json_object'],
            'messages' => [['role' => 'system', 'content' => $system], ['role' => 'user', 'content' => $frage]]], JSON_UNESCAPED_UNICODE)]);
    $r = curl_exec($ch); $code = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE); curl_close($ch);
    $j = is_string($r) ? json_decode($r, true) : null;
    $t = $j['choices'][0]['message']['content'] ?? null;
    if ($code !== 200 || !is_string($t)) json_antwort(502, ['fehler' => 'Die Übersetzung hat gerade nicht geklappt. Bitte gleich noch einmal versuchen.']);
    return $t;
}
const UEBERSETZ_ANWEISUNG = 'Du übersetzt Texte eines persönlichen Blogs vom Deutschen ins Englische. Bleib nah am Ton des Autors (persönlich, '
    . 'nachdenklich, gern mit Witz), schreib natürliches Englisch statt wörtlicher Übersetzung. Behalte die Markdown-Formatierung exakt bei '
    . '(Absätze, Überschriften, Listen, **fett**, *kursiv*, Links [Text](Adresse) und Bilder ![Text](Adresse) – Adressen nie ändern). '
    . 'Eigennamen, Produktnamen und Zitate in anderen Sprachen bleiben, wie sie sind. Füge nichts hinzu und lass nichts weg. '
    . 'Antworte NUR mit JSON: {"titel": "…", "text": "…"}.';
function uebersetze(string $titel, string $text): array {
    $t = mistral(UEBERSETZ_ANWEISUNG, json_encode(['titel' => $titel, 'text' => $text], JSON_UNESCAPED_UNICODE));
    $t = preg_replace('/^```(?:json)?\s*|\s*```$/', '', trim($t)) ?? $t;
    $j = json_decode($t, true);
    if (!is_array($j) || !isset($j['titel'], $j['text'])) json_antwort(502, ['fehler' => 'Die Übersetzung kam unvollständig zurück. Bitte noch einmal versuchen.']);
    return ['titel' => text($j['titel'], 200), 'text' => mb_substr((string)$j['text'], 0, 200000)];
}

// ---------- Aktionen ----------
$a = (string)($_GET['a'] ?? '');
$in = $a === 'bild' ? [] : eingabe();

if ($a === 'liste') {
    $l = array_map('kurz_info', array_values(array_filter(alle_beitraege(), fn($b) => $b['status'] !== 'geloescht')));
    usort($l, fn($x, $y) => strcmp($y['datum'], $x['datum']));
    json_antwort(200, ['ich' => $ICH, 'beitraege' => $l, 'serien' => array_values(alle_serien()), 'vorschau' => ist_vorschau(), 'name' => ein('name'),
        'mistral' => !empty(zugang()['mistral']) || (bool)getenv('BLOG_KI_ATTRAPPE')]);
}

if ($a === 'hole') {
    $b = alle_beitraege()[(string)($in['id'] ?? '')] ?? null;
    if (!$b) json_antwort(404, ['fehler' => 'Diesen Beitrag gibt es nicht.']);
    $b['en_veraltet'] = $b['en']['stand'] !== '' && $b['en']['stand'] !== de_stand($b);
    $b['import'] = ($b['quelle_ordner'] ?? '') === 'startbestand';
    unset($b['quelle_ordner']);
    json_antwort(200, ['beitrag' => $b]);
}

if ($a === 'vorschau') {
    json_antwort(200, ['html' => md(mb_substr((string)($in['text'] ?? ''), 0, 200000))]);
}

if ($a === 'speichern') {
    $s = sperre();
    $alle = alle_beitraege();
    $id = (string)($in['id'] ?? '');
    $neu = $id === '';
    $alt = $neu ? null : ($alle[$id] ?? null);
    if (!$neu && !$alt) json_antwort(404, ['fehler' => 'Diesen Beitrag gibt es nicht.']);
    $titel = text($in['titel'] ?? '', 200);
    if ($titel === '') json_antwort(400, ['fehler' => 'Bitte einen Titel eingeben.']);
    if ($neu) {
        $id = slug($titel);
        if (in_array($id, BLOG_RESERVIERT, true)) $id .= '-beitrag';
        $i = 2; $grund = $id; while (isset($alle[$id])) $id = substr($grund, 0, 75) . '-' . $i++;
    }
    $b = $alt ?? normal(['id' => $id, 'status' => 'entwurf', 'herkunft' => ['quelle' => 'editor']]);
    $b['titel'] = $titel;
    $b['text'] = mb_substr(str_replace("\r\n", "\n", (string)($in['text'] ?? '')), 0, 200000);
    $datum = (string)($in['datum'] ?? '');
    if ($datum !== '') { $z = strtotime($datum); if ($z === false) json_antwort(400, ['fehler' => 'Das Datum verstehe ich nicht.']); $b['datum'] = date('c', $z); }
    $serie = (string)($in['serie'] ?? '');
    if ($serie !== '' && !isset(alle_serien()[$serie])) json_antwort(400, ['fehler' => 'Diese Serie gibt es nicht.']);
    $b['serie'] = $serie === '' ? null : $serie;
    $b['stichwoerter'] = array_values(array_unique(array_filter(array_map(fn($w) => text($w, 40), (array)($in['stichwoerter'] ?? [])), 'strlen')));
    if (isset($in['en']) && is_array($in['en'])) {
        $b['en']['titel'] = text($in['en']['titel'] ?? $b['en']['titel'], 200);
        $b['en']['text'] = mb_substr(str_replace("\r\n", "\n", (string)($in['en']['text'] ?? $b['en']['text'])), 0, 200000);
        $b['en']['geprueft'] = !empty($in['en']['geprueft']) && $b['en']['text'] !== '';
        if (!empty($in['en']['geprueft']) && $b['en']['stand'] === '') $b['en']['stand'] = de_stand($b); // von Hand geschrieben und geprüft
    }
    $b['geaendert'] = date('c');
    speichere_beitrag($b);
    flock($s, LOCK_UN);
    protokoll($neu ? 'neu' : 'gespeichert', $b['id']);
    $b['en_veraltet'] = $b['en']['stand'] !== '' && $b['en']['stand'] !== de_stand($b);
    unset($b['quelle_ordner']);
    json_antwort(200, ['beitrag' => $b, 'uebersetzen_noetig' => $b['en']['stand'] !== de_stand($b)]);
}

if ($a === 'status') {
    $s = sperre();
    $b = alle_beitraege()[(string)($in['id'] ?? '')] ?? null;
    if (!$b) json_antwort(404, ['fehler' => 'Diesen Beitrag gibt es nicht.']);
    $neu = (string)($in['status'] ?? '');
    if (!in_array($neu, ['entwurf', 'veroeffentlicht', 'geloescht'], true)) json_antwort(400, ['fehler' => 'Unbekannter Status.']);
    if ($neu === 'veroeffentlicht' && (trim($b['text']) === '' || trim($b['titel']) === '')) json_antwort(400, ['fehler' => 'Ohne Titel und Text kann ich nichts veröffentlichen.']);
    $b['status'] = $neu; $b['geaendert'] = date('c');
    speichere_beitrag($b);
    flock($s, LOCK_UN);
    protokoll($neu, $b['id']);
    json_antwort(200, ['ok' => true, 'status' => $neu, 'adresse' => basis() . $b['id'] . '/']);
}

if ($a === 'serie') {
    $s = sperre();
    $serien = alle_serien();
    $id = (string)($in['id'] ?? '');
    $titel = text($in['titel'] ?? '', 120);
    if ($titel === '') json_antwort(400, ['fehler' => 'Bitte einen Namen für die Serie eingeben.']);
    if ($id === '') { $id = slug($titel, 60); $i = 2; while (isset($serien[$id])) $id = slug($titel, 55) . '-' . $i++; }
    elseif (!isset($serien[$id])) json_antwort(404, ['fehler' => 'Diese Serie gibt es nicht.']);
    $x = $serien[$id] ?? ['id' => $id, 'en' => ['titel' => '', 'einleitung' => '', 'geprueft' => false, 'stand' => '']];
    $x['titel'] = $titel;
    $x['einleitung'] = mb_substr((string)($in['einleitung'] ?? ''), 0, 20000);
    if (isset($in['en']) && is_array($in['en'])) {
        $x['en']['titel'] = text($in['en']['titel'] ?? '', 120);
        $x['en']['einleitung'] = mb_substr((string)($in['en']['einleitung'] ?? ''), 0, 20000);
        $x['en']['geprueft'] = !empty($in['en']['geprueft']) && $x['en']['titel'] !== '';
    }
    $serien[$id] = $x;
    speichere_serien($serien);
    flock($s, LOCK_UN);
    protokoll('serie', $id);
    json_antwort(200, ['serie' => $x, 'serien' => array_values($serien)]);
}

if ($a === 'uebersetzen') {
    if (isset($in['serie'])) {
        $serien = alle_serien(); $x = $serien[(string)$in['serie']] ?? null;
        if (!$x) json_antwort(404, ['fehler' => 'Diese Serie gibt es nicht.']);
        $u = uebersetze($x['titel'], $x['einleitung']);
        $s = sperre(); $serien = alle_serien();
        $serien[$x['id']]['en'] = ['titel' => $u['titel'], 'einleitung' => $u['text'], 'geprueft' => false, 'stand' => substr(sha1($x['titel'] . "\n" . $x['einleitung']), 0, 12)];
        speichere_serien($serien); flock($s, LOCK_UN);
        protokoll('uebersetzt', 'serie ' . $x['id']);
        json_antwort(200, ['serie' => $serien[$x['id']]]);
    }
    $b = alle_beitraege()[(string)($in['id'] ?? '')] ?? null;
    if (!$b) json_antwort(404, ['fehler' => 'Diesen Beitrag gibt es nicht.']);
    $u = uebersetze($b['titel'], $b['text']);
    $s = sperre();
    $b = alle_beitraege()[$b['id']];
    $b['en'] = ['titel' => $u['titel'], 'text' => $u['text'], 'geprueft' => false, 'stand' => de_stand($b)];
    $b['geaendert'] = date('c');
    speichere_beitrag($b);
    flock($s, LOCK_UN);
    protokoll('uebersetzt', $b['id']);
    json_antwort(200, ['en' => $b['en']]);
}

if ($a === 'bild') {
    $f = $_FILES['bild'] ?? null;
    if (!$f || ($f['error'] ?? 1) !== UPLOAD_ERR_OK) json_antwort(400, ['fehler' => 'Das Bild kam nicht an.']);
    if ($f['size'] > 8_000_000) json_antwort(400, ['fehler' => 'Das Bild ist zu groß (höchstens 8 MB).']);
    $typ = (new finfo(FILEINFO_MIME_TYPE))->file($f['tmp_name']);
    $endung = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp', 'image/gif' => 'gif'][$typ] ?? null;
    if (!$endung) json_antwort(400, ['fehler' => 'Bitte ein Foto oder Bild (JPG, PNG, WebP, GIF) wählen.']);
    $ordner = __DIR__ . '/bilder/' . date('Y-m');
    @mkdir($ordner, 0755, true);
    $name = date('Y-m') . '/' . bin2hex(random_bytes(6)) . '.' . $endung;
    if (!move_uploaded_file($f['tmp_name'], __DIR__ . '/bilder/' . $name) && !rename($f['tmp_name'], __DIR__ . '/bilder/' . $name))
        json_antwort(500, ['fehler' => 'Das Bild konnte nicht gespeichert werden.']);
    protokoll('bild', $name);
    $alt = text($_POST['alt'] ?? '', 120);
    json_antwort(200, ['pfad' => 'bilder/' . $name, 'markdown' => '![' . str_replace(['[', ']'], '', $alt) . '](bilder/' . $name . ')']);
}

json_antwort(400, ['fehler' => 'Unbekannte Aktion.']);
