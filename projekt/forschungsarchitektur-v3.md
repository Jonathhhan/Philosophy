# Forschungsarchitektur v3: Forschungsprogramme und Experimente

## Zweck und Status

Version 3 ergänzt die Forschungsarchitektur v2 um eine Ebene, auf der nicht nur
einzelne Theorien, sondern Forschungsprogramme geordnet und verglichen werden.
Sie ersetzt weder die Verfassung noch die Statusfolge der Version 2. Ein
Forschungsprogramm ist hier eine operative Werkstattordnung aus Fragen,
Methoden, Grenzen, offenen Problemen und Kriterien. Es ist keine neue
Grundthese des Manuskripts.

## Forschungsprogramm

Ein Forschungsprogramm bestimmt, welche Fragen verfolgt werden, welche Methoden
dafür zulässig sind und welche offenen Probleme miteinander konkurrieren. Seine
maschinenlesbare Form folgt
`automation/schemas/research-program.schema.json`. Die Autoritätssektion muss
alle autonomen Änderungen an Verfassung, geschützten Grundbegriffen und
Autoritätsregeln ausschließen. Eine technische Validierung bestätigt nur die
Form dieses Programms.

## Experiment

Ein Experiment führt mindestens zwei Varianten desselben Seeds aus. Varianten
können unterschiedliche Methoden, Agentenrollen oder epistemische Stile
verwenden. Der Vergleich richtet sich nicht nur auf Texte, sondern auf neue
Relationen, Invarianten, Gegenmodelle, offene Spannungen, Vereinfachungen und
ausgewiesene Erklärungskraft. Das Schema steht unter
`automation/schemas/experiment.schema.json`.

Der lokale `ExperimentManager` nimmt die Ausführung als injizierte Funktion
entgegen. Damit bleibt er von einem bestimmten Modell oder Endpoint unabhängig.
Er schreibt ausschließlich nach `generated/experiments/`. Ergebnisse erhalten
Werkstattstatus; der Vergleich wählt keine philosophisch überlegene Variante
und setzt weder Theorie noch Manuskript auf `confirmed`.

## Research Director

Der `ResearchDirector` priorisiert offene Probleme anhand vier deklarierter
Werte zwischen 0 und 1:

- Unsicherheit,
- Vernetzungsgrad,
- theoretische Tragweite,
- Experimentierbarkeit.

Standardmäßig werden die vier Kriterien gleich gewichtet. Das Resultat ist eine
reproduzierbare Priorisierung mit Status `proposal`, keine Entscheidung über
theoretische Wahrheit oder Manuskriptintegration.

## Discovery Manager

Der `DiscoveryManager` berechnet für Agenten und Methoden einen erwartbaren
Erkenntnisgewinn aus denselben vier Kriterien und den deklarierten Kosten. Nur
Kandidaten oberhalb einer expliziten Schwelle werden ausgewählt; die übrigen
werden mit ihrer Berechnung zurückgestellt. `fusion` und `split` werden niemals
ausgeführt. Sie erscheinen ausschließlich als Vorschläge, die eine
Autorenentscheidung verlangen.

## Konstitutionelle Grenze

Die V3-Schicht darf autonom:

- Varianten erzeugen und protokollieren,
- offene Probleme priorisieren,
- Methoden für ein Experiment auswählen,
- Ergebnisse vergleichbar darstellen.

Sie darf nicht autonom:

- `CONSTITUTION.md`, `PROJECT.md`, `GLOSSAR.md`,
  `knowledge/project_binding.yaml` oder Dateien unter `manuskript/` schreiben;
- Verfassung, geschützte Grundbegriffe oder Autoritätsregeln ändern;
- Ergebnisse als `confirmed` oder `stabilized` ausgeben;
- Fusion oder Split von Begriffen, Agenten, Methoden oder Forschungsprogrammen
  vollziehen;
- aus Metriken eine philosophische Letztentscheidung ableiten.

Die inhaltliche Autorität bleibt beim Autor. Tests sichern diese Grenze als
technischen Vertrag; sie beweisen keine philosophische Tragfähigkeit.

