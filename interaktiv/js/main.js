const input = document.querySelector('#beginning');
const observation = document.querySelector('#observation');
const moves = document.querySelector('#moves');
const moveButtons = [...document.querySelectorAll('[data-move]')];
const resetButton = document.querySelector('#reset');
const characterCount = document.querySelector('#char-count');
const actualText = document.querySelector('#actual-text');
const conditions = document.querySelector('#conditions');
const possibilities = document.querySelector('#possibilities');
const history = document.querySelector('#history');
const iterationCount = document.querySelector('#iteration-count');
const stabilizeButton = document.querySelector('#stabilize');
const releaseButton = document.querySelector('#release');
const stabilizationStatus = document.querySelector('#stabilization-status');
const versionsList = document.querySelector('#versions');
const versionCount = document.querySelector('#version-count');

const baseConditions = ['Alphabet', 'Sprache', 'Interface', 'Erwartung'];
const emptyPossibilities = [
  'eine erste Äußerung setzen',
  'den erwarteten Zusammenhang aufnehmen',
  'den Anfang verweigern'
];
const initialPossibilities = [
  'die Aussage fortführen',
  'einen Begriff präzisieren',
  'eine Voraussetzung unterbrechen'
];

const moveDefinitions = {
  fortsetzen: {
    key: 'fortsetzen',
    label: 'Fortsetzen',
    actual: 'Der gesetzte Bezug wird weitergeführt.',
    condition: 'gebildete Erwartung',
    history: 'Bezug fortgesetzt',
    possibilities: [
      'eine Folgerung anschließen',
      'ein Beispiel ergänzen',
      'den Bezug später wiederaufnehmen'
    ],
    observation: 'Die Fortsetzung nimmt den gesetzten Zusammenhang auf. Dadurch werden Folgerung, Beispiel und Wiederaufnahme leichter anschließbar; ein unvermittelter Themenwechsel tritt zurück.'
  },
  praezisieren: {
    key: 'praezisieren',
    label: 'Präzisieren',
    actual: 'Eine Unterscheidung wird bestimmter gefasst.',
    condition: 'geschärfte Unterscheidung',
    history: 'Unterscheidung präzisiert',
    possibilities: [
      'den Geltungsbereich eingrenzen',
      'eine Bedingung ausdrücklich benennen',
      'einen Grenzfall prüfen'
    ],
    observation: 'Die Präzisierung macht nicht einfach mehr Möglichkeiten verfügbar. Sie gliedert den Raum weiterer Anschlussmöglichkeiten neu: Manche Fortsetzungen werden bestimmter, andere passen nicht mehr zur gesetzten Unterscheidung.'
  },
  unterbrechen: {
    key: 'unterbrechen',
    label: 'Unterbrechen',
    actual: 'Die erwartete Fortsetzung wird ausgesetzt.',
    condition: 'sichtbar gewordene Voraussetzung',
    history: 'Fortsetzung unterbrochen',
    possibilities: [
      'eine Voraussetzung prüfen',
      'die Frage neu fassen',
      'den bisherigen Anschluss verwerfen'
    ],
    observation: 'Die Unterbrechung hebt den Zusammenhang nicht auf. Sie macht eine Bedingung bemerkbar, die in der ungestörten Fortsetzung mitwirkte, und eröffnet dadurch andere Fragen.'
  },
  variieren: {
    key: 'variieren',
    label: 'Variieren',
    actual: 'Perspektive oder Gewichtung wird verschoben.',
    condition: 'veränderte Gewichtung',
    history: 'Anschluss variiert',
    possibilities: [
      'die Reihenfolge verändern',
      'eine andere Perspektive aufnehmen',
      'die Variante mit der vorherigen Fassung vergleichen'
    ],
    observation: 'Die Variation hält einen Bezug fest und verändert zugleich seine Form. Erst der Vergleich zeigt, welche Beziehungen durch die neue Gewichtung hervortreten oder zurücktreten.'
  }
};

let selectedMoves = [];
let versions = [];
let versionSequence = 0;

function renderList(element, entries, className) {
  element.replaceChildren();
  entries.forEach((entry) => {
    const item = document.createElement('li');
    item.textContent = entry;
    if (className) {
      item.className = className;
    }
    element.append(item);
  });
}

