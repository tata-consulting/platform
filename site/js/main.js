(() => {
  'use strict';

  /* ------------------------------------------------------------------
     Sticky header shadow on scroll
     ------------------------------------------------------------------ */
  const header = document.querySelector('.site-header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('is-scrolled', window.scrollY > 4);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ------------------------------------------------------------------
     Mega menu - hover on desktop, click/keyboard on touch
     ------------------------------------------------------------------ */
  const navItems = document.querySelectorAll('.primary-nav__item--has-mega');

  navItems.forEach((item) => {
    const trigger = item.querySelector('.primary-nav__link');
    if (!trigger) return;

    const open = () => {
      navItems.forEach((other) => {
        if (other !== item) other.classList.remove('is-open');
      });
      item.classList.add('is-open');
      trigger.setAttribute('aria-expanded', 'true');
    };
    const close = () => {
      item.classList.remove('is-open');
      trigger.setAttribute('aria-expanded', 'false');
    };
    const toggle = () => {
      item.classList.contains('is-open') ? close() : open();
    };

    item.addEventListener('mouseenter', open);
    item.addEventListener('mouseleave', close);

    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      toggle();
    });

    trigger.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') close();
    });
  });

  // Close mega on outside click / Escape
  document.addEventListener('click', (e) => {
    navItems.forEach((item) => {
      if (!item.contains(e.target)) {
        item.classList.remove('is-open');
        const trigger = item.querySelector('.primary-nav__link');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
      }
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      navItems.forEach((item) => {
        item.classList.remove('is-open');
        const trigger = item.querySelector('.primary-nav__link');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
      });
    }
  });

  /* ------------------------------------------------------------------
     Mobile menu
     ------------------------------------------------------------------ */
  const mobileToggle = document.querySelector('.mobile-toggle');
  const mobileMenu = document.querySelector('.mobile-menu');

  if (mobileToggle && mobileMenu) {
    const closeMobile = () => {
      mobileToggle.setAttribute('aria-expanded', 'false');
      mobileMenu.classList.remove('is-open');
      document.body.classList.remove('menu-open');
    };
    const openMobile = () => {
      mobileToggle.setAttribute('aria-expanded', 'true');
      mobileMenu.classList.add('is-open');
      document.body.classList.add('menu-open');
    };
    mobileToggle.addEventListener('click', () => {
      mobileToggle.getAttribute('aria-expanded') === 'true' ? closeMobile() : openMobile();
    });
    // Close on link click
    mobileMenu.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', closeMobile);
    });
    // Close on resize to desktop
    window.addEventListener('resize', () => {
      if (window.innerWidth >= 1024) closeMobile();
    });
    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeMobile();
    });
  }

  /* ------------------------------------------------------------------
     Reveal on scroll
     ------------------------------------------------------------------ */
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-visible'));
  }

  /* ------------------------------------------------------------------
     Footer year
     ------------------------------------------------------------------ */
  const yearEl = document.querySelector('[data-year]');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* ------------------------------------------------------------------
     Contact form - prevent actual submit, give feedback
     ------------------------------------------------------------------ */
  const form = document.querySelector('.contact-form');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const status = form.querySelector('[data-form-status]');
      if (status) {
        status.textContent = 'Thanks - we will reach out within two business days.';
        status.hidden = false;
      }
      form.reset();
    });
  }

  /* ------------------------------------------------------------------
     Newsletter form - prevent submit, brief feedback
     ------------------------------------------------------------------ */
  const newsletter = document.querySelector('.newsletter__form');
  if (newsletter) {
    newsletter.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = newsletter.querySelector('button');
      if (btn) {
        const original = btn.textContent;
        btn.textContent = 'Thanks - check your inbox.';
        btn.disabled = true;
        setTimeout(() => {
          btn.textContent = original;
          btn.disabled = false;
        }, 4000);
      }
      newsletter.reset();
    });
  }
})();
