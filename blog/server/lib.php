<?php
// Blog – gemeinsame Bausteine für Lese-Seiten (index.php), Editor-Schnittstelle (api.php) und Rückmeldungen.
// Inhalte liegen außerhalb des Web-Ordners in <privat>/<name>:
//   startbestand/beitraege/*.json, startbestand/serien.json  – beim Upload mitgeliefert (Import aus alten Quellen)
//   daten/beitraege/*.json, daten/serien.json                – im Editor gespeichert (gehen vor, gleiche id ersetzt)
//   zugang.php                                               – Schlüssel und Einstellungen, beim Upload erzeugt
// Eigene Werte (Name, Adresse, Repo …) kommen aus den Einstellungen, nicht aus dem Code.
declare(strict_types=1);

function privat(): string {
    static $p = null;
    if ($p !== null) return $p;
    if ($e = getenv('BLOG_PRIVAT')) return $p = $e; // nur für lokale Tests
    $ort = ort();                                    // ort.php: <?php return ['privat' => 'name', 'hoch' => 2, 'vorschau' => false];
    $name = preg_match('/^[A-Za-z0-9_-]+$/', (string)($ort['privat'] ?? '')) ? $ort['privat'] : 'blog';
    $hoch = max(1, min(5, (int)($ort['hoch'] ?? 2)));  // Ordner-Ebenen vom Web-Ordner bis neben den Ordner „privat“ (Unterordner wie …/vorschau/: 3)
    return $p = __DIR__ . str_repeat('/..', $hoch) . '/privat/' . $name;
}
function ort(): array { static $o = null; if ($o === null) { $o = @include __DIR__ . '/ort.php'; if (!is_array($o)) $o = []; } return $o; }
function ist_vorschau(): bool { return !empty(ort()['vorschau']) || getenv('BLOG_VORSCHAU') === '1'; }
function zugang(): array { static $z = null; if ($z === null) { $z = @include privat() . '/zugang.php'; if (!is_array($z)) $z = []; } return $z; }

/** Einstellungen mit Vorgaben (eigene Werte in einstellungen.json → zugang.php) */
function ein(string $k): mixed {
    static $e = null;
    if ($e === null) {
        $e = array_merge([
            'name' => 'Mein Blog',
            'untertitel' => '',
            'untertitel_en' => '',
            'autor' => 'Autorin',
            'adresse' => '',          // öffentliche Adresse mit / am Ende (für Feeds); leer = aus der Anfrage
            'stil' => 'a',            // Gestaltung: a, b oder c
            'repo' => '',             // owner/repo für Rückmeldungen als Issues (leer = aus)
            'label' => 'blog',
            'fusszeile' => [],        // [{"text": "Impressum", "url": "…"}]
            'quellen_namen' => [],    // {"blogspot": "Blogspot", …} – Anzeige „Ursprünglich erschienen auf …“
        ], is_array(zugang()['einstellungen'] ?? null) ? zugang()['einstellungen'] : []);
    }
    return $e[$k] ?? null;
}

date_default_timezone_set('Europe/Berlin');

function h(?string $s): string { return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }
function text(mixed $v, int $max = 300): string {
    $s = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', trim((string)$v)) ?? '';
    return mb_substr($s, 0, $max);
}
function slug(string $s, int $max = 80): string {
    $s = mb_strtolower($s);
    $s = strtr($s, ['ä' => 'ae', 'ö' => 'oe', 'ü' => 'ue', 'ß' => 'ss', 'é' => 'e', 'è' => 'e', 'á' => 'a', 'à' => 'a', 'ó' => 'o', 'í' => 'i', 'ñ' => 'n', 'ç' => 'c']);
    $s = preg_replace('/[^a-z0-9]+/', '-', $s) ?? '';
    $s = trim(substr($s, 0, $max), '-');
    return $s === '' ? 'beitrag' : $s;
}
/** Grundadresse dieses Blogs im Web, z. B. /Blog/ oder /Blog/vorschau/ (aus dem Ort von index.php bzw. api.php) */
function basis(): string {
    if (PHP_SAPI === 'cli-server') return '/'; // lokaler Test: Blog liegt im Wurzelordner (SCRIPT_NAME ist dort bei .xml-Adressen unzuverlässig)
    $d =str_replace('\\', '/', dirname((string)($_SERVER['SCRIPT_NAME'] ?? '/index.php')));
    if (str_ends_with($d, '/editor')) $d = substr($d, 0, -7);
    return rtrim($d, '/') . '/';
}
function adresse(): string {
    $a = (string)ein('adresse');
    if (ist_vorschau() && $a !== '') $a = rtrim($a, '/') . '/vorschau/';
    if ($a !== '') return $a;
    $https = (($_SERVER['HTTPS'] ?? '') !== '' && ($_SERVER['HTTPS'] ?? '') !== 'off');
    return ($https ? 'https' : 'http') . '://' . ($_SERVER['HTTP_HOST'] ?? 'localhost') . basis();
}

