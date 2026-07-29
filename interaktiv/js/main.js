const input = document.querySelector('#beginning');
const observation = document.querySelector('#observation');
const moves = document.querySelector('#moves');
const moveButtons = [...document.querySelectorAll('[data-move]')];
const editBeginningButton = document.querySelector('#edit-beginning');
const clearCurrentButton = document.querySelector('#clear-current');
const characterCount = document.querySelector('#char-count');
const beginningEditActions = document.querySelector('#beginning-edit-actions');
const acceptBeginningEditButton = document.querySelector('#accept-beginning-edit');
const cancelBeginningEditButton = document.querySelector('#cancel-beginning-edit');
const connectionComposer = document.querySelector('#connection-composer');
const connectionTitle = document.querySelector('#connection-title');
const movePrompt = document.querySelector('#move-prompt');
const connectionInput = document.querySelector('#connection-text');
const connectionCount = document.querySelector('#connection-count');
const commitMoveButton = document.querySelector('#commit-move');
const cancelMoveButton = document.querySelector('#cancel-move');
const actualText = document.querySelector('#actual-text');
const actualRelation = document.querySelector('#actual-relation');
const conditions = document.querySelector('#conditions');
const possibilities = document.querySelector('#possibilities');
const history = document.querySelector('#history');
const iterationCount = document.querySelector('#iteration-count');
const stabilizeButton = document.querySelector('#stabilize');
const releaseButton = document.querySelector('#release');
const stabilizationStatus = document.querySelector('#stabilization-status');
const versionsList = document.querySelector('#versions');
const versionCount = document.querySelector('#version-count');
const storageStatus = document.querySelector('#storage-status');
const exportSessionButton = document.querySelector('#export-session');
const importSessionButton = document.querySelector('#import-session-trigger');
const importSessionInput = document.querySelector('#import-session');
const clearSessionButton = document.querySelector('#clear-session');

const STORAGE_KEY = 'anschlusslabor.session.v2';
const SESSION_FORMAT = 'anschlusslabor-session';
const SCHEMA_VERSION = 2;
const MAX_STEPS = 50;
const MAX_VERSIONS = 40;
const HISTORY_PREVIEW_LENGTH = 6;

const baseConditions = ['Alphabet', 'Sprache', 'Interface', 'Erwartung'];
const emptyPossibilities = [
  'eine erste Äußerung setzen',
  'den erwarteten Zusammenhang aufnehmen',
  'den Anfang verweigern'
];
const initialPossibilities = [
  'den Wortlaut fortsetzen',
  'eine Unterscheidung präzisieren',
  'eine Voraussetzung unterbrechen',
  'Perspektive oder Gewichtung variieren'
];

