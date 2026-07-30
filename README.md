# Zur Kritik der Organisation von Anschlussmöglichkeiten

Arbeitsrepository für das philosophische Buchprojekt.

## Struktur

- `manuskript/` – fortlaufende Kapiteltexte
- `projekt/architektur.md` – verbindliche Gesamtarchitektur
- `projekt/arbeitsstand.md` – rekonstruierter Stand und offene Sicherungslücken
- `interaktiv/` – geplante HTML-Module zur operativen Darstellung der Begriffe

## Leitgedanke

> Menschen treten in Gespräche ein, die bereits begonnen haben.

Das Projekt untersucht, wie Anschlussmöglichkeiten organisiert, aktualisiert, stabilisiert, kritisiert, revidiert und reorganisiert werden.

## Methodische Regeln

- Probleme vor Begriffe.
- Ableitung vor Definition.
- Notwendigkeit vor Vollständigkeit.
- Anwendungen erst nach der Grundtheorie.

Die Texte werden als Arbeitsfassungen versioniert. Frühere Varianten bleiben über die Git-Historie nachvollziehbar.

## Wissensbasis prüfen

Die YAML-Dateien und ihre internen Referenzen werden mit `python scripts/validate_knowledge.py` geprüft. Die dafür benötigte Entwicklungsabhängigkeit steht in `requirements-dev.txt`.
## Lesefassung bauen

Der aktuelle Manuskriptstand kann als zusammenhängende Markdown-Lesefassung gebaut werden:

```powershell
python scripts/build_manuscript.py
```

Die Ausgabe entsteht unter `build/manuskript-lesefassung.md`. Bearbeitet werden weiterhin die Einzelkapitel unter `manuskript/`.
