# Begriffsnetze

`scripts/begriffsnetz.py` erzeugt ein lesendes Begriffsnetz zu einem Thema. Es liest
`knowledge/concepts/` und sucht passende Manuskriptanker unter `manuskript/`.
Das Netz ist eine Anschlusskarte: Es zeigt deklarierte Relationen, mögliche
Ankerstellen und Grenzen der automatischen Erkennung. Es bestätigt keine neue
Definition und ersetzt keine Autorenentscheidung.

Beispiele:

```powershell
python scripts\begriffsnetz.py "Algorithmusidentität"
python scripts\begriffsnetz.py "Organisation von Anschlussmöglichkeiten" --depth 2 --anchor-limit 20
python scripts\begriffsnetz.py "Montage und Improvisation" --format json
python scripts\begriffsnetz.py "Algorithmusidentität" --output recovered\proposals\begriffsnetz-algorithmusidentitaet.md
```

Ausgabeformen:

- `markdown`: Bericht mit Mermaid-Diagramm, Begriffsliste und Manuskriptankern.
- `json`: maschinenlesbares Netz für spätere Visualisierung oder interaktive Nutzung.

Grenzen:

- Nicht gefundene Begriffe können dennoch philosophisch relevant sein.
- Textuell gefundene Anker sind Prüfhinweise, keine Belege.
- Bei Integration in Manuskript oder Wissensbasis bleibt ein Change Event und gegebenenfalls eine Autorenentscheidung erforderlich.