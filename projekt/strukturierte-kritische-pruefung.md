# Strukturierte kritische Prüfung

## Zweck

Die autonome Theoriegenese weist zunächst nur nach, dass ein Lauf neue strukturierte Unterschiede erzeugt hat. Daraus folgt noch weder Projektbezug noch philosophische Tragfähigkeit.

Der nachgeschaltete Prüfer `automation/structured_reviewer.py` trennt deshalb drei Ebenen:

1. **Neuheit**: Ist gegenüber dem bisherigen Lauf eine neue strukturierte Relation, Definition, Revision oder Gegenmodellbildung entstanden?
2. **Projektbezug**: Bearbeitet das Ergebnis tatsächlich den Gegenstand und die geschützten Relationen des Projekts?
3. **Philosophische Produktivität**: Erhöht das Ergebnis die Erklärungs-, Unterscheidungs- oder Revisionskraft und hält es einer Gegenprüfung stand?

## Aufruf

```powershell
python automation\structured_reviewer.py generated\active\theories\<lauf>.yaml --validate-only
python automation\structured_reviewer.py generated\active\theories\<lauf>.yaml
```

Der Prüfer verwendet denselben konfigurierten Modellzugang wie der Generator:

- `GENERATIVE_API_ENDPOINT`
- `GENERATIVE_API_KEY`
- `GENERATIVE_MODEL`

## Ergebnis

Neben dem Generationsdatensatz entsteht:

```text
<lauf>-review.yaml
```

Die Prüfung enthält mindestens:

- empfohlener Status `generated`, `proposal` oder `rejected`,
- getrennte Bewertungen von Neuheit, Projektbezug und philosophischer Produktivität,
- bestätigte und verworfene Relationen,
- starke Einwände,
- Gegenmodellresultate,
- notwendige Revisionen,
- aufgelöste und neue Bindungseinträge,
- sowie eine Markierung notwendiger Autorenentscheidungen.

## Statusgrenze

`proposal` ist nur zulässig, wenn die philosophische Produktivität als `supported` bewertet wurde und kein ungelöster starker Einwand verbleibt. Der Prüfer verändert weder Manuskript noch bestätigten Wissensbestand.

## Verhältnis zum Generator

```text
Generator
  -> strukturierte Neuheit
  -> kritischer Prüfer
  -> Projektbezug
  -> philosophische Produktivität
  -> proposal | generated | rejected
```

Damit wird die Selbstbeschreibung `productive_difference` weder verworfen noch mit Erkenntnis gleichgesetzt. Sie bleibt eine Behauptung des erzeugenden Laufs, die durch eine getrennte Prüfung bewertet wird.
