import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { Window } from 'happy-dom';

const html = await readFile(new URL('../index.html', import.meta.url), 'utf8');
const script = await readFile(new URL('../js/main.js', import.meta.url), 'utf8');
const storageKey = 'anschlusslabor.session.v2';

function createApp(storedSession) {
  const window = new Window({ url: 'https://anschlusslabor.test/' });
  window.document.write(html);
  window.confirm = () => true;
  if (storedSession) {
    window.localStorage.setItem(storageKey, storedSession);
  }
  window.eval(script);
  return window;
}

function setValue(window, selector, value) {
  const element = window.document.querySelector(selector);
  element.value = value;
  element.dispatchEvent(new window.Event('input', { bubbles: true }));
  return element;
}

function click(window, selector) {
  const element = window.document.querySelector(selector);
  assert.ok(element, 'Expected element ' + selector);
  element.click();
  return element;
}

function versionItem(window, label) {
  return [...window.document.querySelectorAll('.version-item')]
    .find((item) => item.querySelector('.version-summary strong')?.textContent === label);
}

function addConnection(window, move, wording) {
  click(window, `[data-move='${move}']`);
  setValue(window, '#connection-text', wording);
  click(window, '#commit-move');
}

async function importJson(window, payload) {
  const target = window.document.querySelector('#import-session');
  const file = new window.File([JSON.stringify(payload)], 'session.json', { type: 'application/json' });
  Object.defineProperty(target, 'files', { configurable: true, value: [file] });
  await window.importSession({ target });
}

test('Eingaben und Operationswahl besitzen die angekündigten zugänglichen Zustände', () => {
  const window = createApp();
  const beginning = window.document.querySelector('#beginning');
  const counter = window.document.querySelector('#char-count');
  const moveButton = window.document.querySelector("[data-move='fortsetzen']");

  assert.equal(beginning.getAttribute('aria-describedby'), 'beginning-help char-count char-warning');
  assert.equal(counter.getAttribute('aria-live'), null);
  assert.equal(window.document.querySelector('#char-warning').getAttribute('role'), 'status');
  assert.equal(window.document.querySelector('#storage-status').getAttribute('role'), 'status');
  assert.equal(moveButton.getAttribute('aria-pressed'), 'false');
  assert.equal(window.document.querySelector('#import-session-trigger').tagName, 'BUTTON');

  setValue(window, '#beginning', 'Zugänglicher Ausgang.');
  moveButton.click();
  assert.equal(moveButton.getAttribute('aria-pressed'), 'true');
  assert.equal(window.document.querySelector('#connection-text').getAttribute('aria-describedby'), 'move-prompt connection-count connection-warning');
  assert.match(window.document.querySelector('#manuscript-chapter').textContent, /Kapitel 1: Anschließen/);
  assert.match(window.document.querySelector('#manuscript-question').textContent, /Bedingung des vorherigen Wortlauts/);
  window.happyDOM.abort();
});
test('Eingabe aktiviert Operationen und ein konkreter Anschluss erscheint im Verlauf', () => {
  const window = createApp();
  setValue(window, '#beginning', 'Eine Möglichkeit ist bedingt.');

  assert.equal(window.document.querySelector('#moves').disabled, false);
  click(window, "[data-move='fortsetzen']");
  assert.equal(window.document.querySelector('#connection-composer').hidden, false);

  setValue(window, '#connection-text', 'Daraus folgt, dass Bedingungen den Vollzug nicht vollständig festlegen.');
  assert.equal(window.document.querySelector('#commit-move').disabled, false);
  click(window, '#commit-move');

  assert.match(window.document.querySelector('#actual-text').textContent, /Bedingungen den Vollzug/);
  assert.match(window.document.querySelector('#history').textContent, /Als Fortsetzung gesetzt/);
  assert.match(window.document.querySelector('#history').textContent, /Daraus folgt/);
  assert.match(window.document.querySelector('#history').textContent, /Kapitel 1: Anschließen/);
  assert.equal(window.document.querySelector('#beginning').disabled, true);
  assert.match(window.document.querySelector('#actual-relation').textContent, /Als Fortsetzung gesetzt/);
  assert.equal(window.document.querySelector('#zettel-address').textContent, 'Zettel 02');
  assert.match(window.document.querySelector('#plateau-copy').textContent, /Fortsetzen bildet Zettel 02/);
  assert.match(window.document.querySelector('#plateau-link').textContent, /Kapitel 1: Anschließen/);
  assert.match(window.document.querySelector('#plateau-links').textContent, /Zettel 01 → Zettel 02: Fortsetzen/);
  assert.match(window.document.querySelector('#plateau-links').textContent, /Zettel 02 → \?/);
  assert.equal(window.document.querySelector('#relation-check').hidden, false);
  assert.equal(window.document.activeElement, window.document.querySelector('#observation'));

  window.happyDOM.abort();
});