const moveDefinitions = {
  fortsetzen: {
    key: 'fortsetzen',
    label: 'Fortsetzen',
    prompt: 'Wie setzt du den vorherigen Wortlaut fort?',
    placeholder: 'Formuliere eine Folgerung, Ergänzung oder Weiterführung.',
    relation: 'Fortsetzung des vorherigen Anschlusses',
    condition: 'gebildete Erwartung',
    possibilities: [
      'eine Folgerung prüfen',
      'ein Beispiel an den neuen Wortlaut anschließen',
      'den fortgesetzten Bezug später wiederaufnehmen'
    ],
    observation: 'Die Fortsetzung übernimmt nicht nur eine Kategorie. Ihr eigener Wortlaut nimmt den vorherigen Anschluss auf und verändert, welche Folgerungen, Beispiele und Einwände nun passen.'
  },
  praezisieren: {
    key: 'praezisieren',
    label: 'Präzisieren',
    prompt: 'Welche Unterscheidung soll genauer bestimmt werden?',
    placeholder: 'Benenne die Unterscheidung und ihren begrenzten Geltungsbereich.',
    relation: 'Präzisierung des vorherigen Anschlusses',
    condition: 'geschärfte Unterscheidung',
    possibilities: [
      'den Geltungsbereich weiter eingrenzen',
      'eine Bedingung ausdrücklich benennen',
      'einen Grenzfall prüfen'
    ],
    observation: 'Die Präzisierung gliedert den Raum weiterer Anschlüsse neu. Ihr Wortlaut macht manche Fortsetzungen bestimmter und lässt andere nicht mehr ohne Weiteres zur gesetzten Unterscheidung passen.'
  },
  unterbrechen: {
    key: 'unterbrechen',
    label: 'Unterbrechen',
    prompt: 'Welche Voraussetzung des vorherigen Anschlusses wird fraglich?',
    placeholder: 'Formuliere die Unterbrechung als konkrete Frage, Zurückweisung oder Zäsur.',
    relation: 'Unterbrechung einer erwarteten Fortsetzung',
    condition: 'sichtbar gewordene Voraussetzung',
    possibilities: [
      'die sichtbar gewordene Voraussetzung prüfen',
      'die Frage unter veränderten Bedingungen neu fassen',
      'eine andere Anschlusslinie beginnen'
    ],
    observation: 'Die Unterbrechung löscht den vorausgehenden Zusammenhang nicht. Der neue Wortlaut macht eine seiner Bedingungen bemerkbar und eröffnet Anschlüsse, die in der ungestörten Fortsetzung zurückgetreten wären.'
  },
  variieren: {
    key: 'variieren',
    label: 'Variieren',
    prompt: 'Wie verändern sich Perspektive oder Gewichtung des vorherigen Anschlusses?',
    placeholder: 'Formuliere eine erkennbare Abweichung innerhalb desselben Bezugs.',
    relation: 'Variation innerhalb eines fortbestehenden Bezugs',
    condition: 'veränderte Gewichtung',
    possibilities: [
      'die Variante mit dem vorherigen Wortlaut vergleichen',
      'eine andere Perspektive ergänzen',
      'bestimmen, welche Beziehung trotz Variation fortbesteht'
    ],
    observation: 'Die Variation hält einen Bezug fest und verändert zugleich seine Form. Weil beide Wortlaute erhalten bleiben, lässt sich prüfen, welche Beziehungen hervortreten, zurücktreten oder abbrechen.'
  }
};

let working = { root: '', steps: [] };
let versions = [];
let versionSequence = 0;
let stepSequence = 0;
let currentVersionId = null;
let workingParentVersionId = null;
let currentReleaseId = null;
let pendingMoveKey = null;
let editingBeginning = false;
let storageMessage = 'Fassungen werden lokal in diesem Browser bewahrt. Sie sind nicht öffentlich und nicht zwischen Geräten synchronisiert.';

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

function excerpt(value, maximum = 112) {
  const compact = String(value || '').replace(/\s+/g, ' ').trim();
  if (compact.length <= maximum) {
    return compact;
  }
  return compact.slice(0, maximum - 1) + '…';
}

function cloneSteps(steps) {
  return steps.map((step) => ({ ...step }));
}

function signatureOf(value) {
  return JSON.stringify({
    root: value.root.trim(),
    steps: value.steps.map((step) => ({ type: step.type, text: step.text.trim() }))
  });
}

function currentSignature() {
  return signatureOf(working);
}

function currentVersion() {
  return versions.find((version) => version.id === currentVersionId) || null;
}

function versionById(id) {
  return versions.find((version) => version.id === id) || null;
}

function isCurrentVersionExact() {
  const version = currentVersion();
  return Boolean(version && signatureOf(version) === currentSignature());
}


function currentWording(value = working) {
  return value.steps.at(-1)?.text || value.root.trim();
}

function versionLabel(version) {
  return 'Fassung ' + String(version.number).padStart(2, '0');
}

function setStorageMessage(message) {
  storageMessage = message;
  storageStatus.textContent = storageMessage;
}

function serializableSession() {
  return {
    format: SESSION_FORMAT,
    schemaVersion: SCHEMA_VERSION,
    versionSequence,
    stepSequence,
    currentVersionId,
    workingParentVersionId,
    currentReleaseId,
    working: {
      root: working.root,
      steps: cloneSteps(working.steps)
    },
    versions: versions.map((version) => ({
      ...version,
      steps: cloneSteps(version.steps)
    }))
  };
}

