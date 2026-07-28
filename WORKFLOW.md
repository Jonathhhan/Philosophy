# Arbeitsablauf

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

## 3. Kontext lesen

Mindestens zu prüfen sind:

- das vollständige betroffene Kapitel;
- das vorhergehende und folgende Kapitel, soweit vorhanden;
- PROJECT.md;
- GLOSSAR.md;
- STYLE.md;
- relevante frühere Fassungen und Querverweise.

## 4. Schreiben

Bei einem neuen Entwurf:

1. argumentative Funktion des Abschnitts in einer internen Notiz bestimmen;
2. Anschluss an den vorherigen Abschnitt klären;
3. begriffliche Bewegung entwerfen;
4. Fließtext schreiben;
5. Definitionen und Leitthesen prüfen;
6. Übergang zum folgenden Abschnitt herstellen.

Interne Planungsnotizen gehören nicht automatisch in das Manuskript.

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

## 6. Änderung dokumentieren

Bei größeren Änderungen eine kurze Notiz in `projekt/arbeitsstand.md` ergänzen. Sie soll nennen:

- bearbeitete Datei;
- Ziel der Änderung;
- offene Fragen;
- noch nicht integrierte Varianten.

## 7. Technische Ausgabe

Die interaktive Ausgabe folgt dem Manuskript, ersetzt es aber nicht. Jedes Modul muss auch ohne Interaktion begrifflich verständlich bleiben. Die Interaktion soll eine operative Struktur des jeweiligen Begriffs erfahrbar machen und nicht bloß dekorieren.

## 8. Commit-Regeln

Beispiele für Commit-Nachrichten:

- `Add first draft of chapter 1`
- `Clarify distinction between revision and reorganization`
- `Add interactive prototype for Anschluss`
- `Fix internal chapter links`

Keine unbestimmten Nachrichten wie `update`, `changes` oder `stuff`.