// ---------- Inhalte laden ----------
function lies_json(string $f): ?array {
    if (!is_file($f)) return null;
    $d = json_decode((string)file_get_contents($f), true);
    return is_array($d) ? $d : null;
}
/** Alle Beiträge (auch Entwürfe), id => Beitrag. Editor-Fassungen ersetzen den Startbestand. */
function alle_beitraege(): array {
    static $alle = null;
    if ($alle !== null) return $alle;
    $alle = [];
    foreach (['startbestand', 'daten'] as $ordner) {
        foreach (glob(privat() . "/$ordner/beitraege/*.json") ?: [] as $f) {
            $b = lies_json($f);
            if (!$b || !preg_match('/^[a-z0-9-]{1,90}$/', (string)($b['id'] ?? ''))) continue;
            $b['quelle_ordner'] = $ordner;
            $alle[$b['id']] = normal($b);
        }
    }
    return $alle;
}
function normal(array $b): array {
    if (isset($b['datum']) && ($z = strtotime((string)$b['datum'])) !== false) $b['datum'] = date('c', $z); // einheitlich, damit Sortieren stimmt
    $b += ['status' => 'entwurf', 'titel' => '', 'text' => '', 'datum' => date('c'), 'serie' => null, 'reihe' => null, 'stichwoerter' => [], 'en' => [], 'herkunft' => []];
    $b['en'] += ['titel' => '', 'text' => '', 'geprueft' => false, 'stand' => ''];
    $b['geaendert'] ??= $b['datum'];
    if (!is_array($b['stichwoerter'])) $b['stichwoerter'] = [];
    return $b;
}
function alle_serien(): array {
    static $s = null;
    if ($s !== null) return $s;
    $s = [];
    foreach (['startbestand', 'daten'] as $ordner) {
        foreach ((lies_json(privat() . "/$ordner/serien.json")['serien'] ?? []) as $x) {
            if (!is_array($x) || !preg_match('/^[a-z0-9-]{1,60}$/', (string)($x['id'] ?? ''))) continue;
            $x += ['titel' => $x['id'], 'einleitung' => '', 'en' => []];
            $x['en'] += ['titel' => '', 'einleitung' => '', 'geprueft' => false, 'stand' => ''];
            $s[$x['id']] = $x;
        }
    }
    return $s;
}
function de_stand(array $b): string { return substr(sha1($b['titel'] . "\n" . $b['text']), 0, 12); }
function en_sichtbar(array $b): bool { return !empty($b['en']['geprueft']) && trim((string)$b['en']['titel']) !== '' && trim((string)$b['en']['text']) !== ''; }

