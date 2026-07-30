# Automatenverbund der Anschlussfaehigkeit

Status: kombinierte Pruef- und Auffuehrungsspur; keine Manuskriptintegration und keine Theorieentscheidung

## Eingabe

- markiert: Anschliessen
- unmarkiert: Nicht-Anschluss
- Kontext: von der ersten Unterscheidung bis zur Auffuehrung

## Ermoeglichte Anschluesse

- `unterscheidungsautomat` -> `tractatus_automat`
  - gemeinsame Begriffsadressen: aktualisieren, anschliessen, asymmetrie, form, kommunikation, organisieren, reorganisieren, revidieren
  - gemeinsame Manuskriptanker: manuskript\04-form.md:77, manuskript\05-aktualisieren.md:11, manuskript\05-aktualisieren.md:47, manuskript\07-programm.md:59, manuskript\11-organisieren.md:77
- `tractatus_automat` -> `kunstwerk_automat`
  - gemeinsame Begriffsadressen: aktualisieren, anschliessen, form, revidieren

## Verbundlauf

### 1. Unterscheiden: Anschliessen / Nicht-Anschluss
- Markierte Begriffsadressen: anschliessen, form, kommunikation
- Unmarkierte Begriffsadressen: anschliessen, form, aktualisieren, asymmetrie, kommunikation, organisieren

### 2. Propositional ordnen

- 1 Leitsatz: Anschliessen / Nicht-Anschluss: von der ersten Unterscheidung bis zur Auffuehrung ist als Ordnung möglicher Anschlüsse zu prüfen, nicht als isolierte Behauptung.
- 1.1 Bestimmung: Was gesetzt wird, markiert eine Seite; was nicht gesetzt wird, bleibt als Bedingung der Setzung mitzuführen.
- 1.11 Grenze: Der Automat formuliert prüfbare Sätze, aber keine bestätigte Theorieentscheidung.
- 2 Begriffsadresse: Die erste erkannte Begriffsadresse ist Anschließen: Anschließen bezeichnet den Eintritt in einen bereits begonnenen Zusammenhang, durch den eine Möglichkeit aktualisiert und der Raum weiterer Anschlüsse verändert wird..
- 2.1 Nachbarbegriff: Form bildet eine mögliche Anschlussadresse für die weitere Prüfung.
- 2.2 Nachbarbegriff: Kommunikation bildet eine mögliche Anschlussadresse für die weitere Prüfung.

### 3. Auffuehren / Score erzeugen

```text
01: markiere Anschließen; fuehre Nicht-Anschluss als unmarkierte Seite mit.
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
