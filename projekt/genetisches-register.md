# Genetisches Register der Codex-Arbeit

Status: operatives Arbeitsprinzip fuer Codex; keine Manuskriptthese und kein biologischer Erklaerungsanspruch.

Dieses Register beschreibt, wie Codex Gedanken, Entwuerfe und technische Vorschlaege als genealogisch adressierbare Einheiten behandeln kann. Es erweitert das Zettelkasten-/Plateau-Prinzip: Eine Bearbeitung wird nicht nur abgelegt und verknuepft, sondern als Abstammungslinie von Anschlussmoeglichkeiten lesbar.

Der Begriff `genetisch` meint hier nicht Biologie im engeren Sinn. Er bezeichnet die rekonstruktive Frage, woraus ein Gedanke hervorgegangen ist, welche Unterscheidungen er erbt, wo er mutiert, welche Pruefungen er durchlaufen hat und welche Nachkommen er ermoeglicht.

## Grundsatz

Codex soll wichtige Gedanken nicht nur formulieren, sondern ihre Entstehung, Veraenderung und Stabilisierung sichtbar machen.

Eine genetische Codex-Bearbeitung fragt deshalb:

- Aus welchen Quellen, Manuskriptstellen, Entscheidungen oder frueheren Vorschlaegen stammt der Gedanke?
- Welche Unterscheidung traegt ihn?
- Welche Variante oder Mutation wird vorgeschlagen?
- Welche Pruefungen entscheiden ueber Anschlussfaehigkeit?
- Wer oder was hat die Entscheidung stabilisiert: Autor, delegierte Codex-Entscheidung, Validator, TODO?
- Welche spaeteren Bearbeitungen koennen aus ihm hervorgehen?

## Minimalformat

```yaml
id: G-0001
status: quelle | entwicklung | vorschlag | gepruefter_vorschlag | delegierte_codex_entscheidung | bestaetigt | todo | verworfen
adresse:
  primaer:
  weitere: []
herkunft:
  eltern: []
  quellen: []
  entscheidungen: []
unterscheidungen: []
mutation:
  typ: praezisierung | variation | einschub | korrektur | uebertragung | begrenzung | reorganisierung
  beschreibung:
pruefungen:
  konsistenz:
  genealogie:
  quellen:
  stil:
  technische_validierung:
entscheidung:
  status: autor | delegiert | offen | nicht_erforderlich
  referenz:
vererbt_an: []
begrenzt: []
oeffnet: []
todo: []
```

Das Format ist eine Arbeitsmaske. Es verpflichtet nicht dazu, jede kleine Korrektur zu registrieren. Es gilt fuer Gedanken, die mehrere Dateien, Begriffe, Entscheidungen oder Fassungen verbinden.

## Relation zum Zettelkasten

Der genetische Eintrag ersetzt den Zettel nicht. Er ergaenzt ihn um Abstammung und Variation.

- Der Zettel gibt dem Gedanken eine feste Adresse.
- Das Plateau zeigt seine nicht-linearen Anschlussstellen.
- Der genetische Eintrag zeigt seine Herkunft, Mutation, Pruefung und Nachkommen.

Dadurch entsteht keine starre Taxonomie. Wenn ein Gedanke spaeter anders gebraucht wird, wird er nicht umsortiert, sondern bekommt einen Folgezettel, eine Korrektur oder eine neue Vererbungsrelation.

## Relation zur delegierten Codex-Entscheidung

Wenn Codex innerhalb eines ausdruecklich erlaubten Bereichs eine vorlaeufige Entscheidung uebernimmt, kann diese Entscheidung genetisch dokumentiert werden. Dann muss der Eintrag ausweisen:

- warum der Fall delegierbar ist;
- welche Alternativen geprueft wurden;
- warum keine neue Grundthese, kein neuer Grundbegriff und keine Theorieachse entsteht;
- wie der Autor die Entscheidung spaeter revidieren kann.

Eine delegierte Entscheidung ist kein Endpunkt. Sie ist ein stabilisierter Zwischenzustand mit Revisionsadresse.

## Beispiel: Algorithmusidentitaet

```yaml
id: G-0001
status: bestaetigt
adresse:
  primaer: knowledge/concepts/algorithmus.yaml
  weitere:
    - manuskript/08-algorithmus.md
herkunft:
  eltern:
    - programm/algorithmus-unterscheidung
    - montage/ausfuehrung-material
  quellen:
    - sources/master/Algorithmische_Komposition_in_der_Filmmontage.pdf
  entscheidungen:
    - knowledge/change-events/0029-distinction-and-tractatus-automata.yaml
unterscheidungen:
  - strukturelle_gleichheit / funktionale_austauschbarkeit
  - algorithmus / ausfuehrung
  - uebergangsordnung / materieller_traeger
mutation:
  typ: praezisierung
  beschreibung: Algorithmusidentitaet wird nicht ueber gleiche Ergebnisse bestimmt, sondern ueber strukturerhaltende Gleichheit der relevanten Uebergangsordnung auf ausgewiesener Analyseebene.
pruefungen:
  konsistenz: mit Programmbegriff und Algorithmuskapitel abzugleichen
  genealogie: Herkunft aus Montage, Programm und Algorithmus sichtbar halten
  quellen: genaue Seitenangaben nur nach erneuter Quellenpruefung
  stil: nicht als technische Definition isolieren
  technische_validierung: nicht zutreffend
entscheidung:
  status: autor
  referenz: bestehender Projektstand nach Algorithmusidentitaetsdiskussion
vererbt_an:
  - scripts/unterscheidungsautomat.py
  - recovered/proposals/unterscheidung-algorithmus-ausfuehrung.md
begrenzt:
  - Gleichsetzung von Ergebnisgleichheit und Algorithmusidentitaet
oeffnet:
  - genauere Pruefung von Implementierung, Darstellung und Ausfuehrung
todo:
  - Seitenangaben aus der Masterarbeit ergaenzen, falls der Gedanke im Manuskript quellenbezogen ausgearbeitet wird.
```

## Operativer Ablauf

1. **Anschliessen:** Codex sucht Eltern: Quellen, Kapitel, Entscheidungen, fruehere Zettel, Change Events, Vorschlaege.
2. **Unterscheiden:** Codex bestimmt die tragende Differenz des Gedankens.
3. **Variieren:** Codex erzeugt eine kontrollierte Mutation: Praezisierung, Einschub, Korrektur, Uebertragung oder Begrenzung.
4. **Pruefen:** Codex prueft Konsistenz, Genealogie, Quellenstatus, Stil und technische Folgen.
5. **Entscheiden:** Autorentscheidung, delegierte Codex-Entscheidung, offene Variante oder Verwerfung werden sichtbar getrennt.
6. **Vererben:** Codex dokumentiert, welche spaeteren Dateien, Vorschlaege oder Manuskriptstellen auf dem Gedanken aufbauen.

## Grenze

Das genetische Register macht Entwicklung sichtbar. Es beweist nicht, dass eine Entwicklung philosophisch richtig ist. Es verhindert vor allem drei Fehler:

- ein Vorschlag erscheint als bestaetigte Theorie;
- eine technische Umsetzung verdeckt ihre begriffliche Herkunft;
- eine spaetere Fassung verliert die Spur ihrer Entscheidung.