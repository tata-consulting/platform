#!/usr/bin/env python3
"""
One-shot site generator.

Holds the shared chrome (head, utility bar, header, mobile menu, footer) as
templates. Produces fresh HTML for:

  1. The 8 new stub pages introduced for footer "Company" / "Connect" links.
  2. The 5 existing pages, re-emitting them with the updated chrome while
     preserving their custom <main>...</main> body.

The chrome is the single source of truth for nav links, footer links, and
social URLs. Run this once after editing the chrome to propagate everywhere.
"""

from __future__ import annotations

import re
from pathlib import Path
from textwrap import dedent

SITE_DIR = Path(__file__).resolve().parents[1] / "site"

WORDMARK_LIGHT = """\
        <svg viewBox="0 0 220 48" aria-hidden="true" style="color: var(--brand-primary)">
          <g fill="currentColor">
            <path d="M4 12h44v6H32v22h-6V18H4z"/>
            <path d="M82 11.2c-9 0-15.4 6.2-15.4 15s6.4 15 15.4 15c5.2 0 9.4-1.9 12.4-5.4l-4.4-4c-2 2-4.6 3.2-7.8 3.2-5.5 0-9.4-3.7-9.4-8.8s3.9-8.8 9.4-8.8c3 0 5.5 1 7.5 2.9l4.5-4C92 13 87.6 11.2 82 11.2z"/>
            <path d="M112.8 11.2c-7.2 0-12 3.6-12 8.9 0 11.4 17.7 7.8 17.7 13.6 0 1.9-1.9 3-5.5 3-3.7 0-7-1.4-9.5-3.7l-3.4 4.7c2.9 2.6 7.7 4.3 12.6 4.3 7.6 0 12.4-3.6 12.4-9.1 0-11.5-17.7-7.7-17.7-13.5 0-1.8 1.7-2.8 4.8-2.8 2.7 0 5.8.9 8.7 2.6l3-4.9c-3-1.9-7-3.1-11.1-3.1z"/>
          </g>
          <text x="138" y="32" font-family="Inter, system-ui, sans-serif" font-size="18" font-weight="700" fill="currentColor" letter-spacing="-0.02em">Consultancy</text>
        </svg>"""

WORDMARK_DARK = WORDMARK_LIGHT.replace("color: var(--brand-primary)", "color: #fff")

ARROW = '<svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M13 5l7 7-7 7"/></svg>'

CHROME_TOP = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <script>document.documentElement.classList.add('js')</script>
  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" />
  <link rel="stylesheet" href="css/base.css" />
  <link rel="stylesheet" href="css/components.css" />
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <div class="utility-bar">
    <div class="container utility-bar__inner">
      <a href="#"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 010 20M12 2a15 15 0 000 20"/></svg> Global - English</a>
      <a href="investors.html">Investors</a>
      <a href="newsroom.html">Newsroom</a>
      <a href="alumni.html">Alumni</a>
      <a href="#">Sign in</a>
    </div>
  </div>

  <header class="site-header">
    <div class="container site-header__inner">
      <a class="site-header__logo" href="index.html" aria-label="Trion Consultancy Services - Home">