function persistSession() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(serializableSession()));
    setStorageMessage('Fassungen werden lokal in diesem Browser bewahrt. Sie sind nicht öffentlich und nicht zwischen Geräten synchronisiert.');
  } catch {
    setStorageMessage('Der Browser konnte diese Sitzung nicht lokal bewahren. Exportiere sie als JSON, bevor du die Seite schließt.');
  }
}

function normalizeStep(step, fallbackNumber) {
  if (!step || typeof step !== 'object' || !moveDefinitions[step.type]) {
    return null;
  }

  const text = typeof step.text === 'string' ? step.text.trim().slice(0, 400) : '';
  if (!text) {
    return null;
  }

  const numericId = Number(String(step.id || '').replace(/^step-/, ''));
  const number = Number.isInteger(numericId) && numericId > 0 ? numericId : fallbackNumber;
  return {
    id: 'step-' + number,
    type: step.type,
    text,
    previousText: typeof step.previousText === 'string' ? step.previousText.trim().slice(0, 400) : '',
    createdAt: typeof step.createdAt === 'string' ? step.createdAt : null
  };
}

function normalizeSession(raw) {
  if (!raw || typeof raw !== 'object' || raw.format !== SESSION_FORMAT || raw.schemaVersion !== SCHEMA_VERSION) {
    throw new Error('Unbekanntes Sitzungsformat');
  }

  const normalizedVersions = [];
  const seenIds = new Set();
  const sourceVersions = Array.isArray(raw.versions) ? raw.versions.slice(-MAX_VERSIONS) : [];

  sourceVersions.forEach((version, index) => {
    if (!version || typeof version !== 'object') {
      return;
    }

    const number = Number(version.number);
    const id = typeof version.id === 'string' ? version.id : '';
    const root = typeof version.root === 'string' ? version.root.trim().slice(0, 280) : '';
    if (!Number.isInteger(number) || number < 1 || !/^version-\d+$/.test(id) || seenIds.has(id) || !root) {
      return;
    }

    const steps = (Array.isArray(version.steps) ? version.steps : [])
      .slice(0, MAX_STEPS)
      .map((step, stepIndex) => normalizeStep(step, index * MAX_STEPS + stepIndex + 1))
      .filter(Boolean);

    seenIds.add(id);
    normalizedVersions.push({
      id,
      number,
      root,
      steps,
      parentVersionId: typeof version.parentVersionId === 'string' ? version.parentVersionId : null,
      createdAt: typeof version.createdAt === 'string' ? version.createdAt : null,
      releasedAt: typeof version.releasedAt === 'string' ? version.releasedAt : null
    });
  });

  const normalizedWorkingSteps = (Array.isArray(raw.working?.steps) ? raw.working.steps : [])
    .slice(0, MAX_STEPS)
    .map((step, index) => normalizeStep(step, index + 1))
    .filter(Boolean);
  const normalizedWorkingRoot = typeof raw.working?.root === 'string'
    ? raw.working.root.slice(0, 280)
    : '';
  const validIds = new Set(normalizedVersions.map((version) => version.id));

  normalizedVersions.forEach((version) => {
    if (!validIds.has(version.parentVersionId)) {
      version.parentVersionId = null;
    }
  });

  const maximumVersionNumber = normalizedVersions.reduce((maximum, version) => Math.max(maximum, version.number), 0);
  const maximumStepNumber = [...normalizedWorkingSteps, ...normalizedVersions.flatMap((version) => version.steps)]
    .reduce((maximum, step) => Math.max(maximum, Number(step.id.replace('step-', '')) || 0), 0);

  return {
    working: { root: normalizedWorkingRoot, steps: normalizedWorkingSteps },
    versions: normalizedVersions,
    versionSequence: Math.max(Number(raw.versionSequence) || 0, maximumVersionNumber),
    stepSequence: Math.max(Number(raw.stepSequence) || 0, maximumStepNumber),
    currentVersionId: validIds.has(raw.currentVersionId) ? raw.currentVersionId : null,
    workingParentVersionId: validIds.has(raw.workingParentVersionId) ? raw.workingParentVersionId : null,
    currentReleaseId: validIds.has(raw.currentReleaseId) ? raw.currentReleaseId : null
  };
}