test('Bearbeitung der Ausgangsäußerung löscht den Verlauf nicht unsichtbar', () => {
  const window = createApp();
  setValue(window, '#beginning', 'Erste Ausgangsäußerung.');
  addConnection(window, 'praezisieren', 'Die Bedingung ist sprachlich bestimmt.');

  click(window, '#edit-beginning');
  setValue(window, '#beginning', 'Veränderte Ausgangsäußerung.');
  assert.match(window.document.querySelector('#history').textContent, /sprachlich bestimmt/);

  click(window, '#accept-beginning-edit');
  assert.doesNotMatch(window.document.querySelector('#history').textContent, /sprachlich bestimmt/);
  assert.match(window.document.querySelector('#history').textContent, /Veränderte Ausgangsäußerung/);
  assert.match(window.document.querySelector('#observation').textContent, /nicht stillschweigend/);
  assert.equal(window.document.activeElement, window.document.querySelector('#observation'));
  window.happyDOM.abort();
});

test('Freigabe betrifft die sichtbar bearbeitete Version und löst die frühere aktuelle Freigabe ab', () => {
  const window = createApp();
  setValue(window, '#beginning', 'Fassung eins.');
  click(window, '#stabilize');
  click(window, '#release');

  setValue(window, '#beginning', 'Fassung zwei.');
  click(window, '#stabilize');
  click(window, '#release');

  assert.equal(window.document.querySelectorAll('.version-item.is-current-release').length, 1);
  assert.match(versionItem(window, 'Fassung 02').textContent, /aktuell freigegeben/);
  assert.match(versionItem(window, 'Fassung 01').textContent, /früher freigegeben/);

  versionItem(window, 'Fassung 01').querySelector('.version-action').click();
  assert.match(window.document.querySelector('#release').textContent, /Fassung 01/);
  assert.equal(window.document.querySelector('#release').disabled, false);
  click(window, '#release');

  assert.equal(window.document.querySelectorAll('.version-item.is-current-release').length, 1);
  assert.match(versionItem(window, 'Fassung 01').textContent, /aktuell freigegeben/);
  assert.match(versionItem(window, 'Fassung 02').textContent, /früher freigegeben/);
  window.happyDOM.abort();
});

test('Festgehaltene Fassungen und Freigabe überdauern einen Reload im lokalen Träger', () => {
  const firstWindow = createApp();
  setValue(firstWindow, '#beginning', 'Eine lokal bewahrte Äußerung.');
  addConnection(firstWindow, 'variieren', 'Eine auf dem Gerät wiederaufnehmbare Variation.');
  click(firstWindow, '#stabilize');
  click(firstWindow, '#release');
  const stored = firstWindow.localStorage.getItem(storageKey);
  assert.ok(stored);
  firstWindow.happyDOM.abort();

  const secondWindow = createApp(stored);
  assert.match(secondWindow.document.querySelector('#actual-text').textContent, /wiederaufnehmbare Variation/);
  assert.equal(secondWindow.document.querySelector('#version-count').textContent, '1 Fassung');
  assert.equal(secondWindow.document.querySelectorAll('.version-item.is-current-release').length, 1);
  assert.match(secondWindow.document.querySelector('#storage-status').textContent, /wiederaufgenommen/);
  secondWindow.happyDOM.abort();
});

test('Aktuelle Eingabe und gesamte Sitzung besitzen getrennte Löschhandlungen', () => {
  const window = createApp();
  setValue(window, '#beginning', 'Zu bewahrende Fassung.');
  click(window, '#stabilize');
  click(window, '#clear-current');

  assert.equal(window.document.querySelector('#beginning').value, '');
  assert.equal(window.document.querySelector('#version-count').textContent, '1 Fassung');

  window.confirm = () => false;
  click(window, '#clear-session');
  assert.equal(window.document.querySelector('#version-count').textContent, '1 Fassung');

  window.confirm = () => true;
  click(window, '#clear-session');
  assert.equal(window.document.querySelector('#version-count').textContent, '0 Fassungen');
  assert.equal(window.localStorage.getItem(storageKey), null);
  window.happyDOM.abort();
});

