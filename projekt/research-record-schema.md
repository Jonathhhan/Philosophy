# Schema für Forschungsdatensätze

## Statusfolge

`hypothesis -> proposal -> reconstructed -> internally_consistent -> project_consistent -> critically_tested -> confirmed`

Jeder Status kann in `rejected` übergehen. Ein bestätigter Satz kann durch neue Kritik wieder auf `proposal` zurückgesetzt werden.

## Gemeinsame Pflichtfelder

Jeder Forschungsdatensatz enthält:

- eindeutige Kennung
- Typ
- Status
- Behauptung oder Gegenstand
- konkrete Quellstellen
- bekannte Grenzen
- offene Einwände
- erzeugender Agent
- prüfender Agent
- Prüfmodus (`independent_review` oder `self_review`)
- Begründung der Anschlussplausibilität
- Revisionsbedingungen
- produktive Differenz

## Zulässige Typen

- `invariant`
- `tension`
- `countermodel`
- `principle`
- `cycle`

## Regeln

1. Ein erzeugender Agent darf seinen eigenen Vorschlag bestätigen, wenn er `review_mode: self_review` setzt und die Plausibilität des Anschlusses vollständig dokumentiert.
2. Für eine Selbstbestätigung müssen Anschlusskette, Begriffskonsistenz, projektweite Prüfung, mindestens ein ernsthaftes Gegenmodell oder Gegenbeispiel, bekannte Grenzen und Revisionsbedingungen festgehalten sein.
3. Ein ungelöster starker Einwand verhindert den Status `confirmed`, unabhängig vom Prüfmodus.
4. Theoretische Behauptungen benötigen konkrete Quellstellen.
5. Ungelöste Einwände bleiben bei jeder Statusänderung erhalten.
6. Manuskriptintegration erfolgt grundsätzlich erst nach projektweiter und kritischer Prüfung.
7. Ein leerer Lauf wird als `no_productive_difference` dokumentiert.
8. Statusstufen dürfen nur dann zusammengefasst werden, wenn die jeweils erforderlichen Prüfungen im selben Lauf explizit protokolliert sind.

## Beispiel

```yaml
id: invariant-organisation-selection-001
type: invariant
status: hypothesis
claim: Jede Organisation stabilisiert bestimmte Anschlüsse, indem sie andere unwahrscheinlicher macht.
scope: soziale, technische und ästhetische Anschlussordnungen
source_locations:
  - manuskript/11-organisieren.md
  - manuskript/12-verteilen.md
limits: []
open_objections:
  - Ist negative Selektion für jede Form von Organisation notwendig?
created_by: invarianten-agent
reviewed_by: null
review_mode: null
connection_plausibility: null
revision_conditions: []
productive_difference: Verbindet Organisation und Verteilung durch einen allgemeinen Selektionssatz.
```

## Beispiel einer Selbstbestätigung

```yaml
status: confirmed
created_by: invarianten-agent
reviewed_by: invarianten-agent
review_mode: self_review
connection_plausibility:
  chain:
    - Organisation stabilisiert Anschlussbedingungen.
    - Stabilisierung macht einige Fortsetzungen wahrscheinlicher als andere.
    - Diese Differenz erscheint als Verteilung von Anschlusschancen.
  project_check: passed
  countermodel_check: passed_with_limits
  unresolved_strong_objections: []
revision_conditions:
  - Ein Fall von Organisation ohne selektive Wirkung wird nachgewiesen.
  - Die Relation widerspricht einer stärkeren bestätigten Erklärung.
```
