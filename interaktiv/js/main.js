const input = document.querySelector('#beginning');
const observation = document.querySelector('#observation');
const moves = document.querySelector('#moves');
const moveButtons = [...document.querySelectorAll('[data-move]')];
const editBeginningButton = document.querySelector('#edit-beginning');
const clearCurrentButton = document.querySelector('#clear-current');
const characterCount = document.querySelector('#char-count');
const characterWarning = document.querySelector('#char-warning');
const beginningEditActions = document.querySelector('#beginning-edit-actions');
const acceptBeginningEditButton = document.querySelector('#accept-beginning-edit');
const cancelBeginningEditButton = document.querySelector('#cancel-beginning-edit');
const connectionComposer = document.querySelector('#connection-composer');
const connectionTitle = document.querySelector('#connection-title');
const movePrompt = document.querySelector('#move-prompt');
const manuscriptChapter = document.querySelector('#manuscript-chapter');
const manuscriptQuestion = document.querySelector('#manuscript-question');
const connectionInput = document.querySelector('#connection-text');
const connectionCount = document.querySelector('#connection-count');
const connectionWarning = document.querySelector('#connection-warning');
const commitMoveButton = document.querySelector('#commit-move');
const cancelMoveButton = document.querySelector('#cancel-move');
const aiAssistant = document.querySelector('#ai-assistant');
const aiSuggestButton = document.querySelector('#ai-suggest');
const aiCancelButton = document.querySelector('#ai-cancel');
const aiStatus = document.querySelector('#ai-status');
const aiResult = document.querySelector('#ai-result');
const aiResultTitle = document.querySelector('#ai-result-title');
const aiSuggestionText = document.querySelector('#ai-suggestion');
const aiExplanation = document.querySelector('#ai-explanation');
const aiAdoptButton = document.querySelector('#ai-adopt');
const aiDiscardButton = document.querySelector('#ai-discard');
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
const zettelAddress = document.querySelector('#zettel-address');
const plateauCopy = document.querySelector('#plateau-copy');
const plateauLink = document.querySelector('#plateau-link');
const plateauLinks = document.querySelector('#plateau-links');
const storageStatus = document.querySelector('#storage-status');
const draftStatus = document.querySelector('#draft-status');
const exportSessionButton = document.querySelector('#export-session');
const importSessionButton = document.querySelector('#import-session-trigger');
const importSessionInput = document.querySelector('#import-session');
const clearSessionButton = document.querySelector('#clear-session');
const relationCheck = document.querySelector('#relation-check');
const relationCheckPrompt = document.querySelector('#relation-check-prompt');
const automatonStatus = document.querySelector('#automaton-status');
const automatonCopy = document.querySelector('#automaton-copy');
const automatonThought = document.querySelector('#automaton-thought');
const automatonConcepts = document.querySelector('#automaton-concepts');
const automatonChapter = document.querySelector('#automaton-chapter');
const automatonDraft = document.querySelector('#automaton-draft');
const automatonEvent = document.querySelector('#automaton-event');
const automatonValidation = document.querySelector('#automaton-validation');
const automatonDecision = document.querySelector('#automaton-decision');
const automatonGate = document.querySelector('#automaton-gate');
const automatonSteps = [...document.querySelectorAll('[data-automaton-step]')];

