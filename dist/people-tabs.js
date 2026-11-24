(() => {
  const bar = document.querySelector('.people-tabs');
  if (!bar) return;
  const links = Array.from(bar.querySelectorAll('a[href^="#"]'));
  const sections = links.map(link => document.getElementById(link.hash.slice(1)));
  if (!sections.length || sections.some(section => !section)) return;

  const header = document.querySelector('header');
  const root = document.documentElement;
  let readingLine = 0, frame = 0;
  function highlight() {
    frame = 0;
    let current = 0;
    sections.forEach((section, i) => {
      if (section.getBoundingClientRect().top <= readingLine) current = i;
    });
    if (window.scrollY > 0 && window.scrollY + window.innerHeight >= root.scrollHeight - 2) current = sections.length - 1;
    links.forEach((link, i) => {
      if (i === current) link.setAttribute('aria-current','location');
      else link.removeAttribute('aria-current');
    });
  }
  function schedule() {
    if (!frame) frame = requestAnimationFrame(highlight);
  }
  function measure() {
    const h = header?.offsetHeight || 0, n = bar.offsetHeight;
    root.style.setProperty('--people-header', h + 'px');
    root.style.setProperty('--people-nav', n + 'px');
    readingLine = h + n + 10;
    schedule();
  }
  links.forEach((link, i) => {
    link.addEventListener('keydown', event => {
      const idx = {ArrowLeft:(i+links.length-1)%links.length,ArrowRight:(i+1)%links.length,Home:0,End:links.length-1,' ':i}[event.key];
      if (!Number.isInteger(idx) || event.ctrlKey || event.metaKey || event.altKey) return;
      event.preventDefault();
      links[idx].focus({preventScroll:true});
      links[idx].click();
    });
  });
  window.addEventListener('scroll', schedule, {passive:true});
  window.addEventListener('resize', measure);
  window.addEventListener('pageshow', measure);
  if (window.ResizeObserver) {
    const obs = new ResizeObserver(measure);
    if (header) obs.observe(header);
    obs.observe(bar);
  }
  measure();
})();
