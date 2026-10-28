<?php
// Blog – Lese-Seiten: Start, Beitrag, Serie, Serien, Stichwort, Feed (Atom) – jeweils Deutsch und unter en/ Englisch.
// Alle Adressen laufen über .htaccess hierher (im lokalen Test über php -S index.php als Router).
declare(strict_types=1);

if (PHP_SAPI === 'cli-server') {
    $p = parse_url((string)$_SERVER['REQUEST_URI'], PHP_URL_PATH) ?: '/';
    if ($p !== '/' && is_file(__DIR__ . $p)) return false;                       // Bilder, CSS, api.php …
    if (is_dir(__DIR__ . $p) && is_file(rtrim(__DIR__ . $p, '/') . '/index.html')) {
        if (!str_ends_with($p, '/')) { header('Location: ' . $p . '/'); exit; }
        header('Content-Type: text/html; charset=utf-8'); readfile(rtrim(__DIR__ . $p, '/') . '/index.html'); exit;
    }
}
require __DIR__ . '/lib.php';

header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: strict-origin-when-cross-origin');
if (ist_vorschau()) header('X-Robots-Tag: noindex, nofollow');

// Noch nicht gestartet ("live": false): Leser sehen nur einen Platzhalter, der Editor arbeitet schon mit den echten Daten.
if (!ein('live') && !ist_vorschau()) {
    header('X-Robots-Tag: noindex, nofollow');
    header('Content-Type: text/html; charset=utf-8');
    header('Cache-Control: no-store');
    echo '<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">'
        . '<title>' . h((string)ein('name')) . '</title><body style="font:1.1rem/1.5 system-ui,sans-serif;margin:3rem auto;max-width:32rem;padding:0 16px">'
        . '<h1 style="font-size:1.5rem">' . h((string)ein('name')) . ' ☕</h1><p>Hier entsteht gerade ein Blog – bald geht es los.</p></body></html>';
    exit;
}

