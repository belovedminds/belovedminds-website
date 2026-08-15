# Beloved Minds — Marketing Website

Daily AI-powered phone calls for memory care and assisted living
residents. This repository contains the public marketing site at
**belovedminds.care**.

> **Proprietary and confidential.** © 2026 SkyHold Technologies, LLC, an Idaho
> limited liability company. All rights reserved. Beloved Minds is a product and
> brand of SkyHold Technologies, LLC. This is **not** open source — use requires
> a purchased license. See [LICENSE](LICENSE).

---

## Contents

- [Overview](#overview)
- [Tech stack](#tech-stack)
- [Repository layout](#repository-layout)
- [How the theme build works](#how-the-theme-build-works) ← **read before editing**
- [Local development](#local-development)
- [Deployment](#deployment)
- [Routes](#routes)
- [Open items](#open-items)
- [Contact](#contact)

---

## Overview

A single-page marketing site aimed at memory care and assisted living
**facility operators** (not direct-to-consumer). It covers the problem framing,
how the daily call works, the platform feature set, mission and vision, the
facility offering, the giving-back program, the founding team, and a pilot
inquiry form.

The site is intentionally dependency-free: no framework, no bundler, no npm.
Everything is hand-written HTML with an inline `<style>` block, plus a small
Python script that generates color variants.

## Tech stack

| Layer | Choice |
| --- | --- |
| Markup | Static HTML5, single page |
| Styling | Inline `<style>` block, CSS custom properties for the palette |
| Fonts | System font stacks only (no webfont requests) |
| JavaScript | A small inline script (mobile menu toggle, form guard) — no framework |
| Theming | `build-variants.py` (Python 3, standard library only) |
| Hosting | AWS Amplify Hosting (static) |

No build step is required to deploy — Amplify serves the committed HTML directly.
The Python script is a **local authoring tool**, not part of the deploy pipeline.

## Repository layout

```
├── template.html            ← SOURCE OF TRUTH. Edit this file.
├── index.html               ← GENERATED. The live site (Royal Plum theme).
├── build-variants.py        ← Regenerates index.html + all variants.
├── privacy.html             ← Standalone policy page (draft — legal review pending).
├── terms.html               ← Standalone policy page (draft — legal review pending).
├── cancellation.html        ← Standalone policy page (draft — legal review pending).
├── plum/index.html          ← GENERATED. Same page as index.html, serves at /plum.
├── archive/                 ← GENERATED. Retired looks, each with an "archived" banner.
│   ├── heritage/index.html  ←   Heritage Green (the original look) → /archive/heritage
│   ├── slate/index.html     ←   Slate Blue → /archive/slate
│   └── clay/index.html      ←   Warm Clay → /archive/clay
└── assets/
    ├── logo-gold.png        ← Beloved Hands mark (blended, masked)
    ├── logo-color.png       ← Nav logo
    ├── beacon.jpg           ← Footer lighthouse (cropped to the tower in CSS)
    ├── doves.jpg / constellation.jpg / seal.png / Mom.png / family-morning.jpg
    │                        ← Section artwork and founder photo
    ├── loretta-williams.jpg / alessandra-la-bruzzo.jpg / lucile-cameron.jpg
    │                        ← "In loving memory" tribute photos (web-optimized)
    └── favicon.svg / -32.png / -180.png
```

## How the theme build works

**This is the one thing to understand before editing anything.**

`template.html` is the source of truth. `index.html`, `plum/`, and `archive/`
are **generated output**. If you edit `index.html` directly, your
changes are silently destroyed the next time anyone runs the build script.

```
                        ┌─→ index.html                    (Royal Plum — the live site)
template.html ──build──→├─→ plum/index.html               (same page, ../ asset paths)
                        └─→ archive/*/index.html          (heritage, slate, clay + banner)
```

`build-variants.py` holds a `THEMES` list. Each theme supplies only a set of CSS
custom properties (and optionally a few extra CSS rules for a distinct feel).
The script regex-replaces the `:root{...}` block and the `theme-color` meta tag,
so **page content never forks across themes** — there is exactly one copy of the
copy, markup, and layout.

`DEFAULT_SLUG = "plum"` marks which theme becomes the live `index.html`. Royal
Plum was selected in July 2026; the other three are kept buildable but are
written to `archive/<slug>/` with a banner linking back to the live site.

### Editing workflow

```bash
# 1. Edit the source
$EDITOR template.html

# 2. Regenerate index.html and all variants
python build-variants.py

# 3. Review, then commit BOTH template.html and the generated files
git add template.html index.html plum/ archive/
git commit -m "…"
```

Generated files are committed to the repo on purpose — Amplify deploys them
as-is with no build step.

### Changing the palette

Edit the `vars` dict for the relevant theme in `build-variants.py`, then rerun
it. To promote a different look to the live site, change `DEFAULT_SLUG` and
rerun. Note that the archive-vs-live split also affects asset path prefixes
(`""` for `index.html`, `"../"` for `plum/`, `"../../"` for `archive/*/`),
which the script handles automatically.

The script reads and writes UTF-8 explicitly, so it behaves the same on Windows
(where the locale default would otherwise be cp1252 and fail on the em dashes
and symbols in the page) as it does on macOS and Linux.

## Local development

No install, no dependencies. Serve the directory over HTTP:

```bash
python -m http.server 8000
# → http://localhost:8000
```

Opening `index.html` directly via `file://` mostly works, but serving over HTTP
is recommended so relative asset paths and the root-relative links (footer
policy pages) behave the way they do in production.

Requires Python 3 only if you need to regenerate themes.

## Deployment

Hosted on **AWS Amplify Hosting** as a static site (no build command, output
directory `/`). Pushing to `main` triggers a deploy.

Clean URLs need **no host configuration**: each variant is generated as a
directory index (`plum/index.html`, `archive/heritage/index.html`, …), so any
static host serves them at:

| URL | Serves |
| --- | --- |
| `/` | `index.html` (live site) |
| `/plum` | `plum/index.html` |
| `/archive/heritage` | `archive/heritage/index.html` |
| `/archive/slate` | `archive/slate/index.html` |
| `/archive/clay` | `archive/clay/index.html` |

The `/plum` review link was shared with stakeholders — keep it working even
though it now mirrors the live site.

## Routes

The live page is a single scrolling document. In-page anchors:

`#top` · `#mission` · `#how` · `#facilities` · `#families` · `#values` · `#giving` · `#team` · `#contact`

## Open items

Marked in the source with `<!-- EDIT: -->` comments:

- [x] **Contact form wired to Formspree** — posts to
      `https://formspree.io/f/xgawzrgd`. Submits via fetch so the visitor stays
      on the page, with the form's own `action`/`method` as a no-JS fallback.
      Includes a honeypot field and a subject line.
- [x] **`privacy.html`** — rebuilt from the counsel-drafted HIPAA Privacy Policy
      (v1.0, effective 2026-08-15). Public-facing adaptation, not the verbatim
      internal document, which is marked Confidential. Adds a website-visitor section.
- [x] **`cancellation.html`** — the counsel-drafted Cancellation Policy, near-verbatim.
      Effective date set to 2026-08-13; the source document leaves it blank, so set
      the same date on the signed copy.
- [ ] **`terms.html` — short "Website Terms," not counsel-drafted.** Deliberately
      narrow: site is informational, signed agreements control, not-a-medical-service
      disclaimer, IP/seal, no warranty. Worth a glance from counsel, but it creates no
      contractual rights by design so it cannot conflict with the FSA.
- [ ] **Hero card profile is invented.** The "Resident care profile" card in the hero
      (engagement level, confusion response, conversation topics) is placeholder content.
      Rebecca to supply a real, permissioned, anonymized profile. Marked `<!-- EDIT: -->`
      in `template.html`.
- [x] **Contact form wired to Formspree** (`https://formspree.io/f/xgawzrgd`). Submissions open the sender's mail client addressed
      to support@belovedminds.care — they are not delivered server-side, so some will be
      lost. Swap `action` to a Formspree/Resend endpoint for real inbox delivery.
- [ ] **Photography for "What Makes Us Different"** — pending from stakeholder.
- [ ] **Footer entity name** reads "Beloved Minds LLC," which does not match the
      SkyHold Technologies, LLC ownership recorded in [LICENSE](LICENSE).
      Confirm the correct legal entity and align the two.

## Contact

**SkyHold Technologies, LLC** — Idaho, USA

- Rebecca McCallum — Rebeccamccallum@belovedminds.care
- David Beneduci — Davidbeneduci@belovedminds.care

---

*Connecting Hearts & Minds, One Call At A Time.*

Beloved Minds provides daily connection and is not a medical or
emergency service.
