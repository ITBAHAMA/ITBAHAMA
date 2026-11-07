#!/usr/bin/env python3
"""
Builds the "Together, We Can" pixel-art banner for the BRDC IT GitHub README.

Output: assets/together-light.svg and assets/together-dark.svg
Pure SVG + CSS keyframes (no JavaScript), so it animates on GitHub.

Edit SCENES below to change what the team says, then run:
    python3 scripts/build_together.py
"""
from pathlib import Path

# --------------------------------------------------------------------------
# What the bubble says. Each scene is a list of lines (UPPERCASE works best).
# The last scene is the big finale and is drawn larger, letter by letter.
# --------------------------------------------------------------------------
SCENES = [
    ["HI! WE'RE THE BRDC IT TEAM.", "SEVEN BUSINESS UNITS. ONE CREW."],
    ["SYSTEMS UP. TICKETS CLOSED.", "NOBODY DOES IT ALONE."],
]
FINALE = ("TOGETHER,", "WE CAN.")  # second part is drawn in the accent colour
CAPTION = "BRDC IT"

THEMES = {
    "light": dict(card="#f2efe9", stroke="#0f0f101f", ink="#0f0f10", paper="#faf8f4",
                  accent="#0b5cd5", dot="#0f0f10", dot_op=".09", drop_op=".12",
                  pants="#34405a", shoes="#3a2a20", muted="#0f0f1066"),
    "dark":  dict(card="#121316", stroke="#ffffff1f", ink="#f2efe9", paper="#1c1d22",
                  accent="#6aa6ff", dot="#ffffff", dot_op=".07", drop_op=".35",
                  pants="#4a5878", shoes="#5a4030", muted="#f2efe966"),
}

W, H = 1200, 300

# --------------------------------------------------------------------------
# 5x7 pixel font
# --------------------------------------------------------------------------
G = {
 "A": ".###.|#...#|#...#|#####|#...#|#...#|#...#",
 "B": "####.|#...#|#...#|####.|#...#|#...#|####.",
 "C": ".###.|#...#|#....|#....|#....|#...#|.###.",
 "D": "####.|#...#|#...#|#...#|#...#|#...#|####.",
 "E": "#####|#....|#....|####.|#....|#....|#####",
 "F": "#####|#....|#....|####.|#....|#....|#....",
 "G": ".###.|#...#|#....|#.###|#...#|#...#|.####",
 "H": "#...#|#...#|#...#|#####|#...#|#...#|#...#",
 "I": ".###.|..#..|..#..|..#..|..#..|..#..|.###.",
 "J": "..###|...#.|...#.|...#.|#..#.|#..#.|.##..",
 "K": "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#",
 "L": "#....|#....|#....|#....|#....|#....|#####",
 "M": "#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#",
 "N": "#...#|##..#|#.#.#|#..##|#...#|#...#|#...#",
 "O": ".###.|#...#|#...#|#...#|#...#|#...#|.###.",
 "P": "####.|#...#|#...#|####.|#....|#....|#....",
 "Q": ".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#",
 "R": "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
 "S": ".###.|#...#|#....|.###.|....#|#...#|.###.",
 "T": "#####|..#..|..#..|..#..|..#..|..#..|..#..",
 "U": "#...#|#...#|#...#|#...#|#...#|#...#|.###.",
 "V": "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
 "W": "#...#|#...#|#...#|#.#.#|#.#.#|##.##|#...#",
 "X": "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
 "Y": "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..",
 "Z": "#####|....#|...#.|..#..|.#...|#....|#####",
 "0": ".###.|#...#|#..##|#.#.#|##..#|#...#|.###.",
 "1": "..#..|.##..|..#..|..#..|..#..|..#..|.###.",
 "2": ".###.|#...#|....#|...#.|..#..|.#...|#####",
 "3": "####.|....#|....#|.###.|....#|....#|####.",
 "4": "#...#|#...#|#...#|#####|....#|....#|....#",
 "5": "#####|#....|####.|....#|....#|#...#|.###.",
 "6": ".###.|#....|#....|####.|#...#|#...#|.###.",
 "7": "#####|....#|...#.|..#..|..#..|..#..|..#..",
 "8": ".###.|#...#|#...#|.###.|#...#|#...#|.###.",
 "9": ".###.|#...#|#...#|.####|....#|....#|.###.",
 ".": ".|.|.|.|.|.|#",
 ",": ".|.|.|.|.|#|#",
 "!": "#|#|#|#|#|.|#",
 "?": ".###.|#...#|....#|...#.|..#..|.....|..#..",
 "'": "#|#|.|.|.|.|.",
 ":": ".|#|.|.|.|#|.",
 "-": "....|....|....|####|....|....|....",
 "&": ".##..|#..#.|.##..|.##.#|#..#.|#..#.|.##.#",
 " ": "...|...|...|...|...|...|...",
}
GLYPH = {k: v.split("|") for k, v in G.items()}


