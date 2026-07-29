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

test('Eingaben und Operationswahl besitzen die angekündigten zugänglichen Zustände', () => {
  const window = createApp();
  const beginning = window.document.querySelector('#beginning');
  const counter = window.document.querySelector('#char-count');
  const moveButton = window.document.querySelector("[data-move='fortsetzen']");

  assert.equal(beginning.getAttribute('aria-describedby'), 'beginning-help char-count');
  assert.equal(counter.getAttribute('aria-live'), 'polite');
  assert.equal(moveButton.getAttribute('aria-pressed'), 'false');
  assert.equal(window.document.querySelector('#import-session-trigger').tagName, 'BUTTON');

  setValue(window, '#beginning', 'Zugänglicher Ausgang.');
  moveButton.click();
  assert.equal(moveButton.getAttribute('aria-pressed'), 'true');
  assert.equal(window.document.querySelector('#connection-text').getAttribute('aria-describedby'), 'move-prompt connection-count');
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
  assert.match(window.document.querySelector('#history').textContent, /Fortsetzen/);
  assert.match(window.document.querySelector('#history').textContent, /Daraus folgt/);
  assert.equal(window.document.querySelector('#beginning').disabled, true);
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
