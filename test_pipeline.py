import pathlib
import sys
import unittest
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from kaushal_api import render  # noqa: E402
from kaushal_api.collect import collect, relative  # noqa: E402
from tests.fixtures import FakeGitHub  # noqa: E402

NOW = datetime(2026, 8, 24, 10, 0, tzinfo=timezone.utc)

CONTRIB = {
    "totalCommitContributions": 812,
    "contributionCalendar": {
        "totalContributions": 947,
        "weeks": [
            {
                "contributionDays": [
                    {"date": "2026-08-22", "contributionCount": 4},
                    {"date": "2026-08-23", "contributionCount": 6},
                    {"date": "2026-08-24", "contributionCount": 0},
                ]
            }
        ],
    },
}


class TestRelative(unittest.TestCase):
    def test_units(self):
        cases = {
            "2026-08-24T09:59:30Z": "just now",
            "2026-08-24T09:42:00Z": "18 min ago",
            "2026-08-24T07:00:00Z": "3 hours ago",
            "2026-08-21T10:00:00Z": "3 days ago",
            "2026-06-01T10:00:00Z": "2 months ago",
        }
        for ts, expected in cases.items():
            self.assertEqual(relative(ts, NOW), expected, ts)


class TestCollect(unittest.TestCase):
    def setUp(self):
        self.snap = collect(FakeGitHub(contributions=CONTRIB), now=NOW)

    def test_forks_excluded_from_repo_count(self):
        self.assertEqual(self.snap["totals"]["own_repos"], 4)

    def test_stars_summed_across_all_repos(self):
        self.assertEqual(self.snap["totals"]["stars"], 47)

    def test_streak_ignores_today_but_counts_back(self):
        # today is 0 so far, so the streak should still be the two prior days
        self.assertEqual(self.snap["totals"]["streak_days"], 2)

    def test_unmapped_event_types_dropped(self):
        self.assertEqual(len(self.snap["feed"]), 2)
        self.assertEqual(self.snap["feed"][0]["label"], "PUSH")

    def test_commit_message_truncated_to_first_line(self):
        self.assertEqual(self.snap["feed"][0]["detail"], "add contradiction scoring")

    def test_language_percentages_sum_to_about_100(self):
        self.assertAlmostEqual(sum(l["pct"] for l in self.snap["languages"]), 100.0, places=0)

    def test_ci_conclusion_carried_through(self):
        by_key = {p["key"]: p for p in self.snap["projects"]}
        self.assertEqual(by_key["SciRAG-UQ"]["ci"], "failure")
        self.assertIsNone(by_key["AntBot"]["ci"])

    def test_degrades_without_contributions_token(self):
        snap = collect(FakeGitHub(contributions=None), now=NOW)
        self.assertIsNone(snap["totals"]["streak_days"])
        self.assertNotIn("streak", render.system_status(snap))


class TestRender(unittest.TestCase):
    def setUp(self):
        self.snap = collect(FakeGitHub(contributions=CONTRIB), now=NOW)

    def test_panels_are_rectangular(self):
        for name, fn in render.RENDERERS.items():
            lines = fn(self.snap).splitlines()
            widths = {len(l) for l in lines}
            self.assertEqual(len(widths), 1, f"{name} has ragged edges: {widths}")

    def test_bar_saturates_and_floors(self):
        self.assertEqual(render.bar(50, 50, 10), "█" * 10)
        self.assertEqual(render.bar(0, 50, 10), "░" * 10)

    def test_failing_ci_is_called_out(self):
        self.assertIn("⚠ failing: SciRAG-UQ", render.ci_status(self.snap))

    def test_template_regions_replaced(self):
        template = (pathlib.Path(__file__).parent / "README.template.md").read_text()
        out = render.render_readme(template, self.snap)
        self.assertNotIn("{{GENERATED_AT}}", out)
        for name in render.RENDERERS:
            marker = f"<!--START:{name}-->"
            if marker in template:
                self.assertIn("│", out.split(marker, 1)[1][:400], name)

    def test_render_is_idempotent(self):
        template = (pathlib.Path(__file__).parent / "README.template.md").read_text()
        once = render.render_readme(template, self.snap)
        twice = render.render_readme(once, self.snap)
        self.assertEqual(once, twice)

    def test_empty_account_does_not_crash(self):
        snap = collect(FakeGitHub(empty=True), now=NOW)
        for fn in render.RENDERERS.values():
            self.assertTrue(fn(snap))


if __name__ == "__main__":
    unittest.main()