test('Import verlangt Zustimmung und bewahrt den bestehenden Stand bei Abbruch', async () => {
  const sourceWindow = createApp();
  setValue(sourceWindow, '#beginning', 'Importierte Sitzung.');
  addConnection(sourceWindow, 'variieren', 'Importierte Variante.');
  const payload = JSON.parse(sourceWindow.localStorage.getItem(storageKey));
  sourceWindow.happyDOM.abort();

  const window = createApp();
  setValue(window, '#beginning', 'Lokale Sitzung.');
  let prompt = '';
  window.confirm = (message) => {
    prompt = message;
    return false;
  };

  await importJson(window, payload);
  assert.match(prompt, /ersetzt die aktuelle lokale Sitzung/);
  assert.equal(window.document.querySelector('#beginning').value, 'Lokale Sitzung.');
  assert.match(window.document.querySelector('#storage-status').textContent, /abgebrochen/);

  window.confirm = () => true;
  await importJson(window, payload);
  assert.equal(window.document.querySelector('#beginning').value, 'Importierte Sitzung.');
  assert.match(window.document.querySelector('#actual-text').textContent, /Importierte Variante/);
  assert.equal(window.document.activeElement, window.document.querySelector('#storage-status'));
  window.happyDOM.abort();
});

test('Import rekonstruiert Wortlautketten und bereinigt ungültige Genealogien', async () => {
  const payload = {
    format: 'anschlusslabor-session',
    schemaVersion: 2,
    versionSequence: 3,
    stepSequence: 99,
    currentVersionId: null,
    workingParentVersionId: null,
    currentReleaseId: 'version-2',
    working: {
      root: 'Geprüfter Ausgang.',
      steps: [
        { id: 'step-40', type: 'fortsetzen', text: 'Erster Anschluss.', previousText: 'Manipulierter Bezug.' },
        { id: 'step-40', type: 'praezisieren', text: 'Zweiter Anschluss.', previousText: 'Noch ein manipulierter Bezug.' }
      ]
    },
    versions: [
      { id: 'version-1', number: 1, root: 'Fassung eins.', steps: [], parentVersionId: 'version-2', releasedAt: null },
      { id: 'version-2', number: 1, root: 'Fassung zwei.', steps: [], parentVersionId: 'version-1', releasedAt: null },
      { id: 'version-3', number: 1, root: 'Fassung drei.', steps: [], parentVersionId: 'version-3', releasedAt: null }
    ]
  };
  const window = createApp();
  await importJson(window, payload);
  const normalized = JSON.parse(window.localStorage.getItem(storageKey));

  assert.equal(normalized.working.steps[0].previousText, 'Geprüfter Ausgang.');
  assert.equal(normalized.working.steps[1].previousText, 'Erster Anschluss.');
  assert.deepEqual(normalized.versions.map((version) => version.number), [1, 2, 3]);
  assert.equal(normalized.currentReleaseId, null);
  assert.equal(normalized.versions.find((version) => version.id === 'version-3').parentVersionId, null);

  const byId = new Map(normalized.versions.map((version) => [version.id, version]));
  normalized.versions.forEach((version) => {
    const visited = new Set([version.id]);
    let cursor = version;
    while (cursor.parentVersionId) {
      assert.equal(visited.has(cursor.parentVersionId), false, 'Versionsgenealogie darf keinen Zyklus enthalten');
      visited.add(cursor.parentVersionId);
      cursor = byId.get(cursor.parentVersionId);
    }
  });
  assert.match(window.document.querySelector('#actual-relation').textContent, /Erster Anschluss/);
  window.happyDOM.abort();
});

test('Verlaufsnummern bleiben beim Einklappen zeitlich korrekt', () => {
  const window = createApp();
  setValue(window, '#beginning', 'Ausgang.');
  for (let index = 1; index <= 7; index += 1) {
    addConnection(window, index % 2 ? 'fortsetzen' : 'variieren', 'Anschluss ' + index + '.');
  }

  const numbers = [...window.document.querySelectorAll('.history-number')].map((element) => element.textContent);
  assert.deepEqual(numbers, ['01', '02', '03', '04', '05', '06', '07', '08']);
  assert.match(window.document.querySelector('.history-fold summary').textContent, /2 frühere Anschlüsse/);
  assert.equal(window.document.activeElement, window.document.querySelector('#observation'));
  window.happyDOM.abort();
});