/** Veröffentlichte Beiträge einer Sprache, neueste zuerst */
function veroeffentlicht(string $sprache = 'de'): array {
    $l = array_filter(alle_beitraege(), fn($b) => $b['status'] === 'veroeffentlicht' && strtotime($b['datum']) <= time() + 60
        && ($sprache === 'de' || en_sichtbar($b)));
    uasort($l, fn($a, $b) => strcmp($b['datum'], $a['datum']));
    return $l;
}
/** Teile einer Serie in Lese-Reihenfolge: zuerst nach „reihe“ (alte Nummer aus dem Import), sonst nach Datum (ältester zuerst) */
function serien_teile(string $serie, string $sprache = 'de'): array {
    $l = array_values(array_filter(veroeffentlicht($sprache), fn($b) => $b['serie'] === $serie));
    usort($l, fn($a, $b) => [is_int($a['reihe']) ? $a['reihe'] : PHP_INT_MAX, $a['datum']] <=> [is_int($b['reihe']) ? $b['reihe'] : PHP_INT_MAX, $b['datum']]);
    return $l;
}
/** [Teil-Nummer, Anzahl, vorheriger, nächster] eines Beitrags in seiner Serie */
function serien_platz(array $b, string $sprache = 'de'): ?array {
    if (!$b['serie']) return null;
    $t = serien_teile($b['serie'], $sprache);
    foreach ($t as $i => $x) if ($x['id'] === $b['id']) return [$i + 1, count($t), $t[$i - 1] ?? null, $t[$i + 1] ?? null];
    return null;
}
function serien_titel(string $id, string $sprache = 'de'): string {
    $s = alle_serien()[$id] ?? null;
    if (!$s) return $id;
    if ($sprache === 'en' && !empty($s['en']['geprueft']) && $s['en']['titel'] !== '') return $s['en']['titel'];
    return $s['titel'];
}
function feld(array $b, string $k, string $sprache): string { return $sprache === 'en' ? (string)$b['en'][$k] : (string)$b[$k]; }
function lesezeit(string $text): int { return max(1, (int)round(str_word_count(strip_tags(md($text)), 0, 'äöüÄÖÜß') / 200)); }
function anriss(string $text, int $max = 220): string {
    $t = trim(preg_replace('/\s+/u', ' ', html_entity_decode(preg_replace('/<[^>]+>/', ' ', md($text)) ?? '', ENT_QUOTES, 'UTF-8')) ?? '');
    $t = preg_replace('/\s+([.,;:!?])/u', '$1', $t) ?? $t;
    return mb_strlen($t) > $max ? rtrim(mb_substr($t, 0, $max - 1)) . '…' : $t;
}