""" + WORDMARK_LIGHT + """
      </a>

      <nav class="primary-nav" aria-label="Primary">
        <ul class="primary-nav__list">
          <li class="primary-nav__item primary-nav__item--has-mega">
            <a class="primary-nav__link" href="services.html" aria-expanded="false" aria-haspopup="true">
              What we do
              <svg class="primary-nav__caret" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1 1l4 4 4-4"/></svg>
            </a>
            <div class="mega" role="menu">
              <div class="mega__grid">
                <div class="mega__col">
                  <h4>Build</h4>
                  <ul>
                    <li><a href="services.html#cloud">Cloud transformation</a></li>
                    <li><a href="services.html#ai">AI &amp; data</a></li>
                    <li><a href="services.html#security">Cybersecurity</a></li>
                    <li><a href="services.html#engineering">Engineering &amp; R&amp;D</a></li>
                  </ul>
                </div>
                <div class="mega__col">
                  <h4>Run</h4>
                  <ul>
                    <li><a href="services.html#managed">Managed services</a></li>
                    <li><a href="services.html#apps">Enterprise applications</a></li>
                    <li><a href="services.html#network">Network &amp; infrastructure</a></li>
                    <li><a href="services.html#ops">Business operations</a></li>
                  </ul>
                </div>
                <div class="mega__col">
                  <h4>Transform</h4>
                  <ul>
                    <li><a href="services.html#consulting">Strategy &amp; consulting</a></li>
                    <li><a href="services.html#xd">Experience design</a></li>
                    <li><a href="services.html#sustainability">Sustainability</a></li>
                    <li><a href="services.html#platforms">Industry platforms</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </li>
          <li class="primary-nav__item"><a class="primary-nav__link" href="industries.html">Industries</a></li>
          <li class="primary-nav__item"><a class="primary-nav__link" href="insights.html">Insights</a></li>
          <li class="primary-nav__item"><a class="primary-nav__link" href="careers.html">Careers</a></li>
          <li class="primary-nav__item"><a class="primary-nav__link" href="about.html">About</a></li>
          <li class="primary-nav__item"><a class="primary-nav__link" href="investors.html">Investors</a></li>
        </ul>
      </nav>

      <div class="header-cta">
        <button class="header-icon-btn" type="button" aria-label="Search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
        </button>
        <a class="btn btn--primary" href="contact.html">Contact us
          """ + ARROW + """
        </a>
      </div>

      <button class="mobile-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open navigation">
        <span class="mobile-toggle__bars" aria-hidden="true"><span></span><span></span><span></span></span>
      </button>
    </div>
  </header>

  <div class="mobile-menu" id="mobile-menu">
    <ul>
      <li><a href="services.html">What we do</a></li>
      <li><a href="industries.html">Industries</a></li>
      <li><a href="insights.html">Insights</a></li>
      <li><a href="careers.html">Careers</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="investors.html">Investors</a></li>
    </ul>
    <a class="btn btn--primary" href="contact.html">Contact us
      """ + ARROW + """
    </a>
  </div>

