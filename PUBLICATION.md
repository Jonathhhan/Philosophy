# Publikations- und Nutzungshinweise

Status: vorlaeufige Publikationshülle fuer ein noch nicht zitierfaehiges Arbeitsmanuskript.

Diese Datei beschreibt, wie das Repository derzeit gelesen, zitiert, weitergegeben und technisch verstanden werden soll. Sie ersetzt keine Verlags-, Lizenz- oder Datenschutzentscheidung. Solche Entscheidungen bleiben beim Autor.

## 1. Projektstatus

`Zur Kritik der Organisation von Anschlussmoeglichkeiten` liegt als vollstaendiger Arbeitsentwurf mit 17 Kapiteln und Schluss vor. Der aktuelle Manuskriptstand befindet sich unter `manuskript/`; die generierte Lesefassung liegt unter `build/manuskript-lesefassung.md`.

Das Manuskript ist noch keine zitierfaehige Endfassung. Die naechste Arbeitsphase betrifft vor allem:

- Schlussredaktion des Gesamtmanuskripts;
- Literatur- und Quellenapparat;
- Zitierstil und bibliografische Form;
- oeffentliche Dokumentation;
- Entscheidung ueber Publikations-, Lizenz- und Deploymentform.

## 2. Zitierbarkeit

Bis zur ausdruecklichen Freigabe durch den Autor gilt:

- Nicht als abgeschlossene Buchfassung zitieren.
- Keine Kapitelversion als endgueltige Autorenposition behandeln, wenn sie nicht ausdruecklich freigegeben wurde.
- Bei Bezugnahme auf das Repository Datum, Commit und Datei angeben.
- Direkte Zitate aus Manuskriptdateien nur nach Ruecksprache oder mit klarer Kennzeichnung als Arbeitsfassung verwenden.

Empfohlenes internes Zitierformat fuer Arbeitsbezuege:

```text
Jonathan Frank, Zur Kritik der Organisation von Anschlussmoeglichkeiten, Arbeitsfassung, Datei <pfad>, Commit <hash>, Datum <datum>.
```

## 3. Urheberrecht und Lizenz

Alle Manuskripttexte, Projekttexte, rekonstruierten Materialien und interaktiven Inhalte stehen, soweit nicht anders ausgewiesen, unter Urheberrecht von Jonathan Frank.

Derzeit ist keine offene Lizenz gesetzt. Das bedeutet:

- Keine freie Weiterverwendung ohne Erlaubnis.
- Keine stillschweigende Freigabe fuer Training, Nachdruck, kommerzielle Nutzung oder Bearbeitung.
- Technische Abhaengigkeiten behalten ihre eigenen Lizenzen.

TODO: Der Autor entscheidet spaeter, ob eine Lizenzdatei ergaenzt wird und ob Manuskript, Code, interaktive Ausgabe und Archivmaterial unterschiedliche Lizenzregeln erhalten.

## 4. Manuskript, Rekonstruktionen und Archiv

Der verbindliche Buchstand liegt unter `manuskript/`. Fruehere Chatfassungen, rekonstruiertes Material und Assistentenantworten unter `archive/` und `recovered/` sind historische Quellen oder Arbeitsmaterialien. Sie sind nicht automatisch Manuskriptstand.

Bei jeder Uebernahme gilt die Trennung:

- Quelle;
- begriffliche Entwicklung;
- Codex- oder Agentenvorschlag;
- bestaetigte Projektentscheidung;
- aktueller Manuskriptstand.

Unsichere Rekonstruktionen duerfen nicht als gesicherter Autorenwortlaut ausgegeben werden.

## 5. KI- und Codex-Mitwirkung

Codex wurde in diesem Projekt als Schreib-, Pruef-, Integrations- und Dokumentationsassistent eingesetzt. Codex ist keine Theorieautoritaet und kein Ersatz fuer die inhaltliche Entscheidung des Autors.

Die Projektdateien `AGENTS.md`, `WORKFLOW.md`, `projekt/codex-als-anschlussapparat.md`, `projekt/codex-prinzip-zettelkasten-plateaus.md` und `projekt/codex-methode-verfeinerung.md` beschreiben diese Arbeitsweise. Sie gehoeren zur Projektorganisation, nicht automatisch zum Manuskript.

Automatisch oder halbautomatisch erzeugte Vorschlaege muessen als Vorschlag, gepruefter Vorschlag, TODO oder offene Autorentscheidung markiert bleiben, bis sie ausdruecklich stabilisiert werden.

## 6. Quellen- und Literaturpolitik

Die Bachelorarbeit und Masterarbeit unter `sources/` sind genealogische Primaerquellen des Projekts. Sie duerfen nicht als unveraenderte aktuelle Theorie ausgegeben werden. Ihre Funktion ist in `sources/README.md`, `sources/development.md` und `literatur/quellen.md` beschrieben.

Externe Literatur wird nur mit ausgewiesener Funktion aufgenommen: genealogisch, systematisch, begriffsgeschichtlich, methodisch oder kritisch. Sie darf die Architektur des Buches nicht stillschweigend ersetzen und darf das Projekt nicht in eine allgemeine Macht-, Gesellschafts- oder Systemtheorie verschieben.

Genaue Behauptungen und direkte Zitate benoetigen Seitenangaben aus den Originalquellen.

## 7. Anschlusslabor und KI-Funktion

Der interaktive Teil unter `interaktiv/` ist eine operative Darstellung einzelner Projektbegriffe. Er ersetzt nicht das Manuskript und ist nicht selbst die Theorie.

Die optionale KI-Funktion ist ohne serverseitige Schutzkonfiguration deaktiviert. Vor einer oeffentlichen Aktivierung braucht es eine gesonderte Deployment- und Datenschutzentscheidung, insbesondere zu:

- Hostingumgebung;
- API-Secrets;
- Rate Limits und Budgetgrenzen;
- Monitoring und Protokollierung;
- Missbrauchsschutz;
- Nutzerinformation;
- Trennung von lokaler Sitzung, Manuskriptstand und KI-Vorschlag.

Bis zu dieser Entscheidung ist eine lokale oder deaktivierte Demo der sichere Standard.

## 8. Datenschutz und private Materialien

`archive/` und `recovered/` enthalten bereinigte Entwicklungs- und Sicherungsmaterialien. Persoenliche Gespraeche und private Prompts gehoeren nicht in die oeffentliche Buchargumentation.

Vor jeder oeffentlichen Freigabe sind zu pruefen:

- ob private oder personenbezogene Inhalte enthalten sind;
- ob Chatmaterial hinreichend redigiert wurde;
- ob technische Secrets ausgeschlossen sind;
- ob interaktive Logs oder KI-Anfragen gespeichert werden;
- ob README, Anschlusslabor und Archiv dieselbe Datenschutzgrenze formulieren.

## 9. Oeffentliche Freigabe

Vor einer oeffentlichen oder halb-oeffentlichen Freigabe sollten mindestens folgende Punkte abgeschlossen sein:

1. Lizenz- und Urheberrechtsentscheidung.
2. Zitierstatus des Manuskripts.
3. Bibliografie- und Zitierstil.
4. Datenschutzentscheidung fuer Archiv und Anschlusslabor.
5. Entscheidung, ob die KI-Funktion deaktiviert bleibt oder abgesichert deployed wird.
6. Build der aktuellen Lesefassung.
7. Zentrale Projektpruefung.

Bis dahin ist das Repository ein Arbeitsrepository und kein endgueltiges Publikationsartefakt.
