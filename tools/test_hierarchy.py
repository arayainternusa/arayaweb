"""Regression coverage for the owner-approved information hierarchy."""
from pathlib import Path
import re
import unittest
from brand_profiles import BRANDS
from site_content import SERVICES

PUBLIC = Path(__file__).resolve().parents[1] / 'public'


class HierarchyTests(unittest.TestCase):
    def test_service_categories_are_headings_with_preserved_scopes_and_images(self):
        html = (PUBLIC / 'index.html').read_text(encoding='utf-8')
        self.assertNotIn('Explore our services', html)
        self.assertNotIn('class="service-card"', html)
        for key, data in SERVICES.items():
            block = re.search(rf'<article class="service-feature" id="{key}-services".*?</details></article>', html, re.S).group()
            self.assertIn(f'<h3 id="{key}-heading">', block)
            self.assertLess(block.index('class="service-photo"'), block.index('<h3'))
            self.assertIn(f'<details class="service-detail" id="{key}-details">', block)
            self.assertEqual(block.count('class="scope-detail"'), len(data['groups']))
            self.assertIn(data['card_image'], block)
            self.assertIn(f'id="{key}-equipment"', block)
            self.assertNotIn('<a ', block.split('<details', 1)[0])

    def test_brand_section_names_match_contents_and_profile_precedes_index(self):
        for brand in BRANDS:
            html = (PUBLIC / brand / 'index.html').read_text(encoding='utf-8')
            self.assertIn(f'<h2>About {BRANDS[brand]["name"]}</h2>', html)
            self.assertLess(html.index('id="about-brand"'), html.index('id="contents"'))
            portfolio = html.split('id="portfolio"', 1)[1]
            self.assertIn('<h2>Products' + (' &amp; systems' if brand == 'noris' else '') + '</h2>', portfolio)
            self.assertIn('<h2>Equipment details</h2>', html)
        comap = (PUBLIC / 'comap/index.html').read_text(encoding='utf-8')
        section = comap.split('id="applications"', 1)[1]
        self.assertIn('<h2>Applications</h2>', section)
        self.assertEqual(len(re.findall(r'<details class="application-detail".*?<summary>.*?<h4', section, re.S)), 18)

    def test_about_heading_precedes_supporting_photo_in_reading_order(self):
        html = (PUBLIC / 'index.html').read_text(encoding='utf-8')
        about = html.split('id="about"', 1)[1].split('id="services"', 1)[0]
        self.assertLess(about.index('<h2>'), about.index('class="about-media"'))

    def test_expanded_applications_explain_controls_before_diagrams(self):
        html = (PUBLIC / 'comap/index.html').read_text(encoding='utf-8')
        for body in re.findall(r'<div class="application-body">(.*?)</details>', html, re.S):
            if 'class="application-diagrams"' in body:
                self.assertLess(body.index('<dl>'), body.index('class="application-diagrams"'))


if __name__ == '__main__':
    unittest.main()
