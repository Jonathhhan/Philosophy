# Selbstprogrammierendes Kunstwerk der Anschlussunterscheidungen

Status: Auffuehrungsspur; keine Manuskriptintegration und keine Theorieentscheidung

## Erste Unterscheidung

- markiert: Anschliessen
- unmarkiert: Nicht-Anschluss

## Lauf

### 1. Anschließen

- Unmarkierte Seite: Nicht-Anschluss
- Concept-Datei: `knowledge\concepts\anschliessen.yaml`
- Arbeitsdefinition: Anschließen bezeichnet den Eintritt in einen bereits begonnenen Zusammenhang, durch den eine Möglichkeit aktualisiert und der Raum weiterer Anschlüsse verändert wird.
- Grenzen:
  - Kein Anfang beginnt bei null.
  - Auch der Bruch schließt an dasjenige an, von dem er sich absetzt.
  - Anschluss darf nicht auf sprachliche Kommunikation reduziert werden.
- Programmiert naechste Auffuehrung: `01: markiere Anschließen; fuehre Nicht-Anschluss als unmarkierte Seite mit.`

### 2. Algorithmus

- Unmarkierte Seite: das durch Anschließen noch nicht Organisierte
- Anschlussrelation: required_for
- Concept-Datei: `knowledge\concepts\algorithmus.yaml`
- Arbeitsdefinition: wiederholbare Ordnung bedingter Übergänge
- Grenzen:
  - Algorithmus ist keine bloße Metapher.
  - Algorithmus und Programm dürfen nicht gleichgesetzt werden.
  - Der Begriff bleibt auf nichtdigitale Ordnungen bedingter Übergänge anwendbar.
- Programmiert naechste Auffuehrung: `02: markiere Algorithmus; fuehre das durch Anschließen noch nicht Organisierte als unmarkierte Seite mit ueber required_for.`

### 3. Revidieren

- Unmarkierte Seite: das durch Algorithmus noch nicht Organisierte
- Anschlussrelation: required_for
- Concept-Datei: `knowledge\concepts\revidieren.yaml`
- Arbeitsdefinition: Begründetes Zurückkommen auf stabilisierte Anschlussbedingungen, um sie im Licht ihrer Wirkungen, veränderter Umstände oder neu erschlossener Möglichkeiten erneut zu bestimmen.
- Grenzen:
  - Revidieren ist nicht bloße Veränderung, Korrektur, Reparatur oder Anpassung.
  - Revidierbarkeit ist nicht mit Reversibilität identisch.
- Programmiert naechste Auffuehrung: `03: markiere Revidieren; fuehre das durch Algorithmus noch nicht Organisierte als unmarkierte Seite mit ueber required_for.`

### 4. Aktualisieren

- Unmarkierte Seite: die Voraussetzung von Revidieren
- Anschlussrelation: depends_on
- Concept-Datei: `knowledge\concepts\aktualisieren.yaml`
- Arbeitsdefinition: Eine Anschlussmöglichkeit in einen bestimmten Vollzug überführen.
- Grenzen:
  - Aktualisieren ist nicht bloßes Realisieren eines schon fertig vorhandenen Zustands.
  - Eine Aktualisierung verändert nicht notwendig alle, aber stets Bedingungen weiterer Anschlüsse.
- Programmiert naechste Auffuehrung: `04: markiere Aktualisieren; fuehre die Voraussetzung von Revidieren als unmarkierte Seite mit ueber depends_on.`

### 5. Improvisieren

- Unmarkierte Seite: die Rueckwirkung auf Aktualisieren
- Anschlussrelation: inverse_depends_on
- Concept-Datei: `knowledge\concepts\improvisieren.yaml`
- Arbeitsdefinition: Formgebundene und formbildende Tätigkeit unter Bedingungen partieller Unbestimmtheit.
- Grenzen:
  - Improvisation ist weder Regellosigkeit noch reine Spontaneität.
  - Improvisieren bleibt an Material, Situation, Haltung und Formbildung gebunden.
- Programmiert naechste Auffuehrung: `05: markiere Improvisieren; fuehre die Rueckwirkung auf Aktualisieren als unmarkierte Seite mit ueber inverse_depends_on.`

### 6. Montage