"""

CHROME_BOTTOM = """
  <footer class="site-footer">
    <div class="container">
      <div class="newsletter">
        <div class="newsletter__copy">
          <h3>Get the Trion brief.</h3>
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
          <p>Trion Consultancy Services partners with the world's largest enterprises to design, build, and run their digital transformation.</p>
        </div>
        <div class="site-footer__col">
          <h4>What we do</h4>
          <ul>
            <li><a href="services.html#cloud">Cloud</a></li>
            <li><a href="services.html#ai">AI &amp; data</a></li>
            <li><a href="services.html#security">Cybersecurity</a></li>
            <li><a href="services.html#engineering">Engineering</a></li>
            <li><a href="services.html#consulting">Consulting</a></li>
          </ul>
        </div>
        <div class="site-footer__col">
          <h4>Industries</h4>
          <ul>
            <li><a href="industries.html#banking">Banking</a></li>
            <li><a href="industries.html#insurance">Insurance</a></li>
            <li><a href="industries.html#manufacturing">Manufacturing</a></li>
            <li><a href="industries.html#retail">Retail</a></li>
            <li><a href="industries.html#healthcare">Healthcare</a></li>
          </ul>
        </div>
        <div class="site-footer__col">
          <h4>Company</h4>
          <ul>
            <li><a href="about.html">About us</a></li>
            <li><a href="leadership.html">Leadership</a></li>
            <li><a href="careers.html">Careers</a></li>
            <li><a href="investors.html">Investors</a></li>
            <li><a href="newsroom.html">Newsroom</a></li>
            <li><a href="sustainability.html">Sustainability</a></li>
          </ul>
        </div>
        <div class="site-footer__col">
          <h4>Connect</h4>
          <ul>
            <li><a href="contact.html">Contact us</a></li>
            <li><a href="find-office.html">Find an office</a></li>
            <li><a href="partners.html">Partners</a></li>
            <li><a href="alumni.html">Alumni</a></li>
            <li><a href="vendors.html">Vendors</a></li>
            <li><a href="insights.html">Insights</a></li>
          </ul>
        </div>
      </div>
      <div class="site-footer__legal">
        <ul>
          <li><a href="privacy.html">Privacy notice</a></li>
          <li><a href="cookies.html">Cookies</a></li>
          <li><a href="terms.html">Terms of use</a></li>
          <li><a href="accessibility.html">Accessibility</a></li>
          <li><a href="case-studies.html">Case studies</a></li>
        </ul>
      </div>
      <div class="site-footer__bottom">
        <p>&copy; <span data-year>2026</span> Trion Consultancy Services. All rights reserved.</p>
        <div class="site-footer__social" aria-label="Social links">
          <a href="https://www.linkedin.com/company/trion-consultancy-services" aria-label="LinkedIn on LinkedIn" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h14zM8.34 18.34V9.86H5.67v8.48h2.67zM7 8.68a1.54 1.54 0 110-3.08 1.54 1.54 0 010 3.08zm11.34 9.66v-4.64c0-2.49-1.33-3.65-3.1-3.65a2.67 2.67 0 00-2.43 1.34V9.86H10.13c.04.75 0 8.48 0 8.48h2.68v-4.74c0-.24.02-.48.09-.65.19-.48.63-.98 1.36-.98.96 0 1.34.73 1.34 1.8v4.57h2.74z"/></svg></a>
          <a href="https://x.com/trion_consulting" aria-label="Trion on X" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
          <a href="https://www.youtube.com/@trion-consulting" aria-label="Trion on YouTube" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a2.999 2.999 0 00-2.111-2.122C19.505 3.5 12 3.5 12 3.5s-7.505 0-9.387.564A2.999 2.999 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a2.999 2.999 0 002.111 2.122C4.495 20.5 12 20.5 12 20.5s7.505 0 9.387-.564a2.999 2.999 0 002.111-2.122C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.546 15.568V8.432L15.818 12z"/></svg></a>
          <a href="https://www.facebook.com/trionconsultancy" aria-label="Trion on Facebook" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 10-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.51 1.49-3.9 3.78-3.9 1.1 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.77l-.44 2.89h-2.33v6.99A10 10 0 0022 12z"/></svg></a>
        </div>
      </div>
    </div>
  </footer>

  <script src="js/main.js"></script>
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
        <a class="btn btn--ghost-light" href="{btn_href}">{btn_text}
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
            "The people who run Trion.",
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
          <a class="arrow-link" href="contact.html">Browse all roles
            """ + ARROW + """
          </a>
        </div>
        <div class="grid grid--3">
          <a class="service-tile reveal" href="contact.html">
            <h3>Software engineer - Cloud platforms</h3>
            <div class="service-tile__footer"><span class="service-tile__num">Multiple - Global</span></div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>AI/ML engineer</h3>
            <div class="service-tile__footer"><span class="service-tile__num">Bengaluru / Pune / Toronto</span></div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>Cybersecurity consultant</h3>
            <div class="service-tile__footer"><span class="service-tile__num">London / Frankfurt / Singapore</span></div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>Product designer</h3>
            <div class="service-tile__footer"><span class="service-tile__num">New York / Amsterdam</span></div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>Data engineer</h3>
            <div class="service-tile__footer"><span class="service-tile__num">Multiple - Global</span></div>
          </a>
          <a class="service-tile reveal" href="contact.html">
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
          <a class="arrow-link" href="contact.html">Request investor pack
            {ARROW}
          </a>
        </div>
        <div class="grid grid--3">
          <a class="service-tile reveal" href="contact.html">
            <h3>Annual report 2025</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 14.2 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>Q4 FY25 earnings transcript</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 1.1 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>Sustainability report 2025</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 8.6 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>Proxy statement 2025</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 2.3 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>Corporate governance</h3>
            <div class="service-tile__footer"><span class="service-tile__num">Code of conduct &amp; bylaws</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="contact.html">
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
            <a class="arrow-link arrow-link--light" href="mailto:ir@trion.example">ir@trion.example
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
    ("media--ocean",  "May 14, 2026", "Press release",   "Trion expands European delivery footprint with new Madrid campus.", "Three thousand engineers, designers, and consultants will be based in the new center by 2028."),
    ("media--neon",   "Apr 28, 2026", "Press release",   "Q4 FY25 results: revenue up 8.4% YoY, margin holds at 24.6%.", "Annual revenue crosses $29B; record TCV bookings driven by AI and cloud engagements."),
    ("media--sunset", "Apr 02, 2026", "Announcement",    "Trion joins UN Climate Action Compact.", "Commits to net-zero across owned operations by 2030, full supply chain by 2040."),
    ("media--forest", "Mar 18, 2026", "Press release",   "Strategic alliance with a leading hyperscaler expands managed AI services.", "Joint go-to-market across financial services, manufacturing, and healthcare."),
    ("media--ember",  "Feb 24, 2026", "Award",           "Recognized as a Leader in the 2026 Cloud Services Magic Quadrant.", "Sixth consecutive year in the Leaders quadrant."),
    ("media--steel",  "Jan 30, 2026", "Press release",   "Trion to acquire a specialist healthcare data engineering firm.", "Strengthens life sciences delivery in North America and Europe."),
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
                <a class="arrow-link" href="contact.html">Read release
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
          <a class="arrow-link" href="#">Archive
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
            <a class="arrow-link" href="mailto:press@trion.example">press@trion.example
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
    ("Mumbai - Global HQ",    "Trion House<br />N. M. Marg, Apollo Bunder<br />Mumbai 400001, India",                                                      "+91 22 6666 7777",  "+912266667777"),
    ("Bengaluru",             "Trion Park, Whitefield Main Road<br />Whitefield, Bengaluru 560066<br />India",                                              "+91 80 2222 1234",  "+918022221234"),
    ("Delhi NCR",             "Trion Tower, DLF Cyber City Phase III<br />Gurugram 122002<br />India",                                                       "+91 124 444 5555",  "+911244445555"),
    ("New York",              "101 Park Avenue, 26th Floor<br />New York, NY 10178<br />United States",                                                      "+1 212 555 0100",   "+12125550100"),
    ("Toronto",               "199 Bay Street, 30th Floor<br />Toronto, ON M5L 1G9<br />Canada",                                                             "+1 416 555 0150",   "+14165550150"),
    ("London",                "17 Old Bailey<br />London EC4M 7EG<br />United Kingdom",                                                                      "+44 20 7220 0800",  "+442072200800"),
    ("Frankfurt",             "Trianon, Mainzer Landstraße 16<br />60325 Frankfurt am Main<br />Germany",                                                    "+49 69 2222 0700",  "+496922220700"),
    ("Amsterdam",             "Vinoly Building, Claude Debussylaan 80<br />1082 MD Amsterdam<br />Netherlands",                                              "+31 20 521 0500",   "+31205210500"),
    ("Singapore",             "Marina Bay Financial Centre, Tower 3<br />12 Marina Boulevard<br />Singapore 018982",                                         "+65 6222 0222",     "+6562220222"),
    ("Tokyo",                 "Marunouchi Building, 21F<br />2-4-1 Marunouchi, Chiyoda-ku<br />Tokyo 100-6321, Japan",                                       "+81 3 5222 0900",   "+81352220900"),
    ("Sydney",                "Tower One, International Towers<br />100 Barangaroo Avenue, Sydney NSW 2000<br />Australia",                                  "+61 2 8224 0900",   "+61282240900"),
    ("São Paulo",             "Avenida Paulista, 1842<br />Bela Vista, São Paulo - SP<br />Brazil 01310-200",                                                "+55 11 3000 0400",  "+551130000400"),
]


