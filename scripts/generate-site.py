#!/usr/bin/env python3
"""
One-shot site generator.

Holds the shared chrome (head, utility bar, header, mobile menu, footer) as
templates. Produces fresh HTML for:

  1. Generated stub pages, including service and case-study detail pages.
  2. Existing pages, re-emitting them with the updated chrome while preserving
     their custom <main>...</main> body.
  3. A sitemap.xml file based on the current public HTML output and CNAME.

The chrome is the single source of truth for nav links, footer links, and
social URLs. Run this once after editing the chrome to propagate everywhere.
"""

from __future__ import annotations

from datetime import datetime, timezone
from html import escape, unescape
import json
import re
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parents[1] / "site"

WORDMARK_LIGHT = (
    '<img src="/assets/logo/tcs-logo-black.svg" '
    'alt="Tata Consulting Services, PLC" '
    'class="site-header__logo-img" width="160" height="46" />'
)

WORDMARK_DARK = (
    '<img src="/assets/logo/tcs-logo-white.svg" '
    'alt="Tata Consulting Services, PLC" '
    'class="site-footer__logo-img" width="160" height="46" />'
)

ARROW = '<svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg>'

CHROME_TOP = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <script>document.documentElement.classList.add('js')</script>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" />
  <link rel="stylesheet" href="/css/base.css" />
  <link rel="stylesheet" href="/css/components.css" />{head_extra}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <div class="utility-bar">
    <div class="container utility-bar__inner">
      <a href="/find-office.html" aria-label="United Kingdom - English. Find an office in another region."><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 010 20M12 2a15 15 0 000 20"/></svg> United Kingdom - English</a>
      <a href="/investors.html">Investors</a>
      <a href="/newsroom.html">Newsroom</a>
      <a href="/alumni.html">Alumni</a>
      <a href="https://platform.tata-consulting.co.uk" rel="noopener" target="_blank" aria-label="Open the Tata Consulting Services Internal Developer Platform"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 21h8M12 18v3M7 9l-2 2 2 2M17 9l2 2-2 2M13 8l-2 6"/></svg> Platform</a>
    </div>
  </div>

  <header class="site-header">
    <div class="container site-header__inner">
      <a class="site-header__logo" href="/index.html" aria-label="Tata Consulting Services, PLC - Home">
""" + WORDMARK_LIGHT + """
      </a>

      <nav class="primary-nav" aria-label="Primary">
        <ul class="primary-nav__list">
          <li class="primary-nav__item primary-nav__item--has-mega">
            <a class="primary-nav__link" href="/services.html" aria-expanded="false" aria-haspopup="true">
              What we do
              <svg class="primary-nav__caret" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1 1l4 4 4-4"/></svg>
            </a>
            <div class="mega" role="menu">
              <div class="mega__grid">
                <div class="mega__col">
                  <h4>Build</h4>
                  <ul>
                    <li><a href="/services.html#cloud">Cloud transformation</a></li>
                    <li><a href="/services.html#ai">AI &amp; data</a></li>
                    <li><a href="/services.html#security">Cybersecurity</a></li>
                    <li><a href="/services.html#engineering">Engineering &amp; R&amp;D</a></li>
                  </ul>
                </div>
                <div class="mega__col">
                  <h4>Run</h4>
                  <ul>
                    <li><a href="/managed-services.html">Managed services</a></li>
                    <li><a href="/enterprise-applications.html">Enterprise applications</a></li>
                    <li><a href="/network-infrastructure.html">Network &amp; infrastructure</a></li>
                    <li><a href="/business-operations.html">Business operations</a></li>
                  </ul>
                </div>
                <div class="mega__col">
                  <h4>Transform</h4>
                  <ul>
                    <li><a href="/services.html#consulting">Strategy &amp; consulting</a></li>
                    <li><a href="/services.html#xd">Experience design</a></li>
                    <li><a href="/services.html#sustainability">Sustainability</a></li>
                    <li><a href="/services.html#platforms">Industry platforms</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </li>
          <li class="primary-nav__item"><a class="primary-nav__link" href="/industries.html">Industries</a></li>
          <li class="primary-nav__item"><a class="primary-nav__link" href="/insights.html">Insights</a></li>
          <li class="primary-nav__item"><a class="primary-nav__link" href="/careers.html">Careers</a></li>
          <li class="primary-nav__item"><a class="primary-nav__link" href="/about.html">About</a></li>
          <li class="primary-nav__item"><a class="primary-nav__link" href="/investors.html">Investors</a></li>
        </ul>
      </nav>

      <div class="header-cta">
        <button class="header-icon-btn" type="button" data-search-open aria-label="Search" aria-haspopup="dialog" aria-controls="site-search" aria-expanded="false">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
        </button>
        <a class="btn btn--primary" href="/contact.html">Contact us
          """ + ARROW + """
        </a>
      </div>

      <button class="mobile-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open navigation">
        <span class="mobile-toggle__bars" aria-hidden="true"><span></span><span></span><span></span></span>
      </button>
    </div>
  </header>

  <div class="mobile-menu" id="mobile-menu">
    <button class="mobile-menu__search" type="button" data-search-open aria-haspopup="dialog" aria-controls="site-search" aria-expanded="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      Search
    </button>
    <ul>
      <li><a href="/services.html">What we do</a></li>
      <li><a href="/industries.html">Industries</a></li>
      <li><a href="/insights.html">Insights</a></li>
      <li><a href="/careers.html">Careers</a></li>
      <li><a href="/about.html">About</a></li>
      <li><a href="/investors.html">Investors</a></li>
    </ul>
    <a class="btn btn--primary" href="/contact.html">Contact us
      """ + ARROW + """
    </a>
  </div>

  <div class="site-search" id="site-search" data-search-index="search-index.json" hidden>
    <div class="site-search__backdrop" data-search-close></div>
    <div class="site-search__panel" role="dialog" aria-modal="true" aria-labelledby="site-search-label">
      <h2 class="sr-only" id="site-search-label">Search this site</h2>
      <form class="site-search__form" role="search" autocomplete="off">
        <svg class="site-search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
        <input class="site-search__input" id="site-search-input" type="search" role="combobox"
               placeholder="Search services, industries, insights&hellip;" aria-label="Search this site"
               aria-controls="site-search-results" aria-expanded="false" aria-autocomplete="list"
               autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" />
        <button class="site-search__close" type="button" data-search-close aria-label="Close search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>
        </button>
      </form>
      <p class="site-search__status" id="site-search-status" role="status" aria-live="polite"></p>
      <ul class="site-search__results" id="site-search-results" role="listbox" aria-label="Search results"></ul>
    </div>
  </div>

"""

CHROME_BOTTOM = """
  <footer class="site-footer">
    <div class="container">
      <div class="newsletter">
        <div class="newsletter__copy">
          <h3>Get the Tata brief.</h3>
          <p>One email per month - the research, signals, and points of view we'd want a friend in the industry to see.</p>
        </div>
        <form class="newsletter__form" novalidate>
          <label class="sr-only" for="newsletter-email">Work email</label>
          <input id="newsletter-email" type="email" placeholder="you@company.com" autocomplete="email" />
          <button type="submit">Subscribe</button>
        </form>
      </div>

      <div class="site-footer__grid">
        <div class="site-footer__brand">
""" + WORDMARK_DARK + """
          <h3>Building on belief.</h3>
          <p>TCS Labs, PLC, a subsidiary of Tata Consultancy Services, partners with the world's largest enterprises to design, build, and run their digital transformation.</p>
        </div>
        <div class="site-footer__col">
          <h4>What we do</h4>
          <ul>
            <li><a href="/services.html#cloud">Cloud</a></li>
            <li><a href="/services.html#ai">AI &amp; data</a></li>
            <li><a href="/services.html#security">Cybersecurity</a></li>
            <li><a href="/services.html#engineering">Engineering</a></li>
            <li><a href="/services.html#consulting">Consulting</a></li>
          </ul>
        </div>
        <div class="site-footer__col">
          <h4>Industries</h4>
          <ul>
            <li><a href="/industries.html#banking">Banking</a></li>
            <li><a href="/industries.html#insurance">Insurance</a></li>
            <li><a href="/industries.html#manufacturing">Manufacturing</a></li>
            <li><a href="/industries.html#retail">Retail</a></li>
            <li><a href="/industries.html#healthcare">Healthcare</a></li>
          </ul>
        </div>
        <div class="site-footer__col">
          <h4>Company</h4>
          <ul>
            <li><a href="/about.html">About us</a></li>
            <li><a href="/leadership.html">Leadership</a></li>
            <li><a href="/careers.html">Careers</a></li>
            <li><a href="/investors.html">Investors</a></li>
            <li><a href="/newsroom.html">Newsroom</a></li>
            <li><a href="/sustainability.html">Sustainability</a></li>
          </ul>
        </div>
        <div class="site-footer__col">
          <h4>Connect</h4>
          <ul>
            <li><a href="/contact.html">Contact us</a></li>
            <li><a href="/find-office.html">Find an office</a></li>
            <li><a href="/partners.html">Partners</a></li>
            <li><a href="/alumni.html">Alumni</a></li>
            <li><a href="/vendors.html">Vendors</a></li>
            <li><a href="/insights.html">Insights</a></li>
          </ul>
        </div>
      </div>
      <div class="site-footer__legal">
        <ul>
          <li><a href="/privacy.html">Privacy notice</a></li>
          <li><a href="/cookies.html">Cookies</a></li>
          <li><a href="/terms.html">Terms of use</a></li>
          <li><a href="/accessibility.html">Accessibility</a></li>
          <li><a href="/case-studies.html">Case studies</a></li>
        </ul>
      </div>
      <div class="site-footer__bottom">
        <p>&copy; <span data-year>2026</span> TCS Labs, PLC. All rights reserved.</p>
        <div class="site-footer__social" aria-label="Social links">
          <a href="https://www.linkedin.com/company/tata-consulting-services" aria-label="LinkedIn on LinkedIn" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h14zM8.34 18.34V9.86H5.67v8.48h2.67zM7 8.68a1.54 1.54 0 110-3.08 1.54 1.54 0 010 3.08zm11.34 9.66v-4.64c0-2.49-1.33-3.65-3.1-3.65a2.67 2.67 0 00-2.43 1.34V9.86H10.13c.04.75 0 8.48 0 8.48h2.68v-4.74c0-.24.02-.48.09-.65.19-.48.63-.98 1.36-.98.96 0 1.34.73 1.34 1.8v4.57h2.74z"/></svg></a>
          <a href="https://x.com/tata_consulting" aria-label="Tata on X" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
          <a href="https://www.youtube.com/@tata-consulting" aria-label="Tata on YouTube" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a2.999 2.999 0 00-2.111-2.122C19.505 3.5 12 3.5 12 3.5s-7.505 0-9.387.564A2.999 2.999 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a2.999 2.999 0 002.111 2.122C4.495 20.5 12 20.5 12 20.5s7.505 0 9.387-.564a2.999 2.999 0 002.111-2.122C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.546 15.568V8.432L15.818 12z"/></svg></a>
          <a href="https://www.facebook.com/tataconsulting" aria-label="Tata on Facebook" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 10-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.51 1.49-3.9 3.78-3.9 1.1 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.77l-.44 2.89h-2.33v6.99A10 10 0 0022 12z"/></svg></a>
        </div>
      </div>
    </div>
  </footer>

  <script src="/js/main.js"></script>
</body>
</html>
"""


def page_hero(eyebrow: str, title: str, lead: str) -> str:
    return f"""
    <section class="page-hero">
      <div class="container page-hero__inner">
        <span class="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        <p>{lead}</p>
      </div>
    </section>
"""


def cta_strip(headline: str, btn_text: str, btn_href: str) -> str:
    return f"""
    <section class="cta-strip">
      <div class="container cta-strip__inner">
        <h2>{headline}</h2>
        <a class="btn btn--ghost-light" href="/{btn_href}">{btn_text}
          {ARROW}
        </a>
      </div>
    </section>
"""


# -- New stub pages ---------------------------------------------------------

LEADERSHIP_LEADERS = [
    ("Anand Krishnan",     "AK", "media--neon",   "Chief Executive Officer &amp; Managing Director"),
    ("Priya Iyer",         "PI", "media--ocean",  "Chief Operating Officer"),
    ("Marcus Hale",        "MH", "media--sunset", "President, Banking &amp; Financial Services"),
    ("Yuki Tanaka",        "YT", "media--forest", "Chief Technology Officer"),
    ("Sofia Reyes",        "SR", "media--ember",  "President, Europe"),
    ("Rohan Mehta",        "RM", "media--steel",  "Chief Financial Officer"),
    ("Aisha Patel",        "AP", "media--neon",   "Chief Human Resources Officer"),
    ("David Okonkwo",      "DO", "media--ocean",  "Global Head, AI &amp; Data"),
    ("Helena Bauer",       "HB", "media--sunset", "President, Insurance"),
    ("Kenji Sato",         "KS", "media--forest", "President, Manufacturing"),
    ("Lara Schmidt",       "LS", "media--ember",  "President, Retail &amp; Consumer Products"),
    ("Naila Rahman",       "NR", "media--steel",  "President, Healthcare &amp; Life Sciences"),
]


def leadership_main() -> str:
    cards = "\n".join(
        f"""          <div class="leader-card reveal">
            <div class="leader-card__photo {variant}"><span class="leader-card__initials">{initials}</span></div>
            <div class="leader-card__name">{name}</div>
            <div class="leader-card__role">{role}</div>
          </div>"""
        for (name, initials, variant, role) in LEADERSHIP_LEADERS
    )
    return (
        page_hero(
            "Leadership",
            "The people who run Tata.",
            "An operating committee of practitioners. Most of our leaders spent decades inside the disciplines they now oversee - building, delivering, and learning the hard way before stepping into leadership.",
        )
        + f"""
    <section class="section">
      <div class="container">
        <div class="section-head">
          <div class="section-head__title">
            <span class="eyebrow">Operating committee</span>
            <h2>Twelve leaders, one P&amp;L.</h2>
          </div>
        </div>
        <div class="grid grid--4">
{cards}
        </div>
      </div>
    </section>

    <section class="section section--muted">
      <div class="container">
        <div class="quote">
          <div class="quote__mark">"</div>
          <blockquote>
            The role of leadership here is to make the next generation of leaders look obvious in hindsight.
          </blockquote>
          <cite><strong>Anand Krishnan</strong> - Chief Executive Officer</cite>
        </div>
      </div>
    </section>
