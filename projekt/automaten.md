# Automaten der Unterscheidung und propositionalen Ordnung

Diese Werkzeuge erweitern die vorhandenen Projektwerkzeuge um lesende Prüfmodi. Sie stabilisieren keine neue Theorieachse und verändern für sich genommen keine Manuskriptdateien. Im editorischen Arbeitsablauf dienen sie jedoch einer Entscheidung, die entweder zu einem Manuskriptpatch oder zu einem begründeten Abschluss führt.

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

Der Automat fragt nicht nach der letzten Wahrheit. Er läuft bis zu einer Abbruchbedingung:

- gesetzte Schrittgrenze;
- keine unbesuchte deklarierte Anschlussstelle;
- Wiederkehr einer bereits besuchten Begriffsadresse ohne neue Relation;
- ausdrücklicher Stopp durch Grenzwarnung oder editorische Entscheidung.

Die Ausgabe ist eine Aufführungsspur: markierte Seite, unmarkierte Seite, Anschlussrelation, Concept-Datei, Grenzen und generierter Score. Sie ist kein Manuskripttext und keine Theorieentscheidung.

## Automatenverbund

`scripts/automatenverbund.py` kombiniert Unterscheidungsautomat, Tractatus-Automat und Kunstwerk-Automat dort, wo Anschlüsse nachweisbar sind. Der Verbund prüft Brücken über gemeinsame Begriffsadressen, Manuskriptanker oder deklarierte Concept-Relationen. Wo keine Brücke besteht, wird die Verbindung blockiert und als Befund ausgegeben.

Beispiele:

```powershell
python scripts\automatenverbund.py Anschliessen Nicht-Anschluss --context "von der ersten Unterscheidung bis zur Auffuehrung" --max-steps 8
python scripts\automatenverbund.py Algorithmus materielle-Ausfuehrung --context "Identitaet ueber Implementierungen" --format json
python scripts\automatenverbund.py Form Unmarkiertes --output recovered\proposals\automatenverbund-form.md
```

Der Verbund erzeugt drei Stufen:

1. Unterscheiden: markierte und unmarkierte Seite mit Begriffsadressen.
2. Propositional ordnen: Tractatus-Struktur aus Leitsatz, Grenze und Anschluss.
3. Aufführen: Kunstwerk-Score entlang deklarierter Relationen.

Er schreibt nur mit explizitem `--output` und bleibt Proposal, Prüfstruktur oder Aufführungsspur.

## Schutz vor endlosem Regress

Automaten dürfen einander nur innerhalb eines einzelnen, begrenzten Prüflaufs aufrufen. Eine Ausgabe darf nicht allein deshalb zum Eingang eines gleichartigen neuen Laufs werden, weil sie weitere mögliche Unterscheidungen enthält. Möglichkeit allein ist kein Arbeitsauftrag.

Für denselben Gegenstand gilt:

1. ein Hauptlauf;
2. höchstens ein gezielter Gegencheck bei einem konkreten Widerspruch;
3. danach Entscheidung durch den Editor: `PATCH`, `KEEP` oder `BLOCKED`.

Ein Lauf ohne neue Textstelle, neue Quelle, neue Relation oder neuen Widerspruch wird nicht wiederholt. Nach einem Patch wechselt die Redaktion zum nächsten Abschnitt. Eine Rückkehr erfolgt nur, wenn eine spätere Änderung den früheren Befund tatsächlich verändert.

## Gemeinsame Grenzen

- Die Werkzeuge schreiben nur mit explizitem `--output`.
- Ausgaben sind Vorschläge, Prüfstrukturen oder Lesehilfen.
- Ein Audit ist kein Selbstzweck und darf kein weiteres Audit als einzigen Output erzeugen.
- Manuskriptintegration erfordert Quellenprüfung und eine explizite editorische Entscheidung; eine erneute Autorfreigabe ist nur nötig, wenn eine Entscheidung nicht aus den Projektvorgaben und dem Textbestand ableitbar ist.
