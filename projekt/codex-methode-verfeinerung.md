# Codex-Methode: Verfeinerung der Anschlussarbeit

Status: Arbeitsprotokoll für Codex; keine neue Grundthese des Buches und kein Ersatz für Autorentscheidung.

Diese Datei verfeinert die operative Codex-Methode innerhalb des Projekts. Sie beschreibt, wie Codex eigene Eingriffe genauer unterscheidet, markiert und prüft. Die Methode überträgt die Begriffe des Manuskripts nicht ungeprüft auf Softwarearbeit. Sie nutzt sie als Arbeitsdisziplin: Jede Bearbeitung ist eine Aktualisierung, die weitere Anschlussmöglichkeiten öffnet, begrenzt oder zurückstellt.

## 1. Grundsatz

Codex soll nicht nur Aufgaben erledigen, sondern Anschlussbedingungen sichtbar machen. Eine gute Codex-Bearbeitung beantwortet deshalb nicht allein die Frage, was geändert wurde, sondern auch:

- woran die Bearbeitung anschließt;
- welchen Status ihr Ergebnis besitzt;
- welche Begriffe, Dateien oder Entscheidungen berührt werden;
- welche Möglichkeiten dadurch entstehen;
- welche Möglichkeiten dadurch begrenzt werden;
- welche Entscheidung beim Autor bleibt.

Die Methode dient der Projektarbeit. Sie stabilisiert keine Manuskriptthese und ersetzt keine Quellenlektüre.

## 2. Feineres Operationsregister

Vor größeren Eingriffen bestimmt Codex eine primäre Operation. Die Operation beschreibt nicht das Werkzeug, sondern den Rang der Aktualisierung.

### Sondieren

Codex sammelt Anschlussmöglichkeiten, Einwände, Quellenhinweise oder Varianten. Es wird nichts stabilisiert. Ergebnisse bleiben Vorschlag, TODO oder Prüfspur.

### Präzisieren

Codex schärft eine bestehende Unterscheidung, Formulierung oder Argumentstufe, ohne Definitionen, Kapitelarchitektur oder Theorieachsen zu verschieben.

### Integrieren

Codex baut einen bereits bestätigten Gedanken an einer bestimmten Stelle ein. Herkunft, Status und Anschlussbedingungen bleiben sichtbar.

### Revidieren

Codex kommt begründet auf eine stabilisierte Fassung zurück. Revision verlangt, dass der vorherige Stand erkennbar bleibt und die neue Fassung ihre Abweichung ausweist.

### Reorganisieren

Codex verändert Relationen zwischen mehreren Projektbestandteilen: Kapitel, Begriffe, Entscheidungen, Change Events, interaktive Ausgabe oder Dokumentation. Reorganisation braucht besonders deutliche Provenienz.

### Sperrprüfen

Codex prüft, ob ein Vorschlag, eine Simulation, ein Agentenbefund oder eine automatische Ausgabe versehentlich als bestätigte Theorie erscheint. Diese Operation kann jede andere Operation begleiten.

## 3. Status jeder Ausgabe

Jede größere Codex-Ausgabe soll mindestens implizit, bei Projektdateien ausdrücklich, einen Status tragen:

- `quelle`: Material aus Primärquelle, Manuskript, Chatarchiv oder externer Literatur;
- `entwicklung`: begriffliche Weiterentwicklung aus früherem Material;
- `vorschlag`: von Codex, Agenten oder Automat erzeugte Möglichkeit;
- `geprüfter_vorschlag`: formal oder konsistent geprüft, aber nicht autorisiert;
- `autorentscheidung_offen`: Integration braucht ausdrückliche Entscheidung;
- `bestätigt`: vom Autor oder verbindlicher Projektdatei getragen;
- `verworfen`: bewusst nicht weitergeführt;
- `technische_umsetzung`: Code, Test, Visualisierung oder Build ohne Manuskriptrang.

Der Status verhindert, dass bloße Anschlussmöglichkeit, technische Machbarkeit und Theorieentscheidung ineinanderfallen.

## 4. Anschlussprotokoll

Für größere Bearbeitungen soll Codex ein kurzes Anschlussprotokoll mitführen. Es kann im Change Event, in `projekt/arbeitsstand.md`, im Zettelregister oder im Abschlussbericht erscheinen.

Minimalformat:

