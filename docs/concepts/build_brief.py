"""Builds the two-concept game brief as HTML (then printed to PDF by Chromium).
All mockup art is hand-made SVG — placeholder proof-of-concept only."""
import html

OUT = "Two_Small_Roguelites_Concept_Brief.html"

# ---------- SVG helpers ----------
W, H = 230, 470  # phone screen size


def phone(inner, bg1, bg2, caption, w=W, h=H):
    gid = "g" + str(abs(hash(caption)) % 10**8)
    return f"""
<div class="shot">
<svg viewBox="0 0 {w+16} {h+16}" width="{w+16}" height="{h+16}" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">
  <defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient>
    <clipPath id="c{gid}"><rect x="8" y="8" width="{w}" height="{h}" rx="22"/></clipPath></defs>
  <rect x="0" y="0" width="{w+16}" height="{h+16}" rx="28" fill="#05070c" stroke="#2a3346" stroke-width="2"/>
  <g clip-path="url(#c{gid})">
    <rect x="8" y="8" width="{w}" height="{h}" fill="url(#{gid})"/>
    <g transform="translate(8,8)">{inner}</g>
  </g>
</svg>
<div class="cap">{caption}</div>
</div>"""


def pill(x, y, w, h, fill, text="", tc="#fff", fs=11, stroke=None, weight=800):
    s = f'stroke="{stroke}" stroke-width="2"' if stroke else ""
    t = (f'<text x="{x+w/2}" y="{y+h/2+fs*0.36}" text-anchor="middle" font-size="{fs}" '
         f'font-weight="{weight}" fill="{tc}">{html.escape(text)}</text>') if text else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}" {s}/>{t}'


def box(x, y, w, h, fill, r=10, stroke=None, sw=2, op=1):
    s = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {s} opacity="{op}"/>'


def txt(x, y, s, fs=11, fill="#fff", weight=700, anchor="middle", op=1):
    return (f'<text x="{x}" y="{y}" font-size="{fs}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" opacity="{op}">{html.escape(s)}</text>')


def topbar(level, cur1, cur2, accent):
    return (f'<polygon points="14,14 34,8 54,14 54,36 34,44 14,36" fill="{accent}" stroke="#fff" stroke-width="2"/>'
            + txt(34, 31, str(level), 13, "#fff", 900)
            + pill(62, 16, 70, 18, "#00000066", "", stroke="#ffffff33")
            + box(64, 19, 40, 12, accent, 6)
            + pill(140, 14, 40, 20, "#00000066", cur1, "#ffd76a", 10)
            + pill(184, 14, 40, 20, "#00000066", cur2, "#8fe8ff", 10))


def bottomnav(labels, active=2, bg="#1b1426", hi="#e0a73a"):
    out = box(0, H - 54, W, 54, bg, 0)
    n = len(labels)
    cw = W / n
    for i, l in enumerate(labels):
        cx = cw * i + cw / 2
        if i == active:
            out += box(cx - 26, H - 60, 52, 56, hi, 10, "#fff", 2)
            out += f'<polygon points="{cx-9},{H-44} {cx+9},{H-26} {cx+9},{H-44} {cx-9},{H-26}" fill="none" stroke="#2a1a05" stroke-width="3"/>'
            out += txt(cx, H - 12, l, 8, "#2a1a05", 900)
        else:
            out += f'<circle cx="{cx}" cy="{H-34}" r="10" fill="#ffffff22" stroke="#ffffff55" stroke-width="1.5"/>'
            out += txt(cx, H - 12, l, 8, "#ffffffaa", 700)
    return out


def chibi(cx, cy, body, skin="#f2c9a0", hat=None, s=1.0):
    g = f'<g transform="translate({cx},{cy}) scale({s})">'
    g += '<ellipse cx="0" cy="30" rx="16" ry="4" fill="#00000055"/>'
    g += f'<rect x="-10" y="4" width="20" height="24" rx="7" fill="{body}" stroke="#1a1020" stroke-width="2"/>'
    g += f'<circle cx="0" cy="-6" r="13" fill="{skin}" stroke="#1a1020" stroke-width="2"/>'
    g += '<circle cx="-4" cy="-6" r="2" fill="#1a1020"/><circle cx="4" cy="-6" r="2" fill="#1a1020"/>'
    if hat == "wizard":
        g += f'<polygon points="-14,-12 14,-12 4,-38" fill="#5b3fd1" stroke="#1a1020" stroke-width="2"/>'
    elif hat == "helm":
        g += '<path d="M-14,-8 A14,14 0 0 1 14,-8 Z" fill="#9aa4b5" stroke="#1a1020" stroke-width="2"/>'
    elif hat == "hood":
        g += '<path d="M-15,-4 A15,16 0 0 1 15,-4 L11,-10 A11,10 0 0 0 -11,-10 Z" fill="#2f6b3e" stroke="#1a1020" stroke-width="2"/>'
    elif hat == "goggles":
        g += '<rect x="-12" y="-12" width="24" height="7" rx="3" fill="#3cc6c0" stroke="#1a1020" stroke-width="2"/>'
    elif hat == "mask":
        g += '<rect x="-11" y="-4" width="22" height="9" rx="3" fill="#3a3a3a" stroke="#1a1020" stroke-width="2"/>'
    return g + "</g>"


def d20(cx, cy, r, fill, label, tc="#fff"):
    import math
    pts = " ".join(f"{cx + r*math.cos(math.radians(a))},{cy + r*math.sin(math.radians(a))}" for a in range(-90, 270, 60))
    inner = " ".join(f"{cx + r*0.55*math.cos(math.radians(a))},{cy + r*0.55*math.sin(math.radians(a))}" for a in (-90, 30, 150))
    return (f'<polygon points="{pts}" fill="{fill}" stroke="#1a1020" stroke-width="2"/>'
            f'<polygon points="{inner}" fill="#ffffff22" stroke="#1a1020" stroke-width="1.2"/>'
            + txt(cx, cy + r * 0.2, label, r * 0.55, tc, 900))


def card(x, y, w, h, top, title, cost, rarity="#4fb6ff", icon=""):
    return (box(x, y, w, h, rarity, 8, "#fff", 2)
            + box(x + 5, y + 5, w - 10, h * 0.52, top, 6)
            + icon
            + txt(x + w / 2, y + h * 0.68, title.split("|")[0], 8.5, "#fff", 900)
            + (txt(x + w / 2, y + h * 0.68 + 11, title.split("|")[1], 8.5, "#fff", 900) if "|" in title else "")
            + pill(x + 6, y + h + 8, w - 12, 17, "#c0267a", cost, "#fff", 9))


