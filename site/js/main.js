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
     Contact form - validate required fields and reject free email
     domains; give feedback on success
     ------------------------------------------------------------------ */
  const form = document.querySelector('.contact-form');
  if (form) {
    // Common free / consumer email providers - work email required
    const FREE_EMAIL_DOMAINS = new Set([
      'gmail.com', 'googlemail.com',
      'yahoo.com', 'yahoo.co.uk', 'yahoo.co.in', 'ymail.com', 'rocketmail.com',
      'hotmail.com', 'hotmail.co.uk', 'live.com', 'live.co.uk', 'msn.com',
      'outlook.com', 'outlook.co.uk',
      'aol.com', 'aim.com',
      'icloud.com', 'me.com', 'mac.com',
      'proton.me', 'protonmail.com', 'pm.me',
      'gmx.com', 'gmx.net', 'gmx.de', 'gmx.co.uk',
      'mail.com', 'mail.ru',
      'zoho.com', 'zohomail.com',
      'fastmail.com', 'fastmail.fm',
      'tutanota.com', 'tuta.io',
      'yandex.com', 'yandex.ru',
      'qq.com', '163.com', '126.com', 'sina.com', 'sohu.com',
      'rediffmail.com',
      'btinternet.com', 'sky.com', 'virginmedia.com', 'talktalk.net', 'ntlworld.com',
      'comcast.net', 'verizon.net', 'att.net', 'sbcglobal.net', 'cox.net',
      'inbox.com', 'hushmail.com',
      'duck.com', 'duckduckgo.com',
    ]);

    // RFC-5322-lite: enough to reject obvious garbage without false positives
    const EMAIL_RE = /^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/;

    const setError = (input, message) => {
      const field = input.closest('.form-field');
      const errEl = field && field.querySelector('.form-field__error');
      if (errEl) {
        if (message) {
          errEl.textContent = message;
          errEl.hidden = false;
        } else {
          errEl.textContent = '';
          errEl.hidden = true;
        }
      }
      if (message) {
        input.setAttribute('aria-invalid', 'true');
        if (field) field.classList.add('is-invalid');
      } else {
        input.removeAttribute('aria-invalid');
        if (field) field.classList.remove('is-invalid');
      }
    };

    const validateField = (input) => {
      const value = (input.value || '').trim();
      if (input.required && !value) {
        setError(input, 'This field is required.');
        return false;
      }
      if (input.type === 'email') {
        if (!EMAIL_RE.test(value)) {
          setError(input, 'Please enter a valid email address.');
          return false;
        }
        const domain = value.split('@')[1].toLowerCase();
        if (FREE_EMAIL_DOMAINS.has(domain)) {
          setError(input, 'Please use your work email - personal accounts are not accepted.');
          return false;
        }
      }
      if (input.minLength > 0 && value.length < input.minLength) {
        setError(input, `Please enter at least ${input.minLength} characters.`);
        return false;
      }
      setError(input, '');
      return true;
    };

    // Re-validate on blur and on input once a field has been touched
    form.querySelectorAll('input, select, textarea').forEach((el) => {
      el.addEventListener('blur', () => validateField(el));
      el.addEventListener('input', () => {
        if (el.getAttribute('aria-invalid') === 'true') validateField(el);
      });
    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const fields = Array.from(form.querySelectorAll('input, select, textarea'));
      const allValid = fields.reduce((ok, el) => validateField(el) && ok, true);
      const status = form.querySelector('[data-form-status]');

      if (!allValid) {
        if (status) {
          status.textContent = 'Please fix the highlighted fields and try again.';
          status.style.color = '#B00020';
          status.hidden = false;
        }
        const firstInvalid = form.querySelector('[aria-invalid="true"]');
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      if (status) {
        status.textContent = 'Thanks - we will reach out within two business days.';
        status.style.color = '';
        status.hidden = false;
      }
      form.reset();
      // Clear any stale invalid markers
      fields.forEach((el) => setError(el, ''));
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
