"""GitHub-safe Markdown and self-hosted SVG cards. No external stats servers."""
from __future__ import annotations
from html import escape
from .config import BLOCKS


def cell(value: object) -> str:
    return escape(str(value)).replace('|', '&#124;').replace('\n', ' ').replace('\r', ' ').replace('`', '&#96;').replace('[', '&#91;').replace(']', '&#93;')


def activity(snap: dict) -> str:
    rows = ['| Date (UTC) | Activity | Repository |', '| :--- | :--- | :--- |']
    for e in snap['feed'][:5]:
        display_repo = e['repo'] if len(e['repo']) <= 45 else e['repo'][:42] + '…'
        rows.append(f"| {cell(e['at'][:10])} | {cell(e['label'].title())} · {cell(e['detail'] or 'Public activity')} | [{cell(display_repo)}](https://github.com/{e['repo']}) |")
    return '\n'.join(rows) if snap['feed'] else 'Recent public activity will appear here after your next GitHub update.'


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
    bg, fg, muted, border, accent = ('#f6f8fa', '#172b26', '#4c625b', '#cbd8d1', '#087957') if light else ('#111b18', '#edf7f1', '#9db7aa', '#2b4036', '#a6efc4')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<style>text{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;fill:{fg}}}.muted{{fill:{muted}}}.accent{{fill:{accent}}}.mono{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}</style>
<rect x="1" y="1" width="898" height="{height-2}" rx="18" fill="{bg}" stroke="{border}"/>{body}</svg>'''


def dashboard(snap: dict, light: bool = False) -> str:
    stats = [(snap['totals']['own_repos'], 'PUBLIC REPOSITORIES'), (snap['totals']['stars'], 'STARS · OWN REPOS'), (snap['profile']['followers'], 'FOLLOWERS')]
    body = '<text x="32" y="38" class="mono muted" font-size="12" letter-spacing="2">GITHUB / AT A GLANCE</text><circle cx="860" cy="33" r="4" class="accent"/>'
    for i, (value, label) in enumerate(stats):
        x = 32 + i * 298
        body += f'<text x="{x}" y="108" font-size="48" font-weight="650">{value}</text><text x="{x}" y="139" font-size="11" letter-spacing="1.5" class="mono muted">{label}</text>'
    date = escape(snap['generated_at'].replace('T', ' ').replace('Z', ' UTC'))
    body += f'<text x="32" y="181" font-size="11" class="mono muted">PUBLIC DATA · UPDATED {date}</text>'
    return svg_shell(body, 204, 'Public GitHub profile metrics', light)


def language_card(snap: dict, light: bool = False) -> str:
    colors = ['#62c69a', '#83b7e8', '#b8a2e8', '#e9bd7c', '#e599a4', '#a4bf95']
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
