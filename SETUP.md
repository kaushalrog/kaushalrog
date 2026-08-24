# kaushal-api — setup

The README you see on the profile is generated. This repo holds the generator.

```
kaushal_api/config.py    project registry — the only file you hand-edit
kaushal_api/github.py    stdlib GitHub client (REST + GraphQL)
kaushal_api/collect.py   raw API responses  → snapshot dict
kaushal_api/render.py    snapshot dict      → ASCII panels
kaushal_api/build.py     CI entry point
kaushal_api/app.py       optional FastAPI wrapper (not needed for the README)
README.template.md       the source of truth for prose; panels are injected
data/status.json         last snapshot, committed on every run
```

## Install

1. Put these files in the profile repo `kaushalrog/kaushalrog`. That repo's
   `README.md` is what renders on your GitHub profile, and the workflow
   overwrites it on each run — so edit `README.template.md`, never `README.md`.
2. Settings → Actions → General → Workflow permissions → **Read and write**.
   Without this the commit step fails with a 403.
3. Run it once by hand: Actions → telemetry → Run workflow.

## Contributions and streak (optional)

Those two lines need a classic PAT with `read:user`, because the token Actions
provides can't read a user's `contributionsCollection` over GraphQL. Create one
and add it as a repo secret named `PROFILE_TOKEN`. Without it every other panel
still renders and those lines are simply left out.

## Local

```bash
python -m unittest discover -s tests -v      # offline, uses a fake client
GITHUB_TOKEN=ghp_… python -m kaushal_api.build
python -m kaushal_api.build --from-json data/status.json   # re-render, no network
```

## Adding a panel

Write a `snapshot -> str` function in `render.py`, register it in `RENDERERS`,
add its name to `BLOCKS` in `config.py`, and drop
`<!--START:NAME-->` / `<!--END:NAME-->` into the template. `test_panels_are_rectangular`
will catch a ragged box before it ships.

## Notes on behaviour

- **A failed API run leaves the README alone.** `collect_safe` returns `None`
  and `build` exits non-zero rather than writing empty panels.
- **`[skip ci]` is in the commit message** so the auto-commit doesn't retrigger
  the `push` branch of the workflow.
- **Cron is approximate.** GitHub queues scheduled runs; every 6 hours means
  roughly, not exactly.
- **`signal` is commits in the last 30 days**, scaled against your own busiest
  project — it's a relative bar, not an absolute one. The label under the table
  says so, which matters if someone reads AntBot's empty bar as "abandoned"
  rather than "published and finished".
