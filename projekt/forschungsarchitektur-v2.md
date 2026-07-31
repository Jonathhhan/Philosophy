# Forschungsarchitektur v2

## Zweck

Das Repository ist die Werkstatt einer rekursiven Theorieentwicklung. Manuskript, Glossar und Wissensmodell bleiben Darstellungen eines jeweils vorläufig bestätigten Theoriestands; sie sind nicht mit der Theorie selbst identisch.

Die Forschungsarchitektur trennt sechs Operationen:

1. Generierung: aus einem Anfang neue Texte, Begriffe und Relationen hervorbringen.
2. Rekonstruktion: vorhandene Aussagen und Relationen explizieren.
3. Exploration: fehlende Relationen und nicht ausgeschöpfte Konsequenzen suchen.
4. Kritik: Gegenbeispiele, Gegenmodelle und verdeckte Voraussetzungen erzeugen.
5. Integration: tragfähige Vorschläge in den Theoriegraphen überführen.
6. Darstellung: bestätigte Ergebnisse in Manuskript und Glossar ausarbeiten.

Generierung darf der Rekonstruktion vorausgehen. Nicht jeder neue Text muss aus bereits bestätigter Theorie abgeleitet werden. Er muss aber als generiert gekennzeichnet bleiben, bis er in einen Prüf- und Integrationszyklus eintritt.

## Status einer Theorieaussage oder eines Textes

- `generated`: autonom hervorgebrachter Text oder Gedanke ohne vorausgesetzte Bestätigung.
- `hypothesis`: noch nicht systematisch geprüfte theoretische Behauptung.
- `proposal`: begründeter, aber nicht integrierter Vorschlag.
- `reconstructed`: aus bestehenden Textstellen oder einer expliziten Anschlusskette nachvollziehbar rekonstruiert.
- `internally_consistent`: innerhalb der unmittelbaren Begriffskette widerspruchsfrei.
- `project_consistent`: gegen Manuskript, Glossar und Wissensmodell geprüft.
- `critically_tested`: durch Gegenbeispiel-, Gegenmodell- und Spannungsprüfung gelaufen.
- `confirmed`: vorläufig in den bestätigten Bestand aufgenommen.
- `rejected`: begründet verworfen; die Begründung bleibt dokumentiert.

Für Forschungsbehauptungen gilt grundsätzlich:

```text
hypothesis -> proposal -> reconstructed -> internally_consistent -> project_consistent -> critically_tested -> confirmed
```

Generiertes Material kann davor beginnen:

```text
generated -> proposal -> reconstructed -> internally_consistent -> project_consistent -> critically_tested -> confirmed
```

Kein Automat darf einen Status ohne dokumentierte Prüfung überspringen. `confirmed` bedeutet nicht endgültig wahr, sondern vorläufig belastbar und weiterhin revidierbar.

Ein erzeugender Automat darf einen eigenen Vorschlag selbst bestätigen, wenn der Anschluss plausibel ist. Plausibilität liegt nur vor, wenn:

1. die Anschlusskette explizit rekonstruiert ist,
2. die verwendeten Begriffe ihre bisherige Funktion behalten oder eine Verschiebung ausdrücklich begründet wird,
3. der Vorschlag gegen Manuskript, Glossar und Wissensmodell geprüft wurde,
4. mindestens ein ernsthaftes Gegenmodell oder Gegenbeispiel geprüft wurde,
5. kein ungelöster starker Einwand verbleibt,
6. und die Bestätigung samt Begründung, Grenzen und Revisionsbedingungen protokolliert wird.

Selbstbestätigung ist damit keine Abkürzung der Prüfung, sondern eine mögliche Zusammenführung von Erzeugung, Prüfung und Integration in einem hinreichend transparenten Lauf.

## Rein generativer autonomer Modus

Der Modus `autonomous_generative` darf aus einem Anfang einen neuen Text entwickeln, ohne zunächst eine vollständige Quellen-, Konsistenz- oder Gegenmodellprüfung durchzuführen.

Als Anfang gelten insbesondere:

- ein Satz,
- ein Begriff,
- eine Frage,
- eine Beobachtung,
- eine Spannung,
- eine vorhandene Passage,
- eine Relation,
- oder eine leere Fortsetzungsstelle.

Nach dem Start darf der Automat autonom:

1. den Anfang fortsetzen,
2. neue Begriffe und Relationen erproben,
3. alternative Linien erzeugen,
4. eine Linie auswählen und länger entfalten,
5. eigene Zwischenergebnisse revidieren,
6. Übergänge, Beispiele und Gegenbewegungen schreiben,
7. mehrere rekursive Schreibdurchgänge ausführen,
8. und eine vorläufig geschlossene Textgestalt herstellen.

