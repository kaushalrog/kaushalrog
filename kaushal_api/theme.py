"""Blueprint visual theme shared by the generated cards and the hand-tuned assets.

Dark mode is a classic blueprint (white linework on blue). Light mode is a
"whiteprint" (blue linework on white paper).
"""
from __future__ import annotations

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

PALETTES = {
    False: dict(paper='#0f3d7a', minor='#1f4f8f', major='#3364a6', line='#eaf2ff', muted='#a9c4ea',
                note='#ffd54a', accent='#7fe3ff', cell='#123f7e'),
    True: dict(paper='#f7f9fc', minor='#e3ecf7', major='#c6d6ec', line='#0f3d7a', muted='#4a6a94',
               note='#b06f00', accent='#1f78c8', cell='#eef3fa'),
}
BAR_COLORS = {
    False: ['#eaf2ff', '#ffd54a', '#7fe3ff', '#ff9eb5', '#a8f0c6', '#c9b6ff'],
    True: ['#0f3d7a', '#c48a00', '#1f9fd0', '#d0507a', '#2f9e6d', '#7a5fd1'],
}


def palette(light: bool) -> dict:
    return PALETTES[bool(light)]


def grid(width: int, height: int, light: bool, step: int = 12, major_every: int = 5, inset: int = 0) -> str:
    """Drafting-paper grid as two SVG patterns plus the filled background."""
    c = palette(light)
    big = step * major_every
    return (f'<defs><pattern id="gmin" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<path d="M{step} 0H0V{step}" fill="none" stroke="{c["minor"]}" stroke-width="0.6"/></pattern>'
            f'<pattern id="gmaj" width="{big}" height="{big}" patternUnits="userSpaceOnUse">'
            f'<rect width="{big}" height="{big}" fill="url(#gmin)"/>'
            f'<path d="M{big} 0H0V{big}" fill="none" stroke="{c["major"]}" stroke-width="0.9"/></pattern></defs>'
            f'<rect width="{width}" height="{height}" fill="{c["paper"]}"/>'
            f'<rect x="{inset}" y="{inset}" width="{width - 2 * inset}" height="{height - 2 * inset}" fill="url(#gmaj)"/>')


def frame(width: int, height: int, light: bool, inset: int = 10) -> str:
    """Double drawing border with corner registration ticks."""
    c = palette(light)
    i2 = inset + 6
    ticks = ''
    for x, y, dx, dy in ((inset, inset, 1, 1), (width - inset, inset, -1, 1), (inset, height - inset, 1, -1), (width - inset, height - inset, -1, -1)):
        ticks += f'<path d="M{x} {y + dy * 18}V{y}H{x + dx * 18}" fill="none" stroke="{c["line"]}" stroke-width="2"/>'
    return (f'<rect x="{inset}" y="{inset}" width="{width - 2 * inset}" height="{height - 2 * inset}" fill="none" stroke="{c["line"]}" stroke-width="1.4"/>'
            f'<rect x="{i2}" y="{i2}" width="{width - 2 * i2}" height="{height - 2 * i2}" fill="none" stroke="{c["line"]}" stroke-width="0.6" opacity="0.6"/>{ticks}')


def style(light: bool, extra: str = '') -> str:
    c = palette(light)
    return (f'<style>text{{font-family:{MONO};fill:{c["line"]}}}.m{{fill:{c["muted"]}}}.n{{fill:{c["note"]}}}.a{{fill:{c["accent"]}}}'
            f'.k{{letter-spacing:1.6px}}{extra}</style>')
