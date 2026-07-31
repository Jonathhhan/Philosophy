# Codex in diesem Projekt nutzen

Status: praktische Anleitung fuer die Arbeit mit Codex; kein Manuskriptbestandteil.

Diese Anleitung beschreibt, wie Codex im Projekt **Zur Kritik der Organisation von Anschlussmoeglichkeiten** sinnvoll eingesetzt wird. Codex ist hier nicht nur ein Textgenerator, sondern ein Schreib-, Pruef-, Integrations- und Revisionsapparat. Seine Arbeit soll nachvollziehbar bleiben: Jede groessere Aktualisierung muss zeigen, woran sie anschliesst, was sie veraendert, was sie offenlaesst und welche spaeteren Anschlussmoeglichkeiten dadurch entstehen.

## 1. Grundhaltung

Codex arbeitet innerhalb eines bereits bestimmten theoretischen Rahmens. Der Gegenstand des Buches ist die Organisation von Anschlussmoeglichkeiten. Die leitende Bewegung lautet:

```text
Anschlussmoeglichkeiten -> Organisation -> Aktualisierung -> Reorganisation -> Kritik
```

Der zentrale Satz bleibt:

> Jede Aktualisierung veraendert den Raum weiterer Anschlussmoeglichkeiten.

Codex darf entwerfen, pruefen, praezisieren, reorganisieren und technische Ausgaben bauen. Codex darf aber keine Grundthese, keinen Grundbegriff und keine Theorieachse stillschweigend ersetzen.

## 2. So sollte ein guter Auftrag aussehen

Ein guter Codex-Auftrag nennt moeglichst klar:

- was bearbeitet werden soll;
- welche Dateien geaendert werden duerfen;
- welche Dateien nicht geaendert werden duerfen;
- ob Codex nur pruefen oder auch schreiben soll;
- ob Quellen gelesen werden muessen;
- ob philosophische Agenten oder Rollen beteiligt werden sollen;
- ob eine optionale delegierte Codex-Entscheidung erlaubt ist;
- ob am Ende committed und gepusht werden soll.

Beispiel:

```text
Arbeite Kapitel 8 weiter aus. Lies vorher CONSTITUTION.md, PROJECT.md,
GLOSSAR.md, Kapitel 7, Kapitel 8 und die einschlaegigen Concept-Dateien.
Aendere nur manuskript/08-algorithmus.md. Markiere unsichere Quellenfragen
als TODO. Keine neuen Grundbegriffe. Pruefe Konsistenz und dokumentiere die
Aenderung im Arbeitsstand.
```

## 3. Die wichtigsten Arbeitsmodi

### Nur pruefen

Codex liest, vergleicht und berichtet. Keine Dateien werden geaendert.

Geeignet fuer:

- Reviews;
- Konsistenzpruefungen;
- Quellen- und Provenienzvergleiche;
- Diskussion philosophisch strittiger Punkte;
- Entscheidungsvorbereitung.

Formulierung:

```text
Pruefe Kapitel 8 auf Widersprueche zum Programmbegriff. Veraendere keine Dateien.
```

### Schreiben oder praezisieren

Codex bearbeitet eine bestimmte Datei oder einen Abschnitt. Die Aenderung soll klein, nachvollziehbar und anschlussfaehig bleiben.

Formulierung:

```text
Praezisiere den Abschnitt zur Algorithmusidentitaet in Kapitel 8. Aendere nur dieses Kapitel. Keine neue Theorieachse.
```

### Reorganisieren

Codex veraendert Beziehungen zwischen mehreren Projektbestandteilen: Methode, Workflow, interaktive Ausgabe, Wissensbasis, Change Events oder Querverweise.

Formulierung:

```text
Reorganisiere die Codex-Methode so, dass Zettelkasten, Plateau und genetisches Register zusammenarbeiten. Keine Manuskriptdateien aendern.
```

### Interaktiver Teil

