# Philosophie-Automat

Status: Prototyp Stufe 5; Projektwerkzeug, kein Manuskriptkapitel und keine Theorieautorit?t.

Der Philosophie-Automat ist die erste technische Umsetzung des Gedankens „Codex als Anschlussapparat“. Er soll keine Philosophie anstelle des Autors erzeugen. Er prüft, welche bereits deklarierten Begriffe, Projektgrenzen und Anschlussstellen durch einen eingegebenen Gedanken berührt werden.

## Zweck

Der Automat beantwortet nicht die Frage, ob ein Satz philosophisch wahr ist. Er beantwortet eine bescheidenere, für dieses Projekt wichtigere Frage:

> Woran schließt dieser Gedanke an, und welche Prüfungen werden dadurch erforderlich?

Damit wird der Automat zu einer Vorschaltstelle vor Manuskriptarbeit. Er kann helfen, Entwürfe, Einwände, Varianten und TODOs zu sortieren, bevor Codex oder der Autor eine Passage stabilisieren.

## Verwendung

```powershell
python scripts/philosophie_automat.py "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."
```

Für maschinenlesbare Ausgabe:

```powershell
python scripts/philosophie_automat.py --format json "Kritik steht nicht außerhalb der Organisation."
```

Der Automat kann auch Text über stdin lesen.

Mögliche Manuskriptanker suchen:

```powershell
python scripts/philosophie_automat.py --find-anchors "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."
```

Ein Vorschlagsdossier schreiben:

```powershell
python scripts/philosophie_automat.py --write-proposal "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."
```


Kapitelbezogenen Entwurf erzeugen:

```powershell
python scripts/philosophie_automat.py --draft-for manuskript/08-algorithmus.md "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."
```

`--draft-for` liest das angegebene Kapitel als lokalen Kontext. Der Bericht nennt Überschriften, im Kapitel erkannte Begriffe, mögliche Anschlussanker, einen markierten Kapitelentwurf und erforderliche Prüfungen. Der Modus verändert das Manuskript nicht. Eine Einfügung entsteht erst, wenn zusätzlich `--apply`, `--target-file` und `--after-heading` gesetzt werden.

Change-Event-Entwurf anzeigen:

```powershell
python scripts/philosophie_automat.py --draft-for manuskript/08-algorithmus.md --event-draft "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."
```

Change-Event-Entwurf als Vorschlagsdatei sichern:

```powershell
python scripts/philosophie_automat.py --draft-for manuskript/08-algorithmus.md --write-event-draft "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."
```

Event-Entwürfe werden unter `recovered/proposals/change-events/` abgelegt. Sie sind bewusst noch keine bestätigten Dateien unter `knowledge/change-events/`. Erst eine geprüfte Übernahme mit Autorentscheidung und Validierung darf daraus ein stabilisiertes Projekt-Ereignis machen.

Change-Event-Entwurf vorpr?fen:

```powershell
python scripts/philosophie_automat.py --draft-for manuskript/08-algorithmus.md --validate-event-draft "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."
```

Die Vorpr?fung kontrolliert Pflichtfelder, Draft-Status, Autorentscheidungsgrenze, erlaubte Operationen und sichere Zielorte. Sie beweist nicht, dass der Vorschlag philosophisch richtig ist. Sie sagt nur: Dieser Entwurf ist als Entwurf weiterbearbeitbar oder nicht.

Einen Vorschlag vollautomatisch, aber markiert, in eine Manuskriptdatei einfügen:

```powershell
python scripts/philosophie_automat.py --apply --target-file manuskript/08-algorithmus.md --after-heading "## 6. Identität und Ausführung" "Ein Algorithmus bleibt derselbe, obwohl seine materielle Implementierung wechselt."
```

`--apply` benötigt immer eine vorhandene Zieldatei unter `manuskript/` und eine exakte Marker- oder Überschriftszeile. Der eingefügte Text wird als `PHILOSOPHIE_AUTOMAT`-Vorschlag markiert und gilt nicht als bestätigte Theorie.

## Arbeitsweise

1. Er liest die Concept-Dateien unter `knowledge/concepts/`.
2. Er erkennt Begriffe über einfache, nachvollziehbare Namens- und Labeltreffer.
3. Er zeigt Definitionen, Arbeitsnotizen, Grenzen, Quellenpfade und benachbarte Begriffe.
4. Er markiert Projektgrenzen, etwa Macht-/Herrschaftsausweitung, KI-Autorität, technische Reduktion oder voraussetzungslosen Anfang.
5. Er gibt Prüfrollen aus: Genealoge, Konsistenzprüfer, Kritiker und material-technischer Prüfer.
6. Er kann markierte Textvorschläge und Vorschlagsdossiers erzeugen.
7. Er kann mit `--apply` einen Vorschlag an einer explizit angegebenen Manuskriptstelle einfügen, ohne ihn als bestätigt auszugeben.

## Grenzen

Der Automat ist regelbasiert und transparent. Er versteht keine Argumente im starken Sinn, erzeugt keine belastbaren Quellenurteile und ersetzt keine Lektüre. Treffer können fehlen, wenn ein Gedanke andere Wörter verwendet. Treffer können zu weit sein, wenn ein Begriff nur nebenbei erwähnt wird. Automatische Manuskripteinfügungen sind deshalb immer als Vorschlag markiert und müssen editorisch geprüft werden.

Das ist kein Mangel der Stufe 1, sondern ihre philosophische Sicherung. Der Automat soll nicht den Eindruck erwecken, er könne Urteil, Autorentscheidung oder Quellenarbeit automatisieren. Er macht Anschlussbedingungen sichtbar und hält dadurch die weitere Arbeit prüfbar.

## Nächste Stufen

1. Stufe 2: Ein kleines Anschlusslabor-Modul „Gedanke prüfen“, das die Ausgabe sichtbar und interaktiv macht.
2. Stufe 3: KI-gestützte Vorschläge innerhalb eines geschlossenen Schemas, getrennt von Autorentscheidung und Manuskriptstand.
3. Stufe 4: Verbindung mit Change-Event-Vorlagen, sodass aus einer Prüfung ein dokumentierter Vorschlag oder ein TODO entstehen kann.
4. Stufe 5: Kontrollierte automatische Manuskriptänderung mit vorheriger Relationsprüfung, Change Event und nachgelagerter Konsistenzprüfung.

Der Automat ist inzwischen mit Syntax- und JSON-Smoke-Test in `scripts/check_all.py` aufgenommen. TODO: Entscheiden, ob und wie Stufe 2 im Anschlusslabor umgesetzt wird.
