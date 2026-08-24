"""Minimal GitHub API client. Standard library only — no pip install in CI.

Auth comes from GITHUB_TOKEN (the token Actions injects automatically). Without
a token the REST calls still work at 60 requests/hour, which is enough to run
this locally a few times but not enough for the scheduled workflow.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any

API = "https://api.github.com"
GRAPHQL = "https://api.github.com/graphql"
UA = "kaushal-api/1.0 (+https://github.com/kaushalrog)"


class GitHubError(RuntimeError):
    pass


class GitHub:
    def __init__(self, token: str | None = None, retries: int = 3):
        self.token = token or os.environ.get("GITHUB_TOKEN") or ""
        self.retries = retries

    # ---- plumbing ---------------------------------------------------------

    def _headers(self) -> dict[str, str]:
        h = {"Accept": "application/vnd.github+json", "User-Agent": UA}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _request(self, url: str, data: bytes | None = None) -> Any:
        last: Exception | None = None
        for attempt in range(self.retries):
            req = urllib.request.Request(url, data=data, headers=self._headers())
            if data is not None:
                req.add_header("Content-Type", "application/json")
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                # 403 here is nearly always secondary rate limiting; back off.
                if exc.code in (403, 429) and attempt < self.retries - 1:
                    time.sleep(2 ** attempt * 3)
                    last = exc
                    continue
                raise GitHubError(f"{exc.code} on {url}") from exc
            except urllib.error.URLError as exc:
                last = exc
                time.sleep(2 ** attempt)
        raise GitHubError(f"failed after {self.retries} attempts: {url}") from last

    def get(self, path: str, **params: Any) -> Any:
        qs = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
        url = f"{API}{path}" + (f"?{qs}" if qs else "")
        return self._request(url)

    def graphql(self, query: str, **variables: Any) -> Any:
        body = json.dumps({"query": query, "variables": variables}).encode()
        payload = self._request(GRAPHQL, data=body)
        if "errors" in payload:
            raise GitHubError(str(payload["errors"][0].get("message")))
        return payload["data"]

    # ---- endpoints --------------------------------------------------------

    def user(self, login: str) -> dict:
        return self.get(f"/users/{login}")

    def repos(self, login: str) -> list[dict]:
        out: list[dict] = []
        for page in range(1, 6):  # 500 repos is plenty of headroom
            batch = self.get(
                f"/users/{login}/repos", per_page=100, page=page, sort="pushed"
            )
            out.extend(batch)
            if len(batch) < 100:
                break
        return out

    def events(self, login: str, pages: int = 2) -> list[dict]:
        out: list[dict] = []
        for page in range(1, pages + 1):
            out.extend(self.get(f"/users/{login}/events/public", per_page=100, page=page))
        return out

    def commit_count(self, login: str, repo: str, since_iso: str) -> int:
        """Commits by `login` on the default branch since a timestamp."""
        try:
            commits = self.get(
                f"/repos/{login}/{repo}/commits",
                author=login,
                since=since_iso,
                per_page=100,
            )
        except GitHubError:
            return 0
        return len(commits) if isinstance(commits, list) else 0

    def latest_run(self, login: str, repo: str) -> dict | None:
        """Most recent GitHub Actions run, or None if the repo has no CI."""
        try:
            data = self.get(f"/repos/{login}/{repo}/actions/runs", per_page=1)
        except GitHubError:
            return None
        runs = data.get("workflow_runs") or []
        return runs[0] if runs else None

    def languages(self, login: str, repo: str) -> dict[str, int]:
        try:
            return self.get(f"/repos/{login}/{repo}/languages") or {}
        except GitHubError:
            return {}

    def contributions(self, login: str) -> dict | None:
        """Contribution totals and current streak.

        Requires a classic PAT with `read:user`; the default Actions
        GITHUB_TOKEN cannot read another account's contributionsCollection.
        Returns None when unavailable so the caller can degrade gracefully.
        """
        query = """
        query($login: String!) {
          user(login: $login) {
            contributionsCollection {
              totalCommitContributions
              contributionCalendar {
                totalContributions
                weeks { contributionDays { date contributionCount } }
              }
            }
          }
        }
        """
        try:
            data = self.graphql(query, login=login)
        except GitHubError:
            return None
        cc = (data.get("user") or {}).get("contributionsCollection")
        return cc or None