Codex arbeitet an `interaktiv/`. Die interaktive Ausgabe folgt dem Manuskript, ersetzt es aber nicht. KI-Funktionen brauchen klare Status-, Datenschutz- und Sicherheitsgrenzen.

Formulierung:

```text
Arbeite am interaktiven Teil. Mache sichtbar, dass KI-Vorschlaege fluechtig bleiben und erst durch Freigabe eine Fassung werden. Pruefe Tests und Build.
```

## 4. Rekursiv arbeiten

Bei groesseren Aufgaben verwendet Codex den lokalen Recursive-Codex-Apparat. Die Bewegung ist:

1. **Anschliessen:** verbindlichen Stand, Auftrag, Quellen und betroffene Dateien aufnehmen.
2. **Organisieren:** Abhaengigkeiten, Rollen, Querverweise und Entscheidungskompetenz bestimmen.
3. **Aktualisieren:** die kleinste hinreichende Aenderung ausfuehren.
4. **Reorganisieren:** pruefen, ob Relationen zwischen Dateien, Begriffen oder Ausgaben verschoben wurden.
5. **Kritisieren:** Folgen, Widersprueche, Auslassungen und Unsicherheiten pruefen.

Codex soll nicht einfach immer mehr Text erzeugen. Gute Arbeit besteht darin, die richtige Anschlussstelle zu finden und sie tragfaehig zu aktualisieren.

## 5. Zettelkasten, Plateaus, genetisches Register und Montage

Das Projekt nutzt vier operative Formen, die zusammenarbeiten:

| Form | Funktion | Datei |
| --- | --- | --- |
| Zettel | feste Adresse, Status, Verweise | `projekt/codex-zettelregister.md` |
| Plateau | nicht-lineare Konstellation von Anschlussstellen | `projekt/codex-prinzip-zettelkasten-plateaus.md` |
| genetisches Register | Herkunft, Mutation, Pruefung, Entscheidung, Nachkommen | `projekt/genetisches-register.md` |
| Montage | Materialauswahl, Schnitt, ausgefuehrte Varianten, Anordnung und Rueckkopplung | `projekt/codex-prinzip-montage.md` |

Codex soll diese Formen nutzen, wenn ein Gedanke mehr ist als eine lokale Formulierung. Besonders wichtig ist das bei Gedanken, die aus mehreren Quellen, Kapiteln, Entscheidungen oder technischen Umsetzungen hervorgehen.

Kurzform:

```text
Zettel: Wo ist der Gedanke adressiert?
Plateau: Von wo aus kann man anschliessen?
Genetik: Woher kommt der Gedanke, wie mutiert er, was vererbt er?
Montage: Welche Fassung bildet welche Beziehungen, und was zeigt ihr Vergleich?
```

Bei groesseren Kompositionen, Revisionen und Reorganisationen wird Montage als
Arbeitsprinzip aktiv. Codex sichert das Ausgangsmaterial, weist Auswahl und
Auslassung aus, fuehrt bei echter Unbestimmtheit vergleichbare Varianten aus,
sichtet deren Folgen und stabilisiert nur eine gepruefte und autorisierte
Fassung. Das bedeutet weder, dass jeder Datei-Edit Montage sei, noch dass Codex
dadurch autonom urteile.

## 6. Tractatus-philosophicus-Methode fuer Codex

Die Tractatus-Methode ist ein Klaerungsmodus. Codex ordnet einen Gedanken in nummerierte Saetze, Untersaetze, Grenzen und Anschlussbedingungen. Die Methode imitiert keinen Autorstil und macht aus der Nummerierung keine Gewissheit. Sie hilft, zu sehen, welche Saetze voneinander abhaengen und wo ein Gedanke noch unklar, zu allgemein oder nicht anschlussfaehig ist.

Geeignet ist sie fuer:

- Leitsaetze und zentrale Thesen pruefen;
- Begriffe in eine klare Abhaengigkeitsordnung bringen;
- Grenzen einer Aussage sichtbar machen;
- Manuskriptanker fuer einen Gedanken finden;
- zwischen Definition, Anwendung, Einwand, Beispiel und TODO unterscheiden.

