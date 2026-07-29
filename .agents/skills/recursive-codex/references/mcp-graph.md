# Read-only MCP-Anschlussgraph

Der lokale MCP-Server macht ausschließlich Beziehungen abfragbar, die in
Projekt-YAML ausdrücklich deklariert sind. Er ist ein Navigations- und
Prüfwerkzeug, keine vollständige Repräsentation der Theorie.

## Quellen und Reichweite

Der Graph wird bei jeder Abfrage neu aus folgenden Dateien aufgebaut:

- `knowledge/concepts/*.yaml`
- `knowledge/decisions/*.yaml`
- `knowledge/change-events/*.yaml`
- `knowledge/concept-relations.yaml`

`knowledge/concept-relations.yaml` bleibt als historischer und genealogischer
Arbeitsgraph gekennzeichnet. Seine Knoten erhalten den Namensraum
`historical:` und werden nicht mit gegenwärtigen Begriffsknoten im Namensraum
`concept:` verschmolzen. `knowledge/genealogy.yaml` ist vorerst nicht
integriert, weil seine begriffsübergreifenden Entwicklungslinien eine eigene
Modellierungsentscheidung erfordern.

Freitext, Manuskriptpassagen und bloße Dateinähe erzeugen keine Kanten.
Unbekannte, aber referenzierte Begriffe erscheinen als nicht deklarierte
Platzhalter. Das weist eine Dokumentationslücke aus und ergänzt weder eine
Definition noch eine theoretische Behauptung.

## Semantik der Kanten

- Die deklarierte Richtung bleibt erhalten. `A depends_on B` wird als
  `A → B` gespeichert; eine Umkehrkante wird nicht ergänzt.
- `required_for`, `related`, `affected`, `sourced_from` und weitere
  Relationstypen behalten ebenfalls ihre jeweilige Deklarationsrichtung.
- Transitive Wege werden nur traversiert. Sie werden nicht als neue direkte
  Beziehungen ausgegeben.
- Mehrfach deklarierte Beziehungen werden nicht zu einer vermeintlich
  stärkeren Aussage zusammengezogen.
- Jede Kante enthält die Quelldatei und das genaue YAML-Feld einschließlich
  Listenindex.
- Kanten aus Änderungsereignissen führen den Ereignisstatus, die Wirkung und
  gegebenenfalls die Notiz mit. `proposed`, `tested` und `stabilized` sind
  nicht gleichrangig.
- Dateien und Verzeichnisse sind verschiedene Knotentypen. Ein deklarierter
  Verzeichnispfad wird nicht automatisch in seine Dateien aufgelöst.
- Quellenknoten zeigen deklarierte Provenienz, nicht eine durch den Server
  verifizierte Quellenlage.

## Werkzeuge

1. `graph_summary` zeigt Umfang, Knotentypen, Relationsarten, Ereignisstatus,
   nicht deklarierte Referenzen, fehlende Pfade und Diagnosen.
2. `search_nodes` ermittelt stabile typisierte Knotenkennungen.
3. `get_node` liefert einen Knoten mit allen unmittelbar ein- und ausgehenden
   deklarierten Kanten.
4. `trace_relations` verfolgt deklarierte Wege bis zu einer begrenzten Tiefe,
   ohne daraus neue Direktrelationen abzuleiten.

Für eine Prüfung zuerst `graph_summary`, dann `search_nodes`, `get_node` und
erst bei Bedarf `trace_relations` verwenden. Vor einer Theorieänderung bleiben
die angegebenen Projektdateien, Primärquellen und bestätigten Entscheidungen
selbst zu lesen.

## Betrieb

Die Projektkonfiguration steht in `.codex/config.toml`. Sie startet
`scripts/mcp/recursive_graph_server.py` per STDIO aus dem Projektstamm.
Abhängigkeiten werden in demselben Python-Interpreter installiert, den Codex
für den Server verwendet:

```powershell
python -m pip install -r requirements-dev.txt
```

Codex lädt eine projektlokale MCP-Konfiguration erst für ein als vertrauenswürdig
bestätigtes Projekt und gegebenenfalls erst nach einem Neustart oder in einer
neuen Sitzung. Der Server bietet nur read-only Werkzeuge; alle vier tragen
entsprechende MCP-Anmerkungen und besitzen keine Schreiboperation.

Der direkte Kern- und Protokolltest lautet:

```powershell
python -B scripts\test_recursive_graph.py
```
