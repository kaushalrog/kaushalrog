"""Render the snapshot into the ASCII blocks the README embeds.

Everything here is pure: snapshot dict in, string out. That makes the whole
render path testable without touching the network.
"""

from __future__ import annotations

from .config import BLOCKS, PANEL_WIDTH

BAR_FULL = "█"
BAR_EMPTY = "░"


def bar(value: float, peak: float, width: int = 12) -> str:
    if peak <= 0:
        return BAR_EMPTY * width
    filled = max(0, min(width, round(value / peak * width)))
    return BAR_FULL * filled + BAR_EMPTY * (width - filled)


def panel(title: str, lines: list[str], width: int = PANEL_WIDTH) -> str:
    """A box-drawn panel. Lines longer than the width are truncated, not wrapped."""
    inner = width - 2
    top = "┌─ " + title + " " + "─" * max(0, inner - len(title) - 3) + "┐"
    body = [f"│ {line[: inner - 2]:<{inner - 2}} │" for line in lines]
    bottom = "└" + "─" * inner + "┘"
    return "\n".join([top, *body, bottom])


def system_status(snap: dict) -> str:
    t = snap["totals"]
    latest = snap.get("latest")
    active = sum(1 for p in snap["projects"] if p["status"] in ("RESEARCH", "BUILDING"))
    lines = [
        "● ONLINE",
        "",
        f"{'repositories':<16}{t['own_repos']}",
        f"{'stars':<16}{t['stars']}",
        f"{'followers':<16}{snap['profile']['followers']}",
        f"{'active builds':<16}{active}",
    ]
    if t.get("contributions_year") is not None:
        lines.append(f"{'contributions':<16}{t['contributions_year']} (12mo)")
    if t.get("streak_days"):
        lines.append(f"{'streak':<16}{t['streak_days']} days")
    if latest:
        lines += ["", "last activity", f"└── {latest['repo']} · {latest['ago']}"]
    return panel("SYSTEM STATUS", lines)


def project_table(snap: dict) -> str:
    peak = max((p["commits_30d"] for p in snap["projects"]), default=0)
    header = f"{'PID':<6}{'PROJECT':<14}{'STATUS':<11}SIGNAL"
    rows = [header, ""]
    for i, p in enumerate(snap["projects"], start=1):
        rows.append(
            f"{i:03d}   {p['key']:<14}{p['status']:<11}{bar(p['commits_30d'], peak, 10)}"
        )
    rows += ["", f"signal = commits in the last 30 days (peak {peak})"]
    return panel("top -p projects", rows, width=58)


def build_feed(snap: dict) -> str:
    if not snap["feed"]:
        return panel("BUILD FEED", ["no public activity in the window"], width=58)
    lines = []
    for e in snap["feed"]:
        head = f"{e['ago']:<14}{e['label']:<9}{e['repo']}"
        lines.append(head)
        if e["detail"]:
            lines.append(f"              └── {e['detail']}")
    return panel("journalctl -u kaushal", lines, width=58)


def stack_telemetry(snap: dict) -> str:
    langs = snap["languages"]
    peak = max((l["pct"] for l in langs), default=0)
    lines = [f"{l['name']:<14}{l['pct']:>5.1f}%  {bar(l['pct'], peak, 14)}" for l in langs]
    lines += ["", "share of bytes across own public repos"]
    return panel("LANGUAGE MIX", lines, width=58)


def ci_status(snap: dict) -> str:
    lines = []
    for p in snap["projects"]:
        if p["ci"] is None:
            mark, state = "·", "no CI"
        elif p["ci"] == "success":
            mark, state = "✓", "passing"
        else:
            mark, state = "✗", str(p["ci"])
        lines.append(f"{mark} {p['key']:<14}{state}")
    failing = [p["key"] for p in snap["projects"] if p["ci"] not in (None, "success")]
    if failing:
        lines += ["", f"⚠ failing: {', '.join(failing)}"]
    return panel("CI STATUS", lines)


RENDERERS = {
    "SYSTEM_STATUS": system_status,
    "PROJECT_TABLE": project_table,
    "BUILD_FEED": build_feed,
    "STACK_TELEMETRY": stack_telemetry,
    "CI_STATUS": ci_status,
}


def render_readme(template: str, snap: dict) -> str:
    """Replace each <!--START:NAME--> ... <!--END:NAME--> region in the template."""
    out = template
    for name in BLOCKS:
        start, end = f"<!--START:{name}-->", f"<!--END:{name}-->"
        if start not in out or end not in out:
            continue
        head, rest = out.split(start, 1)
        _, tail = rest.split(end, 1)
        block = RENDERERS[name](snap)
        out = f"{head}{start}\n```\n{block}\n```\n{end}{tail}"
    return out.replace("{{GENERATED_AT}}", snap["generated_at"])