Typischer Befehl:

```powershell
python scripts\tractatus_automat.py "Jede Aktualisierung veraendert den Raum weiterer Anschlussmoeglichkeiten"
```

Mit Ausgabe in eine Vorschlagsdatei:

```powershell
python scripts\tractatus_automat.py "Algorithmusidentitaet" --output recovered\proposals\tractatus-algorithmusidentitaet.md
```

Guter Prompt:

```text
Nutze die Tractatus-philosophicus-Methode, um diesen Gedanken propositional zu ordnen. Veraendere noch keine Manuskriptdateien.
```

Die Ausgabe bleibt `Vorschlag` oder `Pruefstruktur`. Wenn ein Satz in das Manuskript uebernommen werden soll, braucht er weiterhin Kontextlekture, Statusmarkierung, Quellenpruefung und gegebenenfalls Autorentscheidung.
## 7. Optionale delegierte Codex-Entscheidung

Der Autor kann Codex erlauben, in einem klar begrenzten Fall eine vorlaeufige Entscheidung zu uebernehmen. Das ist kein Standardmodus.

Delegation ist geeignet fuer:

- Auswahl zwischen kleinen methodischen Varianten;
- Priorisierung von Dokumentationsformen;
- lokale Integrationsentscheidungen ohne neue Theorieachse;
- technische oder redaktionelle Entscheidungen innerhalb vorhandener Regeln.

Nicht delegierbar bleiben:

- neue Grundbegriffe;
- neue Grundthesen;
- neue Theorieachsen;
- Kapitelumordnungen;
- Quellenbehauptungen ohne Primarquellenpruefung;
- Datenschutz, Lizenz, Deployment und oeffentliche Veroeffentlichung;
- Faelle mit mehreren philosophisch gleich starken Loesungen.

Formulierung:

```text
Du darfst in diesem eng begrenzten Fall eine delegierte Codex-Entscheidung treffen. Dokumentiere sie als revidierbar.
```

Codex muss dann im Ergebnis sagen, was delegiert entschieden wurde und wie der Autor es spaeter revidieren kann.

## 8. Quellen und Genealogie

Fuer Arbeiten an Improvisation, Programm, Algorithmus, Montage, Form oder Moeglichkeitsraum gelten die frueheren Arbeiten unter `sources/` als verbindlicher Kontext. Genaue Zitate, Seitenangaben und historische Behauptungen duerfen nur nach Quellenpruefung verwendet werden.

Codex muss unterscheiden:

- Quelle;
- begriffliche Entwicklung;
- Codex-Vorschlag;
- bestaetigte aktuelle Position;
- TODO / offen.

Fruehere Fassungen oder Chatmaterial sind nicht automatisch verbindlicher als der aktuelle Manuskriptstand.

## 9. Wann Codex Agenten oder Rollen nutzen soll

Philosophische Agenten oder Rollen sind sinnvoll, wenn ein Punkt strittig ist oder mehrere plausible Richtungen bestehen. Die Rollen beraten, entscheiden aber nicht.

Typische Rollen:

- Genealoge: Herkunft und Entwicklungsstufen pruefen.
- Begriffswächter: Definitionen und Kapitelgrenzen pruefen.
- Kritiker: Einwaende und verdeckte Voraussetzungen suchen.
- Material-technischer Pruefer: Montage, Material, Programm, Algorithmus und Implementierung sichtbar halten.
- Lektor: Stil und Uebergaenge verbessern.

Formulierung:

```text
Diskutiere diesen Punkt mit philosophischen Rollen. Fuehre die Befunde zusammen, aber veraendere noch keine Dateien.
```



### Automatenverbund

Der Automatenverbund kombiniert die vorhandenen Automaten nur dort, wo Anschlussbruecken bestehen. Er ist sinnvoll, wenn ein Gedanke zugleich unterschieden, propositional geordnet und als Auffuehrungsspur sichtbar gemacht werden soll.