const STORAGE_KEY = 'anschlusslabor.session.v2';
const SESSION_FORMAT = 'anschlusslabor-session';
const SCHEMA_VERSION = 2;
const MAX_STEPS = 50;
const MAX_VERSIONS = 40;
const HISTORY_PREVIEW_LENGTH = 6;
const AI_REQUEST_TIMEOUT_MS = 20_000;

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
    manuscriptChapter: 'Kapitel 1: Anschließen',
    manuscriptQuestion: 'Prüffrage: Welche Bedingung des vorherigen Wortlauts wird aufgenommen und dadurch für weitere Anschlüsse wirksam?',
    placeholder: 'Formuliere eine Folgerung, Ergänzung oder Weiterführung.',
    relation: 'Als Fortsetzung gesetzt',
    condition: 'als Fortsetzung gesetzter Wortlaut',
    possibilities: [
      'eine Folgerung prüfen',
      'ein Beispiel an den neuen Wortlaut anschließen',
      'den fortgesetzten Bezug später wiederaufnehmen'
    ],
    observation: 'Der neue Wortlaut wurde als Fortsetzung gesetzt. Ob er den vorherigen Anschluss tatsächlich weiterführt und welche Folgerungen, Beispiele oder Einwände dadurch passen, bleibt prüfbar.'
  },
  praezisieren: {
    key: 'praezisieren',
    label: 'Präzisieren',
    prompt: 'Welche Unterscheidung soll genauer bestimmt werden?',
    manuscriptChapter: 'Kapitel 4: Form',
    manuscriptQuestion: 'Prüffrage: Welche Differenz wird so bestimmt, dass sie weitere Anschlüsse trägt?',
    placeholder: 'Benenne die Unterscheidung und ihren begrenzten Geltungsbereich.',
    relation: 'Als Präzisierung gesetzt',
    condition: 'als Präzisierung gesetzter Wortlaut',
    possibilities: [
      'den Geltungsbereich weiter eingrenzen',
      'eine Bedingung ausdrücklich benennen',
      'einen Grenzfall prüfen'
    ],
    observation: 'Der neue Wortlaut wurde als Präzisierung gesetzt. Ob er die bezeichnete Unterscheidung tatsächlich bestimmter macht und ihren Geltungsbereich trägt, bleibt prüfbar.'
  },
  unterbrechen: {
    key: 'unterbrechen',
    label: 'Unterbrechen',
    prompt: 'Welche Voraussetzung des vorherigen Anschlusses wird fraglich?',
    manuscriptChapter: 'Kapitel 2: Unterbrechen',
    manuscriptQuestion: 'Prüffrage: Welche bisher unauffällige Bedingung wird durch die Unterbrechung sichtbar oder fraglich?',
    placeholder: 'Formuliere die Unterbrechung als konkrete Frage, Zurückweisung oder Zäsur.',
    relation: 'Als Unterbrechung gesetzt',
    condition: 'als Unterbrechung gesetzter Wortlaut',
    possibilities: [
      'die sichtbar gewordene Voraussetzung prüfen',
      'die Frage unter veränderten Bedingungen neu fassen',
      'eine andere Anschlusslinie beginnen'
    ],
    observation: 'Der neue Wortlaut wurde als Unterbrechung gesetzt. Ob er eine Voraussetzung des vorausgehenden Zusammenhangs tatsächlich sichtbar macht oder nur eine andere Linie beginnt, bleibt prüfbar.'
  },
  variieren: {
    key: 'variieren',
    label: 'Variieren',
    prompt: 'Wie verändern sich Perspektive oder Gewichtung des vorherigen Anschlusses?',
    manuscriptChapter: 'Kapitel 6: Improvisieren',
    manuscriptQuestion: 'Prüffrage: Welche Gewichtung verschiebt sich, ohne dass der Bezug zur vorherigen Fassung verschwindet?',
    placeholder: 'Formuliere eine erkennbare Abweichung innerhalb desselben Bezugs.',
    relation: 'Als Variation gesetzt',
    condition: 'als Variation gesetzter Wortlaut',
    possibilities: [
      'die Variante mit dem vorherigen Wortlaut vergleichen',
      'eine andere Perspektive ergänzen',
      'bestimmen, welche Beziehung trotz Variation fortbesteht'
    ],
    observation: 'Der neue Wortlaut wurde als Variation gesetzt. Ob der vorausgehende Bezug dabei fortbesteht und welche Gewichtung sich tatsächlich verändert, bleibt am Verhältnis beider Wortlaute zu prüfen.'
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
let aiSuggestion = null;
let aiRequest = null;
let aiRequestSequence = 0;
let storageMessage = 'Fassungen werden lokal in diesem Browser bewahrt. Sie sind nicht öffentlich und nicht zwischen Geräten synchronisiert.';

function aiSignature() {
  return JSON.stringify([pendingMoveKey, currentWording()]);
}

function clearAiState({ abort = true, status = '' } = {}) {
  aiRequestSequence += 1;
  if (aiRequest?.timer) {
    clearTimeout(aiRequest.timer);
  }
  if (abort) {
    aiRequest?.controller.abort();
  }
  aiRequest = null;
  aiSuggestion = null;
  aiAssistant.setAttribute('aria-busy', 'false');
  aiSuggestButton.disabled = false;
  aiCancelButton.hidden = true;
  aiResult.hidden = true;
  aiSuggestionText.textContent = '';
  aiExplanation.textContent = '';
  aiStatus.textContent = status;
}

function userFacingAiError(error) {
  if (error instanceof TypeError && /fetch/i.test(error.message || '')) {
    return 'Der KI-Endpunkt ist nicht erreichbar. Öffne das Anschlusslabor über den Worker oder Projektserver; bei einer rein statischen Datei bleibt der manuelle Entwurf verfügbar.';
  }
  return error instanceof Error
    ? error.message
    : 'Der KI-Vorschlag ist derzeit nicht verfügbar. Der manuelle Entwurf bleibt verfügbar.';
}

async function requestAiSuggestion() {
  const previousText = currentWording();
  if (!pendingMoveKey || !previousText || aiRequest) {
    return;
  }

  clearAiState();
  const sequence = aiRequestSequence;
  const signature = aiSignature();
  const controller = new AbortController();
  aiRequest = { controller, sequence, signature, timedOut: false, timer: null };
  aiRequest.timer = setTimeout(() => {
    if (aiRequest?.sequence === sequence) {
      aiRequest.timedOut = true;
      controller.abort();
    }
  }, AI_REQUEST_TIMEOUT_MS);
  aiAssistant.setAttribute('aria-busy', 'true');
  aiSuggestButton.disabled = true;
  aiCancelButton.hidden = false;
  aiStatus.textContent = 'Der Formulierungsvorschlag wird angefordert.';

  try {
    const response = await fetch('/api/anschluss', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal: controller.signal,
      body: JSON.stringify({ move: pendingMoveKey, previousText })
    });
    const result = await response.json().catch(() => ({}));
    if (!aiRequest || aiRequest.sequence !== sequence) {
      return;
    }
    if (aiSignature() !== signature) {
      clearAiState({ abort: false, status: 'Der Bezugsstand hat sich geändert; die KI-Antwort wurde verworfen.' });
      return;
    }
    if (!response.ok) {
      throw new Error(typeof result.error === 'string' ? result.error : 'Der KI-Vorschlag ist derzeit nicht verfügbar.');
    }

    const suggestion = typeof result.suggestion === 'string' ? result.suggestion.trim() : '';
    const explanation = typeof result.explanation === 'string' ? result.explanation.trim() : '';
    if (!suggestion || suggestion.length > 400 || !explanation || explanation.length > 600) {
      throw new Error('Die KI-Antwort hatte kein verwendbares Format.');
    }

    aiSuggestion = { suggestion, explanation, signature };
    aiSuggestionText.textContent = suggestion;
    aiExplanation.textContent = explanation;
    aiResult.hidden = false;
    aiStatus.textContent = 'Ein flüchtiger Vorschlag liegt zur Prüfung vor.';
    if (aiAssistant.contains(document.activeElement)) {
      aiResultTitle.focus();
    }
  } catch (error) {
    if (!aiRequest || aiRequest.sequence !== sequence) {
      return;
    }
    if (error?.name === 'AbortError') {
      aiStatus.textContent = aiRequest.timedOut
        ? 'Die KI-Anfrage hat zu lange gedauert. Der manuelle Entwurf bleibt verfügbar.'
        : 'Die KI-Anfrage wurde abgebrochen.';
    } else {
      aiStatus.textContent = userFacingAiError(error);
    }
  } finally {
    if (aiRequest?.sequence === sequence) {
      clearTimeout(aiRequest.timer);
      aiRequest = null;
      aiAssistant.setAttribute('aria-busy', 'false');
      aiSuggestButton.disabled = false;
      aiCancelButton.hidden = true;
    }
  }
}