"""
        + cta_strip("Want to meet the team?", "Get in touch", "contact.html")
    )


CAREERS_REASONS = [
    ("Build for scale that matters", "Your code, your designs, your decisions - touching tens of millions of people, often within months of joining."),
    ("Decades-long mentorship", "Average tenure of our principal engineers is 18 years. The people teaching you have done the work."),
    ("Learn-by-doing, paid for", "$2,400 a year per employee for learning, plus full sponsorship for certifications that map to your career path."),
    ("Move with the work", "Internal mobility is the default. Forty-one percent of our consultants change role or geography every three years."),
    ("Flexible by default", "Hybrid where it works, remote where it makes sense, on-site where the client needs us. We hire for outcomes."),
    ("Health for the long game", "Comprehensive health, family, mental-health, and retirement benefits - in every country we operate."),
]


def careers_main() -> str:
    tiles = "\n".join(
        f"""          <div class="reveal" style="padding: var(--s-8) 0; border-top: 2px solid var(--brand-primary);">
            <h3 style="margin-bottom: var(--s-3);">{title}</h3>
            <p class="muted">{body}</p>
          </div>"""
        for (title, body) in CAREERS_REASONS
    )
    return (
        page_hero(
            "Careers",
            "Come build something people will still be using in twenty years.",
            "We hire engineers, designers, researchers, consultants, and operators across 55 countries. We're not for everyone. We're for people who'd rather ship the boring, durable thing than the flashy short-lived thing.",
        )
        + """
    <section class="section section--dark">
      <div class="container">
        <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
          <span class="eyebrow" style="color: var(--brand-accent);">By the numbers</span>
          <h2 style="margin-top: var(--s-3);">Hiring at scale, hiring with care.</h2>
        </div>
        <div class="stats">
          <div class="stat reveal"><div class="stat__num">615K+</div><div class="stat__label">People worldwide</div></div>
          <div class="stat reveal"><div class="stat__num">152</div><div class="stat__label">Nationalities</div></div>
          <div class="stat reveal"><div class="stat__num">39.5%</div><div class="stat__label">Women in workforce</div></div>
          <div class="stat reveal"><div class="stat__num">~80K</div><div class="stat__label">New hires last fiscal year</div></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
          <span class="eyebrow">Why join</span>
          <h2 style="margin-top: var(--s-3);">Six things you'd tell a friend after a year.</h2>
        </div>
        <div class="grid grid--3">
""" + tiles + """
        </div>
      </div>
    </section>

    <section class="section section--muted">
      <div class="container">
        <div class="section-head">
          <div class="section-head__title">
            <span class="eyebrow">Open roles</span>
            <h2>Hiring across 14 disciplines.</h2>
          </div>
          <a class="arrow-link" href="/contact.html">Browse all roles
            """ + ARROW + """
          </a>
        </div>
        <div class="grid grid--3">
          <a class="service-tile reveal" href="/contact.html">
            <h3>Software engineer - Cloud platforms</h3>
            <div class="service-tile__footer"><span class="service-tile__num">Multiple - Global</span></div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>AI/ML engineer</h3>
            <div class="service-tile__footer"><span class="service-tile__num">Bengaluru / Pune / Toronto</span></div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>Cybersecurity consultant</h3>
            <div class="service-tile__footer"><span class="service-tile__num">London / Frankfurt / Singapore</span></div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>Product designer</h3>
            <div class="service-tile__footer"><span class="service-tile__num">New York / Amsterdam</span></div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>Data engineer</h3>
            <div class="service-tile__footer"><span class="service-tile__num">Multiple - Global</span></div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>SAP S/4HANA architect</h3>
            <div class="service-tile__footer"><span class="service-tile__num">Walldorf / Mumbai</span></div>
          </a>
        </div>
      </div>
    </section>
""" + cta_strip("Don't see your role? Send us your CV anyway.", "Send a note", "contact.html"))


INVESTORS_HIGHLIGHTS = [
    ("FY25 revenue",          "$29.1B",  "+8.4% YoY in constant currency"),
    ("Operating margin",      "24.6%",   "Sustained Tier-1 IT services band"),
    ("Net new TCV signed",    "$42.7B",  "Across 1,200+ active enterprise relationships"),
    ("Cash conversion",       "112%",    "Free cash flow / net income, trailing twelve months"),
]


def investors_main() -> str:
    stats = "\n".join(
        f"""          <div class="stat reveal">
            <div class="stat__num">{value}</div>
            <div class="stat__label"><strong style="color: var(--text-strong);">{label}</strong><br>{detail}</div>
          </div>"""
        for (label, value, detail) in INVESTORS_HIGHLIGHTS
    )
    return (
        page_hero(
            "Investors",
            "A durable business, built to compound.",
            "Long-running client relationships, a global delivery model that's hard to replicate, and a balance sheet that funds growth from operating cash flow - not financing.",
        )
        + f"""
    <section class="section">
      <div class="container">
        <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
          <span class="eyebrow">Latest results - FY25</span>
          <h2 style="margin-top: var(--s-3);">Headlines from our most recent fiscal year.</h2>
        </div>
        <div class="stats">
{stats}
        </div>
      </div>
    </section>

    <section class="section section--muted">
      <div class="container">
        <div class="section-head">
          <div class="section-head__title">
            <span class="eyebrow">Reports &amp; filings</span>
            <h2>For your due diligence shelf.</h2>
          </div>
          <a class="arrow-link" href="/contact.html">Request investor pack
            {ARROW}
          </a>
        </div>
        <div class="grid grid--3">
          <a class="service-tile reveal" href="/contact.html">
            <h3>Annual report 2025</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 14.2 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>Q4 FY25 earnings transcript</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 1.1 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>Sustainability report 2025</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 8.6 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>Proxy statement 2025</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 2.3 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>Corporate governance</h3>
            <div class="service-tile__footer"><span class="service-tile__num">Code of conduct &amp; bylaws</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>Historical financials</h3>
            <div class="service-tile__footer"><span class="service-tile__num">10-year ledger</span>{ARROW}</div>
          </a>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow" style="color: var(--brand-accent); display:block; margin-bottom: var(--s-3);">Talk to IR</span>
            <h2 style="margin-bottom: var(--s-6);">Direct line to the team.</h2>
            <p style="color: var(--text-on-dark-muted); font-size: 1.0625rem; line-height: 1.6; margin-bottom: var(--s-8);">For analyst inquiries, shareholder questions, or scheduled briefings, reach our investor relations team directly.</p>
            <a class="arrow-link arrow-link--light" href="mailto:ir@tata-consulting.co.uk">ir@tata-consulting.co.uk
              {ARROW}
            </a>
          </div>
          <div class="split__media media--ocean reveal"></div>
        </div>
      </div>
    </section>
"""
    )


NEWSROOM_RELEASES = [
    ("media--ocean",  "May 14, 2026", "Press release",   "Tata expands European delivery footprint with new Madrid campus.", "Three thousand engineers, designers, and consultants will be based in the new center by 2028."),
    ("media--neon",   "Apr 28, 2026", "Press release",   "Q4 FY25 results: revenue up 8.4% YoY, margin holds at 24.6%.", "Annual revenue crosses £23B; record TCV bookings driven by AI and cloud engagements."),
    ("media--sunset", "Apr 02, 2026", "Announcement",    "Tata joins UN Climate Action Compact.", "Commits to net-zero across owned operations by 2030, full supply chain by 2040."),
    ("media--forest", "Mar 18, 2026", "Press release",   "Strategic alliance with a leading hyperscaler expands managed AI services.", "Joint go-to-market across financial services, manufacturing, and healthcare."),
    ("media--ember",  "Feb 24, 2026", "Award",           "Recognised as a Leader in the 2026 Cloud Services Magic Quadrant.", "Sixth consecutive year in the Leaders quadrant."),
    ("media--steel",  "Jan 30, 2026", "Press release",   "Tata to acquire a specialist healthcare data engineering firm.", "Strengthens life sciences delivery in North America and Europe."),
]


def newsroom_main() -> str:
    cards = "\n".join(
        f"""          <article class="story-card reveal">
            <div class="story-card__media {variant}"></div>
            <div class="story-card__body">
              <span class="story-card__tag">{date} - {kind}</span>
              <h3 class="story-card__title">{title}</h3>
              <p class="story-card__excerpt">{excerpt}</p>
              <div class="story-card__footer">
                <a class="arrow-link" href="/contact.html">Read release
                  {ARROW}
                </a>
              </div>
            </div>
          </article>"""
        for (variant, date, kind, title, excerpt) in NEWSROOM_RELEASES
    )
    return (
        page_hero(
            "Newsroom",
            "Announcements, releases, and recognitions.",
            "Where we share the things we're saying publicly - results, partnerships, awards, and the occasional point of view we feel strongly enough to put a name on.",
        )
        + f"""
    <section class="section">
      <div class="container">
        <div class="section-head">
          <div class="section-head__title">
            <span class="eyebrow">Recent</span>
            <h2>Latest announcements.</h2>
          </div>
          <a class="arrow-link" href="/newsroom.html#archive">Archive
            {ARROW}
          </a>
        </div>
        <div class="grid grid--3">
{cards}
        </div>
      </div>
    </section>

    <section class="section section--muted">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow" style="display:block; margin-bottom: var(--s-3);">Media inquiries</span>
            <h2 style="margin-bottom: var(--s-6);">Working on a story?</h2>
            <p class="muted" style="font-size: 1.0625rem; line-height: 1.6; margin-bottom: var(--s-8);">For journalist or analyst inquiries, briefings, or interview requests, our global communications team responds within one business day.</p>
            <a class="arrow-link" href="mailto:press@tata-consulting.co.uk">press@tata-consulting.co.uk
              {ARROW}
            </a>
          </div>
          <div class="split__media media--neon reveal"></div>
        </div>
      </div>
    </section>
"""
    )


FIND_OFFICE_LIST = [
    ("Mumbai - Global HQ",    "Tata House<br />N. M. Marg, Apollo Bunder<br />Mumbai 400001, India",                                                      "+91 22 6665 8282",  "+912266658282"),
    ("Bengaluru",             "Tata Park, Whitefield Main Road<br />Whitefield, Bengaluru 560066<br />India",                                              "+91 80 672 57000.",  "+918067257000"),
    ("Delhi NCR",             "Tata Tower, DLF Cyber City Phase III<br />Gurugram 122002<br />India",                                                       "+91 124 444 5555",  "+911244745235"),
    ("New York",              "101 Park Avenue, 26th Floor<br />New York, NY 10178<br />United States",                                                      "+1 212 555 0100",   "+12125550100"),
    ("Toronto",               "199 Bay Street, 30th Floor<br />Toronto, ON M5L 1G9<br />Canada",                                                             "+1 416 555 0150",   "+14165550150"),
    ("London",                "17 Old Bailey<br />London EC4M 7EG<br />United Kingdom",                                                                      "+44 20 7220 0800",  "+442072200800"),
    ("Frankfurt",             "Trianon, Mainzer Landstraße 16<br />60325 Frankfurt am Main<br />Germany",                                                    "+49 69 2222 0700",  "+496922220700"),
    ("Amsterdam",             "Vinoly Building, Claude Debussylaan 80<br />1082 MD Amsterdam<br />Netherlands",                                              "+31 20 521 0500",   "+31205210500"),
    ("Singapore",             "Marina Bay Financial Centre, Tower 3<br />12 Marina Boulevard<br />Singapore 018982",                                         "+65 6654 1550",     "+6566541550"),
    ("Tokyo",                 "Marunouchi Building, 21F<br />2-4-1 Marunouchi, Chiyoda-ku<br />Tokyo 100-6321, Japan",                                       "+81 3 5222 0900",   "+81352220900"),
    ("Sydney",                "Tower One, International Towers<br />100 Barangaroo Avenue, Sydney NSW 2000<br />Australia",                                  "+61 2 8224 0900",   "+61282240900"),
    ("São Paulo",             "Avenida Paulista, 1842<br />Bela Vista, São Paulo - SP<br />Brazil 01310-200",                                                "+55 11 3000 0400",  "+551130000400"),
]


# Offices that get a subtle highlight and a link to their own page. Keyed by
# the office name in FIND_OFFICE_LIST. London is the UK Engineering Centre of
# Excellence and has a dedicated page (london.html).
FEATURED_OFFICES = {
    "London": {"href": "coe/london.html", "badge": "Engineering Centre of Excellence"},
}


def office_card(name: str, addr: str, tel_display: str, tel_e164: str) -> str:
    feature = FEATURED_OFFICES.get(name)
    classes = "office-card reveal"
    badge = ""
    extra_link = ""
    if feature:
        classes += " office-card--featured"
        badge = f'            <span class="office-card__badge">{feature["badge"]}</span>\n'
        extra_link = (
            f'\n            <a class="office-card__link" href="/{feature["href"]}">Explore the London office'
            f'\n              {ARROW}\n            </a>'
        )
    return (
        f'          <div class="{classes}">\n'
        f'{badge}'
        f'            <h3>{name}</h3>\n'
        f'            <address>{addr}</address>\n'
        f'            <a href="tel:{tel_e164}">{tel_display}</a>{extra_link}\n'
        f'          </div>'
    )


def find_office_main() -> str:
    cards = "\n".join(
        office_card(name, addr, tel_display, tel_e164)
        for (name, addr, tel_display, tel_e164) in FIND_OFFICE_LIST
    )
    return (
        page_hero(
            "Find an office",
            "A presence in 55 countries.",
            "Twelve of our largest hubs are listed below. Whether you want to drop by, ship a contract, or hire a team near you - this is where to start.",
        )
        + f"""
    <section class="section">
      <div class="container">
        <div class="grid grid--3">
{cards}
        </div>
      </div>
    </section>
"""
        + cta_strip("Not located in a region we list?", "Talk to us", "contact.html")
    )


PARTNER_LIST = [
    ("media--neon",   "Hyperscale alliance",     "Cloud platforms",         "Co-engineering, joint go-to-market, and shared customer success across the three largest public-cloud providers."),
    ("media--ocean",  "Strategic alliance",      "Core enterprise software", "Deep delivery practices around SAP, Oracle, Microsoft, Salesforce, ServiceNow, and Workday - implementation, migration, and managed run."),
    ("media--sunset", "Technology partner",      "Data &amp; AI",            "Joint capabilities with Databricks, Snowflake, Confluent, and the leading model providers - to put AI into production, not pilots."),
    ("media--forest", "Innovation network",      "Startups &amp; ventures",  "Tata Ventures invests in and co-builds with 80+ enterprise startups. We bring them into client engagements when their tech is ready."),
    ("media--ember",  "Academic partnership",    "Research &amp; talent",    "Joint research centers with 30+ universities globally. Sponsored chairs, applied research, and a steady pipeline of graduate hires."),
    ("media--steel",  "Industry consortia",      "Standards &amp; advocacy", "Active participation in cloud, AI safety, cybersecurity, and sustainability standards bodies - shaping the rules of the road."),
]


def partners_main() -> str:
    cards = "\n".join(
        f"""          <article class="story-card reveal">
            <div class="story-card__media {variant}"></div>
            <div class="story-card__body">
              <span class="story-card__tag">{tag}</span>
              <h3 class="story-card__title">{title}</h3>
              <p class="story-card__excerpt">{body}</p>
              <div class="story-card__footer">
                <a class="arrow-link" href="/contact.html">Explore partnership
                  {ARROW}
                </a>
              </div>
            </div>
          </article>"""
        for (variant, tag, title, body) in PARTNER_LIST
    )
    return (
        page_hero(
            "Partners",
            "Strong on our own. Stronger together.",
            "We bring 615,000 people. Our partners bring the platforms, the products, the science, and the standards. Clients get the union of both - not the seams.",
        )
        + f"""
    <section class="section">
      <div class="container">
        <div class="grid grid--3">
{cards}
        </div>
      </div>
    </section>

    <section class="section section--muted">
      <div class="container">
        <div class="quote">
          <div class="quote__mark">"</div>
          <blockquote>
            Partnerships aren't a logo wall. They're a way of jointly being accountable for an outcome - which is harder, slower, and almost always worth it.
          </blockquote>
          <cite><strong>Yuki Tanaka</strong> - Chief Technology Officer</cite>
        </div>
      </div>
    </section>