function applyNormalizedSession(session) {
  working = session.working;
  versions = session.versions;
  versionSequence = session.versionSequence;
  stepSequence = session.stepSequence;
  currentVersionId = session.currentVersionId;
  workingParentVersionId = session.workingParentVersionId;
  currentReleaseId = session.currentReleaseId;
  pendingMoveKey = null;
  editingBeginning = false;
}

function loadSession() {
  let stored;
  try {
    stored = localStorage.getItem(STORAGE_KEY);
  } catch {
    storageMessage = 'Der Browser stellt für diese Seite keinen lokalen Speicher bereit. Die Sitzung kann weiterhin als JSON ausgegeben werden.';
    return false;
  }

  if (!stored) {
    return false;
  }

  try {
    applyNormalizedSession(normalizeSession(JSON.parse(stored)));
    storageMessage = 'Die lokal bewahrte Sitzung wurde wiederaufgenommen. Sie ist nicht öffentlich und nicht zwischen Geräten synchronisiert.';
    return true;
  } catch {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch {
      // Der unlesbare Stand kann in diesem Browser nicht entfernt werden.
    }
    storageMessage = 'Ein unlesbarer lokaler Sitzungsstand wurde verworfen. Die Anwendung beginnt mit einer leeren Arbeitsfassung.';
    return false;
  }
}

function renderConditions() {
  const dynamicConditions = working.steps.map((step) => moveDefinitions[step.type].condition);
  if (isCurrentVersionExact()) {
    dynamicConditions.push('wiederaufnehmbare Fassung');
  }
  if (currentReleaseId && currentVersionId === currentReleaseId && isCurrentVersionExact()) {
    dynamicConditions.push('aktuell freigegebene Fassung');
  }

  renderList(conditions, baseConditions);
  [...new Set(dynamicConditions)].slice(-4).forEach((entry) => {
    const item = document.createElement('li');
    item.className = 'dynamic-condition';
    item.textContent = entry;
    conditions.append(item);
  });
}

function createHistoryEntry(entry) {
  const item = document.createElement('li');
  item.className = 'history-entry';

  const meta = document.createElement('span');
  meta.className = 'history-operation';
  meta.textContent = entry.meta;

  const text = document.createElement('p');
  text.textContent = '„' + entry.text + '“';

  item.append(meta, text);
  return item;
}

