"""Audit the deployable static artifact for broken local links and metadata."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys
import argparse
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
CONTENT_ROUTES = {'index.html', 'noris/index.html', 'comap/index.html', 'noris/id/index.html', 'comap/id/index.html', 'privacy/index.html'}
ALL_ROUTES = CONTENT_ROUTES | {f'{key}/index.html' for key in ('marine', 'industrial', 'automation')}
ASSET_SUFFIXES = {'.css', '.js', '.woff2', '.webp', '.jpg', '.jpeg', '.png', '.svg', '.pdf'}


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.links, self.ids, self.errors = path, [], set(), []
        self.h1, self.description, self.robots = 0, None, None
        self.canonical, self.og_url = None, None
        self.schema, self.in_schema = '', False
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get("id"):
            if data["id"] in self.ids:
                self.errors.append(f"Duplicate id: {data['id']}")
            self.ids.add(data["id"])
        self.h1 += tag == "h1"
        if tag == "meta":
            if data.get("name") == "description":
                self.description = data.get("content")
            if data.get("name") == "robots":
                self.robots = data.get("content")
            if data.get('property') == 'og:url':
                self.og_url = data.get('content')
        if tag == 'link' and data.get('rel') == 'canonical':
            self.canonical = data.get('href')
        if tag == 'script' and data.get('type') == 'application/ld+json':
            self.in_schema = True
        if tag == "img" and not data.get("alt"):
            self.errors.append("Image lacks descriptive alt text")
        for attr in ("href", "src"):
            if attr in data:
                self.links.append(data[attr])

    def handle_data(self, data):
        if self.in_schema:
            self.schema += data

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_schema = False


def main():
    global PUBLIC
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=('preview', 'production'), default='preview')
    args = parser.parse_args()
    production = args.target == 'production'
    PUBLIC = ROOT / 'dist/production' if production else ROOT / 'public'
    base = 'https://arayainternusa.co.id/' if production else 'https://arayainternusa.github.io/arayaweb/'
    pages = {path.resolve(): Page(path) for path in PUBLIC.rglob("*.html")}
    errors = []
    if {p.relative_to(PUBLIC.resolve()).as_posix() for p in pages} != ALL_ROUTES:
        errors.append('Expected all content pages and three compatibility routes')
    for path, page in pages.items():
        route = path.relative_to(PUBLIC.resolve()).as_posix()
        expected_robots = ('index, follow' if route in CONTENT_ROUTES else 'noindex, follow') if production else 'noindex, nofollow'
        if page.h1 != 1 or not page.description or page.robots != expected_robots:
            page.errors.append(f'Expected one H1, description and robots={expected_robots}')
        canonical_route = route.removesuffix('index.html') if route in CONTENT_ROUTES else ''
        if page.canonical != base + canonical_route or page.og_url != base + route.removesuffix('index.html'):
            page.errors.append('Wrong canonical or Open Graph URL for build target')
        try:
            json.loads(page.schema)
        except (ValueError, TypeError):
            page.errors.append('Invalid structured data')
        if production and any(url in page.schema for url in ('hakiimm8.github.io', 'at-control.github.io', 'arayainternusa.github.io', 'https://arayainternusa.co.id/araya/')):
            page.errors.append('Production structured data references the old or preview URL')
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target = target / "index.html"
            if not target.is_relative_to(PUBLIC.resolve()) or not target.is_file():
                page.errors.append(f"Broken or escaping local link: {link}")
            elif url.fragment and target in pages and url.fragment not in pages[target].ids:
                page.errors.append(f"Missing fragment: {link}")
        errors.extend(f"{path.relative_to(PUBLIC)}: {message}" for message in page.errors)
    for path in PUBLIC.rglob("*"):
        if path.is_symlink():
            errors.append(f'Forbidden symlink: {path.relative_to(PUBLIC)}')
        if path.is_file() and (path.name == "wp-config.php" or path.suffix in {".php", ".sql", ".log", ".zip"}):
            errors.append(f"Forbidden publication file: {path.name}")
        if production and path.is_file():
            name = path.relative_to(PUBLIC).as_posix()
            if name not in ALL_ROUTES | {'robots.txt', 'sitemap.xml', 'assets/fonts/OFL.txt'} and not (name.startswith('assets/') and path.suffix.lower() in ASSET_SUFFIXES and not any(part.startswith('.') for part in path.relative_to(PUBLIC).parts)):
                errors.append(f'Unexpected production file: {name}')
    for file in (PUBLIC / "assets/fonts/space-grotesk.woff2",):
        if not file.is_file() or file.read_bytes()[:4] != b"wOF2":
            errors.append(f"Missing or invalid font: {file.name}")
    try:
        sitemap = ET.parse(PUBLIC / 'sitemap.xml')
        locations = {node.text for node in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
        if locations != {base + path.removesuffix('index.html') for path in CONTENT_ROUTES}:
            errors.append('Sitemap does not match the target content URLs')
        expected_robots = f'User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n' if production else 'User-agent: *\nAllow: /\n'
        if (PUBLIC / 'robots.txt').read_text(encoding='utf-8') != expected_robots:
            errors.append('robots.txt does not match build target')
    except (OSError, ET.ParseError) as exc:
        errors.append(f'Missing or invalid discovery files: {exc}')
    for path in (ROOT / '.github/workflows').glob('*.y*ml'):
        if 'pull_request' in path.read_text(encoding='utf-8'):
            errors.append(f'Workflow violates the no-PR-Actions policy: {path.name}')
    workflow = (ROOT / '.github/workflows/pages.yml').read_text(encoding='utf-8')
    if 'branches: [main]' not in workflow:
        errors.append('Preview workflow must retain main push publication')
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS {args.target}: {len(pages)} pages; local assets/fragments, metadata, image alt text, font, publication files and no-PR workflows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
