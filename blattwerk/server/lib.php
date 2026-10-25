<?php
// Blattwerk – gemeinsame Teile für Passwort-Tür, App-Auslieferung und Rückmeldungen.
// Aufbau auf dem Server:  <web>/<pfad>/lib.php  →  privat: <web>/../privat/blattwerk/ (nicht abrufbar)
// Einstellungen (Pfad, Repo, Name des Betreibers) kommen aus zugang.php, Feld 'einstellungen' (tools/make_zugang.py).
declare(strict_types=1);

const BW_COOKIE = 'bw_zugang';
const BW_TAGE = 180;
function bw_privat(): string { return getenv('BW_PRIVAT') ?: __DIR__ . '/../../privat/blattwerk'; }

/** Einstellungen mit Vorgaben; überschreibbar über zugang.php → 'einstellungen' */
function bw_einstellung(string $k): string {
    static $e = null;
    if ($e === null) {
        $z = @include bw_privat() . '/zugang.php';
        $e = array_merge(['pfad' => '/blattwerk/', 'repo' => '', 'betreiber' => 'dem Betreiber'],
            (is_array($z) && is_array($z['einstellungen'] ?? null)) ? $z['einstellungen'] : []);
    }
    return (string)($e[$k] ?? '');
}
define('BW_PFAD', bw_einstellung('pfad'));
define('BW_REPO', bw_einstellung('repo'));

function bw_header(): void {
    header('X-Robots-Tag: noindex, nofollow');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: same-origin');
    header('X-Frame-Options: SAMEORIGIN');
}

/** Lädt zugang.php: ['salt', 'hash', 'key', 'gh' (optional)] oder null */
function bw_zugang(): ?array {
    $z = @include bw_privat() . '/zugang.php';
    return (is_array($z) && !empty($z['hash']) && !empty($z['key'])) ? $z : null;
}
function bw_token(string $key, int $bis): string { return $bis . '.' . hash_hmac('sha256', 'blattwerk|' . $bis, $key); }
function bw_gueltig(array $z): bool {
    $wert = (string)($_COOKIE[BW_COOKIE] ?? '');
    $teile = explode('.', $wert, 2);
    if (count($teile) !== 2 || !ctype_digit($teile[0])) return false;
    $bis = (int)$teile[0];
    return $bis >= time() && hash_equals(bw_token($z['key'], $bis), $wert);
}
function bw_setze(string $wert, int $bis): void {
    setcookie(BW_COOKIE, $wert, ['expires' => $bis, 'path' => BW_PFAD, 'secure' => true, 'httponly' => true, 'samesite' => 'Lax']);
}

/** Passwort-Tür: zeigt die Anmeldung oder liefert die App-Datei aus dem privaten Ordner */
function bw_tuer(string $appDatei, string $hier): void {
    bw_header();
    $z = bw_zugang();
    if (!$z) { http_response_code(503); bw_seite('Noch nicht eingerichtet', '<p>Der Zugang ist noch nicht eingerichtet. Bitte ' . htmlspecialchars(bw_einstellung('betreiber')) . ' Bescheid geben.</p>'); return; }
    if (isset($_GET['abmelden'])) { bw_setze('', time() - 3600); header('Location: ' . BW_PFAD); return; }
    $fehler = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $pw = (string)($_POST['passwort'] ?? '');
        if ($pw !== '' && hash_equals($z['hash'], hash_pbkdf2('sha256', $pw, $z['salt'], 100000, 64))) {
            $bis = time() + BW_TAGE * 86400;
            bw_setze(bw_token($z['key'], $bis), $bis);
            header('Location: ' . $hier, true, 303);
            return;
        }
        sleep(2); // bremst Rateversuche
        $fehler = 'Das Passwort stimmt nicht. Bitte noch einmal versuchen.';
    }
    if (bw_gueltig($z)) {
        $app = bw_privat() . '/' . $appDatei;
        if (!is_file($app)) { http_response_code(503); bw_seite('Fehlt', '<p>Diese Fassung ist noch nicht hochgeladen.</p>'); return; }
        header('Content-Type: text/html; charset=utf-8');
        header('Cache-Control: no-store');
        readfile($app);
        return;
    }
    $hinweis = $fehler ? '<p class="fehler" role="alert">' . htmlspecialchars($fehler) . '</p>' : '';
    bw_seite('Anmelden', $hinweis . '
  <form method="post" action="' . htmlspecialchars($hier) . '">
    <label for="pw">Passwort</label>
    <input id="pw" name="passwort" type="password" autocomplete="current-password" required autofocus>
    <button type="submit">Anmelden</button>
  </form>
  <p class="klein">Das Gerät bleibt ' . BW_TAGE . ' Tage angemeldet.</p>');
}

function bw_seite(string $titel, string $inhalt): void {
    header('Content-Type: text/html; charset=utf-8');
    header('Cache-Control: no-store');
    echo '<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow"><title>Blattwerk – ' . htmlspecialchars($titel) . '</title>
<style>
:root{--bg:#edf2f0;--card:#fff;--fg:#16211d;--muted:#5d6b66;--line:#d8e1dd;--accent:#0e7d63;--danger:#b4382c}
@media (prefers-color-scheme:dark){:root{--bg:#111816;--card:#19221f;--fg:#e4ebe8;--muted:#9aaaa4;--line:#2c3a35;--accent:#4cc3a2;--danger:#f08a7b;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--bg);color:var(--fg);
font:16px/1.45 "Avenir Next","Segoe UI",system-ui,sans-serif;padding:24px max(16px,env(safe-area-inset-right)) 24px max(16px,env(safe-area-inset-left))}
main{width:min(380px,100%);background:var(--card);border:1px solid var(--line);border-radius:14px;padding:28px}
h1{margin:0 0 4px;font-size:22px}p{margin:0 0 16px;color:var(--muted)}
form{display:flex;flex-direction:column;gap:8px}label{font-size:14px;color:var(--muted)}
input{min-height:48px;padding:0 12px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--fg);font:inherit}
button{min-height:48px;border:0;border-radius:10px;background:var(--accent);color:var(--card);font:inherit;font-weight:600;margin-top:8px;cursor:pointer}
.fehler{color:var(--danger)}.klein{font-size:13px;margin:16px 0 0}
</style></head><body><main><h1>Blattwerk</h1><p>Arbeitsblätter für die Grundschule</p>' . $inhalt . '</main></body></html>';
}

/** Antwort als JSON */
function bw_json(int $code, array $daten): void {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($daten, JSON_UNESCAPED_UNICODE);
}

/** GitHub-REST-Aufruf mit dem Schlüssel aus zugang.php */
function bw_github(string $methode, string $pfad, ?array $body, string $token): array {
    $ch = curl_init((getenv('BW_GITHUB_API') ?: 'https://api.github.com') . $pfad); // Umgebungsvariable nur für lokale Tests
    $kopf = ['Accept: application/vnd.github+json', 'Authorization: Bearer ' . $token, 'User-Agent: Blattwerk', 'X-GitHub-Api-Version: 2022-11-28'];
    $opt = [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 20, CURLOPT_CUSTOMREQUEST => $methode, CURLOPT_HTTPHEADER => $kopf];
    if ($body !== null) { $opt[CURLOPT_POSTFIELDS] = json_encode($body, JSON_UNESCAPED_UNICODE); $kopf[] = 'Content-Type: application/json'; $opt[CURLOPT_HTTPHEADER] = $kopf; }
    curl_setopt_array($ch, $opt);
    $antwort = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    return [$status, is_string($antwort) ? json_decode($antwort, true) : null];
}
