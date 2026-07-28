const input = document.querySelector('#beginning');
const button = document.querySelector('#analyse');
const conditions = document.querySelector('#conditions');
const response = document.querySelector('#response');

button.addEventListener('click', () => {
  const text = input.value.trim();
  conditions.hidden = false;

  if (!text) {
    response.textContent = 'Auch die leere Eingabe ist kein voraussetzungsloser Anfang: Sie erscheint als Unterlassung innerhalb einer bereits eröffneten Möglichkeit.';
    return;
  }

  const words = text.split(/\s+/).filter(Boolean).length;
  response.textContent = `Deine Eingabe aktualisiert ${words} sprachliche${words === 1 ? 's Element' : ' Elemente'}. Mit ihr verändert sich, was als nächste Fortsetzung anschließen kann.`;
});