// ---------- Markdown (klein, sicher: kein eigenes HTML, keine fremden Bilder) ----------
function md_inline(string $s): string {
    $s = h($s);
    $platz = [];
    $merke = function (string $html) use (&$platz): string { $platz[] = $html; return "\u{E000}" . (count($platz) - 1) . "\u{E001}"; };
    $s = preg_replace_callback('/`([^`]+)`/u', fn($m) => $merke('<code>' . $m[1] . '</code>'), $s) ?? $s;
    // Bilder: nur eigene (relative Pfade), fremde werden zu Links – keine Fremdserver beim Lesen
    $s = preg_replace_callback('/!\[([^\]]*)\]\(([^)\s]+)(?:\s+&quot;([^&]*)&quot;)?\)/u', function ($m) use ($merke) {
        $src = html_entity_decode($m[2], ENT_QUOTES, 'UTF-8');
        if (preg_match('#^(https?:)?//#i', $src) || !preg_match('#^[A-Za-z0-9_./-]+$#', $src) || str_contains($src, '..'))
            return $merke('<a href="' . h($src) . '" rel="nofollow noopener">' . ($m[1] !== '' ? $m[1] : 'Bild') . ' ↗</a>');
        $src = ltrim($src, '/');
        return $merke('<img src="' . h(basis() . $src) . '" alt="' . $m[1] . '" loading="lazy"' . (($m[3] ?? '') !== '' ? ' title="' . $m[3] . '"' : '') . '>');
    }, $s) ?? $s;
    $s = preg_replace_callback('/\[([^\]]+)\]\(([^)\s]+)\)/u', function ($m) use ($merke) {
        $url = html_entity_decode($m[2], ENT_QUOTES, 'UTF-8');
        if (preg_match('/^beitrag:([a-z0-9-]{1,90})$/', $url, $k)) return $merke('<a href="' . h(basis() . $k[1] . '/') . '">' . $m[1] . '</a>');
        if (!preg_match('#^(https?://|mailto:|/|\#)#i', $url)) return $m[0];
        $fremd = (bool)preg_match('#^https?://#i', $url);
        return $merke('<a href="' . h($url) . '"' . ($fremd ? ' rel="noopener"' : '') . '>' . $m[1] . '</a>');
    }, $s) ?? $s;
    $s = preg_replace('/\*\*(.+?)\*\*/u', '<strong>$1</strong>', $s) ?? $s;
    $s = preg_replace('/(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])/u', '<em>$1</em>', $s) ?? $s;
    $s = preg_replace('/(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])/u', '<em>$1</em>', $s) ?? $s;
    $s = preg_replace('/  \n/', "<br>\n", $s) ?? $s;
    return preg_replace_callback("/\u{E000}(\d+)\u{E001}/u", fn($m) => $platz[(int)$m[1]], $s) ?? $s;
}
function md(string $text): string {
    $zeilen = preg_split('/\R/u', str_replace("\t", '    ', $text)) ?: [];
    $out = []; $absatz = []; $liste = null; $zitat = [];
    $schliesse = function () use (&$out, &$absatz, &$liste, &$zitat) {
        if ($absatz) { $out[] = '<p>' . md_inline(implode("\n", $absatz)) . '</p>'; $absatz = []; }
        if ($liste) { $out[] = "<{$liste['tag']}>" . implode('', array_map(fn($x) => '<li>' . md_inline($x) . '</li>', $liste['punkte'])) . "</{$liste['tag']}>"; $liste = null; }
        if ($zitat) { $out[] = '<blockquote>' . md(implode("\n", $zitat)) . '</blockquote>'; $zitat = []; }
    };
    foreach ($zeilen as $z) {
        if (preg_match('/^\s*>\s?(.*)$/u', $z, $m)) { if ($absatz || $liste) { $q = $zitat; $zitat = []; $schliesse(); $zitat = $q; } $zitat[] = $m[1]; continue; }
        if ($zitat && trim($z) !== '') { $zitat[] = $z; continue; }
        if (trim($z) === '') { $schliesse(); continue; }
        if (preg_match('/^(#{1,4})\s+(.+?)\s*#*$/u', $z, $m)) { $schliesse(); $n = min(4, strlen($m[1]) + 1); $out[] = "<h$n>" . md_inline($m[2]) . "</h$n>"; continue; }
        if (preg_match('/^\s*(\*\s*\*\s*\*|-\s*-\s*-|_\s*_\s*_)[\s*_-]*$/u', $z)) { $schliesse(); $out[] = '<hr>'; continue; }
        if (preg_match('/^\s*([-*+]|\d{1,3}[.)])\s+(.*)$/u', $z, $m)) {
            $tag = ctype_digit(rtrim($m[1], '.)')) ? 'ol' : 'ul';
            if ($absatz) { $absatz_alt = $absatz; $absatz = []; $l = $liste; $liste = null; $out[] = '<p>' . md_inline(implode("\n", $absatz_alt)) . '</p>'; $liste = $l; }
            if ($liste && $liste['tag'] !== $tag) $schliesse();
            $liste ??= ['tag' => $tag, 'punkte' => []];
            $liste['punkte'][] = $m[2];
            continue;
        }
        if ($liste && preg_match('/^\s{2,}(\S.*)$/u', $z, $m)) { $liste['punkte'][count($liste['punkte']) - 1] .= "\n" . $m[1]; continue; }
        if ($liste) $schliesse();
        $absatz[] = $z;
    }
    $schliesse();
    return implode("\n", $out);
}

// ---------- Ausgabe-Helfer ----------
function json_antwort(int $code, array $d): never {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($d, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
function schreibe_json(string $f, array $d): void {
    @mkdir(dirname($f), 0700, true);
    $tmp = $f . '.tmp' . bin2hex(random_bytes(3));
    file_put_contents($tmp, json_encode($d, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
    rename($tmp, $f);
}