"""
        + cta_strip("Become a Tata partner.", "Start the conversation", "contact.html")
    )


def alumni_main() -> str:
    return (
        page_hero(
            "Alumni",
            "Once Tata. Always Tata.",
            "Over 850,000 people have been part of Tata across our history. The network you joined when you walked in is yours for life - whether you're still here or building somewhere new.",
        )
        + f"""
    <section class="section section--dark">
      <div class="container">
        <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
          <span class="eyebrow" style="color: var(--brand-accent);">The network in numbers</span>
          <h2 style="margin-top: var(--s-3);">A community that keeps showing up for itself.</h2>
        </div>
        <div class="stats">
          <div class="stat reveal"><div class="stat__num">850K+</div><div class="stat__label">Alumni globally</div></div>
          <div class="stat reveal"><div class="stat__num">140+</div><div class="stat__label">Local chapters in 60 countries</div></div>
          <div class="stat reveal"><div class="stat__num">2,400+</div><div class="stat__label">Boomerang rehires per year</div></div>
          <div class="stat reveal"><div class="stat__num">180+</div><div class="stat__label">Alumni-led events annually</div></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow" style="display:block; margin-bottom: var(--s-3);">Stay connected</span>
            <h2 style="margin-bottom: var(--s-6);">Join the alumni network.</h2>
            <p class="muted" style="font-size: 1.0625rem; line-height: 1.6; margin-bottom: var(--s-4);">Verify your alumnus status to unlock the directory, local events, mentoring, and access to internal job postings during boomerang season.</p>
            <p class="muted" style="font-size: 1.0625rem; line-height: 1.6; margin-bottom: var(--s-8);">If you left within the last five years, your verification is automatic from your last-known work email.</p>
            <a class="btn btn--primary" href="/contact.html">Verify and join
              {ARROW}
            </a>
          </div>
          <div class="split__media media--neon reveal"><img style="object-fit: cover center; width: 100%;" src="/assets/images/alumni.jpg" /></div>
        </div>
      </div>
    </section>

    <section class="section section--muted">
      <div class="container">
        <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
          <span class="eyebrow">What you get</span>
          <h2 style="margin-top: var(--s-3);">Membership benefits.</h2>
        </div>
        <div class="grid grid--3">
          <div class="reveal" style="padding: var(--s-8) 0; border-top: 2px solid var(--brand-primary);">
            <h3 style="margin-bottom: var(--s-3);">Global directory</h3>
            <p class="muted">Search 850,000+ members by skill, geography, employer, or graduation cohort.</p>
          </div>
          <div class="reveal" style="padding: var(--s-8) 0; border-top: 2px solid var(--brand-primary);">
            <h3 style="margin-bottom: var(--s-3);">Local chapters</h3>
            <p class="muted">Quarterly meetups, monthly socials, and chapter-led mentorship in your city.</p>
          </div>
          <div class="reveal" style="padding: var(--s-8) 0; border-top: 2px solid var(--brand-primary);">
            <h3 style="margin-bottom: var(--s-3);">Mentoring</h3>
            <p class="muted">Volunteer to mentor or get matched - both sides report it as the highest-value benefit.</p>
          </div>
          <div class="reveal" style="padding: var(--s-8) 0; border-top: 2px solid var(--brand-primary);">
            <h3 style="margin-bottom: var(--s-3);">Boomerang priority</h3>
            <p class="muted">Internal job postings, fast-track interviews, and credited tenure for returning alumni.</p>
          </div>
          <div class="reveal" style="padding: var(--s-8) 0; border-top: 2px solid var(--brand-primary);">
            <h3 style="margin-bottom: var(--s-3);">Continuing education</h3>
            <p class="muted">Free access to a subset of our internal learning platform across cloud, AI, and consulting.</p>
          </div>
          <div class="reveal" style="padding: var(--s-8) 0; border-top: 2px solid var(--brand-primary);">
            <h3 style="margin-bottom: var(--s-3);">Newsletter</h3>
            <p class="muted">A quarterly digest of what's changing - in Tata and in the industry.</p>
          </div>
        </div>
      </div>
    </section>
"""
        + cta_strip("Lost touch? Find your way back in.", "Reach the alumni team", "contact.html")
    )


def vendors_main() -> str:
    return (
        page_hero(
            "Vendors &amp; suppliers",
            "Working with Tata procurement.",
            "We work with thousands of suppliers globally, from hyperscalers to local hospitality vendors. This is how to register, get paid, and stay compliant.",
        )
        + f"""
    <section class="section">
      <div class="container">
        <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
          <span class="eyebrow">Onboarding</span>
          <h2 style="margin-top: var(--s-3);">Four steps to becoming an approved Tata supplier.</h2>
        </div>
        <div class="grid grid--4">
          <a class="service-tile reveal" href="/contact.html">
            <h3>Register interest</h3>
            <div class="service-tile__footer">
              <span class="service-tile__num">Step 01</span>
              {ARROW}
            </div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>Due diligence</h3>
            <div class="service-tile__footer">
              <span class="service-tile__num">Step 02</span>
              {ARROW}
            </div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>Master agreement</h3>
            <div class="service-tile__footer">
              <span class="service-tile__num">Step 03</span>
              {ARROW}
            </div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>Activate &amp; invoice</h3>
            <div class="service-tile__footer">
              <span class="service-tile__num">Step 04</span>
              {ARROW}
            </div>
          </a>
        </div>
      </div>
    </section>

    <section class="section section--muted">
      <div class="container">
        <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
          <span class="eyebrow">Policies &amp; standards</span>
          <h2 style="margin-top: var(--s-3);">What we expect from suppliers.</h2>
        </div>
        <div class="grid grid--3">
          <div class="reveal" style="padding: var(--s-8) 0; border-top: 2px solid var(--brand-primary);">
            <h3 style="margin-bottom: var(--s-3);">Code of conduct</h3>
            <p class="muted">Human rights, labor practices, anti-bribery, and environmental responsibility.</p>
          </div>
          <div class="reveal" style="padding: var(--s-8) 0; border-top: 2px solid var(--brand-primary);">
            <h3 style="margin-bottom: var(--s-3);">Information security</h3>
            <p class="muted">Baseline controls aligned to ISO 27001 / SOC 2; elevated controls for processors of client data.</p>
          </div>
          <div class="reveal" style="padding: var(--s-8) 0; border-top: 2px solid var(--brand-primary);">
            <h3 style="margin-bottom: var(--s-3);">Sustainability</h3>
            <p class="muted">Scope 1, 2, and material Scope 3 reporting for suppliers above $1M annual spend.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow" style="color: var(--brand-accent); display:block; margin-bottom: var(--s-3);">Procurement team</span>
            <h2 style="margin-bottom: var(--s-6);">Talk to a buyer.</h2>
            <p style="color: var(--text-on-dark-muted); font-size: 1.0625rem; line-height: 1.6; margin-bottom: var(--s-8);">For questions on category strategy, RFP timing, payment terms, or onboarding status, reach the regional procurement team.</p>
            <a class="arrow-link arrow-link--light" href="mailto:procurement@tata-consulting.co.uk">procurement@tata-consulting.co.uk
              {ARROW}
            </a>
          </div>
          <div class="split__media media--steel reveal"></div>
        </div>
      </div>
    </section>
"""
    )


INSIGHTS_ARTICLES = [
    ("media--forest", "Annual study - 1,200 CEOs",  "The AI Premium: where leaders are seeing returns, and where they aren't.",       "Our 12th annual CEO study tracks how AI value is concentrating - and what separates the 14% pulling away."),
    ("media--ember",  "Perspective",                  "Beyond the pilot: what it actually takes to put GenAI into production.",         "A field guide drawn from 340 enterprise GenAI deployments - what worked, what stalled, what we learned."),
    ("media--steel",  "Point of view",                "The next operating model: small teams, large autonomy, AI in the loop.",         "A framework for re-organising IT and operations around outcomes - not towers, not tickets, not handoffs."),
    ("media--neon",   "Research note",                "The cloud bill came due. Now what?",                                              "Why 62% of enterprises are returning to disciplined unit-economics conversations - and the playbook that's working."),
    ("media--ocean",  "Industry brief - Banking",     "Core modernisation in 24 months: a comparison of four playbooks.",                "Strangler, big-bang, sidecar, greenfield - the trade-offs that determine which approach actually finishes."),
    ("media--sunset", "Industry brief - Retail",      "Unified commerce: the data plumbing nobody warned you about.",                    "Why retail platforms break in the integration layer first - and the patterns that hold up under Black Friday."),
    ("media--forest", "Workforce study",              "What 8,400 frontline workers told us about AI augmentation.",                     "The largest survey of its kind reveals a surprising consensus on where AI helps - and where it gets in the way."),
    ("media--ember",  "ESG &amp; sustainability",     "Scope 3 reporting: the data engineering challenge nobody is talking about.",     "Most carbon disclosure tools assume data you don't have. Here's how four clients built the pipeline that actually works."),
    ("media--steel",  "Cybersecurity",                "Zero trust is a posture, not a product. Five enterprises explain why.",          "Architecture, identity, segmentation, telemetry, and culture - the five layers that actually have to move together."),
]


def insights_main() -> str:
    cards = "\n".join(
        f"""          <article class="story-card reveal">
            <div class="story-card__media {variant}"></div>
            <div class="story-card__body">
              <span class="story-card__tag">{tag}</span>
              <h3 class="story-card__title">{title}</h3>
              <p class="story-card__excerpt">{excerpt}</p>
              <div class="story-card__footer">
                <a class="arrow-link" href="/contact.html">Read
                  {ARROW}
                </a>
              </div>
            </div>
          </article>"""
        for (variant, tag, title, excerpt) in INSIGHTS_ARTICLES
    )
    return (
        page_hero(
            "Insights",
            "Research and perspectives from the front line.",
            "Our researchers and practitioners publish what they're learning from the engagements we actually run. No hot takes; just patterns that hold up after the second client.",
        )
        + f"""
    <section class="section">
      <div class="container">
        <div class="section-head">
          <div class="section-head__title">
            <span class="eyebrow">Featured</span>
            <h2>Reports, briefings, and points of view.</h2>
          </div>
          <a class="arrow-link" href="/contact.html">Subscribe to our newsletter
            {ARROW}
          </a>
        </div>
        <div class="grid grid--3">
{cards}
        </div>
      </div>
    </section>

    <section class="section section--muted">
      <div class="container">
        <div class="quote">
          <div class="quote__mark">"</div>
          <blockquote>
            We won't publish a finding until we've seen it work - or fail - at three clients. That's a slow rhythm. It's also why people keep reading us.
          </blockquote>
          <cite><strong>David Okonkwo</strong> - Global Head, AI &amp; Data</cite>
        </div>
      </div>
    </section>
"""
        + cta_strip("Have a question we should be researching?", "Suggest a topic", "contact.html")
    )


SUSTAINABILITY_STATS = [
    ("47%",   "Reduction in Scope 1 + 2 emissions since 2018",       ),
    ("100%",  "Renewable electricity across owned operations by 2027"),
    ("39.5%", "Women in workforce; 38% in middle management"        ),
    ("$2.4K", "Per-employee annual learning budget, all geographies"),
]


def sustainability_main() -> str:
    stats = "\n".join(
        f"""          <div class="stat reveal">
            <div class="stat__num">{n}</div>
            <div class="stat__label">{label}</div>
          </div>"""
        for (n, label) in SUSTAINABILITY_STATS
    )
    return (
        page_hero(
            "Sustainability",
            "A better tomorrow, built deliberately.",
            "We've made specific, dated commitments across planet, people, and governance. They're measured, reported externally, and reviewed by the board every quarter.",
        )
        + f"""
    <section class="section">
      <div class="container">
        <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
          <span class="eyebrow">Where we're focused</span>
          <h2 style="margin-top: var(--s-3);">Three pillars. Twenty-six commitments. One number we report against every quarter.</h2>
        </div>
        <div class="grid grid--3">
          <div class="story-card reveal">
            <div class="story-card__media media--forest"></div>
            <div class="story-card__body">
              <span class="story-card__tag">Planet</span>
              <h3 class="story-card__title">Net-zero across owned operations by 2030.</h3>
              <p class="story-card__excerpt">Renewable electricity in all owned facilities by 2027; full Scope 3 reporting by 2028; net-zero across the supply chain by 2040.</p>
            </div>
          </div>
          <div class="story-card reveal">
            <div class="story-card__media media--sunset"></div>
            <div class="story-card__body">
              <span class="story-card__tag">People</span>
              <h3 class="story-card__title">Equal opportunity by design.</h3>
              <p class="story-card__excerpt">45% women across global workforce by 2030; pay equity audited annually; mental health resources in all countries we operate.</p>
            </div>
          </div>
          <div class="story-card reveal">
            <div class="story-card__media media--steel"></div>
            <div class="story-card__body">
              <span class="story-card__tag">Governance</span>
              <h3 class="story-card__title">Trust as an operating discipline.</h3>
              <p class="story-card__excerpt">Independent board majority; third-party ethics audits annually; supplier code of conduct enforced through procurement.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container">
        <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
          <span class="eyebrow" style="color: var(--brand-accent);">Progress so far</span>
          <h2 style="margin-top: var(--s-3);">Numbers we're held to.</h2>
        </div>
        <div class="stats">
{stats}
        </div>
      </div>
    </section>

    <section class="section section--muted">
      <div class="container">
        <div class="section-head">
          <div class="section-head__title">
            <span class="eyebrow">Reports &amp; disclosures</span>
            <h2>Read the detail.</h2>
          </div>
          <a class="arrow-link" href="/contact.html">Subscribe to ESG updates
            {ARROW}
          </a>
        </div>
        <div class="grid grid--3">
          <a class="service-tile reveal" href="/contact.html">
            <h3>Sustainability report 2025</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 8.6 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>CDP climate disclosure</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 3.1 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="/contact.html">
            <h3>SASB framework alignment</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 1.8 MB</span>{ARROW}</div>
          </a>
        </div>
      </div>
    </section>
"""
        + cta_strip("Partner with us on what's next.", "Talk to the ESG team", "contact.html")
    )


def render_stats(stats: list[tuple[str, str]]) -> str:
   return "\n".join(
       f"""          <div class="stat reveal">
           <div class="stat__num">{value}</div>
           <div class="stat__label">{label}</div>
         </div>"""
       for (value, label) in stats
   )


def render_detail_panels(items: list[tuple[str, str, str]]) -> str:
   return "\n".join(
       f"""          <div class="detail-panel reveal">
           <span class="detail-panel__label">{label}</span>
           <h3>{title}</h3>
           <p>{body}</p>
         </div>"""
       for (label, title, body) in items
   )


def render_capability_tiles(items: list[tuple[str, str, str]]) -> str:
   return "\n".join(
       f"""          <div class="service-tile reveal">
           <span class="story-card__tag">{label}</span>
           <h3>{title}</h3>
           <p>{body}</p>
         </div>"""
       for (label, title, body) in items
    )


def service_graphic_svg(center: str, nodes: list[str], metrics: list[tuple[str, str]]) -> str:
   positions = [
       (36, 44, 132, 70),
       (346, 36, 138, 70),
       (346, 246, 138, 70),
       (36, 254, 132, 70),
   ]
   node_markup = []
   connector_markup = []
   for (label, (x, y, w, h)) in zip(nodes, positions):
       connector_markup.append(
           f'<path d="M {x + w / 2:.0f} {y + h / 2:.0f} Q 258 180 258 180" stroke="rgba(255,255,255,0.35)" stroke-width="2" fill="none" />'
       )
       node_markup.append(
           f"""
           <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.22)" />
           <text x="{x + w / 2}" y="{y + 40}" fill="rgba(255,255,255,0.96)" font-size="14" font-weight="700" text-anchor="middle" font-family="Inter, sans-serif">{label}</text>