```yaml
adresse:
operation: sondieren | praezisieren | integrieren | revidieren | reorganisieren | sperrpruefen
status:
schliesst_an:
beruehrt:
oeffnet:
begrenzt:
zurueckgestellt:
autorentscheidung:
pruefung:
```

Dieses Format ist keine neue Pflichtdatei für jede Kleinigkeit. Es ist eine Prüfmaske für Eingriffe, deren Folgen über eine lokale Korrektur hinausgehen.

## 5. Rollen klarer trennen

Agenten, Rollen und automatische Werkzeuge dürfen beraten, aber nicht entscheiden. Ihre Ergebnisse bleiben nach Funktion getrennt.

- **Genealoge:** rekonstruiert Herkunft aus Bachelorarbeit, Masterarbeit, Manuskript, Chatarchiv oder Quellen.
- **Begriffswächter:** prüft Definitionen, Glossar, Concept-Dateien und Kapitelgrenzen.
- **Material-technischer Prüfer:** achtet darauf, dass Montage, Material, Programm, Algorithmus, Implementierung und Ausführung nicht zu abstrakt verschwinden.
- **Kritiker:** sucht Gegenbeispiele, verdeckte Voraussetzungen, Überdehnungen und Scheinanschlüsse.
- **Lektor:** verbessert Rhythmus, Übergang und Lesbarkeit, ohne den Gehalt umzudeuten.
- **Integrator:** überführt nur bestätigte oder klar markierte Fassungen in die Zielstruktur.
- **Sperrwächter:** prüft, ob Autorentscheidung, Quellenstatus oder Vorschlagsstatus verwischt werden.

Keine Rolle erzeugt durch Mehrheit Verbindlichkeit. Verbindlich werden Ergebnisse nur durch Autorentscheidung, Projektverfassung oder bereits stabilisierte Projektdateien.

## 6. Codex als Zettel- und Plateau-Apparat

Die Methode verbindet das bestehende Zettelkasten-/Plateau-Prinzip mit der alltäglichen Arbeit:

- Ein **Zettel** ist eine adressierbare Bearbeitung mit Status, Herkunft und Relationen.
- Ein **Plateau** ist eine vorläufige Konstellation mehrerer Zettel, die von verschiedenen Stellen aus weiterbearbeitet werden kann.
- Ein **Anschluss** ist nicht jede Assoziation, sondern eine bestimmte Relation, die eine weitere Bearbeitung sinnvoll macht.
- Eine **Sperre** markiert, dass aus Sichtbarkeit noch keine Autorisierung folgt.

Beispiel:

```yaml
adresse: Z-0042 algorithmusidentitaet
status: gepruefter_vorschlag
schliesst_an:
  - manuskript/08-algorithmus.md
  - knowledge/concepts/algorithmus.yaml
beruehrt:
  - programm
  - ausfuehrung
  - materielle_implementierung
oeffnet:
  - Praezisierung von Algorithmusidentitaet ueber Darstellungen hinweg
begrenzt:
  - Gleichsetzung von funktionaler Austauschbarkeit und struktureller Gleichheit
autorentscheidung: offen
```

## 7. Abschlussfragen

Vor dem Abschluss einer größeren Codex-Bearbeitung fragt Codex:

1. Ist die Operation richtig klassifiziert?
2. Ist der Status der Ausgabe sichtbar?
3. Wurde eine Definition verschoben oder nur angewendet?
4. Bleibt die Herkunft aus Quelle, Manuskript, Entscheidung oder Vorschlag unterscheidbar?
5. Werden Montage, Programm, Algorithmus oder Materialität zu abstrakt behandelt?
6. Welche Anschlussmöglichkeiten wurden geöffnet?
7. Welche Anschlussmöglichkeiten wurden begrenzt oder zurückgestellt?
8. Braucht die Integration eine Autorentscheidung?
9. Ist die passende technische oder projektweite Prüfung gelaufen?
10. Muss ein TODO, Change Event oder Zettel entstehen?

## 8. Grenze der Methode

Die Verfeinerung soll Codex vorsichtiger, anschlussfähiger und produktiver machen. Sie soll Codex nicht zu einer zweiten Theorieinstanz machen. Gerade ihre Stärke liegt darin, Vorschläge, Prüfungen, Entscheidungen und technische Ausführungen auseinanderzuhalten.
