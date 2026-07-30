# Forschungsarchitektur v2

## Zweck

Das Repository ist die Werkstatt einer rekursiven Theorieentwicklung. Manuskript, Glossar und Wissensmodell bleiben Darstellungen eines jeweils vorläufig bestätigten Theoriestands; sie sind nicht mit der Theorie selbst identisch.

Die Forschungsarchitektur trennt fünf Operationen:

1. Rekonstruktion: vorhandene Aussagen und Relationen explizieren.
2. Exploration: fehlende Relationen und nicht ausgeschöpfte Konsequenzen suchen.
3. Kritik: Gegenbeispiele, Gegenmodelle und verdeckte Voraussetzungen erzeugen.
4. Integration: tragfähige Vorschläge in den Theoriegraphen überführen.
5. Darstellung: bestätigte Ergebnisse in Manuskript und Glossar ausarbeiten.

## Status einer Theorieaussage

- `hypothesis`: noch nicht systematisch geprüft.
- `proposal`: begründeter, aber nicht integrierter Vorschlag.
- `reconstructed`: aus bestehenden Textstellen nachvollziehbar rekonstruiert.
- `internally_consistent`: innerhalb der unmittelbaren Begriffskette widerspruchsfrei.
- `project_consistent`: gegen Manuskript, Glossar und Wissensmodell geprüft.
- `critically_tested`: durch Gegenbeispiel-, Gegenmodell- und Spannungsprüfung gelaufen.
- `confirmed`: vorläufig in den bestätigten Bestand aufgenommen.
- `rejected`: begründet verworfen; die Begründung bleibt dokumentiert.

Kein Automat darf einen Status ohne dokumentierte Prüfung überspringen. `confirmed` bedeutet nicht endgültig wahr, sondern vorläufig belastbar und weiterhin revidierbar.

Ein erzeugender Automat darf einen eigenen Vorschlag selbst bestätigen, wenn der Anschluss plausibel ist. Plausibilität liegt nur vor, wenn:

1. die Anschlusskette explizit rekonstruiert ist,
2. die verwendeten Begriffe ihre bisherige Funktion behalten oder eine Verschiebung ausdrücklich begründet wird,
3. der Vorschlag gegen Manuskript, Glossar und Wissensmodell geprüft wurde,
4. mindestens ein ernsthaftes Gegenmodell oder Gegenbeispiel geprüft wurde,
5. kein ungelöster starker Einwand verbleibt,
6. und die Bestätigung samt Begründung, Grenzen und Revisionsbedingungen protokolliert wird.

Selbstbestätigung ist damit keine Abkürzung der Prüfung, sondern eine mögliche Zusammenführung von Erzeugung, Prüfung und Integration in einem hinreichend transparenten Lauf.

## Produktiver Forschungszyklus

```text
Theoriegraph
  -> Rekonstruktion
  -> Invariantenbildung
  -> Spannungsanalyse
  -> Konsequenzbildung
  -> Gegenmodell
  -> kritische Prüfung
  -> Integration oder Verwerfung
  -> projektweite Synchronisation
  -> erneuter Durchlauf
```

Ein Zyklus gilt nur dann als produktiv, wenn mindestens eine produktive Differenz entsteht:

- eine neue begründete Relation,
- eine explizierte Voraussetzung,
- eine widerlegte Hypothese,
- eine tragfähige Invariante,
- eine produktive Spannung,
- eine Vereinfachung bei gleichem Erklärungsgehalt,
- eine Korrektur des Theoriegraphen,
- oder eine präzisere Darstellung eines bestätigten Satzes.

Bloße Umformulierungen ohne begrifflichen oder argumentativen Gewinn beenden keinen Zyklus, zählen aber auch nicht als Erkenntnisfortschritt.

## Agentenordnung

### Invarianten-Agent

Sucht Strukturen, die über mehrere Operationen und Kapitel hinweg erhalten bleiben.

### Spannungs-Agent

Identifiziert Differenzen, die nicht vorschnell aufgelöst werden dürfen, weil sie eine produktive Funktion besitzen.

### Gegenmodell-Agent

Konstruiert alternative Modelle mit weniger oder anderen Grundbegriffen, um die Notwendigkeit der bestehenden Architektur zu prüfen.

### Axiomatisierungs-Agent

Verdichtet mehrfach gestützte Aussagen zu revidierbaren rekonstruktiven Grundsätzen.

### Erkenntnis-Agent

Bewertet, ob ein Durchlauf tatsächlich neues Wissen erzeugt hat.

### Integrations-Agent

Entscheidet anhand der protokollierten Resultate, ob eine Aussage verworfen, weiter geprüft oder integriert wird. Diese Funktion kann von einem anderen Automaten oder vom erzeugenden Automaten selbst übernommen werden, sofern die Bedingungen plausibler Selbstbestätigung erfüllt sind.

## Sicherheitsregeln

1. Manuskriptdateien werden nur nach projektweiter Prüfung geändert.
2. Neue Theorie wird zuerst unter `knowledge/hypotheses/`, `knowledge/invariants/` oder `knowledge/tensions/` dokumentiert.
3. Jede Änderung nennt Quellen, Gegenargumente und Status.
4. Bestehende Dateien werden nur vollständig gelesen und vollständig ersetzt.
5. Ein Automat darf eigene Vorschläge bestätigen, wenn er die Plausibilität des Anschlusses, die Gegenprüfung und die verbleibenden Grenzen vollständig dokumentiert.
6. Ein fehlender Befund wird als `no_productive_difference` dokumentiert und nicht künstlich erzeugt.

## Lange Ketten

Die Automaten bearbeiten nicht nur einzelne Kapitel, sondern vollständige Transformationsketten, zum Beispiel:

```text
Anschluss
  -> Aktualisierung
  -> Organisation
  -> Verteilung
  -> Asymmetrie
  -> Kritik
  -> Urteil
  -> Revision
  -> Reorganisation
  -> veränderte Anschlussbedingungen
```

An jeder Kante wird geprüft:

- Welche Voraussetzung wird übersetzt?
- Was bleibt invariant?
- Was verändert sich?
- Welche Alternative wäre möglich?
- Welche Anschlüsse werden eröffnet oder ausgeschlossen?

Damit wird Rekursivität nicht nur Gegenstand der Theorie, sondern Arbeitsweise ihrer Entwicklung.