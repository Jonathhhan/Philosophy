# Codex-Zettelregister

Status: operative Arbeitskarte; kein Manuskriptbestandteil.

Dieses Register sammelt keine Theoriebausteine des Buches. Es hält fest, welche Projektstellen Codex bei größeren Arbeiten als adressierbare Zettel und als Plateaus behandeln kann. Eine Adresse bedeutet: Hier gibt es eine Stelle, an die angeschlossen, von der aus weitergearbeitet oder zu der zurückgekehrt werden kann.

## Luhmann-nahe Registerregeln

Das Register bleibt eine Eingangshilfe, nicht die eigentliche Ordnung. Für neue
Codex-Zettel gelten deshalb folgende Regeln:

- Eine einmal vergebene Adresse bleibt stabil; spätere Verschiebungen werden als
  neue Relationen oder Folgezettel dokumentiert.
- Neue Zettel dürfen als Einschub, Seitenzweig oder Korrekturzettel an ältere
  Zettel anschließen.
- Thematische Nähe wird nicht durch Umnummerieren hergestellt, sondern durch
  Verweise.
- Ein Zettel soll möglichst eine bestimmte Arbeitsfunktion haben: Quelle,
  Entscheidung, Vorschlag, Prüfung, Korrektur, Anschlussfrage oder technische
  Ausgabe.
- Entfernte Anschlüsse sind ausdrücklich erwünscht, wenn ihre Relation benannt
  wird. Bloße Assoziationen bleiben TODO.

### Adressmuster

```text
Z-0003      bestehende Adresse
Z-0003a     Einschub oder Fortsetzung zu Z-0003
Z-0003a1    Präzisierung zu Z-0003a
Z-0003k     späterer Seitenzweig, ohne Z-0003 umzunummerieren
Z-0003R     Rückverweis, Korrektur oder Relationszettel
```
## Z-0001 · Projektverfassung

**Adresse:** `CONSTITUTION.md`

**Status:** bestätigt

**Funktion:** Bestimmt die oberste interne Autorität des Projekts, die Grenzen der Theorie und den Vorrang der Autorenentscheidung.

**Relationen:**

- stützt: `WORKFLOW.md`
- begrenzt: neue Grundbegriffe, Grundthesen und Theorieachsen
- benötigt Prüfung: bei jeder größeren Reorganisation

**Öffnet:** sichere Prüfung, ob ein Vorschlag als Manuskriptthese, Arbeitsregel oder TODO zu behandeln ist.

## Z-0002 · Rekursive Arbeitsbewegung

**Adresse:** `WORKFLOW.md`

**Status:** bestätigt

**Funktion:** Organisiert Codex-Arbeit als Anschließen, Organisieren, Aktualisieren, Reorganisieren und Kritisieren.

**Relationen:**

- stützt: `.agents/skills/recursive-codex/SKILL.md`
- verweist auf: `projekt/codex-auftragsvorlage.md`
- wird präzisiert durch: `projekt/codex-prinzip-zettelkasten-plateaus.md`

**Öffnet:** skalierbare Bearbeitung von lokalen, kompositorischen und strukturellen Aufgaben.

## Z-0003 · Zettelkasten und Plateaus als Codex-Prinzip

**Adresse:** `projekt/codex-prinzip-zettelkasten-plateaus.md`

**Status:** bestätigt als Codex-Arbeitsprinzip; nicht bestätigt als Manuskriptthese

**Funktion:** Macht Codex-Arbeit adressierbar, relational, statusbewusst und nicht-linear anschlussfähig.

**Relationen:**

- stützt: `projekt/codex-auftragsvorlage.md`
- begrenzt: unmarkierte Übernahme von Luhmann oder Deleuze/Guattari als Buchautoritäten
- verweist auf: `knowledge/decisions/0022-codex-zettelkasten-plateaus.yaml`
- dokumentiert durch: `knowledge/change-events/0007-codex-zettelkasten-plateaus.yaml`

**Öffnet:** künftige Codex-Aufträge können als Zettel-/Plateau-Konstellation beschrieben werden.

**Begrenzt:** Nicht-lineare Verknüpfungen werden nicht als Argumente behandelt, solange sie nicht im Manuskript ausgearbeitet sind.

## Z-0004 · Anschlusslabor

**Adresse:** `interaktiv/`

**Status:** technische Ausgabe; kein Ersatz für Manuskripttext

**Funktion:** Erprobt Anschlussoperationen operativ und macht Vorgänge sichtbar.

**Relationen:**

- verweist auf: Manuskriptbegriffe und Kapitelbezüge
- wird begrenzt durch: `WORKFLOW.md`, Abschnitt technische Ausgabe
- kann erweitert werden durch: KI-gestützte Vorschläge, sofern Datenschutz und Statusgrenzen dokumentiert sind

**Öffnet:** eine spätere Verbindung von Leserinteraktion, Codex-Zettelprinzip und Manuskriptbezug.


## Z-0005 � Genetisches Register

**Adresse:** `projekt/genetisches-register.md`

**Status:** delegierte Codex-Entscheidung als Codex-Arbeitsprinzip; kein Manuskriptbestandteil

**Funktion:** Dokumentiert Gedanken als Abstammungslinien aus Herkunft, Unterscheidung, Mutation, Pruefung, Entscheidung und Nachkommen.

**Relationen:**

- praezisiert: `projekt/codex-prinzip-zettelkasten-plateaus.md`
- stuetzt: `projekt/codex-methode-verfeinerung.md`
- verweist auf: `knowledge/change-events/0032-genetisches-register-codex.yaml`
- begrenzt: unmarkierte Verwandlung von Codex-Arbeitsmethode in Manuskriptthese

**Oeffnet:** Codex kann Gedankenentwicklungen als Linien verfolgen, Varianten vergleichen und spaetere Anschlussfolgen besser pruefen.

**Begrenzt:** Genetische Metaphorik darf nicht als Quellenbehauptung oder biologische Theorie ausgegeben werden.

## Z-0006 � Codex-Nutzungsanleitung

**Adresse:** `projekt/codex-nutzungsanleitung.md`

**Status:** operative Gebrauchsanweisung; kein Manuskriptbestandteil

**Funktion:** Buendelt, wie Codex in diesem Projekt genutzt werden soll: rekursiv, zettelkastenfoermig, plateauartig, genetisch, tractatusfoermig, quellenbewusst und mit optional delegierter Entscheidung.

**Relationen:**

- stuetzt: `WORKFLOW.md`
- verweist auf: `projekt/automaten.md`
- verweist auf: `projekt/genetisches-register.md`
- verweist auf: `knowledge/change-events/0033-codex-nutzungsanleitung.yaml`

**Oeffnet:** Neue Codex-Auftraege koennen kuerzer formuliert werden, weil die Anleitung die methodischen Standards gesammelt bereitstellt.

**Begrenzt:** Die Anleitung ersetzt keine projektverbindlichen Dateien und darf nicht als Manuskriptthese gelesen werden.
## Offene Plateaus

- TODO: Technisches Zettel-/Graphformat nur einführen, wenn es mehr leistet als dieses Register.
- TODO: Luhmann und Deleuze/Guattari nur mit Primärquellen und Seitenangaben ins Manuskript integrieren.
- TODO: Prüfen, ob das Anschlusslabor künftig ausgewählte Codex-Zettel sichtbar machen soll.