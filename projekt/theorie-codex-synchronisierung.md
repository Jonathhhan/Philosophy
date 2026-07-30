# Theorie–Codex-Synchronisierung

Die Theorie des Buches und die Codex-Arbeitsweise sind nicht identisch. Die Theorie beschreibt organisierte Anschlussmöglichkeiten; Codex bearbeitet Dateien. Beide sollen jedoch dieselben bestätigten Relationen, Statusgrenzen und Revisionsbedingungen respektieren.

## Operative Entsprechung

| Theoriebewegung | Codex-Operation | Prüffrage |
|---|---|---|
| Anschließen | Projektstand, Auftrag, Quellen und betroffene Dateien aufnehmen | Woran schließt die Änderung tatsächlich an? |
| Organisieren | Abhängigkeiten, Querverweise und Entscheidungskompetenzen bestimmen | Welche Bedingungen tragen oder begrenzen den Eingriff? |
| Aktualisieren | kleinste hinreichende Änderung ausführen | Welche bestimmte Möglichkeit wird jetzt realisiert? |
| Reorganisieren | Folgen für andere Dateien, Begriffe und Ausgaben integrieren | Welche Beziehungen wurden durch die Änderung verändert? |
| Kritisieren | Widersprüche, Auslassungen, Statusfehler und Blockierungen prüfen | Welche Voraussetzungen und Folgen müssen erneut beurteilt werden? |

Diese Entsprechung ist methodisch. Sie führt keine neue Theorieachse ein und macht technische Operationen nicht zu philosophischen Begriffen.

## Synchronisationsregeln

1. Eine Manuskriptänderung und ihre Codex-Begründung müssen auf dieselben bestätigten Definitionen und Entscheidungen verweisen.
2. Eine Änderung des Begriffsstatus muss zugleich in Manuskript, Glossar, Arbeitsregeln und gegebenenfalls Change Event nachvollziehbar werden.
3. `Vorschlag`, `bestätigt`, `delegierte Codex-Entscheidung`, `KEEP`, `PATCH` und `BLOCKED` dürfen nicht ineinander übergehen.
4. Eine technische Ausgabe darf keinen theoretischen Status stabilisieren, den das Manuskript und die Projektdateien nicht besitzen.
5. Eine rekursive Prüfung läuft weiter, solange sie eine neue Relation, einen neuen Widerspruch oder einen konkreten Patch hervorbringt. Wiederholung allein ist keine produktive Differenz.
6. Der Synchronisierer entscheidet nicht philosophisch. Er blockiert nur Integrationen, deren Theorie- und Arbeitsstatus auseinanderlaufen.

## Automatische Prüfung

```powershell
python scripts\theorie_codex_synchronisierer.py
```

Mit den aktuell geänderten Dateien kann zugleich die Eingriffstiefe bestimmt werden:

```powershell
python scripts\theorie_codex_synchronisierer.py `
  manuskript/12-verteilen.md `
  manuskript/13-asymmetrie.md `
  AGENTS.md
```

JSON-Ausgabe für weitere Automaten:

```powershell
python scripts\theorie_codex_synchronisierer.py --format json
```

Der Prozess liefert einen der Statuswerte:

- `synchronized`: Theoriearchitektur und Codex-Arbeitsweise stimmen für den geprüften Stand überein;
- `review`: eine Status- oder Relationsabweichung verlangt Prüfung;
- `blocked`: eine Manuskriptintegration muss bis zur Synchronisierung ausgesetzt werden.

## Einbindung in den rekursiven Prozess

Der Synchronisierer läuft:

1. vor strukturellen Manuskriptänderungen;
2. nach Änderungen bestätigter Definitionen;
3. nach Reorganisationen über mehrere Dateien;
4. vor dem Abschluss eines automatisierten Automatenlaufs.

Ein erfolgreicher Lauf ersetzt weder Quellenprüfung noch philosophische Beurteilung. Er stellt sicher, dass Codex nicht nach anderen Regeln arbeitet als das Projekt, das Codex bearbeitet.
