"""Builds website/concept.html: the collage design study.
Transparent cut-outs (website/concept/cut/*.png) on a quiet line drawing of the POST atrium.
Some pieces carry a hand-drawn layer that draws itself on hover.
Run:  python3 tools/build_concept.py
Edit PIECES to move (at) / scale (s, sy) / rotate (r) a cut-out; TAGS for the paper labels."""
import math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "website", "index.html")
V1 = open(os.path.join(ROOT, "website", "archive", "index-v1.html")).read()
WINDOWS = open(os.path.join(ROOT, "tools", "windows.html")).read()   # the pop-up windows (edit here)
BACKDROP = "concept/backdrop-lite.jpg"
VW, VH = 2000, 1333

def P(name, w, h):
    return (f"concept/cut/{name}.png", (w, h))

SOFA_G = P("sofa-green", 1100, 550)
LOVESEAT = P("loveseat", 1100, 584)
TABLE = P("coffee-table", 1100, 550)
OXBLOOD = P("table-oxblood", 1100, 733)
FIG = P("fig", 733, 1100)
RUG_MOSS = P("rug-moss", 1100, 668)
RUG_ROSE = P("rug-rose", 1100, 619)
RUG_OLIVE = P("rug-olive", 1100, 703)
PERSON = P("person-reading", 820, 584)
CANDLES = ("concept/p-candles.jpg", (1000, 1028))   # not transparent: clipped by the outlines below

# ---- v5 "internet core" set: industrial DIY lounge cut-outs (concept/cut2) ----
def Q(name, w, h):
    return (f"concept/cut2/{name}.png", (w, h))
FLOOR_SOFA = Q("floor-sofa", 900, 407)
TOGO = Q("togo", 900, 522)
TOGO_CHAIR = Q("togo-chair", 900, 615)
BLOB = Q("blob", 823, 420)
POUF = Q("pouf", 900, 538)
MAHJONG = Q("mahjong", 900, 283)
CRT_BLOCKS = Q("crt-blocks", 900, 635)
CRT_CAM = Q("crt-cam", 688, 900)
CRT_STACK = Q("crt-stack", 539, 900)
LAMP = Q("clamp-lamp", 657, 900)
KILIM = Q("kilim", 856, 900)
RUNNER = Q("runner", 505, 900)
RUGS = Q("rugs", 900, 754)
CURTAIN_O = Q("curtain-orange", 596, 900)
PANELS = Q("panels", 840, 900)
RACK = Q("rack", 714, 900)
WAVY = Q("screen-wavy", 689, 900)
STEEL = Q("steel-panel", 332, 900)
PIPES = Q("pipes", 600, 900)
LANTERNS = Q("lanterns", 621, 788)
MUSHROOM = Q("lamp-mushroom", 398, 900)
RACK_F = Q("rack-forest", 569, 900)

# CRT screens inside the cut-outs (cut-out pixels) and the render footage they loop
TV_BLOCKS = [([(22,148),(168,148),(165,256),(25,256)], ["tv4", "tv1"]),
             ([(355,48),(545,48),(545,186),(355,186)], ["tv2", "tv6", "tv3"]),
             ([(667,160),(815,160),(813,262),(668,262)], ["tv5", "tv3"])]
TV_STACK = [([(305,20),(410,20),(410,118),(305,118)], ["tv6", "tv4"]),
            ([(318,165),(462,170),(460,325),(318,320)], ["tv1", "tv5"]),
            ([(210,375),(490,375),(490,580),(210,580)], ["tv3", "tv2", "tv6"]),
            ([(337,628),(505,612),(505,855),(337,850)], ["tv4", "tv1"])]
TV_CAM = [([(196,240),(622,230),(622,632),(200,648)], ["tv5", "tv2"])]
TV_RACK = [([(108,140),(498,140),(498,548),(108,548)], ["tv1", "tv3", "tv2", "tv6"])]

def tv_markup(i, screens):
    """Footage from the renders, clipped into each CRT, with scanlines and a glass sheen."""
    out = []
    for k, (pts, slides) in enumerate(screens):
        xs = [x for x, _ in pts]; ys = [y for _, y in pts]
        x0, y0, w, h = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
        poly = " ".join(f"{x},{y}" for x, y in pts)
        n = len(slides); per = 2.6 * n; off = (i * 1.7 + k * 1.1) % per
        imgs = "".join(
            f'<image class="{"slide" if j else "base"}" style="animation-duration:{per:.1f}s;animation-delay:{-((per - 2.6 * j + off) % per):.1f}s" '
            f'href="concept/tv/{sl}.jpg" x="{x0}" y="{y0}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>'
            for j, sl in enumerate(slides)) if n > 1 else \
            f'<image href="concept/tv/{slides[0]}.jpg" x="{x0}" y="{y0}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>'
        out.append(f'<defs><clipPath id="tv{i}_{k}"><polygon points="{poly}"/></clipPath></defs>'
                   f'<g class="tv" clip-path="url(#tv{i}_{k})">{imgs}'
                   f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#tvscan)"/>'
                   f'<rect class="sheen" x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#sheen)"/></g>')
    return "".join(out)

# ---- three ceramic candle holders (outlines in the candle photo's pixels) ----
HOLDER_BLUE = [(190,118),(225,110),(300,125),(355,128),(325,148),(322,200),(318,250),(300,280),(288,300),(285,345),(345,352),(330,362),(295,365),(300,395),(320,435),(322,470),(308,500),(300,530),(305,550),(345,565),(370,575),(362,590),(320,600),(312,640),(315,760),(325,820),(350,840),(430,850),(465,870),(462,900),(430,915),(300,925),(150,928),(40,915),(25,890),(40,860),(120,845),(205,840),(230,800),(235,700),(238,600),(195,590),(150,580),(142,560),(160,545),(200,560),(240,540),(245,520),(230,500),(222,465),(232,430),(250,395),(255,365),(210,362),(205,350),(255,343),(255,300),(240,280),(225,250),(218,190),(212,140)]
HOLDER_BROWN = [(310,512),(360,505),(430,515),(510,512),(540,522),(505,540),(492,560),(488,610),(470,650),(450,680),(445,700),(465,740),(470,790),(458,830),(445,860),(455,900),(560,920),(605,940),(610,975),(580,1000),(450,1012),(300,1010),(215,995),(208,960),(230,935),(300,915),(395,900),(405,860),(395,835),(368,810),(360,760),(378,725),(400,700),(398,670),(370,640),(350,590),(345,545),(330,530)]
HOLDER_CREAM = [(685,262),(720,255),(790,262),(845,265),(875,270),(845,282),(840,320),(830,360),(805,385),(795,410),(805,445),(820,480),(810,520),(795,545),(790,600),(830,610),(870,625),(865,645),(830,652),(810,670),(812,760),(825,820),(860,850),(950,870),(985,895),(980,925),(940,945),(800,952),(660,950),(600,935),(560,915),(570,895),(620,880),(710,860),(740,820),(750,700),(752,660),(715,652),(682,645),(680,628),(720,615),(760,600),(758,555),(742,525),(728,490),(738,450),(752,420),(750,385),(730,365),(718,320),(712,282)]

# ================= hand-drawn layers (draw themselves on hover) =================
def strokes(lst):
    return "".join(f'<path class="ln" pathLength="1" style="--d:{d:.2f}s" d="{p}"/>' for d, p in lst)

def candle_doodle(cx, top, h, w, d):
    """A candle in a holder cup: body, drip, wick, flickering flame, glow, rays (candle-photo pixels)."""
    x0, x1, t = cx - w / 2, cx + w / 2, top - h
    fy, fcx, fcy = t - 14, cx + 1, t - 50
    body = (f'M{x0:.0f} {top} L{x0 + 2:.0f} {t + 8} Q{x0 + 4:.0f} {t - 1} {cx - 3:.0f} {t + 3} '
            f'Q{cx + 4:.0f} {t + 12} {cx + 7:.0f} {t + 2} Q{x1 - 2:.0f} {t - 2} {x1 - 1:.0f} {t + 8} L{x1:.0f} {top}')
    flame = (f'M{fcx} {fy} C {fcx - 22} {fy - 14} {fcx - 15} {fy - 52} {fcx} {fy - 88} '
             f'C {fcx + 17} {fy - 52} {fcx + 23} {fy - 14} {fcx} {fy}Z')
    inner = (f'M{fcx} {fy - 4} C {fcx - 10} {fy - 12} {fcx - 7} {fy - 32} {fcx} {fy - 50} '
             f'C {fcx + 8} {fy - 32} {fcx + 11} {fy - 12} {fcx} {fy - 4}Z')
    rays = ""
    for k, a in enumerate((-160, -125, -90, -55, -20)):
        r0, r1 = 78, 112 if k % 2 else 98
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        rays += (f'<path class="ln ray" pathLength="1" style="--d:{d + 0.95 + k * 0.05:.2f}s" '
                 f'd="M{fcx + ca * r0:.0f} {fcy + sa * r0:.0f} L{fcx + ca * r1:.0f} {fcy + sa * r1:.0f}"/>')
    return (f'<circle class="gl" style="--d:{d:.2f}s" cx="{fcx}" cy="{fcy}" r="190" fill="url(#candleglow)"/>'
            + strokes([(d, body), (d + 0.35, f'M{x1 - 3:.0f} {t + 12} q 6 20 -1 38'), (d + 0.45, f'M{cx} {t + 2} q -4 -8 1 -16')])
            + f'<g class="fl" style="--d:{d:.2f}s"><path class="f" d="{flame}"/><path class="fi" d="{inner}"/></g>' + rays)