function cancelAiRequest() {
  const controller = aiRequest?.controller;
  if (!controller) {
    return;
  }
  clearTimeout(aiRequest.timer);
  controller.abort();
  aiRequest = null;
  aiRequestSequence += 1;
  aiAssistant.setAttribute('aria-busy', 'false');
  aiSuggestButton.disabled = false;
  aiCancelButton.hidden = true;
  aiStatus.textContent = 'Die KI-Anfrage wurde abgebrochen.';
  aiSuggestButton.focus();
}

function adoptAiSuggestion() {
  if (!aiSuggestion || aiSuggestion.signature !== aiSignature()) {
    clearAiState({ status: 'Der Vorschlag bezog sich auf einen früheren Stand und wurde verworfen.' });
    return;
  }
  if (connectionInput.value.trim() && !window.confirm('Der KI-Vorschlag ersetzt den vorhandenen ungespeicherten Arbeitsentwurf. Fortfahren?')) {
    connectionInput.focus();
    return;
  }

  connectionInput.value = aiSuggestion.suggestion;
  connectionInput.dispatchEvent(new Event('input', { bubbles: true }));
  aiStatus.textContent = 'Der Vorschlag wurde in den offenen Entwurf kopiert. Gespeichert ist er noch nicht.';
  connectionInput.focus();
}

