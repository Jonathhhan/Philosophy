# Anschlusslabor

Das Anschlusslabor macht die rekursive Bewegung des Buchprojekts als bearbeitbare
Anschlussfolge erfahrbar. Es bleibt vollständig ohne KI nutzbar.

## Lokale Prüfung

```powershell
npm install
npm test
npm run check
npm run build
```

Der Build erzeugt einen Worker unter `dist/server/`. Statische Oberfläche und
API-Adapter werden vom selben Ursprung ausgeliefert.

## Optionale KI-Vorschläge

Die KI ist eine Vorschlagsschicht, keine automatische Autorin. Ein Aufruf erfolgt
nur nach einem Klick auf **KI-Vorschlag anfordern**. Übertragen werden ausschließlich
die gewählte Anschlussweise und der aktuelle Bezugswortlaut. Sitzung, Fassungen,
Freigaben und offene Entwürfe werden nicht gesendet.

Ein Ergebnis bleibt flüchtig. Erst **Vorschlag in den Entwurf übernehmen** kopiert
seinen Wortlaut in das ungespeicherte Textfeld. Erst der getrennte Schritt
**Anschluss aktualisieren** verändert und speichert die Arbeitsfassung.

Der Worker benötigt serverseitig:

- `OPENAI_API_KEY` als Secret;
- `AI_SAFETY_SALT` als zufälliges Secret mit mindestens 32 Zeichen für eine nicht rückrechenbare
  Sicherheitskennung;
- `AI_RATE_LIMITER` als Binding mit `limit({ key })`;
- eine vertrauenswürdige Cloudflare-Proxygrenze, weil die Drosselung `CF-Connecting-IP` verwendet;
- optional `OPENAI_MODEL`; Standard ist `gpt-5.6-sol`.

Fehlt eine dieser Schutzvoraussetzungen, antwortet der Endpunkt mit `503` und die
manuelle Oberfläche bleibt nutzbar. Der API-Schlüssel darf nie in Browsercode,
Repositorydateien oder öffentliche Deploymentvariablen gelangen.

Vor einer öffentlichen Aktivierung sind für die konkrete Hostingumgebung außerdem
Budgetgrenzen, Monitoring, eine globale Parallelitätsgrenze und gegebenenfalls eine
Missbrauchschallenge festzulegen. Der Worker begrenzt den Request-Stream auf
2.000 Byte; der Browser bricht sein Warten nach 20 Sekunden ab. Die Tests verwenden
ausschließlich simulierte
API-Antworten; ein realer OpenAI-Aufruf ist ohne Deployment-Secrets bewusst nicht
Teil der lokalen Prüfung.