"""
       )

   metric_markup = []
   for index, (value, label) in enumerate(metrics[:2]):
       x = 86 + (index * 204)
       metric_markup.append(
           f"""
           <rect x="{x}" y="304" width="150" height="44" rx="14" fill="rgba(10,15,35,0.45)" stroke="rgba(255,255,255,0.18)" />
           <text x="{x + 18}" y="330" fill="white" font-size="20" font-weight="800" font-family="Inter, sans-serif">{value}</text>
           <text x="{x + 82}" y="330" fill="rgba(255,255,255,0.72)" font-size="12" font-family="Inter, sans-serif">{label}</text>
"""
       )

   return f"""
       <svg viewBox="0 0 520 360" aria-hidden="true">
         <defs>
           <linearGradient id="service-center" x1="0%" y1="0%" x2="100%" y2="100%">
             <stop offset="0%" stop-color="rgba(255,255,255,0.24)" />
             <stop offset="100%" stop-color="rgba(255,255,255,0.08)" />
           </linearGradient>
         </defs>
         <rect x="120" y="94" width="280" height="172" rx="28" fill="url(#service-center)" stroke="rgba(255,255,255,0.22)" />
         <circle cx="260" cy="180" r="118" fill="none" stroke="rgba(255,255,255,0.1)" stroke-dasharray="6 10" />
         {''.join(connector_markup)}
         {''.join(node_markup)}
         <text x="260" y="160" fill="rgba(255,255,255,0.72)" font-size="12" font-weight="600" text-anchor="middle" letter-spacing="2" font-family="Inter, sans-serif">OPERATING MODEL</text>
         <text x="260" y="192" fill="white" font-size="28" font-weight="800" text-anchor="middle" font-family="Inter, sans-serif">{center}</text>
         <text x="260" y="220" fill="rgba(255,255,255,0.78)" font-size="13" text-anchor="middle" font-family="Inter, sans-serif">Observe · automate · recover · improve</text>
         {''.join(metric_markup)}
       </svg>
"""


def case_graphic_svg(title: str, stages: list[str], metrics: list[tuple[str, str]]) -> str:
   stage_positions = [74, 184, 296, 410]
   stage_markup = []
   for (label, x) in zip(stages, stage_positions):
       stage_markup.append(
           f"""
           <circle cx="{x}" cy="188" r="14" fill="rgba(255,255,255,0.95)" />
           <circle cx="{x}" cy="188" r="28" fill="none" stroke="rgba(255,255,255,0.2)" />
           <text x="{x}" y="235" fill="rgba(255,255,255,0.9)" font-size="12" font-weight="600" text-anchor="middle" font-family="Inter, sans-serif">{label}</text>
"""
       )

   metric_markup = []
   for index, (value, label) in enumerate(metrics[:2]):
       y = 42 + (index * 70)
       metric_markup.append(
           f"""
           <rect x="336" y="{y}" width="146" height="54" rx="16" fill="rgba(10,15,35,0.44)" stroke="rgba(255,255,255,0.18)" />
           <text x="354" y="{y + 25}" fill="white" font-size="21" font-weight="800" font-family="Inter, sans-serif">{value}</text>
           <text x="354" y="{y + 42}" fill="rgba(255,255,255,0.74)" font-size="12" font-family="Inter, sans-serif">{label}</text>
"""
       )

   return f"""
       <svg viewBox="0 0 520 360" aria-hidden="true">
         <path d="M72 188 H422" stroke="rgba(255,255,255,0.28)" stroke-width="4" stroke-linecap="round" />
         <path d="M72 188 C126 118, 188 130, 240 182 S338 254, 422 188" stroke="rgba(255,255,255,0.2)" stroke-width="3" fill="none" />
         <text x="38" y="52" fill="rgba(255,255,255,0.74)" font-size="12" font-weight="600" letter-spacing="2" font-family="Inter, sans-serif">DELIVERY TRAJECTORY</text>
         <text x="38" y="84" fill="white" font-size="28" font-weight="800" font-family="Inter, sans-serif">{title}</text>
         <text x="38" y="112" fill="rgba(255,255,255,0.78)" font-size="13" font-family="Inter, sans-serif">A four-phase program shape used to derisk transition and scale adoption.</text>
         {''.join(metric_markup)}
         {''.join(stage_markup)}
       </svg>