def truck(x, y, s=1.0, parts=True):
    g = f'<g transform="translate({x},{y}) scale({s})">'
    g += '<ellipse cx="60" cy="62" rx="70" ry="7" fill="#00000055"/>'
    g += '<rect x="0" y="18" width="80" height="36" rx="4" fill="#8a5a2b" stroke="#1b120a" stroke-width="3"/>'
    g += '<rect x="80" y="26" width="40" height="28" rx="4" fill="#b8733a" stroke="#1b120a" stroke-width="3"/>'
    g += '<rect x="88" y="30" width="20" height="12" fill="#7fd4e0" stroke="#1b120a" stroke-width="2"/>'
    g += '<line x1="6" y1="28" x2="74" y2="28" stroke="#5d3b1a" stroke-width="3"/>'
    g += '<line x1="6" y1="40" x2="74" y2="40" stroke="#5d3b1a" stroke-width="3"/>'
    for cx in (20, 58, 102):
        g += f'<circle cx="{cx}" cy="56" r="11" fill="#222" stroke="#1b120a" stroke-width="3"/><circle cx="{cx}" cy="56" r="4" fill="#888"/>'
    if parts:
        g += '<polygon points="120,34 136,44 120,54" fill="#c9c9c9" stroke="#1b120a" stroke-width="2"/>'  # plow
        g += '<rect x="22" y="4" width="34" height="10" rx="3" fill="#555" stroke="#1b120a" stroke-width="2"/>'
        g += '<rect x="50" y="6" width="26" height="5" fill="#333"/>'  # gun barrel
        g += '<circle cx="30" cy="9" r="7" fill="#e2572b" stroke="#1b120a" stroke-width="2"/>'
    return g + "</g>"


def raider(cx, cy, s=1.0, col="#c04030"):
    return chibi(cx, cy, col, "#d9b08c", "mask", s)


# ---------- Concept A mockups (Delve & Dice) ----------
A1, A2 = "#3a2350", "#140c1f"
ACC = "#e0a73a"


def a_hub():
    i = topbar(4, "1.2K", "38", "#7b4fd1")
    i += pill(14, 52, 92, 22, "#4b2f72", "Tavern", "#fff", 10, "#ffffff55")
    i += pill(112, 52, 104, 22, ACC, "Daily Delve 2/3", "#2a1a05", 9, "#fff")
    i += txt(W / 2, 98, "FLOOR 7", 22, "#fff", 900)
    i += txt(W / 2, 114, "THE SUNKEN CRYPT", 13, ACC, 900)
    i += '<g transform="translate(0,-8)">'
    # dungeon arch
    i += '<path d="M55,290 L55,185 A60,60 0 0 1 175,185 L175,290 Z" fill="#2a1c38" stroke="#6d5a86" stroke-width="5"/>'
    i += '<path d="M75,290 L75,192 A40,40 0 0 1 155,192 L155,290 Z" fill="#07040b"/>'
    for tx in (40, 190):
        i += f'<rect x="{tx-3}" y="200" width="6" height="22" fill="#6b4a2a"/><ellipse cx="{tx}" cy="194" rx="7" ry="11" fill="#ffb347"/><ellipse cx="{tx}" cy="197" rx="3" ry="6" fill="#fff3c4"/>'
    i += chibi(85, 300, "#a33b3b", hat="helm") + chibi(115, 306, "#2f6b3e", hat="hood") + chibi(145, 300, "#3a3fa3", hat="wizard") + '</g>'
    # loot tokens
    for k, x in enumerate((48, 92, 136, 180)):
        i += d20(x, 338, 13, ["#b03a8a", "#e0a73a", "#e0a73a", "#e0a73a"][k], "20" if k == 0 else "")
    i += pill(52, 360, 126, 32, ACC, "DELVE", "#2a1a05", 17, "#fff", 900)
    i += bottomnav(["Shop", "Classes", "Delve", "Party", "Daily"])
    return phone(i, A1, A2, "Tavern hub: one big DELVE button")


def a_map():
    i = topbar(4, "1.2K", "38", "#7b4fd1")
    i += pill(14, 52, 96, 22, "#00000066", "Torchlight 145", "#ffd76a", 9)
    i += pill(116, 52, 100, 22, "#00000066", "Floor 7 · Room 3/8", "#fff", 9)
    nodes = [(115, 430, "S", "#4e8a5a"), (70, 380, "⚔", "#a33b3b"), (160, 380, "?", "#5b3fd1"),
             (115, 325, "⚔", "#a33b3b"), (60, 270, "$", ACC), (170, 270, "✚", "#2f8fa3"),
             (115, 210, "!", "#b05a2a"), (115, 140, "☠", "#6b1020")]
    links = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6), (6, 7)]
    for a, b in links:
        i += f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="#ffffff44" stroke-width="3" stroke-dasharray="5 5"/>'
    for k, (x, y, s, c) in enumerate(nodes):
        r = 24 if k == 7 else 17
        ring = 'stroke="#ffe27a" stroke-width="4"' if k == 3 else 'stroke="#fff" stroke-width="2"'
        i += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" {ring}/>' + txt(x, y + 5, s, 14, "#fff", 900)
    i += txt(115, 104, "BOSS: THE DROWNED KING", 10, "#ff9b9b", 900)
    i += pill(150, 318, 70, 16, "#ffe27a", "YOU", "#2a1a05", 8)
    return phone(i, "#241634", "#0d0814", "Room map: branch every 1–2 rooms")


def a_boons():
    i = topbar(4, "1.2K", "38", "#7b4fd1")
    i += txt(W / 2, 70, "ROOM CLEARED", 15, "#ffe27a", 900)
    i += txt(W / 2, 88, "Choose a Boon", 11, "#fff", 700)
    i += chibi(80, 140, "#a33b3b", hat="helm", s=0.8) + chibi(115, 145, "#2f6b3e", hat="hood", s=0.8) + chibi(150, 140, "#3a3fa3", hat="wizard", s=0.8)
    i += box(8, 182, W - 16, 210, "#00000088", 12)
    cw, cy = 66, 200
    i += card(14, cy, cw, 130, "#6b1020", "NAT 20:|FIREBALL", "150", "#b03a8a", d20(47, cy + 36, 22, "#e0a73a", "20", "#2a1a05"))
    i += card(82, cy, cw, 130, "#2a4f7a", "+20%|CRIT", "FREE", "#4fb6ff",
              '<path d="M115,215 L105,245 L117,245 L110,265 L128,235 L116,235 L124,215 Z" fill="#ffe27a" stroke="#1a1020" stroke-width="2"/>')
    i += card(150, cy, cw, 130, "#2f6b3e", "HEAL 1|ON KILL", "90", "#4e8a5a",
              '<path d="M183,222 a9,9 0 0 1 13,12 l-13,14 l-13,-14 a9,9 0 0 1 13,-12z" fill="#ff5b6b" stroke="#1a1020" stroke-width="2"/>')
    i += pill(42, 362, 92, 22, "#c0267a", "REROLL  20", "#fff", 10)
    i += pill(140, 362, 48, 22, "#7b4fd1", "AD ▶", "#fff", 9)
    i += txt(W / 2, 420, "Dice-themed boons give the build a tabletop feel", 8, "#ffffffaa", 600)
    return phone(i, "#2b1a3d", "#120a1b", "Boon pick: three cards, optional reroll")


def a_lootroll():
    i = topbar(4, "1.2K", "38", "#7b4fd1")
    i += txt(W / 2, 72, "LOOT ROLL", 20, ACC, 900)
    i += txt(W / 2, 92, "Boss chest: 320 Gold", 11, "#fff", 700)
    # tray
    i += box(18, 120, W - 36, 220, "#5a3a1e", 18, "#2b1a0b", 5)
    i += box(30, 132, W - 60, 196, "#2f5a3a", 12, "#1b3a22", 3)
    dice = [(70, 180, "x2", "#e0a73a"), (125, 205, "x3", "#4fb6ff"), (170, 170, "+50", "#4e8a5a"),
            (90, 270, "x2", "#e0a73a"), (155, 270, "20!", "#b03a8a")]
    for x, y, l, c in dice:
        i += d20(x, y, 22, c, l, "#1a1020" if c == "#e0a73a" else "#fff")
    i += box(40, 352, W - 80, 40, "#00000088", 10, ACC)
    i += txt(W / 2, 378, "320 → 2,310 GOLD", 15, "#ffe27a", 900)
    i += pill(30, 402, 82, 26, ACC, "COLLECT", "#2a1a05", 10, "#fff")
    i += pill(118, 402, 82, 26, "#7b4fd1", "ROLL AGAIN ▶", "#fff", 9, "#fff")
    return phone(i, "#2b1a3d", "#120a1b", "Loot Roll: dice multiply the boss chest")