function renderHistory() {
  history.replaceChildren();
  const root = working.root.trim();

  if (!root) {
    const emptyItem = document.createElement('li');
    emptyItem.className = 'empty-history';
    emptyItem.textContent = 'Noch kein weiterer Vollzug';
    history.append(emptyItem);
    iterationCount.textContent = '0 Aktualisierungen';
    return;
  }

  const entries = [{ meta: 'Ausgangsäußerung', text: root }];
  working.steps.forEach((step) => {
    const definition = moveDefinitions[step.type];
    entries.push({ meta: definition.label + ' · ' + definition.relation, text: step.text });
  });

  if (entries.length > HISTORY_PREVIEW_LENGTH) {
    const hiddenEntries = entries.slice(0, entries.length - HISTORY_PREVIEW_LENGTH);
    const foldItem = document.createElement('li');
    foldItem.className = 'history-fold';
    const details = document.createElement('details');
    const summary = document.createElement('summary');
    summary.textContent = hiddenEntries.length + ' frühere Anschlüsse anzeigen';
    const foldedList = document.createElement('ol');
    foldedList.className = 'folded-history-list';
    hiddenEntries.forEach((entry) => foldedList.append(createHistoryEntry(entry)));
    details.append(summary, foldedList);
    foldItem.append(details);
    history.append(foldItem);
  }

  entries.slice(-HISTORY_PREVIEW_LENGTH).forEach((entry) => history.append(createHistoryEntry(entry)));
  iterationCount.textContent = entries.length + (entries.length === 1 ? ' Aktualisierung' : ' Aktualisierungen');
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
    const isCurrent = currentVersionId === version.id && signatureOf(version) === currentSignature();
    const isCurrentRelease = currentReleaseId === version.id;
    const wasReleased = Boolean(version.releasedAt);
    const item = document.createElement('li');
    item.className = 'version-item';
    item.classList.toggle('is-current-version', isCurrent);
    item.classList.toggle('is-current-release', isCurrentRelease);
    item.classList.toggle('was-released', wasReleased && !isCurrentRelease);

    const details = document.createElement('details');
    details.open = isCurrent || isCurrentRelease;
    const summary = document.createElement('summary');
    summary.className = 'version-summary';

    const title = document.createElement('strong');
    title.textContent = versionLabel(version);
    const state = document.createElement('span');
    if (isCurrentRelease) {
      state.textContent = 'aktuell freigegeben';
    } else if (wasReleased) {
      state.textContent = 'früher freigegeben';
    } else {
      state.textContent = 'festgehalten';
    }
    summary.append(title, state);

    const body = document.createElement('div');
    body.className = 'version-body';
    const text = document.createElement('p');
    text.className = 'version-text';
    text.textContent = '„' + excerpt(currentWording(version)) + '“';

    const path = document.createElement('p');
    path.className = 'version-moves';
    const operationPath = version.steps.length
      ? version.steps.map((step) => moveDefinitions[step.type].label).join(' → ')
      : 'Ausgangsäußerung';
    path.textContent = (version.steps.length + 1) + (version.steps.length === 0 ? ' Aktualisierung · ' : ' Aktualisierungen · ') + operationPath;

    const lineage = document.createElement('p');
    lineage.className = 'version-lineage';
    const parent = versionById(version.parentVersionId);
    lineage.textContent = parent
      ? 'Abzweigung von ' + versionLabel(parent)
      : 'Ausgangsfassung ohne stabilisierte Vorgängerin';

    const restore = document.createElement('button');
    restore.className = 'version-action';
    restore.type = 'button';
    restore.dataset.versionId = version.id;
    restore.disabled = isCurrent;
    restore.textContent = isCurrent ? 'Aktuell bearbeitet' : 'Fassung wiederaufnehmen';
    restore.addEventListener('click', restoreVersion);

    body.append(text, path, lineage, restore);
    details.append(summary, body);
    item.append(details);
    versionsList.append(item);
  });

  versionCount.textContent = versions.length + (versions.length === 1 ? ' Fassung' : ' Fassungen');
}

function renderStabilization() {
  const root = working.root.trim();
  const exactCurrentVersion = isCurrentVersionExact();
  const current = currentVersion();
  const atVersionLimit = versions.length >= MAX_VERSIONS;

  stabilizeButton.disabled = !root || editingBeginning || Boolean(pendingMoveKey) || exactCurrentVersion || atVersionLimit;
  releaseButton.disabled = !exactCurrentVersion || currentReleaseId === currentVersionId;
  releaseButton.textContent = exactCurrentVersion
    ? versionLabel(current) + ' freigeben'
    : 'Aktuelle Fassung freigeben';

  if (atVersionLimit && !exactCurrentVersion) {
    stabilizationStatus.textContent = 'Das lokale Limit von ' + MAX_VERSIONS + ' Fassungen ist erreicht. Exportiere die Sitzung, bevor du sie löschst oder neu beginnst.';
  } else if (!versions.length && !root) {
    stabilizationStatus.textContent = 'Noch besteht keine stabilisierte Fassung.';
  } else if (!versions.length) {
    stabilizationStatus.textContent = 'Die aktuelle Form wirkt bereits auf weitere Anschlüsse, ist aber noch nicht als Fassung festgehalten.';
  } else if (exactCurrentVersion) {
    if (currentReleaseId === currentVersionId) {
      stabilizationStatus.textContent = versionLabel(current) + ' wird aktuell bearbeitet und ist vorläufig als maßgeblicher Stand freigegeben.';
    } else if (current.releasedAt) {
      stabilizationStatus.textContent = versionLabel(current) + ' wird aktuell bearbeitet und war früher freigegeben. Sie kann erneut zum maßgeblichen Stand werden.';
    } else {
      stabilizationStatus.textContent = versionLabel(current) + ' wird aktuell bearbeitet und ist wiederaufnehmbar. Sie ist nicht freigegeben.';
    }
  } else if (workingParentVersionId && versionById(workingParentVersionId)) {
    stabilizationStatus.textContent = 'Die Arbeitsfassung zweigt von ' + versionLabel(versionById(workingParentVersionId)) + ' ab. Erst Festhalten gibt dem veränderten Stand eine eigene Versionsidentität.';
  } else {
    const released = versionById(currentReleaseId);
    stabilizationStatus.textContent = released
      ? 'Die Arbeitsfassung ist noch nicht festgehalten. ' + versionLabel(released) + ' bleibt der aktuell freigegebene Stand.'
      : 'Die Arbeitsfassung ist noch nicht festgehalten; frühere Fassungen bleiben wiederaufnehmbar.';
  }

  renderVersions();
}

