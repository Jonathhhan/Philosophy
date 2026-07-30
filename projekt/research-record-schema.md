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
- produktive Differenz

## Zulässige Typen

- `invariant`
- `tension`
- `countermodel`
- `principle`
- `cycle`

## Regeln

1. Ein erzeugender Agent bestätigt seinen eigenen Vorschlag nicht.
2. Theoretische Behauptungen benötigen konkrete Quellstellen.
3. Ungelöste starke Einwände bleiben bei jeder Statusänderung erhalten.
4. Manuskriptintegration erfolgt grundsätzlich erst nach projektweiter und kritischer Prüfung.
5. Ein leerer Lauf wird als `no_productive_difference` dokumentiert.
6. Statusstufen dürfen nicht übersprungen werden.

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
productive_difference: Verbindet Organisation und Verteilung durch einen allgemeinen Selektionssatz.
```