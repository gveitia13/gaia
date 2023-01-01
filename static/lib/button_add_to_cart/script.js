document.querySelectorAll('.Button').forEach(Button => Button.addEventListener('click', E => {
  if (!Button.classList.contains('Loading')) {
    Button.classList.add('Loading');
    setTimeout(() => Button.classList.remove('Loading'), 3700);
  }
  E.preventDefault();
}));