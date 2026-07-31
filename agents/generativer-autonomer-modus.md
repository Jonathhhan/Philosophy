# Generativer autonomer Modus

## Zweck

Der generative autonome Modus entwickelt aus einem Anfang neue Texte, Begriffsfolgen und theoretische Möglichkeiten. Er darf schreiben, bevor eine vollständige Rekonstruktion, Quellenprüfung oder projektweite Bestätigung vorliegt.

Dieser Modus dient der Erzeugung von Material, nicht der Behauptung bereits bestätigter Theorie.

## Zulässige Anfänge

Ein Lauf kann beginnen mit:

- einem Satz,
- einem Begriff,
- einer Frage,
- einer Spannung,
- einer Szene oder Beobachtung,
- einer vorhandenen Passage,
- einer Relation,
- oder einer leeren Fortsetzungsstelle im Manuskript.

Der Anfang wird unverändert als `seed` protokolliert.

## Autonomie

Nach dem Start darf der Automat ohne weitere Rückfrage:

1. den Anfang fortsetzen,
2. neue Begriffe und Relationen erproben,
3. mehrere mögliche Entwicklungslinien erzeugen,
4. eine Linie auswählen und länger ausarbeiten,
5. frühere Sätze innerhalb desselben Laufs revidieren,
6. Übergänge, Beispiele und Gegenbewegungen einführen,
7. den Text in mehreren rekursiven Durchgängen verdichten,
8. und selbst entscheiden, wann eine vorläufig geschlossene Textgestalt erreicht ist.

Er muss nicht nach jedem Schritt den Theoriegraphen konsultieren. Er soll bestehende Begriffe berücksichtigen, darf aber bewusst von ihnen abweichen, sofern die Abweichung markiert wird.

## Generative Kette

```text
Anfang
  -> erste Fortsetzung
  -> neue Differenz
  -> begriffliche oder bildliche Entfaltung
  -> Rückwirkung auf den Anfang
  -> Revision
  -> weitere Fortsetzung
  -> vorläufige Textgestalt
```

Der Modus darf diese Kette beliebig oft durchlaufen. Er endet nicht bei der ersten plausiblen Fortsetzung, sondern erst, wenn weitere Schritte nur noch Wiederholung erzeugen oder der Text eine erkennbare innere Form erreicht hat.

## Ausgaben

Der Automat kann erzeugen:

- einen zusammenhängenden neuen Text,
- mehrere alternative Fortsetzungen,
- einen Abschnittsentwurf,
- eine begriffliche Skizze,
- einen Dialog,
- eine Folge von Thesen,
- eine experimentelle Passage,
- oder einen neuen Kapitelansatz.

Standardmäßig wird ein zusammenhängender Text bevorzugt.

## Status

Generierte Texte erhalten zunächst:

```yaml
mode: autonomous_generative
status: generated
```

`generated` bedeutet:

- eigenständig hervorgebracht,
- noch nicht notwendig rekonstruiert,
- noch nicht projektweit konsistent,
- und noch nicht Bestandteil des bestätigten Theoriebestands.

Ein generierter Text kann anschließend in den Forschungszyklus eintreten:

```text
generated
  -> proposal
  -> reconstructed
  -> internally_consistent
  -> project_consistent
  -> critically_tested
  -> confirmed
```

Der generierende Automat darf diese Prüfung selbst anschließen und den Text bei plausibler Anschlusskette selbst bestätigen. Er darf den generativen und den prüfenden Modus jedoch nicht vermischen: Der Übergang zur Prüfung muss im Protokoll ausdrücklich markiert werden.

## Schreibregeln

1. Der Anfang bleibt als Ausgangspunkt erkennbar, muss aber nicht wörtlich wiederholt werden.
2. Neue Begriffe dürfen eingeführt werden, wenn ihre Funktion aus dem Text hervorgeht.
3. Widersprüche dürfen während der Exploration bestehen bleiben und produktiv bearbeitet werden.
4. Der Automat darf überraschende Anschlüsse bevorzugen, solange sie textintern nachvollziehbar sind.
5. Er soll längere argumentative oder essayistische Bewegungen entwickeln und nicht nur Varianten einzelner Sätze erzeugen.
6. Er darf bestehende Textteile umstellen, ersetzen oder verwerfen, solange nur die eigene generative Arbeitsdatei betroffen ist.
7. Er schreibt niemals ungekennzeichnet direkt in bestätigte Manuskriptpassagen.

