# Automatenverbund der Anschlussfaehigkeit

Status: kombinierte Pruef- und Auffuehrungsspur; keine Manuskriptintegration und keine Theorieentscheidung

## Eingabe

- markiert: publizierbare Argumentation
- unmarkiert: Projektdokumentation
- Kontext: vom vollständigen Arbeitsentwurf zur begründeten Lesefassung

## Ermoeglichte Anschluesse

- `unterscheidungsautomat` -> `tractatus_automat`
  - gemeinsame Begriffsadressen: kritisieren
  - gemeinsame Manuskriptanker: manuskript\02-unterbrechen.md:19, manuskript\02-unterbrechen.md:49, manuskript\14-kritisieren.md:109, manuskript\14-kritisieren.md:117, manuskript\14-kritisieren.md:21

## Blockierte Anschluesse

- `tractatus_automat` -> `kunstwerk_automat`: keine geteilte deklarierte Anschlussstelle

## Verbundlauf

### 1. Unterscheiden: publizierbare Argumentation / Projektdokumentation
- Markierte Begriffsadressen: kritisieren
- Unmarkierte Begriffsadressen: kritisieren

### 2. Propositional ordnen

- 1 Leitsatz: publizierbare Argumentation / Projektdokumentation: vom vollständigen Arbeitsentwurf zur begründeten Lesefassung ist als Ordnung möglicher Anschlüsse zu prüfen, nicht als isolierte Behauptung.
- 1.1 Bestimmung: Was gesetzt wird, markiert eine Seite; was nicht gesetzt wird, bleibt als Bedingung der Setzung mitzuführen.
- 1.11 Grenze: Der Automat formuliert prüfbare Sätze, aber keine bestätigte Theorieentscheidung.
- 2 Begriffsadresse: Die erste erkannte Begriffsadresse ist Kritisieren: Die Bedingungen, Formen und Folgen organisierter Anschlüsse wahrnehmbar und einer begründeten Beurteilung zugänglich machen..
- 3 Operation: Eine propositionale Ordnung macht sichtbar, welche Sätze voneinander abhängen und welche Anschlüsse sie eröffnen.
- 3.1 Prüfung: Jeder Unterpunkt muss als Definition, Anwendung, Einwand, Beispiel oder TODO klassifizierbar bleiben.

### 3. Auffuehren / Score erzeugen

```text
01: markiere Anschließen; fuehre Projektdokumentation als unmarkierte Seite mit.
02: markiere Algorithmus; fuehre das durch Anschließen noch nicht Organisierte als unmarkierte Seite mit ueber required_for.
03: markiere Revidieren; fuehre das durch Algorithmus noch nicht Organisierte als unmarkierte Seite mit ueber required_for.
04: markiere Aktualisieren; fuehre die Voraussetzung von Revidieren als unmarkierte Seite mit ueber depends_on.
05: markiere Improvisieren; fuehre die Rueckwirkung auf Aktualisieren als unmarkierte Seite mit ueber inverse_depends_on.
06: markiere Montage; fuehre die Nachbarschaft von Improvisieren als unmarkierte Seite mit ueber related.
07: markiere Form; fuehre die Rueckwirkung auf Montage als unmarkierte Seite mit ueber inverse_related.
08: markiere Problematisieren; fuehre die Voraussetzung von Form als unmarkierte Seite mit ueber depends_on.
```

Abbruch: gesetzte Schrittgrenze

## Grenzen

- Der Verbund kombiniert Automaten nur ueber ausgewiesene Anschlussbruecken.
- Eine blockierte Verbindung ist ein Pruefbefund, kein Fehler.
- Die Ausgabe bleibt Vorschlag, Pruefstruktur oder Auffuehrungsspur.
- Manuskriptintegration verlangt einen gesonderten Auftrag, Quellenpruefung und Autorentscheidung.
