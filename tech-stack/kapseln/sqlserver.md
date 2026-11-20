# Kapsel sqlserver 0.4.0

Lesender Zugriff auf einen SQL Server mit der Windows-Anmeldung. Wahlweise.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt, wie ein lokales Werkzeug Daten aus einem SQL Server liest, ohne Kennwort in einer Datei.
GILT FÜR:     Rezepte lokal-python und lokal-powershell, wenn das Werkzeug Daten aus einem SQL Server braucht.
BRAUCHT:      Kapseln kern · lokal-befehle
```

### REGELN
- 1 Nur lesend, mit Windows-Anmeldung; kein Kennwort in einer Datei. Server- und Datenbankname stehen nur in der
  Einstellung auf dem Zielrechner.
- 2 Python: `pyodbc` mit `Trusted_Connection=yes`. Treiber in dieser Reihenfolge: „ODBC Driver 18 for SQL Server“, „ODBC
  Driver 17 for SQL Server“, „SQL Server Native Client 11.0“, „SQL Server“. Fehlt ein Treiber oder scheitert TLS, dann
  nimm den nächsten. Setz `TrustServerCertificate=yes`, beim Treiber 18 zusätzlich `Encrypt=no`. Der Treiber gehört zum
  Rechner, nicht zum Werkzeug.
- 3 PowerShell: `System.Data.SqlClient` aus dem .NET Framework mit `Integrated Security=SSPI`; kein zusätzlicher Treiber.
- 4 Setz Zeitgrenzen für Anmeldung und Abfrage; die Abfrage läuft neben dem Server (Kapsel lokal-befehle), nie in der
  Annahme der Anfragen.
- Grund: Die Windows-Anmeldung hält Kennwörter aus Dateien.
- Fallen: Der Treiber „SQL Server“ liefert Datumsspalten als Text.
- Test: über eine Attrappe (Python: pyodbc-Attrappe auf SQLite); die echte Verbindung prüft der Mensch.
- Stand: Python erprobt · PowerShell: Vorbilder vorhanden (Belege), Stand offen.

## BLOCK B – für Menschen

Das Werkzeug liest Daten aus einer Firmendatenbank mit deinem Windows-Konto. Ein Kennwort steht nirgends, und der Name
des Servers bleibt auf deinem Rechner.
