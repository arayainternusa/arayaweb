"""Deployment gates must reject corrupt live bytes and exposed retired URLs."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit
from check_live import BASE, check
from check import CONTENT_ROUTES, SERVICE_PAGE_ROUTES

class LiveCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='araya-live-check-')
        self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'release.json'
        self.files={n:b'<meta name="robots" content="index, follow">' for n in CONTENT_ROUTES}
        self.files['assets/site.js']=b'// checked JS'
        self.path.write_text(json.dumps({'source_commit':'a'*40,'files':{n:hashlib.sha256(v).hexdigest() for n,v in self.files.items()}}))
    def response(self,url):
        part=urlsplit(url);path=part.path
        if part.scheme=='http' or part.hostname.startswith('www.'):
            return 301,{'Location':BASE+'/'},b''
        redirects={'/araya/':'/','/araya/about-us/':'/#about','/araya/about/':'/#about',
            '/araya/services/':'/#services','/araya/services/marine/':'/#marine-services',
            '/araya/services/industrial/':'/#industrial-services','/araya/services/automation/':'/#automation-services',
            '/araya/team/':'/#leadership','/araya/contact/':'/#contact','/araya/contact-2/':'/#contact',
            '/index.php':'/','/noris':'/noris/','/comap':'/comap/','/privacy':'/privacy/',
            '/noris/id':'/noris/id/','/comap/id':'/comap/id/',
            **{f'/{route.rstrip("/")}': f'/{route}' for route in SERVICE_PAGE_ROUTES}}
        if path in redirects:return 301,{'Location':BASE+redirects[path]},b''
        if path.startswith('/araya/'):return 410,{},b''
        name=path.lstrip('/')
        if path.endswith('/'):name+='index.html'
        return (200,{},self.files[name]) if name in self.files else (404,{},b'not found')
    def test_valid_site_and_migration_pass(self):
        with patch('check_live.fetch',side_effect=self.response):check(self.path)
    def test_changed_live_bytes_fail(self):
        self.files['assets/site.js']=b'corrupted'
        with patch('check_live.fetch',side_effect=self.response),self.assertRaisesRegex(ValueError,'Live file mismatch'):check(self.path)
    def test_exposed_old_wordpress_route_fails(self):
        def exposed(url):
            return (200,{},b'old WordPress') if urlsplit(url).path=='/araya/wp-admin/' else self.response(url)
        with patch('check_live.fetch',side_effect=exposed),self.assertRaisesRegex(ValueError,'exposed/retired'):check(self.path)
    def test_server_noindex_header_fails(self):
        def hidden(url):
            status,headers,body=self.response(url)
            return status,{**headers,'X-Robots-Tag':'noindex'},body
        with patch('check_live.fetch',side_effect=hidden),self.assertRaisesRegex(ValueError,'noindex'):check(self.path)
    def test_provider_forbidden_response_protects_sensitive_paths(self):
        def forbidden(url):
            return (403,{},b'Forbidden') if urlsplit(url).path in {'/.git/config','/wp-config.php'} else self.response(url)
        with patch('check_live.fetch',side_effect=forbidden):check(self.path)

if __name__=='__main__':unittest.main()
