# Nächste Anschlüsse

Status: Proposal und Prüfstruktur. Kein Manuskripttext, keine Theorieentscheidung.

## Ausgangsunterscheidung

Markiert: publizierbare Argumentation

Unmarkiert: bloße Projektdokumentation

Die nächste Phase soll nicht weitere Werkzeuge anhäufen, sondern den vollständigen Entwurf als lesbare, begründete und quellenfähige Buchform stabilisieren.

## Propositionale Ordnung

1. Ein vollständiger Entwurf ist noch keine publizierbare Argumentation.
1.1 Publizierbarkeit verlangt nachvollziehbare Problemübergänge zwischen den Kapiteln.
1.2 Definitionen tragen nur dann, wenn sichtbar wird, warum die nächste Unterscheidung erforderlich ist.
1.3 Wiederholte Abgrenzungen können Präzision sichern, aber auch die Bewegung hemmen.

2. Der nächste Anschluss ist daher eine dramaturgische Revision.
2.1 Jeder Kapitelübergang soll aus einem ungelösten Problem des vorherigen Kapitels hervorgehen.
2.2 Besonders zu prüfen sind Stabilisieren → Organisieren, Asymmetrie → Kritisieren und Beurteilen → Revidieren.
2.3 Der Schluss muss zeigen, warum Reorganisierbarkeit aus der rekursiven Bewegung folgt.

3. Literaturarbeit gehört in diese Revision.
3.1 Gesprächspartner treten dort ein, wo sie eine Unterscheidung schärfen, eine Alternative zeigen oder eine Reichweitengrenze markieren.
3.2 Die Eigenständigkeit des Projekts wird durch ausgewiesene Differenzen sichtbar, nicht durch Abschottung.

4. Automaten und Codex bleiben Prüfapparate.
4.1 Sie können Brücken, Wiederholungen, Leerstellen und Grenzverletzungen anzeigen.
4.2 Sie entscheiden nicht, ob eine philosophische Passage sachlich trägt.

## Priorisierte nächste Anschlüsse

1. Kapitelenden und Kapitelanfänge paarweise auf Problemrest, nächste Operation und Redundanz prüfen.
2. Wiederholte Abgrenzungsformeln erfassen und nur dort bewahren, wo sie eine neue Grenze markieren.
3. Für jeden Hauptbegriff wenige problembezogene Literaturanschlüsse mit Funktion und Differenz bestimmen.
4. Danach die zusammenhängende Lesefassung als Ganzes prüfen.
5. Weitere technische Automatenstufen zurückstellen, solange sie diese Arbeiten nicht konkret unterstützen.

## Lokaler Automatenlauf

```powershell
python scripts\automatenverbund.py "publizierbare Argumentation" "Projektdokumentation" --context "vom vollständigen Arbeitsentwurf zur begründeten Lesefassung" --max-steps 8 --output recovered\proposals\naechste-anschluesse.generated.md
```

Diese Datei folgt den drei dokumentierten Stufen Unterscheiden, propositional Ordnen und Aufführen. Der tatsächliche lokale Programmlauf kann mit dem angegebenen Befehl erzeugt und anschließend mit diesem Proposal verglichen werden.
