"""Draw the hand-tuned blueprint assets: banner, project spec sheets, bill of materials.

Run from the repository root:  python3 design/make_assets.py
Writes assets/banner*.svg, assets/card-*.svg and assets/bom*.svg in dark (blueprint)
and light (whiteprint) variants. Standard library only.
"""
from __future__ import annotations

import pathlib
import sys
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kaushal_api import theme  # noqa: E402

# Resting state is fully drawn; animations start from blank only where CSS animation runs.
DRAW = ('.d{stroke-dasharray:1200;animation:plot 2.4s ease-out backwards}'
        '.d2{animation-delay:.6s}.d3{animation-delay:1.2s}.f{animation:fade .6s ease-out backwards}'
        '.f1{animation-delay:.4s}.f2{animation-delay:1.4s}.f3{animation-delay:2.2s}'
        '@keyframes plot{from{stroke-dashoffset:1200}to{stroke-dashoffset:0}}@keyframes fade{from{opacity:0}to{opacity:1}}'
        '@media (prefers-reduced-motion:reduce){.d,.f{animation:none}}')


def svg(w, h, title, desc, body, light, extra=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
            f'{theme.style(light, extra)}{theme.grid(w, h, light, inset=10)}{theme.frame(w, h, light)}{body}</svg>\n')


def arrow_dim(x1, x2, y, label, c, cls='', size=10, tick=8):
    """Horizontal dimension line with arrowheads, extension ticks and a centred label."""
    mid = (x1 + x2) / 2
    gap = len(label) * size * 0.34 + 10
    return (f'<g class="{cls}" stroke="{c["line"]}" stroke-width="1" fill="none">'
            f'<path d="M{x1} {y - tick}V{y + tick}M{x2} {y - tick}V{y + tick}"/>'
            f'<path d="M{x1} {y}H{mid - gap}M{mid + gap} {y}H{x2}"/>'
            f'<path d="M{x1 + 9} {y - 4}L{x1} {y}L{x1 + 9} {y + 4}M{x2 - 9} {y - 4}L{x2} {y}L{x2 - 9} {y + 4}"/></g>'
            f'<text x="{mid}" y="{y + 3.5}" text-anchor="middle" font-size="{size}" class="k {cls}">{escape(label)}</text>')