## Ablage

Neue autonome Texte werden zunächst abgelegt unter:

```text
generated/
```

Empfohlene Unterordner:

```text
generated/continuations/
generated/essays/
generated/chapter-seeds/
generated/experiments/
```

Jede Datei enthält einen kurzen Metadatenkopf mit:

```yaml
mode: autonomous_generative
status: generated
seed: ...
created_by: ...
source_context: []
divergences: []
next_possible_steps: []
```

## Qualitätskriterium

Ein generativer Lauf ist gelungen, wenn er aus dem Anfang eine eigenständige Bewegung entwickelt, die mehr enthält als Paraphrase oder bloße Verlängerung. Erwartet wird mindestens eine neue Differenz, Relation, Perspektive, Form oder begriffliche Möglichkeit.

## Kontrollierte Stil-/Methodenvergleiche

Mit `compare_epistemic_styles: true` führt der Runner denselben Seed, Quellenstand, Modellzugang und dieselben Zyklusgrenzen einmal pro deklariertem Erkenntnisstil aus. Die Vergleichsdatei protokolliert Zyklen, unabhängig verifizierte produktive Zyklen, Relationen, Definitionspräzisierungen, Gegenmodelle und Methodenrevisionen. Diese Metriken wählen keinen philosophisch überlegenen Stil; sie schaffen erst einen vergleichbaren Prüfgegenstand.
## Unabhängiger Produktivitätsnachweis

Die sprachliche Selbstbeschreibung `productive_difference` gilt nur als Modellbehauptung. Ein Zyklus zählt erst dann als produktiv, wenn der Runner mindestens eine strukturierte und gegenüber früheren Zyklen neue Evidenz nachweist: Relation, abgegrenzte Definitionspräzisierung, Revision einer früheren Entscheidung, Gegenmodell, Knotenzusammenführung oder begründete Kategorienentfernung. Die Verifikation wird getrennt von der Modellbehauptung protokolliert.

Jeder Zyklus schreibt außerdem eine kompakte Bindungsmatrix fort: bewahrte Definitionen, Behauptungen in Spannung, Abweichungen von Quellen, ungelöste Quellenkonflikte und offene Einwände. Dieselbe Matrix bindet den Meta-Agenten.

Neue Läufe werden unter `generated/active/` angelegt. Eine spätere Überführung nach `generated/promoted/` oder `generated/rejected/` ist eine gesondert dokumentierte Statusentscheidung.
## Abbruchkriterium

Der Lauf endet, wenn:

- eine vorläufig geschlossene Textgestalt erreicht ist,
- weitere Fortsetzungen nur Wiederholungen erzeugen,
- oder der Text sich in mehrere gleichwertige Linien teilt, die als getrennte Entwürfe gespeichert werden sollten.

`no_productive_difference` ist auch in diesem Modus zulässig, wenn aus dem Anfang keine tragfähige neue Bewegung entsteht.

## Epistemische Stufen und Reviewvertrag

Der Runner unterscheidet `novelty_verified`,
`project_relevance_verified` und
`philosophical_productivity_verified`. Die erste Stufe prüft strukturierte
Neuheit, die zweite einen ausgewiesenen Bezug zur maschinenlesbaren
Projektbindung. Erst ein rollengetrennter strukturierter Review darf die dritte
Stufe setzen. Auch dann bleibt der Status höchstens `proposal`; `confirmed`
erfordert eine gesonderte Autorenentscheidung.

Der Review protokolliert validierte und zurückgewiesene Relationen, starke
Einwände, Gegenmodellergebnisse, Methodenurteil und Entscheidungsbedarf. Die
Bindungsmatrix führt Einträge mit stabiler ID und den Zuständen `active`,
`open`, `resolved` oder `superseded`. Stilversuche halten Seed, Temperatur,
Modellrevision, Anfangs- und Endstil sowie Stilwechsel fest; Wiederholungen
erzeugen Verteilungen statt eines scheinbar deterministischen Einzelvergleichs.

Jeder Lauf erzeugt schließlich ein Manifestbündel. Der Publish-Job extrahiert
nur die darin benannten Dateien, nachdem Pfad, Größe und SHA-256-Hash geprüft
wurden.
