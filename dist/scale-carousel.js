const carousel = document.querySelector('.scale-carousel');
const slides = [...carousel.querySelectorAll('.scale-slide')];
const slideRegion = carousel.querySelector('.scale-slides');
const controls = carousel.querySelector('.scale-controls');
const position = carousel.querySelector('.scale-position');
const playback = carousel.querySelector('.scale-toggle');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let active = 0;
let playing = !carousel.hasAttribute('data-manual') && !reducedMotion.matches;
let timer;

function step(amount) {
  slides[active].hidden = true;
  active = (active + amount + slides.length) % slides.length;
  slides[active].hidden = false;
  position.textContent = `${active + 1} / ${slides.length}`;
}

function schedule() {
  window.clearTimeout(timer);
  if (playing && !carousel.matches(':hover') && !document.hidden) {
    timer = window.setTimeout(() => {
      step(1);
      schedule();
    }, 6000);
  }
}

function setPlaying(value) {
  playing = value;
  playback.textContent = playing ? 'Pause' : 'Play';
  playback.setAttribute('aria-label', playing ? 'Pause slideshow' : 'Play slideshow');
  slideRegion.setAttribute('aria-live', playing ? 'off' : 'polite');
  schedule();
}

function navigate(amount) {
  setPlaying(false);
  step(amount);
}

for (const button of controls.querySelectorAll('[data-step]')) {
  button.addEventListener('click', () => navigate(Number(button.dataset.step)));
}

playback.addEventListener('click', () => setPlaying(!playing));
carousel.addEventListener('mouseenter', schedule);
carousel.addEventListener('mouseleave', schedule);
carousel.addEventListener('focusin', (event) => {
  if (event.target !== playback || playback.matches(':focus-visible')) {
    setPlaying(false);
  }
});
carousel.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    navigate(event.key === 'ArrowLeft' ? -1 : 1);
  }
});
document.addEventListener('visibilitychange', schedule);
reducedMotion.addEventListener('change', (event) => {
  if (event.matches) setPlaying(false);
});

controls.hidden = false;
setPlaying(playing);
