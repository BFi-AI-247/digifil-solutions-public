<?php
// Blattwerk – Passwort-Tür für <pfad>/vorschau/ (Vorschau-Stand)
// Wird als <pfad>/vorschau/index.php hochgeladen; dieselbe Anmeldung wie die Live-Fassung.
declare(strict_types=1);
require __DIR__ . '/../lib.php';
bw_tuer('app-vorschau.html', BW_PFAD . 'vorschau/');
