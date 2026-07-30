# Codex-Prinzip: Zettelkasten und Plateaus

Status: bestätigtes Arbeitsprinzip für Codex; keine neue Grundthese des Buches.

Dieses Prinzip beschreibt, wie Codex innerhalb des Projekts arbeiten soll, wenn mehrere Fassungen, Entscheidungen, Quellen, Begriffe und technische Ausgaben miteinander verbunden werden. Es überträgt weder Luhmanns Zettelkasten noch Deleuze/Guattaris Plateaus ungeprüft in die Theorie des Manuskripts. Beide dienen hier als operative Orientierungsmodelle für eine nachvollziehbare, relationale und nicht-linear anschließbare Projektarbeit.

## Funktion

Codex arbeitet nicht nur an einzelnen Dateien, sondern an adressierbaren Anschlussstellen. Eine Änderung soll deshalb als Zettel und als Plateau lesbar werden:

- als **Zettel**, weil sie eine Adresse, einen Status, eine Herkunft und bestimmte Verweisbeziehungen besitzt;
- als **Plateau**, weil sie nicht notwendig in einer linearen Reihenfolge aufgeht, sondern von mehreren Stellen aus betreten, fortgesetzt, begrenzt oder reorganisiert werden kann;
- als **rekursive Aktualisierung**, weil jede Änderung den Raum weiterer Bearbeitungsmöglichkeiten verändert.

Das Prinzip ergänzt die rekursive Arbeitsbewegung:

> Anschlussmöglichkeiten → Organisation → Aktualisierung → Reorganisation → Kritik

Es ersetzt sie nicht.

## Arbeitsregeln

1. Jede größere Codex-Änderung erhält eine erkennbare Adresse: Datei, Abschnitt, Entscheidung, Change Event oder TODO.
2. Jede Adresse unterscheidet Quelle, begriffliche Entwicklung, Codex-Vorschlag und bestätigten Status.
3. Beziehungen zwischen Adressen werden nicht bloß gesammelt, sondern typisiert: stützt, begrenzt, verweist auf, widerspricht, öffnet, verschiebt, benötigt Prüfung.
4. Ein Plateau ist eine vorläufige Arbeitskonstellation. Es darf Querverbindungen sichtbar machen, aber keine neue Kapitelordnung behaupten.
5. Nicht-lineare Verbindungen gelten nicht automatisch als Argument. Sie müssen im Manuskript argumentativ ausgearbeitet oder als TODO markiert werden.
6. Codex darf Anschlussmöglichkeiten sichtbar machen, aber nicht anstelle des Autors entscheiden, welche davon Theorie werden.
7. Luhmann und Deleuze/Guattari werden in diesem Prinzip methodisch adressiert. Exakte inhaltliche Behauptungen über ihre Texte benötigen weiterhin Quellenprüfung und Seitenangaben.

## Operativer Ablauf

### 1. Anschließen

Codex bestimmt, an welche vorhandenen Zettel angeschlossen wird:

- verbindliche Projektdateien;
- Manuskriptstellen;
- Entscheidungen unter `knowledge/decisions/`;
- Change Events unter `knowledge/change-events/`;
- Quellen und genealogische Materialien;
- offene TODOs.

### 2. Organisieren

Codex beschreibt, welche Relationen die Bearbeitung tragen:

- Welche Adresse wird fortgesetzt?
- Welche Adresse wird präzisiert?
- Welche Adresse wird begrenzt?
- Welche Adresse bleibt offen?
- Welche spätere Anschlussmöglichkeit entsteht durch den Eingriff?

### 3. Aktualisieren

Codex nimmt die kleinste hinreichende Änderung vor. Die Änderung soll nicht möglichst viele Möglichkeiten erzeugen, sondern die im Auftrag bestimmte Anschlussstelle tragfähig aktualisieren.

### 4. Reorganisieren

Codex prüft, ob die Änderung Beziehungen zwischen mehreren Projektbestandteilen verändert. Wenn ja, werden diese Folgen dokumentiert: als Querverweis, Entscheidung, Change Event, TODO oder bewusste Nicht-Integration.

### 5. Kritisieren

Codex prüft, ob aus einer bloßen Assoziation ein scheinbar gesichertes Argument geworden ist. Besonders zu prüfen ist:

- Wird eine externe Theorie als Autorität verwendet, ohne gelesen und belegt zu sein?
- Wird eine operative Codex-Regel mit einer Buchthese verwechselt?
- Wird die Herkunft aus Montage, Improvisation, Programm und Algorithmus durch zu große Abstraktion verdeckt?
- Werden Zettel bloß akkumuliert, ohne ihre Anschlussfunktion zu bestimmen?
- Wird das Plateau zur Beliebigkeit statt zu einer organisierten offenen Form?

## Codex-Zettelregister

Das optionale Register unter projekt/codex-zettelregister.md sammelt zentrale Arbeitsadressen. Es ist kein Begriffsregister des Manuskripts, sondern eine Karte für Codex-Arbeiten, die mehrere Projektbestandteile verbinden.

## Mini-Format für Codex-Zettel

```yaml
adresse:
status: vorschlag | bestätigt | quelle | entwicklung | todo
herkunft:
relationen:
  - typ:
    ziel:
öffnet:
begrenzt:
todo:
```

Dieses Format ist keine Pflichtdatei für jede Kleinigkeit. Es dient als Denk- und Prüfmaske für größere Codex-Arbeiten.

## Grenzen

Das Prinzip ist kein Ersatz für Lektüre, Argumentation oder Autorenentscheidung. Es erlaubt Codex, projektförmig zu arbeiten: adressierbar wie ein Zettelkasten, nicht-linear anschließbar wie ein Plateau, aber gebunden an die Verfassung des Projekts und an den Vorrang des Manuskripts.