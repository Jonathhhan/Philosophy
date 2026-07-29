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
    label: 'Präzisieren',
    actual: 'Eine Unterscheidung wird bestimmter gefasst.',
    condition: 'geschärfte Unterscheidung',
    history: 'Unterscheidung präzisiert',
    possibilities: [
      'den Geltungsbereich eingrenzen',
      'eine Bedingung ausdrücklich benennen',
      'einen Grenzfall prüfen'
    ],
    observation: 'Die Präzisierung macht nicht einfach mehr Möglichkeiten verfügbar. Sie gliedert den Anschlussraum neu: Manche Fortsetzungen werden bestimmter, andere passen nicht mehr zur gesetzten Unterscheidung.'
  },
  unterbrechen: {
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

function renderConditions() {
  const dynamicConditions = selectedMoves.map((move) => move.condition);
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

function renderInputState() {
  const value = input.value.trim();
  const hasInput = value.length > 0;

  characterCount.textContent = input.value.length + ' von 280 Zeichen';
  document.body.classList.toggle('has-input', hasInput);
  moves.disabled = !hasInput;
  actualText.textContent = hasInput ? '„' + excerpt(value) + '“' : 'Noch keine eigene Äußerung';
  renderList(possibilities, hasInput ? initialPossibilities : emptyPossibilities);
  renderConditions();
  renderHistory(hasInput);

  observation.textContent = hasInput
    ? 'Mit der Äußerung wurde eine Möglichkeit aktualisiert. Ihr Wortlaut ist nun selbst eine Bedingung dafür, was als passende Fortsetzung, Präzisierung, Unterbrechung oder Variation erscheint.'
    : 'Noch wurde kein eigener Anschluss aktualisiert. Alphabet, Sprache, Interface und die Erwartung einer Fortsetzung wirken dennoch bereits als Bedingungen.';
}

function applyMove(event) {
  const button = event.currentTarget;
  const definition = moveDefinitions[button.dataset.move];

  moveButtons.forEach((candidate) => candidate.classList.toggle('is-active', candidate === button));
  selectedMoves.push(definition);
  actualText.textContent = definition.label + ': ' + definition.actual;
  observation.textContent = definition.observation;
  renderList(possibilities, definition.possibilities);
  renderConditions();
  renderHistory(true);
}

input.addEventListener('input', () => {
  clearMoveSelection();
  renderInputState();
});

moveButtons.forEach((button) => button.addEventListener('click', applyMove));

resetButton.addEventListener('click', () => {
  input.value = '';
  clearMoveSelection();
  renderInputState();
  input.focus();
});

renderInputState();