function discardAiSuggestion() {
  clearAiState({ status: 'Der flüchtige KI-Vorschlag wurde verworfen.' });
  aiSuggestButton.focus();
}
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

function hasOpenDraft() {
  return editingBeginning || Boolean(pendingMoveKey);
}

function hasSessionData() {
  return Boolean(working.root.trim() || working.steps.length || versions.length);
}

function updateLimitWarning(element, warning, limit, threshold) {
  const message = element.value.length >= limit - threshold
    ? 'Das Zeichenlimit ist fast erreicht.'
    : '';
  if (warning.textContent !== message) {
    warning.textContent = message;
  }
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

function normalizeTimestamp(value) {
  return typeof value === 'string' && Number.isFinite(Date.parse(value)) ? value : null;
}

function normalizeSteps(source, root, startingSequence) {
  const steps = [];
  let sequence = startingSequence;
  let previousText = root.trim();

  (Array.isArray(source) ? source : []).slice(0, MAX_STEPS).forEach((step) => {
    if (!step || typeof step !== 'object' || !moveDefinitions[step.type]) {
      return;
    }

    const text = typeof step.text === 'string' ? step.text.trim().slice(0, 400) : '';
    if (!text) {
      return;
    }

    sequence += 1;
    steps.push({
      id: 'step-' + sequence,
      type: step.type,
      text,
      previousText: previousText.slice(0, 400),
      createdAt: normalizeTimestamp(step.createdAt)
    });
    previousText = text;
  });

  return { steps, sequence };
}

function removeInvalidGenealogies(normalizedVersions) {
  const versionsById = new Map(normalizedVersions.map((version) => [version.id, version]));

  normalizedVersions.forEach((version) => {
    if (version.parentVersionId === version.id || !versionsById.has(version.parentVersionId)) {
      version.parentVersionId = null;
    }
  });

  normalizedVersions.forEach((version) => {
    const visited = new Set([version.id]);
    let cursor = version;

    while (cursor.parentVersionId) {
      if (visited.has(cursor.parentVersionId)) {
        cursor.parentVersionId = null;
        break;
      }
      visited.add(cursor.parentVersionId);
      cursor = versionsById.get(cursor.parentVersionId);
    }
  });

  return versionsById;
}

function normalizeSession(raw) {
  if (!raw || typeof raw !== 'object' || raw.format !== SESSION_FORMAT || raw.schemaVersion !== SCHEMA_VERSION) {
    throw new Error('Unbekanntes Sitzungsformat');
  }

  const normalizedVersions = [];
  const seenIds = new Set();
  const sourceVersions = Array.isArray(raw.versions) ? raw.versions.slice(-MAX_VERSIONS) : [];
  let normalizedStepSequence = 0;

  sourceVersions.forEach((version) => {
    if (!version || typeof version !== 'object') {
      return;
    }

    const id = typeof version.id === 'string' ? version.id : '';
    const root = typeof version.root === 'string' ? version.root.trim().slice(0, 280) : '';
    if (!/^version-\d+$/.test(id) || seenIds.has(id) || !root) {
      return;
    }

    const normalized = normalizeSteps(version.steps, root, normalizedStepSequence);
    normalizedStepSequence = normalized.sequence;
    seenIds.add(id);
    normalizedVersions.push({
      id,
      number: normalizedVersions.length + 1,
      root,
      steps: normalized.steps,
      parentVersionId: typeof version.parentVersionId === 'string' ? version.parentVersionId : null,
      createdAt: normalizeTimestamp(version.createdAt),
      releasedAt: normalizeTimestamp(version.releasedAt)
    });
  });

  const normalizedWorkingRoot = typeof raw.working?.root === 'string'
    ? raw.working.root.trim().slice(0, 280)
    : '';
  const normalizedWorking = normalizeSteps(raw.working?.steps, normalizedWorkingRoot, normalizedStepSequence);
  normalizedStepSequence = normalizedWorking.sequence;

  const versionsById = removeInvalidGenealogies(normalizedVersions);
  const maximumVersionId = normalizedVersions.reduce((maximum, version) => {
    return Math.max(maximum, Number(version.id.replace('version-', '')) || 0);
  }, 0);
  const releaseVersion = versionsById.get(raw.currentReleaseId);

  return {
    working: { root: normalizedWorkingRoot, steps: normalizedWorking.steps },
    versions: normalizedVersions,
    versionSequence: Math.max(Number(raw.versionSequence) || 0, maximumVersionId, normalizedVersions.length),
    stepSequence: normalizedStepSequence,
    currentVersionId: versionsById.has(raw.currentVersionId) ? raw.currentVersionId : null,
    workingParentVersionId: versionsById.has(raw.workingParentVersionId) ? raw.workingParentVersionId : null,
    currentReleaseId: releaseVersion?.releasedAt ? releaseVersion.id : null
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

function createHistoryEntry(entry, number) {
  const item = document.createElement('li');
  item.className = 'history-entry';

  const numberElement = document.createElement('span');
  numberElement.className = 'history-number';
  numberElement.textContent = String(number).padStart(2, '0');

  const body = document.createElement('div');
  body.className = 'history-entry-body';
  const meta = document.createElement('span');
  meta.className = 'history-operation';
  meta.textContent = entry.meta;

  const text = document.createElement('p');
  text.textContent = '„' + entry.text + '“';

  body.append(meta, text);
  if (entry.manuscriptChapter) {
    const reference = document.createElement('p');
    reference.className = 'history-reference';
    reference.textContent = entry.manuscriptChapter + ': ' + entry.manuscriptQuestion;
    body.append(reference);
  }
  item.append(numberElement, body);
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
    entries.push({
      meta: definition.relation,
      text: step.text,
      manuscriptChapter: step.manuscriptChapter || definition.manuscriptChapter,
      manuscriptQuestion: step.manuscriptQuestion || definition.manuscriptQuestion
    });
  });

  const visibleStart = Math.max(0, entries.length - HISTORY_PREVIEW_LENGTH);
  if (visibleStart > 0) {
    const hiddenEntries = entries.slice(0, visibleStart);
    const foldItem = document.createElement('li');
    foldItem.className = 'history-fold';
    const details = document.createElement('details');
    const summary = document.createElement('summary');
    summary.textContent = hiddenEntries.length + ' frühere Anschlüsse anzeigen';
    const foldedList = document.createElement('ol');
    foldedList.className = 'folded-history-list';
    hiddenEntries.forEach((entry, index) => foldedList.append(createHistoryEntry(entry, index + 1)));
    details.append(summary, foldedList);
    foldItem.append(details);
    history.append(foldItem);
  }

  entries.slice(visibleStart).forEach((entry, index) => {
    history.append(createHistoryEntry(entry, visibleStart + index + 1));
  });
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

function zettelLabel(index) {
  return 'Zettel ' + String(index).padStart(2, '0');
}

function renderPlateauLinks(root, lastStep) {
  plateauLinks.replaceChildren();
  if (!root) {
    const item = document.createElement('li');
    item.textContent = 'Keine gerichtete Verbindung gesetzt.';
    plateauLinks.append(item);
    return;
  }

  working.steps.forEach((step, index) => {
    const definition = moveDefinitions[step.type];
    const item = document.createElement('li');
    item.textContent = zettelLabel(index + 1) + ' → ' + zettelLabel(index + 2) + ': ' + definition.label;
    plateauLinks.append(item);
  });

  const openItem = document.createElement('li');
  openItem.className = 'open-plateau-link';
  openItem.textContent = lastStep
    ? zettelLabel(working.steps.length + 1) + ' → ? : Fortsetzen, Präzisieren, Unterbrechen oder Variieren bleiben möglich.'
    : zettelLabel(1) + ' → ? : Fortsetzen, Präzisieren, Unterbrechen oder Variieren bleiben möglich.';
  plateauLinks.append(openItem);
}

function renderPlateau() {
  const root = working.root.trim();
  const lastStep = working.steps.at(-1);
  const addressNumber = root ? working.steps.length + 1 : 0;
  zettelAddress.textContent = zettelLabel(addressNumber);

  if (!root) {
    plateauCopy.textContent = 'Noch ist kein eigener Zettel adressiert. Die erste Äußerung eröffnet eine lokale Karte weiterer Anschlüsse.';
    plateauLink.textContent = 'Arbeitsmodell: Luhmanns Zettelkasten und Deleuze/Guattaris Plateaus bleiben hier methodische Bezugspunkte, keine neue Theorieachse.';
    renderPlateauLinks(root, lastStep);
    return;
  }

  if (!lastStep) {
    plateauCopy.textContent = 'Die Ausgangsäußerung ist als erster Zettel adressiert. Sie bildet noch kein abgeschlossenes System, sondern einen Einstieg in mögliche Fortsetzungen, Unterbrechungen, Präzisierungen und Variationen.';
    plateauLink.textContent = 'Plateau: ein lokaler Zusammenhang aus Wortlaut, Bedingungen und noch offenen Anschlusswegen.';
    renderPlateauLinks(root, lastStep);
    return;
  }

  const definition = moveDefinitions[lastStep.type];
  plateauCopy.textContent = definition.label + ' bildet ' + zettelLabel(addressNumber) + '. Der neue Wortlaut bleibt auf den vorherigen Zettel bezogen und verändert zugleich, welche weiteren Anschlüsse naheliegen.';
  plateauLink.textContent = 'Prüfspur: ' + definition.manuscriptChapter + ' · ' + definition.manuscriptQuestion;
  renderPlateauLinks(root, lastStep);
}
function inferredConceptsForAutomaton(wording, lastStep) {
  const normalized = String(wording || '').toLowerCase();
  const concepts = new Set();
  if (/algorithm|programm|regel|beding/.test(normalized)) {
    concepts.add('Algorithmus');
    concepts.add('Programm');
  }
  if (/kritik|kritisch|beurteil|urteil/.test(normalized)) {
    concepts.add('Kritisieren');
    concepts.add('Beurteilen');
  }
  if (/organisation|organisier|anschluss|möglich/.test(normalized)) {
    concepts.add('Anschließen');
    concepts.add('Organisieren');
  }
  if (/unterbrech|zäsur|fraglich/.test(normalized) || lastStep?.type === 'unterbrechen') {
    concepts.add('Unterbrechen');
  }
  if (/form|unterscheid|präzis/.test(normalized) || lastStep?.type === 'praezisieren') {
    concepts.add('Form');
  }
  if (/variation|variante|improvis/.test(normalized) || lastStep?.type === 'variieren') {
    concepts.add('Improvisieren');
  }
  if (lastStep?.type === 'fortsetzen') {
    concepts.add('Anschließen');
  }
  return [...concepts].slice(0, 4);
}

function setAutomatonStep(name, active, locked = false) {
  const step = automatonSteps.find((item) => item.dataset.automatonStep === name);
  if (!step) {
    return;
  }
  step.classList.toggle('is-active', active);
  step.classList.toggle('is-locked', locked);
}

function renderAutomaton() {
  const root = working.root.trim();
  const lastStep = working.steps.at(-1);
  const wording = currentWording();
  const hasThought = Boolean(root);
  const hasDraft = Boolean(lastStep);
  const concepts = inferredConceptsForAutomaton(wording, lastStep);
  const definition = lastStep ? moveDefinitions[lastStep.type] : null;

  automatonStatus.textContent = hasDraft ? 'Draft vorprüfbar' : hasThought ? 'Begriffsprüfung möglich' : 'Vorschlagsmaschine';
  automatonThought.textContent = hasThought ? excerpt(wording, 72) : 'kein eigener Wortlaut';
  automatonConcepts.textContent = concepts.length ? concepts.join(', ') : hasThought ? 'keine sichere Begriffsadresse' : 'wartet auf Anschluss';
  automatonChapter.textContent = definition ? definition.manuscriptChapter : hasThought ? 'Kapitelanker noch offen' : 'kein Kapitelanker';
  automatonDraft.textContent = hasDraft ? 'markierter Vorschlag möglich' : hasThought ? 'erst nach konkretem Anschluss' : 'nicht erzeugt';
  automatonEvent.textContent = hasDraft ? 'Change-Event-Entwurf möglich' : 'nicht vorgeschlagen';
  automatonValidation.textContent = hasDraft ? 'als Draft formal vorprüfbar' : 'nicht geprüft';
  automatonDecision.textContent = 'bleibt beim Autor';
  automatonCopy.textContent = hasDraft
    ? 'Der aktuelle Anschluss kann als Vorschlag, Kapitelkontext, Event-Draft und Vorprüfung gedacht werden. Stabilisiert ist dadurch noch nichts.'
    : hasThought
      ? 'Der gesetzte Gedanke kann auf Begriffe und mögliche Kapitelanker bezogen werden. Ein Draft entsteht erst durch einen konkreten Anschluss.'
      : 'Noch liegt kein eigener Gedanke vor. Der Automat bleibt hier als Prozesskarte sichtbar: Er erzeugt Möglichkeiten, aber keine Theorieentscheidung.';
  automatonGate.querySelector('p').textContent = hasDraft
    ? 'Sperrklinke: gültig als Draft heißt nicht bestätigt als Theorie.'
    : 'Grenze: Der Automat erzeugt Möglichkeiten, aber keine Autorentscheidung.';

  setAutomatonStep('thought', hasThought);
  setAutomatonStep('concepts', hasThought);
  setAutomatonStep('chapter', hasThought);
  setAutomatonStep('draft', hasDraft);
  setAutomatonStep('event', hasDraft);
  setAutomatonStep('validation', hasDraft);
  setAutomatonStep('decision', false, true);
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
  const openDraft = hasOpenDraft();

  characterCount.textContent = input.value.length + ' von 280 Zeichen';
  updateLimitWarning(input, characterWarning, 280, 30);
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
    manuscriptChapter.textContent = definition.manuscriptChapter;
    manuscriptQuestion.textContent = definition.manuscriptQuestion;
    connectionInput.placeholder = definition.placeholder;
  }
  connectionCount.textContent = connectionInput.value.length + ' von 400 Zeichen';
  updateLimitWarning(connectionInput, connectionWarning, 400, 40);
  commitMoveButton.disabled = !connectionInput.value.trim() || working.steps.length >= MAX_STEPS;

  exportSessionButton.disabled = openDraft;
  importSessionButton.disabled = openDraft;
  importSessionInput.disabled = openDraft;
  draftStatus.hidden = !openDraft;
  if (openDraft) {
    draftStatus.textContent = editingBeginning
      ? 'Die noch nicht bestätigte Änderung der Ausgangsäußerung wird weder gespeichert noch exportiert.'
      : 'Der noch nicht aktualisierte Anschlussentwurf wird weder gespeichert noch exportiert.';
  }
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
    actualRelation.textContent = definition.relation + ' · Bezug auf „' + excerpt(lastStep.previousText, 64) + '“';
    actualText.textContent = '„' + wording + '“';
    renderList(possibilities, definition.possibilities);
  } else {
    actualRelation.textContent = 'Ausgangsäußerung';
    actualText.textContent = '„' + root + '“';
    renderList(possibilities, initialPossibilities);
  }

  relationCheck.hidden = !lastStep;
  if (lastStep) {
    relationCheckPrompt.textContent = 'Trägt der neue Wortlaut die vorgesehene Relation „' + moveDefinitions[lastStep.type].label + '“?';
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
  renderPlateau();
  renderAutomaton();
  renderStabilization();
  storageStatus.textContent = storageMessage;
}


function selectMove(event) {
  clearAiState();
  pendingMoveKey = event.currentTarget.dataset.move;
  connectionInput.value = '';
  renderInputControls();
  connectionInput.focus();
}

function cancelMove() {
  clearAiState();
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

  clearAiState();

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
    manuscriptChapter: definition.manuscriptChapter,
    manuscriptQuestion: definition.manuscriptQuestion,
    createdAt: new Date().toISOString()
  });
  pendingMoveKey = null;
  connectionInput.value = '';
  input.disabled = true;
  persistSession();
  renderAll(definition.observation);
  observation.focus();
}

