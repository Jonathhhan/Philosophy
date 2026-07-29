# Schema für Änderungsereignisse

Änderungsereignisse unter `knowledge/change-events/` speichern. Sie dokumentieren größere Aktualisierungen, ohne Git-Diff, Manuskript oder Entscheidungsdatei zu ersetzen.

## Pflichtfelder

| Feld | Form | Bedeutung |
|---|---|---|
| `schema_version` | `1` | Version dieses Schemas |
| `id` | `change-...` | stabiles, eindeutiges Ereigniskennzeichen |
| `created_at` | ISO-Datum | Beginn der Bearbeitung |
| `goal` | Text | beauftragtes Ergebnis |
| `operation` | Enum | primäre Eingriffsklassifikation |
| `scope` | Objekt | erlaubte und geschützte Dateien |
| `basis` | Objekt | Projektdateien, Entscheidungen und Quellen |
| `changes` | Liste | tatsächlich geänderte Dateien und Zusammenfassungen |
| `affected_relations` | Liste | berührte Beziehungen und ihre Veränderung |
| `possibilities` | Objekt | eröffnete, begrenzte und zurückgestellte Möglichkeiten |
| `uncertainties` | Liste | nicht geschlossene Unsicherheiten |
| `agent_findings` | Objekt | nach Rollen getrennte Agentenergebnisse |
| `authority` | Objekt | erforderliche und erteilte Autorenentscheidung |
| `validation` | Liste | Prüfungen, Ergebnisse und Belege |
| `status` | Enum | gegenwärtiger Status des Ereignisses |

## Enumerationen

`operation`: `local_update`, `composition`, `revision`, `reorganization`, `audit`

`affected_relations[].relation`:

- `defines`
- `depends_on`
- `cross_references`
- `sourced_from`
- `documents`
- `renders`
- `tests`
- `constrains`
- `supersedes`
- `other`

`affected_relations[].effect`: `preserved`, `changed`, `added`, `removed`, `uncertain`

`authority.decision_status`: `not_required`, `pending`, `accepted`, `rejected`

`validation[].result`: `passed`, `warning`, `failed`, `not_run`

`status`:

- `proposed`: Umfang und erwartete Folgen sind erst vorläufig bestimmt.
- `tested`: Änderung ist ausgeführt und geprüft, aber noch nicht notwendig bestätigt.
- `confirmed`: erforderliche Autorenentscheidung liegt vor.
- `stabilized`: bestätigte Änderung ist in alle beauftragten Beziehungen integriert und geprüft.
- `revised`: ein früheres Ereignis wurde begründet erneut bestimmt.

## Semantische Regeln

1. Für `revision` und `reorganization` mindestens eine betroffene Beziehung ausweisen.
2. Für `reorganization` mindestens eine Beziehung als `changed`, `added` oder `removed` bestimmen.
3. Nach `proposed` mindestens eine Validierung dokumentieren.
4. Bei `confirmed`, `stabilized` oder `revised` keine fehlgeschlagene Validierung offenlassen.
5. Wenn `requires_author_decision: true` gilt, `confirmed`, `stabilized` oder `revised` nur mit `decision_status: accepted` verwenden.
6. Wenn keine Autorenentscheidung erforderlich ist, `decision_status: not_required` verwenden.
7. Bei `stabilized` mindestens eine tatsächliche Änderung ausweisen; ein reiner Audit stabilisiert keine Projektänderung.
8. Eröffnete Möglichkeiten nicht als automatisch besser und begrenzte Möglichkeiten nicht als automatisch schlechter behandeln. Gründe im Ereignis oder in der zugehörigen Entscheidung ausweisen.

## Relationseintrag

```yaml
- from: manuskript/08-algorithmus.md
  relation: defines
  to: knowledge/concepts/algorithmus.yaml
  effect: preserved
  note: Die Definition bleibt unverändert; ergänzt wird nur ihre operative Prüfung.
```

## Statusübergang

```text
proposed → tested → confirmed → stabilized
                    ↘ revised → tested …
```

`confirmed` überspringen, wenn keine Autorenentscheidung erforderlich ist. Einen zurückgewiesenen Vorschlag nicht stabilisieren; seine Provenienz darf als verworfene Variante erhalten bleiben.
