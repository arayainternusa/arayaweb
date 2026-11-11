"""Production metadata, isolation and publication safety regression checks."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
import zipfile
import tempfile
from package_release import git_provenance

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / 'dist/production'
BASE = 'https://arayainternusa.co.id/'


def run(*args):
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)


class ProductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.preview_before = {p.relative_to(ROOT / 'public'): p.read_bytes() for p in (ROOT / 'public').rglob('*') if p.is_file()}
        result = run('tools/build.py', '--target', 'production')
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)

    def test_production_does_not_overwrite_preview(self):
        after = {p.relative_to(ROOT / 'public'): p.read_bytes() for p in (ROOT / 'public').rglob('*') if p.is_file()}
        self.assertEqual(self.preview_before, after)

    def test_production_metadata_and_sitemap(self):
        for route in ('', 'noris/', 'comap/', 'noris/id/', 'comap/id/', 'privacy/'):
            html = (PRODUCTION / route / 'index.html').read_text(encoding='utf-8')
            self.assertIn('content="index, follow"', html)
            self.assertIn(f'rel="canonical" href="{BASE}{route}"', html)
            self.assertIn(f'property="og:url" content="{BASE}{route}"', html)
            self.assertNotIn('hakiimm8.github.io', html)
            self.assertNotIn('at-control.github.io', html)
            self.assertNotIn('arayainternusa.github.io', html)
            self.assertNotIn('https://arayainternusa.co.id/araya/', html)
        sitemap = (PRODUCTION / 'sitemap.xml').read_text(encoding='utf-8')
        self.assertEqual(sitemap.count('<loc>'), 6)
        self.assertIn(f'<loc>{BASE}comap/</loc>', sitemap)
        self.assertIn(f'Sitemap: {BASE}sitemap.xml', (PRODUCTION / 'robots.txt').read_text())
        for key in ('marine', 'industrial', 'automation'):
            self.assertIn('content="noindex, follow"', (PRODUCTION / key / 'index.html').read_text(encoding='utf-8'))

    def test_indonesian_brand_pages_have_reciprocal_language_links(self):
        home = (PRODUCTION / 'index.html').read_text(encoding='utf-8')
        for key, name in [('noris', 'NORIS'), ('comap', 'ComAp')]:
            english = (PRODUCTION / key / 'index.html').read_text(encoding='utf-8')
            indonesian = (PRODUCTION / key / 'id/index.html').read_text(encoding='utf-8')
            title = f'Distributor Resmi {name} di Indonesia'
            self.assertIn('<html lang="id">', indonesian)
            self.assertIn(f'<title>{title} | Araya Internusa</title>', indonesian)
            self.assertIn(f'<h1>{title}</h1>', indonesian)
            self.assertIn(f'href="./{key}/id/" lang="id"', home)
            for page in (english, indonesian):
                self.assertIn(f'hreflang="en" href="{BASE}{key}/"', page)
                self.assertIn(f'hreflang="id" href="{BASE}{key}/id/"', page)

    def test_validation_rejects_preview_robots_and_sensitive_files(self):
        home = PRODUCTION / 'index.html'
        original = home.read_bytes()
        try:
            home.write_bytes(original.replace(b'content="index, follow"', b'content="noindex, nofollow"'))
            self.assertNotEqual(run('tools/check.py', '--target', 'production').returncode, 0)
        finally:
            home.write_bytes(original)
        forbidden = PRODUCTION / 'backup.sql'
        try:
            forbidden.write_text('test fixture, no database data')
            self.assertNotEqual(run('tools/package_release.py').returncode, 0)
        finally:
            forbidden.unlink()
        self.assertEqual(run('tools/check.py', '--target', 'production').returncode, 0)

    def test_zip_matches_manifest_and_contains_only_site(self):
        result = run('tools/package_release.py')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        manifest = json.loads((ROOT / 'dist/release.json').read_text())
        archive_path = ROOT / 'dist/araya-production.zip'
        self.assertEqual(manifest['archive_sha256'], hashlib.sha256(archive_path.read_bytes()).hexdigest())
        with zipfile.ZipFile(archive_path) as archive:
            self.assertEqual(set(archive.namelist()), set(manifest['files']))
            self.assertIn('index.html', archive.namelist())
            self.assertIn('assets/site.css', archive.namelist())
            self.assertFalse(any(n.startswith(('public/', 'tools/', '.git/', 'docs/')) for n in archive.namelist()))
            for name in archive.namelist():
                self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), manifest['files'][name])

    def test_source_provenance_distinguishes_generated_dates_from_edits(self):
        with tempfile.TemporaryDirectory(prefix='araya-provenance-') as folder:
            root = Path(folder)
            def git(*args):
                subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
            (root / 'public/assets').mkdir(parents=True)
            (root / 'tools').mkdir()
            sitemap = root / 'public/sitemap.xml'
            sitemap.write_text('yesterday')
            asset = root / 'public/assets/site.css'
            asset.write_text('body {}')
            template = root / 'tools/build.py'
            template.write_text('# source')
            git('init')
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'fixture')
            self.assertFalse(git_provenance(root)['source_tree_dirty'])
            sitemap.write_text('today')
            self.assertTrue(git_provenance(root)['working_tree_dirty'])
            self.assertFalse(git_provenance(root)['source_tree_dirty'])
            asset.write_text('body {color:red}')
            self.assertTrue(git_provenance(root)['source_tree_dirty'])
            asset.write_text('body {}')
            template.write_text('# changed source')
            self.assertTrue(git_provenance(root)['source_tree_dirty'])
            template.write_text('# source')
            (root / 'new-source.txt').write_text('untracked source')
            self.assertTrue(git_provenance(root)['source_tree_dirty'])


if __name__ == '__main__':
    unittest.main()