"""


CASE_STUDIES = [
   {
       "slug": "case-banking-cloud-native.html",
       "meta_title": "Retail bank cloud-native modernisation - Tata Consulting Services, PLC",
       "meta_description": "How Tata modernised a 220M-account retail bank to a cloud-native operating model in 18 months without customer-facing incidents.",
       "variant": "media--ocean",
       "tag": "Banking - Europe",
       "title": "Modernising a 220M-account retail bank to cloud-native in 18 months.",
       "excerpt": "70% faster time-to-market on new products; 60% reduction in run cost; zero customer-facing incidents during cutover.",
       "lead": "A European retail bank had already spent three years trying to replace its core in waves. We reset the program around domain-by-domain modernisation, an event backbone, and a managed cutover factory that could survive real regulatory scrutiny.",
       "stats": [
           ("220M", "customer accounts migrated"),
           ("18 months", "from reset to final country cutover"),
           ("70%", "faster launch cycle for new products"),
           ("0", "customer-facing incidents during cutover"),
       ],
       "graphic_title": "Core to cloud",
       "graphic_steps": ["Blueprint", "Domain APIs", "Dual run", "Cutover"],
       "graphic_metrics": [("11", "markets migrated"), ("3.8B", "daily API events")],
       "challenge": [
           "The client carried 420 downstream applications on top of a 30-year-old core, with country-specific product logic hard-coded into nightly batches. Every prior migration attempt had stalled when finance, fraud, and servicing teams discovered a dependency too late.",
           "We reframed the objective away from 'replace the core' and toward 'make product launches and resiliency materially better'. That let the bank sequence work by customer journeys, keep regulators informed with live evidence, and prove value before the final country cutover.",
       ],
       "workstreams": [
           ("Stream 01", "Core decomposition", "Deposits, cards, lending, and servicing were carved into independently releasable domains with shared policy services."),
           ("Stream 02", "Event fabric", "Kafka-backed canonical events replaced overnight file movement so risk, finance, and channels could subscribe in real time."),
           ("Stream 03", "Cutover factory", "Every rehearsal executed against the same runbooks, controls, rollback triggers, and executive command-centre dashboards."),
           ("Stream 04", "Run transition", "Managed services and SRE teams stood up 24x7 reliability coverage before the first production migration."),
       ],
       "timeline": [
           ("Months 0-3", "Program reset", "A single control tower, release calendar, and regulator-ready evidence pack replaced 17 local workstreams."),
           ("Months 4-8", "Foundations live", "Deposits and onboarding domains launched behind APIs while the legacy core still handled settlement."),
           ("Months 9-14", "Dual-run scale-up", "Cards, servicing, and customer messaging ran in parallel for six countries with automated reconciliation."),
           ("Months 15-18", "Country cutovers", "Weekend migrations completed with rehearsed rollback points, war-room telemetry, and board-level dashboards."),
       ],
       "outcomes": [
           ("Outcome 01", "Product change moved from quarters to weeks", "The retail product team can now ship rate, fee, and bundle changes through a governed API release path instead of core code freezes."),
           ("Outcome 02", "Run economics improved immediately", "Legacy mainframe demand dropped, incident triage was automated, and the bank closed four expensive manual reconciliation towers."),
           ("Outcome 03", "Reliability became measurable", "SLOs, golden signals, and resilience drills gave the COO the first real-time view of customer-impacting degradation across all markets."),
       ],
       "quote": "The difference was not just better engineering. It was a delivery model that let compliance, operations, and product teams trust the move in real time.",
       "quote_name": "Group CIO",
       "quote_role": "European retail bank",
       "related_services": [
           ("Managed services", "managed-services.html", "Reliability engineering, incident command, and managed cutover operations."),
           ("Enterprise applications", "enterprise-applications.html", "API-led channel modernisation, servicing flows, and release management."),
       ],
   },
   {
       "slug": "case-connected-factory-oem.html",
       "meta_title": "Connected factory transformation - Tata Consulting Services, PLC",
       "meta_description": "How Tata connected 40 plants for a global OEM with real-time supply, quality, and production intelligence.",
       "variant": "media--neon",
       "tag": "Manufacturing - Global OEM",
       "title": "Connected factory across 40 plants on 18 countries' production lines.",
       "excerpt": "Real-time supplier and quality data; 23% drop in unplanned downtime; $180M annualized inventory release.",
       "lead": "The OEM had a world-class engineering culture but no single operational picture of its plants. We connected machines, quality stations, suppliers, and planning systems so plant managers could act on the same signal within minutes, not days.",
       "stats": [
           ("40", "plants connected to one manufacturing fabric"),
           ("18", "countries rolled into the same operating model"),
           ("23%", "reduction in unplanned downtime"),
           ("$180M", "annualised inventory release"),
       ],
       "graphic_title": "Factory signal loop",
       "graphic_steps": ["Source", "Sense", "Predict", "Dispatch"],
       "graphic_metrics": [("96%", "quality signal coverage"), ("14 min", "average alert latency")],
       "challenge": [
           "Each plant had optimised locally around its own MES, supplier cadence, and maintenance routines. That produced heroic local performance but made global planning brittle whenever a component shortage, quality excursion, or equipment issue hit multiple regions at once.",
           "The client wanted more than dashboards. It needed plant supervisors, planners, and suppliers to work off the same operational model so schedule changes could happen mid-shift without creating hidden backlogs downstream.",
       ],
       "workstreams": [
           ("Stream 01", "Industrial data layer", "Machine telemetry, SPC systems, and maintenance signals were normalised into a shared manufacturing event model."),
           ("Stream 02", "Supplier visibility", "Tier-1 and critical Tier-2 suppliers published shipment and quality checkpoints into the same control plane."),
           ("Stream 03", "Digital twin rooms", "Plant teams used scenario boards to simulate changeovers, component shortages, and labour constraints before acting."),
           ("Stream 04", "Edge operations", "Low-latency analytics and local failover kept plants running even when wider network links degraded."),
       ],
       "timeline": [
           ("Quarter 1", "Three-plant pilot", "We proved uptime and quality use cases in one drivetrain, one body, and one final-assembly plant."),
           ("Quarter 2", "Global template", "The OEM approved a reusable plant blueprint spanning data contracts, dashboards, and local operating roles."),
           ("Quarter 3", "Supplier integration", "Critical supply-chain checkpoints were added so planners could see constrained components before shortages hit lines."),
           ("Quarter 4", "Scale and optimise", "All 40 plants moved to common signal thresholds and the network operations team took over global support."),
       ],
       "outcomes": [
           ("Outcome 01", "Maintenance became proactive", "Supervisors received failure signals early enough to shift crews and parts before stoppages cascaded across the line."),
           ("Outcome 02", "Planning freed trapped inventory", "The OEM cut safety-stock bias because demand, supply, and quality signals finally lined up in the same hour."),
           ("Outcome 03", "Plants kept autonomy without fragmentation", "Local leaders still tuned to site conditions, but they now did it within a global decision framework that scaled."),
       ],
       "quote": "We finally stopped arguing about whose spreadsheet was right. The line and the planning room were looking at the same truth.",
       "quote_name": "Chief Digital Officer",
       "quote_role": "Global industrial OEM",
       "related_services": [
           ("Network &amp; infrastructure", "network-infrastructure.html", "Industrial connectivity, edge resilience, and plant observability."),
           ("Managed services", "managed-services.html", "24x7 control-room support for shop-floor operations and supplier signals."),
       ],
       "delivered_from": {
           "heading": "Engineered by our London centre of excellence.",
           "body": "The industrial data layer, edge operations, and digital twin rooms behind this programme were built by our London Engineering Centre of Excellence - the same team behind our IoT, cloud-native, and Internal Developer Platform work.",
           "name": "London",
           "address": "17 Old Bailey<br />London EC4M 7EG<br />United Kingdom",
           "href": "coe/london.html",
           "badge": "Engineering Centre of Excellence",
       },
   },
   {
       "slug": "case-retail-continuous-delivery.html",
       "meta_title": "Retail continuous delivery transformation - Tata Consulting Services, PLC",
       "meta_description": "How Tata moved a heritage retailer from quarterly releases to continuous delivery across 1,800 stores and digital channels.",
       "variant": "media--sunset",
       "tag": "Retail - 150-year-old chain",
       "title": "From quarterly waterfalls to a release every three minutes - 1,800 stores.",
       "excerpt": "Continuous delivery across e-commerce + physical; 8x deployment frequency; 95% reduction in change-failure rate.",
       "lead": "The retailer's digital and store technology teams were moving at completely different speeds. We rebuilt the release model around product squads, feature flags, and shared telemetry so store operations could trust rapid change instead of fearing it.",
       "stats": [
           ("1,800", "stores brought into the same release model"),
           ("8x", "deployment frequency increase"),
           ("95%", "drop in change-failure rate"),
           ("3 min", "average release interval at peak"),
       ],
       "graphic_title": "Unified release train",
       "graphic_steps": ["Prioritise", "Feature flag", "Observe", "Scale"],
       "graphic_metrics": [("420", "teams onboarded"), ("98.7%", "automated test pass")],
       "challenge": [
           "The retailer had modern commerce ambitions, but store systems still depended on slow weekend release windows and manual certification. That meant even simple checkout or loyalty changes dragged through governance queues for weeks.",
           "The underlying issue was organisational. Product, store operations, payments, and merchandising all had different release calendars and different tolerance for risk. We had to make rapid delivery feel safer than slow delivery.",
       ],
       "workstreams": [
           ("Stream 01", "Platform engineering", "A shared delivery platform standardised build pipelines, secrets, progressive delivery, and rollback automation."),
           ("Stream 02", "Store-safe releases", "Feature flags, dark launches, and cohort routing let the client test store changes without nationwide exposure."),
           ("Stream 03", "Experience telemetry", "Digital and in-store journeys were monitored on the same service map so defects could be isolated quickly."),
           ("Stream 04", "Operating model reset", "Quarterly program boards were replaced with weekly product reviews and release readiness scorecards."),
       ],
       "timeline": [
           ("Month 1", "Value-stream mapping", "We identified release bottlenecks across POS, e-commerce, payments, and fulfilment."),
           ("Month 2-4", "Golden paths", "The first product teams moved to standard pipelines, automated testing, and on-call accountability."),
           ("Month 5-8", "Store rollout", "Pilot stores adopted progressive releases with playbooks for trade days, peaks, and local rollback."),
           ("Month 9-12", "Enterprise cadence", "Merchandising and operations leaders shifted planning into a continuous prioritisation rhythm."),
       ],
       "outcomes": [
           ("Outcome 01", "Trading became more responsive", "Product teams now launch promotions, fulfilment tweaks, and checkout changes around market signals instead of around release windows."),
           ("Outcome 02", "Store confidence improved", "Regional managers gained live dashboards and clear release notices so they knew what changed and how to escalate issues."),
           ("Outcome 03", "Engineering quality improved alongside speed", "Teams measured lead time, failure rate, and recovery together, which cut heroics and improved planning accuracy."),
       ],
       "quote": "We thought we had a speed problem. What we actually had was a trust problem between digital, stores, and operations.",
       "quote_name": "Chief Technology &amp; Transformation Officer",
       "quote_role": "Global retailer",
       "related_services": [
           ("Enterprise applications", "enterprise-applications.html", "Commerce, loyalty, ERP, and product workflow modernisation."),
           ("Business operations", "business-operations.html", "Store operations, workforce coordination, and fulfilment process redesign."),
       ],
   },
   {
       "slug": "case-insurance-claims-automation.html",
       "meta_title": "Insurance claims automation - Tata Consulting Services, PLC",
       "meta_description": "How Tata automated property and casualty claims for a top-10 carrier with straight-through processing and faster outcomes.",
       "variant": "media--ember",
       "tag": "Insurance - Top-10 carrier",
       "title": "Claims automated end-to-end for property &amp; casualty.",
       "excerpt": "Average resolution time 14 days → 38 hours; 91% straight-through processing; +18 NPS in 12 months.",
       "lead": "The carrier had strong digital intake but manual decisioning across triage, fraud review, and settlement. We rebuilt claims operations around process mining, orchestration, and human-in-the-loop controls so straight-through processing could scale without increasing leakage.",
       "stats": [
           ("38 hours", "average resolution time after transformation"),
           ("91%", "straight-through processing"),
           ("+18", "NPS improvement in 12 months"),
           ("14 days", "former average claim cycle time"),
       ],
       "graphic_title": "Claims decision spine",
       "graphic_steps": ["Intake", "Triage", "Decision", "Settle"],
       "graphic_metrics": [("27", "automation rulesets"), ("4.2x", "adjuster capacity gain")],
       "challenge": [
           "Digital claim submission was already live, but the real work still happened in swivel-chair handoffs between adjusters, document teams, and payment operations. As claim volumes rose, cycle times stretched and customer sentiment deteriorated.",
           "The client wanted automation without creating a black box. Any new model had to be auditable, easy to override, and explicitly tuned for complex weather, liability, and fraud scenarios.",
       ],
       "workstreams": [
           ("Stream 01", "Process mining", "We traced every manual touch, exception route, and rework pattern across home, auto, and commercial lines."),
           ("Stream 02", "Decision orchestration", "Rules, models, and document services were wrapped in a single claims workflow with visible checkpoints."),
           ("Stream 03", "Human-in-the-loop controls", "Adjusters could intervene on confidence thresholds, special handling flags, and suspicious claim combinations."),
           ("Stream 04", "Operations transition", "The operations team moved to exception management, model tuning, and proactive outreach instead of queue clearing."),
       ],
       "timeline": [
           ("Weeks 1-6", "Claims baseline", "The carrier gained a fact base on the real sources of delay, leakage, and avoidable rework."),
           ("Weeks 7-12", "Automation spine live", "Low-complexity claims began routing through rules and document services with human checkpoints."),
           ("Weeks 13-20", "Fraud and exception tuning", "Confidence thresholds and specialist routing were calibrated using live claim outcomes."),
           ("Weeks 21-32", "National rollout", "The new workflow expanded across lines of business with service-level dashboards and QA feedback loops."),
       ],
       "outcomes": [
           ("Outcome 01", "Customers stopped chasing status", "Most policyholders received a decision path and expected settlement timing within the same business day."),
           ("Outcome 02", "Adjusters focused on the right work", "Specialists spent more time on complex disputes and less time on routine triage or documentation gaps."),
           ("Outcome 03", "Controls improved while the process sped up", "Every automated decision remained explainable to auditors, regulators, and claims leadership."),
       ],
       "quote": "We didn't want a claims robot. We wanted a process that made our best people available for the claims that really need them.",
       "quote_name": "Chief Claims Officer",
       "quote_role": "Top-10 insurer",
       "related_services": [
           ("Business operations", "business-operations.html", "Claims operations redesign, process mining, and intelligent automation."),
           ("Managed services", "managed-services.html", "Workflow support, exception monitoring, and operational resilience."),
       ],
   },
   {
       "slug": "case-healthcare-member-experience.html",
       "meta_title": "Healthcare member experience platform - Tata Consulting Services, PLC",
       "meta_description": "How Tata consolidated 36 healthcare portals into one digital front door serving 22M lives.",
       "variant": "media--forest",
       "tag": "Healthcare - National payer",
       "title": "Member experience platform serving 22M lives.",
       "excerpt": "Consolidated 36 legacy portals into one digital front door; 4.7-star app store rating; 200K calls/month diverted.",
       "lead": "The payer's digital estate had grown through product launches, acquisitions, and vendor changes. We consolidated member access, care navigation, and plan servicing into a single front door that still respected market, employer, and regulatory differences behind the scenes.",
       "stats": [
           ("22M", "lives served through the new platform"),
           ("36", "legacy portals retired"),
           ("4.7", "app store rating after relaunch"),
           ("200K", "calls diverted per month"),
       ],
       "graphic_title": "Digital front door",
       "graphic_steps": ["Identify", "Navigate", "Serve", "Learn"],
       "graphic_metrics": [("14", "member journeys unified"), ("89%", "self-service completion")],
       "challenge": [
           "Members were logging into different portals for claims, benefits, pharmacy, care navigation, and provider messaging. Call-centre agents had become the human glue between systems that should already have been connected.",
           "The payer wanted a unified experience without forcing a massive backend rewrite upfront. That meant front-end coherence, API mediation, and a carefully sequenced retirement plan for legacy surfaces.",
       ],
       "workstreams": [
           ("Stream 01", "Experience blueprint", "We mapped high-friction journeys across commercial, Medicare, and employer-sponsored plans to define one front-door pattern."),
           ("Stream 02", "Identity and access", "A new identity layer gave members, providers, and caregivers context-aware access without duplicate credentials."),
           ("Stream 03", "Journey orchestration", "Claims, benefits, pharmacy, and care programs were stitched together behind APIs and notification services."),
           ("Stream 04", "Service deflection", "Agent tools and member self-service were designed together so contact-centre scripts matched digital flows."),
       ],
       "timeline": [
           ("Sprint 1-4", "Journey prioritisation", "We targeted the member tasks generating the highest avoidable call volume and the most fragmented entry points."),
           ("Sprint 5-10", "Platform foundation", "Identity, navigation, and content services shipped first so old and new journeys could coexist safely."),
           ("Sprint 11-18", "Journey migration", "Benefits, claims status, pharmacy, and care messaging moved into the new front door in waves."),
           ("Sprint 19-24", "Legacy retirement", "Portals and support scripts were decommissioned in lockstep with adoption metrics and agent feedback."),
       ],
       "outcomes": [
           ("Outcome 01", "Members found answers faster", "High-volume service requests became trackable self-service flows with fewer dead ends and clearer next steps."),
           ("Outcome 02", "Agents got a single context view", "Call-centre teams could see what the member had already tried, which shortened calls and improved first-contact resolution."),
           ("Outcome 03", "Digital experience became measurable", "Product teams now improve journeys using task completion, abandon points, and deflection data instead of anecdotes."),
       ],
       "quote": "The biggest win was not the app score. It was hearing our service teams say the digital journey finally matched the conversation they wanted to have with members.",
       "quote_name": "Chief Experience Officer",
       "quote_role": "National healthcare payer",
       "related_services": [
           ("Enterprise applications", "enterprise-applications.html", "Member platforms, CRM integration, workflow, and release operations."),
           ("Business operations", "business-operations.html", "Contact-centre redesign, service deflection, and cross-channel operations."),
       ],
   },
   {
       "slug": "case-public-sector-digital-identity.html",
       "meta_title": "Citizen identity transformation - Tata Consulting Services, PLC",
       "meta_description": "How Tata built a digital identity and service front door for 65M citizens while retiring 40 legacy systems.",
       "variant": "media--steel",
       "tag": "Public sector - National",
       "title": "Citizen identity and a single front door for 65M people.",
       "excerpt": "40 legacy systems retired behind it; 24M monthly active users; cost-per-transaction down 82%.",
       "lead": "The agency needed a single digital front door, but public trust depended on making identity feel safe, accessible, and explainable. We designed the service around verified identity, assisted channels, and a migration plan that retired old systems only when adoption proved stable.",
       "stats": [
           ("65M", "citizens in scope"),
           ("24M", "monthly active users"),
           ("40", "legacy systems retired"),
           ("82%", "lower cost per transaction"),
       ],
       "graphic_title": "Citizen identity spine",
       "graphic_steps": ["Verify", "Consent", "Serve", "Assist"],
       "graphic_metrics": [("99.95%", "service availability"), ("17", "agencies onboarded")],
       "challenge": [
           "Citizens were being redirected across departmental portals, each with separate credentials, inconsistent identity proofing, and uneven accessibility. At the same time, the agency had to preserve assisted channels for people who could not or would not use digital self-service.",
           "The programme carried unusual scrutiny from parliament, watchdogs, and civil society groups. Technical reliability mattered, but clear governance and service transparency mattered just as much.",
       ],
       "workstreams": [
           ("Stream 01", "Identity foundation", "Proofing, authentication, and delegated access flows were designed for both digital-first and assisted use cases."),
           ("Stream 02", "Agency onboarding", "Departments integrated through shared APIs, consent controls, and reusable service patterns instead of bespoke portals."),
           ("Stream 03", "Accessibility at scale", "Design, content, and engineering teams tested with assistive technologies and real user cohorts from the start."),
           ("Stream 04", "Operations and trust", "A live control room tracked performance, fraud signals, accessibility issues, and assisted-channel demand in one place."),
       ],
       "timeline": [
           ("Phase 1", "Identity beta", "The agency launched identity proofing and basic account services with strong monitoring and assisted fallback."),
           ("Phase 2", "Priority services", "High-volume transactions moved first so the team could learn from real demand and support patterns."),
           ("Phase 3", "Department migration", "Legacy portals were retired in waves once adoption, accessibility, and support metrics cleared agreed thresholds."),
           ("Phase 4", "National scale", "The platform expanded into a common front door for multiple agencies with centralised service operations."),
       ],
       "outcomes": [
           ("Outcome 01", "Citizens saw one coherent service", "The experience shifted from navigating departments to completing outcomes, regardless of which agency owned the transaction."),
           ("Outcome 02", "Trust improved through transparency", "Performance, accessibility, and identity controls were visible to leadership and easy to explain to oversight bodies."),
           ("Outcome 03", "Agencies stopped rebuilding the same foundations", "Identity, notifications, and service patterns became reusable capabilities rather than duplicated programs."),
       ],
       "quote": "The programme earned credibility because it never asked citizens to trust a black box. The experience was simple, but the governance was visible.",
       "quote_name": "Director General, Digital Services",
       "quote_role": "National public services organisation",
       "related_services": [
           ("Managed services", "managed-services.html", "Platform operations, resilience, and executive control-room reporting."),
           ("Business operations", "business-operations.html", "Assisted service redesign, workflow, and service performance management."),
       ],
   },
   {
       "slug": "case-energy-grid-edge-intelligence.html",
       "meta_title": "Grid-edge intelligence case study - Tata Consulting Services, PLC",
       "meta_description": "How Tata helped a European utility build grid-edge intelligence across nine countries and reduce customer outage minutes.",
       "variant": "media--ocean",
       "tag": "Energy - European utility",
       "title": "Grid-edge intelligence across 9 countries.",
       "excerpt": "Outage detection sub-90s on average; renewables integration 38% faster; customer-facing outage minutes down 41%.",
       "lead": "The utility had modernised generation forecasting, but its distribution operations still relied on fragmented alarm consoles and regional workflows. We built a grid-edge intelligence layer that joined asset, weather, field, and customer signals fast enough to change operational decisions in flight.",
       "stats": [
           ("9", "countries on one edge-operations model"),
           ("<90s", "average outage detection time"),
           ("38%", "faster renewables integration"),
           ("41%", "fewer customer outage minutes"),
       ],
       "graphic_title": "Grid event orchestration",
       "graphic_steps": ["Detect", "Correlate", "Dispatch", "Restore"],
       "graphic_metrics": [("2.4M", "smart-edge signals/hr"), ("6", "regional control rooms")],
       "challenge": [
           "Grid telemetry, field operations, weather services, and customer communications all existed, but they were consumed by different teams on different tools. That made it difficult to isolate faults quickly or rebalance crews during severe weather and renewables volatility.",
           "The utility wanted a system that operators would actually trust in the middle of an event. That meant strong correlation logic, clear confidence signals, and field workflows that stayed usable under pressure.",
       ],
       "workstreams": [
           ("Stream 01", "Edge telemetry model", "Substation, feeder, meter, and weather signals were normalised into a shared event backbone."),
           ("Stream 02", "Correlation engine", "Signal fusion narrowed likely fault locations and surfaced recommended dispatch paths with visible confidence scores."),
           ("Stream 03", "Field integration", "Dispatch, crew availability, and restoration progress were connected to the same operations workspace."),
           ("Stream 04", "Resilience drills", "Regional teams rehearsed storm scenarios using the new tooling before it became the default operating model."),
       ],
       "timeline": [
           ("Wave 1", "Regional pilot", "Two control rooms and one severe-weather corridor adopted the event model and dispatch workspace."),
           ("Wave 2", "Signal expansion", "DER, smart-meter, and weather feeds increased correlation quality and narrowed false positives."),
           ("Wave 3", "Field rollout", "Crew, contractor, and customer-notification flows moved into the same operational cadence."),
           ("Wave 4", "Cross-border scale", "Nine-country operations teams adopted shared thresholds and joint storm playbooks."),
       ],
       "outcomes": [
           ("Outcome 01", "Operators acted on stronger evidence", "Fewer alarms required manual correlation and dispatchers saw restoration options before customers started calling."),
           ("Outcome 02", "Renewables variability became manageable", "The utility could integrate more distributed generation without overwhelming regional operations teams."),
           ("Outcome 03", "Storm response matured materially", "Control rooms, crews, and communications teams finally worked from the same event picture during peak disruption."),
       ],
       "quote": "Our control rooms stopped being collectors of alarms and became decision centres.",
       "quote_name": "Chief Operations Officer",
       "quote_role": "European utility",
       "related_services": [
           ("Network &amp; infrastructure", "network-infrastructure.html", "Grid connectivity, edge compute, and resilient operations."),
           ("Managed services", "managed-services.html", "24x7 operations support, observability, and recovery engineering."),
       ],
   },
   {
       "slug": "case-telco-5g-bss-modernisation.html",
       "meta_title": "5G core and BSS modernisation - Tata Consulting Services, PLC",
       "meta_description": "How Tata launched 5G core services and modernised BSS in parallel for a tier-1 telecommunications operator.",
       "variant": "media--neon",
       "tag": "Comms - Tier-1 telco",
       "title": "5G core launch and BSS modernisation in parallel.",
       "excerpt": "First 5G slice live in 9 months; OSS migration with zero net-new tickets to support; 2x faster new-product launches.",
       "lead": "The operator could not afford to sequence network and commercial transformation one after the other. We ran 5G core rollout, product catalogue redesign, and BSS simplification in parallel so the business could monetise new network capability as soon as it went live.",
       "stats": [
           ("9 months", "to first live 5G slice"),
           ("2x", "faster new-product launches"),
           ("0", "net-new support tickets after OSS migration"),
           ("14", "legacy product stacks retired"),
       ],
       "graphic_title": "Network to revenue",
       "graphic_steps": ["Design", "Slice", "Monetise", "Support"],
       "graphic_metrics": [("42", "catalogue simplifications"), ("99.99%", "core availability")],
       "challenge": [
           "The telco's network teams were ready to launch 5G services, but product, billing, and service assurance stacks were too fragmented to support rapid commercialisation. Launching network capability without BSS reform would have created a shiny technical win with slow revenue impact.",
           "The programme had to preserve service continuity for existing customers while simplifying product logic, migrating assurance tooling, and training support operations on new service behaviours.",
       ],
       "workstreams": [
           ("Stream 01", "5G core rollout", "Cloud-native network functions, observability, and resilience patterns were implemented with slice readiness from day one."),
           ("Stream 02", "Product catalogue reset", "The commercial catalogue was reduced and rebuilt around reusable product components instead of custom bundle logic."),
           ("Stream 03", "OSS/BSS migration", "Assurance, fulfilment, and billing workflows were reconnected to the new service model without duplicating support queues."),
           ("Stream 04", "Support readiness", "Operations teams rehearsed new-service incidents and commercial edge cases before public launch."),
       ],
       "timeline": [
           ("Month 1-3", "Parallel foundations", "Network, product, and support leaders aligned around one release path instead of separate programs."),
           ("Month 4-6", "Catalogue and core build", "Reusable product components and slice-ready network services progressed against shared milestones."),
           ("Month 7-8", "Dress rehearsals", "Revenue, support, and assurance teams validated service activation, billing, and incident handling in live-like conditions."),
           ("Month 9", "Commercial launch", "The first slice and associated product offers launched together, shortening the path from capability to revenue."),
       ],
       "outcomes": [
           ("Outcome 01", "New network services became sellable immediately", "The operator reduced the lag between technical launch and commercial availability that usually slows telco transformation."),
           ("Outcome 02", "Support absorbed change without chaos", "Because OSS and service operations were redesigned alongside the product stack, incident volume stayed flat through launch."),
           ("Outcome 03", "Future launches got easier", "Teams now add new commercial variants through reusable catalogue components instead of another hard-coded bundle tree."),
       ],
       "quote": "The programme worked because we stopped treating network readiness and commercial readiness as separate definitions of done.",
       "quote_name": "Chief Technology &amp; Information Officer",
       "quote_role": "Tier-1 telecom operator",
       "related_services": [
           ("Network &amp; infrastructure", "network-infrastructure.html", "5G core, edge, OSS, and observability transformation."),
           ("Enterprise applications", "enterprise-applications.html", "Product catalogue, billing, CRM, and release orchestration."),
       ],
   },
   {
       "slug": "case-airline-loyalty-unification.html",
       "meta_title": "Airline loyalty unification - Tata Consulting Services, PLC",
       "meta_description": "How Tata unified a loyalty platform across nine airline sub-brands and unlocked incremental revenue.",
       "variant": "media--sunset",
       "tag": "Travel - Global airline",
       "title": "Loyalty platform unified across 9 sub-brands.",
       "excerpt": "Single member view across the group; +24% repeat booking; +$310M incremental revenue in year one.",
       "lead": "The airline group had accumulated brands, alliances, and loyalty rules faster than it could rationalise them. We designed a shared loyalty spine with local brand flexibility so members finally experienced one programme even when the back-end economics stayed market-specific.",
       "stats": [
           ("9", "sub-brands unified"),
           ("+24%", "repeat booking uplift"),
           ("$310M", "incremental year-one revenue"),
           ("1", "single member profile per traveller"),
       ],
       "graphic_title": "Loyalty revenue engine",
       "graphic_steps": ["Unify", "Recognise", "Reward", "Retain"],
       "graphic_metrics": [("62M", "member profiles merged"), ("4 weeks", "campaign cycle time")],
       "challenge": [
           "Members could earn and redeem across the group, but profile data, pricing rules, and campaign tooling were still fragmented by brand. Marketing teams could not act on traveller behaviour fast enough, and customer service teams had no trustworthy single view of a member.",
           "The airline needed group-level loyalty economics with market-level flexibility. That required more than a database consolidation; it required a new operating model for campaigns, pricing, and member support.",
       ],
       "workstreams": [
           ("Stream 01", "Identity and profile merge", "Traveller data was matched into a single member spine with transparent survivorship rules and support workflows."),
           ("Stream 02", "Earning and redemption logic", "Shared loyalty services handled points, tiers, partner rules, and offer orchestration across all brands."),
           ("Stream 03", "Campaign operations", "Marketing teams shifted from quarterly batch planning to near-real-time traveller segmentation and experiment design."),
           ("Stream 04", "Service integration", "Contact-centre and airport teams accessed one member view with brand-specific context layered on top."),
       ],
       "timeline": [
           ("Stage 1", "Programme blueprint", "The group agreed on shared member concepts, local exceptions, and a phased migration path."),
           ("Stage 2", "Profile unification", "Identity, consent, and historic activity moved into a common member model with rigorous data-quality checks."),
           ("Stage 3", "Commercial activation", "Offer, campaign, and redemption services went live brand by brand without disrupting live bookings."),
           ("Stage 4", "Group optimisation", "The airline began running loyalty experiments and lifecycle plays at the group level with market-specific controls."),
       ],
       "outcomes": [
           ("Outcome 01", "Members experienced the group as one programme", "Travellers could see status, balances, and offers consistently instead of interpreting multiple brand-specific views."),
           ("Outcome 02", "Marketing got a much shorter feedback loop", "The group now tunes offers and tiers using current behaviour rather than waiting for delayed monthly data snapshots."),
           ("Outcome 03", "Support conversations improved materially", "Airport, digital, and contact-centre teams work from the same member history, reducing escalations and compensation leakage."),
       ],
       "quote": "The programme let us keep the personality of each brand while finally behaving like one group when it mattered to the customer.",
       "quote_name": "Chief Commercial Officer",
       "quote_role": "Global airline group",
       "related_services": [
           ("Enterprise applications", "enterprise-applications.html", "Loyalty, CRM, pricing, and campaign platform modernisation."),
           ("Business operations", "business-operations.html", "Customer operations, service enablement, and revenue workflow redesign."),
       ],
   },
]


CASE_STUDIES_BY_SLUG = {study["slug"]: study for study in CASE_STUDIES}


RUN_SERVICE_PAGES = [
   {
       "slug": "managed-services.html",
       "meta_title": "Managed services - Tata Consulting Services, PLC",
       "meta_description": "Outcome-led managed services spanning reliability engineering, observability, service operations, and run-cost optimisation.",
       "variant": "media--ocean",
       "eyebrow": "Run / Managed services",
       "title": "Managed services that make reliability feel routine.",
       "lead": "We take accountability for hybrid estates, service operations, observability, and resilience for clients that cannot afford drama in production. The model is outcome-led: fewer incidents, faster recovery, sharper run economics, and a technology estate that gets better while it runs.",
       "intro": [
           "Our managed services teams combine platform engineering, site reliability, service management, and operational analytics in the same run model. That matters because most client pain does not sit neatly inside a single tower anymore.",
           "We typically begin with a ninety-day stabilisation plan, then move into automation, resilience engineering, and commercial baselining so the operating model keeps compounding instead of settling into reactive support.",
       ],
       "stats": [
           ("99.98%", "critical-service availability across run towers"),
           ("36%", "lower incident volume in year one"),
           ("24x7", "follow-the-sun command coverage"),
           ("43%", "L1/L2 automation after stabilisation"),
       ],
       "graphic_center": "Run command centre",
       "graphic_nodes": ["Telemetry", "SRE", "Automation", "Service desk"],
       "graphic_metrics": [("24x7", "coverage"), ("43%", "automated")],
       "graphic_caption": "A typical managed-services operating model joins observability, command, automation, and service experience into one accountable run spine.",
       "capabilities": [
           ("Capability 01", "Integrated command centre", "A single operational picture across infrastructure, applications, cloud, service demand, and business-impact signals."),
           ("Capability 02", "Reliability engineering", "SLOs, error budgets, resilience rehearsals, recovery design, and the engineering discipline to reduce recurring failure."),
           ("Capability 03", "AIOps and automation", "Signal correlation, self-healing, change-risk controls, and runbook automation that reduce toil instead of shifting it."),
           ("Capability 04", "Service experience", "Multilingual service desk, executive reporting, and clear user-facing communications when issues do happen."),
       ],
       "operating_model": [
           ("Phase 01", "Stabilise fast", "We establish a run baseline, map service criticality, and remove the biggest sources of repeat failure within the first ninety days."),
           ("Phase 02", "Instrument everything", "Golden signals, dependency maps, and business-service views make incident prioritisation and change approval materially better."),
           ("Phase 03", "Improve the run every quarter", "Each QBR tracks automation yield, resilience posture, run-cost takeout, and the next backlog of engineering improvements."),
       ],
       "related_cases": ["case-banking-cloud-native.html", "case-energy-grid-edge-intelligence.html"],
   },
   {
       "slug": "enterprise-applications.html",
       "meta_title": "Enterprise applications - Tata Consulting Services, PLC",
       "meta_description": "Run and modernise enterprise applications across SAP, Oracle, Salesforce, ServiceNow, Workday, commerce, and custom workflow platforms.",
       "variant": "media--sunset",
       "eyebrow": "Run / Enterprise applications",
       "title": "Enterprise applications that release like products, not projects.",
       "lead": "We run and modernise the platforms that move finance, supply chain, loyalty, claims, employee services, and customer journeys. Our focus is not just system uptime; it is clean releases, usable workflows, and a support model that improves the application estate rather than freezing it.",
       "intro": [
           "Most large enterprises now depend on a blend of packaged platforms and custom workflows. The failure mode is familiar: every application team optimises locally while change risk, backlog, and support debt accumulate globally.",
           "We organise around products and business journeys, joining application operations with release engineering, observability, and service experience so every platform can evolve without destabilising the business around it.",
       ],
       "stats": [
           ("14K+", "SAP, Oracle, Salesforce, ServiceNow, and Workday specialists"),
           ("31%", "faster release cadence after operating-model reset"),
           ("96%", "change success rate on governed enterprise releases"),
           ("22%", "reduction in support backlog age"),
       ],
       "graphic_center": "Application spine",
       "graphic_nodes": ["ERP", "CRM", "Workflow", "Integration"],
       "graphic_metrics": [("96%", "release success"), ("31%", "faster cadence")],
       "graphic_caption": "The run model blends application support, release automation, product ownership, and integration observability around the journeys the business actually cares about.",
       "capabilities": [
           ("Capability 01", "ERP and finance operations", "Core finance, procurement, planning, and supply-chain platforms supported with release discipline and business continuity controls."),
           ("Capability 02", "Customer and commerce platforms", "CRM, service, loyalty, and commerce journeys run with integrated telemetry and product-aligned support squads."),
           ("Capability 03", "Employee and workflow systems", "HR, case management, and operational workflow platforms that need both reliability and fast policy change."),
           ("Capability 04", "Integration and release engineering", "API, middleware, data, and test automation capabilities that keep the estate coherent as platforms evolve."),
       ],
       "operating_model": [
           ("Phase 01", "Product-aligned squads", "Support, engineering, and business owners share one backlog and one release view for each major journey."),
           ("Phase 02", "Continuous verification", "Regression packs, synthetic tests, and rollout guardrails catch business-impacting change before users do."),
           ("Phase 03", "Value and license discipline", "Application run is tied to adoption, backlog health, and platform economics rather than ticket closure alone."),
       ],
       "related_cases": ["case-healthcare-member-experience.html", "case-airline-loyalty-unification.html"],
   },
   {
       "slug": "network-infrastructure.html",
       "meta_title": "Network & infrastructure - Tata Consulting Services, PLC",
       "meta_description": "Modernise and run hybrid infrastructure, workplace, network, edge, and resilience foundations for critical enterprises.",
       "variant": "media--steel",
       "eyebrow": "Run / Network & infrastructure",
       "title": "Networks and infrastructure built for resilience, not just reach.",
       "lead": "We design, run, and optimise the hybrid foundations that everything else depends on: cloud landing zones, data centres, workplace, wide-area networks, industrial edge, and the observability needed to keep them healthy under real load.",
       "intro": [
           "Infrastructure programmes often over-focus on migration while under-investing in the discipline required to operate the target state. That is why costs creep, visibility fragments, and incidents still take too long to isolate even after the platform 'modernises'.",
           "Our model brings architecture, reliability, and day-two operations together from the start, so every transformation includes the tooling, standards, and operating rhythm required to keep the estate stable at scale.",
       ],
       "stats": [
           ("4.8M", "managed endpoints, devices, and edge nodes"),
           ("41%", "faster incident isolation on modernised estates"),
           ("92%", "policy compliance on governed infrastructure baselines"),
           ("30%", "lower WAN and hosting spend after optimisation"),
       ],
       "graphic_center": "Hybrid foundation",
       "graphic_nodes": ["Cloud", "WAN", "Workplace", "Edge"],
       "graphic_metrics": [("41%", "faster isolation"), ("92%", "policy aligned")],
       "graphic_caption": "Our infrastructure model connects landing zones, workplace, edge, and network telemetry into one resilient operating baseline instead of four separate support towers.",
       "capabilities": [
           ("Capability 01", "Hybrid cloud foundations", "Landing zones, identity, policy, observability, and cost controls that make cloud estates operable at enterprise scale."),
           ("Capability 02", "Network transformation", "Campus, branch, SD-WAN, core, and telco-grade network modernisation tied to clear resilience and performance outcomes."),
           ("Capability 03", "Digital workplace", "Endpoint, collaboration, field, and workplace services designed around user productivity and support quality."),
           ("Capability 04", "Edge and cyber-resilient infrastructure", "Industrial sites, grid edges, telco stacks, and critical environments that demand local survivability and central visibility."),
       ],
       "operating_model": [
           ("Phase 01", "Design for day-two operations", "We define supportability, observability, and failover patterns before the first migration or rollout begins."),
           ("Phase 02", "Automate provisioning and policy", "Golden paths, zero-touch deployment, and compliance controls reduce configuration drift and ticket demand."),
           ("Phase 03", "Rehearse resilience", "Major incident drills, capacity stress, and regional failover tests become a standing operating discipline."),
       ],
       "related_cases": ["case-energy-grid-edge-intelligence.html", "case-telco-5g-bss-modernisation.html"],
   },
   {
       "slug": "business-operations.html",
       "meta_title": "Business operations - Tata Consulting Services, PLC",
       "meta_description": "Transform and run business operations across claims, finance, procurement, customer service, and intelligent operations.",
       "variant": "media--ember",
       "eyebrow": "Run / Business operations",
       "title": "Business operations that scale without adding friction.",
       "lead": "We redesign and run the processes that customers and employees feel when technology hands off to operations: claims, finance, service, fulfilment, workforce, and the control structures that keep those journeys fast, compliant, and measurable.",
       "intro": [
           "Operations teams are often asked to absorb the mess left behind by fragmented systems and slow policy change. We start by making the work visible with process mining, service metrics, and frontline evidence, then redesign the operating model around flow instead of queues.",
           "The result is not just lower cost-to-serve. Clients get faster outcomes, clearer controls, and a workforce that spends more time on exceptions, empathy, and value-added judgement instead of repetitive manual routing.",
       ],
       "stats": [
           ("91%", "straight-through processing on mature operations flows"),
           ("28%", "faster cash and case cycle times"),
           ("18 pts", "average service-experience uplift"),
           ("35%", "lower cost-to-serve after redesign"),
       ],
       "graphic_center": "Operations control",
       "graphic_nodes": ["Process mining", "Workflow", "Automation", "Frontline"],
       "graphic_metrics": [("91%", "STP"), ("35%", "lower cost")],
       "graphic_caption": "The operating model links process insight, workflow orchestration, automation, and frontline enablement so improvement sticks after go-live.",
       "capabilities": [
           ("Capability 01", "Finance and back-office operations", "Order-to-cash, procure-to-pay, record-to-report, and controls transformation tied to measurable cycle-time improvement."),
           ("Capability 02", "Customer and service operations", "Contact-centre, case, and field-service models designed for channel clarity and better experience outcomes."),
           ("Capability 03", "Industry-specific operations", "Claims, care operations, fulfilment, and other domain-heavy processes where compliance and empathy both matter."),
           ("Capability 04", "Intelligent operations", "Process mining, workflow, automation, and quality controls that reduce rework without creating a brittle black box."),
       ],
       "operating_model": [
           ("Phase 01", "Baseline the real work", "We use process, service, and human evidence to quantify where flow breaks, where rework starts, and which controls matter."),
           ("Phase 02", "Redesign around outcomes", "Queues, rules, tooling, and team roles are rebuilt around end-to-end completion instead of local utilisation metrics."),
           ("Phase 03", "Manage by signal", "Operations leaders gain live views of cycle time, exceptions, quality, and experience so improvement becomes an operating habit."),
       ],
       "related_cases": ["case-insurance-claims-automation.html", "case-retail-continuous-delivery.html"],
   },
]


RUN_SERVICE_PAGES_BY_SLUG = {page["slug"]: page for page in RUN_SERVICE_PAGES}


def render_related_case_cards(case_slugs: list[str]) -> str:
   cards = []
   for slug in case_slugs:
       study = CASE_STUDIES_BY_SLUG[slug]
       cards.append(
           f"""          <article class="story-card reveal">
           <div class="story-card__media {study["variant"]}"></div>
           <div class="story-card__body">
             <span class="story-card__tag">{study["tag"]}</span>
             <h3 class="story-card__title">{study["title"]}</h3>
             <p class="story-card__excerpt">{study["excerpt"]}</p>
             <div class="story-card__footer">
               <a class="arrow-link" href="/{study["slug"]}">Read the case
                 {ARROW}
               </a>
             </div>
           </div>
         </article>"""
       )
   return "\n".join(cards)


def render_related_service_tiles(services: list[tuple[str, str, str]]) -> str:
   return "\n".join(
       f"""          <a class="service-tile reveal" href="{href}">
           <span class="story-card__tag">Related capability</span>
           <h3>{title}</h3>
           <p>{body}</p>
           <div class="service-tile__footer">
             <span class="service-tile__num">Explore</span>
             {ARROW}
           </div>
         </a>"""
       for (title, href, body) in services
   )


def service_detail_main(cfg: dict) -> str:
   stats = render_stats(cfg["stats"])
   capabilities = render_capability_tiles(cfg["capabilities"])
   operating_model = render_detail_panels(cfg["operating_model"])
   related_cases = render_related_case_cards(cfg["related_cases"])
   graphic = service_graphic_svg(cfg["graphic_center"], cfg["graphic_nodes"], cfg["graphic_metrics"])
   return (
       page_hero(cfg["eyebrow"], cfg["title"], cfg["lead"])
       + f"""
   <section class="section">
     <div class="container">
       <div class="split">
         <div class="split__body reveal">
           <h2>What this service category is built to do.</h2>
           <p>{cfg["intro"][0]}</p>
           <p>{cfg["intro"][1]}</p>
           <a class="arrow-link" href="contact.html">Talk to a Run partner
             {ARROW}
           </a>
         </div>
         <div class="reveal">
           <div class="detail-graphic {cfg["variant"]}">
{graphic}
           </div>
           <p class="detail-caption">{cfg["graphic_caption"]}</p>
         </div>
       </div>
     </div>
   </section>

   <section class="section section--dark">
     <div class="container">
       <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
         <span class="eyebrow" style="color: var(--brand-accent);">Outcomes we manage to</span>
         <h2 style="margin-top: var(--s-3);">The run metrics clients hold us to.</h2>
       </div>
       <div class="stats">
{stats}
       </div>
     </div>
   </section>

   <section class="section section--muted">
     <div class="container">
       <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
         <span class="eyebrow">Core capabilities</span>
         <h2 style="margin-top: var(--s-3);">The workstreams inside the run model.</h2>
       </div>
       <div class="grid grid--4">
{capabilities}
       </div>
     </div>
   </section>

   <section class="section">
     <div class="container">
       <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
         <span class="eyebrow">How we operate</span>
         <h2 style="margin-top: var(--s-3);">A disciplined rhythm from stabilisation to continuous improvement.</h2>
       </div>
       <div class="grid grid--3">
{operating_model}
       </div>
     </div>
   </section>

   <section class="section section--dark">
     <div class="container">
       <div class="section-head">
         <div class="section-head__title">
           <span class="eyebrow" style="color: var(--brand-accent);">Where it shows up</span>
           <h2>Case studies that map to this service.</h2>
         </div>
         <a class="arrow-link arrow-link--light" href="/case-studies.html">See all case studies
           {ARROW}
         </a>
       </div>
       <div class="grid grid--2">
{related_cases}
       </div>
     </div>
   </section>