def text_width(s, scale):
    return sum((len(GLYPH[c][0]) + 1) * scale for c in s) - scale


def runs_to_path(cells, x0, y0, sx, sy=None):
    """cells: set of (col,row). Merge horizontal runs into one compact path."""
    sy = sy or sx
    rows = {}
    for c, r in cells:
        rows.setdefault(r, []).append(c)
    d = []
    for r in sorted(rows):
        cs = sorted(rows[r])
        start = prev = cs[0]
        for c in cs[1:] + [None]:
            if c is not None and c == prev + 1:
                prev = c
                continue
            d.append(f"M{x0 + start * sx:g} {y0 + r * sy:g}h{(prev - start + 1) * sx:g}v{sy:g}h-{(prev - start + 1) * sx:g}z")
            if c is not None:
                start = prev = c
    return "".join(d)


def glyph_cells(s):
    cells, cx = set(), 0
    for ch in s:
        g = GLYPH[ch]
        for r, row in enumerate(g):
            for c, v in enumerate(row):
                if v == "#":
                    cells.add((cx + c, r))
        cx += len(g[0]) + 1
    return cells


# --------------------------------------------------------------------------
# Pixel speech bubble on a 6px grid
# --------------------------------------------------------------------------
GRID = 6
BX0, BX1, BY0, BY1 = 50, 190, 6, 33   # bubble in grid cells (x 300..1140, y 36..198)
TAIL = {20: (47, 50), 21: (45, 50), 22: (43, 50), 23: (41, 49), 24: (39, 47),
        25: (37, 45), 26: (36, 43), 27: (35, 40), 28: (34, 37)}


def bubble_mask():
    m = set()
    for r in range(BY0, BY1):
        i = r - BY0
        j = BY1 - 1 - r
        inset = 2 if min(i, j) == 0 else 1 if min(i, j) == 1 else 0
        for c in range(BX0 + inset, BX1 - inset):
            m.add((c, r))
    for r, (a, b) in TAIL.items():
        for c in range(a, b):
            m.add((c, r))
    return m


