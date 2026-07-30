# Arbeitsstand

Stand: 31. Juli 2026

Das Projekt besitzt einen vollständigen Arbeitsentwurf mit 17 Kapiteln und Schluss. Die theoretische Architektur und die zentralen Begriffsentscheidungen sind stabilisiert. Die aktuelle Phase dient nicht dem Ausbau um weitere Grundbegriffe oder Werkzeuge, sondern der argumentativen, literarischen und editorischen Publikationsreife.

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
- automatengeleitetes Audit der Übergänge 10 → 11, 13 → 14, 15 → 16 und 17 → Schluss

## Aktuelle Hauptaufgabe

Der vollständige Manuskriptstand wird von einer stabilen Begriffsarchitektur in eine publizierbare Argumentation überführt.

Die Publikationsphase folgt vier Anschlüssen:

1. **Kapitelübergänge prüfen – abgeschlossen.** Die vier priorisierten Übergänge wurden mit `keep` bewertet; künstliche Ergänzungen waren nicht erforderlich. Das Audit steht unter [`recovered/audits/uebergangsaudit-publikationsphase.md`](../recovered/audits/uebergangsaudit-publikationsphase.md).
2. **Redundanzen verdichten – aktiv.** Wiederholte Definitionen und Abgrenzungen bleiben nur dort erhalten, wo sie eine neue argumentative Leistung erbringen.
3. **Literatur integrieren – anschließend.** Externe Gesprächspartner werden problembezogen eingesetzt, um Unterscheidungen zu schärfen, Alternativen sichtbar zu machen oder Reichweitengrenzen auszuweisen.
4. **Lesefassung beurteilen – abschließend.** Nach lokalen Revisionen wird das Manuskript als zusammenhängender Text gelesen und nicht nur kapitelweise geprüft.

Die automatengeleitete Prüfstruktur für diese Phase steht unter [`recovered/proposals/naechste-anschluesse.md`](../recovered/proposals/naechste-anschluesse.md).

## Redundanzprüfung

Besonders zu prüfen sind:

- wiederholte Formeln zur Abgrenzung von Macht-, Herrschafts-, Gesellschafts- und Subjekttheorie;
- wiederkehrende Sicherungen, dass Stabilisierung, Wirksamkeit oder Fortbestand keine Rechtfertigung begründen;
- mehrfache Abgrenzungen von Programm, Algorithmus, Organisation, Revision und Reorganisation;
- gleichförmige Kapitelendformeln ohne neue argumentative Funktion.

Kürzungen erfolgen nur, wenn eine Wiederholung weder Orientierung, Rückbezug, Kontrast noch eine neue Folgerung leistet.

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

Ein Redundanzaudit unterscheidet für jede Wiederholung:

- notwendige Definition,
- hilfreichen Rückbezug,
- neue argumentative Folgerung,
- bloße Sicherungswiederholung.

Nur die letzte Kategorie wird zur Kürzung vorgeschlagen. Manuskriptänderungen bleiben klein, lokal und begründet.

## Prüfungen

```powershell
python scripts/check_all.py
python scripts/build_manuscript.py
```

Die erfolgreiche technische Prüfung bestätigt Repository-Invarianten, nicht philosophische Vollständigkeit oder Publikationsreife.