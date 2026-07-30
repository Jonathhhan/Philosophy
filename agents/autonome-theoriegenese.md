# Autonome Theoriegenese durch Anschlussentscheidungen

## Grundgedanke

Die Automatisierung soll nicht nur vorhandene Theorie fortschreiben oder einen Anfang stilistisch entfalten. Sie darf aus einem Anfang eine eigenständige Theorie erzeugen, indem sie in jedem Zyklus zwischen mehreren möglichen Anschlüssen entscheidet.

Der Anfang ist dabei weder bloßes Thema noch bereits verbindlicher Grundsatz. Er ist die erste Bedingung eines rekursiven Prozesses, dessen spätere Entscheidungen auf ihn zurückwirken und ihn neu bestimmen können.

## Autonomie

Der Automat darf selbstständig:

- neue Begriffe und Unterscheidungen einführen,
- Begriffe funktional bestimmen,
- Relationen zwischen Begriffen setzen,
- konkurrierende Anschlusslinien erzeugen,
- eine Linie aufgrund ihrer theoretischen Produktivität auswählen,
- frühere Entscheidungen revidieren oder verwerfen,
- lokale Widersprüche als produktive Spannungen erhalten,
- den bisherigen Text grundlegend reorganisieren,
- Gegenbewegungen und Gegenmodelle in die Theorie einbauen,
- und selbst entscheiden, wann weitere Zyklen keine produktive Differenz mehr erwarten lassen.

## Anschlussentscheidung

Jeder Zyklus protokolliert mindestens:

```yaml
cycle: 1
chosen_connection: ...
alternatives_rejected: []
new_concepts: []
new_relations: []
productive_difference: ...
revisions: []
tensions_preserved: []
continue: true
```

Eine Anschlussentscheidung gilt als produktiv, wenn sie mindestens eine der folgenden Leistungen erbringt:

- neue Erklärungsfähigkeit,
- präzisere Unterscheidung,
- Verbindung bislang getrennter Probleme,
- Rekonstruktion einer verdeckten Voraussetzung,
- Widerlegung oder Revision einer früheren Entscheidung,
- Bildung eines tragfähigen neuen Begriffs,
- oder Eröffnung eines neuen prüfbaren Theoriepfads.

Bloße sprachliche Plausibilität reicht nicht aus.

## Verhältnis zum bestehenden Projekt

Die autonome Theoriegenese darf vom vorhandenen Theoriegraphen abweichen. Sie muss Abweichungen während der Generierung nicht vermeiden, sondern als mögliche neue Theoriearchitektur erproben.

Der erzeugte Bestand bleibt zunächst getrennt:

```text
generated/theories/
```

Jeder Lauf erzeugt:

1. einen zusammenhängenden Theorietext,
2. ein Protokoll aller Anschlussentscheidungen,
3. einen vorläufigen Theoriegraphen aus Begriffen und Relationen,
4. optional eine kritische Prüfung.

## Status

Alle Ergebnisse beginnen als:

```yaml
mode: autonomous_theory_generation
status: generated
```

Der Automat darf einzelne Relationen später selbst in den Status `proposal` oder nach vollständiger Prüfung weiter überführen. Der gesamte generierte Text wird jedoch nicht pauschal bestätigt. Bestätigung erfolgt relationen- oder satzweise und bleibt revidierbar.

## Freiheit und Begrenzung

Die Begrenzung der Autonomie besteht nicht in einer inhaltlichen Vorgabe, sondern in vier formalen Bedingungen:

1. Jede wichtige Anschlussentscheidung wird protokolliert.
2. Frühere Entscheidungen bleiben revidierbar.
3. Generierte Theorie wird nicht ungekennzeichnet in Manuskript oder bestätigten Bestand geschrieben.
4. Ein späterer Prüfmodus kann jede Entscheidung einzeln rekonstruieren, kritisieren oder verwerfen.

Dadurch erhält die Automatisierung großen theoretischen Spielraum, ohne die Unterscheidung zwischen Hervorbringung und Bestätigung aufzugeben.