test('Offene Entwürfe sperren Import und Export und werden als ungesichert ausgewiesen', () => {
  const window = createApp();
  setValue(window, '#beginning', 'Arbeitsausgang.');
  click(window, "[data-move='praezisieren']");
  setValue(window, '#connection-text', 'Noch nicht aktualisierter Entwurf.');

  assert.equal(window.document.querySelector('#export-session').disabled, true);
  assert.equal(window.document.querySelector('#import-session-trigger').disabled, true);
  assert.equal(window.document.querySelector('#draft-status').hidden, false);
  assert.match(window.document.querySelector('#draft-status').textContent, /nicht aktualisierte/);
  assert.doesNotMatch(window.localStorage.getItem(storageKey), /Noch nicht aktualisierter Entwurf/);

  click(window, '#cancel-move');
  assert.equal(window.document.querySelector('#export-session').disabled, false);
  addConnection(window, 'fortsetzen', 'Festgehaltener Anschluss.');
  click(window, '#edit-beginning');
  setValue(window, '#beginning', 'Noch nicht bestätigte Änderung.');
  assert.equal(window.document.querySelector('#export-session').disabled, true);
  assert.match(window.document.querySelector('#draft-status').textContent, /noch nicht bestätigte Änderung/);

  setValue(window, '#beginning', 'x'.repeat(251));
  assert.equal(window.document.querySelector('#char-warning').textContent, 'Das Zeichenlimit ist fast erreicht.');
  window.happyDOM.abort();
});