def banner(light):
    c = theme.palette(light)
    L = c['line']
    b = '<text x="36" y="46" font-size="10" class="k m f">DRAWING NO. KR-001 · GENERAL ARRANGEMENT · ENGINEER, HUMAN</text>'
    # name and its dimension
    b += '<text x="34" y="118" font-size="54" font-weight="700" letter-spacing="-1" class="f f1">KAUSHAL REDDY</text>'
    b += arrow_dim(36, 466, 142, '1 × ENGINEER', c, 'f f1')
    # three domains with a chained dimension
    b += ('<g class="f f2"><text x="36" y="186" font-size="15">AI SYSTEMS</text><text x="186" y="186" font-size="15">SECURITY</text>'
          '<text x="320" y="186" font-size="15">EDGE COMPUTING</text></g>')
    b += (f'<g class="f f2" stroke="{L}" stroke-width="1" fill="none"><path d="M36 202H466"/>'
          f'<path d="M36 196V208M176 196V208M310 196V208M466 196V208"/></g>')
    b += '<text x="36" y="224" font-size="9" class="k m f f2">3 DOMAINS · EQUAL SPACING NOT GUARANTEED</text>'
    # schematic: signal -> model -> confident? -> act / abstain
    S = f'stroke="{L}" stroke-width="1.4" fill="none"'
    b += (f'<g class="d"><rect x="520" y="74" width="92" height="40" {S}/><path d="M612 94H648" {S}/>'
          f'<path d="M641 90L648 94L641 98" {S}/></g>'
          f'<g class="d d2"><rect x="648" y="74" width="92" height="40" {S}/><path d="M740 94H770" {S}/>'
          f'<path d="M763 90L770 94L763 98" {S}/></g>'
          f'<g class="d d3"><path d="M806 66L842 94L806 122L770 94Z" {S}/>'
          f'<path d="M806 122V160" {S}/><path d="M802 153L806 160L810 153" {S}/>'
          f'<path d="M842 94H866V160" {S}/><path d="M862 153L866 160L870 153" {S}/></g>')
    b += ('<g class="f f2" font-size="11"><text x="566" y="98" text-anchor="middle">SIGNAL</text>'
          '<text x="694" y="98" text-anchor="middle">MODEL</text><text x="806" y="98" text-anchor="middle" font-size="10">SURE?</text>'
          '<text x="806" y="176" text-anchor="middle">ACT</text><text x="866" y="176" text-anchor="middle" class="a">ABSTAIN</text>'
          '<text x="790" y="140" font-size="9" class="m">YES</text><text x="848" y="86" font-size="9" class="m">NO</text></g>')
    # note callout
    b += (f'<g class="f f3"><path d="M712 196L786 114" stroke="{c["note"]}" stroke-width="1"/>'
          f'<circle cx="786" cy="114" r="2.5" fill="{c["note"]}"/>'
          f'<text x="520" y="204" font-size="11" class="n">NOTE 1: A MODEL MUST KNOW</text>'
          f'<text x="520" y="220" font-size="11" class="n">WHEN IT IS WRONG.</text></g>')
    # title block
    tb_x, tb_y, tb_w, tb_h = 520, 250, 362, 86
    b += (f'<g stroke="{L}" stroke-width="1" fill="{c["cell"]}"><rect x="{tb_x}" y="{tb_y}" width="{tb_w}" height="{tb_h}"/></g>'
          f'<g stroke="{L}" stroke-width="0.8"><path d="M{tb_x} {tb_y + 44}H{tb_x + tb_w}"/>'
          f'<path d="M{tb_x + 120} {tb_y + 44}V{tb_y + tb_h}M{tb_x + 200} {tb_y + 44}V{tb_y + tb_h}M{tb_x + 270} {tb_y + 44}V{tb_y + tb_h}"/></g>')
    cells = [(tb_x + 8, 'DRAWN', 'K. REDDY'), (tb_x + 128, 'SCALE', '1 : 1'), (tb_x + 208, 'REV', 'C'), (tb_x + 278, 'SHEET', '1 / 5')]
    b += f'<text x="{tb_x + 8}" y="{tb_y + 16}" font-size="8" class="k m">TITLE</text>'
    b += f'<text x="{tb_x + 8}" y="{tb_y + 34}" font-size="12" font-weight="700">BUILT FOR THE RUN AFTER THE DEMO</text>'
    for x, k, v in cells:
        b += f'<text x="{x}" y="{tb_y + 58}" font-size="8" class="k m">{k}</text><text x="{x}" y="{tb_y + 76}" font-size="12">{v}</text>'
    b += '<text x="36" y="318" font-size="11" class="k m">INTELLIGENT BY DESIGN · RELIABLE IN THE REAL WORLD</text>'
    return svg(900, 350, 'Kaushal Reddy: AI systems, security and edge computing',
               'Blueprint drawing KR-001: the name Kaushal Reddy with a dimension line labelled one engineer, three domains '
               '(AI systems, security, edge computing), and a schematic where a model either acts or abstains when unsure.',
               b, light, DRAW)


CARDS = [
    dict(slug='wds-ids', no='KR-101', part='WDS-IDS', tag='SECURITY + EDGE', status='RESEARCH',
         q=['CAN YOU CATCH AN ATTACK WITHOUT', 'READING THE PAYLOAD?'],
         spec=[('METHOD', 'OS behaviour + drift'), ('DATA', 'SRBH-20 · 5-fold CV'), ('LATENCY', '< 12 ms on Raspberry Pi 5')],
         glyph='wave'),
    dict(slug='scirag-uq', no='KR-102', part='SCIRAG-UQ', tag='RETRIEVAL + REASONING', status='BUILDING',
         q=['WHEN SHOULD A MODEL SAY', '"I DON\'T KNOW"?'],
         spec=[('METHOD', 'multi-signal confidence'), ('OUTPUT', 'answer  |  abstain'), ('TARGET', 'BDA 2026')],
         glyph='branch'),
    dict(slug='trafficflow', no='KR-103', part='TRAFFICFLOW AI', tag='AI + URBAN SYSTEMS', status='ACCEPTED',
         q=['WHAT IF A TRAFFIC LIGHT', 'COULD READ THE QUEUE?'],
         spec=[('METHOD', 'ML + fuzzy logic'), ('UI', 'live congestion dashboard'), ('VENUE', 'ICPEEV 2026 · accepted')],
         glyph='light'),
    dict(slug='ct-recon', no='KR-104', part='MCDIP-ADMM', tag='VISION + OPTIMIZATION', status='RESEARCH',
         q=['HOW MUCH OF A CT SCAN', 'SURVIVES LESS RADIATION?'],
         spec=[('METHOD', 'ADMM + multi-code DIP'), ('EVAL', 'PSNR · SSIM, synthetic'), ('MODE', 'unsupervised')],
         glyph='ring'),
]