def a_class():
    i = topbar(4, "1.2K", "38", "#7b4fd1")
    i += txt(W / 2, 70, "CLERIC · LV 3", 15, "#fff", 900)
    i += chibi(W / 2, 112, "#e8e0c8", hat="helm", s=1.3)
    i += box(10, 160, W - 20, 230, "#00000077", 12)
    i += txt(W / 2, 180, "TRAIT PATH", 11, ACC, 900)
    tree = [(115, 210, True), (70, 255, True), (160, 255, False), (70, 300, False), (160, 300, False), (115, 345, False)]
    for a, b in [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5)]:
        i += f'<line x1="{tree[a][0]}" y1="{tree[a][1]}" x2="{tree[b][0]}" y2="{tree[b][1]}" stroke="#ffffff55" stroke-width="3"/>'
    for x, y, on in tree:
        i += f'<circle cx="{x}" cy="{y}" r="15" fill="{ACC if on else "#3a2c4a"}" stroke="#fff" stroke-width="2"/>'
        if not on:
            i += f'<rect x="{x-5}" y="{y-2}" width="10" height="8" rx="1" fill="#aaa"/><path d="M{x-3},{y-2} v-3 a3,3 0 0 1 6,0 v3" fill="none" stroke="#aaa" stroke-width="2"/>'
    i += txt(115, 380, "Lv 5: Blessed dice re-roll natural 1s", 8, "#ffffffbb", 600)
    i += pill(14, 402, 98, 26, "#4e8a5a", "LEVEL UP 400", "#fff", 9, "#fff")
    i += pill(118, 402, 98, 26, "#5b3fd1", "OUTFITS", "#fff", 9, "#fff")
    return phone(i, "#2b1a3d", "#120a1b", "Class screen: short trait path, locks visible")


def a_shop():
    i = topbar(4, "1.2K", "38", "#7b4fd1")
    i += txt(W / 2, 66, "THE MERCHANT", 15, ACC, 900)
    i += box(12, 80, W - 24, 128, "#5b3fd1", 14, "#fff", 2)
    i += txt(24, 104, "ADVENTURER'S", 14, "#fff", 900, "start") + txt(24, 120, "EDITION", 14, "#ffe27a", 900, "start")
    for k, l in enumerate(["No forced ads", "+1 party slot", "2x daily delves"]):
        i += txt(24, 142 + k * 14, "• " + l, 9, "#fff", 600, "start")
    i += d20(180, 120, 26, "#e0a73a", "20", "#2a1a05")
    i += pill(130, 176, 80, 24, "#3ac46a", "$4.99", "#fff", 12, "#fff")
    i += txt(30, 192, "ONE TIME", 8, "#ffffffaa", 700, "start")
    i += box(12, 218, 104, 120, "#a33b3b", 12, "#fff", 2) + chibi(64, 262, "#222", hat="hood")
    i += txt(64, 304, "ROGUE", 10, "#fff", 900) + pill(26, 312, 76, 18, "#3ac46a", "$1.99", "#fff", 10)
    i += box(124, 218, 94, 120, "#2a4f7a", 12, "#fff", 2) + d20(152, 255, 16, "#ff6bd6", "20") + d20(190, 262, 16, "#6bffd6", "20", "#1a1020")
    i += txt(171, 304, "DICE SKINS", 10, "#fff", 900) + pill(134, 312, 74, 18, "#3ac46a", "$0.99", "#fff", 10)
    i += txt(W / 2, 362, "Every class can also be earned with Gold", 8, "#ffffffbb", 600)
    i += bottomnav(["Shop", "Classes", "Delve", "Party", "Daily"], 0)
    return phone(i, "#2b1a3d", "#120a1b", "Shop: about 4 SKUs, no gems, no timers")


# ---------- Concept B mockups (Scrapline) ----------
B1, B2 = "#d98c4a", "#3b1f14"
BACC = "#3cc6c0"


def b_hub():
    i = topbar(6, "3.4K", "12", "#b8462a")
    i += pill(14, 52, 92, 22, "#00000055", "Settlement", "#fff", 10, "#ffffff55")
    i += pill(112, 52, 104, 22, BACC, "Supply Run 1/3", "#0a2a2a", 9, "#fff")
    i += txt(W / 2, 106, "ROUTE 9", 22, "#fff", 900)
    i += txt(W / 2, 126, "THE ASH FLATS", 13, "#ffe0a0", 900)
    i += '<circle cx="170" cy="170" r="26" fill="#ffd27a" opacity=".85"/>'
    i += '<polygon points="0,250 40,215 70,235 110,200 150,230 190,205 230,240 230,300 0,300" fill="#8a4a2a" opacity=".7"/>'
    i += '<rect x="30" y="205" width="14" height="45" fill="#4a2a1a"/><rect x="48" y="190" width="10" height="60" fill="#4a2a1a"/><rect x="190" y="210" width="12" height="40" fill="#4a2a1a"/>'
    i += box(0, 290, W, 70, "#5a2e1a", 0) + '<line x1="0" y1="325" x2="230" y2="325" stroke="#ffd27a" stroke-width="3" stroke-dasharray="14 10"/>'
    i += truck(48, 240, 1.0)
    i += pill(14, 346, 200, 14, "#00000066") + box(16, 348, 130, 10, "#e2572b", 5) + txt(W / 2, 372, "FUEL 6/9 · ARMOR 3", 9, "#fff", 800)
    i += pill(52, 378, 126, 28, BACC, "ROLL OUT", "#0a2a2a", 16, "#fff", 900)
    i += bottomnav(["Shop", "Garage", "Roll Out", "Crew", "Season"], 2, "#2a160e", BACC)
    return phone(i, B1, B2, "Garage hub: your rig is the hero")


def b_route():
    i = topbar(6, "3.4K", "12", "#b8462a")
    i += pill(14, 52, 96, 22, "#00000066", "Scrap 210", "#ffd76a", 9)
    i += pill(116, 52, 100, 22, "#00000066", "Fuel ▮▮▮▮▮▯▯", "#ff9a6a", 9)
    nodes = [(115, 430, "▶", "#4e8a5a"), (60, 375, "⚔", "#b8462a"), (170, 375, "⛏", "#8a6a3a"),
             (40, 310, "$", "#d9a03a"), (115, 315, "☢", "#7aa02a"), (190, 310, "⚔", "#b8462a"),
             (75, 245, "⛺", BACC), (165, 245, "⛏", "#8a6a3a"), (115, 170, "☠", "#6b1020")]
    links = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 6), (4, 6), (4, 7), (5, 7), (6, 8), (7, 8)]
    for a, b in links:
        i += f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="#ffe0a088" stroke-width="3" stroke-dasharray="5 5"/>'
    for k, (x, y, s, c) in enumerate(nodes):
        r = 24 if k == 8 else 17
        ring = 'stroke="#ffe27a" stroke-width="4"' if k == 1 else 'stroke="#fff" stroke-width="2"'
        i += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" {ring}/>' + txt(x, y + 5, s, 13, "#fff", 900)
    i += txt(115, 135, "WARLORD CONVOY", 10, "#ffb0a0", 900)
    i += box(10, 88, 210, 30, "#00000066", 8) + txt(115, 108, "Detours = more loot, more fuel burned", 8.5, "#fff", 600)
    return phone(i, "#7a4a2a", "#2a140c", "Route map: fuel turns every route into a choice")