function beginBeginningEdit() {
  clearAiState();
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
  observation.focus();
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
  clearAiState();
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
  clearAiState();
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

  clearAiState();

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
    if (hasSessionData() && !window.confirm('Die importierte Sitzung ersetzt die aktuelle lokale Sitzung. Vorher exportieren oder fortfahren?')) {
      setStorageMessage('Der Import wurde abgebrochen. Die aktuelle lokale Sitzung blieb unverändert.');
      storageStatus.focus();
      return;
    }

    clearAiState();
    applyNormalizedSession(imported);
    input.value = working.root;
    connectionInput.value = '';
    persistSession();
    storageMessage = 'Die JSON-Sitzung wurde als lokaler Arbeitsstand wiederaufgenommen.';
    renderAll('Die importierte Sitzung ist wieder anschlussfähig. Ihre geprüften Fassungen, Abstammungen und Freigabestatus wurden übernommen.');
    storageStatus.focus();
  } catch {
    setStorageMessage('Die ausgewählte Datei konnte nicht als gültige Anschlusslabor-Sitzung gelesen werden. Der bestehende Stand blieb unverändert.');
    storageStatus.focus();
  } finally {
    event.target.value = '';
  }
}

input.addEventListener('input', () => {
  if (pendingMoveKey && (aiRequest || aiSuggestion)) {
    clearAiState({ status: 'Der Bezugswortlaut hat sich geändert; der flüchtige KI-Vorschlag wurde verworfen.' });
  }
  characterCount.textContent = input.value.length + ' von 280 Zeichen';
  updateLimitWarning(input, characterWarning, 280, 30);
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
  updateLimitWarning(connectionInput, connectionWarning, 400, 40);
  commitMoveButton.disabled = !connectionInput.value.trim() || working.steps.length >= MAX_STEPS;
});

