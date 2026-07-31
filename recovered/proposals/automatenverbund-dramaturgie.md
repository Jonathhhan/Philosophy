# Automatenverbund der Anschlussfaehigkeit

Status: kombinierte Pruef- und Auffuehrungsspur; keine Manuskriptintegration und keine Theorieentscheidung

## Eingabe

- markiert: dramaturgische Verdichtung
- unmarkiert: Einleitung
- Kontext: von der ersten Unterscheidung bis zur Auffuehrung

## Ermoeglichte Anschluesse

- `unterscheidungsautomat` -> `tractatus_automat`
  - gemeinsame Begriffsadressen: form
  - gemeinsame Manuskriptanker: manuskript\04-form.md:23, manuskript\04-form.md:55, manuskript\04-form.md:7, manuskript\04-form.md:79, manuskript\04-form.md:9
- `tractatus_automat` -> `kunstwerk_automat`
  - gemeinsame Begriffsadressen: form

## Verbundlauf

### 1. Unterscheiden: dramaturgische Verdichtung / Einleitung
- Markierte Begriffsadressen: form
- Unmarkierte Begriffsadressen: form

### 2. Propositional ordnen

- 1 Leitsatz: dramaturgische Verdichtung / Einleitung: von der ersten Unterscheidung bis zur Auffuehrung ist als Ordnung möglicher Anschlüsse zu prüfen, nicht als isolierte Behauptung.
- 1.1 Bestimmung: Was gesetzt wird, markiert eine Seite; was nicht gesetzt wird, bleibt als Bedingung der Setzung mitzuführen.
- 1.11 Grenze: Der Automat formuliert prüfbare Sätze, aber keine bestätigte Theorieentscheidung.
- 2 Begriffsadresse: Die erste erkannte Begriffsadresse ist Form: Eine relationale Bestimmung, durch die Unterschiede für weitere Anschlüsse wirksam werden..
- 3 Operation: Eine propositionale Ordnung macht sichtbar, welche Sätze voneinander abhängen und welche Anschlüsse sie eröffnen.
- 3.1 Prüfung: Jeder Unterpunkt muss als Definition, Anwendung, Einwand, Beispiel oder TODO klassifizierbar bleiben.

### 3. Auffuehren / Score erzeugen

```text
01: markiere Anschließen; fuehre Einleitung als unmarkierte Seite mit.
02: markiere Algorithmus; fuehre das durch Anschließen noch nicht Organisierte als unmarkierte Seite mit ueber required_for.
03: markiere Revidieren; fuehre das durch Algorithmus noch nicht Organisierte als unmarkierte Seite mit ueber required_for.
04: markiere Aktualisieren; fuehre die Voraussetzung von Revidieren als unmarkierte Seite mit ueber depends_on.
05: markiere Improvisieren; fuehre die Rueckwirkung auf Aktualisieren als unmarkierte Seite mit ueber inverse_depends_on.
06: markiere Montage; fuehre die Nachbarschaft von Improvisieren als unmarkierte Seite mit ueber related.
07: markiere Form; fuehre die Rueckwirkung auf Montage als unmarkierte Seite mit ueber inverse_related.
08: markiere Problematisieren; fuehre die Voraussetzung von Form als unmarkierte Seite mit ueber depends_on.
09: markiere Unterbrechen; fuehre die Voraussetzung von Problematisieren als unmarkierte Seite mit ueber depends_on.
10: markiere Fortsetzen; fuehre die Rueckwirkung auf Unterbrechen als unmarkierte Seite mit ueber inverse_related.
```

Abbruch: gesetzte Schrittgrenze

## Grenzen

- Der Verbund kombiniert Automaten nur ueber ausgewiesene Anschlussbruecken.
- Eine blockierte Verbindung ist ein Pruefbefund, kein Fehler.
- Die Ausgabe bleibt Vorschlag, Pruefstruktur oder Auffuehrungsspur.
- Manuskriptintegration verlangt einen gesonderten Auftrag, Quellenpruefung und Autorentscheidung.
