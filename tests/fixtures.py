"""A fake GitHub that returns plausible data, so tests never touch the network."""

from __future__ import annotations


class FakeGitHub:
    def __init__(self, *, contributions: dict | None = None, empty: bool = False):
        self._contributions = contributions
        self._empty = empty

    def user(self, login):
        return {"followers": 126, "public_repos": 29}

    def repos(self, login):
        if self._empty:
            return []
        return [
            {"name": "ids---System", "stargazers_count": 21, "pushed_at": "2026-08-24T09:10:00Z", "fork": False},
            {"name": "scirag-uq", "stargazers_count": 9, "pushed_at": "2026-08-23T18:00:00Z", "fork": False},
            {"name": "TrafficFlowAI", "stargazers_count": 4, "pushed_at": "2026-07-02T11:00:00Z", "fork": False},
            {"name": "AntBot", "stargazers_count": 13, "pushed_at": "2026-02-14T08:00:00Z", "fork": False},
            {"name": "some-fork", "stargazers_count": 100, "pushed_at": "2026-01-01T00:00:00Z", "fork": True},
        ]

    def events(self, login, pages=2):
        if self._empty:
            return []
        return [
            {
                "type": "PushEvent",
                "repo": {"name": "kaushalrog/scirag-uq"},
                "created_at": "2026-08-24T09:40:00Z",
                "payload": {"size": 2, "commits": [{"message": "add contradiction scoring\n\nlong body"}]},
            },
            {
                "type": "PullRequestEvent",
                "repo": {"name": "KhronosGroup/Vulkan-Loader"},
                "created_at": "2026-08-23T16:32:00Z",
                "payload": {"action": "opened", "pull_request": {"number": 1842}},
            },
            {"type": "MemberEvent", "repo": {"name": "x/y"}, "created_at": "2026-08-23T10:00:00Z", "payload": {}},
        ]

    def commit_count(self, login, repo, since):
        return {"ids---System": 17, "scirag-uq": 31, "TrafficFlowAI": 2, "AntBot": 0}.get(repo, 0)

    def latest_run(self, login, repo):
        if repo == "scirag-uq":
            return {"conclusion": "failure", "html_url": "https://example.invalid/run/2"}
        if repo == "ids---System":
            return {"conclusion": "success", "html_url": "https://example.invalid/run/1"}
        return None

    def languages(self, login, repo):
        return {"Python": 90000, "C++": 20000} if repo != "AntBot" else {"C++": 40000}

    def contributions(self, login):
        return self._contributions
