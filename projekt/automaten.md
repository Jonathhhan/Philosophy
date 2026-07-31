# Automaten der Unterscheidung und propositionalen Ordnung

Diese Werkzeuge erweitern die vorhandenen Projektwerkzeuge um lesende Prüfmodi. Sie stabilisieren keine neue Theorieachse und verändern für sich genommen keine Manuskriptdateien. Der Automatenverbund kann die Prüfungen jedoch selbstständig verketten, bereits geprüfte Zustände persistent erkennen und bis zu einer produktiven Differenz weiterarbeiten.

## Codex-Automat der Unterscheidung

`scripts/unterscheidungsautomat.py` analysiert eine Unterscheidung als markierte und unmarkierte Seite. Er ist von George Spencer Browns Formdenken inspiriert, wird hier aber nur als operative Beobachtungsfigur verwendet.

Beispiele:

```powershell
python scripts\unterscheidungsautomat.py "Organisation" "nicht organisierter Möglichkeitsraum"
python scripts\unterscheidungsautomat.py "Algorithmus" "materielle Ausführung" --context "Identität über Implementierungen hinweg"
python scripts\unterscheidungsautomat.py "Kritik" "Organisation" --format json
```

Der Automat fragt:

- Welche Seite wird markiert?
- Welche Seite läuft unmarkiert mit?
- Welche Concept-Dateien werden berührt?
- Welche Manuskriptanker bieten Leseanschlüsse?
- Welche Grenzwarnungen entstehen?

## Tractatus-philosophicus-Automat

`scripts/tractatus_automat.py` erzeugt zu einem Thema eine nummerierte, propositionale Prüfstruktur. Die Nummerierung dient der Ordnung von Leitsatz, Unterthese, Grenze und Anschluss. Sie imitiert keinen Autorstil und ersetzt keine philosophische Ausarbeitung.

Beispiele:

```powershell
python scripts\tractatus_automat.py "Jede Aktualisierung verändert den Raum weiterer Anschlussmöglichkeiten"
python scripts\tractatus_automat.py "Algorithmusidentität" --output recovered\proposals\tractatus-algorithmusidentitaet.md
python scripts\tractatus_automat.py "Organisation und Kritik" --format json
```

## Selbstprogrammierendes Kunstwerk der Anschlussunterscheidungen

`scripts/kunstwerk_automat.py` lässt eine Folge von Unterscheidungen von einer Startmarkierung aus laufen. Der Automat verändert nicht seinen Quellcode. Stattdessen erzeugt jeder Schritt eine neue Programmlinie seines eigenen Scores: Die Aufführung schreibt also die Regelspur, nach der sie als Kunstwerk lesbar wird.

Beispiele:

```powershell
python scripts\kunstwerk_automat.py Anschliessen Nicht-Anschluss --max-steps 17
python scripts\kunstwerk_automat.py Algorithmus materielle-Ausfuehrung --max-steps 8 --format json
python scripts\kunstwerk_automat.py Form Unmarkiertes --output recovered\proposals\kunstwerk-form-lauf.md
```

Der Automat läuft bis zu einer Abbruchbedingung:

- gesetzte Schrittgrenze;
- keine unbesuchte deklarierte Anschlussstelle;
- Wiederkehr einer bereits besuchten Begriffsadresse ohne neue Relation;
- ausdrücklicher Stopp durch Grenzwarnung oder editorische Entscheidung.

Die Ausgabe ist eine Aufführungsspur: markierte Seite, unmarkierte Seite, Anschlussrelation, Concept-Datei, Grenzen und generierter Score. Sie ist kein Manuskripttext und keine Theorieentscheidung.

## Automatenverbund

`scripts/automatenverbund.py` kombiniert Unterscheidungsautomat, Tractatus-Automat und Kunstwerk-Automat dort, wo Anschlüsse nachweisbar sind. Der Verbund prüft Brücken über gemeinsame Begriffsadressen, Manuskriptanker oder deklarierte Concept-Relationen. Wo keine Brücke besteht, wird die Verbindung blockiert und als Befund ausgegeben.

