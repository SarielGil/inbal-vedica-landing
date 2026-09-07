const navToggle = document.getElementById('site-nav-toggle');
const navMenu = document.getElementById('site-nav-menu');

if (navToggle && navMenu) {
  const closeMenu = () => {
    navMenu.classList.remove('is-open');
    navToggle.setAttribute('aria-expanded', 'false');
    navToggle.setAttribute('aria-label', 'פתיחת תפריט ניווט');
  };

  navToggle.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
    navToggle.setAttribute('aria-label', isOpen ? 'סגירת תפריט ניווט' : 'פתיחת תפריט ניווט');
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && navMenu.classList.contains('is-open')) {
      closeMenu();
      navToggle.focus();
    }
  });

  navMenu.addEventListener('focusout', (event) => {
    if (!navMenu.contains(event.relatedTarget) && event.relatedTarget !== navToggle) {
      closeMenu();
    }
  });

  navMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeMenu);
  });

  document.addEventListener('click', (event) => {
    if (window.innerWidth >= 1024) {
      return;
    }
    if (!navMenu.contains(event.target) && !navToggle.contains(event.target)) {
      closeMenu();
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024) {
      closeMenu();
    }
  });
}