"""
       + cta_strip("Need a run model that improves every quarter?", "Start the conversation", "contact.html")
   )


def render_delivered_from(info: dict | None) -> str:
   """Optional "Delivered from" band tying a case to a Tata office.

   Rendered only when a case config supplies a ``delivered_from`` block, so the
   shared case template stays unchanged for cases without a featured location.
   """
   if not info:
       return ""
   return f"""
   <section class="section section--muted" aria-labelledby="delivered-from-title">
     <div class="container">
       <div class="split">
         <div class="split__body reveal">
           <span class="eyebrow" style="display:block; margin-bottom: var(--s-3);">Delivered from</span>
           <h2 id="delivered-from-title">{info["heading"]}</h2>
           <p>{info["body"]}</p>
           <a class="arrow-link" href="/{info["href"]}">Explore the London office
             {ARROW}
           </a>
         </div>
         <div class="reveal">
           <div class="office-card office-card--featured">
             <span class="office-card__badge">{info["badge"]}</span>
             <h3>{info["name"]}</h3>
             <address>{info["address"]}</address>
             <a class="office-card__link" href="{info["href"]}">Explore the London office
               {ARROW}
             </a>
           </div>
         </div>
       </div>
     </div>
   </section>"""


def case_detail_main(cfg: dict) -> str:
   stats = render_stats(cfg["stats"])
   workstreams = render_capability_tiles(cfg["workstreams"])
   timeline = render_detail_panels(cfg["timeline"])
   outcomes = render_detail_panels(cfg["outcomes"])
   related_services = render_related_service_tiles(cfg["related_services"])
   graphic = case_graphic_svg(cfg["graphic_title"], cfg["graphic_steps"], cfg["graphic_metrics"])
   delivered_from = render_delivered_from(cfg.get("delivered_from"))
   return (
       page_hero("Case study", cfg["title"], cfg["lead"])
       + f"""
   <section class="section">
     <div class="container">
       <div class="stats">
{stats}
       </div>
     </div>
   </section>

   <section class="section section--muted">
     <div class="container">
       <div class="split">
         <div class="split__body reveal">
           <h2>The situation we walked into.</h2>
           <p>{cfg["challenge"][0]}</p>
           <p>{cfg["challenge"][1]}</p>
         </div>
         <div class="reveal">
           <div class="detail-graphic {cfg["variant"]}">
{graphic}
           </div>
           <p class="detail-caption">A simplified view of the delivery shape, the control points that mattered, and the signals the client team used to keep the program on track.</p>
         </div>
       </div>
     </div>
   </section>

   <section class="section">
     <div class="container">
       <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
         <span class="eyebrow">Program workstreams</span>
         <h2 style="margin-top: var(--s-3);">The changes that made the outcome possible.</h2>
       </div>
       <div class="grid grid--4">
{workstreams}
       </div>
     </div>
   </section>

   <section class="section section--dark">
     <div class="container">
       <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 760px;">
         <span class="eyebrow" style="color: var(--brand-accent);">Execution rhythm</span>
         <h2 style="margin-top: var(--s-3);">How the delivery moved from pilot to scaled operation.</h2>
       </div>
       <div class="grid grid--4">
{timeline}
       </div>
     </div>
   </section>

   <section class="section">
     <div class="container">
       <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 760px;">
         <span class="eyebrow">Twelve months later</span>
         <h2 style="margin-top: var(--s-3);">What changed after the transformation settled into the run.</h2>
       </div>
       <div class="grid grid--3">
{outcomes}
       </div>
     </div>
   </section>

   <section class="section section--muted">
     <div class="container">
       <div class="quote">
         <div class="quote__mark">"</div>
         <blockquote>{cfg["quote"]}</blockquote>
         <cite><strong>{cfg["quote_name"]}</strong> - {cfg["quote_role"]}</cite>
       </div>
     </div>
   </section>

   <section class="section">
     <div class="container">
       <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
         <span class="eyebrow">Related capabilities</span>
         <h2 style="margin-top: var(--s-3);">The Tata services behind this outcome.</h2>
       </div>
       <div class="grid grid--2">
{related_services}
       </div>
     </div>
   </section>
{delivered_from}
"""
       + cta_strip("Want the full delivery playbook for a similar transformation?", "Request the deeper dive", "contact.html")
   )


def case_studies_main() -> str:
   cards = "\n".join(
       f"""          <article class="story-card reveal">
           <div class="story-card__media {study["variant"]}"></div>
           <div class="story-card__body">
             <span class="story-card__tag">{study["tag"]}</span>
             <h3 class="story-card__title">{study["title"]}</h3>
             <p class="story-card__excerpt">{study["excerpt"]}</p>
             <div class="story-card__footer">
               <a class="arrow-link" href="/{study["slug"]}">Read the case
                 {ARROW}
               </a>
             </div>
           </div>
         </article>"""
       for study in CASE_STUDIES
   )
   return (
       page_hero(
           "Case studies",
           "Outcomes our clients are most proud of.",
           "Anonymized where it matters, named where the client wants to be named. Each story now links through to a full delivery story with the operating context, the workstreams, and the measurable results one year later.",
       )
       + f"""
   <section class="section">
     <div class="container">
       <div class="grid grid--3">
{cards}
       </div>
     </div>
   </section>