def glyph(kind, x, y, c):
    S = f'stroke="{c["line"]}" stroke-width="1.3" fill="none"'
    N = f'stroke="{c["note"]}" stroke-width="1.3" fill="none"'
    if kind == 'wave':
        return (f'<path d="M{x} {y + 30}h10l5-6 5 6 5-5 5 5h6l4-26 5 46 4-20h8l5-5 5 5h10" {S}/>'
                f'<circle cx="{x + 44}" cy="{y + 4}" r="7" {N}/>')
    if kind == 'branch':
        return (f'<rect x="{x}" y="{y + 18}" width="22" height="16" {S}/><path d="M{x + 22} {y + 26}H{x + 36}" {S}/>'
                f'<path d="M{x + 48} {y + 14}L{x + 60} {y + 26}L{x + 48} {y + 38}L{x + 36} {y + 26}Z" {S}/>'
                f'<path d="M{x + 60} {y + 26}H{x + 76}M{x + 48} {y + 38}V{y + 52}" {S}/><circle cx="{x + 80}" cy="{y + 26}" r="4" {N}/>')
    if kind == 'light':
        return (f'<rect x="{x + 24}" y="{y}" width="26" height="58" rx="4" {S}/>'
                f'<circle cx="{x + 37}" cy="{y + 12}" r="6" {S}/><circle cx="{x + 37}" cy="{y + 29}" r="6" {N}/>'
                f'<circle cx="{x + 37}" cy="{y + 46}" r="6" {S}/><path d="M{x} {y + 66}H{x + 80}" {S} stroke-dasharray="4 4"/>')
    return (f'<circle cx="{x + 38}" cy="{y + 30}" r="28" {S}/><circle cx="{x + 38}" cy="{y + 30}" r="16" {S}/>'
            f'<path d="M{x + 38} {y - 4}V{y + 64}M{x + 4} {y + 30}H{x + 72}" {S} stroke-dasharray="3 3"/>'
            f'<circle cx="{x + 46}" cy="{y + 24}" r="4" {N}/>')


def card(d, light):
    c = theme.palette(light)
    L = c['line']
    w, h = 440, 250
    b = (f'<text x="26" y="38" font-size="9" class="k m">DWG {d["no"]} · {d["tag"]}</text>'
         f'<rect x="{w - 26 - len(d["status"]) * 7.4 - 14}" y="26" width="{len(d["status"]) * 7.4 + 14}" height="18" fill="none" stroke="{c["note"]}"/>'
         f'<text x="{w - 33}" y="39" text-anchor="end" font-size="10" class="k n">{d["status"]}</text>'
         f'<text x="26" y="72" font-size="22" font-weight="700">{escape(d["part"])}</text>')
    for i, line in enumerate(d['q']):
        b += f'<text x="26" y="{98 + i * 17}" font-size="11.5" class="a">{escape(line)}</text>'
    b += glyph(d['glyph'], 336, 76, c)
    ty = 148
    b += f'<rect x="26" y="{ty}" width="{w - 52}" height="78" fill="{c["cell"]}" stroke="{L}" stroke-width="1"/>'
    for i, (k, v) in enumerate(d['spec']):
        y = ty + 22 + i * 24
        if i:
            b += f'<path d="M26 {y - 15}H{w - 26}" stroke="{L}" stroke-width="0.5" opacity="0.6"/>'
        b += f'<text x="38" y="{y}" font-size="9" class="k m">{k}</text><text x="116" y="{y}" font-size="11.5">{escape(v)}</text>'
    b += f'<path d="M106 {ty}V{ty + 78}" stroke="{L}" stroke-width="0.5" opacity="0.6"/>'
    return svg(w, h, f'{d["part"]}: {" ".join(d["q"]).title()}',
               f'Spec sheet {d["no"]}, status {d["status"].lower()}. ' + '; '.join(f'{k.lower()}: {v}' for k, v in d['spec']) + '.',
               b, light)