function renderInputControls() {
  const root = working.root.trim();
  const hasSteps = working.steps.length > 0;

  characterCount.textContent = input.value.length + ' von 280 Zeichen';
  input.disabled = hasSteps && !editingBeginning;
  editBeginningButton.hidden = !hasSteps || editingBeginning;
  beginningEditActions.hidden = !editingBeginning;
  acceptBeginningEditButton.disabled = !input.value.trim();
  clearCurrentButton.disabled = !root && !input.value.trim();

  moves.disabled = !root || editingBeginning || working.steps.length >= MAX_STEPS;
  moveButtons.forEach((button) => {
    const selected = button.dataset.move === pendingMoveKey;
    button.classList.toggle('is-selected', selected);
    button.setAttribute('aria-pressed', String(selected));
  });

  connectionComposer.hidden = !pendingMoveKey;
  if (pendingMoveKey) {
    const definition = moveDefinitions[pendingMoveKey];
    connectionTitle.textContent = definition.label + ': Formuliere den nächsten Vollzug';
    movePrompt.textContent = definition.prompt;
    connectionInput.placeholder = definition.placeholder;
  }
  connectionCount.textContent = connectionInput.value.length + ' von 400 Zeichen';
  commitMoveButton.disabled = !connectionInput.value.trim() || working.steps.length >= MAX_STEPS;
}

function renderProcess(message) {
  const root = working.root.trim();
  const hasInput = Boolean(root);
  const lastStep = working.steps.at(-1);
  const wording = currentWording();

  document.body.classList.toggle('has-input', hasInput);

  if (!hasInput) {
    actualRelation.textContent = 'Noch keine relationale Bestimmung';
    actualText.textContent = 'Noch keine eigene Äußerung';
    renderList(possibilities, emptyPossibilities);
  } else if (lastStep) {
    const definition = moveDefinitions[lastStep.type];
    actualRelation.textContent = definition.label + ' · Bezug auf „' + excerpt(lastStep.previousText, 64) + '“';
    actualText.textContent = '„' + wording + '“';
    renderList(possibilities, definition.possibilities);
  } else {
    actualRelation.textContent = 'Ausgangsäußerung';
    actualText.textContent = '„' + root + '“';
    renderList(possibilities, initialPossibilities);
  }

  renderConditions();
  renderHistory();

  const defaultObservation = lastStep
    ? moveDefinitions[lastStep.type].observation
    : hasInput
      ? 'Mit der Äußerung wurde eine Möglichkeit aktualisiert. Ihr Wortlaut ist nun selbst eine Bedingung dafür, was als passende Fortsetzung, Präzisierung, Unterbrechung oder Variation erscheint.'
      : 'Noch wurde kein eigener Anschluss aktualisiert. Alphabet, Sprache, Interface und die Erwartung einer Fortsetzung wirken dennoch bereits als Bedingungen.';
  observation.textContent = message || defaultObservation;
}

function renderAll(message) {
  renderInputControls();
  renderProcess(message);
  renderStabilization();
  storageStatus.textContent = storageMessage;
}

function selectMove(event) {
  pendingMoveKey = event.currentTarget.dataset.move;
  connectionInput.value = '';
  renderInputControls();
  connectionInput.focus();
}

function cancelMove() {
  pendingMoveKey = null;
  connectionInput.value = '';
  renderInputControls();
  moveButtons[0]?.focus();
}

