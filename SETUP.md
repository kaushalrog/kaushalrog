# Profile maintenance

The live profile is generated from `README.template.md`. Edit that template for
bio, links, project cards, and skills. Edit `kaushal_api/config.py` for tracked
project repositories. The generator owns `README.md`, `assets/stats*.svg`,
`assets/languages*.svg`, and `data/status.json`.

## Automatic updates

`.github/workflows/telemetry.yml` runs at minute 17 of each hour, on changes to
the template/generator/workflow on main, and from **Actions → Refresh profile →
Run workflow**. It uses GitHub's built-in token; no personal token, service,
subscription, or extra secret is needed. The workflow explicitly requests
`contents: write` to commit the generated files.

Scheduled refreshes poll public account activity across repositories. A push to
another repository appears on the next refresh, rather than immediately.
GitHub may delay scheduled jobs. In public repositories GitHub disables
scheduled workflows after 60 days without repository activity; re-enable from
the Actions tab if needed. Check the workflow page for the last successful run.

API collection failures stop the update and preserve the last good snapshot.
Generated commits do not retrigger the workflow. Only public data is collected.
Language shares measure bytes, not time spent or proficiency. Stars exclude
forks. The activity feed excludes this profile repository to avoid bot noise.
No contributions/streak claims are rendered or personal-token data requested.

## Local checks

```sh
python3 -m unittest discover -v
GITHUB_TOKEN="$(gh auth token)" python3 -m kaushal_api.build
python3 -m kaushal_api.build --from-json data/status.json
```

Python 3.12 in Actions; standard library only, with no packages to install.
Cards are committed SVGs with explicit light and dark variants, selected by
GitHub's color-scheme setting. They do not depend on third-party stats servers.

Sources: [scheduled events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
and [workflow token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).
