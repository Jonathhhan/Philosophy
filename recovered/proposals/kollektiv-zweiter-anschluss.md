# Automatenverbund der Anschlussfaehigkeit

Status: kombinierte Pruef- und Auffuehrungsspur; keine automatische Theorieentscheidung

## Eingabe

- markiert: Problematisieren
- unmarkiert: Aktualisieren
- Kontext: Wie wird aus der Aktualisierung eines Rollenbefunds eine konkrete, prüfbare Spannung, ohne Rollenpluralität mit Dissens gleichzusetzen?

## Iterativer Lauf

- Lauf 1: Problematisieren / Aktualisieren
  - neue Begriffe: moeglichkeitsraum
  - neue Manuskriptanker: manuskript\01-anschliessen.md:5, manuskript\01-anschliessen.md:9, manuskript\05-aktualisieren.md:99, manuskript\07-programm.md:61, manuskript\16-revidieren.md:23
  - neue Anschluesse: tractatus_automat->kunstwerk_automat:gemeinsame Begriffsadressen: aktualisieren, asymmetrie, freiheit, problematisieren, unterscheidungsautomat->tractatus_automat:gemeinsame Begriffsadressen: aktualisieren, asymmetrie, form, freiheit, problematisieren, tragfaehigkeit, unterscheidungsautomat->tractatus_automat:gemeinsame Manuskriptanker: manuskript\01-anschliessen.md:5, manuskript\01-anschliessen.md:9, manuskript\04-form.md:77, manuskript\05-aktualisieren.md:11, manuskript\05-aktualisieren.md:111
- Lauf 2: aktualisieren / Problematisieren
  - neue Anschluesse: tractatus_automat->kunstwerk_automat:gemeinsame Begriffsadressen: aktualisieren, problematisieren, tragfaehigkeit
- Abbruch: produktive Differenz gefunden
- terminale Eingabe: aktualisieren / Problematisieren
- Zustand: `recovered\state\kollektiv-naechster-anschluss.json`

## Ermoeglichte Anschluesse

- `unterscheidungsautomat` -> `tractatus_automat`
  - gemeinsame Begriffsadressen: aktualisieren, asymmetrie, form, freiheit, problematisieren, tragfaehigkeit
  - gemeinsame Manuskriptanker: manuskript\01-anschliessen.md:5, manuskript\01-anschliessen.md:9, manuskript\04-form.md:77, manuskript\05-aktualisieren.md:11, manuskript\05-aktualisieren.md:111
- `tractatus_automat` -> `kunstwerk_automat`
  - gemeinsame Begriffsadressen: aktualisieren, problematisieren, tragfaehigkeit

## Verbundlauf

### 1. Unterscheiden: aktualisieren / Problematisieren
- Markierte Begriffsadressen: aktualisieren, asymmetrie, form, freiheit, tragfaehigkeit
- Unmarkierte Begriffsadressen: aktualisieren, problematisieren, form, freiheit, tragfaehigkeit

### 2. Propositional ordnen

- 1 Leitsatz: aktualisieren / Problematisieren: Wie wird aus der Aktualisierung eines Rollenbefunds eine konkrete, prüfbare Spannung, ohne Rollenpluralität mit Dissens gleichzusetzen? ist als Ordnung möglicher Anschlüsse zu prüfen, nicht als isolierte Behauptung.
- 1.1 Bestimmung: Was gesetzt wird, markiert eine Seite; was nicht gesetzt wird, bleibt als Bedingung der Setzung mitzuführen.
- 1.11 Grenze: Der Automat formuliert prüfbare Sätze, aber keine bestätigte Theorieentscheidung.
- 2 Begriffsadresse: Die erste erkannte Begriffsadresse ist Aktualisieren: Eine Anschlussmöglichkeit in einen bestimmten Vollzug überführen..
- 2.1 Nachbarbegriff: Problematisieren bildet eine mögliche Anschlussadresse für die weitere Prüfung.
- 2.2 Nachbarbegriff: Asymmetrie bildet eine mögliche Anschlussadresse für die weitere Prüfung.

### 3. Auffuehren / Score erzeugen

```text
01: markiere Aktualisieren; fuehre Problematisieren als unmarkierte Seite mit.
02: markiere Programm; fuehre das durch Aktualisieren noch nicht Organisierte als unmarkierte Seite mit ueber required_for.
03: markiere Reorganisieren; fuehre das durch Programm noch nicht Organisierte als unmarkierte Seite mit ueber required_for.
04: markiere Revidieren; fuehre die Voraussetzung von Reorganisieren als unmarkierte Seite mit ueber depends_on.
05: markiere Tragfähigkeit; fuehre die Rueckwirkung auf Revidieren als unmarkierte Seite mit ueber inverse_related.
06: markiere Beurteilen; fuehre die Voraussetzung von Tragfähigkeit als unmarkierte Seite mit ueber depends_on.
07: markiere Kritisieren; fuehre die Voraussetzung von Beurteilen als unmarkierte Seite mit ueber depends_on.
08: markiere Problematisieren; fuehre die Voraussetzung von Kritisieren als unmarkierte Seite mit ueber depends_on.
```

Abbruch: gesetzte Schrittgrenze

## Grenzen

- Der Verbund kombiniert Automaten nur ueber ausgewiesene Anschlussbruecken.
- Eine blockierte Verbindung ist ein Pruefbefund, kein Fehler.
- Eine produktive Differenz ist ein neuer Begriff, Manuskriptanker oder Anschluss.
- Manuskriptintegration bleibt eine explizite editorische Operation.
