# Produktive Ketten für Theorie- und Codex-Arbeit

## Zweck

Längere Arbeitsketten verbinden mehrere eigenständige Operationen, ohne ihre Unterschiede einzuebnen. Sie dienen dazu, einen Befund über mehrere begründete Übergänge bis zu einer Manuskriptänderung oder Reorganisation zu verfolgen.

Die Kette ist weder ein freies Assoziieren noch eine Pflicht, jeden Gegenstand durch sämtliche Kapitelbegriffe zu führen. Sie wird verwendet, wenn eine Änderung mehrere Theorie- oder Projektebenen berührt und ein lokaler Patch ihre Folgen nicht hinreichend erfasst.

## Verbindliche Kette

1. **Anschließen** – Auftrag, Textanker, Quellen, bestätigte Entscheidungen und betroffene Dateien aufnehmen.
2. **Rekonstruieren** – die relevante Beziehung zwischen Bedingungen, Vollzügen und Folgen ausweisen.
3. **Beurteilen** – Maßstab, Vergleich und Gewichtung bestimmen oder eine erforderliche Autorenentscheidung kenntlich machen.
4. **Revidieren** – die konkrete stabilisierte Bedingung erneut bestimmen.
5. **Reorganisieren** – prüfen und gegebenenfalls verändern, wie mehrere Bedingungen nach der Revision zusammenwirken.
6. **Kritisieren** – die hervorgebrachte Ordnung auf neue Folgen, Ausschlüsse, Widersprüche und Statusverschiebungen prüfen.

Die Stellung von `Kritisieren` am Ende bezeichnet die rekursive Abschlussprüfung. Im Theoriegang kann Kritik zugleich den Anfang einer Kette bilden. Codex muss deshalb kenntlich machen, ob eine Kritik einen Gegenstand eröffnet oder einen bereits ausgeführten Eingriff erneut prüft.

## Erforderliche Outputs

Jede Schwelle erzeugt einen anderen Output:

| Schwelle | Erforderlicher Output |
|---|---|
| Anschließen | Evidenz, Textanker oder verbindliche Projektentscheidung |
| Rekonstruieren | bestimmte Relation mit ausgewiesener Grundlage |
| Beurteilen | Maßstab, Gewichtung oder dokumentierter Entscheidungsstatus |
| Revidieren | konkret veränderte stabilisierte Anschlussbedingung |
| Reorganisieren | veränderte oder ausdrücklich unveränderte Folgebeziehungen |
| Kritisieren | neue produktive Frage, bestätigte Tragfähigkeit oder begründete Blockierung |

Ein Output darf den nächsten nicht simulieren. Insbesondere gilt:

- Sichtbarkeit ist noch kein Urteil.
- Ein Urteil ist noch keine Revision.
- Eine Textänderung ist noch keine Reorganisation.
- Eine neue Frage ist noch keine produktive Differenz.

## Produktive Differenz

Eine Kette darf sich nur fortsetzen oder zu einer früheren Schwelle zurückkehren, wenn mindestens eines neu entstanden ist:

- eine bisher nicht berücksichtigte Textstelle oder Quelle;
- eine neue, typisierte Relation;
- ein Widerspruch zwischen bestätigten Aussagen;
- ein ausgewiesener Maßstab oder eine bestätigte Entscheidung;
- eine veränderte Anschlussbedingung;
- eine veränderte Beziehung mehrerer Bedingungen;
- eine Folge, die aus dem vorherigen Stand nicht erfasst wurde.

Die bloße Erzeugung weiterer Formulierungen, Varianten, Auditdateien oder Agentenantworten ist keine produktive Differenz.

## Rückläufe

Rückläufe sind erlaubt, aber adressiert:

- von Revidieren zu Rekonstruieren, wenn der Revisionsgegenstand falsch bestimmt wurde;
- von Reorganisieren zu Beurteilen, wenn relationale Folgen den Maßstab verändern;
- von Kritisieren zu Anschließen, wenn neue Evidenz oder eine neue betroffene Stelle gefunden wurde;
- von jeder Schwelle zu BLOCKED, wenn Evidenz, Quelle oder Entscheidung fehlt.

Ein Rücklauf wiederholt nicht denselben Auftrag. Er nennt die neue Differenz, die frühere Ausgabe und die Stelle, an der diese Ausgabe nicht mehr trägt.

## Automatisierter Lauf

`scripts/produktive_kette.py` validiert eine Kette aus JSON-Eingaben. Für jede Schwelle werden `status`, `output_kind`, `output`, Evidenz sowie eröffnete und blockierte Möglichkeiten erfasst.

Beispielstruktur:

```json
{
  "stages": [
    {
      "status": "productive",
      "output_kind": "evidence",
      "output": "Kapitel 12 und 13 verwenden verschiedene Definitionen von Verteilen.",
      "evidence": ["manuskript/12-verteilen.md", "manuskript/13-asymmetrie.md"]
    },
    {
      "status": "productive",
      "output_kind": "relation",
      "output": "Die Folgekapitel reproduzieren die alte Definition und verschieben damit den Gegenstand der Verteilung."
    }
  ]
}
```

Aufruf:

```powershell
python scripts\produktive_kette.py "Verteilen und Asymmetrie" `
  --input recovered\state\verteilen-kette.json `
  --output recovered\proposals\verteilen-kettenlauf.md
```

Der Zustand wird standardmäßig unter `recovered/state/produktive-ketten.json` gespeichert. Bereits bekannte produktive Outputs gelten nicht erneut als neue Differenz.

## Status und Entscheidung

- `productive`: Die Schwelle besitzt den erforderlichen Output und verändert die weitere Bearbeitung.
- `review`: Der Output ist vorhanden, aber noch nicht hinreichend bestimmt oder bestätigt.
- `blocked`: Evidenz, Quelle, Entscheidung oder zulässiger Eingriff fehlt.
- `exhausted`: Die vollständige Kette erzeugt gegenüber dem gespeicherten Stand keine neue Differenz.

Nur eine produktive Kette darf eine weiter reichende Integration begründen. Ein lokaler, bereits bestätigter Patch benötigt nicht künstlich eine vollständige Kette.

## Verhältnis zur Theorie

Die Arbeitsweise ist durch die Theorie orientiert, aber nicht mit ihr identisch. `Anschließen`, `Beurteilen`, `Revidieren` und `Reorganisieren` besitzen im Manuskript eigenständige begriffliche Funktionen. Die Codex-Kette verwendet diese Unterschiede als Prüfdisziplin für Projektarbeit. Ein erfolgreicher technischer Lauf beweist keine philosophische These.