moveButtons.forEach((button) => button.addEventListener('click', selectMove));
editBeginningButton.addEventListener('click', beginBeginningEdit);
acceptBeginningEditButton.addEventListener('click', acceptBeginningEdit);
cancelBeginningEditButton.addEventListener('click', cancelBeginningEdit);
clearCurrentButton.addEventListener('click', clearCurrent);
commitMoveButton.addEventListener('click', commitMove);
cancelMoveButton.addEventListener('click', cancelMove);
aiSuggestButton.addEventListener('click', requestAiSuggestion);
aiCancelButton.addEventListener('click', cancelAiRequest);
aiAdoptButton.addEventListener('click', adoptAiSuggestion);
aiDiscardButton.addEventListener('click', discardAiSuggestion);
stabilizeButton.addEventListener('click', stabilizeCurrent);
releaseButton.addEventListener('click', releaseCurrentVersion);
exportSessionButton.addEventListener('click', exportSession);
importSessionButton.addEventListener('click', () => importSessionInput.click());
importSessionInput.addEventListener('change', importSession);
clearSessionButton.addEventListener('click', clearEntireSession);

const resumed = loadSession();
input.value = working.root;
renderAll(resumed ? 'Die lokal bewahrte Sitzung wurde wiederaufgenommen. Festgehaltene Fassungen besitzen damit relative Dauer über einen Seitenaufruf hinaus.' : undefined);
