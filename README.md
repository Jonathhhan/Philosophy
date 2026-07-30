# Zur Kritik der Organisation von Anschlussmöglichkeiten

Philosophisches Buchprojekt von Jonathan Frank über die Entstehung, Ordnung, Aktualisierung und Reorganisation von Anschlussmöglichkeiten.

> Jede Aktualisierung verändert den Raum weiterer Anschlussmöglichkeiten.

## Status

Das Repository enthält einen vollständigen Arbeitsentwurf mit 17 Kapiteln und Schluss. Das Manuskript ist noch keine zitierfähige Endfassung. Die laufende Publikationsphase konzentriert sich auf:

1. argumentative Übergänge und Dramaturgie,
2. Redundanzabbau und begriffliche Konsistenz,
3. Quellen- und Literaturapparat,
4. eine publizierbare Lesefassung.

Der verbindliche Buchstand liegt unter `manuskript/`.

## Worum geht es?

Das Buch beginnt nicht bei fertigen Dingen oder isolierten Subjekten, sondern bei Vollzügen, die an bereits wirksame Bedingungen anschließen. Jeder vollzogene Anschluss verändert die Bedingungen weiterer Anschlüsse: Möglichkeiten werden eröffnet, gewichtet, erschwert, stabilisiert oder ausgeschlossen.

Aus dieser rekursiven Bewegung entwickelt das Projekt eine Theorie der Organisation von Anschlussmöglichkeiten. Montage ist dabei kein bloßes Beispiel, sondern epistemischer Ausgangspunkt. An Material, Schnitten, Varianten, Fassungen, Programmen und algorithmischen Übergängen wird sichtbar, wie Formen entstehen und weitere Bearbeitung ermöglichen oder begrenzen.

Der zweite Teil untersucht Organisation, Verteilung und Asymmetrie. Der dritte Teil entwickelt Kritik, Beurteilung, Revision und Reorganisation. Der Schluss bündelt die These, dass auch die Möglichkeit zur Reorganisation selbst organisiert ist.

## Einstieg

Für einen schnellen systematischen Überblick empfiehlt sich dieser Leseweg:

1. `manuskript/01-anschliessen.md`
2. `manuskript/08-algorithmus.md`
3. `manuskript/15-beurteilen.md`
4. `manuskript/schluss.md`

Eine kommentierte Orientierung steht in [`projekt/leseweg.md`](projekt/leseweg.md).

## Architektur

### Teil I – Formbildung und Aktualisierung

1. Anschließen
2. Unterbrechen
3. Problematisieren
4. Form
5. Aktualisieren
6. Improvisieren
7. Programm
8. Algorithmus
9. Komponieren
10. Stabilisieren

### Teil II – Organisation und Verteilung

11. Organisieren
12. Verteilen
13. Asymmetrie

### Teil III – Kritik und Reorganisation

14. Kritisieren
15. Beurteilen
16. Revidieren
17. Reorganisieren

### Schluss

**Die Organisation der Möglichkeit zur Reorganisation**

## Zentrale Unterscheidungen

- **Programm:** wirksame Vorordnung möglicher Anschlüsse.
- **Algorithmus:** wiederholbare Ordnung bedingter Übergänge.
- **Revision:** begründetes Zurückkommen auf eine stabilisierte Anschlussbedingung.
- **Reorganisation:** Veränderung der Beziehungen zwischen mehreren Anschlussbedingungen.
- **Tragfähigkeit:** begründete Fortsetzbarkeit unter ausgewiesenen Bedingungen bei erhaltener Korrigierbarkeit.

Das Projekt entwickelt keine allgemeine Macht-, Herrschafts- oder Gesellschaftstheorie. Macht, Herrschaft und Legitimation erscheinen allenfalls als abgeleitete Diagnosebegriffe organisierter Asymmetrie.

## Repository-Struktur

- `manuskript/` – aktuelle Kapiteltexte und verbindlicher Buchstand
- `build/manuskript-lesefassung.md` – generierte zusammenhängende Lesefassung
- `projekt/` – Architektur, Leseweg, Arbeitsstand und Arbeitsprotokolle
- `GLOSSAR.md` – stabilisierte und vorläufige Begriffsbestimmungen
- `knowledge/` – Entscheidungen, Begriffsdateien, Relationen und Change Events
- `sources/` – genealogische Primärquellen und erschlossene Quellen
- `literatur/` – Arbeitsapparat für Literatur und Gesprächspartner
- `recovered/` – Audits, Rekonstruktionsdossiers und Vorschläge
- `archive/` – datenschutzbereinigte Entwicklungsarchive
- `interaktiv/` – Anschlusslabor zur operativen Erprobung einzelner Begriffe

Hinweise zu Zitierbarkeit, Urheberrecht, KI-Mitwirkung, Datenschutz und öffentlicher Freigabe stehen in [`PUBLICATION.md`](PUBLICATION.md).

## Quellen- und Rekonstruktionspolitik

Frühere Chatfassungen, rekonstruierte Passagen und Assistentenantworten sind historische Quellen oder Arbeitsmaterialien, aber keine automatisch verbindlichen Manuskriptfassungen. Unsichere Rekonstruktionen bleiben markiert und dürfen nicht als gesicherter Autorenwortlaut behandelt werden.

Die Bachelor- und Masterarbeit unter `sources/` sind genealogische Primärquellen des Projekts. Externe Literatur wird als Gesprächspartner, Kontrast oder methodischer Kontext geführt und darf die Architektur des Buches nicht stillschweigend ersetzen.

## Anschlusslabor

Der interaktive Teil unter `interaktiv/` macht Anschlussoperationen praktisch erfahrbar. Er ersetzt die Argumentation des Manuskripts nicht. Eine optionale KI-Funktion bleibt ohne serverseitige Schutzkonfiguration deaktiviert.

## Codex-Arbeitsweise

Codex wird in diesem Repository nicht als Autorersatz oder Theorieautorität behandelt. Größere Änderungen werden als adressierbare Aktualisierungen geführt: Herkunft, betroffene Relationen, bewahrte Entscheidungen, eröffnete Möglichkeiten und offene Aufgaben sollen sichtbar bleiben.

Die methodischen Grundlagen stehen in:

- `CONSTITUTION.md`
- `WORKFLOW.md`
- `projekt/codex-als-anschlussapparat.md`
- `projekt/codex-nutzungsanleitung.md`

## Lesefassung bauen

```powershell
python scripts/build_manuscript.py
```

Die Ausgabe entsteht unter `build/manuskript-lesefassung.md`. Bearbeitet werden weiterhin die Einzelkapitel unter `manuskript/`.

## Projekt prüfen

Die zentrale Prüfung bündelt Wissensvalidierung, Change Events, Recursive State, MCP-Tests und das Anschlusslabor:

```powershell
python scripts/check_all.py
```

Einzelne Prüfungen:

```powershell
python scripts/validate_knowledge.py
python -B .agents\skills\recursive-codex\scripts\check_recursive_state.py
```

Für das Anschlusslabor:

```powershell
cd interaktiv
npm test
npm run build
```

Weitere lesende Werkzeuge stehen unter `scripts/`, darunter Begriffsnetze, Unterscheidungsanalyse, propositionale Prüfstrukturen und der Philosophie-Automat. Sie erzeugen Prüfungen oder Vorschläge und ersetzen keine Manuskriptentscheidung.