```powershell
python scripts\automatenverbund.py Anschliessen Nicht-Anschluss --context "von der ersten Unterscheidung bis zur Auffuehrung" --max-steps 8
```

Guter Prompt:

```text
Kombiniere die Automaten, aber nur wo Anschluesse ausgewiesen sind. Schreibe eine Proposal-Spur und veraendere kein Manuskript.
```
### Selbstprogrammierendes Kunstwerk

Der Kunstwerk-Automat verbindet Unterscheidungslogik, Concept-Relationen und Score. Er startet mit einer ersten Unterscheidung und erzeugt daraus eine Folge weiterer Markierungen. Jeder Schritt schreibt zugleich eine Programmlinie der Auffuehrung.

```powershell
python scripts\kunstwerk_automat.py Anschliessen Nicht-Anschluss --max-steps 17
```

Guter Prompt:

```text
Lass das selbstprogrammierende Kunstwerk von der ersten Unterscheidung aus laufen. Schreibe die Auffuehrung als Proposal, aber veraendere kein Manuskript.
```

Die Ausgabe ist ein Kunst-/Pruefobjekt. Sie darf als Denk- und Visualisierungsmaterial dienen, aber nicht automatisch als Buchargument.
## 10. Pruefungen

Nach groesseren Aenderungen soll Codex passende Pruefungen ausfuehren. Typisch sind:

```powershell
python -B .agents\skills\recursive-codex\scripts\validate_change_event.py knowledge\change-events\NNNN-name.yaml
python scripts\check_all.py --skip-install
```

Bei Arbeiten am interaktiven Teil gehoeren Tests und Build dazu. Ein Abschluss ist erst sauber, wenn die relevanten Pruefungen bestanden sind oder ein Blocker ausdruecklich dokumentiert ist.

## 11. Commit und Push

Wenn der Autor `commit + push` oder `push to main origin` sagt, soll Codex vorher den Arbeitsstand pruefen, sinnvolle Dateien stagen, eine konkrete Commit-Nachricht verwenden und danach pushen.

Wichtig: Inhaltliche, methodische und technische Aenderungen sollten moeglichst getrennt committed werden. Wenn bereits viele uncommitted Aenderungen vorliegen, muss Codex den Umfang nennen, statt stillschweigend alles als eine Sache auszugeben.

## 12. Gute Kurzprompts

```text
review repo
```

Prueft den Zustand und berichtet, ohne automatisch zu aendern.

```text
weiter
```

Setzt die zuletzt begonnene Arbeit fort. Codex muss aus dem Arbeitsstand und Git-Status rekonstruieren, was sinnvoll anschliesst.

```text
arbeite am interaktiven teil
```

Bearbeitet `interaktiv/` und prueft Tests/Build.

```text
diskutiere mit philosophischen Agenten, veraendere noch keine Dateien
```

Erzeugt Kritik und Varianten, aber keine Integration.

```text
mache das, delegierte Codex-Entscheidung erlaubt
```

Erlaubt Codex eine begrenzte, revidierbare Entscheidung innerhalb der bestehenden Regeln.

```text
commit + push
```

Prueft, staged, committed und pushed den aktuellen Stand, sofern kein Risiko oder unklarer Umfang blockiert.

## 13. Was Codex am Ende berichten soll

Ein guter Abschlussbericht nennt knapp:

- was aktualisiert wurde;
- welche Anschlussbedingungen betroffen sind;
- welche Moeglichkeiten geoeffnet, begrenzt oder zurueckgestellt wurden;
- welche Entscheidung bestaetigt, delegiert oder offen ist;
- welche Pruefungen gelaufen sind;
- ob committed oder gepusht wurde.

Codex soll nicht nur sagen: `erledigt`. Besser ist: `erledigt, geprueft, mit diesen offenen Grenzen`.