function excerpt(value) {
  const compact = value.replace(/\s+/g, ' ').trim();
  if (compact.length <= 94) {
    return compact;
  }
  return compact.slice(0, 91) + '…';
}

function currentSignature() {
  return JSON.stringify({
    input: input.value.trim(),
    moves: selectedMoves.map((move) => move.key)
  });
}

function latestVersion() {
  return versions.at(-1);
}

function renderConditions() {
  const dynamicConditions = selectedMoves.map((move) => move.condition);
  const latest = latestVersion();

  if (latest?.released && latest.signature === currentSignature()) {
    dynamicConditions.push('freigegebene Fassung');
  }

  const uniqueConditions = [...new Set(dynamicConditions)].slice(-4);
  renderList(conditions, baseConditions);
  uniqueConditions.forEach((entry) => {
    const item = document.createElement('li');
    item.className = 'dynamic-condition';
    item.textContent = entry;
    conditions.append(item);
  });
}

function renderHistory(hasInput) {
  history.replaceChildren();

  if (!hasInput) {
    const emptyItem = document.createElement('li');
    emptyItem.className = 'empty-history';
    emptyItem.textContent = 'Noch kein weiterer Vollzug';
    history.append(emptyItem);
    iterationCount.textContent = '0 Aktualisierungen';
    return;
  }

  const initialItem = document.createElement('li');
  initialItem.textContent = 'Äußerung gesetzt';
  history.append(initialItem);

  selectedMoves.forEach((move) => {
    const item = document.createElement('li');
    item.textContent = move.history;
    history.append(item);
  });

  const count = selectedMoves.length + 1;
  iterationCount.textContent = count + (count === 1 ? ' Aktualisierung' : ' Aktualisierungen');
}

function clearMoveSelection() {
  selectedMoves = [];
  moveButtons.forEach((button) => button.classList.remove('is-active'));
}

function renderVersions() {
  versionsList.replaceChildren();

  if (versions.length === 0) {
    const emptyItem = document.createElement('li');
    emptyItem.className = 'empty-version';
    emptyItem.textContent = 'Noch keine Fassung festgehalten';
    versionsList.append(emptyItem);
    versionCount.textContent = '0 Fassungen';
    return;
  }

  [...versions].reverse().forEach((version) => {
    const item = document.createElement('li');
    item.className = 'version-item';
    item.classList.toggle('is-released', version.released);

    const meta = document.createElement('div');
    meta.className = 'version-meta';

    const title = document.createElement('strong');
    title.textContent = 'Fassung ' + String(version.number).padStart(2, '0');

    const state = document.createElement('span');
    state.textContent = version.released ? 'freigegeben' : 'festgehalten';

    meta.append(title, state);

    const text = document.createElement('p');
    text.className = 'version-text';
    text.textContent = '„' + excerpt(version.input) + '“';

    const movesText = document.createElement('p');
    movesText.className = 'version-moves';
    const count = version.moveKeys.length + 1;
    const path = version.moveKeys.length
      ? version.moveKeys.map((key) => moveDefinitions[key].label).join(' → ')
      : 'Ausgangsäußerung';
    movesText.textContent = count + (count === 1 ? ' Aktualisierung · ' : ' Aktualisierungen · ') + path;

    const restore = document.createElement('button');
    restore.className = 'version-action';
    restore.type = 'button';
    restore.dataset.version = String(version.number);
    restore.textContent = 'Fassung wiederaufnehmen';
    restore.addEventListener('click', restoreVersion);

    item.append(meta, text, movesText, restore);
    versionsList.append(item);
  });

  versionCount.textContent = versions.length + (versions.length === 1 ? ' Fassung' : ' Fassungen');
}

function renderStabilization() {
  const hasInput = input.value.trim().length > 0;
  const latest = latestVersion();
  const matchesLatest = latest?.signature === currentSignature();

  stabilizeButton.disabled = !hasInput || Boolean(matchesLatest);
  releaseButton.disabled = !latest || latest.released;

  if (!latest) {
    stabilizationStatus.textContent = hasInput
      ? 'Die aktuelle Form wirkt bereits auf weitere Anschlüsse, ist aber noch nicht als Fassung festgehalten.'
      : 'Noch besteht keine stabilisierte Fassung.';
  } else if (matchesLatest) {
    const label = 'Fassung ' + String(latest.number).padStart(2, '0');
    stabilizationStatus.textContent = latest.released
      ? label + ' ist festgehalten und vorläufig als maßgeblicher Stand freigegeben.'
      : label + ' hält den aktuellen Stand fest. Weitere Aktualisierungen bleiben möglich.';
  } else {
    stabilizationStatus.textContent = 'Die aktuelle Form weicht von Fassung '
      + String(latest.number).padStart(2, '0')
      + ' ab. Die frühere Fassung bleibt dennoch wiederaufnehmbar.';
  }

  renderVersions();
}

