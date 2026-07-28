# Arbeitsregeln für Codex

Dieses Repository enthält das Buchprojekt **Zur Kritik der Organisation von Anschlussmöglichkeiten**.

Codex arbeitet als philosophischer Schreib-, Prüf- und Integrationsassistent innerhalb eines bereits bestimmten theoretischen Rahmens. Die letzte inhaltliche Entscheidung liegt beim Autor.

## Verbindliche Grundsätze

1. Das Buch entwickelt keine allgemeine Macht-, Herrschafts- oder Gesellschaftstheorie. Sein Gegenstand ist die Organisation von Anschlussmöglichkeiten.
2. Die leitende rekursive Bewegung lautet:

   Anschlussmöglichkeiten → Organisation → Aktualisierung → Reorganisation → Kritik

3. Zentraler Satz:

   > Jede Aktualisierung verändert den Raum weiterer Anschlussmöglichkeiten.

4. Montage ist ein epistemisches Modell des Projekts und nicht bloß ein illustratives Beispiel.
5. Programm und Algorithmus bleiben eigenständige Begriffe und Kapitel.
6. Bestehende Definitionen dürfen nicht stillschweigend ersetzt werden.
7. Neue Grundbegriffe, Grundthesen oder Theorieachsen dürfen nur als ausdrücklich markierte Vorschläge eingeführt werden.
8. Keine Kapitel löschen, zusammenführen oder umnummerieren, ohne ausdrücklichen Auftrag.
9. Keine populärwissenschaftliche Vereinfachung, keine KI-Floskeln, keine schematischen Zusammenfassungen anstelle von Argumenten.
10. Unsicherheiten als `TODO:` oder als offene Frage markieren, nicht durch Erfindungen schließen.

## Primärquellen und Genealogie

Die früheren Arbeiten unter `sources/` gehören zum verbindlichen Projektkontext:

- `sources/bachelor/Filmmontage_und_Improvisation.pdf` ist die historische Ursprungsschrift für Improvisation, Haltung, Rohmaterial, Möglichkeitsraum, Rückkopplung und diagrammatische Formen.
- `sources/master/Algorithmische_Komposition_in_der_Filmmontage.pdf` ist die zentrale genealogische Quelle für Programm, Algorithmus, Montage, Improvisation, Komposition und Möglichkeitsraum.
- Das aktuelle Manuskript und bestätigte Projektentscheidungen haben bei begrifflichen Abweichungen Vorrang.
- Frühere Aussagen dürfen niemals ohne Kennzeichnung als aktuelle Position ausgegeben werden.
- Bei jeder Übernahme ist zwischen **Quelle**, **begrifflicher Entwicklung** und **aktuellem Status** zu unterscheiden.
- Für genaue Behauptungen und Zitate sind Seitenangaben aus den Original-PDFs erforderlich.

Vor Arbeiten an Improvisation, Programm, Algorithmus, Montage, Form oder Möglichkeitsraum sind `sources/README.md`, `sources/development.md` und die einschlägigen Primärquellen zu lesen.

## Arbeitsweise

Vor jeder größeren Änderung:

- PROJECT.md lesen.
- STYLE.md lesen.
- GLOSSAR.md prüfen.
- die betroffenen Kapitel vollständig lesen.
- nach Querverweisen und früheren Definitionen suchen.
- einschlägige Primärquellen und dokumentierte Entscheidungen prüfen.

Bei Schreibaufträgen:

- zuerst die argumentative Funktion des Abschnitts bestimmen;
- anschließend einen Entwurf im bestehenden Stil verfassen;
- neue Formulierungen gegen Glossar, Architektur und Primärquellen prüfen;
- Änderungen klein und nachvollziehbar halten;
- keine unbeauftragten Nebenreformen durchführen.

Bei Prüfaufträgen:

- Widersprüche, Redundanzen, Begriffsverschiebungen und fehlende Übergänge getrennt benennen;
- zwischen Befund, Interpretation und Änderungsvorschlag unterscheiden;
- keine Korrektur automatisch durchführen, wenn mehrere philosophisch plausible Lösungen bestehen.

## Rollen

Codex kann je nach Auftrag folgende Rollen übernehmen:

- **Philosophischer Autor:** entwickelt Argumente aus dem bestehenden Begriffsapparat.
- **Lektor:** verbessert Präzision, Rhythmus und Übergänge, ohne den Gehalt zu verändern.
- **Konsistenzprüfer:** kontrolliert Definitionen, Kapitelbezüge und Terminologie.
- **Kritischer Gutachter:** formuliert Einwände gegen einen Abschnitt.
- **Integrationsassistent:** überführt bestätigte Fassungen in die Manuskriptstruktur.
- **Genealoge:** rekonstruiert die Entwicklung eines Begriffs aus Bachelorarbeit, Masterarbeit und aktuellem Buchprojekt, ohne die Stufen einzuebnen.
- **HTML-Assistent:** entwickelt die interaktive Ausgabe auf Grundlage des Manuskripts.

Diese Rollen dürfen nicht vermischt werden, wenn der Auftrag nur eine davon verlangt.

## Git-Regeln

- Inhaltliche und technische Änderungen möglichst getrennt committen.
- Commit-Nachrichten konkret formulieren.
- Bestehende Fassungen nicht vernichten; Git-Historie erhalten.
- Große Umschreibungen bevorzugt auf einem eigenen Branch oder in einem Pull Request durchführen.
