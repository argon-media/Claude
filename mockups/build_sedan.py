"""Generate an original vector mockup of a sport sedan (side profile).

Drawn from scratch as SVG -- no pixels from the reference photo are used and
no manufacturer logos or badges are included.  Usage:

    python3 build_sedan.py [body_hex] [out_basename]
"""
import math
import sys

W, H = 1600, 530
BODY = sys.argv[1] if len(sys.argv) > 1 else "#d8141a"
OUT = sys.argv[2] if len(sys.argv) > 2 else "sedan-side-red"

FW, RW, WY = 262, 1235, 400   # wheel centres
ARCH = 125


def shade(hex_color, f):
    """Lighten (f>0) or darken (f<0) a hex colour."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    if f >= 0:
        r, g, b = (c + (255 - c) * f for c in (r, g, b))
    else:
        r, g, b = (c * (1 + f) for c in (r, g, b))
    return "#%02x%02x%02x" % (round(r), round(g), round(b))


def arch_x(cx):
    dx = math.sqrt(ARCH ** 2 - 30 ** 2)
    return cx - dx, cx + dx


fl, fr = arch_x(FW)
rl, rr = arch_x(RW)

body = (
    f"M 62,428 L 46,336 C 44,288 70,246 130,222 "
    f"C 220,190 350,168 470,160 L 525,152 "
    f"C 600,100 670,56 745,42 C 860,22 1010,20 1115,40 "
    f"C 1205,62 1300,106 1385,130 L 1500,136 L 1522,148 "
    f"C 1532,190 1532,240 1546,298 L 1556,350 C 1558,385 1548,420 1522,432 "
    f"L {rr:.0f},432 A {ARCH} {ARCH} 0 1 0 {rl:.0f},432 "
    f"L {fr:.0f},440 A {ARCH} {ARCH} 0 1 0 {fl:.0f},432 Z"
)

glass = ("M 548,188 C 615,122 690,74 768,60 C 885,46 1010,48 1108,62 "
         "C 1180,84 1232,118 1256,150 L 1215,168 L 568,192 Z")


def wheel(cx, cy):
    parts = [
        f'<circle cx="{cx}" cy="{cy}" r="110" fill="#111"/>',
        f'<circle cx="{cx}" cy="{cy}" r="104" fill="none" stroke="#2a2a2a" stroke-width="4"/>',
        f'<circle cx="{cx}" cy="{cy}" r="82" fill="#1b1b1d"/>',
        # brake disc + caliper
        f'<circle cx="{cx}" cy="{cy}" r="60" fill="#3a3a3c"/>',
        f'<path d="M {cx - 58},{cy - 30} A 66 66 0 0 0 {cx - 58},{cy + 30} '
        f'L {cx - 44},{cy + 22} A 50 50 0 0 1 {cx - 44},{cy - 22} Z" fill="#c9a227"/>',
    ]
    spokes = []
    for i in range(10):
        a = math.radians(i * 36 - 90)
        for off in (-0.07, 0.07):
            x1 = cx + 18 * math.cos(a + off * 3)
            y1 = cy + 18 * math.sin(a + off * 3)
            x2 = cx + 80 * math.cos(a + off)
            y2 = cy + 80 * math.sin(a + off)
            spokes.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    parts.append('<g stroke="#2b2b2e" stroke-width="7" stroke-linecap="round">'
                 + "".join(spokes) + "</g>")
    parts += [
        f'<circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="#2f2f32" stroke-width="3"/>',
        f'<circle cx="{cx}" cy="{cy}" r="20" fill="#2b2b2e"/>',
        f'<circle cx="{cx}" cy="{cy}" r="9" fill="#55575c"/>',
    ]
    return "\n".join(parts)


svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="paint" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{shade(BODY, 0.18)}"/>
    <stop offset="0.38" stop-color="{shade(BODY, 0.05)}"/>
    <stop offset="0.55" stop-color="{BODY}"/>
    <stop offset="1" stop-color="{shade(BODY, -0.35)}"/>
  </linearGradient>
  <linearGradient id="shoulder" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#fff" stop-opacity="0.22"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1c1d20"/>
    <stop offset="1" stop-color="#050506"/>
  </linearGradient>
  <radialGradient id="shadow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#000" stop-opacity="0.45"/>
    <stop offset="1" stop-color="#000" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="bodyClip"><path d="{body}"/></clipPath>
</defs>

<ellipse cx="800" cy="505" rx="780" ry="22" fill="url(#shadow)"/>

<!-- wheel wells -->
<clipPath id="wellClip"><rect x="0" y="0" width="{W}" height="442"/></clipPath>
<g clip-path="url(#wellClip)" fill="#0a0a0b">
  <circle cx="{FW}" cy="{WY}" r="{ARCH}"/>
  <circle cx="{RW}" cy="{WY}" r="{ARCH}"/>
</g>

<!-- body -->
<path d="{body}" fill="url(#paint)"/>
<g clip-path="url(#bodyClip)">
  <!-- shoulder highlight -->
  <path d="M 120,236 C 500,200 1000,176 1530,170 L 1530,250 C 1000,250 500,262 120,282 Z" fill="url(#shoulder)"/>
  <!-- hood sheen -->
  <path d="M 110,232 C 220,196 360,176 470,166 L 470,176 C 340,190 220,214 120,250 Z" fill="#fff" opacity="0.18"/>
  <!-- lower body crease -->
  <path d="M 380,370 C 700,360 900,356 1120,350" stroke="{shade(BODY, -0.3)}" stroke-width="2" fill="none" opacity="0.6"/>
  <!-- carbon roof -->
  <path d="M 700,56 C 860,26 1010,24 1115,40 C 1205,62 1300,106 1385,130 L 1378,138 C 1290,114 1200,74 1110,52 C 1005,36 860,38 700,64 Z" fill="#141416"/>
  <!-- side skirt -->
  <path d="M {fr:.0f},418 L {rl:.0f},414 L {rl:.0f},440 L {fr:.0f},446 Z" fill="#141416"/>
  <!-- rear diffuser / bumper lower -->
  <path d="M {rr - 5:.0f},405 L 1556,385 L 1556,440 L {rr - 5:.0f},440 Z" fill="#141416"/>
  <!-- front splitter + intake -->
  <path d="M 40,330 C 60,334 82,340 96,352 L 100,410 L 40,416 Z" fill="#141416"/>
  <path d="M 40,420 L 150,416 L 150,440 L 40,440 Z" fill="#101012"/>
</g>

<!-- glass + pillars -->
<path d="{glass}" fill="url(#glass)"/>
<path d="M 862,52 L 895,50 L 878,184 L 846,186 Z" fill="#0b0b0c"/>
<path d="M 1098,60 L 1112,62 L 1112,172 L 1100,172 Z" fill="#2a2b2e"/>
<path d="M 548,188 L 568,192 L 1215,168 L 1256,150 L 1260,158 L 1218,176 L 566,200 Z" fill="#0d0d0f"/>
<path d="M 600,140 C 660,96 720,72 780,64" stroke="#fff" stroke-opacity="0.08" stroke-width="10" fill="none"/>

<!-- panel seams -->
<g fill="none" stroke="{shade(BODY, -0.45)}" stroke-width="2.2">
  <path d="M 492,196 C 486,260 488,340 498,418"/>
  <path d="M 880,186 C 872,260 862,340 858,414"/>
  <path d="M 1215,176 C 1195,236 1172,276 1150,302"/>
</g>

<!-- door handles -->
<rect x="764" y="214" width="74" height="16" rx="8" fill="{shade(BODY, -0.2)}"/>
<rect x="766" y="216" width="70" height="7" rx="3.5" fill="{shade(BODY, 0.25)}" opacity="0.7"/>
<rect x="1090" y="198" width="74" height="16" rx="8" fill="{shade(BODY, -0.2)}"/>
<rect x="1092" y="200" width="70" height="7" rx="3.5" fill="{shade(BODY, 0.25)}" opacity="0.7"/>

<!-- mirror -->
<path d="M 560,186 L 572,160 L 600,158 L 600,190 Z" fill="#111"/>
<path d="M 568,152 C 575,140 610,138 626,148 L 628,176 C 612,186 580,188 568,180 Z" fill="url(#paint)"/>
<path d="M 572,150 C 590,142 612,142 624,150" stroke="#fff" stroke-opacity="0.5" stroke-width="2" fill="none"/>

<!-- fender vent (unbadged) -->
<path d="M 404,288 L 448,246 L 480,244 L 434,318 Z" fill="#1a1a1c"/>
<path d="M 420,286 L 452,254" stroke="#3a3a3e" stroke-width="2"/>

<!-- headlight -->
<path d="M 72,268 C 100,256 140,252 172,258 L 160,284 C 128,292 98,298 76,300 Z" fill="#0f1116"/>
<path d="M 86,280 C 110,272 136,268 156,268" stroke="#9fb4d8" stroke-width="2.5" fill="none" opacity="0.8"/>
<!-- side marker -->
<rect x="128" y="352" width="6" height="56" rx="3" fill="#c98410" opacity="0.85"/>

<!-- tail light -->
<path d="M 1428,196 L 1510,188 C 1520,196 1522,222 1516,240 L 1468,236 Z" fill="#3a0608"/>
<path d="M 1440,204 L 1506,198" stroke="#ff3b3b" stroke-width="3" opacity="0.8"/>
<!-- boot spoiler -->
<path d="M 1420,134 L 1500,134 L 1524,146 L 1440,146 Z" fill="#141416"/>

<!-- wheels -->
{wheel(FW, WY)}
{wheel(RW, WY)}
</svg>
'''

with open(f"{OUT}.svg", "w") as fh:
    fh.write(svg)
print(f"wrote {OUT}.svg")