def find_office_main() -> str:
    cards = "\n".join(
        f"""          <div class="office-card reveal">
            <h3>{name}</h3>
            <address>{addr}</address>
            <a href="tel:{tel_e164}">{tel_display}</a>
          </div>"""
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
        + cta_strip("Need a region we don't list?", "Talk to us", "contact.html")
    )


PARTNER_LIST = [
    ("media--neon",   "Hyperscale alliance",     "Cloud platforms",         "Co-engineering, joint go-to-market, and shared customer success across the three largest public-cloud providers."),
    ("media--ocean",  "Strategic alliance",      "Core enterprise software", "Deep delivery practices around SAP, Oracle, Microsoft, Salesforce, ServiceNow, and Workday - implementation, migration, and managed run."),
    ("media--sunset", "Technology partner",      "Data &amp; AI",            "Joint capabilities with Databricks, Snowflake, Confluent, and the leading model providers - to put AI into production, not pilots."),
    ("media--forest", "Innovation network",      "Startups &amp; ventures",  "Trion Ventures invests in and co-builds with 80+ enterprise startups. We bring them into client engagements when their tech is ready."),
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
                <a class="arrow-link" href="contact.html">Explore partnership
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
        + cta_strip("Become a Trion partner.", "Start the conversation", "contact.html")
    )


