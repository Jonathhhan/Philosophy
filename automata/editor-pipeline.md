# Editor Pipeline

Diese Pipeline beschreibt den editorischen Arbeitsablauf. Ihr Zweck ist die Revision des Manuskripts und die Hervorbringung neuer, textlich wirksamer Unterschiede.

## Reihenfolge
1. Automatenverbund
2. Unterscheidungsautomat
3. Redundanzautomat
4. Begriffsnetz
5. Tractatus-Automat
6. Kapitelautomat
7. Editor

Die Automaten bilden einen produktiven Verbund. Ein Lauf darf frühere Befunde aufnehmen und in veränderter Konstellation erneut verarbeiten. Er darf jedoch keine identische Prüfung bloß wiederholen.

## Entscheidungsregeln
- KEEP: notwendige argumentative Funktion
- SHORTEN: Wiederholung ohne neue Funktion
- MERGE: zusammenführen gleicher Begriffe oder Definitionen
- MOVE: an logisch passendere Stelle verschieben

## Produktive Differenz
Ein Automatenlauf gilt erst dann als abgeschlossen, wenn mindestens eine produktive Differenz entstanden ist:

1. **PATCH** – Eine neue oder präzisere Bestimmung wird unmittelbar im Manuskript umgesetzt und committed.
2. **RELATION** – Zwischen bereits vorhandenen Begriffen, Kapiteln oder Manuskriptankern wird eine bislang nicht ausgewiesene, argumentativ tragfähige Beziehung bestimmt.
3. **DISTINCTION** – Eine bisher verdeckte Unterscheidung wird so präzisiert, dass sie eine spätere Textrevision oder Begriffsentscheidung trägt.
4. **BLOCK** – Eine scheinbare Anschlussmöglichkeit wird begründet ausgeschlossen und dadurch der Möglichkeitsraum der weiteren Arbeit verändert.

Eine bloße Wiederholung bekannter Befunde ist keine produktive Differenz.

## Arbeitsweise bis zur Neuheit
Solange noch keine produktive Differenz entstanden ist, arbeitet der Verbund weiter:

- Er wechselt vom Ausgangsbegriff zu benachbarten Begriffsadressen.
- Er prüft weitere Manuskriptanker und angrenzende Kapitel.
- Er verändert die markierte und unmarkierte Seite der Unterscheidung.
- Er vergleicht den aktuellen Befund mit bereits erzeugten Signaturen.
- Er überspringt identische Konstellationen und verfolgt nur noch nicht geprüfte Anschlüsse.

Der Editor beendet den Lauf nicht wegen eines negativen Einzelbefunds. Er entscheidet erst, nachdem entweder etwas Neues entstanden ist oder der erreichbare Suchraum erschöpft wurde.

## Schutz vor endlosem Regress
Der Regress wird nicht durch eine willkürliche Zahl von Prüfschritten beendet, sondern durch Zyklenerkennung und Erschöpfung:

- Eine identische Kombination aus Begriffen, Manuskriptankern, Relationen und Befund wird nicht erneut ausgeführt.
- Bereits besuchte Anschlussstellen werden nur wieder geöffnet, wenn eine spätere Änderung ihre Bedingungen verändert hat.
- Ein Audit darf kein weiteres Audit als einzigen Output erzeugen.
- Der Lauf endet ohne Patch nur dann, wenn alle erreichbaren, noch nicht besuchten Anschlüsse geprüft wurden und keine produktive Differenz hervorgebracht werden konnte.

In diesem Fall lautet der Abschluss **EXHAUSTED**. Er dokumentiert nicht bloß Untätigkeit, sondern den begründeten Befund, dass unter den gegenwärtigen Bedingungen kein neuer Anschluss erreichbar war.

## Prinzip
Die Automaten arbeiten weiter, bis etwas Neues entstanden ist. Neuheit bedeutet dabei nicht bloße Variation der Formulierung, sondern eine Differenz, die den Begriffsraum, den Argumentationsgang oder den Manuskripttext verändert. Der Editor trägt die Entscheidung darüber, ob diese Schwelle erreicht ist.
