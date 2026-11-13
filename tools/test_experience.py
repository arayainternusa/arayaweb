"""Regression checks for enquiry context and navigation in the generated site."""
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

PUBLIC = Path(__file__).resolve().parents[1] / 'public'
SHIP_SERVICE_TOPICS = {
    'perbaikan-kapal': 'perbaikan kapal',
    'perbaikan-kelistrikan-kapal': 'kelistrikan kapal',
    'perbaikan-mesin-kapal': 'perbaikan mesin kapal (ME & AE)',
    'retrofit-kontrol-monitoring-kapal': 'otomasi dan monitoring kapal',
    'perbaikan-kemudi-manuver-kapal': 'sistem kemudi dan manuver kapal',
    'perbaikan-crane-kapal-industri': 'perbaikan crane kapal atau industri',
}


class Links(HTMLParser):
    def __init__(self, path=None, *, html=None):
        super().__init__()
        self.links = []
        self.feed(html if html is not None else path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs))


class ExperienceTests(unittest.TestCase):
    def test_contact_keeps_current_page(self):
        for path in PUBLIC.rglob('index.html'):
            if path.parent.name in {'marine', 'industrial', 'automation', 'perbaikan-kapal-surabaya-gresik'}:
                continue  # These URLs are now compatibility redirects.
            with self.subTest(page=path.parent.name):
                link = next(a for a in Links(path).links if a.get('class') == 'nav-contact')
                self.assertEqual(link['href'], '#contact')

    def test_brand_actions_only_in_final_contact(self):
        for brand in ['noris', 'comap']:
            html = (PUBLIC / brand / 'index.html').read_text(encoding='utf-8')
            body = html.split('<main id="main">', 1)[1].split('</main>', 1)[0]
            for link in Links(html=body).links:
                href = link['href']
                self.assertTrue(href.startswith('#') or href.startswith('../assets/images/'), href)
                self.assertNotIn('button', link.get('class', '').split())
            self.assertNotIn('product-actions', body)
            self.assertNotIn('application-links', body)
            self.assertNotIn('project-connections', body)
            self.assertNotIn('brand-actions', body)
            contact = html.split('<section class="contact"', 1)[1]
            whatsapp = next(a for a in Links(html=contact).links if a.get('class') == 'button')
            draft = parse_qs(urlsplit(whatsapp['href']).query)['text'][0]
            self.assertIn(brand.lower(), draft.lower())

    def test_company_positioning(self):
        html = (PUBLIC / 'index.html').read_text(encoding='utf-8')
        self.assertNotIn('Local engineers', html)
        self.assertNotIn('local talent', html)
        self.assertIn('International technical backing', html)
        self.assertIn('Certified &amp; experienced', html)

    def test_single_landing_page(self):
        html = (PUBLIC / 'index.html').read_text(encoding='utf-8')
        self.assertNotIn('Common requests', html)
        for service in ['marine', 'industrial', 'automation']:
            self.assertIn(f'id="{service}-services"', html)
            self.assertTrue(any(urlsplit(link['href']).fragment == f'{service}-services'
                                for link in Links(html=html).links))
            for page in ['index.html', 'noris/index.html', 'comap/index.html']:
                self.assertNotIn(f'href="./{service}/"', (PUBLIC / page).read_text(encoding='utf-8'))
                self.assertNotIn(f'href="../{service}/"', (PUBLIC / page).read_text(encoding='utf-8'))
        sitemap = (PUBLIC / 'sitemap.xml').read_text(encoding='utf-8')
        self.assertIn('/instalasi-fire-alarm/</loc>', sitemap)
        self.assertEqual(sitemap.count('<url>'), 7 + len(SHIP_SERVICE_TOPICS))

    def test_fire_alarm_service_discovery_and_enquiry(self):
        home = Links(PUBLIC / 'index.html').links
        self.assertTrue(any(link['href'] == './instalasi-fire-alarm/' for link in home))
        page = Links(PUBLIC / 'instalasi-fire-alarm/index.html').links
        whatsapp = next(link for link in page if link.get('data-contact-location') == 'contact'
                        and urlsplit(link['href']).netloc == 'wa.me')
        self.assertIn('sistem fire alarm', parse_qs(urlsplit(whatsapp['href']).query)['text'][0])

    def test_ship_service_pages_are_discoverable_and_keep_the_enquiry_topic(self):
        hub = 'perbaikan-kapal'
        home = (PUBLIC / 'index.html').read_text(encoding='utf-8')
        footer = home.split('class="container footer-grid"', 1)[1]
        self.assertIn(f'./{hub}/', [link['href'] for link in Links(html=footer).links])
        hub_links = [link['href'] for link in Links(PUBLIC / hub / 'index.html').links]
        self.assertIn('../instalasi-fire-alarm/', hub_links)
        sitemap = (PUBLIC / 'sitemap.xml').read_text(encoding='utf-8')
        for slug, topic in SHIP_SERVICE_TOPICS.items():
            with self.subTest(page=slug):
                self.assertIn(f'/{slug}/</loc>', sitemap)
                path = PUBLIC / slug / 'index.html'
                html = path.read_text(encoding='utf-8')
                self.assertIn('<html lang="id">', html)
                self.assertNotIn('<figcaption>', html)
                if slug == 'perbaikan-kelistrikan-kapal':
                    self.assertIn('<h1>Instalasi dan Perbaikan Kelistrikan Kapal</h1>', html)
                    self.assertIn('<h3>Panel Listrik &amp; Switchboard Kapal</h3>', html)
                if slug == 'perbaikan-mesin-kapal':
                    self.assertIn('motor induk (ME) dan motor bantu (AE)', html)
                    self.assertIn('<h3>Safety Device &amp; Kontrol Mesin</h3>', html)
                    self.assertNotIn('genset', html.lower())
                if slug == 'retrofit-kontrol-monitoring-kapal':
                    self.assertIn('<h1>Otomasi &amp; Monitoring Kapal</h1>', html)
                    self.assertIn('<h3>General Alarm Kapal</h3>', html)
                    self.assertIn('<h3>Alarm Monitoring System (AMS)</h3>', html)
                links = Links(html=html).links
                whatsapp = next(link for link in links if link.get('data-contact-location') == 'contact'
                                and urlsplit(link['href']).netloc == 'wa.me')
                self.assertIn(topic, parse_qs(urlsplit(whatsapp['href']).query)['text'][0])
                if slug != hub:
                    self.assertIn(f'../{slug}/', hub_links)
                    self.assertIn(f'../{hub}/', [link['href'] for link in links])

    def test_service_sectors_contain_scopes_without_repeated_promotions(self):
        import re
        from site_content import SERVICES
        html = (PUBLIC / 'index.html').read_text(encoding='utf-8')
        for key, service in SERVICES.items():
            with self.subTest(sector=key):
                block = re.search(rf'<article class="service-feature" id="{key}-services".*?</details></article>', html, re.S).group()
                intro, details = block.split('<details', 1)
                self.assertEqual(Links(html=intro).links, [])
                expected_links = {
                    './instalasi-fire-alarm/', './perbaikan-kelistrikan-kapal/',
                    './perbaikan-mesin-kapal/', './retrofit-kontrol-monitoring-kapal/',
                    './perbaikan-kemudi-manuver-kapal/', './perbaikan-crane-kapal-industri/',
                } if key == 'marine' else set()
                detail_links = [link['href'] for link in Links(html=details).links]
                self.assertCountEqual(detail_links, expected_links)
                self.assertNotIn('What to send us', block)
                self.assertNotIn('service-brand-links', block)
                self.assertEqual(block.count('class="scope-detail"'), len(service['groups']))
                self.assertIn(f'id="{key}-equipment"', block)
        self.assertEqual(html.count('class="brand-panel"'), 2)
        self.assertEqual(html.count('id="contact"'), 1)

    def test_brand_contents_and_reading_flow(self):
        from brand_profiles import BRANDS
        import re
        for brand, data in BRANDS.items():
            html = (PUBLIC / brand / 'index.html').read_text(encoding='utf-8')
            # Limit links to the Contents component so unrelated product links
            # cannot mask a missing index entry.
            contents = re.search(r'<section class="brand-toc".*?</section>', html, re.S).group()
            links = Links(html=contents)
            anchors = {a['href'][1:] for a in links.links}
            expected = {'applications', 'portfolio'} if data.get('application_groups') else {p['id'] for p in data['products']}
            self.assertEqual(anchors, expected, brand)
            if data.get('application_groups'):
                self.assertEqual(html.count('class="application-detail"'), 18)
                self.assertEqual(html.count('class="portfolio-row"'), 6)
            order = ['about-brand', 'contents', 'portfolio', 'brand-faq', 'araya-support']
            if data.get('application_groups'):
                order.insert(2, 'applications')
            else:
                self.assertNotIn('Choose by task', html)
                self.assertNotIn('Choose an application', html)
                self.assertIn('class="brand-toc-group brand-product-group"', contents)
                self.assertNotIn('<details', contents)
                self.assertEqual(html.count('class="portfolio-row"'), 8)
            positions = [html.index(f'id="{anchor}"') for anchor in order]
            self.assertEqual(positions, sorted(positions), brand)
            for anchor in anchors:
                self.assertIn(f'id="{anchor}"', html, brand)


if __name__ == '__main__':
    unittest.main()