def alumni_main() -> str:
    return (
        page_hero(
            "Alumni",
            "Once Trion. Always Trion.",
            "Over 850,000 people have been part of Trion across our history. The network you joined when you walked in is yours for life - whether you're still here or building somewhere new.",
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
            <a class="btn btn--primary" href="contact.html">Verify and join
              {ARROW}
            </a>
          </div>
          <div class="split__media media--neon reveal"></div>
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
            <p class="muted">A quarterly digest of what's changing - in Trion and in the industry.</p>
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
            "Working with Trion procurement.",
            "We work with thousands of suppliers globally, from hyperscalers to local hospitality vendors. This is how to register, get paid, and stay compliant.",
        )
        + f"""
    <section class="section">
      <div class="container">
        <div class="section-head__title" style="margin-bottom: var(--s-12); max-width: 720px;">
          <span class="eyebrow">Onboarding</span>
          <h2 style="margin-top: var(--s-3);">Four steps to becoming an approved Trion supplier.</h2>
        </div>
        <div class="grid grid--4">
          <a class="service-tile reveal" href="contact.html">
            <h3>Register interest</h3>
            <div class="service-tile__footer">
              <span class="service-tile__num">Step 01</span>
              {ARROW}
            </div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>Due diligence</h3>
            <div class="service-tile__footer">
              <span class="service-tile__num">Step 02</span>
              {ARROW}
            </div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>Master agreement</h3>
            <div class="service-tile__footer">
              <span class="service-tile__num">Step 03</span>
              {ARROW}
            </div>
          </a>
          <a class="service-tile reveal" href="contact.html">
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
            <a class="arrow-link arrow-link--light" href="mailto:procurement@trion.example">procurement@trion.example
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
    ("media--steel",  "Point of view",                "The next operating model: small teams, large autonomy, AI in the loop.",         "A framework for re-organizing IT and operations around outcomes - not towers, not tickets, not handoffs."),
    ("media--neon",   "Research note",                "The cloud bill came due. Now what?",                                              "Why 62% of enterprises are returning to disciplined unit-economics conversations - and the playbook that's working."),
    ("media--ocean",  "Industry brief - Banking",     "Core modernization in 24 months: a comparison of four playbooks.",                "Strangler, big-bang, sidecar, greenfield - the trade-offs that determine which approach actually finishes."),
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
                <a class="arrow-link" href="contact.html">Read
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
          <a class="arrow-link" href="contact.html">Subscribe to our newsletter
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
          <a class="arrow-link" href="contact.html">Subscribe to ESG updates
            {ARROW}
          </a>
        </div>
        <div class="grid grid--3">
          <a class="service-tile reveal" href="contact.html">
            <h3>Sustainability report 2025</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 8.6 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>CDP climate disclosure</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 3.1 MB</span>{ARROW}</div>
          </a>
          <a class="service-tile reveal" href="contact.html">
            <h3>SASB framework alignment</h3>
            <div class="service-tile__footer"><span class="service-tile__num">PDF - 1.8 MB</span>{ARROW}</div>
          </a>
        </div>
      </div>
    </section>
"""
        + cta_strip("Partner with us on what's next.", "Talk to the ESG team", "contact.html")
    )


