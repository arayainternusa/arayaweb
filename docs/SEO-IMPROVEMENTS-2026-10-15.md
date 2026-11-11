# Implemented SEO improvements — 15 October 2026

The owner selected **authorised distributor** for Noris and ComAp and authorised the other improvements proposed in the [14 October SEO review](SEO-REVIEW-2026-10-14.md). This pass keeps the approved single landing page, separate brand pages, visual style, final-section enquiries and leadership placement.

## Metadata and brand positioning

| Page | Updated title |
| --- | --- |
| Home | Marine & Industrial Automation Indonesia \| Araya Internusa |
| Noris | Noris Authorised Distributor Indonesia \| Araya Internusa |
| ComAp | ComAp Authorised Distributor Indonesia \| Araya Internusa |

Updated all three descriptions and generated Open Graph titles/descriptions. Brand hero introductions now state the authorised-distributor role and core engineering scope. The shared homepage partner introduction uses the same designation. Manufacturer company labels and technology H1s remain as approved, with no geographic suffix added to the company labels.

The profile renderer now reads each brand's `local` relationship statement from its data, so future brands do not automatically inherit an authorised status. The designation is owner-directed business copy; no manufacturer appointment document, validity period, exclusive territory or new credential has been independently verified in this pass. Exact certificates and publishable appointment evidence can be added when supplied.

## Service content

Expanded the existing 30 service explanations with relevant work scope and equipment/interface context. Added two previously owner-mentioned scopes: **water-level monitoring** and **cargo monitoring systems**. Marine now has 12 scopes, Industrial 8 and Automation & Electrical 12: **32 total**.

Existing anchors remain. Updated the existing marine headings/copy to explicitly cover:

- Fire alarm, general alarm and alarm monitoring systems (AMS).
- Engine overhaul, repair, control, throttle and monitoring.
- Generator synchronisation, load sharing and automatic start/stop.
- Steering alongside manoeuvring, CPP and bow thrusters.

The two new anchors are `#marine-water-level` and `#marine-cargo-monitoring`. These scopes come from the owner's earlier service list; the original company profile supports the other service families. Descriptions explain the existing offer without claiming named project outcomes, inventory, product approvals or manufacturer certification.

Full explanations remain in the native disclosures and initial HTML. Collapsed photo-led service features, column-first reading order, final Contact section and absence of repeated per-sector actions are retained. English remains the website language; no hidden keyword list, thin city pages or additional service routes were added.

## Structured data and indexing

- Company `knowsAbout` now reflects AMS, engine overhaul/control, generator synchronisation/load sharing and water-level/cargo monitoring.
- Company schema logo points to the existing sharp original orange emblem SVG, which is readable on a light background.
- Visible brand FAQs remain; removed FAQPage JSON-LD following Google's [retirement of FAQ rich results in May 2026](https://developers.google.com/search/updates#may-2026). Company/service and breadcrumb schema remain. This is cleanup, not a claimed ranking gain.
- Preview retains `noindex, nofollow`. The production candidate retains `index, follow`, company-domain canonicals, a three-page sitemap and discovery settings.

## Migration preparation

[Legacy URL map](LEGACY-URL-MAP-2026-10-15.csv) records all 65 published URLs from the verified WordPress export. Ten have equivalent new-content destinations: home, two About routes, services, three sector routes, Team and two Contact routes.

The remaining 55 are marked for content review or likely demo retirement. A slug alone is insufficient to determine a page's business value. Existing project/article/store pages must be reviewed before choosing preservation, consolidation or a real 404/410. No blanket homepage redirect or active server change was made. The CSV is a cutover planning artifact, not an installed redirect configuration.

## Verification

- Preview build/static validator: six routes, local links/assets/fragments, one H1, metadata and no PR-triggered workflows pass.
- Experience (6), hierarchy (4), loading (3), production (5) checks and JavaScript syntax pass.
- Manual source checks verify all prior homepage IDs remain, all 32 scopes exist in initial HTML, brand title/description/visible role wording match, obsolete FAQPage markup is absent and target-specific indexing stays intact.
- Browser: Noris and ComAp introductions render correctly; ComAp still has 18 applications and 6 product families. Checked 390px mobile, 355px narrow mobile and 1280px desktop without horizontal overflow. Expanded service lists remain one column on mobile/two on desktop. Generator bookmark opens the marine disclosure and clears the sticky header. Leadership remains the final main section before Get in Touch.
- Screenshots and browser observations are retained privately under the owner's `docs/evidence/seo-improvements-20261015/`. The local HTTP preview was restarted on port 8767 after the previous session ended.

Publication status is recorded in [Progress](PROGRESS.md). No fresh Core Web Vitals result is asserted; the audit's PageSpeed API request was rate limited. Live WordPress activation is separate from this preview/content update.

## Remaining inputs and launch work

1. Publishable appointment/certificate details: exact designation, issuer, scope and validity; general owner-approved wording is already implemented.
2. Real project examples: vessel/site description, system, problem, Araya scope, outcome and permission-cleared photos. No case studies were invented from generic work photographs.
3. Search Console, analytics and Business Profile access/verification after production launch; production sitemap submission and live indexing/redirect checks.

## NORIS search visibility follow-up — 11 November 2026

Google Indonesia omitted Araya from the first page and AI Overview for the distributor query. The production NORIS URL returned HTTP 200, allowed indexing, used a self-referencing canonical and appeared in the sitemap. A Google `site:` check returned no result for the NORIS URL. URL Inspection is needed to establish its indexing status.

The NORIS title, description and main heading now identify the page as an authorised distributor page for Indonesia. The introduction names PT Araya Internusa and NORIS Group GmbH. The homepage states the authorised distributor relationship for both NORIS and ComAp and links directly to the NORIS page. The production homepage carries the HTML tag for Search Console URL-prefix verification. After deployment, use the verified property to submit `sitemap.xml` and inspect and request indexing for `/noris/`.
4. Decisions for the 55 legacy pages without a confirmed equivalent, followed by reviewed live activation and permanent server redirects.
5. Fresh mobile performance/field data on the actual production site. Indonesian translations remain an optional future content decision.
