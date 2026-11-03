<?php
// Tests für kanon_basis.php – Aufruf: php kanon/kanon_01_single_agent/tests/test_kanon_basis.php (Ende „OK“)
declare(strict_types=1);
$_SERVER['SCRIPT_FILENAME'] = __FILE__;
require __DIR__ . '/../kanon_basis.php';

$fehler = 0;
function pruefe(bool $ok, string $was): void { global $fehler; if (!$ok) { $fehler++; echo "FEHLER: $was\n"; } }

pruefe(kanon_regelstand("Regelstand: 2026-10-27b\n# R") === '2026-10-27b', 'Regelstand lesen');
pruefe(kanon_regelstand("# ohne") === null, 'ohne Regelstand');
pruefe(kanon_regelstand_ok(['regelstand' => ' 2026-10-27b'], '2026-10-27b'), 'Regelstand bestätigt');
pruefe(!kanon_regelstand_ok(['regelstand' => '2026-10-27a'], '2026-10-27b'), 'falscher Regelstand');
pruefe(!kanon_regelstand_ok('kein json', '2026-10-27b'), 'kein Objekt');

pruefe(kanon_pflichtfelder(['a' => 'x', 'b' => []], ['a' => 'string', 'b' => 'array', 'c' => 'string?']) === [], 'Pflichtfelder ok');
pruefe(count(kanon_pflichtfelder(['a' => 1], ['a' => 'string', 'b' => 'array'])) === 2, 'Pflichtfelder fehlen/Typ');

pruefe(count(kanon_marker_offen('Text ⟦Vorschlag: 1902⟧')) === 1, 'Marker');
pruefe(kanon_zahlen_ohne_beleg('in seinen 20ern', ['meinen 20ern']) === [], 'Zahl belegt');
pruefe(kanon_zahlen_ohne_beleg('in den 2000ern', ['meinen 20ern']) === ['2000'], 'Zahl unbelegt');
pruefe(kanon_zahlen_ohne_beleg("1. a\n2. b", []) === [], 'Listennummern');
pruefe(kanon_sperrtreffer('Mit Anna', ['anna', 'Ben']) === ['anna'], 'Sperre');
pruefe(kanon_sperrtreffer('Annabell', ['Anna']) === [], 'Sperre ganzes Wort');
pruefe(count(kanon_behauptungen('Ich habe den Abend gelöscht.')) === 1, 'Behauptung');
pruefe(kanon_behauptungen('Wenn du bestätigst, wird er gelöscht.') === [], 'keine Behauptung');
pruefe(kanon_bekannt('a1', ['a1', 'a2']) && !kanon_bekannt('a9', ['a1']) && !kanon_bekannt(null, []), 'bekannte IDs');
pruefe((bool)preg_match('/\+0[12]:00$/', kanon_jetzt()), 'Zeitzone');
$tmp = sys_get_temp_dir() . '/kanon_protokoll_' . getmypid() . '.md'; @unlink($tmp);
$s = new DateTimeImmutable('2026-10-28 20:47:03', new DateTimeZone('Europe/Berlin'));
pruefe(kanon_laufzeile($tmp, $s, $s->modify('+12 seconds'), 'Kommentar', '2026-10-28a', 'ok', 'a | b'), 'Protokoll anlegen');
pruefe(kanon_laufzeile($tmp, $s, $s->modify('+5 minutes'), 'Kommentar', '2026-10-28a', 'fehler', "x\ny"), 'Protokoll anhängen');
$z = explode("\n", trim((string)file_get_contents($tmp)));
pruefe($z[0] === '# Laufprotokoll' && end($z) === '| 2026-10-28 20:47:03 CET (gemessen) | 5 min | Kommentar | 2026-10-28a | fehler | x y |', 'Protokoll Zeile');
pruefe(in_array('| 2026-10-28 20:47:03 CET (gemessen) | 12 s | Kommentar | 2026-10-28a | ok | a / b |', $z, true), 'Protokoll Zelle maskiert');
pruefe(!kanon_laufzeile($tmp, $s, $s, 'x', 'y', 'vielleicht', 'z'), 'Protokoll Ergebnis nur ok/fehler');
@unlink($tmp);
$b = kanon_beleg('2026-10-27b', 'mistral-large-latest', true, ['x']);
pruefe($b['modell'] === 'mistral-large-latest (Konfiguration)' && $b['bestaetigt'] === true, 'Beleg');

echo $fehler ? "$fehler Fehler\n" : "OK\n";
exit($fehler ? 1 : 0);