def b_raid():
    i = topbar(6, "3.4K", "12", "#b8462a")
    i += pill(14, 52, 70, 20, "#00000066", "210", "#ffd76a", 10)
    i += pill(120, 52, 96, 20, "#00000066", "RAID 3/5", "#fff", 10)
    i += box(0, 80, W, 140, "#c27a44", 0) + box(0, 180, W, 40, "#5a2e1a", 0)
    i += truck(58, 140, 0.9)
    i += raider(22, 175, 0.7) + raider(40, 190, 0.6) + raider(205, 178, 0.7, "#8a3a8a")
    i += '<line x1="104" y1="148" x2="30" y2="170" stroke="#ffe27a" stroke-width="2" stroke-dasharray="3 3"/>'
    i += box(8, 228, W - 16, 176, "#00000099", 12)
    i += txt(W / 2, 248, "SALVAGE: PICK A PART", 11, "#ffe27a", 900)
    cw, cy = 66, 258
    i += card(14, cy, cw, 112, "#5a5a5a", "HARPOON|GUN", "150", "#4fb6ff",
              '<line x1="28" y1="290" x2="66" y2="275" stroke="#ddd" stroke-width="4"/><polygon points="66,270 76,272 68,282" fill="#ddd"/>')
    i += card(82, cy, cw, 112, "#6b2a10", "FLAME|THROWER", "FREE", "#e2572b",
              '<path d="M115,300 C100,290 108,275 115,265 C122,275 130,290 115,300 Z" fill="#ffb347" stroke="#1a1020" stroke-width="2"/>')
    i += card(150, cy, cw, 112, "#3a3a3a", "SPIKED|PLOW", "120", "#b8b8b8",
              '<polygon points="165,295 205,280 205,300" fill="#ccc" stroke="#1a1020" stroke-width="2"/>')
    i += pill(42, 410, 92, 20, "#c0267a", "REROLL  20", "#fff", 9)
    i += pill(140, 410, 48, 20, "#7b4fd1", "AD ▶", "#fff", 9)
    return phone(i, "#e0a06a", "#2a140c", "Raid + part pick: upgrades bolt onto the truck")


def b_sorter():
    i = topbar(6, "3.4K", "12", "#b8462a")
    i += txt(W / 2, 70, "SCRAP SORTER", 19, BACC, 900)
    i += txt(W / 2, 88, "Run haul: 480 Scrap", 10, "#fff", 700)
    i += box(10, 100, W - 20, 300, "#2a1a12", 10, "#5a3a2a", 3)
    belts = [(20, 130, 150, 160, "x2", "#d9a03a"), (80, 200, 210, 230, "x3", "#3ac46a"),
             (20, 270, 150, 300, "x2", "#d9a03a"), (80, 330, 210, 360, "x5", "#b03a8a")]
    for x1, y1, x2, y2, l, c in belts:
        i += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#555" stroke-width="12" stroke-linecap="round"/>'
        i += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#888" stroke-width="2" stroke-dasharray="6 6"/>'
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        i += box(mx - 18, my - 26, 36, 16, c, 4, "#fff", 1.5) + txt(mx, my - 14, l, 10, "#fff", 900)
    import random
    random.seed(4)
    for _ in range(28):
        x, y = random.randint(30, 200), random.randint(110, 390)
        i += f'<rect x="{x}" y="{y}" width="7" height="7" transform="rotate({random.randint(0,90)} {x} {y})" fill="{random.choice(["#c9c9c9","#b8733a","#8a8a8a"])}" stroke="#222" stroke-width="1"/>'
    i += '<path d="M90,96 h50 v14 h-10 v-6 h-30 v6 h-10 z" fill="#e2572b" stroke="#fff" stroke-width="2"/>'  # magnet
    i += box(60, 402, 110, 30, "#00000099", 8, BACC) + txt(W / 2, 422, "480 → 3,060", 13, "#ffe27a", 900)
    return phone(i, "#5a3a2a", "#1a0e08", "Scrap Sorter: multiplies the run haul")


def b_settlement():
    i = topbar(6, "3.4K", "12", "#b8462a")
    i += txt(W / 2, 70, "HAVEN · POP 14", 15, "#fff", 900)
    i += box(10, 84, W - 20, 300, "#6a4a2a", 12, "#3a2414", 3)
    blds = [(24, 100, "GARAGE", "Lv 3", "#8a5a2b", True), (124, 100, "MED TENT", "Lv 2", "#3a7a6a", True),
            (24, 196, "WORKSHOP", "Lv 1", "#5a5a6a", True), (124, 196, "RADIO", "Lv 1", "#7a4a7a", True),
            (24, 292, "WATER", "LOCKED", "#3a3a3a", False), (124, 292, "ARMORY", "LOCKED", "#3a3a3a", False)]
    for x, y, n, l, c, on in blds:
        i += box(x, y, 82, 82, c, 10, "#fff" if on else "#888", 2)
        i += f'<polygon points="{x+12},{y+40} {x+41},{y+16} {x+70},{y+40}" fill="#00000044"/><rect x="{x+18}" y="{y+40}" width="46" height="22" fill="#00000033"/>'
        i += txt(x + 41, y + 74, n, 8, "#fff", 900)
        i += pill(x + 50, y + 4, 30, 14, "#000000aa", l if on else "LOCKED", "#fff", 7)
    i += txt(W / 2, 402, "Garage Lv 4: unlocks Bus chassis", 8.5, "#ffe0a0", 700)
    i += bottomnav(["Shop", "Garage", "Roll Out", "Crew", "Season"], 1, "#2a160e", BACC)
    return phone(i, "#a06a3a", "#2a140c", "Settlement: base-building meta without PvP")


def b_pass():
    i = topbar(6, "3.4K", "12", "#b8462a")
    i += box(0, 44, W, 70, "#b8462a", 0)
    i += txt(14, 74, "ROAD SEASON 1", 15, "#fff", 900, "start") + txt(14, 92, "Rust & Chrome · 28d left", 9, "#ffe0a0", 700, "start")
    i += pill(150, 66, 70, 24, BACC, "$3.99", "#0a2a2a", 12, "#fff")
    i += txt(60, 134, "FREE", 10, "#fff", 900) + txt(170, 134, "COSMETIC", 10, BACC, 900)
    i += f'<rect x="111" y="142" width="8" height="280" fill="#3a2414"/>'
    rows = [("Scrap x200", "Chrome paint"), ("Fuel can", "Skull decal"), ("Crew: Mara", "Flame exhaust"), ("Scrap x400", "Gold hubcaps")]
    for k, (f, p) in enumerate(rows):
        y = 150 + k * 68
        i += box(14, y, 88, 56, "#5a3a2a", 10, "#fff", 2) + txt(58, y + 33, f, 8.5, "#fff", 800)
        i += box(128, y, 88, 56, "#1d4a4a", 10, BACC, 2) + txt(172, y + 33, p, 8.5, "#fff", 800)
        i += f'<circle cx="115" cy="{y+28}" r="11" fill="#ffd76a" stroke="#fff" stroke-width="2"/>' + txt(115, y + 32, str(k + 1), 10, "#2a1a05", 900)
    return phone(i, "#5a3020", "#1a0e08", "Road Season: premium track is cosmetic only")