- Unmarkierte Seite: die Nachbarschaft von Improvisieren
- Anschlussrelation: related
- Concept-Datei: `knowledge\concepts\montage.yaml`
- Arbeitsdefinition: Epistemisches Modell relationaler Formbildung, in dem Auswahl, Unterbrechung, Übergang, Variation, Komposition, Stabilisierung und Revision praktisch sichtbar werden.
- Grenzen:
  - Montage ist epistemischer Ausgangspunkt und Modell rekursiver Formbildung, nicht bloß ein Beispiel.
  - Exakte historische oder quellenbezogene Behauptungen benötigen Seitenangaben aus den Primärquellen.
- Programmiert naechste Auffuehrung: `06: markiere Montage; fuehre die Nachbarschaft von Improvisieren als unmarkierte Seite mit ueber related.`

### 7. Form

- Unmarkierte Seite: die Rueckwirkung auf Montage
- Anschlussrelation: inverse_related
- Concept-Datei: `knowledge\concepts\form.yaml`
- Arbeitsdefinition: Eine relationale Bestimmung, durch die Unterschiede für weitere Anschlüsse wirksam werden.
- Grenzen:
  - Form ist nicht mit äußerer Gestalt gleichzusetzen.
  - Form bezeichnet das Wirksamwerden relevanter Unterschiede für weitere Anschlüsse.
- Programmiert naechste Auffuehrung: `07: markiere Form; fuehre die Rueckwirkung auf Montage als unmarkierte Seite mit ueber inverse_related.`

### 8. Problematisieren

- Unmarkierte Seite: die Voraussetzung von Form
- Anschlussrelation: depends_on
- Concept-Datei: `knowledge\concepts\problematisieren.yaml`
- Arbeitsdefinition: Eine zunächst unbestimmte Fraglichkeit selektiv als bearbeitbare Frage fassen, ohne damit bereits ihre Lösung, Form oder Beurteilung festzulegen.
- Grenzen:
  - Problematisieren legt noch keine Lösung, Form oder normative Beurteilung fest.
- Programmiert naechste Auffuehrung: `08: markiere Problematisieren; fuehre die Voraussetzung von Form als unmarkierte Seite mit ueber depends_on.`

### 9. Unterbrechen

- Unmarkierte Seite: die Voraussetzung von Problematisieren
- Anschlussrelation: depends_on
- Concept-Datei: `knowledge\concepts\unterbrechen.yaml`
- Arbeitsdefinition: Einen laufenden oder erwarteten Anschluss so aussetzen, stören oder abbrechen, dass seine Bedingungen sichtbar oder fraglich werden.
- Grenzen:
  - Unterbrechen ist nicht bloß Pause oder endgültiger Abbruch.
  - Auch der Bruch schließt an dasjenige an, von dem er sich absetzt.
- Programmiert naechste Auffuehrung: `09: markiere Unterbrechen; fuehre die Voraussetzung von Problematisieren als unmarkierte Seite mit ueber depends_on.`

### 10. Fortsetzen

- Unmarkierte Seite: die Rueckwirkung auf Unterbrechen
- Anschlussrelation: inverse_related
- Concept-Datei: `knowledge\concepts\fortsetzen.yaml`
- Arbeitsdefinition: Einen Zusammenhang so weiterführen, dass an bereits wirksame Bedingungen angeschlossen wird.
- Grenzen:
  - Fortsetzen ist kein bloßer zeitlicher Nachfolger, sondern bleibt an Anschlussbedingungen gebunden.
- Programmiert naechste Auffuehrung: `10: markiere Fortsetzen; fuehre die Rueckwirkung auf Unterbrechen als unmarkierte Seite mit ueber inverse_related.`

## Generierter Score

```text
01: markiere Anschließen; fuehre Nicht-Anschluss als unmarkierte Seite mit.
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

## Abbruch

Der Lauf endet durch: gesetzte Schrittgrenze.

## Grenzen

- Der Automat veraendert nicht seinen Quellcode, sondern erzeugt einen auffuehrbaren Score.
- Die Folge nutzt deklarierte Concept-Relationen und bleibt dadurch projektgebunden.
- Die letzte Station ist eine Abbruchbedingung, keine philosophische Letztbegruendung.
- Manuskriptintegration braucht einen gesonderten Auftrag, Quellenpruefung und Autorentscheidung.
