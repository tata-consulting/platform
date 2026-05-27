# Contributing

Thanks for your interest in improving this site. This document explains how to set up the project locally, how the code is organized, and the conventions we follow so changes stay consistent.

## What this is

A static marketing site for Trion Consultancy Services. Plain HTML, CSS, and vanilla JavaScript, with no runtime build step. A Python script generates pages from a shared chrome template so the header, nav, and footer stay in sync across the site.

## Prerequisites

- Python 3.9+ (for the generator and the local server)
- A modern browser (Chrome, Firefox, Safari, or Edge - all current)
- Git

No npm, no bundler, no framework runtime.

## Run it locally

```bash
git clone <repo-url>
cd platform
python3 -m http.server 8765 --directory site
```

Open `http://localhost:8765/` in your browser.

You can also open any `site/*.html` directly from the filesystem (`file://`), but a few features (the Inter web font, intra-page anchors) work better over HTTP.

## Project layout

```
platform/
├── site/                       The production output - HTML, CSS, JS, assets
│   ├── index.html              Home
│   ├── about.html              Page-specific content lives in <main>
│   ├── services.html           ...
│   ├── ...                     (20 pages total)
│   ├── css/
│   │   ├── base.css            Reset, design tokens, typography, layout primitives
│   │   └── components.css      Buttons, cards, header, footer, forms, etc.
│   ├── js/
│   │   └── main.js             Sticky header, mega-menu, mobile menu, reveal-on-scroll, form handlers
│   ├── assets/                 Logo, imagery
│   └── favicon.svg
│
├── scripts/
│   └── generate-site.py        Single source of truth for shared chrome + page configs
│
├── docs/                       Design specs, internal notes
├── .github/workflows/          CI for GitHub Pages deployment
└── CONTRIBUTING.md             This file
```

## Making changes

### Editing existing page content

Each page's unique content lives between `<main id="main">` and `</main>` in the corresponding `site/*.html`. Edit the file directly.

The generator preserves whatever is inside `<main>` when it re-emits a page, so direct edits to a page's body are safe across regenerations.

### Changing the header, footer, nav, or any chrome

These live in `scripts/generate-site.py` (in `CHROME_TOP` and `CHROME_BOTTOM`). After editing the template:

```bash
python3 scripts/generate-site.py
```

This re-emits all 20 pages with the new chrome while preserving each page's `<main>`. Commit the regenerated HTML alongside the generator change.

### Adding a new page

1. Add a config entry to `STUB_PAGES` in `scripts/generate-site.py` with `title`, `description`, and `main_html` (or write a `*_main()` helper that returns the body markup).
2. Add a link to the new page wherever it belongs: primary nav, mega menu, footer columns, footer legal row, mobile menu - all in `CHROME_TOP` / `CHROME_BOTTOM`.
3. Run the generator.
4. Open the new page in the browser and verify it loads cleanly.

### Styling

- Design tokens (colors, spacing, type scale, motion timing, breakpoints) live as CSS custom properties on `:root` in `site/css/base.css`. Add new tokens there; don't hardcode values in components.
- Component styles live in `site/css/components.css`, grouped by component with header comments.
- Mobile-first - default rules target the smallest viewport, then `@media (min-width: ...)` adds desktop styles.
- BEM-ish naming: `.block`, `.block__element`, `.block--modifier`. Stick to it for new components.
- Avoid `!important` unless documenting why in a comment.

### JavaScript

- Vanilla, no dependencies.
- Everything runs inside the IIFE in `site/js/main.js`.
- Feature-detect (`'IntersectionObserver' in window`) and degrade gracefully when an API is missing.
- Respect `prefers-reduced-motion` for any animation.

## Conventions

### HTML

- Use semantic landmarks: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`.
- Every page starts with a skip link to `#main`.
- Interactive elements that aren't links or form controls should be `<button>` with the right `aria-*` attributes.
- Icons are inline SVG with `aria-hidden="true"` if decorative, or an accompanying `<span class="sr-only">` label if functional.

### Accessibility

We target WCAG 2.2 AA. Before opening a PR that touches markup or CSS, verify:

- Tab order is logical and every interactive element has a visible focus state.
- Text contrast is at least 4.5:1 against its background (3:1 for large text).
- All images have meaningful `alt` text or `alt=""` if decorative.
- Any animation respects `prefers-reduced-motion`.
- The page works with JavaScript disabled - content should be readable even without `.reveal` animations firing.

### Copy

- Direct and specific. No marketing fluff, no superlatives without numbers behind them.
- Use the `-` character (hyphen or surrounded by spaces), never `—` (em dash).
- Sentence case for headlines (capitalize first word + proper nouns only).
- Numbers above 10 as digits; spell out "one" through "nine" unless they're part of a measurement.

### Comments in code

Write a comment only when the *why* isn't obvious from the code. Don't restate *what* the code does.

## Verifying changes before a PR

For every page you touched:

1. Load it at `http://localhost:8765/<page>.html`.
2. Open DevTools - no errors or warnings in the console, no failed network requests (favicon may 404 in some browsers if the page is opened over `file://`; over HTTP it should be clean).
3. Tab through the page. Focus should move predictably and every interactive element should have a visible focus ring.
4. Resize the window from ~360px (mobile) to 1440px+ (desktop). The layout should reflow without overflow or clipped content.
5. Test the mobile menu (hamburger), mega menu (hover on desktop, click on touch), and any forms.

For chrome changes (anything emitted by the generator):

6. Spot-check three or four representative pages, not just one - the chrome is shared, so a bug shows up everywhere.

## Commits and pull requests

- Sign off every commit: `git commit -s`. When rebasing: `git rebase --signoff`.
- Prefer small, focused commits over one large commit.
- Commit message format: `type: short imperative summary` where `type` is one of `feat`, `fix`, `docs`, `chore`, `refactor`, or `style`. Example: `feat: add sustainability page` or `fix: dark-section service tile contrast`.
- The PR description should explain the *why* and link to any related issue. Include screenshots for visible changes.

PR checklist:

- [ ] All affected pages load without console errors
- [ ] Manual verification per the list above
- [ ] Generator was re-run if the chrome was edited
- [ ] No `console.log` left in `main.js`
- [ ] Commit messages signed off

## Reporting bugs and requesting features

Open an issue with:

- What you expected to happen
- What actually happened
- Steps to reproduce, including the URL and browser/version
- A screenshot if the issue is visual

## Code of Conduct

By participating in this project you agree to abide by the project's `GOVERNANCE.md`. Be kind, be specific, assume good intent.

## Questions

If something here is unclear, open an issue tagged `question` rather than guessing.