# ---------- small diagram helpers ----------
def loop(steps, colors):
    out = '<div class="loop">'
    for k, (t, d) in enumerate(steps):
        out += f'<div class="step"><span class="dot" style="background:{colors[k % len(colors)]}"></span><b>{t}</b><small>{d}</small></div>'
        if k < len(steps) - 1:
            out += '<div class="arr">›</div>'
    return out + "</div>"


def panel(title, body, color, items=None, cls=""):
    lis = "".join(f"<li>{x}</li>" for x in (items or []))
    return f'<div class="panel {cls}" style="--c:{color}"><h3>{title}</h3><p>{body}</p>{"<ul>"+lis+"</ul>" if lis else ""}</div>'


def tag(kind):
    return {"S": '<span class="tag s">SOURCED</span>', "I": '<span class="tag i">INFERRED</span>',
            "P": '<span class="tag p">PROPOSED</span>'}[kind]


pages = []


def page(kicker, title, body, foot, color="#59d8ff"):
    n = len(pages) + 1
    pages.append(f"""<section class="page"><div class="kicker" style="color:{color}">{kicker}</div>
<h1>{title}</h1>{body}<div class="foot"><i>{foot}</i><span>{n:02d}</span></div></section>""")


CY, GR, YE, PU, RE = "#59d8ff", "#57e08a", "#ffc84a", "#b06bff", "#ff6b6b"

# ---- 1 cover
pages.append(f"""<section class="page cover">
<div class="kicker" style="color:{CY}">GAME CONCEPT BRIEF · OCTOBER 2026</div>
<h1 class="big">TWO SMALL ROGUELITES</h1>
<div class="sub">Delve &amp; Dice and Scrapline: two concepts that reuse Cup Heroes' structure with much lighter monetization</div>
<div class="covergrid">
 <div>
  {panel("Purpose", "Two concepts that borrow a few systems from the Cup Heroes teardown (wave fights, three-card upgrades, a reward multiplier, layered meta) and sell to players on a much smaller, fairer scale. These are ideas, not specs.", CY)}
  {panel("Reading Key", "Every claim is tagged so you can tell research from design ideas:", YE,
         [tag("S") + " Taken from a cited source (see the Sources page)",
          tag("I") + " My reasoning from the sources; not proven",
          tag("P") + " A design proposal for us to debate",
          "All art is placeholder SVG drawn for this brief"])}
 </div>
 <div class="coverart">{a_hub()}{b_hub()}</div>
</div><div class="strip">
 {panel("Market research", "Why a dungeon crawler and a post-apocalyptic game; small-scale benchmarks (p.2–3)", GR)}
 {panel("System filter", "What we keep from Cup Heroes and what we cut (p.4)", RE)}
 {panel("Delve &amp; Dice", "Pitch, loop, meta, economy and mockups (p.5–7)", PU)}
 {panel("Scrapline", "Pitch, loop, meta, economy and mockups (p.8–10)", YE)}
</div><div class="foot"><i>Built on the user-supplied Cup Heroes Game Design Inspiration Brief.</i><span>01</span></div></section>""")

# ---- 2 research: why these genres
page("1. MARKET RESEARCH", "Why a Dungeon Crawler and a Post-Apocalyptic Game", f"""
<div class="cols3">
{panel("Roguelikes are growing", "", GR, [
    tag("S") + " AppMagic (2025 monetization report): roguelike titles <b>grew 26.2% YoY</b>, while RPG revenue overall fell 17% to $11bn.",
    tag("S") + " Sensor Tower: mobile games made about <b>$82B</b> in 2025 (+1%). RPG is declining; strategy ($20.2B) and puzzle are growing.",
    tag("I") + " The roguelite <i>format</i> is the healthy part of a shrinking RPG market."])}
{panel("Dungeon crawlers work at small scale", "", CY, [
    tag("S") + " Soul Knight: IAPs are only <b>$0.99–$3.99</b> (mostly character unlocks). Adapty estimates about $400K/month.",
    tag("S") + " Shattered Pixel Dungeon: <b>solo developer</b>, no ads or microtransactions, cosmetic-only supporter extras.",
    tag("S") + " Archero 2 (the heavy end): $32.8M in its first 30 days.",
    tag("I") + " The fantasy-crawler audience accepts both light and heavy monetization."])}
{panel("Post-apocalyptic is a theme, not a genre", "", YE, [
    tag("S") + " Last War: Survival: <b>&gt;$900M</b> lifetime, 60M+ downloads (Sensor Tower, via wnhub).",
    tag("S") + " Whiteout Survival: <b>$500M</b> in about a year (Sensor Tower, via TechNode).",
    tag("S") + " Both are 4X strategy games; Sensor Tower's regional apocalypse charts are dominated by strategy.",
    tag("I") + " The theme draws spenders, but almost no roguelite is chasing them. That's the gap."])}
</div>
<div class="note"><b>Why not Space?</b> I couldn't find data on space roguelites specifically. Sensor Tower's space charts are led by unrelated games (Honkai: Star Rail, Galaxy Attack), and one 'Space Survivor' title shows about $54/week in the UK. That doesn't rule space out, I just couldn't back it up. <b>DnD and RPG Adventure</b> are folded into Concept A as its theme.</div>
""", "Figures are third-party estimates (AppMagic, Sensor Tower, Adapty) unless noted. Full list on the Sources page.", GR)