"""
       + cta_strip("Want to read a case from your industry?", "Request the deeper dive", "contact.html")
   )


RUN_SERVICE_PAGE_STUBS = {
   page["slug"]: {
       "title": page["meta_title"],
       "description": page["meta_description"],
       "main_html": service_detail_main(page),
   }
   for page in RUN_SERVICE_PAGES
}


CASE_STUDY_PAGE_STUBS = {
   study["slug"]: {
       "title": study["meta_title"],
       "description": study["meta_description"],
       "main_html": case_detail_main(study),
   }
   for study in CASE_STUDIES
}


def legal_main(eyebrow: str, title: str, lead: str, sections: list) -> str:
    body = ""
    for s in sections:
        head, paras = s
        para_html = "\n".join(f'            <p>{p}</p>' for p in paras)
        body += f"""
        <div class="legal-section reveal">
          <h2>{head}</h2>
{para_html}
        </div>
"""
    return (
        page_hero(eyebrow, title, lead)
        + f"""
    <section class="section">
      <div class="container">
        <div class="legal-doc">
          <p class="muted" style="margin-bottom: var(--s-10);">Last updated: 27 May 2026.</p>
{body}
        </div>
      </div>
    </section>
"""
    )


def privacy_main() -> str:
    return legal_main(
        "Legal",
        "Privacy notice.",
        "This notice describes how Tata Consulting Services, PLC collects, uses, shares, and safeguards personal information when you visit our websites, contact us, or use services we provide.",
        [
            ("Information we collect", [
                "We collect information you give us directly - such as your name, work email, employer, and the contents of any message you send via a contact form.",
                "We collect technical information automatically, including IP address, device and browser identifiers, and pages viewed.",
                "We do not collect special-category data (health, biometric, political opinion, etc.) through this site.",
            ]),
            ("How we use it", [
                "To respond to your inquiries and route them to the right team.",
                "To send you information you have requested (e.g., newsletters or reports).",
                "To maintain and improve the website, including measuring aggregate usage patterns.",
                "To meet legal, regulatory, and contractual obligations.",
            ]),
            ("How we share it", [
                "With members of the Tata group and with vendors who process information on our behalf under written contract.",
                "When required by law, regulation, court order, or to protect the rights, property, or safety of Tata, our clients, or others.",
                "We do not sell personal information.",
            ]),
            ("Your rights", [
                "Depending on where you live, you may have the right to access, correct, delete, restrict, or object to the processing of personal information we hold about you, and to data portability.",
                "To exercise any of these rights, contact our privacy team at <a href=\"mailto:privacy@tata-consulting.co.uk\">privacy@tata-consulting.co.uk</a>.",
                "You may also lodge a complaint with the data protection authority in your country.",
            ]),
            ("Retention", [
                "We retain personal information only as long as needed to fulfil the purposes for which it was collected, including legal, accounting, or reporting requirements.",
            ]),
            ("Contact", [
                "Tata Consulting Services, PLC - Data Privacy Office. Email: <a href=\"mailto:privacy@tata-consulting.co.uk\">privacy@tata-consulting.co.uk</a>.",
            ]),
        ],
    )


def cookies_main() -> str:
    return legal_main(
        "Legal",
        "Cookies.",
        "We use a small set of cookies to make this site work and to understand how it is used. You can choose which categories to enable below.",
        [
            ("What cookies are", [
                "Cookies are small text files placed on your device by websites you visit. They are widely used to make sites work or work more efficiently, and to provide information to site owners.",
            ]),
            ("Categories we use", [
                "<strong>Strictly necessary.</strong> Required for the site to function. These cannot be turned off in our system.",
                "<strong>Analytics.</strong> Help us understand how visitors interact with the site by collecting and reporting information anonymously.",
                "<strong>Functional.</strong> Remember choices you make (such as your country or language).",
                "<strong>Marketing.</strong> Used to deliver more relevant marketing on third-party sites. Off by default.",
            ]),
            ("Managing cookies", [
                "Most browsers let you refuse or delete cookies. Doing so may prevent some features of this site from working as intended.",
                "You can update your preferences at any time via the cookie banner.",
            ]),
            ("Contact", [
                "Questions about cookies? Email <a href=\"mailto:privacy@tata-consulting.co.uk\">privacy@tata-consulting.co.uk</a>.",
            ]),
        ],
    )


def terms_main() -> str:
    return legal_main(
        "Legal",
        "Terms of use.",
        "These terms govern your use of this website. By using the site you agree to them; if you do not, please stop using the site.",
        [
            ("Use of materials", [
                "Content on this site is provided for general information. You may view, download, and print pages for your personal, non-commercial use, provided that you do not modify the content and that you retain all copyright and other proprietary notices.",
            ]),
            ("Intellectual property", [
                "All trademarks, service marks, logos, and trade names used on this site are the property of Tata Consulting Services, PLC or their respective owners. Nothing on the site grants any license or right to use any such mark.",
            ]),
            ("No warranty", [
                "The site is provided on an \"as-is\" and \"as-available\" basis. To the fullest extent permitted by applicable law, Tata disclaims all warranties, express or implied, including warranties of merchantability, fitness for a particular purpose, and non-infringement.",
            ]),
            ("Limitation of liability", [
                "To the fullest extent permitted by law, Tata will not be liable for any indirect, incidental, special, consequential, or punitive damages, including lost profits, arising out of or related to your use of the site.",
            ]),
            ("Governing law", [
                "These terms are governed by the laws of England and Wales, without regard to conflict-of-laws principles. Any dispute will be brought in the courts of London, England.",
            ]),
            ("Contact", [
                "Questions about these terms? Email <a href=\"mailto:legal@tata-consulting.co.uk\">legal@tata-consulting.co.uk</a>.",
            ]),
        ],
    )


def accessibility_main() -> str:
    return legal_main(
        "Legal",
        "Accessibility.",
        "Tata is committed to making this site usable by the widest possible audience, regardless of ability, technology, or context.",
        [
            ("Standards we aim for", [
                "We target conformance with the Web Content Accessibility Guidelines (WCAG) 2.2 at Level AA.",
                "Pages are built with semantic HTML, full keyboard support, visible focus states, sufficient colour contrast, and respect for the user's <code>prefers-reduced-motion</code> setting.",
            ]),
            ("Known limitations", [
                "Some embedded third-party content (charts, videos, maps) may not yet meet our internal standards. Where we are aware of issues we are working on remediations.",
            ]),
            ("Assistive technology compatibility", [
                "We test against current versions of NVDA, JAWS, VoiceOver (macOS, iOS), and TalkBack with the latest stable versions of Chrome, Edge, Firefox, and Safari.",
            ]),
            ("Feedback", [
                "If you encounter an accessibility barrier on this site, please contact <a href=\"mailto:accessibility@tata-consulting.co.uk\">accessibility@tata-consulting.co.uk</a>. We aim to respond within five working days.",
            ]),
        ],
    )


STUB_PAGES = {
    "leadership.html": {
        "title": "Leadership - Tata Consulting Services, PLC",
        "description": "Meet the operating committee of Tata Consulting Services, PLC - twelve practitioners who lead one of the world's largest professional services firms.",
        "main_html": leadership_main(),
    },
    "careers.html": {
        "title": "Careers - Tata Consulting Services, PLC",
        "description": "Build a long-term career at Tata - engineering, design, research, consulting, and operations roles across 55 countries.",
        "main_html": careers_main(),
    },
    "investors.html": {
        "title": "Investors - Tata Consulting Services, PLC",
        "description": "Financial performance, reports, filings, and investor relations for Tata Consulting Services, PLC.",
        "main_html": investors_main(),
    },
    "newsroom.html": {
        "title": "Newsroom - Tata Consulting Services, PLC",
        "description": "Press releases, announcements, awards, and media resources from Tata Consulting Services, PLC.",
        "main_html": newsroom_main(),
    },
    "find-office.html": {
        "title": "Find an office - Tata Consulting Services, PLC",
        "description": "Tata office locations across India, the Americas, Europe, Asia-Pacific, and the Middle East.",
        "main_html": find_office_main(),
    },
    "partners.html": {
        "title": "Partners - Tata Consulting Services, PLC",
        "description": "Hyperscale alliances, strategic alliances, technology partners, the Tata Ventures network, and academic partnerships.",
        "main_html": partners_main(),
    },
    "alumni.html": {
        "title": "Alumni - Tata Consulting Services, PLC",
        "description": "Stay connected through the Tata alumni network - 850,000+ members, 140+ local chapters, mentoring, events, and boomerang priority.",
        "main_html": alumni_main(),
    },
    "vendors.html": {
        "title": "Vendors &amp; suppliers - Tata Consulting Services, PLC",
        "description": "How to register, onboard, and work with Tata procurement as a supplier or vendor.",
        "main_html": vendors_main(),
    },
    "insights.html": {
        "title": "Insights - Tata Consulting Services, PLC",
        "description": "Research, perspectives, and points of view from Tata practitioners across AI, cloud, cybersecurity, industry, and the future of work.",
        "main_html": insights_main(),
    },
    "sustainability.html": {
        "title": "Sustainability - Tata Consulting Services, PLC",
        "description": "Tata's commitments and progress on climate, people, and governance - reported quarterly and audited externally.",
        "main_html": sustainability_main(),
    },
    "case-studies.html": {
        "title": "Case studies - Tata Consulting Services, PLC",
        "description": "Outcomes our clients are most proud of - across banking, manufacturing, retail, insurance, healthcare, public sector, energy, communications, and travel.",
        "main_html": case_studies_main(),
    },
    **RUN_SERVICE_PAGE_STUBS,
    **CASE_STUDY_PAGE_STUBS,
    "privacy.html": {
        "title": "Privacy notice - Tata Consulting Services, PLC",
        "description": "How Tata collects, uses, shares, and safeguards personal information.",
        "main_html": privacy_main(),
    },
    "cookies.html": {
        "title": "Cookies - Tata Consulting Services, PLC",
        "description": "Information about the cookies this website uses and how to manage your preferences.",
        "main_html": cookies_main(),
    },
    "terms.html": {
        "title": "Terms of use - Tata Consulting Services, PLC",
        "description": "Terms governing your use of the Tata Consulting Services, PLC website.",
        "main_html": terms_main(),
    },
    "accessibility.html": {
        "title": "Accessibility - Tata Consulting Services, PLC",
        "description": "Tata's commitment to accessibility, the standards we target, known limitations, and how to give us feedback.",
        "main_html": accessibility_main(),
    },
}


# -- Re-emit existing pages with updated chrome -----------------------------

EXISTING_PAGES = {
    "index.html":     ("Tata Consulting Services, PLC - Building on belief",
                        "Tata Consulting Services, PLC partners with the world's largest enterprises to design and run their digital transformation - across cloud, AI, cybersecurity, and operations."),
    "about.html":     ("About - Tata Consulting Services, PLC",
                        "For 56 years we have helped the world's largest organisations transform. Get to know the people, the purpose, and the philosophy behind Tata Consulting Services, PLC."),
    "services.html":  ("What we do - Tata Consulting Services, PLC",
                        "From cloud and AI to cybersecurity, engineering, and managed operations - explore the full set of services Tata delivers to the world's largest enterprises."),
    "industries.html":("Industries - Tata Consulting Services, PLC",
                        "Tata brings deep industry knowledge to banking, insurance, manufacturing, retail, healthcare, public services, communications, and energy."),
    "contact.html":   ("Contact - Tata Consulting Services, PLC",
                        "Start a conversation with Tata Consulting Services, PLC. Find an office near you, or send us a note and we will respond within two business days."),
    "coe/london.html":    ("London - Engineering Centre of Excellence - Tata Consulting Services, PLC",
                        "The Tata Consulting Services, PLC London office is an engineering centre of excellence specialising in cloud, cloud-native, IoT, DevOps, AI, and automation - including next-generation Internal Developer Platforms, container orchestration (Kubernetes, OpenShift), and Developer Experience (DevEx)."),
    "coe/idp.html":       ("Internal Developer Platform - Tata Consulting Services, PLC",
                        "The Tata Internal Developer Platform is built and operated by the London Engineering Centre of Excellence on an open, cloud-native, AI-enabled stack. Service provider-grade architecture, strict multi-tenancy, policy-as-code RBAC, and a developer experience worth opening every morning - for hundreds of thousands of Tata engineers and client teams."),
}

MAIN_RE = re.compile(r"<main[^>]*>(.*?)</main>", re.DOTALL)
HEAD_RE = re.compile(r"<head\b[^>]*>(.*?)</head>", re.DOTALL | re.IGNORECASE)
HEAD_STYLE_RE = re.compile(r"[ \t]*<style\b[^>]*>.*?</style>", re.DOTALL | re.IGNORECASE)

# Bespoke per-page <head> additions the standard chrome does not carry. The
# London and IDP pages use JetBrains Mono for code/architecture callouts; their
# inline <style> blocks are preserved automatically (see preserve_head_extra).
JETBRAINS_MONO_LINK = (
    '  <link rel="stylesheet" '
    'href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" />'
)
PAGE_HEAD_EXTRA = {
    "coe/london.html": JETBRAINS_MONO_LINK,
    "coe/idp.html": JETBRAINS_MONO_LINK,
}


def preserve_head_extra(filename: str, old_html: str) -> str:
    """Collect <head> additions that must survive re-emission of an existing page.

    The chrome owns the head's shared parts; anything page-specific (an extra
    font declared in PAGE_HEAD_EXTRA, plus any inline <style> blocks the page
    carries in its own <head>) is preserved verbatim so the generator can manage
    these pages without flattening their bespoke styling.
    """
    parts = []
    extra_font = PAGE_HEAD_EXTRA.get(filename)
    if extra_font:
        parts.append(extra_font)

    head_match = HEAD_RE.search(old_html)
    if head_match:
        for style in HEAD_STYLE_RE.findall(head_match.group(1)):
            parts.append(style.strip("\n"))

    return "\n".join(parts)


def emit_page(
    path: Path,
    title: str,
    description: str,
    main_inner: str,
    head_extra: str = "",
) -> None:
    # strip() (not strip("\n")): the body is re-wrapped with its own surrounding
    # whitespace on every run, so trailing spaces left by strip("\n") would
    # accumulate a blank line per regeneration. Full strip gives a fixed point.
    main_inner = main_inner.strip()
    head_slot = f"\n{head_extra}" if head_extra else ""
    body = f'  <main id="main">\n{main_inner}\n  </main>\n'
    top = CHROME_TOP.format(title=title, description=description, head_extra=head_slot)
    full = top + body + CHROME_BOTTOM
    path.write_text(full, encoding="utf-8")


# -- Client-side search index ------------------------------------------------
#
# The header search button and overlay (see CHROME_TOP) are powered entirely on
# the client by site/js/main.js, which fetches the index emitted here. Keeping
# the index a build artifact means it can never drift from the pages it
# describes: every page that is emitted contributes exactly one record.

_SVG_RE = re.compile(r"<svg\b[^>]*>.*?</svg>", re.DOTALL | re.IGNORECASE)
_SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")

# Cap per-page body text so the whole index stays small enough to ship to every
# visitor on first search. ~2.5k chars covers the meaningful copy on these pages
# without bloating the payload with boilerplate from long detail pages.
SEARCH_BODY_MAX_CHARS = 2500

# The brand suffix is on nearly every <title>; strip it for clean result labels.
_TITLE_SUFFIX = " - Tata Consulting Services, PLC"


def html_to_text(html: str) -> str:
    """Reduce an HTML fragment to indexable plain text.

    SVG, script, and style blocks are dropped wholesale (they carry no readable
    copy - the case-study and service graphics are pure SVG), then remaining
    tags are stripped, entities decoded, and whitespace collapsed.
    """
    text = _SVG_RE.sub(" ", html)
    text = _SCRIPT_STYLE_RE.sub(" ", text)
    text = _TAG_RE.sub(" ", text)
    text = unescape(text)
    return _WS_RE.sub(" ", text).strip()


def clean_title(title: str) -> str:
    title = unescape(title).strip()
    if title.endswith(_TITLE_SUFFIX):
        title = title[: -len(_TITLE_SUFFIX)].strip()
    return title


def search_record(filename: str, title: str, description: str, main_inner: str) -> dict:
    body = html_to_text(main_inner)
    if len(body) > SEARCH_BODY_MAX_CHARS:
        body = body[:SEARCH_BODY_MAX_CHARS].rsplit(" ", 1)[0] + "…"
    return {
        "u": filename,
        "t": clean_title(title),
        "d": unescape(description).strip(),
        "b": body,
    }


def emit_search_index(records: list[dict]) -> None:
    records = sorted(records, key=lambda r: r["u"])
    payload = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    (SITE_DIR / "search-index.json").write_text(payload + "\n", encoding="utf-8")


def site_base_url() -> str:
    domain = (SITE_DIR / "CNAME").read_text(encoding="utf-8").strip()
    if not domain:
        raise SystemExit("site/CNAME is empty")
    if domain.startswith(("http://", "https://")):
        return domain.rstrip("/")
    return f"https://{domain}"


def sitemap_url(base_url: str, filename: str) -> str:
    return f"{base_url}/" if filename == "index.html" else f"{base_url}/{filename}"


def emit_sitemap() -> None:
    base_url = site_base_url()
    urls = []
    for path in sorted(SITE_DIR.glob("*.html")):
        lastmod = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).date().isoformat()
        urls.append(
            f"""  <url>
    <loc>{escape(sitemap_url(base_url, path.name))}</loc>
    <lastmod>{lastmod}</lastmod>
  </url>"""
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{"\n".join(urls)}\n'
        '</urlset>\n'
    )
    (SITE_DIR / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def main() -> int:
    written = []
    search_records = []

    # Regenerate existing pages, preserving their <main> bodies and any
    # bespoke <head> additions.
    for filename, (title, description) in EXISTING_PAGES.items():
        path = SITE_DIR / filename
        if not path.exists():
            raise SystemExit(f"missing source page: {path}")
        old = path.read_text(encoding="utf-8")
        m = MAIN_RE.search(old)
        if not m:
            raise SystemExit(f"no <main> block in {path}")
        main_inner = m.group(1)
        head_extra = preserve_head_extra(filename, old)
        emit_page(path, title, description, main_inner, head_extra=head_extra)
        search_records.append(search_record(filename, title, description, main_inner))
        written.append(filename)

    # Generate new stub pages.
    for filename, cfg in STUB_PAGES.items():
        path = SITE_DIR / filename
        emit_page(path, cfg["title"], cfg["description"], cfg["main_html"])
        search_records.append(
            search_record(filename, cfg["title"], cfg["description"], cfg["main_html"])
        )
        written.append(filename)

    emit_search_index(search_records)
    written.append("search-index.json")

    emit_sitemap()
    written.append("sitemap.xml")

    print(f"Wrote {len(written)} files:")
    for name in written:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