FEATURED = dict(
    no='KR-100', part='SATELLITE OPTICAL FAULT RECOVERY', status='LATEST · LIVE SITE',
    q='WHEN A LASER LINK BETWEEN SATELLITES FAILS, WHAT BROKE, AND CAN IT BE FIXED?',
    stack='MATLAB R2026a · Simulink · 4–10 satellites · 320 matched trials',
    # (label, before, after, unit, higher_is_better)
    bars=[('DETECTION ACCURACY', 72.1, 96.5, '%', True), ('EXACT FAULT ISOLATION', 9.5, 71.5, '%', True),
          ('FALSE-ALARM RATE', 33.4, 3.0, '%', False)],
    footer='V1 → V2 SUPERVISOR · 4-SATELLITE NETWORK · REPRODUCED 320 / 320 TRIALS EXACTLY',
)


def featured(light):
    c = theme.palette(light)
    L, d = c['line'], FEATURED
    w, h = 900, 320
    b = (f'<text x="34" y="44" font-size="10" class="k m">DWG {d["no"]} · FEATURED PROJECT</text>'
         f'<rect x="{w - 34 - len(d["status"]) * 7.4 - 16}" y="30" width="{len(d["status"]) * 7.4 + 16}" height="20" fill="{c["note"]}"/>'
         f'<text x="{w - 42}" y="44" text-anchor="end" font-size="10" font-weight="700" class="k" style="fill:{c["paper"]}">{d["status"]}</text>'
         f'<text x="34" y="82" font-size="26" font-weight="700">{d["part"]}</text>'
         f'<text x="34" y="106" font-size="11.5" class="a">{escape(d["q"])}</text>'
         f'<text x="34" y="126" font-size="10" class="m">{escape(d["stack"])}</text>')
    # before/after bars
    x0, bw, y = 34, 300, 160
    b += (f'<text x="{x0}" y="{y - 8}" font-size="8" class="k m">METRIC</text>'
          f'<rect x="{x0 + 176}" y="{y - 15}" width="14" height="6" fill="{c["muted"]}" opacity="0.6"/>'
          f'<text x="{x0 + 196}" y="{y - 8}" font-size="8" class="k m">V1 ORIGINAL</text>'
          f'<rect x="{x0 + 300}" y="{y - 15}" width="14" height="6" fill="{c["note"]}"/>'
          f'<text x="{x0 + 320}" y="{y - 8}" font-size="8" class="k m">V2 REVISED</text>')
    for i, (lab, a, z, u, hi) in enumerate(d['bars']):
        yy = y + i * 34
        b += (f'<text x="{x0}" y="{yy + 10}" font-size="9" class="k">{lab}</text>'
              f'<rect x="{x0 + 176}" y="{yy}" width="{bw}" height="6" fill="none" stroke="{L}" stroke-width="0.6"/>'
              f'<rect x="{x0 + 176}" y="{yy}" width="{bw * a / 100:.1f}" height="6" fill="{c["muted"]}" opacity="0.6"/>'
              f'<rect x="{x0 + 176}" y="{yy + 8}" width="{bw * z / 100:.1f}" height="6" fill="{c["note"]}"/>'
              f'<text x="{x0 + 176}" y="{yy + 27}" font-size="10" class="m">{a}{u}</text>'
              f'<text x="{x0 + 176 + bw}" y="{yy + 27}" font-size="11" font-weight="700" text-anchor="end" class="n">{z}{u} {"↑" if hi else "↓"}</text>')
    # constellation: ring of four satellites, edge 1 faulted
    cx, cy, r = 700, 178, 74
    pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{L}" stroke-width="0.6" stroke-dasharray="2 4"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="16" fill="none" stroke="{L}" stroke-width="0.8"/><text x="{cx}" y="{cy + 3}" text-anchor="middle" font-size="7" class="m">EARTH</text>'
    for i in range(4):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % 4]
        if i == 0:
            b += f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c["note"]}" stroke-width="1.6" stroke-dasharray="5 4"/>'
        else:
            b += f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{L}" stroke-width="1.2"/>'
    for i, (x, yy) in enumerate(pts):
        b += (f'<rect x="{x - 7}" y="{yy - 7}" width="14" height="14" fill="{c["cell"]}" stroke="{L}" stroke-width="1.2"/>'
              f'<path d="M{x - 18} {yy}H{x - 8}M{x + 8} {yy}H{x + 18}" stroke="{c["accent"]}" stroke-width="3"/>')
    b += (f'<path d="M{cx + 40} {cy - 40}L{cx + 92} {cy - 86}H{cx + 150}" stroke="{c["note"]}" stroke-width="0.8" fill="none"/>'
          f'<text x="{cx + 94}" y="{cy - 92}" font-size="9" class="n">EDGE 1 · FAULT</text>'
          f'<text x="{cx + 94}" y="{cy - 74}" font-size="9" class="n">DIAGNOSE → FIX</text>'
          f'<text x="{cx + 94}" y="{cy - 62}" font-size="9" class="n">→ VERIFY</text>')
    b += (f'<path d="M34 {h - 42}H{w - 34}" stroke="{L}" stroke-width="0.6" opacity="0.7"/>'
          f'<text x="34" y="{h - 24}" font-size="9" class="k m">{escape(d["footer"])}</text>')
    return svg(w, h, 'Featured: Satellite Optical Fault Recovery',
               'Featured project KR-100. Active fault diagnosis and verified recovery for satellite laser links, '
               'MATLAB and Simulink, 320 matched trials. Detection accuracy 72.1% to 96.5%, exact fault isolation 9.5% to 71.5%, '
               'false-alarm rate 33.4% to 3.0%. Reproduced 320 of 320 trials exactly.', b, light)


