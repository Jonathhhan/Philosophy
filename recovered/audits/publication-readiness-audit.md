# Publikationsreife-Audit

## Gegenstand und Grenze

Dieser Audit prueft den aktuellen Repository-Stand nicht als weiteren Theorieentwurf, sondern als Publikationsprojekt. Grundlage sind `CONSTITUTION.md`, `PROJECT.md`, `WORKFLOW.md`, `GLOSSAR.md`, `README.md`, `projekt/arbeitsstand.md`, die vorhandenen Audits, die Kapitel unter `manuskript/`, der Quellenbereich unter `sources/`, die Wissensdateien unter `knowledge/` und der interaktive Teil unter `interaktiv/`.

Am Manuskript wurde nichts geaendert. Der Audit fuehrt keine neue Infrastruktur, keine neue Theorieachse und keine neue Arbeitsmetapher ein. Er fragt, welche wenigen Schritte jetzt den groessten Qualitaetsgewinn fuer eine wissenschaftlich und oeffentlich verantwortbare Fassung bringen.

## Gesamturteil

Das Projekt hat die Schwelle vom Entwicklungsmanuskript zum publizierbaren Buchentwurf erreicht. Die Kapitel 1 bis 17 und der Schluss liegen vollstaendig vor, die Architektur ist stabil, zentrale Definitionen sind dokumentiert, die genealogische Herkunft aus Bachelorarbeit und Masterarbeit ist in den Kapiteln sichtbar, und der interaktive Teil ist als Anschlusslabor technisch und begrifflich von der Manuskriptargumentation getrennt.

Der naechste Qualitaetssprung entsteht nicht durch weitere Agenten-, Graph-, Hook- oder Automationsschichten. Die bestehende Infrastruktur ist fuer ein philosophisches Einzelprojekt bereits stark und teilweise weiter ausgebaut als die publizierende Huelle. Die Prioritaet sollte nun umgekehrt werden: Infrastruktur stabil halten, Publikationsreife ausbauen.

## Wichtigste Befunde

### 1. Manuskriptstand

Der Manuskriptbestand ist vollstaendig: 17 Kapitel plus Schluss. Der vorhandene Gesamtaudit bewertet den Argumentationsgang als konsistent und nennt keine offene strukturelle Kapitelreorganisation. Die zuvor gefundenen lokalen Konsistenzbefunde wurden laut `projekt/arbeitsstand.md` bearbeitet.

Publikationsseitig fehlt weniger ein weiteres Kapitel als eine Schlussredaktion des gesamten Buchkoerpers. Noetig ist eine Autorenlektuere, die den Text nicht mehr aus Sicht einzelner Codex-Auftraege liest, sondern als zusammenhaengendes Buch: Rhythmus, Wiederholungen, Uebergaenge, Gewichtung der Beispiele und Lesbarkeit der Definitionen.

Empfehlung: keine neue grosse Umschreibung beginnen. Zuerst einen geschlossenen Lesestand herstellen und nur solche Aenderungen eintragen, die der Autor bei der Gesamtlektuere wirklich als Stoerung des Buches wahrnimmt.

### 2. Quellen- und Literaturapparat

Die genealogischen Eigenquellen sind gut vorbereitet. Die Kapitel enthalten Fussnoten zu Bachelorarbeit, Masterarbeit und Gutachten, vor allem dort, wo Montage, Improvisation, Programm, Algorithmus, Komposition, Stabilisierung, Organisation, Verteilung, Asymmetrie, Kritik, Beurteilung, Revision und Reorganisation aus den frueheren Arbeiten konkretisiert werden.

Noch nicht publikationsreif ist der allgemeine Literaturapparat. Es gibt keine sichtbare Bibliographie, keine `.bib`-Datei, keine einheitliche Zitationsstrategie fuer externe philosophische Gespraechspartner und keinen vollstaendigen Nachweisapparat fuer oeffentliche Bezugnahmen. Das ist jetzt die groesste wissenschaftliche Luecke.

Empfehlung: zuerst eine kleine, kontrollierte Literaturliste anlegen, nicht eine ausufernde Forschungsbibliographie. Jede Quelle soll eine Funktion haben: genealogisch, systematisch, begriffsgeschichtlich, methodisch oder kritisch. Externe Autorinnen und Autoren duerfen das Buch nicht in eine allgemeine System-, Macht- oder Gesellschaftstheorie verschieben.

### 3. Manuskript-Build

Das Repository enthaelt viele sehr gute Einzeldateien, aber keinen erkennbaren zusammenhaengenden Buch-Build. Es gibt keinen dokumentierten Befehl, der aus `manuskript/` eine fortlaufende Lese- oder Abgabefassung erzeugt. Ebenso fehlen noch eindeutige Entscheidungen zu Zielformat, Zitierstil, Inhaltsverzeichnis, Abbildungsverzeichnis und Umgang mit Mermaid-Diagrammen in PDF/DOCX/HTML.

Empfehlung: einen minimalen Build-Pfad definieren, bevor weitere Textarbeit beginnt. Zunaechst reicht eine fortlaufende Markdown-Datei oder ein PDF-Prototyp. Wichtig ist nicht typografische Perfektion, sondern dass der Autor das Buch einmal als Ganzes lesen kann.

### 4. Oeffentliche Dokumentation

