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
     Site search - accessible overlay backed by a lazy-loaded JSON index
     (site/search-index.json, emitted by scripts/generate-site.py).
     ------------------------------------------------------------------ */
  const searchRoot = document.getElementById('site-search');
  const searchTriggers = document.querySelectorAll('[data-search-open]');

  if (searchRoot && searchTriggers.length) {
    const input = searchRoot.querySelector('.site-search__input');
    const resultsEl = searchRoot.querySelector('.site-search__results');
    const statusEl = searchRoot.querySelector('.site-search__status');
    const closers = searchRoot.querySelectorAll('[data-search-close]');
    const indexUrl = searchRoot.getAttribute('data-search-index') || 'search-index.json';
    const MAX_RESULTS = 8;

    let indexPromise = null; // cached fetch - the index is fetched at most once
    let records = null;
    let lastFocused = null;
    let current = []; // result records currently rendered
    let activeIndex = -1; // keyboard-highlighted result

    const escapeHtml = (s) =>
      s.replace(/[&<>"']/g, (c) =>
        ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])
      );
    const escapeRegExp = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const tokenize = (q) => q.toLowerCase().split(/\s+/).filter(Boolean);

    const loadIndex = () => {
      if (!indexPromise) {
        indexPromise = fetch(indexUrl)
          .then((r) => {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.json();
          })
          .then((data) => {
            records = Array.isArray(data) ? data : [];
            return records;
          })
          .catch((err) => {
            indexPromise = null; // allow a retry on the next open
            throw err;
          });
      }
      return indexPromise;
    };

    // AND semantics: a record qualifies only if every term appears somewhere.
    // Title hits weigh heaviest, then description, then body.
    const search = (query) => {
      const terms = tokenize(query);
      if (!terms.length || !records) return [];
      const phrase = query.toLowerCase();
      const scored = [];

      for (const rec of records) {
        const title = (rec.t || '').toLowerCase();
        const desc = (rec.d || '').toLowerCase();
        const body = (rec.b || '').toLowerCase();
        let score = 0;
        let qualifies = true;

        for (const term of terms) {
          const inTitle = title.includes(term);
          const inDesc = desc.includes(term);
          const inBody = body.includes(term);
          if (!inTitle && !inDesc && !inBody) {
            qualifies = false;
            break;
          }
          if (inTitle) score += title.startsWith(term) ? 12 : 8;
          if (inDesc) score += 4;
          if (inBody) score += 2;
        }

        if (!qualifies) continue;
        if (title.includes(phrase)) score += 6; // exact phrase in title
        scored.push({ rec, score });
      }

      scored.sort((a, b) => b.score - a.score || a.rec.t.localeCompare(b.rec.t));
      return scored.slice(0, MAX_RESULTS).map((s) => s.rec);
    };

    // Highlight on the raw text, escaping every segment so matched terms can
    // never inject markup.
    const highlight = (text, terms) => {
      if (!terms.length) return escapeHtml(text);
      const re = new RegExp('(' + terms.map(escapeRegExp).join('|') + ')', 'gi');
      let out = '';
      let last = 0;
      let m;
      while ((m = re.exec(text)) !== null) {
        out += escapeHtml(text.slice(last, m.index)) + '<mark>' + escapeHtml(m[0]) + '</mark>';
        last = m.index + m[0].length;
        if (m.index === re.lastIndex) re.lastIndex++; // guard against zero-length matches
      }
      return out + escapeHtml(text.slice(last));
    };

    // A snippet centred on the first matching term, preferring body context.
    const snippet = (rec, terms) => {
      const haystack = rec.b && rec.b.length ? rec.b : rec.d || '';
      const lower = haystack.toLowerCase();
      let pos = -1;
      for (const term of terms) {
        const i = lower.indexOf(term);
        if (i !== -1 && (pos === -1 || i < pos)) pos = i;
      }
      const start = pos > 60 ? pos - 60 : 0;
      let slice = haystack.slice(start, start + 180);
      if (start > 0) slice = '…' + slice;
      if (start + 180 < haystack.length) slice += '…';
      return highlight(slice, terms);
    };

    const setActive = (i) => {
      const items = resultsEl.children;
      if (!items.length) {
        activeIndex = -1;
        input.removeAttribute('aria-activedescendant');
        return;
      }
      if (i < 0) i = items.length - 1;
      if (i >= items.length) i = 0;
      activeIndex = i;
      Array.from(items).forEach((li, idx) => {
        const on = idx === i;
        li.classList.toggle('is-active', on);
        li.setAttribute('aria-selected', on ? 'true' : 'false');
        if (on) {
          input.setAttribute('aria-activedescendant', li.id);
          li.scrollIntoView({ block: 'nearest' });
        }
      });
    };

    const go = (rec) => {
      if (rec && rec.u) window.location.href = rec.u;
    };

    const render = (query) => {
      const terms = tokenize(query);
      current = query ? search(query) : [];
      activeIndex = -1;
      resultsEl.innerHTML = '';
      input.removeAttribute('aria-activedescendant');

      if (!query) {
        statusEl.textContent = '';
        input.setAttribute('aria-expanded', 'false');
        return;
      }
      if (!current.length) {
        statusEl.textContent = 'No results for “' + query + '”.';
        input.setAttribute('aria-expanded', 'false');
        return;
      }

      statusEl.textContent =
        current.length + ' result' + (current.length === 1 ? '' : 's') + ' for “' + query + '”.';
      input.setAttribute('aria-expanded', 'true');

      current.forEach((rec, i) => {
        const li = document.createElement('li');
        li.className = 'site-search__result';
        li.id = 'site-search-result-' + i;
        li.setAttribute('role', 'option');
        li.setAttribute('aria-selected', 'false');

        const a = document.createElement('a');
        a.className = 'site-search__result-link';
        a.href = rec.u;
        a.tabIndex = -1;
        a.innerHTML =
          '<span class="site-search__result-title">' + highlight(rec.t || rec.u, terms) + '</span>' +
          '<span class="site-search__result-snippet">' + snippet(rec, terms) + '</span>';

        li.appendChild(a);
        li.addEventListener('mouseenter', () => setActive(i));
        li.addEventListener('click', () => go(rec));
        resultsEl.appendChild(li);
      });
    };

    const open = () => {
      if (!searchRoot.hidden) return;
      lastFocused = document.activeElement;

      // If the mobile menu is open, fold it away first so search owns the screen.
      const mm = document.querySelector('.mobile-menu');
      const mt = document.querySelector('.mobile-toggle');
      if (mm && mm.classList.contains('is-open')) {
        mm.classList.remove('is-open');
        if (mt) mt.setAttribute('aria-expanded', 'false');
      }

      searchRoot.hidden = false;
      document.body.classList.add('search-open');
      document.body.classList.remove('menu-open');
      searchTriggers.forEach((t) => t.setAttribute('aria-expanded', 'true'));

      loadIndex()
        .then(() => {
          if (input.value.trim()) render(input.value.trim());
        })
        .catch(() => {
          statusEl.textContent = 'Search is unavailable right now. Please try again later.';
        });

      requestAnimationFrame(() => {
        input.focus();
        input.select();
      });
    };

    const close = () => {
      if (searchRoot.hidden) return;
      searchRoot.hidden = true;
      document.body.classList.remove('search-open');
      searchTriggers.forEach((t) => t.setAttribute('aria-expanded', 'false'));
      if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
    };

    // Keep focus inside the panel while it is open. Result links are removed
    // from the tab order (arrow keys drive them), so this cycles input <-> close.
    const trapTab = (e) => {
      const focusable = Array.from(
        searchRoot.querySelectorAll('input, button:not([disabled])')
      ).filter((el) => el.offsetParent !== null);
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    searchTriggers.forEach((t) => t.addEventListener('click', open));
    closers.forEach((c) => c.addEventListener('click', close));
    input.addEventListener('input', () => render(input.value.trim()));

    searchRoot.addEventListener('keydown', (e) => {
      switch (e.key) {
        case 'Escape':
          e.preventDefault();
          close();
          break;
        case 'ArrowDown':
          e.preventDefault();
          setActive(activeIndex + 1);
          break;
        case 'ArrowUp':
          e.preventDefault();
          setActive(activeIndex - 1);
          break;
        case 'Enter':
          if (current.length) {
            e.preventDefault();
            go(current[activeIndex >= 0 ? activeIndex : 0]);
          }
          break;
        case 'Tab':
          trapTab(e);
          break;
        default:
          break;
      }
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
