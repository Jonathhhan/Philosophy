# Editor Pipeline

Diese Pipeline beschreibt den editorischen Arbeitsablauf. Ihr Zweck ist die Revision des Manuskripts, nicht die unbegrenzte Erzeugung weiterer Prüftexte.

## Reihenfolge
1. Automatenverbund
2. Unterscheidungsautomat
3. Redundanzautomat
4. Begriffsnetz
5. Tractatus-Automat
6. Kapitelautomat
7. Editor

Die Automaten bilden keinen rekursiven Auftragsgenerator. Ein Lauf darf frühere Befunde aufnehmen, aber nicht allein deshalb einen weiteren Lauf derselben Art auslösen.

## Entscheidungsregeln
- KEEP: notwendige argumentative Funktion
- SHORTEN: Wiederholung ohne neue Funktion
- MERGE: zusammenführen gleicher Begriffe oder Definitionen
- MOVE: an logisch passendere Stelle verschieben

## Verbindlicher Abschluss jedes Laufs
Jeder Lauf endet mit genau einer der folgenden Entscheidungen:

1. **PATCH** – Ein hinreichend bestimmter Befund wird unmittelbar im Manuskript umgesetzt und committed.
2. **KEEP** – Die geprüfte Stelle bleibt mit knapper Begründung unverändert; derselbe Befund wird nicht erneut geprüft.
3. **BLOCKED** – Eine Änderung wäre ohne Quelle, Textgrundlage oder begriffliche Entscheidung spekulativ. Der Lauf endet, bis neue Evidenz vorliegt.

Ein Audit darf kein weiteres Audit als einzigen Output erzeugen. Vorschlags- und Auditdateien sind nur zulässig, wenn sie einen konkreten Manuskriptpatch vorbereiten, eine offene Evidenzfrage dokumentieren oder einen abgeschlossenen Befund nachvollziehbar festhalten.

## Abbruchbedingungen
Ein Gegenstand gilt für den laufenden Redaktionsdurchgang als abgeschlossen, wenn:

- ein Patch committed wurde,
- die Entscheidung KEEP dokumentiert ist,
- keine neue Textstelle oder neue Evidenz gegenüber dem letzten Lauf vorliegt,
- oder die maximale Prüftiefe von einem Hauptlauf plus einem gezielten Gegencheck erreicht ist.

Danach wechselt die Pipeline zum nächsten noch ungeprüften Manuskriptabschnitt. Sie kehrt nur zurück, wenn eine spätere Änderung den früheren Befund tatsächlich berührt.

## Prinzip
Erst prüfen, dann entscheiden, dann überarbeiten oder abschließen. Jede Revision muss argumentativ begründet werden. Prüfung ist kein Selbstzweck: Der Editor trägt die Entscheidung und verhindert einen endlosen Regress der Prüfungen.
