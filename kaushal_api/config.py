"""Static configuration: who you are, and which repos are 'the projects'.

Everything else in this package is derived from the GitHub API. This file is the
only place you hand-edit when a project's status changes.
"""

from dataclasses import dataclass

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
        repo="ids---System",
        status="RESEARCH",
        blurb="behavioral intrusion detection, no payload inspection",
        evidence="SRBH-20, 5-fold CV, <12ms end-to-end on Pi 5",
    ),
    Project(
        key="SciRAG-UQ",
        repo="scirag-uq",
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
        key="CT Reconstruction",
        repo="mcdip-admm-ct-reconstruction",
        status="RESEARCH",
        blurb="unsupervised low-dose CT reconstruction with ADMM and Deep Image Prior",
        evidence="synthetic-data evaluation using PSNR and SSIM",
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

# Generated regions in README.template.md.
BLOCKS = ("ACTIVITY", "PROJECT_PULSE")
