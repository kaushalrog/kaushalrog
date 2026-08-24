"""Entry point for CI: python -m kaushal_api.build

Writes data/status.json and rewrites README.md from README.template.md.
Exits non-zero only on a genuine failure — a rate-limited API run leaves the
existing README untouched rather than replacing it with empty panels.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

from .collect import collect_safe
from .render import render_readme

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", default=str(ROOT / "README.template.md"))
    ap.add_argument("--out", default=str(ROOT / "README.md"))
    ap.add_argument("--data", default=str(ROOT / "data" / "status.json"))
    ap.add_argument(
        "--from-json",
        help="skip the API and render from an existing snapshot (for local preview)",
    )
    args = ap.parse_args(argv)

    if args.from_json:
        snap = json.loads(pathlib.Path(args.from_json).read_text())
    else:
        snap, err = collect_safe()
        if snap is None:
            print(f"collect failed: {err}", file=sys.stderr)
            return 1

    data_path = pathlib.Path(args.data)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(snap, indent=2) + "\n")

    template = pathlib.Path(args.template).read_text()
    pathlib.Path(args.out).write_text(render_readme(template, snap))
    print(f"rendered {args.out} from snapshot at {snap['generated_at']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
