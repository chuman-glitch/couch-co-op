"""Generates the Couch Co-Op living-room SVG and splices it into website/index.html."""
import math, random, sys

random.seed(7)
HTML = sys.argv[1]
o = []
A = o.append


def n(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def poly(pts, **kw):
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    return f'<polygon points="{" ".join(f"{n(x)},{n(y)}" for x, y in pts)}" {attrs}/>'


# ------------------------------------------------------------------ defs
DEFS = """
<defs>
  <linearGradient id="gWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e211d"/><stop offset=".6" stop-color="#46322a"/><stop offset="1" stop-color="#5a4034"/></linearGradient>
  <linearGradient id="gFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6750"/><stop offset=".45" stop-color="#6a4d3c"/><stop offset="1" stop-color="#3b2a22"/></linearGradient>
  <linearGradient id="gSunset" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe2ad"/><stop offset=".45" stop-color="#f7b072"/><stop offset=".8" stop-color="#d9765a"/><stop offset="1" stop-color="#9b4b45"/></linearGradient>
  <linearGradient id="gDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2246"/><stop offset=".7" stop-color="#3b3160"/><stop offset="1" stop-color="#5a3a55"/></linearGradient>
  <linearGradient id="gBeam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd59a" stop-opacity=".5"/><stop offset="1" stop-color="#ffd59a" stop-opacity="0"/></linearGradient>
  <linearGradient id="gPly" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c99b64"/><stop offset=".5" stop-color="#ddb47e"/><stop offset="1" stop-color="#c79a63"/></linearGradient>
  <linearGradient id="gPlyFront" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e7c28c"/><stop offset="1" stop-color="#c3955e"/></linearGradient>
  <radialGradient id="gPlyShade" cx=".5" cy=".45" r=".7"><stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#2a160b" stop-opacity=".45"/></radialGradient>
  <linearGradient id="gPipe" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8f8c87"/><stop offset=".4" stop-color="#e8e5df"/><stop offset="1" stop-color="#7d7a75"/></linearGradient>
  <linearGradient id="gSheer" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff6e8" stop-opacity=".22"/><stop offset=".3" stop-color="#fff6e8" stop-opacity=".42"/><stop offset=".55" stop-color="#fff6e8" stop-opacity=".2"/><stop offset=".8" stop-color="#fff6e8" stop-opacity=".45"/><stop offset="1" stop-color="#fff6e8" stop-opacity=".25"/></linearGradient>
  <linearGradient id="gCanopy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6ead6" stop-opacity=".95"/><stop offset="1" stop-color="#e4cfae" stop-opacity=".92"/></linearGradient>
  <linearGradient id="gVelvet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#868d58"/><stop offset=".35" stop-color="#5e6537"/><stop offset="1" stop-color="#363b1f"/></linearGradient>
  <radialGradient id="gSheen" cx=".25" cy=".15" r=".7"><stop offset="0" stop-color="#fff2cc" stop-opacity=".35"/><stop offset="1" stop-color="#fff2cc" stop-opacity="0"/></radialGradient>
  <radialGradient id="gRust" cx=".4" cy=".3" r=".8"><stop offset="0" stop-color="#d4643f"/><stop offset="1" stop-color="#8f3523"/></radialGradient>
  <radialGradient id="gMustard" cx=".4" cy=".3" r=".8"><stop offset="0" stop-color="#f0c060"/><stop offset="1" stop-color="#b6801f"/></radialGradient>
  <linearGradient id="gLeafA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8dbb62"/><stop offset="1" stop-color="#3f6e3a"/></linearGradient>
  <linearGradient id="gLeafB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6c9a4e"/><stop offset="1" stop-color="#2d5530"/></linearGradient>
  <linearGradient id="gMon" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5e9450"/><stop offset="1" stop-color="#244a2a"/></linearGradient>
  <radialGradient id="gGlobe" cx=".42" cy=".38" r=".62"><stop offset="0" stop-color="#fffbea"/><stop offset=".6" stop-color="#ffd890"/><stop offset="1" stop-color="#f0a250"/></radialGradient>
  <radialGradient id="gWarm"><stop offset="0" stop-color="#ffc979" stop-opacity=".8"/><stop offset=".45" stop-color="#ffb35c" stop-opacity=".25"/><stop offset="1" stop-color="#ffb35c" stop-opacity="0"/></radialGradient>
  <radialGradient id="gTvGlow"><stop offset="0" stop-color="#b9a6ff" stop-opacity=".55"/><stop offset=".5" stop-color="#9ec3ff" stop-opacity=".18"/><stop offset="1" stop-color="#9ec3ff" stop-opacity="0"/></radialGradient>
  <radialGradient id="gArtGlow"><stop offset="0" stop-color="#7fb2ff" stop-opacity=".5"/><stop offset="1" stop-color="#7fb2ff" stop-opacity="0"/></radialGradient>
  <linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#86c6ef"/><stop offset=".6" stop-color="#f5cfd6"/><stop offset="1" stop-color="#ffe0b0"/></linearGradient>
  <linearGradient id="gFall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8f3ff"/><stop offset="1" stop-color="#8ed0f5" stop-opacity=".2"/></linearGradient>
  <linearGradient id="gCeramic" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfc4b3"/><stop offset=".4" stop-color="#f3ece0"/><stop offset="1" stop-color="#b8ad9c"/></linearGradient>
  <linearGradient id="gTerracotta" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a5502f"/><stop offset=".4" stop-color="#d3784e"/><stop offset="1" stop-color="#8c4227"/></linearGradient>
  <linearGradient id="gWood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d5a56c"/><stop offset="1" stop-color="#9f7243"/></linearGradient>
  <pattern id="pBoucle" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="#fff" opacity=".18"/><circle cx="6" cy="6" r="1.1" fill="#000" opacity=".12"/></pattern>
  <pattern id="pCoir" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#b88d55"/><circle cx="1.5" cy="1.5" r="1" fill="#9c7440"/><circle cx="4.5" cy="4.5" r="1" fill="#cfa66c"/></pattern>
  <pattern id="pCork" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#bf9461"/><circle cx="3" cy="3" r="1.1" fill="#a87b4b"/><circle cx="8" cy="7" r=".9" fill="#d3a978"/></pattern>
  <filter id="fBlur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>
  <filter id="fBlurBig" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
  <filter id="fShadow" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#1a0d06" flood-opacity=".45"/></filter>
  <g id="leaf"><path d="M0 0 C 8 -12 26 -14 32 -2 C 28 10 12 14 0 0Z"/><path d="M1 0 Q 16 -3 30 -2" fill="none" stroke="#1d3a1d" stroke-opacity=".35" stroke-width="1"/></g>
  <mask id="monMask" maskUnits="userSpaceOnUse" x="-70" y="-60" width="140" height="120">
    <path d="M0 48 C -32 50 -64 18 -58 -12 C -52 -42 -22 -54 0 -40 C 22 -54 52 -42 58 -12 C 64 18 32 50 0 48Z" fill="#fff"/>
    <g stroke="#000" stroke-width="5" stroke-linecap="round">SLITS</g>
    <g fill="#000">HOLES</g>
  </mask>
  <g id="mon"><path mask="url(#monMask)" d="M0 48 C -32 50 -64 18 -58 -12 C -52 -42 -22 -54 0 -40 C 22 -54 52 -42 58 -12 C 64 18 32 50 0 48Z"/><path d="M0 46 Q 2 0 0 -38" fill="none" stroke="#a9cf86" stroke-opacity=".55" stroke-width="2"/></g>
</defs>
"""
slits, holes = [], []
for side in (-1, 1):
    for i, a in enumerate((-60, -30, 0, 28, 55)):
        ang = math.radians(a)
        dx, dy = side * math.cos(ang), math.sin(ang)
        r0, r1 = 66, 34 + (i % 2) * 6
        slits.append(f'<line x1="{n(dx*r0)}" y1="{n(dy*r0-4)}" x2="{n(dx*r1)}" y2="{n(dy*r1-4)}"/>')
    holes.append(f'<ellipse cx="{side*22}" cy="-6" rx="5" ry="3"/>')
    holes.append(f'<ellipse cx="{side*18}" cy="18" rx="4" ry="2.5"/>')
DEFS = DEFS.replace("SLITS", "".join(slits)).replace("HOLES", "".join(holes))
A(DEFS)


def leaf(x, y, rot, s, g="gLeafA"):
    return f'<use href="#leaf" transform="translate({n(x)} {n(y)}) rotate({n(rot)}) scale({n(s)})" fill="url(#{g})"/>'


def vine(x0, y0, length, amp=10, freq=0.035, side=1, scale=1.0):
    pts = []
    for i in range(0, int(length), 4):
        pts.append((x0 + math.sin(i * freq + x0) * amp, y0 + i))
    d = "M" + " L".join(f"{n(x)} {n(y)}" for x, y in pts)
    s = [f'<path d="{d}" fill="none" stroke="#3d5a31" stroke-width="1.6"/>']
    for k, (x, y) in enumerate(pts[2::4]):
        flip = 1 if k % 2 else -1
        rot = 90 + flip * random.uniform(35, 70)
        sc = scale * random.uniform(0.55, 0.85) * (1 - 0.25 * (y - y0) / length)
        s.append(leaf(x, y, rot, sc, "gLeafA" if k % 3 else "gLeafB"))
    return "".join(s)


def books(x, base, count, maxh=48):
    pal = ["#b8442e", "#e3c58f", "#4a5d7e", "#7a8a4f", "#d98b4a", "#efe4cf", "#5a3a2c", "#2f4a5e"]
    s, cx = [], x
    for i in range(count):
        w = random.randint(7, 13)
        h = random.randint(int(maxh * 0.7), maxh)
        c = random.choice(pal)
        s.append(f'<rect x="{cx}" y="{base-h}" width="{w}" height="{h}" fill="{c}"/>')
        s.append(f'<rect x="{cx}" y="{base-h+6}" width="{w}" height="2" fill="#fff" opacity=".25"/>')
        cx += w + 1
    return "".join(s)


def pot_plant(x, base, w=26, g="gTerracotta", leaves=7, spread=1.0):
    s = [f'<path d="M{x-w/2} {base-26} L{x+w/2} {base-26} L{x+w/2-4} {base} L{x-w/2+4} {base}Z" fill="url(#{g})"/>',
         f'<rect x="{x-w/2-2}" y="{base-29}" width="{w+4}" height="5" rx="2" fill="url(#{g})"/>']
    for i in range(leaves):
        a = -90 + (i - (leaves - 1) / 2) * 24 * spread + random.uniform(-6, 6)
        s.append(leaf(x, base - 28, a, random.uniform(0.75, 1.05), "gLeafA" if i % 2 else "gLeafB"))
    return "".join(s)


def sneaker(x, y, color, s=1.0, flip=False):
    tf = f"translate({n(x)} {n(y)}) scale({'-' if flip else ''}{n(s)} {n(s)})"
    return (f'<g transform="{tf}">'
            f'<path d="M2 -7 C 2 -22 12 -28 24 -28 L 32 -28 C 40 -20 50 -15 58 -11 L 60 -6 L 2 -6Z" fill="{color}"/>'
            f'<path d="M14 -27 C 18 -22 28 -21 32 -27" fill="#2a2421"/>'
            f'<g stroke="#fff" stroke-opacity=".7" stroke-width="1.5"><line x1="34" y1="-24" x2="38" y2="-19"/><line x1="38" y1="-21" x2="42" y2="-16"/></g>'
            f'<rect x="0" y="-7" width="62" height="8" rx="4" fill="#f4efe6"/><rect x="0" y="-1" width="62" height="2" rx="1" fill="#cfc6b8"/></g>')


# ------------------------------------------------------------------ room shell
A('<rect width="1600" height="612" fill="url(#gWall)"/>')
# concrete columns
A('<rect x="0" y="0" width="16" height="612" fill="#3a2b25"/>')
# left industrial window
A('<g id="winL"><rect x="24" y="58" width="208" height="520" fill="url(#gSunset)"/>')
A('<path d="M24 520 L24 470 L52 470 L52 440 L80 440 L80 486 L110 486 L110 420 L132 420 L132 400 L150 400 L150 455 L184 455 L184 478 L232 478 L232 578 L24 578Z" fill="#7a3d3c" opacity=".6"/>')
A('<rect class="night-only win-night" x="24" y="58" width="208" height="520" fill="url(#gDusk)"/>')
A('<g stroke="#241914" stroke-width="7">' + "".join(f'<line x1="{x}" y1="58" x2="{x}" y2="578"/>' for x in (24, 93, 163, 232))
  + "".join(f'<line x1="24" y1="{y}" x2="232" y2="{y}"/>' for y in (58, 145, 232, 319, 406, 493, 578)) + "</g></g>")
# right high window
A('<g id="winR"><rect x="1386" y="58" width="196" height="214" fill="url(#gSunset)"/><rect class="night-only win-night" x="1386" y="58" width="196" height="214" fill="url(#gDusk)"/>')
A('<g stroke="#241914" stroke-width="7">' + "".join(f'<line x1="{x}" y1="58" x2="{x}" y2="272"/>' for x in (1386, 1451, 1517, 1582))
  + "".join(f'<line x1="1386" y1="{y}" x2="1582" y2="{y}"/>' for y in (58, 165, 272)) + "</g></g>")
# floor
A('<rect y="610" width="1600" height="290" fill="url(#gFloor)"/>')
A('<rect y="608" width="1600" height="5" fill="#2a1d18" opacity=".6"/>')
# sun patch on floor + volumetric beam
A('<g class="day-only">')
A(poly([(232, 120), (232, 560), (820, 740), (820, 330)], fill="url(#gBeam)", opacity=".35"))
A(poly([(40, 615), (232, 615), (760, 900), (300, 900)], fill="#ffcf8f", opacity=".22", filter="url(#fBlur)"))
A("</g>")

# ------------------------------------------------------------------ the pop-up structure
# plywood back wall
A('<rect x="340" y="140" width="920" height="470" fill="url(#gPly)"/>')
for px in (570, 800, 1030):
    A(f'<line x1="{px}" y1="140" x2="{px}" y2="610" stroke="#a87c4b" stroke-width="2" opacity=".6"/>')
grain = []
for i in range(70):
    x = random.uniform(345, 1255)
    y = random.uniform(150, 600)
    L = random.uniform(30, 90)
    grain.append(f'M{n(x)} {n(y)} q {n(L/2)} {n(random.uniform(-4,4))} {n(L)} 0')
A(f'<path d="{" ".join(grain)}" fill="none" stroke="#9b6e3f" stroke-opacity=".18" stroke-width="1.4"/>')
A('<rect x="340" y="140" width="920" height="470" fill="url(#gPlyShade)"/>')

# inner scaffold posts
def pipe_v(x, y1, y2, w=8):
    return (f'<rect x="{x-w/2}" y="{y1}" width="{w}" height="{y2-y1}" fill="url(#gPipe)"/>')


def clamp(x, y):
    return f'<rect x="{x-8}" y="{y-6}" width="16" height="12" rx="3" fill="#77736d"/><circle cx="{x+6}" cy="{y}" r="2.5" fill="#5a5651"/>'


A(pipe_v(550, 140, 612, 7) + pipe_v(1050, 140, 612, 7))

# ---- hotspot: program board (left column)
A('<g class="hot" id="hs-program" data-panel="program" data-label="Program" tabindex="0" role="button" aria-label="Program board: events and what is on">')
A('<g filter="url(#fShadow)"><rect x="362" y="286" width="170" height="160" rx="3" fill="url(#pCork)" stroke="#6a4a2c" stroke-width="7"/></g>')
A('<rect x="376" y="300" width="62" height="78" fill="#f3ede2" transform="rotate(-3 407 339)"/>'
  '<g transform="rotate(-3 407 339)"><rect x="382" y="306" width="50" height="16" fill="#b8442e"/>'
  '<g stroke="#2a2421" stroke-opacity=".5" stroke-width="2"><line x1="382" y1="332" x2="430" y2="332"/><line x1="382" y1="340" x2="424" y2="340"/><line x1="382" y1="348" x2="428" y2="348"/><line x1="382" y1="356" x2="418" y2="356"/></g></g>')
A('<rect x="448" y="298" width="72" height="54" fill="#f0c060" transform="rotate(4 484 325)"/>'
  '<text x="484" y="330" text-anchor="middle" transform="rotate(4 484 325)" font-family="Unbounded, sans-serif" font-weight="900" font-size="12" fill="#2a2421">CO-OP</text>'
  '<text x="484" y="343" text-anchor="middle" transform="rotate(4 484 325)" font-family="Space Grotesk, sans-serif" font-weight="700" font-size="8" fill="#2a2421">NIGHT · FRI</text>')
A('<rect x="452" y="362" width="66" height="72" fill="#6f86b8" transform="rotate(-2 485 398)"/>'
  '<circle cx="485" cy="392" r="16" fill="#f3ede2" transform="rotate(-2 485 398)" opacity=".9"/>')
A('<rect x="380" y="388" width="60" height="48" fill="#f3ede2" transform="rotate(3 410 412)"/>'
  '<g transform="rotate(3 410 412)" fill="#b8442e"><circle cx="396" cy="410" r="5"/><circle cx="410" cy="410" r="5" fill="#f0c060"/><circle cx="424" cy="410" r="5" fill="#6f86b8"/></g>')
A('<g fill="#c0392b"><circle cx="407" cy="303" r="3.5"/><circle cx="484" cy="301" r="3.5"/><circle cx="485" cy="366" r="3.5"/><circle cx="410" cy="391" r="3.5"/></g>')
A('<rect class="hit" x="354" y="278" width="186" height="176" fill="transparent"/></g>')

# left shelf + cubby
A('<rect x="346" y="500" width="198" height="9" fill="url(#gPlyFront)"/><rect x="346" y="509" width="198" height="4" fill="#000" opacity=".2"/>')
A(books(356, 500, 9, 46))
A('<rect x="456" y="466" width="40" height="34" rx="3" fill="#2a2421"/><circle cx="486" cy="476" r="3" fill="#ffcf8a"/>')
A(pot_plant(520, 500, 22, "gCeramic", 6))
A('<g><path d="M360 600 L360 560 Q 360 548 372 548 L428 548 Q 440 548 440 560 L440 600Z" fill="#b38a55"/>'
  '<g stroke="#8a6436" stroke-width="2" opacity=".7">' + "".join(f'<line x1="360" y1="{y}" x2="440" y2="{y}"/>' for y in range(556, 600, 7)) + '</g>'
  '<path d="M452 600 L452 566 Q 452 556 462 556 L520 556 Q 530 556 530 566 L530 600Z" fill="#cfa86e"/>'
  '<g stroke="#a47e48" stroke-width="2" opacity=".7">' + "".join(f'<line x1="452" y1="{y}" x2="530" y2="{y}"/>' for y in range(564, 600, 7)) + '</g></g>')

# ---- hotspot: main screen
A('<g class="hot" id="hs-main" data-panel="featured" data-label="Featured screen" tabindex="0" role="button" aria-label="Featured screen: the main game on show">')
A('<ellipse cx="800" cy="335" rx="330" ry="200" fill="url(#gTvGlow)" class="glow"/>')
A('<g filter="url(#fShadow)"><rect x="575" y="205" width="450" height="262" rx="7" fill="#121012"/></g>')
A('<rect x="578" y="208" width="444" height="3" fill="#fff" opacity=".12"/>')
A('<svg id="tvScreen" x="585" y="215" width="430" height="242" viewBox="0 0 430 242" class="game">'
  '<rect width="430" height="242" fill="url(#gSky)"/>'
  '<circle class="sun" cx="330" cy="62" r="26" fill="#fff4cf"/>'
  '<g fill="#fff" opacity=".85"><ellipse cx="80" cy="50" rx="34" ry="10"/><ellipse cx="100" cy="44" rx="20" ry="10"/><ellipse cx="260" cy="36" rx="28" ry="8"/><ellipse cx="380" cy="110" rx="26" ry="7"/></g>'
  '<g fill="#c4b2e4" opacity=".7"><path d="M0 150 Q 40 120 80 140 Q 120 110 160 138 L160 160 L0 160Z"/><path d="M280 140 Q 330 112 380 132 Q 410 120 430 130 L430 160 L280 160Z"/></g>'
  '<path d="M40 150 Q 50 128 110 126 Q 170 124 185 150 Q 170 196 120 212 Q 70 196 40 150Z" fill="#c9805a"/>'
  '<path d="M40 150 Q 50 126 110 124 Q 170 122 185 150 Q 110 162 40 150Z" fill="#8cc76a"/>'
  '<path d="M250 160 Q 262 140 320 138 Q 378 140 392 162 Q 378 200 322 216 Q 266 200 250 160Z" fill="#c9805a"/>'
  '<path d="M250 160 Q 262 138 320 136 Q 378 138 392 162 Q 320 174 250 160Z" fill="#9ad277"/>'
  '<rect x="94" y="150" width="14" height="70" fill="url(#gFall)" opacity=".8"/>'
  '<path d="M180 146 Q 218 160 256 154" fill="none" stroke="#8a5a3a" stroke-width="3" stroke-dasharray="6 3"/>'
  '<g fill="#5a8a4a"><circle cx="70" cy="128" r="10"/><circle cx="78" cy="122" r="8" fill="#6fa257"/><rect x="72" y="132" width="3" height="10" fill="#7a5a3a"/>'
  '<circle cx="360" cy="140" r="9"/><rect x="359" y="146" width="3" height="8" fill="#7a5a3a"/></g>'
  '<g class="coins" fill="#ffd34d" stroke="#d9a520" stroke-width="1.5"><circle cx="210" cy="118" r="5"/><circle cx="228" cy="110" r="5"/><circle cx="246" cy="118" r="5"/></g>'
  '<g class="players"><ellipse cx="140" cy="132" rx="10" ry="11" fill="#f2b83f"/><circle cx="136" cy="130" r="1.8" fill="#2a2421"/><circle cx="143" cy="130" r="1.8" fill="#2a2421"/>'
  '<ellipse cx="164" cy="134" rx="9" ry="10" fill="#f7efe4"/><rect x="155" y="137" width="18" height="4" rx="2" fill="#c0442b"/><circle cx="161" cy="132" r="1.8" fill="#2a2421"/><circle cx="167" cy="132" r="1.8" fill="#2a2421"/></g>'
  '<g font-family="Space Grotesk, sans-serif" font-weight="700" font-size="10">'
  '<rect x="10" y="10" width="78" height="18" rx="9" fill="#000" opacity=".35"/><text x="49" y="23" text-anchor="middle" fill="#fff" letter-spacing="1">2P CO-OP</text>'
  '<rect x="10" y="212" width="66" height="20" rx="10" fill="#fff" opacity=".85"/><circle cx="21" cy="222" r="6" fill="#f2b83f"/><text x="32" y="226" fill="#2a2421">P1 ♥♥♥</text>'
  '<rect x="82" y="212" width="66" height="20" rx="10" fill="#fff" opacity=".85"/><circle cx="93" cy="222" r="6" fill="#f7efe4" stroke="#c0442b" stroke-width="2"/><text x="104" y="226" fill="#2a2421">P2 ♥♥♥</text>'
  '</g><rect width="430" height="242" fill="url(#gSheen)" opacity=".5"/></svg>')
A('<rect class="hit" x="565" y="195" width="470" height="282" fill="transparent"/></g>')

# right column: poster hotspot
A('<g class="hot" id="hs-poster" data-panel="publishers" data-label="For publishers" tabindex="0" role="button" aria-label="Poster: for publishers and game studios">')
A('<g filter="url(#fShadow)"><rect x="1096" y="174" width="140" height="160" fill="#3b2a20"/></g>')
A('<rect x="1104" y="182" width="124" height="144" fill="#f3ede2"/>')
A('<rect x="1112" y="190" width="108" height="72" fill="#b8442e"/>')
A('<g fill="#f3ede2"><circle cx="1144" cy="226" r="9"/><circle cx="1166" cy="226" r="9"/><circle cx="1188" cy="226" r="9"/></g>')
A('<text x="1166" y="284" text-anchor="middle" font-family="Unbounded, sans-serif" font-weight="900" font-size="14" fill="#1e1e1e">YOUR GAME</text>')
A('<text x="1166" y="302" text-anchor="middle" font-family="Unbounded, sans-serif" font-weight="900" font-size="14" fill="#1e1e1e">HERE</text>')
A('<text x="1166" y="318" text-anchor="middle" font-family="Space Grotesk, sans-serif" font-weight="700" font-size="7.5" fill="#4a1f1c" letter-spacing="1.2">PUBLISHER SHOWCASE</text>')
A('<rect class="hit" x="1088" y="166" width="156" height="176" fill="transparent"/></g>')

# right small shelf
A('<rect x="1058" y="372" width="196" height="8" fill="url(#gPlyFront)"/><rect x="1058" y="380" width="196" height="3" fill="#000" opacity=".2"/>')
A('<path d="M1076 372 C 1068 352 1076 336 1084 336 C 1092 336 1100 352 1092 372Z" fill="url(#gCeramic)"/>')
A(books(1104, 372, 4, 34))
A('<circle cx="1224" cy="356" r="15" fill="url(#gGlobe)"/><rect x="1216" y="369" width="16" height="4" fill="#b08a4a"/>')
A('<circle cx="1224" cy="356" r="40" fill="url(#gWarm)" class="lampglow"/>')

# ---- hotspot: side screen
A('<g class="hot" id="hs-side" data-panel="sidescreen" data-label="Side screen" tabindex="0" role="button" aria-label="Side screen: more games and interactive art">')
A('<ellipse cx="1160" cy="445" rx="140" ry="90" fill="url(#gArtGlow)" class="glow"/>')
A('<g filter="url(#fShadow)"><rect x="1078" y="394" width="164" height="100" rx="5" fill="#121012"/></g>')
A('<svg id="artScreen" x="1085" y="401" width="150" height="86" viewBox="0 0 150 86"><rect width="150" height="86" fill="#1c2242"/>'
  '<g class="art" style="transform-origin:75px 43px">'
  '<circle cx="75" cy="43" r="34" fill="none" stroke="#f0a24a" stroke-width="7" stroke-dasharray="30 12"/>'
  '<circle cx="75" cy="43" r="22" fill="none" stroke="#6f9cf0" stroke-width="7" stroke-dasharray="18 8"/>'
  '<circle cx="75" cy="43" r="10" fill="#e4553b"/></g>'
  '<g fill="#f3ede2" opacity=".7"><circle cx="18" cy="16" r="2"/><circle cx="130" cy="70" r="2.5"/><circle cx="128" cy="14" r="1.6"/></g></svg>')
A('<rect x="1100" y="494" width="10" height="10" fill="#2a2421"/><rect x="1210" y="494" width="10" height="10" fill="#2a2421"/>')
A('<rect class="hit" x="1070" y="386" width="180" height="120" fill="transparent"/></g>')
A('<rect x="1058" y="504" width="196" height="8" fill="url(#gPlyFront)"/><rect x="1058" y="512" width="196" height="3" fill="#000" opacity=".2"/>')
A('<path d="M1072 604 L1072 560 Q 1072 548 1084 548 L1150 548 Q 1162 548 1162 560 L1162 604Z" fill="#c09765"/>'
  '<g stroke="#8a6436" stroke-width="2" opacity=".7">' + "".join(f'<line x1="1072" y1="{y}" x2="1162" y2="{y}"/>' for y in range(556, 604, 7)) + '</g>')
A(books(1176, 604, 6, 52))

# ---- hotspot: consoles (media bench)
A('<g class="hot" id="hs-console" data-panel="setup" data-label="The setup" tabindex="0" role="button" aria-label="Console bench: how the room is set up">')
A('<rect x="560" y="598" width="480" height="14" fill="#ffcf8a" opacity=".7" filter="url(#fBlur)" class="lampglow"/>')
A(poly([(560, 492), (1040, 492), (1054, 506), (546, 506)], fill="#e9c995"))
A('<rect x="546" y="506" width="508" height="96" fill="url(#gPlyFront)"/>')
for (x1, x2) in ((562, 700), (716, 884), (900, 1038)):
    A(f'<rect x="{x1}" y="520" width="{x2-x1}" height="70" rx="2" fill="#5b3f27"/>')
    A(f'<rect x="{x1}" y="520" width="{x2-x1}" height="10" fill="#000" opacity=".25"/>')
A(books(572, 590, 9, 54))
A('<path d="M740 590 Q 740 560 770 560 L 860 560 Q 870 560 870 590Z" fill="#cfa86e"/><g stroke="#a47e48" stroke-width="2" opacity=".7">' + "".join(f'<line x1="742" y1="{y}" x2="868" y2="{y}"/>' for y in range(566, 590, 6)) + '</g>')
A('<g><rect x="912" y="560" width="40" height="30" rx="3" fill="#2a2421"/><circle cx="932" cy="575" r="8" fill="#3d3532"/><rect x="960" y="548" width="66" height="42" fill="#e3c58f"/><rect x="964" y="552" width="58" height="34" fill="#b8442e" opacity=".85"/></g>')
A('<rect x="634" y="474" width="92" height="20" rx="4" fill="#efe9df"/><rect x="634" y="474" width="92" height="4" rx="2" fill="#fff"/><circle cx="714" cy="484" r="2.6" fill="#7fe0a0" class="led"/>')
A('<rect x="868" y="472" width="100" height="22" rx="4" fill="#1d1b1c"/><rect x="868" y="472" width="100" height="3" rx="1.5" fill="#3a3637"/><circle cx="956" cy="483" r="2.6" fill="#7fb2ff" class="led"/>')
A('<path d="M680 494 C 690 560 730 610 770 640" stroke="#1d1b1c" stroke-width="2" fill="none"/><path d="M910 494 C 900 560 860 610 830 640" stroke="#1d1b1c" stroke-width="2" fill="none"/>')
A('<rect class="hit" x="540" y="462" width="520" height="150" fill="transparent"/></g>')
A(pot_plant(1022, 492, 26, "gCeramic", 8))
A('<rect x="566" y="472" width="22" height="20" rx="3" fill="#f3e2c2" opacity=".9"/><ellipse cx="577" cy="470" rx="16" ry="12" fill="url(#gWarm)" class="lampglow"/>')

# ------------------------------------------------------------------ structure front: posts, canopy, curtains, vines
# side curtains in perspective
A(poly([(250, 40), (340, 140), (340, 612), (250, 772)], fill="url(#gSheer)"))
A(poly([(1350, 40), (1260, 140), (1260, 612), (1350, 772)], fill="url(#gSheer)"))
A('<g stroke="#fff6e8" stroke-opacity=".22" stroke-width="2" fill="none">'
  + "".join(f'<path d="M{x} {40+(x-250)*1.1} Q {x+8} 400 {x-3} {772-(x-250)*1.75}"/>' for x in (268, 290, 312, 332))
  + "".join(f'<path d="M{1600-x} {40+(x-250)*1.1} Q {1600-x-8} 400 {1600-x+3} {772-(x-250)*1.75}"/>' for x in (268, 290, 312, 332)) + "</g>")
# back + front posts and beams
A(pipe_v(340, 140, 612) + pipe_v(1260, 140, 612))
A('<rect x="340" y="136" width="920" height="8" fill="url(#gPipe)"/>')
A('<line x1="250" y1="40" x2="340" y2="140" stroke="#bdb9b2" stroke-width="7"/><line x1="1350" y1="40" x2="1260" y2="140" stroke="#bdb9b2" stroke-width="7"/>')
# canopy (sheer fabric sagging from front beam to back beam)
A('<path d="M250 40 L1350 40 L1260 140 Q 800 222 340 140 Z" fill="url(#gCanopy)"/>')
A('<g stroke="#c9ad85" stroke-opacity=".55" stroke-width="2" fill="none">'
  + "".join(f'<path d="M{x} 40 Q {x + (800-x)*0.05} 120 {340 + (x-250)*0.836} {140 + 82*math.sin(math.pi*(x-250)/1100):.0f}"/>' for x in range(330, 1300, 90)) + "</g>")
A('<path d="M340 140 Q 800 222 1260 140" fill="none" stroke="#fff8ea" stroke-width="3" opacity=".6"/>')
A('<rect x="246" y="36" width="1108" height="9" fill="url(#gPipe)"/>')
A(pipe_v(250, 30, 772, 10) + pipe_v(1350, 30, 772, 10))
for (x, y) in ((250, 40), (1350, 40), (340, 140), (1260, 140), (550, 140), (1050, 140), (250, 330), (1350, 330)):
    A(clamp(x, y))
# vines from the canopy edge
A(vine(268, 60, 330, 8, 0.04, scale=1.1))
A(vine(300, 92, 250, 7, 0.05))
A(vine(1332, 60, 360, 8, 0.04, scale=1.1))
A(vine(1300, 92, 230, 7, 0.05))
A(vine(520, 44, 120, 5, 0.06, scale=0.9))
A(vine(1090, 44, 105, 5, 0.06, scale=0.9))

# paper lantern pendant
A('<line x1="440" y1="152" x2="440" y2="194" stroke="#2a2421" stroke-width="1.5"/>')
A('<circle cx="440" cy="230" r="90" fill="url(#gWarm)" class="lampglow"/>')
A('<ellipse cx="440" cy="230" rx="44" ry="37" fill="url(#gGlobe)"/>')
A('<g stroke="#d59a52" stroke-opacity=".5" stroke-width="1.3" fill="none">' + "".join(f'<ellipse cx="440" cy="{230+dy}" rx="{n(44*math.sqrt(max(0,1-(dy/37)**2)))}" ry="2.5"/>' for dy in range(-30, 34, 6)) + "</g>")
A('<rect x="432" y="190" width="16" height="6" rx="2" fill="#2a2421"/>')

# ---- hotspot: door (outside the structure)
A('<g class="hot" id="hs-door" data-panel="visit" data-label="Visit us" tabindex="0" role="button" aria-label="Door: how to find us at POST Houston">')
A('<rect x="1456" y="322" width="128" height="292" fill="#1d1411"/><rect x="1464" y="330" width="112" height="284" fill="#4a3329"/>')
A('<rect x="1476" y="344" width="88" height="120" fill="#ffcf8a" opacity=".22"/><rect x="1476" y="476" width="88" height="124" fill="#000" opacity=".12"/>')
A('<rect x="1552" y="470" width="6" height="26" rx="3" fill="#d9b27c"/>')
A('<rect x="1478" y="290" width="84" height="24" rx="3" fill="#b8442e"/><text x="1520" y="307" text-anchor="middle" font-family="Unbounded, sans-serif" font-weight="900" font-size="12" fill="#f3ede2" letter-spacing="1">POST</text>')
A('<rect class="hit" x="1448" y="282" width="144" height="336" fill="transparent"/></g>')

# ------------------------------------------------------------------ floor: rug, table, poufs
BL, BR, FR, FL = (440, 632), (1160, 632), (1336, 872), (264, 872)
A(poly([BL, BR, FR, FL], fill="#2a1a14", opacity=".35", filter="url(#fBlur)", transform="translate(0 8)"))
rows, cols = 7, 10
cells = []
for r in range(rows):
    t0, t1 = (r / rows) ** 1.3, ((r + 1) / rows) ** 1.3
    for c in range(cols):
        u0, u1 = c / cols, (c + 1) / cols
        L0, R0 = lerp(BL, FL, t0), lerp(BR, FR, t0)
        L1, R1 = lerp(BL, FL, t1), lerp(BR, FR, t1)
        pts = [lerp(L0, R0, u0), lerp(L0, R0, u1), lerp(L1, R1, u1), lerp(L1, R1, u0)]
        col = "#b44a31" if (r + c) % 2 else "#ead9bd"
        if (r * 3 + c * 7) % 11 == 0:
            col = "#c98b5a"
        cells.append(poly(pts, fill=col))
A("<g>" + "".join(cells) + "</g>")
A(poly([BL, BR, FR, FL], fill="url(#pBoucle)"))
A('<linearGradient id="gRugShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1a14" stop-opacity=".35"/><stop offset="1" stop-color="#2a1a14" stop-opacity="0"/></linearGradient>')
A(poly([BL, BR, FR, FL], fill="url(#gRugShade)"))
A(poly([BL, BR, FR, FL], fill="none", stroke="#f0e2c8", stroke_width="4", opacity=".8"))
A('<g stroke="#f0e2c8" stroke-width="2" opacity=".7">' + "".join(f'<line x1="{n(x)}" y1="872" x2="{n(x+random.uniform(-2,2))}" y2="881"/>' for x in [264 + i * 9 for i in range(120)]) + "</g>")
# light reflections on the floor
A('<rect x="600" y="614" width="400" height="20" rx="10" fill="#c9b2ff" opacity=".18" filter="url(#fBlur)"/>')

# coffee table
A('<ellipse cx="800" cy="676" rx="104" ry="14" fill="#1a0d06" opacity=".35" filter="url(#fBlur)"/>')
A('<path d="M700 650 L700 662 Q 800 684 900 662 L900 650Z" fill="#a1723f"/><ellipse cx="800" cy="650" rx="100" ry="18" fill="url(#gWood)"/>')
A('<ellipse cx="760" cy="646" rx="26" ry="7" fill="#e9dfcf"/><ellipse cx="760" cy="644" rx="20" ry="4" fill="#d1a14a"/>')
A('<path d="M820 650 q 6 -8 16 -6 q 10 -2 16 6 q -4 4 -16 3 q -12 1 -16 -3z" fill="#1d1b1c"/>')
A('<rect x="866" y="636" width="10" height="12" rx="2" fill="#f3e2c2"/><ellipse cx="871" cy="634" rx="12" ry="10" fill="url(#gWarm)" class="lampglow"/>')

# poufs (behind the couch)
def pouf(cx, cy, rx, h, g):
    return (f'<ellipse cx="{cx}" cy="{cy+h+4}" rx="{rx+6}" ry="10" fill="#1a0d06" opacity=".35" filter="url(#fBlur)"/>'
            f'<path d="M{cx-rx} {cy} L{cx-rx+4} {cy+h} Q {cx} {cy+h+18} {cx+rx-4} {cy+h} L{cx+rx} {cy}Z" fill="url(#{g})"/>'
            f'<path d="M{cx-rx} {cy} L{cx-rx+4} {cy+h} Q {cx} {cy+h+18} {cx+rx-4} {cy+h} L{cx+rx} {cy}Z" fill="url(#pBoucle)"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.32:.0f}" fill="url(#{g})"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.32:.0f}" fill="url(#pBoucle)"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.32:.0f}" fill="none" stroke="#000" stroke-opacity=".15" stroke-width="2"/>')


A(pouf(520, 668, 64, 34, "gRust"))
A(pouf(1090, 664, 58, 32, "gMustard"))

# ------------------------------------------------------------------ couch (hotspot)
A('<g class="hot" id="hs-couch" data-panel="dropin" data-label="Drop in · free play" tabindex="0" role="button" aria-label="Couch: drop in and play for free">')
A('<ellipse cx="800" cy="864" rx="350" ry="18" fill="#1a0d06" opacity=".5" filter="url(#fBlur)"/>')
# pillows peeking over the back
A('<rect x="566" y="672" width="92" height="50" rx="20" fill="url(#gRust)" transform="rotate(-9 612 697)"/>')
A('<circle cx="958" cy="694" r="26" fill="#e7a693"/><path d="M940 686 q 18 -12 36 4 M944 704 q 16 8 30 -6" stroke="#c5806d" stroke-width="3" fill="none"/>')
# arms
for x in (458, 1022):
    A(f'<rect x="{x}" y="728" width="120" height="132" rx="54" fill="url(#gVelvet)"/>')
    A(f'<rect x="{x}" y="728" width="120" height="132" rx="54" fill="url(#gSheen)"/>')
# base (seat block seen from behind)
A('<rect x="500" y="800" width="600" height="62" rx="24" fill="#3a3f22"/>')
A('<rect x="500" y="800" width="600" height="62" rx="24" fill="url(#gSheen)" opacity=".5"/>')
# three plush back cushions
for i, x in enumerate((506, 704, 902)):
    w = 192
    top = 700 + (4 if i == 1 else 0)
    A(f'<rect x="{x}" y="{top}" width="{w}" height="{830-top}" rx="46" fill="url(#gVelvet)"/>')
    for k in range(3):
        y = top + 34 + k * 30
        A(f'<path d="M{x+14} {y} Q {x+w/2} {y-9} {x+w-14} {y}" fill="none" stroke="#262a14" stroke-opacity=".5" stroke-width="3"/>')
        A(f'<path d="M{x+14} {y+4} Q {x+w/2} {y-5} {x+w-14} {y+4}" fill="none" stroke="#a2a970" stroke-opacity=".28" stroke-width="2"/>')
    A(f'<path d="M{x+30} {top+8} Q {x+w/2} {top-2} {x+w-30} {top+8}" fill="none" stroke="#c0c68e" stroke-opacity=".6" stroke-width="4" stroke-linecap="round"/>')
    A(f'<rect x="{x}" y="{top}" width="{w}" height="{830-top}" rx="46" fill="url(#gSheen)"/>')
# throw blanket draped over the right cushion
A('<clipPath id="cpThrow"><path d="M930 712 Q 1000 690 1080 712 Q 1086 760 1076 806 L 940 812 Q 926 760 930 712Z"/></clipPath>')
A('<g clip-path="url(#cpThrow)"><rect x="920" y="686" width="170" height="140" fill="#efe6d4"/>'
  '<g fill="#3557b0"><path d="M944 726 q 26 -16 42 8 q 8 24 -16 32 q -26 -8 -26 -40z"/><path d="M1010 742 q 34 -8 44 24 q -16 26 -44 10 q -12 -16 0 -34z"/><path d="M1040 704 q 20 0 24 18 l -26 8z"/></g>'
  '<path d="M930 712 Q 1000 690 1080 712" fill="none" stroke="#fff" stroke-width="6" opacity=".35"/>'
  '<rect x="920" y="686" width="170" height="140" fill="url(#gSheen)"/></g>')
A('<g stroke="#e6dac4" stroke-width="2">' + "".join(f'<line x1="{x}" y1="{n(806+ (x-940)*0.04)}" x2="{x}" y2="{n(816+(x-940)*0.04)}"/>' for x in range(942, 1076, 6)) + "</g>")
A('<rect class="hit" x="452" y="662" width="696" height="210" fill="transparent"/></g>')

# ------------------------------------------------------------------ foreground left: monstera, globe lamp, mat
# monstera
A('<ellipse cx="190" cy="846" rx="54" ry="10" fill="#1a0d06" opacity=".45" filter="url(#fBlur)"/>')
mon_leaves = [(112, 640, -40, 0.95), (196, 586, 4, 1.05), (282, 650, 42, 0.92), (88, 724, -68, 0.8), (276, 734, 64, 0.75), (168, 680, -14, 0.85)]
for (x, y, rot, s) in mon_leaves:
    a = math.radians(rot)
    bx, by = x + (-math.sin(a) * -48) * s, y + (math.cos(a) * 48) * s
    A(f'<path d="M190 790 Q {n((190+bx)/2 + (bx-190)*0.15)} {n((790+by)/2 + 10)} {n(bx)} {n(by)}" stroke="#3e6a35" stroke-width="3.5" fill="none"/>')
for i, (x, y, rot, s) in enumerate(mon_leaves):
    A(f'<use href="#mon" transform="translate({x} {y}) rotate({rot}) scale({s})" fill="url(#gMon)"/>')
A('<path d="M146 784 L234 784 L226 846 L154 846Z" fill="url(#gCeramic)"/><rect x="142" y="778" width="96" height="10" rx="4" fill="#e9e2d6"/>')

# ---- hotspot: globe floor lamp (lights)
A('<g class="hot" id="hs-lamp" data-action="lights" data-label="Lamp" tabindex="0" role="button" aria-label="Globe lamp: switch between golden hour and movie night" aria-pressed="false">')
A('<circle cx="385" cy="762" r="150" fill="url(#gWarm)" class="lampglow"/>')
A('<ellipse cx="385" cy="826" rx="70" ry="12" fill="#ffcf8a" opacity=".35" class="lampglow" filter="url(#fBlur)"/>')
A('<circle cx="385" cy="770" r="46" fill="url(#gGlobe)"/>')
A('<ellipse cx="372" cy="752" rx="16" ry="10" fill="#fff" opacity=".45"/>')
A('<path d="M366 812 L404 812 L410 826 L360 826Z" fill="#b08a4a"/>')
A('<rect class="hit" x="330" y="716" width="110" height="116" fill="transparent"/></g>')

# ---- hotspot: shoes off mat
A('<g class="hot" id="hs-shoes" data-panel="vision" data-label="Our vision" tabindex="0" role="button" aria-label="Doormat: shoes off. About Couch Co-Op">')
A(poly([(14, 846), (292, 846), (314, 898), (-6, 898)], fill="url(#pCoir)"))
A(poly([(14, 846), (292, 846), (314, 898), (-6, 898)], fill="none", stroke="#8c6535", stroke_width="3"))
A('<text x="152" y="888" text-anchor="middle" font-family="Unbounded, sans-serif" font-weight="900" font-size="17" fill="#3b2a20" letter-spacing="2">SHOES OFF</text>')
A(sneaker(28, 858, "#f3efe9", 0.8) + sneaker(52, 866, "#f3efe9", 0.8))
A(sneaker(118, 856, "#b8442e", 0.78) + sneaker(142, 864, "#b8442e", 0.78))
A('<path d="M214 862 q 0 -12 16 -12 h 28 q 10 0 10 12 z" fill="#6f86b8"/><rect x="210" y="860" width="62" height="6" rx="3" fill="#3e4c6e"/>')
A('<rect class="hit" x="0" y="800" width="316" height="100" fill="transparent"/></g>')

# ------------------------------------------------------------------ foreground right: side table (book), tree
A('<g class="hot" id="hs-book" data-panel="book" data-label="Book the room" tabindex="0" role="button" aria-label="Reserved sign: book the room">')
A('<ellipse cx="1246" cy="858" rx="64" ry="10" fill="#1a0d06" opacity=".45" filter="url(#fBlur)"/>')
A('<rect x="1236" y="762" width="20" height="94" fill="#8f6538"/><ellipse cx="1246" cy="856" rx="34" ry="6" fill="#8f6538"/>')
A('<path d="M1180 760 L1180 768 Q 1246 784 1312 768 L1312 760Z" fill="#a1723f"/><ellipse cx="1246" cy="760" rx="66" ry="15" fill="url(#gWood)"/>')
A(poly([(1204, 760), (1226, 712), (1270, 712), (1290, 760)], fill="#1e1e1e"))
A(poly([(1211, 756), (1230, 717), (1266, 717), (1283, 756)], fill="#f3ede2"))
A('<text x="1247" y="742" text-anchor="middle" font-family="Unbounded, sans-serif" font-weight="900" font-size="10" fill="#b8442e" letter-spacing=".5">RESERVE</text>')
A('<rect x="1186" y="740" width="16" height="18" rx="3" fill="#f3e2c2"/><path d="M1202 744 q 7 0 7 6 q 0 6 -7 6" fill="none" stroke="#f3e2c2" stroke-width="2.5"/>')
A('<rect class="hit" x="1172" y="700" width="150" height="168" fill="transparent"/></g>')
# small tree
A('<ellipse cx="1404" cy="874" rx="50" ry="9" fill="#1a0d06" opacity=".45" filter="url(#fBlur)"/>')
A('<path d="M1404 816 C 1400 760 1410 700 1398 620 M1402 720 C 1420 690 1440 676 1452 650 M1400 680 C 1380 660 1366 640 1360 610" stroke="#5a4130" stroke-width="3.5" fill="none"/>')
tree = []
for (cx, cy, r) in ((1398, 612, 46), (1450, 648, 36), (1360, 610, 34), (1420, 690, 28), (1380, 660, 30)):
    for _ in range(48):
        a = random.uniform(0, 2 * math.pi)
        d = random.uniform(0, r)
        x, y = cx + math.cos(a) * d, cy + math.sin(a) * d * 0.8
        tree.append(f'<ellipse cx="{n(x)}" cy="{n(y)}" rx="{n(random.uniform(5,8))}" ry="{n(random.uniform(3,4.5))}" transform="rotate({random.randint(0,180)} {n(x)} {n(y)})" fill="{random.choice(["#5e8f48", "#77a85a", "#3f6b37", "#8ab86a"])}"/>')
A("".join(tree))
A('<path d="M1370 812 L1438 812 L1430 874 L1378 874Z" fill="#2a2421"/><rect x="1366" y="806" width="76" height="9" rx="3" fill="#3a3330"/>')

# ------------------------------------------------------------------ overlays
A('<g id="markers" aria-hidden="true"></g>')
A('<rect id="veil" width="1600" height="900" fill="#0c0a16" opacity="0" pointer-events="none"/>')
A('<g id="nightglow" pointer-events="none">'
  '<ellipse cx="800" cy="340" rx="360" ry="250" fill="url(#gTvGlow)"/>'
  '<ellipse cx="800" cy="740" rx="300" ry="60" fill="url(#gTvGlow)" opacity=".35"/>'
  '<ellipse cx="1160" cy="445" rx="150" ry="100" fill="url(#gArtGlow)"/>'
  '<circle cx="440" cy="230" r="110" fill="url(#gWarm)"/><ellipse cx="440" cy="230" rx="44" ry="37" fill="url(#gGlobe)" opacity=".85"/>'
  '<circle cx="385" cy="770" r="170" fill="url(#gWarm)"/><circle cx="385" cy="770" r="46" fill="url(#gGlobe)" opacity=".85"/>'
  '<circle cx="1224" cy="356" r="50" fill="url(#gWarm)"/>'
  '<rect x="560" y="598" width="480" height="14" fill="#ffcf8a" opacity=".8" filter="url(#fBlur)"/>'
  '</g>')
A('<g id="nightscreens" pointer-events="none"><use href="#tvScreen"/><use href="#artScreen"/></g>')

scene = "\n".join(o)
html = open(HTML).read()
start = html.index('<svg class="scene"')
head_end = html.index(">", start) + 1
end = html.index("</svg>\n  </div>", start)
html = html[:head_end] + "\n" + scene + "\n  " + html[end:]
open(HTML, "w").write(html)
print("scene bytes", len(scene))