CASE_STUDIES = [
    ("media--ocean",  "Banking - Europe",            "Modernizing a 220M-account retail bank to cloud-native in 18 months.",                "70% faster time-to-market on new products; 60% reduction in run cost; zero customer-facing incidents during cutover."),
    ("media--neon",   "Manufacturing - Global OEM",  "Connected factory across 40 plants on 18 countries' production lines.",               "Real-time supplier and quality data; 23% drop in unplanned downtime; $180M annualized inventory release."),
    ("media--sunset", "Retail - 150-year-old chain", "From quarterly waterfalls to a release every three minutes - 1,800 stores.",          "Continuous delivery across e-commerce + physical; 8x deployment frequency; 95% reduction in change-failure rate."),
    ("media--ember",  "Insurance - Top-10 carrier",  "Claims automated end-to-end for property &amp; casualty.",                            "Average resolution time 14 days → 38 hours; 91% straight-through processing; +18 NPS in 12 months."),
    ("media--forest", "Healthcare - National payer", "Member experience platform serving 22M lives.",                                       "Consolidated 36 legacy portals into one digital front door; 4.7-star app store rating; 200K calls/month diverted."),
    ("media--steel",  "Public sector - National",     "Citizen identity and a single front door for 65M people.",                            "40 legacy systems retired behind it; 24M monthly active users; cost-per-transaction down 82%."),
    ("media--ocean",  "Energy - European utility",   "Grid-edge intelligence across 9 countries.",                                          "Outage detection sub-90s on average; renewables integration 38% faster; customer-facing outage minutes down 41%."),
    ("media--neon",   "Comms - Tier-1 telco",        "5G core launch and BSS modernization in parallel.",                                   "First 5G slice live in 9 months; OSS migration with zero net-new tickets to support; 2x faster new-product launches."),
    ("media--sunset", "Travel - Global airline",     "Loyalty platform unified across 9 sub-brands.",                                       "Single member view across the group; +24% repeat booking; +$310M incremental revenue in year one."),
]


