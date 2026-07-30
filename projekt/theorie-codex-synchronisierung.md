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

## Längere produktive Ketten

Bei Eingriffen über mehrere Theorie- oder Projektebenen reicht die allgemeine rekursive Bewegung nicht als Ablaufbeschreibung. Dann gilt zusätzlich die Kettenlogik aus `projekt/produktive-ketten.md`.

Zwischen Kritik, Urteil, Revision und Reorganisation liegen unterscheidbare Schwellen. Codex muss für jede Schwelle einen eigenen Output nachweisen:

1. **Anschließen:** Evidenz, Textanker oder verbindliche Entscheidung;
2. **Rekonstruieren:** bestimmte Relation zwischen Bedingungen, Vollzügen und Folgen;
3. **Beurteilen:** ausgewiesener Maßstab, Gewichtung oder dokumentierter Entscheidungsstatus;
4. **Revidieren:** konkret erneut bestimmte stabilisierte Anschlussbedingung;
5. **Reorganisieren:** geprüfte und gegebenenfalls veränderte Folgebeziehungen;
6. **Kritisieren:** neue produktive Frage, bestätigte Tragfähigkeit oder begründete Blockierung.

Ein Schritt darf den nächsten nicht durch sprachliche Plausibilität ersetzen. Sichtbarkeit ist kein Urteil, ein Urteil ist keine Revision, und eine Änderung mehrerer Dateien ist nicht allein deshalb eine Reorganisation.

Rückläufe sind nur zulässig, wenn eine neue Differenz angegeben wird. Dazu zählen neue Evidenz, ein bisher unbeachteter Widerspruch, eine veränderte Relation, ein neuer Maßstab oder eine unerwartete Folge. Die bloße Möglichkeit weiterer Fragen oder die Erzeugung eines zusätzlichen Audits genügt nicht.

Der ausführbare Prüfer ist:

```powershell
python scripts\produktive_kette.py "Gegenstand" `
  --input recovered\state\kette.json `
  --output recovered\proposals\kettenlauf.md
```

Der Theorie–Codex-Synchronisierer prüft den gemeinsamen Status; der Kettenprüfer kontrolliert die Übergänge innerhalb eines längeren Laufs. Keines der Werkzeuge ersetzt die philosophische Beurteilung.

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
4. vor dem Abschluss eines automatisierten Automatenlaufs;
5. vor und nach einer längeren produktiven Kette.

Ein erfolgreicher Lauf ersetzt weder Quellenprüfung noch philosophische Beurteilung. Er stellt sicher, dass Codex nicht nach anderen Regeln arbeitet als das Projekt, das Codex bearbeitet.
