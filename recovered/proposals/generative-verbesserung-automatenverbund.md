# Automatenverbund der Anschlussfaehigkeit

Status: kombinierte Pruef- und Auffuehrungsspur; keine automatische Theorieentscheidung

## Eingabe

- markiert: aktualisieren
- unmarkiert: Generierung
- Kontext: Qualität der autonomen Theoriegenese: deklarierter source_context versus tatsächlich im Prompt verwendeter Quelleninhalt, Provenienz, Projektgrenzen und produktive Differenz

## Iterativer Lauf

- Lauf 1: Generierung / bloße Dateierzeugung
  - neue Begriffe: aktualisieren, algorithmus, anschliessen, form, fortsetzen, improvisieren, moeglichkeitsraum, montage, problematisieren, revidieren, unterbrechen
  - neue Manuskriptanker: manuskript\04-form.md:83, manuskript\05-aktualisieren.md:47, manuskript\05-aktualisieren.md:9, manuskript\05-aktualisieren.md:99, manuskript\07-programm.md:105, manuskript\08-algorithmus.md:101, manuskript\08-algorithmus.md:37, manuskript\11-organisieren.md:87
  - neue Anschluesse: tractatus_automat->kunstwerk_automat:gemeinsame Begriffsadressen: aktualisieren, algorithmus, fortsetzen, revidieren, unterscheidungsautomat->tractatus_automat:gemeinsame Begriffsadressen: aktualisieren, algorithmus, fortsetzen, moeglichkeitsraum, revidieren, unterscheidungsautomat->tractatus_automat:gemeinsame Manuskriptanker: manuskript\04-form.md:83, manuskript\05-aktualisieren.md:47, manuskript\05-aktualisieren.md:9, manuskript\05-aktualisieren.md:99, manuskript\07-programm.md:105
- Lauf 2: aktualisieren / Generierung
  - neue Begriffe: asymmetrie, komposition, programm, reorganisieren, stabilisieren
  - neue Manuskriptanker: manuskript\01-anschliessen.md:32, manuskript\02-unterbrechen.md:31, manuskript\04-form.md:77, manuskript\07-programm.md:21, manuskript\12-verteilen.md:119, manuskript\13-asymmetrie.md:89, manuskript\16-revidieren.md:23
  - neue Anschluesse: tractatus_automat->kunstwerk_automat:gemeinsame Begriffsadressen: aktualisieren, unterscheidungsautomat->tractatus_automat:gemeinsame Begriffsadressen: aktualisieren, asymmetrie, unterscheidungsautomat->tractatus_automat:gemeinsame Manuskriptanker: manuskript\01-anschliessen.md:32, manuskript\02-unterbrechen.md:31, manuskript\04-form.md:77, manuskript\05-aktualisieren.md:99, manuskript\07-programm.md:21
- Abbruch: produktive Differenz gefunden
- Zustand: `recovered\state\generative-verbesserung.json`

## Ermoeglichte Anschluesse

- `unterscheidungsautomat` -> `tractatus_automat`
  - gemeinsame Begriffsadressen: aktualisieren, asymmetrie
  - gemeinsame Manuskriptanker: manuskript\01-anschliessen.md:32, manuskript\02-unterbrechen.md:31, manuskript\04-form.md:77, manuskript\05-aktualisieren.md:99, manuskript\07-programm.md:21
- `tractatus_automat` -> `kunstwerk_automat`
  - gemeinsame Begriffsadressen: aktualisieren

## Verbundlauf

### 1. Unterscheiden: aktualisieren / Generierung
- Markierte Begriffsadressen: aktualisieren, asymmetrie

### 2. Propositional ordnen

- 1 Leitsatz: aktualisieren / Generierung: Qualität der autonomen Theoriegenese: deklarierter source_context versus tatsächlich im Prompt verwendeter Quelleninhalt, Provenienz, Projektgrenzen und produktive Differenz ist als Ordnung möglicher Anschlüsse zu prüfen, nicht als isolierte Behauptung.
- 1.1 Bestimmung: Was gesetzt wird, markiert eine Seite; was nicht gesetzt wird, bleibt als Bedingung der Setzung mitzuführen.
- 1.11 Grenze: Der Automat formuliert prüfbare Sätze, aber keine bestätigte Theorieentscheidung.
- 2 Begriffsadresse: Die erste erkannte Begriffsadresse ist Aktualisieren: Eine Anschlussmöglichkeit in einen bestimmten Vollzug überführen..
- 2.1 Nachbarbegriff: Asymmetrie bildet eine mögliche Anschlussadresse für die weitere Prüfung.
- 3 Operation: Eine propositionale Ordnung macht sichtbar, welche Sätze voneinander abhängen und welche Anschlüsse sie eröffnen.

### 3. Auffuehren / Score erzeugen

```text
01: markiere Aktualisieren; fuehre Generierung als unmarkierte Seite mit.
02: markiere Programm; fuehre das durch Aktualisieren noch nicht Organisierte als unmarkierte Seite mit ueber required_for.
03: markiere Reorganisieren; fuehre das durch Programm noch nicht Organisierte als unmarkierte Seite mit ueber required_for.
04: markiere Revidieren; fuehre die Voraussetzung von Reorganisieren als unmarkierte Seite mit ueber depends_on.
05: markiere Stabilisieren; fuehre die Nachbarschaft von Revidieren als unmarkierte Seite mit ueber related.
06: markiere Komposition; fuehre die Nachbarschaft von Stabilisieren als unmarkierte Seite mit ueber related.
07: markiere Montage; fuehre die Rueckwirkung auf Komposition als unmarkierte Seite mit ueber inverse_related.
08: markiere Improvisieren; fuehre das durch Montage noch nicht Organisierte als unmarkierte Seite mit ueber required_for.
09: markiere Form; fuehre die Voraussetzung von Improvisieren als unmarkierte Seite mit ueber depends_on.
10: markiere Problematisieren; fuehre die Voraussetzung von Form als unmarkierte Seite mit ueber depends_on.
```

Abbruch: gesetzte Schrittgrenze

## Grenzen

- Der Verbund kombiniert Automaten nur ueber ausgewiesene Anschlussbruecken.
- Eine blockierte Verbindung ist ein Pruefbefund, kein Fehler.
- Eine produktive Differenz ist ein neuer Begriff, Manuskriptanker oder Anschluss.
- Manuskriptintegration bleibt eine explizite editorische Operation.
