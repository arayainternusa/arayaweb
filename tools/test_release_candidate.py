"""Regression tests for promoting only trusted, complete CI packages."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
import warnings
from release_candidate import validate_run, validate_package, destination

SHA = 'a' * 40
REPO = 'arayainternusa/arayaweb'


class CandidateTests(unittest.TestCase):
    def run_record(self):
        return dict(path='.github/workflows/pages.yml', head_branch='main', head_sha=SHA,
                    status='completed', conclusion='success', event='push',
                    head_repository={'full_name': REPO})

    def test_only_successful_main_builds_from_this_repository(self):
        self.assertEqual(validate_run(self.run_record(), REPO), SHA)
        for field, value in [('path', '.github/workflows/other.yml'), ('head_branch', 'feature'),
                             ('status', 'in_progress'), ('conclusion', 'failure'),
                             ('event', 'pull_request'), ('head_sha', 'bad')]:
            record = self.run_record()
            record[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_run(record, REPO)
        record = self.run_record()
        record['head_repository']['full_name'] = 'someone/fork'
        with self.assertRaises(ValueError):
            validate_run(record, REPO)

    def package(self, root, *, extras=None, overrides=None):
        files = {p: b'fixture' for p in (
            'index.html', 'noris/index.html', 'comap/index.html', 'noris/id/index.html', 'comap/id/index.html', 'privacy/index.html', 'marine/index.html',
            'industrial/index.html', 'automation/index.html', 'robots.txt', 'sitemap.xml',
            'assets/site.css', 'assets/site.js', 'assets/measurement.js', 'assets/measurement.css', 'assets/company-date.js',
            'assets/service-redirect.js', 'assets/fonts/space-grotesk.woff2', 'assets/fonts/OFL.txt')}
        files.update(extras or {})
        archive = root / 'araya-production.zip'
        with zipfile.ZipFile(archive, 'w') as zipped:
            for name, data in files.items():
                zipped.writestr(name, data)
        manifest = dict(target='https://arayainternusa.co.id/', source_commit=SHA,
                        source_tree_dirty=False, archive=archive.name,
                        archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                        files={p: hashlib.sha256(d).hexdigest() for p, d in files.items()})
        manifest.update(overrides or {})
        (root / 'release.json').write_text(json.dumps(manifest), encoding='utf-8')
        return manifest

    def test_package_checks_hashes_provenance_and_complete_file_set(self):
        with tempfile.TemporaryDirectory(prefix='araya-candidate-') as folder:
            root = Path(folder)
            manifest = self.package(root)
            archive_hash, manifest_hash = validate_package(root, SHA)
            self.assertEqual(archive_hash, manifest['archive_sha256'])
            self.assertEqual(manifest_hash, hashlib.sha256((root / 'release.json').read_bytes()).hexdigest())
            for overrides in ({'source_tree_dirty': True}, {'source_commit': 'b' * 40},
                              {'target': 'https://example.invalid/'}, {'archive_sha256': '0' * 64}):
                self.package(root, overrides=overrides)
                with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                    validate_package(root, SHA)
            manifest = self.package(root)
            manifest['files'].pop('comap/index.html')
            (root / 'release.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                validate_package(root, SHA)
            self.package(root)
            with (root / 'araya-production.zip').open('ab') as output:
                output.write(b'tampered')
            with self.assertRaises(ValueError):
                validate_package(root, SHA)

    def test_package_rejects_escape_sensitive_unlisted_and_duplicate_paths(self):
        with tempfile.TemporaryDirectory(prefix='araya-candidate-') as folder:
            root = Path(folder)
            for name in ('../outside.html', '/index.html', 'assets/../secret.css',
                         'assets\\bad.css', '.git/config', 'wp-config.php', 'assets/backup.sql'):
                self.package(root, extras={name: b'unsafe fixture'})
                with self.subTest(name=name), self.assertRaises(ValueError):
                    validate_package(root, SHA)
            manifest = self.package(root)
            with zipfile.ZipFile(root / 'araya-production.zip', 'a') as archive:
                archive.writestr('assets/extra.css', b'not in manifest')
            manifest['archive_sha256'] = hashlib.sha256((root / 'araya-production.zip').read_bytes()).hexdigest()
            (root / 'release.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                validate_package(root, SHA)
            manifest = self.package(root)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', UserWarning)
                with zipfile.ZipFile(root / 'araya-production.zip', 'a') as archive:
                    archive.writestr('index.html', b'duplicate')
            manifest['archive_sha256'] = hashlib.sha256((root / 'araya-production.zip').read_bytes()).hexdigest()
            (root / 'release.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                validate_package(root, SHA)

    def test_rejects_inner_tampering_even_when_archive_hash_matches(self):
        with tempfile.TemporaryDirectory(prefix='araya-candidate-') as folder:
            root = Path(folder)
            manifest = self.package(root)
            path = root / 'araya-production.zip'
            with zipfile.ZipFile(path) as archive:
                files = {name: archive.read(name) for name in archive.namelist()}
            files['index.html'] = b'tampered inner file'
            with zipfile.ZipFile(path, 'w') as archive:
                for name, data in files.items():
                    archive.writestr(name, data)
            manifest['archive_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
            (root / 'release.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                validate_package(root, SHA)

    def test_rejects_symlinks_even_when_all_hashes_match(self):
        with tempfile.TemporaryDirectory(prefix='araya-candidate-') as folder:
            root = Path(folder)
            manifest = self.package(root)
            path = root / 'araya-production.zip'
            with zipfile.ZipFile(path, 'a') as archive:
                entry = zipfile.ZipInfo('assets/link.css')
                entry.create_system = 3
                entry.external_attr = 0o120777 << 16
                archive.writestr(entry, b'/outside')
            manifest['files']['assets/link.css'] = hashlib.sha256(b'/outside').hexdigest()
            manifest['archive_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
            (root / 'release.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                validate_package(root, SHA)

    def test_destination_is_new_private_account_directory(self):
        self.assertEqual(destination('account1', SHA, '123', '2'),
                         f'/home/account1/araya-deploy/incoming/{SHA}-123-2')
        for user, sha, run, attempt in [('user;id', SHA, '1', '1'), ('../root', SHA, '1', '1'),
                                       ('user', '../bad', '1', '1'), ('user', SHA, '1;id', '1'),
                                       ('user', SHA, '1', '-1')]:
            with self.subTest(user=user, sha=sha, run=run), self.assertRaises(ValueError):
                destination(user, sha, run, attempt)


if __name__ == '__main__':
    unittest.main()