def case_studies_main() -> str:
    cards = "\n".join(
        f"""          <article class="story-card reveal">
            <div class="story-card__media {variant}"></div>
            <div class="story-card__body">
              <span class="story-card__tag">{tag}</span>
              <h3 class="story-card__title">{title}</h3>
              <p class="story-card__excerpt">{excerpt}</p>
              <div class="story-card__footer">
                <a class="arrow-link" href="contact.html">Read the case
                  {ARROW}
                </a>
              </div>
            </div>
          </article>"""
        for (variant, tag, title, excerpt) in CASE_STUDIES
    )
    return (
        page_hero(
            "Case studies",
            "Outcomes our clients are most proud of.",
            "Anonymized where it matters, named where the client wants to be named. Each story walks through the problem, the approach, the obstacles, and the measurable result twelve months later.",
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
        "This notice describes how Trion Consultancy Services collects, uses, shares, and safeguards personal information when you visit our websites, contact us, or use services we provide.",
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
                "With members of the Trion group and with vendors who process information on our behalf under written contract.",
                "When required by law, regulation, court order, or to protect the rights, property, or safety of Trion, our clients, or others.",
                "We do not sell personal information.",
            ]),
            ("Your rights", [
                "Depending on where you live, you may have the right to access, correct, delete, restrict, or object to the processing of personal information we hold about you, and to data portability.",
                "To exercise any of these rights, contact our privacy team at <a href=\"mailto:privacy@trion.example\">privacy@trion.example</a>.",
                "You may also lodge a complaint with the data protection authority in your country.",
            ]),
            ("Retention", [
                "We retain personal information only as long as needed to fulfil the purposes for which it was collected, including legal, accounting, or reporting requirements.",
            ]),
            ("Contact", [
                "Trion Consultancy Services - Data Privacy Office. Email: <a href=\"mailto:privacy@trion.example\">privacy@trion.example</a>.",
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
                "Questions about cookies? Email <a href=\"mailto:privacy@trion.example\">privacy@trion.example</a>.",
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
                "All trademarks, service marks, logos, and trade names used on this site are the property of Trion Consultancy Services or their respective owners. Nothing on the site grants any license or right to use any such mark.",
            ]),
            ("No warranty", [
                "The site is provided on an \"as-is\" and \"as-available\" basis. To the fullest extent permitted by applicable law, Trion disclaims all warranties, express or implied, including warranties of merchantability, fitness for a particular purpose, and non-infringement.",
            ]),
            ("Limitation of liability", [
                "To the fullest extent permitted by law, Trion will not be liable for any indirect, incidental, special, consequential, or punitive damages, including lost profits, arising out of or related to your use of the site.",
            ]),
            ("Governing law", [
                "These terms are governed by the laws of England and Wales, without regard to conflict-of-laws principles. Any dispute will be brought in the courts of London, England.",
            ]),
            ("Contact", [
                "Questions about these terms? Email <a href=\"mailto:legal@trion.example\">legal@trion.example</a>.",
            ]),
        ],
    )


def accessibility_main() -> str:
    return legal_main(
        "Legal",
        "Accessibility.",
        "Trion is committed to making this site usable by the widest possible audience, regardless of ability, technology, or context.",
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
                "If you encounter an accessibility barrier on this site, please contact <a href=\"mailto:accessibility@trion.example\">accessibility@trion.example</a>. We aim to respond within five working days.",
            ]),
        ],
    )


STUB_PAGES = {
    "leadership.html": {
        "title": "Leadership - Trion Consultancy Services",
        "description": "Meet the operating committee of Trion Consultancy Services - twelve practitioners who lead one of the world's largest professional services firms.",
        "main_html": leadership_main(),
    },
    "careers.html": {
        "title": "Careers - Trion Consultancy Services",
        "description": "Build a long-term career at Trion - engineering, design, research, consulting, and operations roles across 55 countries.",
        "main_html": careers_main(),
    },
    "investors.html": {
        "title": "Investors - Trion Consultancy Services",
        "description": "Financial performance, reports, filings, and investor relations for Trion Consultancy Services.",
        "main_html": investors_main(),
    },
    "newsroom.html": {
        "title": "Newsroom - Trion Consultancy Services",
        "description": "Press releases, announcements, awards, and media resources from Trion Consultancy Services.",
        "main_html": newsroom_main(),
    },
    "find-office.html": {
        "title": "Find an office - Trion Consultancy Services",
        "description": "Trion office locations across India, the Americas, Europe, Asia-Pacific, and the Middle East.",
        "main_html": find_office_main(),
    },
    "partners.html": {
        "title": "Partners - Trion Consultancy Services",
        "description": "Hyperscale alliances, strategic alliances, technology partners, the Trion Ventures network, and academic partnerships.",
        "main_html": partners_main(),
    },
    "alumni.html": {
        "title": "Alumni - Trion Consultancy Services",
        "description": "Stay connected through the Trion alumni network - 850,000+ members, 140+ local chapters, mentoring, events, and boomerang priority.",
        "main_html": alumni_main(),
    },
    "vendors.html": {
        "title": "Vendors &amp; suppliers - Trion Consultancy Services",
        "description": "How to register, onboard, and work with Trion procurement as a supplier or vendor.",
        "main_html": vendors_main(),
    },
    "insights.html": {
        "title": "Insights - Trion Consultancy Services",
        "description": "Research, perspectives, and points of view from Trion practitioners across AI, cloud, cybersecurity, industry, and the future of work.",
        "main_html": insights_main(),
    },
    "sustainability.html": {
        "title": "Sustainability - Trion Consultancy Services",
        "description": "Trion's commitments and progress on climate, people, and governance - reported quarterly and audited externally.",
        "main_html": sustainability_main(),
    },
    "case-studies.html": {
        "title": "Case studies - Trion Consultancy Services",
        "description": "Outcomes our clients are most proud of - across banking, manufacturing, retail, insurance, healthcare, public sector, energy, communications, and travel.",
        "main_html": case_studies_main(),
    },
    "privacy.html": {
        "title": "Privacy notice - Trion Consultancy Services",
        "description": "How Trion collects, uses, shares, and safeguards personal information.",
        "main_html": privacy_main(),
    },
    "cookies.html": {
        "title": "Cookies - Trion Consultancy Services",
        "description": "Information about the cookies this website uses and how to manage your preferences.",
        "main_html": cookies_main(),
    },
    "terms.html": {
        "title": "Terms of use - Trion Consultancy Services",
        "description": "Terms governing your use of the Trion Consultancy Services website.",
        "main_html": terms_main(),
    },
    "accessibility.html": {
        "title": "Accessibility - Trion Consultancy Services",
        "description": "Trion's commitment to accessibility, the standards we target, known limitations, and how to give us feedback.",
        "main_html": accessibility_main(),
    },
}


