# Zur Kritik der Organisation von Anschlussmöglichkeiten

Arbeitsrepository für ein philosophisches Buchprojekt von Jonathan Frank.

Status: vollständiger Arbeitsentwurf mit 17 Kapiteln und Schluss. Das Manuskript ist noch keine zitierfähige Endfassung; die nächste Arbeitsphase dient Gesamtrevision, Übergängen, Redundanzabbau, Literaturapparat und publizierbarer Lesefassung.

## Synopsis

Das Buch untersucht, wie Anschlussmöglichkeiten entstehen, geordnet, aktualisiert, stabilisiert, verteilt, beurteilt, revidiert und reorganisiert werden. Es beginnt nicht bei fertigen Dingen oder isolierten Subjekten, sondern bei Vollzügen, die an bereits wirksame Bedingungen anschließen. Jede Aktualisierung verändert den Raum weiterer Anschlussmöglichkeiten: Ein vollzogener Anschluss wird selbst Bestandteil der Bedingungen, unter denen weitere Anschlüsse möglich, wahrscheinlicher, schwieriger oder ausgeschlossen werden.

Aus dieser rekursiven Bewegung entwickelt das Projekt eine Theorie der Organisation von Anschlussmöglichkeiten. Montage ist dabei kein bloßes Beispiel, sondern epistemisches Modell: An Fassungen, Schnitten, Varianten, Programmen und algorithmischen Übergängen wird sichtbar, wie Formen entstehen und weitere Bearbeitung ermöglichen oder begrenzen. Der zweite Teil überträgt diese Begriffsarbeit auf Organisation, Verteilung und Asymmetrie, ohne daraus eine allgemeine Macht- oder Gesellschaftstheorie zu machen. Der dritte Teil fragt nach Kritik, Beurteilung, Revision und Reorganisation. Der Schluss bündelt die These, dass auch die Möglichkeit zur Reorganisation selbst organisiert ist.

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

Die Organisation der Möglichkeit zur Reorganisation

## Leitgedanke

> Jede Aktualisierung verändert den Raum weiterer Anschlussmöglichkeiten.

Das Projekt entwickelt keine allgemeine Macht-, Herrschafts- oder Gesellschaftstheorie. Macht, Herrschaft und Legitimation erscheinen allenfalls als abgeleitete Diagnosebegriffe organisierter Asymmetrie.

## Repository-Struktur

- `manuskript/` – aktuelle Kapiteltexte; primärer Buchstand.
- `build/manuskript-lesefassung.md` – generierte zusammenhängende Markdown-Lesefassung.
- `projekt/` – Architektur, Arbeitsstand, Codex-Arbeitsprinzipien und Auftragsvorlagen.
- `GLOSSAR.md` – verbindliche oder vorläufig stabilisierte Arbeitsdefinitionen.
- `knowledge/` – Entscheidungen, Begriffsdateien, Relationen und Change Events als Prüf- und Navigationsinstrumente.
- `sources/` – Bachelorarbeit, Masterarbeit, Gutachten und erschlossene Primärquellen des Projekts.
- `literatur/` – Arbeitsapparat für Quellen, Literatur und externe Gesprächspartner.
- `recovered/` – Audits, Rekonstruktionsdossiers und quellenkritische Sicherungen.
- `archive/` – datenschutzbereinigte Chat- und Entwicklungsarchive.
- `interaktiv/` – Anschlusslabor zur operativen Darstellung einzelner Begriffe; kein Ersatz für das Manuskript.

## Quellen- und Rekonstruktionspolitik

Das aktuelle Manuskript unter `manuskript/` ist der geltende Buchstand. Frühere Chatfassungen, rekonstruierte Passagen und Assistentenantworten sind historische Quellen oder Arbeitsmaterialien, aber keine automatisch verbindlichen Manuskriptfassungen. Unsichere Rekonstruktionen bleiben markiert und dürfen nicht als gesicherter Autorenwortlaut behandelt werden.

Die Bachelor- und Masterarbeit unter `sources/` sind genealogische Primärquellen des Projekts. Externe Literatur wird als Gesprächspartner, Kontrast oder methodischer Kontext geführt und darf die Architektur des Buches nicht stillschweigend ersetzen.

## Anschlusslabor

Der interaktive Teil unter `interaktiv/` macht Anschlussoperationen praktisch erfahrbar. Er illustriert die Theorie nicht bloß, ersetzt aber auch nicht die argumentative Entwicklung des Manuskripts. Eine optionale KI-Funktion bleibt an Datenschutz-, Sicherheits- und Deploymententscheidungen gebunden und ist ohne serverseitige Schutzkonfiguration deaktiviert.

## Lesefassung bauen

Der aktuelle Manuskriptstand kann als zusammenhängende Markdown-Lesefassung gebaut werden:

```powershell
python scripts/build_manuscript.py
```

Die Ausgabe entsteht unter `build/manuskript-lesefassung.md`. Bearbeitet werden weiterhin die Einzelkapitel unter `manuskript/`.

## Prüfungen

Die Wissensbasis wird geprüft mit:

```powershell
python scripts/validate_knowledge.py
```

Der rekursive Projektzustand wird geprüft mit:

```powershell
python -B .agents\skills\recursive-codex\scripts\check_recursive_state.py
```

Für das Anschlusslabor:

```powershell
cd interaktiv
npm test
npm run build
```