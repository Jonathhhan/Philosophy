const input = document.querySelector('#beginning');
const observation = document.querySelector('#observation');
const nodes = [...document.querySelectorAll('#nodes span')];

const messages = [
  'Noch scheint das Feld leer. Doch Alphabet, Sprache, Eingaberegeln und mögliche Zeichen sind bereits vorgeordnet.',
  'Mit dem ersten Zeichen wird eine Möglichkeit aktualisiert. Andere Fortsetzungen werden dadurch wahrscheinlicher, unwahrscheinlicher oder ausgeschlossen.',
  'Die Eingabe beginnt nicht bei null: Sie schließt an Sprache, Zeichenordnung, Interface und Erwartung an.',
  'Der entstandene Satz ist nun selbst Bedingung weiterer Anschlüsse.'
];

input.addEventListener('input', () => {
  const length = input.value.trim().length;
  const stage = length === 0 ? 0 : length < 8 ? 1 : length < 28 ? 2 : 3;

  observation.textContent = messages[stage];
  nodes.forEach((node, index) => {
    node.classList.toggle('active', index <= stage + 1);
  });
});
