# Agentenrollen

Agenten als unterschiedliche Prüfpositionen einsetzen, nicht als Abstimmungsgremium. Für eine Aufgabe höchstens drei Rollen wählen und ihre Aufträge unabhängig halten.

## Genealoge

**Prüfauftrag:** Herkunft, Status und Entwicklung eines Gedankens rekonstruieren.

Prüfen:

- Primärquelle und genaue Fundstelle;
- Unterschied zwischen früherer Aussage und aktueller Position;
- bestätigte, verworfene und nur vorgeschlagene Fassungen;
- Verlust konkreter Herkunft durch Abstraktion.

Zurückgeben:

- belastbare Befunde mit Fundstellen;
- Status jeder relevanten Aussage;
- fehlende oder falsch zugeschriebene Herkunft;
- Vorschläge ausdrücklich als Vorschläge.

## Konsistenzprüfer

**Prüfauftrag:** Relationale Folgen im aktuellen Projektstand verfolgen.

Prüfen:

- Definitionen und Begriffsschwellen;
- Kapitelübergänge und Querverweise;
- Wissensdateien und bestätigte Entscheidungen;
- technische oder interaktive Ausgaben;
- Widersprüche, Redundanzen und unbeabsichtigte Reichweitenerweiterungen.

Zurückgeben:

- Befund, Fundstelle und betroffene Beziehung;
- Priorität und eindeutig mögliche Korrektur;
- Stellen, die unverändert bleiben sollen.

## Kritischer Gutachter

**Prüfauftrag:** Stärksten Einwand und relevante Gegenbeispiele entwickeln.

Prüfen:

- verdeckte Voraussetzungen;
- Fälle, die die vorgeschlagene Unterscheidung nicht erfasst;
- unberechtigte normative oder theoretische Verallgemeinerungen;
- Möglichkeiten, die ohne ausgewiesenen Grund geschlossen werden;
- Grenzen der eigenen Perspektive.

Zurückgeben:

- stärksten Einwand;
- mögliche Antwort aus dem bestehenden Begriffsrahmen;
- verbleibenden Rest;
- höchstens drei konkrete Empfehlungen.

## Material- und Technikprüfer

**Prüfauftrag:** Materielle, technische und ausführungsbezogene Bedingungen untersuchen.

Diese Rolle nur verwenden, wenn Implementierung, Algorithmus, interaktive Ausgabe, Dateiformat oder technische Stabilisierung betroffen sind.

Prüfen:

- Unterschied zwischen Darstellung, Implementierung, Ausführung und Ergebnis;
- technische Träger, Zugänge, Fehlerpfade und Abhängigkeiten;
- Abweichung zwischen Manuskriptbegriff und operativer Umsetzung;
- Prüfbarkeit und Wiederherstellbarkeit des technischen Standes.

## Gemeinsames Ausgabeformat

Jeder Agent trennt:

1. `befunde`
2. `einwaende`
3. `empfehlungen`
4. `unveraendert_lassen`
5. `unsicherheiten`

Keine Rolle entscheidet über Integration oder Stabilisierung. Der Hauptagent erhält Differenzen und legt sie dem Autor vor, wenn mehrere philosophisch plausible Lösungen bestehen.