Der generative Modus dient nicht nur der Produktion einzelner Sätze. Er soll längere argumentative, essayistische oder experimentelle Bewegungen entwickeln.

Sein Grundzyklus lautet:

```text
Anfang
  -> Fortsetzung
  -> neue Differenz
  -> Entfaltung
  -> Rückwirkung auf den Anfang
  -> Revision
  -> weitere Fortsetzung
  -> vorläufige Textgestalt
```

Generierter Text wird zunächst unter `generated/` gespeichert und erhält den Status `generated`. Er darf neue Begriffe enthalten, von bestehenden Begriffsfunktionen abweichen und ungelöste Spannungen offenlassen, sofern Herkunft und Abweichungen gekennzeichnet werden.

Der Automat darf anschließend selbst vom generativen in den prüfenden Modus wechseln. Dieser Moduswechsel muss ausdrücklich protokolliert sein. Erst dann darf er den Text rekonstruieren, projektweit prüfen, kritisieren und bei plausiblem Anschluss selbst bestätigen.

Die vollständige Spezifikation steht in `agents/generativer-autonomer-modus.md`.

## Produktiver Forschungszyklus

```text
Theoriegraph oder generierter Text
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
- eine eigenständige neue Textbewegung,
- oder eine präzisere Darstellung eines bestätigten Satzes.

Bloße Umformulierungen ohne begrifflichen, argumentativen oder formalen Gewinn beenden keinen Zyklus, zählen aber auch nicht als Erkenntnisfortschritt.

Im autonomen Runner wird diese Produktivität nicht aus der Selbstauskunft des erzeugenden Modells abgeleitet. Ein separater deterministischer Prüfschritt verlangt strukturierte Neuheit und protokolliert Modellbehauptung und Verifikation getrennt.

## Agentenordnung

### Generativer autonomer Modus

Entwickelt aus einem Anfang eigenständige neue Texte und Möglichkeiten. Seine Ergebnisse sind zunächst generiertes Material, nicht bestätigte Theorie.

### Invarianten-Agent

Sucht Strukturen, die über mehrere Operationen und Kapitel hinweg erhalten bleiben.

### Spannungs-Agent

Identifiziert Differenzen, die nicht vorschnell aufgelöst werden dürfen, weil sie eine produktive Funktion besitzen.

### Gegenmodell-Agent

Konstruiert alternative Modelle mit weniger oder anderen Grundbegriffen, um die Notwendigkeit der bestehenden Architektur zu prüfen.

### Axiomatisierungs-Agent

Verdichtet mehrfach gestützte Aussagen zu revidierbaren rekonstruktiven Grundsätzen.

### Erkenntnis-Agent

Bewertet, ob ein Durchlauf tatsächlich neues Wissen oder eine eigenständige neue Textbewegung erzeugt hat.

### Integrations-Agent

Entscheidet anhand der protokollierten Resultate, ob eine Aussage oder ein generierter Text verworfen, weiter geprüft oder integriert wird. Diese Funktion kann von einem anderen Automaten oder vom erzeugenden Automaten selbst übernommen werden, sofern die Bedingungen plausibler Selbstbestätigung erfüllt sind.

## Sicherheitsregeln

1. Bestätigte Manuskriptdateien werden nur nach projektweiter Prüfung geändert.
2. Rein generative Texte werden zuerst unter `generated/` abgelegt.
3. Neue Theorie wird zunächst unter `knowledge/hypotheses/`, `knowledge/invariants/` oder `knowledge/tensions/` dokumentiert.
4. Jede prüfende Änderung nennt Quellen, Gegenargumente und Status.
5. Bestehende Dateien werden nur vollständig gelesen und vollständig ersetzt.
6. Ein Automat darf eigene Vorschläge bestätigen, wenn er die Plausibilität des Anschlusses, die Gegenprüfung und die verbleibenden Grenzen vollständig dokumentiert.
7. Im generativen Modus sind Quellen und Gegenargumente noch nicht verpflichtend; der Modus und der Anfang müssen jedoch eindeutig protokolliert sein.
8. Generierter Text darf nicht ungekennzeichnet als bestätigter Manuskripttext erscheinen.
9. Ein fehlender Befund wird als `no_productive_difference` dokumentiert und nicht künstlich erzeugt.

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

Im rein generativen Modus dürfen neue Ketten zunächst auch ohne vollständige Prüfung entstehen. Ihre Kanten werden erst beim Übergang in den Forschungszyklus rekonstruiert und bewertet.

Damit wird Rekursivität nicht nur Gegenstand der Theorie, sondern Arbeitsweise ihrer Entwicklung und ihres Schreibens.