function commitMove() {
  const definition = moveDefinitions[pendingMoveKey];
  const text = connectionInput.value.trim();
  if (!definition || !text || working.steps.length >= MAX_STEPS) {
    return;
  }

  if (isCurrentVersionExact()) {
    workingParentVersionId = currentVersionId;
  }
  currentVersionId = null;
  stepSequence += 1;
  working.steps.push({
    id: 'step-' + stepSequence,
    type: definition.key,
    text,
    previousText: currentWording(),
    createdAt: new Date().toISOString()
  });
  pendingMoveKey = null;
  connectionInput.value = '';
  input.disabled = true;
  persistSession();
  renderAll(definition.observation);
}

function beginBeginningEdit() {
  editingBeginning = true;
  pendingMoveKey = null;
  connectionInput.value = '';
  input.disabled = false;
  renderInputControls();
  input.focus();
  input.setSelectionRange(input.value.length, input.value.length);
}

function acceptBeginningEdit() {
  const root = input.value.trim();
  if (!root) {
    return;
  }

  if (isCurrentVersionExact()) {
    workingParentVersionId = currentVersionId;
  }
  working = { root, steps: [] };
  currentVersionId = null;
  editingBeginning = false;
  persistSession();
  renderAll('Die geänderte Ausgangsäußerung bildet eine neue Arbeitsfassung. Die frühere Anschlussfolge wurde nicht stillschweigend umgeschrieben und bleibt in stabilisierten Fassungen erhalten.');
}

function cancelBeginningEdit() {
  input.value = working.root;
  editingBeginning = false;
  renderAll('Die Änderung der Ausgangsäußerung wurde verworfen. Die bisherige Anschlussfolge bleibt unverändert.');
}

function stabilizeCurrent() {
  const root = working.root.trim();
  if (!root || pendingMoveKey || isCurrentVersionExact() || versions.length >= MAX_VERSIONS) {
    return;
  }

  versionSequence += 1;
  const parentVersionId = versionById(workingParentVersionId) ? workingParentVersionId : null;
  const version = {
    id: 'version-' + versionSequence,
    number: versionSequence,
    root,
    steps: cloneSteps(working.steps),
    parentVersionId,
    createdAt: new Date().toISOString(),
    releasedAt: null
  };

  versions.push(version);
  currentVersionId = version.id;
  workingParentVersionId = version.id;
  persistSession();
  renderAll(versionLabel(version) + ' hält den erreichten Zusammenhang fest. Die Abstammung von einer früheren Fassung bleibt kenntlich.');
}

function releaseCurrentVersion() {
  const version = currentVersion();
  if (!version || !isCurrentVersionExact() || currentReleaseId === version.id) {
    return;
  }

  version.releasedAt = new Date().toISOString();
  currentReleaseId = version.id;
  persistSession();
  renderAll('Die Freigabe behandelt ' + versionLabel(version) + ' vorläufig als maßgeblich. Eine frühere Freigabe bleibt als historischer Status sichtbar, ist aber nicht mehr der aktuelle Stand.');
}

function restoreVersion(event) {
  const version = versionById(event.currentTarget.dataset.versionId);
  if (!version) {
    return;
  }

  working = {
    root: version.root,
    steps: cloneSteps(version.steps)
  };
  currentVersionId = version.id;
  workingParentVersionId = version.id;
  pendingMoveKey = null;
  editingBeginning = false;
  input.value = working.root;
  connectionInput.value = '';
  persistSession();
  renderAll(versionLabel(version) + ' wurde als aktuell bearbeitete Fassung wiederaufgenommen. Freigeben betrifft nun genau diese sichtbare Version.');
}

function clearCurrent() {
  working = { root: '', steps: [] };
  currentVersionId = null;
  workingParentVersionId = null;
  pendingMoveKey = null;
  editingBeginning = false;
  input.value = '';
  connectionInput.value = '';
  persistSession();
  renderAll('Die aktuelle Eingabe wurde geleert. Festgehaltene Fassungen und der aktuelle Freigabestatus bleiben erhalten.');
  input.focus();
}