test('KI-Vorschläge bleiben bis zur ausdrücklichen Aktualisierung flüchtig', async () => {
  const window = createApp();
  let request;
  window.fetch = async (url, options) => {
    request = { url, options };
    return new window.Response(JSON.stringify({
      suggestion: '<img onerror="window.compromised=true"> Eine vorgeschlagene Fortsetzung.',
      explanation: 'Der Wortlaut könnte die gesetzte Linie weiterführen.'
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  };

  setValue(window, '#beginning', 'Eine bedingte Ausgangsäußerung.');
  click(window, "[data-move='fortsetzen']");
  const storedBeforeRequest = window.localStorage.getItem(storageKey);
  click(window, '#ai-suggest');
  await window.happyDOM.waitUntilComplete();

  const payload = JSON.parse(request.options.body);
  assert.equal(request.url, '/api/anschluss');
  assert.deepEqual(payload, {
    move: 'fortsetzen',
    previousText: 'Eine bedingte Ausgangsäußerung.'
  });
  assert.deepEqual(Object.keys(payload).sort(), ['move', 'previousText']);
  assert.equal(window.document.querySelector('#ai-result').hidden, false);
  assert.equal(window.document.querySelector('#ai-suggestion img'), null);
  assert.match(window.document.querySelector('#ai-suggestion').textContent, /<img onerror/);
  assert.equal(window.localStorage.getItem(storageKey), storedBeforeRequest);
  const reloadedWindow = createApp(storedBeforeRequest);
  assert.equal(reloadedWindow.document.querySelector('#ai-result').hidden, true);
  assert.equal(reloadedWindow.document.querySelector('#ai-status').textContent, '');
  reloadedWindow.happyDOM.abort();

  click(window, '#ai-adopt');
  assert.match(window.document.querySelector('#connection-text').value, /vorgeschlagene Fortsetzung/);
  assert.equal(window.localStorage.getItem(storageKey), storedBeforeRequest);

  click(window, '#commit-move');
  assert.match(window.localStorage.getItem(storageKey), /vorgeschlagene Fortsetzung/);
  assert.equal(window.document.activeElement, window.document.querySelector('#observation'));
  window.happyDOM.abort();
});

test('Veraltete oder nicht verfügbare KI-Antworten verändern den manuellen Entwurf nicht', async () => {
  const window = createApp();
  let resolveRequest;
  window.fetch = () => new Promise((resolve) => {
    resolveRequest = resolve;
  });

  setValue(window, '#beginning', 'Ausgang für einen flüchtigen Vorschlag.');
  click(window, "[data-move='fortsetzen']");
  click(window, '#ai-suggest');
  assert.equal(window.document.querySelector('#ai-assistant').getAttribute('aria-busy'), 'true');

  click(window, "[data-move='variieren']");
  resolveRequest(new window.Response(JSON.stringify({
    suggestion: 'Veralteter Vorschlag.',
    explanation: 'Nicht mehr einschlägig.'
  }), { status: 200, headers: { 'Content-Type': 'application/json' } }));
  await window.happyDOM.waitUntilComplete();

  assert.equal(window.document.querySelector('#ai-result').hidden, true);
  assert.equal(window.document.querySelector('#connection-text').value, '');
  assert.doesNotMatch(window.localStorage.getItem(storageKey), /Veralteter Vorschlag/);

  window.fetch = async () => new window.Response(JSON.stringify({
    error: 'Die KI-Vorschlagsfunktion ist auf diesem Server nicht eingerichtet.'
  }), { status: 503, headers: { 'Content-Type': 'application/json' } });
  click(window, '#ai-suggest');
  await window.happyDOM.waitUntilComplete();
  assert.match(window.document.querySelector('#ai-status').textContent, /nicht eingerichtet/);

  setValue(window, '#connection-text', 'Der manuelle Weg bleibt verfügbar.');
  click(window, '#commit-move');
  assert.match(window.localStorage.getItem(storageKey), /manuelle Weg bleibt verfügbar/);
  window.happyDOM.abort();
});

test('Nicht erreichbarer KI-Endpunkt wird als Konfigurationsgrenze erklärt', async () => {
  const window = createApp();
  window.fetch = async () => {
    throw new window.TypeError('Failed to fetch');
  };

  setValue(window, '#beginning', 'Ein Ausgang für eine nicht erreichbare KI-Funktion.');
  click(window, "[data-move='fortsetzen']");
  click(window, '#ai-suggest');
  await window.happyDOM.waitUntilComplete();

  assert.match(window.document.querySelector('#ai-status').textContent, /KI-Endpunkt/);
  assert.match(window.document.querySelector('#ai-status').textContent, /Worker oder Projektserver/);
  assert.match(window.document.querySelector('#ai-status').textContent, /manuelle Entwurf verfügbar/);
  assert.equal(window.document.querySelector('#connection-text').value, '');
  window.happyDOM.abort();
});

test('Eine asynchrone KI-Antwort unterbricht das manuelle Schreiben nicht', async () => {
  const window = createApp();
  let resolveRequest;
  window.fetch = () => new Promise((resolve) => {
    resolveRequest = resolve;
  });

  setValue(window, '#beginning', 'Ein Bezug für paralleles Schreiben.');
  click(window, "[data-move='praezisieren']");
  click(window, '#ai-suggest');
  const draft = setValue(window, '#connection-text', 'Ein bereits begonnener manueller Entwurf.');
  draft.focus();

  resolveRequest(new window.Response(JSON.stringify({
    suggestion: 'Ein ergänzender Vorschlag.',
    explanation: 'Er könnte die gewählte Unterscheidung genauer bestimmen.'
  }), { status: 200, headers: { 'Content-Type': 'application/json' } }));
  await window.happyDOM.waitUntilComplete();

  assert.equal(window.document.activeElement, draft);
  assert.equal(draft.value, 'Ein bereits begonnener manueller Entwurf.');
  assert.equal(window.document.querySelector('#ai-result').hidden, false);
  window.happyDOM.abort();
});


test('Philosophie-Automat visualisiert Vorschlag, Draft und Autorentscheidung getrennt', () => {
  const window = createApp();
  assert.match(window.document.querySelector('#automaton-copy').textContent, /keine Theorieentscheidung/);
  assert.equal(window.document.querySelector("[data-automaton-step='decision']").classList.contains('is-locked'), true);

  setValue(window, '#beginning', 'Ein Algorithmus ordnet bedingte Übergänge.');
  assert.match(window.document.querySelector('#automaton-status').textContent, /Begriffsprüfung/);
  assert.match(window.document.querySelector('#automaton-concepts').textContent, /Algorithmus/);
  assert.equal(window.document.querySelector("[data-automaton-step='draft']").classList.contains('is-active'), false);

  addConnection(window, 'praezisieren', 'Die Unterscheidung betrifft die wiederholbare Ordnung der Übergänge.');
  assert.match(window.document.querySelector('#automaton-status').textContent, /Draft vorprüfbar/);
  assert.match(window.document.querySelector('#automaton-draft').textContent, /markierter Vorschlag/);
  assert.match(window.document.querySelector('#automaton-event').textContent, /Change-Event/);
  assert.match(window.document.querySelector('#automaton-validation').textContent, /formal vorprüfbar/);
  assert.match(window.document.querySelector('#automaton-gate').textContent, /nicht bestätigt/);
  assert.match(window.document.querySelector('#automaton-decision').textContent, /Autor/);
  window.happyDOM.abort();
});
