"""Turn raw GitHub responses into one flat snapshot dict.

The snapshot is the single source of truth: the README renderer reads it, and
so does the optional FastAPI app. Nothing downstream touches the API directly.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .config import EVENT_LABELS, PROJECTS, USER
from .github import GitHub, GitHubError

WINDOW_DAYS = 30


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse(ts: str) -> datetime:
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def relative(ts: str, now: datetime | None = None) -> str:
    """'18 min ago' / '3 days ago'. Deliberately coarse — it's a README."""
    now = now or datetime.now(timezone.utc)
    delta = now - _parse(ts)
    mins = int(delta.total_seconds() // 60)
    if mins < 1:
        return "just now"
    if mins < 60:
        return f"{mins} min ago"
    hours = mins // 60
    if hours < 24:
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    days = hours // 24
    if days < 30:
        return f"{days} day{'s' if days > 1 else ''} ago"
    months = days // 30
    return f"{months} month{'s' if months > 1 else ''} ago"


def _streak(calendar: dict, now: datetime) -> int:
    """Consecutive days ending today (or yesterday) with at least one contribution."""
    days = [
        d
        for week in calendar.get("weeks", [])
        for d in week.get("contributionDays", [])
    ]
    days.sort(key=lambda d: d["date"], reverse=True)
    streak = 0
    for i, day in enumerate(days):
        if day["contributionCount"] > 0:
            streak += 1
        elif i == 0:
            continue  # today may simply not have happened yet
        else:
            break
    return streak


def _event_detail(event: dict) -> str:
    payload = event.get("payload") or {}
    if event["type"] == "PushEvent":
        commits = payload.get("commits") or []
        if commits:
            msg = commits[-1].get("message", "").splitlines()[0]
            return msg[:52]
        return "Pushed code"
    if event["type"] == "PullRequestEvent":
        pr = payload.get("pull_request") or {}
        return f"{payload.get('action', '')} #{pr.get('number', '?')}"
    if event["type"] == "ReleaseEvent":
        return (payload.get("release") or {}).get("tag_name", "")
    if event["type"] == "CreateEvent":
        return f"{payload.get('ref_type', '')} {payload.get('ref') or ''}".strip()
    return ""


def collect(gh: GitHub | None = None, user: str = USER, now: datetime | None = None) -> dict:
    gh = gh or GitHub()
    now = now or datetime.now(timezone.utc)
    since = _iso(now - timedelta(days=WINDOW_DAYS))

    profile = gh.user(user)
    repos = gh.repos(user)
    by_name = {r["name"].lower(): r for r in repos}
    events = sorted(gh.events(user), key=lambda e: e.get("created_at", ""), reverse=True)

    # --- projects ---------------------------------------------------------
    projects = []
    for spec in PROJECTS:
        repo = by_name.get(spec.repo.lower())
        commits = gh.commit_count(user, spec.repo, since) if repo else 0
        run = None  # CI health is not part of the public profile.
        projects.append(
            {
                "key": spec.key,
                "repo": spec.repo,
                "status": spec.status,
                "blurb": spec.blurb,
                "evidence": spec.evidence,
                "exists": repo is not None,
                "stars": (repo or {}).get("stargazers_count", 0),
                "pushed_at": (repo or {}).get("pushed_at"),
                "last_push": relative(repo["pushed_at"], now) if repo else "—",
                "commits_30d": commits,
                "ci": (run or {}).get("conclusion") if run else None,
                "ci_run_url": (run or {}).get("html_url") if run else None,
            }
        )

    # --- build feed -------------------------------------------------------
    feed = []
    for event in events:
        label = EVENT_LABELS.get(event.get("type", ""))
        event_repo = (event.get("repo") or {}).get("name", "")
        if not label or event_repo.lower() == f"{user}/{user}".lower():
            continue
        feed.append(
            {
                "label": label,
                "repo": event_repo,
                "url": f"https://github.com/{event_repo}",
                "detail": _event_detail(event),
                "at": event["created_at"],
                "ago": relative(event["created_at"], now),
            }
        )
        if len(feed) >= 8:
            break

    # --- language mix (own repos only, weighted by bytes) ------------------
    mix: dict[str, int] = {}
    for repo in repos:
        if repo.get("fork") or repo.get("archived"):
            continue
        for lang, size in gh.languages(user, repo["name"]).items():
            mix[lang] = mix.get(lang, 0) + size
    total_bytes = sum(mix.values()) or 1
    languages = [
        {"name": name, "pct": round(size * 100 / total_bytes, 1), "bytes": size}
        for name, size in sorted(mix.items(), key=lambda kv: -kv[1])[:6]
    ]

    streak = None
    total_contributions = None

    latest = feed[0] if feed else None
    return {
        "generated_at": _iso(now),
        "user": user,
        "profile": {
            "followers": profile.get("followers", 0),
            "public_repos": profile.get("public_repos", 0),
        },
        "totals": {
            "stars": sum(r.get("stargazers_count", 0) for r in repos if not r.get("fork")),
            "own_repos": sum(1 for r in repos if not r.get("fork")),
            "commits_30d": sum(p["commits_30d"] for p in projects),
            "contributions_year": total_contributions,
            "streak_days": streak,
        },
        "latest": latest,
        "projects": projects,
        "feed": feed,
        "languages": languages,
    }


def collect_safe(**kwargs) -> tuple[dict | None, str | None]:
    """Never let a bad API day rewrite the README with garbage."""
    try:
        return collect(**kwargs), None
    except GitHubError as exc:
        return None, str(exc)
