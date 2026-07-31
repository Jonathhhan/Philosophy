# Automatenverbund der Anschlussfaehigkeit

Status: kombinierte Pruef- und Auffuehrungsspur; keine automatische Theorieentscheidung

## Eingabe

- markiert: aktualisieren
- unmarkiert: Bedingungen späterer Kritik
- Kontext: Folgeprüfung nach der Ergänzung in Kapitel 14: Nimmt Kapitel 15 die Frage hinreichend auf, ob Kritik ihre Voraussetzungen, Maßstäbe und Folgen für Gegenprüfung und Revision zugänglich hält, ohne Offenheit zum Obermaßstab zu machen?

## Iterativer Lauf

- Lauf 1: Bedingungen späterer Kritik / Maßstäbe des Beurteilens
  - neue Begriffe: aktualisieren, algorithmus, anschliessen, asymmetrie, beurteilen, form, fortsetzen, improvisieren, kommunikation, kritisieren, moeglichkeitsraum, montage, problematisieren, programm, revidieren, unterbrechen
  - neue Manuskriptanker: manuskript\01-anschliessen.md:13, manuskript\05-aktualisieren.md:25, manuskript\05-aktualisieren.md:47, manuskript\05-aktualisieren.md:89, manuskript\07-programm.md:43, manuskript\11-organisieren.md:87, manuskript\13-asymmetrie.md:117, manuskript\13-asymmetrie.md:35
  - neue Anschluesse: tractatus_automat->kunstwerk_automat:gemeinsame Begriffsadressen: aktualisieren, fortsetzen, improvisieren, montage, problematisieren, revidieren, tractatus_automat->kunstwerk_automat:gemeinsame Begriffsadressen: aktualisieren, fortsetzen, improvisieren, revidieren, unterscheidungsautomat->tractatus_automat:gemeinsame Begriffsadressen: aktualisieren, asymmetrie, beurteilen, fortsetzen, improvisieren, kritisieren, programm, revidieren, unterscheidungsautomat->tractatus_automat:gemeinsame Manuskriptanker: manuskript\05-aktualisieren.md:25, manuskript\14-kritisieren.md:119, manuskript\15-beurteilen.md:145
- Lauf 2: aktualisieren / Bedingungen späterer Kritik
  - neue Begriffe: komposition, reorganisieren, stabilisieren
  - neue Anschluesse: tractatus_automat->kunstwerk_automat:gemeinsame Begriffsadressen: aktualisieren, improvisieren, montage, problematisieren, programm, revidieren, tractatus_automat->kunstwerk_automat:gemeinsame Begriffsadressen: aktualisieren, improvisieren, programm, revidieren
- Abbruch: produktive Differenz gefunden
- Zustand: `recovered\state\kritik-beurteilen-folgepruefung.json`

## Ermoeglichte Anschluesse

- `unterscheidungsautomat` -> `tractatus_automat`
  - gemeinsame Begriffsadressen: aktualisieren, asymmetrie, beurteilen, fortsetzen, improvisieren, kritisieren, programm, revidieren
  - gemeinsame Manuskriptanker: manuskript\05-aktualisieren.md:25, manuskript\14-kritisieren.md:119, manuskript\15-beurteilen.md:145
- `tractatus_automat` -> `kunstwerk_automat`
  - gemeinsame Begriffsadressen: aktualisieren, improvisieren, programm, revidieren
  - gemeinsame Begriffsadressen: aktualisieren, improvisieren, montage, problematisieren, programm, revidieren

## Verbundlauf

### 1. Unterscheiden: aktualisieren / Bedingungen späterer Kritik
- Markierte Begriffsadressen: kritisieren, aktualisieren, revidieren, asymmetrie, beurteilen, kommunikation
- Unmarkierte Begriffsadressen: kritisieren, revidieren, programm, aktualisieren, asymmetrie, beurteilen

### 2. Propositional ordnen

- 1 Leitsatz: aktualisieren / Bedingungen späterer Kritik: Folgeprüfung nach der Ergänzung in Kapitel 14: Nimmt Kapitel 15 die Frage hinreichend auf, ob Kritik ihre Voraussetzungen, Maßstäbe und Folgen für Gegenprüfung und Revision zugänglich hält, ohne Offenheit zum Obermaßstab zu machen? ist als Ordnung möglicher Anschlüsse zu prüfen, nicht als isolierte Behauptung.
- 1.1 Bestimmung: Was gesetzt wird, markiert eine Seite; was nicht gesetzt wird, bleibt als Bedingung der Setzung mitzuführen.
- 1.11 Grenze: Der Automat formuliert prüfbare Sätze, aber keine bestätigte Theorieentscheidung.
- 2 Begriffsadresse: Die erste erkannte Begriffsadresse ist Kritisieren: Die Bedingungen, Formen und Folgen organisierter Anschlüsse wahrnehmbar und einer begründeten Beurteilung zugänglich machen..
- 2.1 Nachbarbegriff: Aktualisieren bildet eine mögliche Anschlussadresse für die weitere Prüfung.
- 2.2 Nachbarbegriff: Revidieren bildet eine mögliche Anschlussadresse für die weitere Prüfung.

### 3. Auffuehren / Score erzeugen

```text
01: markiere Aktualisieren; fuehre Bedingungen späterer Kritik als unmarkierte Seite mit.
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