BOM = [
    ('01', 'LANGUAGES', 'Python · C++ · Java · SQL · Bash'),
    ('02', 'MACHINE LEARNING', 'PyTorch · TensorFlow · scikit-learn · LightGBM'),
    ('03', 'LLM SYSTEMS', 'RAG · Transformers · agentic AI · MCP'),
    ('04', 'RETRIEVAL', 'FAISS · ChromaDB'),
    ('05', 'SYSTEMS', 'Linux · Docker · FastAPI · REST APIs · GitHub Actions'),
    ('06', 'SECURITY', 'behavioural analysis · intrusion detection'),
    ('07', 'HARDWARE', 'Raspberry Pi · Arduino'),
]


def bom(light):
    c = theme.palette(light)
    L = c['line']
    rh, top = 28, 66
    h = top + rh * (len(BOM) + 1) + 40
    b = '<text x="34" y="46" font-size="11" class="k m">SHEET 5 · BILL OF MATERIALS</text>'
    tw = 832
    b += f'<rect x="34" y="{top}" width="{tw}" height="{rh * (len(BOM) + 1)}" fill="{c["cell"]}" stroke="{L}" stroke-width="1"/>'
    b += f'<path d="M34 {top + rh}H{34 + tw}" stroke="{L}" stroke-width="1"/>'
    b += f'<path d="M94 {top}V{top + rh * (len(BOM) + 1)}M284 {top}V{top + rh * (len(BOM) + 1)}" stroke="{L}" stroke-width="0.8"/>'
    b += (f'<text x="46" y="{top + 18}" font-size="9" class="k m">ITEM</text><text x="106" y="{top + 18}" font-size="9" class="k m">ASSEMBLY</text>'
          f'<text x="296" y="{top + 18}" font-size="9" class="k m">PARTS</text>')
    for i, (n, k, v) in enumerate(BOM):
        y = top + rh * (i + 1)
        if i:
            b += f'<path d="M34 {y}H{34 + tw}" stroke="{L}" stroke-width="0.4" opacity="0.6"/>'
        b += (f'<text x="46" y="{y + 19}" font-size="11" class="n">{n}</text><text x="106" y="{y + 19}" font-size="11">{k}</text>'
              f'<text x="296" y="{y + 19}" font-size="12">{escape(v)}</text>')
    b += f'<text x="34" y="{h - 22}" font-size="9" class="k m">ALL PARTS IN SERVICE · SUBSTITUTIONS CONSIDERED ON MERIT</text>'
    return svg(900, h, 'Toolbox: bill of materials',
               'Tools by area. ' + '; '.join(f'{k.title()}: {v}' for _, k, v in BOM) + '.', b, light)


def main():
    out = ROOT / 'assets'
    out.mkdir(exist_ok=True)
    files = {}
    for light in (False, True):
        sfx = '-light' if light else ''
        files[f'banner{sfx}.svg'] = banner(light)
        files[f'bom{sfx}.svg'] = bom(light)
        files[f'featured{sfx}.svg'] = featured(light)
        for d in CARDS:
            files[f'card-{d["slug"]}{sfx}.svg'] = card(d, light)
    for name, content in files.items():
        (out / name).write_text(content)
    print('wrote', len(files), 'files to', out)


if __name__ == '__main__':
    main()