CANDLE_DOODLE = candle_doodle(272, 128, 230, 30, 0.0) + candle_doodle(425, 515, 170, 34, 0.18) + candle_doodle(780, 264, 210, 30, 0.36)

def lamp_doodle():
    """Clamp lamp: a soft pool of light that comes on with it (no drawn lines)."""
    return '<ellipse class="gl" style="--d:0s" cx="470" cy="1000" rx="520" ry="380" fill="url(#candleglow)"/>'

# ============================ the collage ============================
# drawn in order (back to front). id=None → decoration. png → transparent cut-out; polys → clipped photo.
# sy squashes a piece vertically (rugs lying on the floor); dfit=(fx,fy,tx,ty,k) fits a doodle onto a piece.
TOWER = ("concept/render/tower.jpg", (822, 806))
# outline in tower.jpg pixels (render x1030–2400 × 0.6)
TOWER_POLY = [(282,0),(609,0),(609,806),(262,806),(262,228),(264,99),(282,90)]
# the render's two real screens, in the same pixels: (id, corners, angle, slides, kicker, lines, size)
SCREENS = [
  ("publishers", [(279,316),(426,277),(429,468),(280,474)], -14, ["slide1", "slide2", "slide3"], "FEATURED SCREEN", ["YOUR GAME", "HERE"], 16),
  ("sidescreen", [(271,98),(435,38),(457,196),(293,229)], -20, ["slide4"], "ALSO", ["PLAYING"], 22),
]

def screens_markup():
    out = []
    for k, (sid, pts, ang, slides, kicker, lines, size) in enumerate(SCREENS):
        xs = [x for x, _ in pts]; ys = [y for _, y in pts]
        x0, y0, w, h = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
        cx, cy = x0 + w / 2, y0 + h / 2
        poly = " ".join(f"{x},{y}" for x, y in pts)
        n = len(slides); period = 3 * n
        imgs = "".join(
            f'<image{' class="slide"' if n > 1 else ""} style="animation-duration:{period}s;animation-delay:{-(period - 3 * j) % period}s" '
            f'href="concept/render/{sl}.jpg" x="{x0}" y="{y0}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>'
            for j, sl in enumerate(slides))
        lh = size * 1.05
        ty = -(len(lines) - 1) * lh / 2 + size * 0.35
        text = f'<text class="st-k" y="{ty - size * 1.1:.1f}" text-anchor="middle" style="font-size:{size * .32:.1f}px">{kicker}</text>'
        text += "".join(f'<text class="st-t" y="{ty + i * lh:.1f}" text-anchor="middle" style="font-size:{size}px">{ln}</text>' for i, ln in enumerate(lines))
        out.append(
            f'<defs><clipPath id="scr{k}"><polygon points="{poly}"/></clipPath></defs>'
            f'<g class="piece screen" data-id="{sid}" data-open="{sid}" tabindex="0" role="button" aria-label="{NUMS[sid]} {TITLES[sid]}">'
            f'<g clip-path="url(#scr{k})">{imgs}</g>'
            f'<g class="flip"><polygon class="blue" points="{poly}"/>'
            f'<g transform="translate({cx:.0f} {cy:.0f}) rotate({ang})">{text}</g></g>'
            f'<polygon class="bezel" points="{poly}"/></g>')
    return "".join(out)

PIECES = [
  # back: pipe scaffold + a rack with a big screen (right); a stainless panel and a wavy steel screen (left)
  dict(id=None,     src=PIPES,     at=(1900,520),  s=0.75, r=0, thin=True),
  dict(id=None,     src=RACK_F,    at=(1690,640),  s=0.62, r=0, thin=True, tv=TV_RACK),
  dict(id=None,     src=LANTERNS,  at=(150,640),   s=0.55, r=0),
  # floor: rugs
  dict(id="setup",  src=KILIM,     at=(1010,1170), s=1.05, sy=0.42, r=-3, flat=True),
  dict(id="vision", src=RUGS,      at=(1640,1215), s=0.62, sy=0.5, r=4, flat=True),
  # the scaffold tower from the render with its two live screens
  dict(id=None,     src=TOWER, polys=[TOWER_POLY], at=(1000,640), s=1.08, r=0, screens=True),
  # LAN corner: CRTs on cinderblocks, a CRT stack, all playing footage from the renders
  dict(id="program", src=CRT_BLOCKS, at=(1450,900), s=0.48, r=0, tv=TV_BLOCKS),
  dict(id=None,     src=MUSHROOM,  at=(330,960),   s=0.36, r=0),
  # front: one floor sofa, one lounge chair, one pouf
  dict(id="dropin", src=FLOOR_SOFA, at=(640,1050), s=0.7,  r=-2),
  dict(id="book",   src=TOGO,      at=(1300,1060), s=0.52, r=3),
  dict(id="visit",  src=CRT_CAM,   at=(200,1080),  s=0.36, r=-3, tv=TV_CAM),
  dict(id=None,     src=POUF,      at=(990,1195),  s=0.34, r=-1),
  # a clamp lamp hung off the rack: the light switch
  dict(id=None,     src=LAMP,      at=(1520,300),  s=0.3,  r=0),
]


# blue stickers: screens hung on the crossed staircases
STICKERS = []
_OLD_STICKERS = [
  dict(id="publishers", pts=[(838,492),(1162,480),(1168,694),(844,706)], at=(1003,593), rot=-2, kicker="FEATURED SCREEN", lines=["YOUR GAME", "HERE"], size=40, cords=True),
  dict(id="sidescreen", pts=[(1488,690),(1630,698),(1626,792),(1484,786)], at=(1557,744), rot=3, kicker="ALSO", lines=["PLAYING"], size=20),
]

TAGS = [  # numbered as a path: front row L→R, back along the floor R→L, then up the back wall
  dict(id="dropin",     num="01", text="drop in · play", at=(360,830),   to=(560,930),   rot=0),
  dict(id="book",       num="02", text="book the room",  at=(1080,870),  to=(1250,955),  rot=0),
  dict(id="program",    num="03", text="snacks & nights", at=(1460,690), to=(1450,770),  rot=0),
  dict(id="vision",     num="04", text="shoes off",      at=(1700,1110), to=(1680,1200), rot=0),
  dict(id="setup",      num="05", text="the setup",      at=(1150,1232), to=(1215,1200), rot=0),
  dict(id="visit",      num="06", text="live cam · visit", at=(300,1232), to=(240,1215), rot=0),
  dict(id="publishers", num="07", text="for publishers", at=(1250,600),  to=(1015,620),  rot=0, dot=(930,690)),
  dict(id="sidescreen", num="08", text="side screen",    at=(1250,380),  to=(1040,360),  rot=0, dot=(760,590)),
]
TITLES = dict(book="Book the room", dropin="Drop in", publishers="For publishers", vision="Our vision", setup="The setup",
              sidescreen="Side screen", program="Program", visit="Visit us")
NUMS = {t["id"]: t["num"] for t in TAGS}