function renderInputState(message) {
  const value = input.value.trim();
  const hasInput = value.length > 0;
  const lastMove = selectedMoves.at(-1);

  characterCount.textContent = input.value.length + ' von 280 Zeichen';
  document.body.classList.toggle('has-input', hasInput);
  moves.disabled = !hasInput;

  if (!hasInput) {
    actualText.textContent = 'Noch keine eigene Äußerung';
    renderList(possibilities, emptyPossibilities);
  } else if (lastMove) {
    actualText.textContent = lastMove.label + ': ' + lastMove.actual;
    renderList(possibilities, lastMove.possibilities);
  } else {
    actualText.textContent = '„' + excerpt(value) + '“';
    renderList(possibilities, initialPossibilities);
  }

  renderConditions();
  renderHistory(hasInput);

  observation.textContent = message || (hasInput
    ? 'Mit der Äußerung wurde eine Möglichkeit aktualisiert. Ihr Wortlaut ist nun selbst eine Bedingung dafür, was als passende Fortsetzung, Präzisierung, Unterbrechung oder Variation erscheint.'
    : 'Noch wurde kein eigener Anschluss aktualisiert. Alphabet, Sprache, Interface und die Erwartung einer Fortsetzung wirken dennoch bereits als Bedingungen.');

  renderStabilization();
}

function applyMove(event) {
  const button = event.currentTarget;
  const definition = moveDefinitions[button.dataset.move];

  moveButtons.forEach((candidate) => candidate.classList.toggle('is-active', candidate === button));
  selectedMoves.push(definition);
  renderInputState(definition.observation);
}

function stabilizeCurrent() {
  const value = input.value.trim();

  if (!value) {
    return;
  }

  versionSequence += 1;
  const version = {
    number: versionSequence,
    input: value,
    moveKeys: selectedMoves.map((move) => move.key),
    signature: currentSignature(),
    released: false
  };

  versions.push(version);
  renderInputState('Fassung '
    + String(version.number).padStart(2, '0')
    + ' hält den erreichten Zusammenhang fest. Seine Dauer beruht nun auf einer wiederaufnehmbaren Bezeichnung und Version.');
}

function releaseLatestVersion() {
  const latest = latestVersion();

  if (!latest) {
    return;
  }

  latest.released = true;
  renderInputState('Die Freigabe behandelt Fassung '
    + String(latest.number).padStart(2, '0')
    + ' vorläufig als maßgeblich. Sie beweist weder Vollkommenheit noch Rechtfertigung.');
}

function restoreVersion(event) {
  const number = Number(event.currentTarget.dataset.version);
  const version = versions.find((candidate) => candidate.number === number);

  if (!version) {
    return;
  }

  input.value = version.input;
  selectedMoves = version.moveKeys.map((key) => moveDefinitions[key]);
  const activeKey = selectedMoves.at(-1)?.key;
  moveButtons.forEach((button) => {
    button.classList.toggle('is-active', button.dataset.move === activeKey);
  });
  renderInputState('Fassung '
    + String(version.number).padStart(2, '0')
    + ' wurde wiederaufgenommen. Stabilisierung erhält einen Stand, ohne spätere Aktualisierung auszuschließen.');
}

input.addEventListener('input', () => {
  clearMoveSelection();
  renderInputState();
});

moveButtons.forEach((button) => button.addEventListener('click', applyMove));
stabilizeButton.addEventListener('click', stabilizeCurrent);
releaseButton.addEventListener('click', releaseLatestVersion);

resetButton.addEventListener('click', () => {
  input.value = '';
  clearMoveSelection();
  versions = [];
  versionSequence = 0;
  renderInputState();
  input.focus();
});

renderInputState();
