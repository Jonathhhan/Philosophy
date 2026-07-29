---
name: recursive-codex
description: Steuert größere Änderungen als rekursive, revidierbare Projektarbeit mit Eingriffsklassifikation, Provenienz, Relationsprüfung, optionalen kritischen Agentenrollen und expliziter Abschlussprüfung. Verwenden bei Manuskript- oder Architekturarbeit, Änderungen bestätigter Definitionen oder Entscheidungen, philosophisch strittigen Integrationen, projektübergreifenden Folgen, Audits sowie Aufträgen wie „arbeite rekursiv“, „prüfe Anschlussbedingungen“, „revidiere“ oder „reorganisiere“.
---

# Recursive Codex

Änderungen als Aktualisierungen eines bereits organisierten Projektstands behandeln. Relationale Folgen und Entscheidungskompetenzen mitführen, ohne die Buchbegriffe auf beliebige technische Vorgänge zu verallgemeinern.

## Verbindlichen Kontext aufnehmen

1. `CONSTITUTION.md` lesen und die geltende Autoritätshierarchie bestimmen.
2. `AGENTS.md`, `WORKFLOW.md` und `projekt/codex-auftragsvorlage.md` lesen.
3. Betroffene Dateien, Definitionen, Entscheidungen, Quellen und technische Ausgaben bestimmen.
4. Quelle, begriffliche Entwicklung, Agentenvorschlag und bestätigten Status unterscheiden.
5. Geschützte Dateien und erforderliche Autorenentscheidungen festhalten.

## Eingriff klassifizieren

Genau eine primäre Operation bestimmen:

- `local_update`: lokal anschließen, aktualisieren und prüfen;
- `composition`: mehrere Elemente oder Abschnitte zu einem Zusammenhang integrieren;
- `revision`: begründet auf eine stabilisierte Fassung oder Entscheidung zurückkommen;
- `reorganization`: Beziehungen mehrerer Projektbestandteile verändern;
- `audit`: prüfen und berichten, ohne Dateien zu verändern.

Bei mehreren plausiblen Klassifikationen die weiter reichende Operation wählen oder die Unklarheit vor der Integration ausweisen. Eine strukturelle Änderung niemals als lokale Korrektur behandeln.

## Arbeitsmodus bestimmen

- Bestätigte Vorgaben direkt ausführen, soweit der Auftrag die Änderung autorisiert.
- Unter partieller Unbestimmtheit mindestens zwei unterscheidbare Varianten entwickeln, wenn mehrere philosophisch plausible Lösungen bestehen.
- Unbestätigte Varianten nicht in stabilisierte Theorie überführen.
- Keine Mehrheitsentscheidung aus Agentenergebnissen ableiten.
- Neue Grundbegriffe, Grundthesen oder Theorieachsen nur als Vorschlag markieren.

## Agentenrollen einsetzen

Bei philosophisch strittigen strukturellen Änderungen oder ausdrücklichem Agentenauftrag zwei oder drei unabhängige, möglichst read-only Prüfungen delegieren. Die Rollen aus [agent-roles.md](references/agent-roles.md) auswählen.

Den Agenten nur Aufgabe, erforderliche Primärartefakte und ihren Prüfauftrag geben. Keine erwartete Antwort oder vermutete Schwachstelle vorgeben. Ergebnisse als Befunde, Einwände und Vorschläge zusammenführen; abweichende Positionen erhalten.

Bei lokaler, eindeutig bestimmter Arbeit keine Agenten allein zur Bestätigung einsetzen.

## Änderungsereignis führen

Für `revision`, `reorganization` und größere `composition` vor der Änderung ein Ereignis aus [change-event.yaml](assets/change-event.yaml) unter `knowledge/change-events/` anlegen. Bei einem reinen `audit` nur dann ein Ereignis anlegen, wenn der Auftrag eine dauerhafte Dokumentation verlangt.

Das Schema vollständig nach [change-event-schema.md](references/change-event-schema.md) ausfüllen:

1. Ziel, Umfang und Grundlage eintragen.
2. Betroffene Beziehungen und erwartete Folgen als vorläufig markieren.
3. Nach der Änderung tatsächliche Folgen, zurückgestellte Möglichkeiten und Unsicherheiten ergänzen.
4. Agentenbefunde nach Rollen getrennt dokumentieren.
5. Autorisierungsstatus und Validierungsergebnisse aktualisieren.
6. Status nur nach den im Schema festgelegten Bedingungen anheben.

Das Ereignis mit folgendem Befehl prüfen:

```powershell
python -B .agents\skills\recursive-codex\scripts\validate_change_event.py <ereignis.yaml>
```

## Deklarierte Beziehungen mit dem MCP-Graphen prüfen

Wenn die projektlokale MCP-Konfiguration aktiv ist, den read-only
`recursive_project_graph` zur Orientierung über bereits deklarierte Begriffe,
Entscheidungen, Änderungsereignisse und Projektpfade verwenden. Die
Abfragefolge, Relationssemantik, historischen Namensräume und Grenzen stehen
in [mcp-graph.md](references/mcp-graph.md).

Mit `graph_summary` beginnen. Nicht deklarierte Knoten und Diagnosen als
Prüfhinweise behandeln, nicht automatisch schließen. Vor Änderungen die von
den Kanten genannten Dateien selbst lesen. Graphwege sind keine neuen
Direktrelationen, und der Graph ersetzt weder Quellenprüfung noch
Autorenentscheidung.
## Rekursive Abschlussprüfung verwenden

Vor dem Abschluss größerer Änderungen die projektweite Zustandsprüfung ausführen:

```powershell
python -B .agents\skills\recursive-codex\scripts\check_recursive_state.py
```

Der projektlokale `Stop`-Hook kann bei einem Fehler höchstens einen weiteren Prüfgang anfordern. Seine genaue Reichweite, Warnungspolitik, Vertrauensvoraussetzungen und Grenzen stehen in [closure-gate.md](references/closure-gate.md). Die mechanische Prüfung bestätigt Schema und deklarierte Wissensintegrität, nicht die philosophische Vollständigkeit der Relationsanalyse.

## Aktualisieren und Relationsfolgen prüfen

1. Kleinste hinreichende Änderung ausführen.
2. Unbeauftragte Nebenreformen vermeiden.
3. Definitionen, Querverweise, Wissensdateien, Quellenstatus und technische Ausgaben prüfen.
4. Festhalten, welche Bearbeitungsmöglichkeiten eröffnet, begrenzt oder zurückgestellt werden.
5. Nicht voraussetzen, dass mehr Möglichkeiten automatisch besser sind.
6. Bei unerwarteten relationalen Folgen zur Klassifikation zurückkehren und den Eingriff gegebenenfalls als Reorganisation behandeln.

## Abschlussprüfung

Die Arbeit erst abschließen, wenn:

- der erlaubte Umfang eingehalten ist;
- Definitionen und bestätigte Entscheidungen nicht stillschweigend verändert wurden;
- relevante Folgebeziehungen geprüft sind;
- Quellen und Provenienz kenntlich bleiben;
- Agentenvorschläge nicht als gesicherte Theorie erscheinen;
- offene Entscheidungen als offen ausgewiesen sind;
- erforderliche Autorenbestätigungen vor Stabilisierung vorliegen;
- passende Projektprüfungen erfolgreich gelaufen oder begründet als nicht ausführbar dokumentiert sind;
- das Änderungsereignis, sofern erforderlich, valide ist.

Bei fehlgeschlagener Prüfung nicht stabilisieren. Entweder lokal revidieren, den Eingriff neu klassifizieren oder die konkrete Autorenentscheidung einholen.

## Ergebnis berichten

Kompakt berichten:

- **Aktualisiert**
- **Betroffene Anschlussbedingungen und Querverweise**
- **Eröffnete, begrenzte oder zurückgestellte Möglichkeiten**
- **Bestätigte und offene Entscheidungen**
- **Prüfungen und Ergebnis**

Werkzeuge und Zwischenschritte nur nennen, wenn sie für Nachvollziehbarkeit, Risiko oder einen Blocker relevant sind.
