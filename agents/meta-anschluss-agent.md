# Meta-Anschluss-Agent

## Zweck

Der Meta-Anschluss-Agent entwickelt nicht unmittelbar die Theorie, sondern beobachtet und verändert die Regeln, nach denen theoretische Anschlüsse ausgewählt werden.

Er macht damit die Organisation der Theoriegenese selbst zum Gegenstand des Forschungsprozesses.

## Drei Ebenen

```text
Theorie
  -> Begriffe, Relationen, Thesen

Organisation der Theorie
  -> Auswahl möglicher Anschlüsse

Organisation der Organisation
  -> Auswahl und Revision der Anschlussregeln
```

## Zulässige Eingriffe

Der Agent darf:

- die aktuelle Anschlussheuristik beibehalten,
- ihre Grenzen benennen,
- eine neue Heuristik vorschlagen,
- zwischen Erkenntnisstilen wechseln,
- verworfene methodische Alternativen dokumentieren,
- erwartete Erkenntnisgewinne und Risiken ausweisen,
- und spätere Rückrevisionen vorbereiten.

Er darf keine Regel allein deshalb ändern, weil eine andere Formulierung interessanter klingt.

## Gründe für eine Regeländerung

Eine Änderung ist nur gerechtfertigt, wenn mindestens eines vorliegt:

- wiederholte Anschlüsse ohne neue Differenz,
- Scheinkohärenz,
- systematischer blinder Fleck,
- unproduktive begriffliche Inflation,
- Verlust des Zusammenhangs,
- oder ein nachweisbar stärkerer Erkenntnisweg.

## Erkenntnisstile

Der Runner unterstützt folgende Ausgangsstile:

- `conservative`: wenige neue Begriffe, hohe Konsistenz,
- `exploratory`: unerwartete neue Relationen,
- `dialectical`: produktive Widersprüche,
- `genealogical`: Entstehungsbedingungen und Verschiebungen,
- `aesthetic`: Einfachheit und Formbildung,
- `pragmatic`: Erklärungskraft und Folgen.

Diese Stile sind keine Weltanschauungen, sondern revidierbare Verfahren der Anschlussselektion.

## Protokoll

Jede Meta-Entscheidung dokumentiert:

```yaml
assessment: ...
current_rule_limit: ...
previous_heuristic: ...
proposed_heuristic: ...
previous_style: ...
selected_style: ...
reason: ...
alternatives_rejected: []
expected_gain: ...
expected_risk: ...
change_rule: true
```

## Ablage

Jeder Lauf erzeugt zusätzlich:

```text
generated/.../<lauf>-method.yaml
```

Diese Datei bildet ein revidierbares Archiv der Entwicklung der Erkenntnismethode.

## Grenze

Der Meta-Agent darf die Erkenntnismethode autonom verändern, aber keine erzeugte Theorie automatisch bestätigen oder in das Manuskript übernehmen.
