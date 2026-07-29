# Rekursive Abschlussprüfung

Die Abschlussprüfung verbindet eine unabhängig ausführbare Zustandsprüfung mit einem projektlokalen Codex-`Stop`-Hook. Sie ist ein technischer Schutzmechanismus, keine inhaltliche Entscheidungsinstanz und keine Garantie vollständiger Stabilisierung.

## Mechanisch geprüfte Invarianten

`check_recursive_state.py` prüft in fester Reihenfolge:

1. Jede YAML-Datei unter `knowledge/change-events/` ist lesbar und erfüllt das Schema von `validate_change_event.py`.
2. `scripts/validate_knowledge.py` läuft erfolgreich.
3. Vorhandene Wissenswarnungen werden ausgewiesen, blockieren den Abschluss aber nicht.

Der Prüfer behauptet nicht, dass alle philosophisch oder architektonisch relevanten Beziehungen dokumentiert sind. Insbesondere leitet er aus Git-Pfaden nicht selbst ab, welche Änderungen strukturell oder relationspflichtig sind.

Manuell ausführen:

```powershell
python -B .agents\skills\recursive-codex\scripts\check_recursive_state.py
```

Maschinenlesbare Ausgabe:

```powershell
python -B .agents\skills\recursive-codex\scripts\check_recursive_state.py --json
```

## Verhalten des Stop-Hooks

| Prüfergebnis | `stop_hook_active` | Hook-Reaktion |
|---|---:|---|
| gültig | beliebig | Turn darf enden |
| ungültig | `false` | genau eine weitere Bearbeitung wird angefordert |
| weiterhin ungültig | `true` | keine zweite Fortsetzung; verbleibender Blocker muss offengelegt werden |

Der Hook verändert keine Datei. Er korrigiert kein Ereignis, entscheidet keine Variante und stabilisiert keine Theorie. Andere Stop-Hooks oder verwaltete Codex-Richtlinien können seine Fortsetzungsanforderung überstimmen.

## Aktivierung und Vertrauen

Die Definition liegt in `.codex/hooks.json`. Projektlokale Hooks werden nur geladen, wenn das Repository in Codex als vertrauenswürdig gilt. Nicht verwaltete Hook-Definitionen müssen zusätzlich in der Hook-Ansicht geprüft und ausdrücklich als vertrauenswürdig bestätigt werden. Nach Änderungen an der Definition kann eine erneute Bestätigung erforderlich sein. Je nach Codex-Oberfläche kann außerdem ein Neustart oder eine neue Sitzung nötig sein.

## Getrennte Prüfungen

Selbsttests:

```powershell
python -B .agents\skills\recursive-codex\scripts\validate_change_event.py --self-test
python -B .agents\skills\recursive-codex\scripts\check_recursive_state.py --self-test
python -B .codex\hooks\recursive_stop.py --self-test
```

Den Hook-Vertrag mit einem gültigen Stop-Ereignis prüfen:

```powershell
'{"hook_event_name":"Stop","cwd":"C:\\Pfad\\zum\\Repository","stop_hook_active":false}' |
  python -B .codex\hooks\recursive_stop.py
```

Auf `stdout` muss genau ein JSON-Objekt erscheinen.

## Bewusst zurückgestellte Abdeckung

Eine spätere deklarative Abdeckungsprüfung benötigt eine bestätigte Festlegung von:

- Baseline und aktivem Änderungsereignis;
- relationspflichtigen Dateien oder Pfadmustern;
- zulässigem Ereignisstatus;
- Behandlung bereits stabilisierter Ereignisse;
- Verhältnis von Git-Zustand und inhaltlicher Reichweite.

Ohne diese Entscheidungen bleibt die Relationsprüfung Aufgabe des Skills, der Agentenrollen und des Autors; sie wird nicht als mechanisch bewiesen ausgegeben.
