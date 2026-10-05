"""Generates the animated SVGs used by the profile README (pure SVG + CSS, no JS, so GitHub renders them)."""
import base64
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
_font = lambda w: base64.b64encode((OUT / "fonts" / f"jbm-{w}.woff2").read_bytes()).decode()
# Embedded JetBrains Mono (subset): an <img> SVG cannot fetch web fonts, so the font travels inside the file.
FONTFACE = "".join(
    f"@font-face{{font-family:'JBM';font-weight:{w};src:url(data:font/woff2;base64,{_font(w)}) format('woff2')}}"
    for w in (400, 700))
CODE = "'JBM', " + MONO
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
    W, H = 640, 44
    lines = [
        "I build and ship full-stack web apps end to end",
        "and keep the infrastructure behind them running.",
        "Full-stack engineer · Next.js · TypeScript",
        "APIs in FastAPI &amp; Laravel, data in MongoDB &amp; MySQL",
        "Shipping to production on Vercel &amp; Render",
        "Cloud, networks &amp; systems that stay up",
    ]
    per = 4.0
    total = per * len(lines)
    css, body = [], []
    for i, text in enumerate(lines):
        width = len(text.replace('&amp;', '&')) * 10 + 4
        x0 = (W - width) / 2
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
            f'<clipPath id="c{i}"><rect x="{x0:.0f}" y="0" height="{H}" width="0"/></clipPath>'
            f'<g class="l{i}"><text x="{x0:.0f}" y="28" clip-path="url(#c{i})" textLength="{len(text.replace('&amp;', '&')) * 10}" lengthAdjust="spacingAndGlyphs">{text}</text>'
            f'<g class="k{i}"><rect x="{x0 + 1:.0f}" y="12" width="2.5" height="21" class="caret"/></g></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{' '.join(lines)}">
<style>
  {FONTFACE}
  text{{font-family:{CODE};font-size:17px;fill:{ACCENT}}}
  .caret{{fill:{GLOW};animation:blink 1s step-end infinite}}
  @keyframes blink{{50%{{opacity:0}}}}
  {''.join(css)}
  @media (prefers-reduced-motion: reduce){{*{{animation:none!important}}g[class^=l]{{opacity:0}}.caret{{display:none}}g.l0{{opacity:1}}#c0 rect{{width:{len(lines[0]) * 10 + 4:.0f}px}}}}
</style>
{''.join(body)}
</svg>'''


LINKEDIN_ICON = ("M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414"
                 "v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926"
                 "-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019"
                 "H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227"
                 " 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z")


def social(label, value, icon, tint, delay):
    """A pill button: tinted icon disc, small caps label over the value, and a light sweep along the border."""
    H, CW = 56, 8.4
    W = int(70 + len(value.replace('&amp;', '&')) * CW + 26)
    if icon == "linkedin":
        glyph = f'<g transform="translate(19 16) scale(1)"><path d="{LINKEDIN_ICON}" fill="#fff"/></g>'
    elif icon == "mail":
        glyph = ('<g transform="translate(18 18)" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round">'
                 '<rect x="1" y="2" width="24" height="17" rx="3"/><path d="M2 4l11 8 11-8"/></g>')
    else:  # status: pulsing dot
        glyph = ('<circle cx="31" cy="28" r="6" fill="#fff"/>'
                 '<circle cx="31" cy="28" r="6" fill="none" stroke="#fff" stroke-width="2" class="ping"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}: {value}">
<defs>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{tint}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
  <linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <clipPath id="pill"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="{H / 2 - 1}"/></clipPath>
</defs>
<style>
  {FONTFACE}
  .lbl{{font-family:{CODE};font-size:10.5px;letter-spacing:2px;fill:{MUTED}}}
  .val{{font-family:{CODE};font-size:14px;font-weight:700;fill:{INK}}}
  .sweep{{animation:sweep 5s ease-in-out {delay}s infinite both}}
  @keyframes sweep{{0%{{transform:translateX(-140px)}}35%,100%{{transform:translateX({W + 40}px)}}}}
  .ping{{transform-origin:31px 28px;animation:ping 1.8s ease-out infinite}}
  @keyframes ping{{from{{transform:scale(1);opacity:.9}}to{{transform:scale(2.4);opacity:0}}}}
  {REDUCED}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="{H / 2 - 1}" fill="{BG0}" stroke="url(#edge)" stroke-width="2"/>
<g clip-path="url(#pill)"><rect class="sweep" x="0" y="0" width="90" height="{H}" fill="url(#shine)" opacity=".08"/></g>
<circle cx="31" cy="28" r="20" fill="{tint}"/>
{glyph}
<text x="62" y="23" class="lbl">{label.upper()}</text>
<text x="62" y="41" class="val">{value}</text>
</svg>"""


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
(OUT / "social-linkedin.svg").write_text(social("LinkedIn", "in/felistas-charuka", "linkedin", "#0a66c2", 0), encoding="utf-8")
(OUT / "social-email.svg").write_text(social("Email", "felistas03charuka@gmail.com", "mail", "#c2410c", 1.2), encoding="utf-8")
(OUT / "social-status.svg").write_text(social("Status", "Open to SWE &amp; IT roles", "status", "#2f9e44", 2.4), encoding="utf-8")
(OUT / "footer.svg").write_text(footer(), encoding="utf-8")
print("built", [p.name for p in OUT.iterdir()])
