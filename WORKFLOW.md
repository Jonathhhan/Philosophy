# Arbeitsablauf

## Rekursive Arbeitsbewegung

Codex behandelt jede inhaltliche oder technische Änderung als Aktualisierung eines bereits organisierten Projektstands. Die Begriffe des Buches strukturieren die Prüfung analogisch; sie werden dadurch weder neu definiert noch zu Bezeichnungen beliebiger Softwarevorgänge verallgemeinert.

Die verbindliche Arbeitsbewegung lautet:

1. **Anschließen:** Auftrag, geltenden Stand, Quellen und betroffene Dateien aufnehmen.
2. **Organisieren:** Abhängigkeiten, Querverweise, Rollen und Entscheidungskompetenzen bestimmen.
3. **Aktualisieren:** die kleinste hinreichende Änderung ausführen.
4. **Reorganisieren:** relationale Folgen für weitere Projektbestandteile prüfen und nur bei Bedarf integrieren.
5. **Kritisieren:** Ergebnis, Auslassungen, Widersprüche und neu entstandene Unsicherheiten untersuchen.

Die Prüfung kann zu einer erneuten Problematisierung, Beurteilung oder Revision führen. Der Ablauf endet nicht deshalb erfolgreich, weil eine Datei geändert wurde, sondern wenn der beauftragte Gegenstand konsistent bearbeitet und seine relevanten Folgen geprüft sind.

Das Protokoll wird nach Eingriffstiefe skaliert:

- **lokal:** Anschließen → Aktualisieren → Prüfen;
- **kompositorisch:** Problematisieren → Form bestimmen → Aktualisieren → Komponieren → Stabilisieren → Prüfen;
- **strukturell:** vollständige rekursive Bewegung einschließlich Quellenprüfung, Beurteilung, Autorenentscheidung und erneuter Konsistenzprüfung.

Die Aufgabenvorlage unter `projekt/codex-auftragsvorlage.md` kann für umfangreiche oder wiederkehrende Arbeiten verwendet werden.

## 1. Ausgangsmaterial sichern

Neue Textfassungen werden zunächst unverändert oder nur typografisch bereinigt in das passende Manuskriptkapitel übernommen. Unsichere, abgebrochene oder beschädigte Stellen werden markiert. Rekonstruktionen dürfen nicht als Originaltext ausgegeben werden.

## 2. Auftrag bestimmen

Vor einer Bearbeitung ist festzuhalten, welche Art von Arbeit verlangt ist:

- Entwurf
- Fortsetzung
- argumentative Prüfung
- stilistisches Lektorat
- strukturelle Reorganisation
- Konsistenzprüfung
- Quellenarbeit
- technische Integration
- interaktive Umsetzung

Eine Aufgabe soll nicht stillschweigend in eine andere verwandelt werden.

Zusätzlich sind Rolle, Eingriffstiefe, veränderbare und geschützte Dateien sowie die erforderliche Entscheidungskompetenz zu bestimmen. Eine strukturelle Änderung darf nicht als lokale Korrektur ausgeführt werden. Wenn mehrere philosophisch plausible Richtungen bestehen, endet die Bearbeitung zunächst mit Varianten oder einer Autorenfrage.

## 3. Kontext lesen

Mindestens zu prüfen sind:

- das vollständige betroffene Kapitel;
- das vorhergehende und folgende Kapitel, soweit vorhanden;
- PROJECT.md;
- GLOSSAR.md;
- STYLE.md;
- relevante frühere Fassungen und Querverweise.

Das Kontextlesen bildet den Anschluss an den bestehenden Projektstand. Vor der Änderung ist zusätzlich zu bestimmen, welche Definitionen, Entscheidungen, Quellen, Kapitel, Wissensdateien und technischen Ausgaben von ihr abhängen. Diese Relationsprüfung organisiert den Eingriff, bevor er ausgeführt wird.

## 4. Schreiben

Bei einem neuen Entwurf:

1. argumentative Funktion des Abschnitts in einer internen Notiz bestimmen;
2. Anschluss an den vorherigen Abschnitt klären;
3. begriffliche Bewegung entwerfen;
4. Fließtext schreiben;
5. Definitionen und Leitthesen prüfen;
6. Übergang zum folgenden Abschnitt herstellen.

Interne Planungsnotizen gehören nicht automatisch in das Manuskript.

Vor dem Schreiben ist der Arbeitsmodus kenntlich zu machen: Folgt die Änderung einem bestätigten Arbeitsprogramm aus Definitionen und Entscheidungen, werden unter partieller Unbestimmtheit Varianten entwickelt, wird eine stabilisierte Fassung revidiert oder werden Beziehungen mehrerer Projektbestandteile reorganisiert? Varianten und Agentenvorschläge dürfen nicht ohne Autorenbestätigung als stabilisierte Theorie integriert werden.

## 5. Prüfen

Nach jeder inhaltlichen Änderung:

- Wurde eine Definition verschoben?
- Wurde ein neuer Grundbegriff eingeführt?
- Entsteht ein Widerspruch zu einem anderen Kapitel?
- Wird Montage nur als Beispiel behandelt, obwohl sie epistemische Funktion hat?
- Werden Programm und Algorithmus vermischt?
- Wird Revision mit Reorganisation verwechselt?
- Wird eine lokale Aussage unbegründet verallgemeinert?
- Bleibt die rekursive Bewegung des Projekts erkennbar?
- Verändert der Eingriff nur eine Fassung oder die Beziehungen mehrerer Projektbestandteile?
- Welche weiteren Bearbeitungsmöglichkeiten werden eröffnet, begrenzt oder zurückgestellt?
- Bleiben Quelle, begriffliche Entwicklung, Agentenvorschlag und bestätigter Status unterscheidbar?


## 6. Änderung dokumentieren

Bei größeren Änderungen eine kurze Notiz in `projekt/arbeitsstand.md` ergänzen. Sie soll nennen:

- bearbeitete Datei;
- Ziel der Änderung;
- offene Fragen;
- noch nicht integrierte Varianten.
- betroffene Anschlussbedingungen und Querverweise;
- eröffnete, begrenzte oder zurückgestellte Bearbeitungsmöglichkeiten;
- bestätigte und weiterhin unbestätigte Entscheidungen;
- durchgeführte Prüfungen und ihr Ergebnis.

Der Abschlussbericht an den Autor verwendet dieselben Angaben in knapper Form. Er beschreibt das Ergebnis, nicht lediglich die ausgeführten Werkzeuge oder Arbeitsschritte.

## 7. Technische Ausgabe

Die interaktive Ausgabe folgt dem Manuskript, ersetzt es aber nicht. Jedes Modul muss auch ohne Interaktion begrifflich verständlich bleiben. Die Interaktion soll eine operative Struktur des jeweiligen Begriffs erfahrbar machen und nicht bloß dekorieren.

## 8. Commit-Regeln

Beispiele für Commit-Nachrichten:

- `Add first draft of chapter 1`
- `Clarify distinction between revision and reorganization`
- `Add interactive prototype for Anschluss`
- `Fix internal chapter links`

Keine unbestimmten Nachrichten wie `update`, `changes` oder `stuff`.