def d_of(polys):
    return " ".join("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in p) + "Z" for p in polys)

defs, body = [], []
for i, p in enumerate(PIECES):
    img, (w, h) = p["src"]
    if p.get("polys"):
        xs = [x for q in p["polys"] for x, _ in q]; ys = [y for q in p["polys"] for _, y in q]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        cid = f"c{i}"
        defs.append(f'<clipPath id="{cid}"><path d="{d_of(p["polys"])}"/></clipPath>')
        art = (f'<path class="paper" d="{d_of(p["polys"])}"/>'
               f'<image href="{img}" width="{w}" height="{h}" clip-path="url(#{cid})" preserveAspectRatio="none"/>')
    else:
        cx, cy = w / 2, h / 2
        mask = ""
        if p.get("erase"):   # polygon(s) hidden from a cut-out (stray background bits)
            mid = f"m{i}"
            holes = "".join(f'<polygon points="{" ".join(f"{x},{y}" for x, y in q)}" fill="#000"/>' for q in p["erase"])
            defs.append(f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="#fff"/>{holes}</mask>')
            mask = f' mask="url(#{mid})"'
        cls = "flat" if p.get("flat") else ("thin" if p.get("thin") else "cut")
        lite = img.replace("cut2/", "lite/").replace(".png", ".jpg")
        if os.path.exists(os.path.join(ROOT, "website", lite)):
            # light version: JPEG colour + JPEG alpha, recombined with a luminance mask (≈80% smaller than PNG)
            aid = f"a{i}"
            defs.append(f'<mask id="{aid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">'
                        f'<image href="{lite[:-4]}-a.jpg" width="{w}" height="{h}" preserveAspectRatio="none"/></mask>')
            art = f'<g{mask}><image class="{cls}" href="{lite}" width="{w}" height="{h}" preserveAspectRatio="none" mask="url(#{aid})"/></g>'
        else:
            art = f'<g{mask}><image class="{cls}" href="{img}" width="{w}" height="{h}"/></g>'
    s, sy = p["s"], p["s"] * p.get("sy", 1)
    tf = f'translate({p["at"][0]} {p["at"][1]}) rotate({p["r"]}) scale({s} {sy}) translate({-cx:.1f} {-cy:.1f})'
    doodle = ""
    if p.get("doodle"):
        fx, fy, tx, ty, k = p.get("dfit", (0, 0, 0, 0, 1))
        dtf = f' transform="translate({tx} {ty}) scale({k}) translate({-fx} {-fy})"' if k != 1 else ""
        doodle = f'<g class="doodle"{dtf} style="--sw:{2.3 / s / k:.1f}px">{p["doodle"]}</g>'
    attrs = (f'class="piece" data-id="{p["id"]}"{"" if p["id"] == "lights" else f' data-open="{p["id"]}"'} tabindex="0" role="button" aria-label="{NUMS[p["id"]]} {TITLES.get(p["id"], p["id"])}"'
             if p["id"] else ('class="piece decor"' if p.get("screens") else 'class="piece decor" aria-hidden="true"'))
    extra = screens_markup() if p.get("screens") else ""
    if p.get("tv"):
        art += tv_markup(i, p["tv"])
    body.append(f'<g {attrs}><g transform="{tf}"><g class="lift{" low" if p.get("flat") else ""}">{art}{doodle}</g>{extra}</g></g>')

stickers = []
for st in STICKERS:
    pts = " ".join(f"{x},{y}" for x, y in st["pts"])
    lh = st["size"] * 1.05
    y = -(len(st["lines"]) - 1) * lh / 2 + st["size"] * 0.35
    texts = f'<text class="st-k" y="{y - st["size"] * 1.15:.1f}" text-anchor="middle" style="font-size:{max(st["size"] * .3, 8):.1f}px">{st["kicker"]}</text>'
    for k, line in enumerate(st["lines"]):
        texts += f'<text class="st-t" y="{y + k * lh:.1f}" text-anchor="middle" style="font-size:{st["size"]}px">{line}</text>'
    cords = ""
    if st.get("cords"):
        (ax, ay), (bx, by) = st["pts"][0], st["pts"][1]
        cords = f'<path class="cordline" d="M{ax + 30} {ay + 2} L{ax + 60} 0 M{bx - 30} {by + 2} L{bx - 60} 0"/>'
    stickers.append(f'<g class="piece sticker" data-id="{st["id"]}" data-open="{st["id"]}" tabindex="0" role="button" aria-label="{NUMS[st["id"]]} {TITLES[st["id"]]}">'
                    f'{cords}<g class="lift"><polygon class="blue" points="{pts}"/>'
                    f'<g transform="translate({st["at"][0]} {st["at"][1]}) rotate({st["rot"]})">{texts}</g></g></g>')

tags = []
for t in TAGS:
    x, y = t["at"]
    label = t["text"].upper()
    w = 62 + 12.4 * len(label)
    tx, ty = t["to"]
    dx, dy = t.get("dot", (tx, ty - 34))   # phone-size dot (kept inside the visible band)
    # Win98-style chip: grey bevelled box, navy number, pixel type; a dotted leader to a square pin
    tags.append(f'<g class="ptag" data-for="{t["id"]}">'
                f'<path class="string" d="M{x + 22} {y + 22} L {tx} {y + 22} L {tx} {ty}"/>'
                f'<rect class="pin" x="{tx - 5}" y="{ty - 5}" width="10" height="10"/>'
                f'<g class="card" data-for="{t["id"]}"><g class="full"><rect class="bg" x="{x}" y="{y}" width="{w:.0f}" height="44"/>'
                f'<path class="hi" d="M{x + 1.5} {y + 42.5} V{y + 1.5} H{x + w - 1.5:.0f}"/>'
                f'<path class="lo" d="M{x + 1.5} {y + 42.5} H{x + w - 1.5:.0f} V{y + 1.5}"/>'
                f'<text class="lbl" x="{x + 56}" y="{y + 31}">{label}</text></g>'
                f'<rect class="mini" x="{x}" y="{y}" width="52" height="44"/>'
                f'<rect class="chip" x="{x + 6}" y="{y + 6}" width="40" height="32"/>'
                f'<text class="num" x="{x + 26}" y="{y + 30}" text-anchor="middle">{t["num"]}</text></g>'
                f'<g class="dot" data-for="{t["id"]}"><circle cx="{dx}" cy="{dy}" r="34"/>'
                f'<text x="{dx}" y="{dy + 13}" text-anchor="middle">{t["num"]}</text></g></g>')

SCENE = f'''<svg class="collage" id="scene" viewBox="0 0 {VW} {VH}" preserveAspectRatio="xMidYMax slice" role="group" aria-label="Couch Co-Op: a living room for play, collaged into the POST Houston atrium">
  <defs>
    {"".join(defs)}
    <filter id="drop" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#000" flood-opacity=".6"/></filter>
    <filter id="sticker" x="-10%" y="-10%" width="120%" height="125%">
      <feMorphology in="SourceAlpha" operator="dilate" radius="10" result="grow"/>
      <feFlood flood-color="#f1e8d4"/><feComposite in2="grow" operator="in" result="edge"/>
      <feMerge><feMergeNode in="edge"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="tvscan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.6" fill="#000" opacity=".35"/></pattern>
    <radialGradient id="sheen" cx=".3" cy=".2" r=".9"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient>
    <radialGradient id="glow"><stop offset="0" stop-color="#ffd27a" stop-opacity=".7"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>
    <radialGradient id="candleglow"><stop offset="0" stop-color="#ffcf6e" stop-opacity=".75"/><stop offset=".4" stop-color="#ffb347" stop-opacity=".22"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
    <radialGradient id="fade" cx=".5" cy=".55" r=".75"><stop offset=".55" stop-color="#14110e" stop-opacity="0"/><stop offset="1" stop-color="#14110e" stop-opacity=".85"/></radialGradient>
    <linearGradient id="left" x1="0" x2="1"><stop offset=".12" stop-color="#14110e" stop-opacity=".92"/><stop offset=".42" stop-color="#14110e" stop-opacity="0"/></linearGradient>
    <radialGradient id="pool" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffcf8a" stop-opacity=".16"/><stop offset="1" stop-color="#ffcf8a" stop-opacity="0"/></radialGradient>
  </defs>
  <image href="{BACKDROP}" width="{VW}" height="{VH}" opacity=".22"/>
  <path d="M-507 880 L-2640 1333 M-399 880 L-2380 1333 M-292 880 L-2120 1333 M-184 880 L-1860 1333 M-76 880 L-1600 1333 M31 880 L-1340 1333 M139 880 L-1080 1333 M247 880 L-820 1333 M354 880 L-560 1333 M462 880 L-300 1333 M569 880 L-40 1333 M677 880 L220 1333 M785 880 L480 1333 M892 880 L740 1333 M1000 880 L1000 1333 M1108 880 L1260 1333 M1215 880 L1520 1333 M1323 880 L1780 1333 M1431 880 L2040 1333 M1538 880 L2300 1333 M1646 880 L2560 1333 M1753 880 L2820 1333 M1861 880 L3080 1333 M1969 880 L3340 1333 M2076 880 L3600 1333 M2184 880 L3860 1333 M2292 880 L4120 1333 M2399 880 L4380 1333 M2507 880 L4640 1333 M0 893 H2000 M0 910 H2000 M0 932 H2000 M0 962 H2000 M0 1002 H2000 M0 1055 H2000 M0 1125 H2000 M0 1215 H2000 M0 1330 H2000" fill="none" stroke="#f1e8d4" stroke-opacity=".09" stroke-width="1.2" vector-effect="non-scaling-stroke"/>
  <rect y="878" width="{VW}" height="2" fill="#f1e8d4" opacity=".14"/>
  <rect width="{VW}" height="{VH}" fill="url(#fade)"/>
  <rect width="{VW}" height="760" fill="url(#left)"/>
  <ellipse cx="1000" cy="1120" rx="900" ry="260" fill="url(#pool)"/>
  <rect id="veil" width="{VW}" height="{VH}" fill="#000" opacity="0"/>
  <g id="glows" opacity="0"><circle cx="1800" cy="1080" r="260" fill="url(#glow)"/></g>
  {"".join(stickers)}
  {"".join(body)}
  <g class="ptags" aria-hidden="true">{"".join(tags)}</g>
</svg>'''

VER_JS = int(os.path.getmtime(os.path.join(ROOT, "website", "panels.js")))
VER_CSS = int(os.path.getmtime(os.path.join(ROOT, "website", "style.css")))

HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Couch Co-Op</title>
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-64.png" sizes="64x64" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="description" content="Couch Co-Op is a public living room for play: cooperative games and interactive art. Pilot edition at POST Houston.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@900&family=Instrument+Serif:ital@0;1&family=Space+Grotesk:wght@500;700&family=VT323&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={VER_CSS}">
<style>
  :root {{ --night:#14110e; --paper:#f1e8d4; --ink:#2a2420; --cut:#000080; --amber:#f3b23c; --silver:#c3c3c3; --navy:#000080; }}
  * {{ box-sizing:border-box; }}
  html,body {{ margin:0; height:100%; background:var(--night); color:var(--paper); overflow:hidden; font-family:"Space Grotesk",system-ui,sans-serif; -webkit-font-smoothing:antialiased; }}
  .collage {{ position:fixed; inset:0; width:100%; height:100%; display:block; opacity:0; transition:opacity .7s ease; }}
  body.ready .collage {{ opacity:1; }}
  .loader {{ position:fixed; left:50%; top:50%; transform:translate(-50%,-50%); z-index:5; width:min(280px,70vw); text-align:center;
    font:400 20px/1 VT323, monospace; letter-spacing:1px; color:#f1e8d4b3; transition:opacity .4s; pointer-events:none; }}
  .loader p {{ margin:0 0 10px; }}
  .loader .track {{ height:14px; padding:2px; background:#000; box-shadow:inset 1px 1px #808080, inset -1px -1px #f1e8d455; }}
  .loader i {{ display:block; height:100%; width:0; background:var(--navy); box-shadow:inset 0 0 0 1px #3a4bd8; transition:width .2s steps(4); }}
  body.ready .loader {{ opacity:0; }}

  /* cut-outs */
  .piece {{ cursor:pointer; outline:none; }}
  .piece.decor {{ cursor:default; }}
  .piece .lift {{ transition:transform .35s cubic-bezier(.2,.9,.3,1.3); transform-box:fill-box; transform-origin:center; filter:url(#drop); }}
  .piece image.cut {{ }}
  .piece image.flat {{ opacity:.95; }}
  .piece image.thin {{ filter:brightness(.85); }}
  .piece .paper {{ fill:var(--paper); stroke:var(--paper); stroke-width:6; stroke-linejoin:round; vector-effect:non-scaling-stroke; }}
  .piece:not(.decor):hover .lift, .piece:focus-visible .lift, .piece.on .lift {{ transform:translateY(-8px) scale(1.03); }}
  .piece.on .lift.low, .piece:hover .lift.low {{ transform:scale(1.015); }}
  .sticker .blue {{ fill:var(--cut); stroke:var(--paper); stroke-width:6; vector-effect:non-scaling-stroke; }}
  .sticker:hover .blue, .sticker.on .blue {{ fill:#2846e6; }}
  .sticker .cordline {{ fill:none; stroke:#a8977f; stroke-width:1.3; vector-effect:non-scaling-stroke; }}
  .screen {{ cursor:pointer; outline:none; }}
  .screen .slide, .tv .slide {{ opacity:0; animation:slide linear infinite; }}
  .tv image {{ filter:saturate(1.15) contrast(1.05); }}
  @keyframes slide {{ 0%, 30% {{ opacity:1; }} 36%, 94% {{ opacity:0; }} 100% {{ opacity:1; }} }}
  .screen .bezel {{ fill:none; stroke:#0d0c0b; stroke-width:3; vector-effect:non-scaling-stroke; }}
  .screen .flip {{ opacity:0; transition:opacity .25s; }}
  .screen .blue {{ fill:var(--cut); }}
  .screen:hover .flip, .screen.on .flip, .screen:focus-visible .flip {{ opacity:1; }}
  .screen:focus-visible .bezel {{ stroke:var(--amber); }}
  .piece.decor .lift {{ cursor:default; }}
  .st-k {{ font-family:VT323, monospace; letter-spacing:1px; fill:var(--paper); opacity:.8; }}
  .st-t {{ font-family:VT323, monospace; fill:var(--paper); }}

  /* hand-drawn layers that draw themselves on hover */
  .doodle {{ pointer-events:none; }}
  .doodle .ln {{ fill:none; stroke:var(--paper); stroke-width:var(--sw); stroke-linecap:round; stroke-linejoin:round;
    stroke-dasharray:1; stroke-dashoffset:1; transition:stroke-dashoffset .55s ease var(--d,0s); }}
  .doodle .ray {{ stroke:#ffd27a; }}
  .doodle .dtext {{ font:900 30px Unbounded; fill:var(--amber); opacity:0; transition:opacity .4s ease var(--d); }}
  .piece.on .doodle .dtext {{ opacity:1; }}
  .doodle .fl {{ transform:scale(0); transform-box:fill-box; transform-origin:50% 100%; transition:transform .4s cubic-bezier(.3,1.7,.5,1) calc(var(--d,0s) + .6s); }}
  .doodle .f {{ fill:#ffbf4d; stroke:var(--paper); stroke-width:var(--sw); stroke-linejoin:round; }}
  .doodle .fi {{ fill:#fff4cf; }}
  .doodle .fl path {{ transform-box:fill-box; transform-origin:50% 100%; animation:flick 1.3s ease-in-out infinite alternate; }}
  .doodle .fi {{ animation-duration:.9s !important; }}
  @keyframes flick {{ 0% {{ transform:skewX(-5deg) scaleY(.92); }} 45% {{ transform:skewX(4deg) scaleY(1.07); }} 100% {{ transform:skewX(-2deg) scaleY(.97); }} }}
  .doodle .gl {{ opacity:0; mix-blend-mode:screen; transition:opacity .7s ease calc(var(--d,0s) + .7s); }}
  .doodle .hrt {{ fill:#e8735a; stroke:var(--paper); stroke-width:calc(var(--sw) * .6); opacity:0; transform-box:fill-box; transform-origin:center; }}
  .piece.on .doodle .hrt, .piece:focus-visible .doodle .hrt {{ animation:floatUp 2.4s ease-out var(--d) infinite; }}
  @keyframes floatUp {{ 0% {{ opacity:0; transform:translateY(0) scale(.6); }} 20% {{ opacity:1; transform:translateY(-8px) scale(1); }} 100% {{ opacity:0; transform:translateY(-50px) scale(.9) rotate(12deg); }} }}
  .piece.on .doodle .ln, .piece:focus-visible .doodle .ln, body.dark .piece[data-id="lights"] .doodle .ln {{ stroke-dashoffset:0; }}
  .piece.on .doodle .fl, .piece:focus-visible .doodle .fl, body.dark .piece[data-id="lights"] .doodle .fl {{ transform:scale(1); }}
  .piece.on .doodle .gl, .piece:focus-visible .doodle .gl, body.dark .piece[data-id="lights"] .doodle .gl {{ opacity:1; }}
  body:not(.dark) .piece:not(.on):not(:focus-visible) .doodle * {{ transition-delay:0s !important; transition-duration:.3s !important; }}

  /* tags */
  .ptag .bg {{ fill:var(--silver); stroke:#0a0a0a; stroke-width:2; filter:url(#drop); }}
  .ptag .hi {{ fill:none; stroke:#fff; stroke-width:3; }}
  .ptag .lo {{ fill:none; stroke:#6b6b6b; stroke-width:3; }}
  .ptag .chip {{ fill:var(--navy); }}
  .ptag .num {{ font:400 30px VT323, monospace; fill:#fff; }}
  .ptag .lbl {{ font:400 30px VT323, monospace; fill:#000; letter-spacing:.5px; }}
  .ptag .string {{ fill:none; stroke:var(--paper); stroke-width:1.3; vector-effect:non-scaling-stroke; opacity:.8; }}
  .ptag .pin {{ fill:var(--paper); stroke:#000; stroke-width:2; }}
  .ptag {{ transition:opacity .3s; }}
  .collage.hovering .ptag {{ opacity:.45; }}
  .collage.hovering .ptag.on {{ opacity:1; }}
  .ptag.on .chip {{ fill:var(--cut); }}
  /* calm by default: just the number; the label slides out on hover */
  .ptag .mini {{ fill:var(--silver); stroke:#0a0a0a; stroke-width:2; filter:url(#drop); }}
  .ptag .full {{ opacity:0; transition:opacity .15s; }}
  .ptag.on .full {{ opacity:1; }} .ptag.on .mini {{ opacity:0; }}
  .ptag .string {{ opacity:.35 !important; }} .ptag.on .string {{ opacity:.9 !important; }}
  .ptags {{ pointer-events:none; }} .ptag .card, .ptag .dot {{ pointer-events:all; cursor:pointer; }}
  .ptag.on .bg {{ fill:#dcdcdc; }}

  /* ===== internet core: CCTV feed, detection boxes, Win98 chrome ===== */
  .scan {{ position:fixed; inset:0; z-index:8; pointer-events:none;
    background:repeating-linear-gradient(180deg, #0000 0 2px, #0000002e 2px 3px), radial-gradient(ellipse at 50% 55%, #0000 55%, #000a 100%); mix-blend-mode:multiply; }}
  .grain {{ position:fixed; inset:-50%; z-index:8; pointer-events:none; opacity:.07; background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E"); animation:grain 1s steps(4) infinite; }}
  @keyframes grain {{ 0% {{ transform:translate(0,0); }} 25% {{ transform:translate(-3%,2%); }} 50% {{ transform:translate(2%,-3%); }} 75% {{ transform:translate(-2%,-1%); }} }}
  .hud {{ position:fixed; z-index:9; pointer-events:none; font:400 22px/1 VT323, monospace; color:#e9f0e6; letter-spacing:1px; text-shadow:0 0 6px #000, 0 0 2px #000; }}
  .hud.bl {{ left:clamp(20px,3vw,44px); bottom:22px; display:flex; gap:18px; align-items:center; }}
  .hud.br {{ right:clamp(20px,3vw,44px); bottom:22px; text-align:right; }}
  .rec {{ color:#ff3b2f; }} .rec::before {{ content:"●"; margin-right:6px; animation:blink 1.2s steps(2) infinite; }}
  .hud .open, .hud .closed {{ color:var(--paper); }}
  @keyframes blink {{ 50% {{ opacity:0; }} }}
  .lock {{ position:fixed; z-index:9; pointer-events:none; opacity:0; transition:opacity .15s; }}
  .lock.on {{ opacity:1; }}
  .lock i {{ position:absolute; width:18px; height:18px; border:2px solid #e9f0e6; filter:drop-shadow(0 0 2px #000); }}
  .lock i:nth-child(1) {{ left:0; top:0; border-right:0; border-bottom:0; }}
  .lock i:nth-child(2) {{ right:0; top:0; border-left:0; border-bottom:0; }}
  .lock i:nth-child(3) {{ left:0; bottom:0; border-right:0; border-top:0; }}
  .lock i:nth-child(4) {{ right:0; bottom:0; border-left:0; border-top:0; }}
  .lock b {{ display:none; position:absolute; left:0; top:100%; margin-top:4px; white-space:nowrap; font:400 20px/1 VT323, monospace; background:#e9f0e6; color:#000; padding:2px 6px 1px; }}
  .lock.on {{ animation:lockin .25s steps(3); }}
  @keyframes lockin {{ from {{ transform:scale(1.12); }} }}
  /* pixel cursors */
  html, body, .piece.decor {{ cursor:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='22' height='32' shape-rendering='crispEdges'%3E%3Cpath d='M1 1v23l6-6 4 10 4-2-4-9h8z' fill='%23fff' stroke='%23000' stroke-width='1.6'/%3E%3C/svg%3E") 1 1, default; }}
  .piece, .screen, button, a, .ptag {{ cursor:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='26' height='30' shape-rendering='crispEdges'%3E%3Cpath d='M8 1h3v10h2V8h3v4h2V10h3v3h2v3h1v7l-2 4v2H9v-3l-6-6v-3h3l2 2z' fill='%23fff' stroke='%23000' stroke-width='1.6'/%3E%3C/svg%3E") 9 1, pointer; }}
  /* Win98 bevel buttons in the top bar */
  .btn, .btn.ghost {{ background:var(--silver); color:#000; border-radius:0; font:400 22px/1 VT323, monospace; padding:7px 14px 6px; letter-spacing:.5px;
    box-shadow:inset -2px -2px #0a0a0a, inset 2px 2px #fff, inset -4px -4px #808080, inset 4px 4px #dfdfdf; }}
  .btn:active {{ box-shadow:inset 2px 2px #0a0a0a, inset -2px -2px #fff, inset 4px 4px #808080; }}
  .btn.primary {{ background:var(--navy); color:#fff; box-shadow:inset -2px -2px #000, inset 2px 2px #5a74e8; }}
  .study {{ font:400 20px VT323, monospace; letter-spacing:1px; color:#f1e8d499; }}
  /* boot dialog */
  .boot {{ position:fixed; inset:0; z-index:60; display:grid; place-items:center; background:#000; transition:opacity .5s, visibility .5s; }}
  .boot.done {{ opacity:0; visibility:hidden; }}
  .boot .dlg {{ width:min(420px, calc(100% - 40px)); background:var(--silver); color:#000; font:400 22px VT323, monospace;
    box-shadow:inset -2px -2px #0a0a0a, inset 2px 2px #fff, inset -4px -4px #808080, inset 4px 4px #dfdfdf; padding:4px; }}
  .dlg .tb {{ background:linear-gradient(90deg, var(--navy), #1084d0); color:#fff; padding:3px 6px; display:flex; justify-content:space-between; }}
  .dlg .tb span:last-child {{ background:var(--silver); color:#000; width:20px; text-align:center; box-shadow:inset -1px -1px #0a0a0a, inset 1px 1px #fff; }}
  .dlg .in {{ padding:18px 18px 16px; }}
  .dlg .bar {{ height:24px; margin:12px 0 6px; padding:3px; background:#fff; box-shadow:inset 2px 2px #808080, inset -2px -2px #fff; display:flex; gap:3px; overflow:hidden; }}
  .dlg .bar i {{ flex:0 0 14px; background:var(--navy); opacity:0; animation:fill 1.6s steps(1) forwards; }}
  @keyframes fill {{ to {{ opacity:1; }} }}
  .dlg small {{ font-size:18px; color:#444; }}
  /* the content windows, re-skinned as Win98 dialogs */
  .window {{ border-radius:0 !important; border:0 !important; background:var(--silver) !important; padding:4px !important;
    box-shadow:inset -2px -2px #0a0a0a, inset 2px 2px #fff, inset -4px -4px #808080, inset 4px 4px #dfdfdf, 0 30px 80px #000 !important; }}
  .winbar {{ background:linear-gradient(90deg, var(--navy), #1084d0) !important; color:#fff !important; padding:4px 4px 4px 10px !important; border:0 !important; gap:10px !important; }}
  .winbar h2, .winnum {{ font:400 22px/1 VT323, monospace !important; letter-spacing:.5px !important; color:#fff !important; text-transform:none !important; }}
  .winbar .close {{ background:var(--silver) !important; color:#000 !important; font:400 18px/1 VT323, monospace !important; padding:4px 8px !important;
    box-shadow:inset -1px -1px #0a0a0a, inset 1px 1px #fff, inset -2px -2px #808080 !important; }}
  .winbody {{ background:var(--paper); margin-top:4px; box-shadow:inset 2px 2px #808080, inset -2px -2px #fff; }}
  @media (prefers-reduced-motion: reduce) {{ .grain, .rec::before, .hero h1::after {{ animation:none; }} .boot {{ display:none; }} }}

  /* lights */
  #veil, #glows {{ transition:opacity .8s; }}
  body.dark #veil {{ opacity:.55; }}
  body.dark #glows {{ opacity:1; mix-blend-mode:screen; }}

  /* frame UI */
  .top {{ position:fixed; inset:0 0 auto; z-index:10; display:flex; align-items:center; padding:24px clamp(20px,3vw,44px); gap:20px; }}
  .logo .mark {{ width:1.05em; height:1.05em; image-rendering:pixelated; vertical-align:-.16em; margin-right:.3em; }}
  .logo {{ font:400 34px/1 VT323, monospace; letter-spacing:1px; color:var(--paper); text-decoration:none; }}
  .top nav {{ margin-left:auto; display:flex; gap:8px; }}
  .btn {{ border:0; }}
  .hero {{ position:fixed; left:clamp(20px,3vw,44px); top:clamp(88px,12vh,128px); z-index:10; pointer-events:none; max-width:min(760px,52vw); }}
  .hero h1 {{ margin:0 0 16px; font:400 clamp(40px,4.3vw,78px)/.85 VT323, monospace; letter-spacing:-1px; text-shadow:0 2px 0 #000, 0 0 18px #000; }}
  .hero h1 mark {{ background:var(--navy); color:#fff; padding:0 .12em; text-shadow:none; }}
  .hero em {{ color:var(--amber); }}
  .hero p {{ display:inline-block; background:#ffffe1; color:#000 !important; border:1px solid #000; padding:5px 8px; font:13px/1.45 Tahoma, Verdana, "Segoe UI", sans-serif !important; box-shadow:2px 2px 0 #0008; margin:0; font-size:15px; line-height:1.5; color:#f1e8d4b0; max-width:26em; }}

  /* placeholder window */
  .ov {{ position:fixed; inset:0; z-index:20; display:grid; place-items:center; background:#000c; }}
  .ov[hidden] {{ display:none; }}
  .card {{ background:var(--paper); color:var(--ink); width:min(520px,calc(100% - 32px)); padding:30px 32px 34px; position:relative; transform:rotate(-1.2deg); box-shadow:0 30px 80px #000; }}
  .card .n {{ font:700 11px "Space Grotesk"; letter-spacing:2px; color:var(--cut); }}
  .card h2 {{ margin:6px 0 10px; font:400 52px/1 "Instrument Serif",serif; }}
  .card p {{ margin:0; color:#6f675e; }}
  .card button {{ position:absolute; top:14px; right:16px; border:0; background:none; font:700 12px "Space Grotesk"; letter-spacing:1px; cursor:pointer; }}

  .ptag .dot {{ display:none; }}
  .tip {{ position:fixed; z-index:9; pointer-events:none; max-width:260px; background:#ffffe1; color:#000; border:1px solid #000; box-shadow:2px 2px 0 #0009;
    font:12px/1.4 Tahoma, Verdana, "Segoe UI", sans-serif; padding:6px 9px 7px; opacity:0; transform:translateY(4px); transition:opacity .12s, transform .12s; }}
  .tip.on {{ opacity:1; transform:none; transition-delay:.25s; }}
  .tip b {{ display:block; font-weight:700; margin-bottom:2px; }}
  .tip::before {{ content:""; position:absolute; left:14px; top:-8px; border:8px solid transparent; border-top:0; border-bottom-color:#000; }}
  .tip::after {{ content:""; position:absolute; left:15px; top:-6px; border:7px solid transparent; border-top:0; border-bottom-color:#ffffe1; }}
  .ptag .dot circle {{ fill:var(--cut); stroke:var(--paper); stroke-width:3; vector-effect:non-scaling-stroke; filter:url(#drop); }}
  .ptag .dot text {{ font:700 36px "Space Grotesk"; fill:#fff; }}
  .swipe {{ display:none; }}
  .phone-screen {{ background:url("concept/backdrop-post.jpg") center / cover !important; }}
  body:not(.upright) .rotate ~ .top {{ }}

  /* short screens (phones held sideways): numbered dots instead of labels */
  @media (max-height:560px) {{
    .ptag > g:first-of-type, .ptag .string, .ptag .pin {{ display:none; }}
    .ptag .dot {{ display:inline; }}
    .hero h1 {{ font-size:32px; }} .hero p {{ display:none; }} .hero {{ top:54px; }}
    .top {{ padding:10px 14px; gap:12px; }} .logo {{ font-size:15px; }} .study {{ display:none; }}
    .btn, .btn.ghost {{ padding:5px 8px 4px; font-size:17px; }}
    .hud {{ font-size:15px; bottom:10px !important; }} .hud.bl {{ gap:10px; }} .hud.bl span:nth-child(2) {{ display:none; }}
    .lock b {{ font-size:15px; }}
  }}

  /* phones held upright: start screen, then a swipeable room */
  @media (max-width:760px) and (orientation:portrait) {{
    body:not(.upright) .top, body:not(.upright) .hero {{ visibility:hidden; }}
    .study, #lightsBtn {{ display:none; }}
    .top {{ padding:14px 16px; gap:10px; }} .logo {{ font-size:16px; }} .btn {{ padding:8px 11px; font-size:11px; }}
    .pan {{ position:fixed; inset:0; overflow-x:auto; overflow-y:hidden; scrollbar-width:none; -webkit-overflow-scrolling:touch; }}
    .pan::-webkit-scrollbar {{ display:none; }}
    .collage {{ position:absolute; inset:auto; top:0; left:0; height:100svh; width:150svh; }}
    .hero {{ top:64px; max-width:none; right:16px; }}
    .hero h1 {{ font-size:40px; }} .hero p {{ font-size:14px; }}
    .swipe {{ display:block; position:fixed; left:50%; bottom:max(14px, env(safe-area-inset-bottom)); transform:translateX(-50%); z-index:9; margin:0;
      padding:7px 14px; border-radius:999px; background:#14110ecc; color:var(--paper); font-size:12px; font-weight:700; letter-spacing:1px; text-transform:uppercase; pointer-events:none; transition:opacity .6s; }}
    .swiped .swipe {{ opacity:0; }}
  }}
</style>
</head>
<body>
<header class="top">
  <a class="logo" href="#"><img class="mark" src="favicon.svg" alt="" width="26" height="26">COUCH CO-OP</a>
  <span class="study">Pilot · POST Houston</span>
  <nav><button class="btn ghost" data-open="menu" aria-haspopup="dialog">Index</button><button class="btn primary" data-open="book">Book the room</button></nav>
</header>
<div class="loader" aria-hidden="true"><p>LOADING THE LIVING ROOM <span id="loadtxt"></span></p><div class="track"><i id="loadbar"></i></div></div>
<div class="pan" id="pan">{SCENE}</div>
<div class="scan" aria-hidden="true"></div>
<div class="hud bl" aria-hidden="true"><span class="rec">REC</span><span id="clock"></span></div>
<div class="hud br" id="openNow" aria-live="polite"></div>
<div class="lock" id="lock" aria-hidden="true"><i></i><i></i><i></i><i></i><b></b></div>
<div class="tip" id="tip" aria-hidden="true"></div>
<p class="swipe" aria-hidden="true">← swipe the room →</p>
<div class="rotate" id="rotate">
  <div class="rotate-inner">
    <p class="rotate-logo">COUCH CO-OP</p>
    <div class="phone" aria-hidden="true"><div class="phone-screen"></div></div>
    <p class="rotate-title">Turn your phone <em>sideways</em></p>
    <p class="rotate-sub">to step into the living room</p>
    <p class="press">▶ PRESS START</p>
    <button class="rotate-skip" id="rotateSkip">Stay upright instead</button>
  </div>
</div>
<div class="hero"><h1>A public living room<br><mark>for play.</mark></h1><p>Co-op games &amp; interactive art · POST Houston</p></div>
{WINDOWS}
<script src="panels.js?v={VER_JS}"></script>
<script>
  const scene = document.getElementById("scene");
  // show the room only once every picture in it has arrived; retry any that fail
  const ready = () => document.body.classList.add("ready");
  (() => {{
    const imgs = [...scene.querySelectorAll("image")];
    const urls = [...new Set(imgs.map(i => i.getAttribute("href")))];
    const bar = document.getElementById("loadbar"), txt = document.getElementById("loadtxt");
    let done = 0;
    const tick = () => {{
      done++;
      bar.style.width = Math.round(done / urls.length * 100) + "%";
      txt.textContent = `${{done}}/${{urls.length}}`;
      if (done === urls.length) ready();
    }};
    urls.forEach(u => {{
      let tries = 0;
      const load = () => {{
        const im = new Image();
        im.onload = () => {{
          // re-point any SVG image that gave up while the network was busy
          if (tries) imgs.filter(i => i.getAttribute("href") === u).forEach(i => i.setAttribute("href", im.src));
          (im.decode ? im.decode().catch(() => {{}}) : Promise.resolve()).then(tick);
        }};
        im.onerror = () => {{ if (++tries < 4) setTimeout(load, 600 * tries); else tick(); }};
        im.src = tries ? `${{u}}?r=${{tries}}` : u;
      }};
      load();
    }});
    setTimeout(ready, 15000);   // never hold the room back forever
  }})();
  function toggleLights() {{
    const on = document.body.classList.toggle("dark");
    const b = document.getElementById("lightsBtn");
    b.textContent = on ? "Lights on" : "Lights off"; b.setAttribute("aria-pressed", String(on));
  }}


  // CCTV clock (Houston time) and open-play status
  const fmt = new Intl.DateTimeFormat("en-CA", {{ timeZone:"America/Chicago", year:"numeric", month:"2-digit", day:"2-digit", hour:"2-digit", minute:"2-digit", second:"2-digit", hour12:false }});
  const tick2 = () => {{
    const p = Object.fromEntries(fmt.formatToParts(new Date()).map(x => [x.type, x.value]));
    document.getElementById("clock").textContent = `${{p.year}}-${{p.month}}-${{p.day}} ${{p.hour}}:${{p.minute}}:${{p.second}}`;
    const h = +p.hour % 24;
    document.getElementById("openNow").innerHTML = (h >= 10 && h < 22)
      ? '<span class="open">● OPEN NOW</span> · 10–22'
      : '<span class="closed">○ CLOSED</span> · OPEN 10–22';
  }};
  tick2(); setInterval(tick2, 1000);

  // detection box: locks onto whatever you point at
  const lock = document.getElementById("lock"), tip = document.getElementById("tip");
  const TIPS = {{
    dropin:["Drop in", "Free open play, daily 10am–10pm. Grab a controller."],
    book:["Book the room", "Both consoles and screens, up to 6 people. $15 for 2 hours."],
    program:["Snacks & nights", "Co-op nights, launches and screenings."],
    vision:["Shoes off", "House rule #1, and what the room is for."],
    setup:["The setup", "2 consoles, 2 screens, room for 4–6."],
    visit:["Visit", "Inside POST Houston. Open daily."],
    publishers:["For publishers", "Feature your game on the main screen."],
    sidescreen:["Side screen", "Small games and interactive art."],
  }};
  const LABELS = {{ book:"BOOK_THE_ROOM", dropin:"DROP_IN", publishers:"FEATURED_SCREEN", vision:"SHOES_OFF", setup:"THE_SETUP",
    sidescreen:"SIDE_SCREEN", program:"SNACKS_&_NIGHTS", visit:"LIVE_CAM", lights:"LAMP" }};
  function lockOn(el) {{
    const id = el.dataset.id;
    const els = [el.classList.contains("screen") ? el.querySelector(".bezel") : (el.querySelector(".lift > g > image, .lift > image") || el)];
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    els.forEach(e => {{ const r = e.getBoundingClientRect(); x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom); }});
    const pad = 8;
    Object.assign(lock.style, {{ left:(x0 - pad) + "px", top:(y0 - pad) + "px", width:(x1 - x0 + pad * 2) + "px", height:(y1 - y0 + pad * 2) + "px" }});
    lock.querySelector("b").textContent = `${{NUMS[id] || ""}} ${{LABELS[id] || id.toUpperCase()}} ${{(0.9 + Math.random() * 0.09).toFixed(2)}}`;
    lock.classList.remove("on"); tip.classList.remove("on"); void lock.offsetWidth; lock.classList.add("on");
    const t = TIPS[id];
    if (t) {{
      tip.innerHTML = `<b>${{t[0]}}</b>${{t[1]}}`;
      const tw = 260, left = Math.min(innerWidth - tw - 12, Math.max(12, x1 - 60));
      Object.assign(tip.style, {{ left:left + "px", top:Math.min(innerHeight - 90, y0 + 18) + "px" }});
      tip.classList.add("on");
    }}
  }}
  const NUMS = {{}}; document.querySelectorAll(".ptag").forEach(t => NUMS[t.dataset.for] = "ID" + t.querySelector(".num").textContent);
  const pan = document.getElementById("pan");
  const centre = () => {{ if (pan.scrollWidth > pan.clientWidth) pan.scrollLeft = (pan.scrollWidth - pan.clientWidth) * 0.42; }};
  addEventListener("load", centre); addEventListener("resize", centre);
  ["touchstart", "wheel", "pointerdown"].forEach(ev => pan.addEventListener(ev, () => setTimeout(() => document.body.classList.add("swiped"), 1200), {{ once:true, passive:true }}));
  document.getElementById("rotateSkip").onclick = () => {{ document.body.classList.add("upright"); centre(); }};

  // no hover on touch screens: let the drawings play by themselves, one after another
  if (matchMedia("(hover: none)").matches) {{
    const cycle = ["dropin", "program", "vision", "lights"]; let k = 0;
    const tick = () => {{
      document.querySelectorAll(".piece.auto").forEach(p => p.classList.remove("on", "auto"));
      document.querySelectorAll(`.piece[data-id="${{cycle[k++ % cycle.length]}}"]`).forEach(p => p.classList.add("on", "auto"));
    }};
    tick(); setInterval(tick, 3600);
  }}
  document.querySelectorAll(".ptag .card, .ptag .dot").forEach(c => {{
    const target = () => document.querySelector(`.piece[data-id="${{c.dataset.for}}"]`);
    c.addEventListener("mouseenter", () => target()?.dispatchEvent(new Event("mouseenter")));
    c.addEventListener("mouseleave", () => target()?.dispatchEvent(new Event("mouseleave")));
    c.addEventListener("click", () => {{ const t = target(); if (!t) return; t.dataset.open ? openPanel(t.dataset.open) : toggleLights(); }});
  }});
  document.querySelectorAll(".piece[data-id]").forEach(el => {{
    if (el.dataset.id === "lights") el.addEventListener("click", toggleLights);
    el.addEventListener("keydown", e => {{
      if (e.key !== "Enter" && e.key !== " ") return;
      e.preventDefault();
      el.dataset.open ? openPanel(el.dataset.open) : toggleLights();
    }});
    const on = () => {{
      scene.classList.add("hovering"); lockOn(el);
      document.querySelectorAll(`.piece[data-id="${{el.dataset.id}}"]`).forEach(p => p.classList.add("on"));
      document.querySelectorAll(`.ptag[data-for="${{el.dataset.id}}"]`).forEach(n => n.classList.add("on"));
    }};
    const off = () => {{
      scene.classList.remove("hovering"); lock.classList.remove("on"); tip.classList.remove("on");
      document.querySelectorAll(".piece.on, .ptag.on").forEach(n => n.classList.remove("on"));
    }};
    el.addEventListener("mouseenter", on); el.addEventListener("mouseleave", off);
    el.addEventListener("focus", on); el.addEventListener("blur", off);
  }});
</script>
</body>
</html>
'''

open(os.path.join(ROOT, "website", "retro.html"), "w").write(HTML)   # the earlier Win98/CCTV look, kept for reference
print("wrote", OUT)

# ===================== quiet variant (website/quiet.html) =====================
# Same room, no OS costume: one type family (IBM Plex), flat panels, plain labels,
# no CCTV readout / scanlines / pixel cursor. Kept: collage, CRT footage, numbered
# chips, corner brackets, and the navy "selected text" highlight on "for play.".
QUIET_CSS = """
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style id="quiet">
  :root { --q-ink:#f1e8d4; --q-dim:#f1e8d48c; --q-line:#f1e8d433; --q-bg:#14110e; --mono:"IBM Plex Mono", ui-monospace, monospace; --sans:"IBM Plex Sans", system-ui, sans-serif; }
  html, body, .piece.decor, .piece, .screen, button, a, .ptag { cursor:auto; }
  .piece:not(.decor), .screen, button, a, .ptag .card, .ptag .dot { cursor:pointer; }
  body { font-family:var(--sans); }
  .scan, .grain { display:none !important; }
  .hud.bl { font:400 12px/1 var(--mono) !important; letter-spacing:.06em !important; color:var(--q-ink) !important; text-shadow:none !important;
    background:var(--q-bg); padding:7px 10px; gap:12px !important; }
  .rec { color:#ff3b2f !important; } .rec::before { margin-right:6px; }
  /* top bar */
  .logo { font:500 15px/1 var(--mono) !important; letter-spacing:.14em !important; }
  .logo .mark { width:20px !important; height:20px !important; image-rendering:auto !important; vertical-align:-5px !important; margin-right:10px !important; }
  .study { font:400 12px var(--mono) !important; letter-spacing:.06em !important; color:var(--q-dim) !important; }
  .btn, .btn.ghost { font:500 12px/1 var(--mono) !important; letter-spacing:.08em !important; text-transform:uppercase; padding:10px 14px !important;
    background:transparent !important; color:var(--q-ink) !important; box-shadow:inset 0 0 0 1px var(--q-line) !important; border-radius:0 !important; }
  .btn:hover { box-shadow:inset 0 0 0 1px var(--q-ink) !important; }
  .btn.primary { background:var(--q-ink) !important; color:#000 !important; box-shadow:none !important; }
  /* hero */
  .hero h1 { font:500 clamp(30px,3.1vw,50px)/1.05 var(--mono) !important; letter-spacing:-.04em !important; text-shadow:0 0 24px #000 !important; }
  .hero h1 mark { padding:0 .08em; }
  .hero p { background:none !important; border:0 !important; box-shadow:none !important; padding:0 !important;
    font:400 14px/1.5 var(--sans) !important; color:var(--q-dim) !important; text-shadow:0 0 12px #000; }
  /* numbered chips: flat squares, label in plain type */
  .ptag .bg, .ptag .mini { fill:var(--q-bg) !important; stroke:var(--q-line) !important; stroke-width:1.5 !important; filter:none !important; }
  .ptag .hi, .ptag .lo { display:none; }
  .ptag .chip { fill:transparent !important; }
  .ptag.on .chip { fill:var(--cut) !important; }
  .ptag .num { font:500 20px var(--mono) !important; fill:var(--q-ink) !important; }
  .ptag .lbl { font:500 18px var(--mono) !important; letter-spacing:.06em !important; fill:var(--q-ink) !important; }
  .ptag.on .bg { fill:var(--q-bg) !important; stroke:var(--q-ink) !important; }
  .ptag .pin { fill:var(--q-ink) !important; stroke:none !important; }
  .ptag .dot circle { fill:var(--q-bg) !important; stroke:var(--q-ink) !important; stroke-width:1.5 !important; filter:none !important; }
  .ptag .dot text { font:500 30px var(--mono) !important; fill:var(--q-ink) !important; }
  /* hover: thin brackets + a plain label */
  .lock i { border-width:1px !important; width:14px !important; height:14px !important; border-color:var(--q-ink) !important; }
  .lock.on { animation:none !important; }
  .tip { background:var(--q-bg) !important; color:var(--q-ink) !important; border:1px solid var(--q-line) !important; box-shadow:none !important;
    font:400 13px/1.45 var(--sans) !important; padding:10px 12px !important; max-width:240px !important; }
  .tip b { font:500 11px/1 var(--mono) !important; letter-spacing:.08em; text-transform:uppercase; margin-bottom:6px !important; color:var(--q-ink); }
  .tip::before, .tip::after { display:none !important; }
  .hud.br { font:400 12px/1 var(--mono) !important; letter-spacing:.06em !important; color:var(--q-ink) !important; text-shadow:none !important; background:var(--q-bg); padding:7px 10px; }
  .hud .open, .hud .closed { color:var(--q-ink) !important; }
  /* loader */
  .loader { font:400 11px/1 var(--mono) !important; letter-spacing:.14em !important; color:var(--q-dim) !important; }
  .loader .track { height:1px !important; padding:0 !important; background:var(--q-line) !important; box-shadow:none !important; }
  .loader i { background:var(--q-ink) !important; box-shadow:none !important; }
  /* screens on the tower */
  .st-k, .st-t { font-family:var(--mono) !important; }

  /* ---------- windows: flat paper panels ---------- */
  .window { background:#f3efe6 !important; padding:0 !important; box-shadow:0 40px 120px #000 !important; font-family:var(--sans) !important; color:#141210 !important; }
  .winbar { background:transparent !important; color:#141210 !important; padding:14px 18px 14px 28px !important; border-bottom:1px solid #1412101f !important; }
  .winbar h2, .winnum { font:500 11px/1 var(--mono) !important; letter-spacing:.12em !important; text-transform:uppercase !important; color:#141210 !important; }
  .winnum { color:var(--cut) !important; }
  .winbar .close { background:none !important; box-shadow:none !important; font:500 11px/1 var(--mono) !important; letter-spacing:.12em !important; color:#141210 !important; padding:8px 0 8px 10px !important; }
  .winbody { background:transparent !important; box-shadow:none !important; margin:0 !important; padding:28px 32px 34px !important; }
  .kicker { font:500 11px/1 var(--mono) !important; letter-spacing:.12em !important; color:#14121099 !important; }
  .display { font:600 clamp(34px,4.6vw,48px)/1.02 var(--sans) !important; letter-spacing:-.03em !important; }
  .display em { font-style:normal; background:var(--cut); color:#fff; padding:0 .08em; }
  .lead { font:400 17px/1.5 var(--sans) !important; color:#141210 !important; }
  .winbody p { font-family:var(--sans); font-size:14px; }
  .pic { padding:0 !important; box-shadow:none !important; background:none !important; }
  .grp { border-top:1px solid #1412101f !important; }
  .grp > h4, .winbody .grp > h4 { font:500 11px/1 var(--mono) !important; letter-spacing:.12em !important; }
  .facts b, .price, .way b, .day b, .menu .lbl, .ticks, .summary b { font-family:var(--sans) !important; font-weight:600 !important; letter-spacing:-.02em; }
  .facts b { font-size:32px !important; } .price { font-size:44px !important; } .way b { font-size:22px !important; } .menu .lbl { font-size:24px !important; }
  .ticks { font:400 15px/1.9 var(--sans) !important; }
  .day, .hslot, .window .btn, .window .btn.wide, .way { background:#fff !important; color:#141210 !important; box-shadow:inset 0 0 0 1px #14121026 !important; border-radius:0 !important; }
  .day b { font-size:26px !important; }
  .day small, .hslot small { font-family:var(--mono) !important; }
  .day[aria-checked="true"], .hslot.sel { background:var(--cut) !important; color:#fff !important; box-shadow:none !important; }
  .hslot.taken, .hslot.past { background:transparent !important; color:#14121055 !important; box-shadow:inset 0 0 0 1px #1412100f !important; }
  .booking input, .booking select { background:#fff !important; box-shadow:inset 0 0 0 1px #14121033 !important; font-family:var(--sans) !important; font-size:14px !important; }
  .window .btn, .window .btn.wide { font:500 12px/1 var(--mono) !important; letter-spacing:.1em !important; text-transform:uppercase; padding:14px 18px !important; }
  .window .btn:hover { box-shadow:inset 0 0 0 1px #141210 !important; }
  .window .btn.wide, .window > .winbody > .btn { background:#141210 !important; color:#f3efe6 !important; box-shadow:none !important; }
  .summary { background:#141210 !important; color:#f3efe6 !important; font:400 14px/1.5 var(--sans) !important; }
  .summary b { font-size:22px !important; }
  .way:nth-child(2) { background:var(--cut) !important; color:#fff !important; box-shadow:none !important; }
  .pkg.premium { background:var(--cut) !important; }
  .menu button:hover .lbl { background:none !important; color:var(--cut) !important; }
  .rotate-title, .rotate-logo { font-family:var(--mono) !important; }
  body.og .top nav, body.og .hud, body.og .ptags, body.og .loader, body.og .study, body.og .hero p { display:none !important; }
  body.og .collage { opacity:1 !important; transition:none !important; }
  @media (max-height:560px) { .hero h1 { font-size:22px !important; } .hero { top:48px !important; } .logo { font-size:12px !important; } }
</style>
"""
QUIET_MARK = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
              '<rect x="3" y="17" width="26" height="9" rx="2" fill="#000080"/>'
              '<rect x="1" y="14" width="5" height="12" rx="2" fill="#000080"/><rect x="26" y="14" width="5" height="12" rx="2" fill="#000080"/>'
              '<path d="M7 17c0-6 4-10 10-10s9 4 9 8c0 2-1 3-3 3H9c-1 0-2-.5-2-1z" fill="#c8894a"/>'
              '<circle cx="13" cy="12" r="1" fill="#6b3e1c"/><circle cx="20" cy="11" r="1" fill="#6b3e1c"/><circle cx="17" cy="15" r=".9" fill="#6b3e1c"/>'
              '</svg>\n')
open(os.path.join(ROOT, "website", "mark-quiet.svg"), "w").write(QUIET_MARK)
OG = """
<meta property="og:type" content="website">
<meta property="og:site_name" content="Couch Co-Op">
<meta property="og:title" content="Couch Co-Op · A public living room for play">
<meta property="og:description" content="Co-op games and interactive art in a pop-up living room at POST Houston. Free open play daily, 10am–10pm.">
<meta property="og:url" content="https://couchco-op.com/">
<meta property="og:image" content="https://couchco-op.com/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A collage of a living room for play: floor sofas, CRT screens playing games, paper lanterns and a scaffold tower">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://couchco-op.com/og-image.jpg">
<meta name="theme-color" content="#14110e">
"""
Q = HTML.replace("</head>", QUIET_CSS + OG + "</head>", 1)
Q = Q.replace("<body>", '<body>\n<script>if (/[?&]og\\b/.test(location.search)) document.body.classList.add("og");</script>', 1)
Q = Q.replace('<img class="mark" src="favicon.svg"', '<img class="mark" src="mark-quiet.svg"', 1)
Q = Q.replace('<link rel="icon" href="favicon.svg" type="image/svg+xml">', '<link rel="icon" href="mark-quiet.svg" type="image/svg+xml">', 1)
Q = Q.replace("LOADING THE LIVING ROOM", "LOADING", 1)
Q = Q.replace("'<span class=\"open\">● OPEN NOW</span> · 10–22'", "'<span class=\"open\">Open now</span> · daily 10–22'", 1)
Q = Q.replace("'<span class=\"closed\">○ CLOSED</span> · OPEN 10–22'", "'<span class=\"closed\">Closed</span> · open daily 10–22'", 1)
open(OUT, "w").write(Q)
print("wrote index.html (quiet + REC)")