`README.md` beschreibt das Arbeitsrepository knapp und intern sinnvoll. Fuer eine oeffentliche oder halb-oeffentliche Freigabe ist es noch zu duenn. Es fehlen Angaben zu Projektstatus, Zitierbarkeit, Lizenz/Urheberrecht, Datenschutz, Umgang mit rekonstruierten Chatmaterialien, KI-Anteil und Grenzen der interaktiven Ausgabe.

Empfehlung: README und gegebenenfalls eine eigene `PUBLICATION.md` oder `PUBLIC-README.md` ergaenzen. Dabei sollte klar werden: Das Manuskript ist der primaere Gegenstand; die interaktive Ausgabe ist eine operative Darstellung; Codex war ein Schreib-, Pruef- und Integrationsassistent; die letzte inhaltliche Entscheidung liegt beim Autor.

### 5. Interaktive Ausgabe und KI-Funktion

Das Anschlusslabor ist konzeptionell stark, weil es die Operationen des Buches erfahrbar macht und nicht bloss illustriert. Die optionale KI-Schicht ist bereits gut begrenzt: fluechtig, manuell anzufordern, nicht Autorin, keine automatische Speicherung, serverseitige Secrets, Rate-Limiter und deaktivierter Zustand bei fehlenden Schutzvoraussetzungen.

Offen bleibt die oeffentliche Betriebsentscheidung. Vor Deployment braucht es ein bewusstes Datenschutz- und Missbrauchskonzept: Hostingumgebung, Secrets, Budgetgrenzen, Monitoring, Rate Limits, globale Parallelitaetsgrenze, Protokollierungspolitik und klare Nutzerinformation.

Empfehlung: die KI-Funktion nicht oeffentlich aktivieren, bevor diese Punkte als Deployment-Entscheidung dokumentiert sind. Eine rein lokale oder deaktivierte Demo ist dagegen vertretbar.

### 6. Validatoren

Die zentrale Pruefung `python scripts/check_all.py` ist fuer den Entwicklungsstand stark. Bekannte Wissenswarnungen bleiben sichtbar und nicht blockierend. Weitere Validatoren sollten jetzt nur gezielt ergaenzt werden, wo sie unmittelbar Publikationsrisiken senken.

Empfehlung: keine neue Kontrollarchitektur. Sinnvoll waeren nur wenige haertende Checks: fehlende Fussnotendefinitionen im Gesamtbuild, nicht vorhandene referenzierte Dateien, TODOs im publikationsnahen Bestand, kaputte interne Kapitelverweise, Datenschutzmarker in oeffentlichen Dateien und ein Hinweis, wenn keine Bibliographie vorhanden ist.

## Prioritaeten

1. Literatur- und Quellenapparat konsolidieren.

   Ergebnis: eine kontrollierte Bibliographie, klare Zitationsregeln und ein Kapitel-zu-Quelle-Plan. Keine erfundenen Seitenangaben; externe Quellen nur mit ausgewiesener Funktion.

2. Zusammenhaengenden Manuskript-Build herstellen.

   Ergebnis: eine fortlaufende Lesefassung aus `manuskript/` mit Inhaltsverzeichnis und reproduzierbarem Build-Befehl.

3. Vollstaendige Autorenlektuere durchfuehren.

   Ergebnis: eine Leseliste mit echten Stoerungen, nicht mit abstrakten Optimierungswuenschen. Danach kleine redaktionelle Aenderungen.

4. Oeffentliche Projektdokumentation ergaenzen.

   Ergebnis: Status, Urheberrecht/Lizenzfrage, KI-Mitwirkung, Datenschutzgrenzen, interaktiver Teil und Zitierbarkeit sind fuer Dritte verstaendlich.

5. Deployment- und Datenschutzentscheidung fuer das Anschlusslabor treffen.

   Ergebnis: entweder bewusst deaktivierte KI-Demo oder dokumentiert abgesicherter Betrieb.

6. Validatoren punktuell haerten.

   Ergebnis: wenige Checks gegen publikationsnahe Fehler, ohne neue Agenten- oder Graphschichten.

## Was bewusst nicht empfohlen wird

Keine neue Zettelkasten- oder Rhizom-Infrastruktur im jetzigen Moment. Die Idee bleibt anschlussfaehig, aber ihr Nutzen ist kleiner als der Nutzen eines belastbaren Apparats und einer durchgehenden Lesefassung.

Keine weitere globale Manuskriptrekonstruktion aus Chatmaterial. Die aktuellen Kapitel sind der geltende Manuskriptstand und sollen als bewusst komponierte Fassungen behandelt werden.

Keine Ausweitung auf allgemeine Macht-, Gesellschafts- oder Systemtheorie. Externe Literatur darf als Gespraechspartner auftreten, aber nicht die Reichweite des Projekts verschieben.

Keine oeffentliche Aktivierung der KI-Schicht ohne dokumentierte Schutzentscheidungen.

## Naechster konkreter Arbeitsschritt

Der sinnvollste naechste Schritt ist ein Quellen- und Literaturapparat-Plan. Er sollte fuer jedes Kapitel festhalten:

- welche bestehenden Eigenquellen bereits belegt sind;
- welche externen Quellen wirklich benoetigt werden;
- welche Begriffe ohne externe Literatur auskommen;
- wo Seitenangaben noch am PDF zu pruefen sind;
- welche Quellen nur als Gespraechspartner, nicht als Grundlage der Theorie erscheinen duerfen.

Danach kann der Manuskript-Build kommen. In dieser Reihenfolge wird zuerst wissenschaftliche Belastbarkeit hergestellt und dann die technische Lesefassung gebaut.