# -- Re-emit existing pages with updated chrome -----------------------------

EXISTING_PAGES = {
    "index.html":     ("Trion Consultancy Services - Building on belief",
                        "Trion Consultancy Services partners with the world's largest enterprises to design and run their digital transformation - across cloud, AI, cybersecurity, and operations."),
    "about.html":     ("About - Trion Consultancy Services",
                        "For 56 years we have helped the world's largest organizations transform. Get to know the people, the purpose, and the philosophy behind Trion Consultancy Services."),
    "services.html":  ("What we do - Trion Consultancy Services",
                        "From cloud and AI to cybersecurity, engineering, and managed operations - explore the full set of services Trion delivers to the world's largest enterprises."),
    "industries.html":("Industries - Trion Consultancy Services",
                        "Trion brings deep industry knowledge to banking, insurance, manufacturing, retail, healthcare, public services, communications, and energy."),
    "contact.html":   ("Contact - Trion Consultancy Services",
                        "Start a conversation with Trion Consultancy Services. Find an office near you, or send us a note and we will respond within two business days."),
}

MAIN_RE = re.compile(r"<main[^>]*>(.*?)</main>", re.DOTALL)


def emit_page(path: Path, title: str, description: str, main_inner: str) -> None:
    main_inner = main_inner.strip("\n")
    body = f'  <main id="main">\n{main_inner}\n  </main>\n'
    full = CHROME_TOP.format(title=title, description=description) + body + CHROME_BOTTOM
    path.write_text(full, encoding="utf-8")


def main() -> int:
    written = []

    # Regenerate existing pages, preserving their <main> bodies.
    for filename, (title, description) in EXISTING_PAGES.items():
        path = SITE_DIR / filename
        if not path.exists():
            raise SystemExit(f"missing source page: {path}")
        old = path.read_text(encoding="utf-8")
        m = MAIN_RE.search(old)
        if not m:
            raise SystemExit(f"no <main> block in {path}")
        main_inner = m.group(1)
        emit_page(path, title, description, main_inner)
        written.append(filename)

    # Generate new stub pages.
    for filename, cfg in STUB_PAGES.items():
        path = SITE_DIR / filename
        emit_page(path, cfg["title"], cfg["description"], cfg["main_html"])
        written.append(filename)

    print(f"Wrote {len(written)} pages:")
    for name in written:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
