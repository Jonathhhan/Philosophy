# Schema für Forschungs- und Generationsdatensätze

## Statusfolgen

Für Forschungsbehauptungen:

`hypothesis -> proposal -> reconstructed -> internally_consistent -> project_consistent -> critically_tested -> confirmed`

Für autonom generiertes Material:

`generated -> proposal -> reconstructed -> internally_consistent -> project_consistent -> critically_tested -> confirmed`

Jeder Status kann in `rejected` übergehen. Ein bestätigter Satz kann durch neue Kritik wieder auf `proposal` zurückgesetzt werden. `generated` bezeichnet Material, dessen produktive Hervorbringung dokumentiert ist, dessen theoretische Geltung aber noch nicht vorausgesetzt wird.

## Gemeinsame Pflichtfelder

Jeder Datensatz enthält:

- eindeutige Kennung,
- Typ,
- Status,
- Behauptung, Gegenstand oder erzeugten Text,
- erzeugenden Agenten,
- Arbeitsmodus,
- produktive Differenz,
- und bekannte nächste Schritte.

Für prüfende Forschungsdatensätze kommen hinzu:

- konkrete Quellstellen,
- bekannte Grenzen,
- offene Einwände,
- prüfender Agent,
- Prüfmodus (`independent_review` oder `self_review`),
- Begründung der Anschlussplausibilität,
- und Revisionsbedingungen.

Für autonom generierte Texte kommen hinzu:

- unveränderter Anfang (`seed`),
- verwendeter Kontext,
- eingeführte neue Begriffe oder Relationen,
- markierte Abweichungen vom bestätigten Bestand,
- Anzahl oder Beschreibung der generativen Durchgänge,
- und Abbruchgrund;
- die unabhängige Produktivitätsverifikation je Zyklus;
- die fortgeschriebene Bindungsmatrix;
- sowie Verfassungsverträglichkeit und gefährdete Projektrelationen jeder Meta-Entscheidung.

## Zulässige Typen

- `generated_text`
- `continuation`
- `chapter_seed`
- `experiment`
- `invariant`
- `tension`
- `countermodel`
- `principle`
- `cycle`

## Arbeitsmodi

- `autonomous_generative`: freie autonome Texterzeugung aus einem Anfang.
- `research`: Rekonstruktion, Prüfung und Theorieentwicklung.
- `integration`: Überführung geprüfter Ergebnisse in Theoriegraph, Glossar oder Manuskript.
- `editorial`: sprachliche und strukturelle Ausarbeitung bestätigter oder ausdrücklich ausgewählter Texte.

Ein Datensatz darf den Modus wechseln. Jeder Wechsel wird in `mode_transitions` protokolliert.

## Regeln

1. Im Modus `autonomous_generative` darf ein Automat ohne vorherige Quellen- oder Konsistenzprüfung neue Texte, Begriffe und Relationen erzeugen.
2. Der Anfang muss als `seed` vollständig erhalten und der erzeugte Text zunächst als `generated` gekennzeichnet werden.
3. Generiertes Material darf nicht ungekennzeichnet in bestätigte Manuskriptpassagen übernommen werden.
4. Der generierende Automat darf selbst in den Forschungsmodus wechseln, den Text prüfen und ihn bei plausibler Anschlusskette selbst bestätigen.
5. Ein Moduswechsel von `autonomous_generative` zu `research` muss ausdrücklich protokolliert werden.
6. Ein erzeugender Agent darf seinen eigenen Vorschlag bestätigen, wenn er `review_mode: self_review` setzt und die Plausibilität des Anschlusses vollständig dokumentiert.
7. Für eine Selbstbestätigung müssen Anschlusskette, Begriffskonsistenz, projektweite Prüfung, mindestens ein ernsthaftes Gegenmodell oder Gegenbeispiel, bekannte Grenzen und Revisionsbedingungen festgehalten sein.
8. Ein ungelöster starker Einwand verhindert den Status `confirmed`, unabhängig vom Prüfmodus.
9. Theoretische Behauptungen benötigen spätestens ab `reconstructed` konkrete Quellstellen oder eine explizit dokumentierte interne Herleitung.
10. Ungelöste Einwände bleiben bei jeder Statusänderung erhalten.
11. Manuskriptintegration erfolgt grundsätzlich erst nach projektweiter und kritischer Prüfung oder nach einer ausdrücklich dokumentierten redaktionellen Entscheidung, einen generierten Text als experimentellen Text zu veröffentlichen.
12. Ein leerer Lauf wird als `no_productive_difference` dokumentiert.
13. Statusstufen dürfen nur dann zusammengefasst werden, wenn die jeweils erforderlichen Prüfungen im selben Lauf explizit protokolliert sind.

## Beispiel eines autonom generierten Textes

```yaml
id: generated-continuation-001
type: continuation
mode: autonomous_generative
status: generated
seed: Menschen treten in Gespräche ein, die bereits begonnen haben.
text: |
  ...
created_by: generativer-autonomer-modus
source_context:
  - manuskript/01-anschliessen.md
introduced_concepts:
  - vorlaufender-anschluss
divergences:
  - Der Begriff ist im bestätigten Glossar noch nicht definiert.
generative_passes:
  - Fortsetzung des Anfangs
  - Einführung einer Gegenbewegung
  - Revision des Schlusses
stop_reason: Vorläufig geschlossene essayistische Bewegung erreicht.
productive_difference: Entwickelt aus dem zeitlichen Vorlauf des Gesprächs eine relationale Bedingung von Handlung.
next_possible_steps:
  - Gegenmodell ohne zeitlichen Vorlauf prüfen.
  - Relation zum Begriff Programm rekonstruieren.
mode_transitions: []
```

## Beispiel einer Forschungsbehauptung

```yaml
id: invariant-organisation-selection-001
type: invariant
mode: research
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
next_possible_steps:
  - Gegenmodell prüfen.
mode_transitions: []
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
mode_transitions:
  - from: autonomous_generative
    to: research
    reason: Der generierte Gedanke wurde als prüfbare Invariante formuliert.
```

## Strukturierter Review und Reproduzierbarkeit

Generative Records führen `sampling_seed`, `temperature`, `model_revision`,
`project_binding_provenance` und eine lebenszyklusfähige `binding_matrix`.
`review` ist entweder `null` oder ein Objekt mit `recommended_status`,
`validated_relations`, `rejected_relations`, `strong_objections`,
`countermodel_results`, `method_assessment` und
`requires_author_decision`. Unbekannte Felder sind Vertragsfehler.

Die drei Prüfwerte `novelty_verified`, `project_relevance_verified` und
`philosophical_productivity_verified` dürfen nicht zusammengezogen werden.
Ein Review kann `proposal`, aber nicht automatisch `confirmed` empfehlen.
