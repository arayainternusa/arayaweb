# Adding a brand partner

On 11 November 2026, the owner confirmed that Araya holds the appointment letter as the **sole authorised distributor for NORIS in Indonesia**. The homepage and both NORIS language pages use this designation. ComAp uses **authorised distributor**. This updates the October designation for NORIS.

Current relationship wording is explicit in each brand's `intro`, `description`, `title` and `local` fields. `local` supplies the Araya relationship paragraph in the manufacturer profile. Noris and ComAp use the owner's 15 October approved **authorised distributor** designation; a new brand must use its own confirmed relationship. Do not infer authorisation, exclusivity or named credentials from the shared renderer.

The shared header uses a **Brand Partners** dropdown with separate Noris and ComAp links. Dropdown links, footer brand links and generated brand routes come from `BRANDS` in `tools/brand_profiles.py`. The homepage keeps separate Explore Noris / Explore ComAp buttons.

## Add a confirmed future partner

1. Add a new entry to `BRANDS` using an existing entry as the structure. Use a unique URL-safe key such as the confirmed brand's slug; its route becomes `/<key>/` under the GitHub project path.
2. Fill in the name, metadata, heading, profile, product families, applications, enquiry checklist, FAQs and relevant service connections. Use accurate Araya relationship wording and manufacturer sources. Adapt model and compatibility statements to the brand.
3. Set the `other` cross-brand link to an existing brand key, and provide its link label.
4. Add a permitted product image under `public/assets/images/` and specify its file, actual dimensions, alt text, source page and attribution. If useful, add its download to the optional `tools/fetch_brand_assets.py` helper. Do not generate or redraw manufacturer logos/products.
5. Run `python tools/build.py`. It generates the new page and adds its menu/footer link on every page. The renderer is shared in `tools/brand_pages.py`; no separate menu markup is required.
6. If the new brand should appear prominently on the homepage, add a card/button in `HOME` inside `tools/build.py`. Homepage featured cards/buttons are curated separately from the full partner menu.
7. Update [content sources](CONTENT-SOURCES.md), [project notes](PROJECT-NOTES.md) and [progress](PROGRESS.md). Record any unconfirmed inventory, approvals, service scope or image rights.
8. Run `python tools/check.py`, `node --check public/assets/site.js` and `git diff --check`. Check desktop/mobile dropdown behaviour, keyboard access, the new route, images, metadata, enquiry links and relative paths from nested pages before publishing.

## Dropdown behaviour

- Native HTML details/summary provides click and keyboard opening, including without JavaScript.
- Escape closes the dropdown and returns focus to its summary. On mobile, a further Escape closes the outer navigation.
- Outside clicks and focus moving out of the partner group close it. Choosing a link closes navigation.
- The mobile dropdown expands within the navigation; desktop uses an anchored panel.
- CSS and JavaScript URLs include content hashes so new markup gets matching changed assets.

There is no practical brand-count limit in the data model, but retest the dropdown height and mobile navigation when adding more entries. Add only confirmed partners and real content; no placeholder partner is included in the current menu.


## Product-section pictures

Each product entry can include an optional `image` dictionary: `file`, actual `width` and `height`, descriptive `alt`, and a short `caption`. Place the real manufacturer WebP file in `public/assets/images/`; the shared renderer adds a lazy-loaded figure below the family heading and credits the brand with a link to that product’s `source`. It contains the complete image without cropping or stretching. Example software screens must be described as examples. Keep download URLs in `tools/fetch_brand_assets.py` and provenance in `CONTENT-SOURCES.md`. Omit the image dictionary when no suitable image is available. Rebuild and check both desktop and mobile after changing images.


## Detailed application guides

ComAp uses optional `application_groups` from `tools/comap_applications.py`. Each group contains a stable anchor, title, introduction, conceptual flow, credited diagram and application entries. Entries have purpose, typical system, control functions, example families, selection inputs, related anchors and manufacturer source. The shared `application_guide` renderer in `brand_pages.py` places this before products when the field exists. Application reference URLs stay in the research data/docs; the informational page omits per-entry shortcut links. All application entries are closed initially and use native details/summary. JavaScript opens an entry referenced by a hash or related link. Retest keyboard, direct hashes, related links, mobile widths and the no-JavaScript path after changes. Validate region-specific availability against current manufacturer sources.


### Diagrams and enlarged view

Application entries can have a `diagrams` list; current assignments are in APPLICATION_DIAGRAMS in tools/comap_applications.py. Each picture supplies file, actual width/height, alt and caption; its credit uses the application source. Group diagrams additionally have their own source. The shared diagram_figure helper gives both kinds the same original-image fallback link and viewer trigger. A native dialog is rendered once on pages with a detailed guide or an optional product diagram. JavaScript supplies fit/zoom, scrolling, source/title updates, close handling and focus return. Retest all pictures, modified-click/no-JavaScript fallback, zoom limits, image scrolling, background scroll lock, close/Escape/backdrop and focus return on desktop and mobile after changing the viewer.


### Product system diagrams

A product may also include `diagram` (file, actual width/height, alt, caption), `flow` (ordered explanation steps) and `diagram_note` (interface or operating context). The shared portfolio renderer places this below both product columns at full row width; noriNet is the first example. The product `source` supplies its diagram credit. `diagram_figure` accepts a brand argument, defaulting to ComAp for application guides; product diagrams use the product page's brand. JavaScript updates the modal source label as well as its URL. Keep only one dialog per page and verify both brand credits when changing shared viewer code.

Company content outside the brand guides lives in `tools/site_content.py`: clients, multi-brand equipment and services rendered on the single homepage. Service details are rendered by `tools/landing_services.py`; do not add standalone service routes.


## Simple Contents and reading order

ComAp exposes only Applications and Products in its Contents. Noris lists products in two visible groups using `contents_product_groups`: `(title, [product IDs])` pairs. The full catalogue follows the same groups. Reference every product exactly once and retain stable IDs. No Choose by task, hero actions, per-entry shortcut/actions, persistent section menu or related-page promotion belongs in the guides. CTA buttons are in the final shared contact section; in-page diagram controls remain available. Image credits are plain text and source provenance remains in data/docs. `tools/test_experience.py` verifies topic destinations, counts, reading order and that brand content has no external/page-redirection actions. Rebuild and test desktop/mobile and diagram enlargement after changes. See [current owner decisions](BRAND-SIMPLIFICATION-AND-MOTION-2026-10-14.md).