const TEXTE = [
    'de' => ['neu' => 'Neueste Beiträge', 'serien' => 'Serien', 'teil' => 'Teil %d von %d', 'vor' => 'Vorheriger Teil', 'nach' => 'Nächster Teil',
        'von_vorne' => 'Von vorne lesen', 'alle_teile' => 'Alle Teile der Serie', 'lesezeit' => '%d Min. Lesezeit', 'stichwoerter' => 'Stichwörter',
        'ursprung' => 'Ursprünglich erschienen auf %s', 'andere' => 'English', 'rm' => 'Rückmeldung geben', 'serie' => 'Serie',
        'teile' => '%d Teile', 'ein_teil' => '1 Teil', 'weg' => 'Diese Seite gibt es nicht (mehr).', 'zur_start' => 'Zur Startseite',
        'aeltere' => 'Ältere Beiträge', 'neuere' => 'Neuere Beiträge', 'stichwort' => 'Stichwort', 'feed' => 'Feed abonnieren',
        'leer' => 'Hier erscheinen bald die ersten Beiträge.', 'rm_hilfe' => 'Fehler entdeckt oder ein Gedanke dazu? Schreib es kurz – es geht nur an mich, nichts wird hier veröffentlicht.',
        'fehler' => 'Fehler', 'wunsch' => 'Idee', 'sonstiges' => 'Sonstiges', 'senden' => 'Senden', 'danke' => 'Danke! Ist angekommen.',
        'gestaltung' => 'Gestaltung:', 'stil_a' => 'Kaffeehaus', 'stil_c' => 'digifil',
        'monate' => ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']],
    'en' => ['neu' => 'Latest posts', 'serien' => 'Series', 'teil' => 'Part %d of %d', 'vor' => 'Previous part', 'nach' => 'Next part',
        'von_vorne' => 'Start from the beginning', 'alle_teile' => 'All parts of the series', 'lesezeit' => '%d min read', 'stichwoerter' => 'Tags',
        'ursprung' => 'Originally published on %s', 'andere' => 'Deutsch', 'rm' => 'Send feedback', 'serie' => 'Series',
        'teile' => '%d parts', 'ein_teil' => '1 part', 'weg' => 'This page does not exist (any more).', 'zur_start' => 'Back to the start',
        'aeltere' => 'Older posts', 'neuere' => 'Newer posts', 'stichwort' => 'Tag', 'feed' => 'Subscribe (feed)',
        'leer' => 'The first posts will appear here soon.', 'rm_hilfe' => 'Spotted a mistake or have a thought? Write a few words – it only goes to me, nothing is published here.',
        'fehler' => 'Mistake', 'wunsch' => 'Idea', 'sonstiges' => 'Other', 'senden' => 'Send', 'danke' => 'Thank you! Received.',
        'gestaltung' => 'Look:', 'stil_a' => 'Coffee house', 'stil_c' => 'digifil',
        'monate' => ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']],
];
$L = 'de';
function t(string $k, mixed ...$a): string { global $L; $s = TEXTE[$L][$k]; return $a ? sprintf($s, ...$a) : $s; }
function datum_text(string $iso): string {
    global $L; $z = strtotime($iso); $m = TEXTE[$L]['monate'][(int)date('n', $z) - 1];
    return $L === 'en' ? $m . ' ' . date('j, Y', $z) : date('j.', $z) . ' ' . $m . ' ' . date('Y', $z);
}
function link_zu(string $pfad = '', ?string $sprache = null): string { global $L; $s = $sprache ?? $L; return basis() . ($s === 'en' ? 'en/' : '') . $pfad; }

// ---------- Adresse zerlegen ----------
$pfad = (string)(parse_url((string)($_SERVER['REQUEST_URI'] ?? '/'), PHP_URL_PATH) ?: '/');
$b = basis();
$pfad = str_starts_with($pfad, $b) ? substr($pfad, strlen($b)) : ltrim($pfad, '/');
$teile = array_values(array_filter(explode('/', rawurldecode($pfad)), 'strlen'));
if (($teile[0] ?? '') === 'en') { $L = 'en'; array_shift($teile); }

// ---------- Bausteine ----------
function seite(string $titel, string $inhalt, array $opt = []): never {
    global $L;
    $name = (string)ein('name');
    $unter = (string)ein($L === 'en' && ein('untertitel_en') ? 'untertitel_en' : 'untertitel');
    $stil = in_array(ein('stil'), ['a', 'b', 'c'], true) ? ein('stil') : 'a';
    $beschr = $opt['beschreibung'] ?? $unter;
    $andere = $opt['andere'] ?? null; // Adresse der anderen Sprache, falls vorhanden
    http_response_code($opt['code'] ?? 200);
    header('Content-Type: text/html; charset=utf-8');
    $vorschau = ist_vorschau();
    $fuss = '';
    foreach ((array)ein('fusszeile') as $f) if (is_array($f) && !empty($f['url'])) $fuss .= ' · <a href="' . h($f['url']) . '">' . h($f['text'] ?? $f['url']) . '</a>';
    $vt = $titel === $name ? $name : "$titel · $name";
    echo '<!doctype html><html lang="' . $L . '" data-stil="' . $stil . '"><head><meta charset="utf-8">'
        . '<meta name="viewport" content="width=device-width, initial-scale=1">'
        . '<title>' . ($vorschau ? 'Vorschau · ' : '') . h($vt) . '</title>'
        . '<meta name="description" content="' . h($beschr) . '">'
        . ($vorschau ? '<meta name="robots" content="noindex, nofollow">' : '')
        . '<meta property="og:title" content="' . h($titel) . '"><meta property="og:description" content="' . h($beschr) . '"><meta property="og:type" content="' . (isset($opt['artikel']) ? 'article' : 'website') . '">'
        . (isset($opt['kanon']) ? '<link rel="canonical" href="' . h(adresse() . $opt['kanon']) . '">' : '')
        . ($andere ? '<link rel="alternate" hreflang="' . ($L === 'en' ? 'de' : 'en') . '" href="' . h($andere) . '">' : '')
        . '<link rel="alternate" type="application/atom+xml" title="' . h($name) . '" href="' . h(link_zu('feed.xml')) . '">'
        . '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Ctext y=%2226%22 font-size=%2226%22%3E%E2%98%95%3C/text%3E%3C/svg%3E">'
        . '<link rel="stylesheet" href="' . h(basis()) . 'blog.css">'
        . '<script data-stilwahl>try{var s=localStorage.getItem("blog-stil");if(s&&/^[' . ($vorschau ? 'abc' : 'ac') . ']$/.test(s))document.documentElement.dataset.stil=s}catch(e){}</script>'
        . '</head><body>'
        . ($vorschau ? '<div class="vorschau-schild">VORSCHAU · Gestaltung: <button data-s="a">A Kaffeehaus</button> <button data-s="b">B Klar</button> <button data-s="c">C digifil</button></div>' : '')
        . '<header class="kopf"><div class="breit"><a class="marke" href="' . h(link_zu()) . '">' . h($name) . '</a>'
        . ($unter !== '' ? '<p class="unter">' . h($unter) . '</p>' : '')
        . '<nav class="leiste"><a href="' . h(link_zu('serien/')) . '">' . t('serien') . '</a>'
        . ($andere ? '<a href="' . h($andere) . '" hreflang="' . ($L === 'en' ? 'de' : 'en') . '">' . t('andere') . '</a>' : '')
        . '</nav></div></header>'
        . '<main class="breit">' . $inhalt . '</main>'
        . '<footer class="fuss"><div class="breit">'
        . '<details class="rm"><summary>' . t('rm') . '</summary><form id="rm"><p class="klein">' . t('rm_hilfe') . '</p>'
        . '<div class="arten" role="radiogroup">'
        . '<label><input type="radio" name="art" value="fehler"> ' . t('fehler') . '</label>'
        . '<label><input type="radio" name="art" value="wunsch"> ' . t('wunsch') . '</label>'
        . '<label><input type="radio" name="art" value="sonstiges" checked> ' . t('sonstiges') . '</label></div>'
        . '<textarea name="text" rows="4" maxlength="1000" required></textarea>'
        . '<input name="web" tabindex="-1" autocomplete="off" class="versteckt" aria-hidden="true">'
        . '<button type="submit">' . t('senden') . '</button> <span class="rm-status" aria-live="polite" data-danke="' . h(t('danke')) . '"></span></form></details>'
        . '<p class="klein"><a href="' . h(link_zu('feed.xml')) . '">' . t('feed') . '</a>' . $fuss . '</p>'
        . '<p class="klein stilwahl">' . t('gestaltung') . ' <button type="button" data-s="a">' . t('stil_a') . '</button> <button type="button" data-s="c">' . t('stil_c') . '</button></p>'
        . '</div></footer>'
        . '<script src="' . h(basis()) . 'blog.js" defer></script>'
        . '</body></html>';
    exit;
}
function meta_zeile(array $x, bool $mit_serie = true): string {
    global $L;
    $s = '<time datetime="' . h($x['datum']) . '">' . datum_text($x['datum']) . '</time> · <span class="tasse">☕ ' . t('lesezeit', lesezeit(feld($x, 'text', $L))) . '</span>';
    if ($mit_serie && ($p = serien_platz($x, $L))) $s .= ' · <a class="serie-chip" href="' . h(link_zu('serie/' . $x['serie'] . '/')) . '">' . h(serien_titel($x['serie'], $L)) . ' · ' . t('teil', $p[0], $p[1]) . '</a>';
    return '<p class="meta">' . $s . '</p>';
}
function karte(array $x): string {
    global $L;
    return '<article class="karte"><h2><a href="' . h(link_zu($x['id'] . '/')) . '">' . h(feld($x, 'titel', $L)) . '</a></h2>'
        . meta_zeile($x) . '<p class="anriss">' . h(anriss(feld($x, 'text', $L))) . '</p></article>';
}
function serien_liste(): string {
    global $L;
    $h = '';
    foreach (alle_serien() as $id => $s) {
        $n = count(serien_teile($id, $L));
        if ($n === 0) continue;
        $h .= '<li><a href="' . h(link_zu("serie/$id/")) . '">' . h(serien_titel($id, $L)) . '</a> <span class="zahl">' . ($n === 1 ? t('ein_teil') : t('teile', $n)) . '</span></li>';
    }
    return $h === '' ? '' : '<ul class="serien">' . $h . '</ul>';
}
function nicht_gefunden(): never {
    seite('404', '<h1>' . t('weg') . '</h1><p><a href="' . h(link_zu()) . '">' . t('zur_start') . '</a></p>', ['code' => 404]);
}

// ---------- Seiten ----------
$was = $teile[0] ?? '';

if ($was === 'feed.xml' && count($teile) === 1) {
    header('Content-Type: application/atom+xml; charset=utf-8');
    header('Cache-Control: max-age=600');
    $liste = array_slice(veroeffentlicht($L), 0, 30);
    $basisurl = adresse() . ($L === 'en' ? 'en/' : '');
    $neu = $liste ? max(array_map(fn($x) => strtotime($x['geaendert'] ?? $x['datum']), $liste)) : time();
    $x = new XMLWriter(); $x->openMemory(); $x->setIndent(true); $x->startDocument('1.0', 'UTF-8');
    $x->startElement('feed'); $x->writeAttribute('xmlns', 'http://www.w3.org/2005/Atom'); $x->writeAttribute('xml:lang', $L);
    $x->writeElement('title', (string)ein('name'));
    if ($u = (string)ein($L === 'en' && ein('untertitel_en') ? 'untertitel_en' : 'untertitel')) $x->writeElement('subtitle', $u);
    $x->writeElement('id', $basisurl);
    $x->startElement('link'); $x->writeAttribute('rel', 'alternate'); $x->writeAttribute('href', $basisurl); $x->endElement();
    $x->startElement('link'); $x->writeAttribute('rel', 'self'); $x->writeAttribute('href', $basisurl . 'feed.xml'); $x->endElement();
    $x->writeElement('updated', date('c', $neu));
    $x->startElement('author'); $x->writeElement('name', (string)ein('autor')); $x->endElement();
    foreach ($liste as $b2) {
        $url = $basisurl . $b2['id'] . '/';
        $x->startElement('entry');
        $x->writeElement('title', feld($b2, 'titel', $L));
        $x->startElement('link'); $x->writeAttribute('rel', 'alternate'); $x->writeAttribute('href', $url); $x->endElement();
        $x->writeElement('id', $url);
        $x->writeElement('published', date('c', strtotime($b2['datum'])));
        $x->writeElement('updated', date('c', strtotime($b2['geaendert'] ?? $b2['datum'])));
        if ($p = serien_platz($b2, $L)) {
            $x->startElement('category'); $x->writeAttribute('term', $b2['serie']);
            $x->writeAttribute('label', serien_titel($b2['serie'], $L) . ' · ' . t('teil', $p[0], $p[1])); $x->endElement();
        }
        foreach ($b2['stichwoerter'] as $w) { $x->startElement('category'); $x->writeAttribute('term', (string)$w); $x->endElement(); }
        $x->startElement('summary'); $x->writeAttribute('type', 'text'); $x->text(anriss(feld($b2, 'text', $L), 300)); $x->endElement();
        $html = md(feld($b2, 'text', $L));
        $html = preg_replace('#(src|href)="/#', '$1="' . preg_replace('#^(https?://[^/]+).*$#', '$1', adresse()) . '/', $html) ?? $html; // absolute Adressen im Feed
        $x->startElement('content'); $x->writeAttribute('type', 'html'); $x->text($html); $x->endElement();
        $x->endElement();
    }
    $x->endElement(); $x->endDocument();
    echo $x->outputMemory();
    exit;
}

if ($was === '') {
    $alle = array_values(veroeffentlicht($L));
    $seite_nr = max(1, (int)($_GET['seite'] ?? 1)); $pro = 15;
    $stueck = array_slice($alle, ($seite_nr - 1) * $pro, $pro);
    if (!$stueck && $seite_nr > 1) nicht_gefunden();
    $h = serien_liste();
    if ($h !== '') $h = '<section class="serien-kasten"><h2 class="abschnitt">' . t('serien') . '</h2>' . $h . '</section>';
    $h .= '<h1 class="abschnitt">' . t('neu') . '</h1>';
    $h .= $stueck ? implode('', array_map('karte', $stueck)) : '<p class="leer">' . t('leer') . '</p>';
    $nav = '';
    if ($seite_nr > 1) $nav .= '<a href="' . h(link_zu($seite_nr > 2 ? '?seite=' . ($seite_nr - 1) : '')) . '">‹ ' . t('neuere') . '</a>';
    if (count($alle) > $seite_nr * $pro) $nav .= '<a href="' . h(link_zu('?seite=' . ($seite_nr + 1))) . '">' . t('aeltere') . ' ›</a>';
    if ($nav) $h .= '<nav class="blaettern">' . $nav . '</nav>';
    $andere = $L === 'de' ? (veroeffentlicht('en') ? link_zu('', 'en') : null) : link_zu('', 'de');
    seite((string)ein('name'), $h, ['andere' => $andere, 'kanon' => $L === 'en' ? 'en/' : '']);
}

if ($was === 'serien' && count($teile) === 1) {
    $h = '<h1 class="abschnitt">' . t('serien') . '</h1>';
    foreach (alle_serien() as $id => $s) {
        $tt = serien_teile($id, $L);
        if (!$tt) continue;
        $ein = $L === 'en' && !empty($s['en']['geprueft']) ? $s['en']['einleitung'] : ($L === 'de' ? $s['einleitung'] : '');
        $h .= '<article class="karte"><h2><a href="' . h(link_zu("serie/$id/")) . '">' . h(serien_titel($id, $L)) . '</a></h2>'
            . '<p class="meta">' . (count($tt) === 1 ? t('ein_teil') : t('teile', count($tt))) . ' · ' . datum_text($tt[0]['datum']) . ' – ' . datum_text(end($tt)['datum']) . '</p>'
            . ($ein !== '' ? '<p class="anriss">' . h(anriss($ein)) . '</p>' : '') . '</article>';
    }
    seite(t('serien'), $h, ['andere' => link_zu('serien/', $L === 'de' ? 'en' : 'de'), 'kanon' => ($L === 'en' ? 'en/' : '') . 'serien/']);
}

if ($was === 'serie' && count($teile) === 2) {
    $id = $teile[1]; $s = alle_serien()[$id] ?? null;
    $tt = $s ? serien_teile($id, $L) : [];
    if (!$tt) nicht_gefunden();
    $ein = $L === 'en' ? (!empty($s['en']['geprueft']) ? $s['en']['einleitung'] : '') : $s['einleitung'];
    $h = '<p class="vorspann">' . t('serie') . '</p><h1>' . h(serien_titel($id, $L)) . '</h1>'
        . ($ein !== '' ? '<div class="text einleitung">' . md($ein) . '</div>' : '')
        . '<p><a class="knopf" href="' . h(link_zu($tt[0]['id'] . '/')) . '">' . t('von_vorne') . ' →</a></p><ol class="teile">';
    foreach ($tt as $i => $x) $h .= '<li><a href="' . h(link_zu($x['id'] . '/')) . '">' . h(feld($x, 'titel', $L)) . '</a> <span class="zahl">' . datum_text($x['datum']) . '</span></li>';
    $h .= '</ol>';
    $andere = $L === 'de' ? (serien_teile($id, 'en') ? link_zu("serie/$id/", 'en') : null) : link_zu("serie/$id/", 'de');
    seite(serien_titel($id, $L), $h, ['andere' => $andere, 'beschreibung' => anriss($ein ?: serien_titel($id, $L)), 'kanon' => ($L === 'en' ? 'en/' : '') . "serie/$id/"]);
}

if ($was === 'stichwort' && count($teile) === 2) {
    $wort = null; $liste = [];
    foreach (veroeffentlicht($L) as $x) foreach ($x['stichwoerter'] as $w) if (slug((string)$w) === $teile[1]) { $wort ??= (string)$w; $liste[] = $x; break; }
    if (!$liste) nicht_gefunden();
    seite($wort, '<p class="vorspann">' . t('stichwort') . '</p><h1>' . h($wort) . '</h1>' . implode('', array_map('karte', $liste)),
        ['andere' => link_zu('stichwort/' . $teile[1] . '/', $L === 'de' ? 'en' : 'de')]);
}

if (count($teile) === 1 && preg_match('/^[a-z0-9-]{1,90}$/', $was)) {
    $x = alle_beitraege()[$was] ?? null;
    if (!$x || $x['status'] !== 'veroeffentlicht' || strtotime($x['datum']) > time() + 60) nicht_gefunden();
    if ($L === 'en' && !en_sichtbar($x)) { header('Location: ' . link_zu($x['id'] . '/', 'de'), true, 302); exit; }
    $h = '<article class="beitrag">';
    $p = serien_platz($x, $L);
    if ($p) $h .= '<p class="vorspann"><a href="' . h(link_zu('serie/' . $x['serie'] . '/')) . '">' . h(serien_titel($x['serie'], $L)) . '</a> · ' . t('teil', $p[0], $p[1]) . '</p>';
    $h .= '<h1>' . h(feld($x, 'titel', $L)) . '</h1>' . meta_zeile($x, !$p) . '<div class="text">' . md(feld($x, 'text', $L)) . '</div>';
    if ($x['stichwoerter']) $h .= '<p class="stichwoerter"><span>' . t('stichwoerter') . ':</span> ' . implode(' ', array_map(fn($w) => '<a href="' . h(link_zu('stichwort/' . slug((string)$w) . '/')) . '">' . h((string)$w) . '</a>', $x['stichwoerter'])) . '</p>';
    $hk = $x['herkunft'];
    if (!empty($hk['url'])) {
        $qn = ((array)ein('quellen_namen'))[$hk['quelle'] ?? ''] ?? (parse_url((string)$hk['url'], PHP_URL_HOST) ?: '');
        $h .= '<p class="ursprung">' . sprintf(h(t('ursprung')), '<a href="' . h($hk['url']) . '" rel="noopener">' . h($qn) . '</a>')
            . (!empty($hk['bezeichnung']) ? ' · ' . h((string)$hk['bezeichnung']) : '') . '</p>';
    }
    if ($p) {
        $h .= '<nav class="serien-nav" aria-label="' . h(t('serie')) . '">'
            . ($p[2] ? '<a class="vor" href="' . h(link_zu($p[2]['id'] . '/')) . '"><span>‹ ' . t('vor') . '</span>' . h(feld($p[2], 'titel', $L)) . '</a>' : '<span></span>')
            . ($p[3] ? '<a class="nach" href="' . h(link_zu($p[3]['id'] . '/')) . '"><span>' . t('nach') . ' ›</span>' . h(feld($p[3], 'titel', $L)) . '</a>' : '<span></span>')
            . '<a class="alle" href="' . h(link_zu('serie/' . $x['serie'] . '/')) . '">' . t('alle_teile') . ' (' . $p[1] . ')</a></nav>';
    }
    $h .= '</article>';
    $andere = $L === 'de' ? (en_sichtbar($x) ? link_zu($x['id'] . '/', 'en') : null) : link_zu($x['id'] . '/', 'de');
    seite(feld($x, 'titel', $L), $h, ['andere' => $andere, 'beschreibung' => anriss(feld($x, 'text', $L), 160), 'artikel' => true,
        'kanon' => ($L === 'en' ? 'en/' : '') . $x['id'] . '/']);
}

nicht_gefunden();
