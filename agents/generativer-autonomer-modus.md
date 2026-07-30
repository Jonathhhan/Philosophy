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

## Abbruchkriterium

Der Lauf endet, wenn:

- eine vorläufig geschlossene Textgestalt erreicht ist,
- weitere Fortsetzungen nur Wiederholungen erzeugen,
- oder der Text sich in mehrere gleichwertige Linien teilt, die als getrennte Entwürfe gespeichert werden sollten.

`no_productive_difference` ist auch in diesem Modus zulässig, wenn aus dem Anfang keine tragfähige neue Bewegung entsteht.