Ein einzelner Lauf:

```powershell
python scripts\automatenverbund.py Anschliessen Nicht-Anschluss --context "von der ersten Unterscheidung bis zur Aufführung" --max-steps 8
```

Der Verbund erzeugt drei Stufen:

1. Unterscheiden: markierte und unmarkierte Seite mit Begriffsadressen.
2. Propositional ordnen: Tractatus-Struktur aus Leitsatz, Grenze und Anschluss.
3. Aufführen: Kunstwerk-Score entlang deklarierter Relationen.

## Iterativer Modus bis zur produktiven Differenz

Mit `--until-new` verfolgt der Verbund die im Lauf gefundenen Begriffsadressen selbstständig weiter. Jeder neu erreichte Begriff wird mit dem vorherigen Begriff als Gegenbegriff geprüft. Bereits bearbeitete Eingaben werden nicht wiederholt.

```powershell
python scripts\automatenverbund.py Organisation Nicht-Organisation `
  --context "Organisation von Möglichkeiten" `
  --until-new `
  --max-runs 20 `
  --output recovered\proposals\naechste-produktive-differenz.md
```

Der iterative Modus verwaltet standardmäßig seinen persistenten Zustand in:

```text
recovered/state/automatenverbund-state.json
```

Gespeichert werden:

- bereits geprüfte Begriffspaare;
- erreichte Begriffsadressen;
- gefundene Manuskriptanker;
- nachgewiesene Anschlussbrücken.

Die Gesamtausgabe unterscheidet dabei die ursprüngliche Eingabe von der terminalen Eingabe des letzten Folgelaufs. Dadurch bleibt nachvollziehbar, welche Unterscheidung den Lauf ausgelöst hat, auch wenn der Verbund anschließend selbst weitere Begriffsadressen verfolgt.

Der erste Lauf bildet den Ausgangsstand. Danach arbeitet der Verbund weiter, bis mindestens eine produktive Differenz entsteht:

- ein zuvor nicht erreichter Begriff;
- ein neuer Manuskriptanker;
- eine neue Anschlussbrücke zwischen Automaten.

Ein weiterer Prüftext ohne neue Differenz beendet den Prozess nicht. Er wird als bereits bekannter Zustand behandelt, und der Verbund verfolgt den nächsten noch ungeprüften Anschluss. Entsteht innerhalb der Laufgrenze nichts Neues, endet der Lauf mit der ausdrücklichen Diagnose, dass der erreichbare neue Suchraum erschöpft oder die gesetzte Laufgrenze erreicht ist.

Ein eigener Zustandsstand kann mit `--state-file` gewählt werden:

```powershell
python scripts\automatenverbund.py Verteilung Asymmetrie `
  --until-new `
  --state-file recovered\state\verteilung-asymmetrie.json
```

## Verhältnis zur Redaktion

Eine produktive Differenz ist noch kein gültiger Manuskripttext. Sie ist ein neuer, hinreichend bestimmter editorischer Prüfgegenstand. Die anschließende Redaktion entscheidet:

- `PATCH`, wenn die Differenz einen begründbaren Manuskripteingriff trägt;
- `KEEP`, wenn der neue Befund eine vorhandene Stelle bestätigt;
- `BLOCKED`, wenn für eine Integration Evidenz oder begriffliche Bestimmung fehlt.

Der Automatenlauf verhindert damit zwei entgegengesetzte Fehler: Er bricht nicht schon bei einer weiteren bloßen Prüfspur ab, und er wiederholt auch nicht endlos denselben Zustand.

## Gemeinsame Grenzen

- Die Werkzeuge schreiben Ausgaben nur mit explizitem `--output`.
- Der persistente Zustand ist kein theoretischer Wahrheitsbestand, sondern ein Gedächtnis bereits geprüfter Anschlüsse.
- Eine produktive Differenz ist zunächst ein editorischer Prüfgegenstand, noch keine Theorieentscheidung.
- Manuskriptintegration bleibt eine explizite editorische Operation mit Quellenprüfung und begrifflicher Begründung.
