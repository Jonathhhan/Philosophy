# Arbeitsstand

Stand: 31. Juli 2026

Das Projekt besitzt einen vollständigen Arbeitsentwurf mit 17 Kapiteln und Schluss. Die theoretische Architektur und die zentralen Begriffsentscheidungen sind stabilisiert. Die nächste Phase dient nicht dem Ausbau um weitere Grundbegriffe oder Werkzeuge, sondern der argumentativen, literarischen und editorischen Publikationsreife.

Abgeschlossene Entwicklungsphasen stehen im [`Änderungsjournal`](aenderungsjournal.md). Verbindliche Architekturentscheidungen stehen in [`architektur.md`](architektur.md), Begriffsdefinitionen im `GLOSSAR.md` und bestätigte Einzelentscheidungen unter `knowledge/decisions/`.

## Gesichert

- Arbeitstitel und verbindliche Architektur
- rekursive Grundbewegung des Projekts
- aktuelle Manuskriptfassungen der Kapitel 1 bis 17 und des Schlusses
- Montage als epistemischer Ausgangspunkt und Modell rekursiver Formbildung
- zentrale Definitionen zu Form, Improvisieren, Programm, Algorithmus, Komponieren, Stabilisieren, Organisieren, Verteilen, Asymmetrie, Kritisieren, Beurteilen, Revidieren und Reorganisieren
- Tragfähigkeit als zusammenfassender Urteilsbegriff, nicht als universaler Grundmaßstab
- Unterscheidung von `Reorganisieren` als Tätigkeit und `Reorganisation` als möglichem Ergebnis
- quellenkritische Sicherung rekonstruierter Manuskript- und Chatbestände
- funktionaler Stand des Anschlusslabors
- Change Events, Wissensbasis, zentrale Projektprüfung und CI
- dokumentierte Arbeitsweise von Codex und Automaten als Prüfapparate, nicht als Theorieautoritäten

## Aktuelle Hauptaufgabe

Der vollständige Manuskriptstand wird von einer stabilen Begriffsarchitektur in eine publizierbare Argumentation überführt.

Dafür gelten vier Prioritäten:

1. **Kapitelübergänge prüfen.** Kapitelenden und Kapitelanfänge werden paarweise darauf gelesen, welches ungelöste Problem die nächste Operation erforderlich macht.
2. **Redundanzen verdichten.** Wiederholte Definitionen und Abgrenzungen bleiben nur dort erhalten, wo sie eine neue argumentative Leistung erbringen.
3. **Literatur integrieren.** Externe Gesprächspartner werden problembezogen eingesetzt, um Unterscheidungen zu schärfen, Alternativen sichtbar zu machen oder Reichweitengrenzen auszuweisen.
4. **Lesefassung beurteilen.** Nach lokalen Revisionen wird das Manuskript als zusammenhängender Text gelesen und nicht nur kapitelweise geprüft.

Die automatengeleitete Prüfstruktur für diese Phase steht unter [`recovered/proposals/naechste-anschluesse.md`](../recovered/proposals/naechste-anschluesse.md).

## Besonders zu prüfende Übergänge

- Kapitel 10 → 11: von der Stabilisierung einzelner Formen zur Organisation mehrerer Anschlussbedingungen
- Kapitel 13 → 14: von der Beschreibung asymmetrischer Bedingungen zur kritischen Prüfung
- Kapitel 15 → 16: vom begründeten Urteil zur erneuten Bestimmung stabilisierter Bedingungen
- Kapitel 17 → Schluss: von konkreter Reorganisation zur Organisation ihrer Möglichkeit

## Noch zu sichern

- konsolidierter Quellen- und Literaturapparat
- vollständige Autorenlektüre der zusammenhängenden Lesefassung
- Prüfung noch nicht abschließend bewerteter rekonstruierter Varianten
- publizierbare Ausgabe mit konsistenten Nachweisen, Abbildungen und editorischen Angaben

## Arbeitsgrenzen

- Keine neue Grundthese oder Theorieachse ohne ausdrückliche Autorenentscheidung.
- Keine stillschweigende Erweiterung zu einer allgemeinen Macht-, Herrschafts-, Gesellschafts- oder Subjekttheorie.
- Literatur darf die Architektur nicht ersetzen, sondern muss an ausgewiesenen Problemen in sie eintreten.
- Projektwerkzeuge, Codex und Automaten erzeugen Vorschläge und Prüfstrukturen, aber keine verbindlichen philosophischen Entscheidungen.
- Weitere technische Automatenstufen bleiben zurückgestellt, solange sie die aktuelle Publikationsphase nicht konkret unterstützen.

## Nächster konkreter Arbeitsschritt

Ein Übergangsaudit erstellt für jedes Kapitelpaar eine kurze Karte aus:

- erreichtem Ergebnis des vorherigen Kapitels,
- offen gebliebenem Problem,
- Notwendigkeit der nächsten Operation,
- möglicher Redundanz,
- benötigtem Literaturanschluss.

Erst auf Grundlage dieses Audits werden Manuskriptpassagen verändert.

## Prüfungen

```powershell
python scripts/check_all.py
python scripts/build_manuscript.py
```

Die erfolgreiche technische Prüfung bestätigt Repository-Invarianten, nicht philosophische Vollständigkeit oder Publikationsreife.
