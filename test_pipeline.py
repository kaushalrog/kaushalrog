"""Behavioral checks for collection, GitHub markup, and failure preservation."""
import pathlib
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from unittest.mock import patch
from kaushal_api.collect import collect, relative, _event_detail
from kaushal_api.render import render_readme, activity, dashboard, language_card
from kaushal_api.github import GitHub, GitHubError
from kaushal_api.build import main
from tests.fixtures import FakeGitHub

NOW = datetime(2026, 8, 24, 10, 0, tzinfo=timezone.utc)
ROOT = pathlib.Path(__file__).parent


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.snap = collect(FakeGitHub(), now=NOW)
        self.template = (ROOT / 'README.template.md').read_text()

    def test_actual_repo_names_are_resolved(self):
        projects = {p['key']: p for p in self.snap['projects']}
        self.assertTrue(projects['WDS-IDS']['exists'])
        self.assertTrue(projects['SciRAG-UQ']['exists'])
        self.assertEqual(projects['SciRAG-UQ']['commits_30d'], 31)

    def test_forks_excluded(self):
        self.assertEqual(self.snap['totals']['own_repos'], 4)
        self.assertEqual(self.snap['totals']['stars'], 47)

    def test_repo_names_match_case_insensitively(self):
        gh = FakeGitHub()
        repos = gh.repos('kaushalrog')
        repos[1]['name'] = 'SCIRAG-UQ'
        gh.repos = lambda login: repos
        self.assertTrue(collect(gh, now=NOW)['projects'][1]['exists'])

    def test_profile_bot_activity_excluded(self):
        gh = FakeGitHub()
        events = gh.events('kaushalrog')
        events.insert(0, dict(events[0], repo={'name': 'kaushalrog/kaushalrog'}))
        gh.events = lambda login: events
        snap = collect(gh, now=NOW)
        self.assertEqual(len(snap['feed']), 2)
        self.assertIn('KhronosGroup/Vulkan-Loader', activity(snap))

    def test_missing_push_counts_not_invented(self):
        self.assertEqual(_event_detail({'type': 'PushEvent', 'payload': {}}), 'Pushed code')

    def test_missing_markers_fail_loudly(self):
        with self.assertRaises(ValueError):
            render_readme('broken template', self.snap)

    def test_render_idempotent_and_no_placeholders(self):
        once = render_readme(self.template, self.snap)
        self.assertEqual(once, render_readme(once, self.snap))
        self.assertNotIn('{{GENERATED_AT}}', once)
        self.assertIn('add contradiction scoring', once)

    def test_untrusted_activity_is_escaped(self):
        self.snap['feed'][0]['detail'] = '<script> | [link] `code`\nnext'
        block = activity(self.snap)
        self.assertNotIn('<script>', block)
        self.assertIn('&#124;', block)
        self.assertNotIn('[link]', block)

    def test_svg_cards_are_valid_in_both_themes(self):
        for fn in (dashboard, language_card):
            for light in (True, False):
                self.assertEqual(ET.fromstring(fn(self.snap, light)).tag, '{http://www.w3.org/2000/svg}svg')

    def test_empty_account_renders(self):
        snap = collect(FakeGitHub(empty=True), now=NOW)
        self.assertIn('Recent public activity will appear', render_readme(self.template, snap))
        ET.fromstring(language_card(snap))

    def test_commit_count_paginates(self):
        gh = GitHub()
        with patch.object(gh, 'get', side_effect=[[{}] * 100, [{}] * 23]) as get:
            self.assertEqual(gh.commit_count('user', 'repo', '2026-01-01'), 123)
            self.assertEqual(get.call_args.kwargs['page'], 2)

    def test_failed_collection_preserves_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp) / 'README.md'
            out.write_text('last good profile')
            with patch('kaushal_api.build.collect_safe', return_value=(None, 'API unavailable')):
                self.assertEqual(main(['--out', str(out)]), 1)
            self.assertEqual(out.read_text(), 'last good profile')
            self.assertFalse((out.parent / 'assets').exists())

    def test_language_failure_is_not_silently_zero(self):
        with patch.object(GitHub, 'get', side_effect=GitHubError('rate limit')):
            with self.assertRaises(GitHubError):
                GitHub().languages('user', 'repo')

    def test_feed_is_chronological(self):
        gh = FakeGitHub()
        events = gh.events('kaushalrog')
        gh.events = lambda login: list(reversed(events))
        dates = [e['at'] for e in collect(gh, now=NOW)['feed']]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_relative_date(self):
        self.assertEqual(relative('2026-08-24T09:42:00Z', NOW), '18 min ago')


if __name__ == '__main__':
    unittest.main()
