"""GitHub-safe Markdown and self-hosted SVG cards. No external stats servers."""
from __future__ import annotations
from html import escape
from .config import BLOCKS
from . import theme


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


def svg_shell(body: str, height: int, title: str, light: bool = False, sheet: str = '') -> str:
    """Blueprint drawing sheet: grid paper, double border, corner ticks and a sheet label."""
    c = theme.palette(light)
    label = f'<text x="868" y="{height - 22}" text-anchor="end" font-size="9" class="m k">{escape(sheet)}</text>' if sheet else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
{theme.style(light)}{theme.grid(900, height, light, inset=10)}{theme.frame(900, height, light)}{body}{label}</svg>'''


def dashboard(snap: dict, light: bool = False) -> str:
    c = theme.palette(light)
    stats = [(snap['totals']['own_repos'], 'PUBLIC REPOSITORIES'), (snap['totals']['stars'], 'STARS · OWN REPOS'), (snap['profile']['followers'], 'FOLLOWERS')]
    body = '<text x="34" y="44" font-size="11" class="k m">DETAIL A · GITHUB TELEMETRY</text>'
    for i, (value, label) in enumerate(stats):
        x = 34 + i * 284
        body += (f'<rect x="{x}" y="60" width="264" height="96" fill="{c["cell"]}" stroke="{c["line"]}" stroke-width="1"/>'
                 f'<text x="{x + 16}" y="122" font-size="44" font-weight="700">{value}</text>'
                 f'<text x="{x + 16}" y="144" font-size="10" class="k m">{label}</text>'
                 f'<text x="{x + 248}" y="78" text-anchor="end" font-size="9" class="n">0{i + 1}</text>')
    date = escape(snap['generated_at'].replace('T', ' ').replace('Z', ' UTC'))
    body += (f'<path d="M34 172H832" stroke="{c["line"]}" stroke-width="0.8"/>'
             f'<path d="M34 168V176M832 168V176" stroke="{c["line"]}"/>'
             f'<text x="34" y="190" font-size="10" class="m">MEASURED {date} · PUBLIC DATA ONLY</text>')
    return svg_shell(body, 214, 'Public GitHub profile metrics', light, 'SHEET 3 / AUTO-GENERATED')


def language_card(snap: dict, light: bool = False) -> str:
    c = theme.palette(light)
    colors = theme.BAR_COLORS[bool(light)]
    body = '<text x="34" y="44" font-size="11" class="k m">DETAIL B · LANGUAGE MIX BY CODE BYTES</text>'
    x = 34.0
    langs = snap['languages']
    body += f'<rect x="34" y="60" width="798" height="16" fill="none" stroke="{c["line"]}" stroke-width="1"/>'
    for i, lang in enumerate(langs):
        width = 798 * lang['pct'] / 100
        body += f'<rect x="{x:.2f}" y="61" width="{width:.2f}" height="14" fill="{colors[i % 6]}"/>'
        x += width
        lx, ly = 34 + (i % 3) * 266, 108 + (i // 3) * 30
        body += (f'<rect x="{lx}" y="{ly - 10}" width="10" height="10" fill="{colors[i % 6]}" stroke="{c["line"]}" stroke-width="0.6"/>'
                 f'<text x="{lx + 18}" y="{ly}" font-size="12">{escape(lang["name"])} <tspan class="m">{lang["pct"]:.1f}%</tspan></text>')
    if not langs:
        body += '<text x="34" y="108" font-size="12" class="m">No public language data available.</text>'
    body += '<text x="34" y="172" font-size="9" class="k m">EXCLUDES FORKS + ARCHIVED REPOS · TOP SIX SHOWN · VOLUME, NOT PROFICIENCY</text>'
    return svg_shell(body, 196, 'Language distribution by code bytes, not proficiency', light, 'SHEET 4 / AUTO-GENERATED')
