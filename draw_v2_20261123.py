#!/usr/bin/env python3
"""Entry image v2 for make.fun news-image-20261123 (Monday 23 Nov 2026).
Improved from v1 following the 22 Nov final judge commentary: larger
type, cleaner panels, more white space, simple flat illustrations,
a dotted world map + UTC table, and CLAIM vs REPORTED tagging.
Newspaper style, big date, DATE CHECK strip and reader poll kept
from our earlier v4/v1. Total items: 39 = 3 lead + 4 numbers +
18 regional + 3 science + 8 in brief + 3 sport.
All stories verified for 23 Nov 2026 from sources read directly
(One Turn day report, BBC, Reuters, AP, Al Jazeera items).
Output: news-2026-11-23-v2.png (1024x1024, <=1MiB). v1 untouched.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
FD = "/usr/share/fonts/truetype/noto"
S_BLACK = f"{FD}/NotoSerif-Black.ttf"
S_BOLD = f"{FD}/NotoSerif-Bold.ttf"
XBOLD = f"{FD}/NotoSans-ExtraBold.ttf"
BOLD = f"{FD}/NotoSans-Bold.ttf"
SEMI = f"{FD}/NotoSans-SemiBold.ttf"
REG = f"{FD}/NotoSans-Regular.ttf"

PAPER = (247, 243, 233)
CARD = (255, 253, 247)
INK = (16, 17, 22)
MUTED = (82, 84, 94)
RED = (178, 24, 38)
TEAL = (8, 118, 110)
BLUE = (28, 78, 160)
GREEN = (28, 120, 62)
PURPLE = (104, 62, 168)
ORANGE = (196, 92, 16)
DARK = (14, 16, 24)
WHITE = (246, 248, 251)
DMUTED = (168, 178, 198)
CLAIMC = (196, 92, 16)

def F(p, s): return ImageFont.truetype(p, s)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def block(draw, xy, text, fnt, fill, max_w, leading=1.16, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    if max_lines: lines = lines[:max_lines]
    lh = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill); y += lh
    return y

def pill(draw, x, y, text, color):
    f = F(BOLD, 9)
    w = draw.textlength(text, font=f) + 10
    draw.rounded_rectangle([x, y, x + w, y + 14], radius=4, fill=color)
    draw.text((x + 5, y + 2), text, font=f, fill=(255, 255, 255))
    return w

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 24

# ---------- masthead ----------
d.text((M, 2), "The World in One Day", font=F(S_BLACK, 52), fill=INK)
r = "ONE PAGE  •  EVERY REGION"
d.text((W - M - d.textlength(r, font=F(XBOLD, 15)), 30), r, font=F(XBOLD, 15), fill=RED)
d.rectangle([M, 68, W - M, 71], fill=INK)
d.rectangle([M, 74, W - M, 75], fill=INK)
# date band
d.rectangle([M, 82, W - M, 136], fill=INK)
d.text((M + 14, 92), "MONDAY, 23 NOVEMBER 2026", font=F(XBOLD, 33), fill=(255, 255, 255))
r = "39 STORIES"
d.text((W - M - 14 - d.textlength(r, font=F(XBOLD, 20)), 100), r, font=F(XBOLD, 20), fill=(240, 196, 92))

# ---------- lead ----------
LY = 148
d.rectangle([M, LY, 618, LY + 168], fill=CARD)
d.rectangle([M, LY, 618, LY + 6], fill=RED)
d.text((M + 18, LY + 15), "TECH & MARKETS  •  SANTA CLARA, USA", font=F(BOLD, 13.5), fill=RED)
d.text((M + 18, LY + 36), "Nvidia brings back", font=F(S_BLACK, 40), fill=INK)
d.text((M + 18, LY + 82), "Jensen Huang as CEO", font=F(S_BLACK, 40), fill=RED)
block(d, (M + 18, LY + 130),
      "Reinstated 11 days after he quit. Shares leap about 31% and Wall Street surges.",
      F(SEMI, 14.5), (52, 54, 62), 430, max_lines=2)
# chip icon (bigger)
cx, cy = 500, LY + 122
d.rectangle([cx, cy, cx + 72, cy + 38], outline=INK, width=3)
d.rectangle([cx + 16, cy + 9, cx + 56, cy + 29], fill=TEAL)
for i in range(4):
    xx = cx + 7 + i * 16
    d.line([xx, cy - 8, xx, cy], fill=INK, width=3)
    d.line([xx, cy + 38, xx, cy + 46], fill=INK, width=3)

def dark_card(y, tag, color, head, body, icon=None, claim=False):
    d.rectangle([634, y, W - M, y + 81], fill=DARK)
    d.rectangle([634, y, 638, y + 81], fill=color)
    d.text((652, y + 8), tag, font=F(BOLD, 11.5), fill=color)
    if claim:
        pill(d, 652 + d.textlength(tag, font=F(BOLD, 11.5)) + 8, y + 6, "CLAIM", CLAIMC)
    block(d, (652, y + 26), head, F(XBOLD, 19), WHITE, 330, leading=1.05, max_lines=1)
    block(d, (652, y + 52), body, F(REG, 12), DMUTED, 262, leading=1.14, max_lines=2)
    if icon == "ship":
        sx, sy = 928, y + 46
        d.polygon([(sx, sy + 14), (sx + 52, sy + 14), (sx + 44, sy + 24), (sx + 8, sy + 24)], fill=(120, 170, 220))
        d.rectangle([sx + 18, sy + 2, sx + 34, sy + 14], fill=(120, 170, 220))
        d.line([sx + 26, sy - 6, sx + 26, sy + 2], fill=(120, 170, 220), width=3)
        for wx in (sx - 2, sx + 18, sx + 38):
            d.arc([wx, sy + 26, wx + 16, sy + 34], 0, 180, fill=(120, 170, 220), width=2)
    if icon == "flame":
        sx, sy = 950, y + 40
        d.polygon([(sx, sy + 28), (sx - 10, sy + 12), (sx - 4, sy + 2), (sx + 2, sy - 8),
                   (sx + 8, sy + 2), (sx + 14, sy + 10), (sx + 10, sy + 28)], fill=(240, 140, 40))
        d.ellipse([sx - 3, sy + 16, sx + 7, sy + 28], fill=(240, 200, 80))

dark_card(LY, "WAR  •  BENGHAZI, LIBYA", (240, 84, 96), "Ukraine sinks Russian corvette",
          "Seven naval drones sink the Merkury in port — Kyiv's first admitted Mediterranean strike.", icon="ship")
dark_card(LY + 87, "WAR  •  STRAIT OF HORMUZ", (240, 196, 92), "Iran vows to defy US blockade",
          "Tehran says it will use all means. Iranian media report tankers hit by mines.", icon="flame", claim=True)

# ---------- by the numbers ----------
NY = 328
d.rectangle([M, NY, W - M, NY + 38], fill=(238, 231, 214))
nums = [("+4.7%", "S&P 500 jumps in the big rebound"),
        ("-5.06%", "Japan's Nikkei falls as Asia slides"),
        ("-4%", "oil falls nearly 4% as supply returns"),
        ("$44B", "CrowdStrike deal to buy Zscaler")]
x = M + 12
for big, small in nums:
    d.text((x, NY + 7), big, font=F(S_BLACK, 21), fill=RED)
    bw = d.textlength(big, font=F(S_BLACK, 21))
    block(d, (x + bw + 8, NY + 6), small, F(SEMI, 10.5), (52, 54, 62), 132, leading=1.1, max_lines=2)
    x += 245

# ---------- regions: 6 blocks x 3, larger type ----------
REGIONS = [
    ("EUROPE", BLUE, [
        ("NATO pledges space defence", "Berlin vows to defend every inch, after reports of a Russian nuclear satellite.", None),
        ("Belgium strike shuts airports", "National strike grounds flights; 429 Brussels flights cancelled.", None),
        ("Burnham defends EU deal", "UK PM tells MPs closer EU ties could make the next decade better.", None),
    ]),
    ("MIDDLE EAST", RED, [
        ("Houthis say refinery hit", "Group claims an attack on Saudi Arabia's Rabigh refinery.", "CLAIM"),
        ("Gaza: UN worker killed", "A UN relief worker is killed in a strike; Oxfam calls Gaza a toxic wasteland.", None),
        ("Israel coalition talks fail", "Netanyahu and Eisenkot parties end talks with no deal.", None),
    ]),
    ("ASIA-PACIFIC", PURPLE, [
        ("Factory fire kills 24", "Banten candy plant blaze in Indonesia: 24 dead, about 30 missing.", None),
        ("India pledges $1.6B to Nepal", "Delhi deals on rail, hydropower and flood rebuilding.", None),
        ("Singapore–China: 29 deals", "A record number of agreements at the joint council in Singapore.", None),
    ]),
    ("AMERICAS", GREEN, [
        ("Democrats win 258 seats", "Largest US House majority since 1992, after a North Carolina flip.", None),
        ("Congressman Gomez to resign", "California Democrat quits after an ethics finding on misconduct.", None),
        ("States sue SpaceX over Grok", "Virginia and Oregon sue over sexualised images from the chatbot.", None),
    ]),
    ("AFRICA", ORANGE, [
        ("Nigeria funeral boat sinks", "At least 24 mourners die in Bayelsa; overcrowding blamed.", None),
        ("Kenya & DR Congo restore ties", "Presidents Ruto and Tshisekedi agree full diplomatic relations.", None),
        ("South Sudan attack kills 24", "Paramilitary raid on Tonj East kills 24, including seven children.", None),
    ]),
    ("UKRAINE & RUSSIA", (150, 30, 90), [
        ("Dymer toll rises to 11", "A boy, 7, and a woman, 79, are pulled alive from the rubble.", None),
        ("Russian ship towed in Baltic", "Freighter Sparta II reaches St Petersburg after a drone strike.", None),
        ("EU plans 22nd sanctions", "New package targets crypto and ex-combatants' visas.", None),
    ]),
]
RY = 378
RW, RH, RG = 318, 154, 7
for i, (name, color, stories) in enumerate(REGIONS):
    cx = M + (i % 3) * (RW + RG); cy = RY + (i // 3) * (RH + 8)
    d.rectangle([cx, cy, cx + RW, cy + RH], fill=CARD)
    d.rectangle([cx, cy, cx + RW, cy + 23], fill=color)
    d.text((cx + 10, cy + 4), name, font=F(XBOLD, 13), fill=(255, 255, 255))
    sy = cy + 31
    for head, body, tag in stories:
        hw = block(d, (cx + 10, sy), head, F(S_BOLD, 14.5), INK, RW - 20, leading=1.0, max_lines=1)
        if tag:
            tw = d.textlength(head, font=F(S_BOLD, 14.5))
            pill(d, cx + 10 + tw + 7, sy + 1, tag, CLAIMC)
        block(d, (cx + 10, sy + 18), body, F(REG, 11.5), MUTED, RW - 20, leading=1.12, max_lines=2)
        sy += 42

# ---------- science band ----------
SY0 = RY + 2 * (RH + 8) + 4  # 722
d.rectangle([M, SY0, W - M, SY0 + 58], fill=CARD)
d.rectangle([M, SY0, M + 6, SY0 + 58], fill=TEAL)
d.text((M + 16, SY0 + 6), "SCIENCE & SPACE", font=F(XBOLD, 12.5), fill=TEAL)
SCI = [
    ("BepiColombo orbits Mercury", "ESA–JAXA probes arrive, eight years after launch."),
    ("Claimed proof of Riemann puzzle", "Posted by an Anthropic mathematician; not yet verified."),
    ("Cancer drug shrinks tumours", "In a pancreatic trial, some tumours vanish."),
]
sx = M + 16
for j, (head, body) in enumerate(SCI):
    x0 = M + 16 + j * 328
    if j == 1:
        block(d, (x0, SY0 + 24), head, F(S_BOLD, 13.5), INK, 240, leading=1.0, max_lines=1)
        tw = d.textlength(head, font=F(S_BOLD, 13.5))
        pill(d, x0 + tw + 7, SY0 + 25, "CLAIM", CLAIMC)
    else:
        block(d, (x0, SY0 + 24), head, F(S_BOLD, 13.5), INK, 312, leading=1.0, max_lines=1)
    block(d, (x0, SY0 + 40), body, F(REG, 11), MUTED, 312, leading=1.1, max_lines=1)

# ---------- date check + tag legend ----------
DY = SY0 + 66
d.rectangle([M, DY, W - M, DY + 34], fill=(238, 231, 214))
d.text((M + 10, DY + 4), "DATE CHECK:  MONDAY 23 NOVEMBER 2026  •  Every story happened or was first reported on this day, in some timezone",
       font=F(BOLD, 11), fill=(52, 54, 62))
d.text((M + 10, DY + 20), "TAGS:", font=F(BOLD, 10.5), fill=(52, 54, 62))
pill(d, M + 52, DY + 19, "CLAIM", CLAIMC)
d.text((M + 108, DY + 20), "= one side's claim, not independently confirmed.  No tag = reported by news agencies.",
       font=F(SEMI, 10.5), fill=(52, 54, 62))

# ---------- bottom: map/UTC left, in brief right ----------
BY = DY + 42
# map panel
d.rectangle([M, BY, M + 478, BY + 106], fill=CARD)
d.text((M + 12, BY + 7), "THE DAY AROUND THE WORLD", font=F(XBOLD, 12.5), fill=INK)
MAP = [
    "                                                              ",
    "        ####                                                  ",
    "   ##########        ###   ###############                    ",
    "  ############      #############################             ",
    "   #########         ###############################          ",
    "    #######           ##################  ##########          ",
    "     #####     ##      ################    ########           ",
    "      ###     ####      ##############      ######            ",
    "       ##    ######      ############        ####             ",
    "            ########      ##########                          ",
    "            ########       ########         #####             ",
    "             ######         ######         ########           ",
    "             #####          #####           ######            ",
    "              ###           ####             ####             ",
    "              ##            ###                               ",
    "                                                              ",
]
mx, my = M + 16, BY + 28
for ri, row in enumerate(MAP):
    for ci, ch in enumerate(row):
        if ch == "#":
            d.ellipse([mx + ci * 7, my + ri * 4, mx + ci * 7 + 3, my + ri * 4 + 3], fill=(140, 165, 190))
PINS = [(5, 5, "Santa Clara"), (33, 4, "Kyiv"), (30, 9, "Benghazi"),
        (39, 8, "Hormuz"), (48, 12, "Banten"), (28, 11, "Nigeria")]
for pc, pr, _ in PINS:
    x0, y0 = mx + pc * 7, my + pr * 4
    d.ellipse([x0 - 3, y0 - 3, x0 + 5, y0 + 5], fill=RED)
d.text((M + 12, BY + 93), "Pins:  Santa Clara  •  Kyiv  •  Benghazi  •  Hormuz  •  Nigeria  •  Banten",
       font=F(SEMI, 10), fill=MUTED)
# UTC table under map panel
UY = BY + 112
d.text((M, UY), "12:00 UTC, MON 23 NOV —  Los Angeles 04:00  •  London 12:00  •  Dubai 16:00  •  Tokyo 21:00",
       font=F(BOLD, 10), fill=(52, 54, 62))

# in brief
BX = M + 492
BW = W - M - BX
d.text((BX, BY), "ALSO ON 23 NOVEMBER — IN BRIEF", font=F(XBOLD, 14.5), fill=INK)
d.rectangle([BX, BY + 21, W - M, BY + 23], fill=INK)
BRIEFS = [
    "US blacklists AI firm Megaspeed over chips to China",
    "US sanctions Iran 'shadow banking': 8 people, 22 entities",
    "Spain's top court grants amnesty to Puigdemont",
    "Capita shares plunge 70% as chief quits over pensions",
    "ConocoPhillips exits Norway in a $4.4B sale",
    "European gas prices jump 8.6% on cold forecasts",
    "WFP: wars put food aid for 7.3M more people at risk",
    "12,000 evacuated at a Manchester concert",
]
cols = [BRIEFS[0:4], BRIEFS[4:8]]
for ci, col in enumerate(cols):
    x = BX + ci * (BW // 2 + 2); y = BY + 29
    for it in col:
        d.rectangle([x, y + 4, x + 6, y + 10], fill=RED)
        yend = block(d, (x + 12, y), it, F(SEMI, 11), (30, 31, 38), BW // 2 - 14, leading=1.1, max_lines=2)
        y = yend + 3

# ---------- sport + poll ----------
PY = 956
d.rectangle([M, PY, 690, PY + 44], fill=INK)
d.text((M + 12, PY + 13), "SPORT", font=F(XBOLD, 13.5), fill=(240, 196, 92))
d.text((M + 80, PY + 5), "•  Alcaraz wins first ATP Finals title  •  Márquez takes 8th MotoGP crown", font=F(SEMI, 11), fill=(255, 255, 255))
d.text((M + 80, PY + 24), "•  UK confirmed as host of the 2035 Women's World Cup", font=F(SEMI, 11), fill=(255, 255, 255))
PX0 = 698
d.rectangle([PX0, PY, W - M, PY + 44], outline=INK, width=2)
d.rectangle([PX0, PY, W - M, PY + 18], fill=RED)
d.text((PX0 + 8, PY + 3), "READER POLL — Which story defined the day?", font=F(XBOLD, 10), fill=(255, 255, 255))
d.text((PX0 + 8, PY + 22), "☐ Huang returns   ☐ Merkury sunk   ☐ Dymer", font=F(SEMI, 10.5), fill=(30, 31, 38))

src = "Sources: BBC • Reuters • AP • Al Jazeera • The Guardian • CNBC • France 24 • One Turn day report — every story dated Monday 23 November 2026"
d.text((M, PY + 50), src, font=F(REG, 9.5), fill=MUTED)

out = "/home/hatch/workspace/makefun/work/news-2026-11-23-v2.png"
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
