"""Static configuration: who you are, and which repos are 'the projects'.

Everything else in this package is derived from the GitHub API. This file is the
only place you hand-edit when a project's status changes.
"""

from dataclasses import dataclass, field

USER = "kaushalrog"

# How wide the ASCII panels render. 46 fits GitHub's README column without wrapping.
PANEL_WIDTH = 46


@dataclass
class Project:
    """A pinned project. `repo` must be the real repo name under USER."""

    key: str
    repo: str
    status: str  # RESEARCH | BUILDING | ACCEPTED | PUBLISHED
    blurb: str
    # Optional: a hard fact that isn't derivable from the API (paper URL, venue).
    evidence: str = ""


PROJECTS: list[Project] = [
    Project(
        key="WDS-IDS",
        repo="ids-System",
        status="RESEARCH",
        blurb="behavioral intrusion detection, no payload inspection",
        evidence="SRBH-20, 5-fold CV, <12ms end-to-end on Pi 5",
    ),
    Project(
        key="SciRAG-UQ",
        repo="SciRAG-UQ",
        status="BUILDING",
        blurb="uncertainty-aware RAG that abstains instead of guessing",
        evidence="target venue: BDA 2026",
    ),
    Project(
        key="TrafficFlow",
        repo="TrafficFlowAI",
        status="ACCEPTED",
        blurb="hybrid fuzzy-AI adaptive signal control",
        evidence="accepted, ICPEEV 2026, Mahindra University",
    ),
    Project(
        key="AntBot",
        repo="AntBot",
        status="PUBLISHED",
        blurb="low-cost hexapod surveillance platform",
        evidence="IEEE, Jan 2026 — document/11426098",
    ),
]

# Event types worth showing in the build feed, mapped to short labels.
EVENT_LABELS: dict[str, str] = {
    "PushEvent": "PUSH",
    "PullRequestEvent": "PR",
    "IssuesEvent": "ISSUE",
    "CreateEvent": "CREATE",
    "ReleaseEvent": "RELEASE",
    "WatchEvent": "STAR",
    "ForkEvent": "FORK",
    "IssueCommentEvent": "COMMENT",
}

# Markers in README.template.md that get replaced with generated blocks.
BLOCKS: tuple[str, ...] = (
    "SYSTEM_STATUS",
    "PROJECT_TABLE",
    "BUILD_FEED",
    "STACK_TELEMETRY",
    "CI_STATUS",
)
