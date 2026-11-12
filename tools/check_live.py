"""Verify the exact deployed static release over public HTTPS, without sending enquiries."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener
from check import CONTENT_ROUTES, SERVICE_PAGE_ROUTES

BASE = 'https://arayainternusa.co.id'
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def fetch(url):
    request = Request(url, headers={'User-Agent': 'Araya-release-verification/1.0', 'Cache-Control': 'no-cache'})
    try:
        with build_opener(NoRedirect).open(request, timeout=25) as response:
            return response.status, response.headers, response.read()
    except HTTPError as response:
        return response.code, response.headers, response.read()

def verify_file(item, sha):
    name, expected = item
    code, headers, data = fetch(f'{BASE}/{name}?araya_release={sha}')
    if code != 200 or hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f'Live file mismatch: {name} (HTTP {code})')
    if 'noindex' in headers.get('X-Robots-Tag', '').lower():
        raise ValueError(f'Unexpected noindex response header: {name}')

def check(manifest_path):
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    sha = manifest['source_commit']
    with ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(lambda item: verify_file(item, sha), manifest['files'].items()))
    for name in sorted(CONTENT_ROUTES):
        route = '/' + name.removesuffix('index.html')
        code, headers, body = fetch(f'{BASE}{route}?araya_release={sha}')
        if code != 200 or hashlib.sha256(body).hexdigest() != manifest['files'][name] or b'content="index, follow"' not in body:
            raise ValueError(f'Live content/indexing mismatch: {route}')
    redirects = {'/araya/':'/', '/araya/about-us/':'/#about', '/araya/about/':'/#about',
        '/araya/services/':'/#services','/araya/services/marine/':'/#marine-services',
        '/araya/services/industrial/':'/#industrial-services', '/araya/services/automation/':'/#automation-services',
        '/araya/team/':'/#leadership','/araya/contact/':'/#contact','/araya/contact-2/':'/#contact',
        '/index.php':'/','/noris':'/noris/','/comap':'/comap/','/privacy':'/privacy/',
        '/noris/id':'/noris/id/','/comap/id':'/comap/id/',
        **{f'/{route.rstrip("/")}': f'/{route}' for route in SERVICE_PAGE_ROUTES}}
    for source, target in redirects.items():
        code, headers, _ = fetch(BASE+source)
        location = headers.get('Location', '')
        if code != 301 or location not in {target, BASE+target}:
            raise ValueError(f'Legacy/canonical redirect mismatch: {source} ({code}, {location})')
    for route, statuses in [('/araya/wp-admin/', {410}),('/araya/wp-content/uploads/company-profile.pdf',{410}),
            ('/araya/project1/',{410}),('/araya/project2/',{410}),('/araya.zip',{404}),('/araya-release-missing-test',{404}),
            ('/.araya-current/index.html',{403,404}),('/%2earaya-current/index.html',{403,404}),
            (f'/.araya-releases/{sha}-1-1/index.html',{403,404}),('/.git/config',{403,404}),('/wp-config.php',{403,404})]:
        code, _, _ = fetch(BASE+route)
        if code not in statuses:
            raise ValueError(f'Unexpected exposed/retired path: {route} (HTTP {code})')
    for source in ('http://arayainternusa.co.id/', 'https://www.arayainternusa.co.id/'):
        code, headers, _ = fetch(source)
        if code != 301 or headers.get('Location') != BASE+'/':
            raise ValueError(f'HTTPS/hostname redirect mismatch: {source}')
    print(f'PASS live HTTPS: {len(manifest["files"])} exact file hashes, {len(CONTENT_ROUTES)} indexable pages, redirects, retired downloads and protected paths.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('manifest');parser.add_argument('--attempts',type=int,default=1);args=parser.parse_args()
    if not 1 <= args.attempts <= 5: parser.error('attempts must be between 1 and 5')
    for attempt in range(args.attempts):
        try:
            check(args.manifest)
            break
        except Exception as exc:
            if attempt+1 == args.attempts: raise
            print(f'Live check not settled ({exc}); retrying after LiteSpeed configuration refresh.',flush=True)
            time.sleep(5)
