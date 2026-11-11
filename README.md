# Araya design preview

Static review preview for PT Araya Internusa, preserving the existing website's orange/charcoal/white industrial styling and Space Grotesk typography.

Preview: https://arayainternusa.github.io/arayaweb/

Repository: https://github.com/arayainternusa/arayaweb/ — public. Transfer and CI/CD verification: [29 October notes](docs/REPOSITORY-TRANSFER-2026-10-29.md).

Organization rename and preview URL migration: [30 October notes](docs/GITHUB-ORGANIZATION-RENAME-2026-10-30.md).

Saved audit findings, design decisions, verification results and next steps: [Project notes](docs/PROJECT-NOTES.md).

Start with the [documentation index](docs/README.md), [progress/release record](docs/PROGRESS.md) and [content sources](docs/CONTENT-SOURCES.md). Static production launched from [2d59720](https://github.com/hakiimm8/arayaweb/commit/2d5972009badeeb3ff9bbf9eefc01bca6b182472); later main pushes automatically deploy after CI passes. Authorised-distributor positioning and service SEO: [implementation notes](docs/SEO-IMPROVEMENTS-2026-10-15.md). Leadership immediately precedes Get in Touch. Leadership and balanced service photography: [implementation notes](docs/LEADERSHIP-AND-SERVICE-BALANCE-2026-10-14.md). Photo-led services and owner photography: [implementation notes](docs/WORK-PHOTOS-2026-10-14.md). Hierarchy/mobile fixes and verification: [implementation notes](docs/HIERARCHY-FIXES-2026-10-14.md). The 14 October experience improvements are recorded in [implementation notes](docs/IMPROVEMENTS-2026-10-14.md); current deployment status is in the progress/release record.

## Files

- `public/`: the complete published site, with one Araya landing page, Noris and ComAp guides, three legacy service redirects and sitemap.xml.
- `tools/site_content.py`: service content for the single landing page, clients and multi-brand equipment lists.
- `tools/prepare_site_assets.py`: client logos, date-stamp-free responsive photos, the share image and the proportioned logo.
- `tools/build.py`: shared HTML template and page copy. Run `python tools/build.py` after editing.
- `tools/brand_profiles.py` and `tools/brand_pages.py`: researched brand content and dedicated brand-page layout.
- `tools/comap_applications.py`: 18 published application explanations grouped by marine, power generation and smart energy management.
- `.github/workflows/pages.yml`: publishes `public/` on push to main or manual dispatch. No PR triggers.
- `.github/workflows/production-stage.yml`: manually uploads a verified successful main build package into private Rumahweb staging. It does not activate the website.

The build templates require Python 3.12 or newer.

## Production preparation

Target domain: `https://arayainternusa.co.id/`. Run `python tools/build.py --target production`, `python tools/check.py --target production` and `python tools/package_release.py` to create an isolated production ZIP and checksum manifest under ignored `dist/`. After successful main CI and noindex preview publication, `production.yml` automatically validates and uploads that exact package through pinned SSH, activates an immutable static release and checks every public file over HTTPS. Failed live checks trigger guarded rollback. No database or company-profile download is required. [Launch, backups and manual recovery](docs/PRODUCTION-LAUNCH-2026-10-15.md).

Read the [deployment runbook](docs/PRODUCTION-DEPLOYMENT.md) for the SSH recommendation, verified root redirect, first-cutover and rollback requirements. Production WordPress remains unchanged until a separately approved live cutover.

Owner-approved SSH access and the main-restricted GitHub `production` environment are configured. Use the manual **Stage production package on Rumahweb** workflow with the successful build run ID. Its validator checks repository/workflow/branch provenance, clean source, ZIP and individual file hashes, and safe publication paths before upload. See the [staging implementation record](docs/PRODUCTION-SSH-PLAN-2026-10-14.md).

Current structure and automatic years: [implementation notes](docs/LANDING-AND-DATES-2026-10-14.md). Date regression checks: node tools/test_company_dates.cjs.

To preview locally, serve `public/` with a static HTTP server. WordPress and PHP are not required for this preview.

The **Brand Partners** dropdown and footer brand links are generated from `BRANDS` in `tools/brand_profiles.py`. See [adding a future partner](docs/BRAND-MAINTENANCE.md). The homepage has individual Noris and ComAp buttons.

## Scope and sources

This is a public design preview with noindex,nofollow metadata. The production WordPress site remains at https://arayainternusa.co.id/araya/. Preview hosting performance does not represent production WordPress performance.

Existing Araya logo, engineering photographs, company history, and displayed business contacts come from the owner's supplied website files and live site. Email/phone destinations have been aligned with their displayed labels; deliverability has not been tested. No enquiry is automatically sent. Service and brand links stay within the preview, with separate links to manufacturer references.

Marine and industrial sections describe project scopes provided by the owner and the existing service pages. They are capability descriptions, not invented named case studies. Product families, example models, and 14 manufacturer product images have source attribution in [Content sources](docs/CONTENT-SOURCES.md). Model availability and project suitability require discussion with Araya.

Dedicated Noris and ComAp guides include manufacturer background, grouped product information, an informational equipment brief and expandable FAQs. Only the final shared contact section has enquiry CTA buttons. Noris covers eight product areas; ComAp covers six. These are Araya's brand guides for Indonesia; manufacturer links lead to current product details and documents.

The owner confirmed that Araya holds the appointment letter as the sole authorised distributor for NORIS in Indonesia. ComAp uses the authorised distributor designation. General certification wording is owner-approved.

Manufacturer application sources checked 2026-10-08:

- https://www.noris-group.com/industries/shipbuilding
- https://www.comap-control.com/products/controllers/

Space Grotesk is distributed under the SIL Open Font License; see `public/assets/fonts/OFL.txt` and https://github.com/google/fonts/tree/main/ofl/spacegrotesk.

WordPress files, database exports, private configuration, backups and logs are not part of this repository or deployment artifact.

ComAp now leads with an expandable application guide and real manufacturer system diagrams before the product catalogue. See [application sources and scope](docs/COMAP-APPLICATIONS.md).

Noris includes noriNet remote vessel monitoring, a manufacturer dashboard picture and a zoomable vessel-to-shore system diagram. See [NORINET research and implementation](docs/NORINET-RESEARCH.md).


Noris presents two visible product groups. ComAp has two Contents choices: Applications and Products, with application explanations first. Per-entry actions and related-page promotions are removed. See [current owner decisions and verification](docs/BRAND-SIMPLIFICATION-AND-MOTION-2026-10-14.md).


Image discovery, lighter motion, finite metric counters and profile-derived SVG branding: [implementation and verification](docs/LOADING-COUNTERS-AND-BRANDING-2026-10-14.md). Run `python tools/test_loading.py` and `node tools/test_counters.cjs` after relevant changes.
