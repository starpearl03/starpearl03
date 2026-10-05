"""Generates the animated SVGs used by the profile README (pure SVG + CSS, no JS, so GitHub renders them)."""
import math
import random
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)
random.seed(7)

BG0, BG1 = "#0b1020", "#1f3864"
INK, MUTED, ACCENT, GLOW = "#f2f4f8", "#a9b4c8", "#7aa2f7", "#f6c177"
SANS = "'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"
REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def banner():
    W, H = 1200, 320
    glyphs = list("{}<>/=;01+·*#") + ["</>", "fn", "=>", "&&"]
    field = []
    for _ in range(120):
        x, y = random.uniform(10, W - 10), random.uniform(16, H - 8)
        if 40 < x < 760 and 70 < y < 270:  # keep the text area calm
            continue
        g = random.choice(glyphs).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        dur, delay = random.uniform(3, 7), random.uniform(0, 6)
        size = random.choice([11, 12, 13, 15])
        field.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" class="g" '
                     f'style="animation-duration:{dur:.1f}s;animation-delay:-{delay:.1f}s">{g}</text>')

    # "Dusk" glyph sphere: points on a sphere projected to 2D, rotating via a horizontal scroll of longitude.
    cx, cy, r = 1010, 160, 92
    sphere = []
    for lat in range(-75, 76, 15):
        ring_r = r * math.cos(math.radians(lat))
        y = cy - r * math.sin(math.radians(lat))
        n = max(4, int(ring_r / 9))
        for i in range(n):
            phase = i / n
            sphere.append(
                f'<circle cx="{cx}" cy="{y:.1f}" r="2.1" class="p" '
                f'style="--rx:{ring_r:.1f}px;animation-delay:-{phase * 9:.2f}s"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Felistas Charuka, Software Engineer">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
  <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".35"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
</defs>
<style>
  .g{{fill:{ACCENT};font-family:{MONO};opacity:.08;animation:tw ease-in-out infinite}}
  @keyframes tw{{0%,100%{{opacity:.06}}50%{{opacity:.5}}}}
  .p{{fill:{GLOW};animation:orbit 9s linear infinite}}
  @keyframes orbit{{
    0%{{transform:translateX(0);opacity:.15;animation-timing-function:ease-out}}
    25%{{transform:translateX(var(--rx));opacity:.55;animation-timing-function:ease-in}}
    50%{{transform:translateX(0);opacity:1;animation-timing-function:ease-out}}
    75%{{transform:translateX(calc(var(--rx) * -1));opacity:.55;animation-timing-function:ease-in}}
    100%{{transform:translateX(0);opacity:.15;animation-timing-function:ease-out}}}}
  .halo{{animation:breathe 6s ease-in-out infinite;transform-origin:{cx}px {cy}px}}
  @keyframes breathe{{0%,100%{{transform:scale(.92);opacity:.7}}50%{{transform:scale(1.06);opacity:1}}}}
  .in{{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}}
  @keyframes rise{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
  .name{{font-family:{SERIF};font-size:64px;fill:{INK}}}
  .role{{font-family:{SANS};font-size:22px;fill:{GLOW};letter-spacing:.5px}}
  .meta{{font-family:{MONO};font-size:15px;fill:{MUTED}}}
  .rule{{stroke:{ACCENT};stroke-width:2;stroke-dasharray:260;animation:draw 1.4s .5s ease both}}
  @keyframes draw{{from{{stroke-dashoffset:260}}to{{stroke-dashoffset:0}}}}
  @media (prefers-reduced-motion: reduce){{*{{animation-play-state:paused!important}}.in,.rule{{animation:none!important}}}}
</style>
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
{''.join(field)}
<circle class="halo" cx="{cx}" cy="{cy}" r="{r + 40}" fill="url(#halo)"/>
<g>{''.join(sphere)}</g>
<text x="64" y="118" class="meta in" style="animation-delay:.05s">// hello, world — I'm</text>
<text x="60" y="186" class="name in" style="animation-delay:.2s">Felistas Charuka</text>
<line x1="64" y1="208" x2="324" y2="208" class="rule"/>
<text x="64" y="244" class="role in" style="animation-delay:.45s">Software Engineer · Full-Stack Web · IT Systems</text>
<text x="64" y="276" class="meta in" style="animation-delay:.7s">Harare, Zimbabwe  ·  B.Sc. Computer Science, University of Zimbabwe</text>
</svg>'''


def typing():
    """Cycling lines with a typewriter reveal (clip width animation) and a blinking caret."""
    W, H = 760, 44
    lines = [
        "I build web apps from first commit to production.",
        "Next.js · TypeScript · Laravel · FastAPI · MongoDB",
        "and I keep the systems behind them running.",
        "Open to Software Engineer &amp; IT Support roles.",
    ]
    per = 4.0
    total = per * len(lines)
    css, body = [], []
    for i, text in enumerate(lines):
        width = len(text.replace('&amp;', '&')) * 10 + 4
        s, e = i * per / total * 100, (i + 1) * per / total * 100
        a, b, c = s + 1.6 / total * 100, e - 0.9 / total * 100, e - 0.3 / total * 100
        css.append(
            f"@keyframes t{i}{{0%,{s:.2f}%{{width:0}}{a:.2f}%,{b:.2f}%{{width:{width:.0f}px}}{c:.2f}%,100%{{width:0}}}}"
            f"#c{i} rect{{animation:t{i} {total}s steps({len(text.replace('&amp;', '&'))}) infinite}}"
            f"@keyframes k{i}{{0%,{s:.2f}%{{transform:translateX(0)}}{a:.2f}%,{b:.2f}%{{transform:translateX({width:.0f}px)}}"
            f"{c:.2f}%,100%{{transform:translateX(0)}}}}"
            f"@keyframes v{i}{{0%,{s - 0.01 if s else 0:.2f}%{{opacity:0}}{s:.2f}%,{e - 0.01:.2f}%{{opacity:1}}{e:.2f}%,100%{{opacity:0}}}}"
            f".l{i}{{animation:v{i} {total}s step-end infinite}}"
            f".k{i}{{animation:k{i} {total}s steps({len(text.replace('&amp;', '&'))}) infinite}}")
        body.append(
            f'<clipPath id="c{i}"><rect x="20" y="0" height="{H}" width="0"/></clipPath>'
            f'<g class="l{i}"><text x="20" y="28" clip-path="url(#c{i})" textLength="{len(text.replace('&amp;', '&')) * 10}" lengthAdjust="spacingAndGlyphs">{text}</text>'
            f'<g class="k{i}"><rect x="21" y="12" width="2.5" height="21" class="caret"/></g></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{' '.join(lines)}">
<style>
  text{{font-family:{MONO};font-size:17px;fill:{ACCENT}}}
  .caret{{fill:{GLOW};animation:blink 1s step-end infinite}}
  @keyframes blink{{50%{{opacity:0}}}}
  {''.join(css)}
  @media (prefers-reduced-motion: reduce){{*{{animation:none!important}}.l0{{opacity:1}}#c0 rect{{width:{len(lines[0]) * 10 + 4:.0f}px}}}}
</style>
{''.join(body)}
</svg>'''


def footer():
    W, H = 1200, 90
    def wave(amp, phase, y0):
        pts = []
        for x in range(0, W * 2 + 1, 20):
            pts.append(f"{x},{y0 + amp * math.sin((x / W) * 4 * math.pi + phase):.1f}")
        return "M" + " L".join(pts) + f" L{W * 2},{H} L0,{H} Z"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" preserveAspectRatio="none">
<defs><linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient></defs>
<style>.w{{animation:slide linear infinite}}@keyframes slide{{to{{transform:translateX(-{W}px)}}}}{REDUCED}</style>
<path class="w" style="animation-duration:14s;opacity:.35" fill="{ACCENT}" d="{wave(9, 0, 38)}"/>
<path class="w" style="animation-duration:9s" fill="url(#f)" d="{wave(7, 1.6, 50)}"/>
</svg>'''


(OUT / "banner.svg").write_text(banner(), encoding="utf-8")
(OUT / "typing.svg").write_text(typing(), encoding="utf-8")
(OUT / "footer.svg").write_text(footer(), encoding="utf-8")
print("built", [p.name for p in OUT.iterdir()])