# ---- 3 small-scale benchmarks table
rows = [
    ("Balatro (mobile)", "Premium $9.99, no ads or IAP", "~$4.4M in ~2 months after launch (Sep 2024); averaged ~$71K/day in Nov", "AppMagic via PocketGamer.biz"),
    ("Slay the Spire (mobile)", "Premium $9.99 (Humble)", "Android: ~10K downloads and ~$90K in a month (stale snapshot)", "Sensor Tower page; TouchArcade"),
    ("20 Minutes Till Dawn", "Separate free and $4.99 Premium listings (Erabit port)", "Premium: ~230K Android downloads; ~9.3K in the last 30 days", "AppBrain; Google Play"),
    ("Brotato (mobile)", "Premium listings (Android one published by Erabit)", "iOS ~$10K/mo; Android ~$20K/mo", "apprank.io; TrendApps (estimates)"),
    ("Soul Knight", "F2P, small IAPs $0.99–$3.99", "~$400K/mo; ~300K downloads/mo", "Adapty paywall library (estimate)"),
    ("Shattered Pixel Dungeon", "Free / pay-what-you-want, cosmetic supporter extras", "Steam alone: ~54.9K copies, ~$467K gross", "Raijin (estimate); Flathub; itch.io"),
    ("Archero 2 (reference)", "Heavy F2P: gems, packs, passes", "$6.6M first week, $32.8M first 30 days", "AppMagic via PocketGamer.biz"),
]
tbl = "<table><tr><th>Game</th><th>Model</th><th>Reported performance</th><th>Source</th></tr>" + "".join(
    f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td class='src'>{d}</td></tr>" for a, b, c, d in rows) + "</table>"
page("2. BENCHMARKS", "How Small Roguelites Make Money on Mobile", tbl + f"""
<div class="cols3 tight">
{panel("Pattern 1: Premium", "A one-time price of $4.99–$9.99. Balatro shows the ceiling for a hit; Brotato's mobile listings show what more typical premium sales look like.", CY)}
{panel("Pattern 2: Free + Premium", "Two separate listings, as with 20 Minutes Till Dawn on Google Play. Erabit Studios has ported both 20MTD and Brotato, so a publisher for this route exists.", GR)}
{panel("Pattern 3: Light F2P", "Unlocks you can earn or buy at a few dollars each, like Soul Knight. No gacha or premium currency is needed.", YE)}
</div>""", "All revenue numbers are third-party estimates with different methods and time windows. Don't compare them directly; use them only as a sense of scale.", YE)

# ---- 4 keep vs cut
page("3. SYSTEM FILTER", "What We Keep From Cup Heroes, and What We Cut", f"""
<div class="cols2">
{panel("KEEP (the fun parts)", "These systems keep the play loop engaging and don't depend on heavy spending:", GR, [
    "Short wave fights on one readable screen",
    "Three-card upgrade picks between fights, with a small paid reroll",
    "Run currency kept separate from meta currency",
    "A tactile reward multiplier mini-game (re-themed for each concept)",
    "Hero/class roster with a short trait path and visible locked nodes",
    "Daily calendar and a daily seeded challenge",
    "Big single primary button, progress always on screen, small celebrations"])}
{panel("CUT OR SHRINK (the heavy parts)", "These drive Cup Heroes' high spending and are what you wanted to avoid:", RE, [
    "<s>Premium gem currency</s>: we price everything in real dollars, so there's no exchange-rate confusion",
    "<s>Booster/shard packs</s>: no random paid rewards",
    "<s>Countdown bundles with value tags</s>: no artificial urgency",
    "<s>Stacked pass + gems + boosters</s>: at most one optional pass, cosmetic only",
    "<s>Forced interstitial ads</s>: rewarded ads only, always opt-in",
    "<s>Guilds and other social systems</s>: out of scope for a small team",
    "No energy or stamina system: play as much as you like"])}
</div>
<div class="note">{tag("P")} Target: <b>about 4–6 store items in total</b> and <b>at most 3 currencies</b> (run currency, meta currency and an optional season currency). Cup Heroes shows at least 4 currencies and 6+ offer types on its menus.</div>
""", "Cup Heroes observations come from the supplied teardown (pages 2, 7 and 8).", RE)

# ---- Concept A
page("CONCEPT A · DUNGEON CRAWLER / D&amp;D", "Delve &amp; Dice", f"""
<div class="hero">
 <div class="herotext">
  <p class="pitch">Pick a party of three adventurers and clear a cursed dungeon room by room. Every big moment comes down to a dice roll you can see.</p>
  {panel("Fantasy", "A tabletop session in your pocket: a tavern hub, classes, dungeon floors, and dice you can feel.", PU)}
  {panel("Run length", "10–15 minutes: 5 floors of about 8 rooms, with a boss every 5th floor.", CY)}
  {panel("Hook vs. Cup Heroes", "Upgrades and rewards hinge on visible d20 rolls (a natural 20 triggers boons). The randomness is the theme, not a paywall.", YE)}
  {panel("Audience", "Players who like Soul Knight, Slay the Spire or Archero, plus tabletop fans.", GR)}
 </div>
 <div class="shots2">{a_hub()}{a_map()}</div>
</div>""", "All art is placeholder SVG mockups. Party size, floor counts and run times are starting proposals.", PU)

page("CONCEPT A · CORE LOOP", "Run Structure &amp; Boon Choices", loop([
    ("PARTY UP", "Pick 3 classes"), ("DELVE", "Choose a room path"), ("FIGHT", "Auto-battle waves"),
    ("BOON", "Pick 1 of 3"), ("LOOT ROLL", "Dice multiply the chest"), ("TAVERN", "Spend Gold"), ("RETURN", "Daily delve")],
    [CY, GR, YE, PU]) + f"""
<div class="hero rev">
 <div class="shots2">{a_boons()}{a_lootroll()}</div>
 <div class="herotext">
  {panel("Room types", "Combat · Elite · Trap (a d20 save) · Shrine (trade HP for a boon) · Merchant · Rest · Boss. A branching path every 1–2 rooms means a choice every minute.", CY)}
  {panel("Boons", "Some boons are dice-keyed (\"Natural 20: Fireball\", \"Roll 15+: dodge\"), others are flat stats. Most class builds lean on one dice mechanic. Reroll costs Torchlight, or one optional ad.", PU)}
  {panel("Loot Roll", "Replaces Cup Heroes' pachinko board. After a boss, roll 3–5 dice into a tray; the faces multiply Gold. A rare natural 20 drops a class shard. One extra roll per day from an optional ad.", YE)}
 </div>
</div>""", "Inspiration: Cup Heroes three-card shop and multiplier mini-game (pages 5–6), re-themed around dice.", CY)

page("CONCEPT A · META &amp; ECONOMY", "Classes, Currencies &amp; a Fair Shop", f"""
<div class="hero">
 <div class="herotext">
  <div class="cols2 tight">
  {panel("Run currency: Torchlight", "Earned in rooms; spent at merchants and on rerolls. Resets after each run.", CY)}
  {panel("Meta currency: Gold", "Comes from Loot Rolls. Spent on class levels, the tavern and unlocking classes.", YE)}
  {panel("Classes", "8 at launch (Fighter, Rogue, Cleric, Wizard, Ranger, Bard, Paladin, Warlock), each with a 6-node trait path.", PU)}
  {panel("Retention", "7-day calendar, a daily seeded dungeon with a leaderboard, and weekly 'module' modifiers.", GR)}
  </div>
  {panel("Store (4 items, priced in dollars)", "", RE, [
      "<b>$4.99 Adventurer's Edition</b>, one-time: no forced ads, +1 party slot, 2x daily delves",
      "<b>$1.99 class unlocks</b>: every class can also be earned with Gold",
      "<b>$0.99–$1.99 dice skins and outfits</b>: cosmetic only",
      "<b>Rewarded ads</b>: optional reroll or extra Loot Roll, capped per day"])}
  <div class="note">{tag("I")} Alternative: sell it as a <b>$4.99–$6.99 premium game</b> with no IAP, like Slay the Spire or Balatro, keeping only the cosmetics. The design doesn't change.</div>
 </div>
 <div class="shots2">{a_class()}{a_shop()}</div>
</div>""", "Prices are proposals benchmarked against Soul Knight ($0.99–$3.99 IAP) and premium roguelites ($4.99–$9.99).", YE)

# ---- Concept B
page("CONCEPT B · POST-APOCALYPTIC", "Scrapline", f"""
<div class="hero">
 <div class="herotext">
  <p class="pitch">You drive an armored rig across a ruined wasteland. Choose your route, survive raids at every stop, and bolt salvaged weapons onto the truck until it's a monster.</p>
  {panel("Fantasy", "Road-warrior convoy and scavenger survival: the truck is your hero and your build.", YE)}
  {panel("Run length", "10–15 minutes: a route of about 10 stops ending in a warlord convoy boss.", CY)}
  {panel("Hook vs. Cup Heroes", "Upgrades physically appear on the truck, so you can see your build. Fuel makes every route choice a risk.", RE)}
  {panel("Audience", "Fans of post-apocalyptic strategy games (Last War, Whiteout Survival) who want something shorter and fairer, plus survivor-like players.", GR)}
 </div>
 <div class="shots2">{b_hub()}{b_route()}</div>
</div>""", "All art is placeholder SVG mockups. Stop counts and run times are starting proposals.", YE)

page("CONCEPT B · CORE LOOP", "Route, Raid &amp; Salvage", loop([
    ("ROLL OUT", "Pick rig + crew"), ("ROUTE", "Choose the next stop"), ("RAID", "Defend the truck"),
    ("SALVAGE", "Pick 1 of 3 parts"), ("SORT", "Scrap Sorter multiplier"), ("SETTLE", "Build Haven"), ("RETURN", "Supply runs")],
    [YE, RE, CY, GR]) + f"""
<div class="hero rev">
 <div class="shots2">{b_raid()}{b_sorter()}</div>
 <div class="herotext">
  {panel("Stops", "Raid · Scavenge (pick 1 of 2 crates) · Trader · Radstorm (a hazard modifier) · Outpost (repair) · Boss convoy. Each stop costs fuel, and longer routes pay better.", CY)}
  {panel("Raids", "Wave fights where raiders come from both sides and the truck holds the middle. The parts you've bolted on fire automatically, like Cup Heroes' auto-combat but with the truck at the center.", RE)}
  {panel("Scrap Sorter", "Replaces Cup Heroes' pachinko board. Your haul tumbles down conveyor belts through magnet gates that multiply it (x2, x3, x5). The physics are the same as Cup Heroes' board, but it's themed as a junkyard.", YE)}
 </div>
</div>""", "Inspiration: Cup Heroes wave combat, upgrade shop and multiplier board (pages 5–6), re-themed.", RE)

page("CONCEPT B · META &amp; ECONOMY", "Haven, Currencies &amp; a Fair Shop", f"""
<div class="hero">
 <div class="herotext">
  <div class="cols2 tight">
  {panel("Run currency: Scrap", "Earned at stops and spent at traders during the run. What's left at the end goes through the Scrap Sorter.", CY)}
  {panel("Meta currency: Parts", "What comes out of the Sorter. Spent on Haven buildings, chassis and crew.", YE)}
  {panel("Haven (settlement)", "6 buildings that give permanent bonuses and unlock new chassis (Buggy, Truck, Bus, Tanker). It's the base-building of 4X without the PvP.", GR)}
  {panel("Retention", "Daily Supply Run bounties, a 7-day calendar, and a 28-day Road Season with a free track.", PU)}
  </div>
  {panel("Store (4 items, priced in dollars)", "", RE, [
      "<b>$2.99 No Forced Ads</b>, one-time; optional ads still give bonuses",
      "<b>$1.99 Starter Rig</b>, one-time: a unique chassis plus Parts",
      "<b>$3.99 Road Season</b>: the premium track is <i>cosmetic only</i> (paint, decals, exhaust)",
      "<b>Rewarded ads</b>: one revive per run, or double the Sorter haul"])}
  <div class="note">{tag("I")} Cup Heroes' heavy pressure comes from stacking a pass, gems, boosters and timed bundles. Here the pass is the only recurring purchase, and it never sells power.</div>
 </div>
 <div class="shots2">{b_settlement()}{b_pass()}</div>
</div>""", "Ad mix: Sensor Tower separates ads-first titles (~80% of revenue from ads) from IAP-first ones (~78–80% IAP). Scrapline leans IAP with optional ads.", GR)

# ---- comparison
page("4. SIDE BY SIDE", "Comparing the Two Concepts", f"""
<table class="cmp">
<tr><th></th><th>Delve &amp; Dice</th><th>Scrapline</th></tr>
<tr><td>Genre / theme</td><td>Dungeon crawler · D&amp;D fantasy</td><td>Route roguelite · post-apocalyptic</td></tr>
<tr><td>Systems borrowed</td><td>Three-card picks, multiplier (Loot Roll), class roster, daily calendar</td><td>Wave fights, three-card picks, multiplier (Scrap Sorter), base meta, season pass</td></tr>
<tr><td>Revenue model</td><td>One-time unlock + small class/cosmetic items, or premium</td><td>Light F2P: no-ads purchase + starter pack + cosmetic pass</td></tr>
<tr><td>Store items</td><td>4</td><td>4</td></tr>
<tr><td>Evidence it can work</td><td>{tag("S")} Soul Knight, Shattered Pixel Dungeon, Balatro, Slay the Spire</td><td>{tag("S")} The theme earns huge sums in 4X; {tag("I")} that it transfers to roguelites is unproven</td></tr>
<tr><td>Art scope</td><td>Chibi fantasy party and dungeon tiles; lots of cheap asset packs exist</td><td>One truck plus modular parts and a few raider types; arguably cheaper</td></tr>
<tr><td>Biggest risk</td><td>Very crowded genre; the dice hook has to stand out in screenshots</td><td>No direct roguelite comparison; 4X fans may not want short sessions</td></tr>
<tr><td>Prototype first</td><td>The Loot Roll and dice boons: is rolling fun 50 times?</td><td>Does bolting parts onto the truck feel powerful?</td></tr>
</table>
<div class="note">{tag("P")} <b>Suggested next step:</b> build a gray-box prototype of each concept's core moment (one raid plus part pick, or one floor plus a Loot Roll) and playtest both before choosing. No meta systems or store yet.</div>
""", "Both concepts are deliberately scoped for a small team: one hub, one run mode, one meta layer, and a store of about 4 items.", CY)

# ---- sources
srcs = [
    ("AppMagic Mobile Games Monetization Report 2025 (summary): roguelike +26.2% YoY, RPG $11bn −17%", "https://gamedevreports.substack.com/p/appmagic-mobile-games-monetization"),
    ("Sensor Tower State of Gaming 2026 press release: $82B mobile IAP in 2025, strategy $20.2B", "https://sensortower.com/press/press-release-sensor-tower-state-of-gaming-gaming-drove-52-billion-downloads-82b-iap-revenue-on-mobile-and-12b-premium-revenue-on-steam"),
    ("PocketGamer.biz: Archero 2 makes $32.8M in its first 30 days", "https://www.pocketgamer.biz/archero-2-makes-328m-in-first-30-days-from-player-spending"),
    ("PocketGamer.biz: Archero 2 makes $6.6M in its first week", "https://www.pocketgamer.biz/habbys-archero-2-makes-6-6m-in-first-week-over-10-of-archeros-lifetime-earnings"),
    ("Adapty paywall library: Soul Knight revenue and IAP price estimates", "https://adapty.io/paywall-library/soul-knight/"),
    ("Flathub: Shattered Pixel Dungeon (no ads/IAP, cosmetic supporter extras)", "https://flathub.org/sv/apps/com.shatteredpixel.shatteredpixeldungeon"),
    ("itch.io: Shattered Pixel Dungeon purchase page (pay what you want)", "https://shattered-pixel.itch.io/shattered-pixel-dungeon/purchase"),
    ("Raijin: Shattered Pixel Dungeon Steam estimates", "https://raijin.gg/app/1769170/Shattered_Pixel_Dungeon"),
    ("PocketGamer.biz: Balatro nears $4.4M on mobile", "https://www.pocketgamer.biz/balatro-nears-44m-on-mobile-amid-a-sudden-spending-surge/"),
    ("Sensor Tower app overview: Slay the Spire (Google Play, US)", "https://app.sensortower.com/overview/com.humble.SlayTheSpire?country=US"),
    ("TouchArcade: Humble Games premium mobile pricing (Slay the Spire $9.99)", "https://toucharcade.com/2023/05/15/humble-games-discount-anniversary-slay-the-spire-mobile-price-forager-crying-suns-deal/"),
    ("AppBrain: 20 Minutes Till Dawn: Premium Android stats", "https://www.appbrain.com/app/20-minutes-till-dawn-full/com.Flanne.MinutesTillDawn.roguelike.shooting.gp"),
    ("Google Play: 20 Minutes Till Dawn: Premium listing", "https://play.google.com/store/apps/details?id=com.Flanne.MinutesTillDawn.roguelike.shooting.gp"),
    ("Wikipedia: 20 Minutes Till Dawn (Erabit mobile port)", "https://en.wikipedia.org/wiki/20_Minutes_Till_Dawn"),
    ("apprank.io: Brotato iOS revenue estimate", "https://apprank.io/brotato-4925"),
    ("TrendApps: Brotato: Premium Android estimate", "https://trendapps.dev/app/android/com-brotato-shooting-survivors-games-paid-android/"),
    ("wnhub.io: Last War: Survival nears $1B (Sensor Tower)", "https://wnhub.io/news/analytics/item-45553"),
    ("TechNode: Whiteout Survival hits $500M in one year", "https://technode.com/2024/03/14/whiteout-survival-achieves-500-million-revenue-within-one-year-of-release/"),
    ("Sensor Tower blog: regional top apocalypse games (example)", "https://sensortower.com/blog/2024-q2-android-top-5-apocalipse%20games-units-ua-601320cf241bc16eb8127cb8"),
    ("Sensor Tower blog: US iOS top space games Q2 2025", "https://sensortower.com/blog/2025-q2-ios-top-5-space%20games-revenue-us-600e9341241bc16eb8f27ad6"),
    ("Sensor Tower: Gaming Deep Dive ad monetization report (ads-first vs IAP-first split)", "https://sensortower.com/blog/gaming-deep-dive-ad-monetization-report"),
]
lst = "<ol class='srcs'>" + "".join(f"<li>{t}<br><a href='{u}'>{html.escape(u)}</a></li>" for t, u in srcs) + "</ol>"
page("5. SOURCES", "Where the Numbers Come From", lst + """
<div class="note small"><b>Method and caveats:</b> I gathered these through web search in October 2026. Several pages (Sensor Tower, AppMagic summaries) couldn't be opened directly from my environment, so some figures come from the search engine's excerpts of those pages. All revenue figures are third-party <i>estimates</i>, not developer disclosures, and AppMagic (net) and Sensor Tower (gross) measure differently. I found no data for space-themed roguelites, so that genre isn't covered.</div>
""", "Nothing in this brief claims hidden metrics, balance values or developer-confirmed revenue.", PU)

CSS = """
@page { size: 1100px 850px; margin: 0; }
* { box-sizing: border-box; }
body { margin:0; background:#0b0f17; color:#e8edf6; font-family: Inter, sans-serif; }
.page { width:1100px; height:850px; padding:38px 52px 0; position:relative; page-break-after:always; overflow:hidden; background:#0b0f17; }
.kicker { font-size:12px; font-weight:800; letter-spacing:.06em; }
h1 { font-size:33px; margin:6px 0 18px; font-weight:800; color:#fff; }
h1.big { font-size:58px; margin:22px 0 6px; letter-spacing:-.01em; }
.sub { font-size:18px; color:#9aa6ba; margin-bottom:26px; }
.foot { position:absolute; left:52px; right:42px; bottom:24px; display:flex; justify-content:space-between; font-size:10.5px; color:#8f9bb0; }
.panel { background:#161d2b; border-radius:14px; padding:13px 17px 12px; border-top:5px solid var(--c); margin-bottom:11px; }
.panel h3 { margin:0 0 5px; font-size:15px; color:#fff; }
.panel p { margin:0; font-size:11.5px; line-height:1.45; color:#a9b4c6; }
.panel ul { margin:6px 0 0; padding-left:15px; }
.panel li { font-size:11.5px; line-height:1.45; margin-bottom:4px; color:#dbe2ee; }
.panel li::marker { color: var(--c); }
.cols3 { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
.cols2 { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
.tight .panel { margin-bottom:0; }
.tight { margin-top:12px; gap:10px; }
.covergrid { display:grid; grid-template-columns: 1fr 520px; gap:26px; }
.coverart { zoom:.86; display:flex; gap:14px; justify-content:center; }
.shot { display:flex; flex-direction:column; align-items:center; }
.cap { margin-top:-4px; background:#0a12a8; color:#fff; font-size:10.5px; font-weight:700; padding:6px 10px; border-radius:6px; width:230px; text-align:center; }
.hero { display:grid; grid-template-columns: 1fr 520px; gap:24px; align-items:start; }
.shots2 { display:flex; gap:12px; }
.hero.rev { grid-template-columns: 520px 1fr; }
.strip { position:absolute; left:52px; right:52px; bottom:52px; display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
.pitch { font-size:16px; line-height:1.45; color:#fff; margin:0 0 14px; font-weight:600; }
.loop { display:flex; align-items:center; gap:4px; margin:-4px 0 14px; }
.step { flex:1; background:#161d2b; border-radius:10px; padding:8px 4px; text-align:center; }
.step b { display:block; font-size:11px; margin-top:3px; }
.step small { display:block; font-size:9.5px; color:#9aa6ba; margin-top:2px; }
.dot { display:inline-block; width:14px; height:14px; border-radius:50%; }
.arr { color:#8f9bb0; font-size:20px; font-weight:800; }
.tag { font-size:8.5px; font-weight:900; padding:1px 5px; border-radius:4px; letter-spacing:.04em; vertical-align:1px; }
.tag.s { background:#1d5c3a; color:#8ff0b5; } .tag.i { background:#5c4a1d; color:#ffd98a; } .tag.p { background:#3d2a66; color:#d2b6ff; }
.note { background:#121a2a; border-left:4px solid #59d8ff; padding:10px 14px; border-radius:8px; font-size:12px; line-height:1.5; color:#c7d0de; margin-top:12px; }
.note.small { font-size:10.5px; }
table { width:100%; border-collapse:separate; border-spacing:0; background:#161d2b; border-radius:12px; overflow:hidden; font-size:11.5px; }
th { text-align:left; background:#1f2940; color:#59d8ff; padding:8px 12px; font-size:11px; letter-spacing:.03em; }
td { padding:7px 12px; border-top:1px solid #222c40; color:#dbe2ee; vertical-align:top; line-height:1.4; }
td.src { color:#8f9bb0; font-size:10.5px; }
table.cmp td:first-child { color:#ffc84a; font-weight:700; width:150px; }
.srcs { columns:2; column-gap:30px; font-size:10.2px; line-height:1.35; padding-left:18px; margin:0; color:#dbe2ee; }
.srcs li { margin-bottom:6px; break-inside:avoid; }
.srcs a { color:#59d8ff; text-decoration:none; word-break:break-all; font-size:9px; }
"""

with open(OUT, "w") as f:
    f.write(f"<!doctype html><html><head><meta charset='utf-8'><title>Two Small Roguelites</title><style>{CSS}</style></head><body>{''.join(pages)}</body></html>")
print("pages:", len(pages))