def bubble_svg():
    m = bubble_mask()
    outline = {(c, r) for (c, r) in m
               if any((c + dc, r + dr) not in m for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    inner = m - outline
    drop = {(c + 1, r + 1) for (c, r) in m}
    return (f'<path class="drop" d="{runs_to_path(drop, 0, 0, GRID)}"/>'
            f'<path class="paper" d="{runs_to_path(inner, 0, 0, GRID)}"/>'
            f'<path class="ink" d="{runs_to_path(outline, 0, 0, GRID)}"/>')


# --------------------------------------------------------------------------
# Original pixel characters (12 x 18 cells)
# H hair  S skin  E eye  T shirt  P pants  B shoes  C cap
# --------------------------------------------------------------------------
BODY_IDLE = [
    "..TTTTTTTT..",
    ".TTTTTTTTTT.",
    ".TTTTTTTTTT.",
    ".TTTTTTTTTT.",
    ".STTTTTTTTS.",
]
BODY_CHEER = [
    "..TTTTTTTT..",
    "..TTTTTTTT..",
    "..TTTTTTTT..",
    "..TTTTTTTT..",
    "..TTTTTTTT..",
]
LEGS = [
    "..PPPPPPPP..",
    "..PPP..PPP..",
    "..PPP..PPP..",
    "..PPP..PPP..",
    ".BBBB..BBBB.",
]
HEADS = {
    "short": ["...HHHHHH...", "..HHHHHHHH..", "..HSSSSSSH..", "..SSESSESS..",
              "..SSSSSSSS..", "..SSSSSSSS..", "...SSSSSS...", "....SSSS...."],
    "long":  ["...HHHHHH...", "..HHHHHHHH..", "..HHSSSSHH..", "..HSESSESH..",
              "..HSSSSSSH..", "..HSSSSSSH..", "..HHSSSSHH..", "..H.SSSS.H.."],
    "cap":   ["...CCCCCC...", "..CCCCCCCCCC", "..HSSSSSS...", "..SSESSESS..",
              "..SSSSSSSS..", "..SSSSSSSS..", "...SSSSSS...", "....SSSS...."],
}
# arms raised beside the head for the cheer pose
CHEER_ARMS = {2: "S..........S", 3: "S..........S", 4: "T..........T",
              5: "T..........T", 6: "TT........TT", 7: ".TT......TT."}

MOUTH_CLOSED = {(5, 5), (6, 5)}
MOUTH_OPEN = {(5, 5), (6, 5), (5, 6), (6, 6), (4, 5), (7, 5)}
MOUTH_CHEER = {(4, 5), (5, 5), (6, 5), (7, 5), (5, 6), (6, 6), (3, 4), (8, 4)}

CREW = [  # head style, hair, skin, shirt
    ("short", "#1b1b1f", "#e0ac69", "accent"),
    ("long",  "#5a3a22", "#c68642", "#e8a33d"),
    ("cap",   "#2a2016", "#f1c27d", "#3f8f5a"),
]
CAP_COL = "#d6453d"
PX = 5
CHAR_X = [44, 112, 180]
CHAR_Y = 180


def sprite(rows, colors):
    by_col = {}
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in colors:
                by_col.setdefault(colors[ch], set()).add((c, r))
    return by_col


def char_layers(style, hair, skin, shirt, theme):
    head = HEADS[style]
    colors = {"H": hair, "S": skin, "E": "#0f0f10", "T": shirt, "P": theme["pants"],
              "B": theme["shoes"], "C": CAP_COL}
    idle = head + BODY_IDLE + LEGS
    cheer = [list(r) for r in head + BODY_CHEER + LEGS]
    for r, s in CHEER_ARMS.items():
        for c, ch in enumerate(s):
            if ch != ".":
                cheer[r][c] = ch
    cheer = ["".join(r) for r in cheer]
    return sprite(idle, colors), sprite(cheer, colors)


def paths(by_col, x0, y0):
    return "".join(f'<path fill="{col}" d="{runs_to_path(cells, x0, y0, PX)}"/>'
                   for col, cells in by_col.items())


HEART = [".#.#.", "#####", "#####", ".###.", "..#.."]
SPARK = [".#.", "###", ".#."]


def shape_path(rows, x0, y0, s):
    return runs_to_path({(c, r) for r, row in enumerate(rows) for c, v in enumerate(row) if v == "#"},
                        x0, y0, s)


# --------------------------------------------------------------------------
# Timeline
# --------------------------------------------------------------------------
WORD_GAP, LINE_GAP, HOLD, SCENE_GAP = 0.28, 0.35, 2.4, 0.35
LETTER_GAP, FINALE_HOLD, LOOP_PAUSE = 0.09, 4.2, 0.6


def build_timeline():
    t = 0.3
    scenes = []
    for lines in SCENES:
        words, start = [], t
        for li, line in enumerate(lines):
            if li:
                t += LINE_GAP
            for w in line.split(" "):
                words.append((li, w, t))
                t += WORD_GAP
        talk_end = t
        end = t + HOLD
        scenes.append(dict(words=words, start=start, talk_end=talk_end, end=end))
        t = end + SCENE_GAP
    fin_start = t
    letters = []
    full = FINALE[0] + " " + FINALE[1]
    for i, ch in enumerate(full):
        letters.append((i, ch, t))
        if ch != " ":
            t += LETTER_GAP
    fin_end = t + FINALE_HOLD
    total = fin_end + LOOP_PAUSE
    return scenes, (fin_start, letters, fin_end), total


def pct(t, total):
    return f"{100 * t / total:.3f}%"


def build(theme_name):
    th = THEMES[theme_name]
    scenes, (fin_start, letters, fin_end), T = build_timeline()
    css, body = [], []
    dur = f"{T:.2f}s"

    def kf(name, frames, base_opacity="0"):
        steps = "".join(f"{p}{{{v}}}" for p, v in frames)
        css.append(f"@keyframes {name}{{{steps}}}"
                   f".{name}{{opacity:{base_opacity};animation:{name} {dur} step-end infinite}}")

    # --- scene words
    s_body = 4
    adv_line = 7 * s_body + 20
    text_x = BX0 * GRID + 36
    cy = (BY0 + BY1) * GRID / 2
    for si, sc in enumerate(scenes):
        nlines = max(li for li, _, _ in sc["words"]) + 1
        top = cy - (nlines * 7 * s_body + (nlines - 1) * 20) / 2
        xcur = {}
        for wi, (li, w, t) in enumerate(sc["words"]):
            x = xcur.get(li, text_x)
            name = f"w{si}_{wi}"
            kf(name, [("0%", "opacity:0"), (pct(t, T), "opacity:1"), (pct(sc["end"], T), "opacity:0")])
            body.append(f'<path class="ink {name}" d="{runs_to_path(glyph_cells(w), x, top + li * adv_line, s_body)}"/>')
            xcur[li] = x + text_width(w + " ", s_body) + s_body
    # --- finale, letter by letter with a little pop
    s_fin = 6
    full = FINALE[0] + " " + FINALE[1]
    fx = (BX0 + BX1) * GRID / 2 - text_width(full, s_fin) / 2
    fy = cy - 7 * s_fin / 2
    x = fx
    for i, ch, t in letters:
        if ch != " ":
            cls = "acc" if i > len(FINALE[0]) else "ink"
            name = f"f{i}"
            kf(name, [("0%", "opacity:0;transform:translateY(0)"),
                      (pct(t, T), "opacity:1;transform:translateY(-6px)"),
                      (pct(t + 0.12, T), "opacity:1;transform:translateY(0)"),
                      (pct(fin_end, T), "opacity:0;transform:translateY(0)")])
            body.append(f'<path class="{cls} fin {name}" d="{runs_to_path(glyph_cells(ch), x, fy, s_fin)}"/>')
        x += (len(GLYPH[ch][0]) + 1) * s_fin
    # underline that draws in under the finale
    ul_y = fy + 7 * s_fin + 12
    ul_w = text_width(full, s_fin)
    ul_t = letters[-1][2] + 0.2
    segs = 12
    for k in range(segs):
        name = f"ul{k}"
        tk = ul_t + k * 0.04
        kf(name, [("0%", "opacity:0"), (pct(tk, T), "opacity:1"), (pct(fin_end, T), "opacity:0")])
        sw = ul_w / segs
        body.append(f'<rect class="acc fin {name}" x="{fx + k * sw:.1f}" y="{ul_y:.1f}" width="{sw - 2:.1f}" height="6"/>')

    # --- sparkles in the finale
    spark_pos = [(318, 54), (1100, 54), (1100, 160), (330, 168)]
    for k, (sx, sy) in enumerate(spark_pos):
        frames = [("0%", "opacity:0")]
        t = fin_start + 0.3 + k * 0.18
        while t < fin_end - 0.2:
            frames += [(pct(t, T), "opacity:1"), (pct(t + 0.35, T), "opacity:0")]
            t += 1.1
        kf(f"sp{k}", frames)
        body.append(f'<path class="acc sp{k}" d="{shape_path(SPARK, sx, sy, 6)}"/>')

    # --- crew
    talk_frames = [("0%", "opacity:0")]
    for sc in scenes:
        t = sc["start"]
        while t < sc["talk_end"]:
            talk_frames += [(pct(t, T), "opacity:1"), (pct(t + 0.14, T), "opacity:0")]
            t += 0.28
    cheer_on = fin_start + 0.2
    pose_idle = [("0%", "opacity:1"), (pct(cheer_on, T), "opacity:0"), (pct(fin_end, T), "opacity:1")]
    pose_cheer = [("0%", "opacity:0"), (pct(cheer_on, T), "opacity:1"), (pct(fin_end, T), "opacity:0")]
    kf("idle", pose_idle, "1")
    kf("cheer", pose_cheer)
    kf("talk", talk_frames)

    crew_svg = []
    for k, (style, hair, skin, shirt) in enumerate(CREW):
        shirt = th["accent"] if shirt == "accent" else shirt
        idle, cheer = char_layers(style, hair, skin, shirt, th)
        x0, y0 = CHAR_X[k], CHAR_Y
        # hop during the finale, staggered per character
        hop = [("0%", "transform:translateY(0)")]
        t = cheer_on + k * 0.15
        while t < fin_end - 0.3:
            hop += [(pct(t, T), "transform:translateY(-10px)"), (pct(t + 0.2, T), "transform:translateY(0)")]
            t += 0.6
        name = f"hop{k}"
        steps = "".join(f"{p}{{{v}}}" for p, v in hop)
        css.append(f"@keyframes {name}{{{steps}}}.{name}{{animation:{name} {dur} step-end infinite}}")
        # floating heart
        hf = [("0%", "opacity:0;transform:translateY(0)")]
        t0 = cheer_on + 0.4 + k * 0.5
        while t0 < fin_end - 1.2:
            for step in range(5):
                hf.append((pct(t0 + step * 0.16, T), f"opacity:1;transform:translateY({-6 * step}px)"))
            hf.append((pct(t0 + 0.8, T), "opacity:0;transform:translateY(0)"))
            t0 += 1.5
        kf(f"ht{k}", hf)
        crew_svg.append(
            f'<rect class="ink" opacity=".10" x="{x0 + 4}" y="{y0 + 18 * PX + 2}" width="{12 * PX - 8}" height="6"/>'
            f'<g class="{name}">'
            f'<g class="idle">{paths(idle, x0, y0)}</g>'
            f'<g class="cheer">{paths(cheer, x0, y0)}</g>'
            f'<path fill="#0f0f10" d="{runs_to_path(MOUTH_CLOSED, x0, y0, PX)}"/>'
            f'<path class="talk" fill="#3a0f12" d="{runs_to_path(MOUTH_OPEN, x0, y0, PX)}"/>'
            f'<path class="cheer" fill="#3a0f12" d="{runs_to_path(MOUTH_CHEER, x0, y0, PX)}"/>'
            f'</g>'
            f'<path class="ht{k}" fill="#e5484d" d="{shape_path(HEART, x0 + 20, y0 - 34, 4)}"/>'
        )

    caption_w = text_width(CAPTION, 2)
    caption = (f'<path fill="{th["muted"]}" d="{runs_to_path(glyph_cells(CAPTION), W - 40 - caption_w, H - 34, 2)}"/>')

    label = " / ".join(" ".join(s) for s in SCENES) + " / " + " ".join(FINALE)
    style = (
        f".ink{{fill:{th['ink']}}}.acc{{fill:{th['accent']}}}.paper{{fill:{th['paper']}}}"
        f".drop{{fill:#0f0f10;opacity:{th['drop_op']}}}"
        + "".join(css)
        + "@media (prefers-reduced-motion:reduce){*{animation:none!important}"
          "[class*=' w'],[class^='w']{opacity:0!important}.fin{opacity:1!important}"
          ".cheer{opacity:1!important}.idle{opacity:0!important}}"
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Pixel BRDC IT crew in a speech bubble: {label}">
<title>{label}</title>
<defs>
<style>{style}</style>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="1" fill="{th['dot']}"/></pattern>
<linearGradient id="fade" x1="1" x2="0"><stop offset=".3" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>
<mask id="dotmask"><rect width="{W}" height="{H}" fill="url(#fade)" opacity="{th['dot_op']}"/></mask>
<clipPath id="card"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24"/></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24" fill="{th['card']}" stroke="{th['stroke']}" stroke-width="2"/>
<rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#dotmask)" clip-path="url(#card)"/>
{''.join(crew_svg)}
{bubble_svg()}
{''.join(body)}
{caption}
</svg>
'''
    return svg, T


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    (root / "assets").mkdir(exist_ok=True)
    for name in THEMES:
        svg, T = build(name)
        out = root / "assets" / f"together-{name}.svg"
        out.write_text(svg)
        print(f"{out.name}: {len(svg) / 1024:.1f} KB, loop {T:.1f}s")
