"""Optional FastAPI surface over the same collector.

You do not need this to run the README — Actions calls kaushal_api.build
directly. Run it if you want live endpoints:

    pip install fastapi uvicorn
    uvicorn kaushal_api.app:app --reload

Responses are served from a short-lived in-process cache so a burst of requests
can't burn your GitHub rate limit.
"""

from __future__ import annotations

import json
import pathlib
import time

from fastapi import FastAPI, HTTPException

from .collect import collect_safe
from .render import RENDERERS

app = FastAPI(title="kaushal-api", version="1.0")

CACHE_TTL = 600  # seconds
_cache: dict[str, tuple[float, dict]] = {}
SNAPSHOT = pathlib.Path(__file__).resolve().parent.parent / "data" / "status.json"


def snapshot(live: bool = True) -> dict:
    """Live data when possible; the last committed snapshot as a fallback."""
    hit = _cache.get("snap")
    if hit and time.time() - hit[0] < CACHE_TTL:
        return hit[1]
    if live:
        snap, _ = collect_safe()
        if snap:
            _cache["snap"] = (time.time(), snap)
            return snap
    if SNAPSHOT.exists():
        return json.loads(SNAPSHOT.read_text())
    raise HTTPException(503, "no snapshot available")


@app.get("/api/status")
def status() -> dict:
    snap = snapshot()
    return {
        "status": "building",
        "generated_at": snap["generated_at"],
        "totals": snap["totals"],
        "latest": snap["latest"],
    }


@app.get("/api/projects")
def projects() -> list[dict]:
    return snapshot()["projects"]


@app.get("/api/feed")
def feed() -> list[dict]:
    return snapshot()["feed"]


@app.get("/api/languages")
def languages() -> list[dict]:
    return snapshot()["languages"]


@app.get("/api/panel/{name}")
def panel(name: str) -> dict:
    """The rendered Markdown block, handy for embedding elsewhere."""
    key = name.upper()
    if key not in RENDERERS:
        raise HTTPException(404, f"unknown panel: {name}")
    return {"name": key, "text": RENDERERS[key](snapshot())}
