"""GitHub-safe Markdown and self-hosted SVG cards. No external stats servers."""
from __future__ import annotations
from html import escape
from .config import BLOCKS


def cell(value: object) -> str:
    return escape(str(value)).replace('|', '&#124;').replace('\n', ' ').replace('\r', ' ').replace('`', '&#96;').replace('[', '&#91;').replace(']', '&#93;')


def activity(snap: dict) -> str:
    rows = []
    for e in snap['feed'][:5]:
        display_repo = e['repo'] if len(e['repo']) <= 45 else e['repo'][:42] + '…'
        label = {'PR': 'Pull request', 'PUSH': 'Push'}.get(e['label'], e['label'].title())
        rows.append(f"- `{cell(e['at'][:10])}` &nbsp; **{cell(label)}** · [{cell(display_repo)}](https://github.com/{e['repo']}) — {cell(e['detail'] or 'Public activity')}")
    return '\n'.join(rows) if rows else 'Recent public activity will appear here after your next GitHub update.'


def project_pulse(snap: dict) -> str:
    rows = ['| Project | Your commits · last 30 days | Latest push (UTC) |', '| :--- | ---: | :--- |']
    for p in snap['projects']:
        if p['exists']:
            rows.append(f"| [{cell(p['key'])}](https://github.com/{snap['user']}/{p['repo']}) | {p['commits_30d']} | {cell((p['pushed_at'] or '')[:10])} |")
    return '\n'.join(rows)


RENDERERS = {'ACTIVITY': activity, 'PROJECT_PULSE': project_pulse}


def render_readme(template: str, snap: dict) -> str:
    out = template
    for name in BLOCKS:
        start, end = f'<!--START:{name}-->', f'<!--END:{name}-->'
        if out.count(start) != 1 or out.count(end) != 1:
            raise ValueError(f'Expected exactly one marker pair for {name}')
        head, rest = out.split(start, 1)
        _, tail = rest.split(end, 1)
        out = f'{head}{start}\n{RENDERERS[name](snap)}\n{end}{tail}'
    return out.replace('{{GENERATED_AT}}', snap['generated_at'])


def svg_shell(body: str, height: int, title: str, light: bool = False) -> str:
    bg, fg, muted, border, accent = ('#eee9df', '#272520', '#696156', '#c5bcad', '#9b3e25') if light else ('#191817', '#eee9df', '#b5aa98', '#494239', '#e5a078')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<style>text{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;fill:{fg}}}.muted{{fill:{muted}}}.accent{{fill:{accent}}}.mono{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}</style>
<rect x="1" y="1" width="898" height="{height-2}" rx="0" fill="{bg}" stroke="{border}"/>{body}</svg>'''


def dashboard(snap: dict, light: bool = False) -> str:
    stats = [(snap['totals']['own_repos'], 'OWN PUBLIC REPOS'), (snap['totals']['stars'], 'STARS ON OWN REPOS'), (snap['profile']['followers'], 'FOLLOWERS')]
    body = '<text x="24" y="30" class="mono muted" font-size="11" letter-spacing="2">GITHUB / OBSERVATIONS</text>'
    for i, (value, label) in enumerate(stats):
        x = 24 + i * 298
        if i:
            body += f'<path d="M{x-16} 53V119" stroke="currentColor" opacity=".2"/>'
        body += f'<text x="{x}" y="94" font-size="44" font-weight="400" style="font-family:Georgia,serif">{value:02d}</text><text x="{x}" y="119" font-size="11" letter-spacing="1" class="mono muted">{label}</text>'
    date = escape(snap['generated_at'].replace('T', ' ').replace('Z', ' UTC'))
    body += f'<text x="24" y="157" font-size="10" class="mono muted">PUBLIC DATA / {date}</text>'
    return svg_shell(body, 178, 'Public GitHub profile metrics', light)


def language_card(snap: dict, light: bool = False) -> str:
    colors = ['#d19572', '#b5aa98', '#97a594', '#b69b82', '#a0a6b0', '#c4b9a5']
    body = '<text x="32" y="37" class="mono muted" font-size="12" letter-spacing="2">LANGUAGES / ACROSS PUBLIC REPOSITORIES</text>'
    x = 32.0
    langs = snap['languages']
    for i, lang in enumerate(langs):
        width = 836 * lang['pct'] / 100
        body += f'<rect x="{x:.2f}" y="58" width="{width:.2f}" height="10" fill="{colors[i % 6]}"/>'
        x += width
        lx, ly = 32 + (i % 3) * 284, 100 + (i // 3) * 30
        body += f'<circle cx="{lx+4}" cy="{ly-4}" r="4" fill="{colors[i % 6]}"/><text x="{lx+18}" y="{ly}" font-size="12">{escape(lang["name"])} <tspan class="muted">{lang["pct"]:.1f}%</tspan></text>'
    if not langs:
        body += '<text x="32" y="100" font-size="13" class="muted">No public language data available.</text>'
    body += '<text x="32" y="164" font-size="10" class="mono muted">SHARE OF CODE BYTES · EXCLUDES FORKS + ARCHIVED REPOS · TOP SIX SHOWN</text>'
    return svg_shell(body, 186, 'Language distribution by code bytes, not proficiency', light)
