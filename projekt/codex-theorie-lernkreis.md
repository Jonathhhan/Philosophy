# Codex-Theorie-Lernkreis

Status: bestätigtes Arbeitsprinzip für Codex; keine neue Grundthese und kein
Manuskriptbestandteil.

Der Lernkreis organisiert eine wechselseitige, aber asymmetrische Beziehung.
Die bestätigte Theorie verändert unmittelbar, wie Codex im Projekt auswählt,
formuliert, prüft und revidiert. Ergebnisse dieser Arbeit verändern die Theorie
dagegen nicht unmittelbar. Codex kann ihr Widerstände, Nebenfolgen,
Gegenbeispiele und Präzisierungsvorschläge zurückgeben. Erst Quellenprüfung,
begriffliche Rekonstruktion und Autorenentscheidung machen daraus gegebenenfalls
eine theoretische Revision.

„Lernen“ bezeichnet hier keine Modellnachschulung und kein autonomes
Sinnverstehen. Es bezeichnet dokumentierte Veränderungen der Arbeitsregeln und
des vorläufig bestätigten Theoriestands.

## Doppelte Bewegung

### Theorie → Codex

Bestätigte Begriffe, Unterscheidungen und Entscheidungen werden in operative
Prüfbedingungen übersetzt. Codex muss ausweisen:

- welche theoretische Vorgabe seine Bearbeitung organisiert;
- wie sie Auswahl, Variantenbildung oder Prüfung verändert;
- wo die operative Übersetzung gegenüber dem Begriff verkürzt bleibt;
- welche Gegenprobe eine bloße Selbstbestätigung verhindern soll.

Eine erfolgreiche Ausführung zeigt nur, dass die Übersetzung ausführbar und
projektkonsistent ist. Sie bestätigt nicht die philosophische Wahrheit der
Vorgabe.

### Codex → Theorie

Ausgeführte Bearbeitungen können diagnostische Rückgaben hervorbringen:

- Widerstände gegen eine eindeutige Operationalisierung;
- Gegenbeispiele und alternative Beschreibungen ohne Projektvokabular;
- unerwartete Folgen verschiedener Fassungen;
- verdeckte Abhängigkeiten, Auslassungen und Stabilisierungskosten;
- Spannungen zwischen Definition und Anwendung;
- gescheiterte Übertragungen und bestimmte Reichweitengrenzen.

Diese Rückgaben beginnen als `operative_beobachtung` oder
`theoretische_irritation`. Codex darf daraus einen `theoretischen_vorschlag`
entwickeln, aber weder Glossar noch Grundthese, Theorieachse oder Manuskript
automatisch ändern.

## Rückübersetzungssperre

Zwischen operativem Befund und theoretischer Integration liegt eine Sperre.
Vor ihrer Öffnung sind mindestens zu prüfen:

1. Ist der Befund durch die Projektinstruktionen selbst vorgeordnet?
2. Handelt es sich um philosophischen Widerstand oder nur um technische
   Störung, Prompt-Effekt oder Darstellungsgrenze?
3. Lässt sich der Befund ohne das Vokabular des Projekts beschreiben?
4. Welche nicht erzeugten oder zurückgestellten Alternativen beeinflussen ihn?
5. Welche Quellen, Kapitel, Definitionen und Gegenmodelle müssen geprüft werden?
6. Welche Autorenentscheidung wäre für eine Integration erforderlich?

Die Sperre verhindert einen Zirkel, in dem eine Theorie ihre eigenen
Arbeitsregeln erzeugt und deren Befolgung anschließend als Beweis ihrer
Richtigkeit behandelt.

## Lernprotokoll

Für einen substanziellen Lernkreis wird im Change Event oder Forschungsdatensatz
folgende Spur geführt:

```yaml
theoretische_vorgabe:
operative_uebersetzung:
ausgefuehrte_probe:
gegenprobe:
beobachteter_befund:
alternative_deutung:
uebersetzungsverlust:
rueckgabe_status: operative_beobachtung | theoretische_irritation | theoretischer_vorschlag | verworfen
codex_anpassung:
moegliche_theoriefolge:
autorentscheidung: nicht_erforderlich | offen | akzeptiert | verworfen
```

Ein leerer oder gescheiterter Durchlauf wird festgehalten. Produktivität darf
nicht durch künstlich erzeugte Neuheit simuliert werden.

## Operativer Ablauf

1. **Vorgabe aufnehmen:** Autorität, Begriffsfunktion und Reichweite bestimmen.
2. **Übersetzen:** eine begrenzte Prüfregel oder Arbeitsform bilden und den
   Übersetzungsverlust nennen.
3. **Ausführen:** mindestens eine konkrete Bearbeitung und bei echter
   Unbestimmtheit eine relevante Variante ausführen.
4. **Gegenprüfen:** Gegenmodell, beschreibungsfremde Alternative oder
   Nichtübertragbarkeit prüfen.
5. **Zurückgeben:** Befund und alternative Deutung mit vorläufigem Status
   dokumentieren.
6. **Trennen:** Codex-Anpassung darf direkt geprüft werden; eine Theoriefolge
   bleibt bis zur Autorisierung Vorschlag, TODO oder Verwerfung.
7. **Revidieren:** Eine bestätigte Theoriefolge wird in einem eigenen,
   quellen- und relationsgeprüften Eingriff integriert und wirkt danach erneut
   auf Codex zurück.

## Verhältnis zu den anderen Arbeitsformen

- Das rekursive Protokoll steuert Umfang, Autorität und Abschluss.
- Zettelkasten und Plateaus adressieren Vorgaben, Befunde und offene Anschlüsse.
- Das genetische Register verfolgt Herkunft, Mutation und Vererbung.
- Montage führt Varianten aus und macht ihre relationalen Folgen sichtbar.
- Forschungsdatensätze tragen Hypothesen, Gegenmodelle und Statusübergänge.
- Change Events dokumentieren tatsächliche Änderungen des Projektstands.

Der Lernkreis ist daher kein zweites Wissens- oder Ereignissystem. Er verbindet
vorhandene Formen durch eine kontrollierte Rückkante.

## Grenzen

1. Codex ist kein wahrnehmendes oder urteilendes Subjekt und keine zweite
   Theorieautorität.
2. Validator-, Test- oder Build-Erfolg beweist keine philosophische Geltung.
3. Häufige Reproduzierbarkeit macht einen Befund nicht notwendig theoretisch
   relevant.
4. Codex besitzt Auswahl-, Reihenfolge- und Aufmerksamkeitsmacht; diese
   Vorordnung muss in Auslassungen und Gegenproben sichtbar werden.
5. Die Theorie darf nicht zur bloßen Softwaremetapher werden.
6. Negative Befunde, Nichtübertragbarkeit und Übersetzungsverluste sind
   mögliche Ergebnisse und dürfen nicht geglättet werden.
7. Neue Grundbegriffe, Grundthesen, Theorieachsen und Manuskriptrevisionen
   bleiben einer ausdrücklichen Autorenentscheidung vorbehalten.

Leitformel:

> Codex prüft die Theorie nicht von außen; seine theoriegeleitete Arbeit kann jedoch Widerstände, Nebenfolgen und Grenzen hervorbringen, die der Theorie als revidierbare Vorschläge zurückgegeben werden.

