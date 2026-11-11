# Bilingual brand pages and Project2 removal

## Brand pages

- The English guides remain at `/noris/` and `/comap/`, including their technical detail and diagrams.
- `/noris/id/` and `/comap/id/` are shorter Bahasa Indonesia buyer guides. They cover product families, example models, selected manufacturer diagrams, and the information needed for a quotation. Contact and consent controls use Bahasa Indonesia. The privacy notice is labelled as English.
- The homepage brand cards link to the Indonesian guides. Each guide has a visible language switch and reciprocal `en` and `id` hreflang links. Each URL has its own canonical address and sitemap entry.
- Both NORIS guides use the official noriStar bridge panel photograph in the hero and propulsion sections. The speed sensors retain their own product photo.
- Preview HTML uses noindex. The production build enables indexing for both languages and includes the new routes in the package and HTTPS verification. The owner reviewed the local preview and approved production deployment. After deployment, request indexing for the two new URLs in Search Console.

## Retired WordPress result

Search Console showed that `https://arayainternusa.co.id/araya/project2/` was still indexed. The live server returns HTTP 410 for this route and the current sitemap excludes it. An exact-URL temporary removal request was submitted on 11 November 2026. Google showed “Processing request” after submission. The existing HTTP 410 remains the permanent signal when Google recrawls the URL.

Sources for the search configuration and removal behaviour are [Google’s localized version guidance](https://developers.google.com/search/docs/specialty/international/localized-versions) and [Search Console Removals](https://support.google.com/webmasters/answer/9689846).
