# Kapsel veroeffentlichung 0.4.0

Eine offene Fassung des Werkzeugs durch Spiegeln in ein öffentliches Repo. Wahlweise.

## BLOCK A – für die bauende KI

```text
ZWECK:        Regelt, wie aus dem privaten Repo eine öffentliche Fassung wird.
GILT FÜR:     jedes Rezept, wahlweise, wenn es eine offene Fassung geben soll.
BRAUCHT:      Kapsel kern
```

### REGELN
- 1 Eine offene Fassung entsteht durch Spiegeln in ein öffentliches Repo. Der Spiegel prüft eine Liste verbotener
  Begriffe (Namen, Orte, Adressen) und bricht bei einem Treffer ab; persönliche Werte stehen deshalb nur in
  Einstellungen (Kapsel kern).
- 2 Code, der in beiden Fassungen gleich ist, wird im privaten Repo gepflegt und gespiegelt, nie im öffentlichen
  geändert.
- 3 Dateien mit internen Namen (z. B. Belege) gehören nicht in die offene Fassung; der Spiegel schließt sie aus.
- Grund: Eine Fassung wird gepflegt, die andere folgt; ein Treffer hält alles an, statt etwas Privates zu zeigen.
- Stand: erprobt.

## BLOCK B – für Menschen

Was öffentlich sein soll, wird aus dem privaten Repo gespiegelt. Steht ein Name oder eine Adresse darin, dann bricht der
Spiegel ab, statt sie zu zeigen.
