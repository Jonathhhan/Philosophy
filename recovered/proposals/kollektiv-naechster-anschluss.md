# Automatenverbund der Anschlussfaehigkeit

Status: kombinierte Pruef- und Auffuehrungsspur; keine automatische Theorieentscheidung

## Eingabe

- markiert: Rollenpluralität
- unmarkiert: behaupteter Dissens
- Kontext: Wann bildet Verschiedenheit eine konkrete, nicht durch Mehrheit aufzulösende Spannung?

## Iterativer Lauf

- Lauf 1: Rollenpluralität / behaupteter Dissens
  - neue Begriffe: aktualisieren, algorithmus, anschliessen, asymmetrie, form, freiheit, kommunikation, komposition, programm, regel, reorganisieren, revidieren, stabilisieren, tragfaehigkeit
  - neue Manuskriptanker: manuskript\01-anschliessen.md:26, manuskript\04-form.md:77, manuskript\05-aktualisieren.md:11, manuskript\05-aktualisieren.md:111, manuskript\05-aktualisieren.md:47, manuskript\07-programm.md:59, manuskript\09-komponieren.md:104, manuskript\09-komponieren.md:55
  - neue Anschluesse: tractatus_automat->kunstwerk_automat:gemeinsame Begriffsadressen: aktualisieren, algorithmus, anschliessen, stabilisieren, unterscheidungsautomat->tractatus_automat:gemeinsame Begriffsadressen: aktualisieren, algorithmus, anschliessen, asymmetrie, form, freiheit, reorganisieren, stabilisieren, unterscheidungsautomat->tractatus_automat:gemeinsame Manuskriptanker: manuskript\01-anschliessen.md:26, manuskript\04-form.md:77, manuskript\05-aktualisieren.md:11, manuskript\05-aktualisieren.md:111, manuskript\05-aktualisieren.md:47
- Lauf 2: aktualisieren / Rollenpluralität
  - neue Begriffe: beurteilen, kritisieren, problematisieren
  - neue Anschluesse: tractatus_automat->kunstwerk_automat:gemeinsame Begriffsadressen: aktualisieren, reorganisieren
- Abbruch: produktive Differenz gefunden
- terminale Eingabe: aktualisieren / Rollenpluralität
- Zustand: `recovered\state\kollektiv-naechster-anschluss.json`

## Ermoeglichte Anschluesse

- `unterscheidungsautomat` -> `tractatus_automat`
  - gemeinsame Begriffsadressen: aktualisieren, algorithmus, anschliessen, asymmetrie, form, freiheit, reorganisieren, stabilisieren
  - gemeinsame Manuskriptanker: manuskript\01-anschliessen.md:26, manuskript\04-form.md:77, manuskript\05-aktualisieren.md:11, manuskript\05-aktualisieren.md:111, manuskript\05-aktualisieren.md:47
- `tractatus_automat` -> `kunstwerk_automat`
  - gemeinsame Begriffsadressen: aktualisieren, reorganisieren

## Verbundlauf

### 1. Unterscheiden: aktualisieren / Rollenpluralität
- Markierte Begriffsadressen: aktualisieren, asymmetrie, anschliessen, form, reorganisieren, stabilisieren
- Unmarkierte Begriffsadressen: anschliessen, asymmetrie, form, reorganisieren, stabilisieren, aktualisieren

### 2. Propositional ordnen

- 1 Leitsatz: aktualisieren / Rollenpluralität: Wann bildet Verschiedenheit eine konkrete, nicht durch Mehrheit aufzulösende Spannung? ist als Ordnung möglicher Anschlüsse zu prüfen, nicht als isolierte Behauptung.
- 1.1 Bestimmung: Was gesetzt wird, markiert eine Seite; was nicht gesetzt wird, bleibt als Bedingung der Setzung mitzuführen.
- 1.11 Grenze: Der Automat formuliert prüfbare Sätze, aber keine bestätigte Theorieentscheidung.
- 2 Begriffsadresse: Die erste erkannte Begriffsadresse ist Aktualisieren: Eine Anschlussmöglichkeit in einen bestimmten Vollzug überführen..
- 2.1 Nachbarbegriff: Asymmetrie bildet eine mögliche Anschlussadresse für die weitere Prüfung.
- 2.2 Nachbarbegriff: Anschließen bildet eine mögliche Anschlussadresse für die weitere Prüfung.

### 3. Auffuehren / Score erzeugen

```text
01: markiere Aktualisieren; fuehre Rollenpluralität als unmarkierte Seite mit.
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
