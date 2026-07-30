# Änderungsjournal

Dieses Journal hält abgeschlossene Entwicklungsphasen des Projekts in komprimierter Form fest. Der jeweils geltende Arbeitsstand steht in [`arbeitsstand.md`](arbeitsstand.md). Verbindliche Begriffs- und Architekturentscheidungen stehen weiterhin in den dafür vorgesehenen Dateien unter `knowledge/`, im `GLOSSAR.md` und in `projekt/architektur.md`.

## 2026-07-29 – Manuskriptarchitektur und erster Gesamtausbau

- Die Architektur mit 17 Kapiteln und Schluss wurde stabilisiert.
- Kapitel 3 bis 9 wurden aus Montage, Improvisation, Programm und Algorithmus genealogisch konkretisiert.
- Der `Alphaville`-Versuch des Montage-Automaten wurde als durchgehender Leitfall integriert.
- Vier Prozessdiagramme wurden als Bestandteile des Buches bestätigt.
- Kapitel 10 bis 17 sowie der Schluss wurden als aktuelle Manuskriptfassungen angelegt.
- Werk wurde als besonderer Fall der Stabilisierung bestimmt.
- Organisieren, Verteilen und Asymmetrie wurden als eigene Operationen voneinander abgegrenzt.
- Kritisieren, Beurteilen, Revidieren und Reorganisieren wurden funktional unterschieden.
- Tragfähigkeit wurde als zusammenfassender Urteilsbegriff, nicht als universaler Grundmaßstab festgelegt.
- Reorganisieren wurde als Tätigkeit von Reorganisation als möglichem Ergebnis unterschieden.

## 2026-07-29 – Anschlusslabor

- Der interaktive Prototyp wurde zu einem Anschlusslabor ausgebaut.
- Fortsetzen, Präzisieren, Unterbrechen und Variieren wurden als operative Anschlussweisen umgesetzt.
- Fassungen, Freigaben, Wiederaufnahmen und Abstammungslinien wurden getrennt modelliert.
- Import, Export, lokale Speicherung und Löschvorgänge wurden abgesichert.
- Bedienung, Fokusführung, Bewegungsreduktion und semantische Auszeichnung wurden verbessert.
- Die theoretische Grenze blieb festgehalten: Das Labor macht Operationen erfahrbar, ersetzt aber nicht die Argumentation des Manuskripts.

## 2026-07-30 – Governance, Wissensbasis und Prüfung

- `CONSTITUTION.md`, `AGENTS.md`, `WORKFLOW.md` und der Recursive-Codex-Skill wurden auf eine gemeinsame Autoritätshierarchie ausgerichtet.
- Change Events, Concept-Dateien, Entscheidungen und Relationsprüfungen wurden als maschinenlesbare Projektschicht stabilisiert.
- Ein read-only MCP-Anschlussgraph wurde eingerichtet.
- `scripts/check_all.py` bündelt die zentralen Prüfungen.
- Eine GitHub-Actions-Validierung führt denselben Gesamtbefehl bei Pushes und Pull Requests aus.
- Die zuvor bekannten Wissenswarnungen wurden beseitigt.
- Die Prüfungen sichern Repository-Invarianten, beanspruchen aber keine philosophische Vollständigkeit.

## 2026-07-30 – Argumentations- und Publikationsphase

- Ein Argumentationsaudit für Kapitel 1 bis 17 wurde erstellt.
- Als prioritäre Punkte wurden Modalität der Anschlussmöglichkeiten, Subjektrolle, Tragfähigkeit, Kapitelübergänge und wiederholte Abgrenzungen identifiziert.
- Kapitel 5 präzisiert seitdem den Status von Anschlussmöglichkeiten zwischen bloßer Denkbarkeit und praktisch relevanter Option.
- Kapitel 15 präzisiert Tragfähigkeit als begründete Fortsetzbarkeit unter erhaltenen Korrekturbedingungen.
- Kapitel 15 bestimmt Verantwortung als zurechenbare Antwortfähigkeit innerhalb verteilter Anschlussbedingungen.
- Die öffentliche Projektoberfläche wurde durch README, Publikationshinweise, Positionskarte und Leseweg verbessert.

## 2026-07-30 – Codex als Anschlussapparat

- Codex wurde als organisierter Prüf-, Schreib- und Reorganisationsapparat beschrieben, nicht als Autorersatz oder Theorieautorität.
- Ein Zettelkasten-/Plateau-Prinzip, ein genetisches Register und ein feineres Operationsregister wurden als Arbeitsmethoden dokumentiert.
- Delegierte Entscheidungen wurden auf ausdrücklich erlaubte, begrenzte Fälle beschränkt.
- Manuskriptthesen, Grundbegriffe, Theorieachsen, Quellenbehauptungen, Datenschutz, Lizenz und Veröffentlichung bleiben nicht delegierbar.

## 2026-07-30 – Philosophie-Automat und weitere Prüfwerkzeuge

- `scripts/philosophie_automat.py` wurde in mehreren Stufen ausgebaut: Begriffsprüfung, Kapitelkontext, markierter Entwurf, Event-Draft und Vorprüfung.
- Automatische Übernahmen bleiben gesperrt oder ausdrücklich autorisierungspflichtig.
- Begriffsnetz-, Unterscheidungs-, Tractatus- und Kunstwerk-Automaten wurden als lesende oder vorschlagende Prüfwerkzeuge ergänzt.
- Der Automatenverbund verbindet diese Werkzeuge nur über ausgewiesene Begriffsadressen, Manuskriptanker oder deklarierte Relationen.
- Kein Automat ersetzt Autorenentscheidung, Quellenprüfung oder Manuskriptargumentation.

## Fortführung

Neue Einträge sollen nur abgeschlossene oder stabilisierte Entwicklungsphasen dokumentieren. Laufende Prioritäten, offene Entscheidungen und nächste Schritte gehören ausschließlich in `projekt/arbeitsstand.md`.