function clearEntireSession() {
  const hasState = Boolean(working.root.trim() || versions.length);
  if (hasState && !window.confirm('Gesamte Sitzung einschließlich aller Fassungen und Freigaben löschen? Diese Handlung kann nur über einen vorherigen JSON-Export rückgängig gemacht werden.')) {
    return;
  }

  working = { root: '', steps: [] };
  versions = [];
  versionSequence = 0;
  stepSequence = 0;
  currentVersionId = null;
  workingParentVersionId = null;
  currentReleaseId = null;
  pendingMoveKey = null;
  editingBeginning = false;
  input.value = '';
  connectionInput.value = '';
  try {
    localStorage.removeItem(STORAGE_KEY);
    storageMessage = 'Die gesamte lokale Sitzung wurde gelöscht.';
  } catch {
    storageMessage = 'Die Arbeitsoberfläche wurde geleert; der Browser verweigerte jedoch den Zugriff auf seinen lokalen Speicher.';
  }
  renderAll('Die gesamte Sitzung einschließlich aller Fassungen und Freigaben wurde gelöscht.');
  input.focus();
}

function exportSession() {
  const json = JSON.stringify(serializableSession(), null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const download = document.createElement('a');
  const date = new Date().toISOString().slice(0, 10);
  download.href = url;
  download.download = 'anschlusslabor-sitzung-' + date + '.json';
  document.body.append(download);
  download.click();
  download.remove();
  URL.revokeObjectURL(url);
  setStorageMessage('Die Sitzung wurde als JSON ausgegeben. Diese Datei ist ein weiterer materieller Träger des festgehaltenen Stands.');
}

async function importSession(event) {
  const file = event.target.files?.[0];
  if (!file) {
    return;
  }

  try {
    if (file.size > 1_000_000) {
      throw new Error('Datei zu groß');
    }
    const imported = normalizeSession(JSON.parse(await file.text()));
    applyNormalizedSession(imported);
    input.value = working.root;
    connectionInput.value = '';
    persistSession();
    storageMessage = 'Die JSON-Sitzung wurde als lokaler Arbeitsstand wiederaufgenommen.';
    renderAll('Die importierte Sitzung ist wieder anschlussfähig. Ihre Fassungen, Abstammungen und Freigabegeschichte wurden übernommen.');
  } catch {
    setStorageMessage('Die ausgewählte Datei konnte nicht als gültige Anschlusslabor-Sitzung gelesen werden. Der bestehende Stand blieb unverändert.');
  } finally {
    event.target.value = '';
  }
}

input.addEventListener('input', () => {
  characterCount.textContent = input.value.length + ' von 280 Zeichen';
  acceptBeginningEditButton.disabled = !input.value.trim();

  if (editingBeginning) {
    return;
  }

  if (isCurrentVersionExact()) {
    workingParentVersionId = currentVersionId;
  }
  working.root = input.value;
  currentVersionId = null;
  persistSession();
  renderAll();
});

connectionInput.addEventListener('input', () => {
  connectionCount.textContent = connectionInput.value.length + ' von 400 Zeichen';
  commitMoveButton.disabled = !connectionInput.value.trim() || working.steps.length >= MAX_STEPS;
});

moveButtons.forEach((button) => button.addEventListener('click', selectMove));
editBeginningButton.addEventListener('click', beginBeginningEdit);
acceptBeginningEditButton.addEventListener('click', acceptBeginningEdit);
cancelBeginningEditButton.addEventListener('click', cancelBeginningEdit);
clearCurrentButton.addEventListener('click', clearCurrent);
commitMoveButton.addEventListener('click', commitMove);
cancelMoveButton.addEventListener('click', cancelMove);
stabilizeButton.addEventListener('click', stabilizeCurrent);
releaseButton.addEventListener('click', releaseCurrentVersion);
exportSessionButton.addEventListener('click', exportSession);
importSessionButton.addEventListener('click', () => importSessionInput.click());
importSessionInput.addEventListener('change', importSession);
clearSessionButton.addEventListener('click', clearEntireSession);

const resumed = loadSession();
input.value = working.root;
renderAll(resumed ? 'Die lokal bewahrte Sitzung wurde wiederaufgenommen. Festgehaltene Fassungen besitzen damit relative Dauer über einen Seitenaufruf hinaus.' : undefined);
