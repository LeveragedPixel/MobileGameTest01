"""Web of Dice brief in the house style. Facts come from the webofdice repo
(README.md, DESIGN.md, V2_REQUIREMENTS.md, BALANCE_SPEC.md, docs/game_data.json).
Mockups are landscape (the game is 1280x720) and use art/pal.gd colours."""
import os, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "build_prototype_briefs.py")).read())  # pulls in build.py helpers + CSS2/render/mkpage

# art/pal.gd
P = dict(OUT="#1a0f0c", BG="#140d0b", MID="#2a1b16", WOOD="#3a2418", WOODL="#5a3a24", PARCH="#e8d4a2",
         PARCHD="#c9ad73", GOLD="#f2b94b", GOLDD="#b87a1e", CREAM="#f6e8c8", RED="#d9534f", REDD="#8e2a2a",
         GREEN="#6cc070", GREEND="#2f6b3a", TEAL="#4fb3a9", BLUE="#4a7fd0", PURPLE="#7a5aa8", BONE="#eee3c8",
         STEEL="#b9c3cf", FIRE="#f0792a")
TC = {"guild": "#c9962e", "fight": "#b83a35", "elite": "#7a2e6e", "tavern": "#c77b2c", "shop": "#4b8f5a",
      "camp": "#d9661e", "event": "#3f6fb5", "cage": "#6b7a8a", "ruin": "#7d7466", "boss": "#8a1424", "road": "#8a7650"}
WC = P["GOLD"]
LW, LH = 480, 270


def lscreen(inner, caption, disp=480):
    gid = "L" + str(abs(hash(caption)) % 10**8)
    w, h = LW + 16, LH + 16
    return f"""<div class="shot"><svg viewBox="0 0 {w} {h}" width="{disp}" height="{disp*h/w:.0f}" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">
<defs><clipPath id="c{gid}"><rect x="8" y="8" width="{LW}" height="{LH}" rx="14"/></clipPath></defs>
<rect width="{w}" height="{h}" rx="20" fill="#05070c" stroke="#2a3346" stroke-width="2"/>
<g clip-path="url(#c{gid})"><rect x="8" y="8" width="{LW}" height="{LH}" fill="{P['BG']}"/><g transform="translate(8,8)">{inner}</g></g>
</svg><div class="cap" style="width:{disp-20}px">{caption}</div></div>"""


def wbtn(x, y, w, h, fill, t1, t2="", tc="#fff", fs=10):
    o = box(x, y, w, h, fill, 7, P["OUT"], 2.5)
    if t2:
        o += txt(x + w / 2, y + h / 2 - 1, t1, fs, tc, 900) + txt(x + w / 2, y + h / 2 + 10, t2, fs * 0.72, tc, 700, op=.9)
    else:
        o += txt(x + w / 2, y + h / 2 + fs * 0.36, t1, fs, tc, 900)
    return o


def wtop(gold="74", pots="3", danger=6):
    o = box(0, 0, LW, 26, P["WOOD"], 0) + f'<line x1="0" y1="26" x2="{LW}" y2="26" stroke="{P["OUT"]}" stroke-width="3"/>'
    o += f'<circle cx="16" cy="13" r="7" fill="{P["GOLD"]}" stroke="{P["OUT"]}" stroke-width="2"/>' + txt(30, 17, gold, 10, P["CREAM"], 900, "start")
    o += f'<rect x="64" y="5" width="9" height="15" rx="3" fill="{P["RED"]}" stroke="{P["OUT"]}" stroke-width="2"/>' + txt(78, 17, pots, 10, P["CREAM"], 900, "start")
    o += txt(110, 17, "DANGER", 8, P["PARCHD"], 900, "start") + box(150, 8, 120, 10, P["MID"], 5, P["OUT"], 1.5)
    o += box(150, 8, 6 * danger, 10, P["FIRE"] if danger >= 10 else P["GOLD"], 5)
    o += f'<line x1="210" y1="5" x2="210" y2="21" stroke="{P["RED"]}" stroke-width="2"/>'
    o += txt(282, 17, f"{danger}/20", 9, P["CREAM"], 800, "start")
    o += txt(330, 17, "VISION 1", 8.5, P["TEAL"], 900, "start")
    return o


def node(x, y, kind, label="", fog=False, glow=False, used=False, r=11):
    if fog:
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#8f8a7a" stroke="{P["OUT"]}" stroke-width="2" opacity=".7"/>' + txt(x, y + 4, "?", 11, "#3a332a", 900)
    c = TC["road"] if used else TC[kind]
    o = ""
    if glow:
        o += f'<circle cx="{x}" cy="{y}" r="{r+6}" fill="none" stroke="{P["GOLD"]}" stroke-width="3" opacity=".9"/>'
    o += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{P["OUT"]}" stroke-width="2.5"/>'
    sym = {"guild": "G", "fight": "⚔", "elite": "☠", "tavern": "T", "shop": "$", "camp": "▲", "event": "?", "cage": "#", "ruin": "R", "boss": "♛", "road": ""}[kind if not used else "road"]
    o += txt(x, y + 4, sym, 10, "#fff", 900)
    if label:
        o += txt(x, y + r + 11, label, 7.5, P["OUT"], 800)
    return o


def w_map(popup=True):
    o = f'<rect x="0" y="26" width="{LW}" height="{LH-26}" fill="{P["PARCH"]}"/>'
    random.seed(8)
    for _ in range(40):
        o += f'<circle cx="{random.randint(0,LW)}" cy="{random.randint(30,LH)}" r="{random.randint(6,20)}" fill="{P["PARCHD"]}" opacity=".25"/>'
    N = {"g": (70, 200, "guild", "Guild"), "a": (140, 150, "fight", "Old Mill Bridge"), "b": (130, 235, "tavern", "Gilded Boar"),
         "c": (215, 110, "event", ""), "d": (220, 195, "shop", "Wenna's Cart"), "e": (290, 70, "fight", ""),
         "f": (300, 160, "elite", ""), "h": (300, 240, "camp", ""), "i": (370, 110, "ruin", ""), "j": (380, 200, "cage", ""),
         "k": (440, 70, "boss", ""), "l": (445, 160, "fight", "")}
    E = ["ga", "gb", "ac", "ad", "bd", "bh", "ce", "cf", "df", "dh", "ei", "fi", "fj", "hj", "ik", "jl", "il", "kl"]
    route = {"ad", "df"}
    for a, b in E:
        x1, y1 = N[a][:2]; x2, y2 = N[b][:2]
        if a + b in route:
            o += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{P["GOLD"]}" stroke-width="6" opacity=".85"/>'
        o += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{P["WOODL"]}" stroke-width="2.5" stroke-dasharray="5 4"/>'
    fog = set("eijkl")
    for k, (x, y, kind, lab) in N.items():
        o += node(x, y, kind, lab, fog=k in fog, glow=k in "cd" or k == "b", used=k == "g" and False)
    # party token at Old Mill Bridge
    o += f'<circle cx="140" cy="150" r="15" fill="none" stroke="{P["CREAM"]}" stroke-width="3"/>' + chibi(140, 128, P["BLUE"], hat="helm", s=0.55)
    o += wtop()
    o += wbtn(10, 236, 74, 26, P["GOLDD"], "INVENTORY", fs=8) + wbtn(90, 236, 56, 26, P["REDD"], "POTION", fs=8)
    if popup:
        o += box(318, 34, 154, 66, P["PARCH"], 8, P["OUT"], 2.5)
        o += txt(395, 52, "QUEST: Slay the Captain", 8.5, P["OUT"], 900)
        o += txt(395, 66, "at Wenna's Cart → The Salt Road", 7.5, P["WOOD"], 700)
        o += txt(395, 82, "Reward: Ember Blade (+2 ATK)", 8, P["GREEND"], 900)
        o += txt(395, 94, "Route highlighted in gold", 7, P["WOODL"], 700)
    return o


def foe(x, y, kind, s=1.0):
    g = f'<g transform="translate({x},{y}) scale({s})">' + '<ellipse cx="0" cy="30" rx="22" ry="5" fill="#00000066"/>'
    if kind == "wolf":
        g += f'<ellipse cx="0" cy="12" rx="24" ry="13" fill="#7d8a99" stroke="{P["OUT"]}" stroke-width="2.5"/>'
        g += f'<ellipse cx="-20" cy="2" rx="11" ry="9" fill="#7d8a99" stroke="{P["OUT"]}" stroke-width="2.5"/>'
        g += f'<polygon points="-26,-6 -22,-16 -18,-6" fill="#7d8a99" stroke="{P["OUT"]}" stroke-width="2"/>'
        g += '<circle cx="-24" cy="1" r="2" fill="#ffdc4b"/>'
        for lx in (-14, -4, 8, 16):
            g += f'<rect x="{lx}" y="20" width="5" height="10" fill="#5d6a79" stroke="{P["OUT"]}" stroke-width="1.5"/>'
    elif kind == "goblin":
        g += f'<rect x="-9" y="4" width="18" height="22" rx="6" fill="#6b4a2a" stroke="{P["OUT"]}" stroke-width="2.5"/>'
        g += f'<circle cx="0" cy="-6" r="12" fill="#7fae4a" stroke="{P["OUT"]}" stroke-width="2.5"/>'
        g += f'<polygon points="-12,-8 -24,-14 -12,-2" fill="#7fae4a" stroke="{P["OUT"]}" stroke-width="2"/><polygon points="12,-8 24,-14 12,-2" fill="#7fae4a" stroke="{P["OUT"]}" stroke-width="2"/>'
        g += '<circle cx="-4" cy="-7" r="2.5" fill="#ffdc4b"/><circle cx="4" cy="-7" r="2.5" fill="#ffdc4b"/>'
    elif kind == "king":
        g += f'<rect x="-18" y="0" width="36" height="34" rx="8" fill="#3a2a4a" stroke="{P["OUT"]}" stroke-width="3"/>'
        g += f'<circle cx="0" cy="-12" r="17" fill="{P["BONE"]}" stroke="{P["OUT"]}" stroke-width="3"/>'
        g += f'<polygon points="-16,-24 -10,-40 -4,-28 0,-42 4,-28 10,-40 16,-24" fill="{P["GOLD"]}" stroke="{P["OUT"]}" stroke-width="2"/>'
        g += '<circle cx="-6" cy="-12" r="4" fill="#3a0a14"/><circle cx="6" cy="-12" r="4" fill="#3a0a14"/>'
    return g + "</g>"


def hpbar(x, y, w, frac, col):
    return box(x, y, w, 5, "#00000088", 2) + box(x, y, w * frac, 5, col, 2)


def w_battle():
    o = f'<rect width="{LW}" height="{LH}" fill="{P["WOOD"]}"/>'
    for k in range(0, LW, 40):
        o += f'<line x1="{k}" y1="40" x2="{k+20}" y2="{LH}" stroke="{P["MID"]}" stroke-width="10" opacity=".35"/>'
    o += f'<ellipse cx="240" cy="185" rx="230" ry="60" fill="{P["WOODL"]}" opacity=".5"/>'
    # turn order bar
    o += box(120, 6, 240, 30, "#00000077", 8)
    order = [(P["BLUE"], "helm", True), ("#7d8a99", None, False), (P["GREEND"], "hood", False), ("#7fae4a", None, False), (P["PURPLE"], "wizard", False)]
    for k, (c, h, act) in enumerate(order):
        x = 140 + k * 46
        o += f'<circle cx="{x}" cy="21" r="{13 if act else 10}" fill="{c}" stroke="{P["GOLD"] if act else P["OUT"]}" stroke-width="{3 if act else 2}"/>'
    o += txt(240, 46, "ROUND 2 · Bram's turn", 8, P["CREAM"], 800)
    # heroes
    heroes = [(70, 150, P["BLUE"], "helm", 0.8, "Bram"), (115, 175, P["GREEND"], "hood", 0.55, "Vex"), (60, 205, P["PURPLE"], "wizard", 0.35, "Ilsa")]
    for x, y, c, h, f, n in heroes:
        o += chibi(x, y, c, hat=h, s=1.0) + hpbar(x - 16, y + 36, 32, f, P["GREEN"] if f > .4 else P["FIRE"])
    o += '<circle cx="70" cy="150" r="30" fill="none" stroke="#f2b94b" stroke-width="2" stroke-dasharray="4 3"/>'
    # enemies
    o += foe(330, 145, "wolf") + hpbar(310, 182, 40, .7, P["RED"])
    o += foe(400, 190, "goblin") + hpbar(380, 224, 40, .35, P["RED"])
    o += box(360, 92, 100, 38, P["PARCH"], 6, P["OUT"], 2) + txt(410, 107, "Road Wolf  14/20", 8, P["OUT"], 900) + txt(410, 121, "Your hit chance: 60%", 7.5, P["GREEND"], 900)
    # rolled d20
    o += d20(230, 120, 26, P["GOLD"], "17", P["OUT"]) + txt(230, 160, "HIT! 9 damage", 10, P["CREAM"], 900)
    # action bar
    o += box(0, 232, LW, 38, P["MID"], 0)
    acts = [(P["REDD"], "1 ATTACK", "60% · 1d8+3"), (P["GOLDD"], "2 POWER STRIKE", "70% · 2d8+3"), ("#2f4f7a", "3 DEFEND", "+4 DEF"),
            (P["GREEND"], "4 POTION", "3 left"), ("#555", "5 FLEE", "55%")]
    for k, (c, a, b) in enumerate(acts):
        o += wbtn(6 + k * 94, 236, 88, 30, c, a, b, fs=8.5)
    return o


def w_party():
    o = f'<rect width="{LW}" height="{LH}" fill="{P["MID"]}"/>' + txt(240, 22, "CHOOSE YOUR PARTY (3)", 13, P["GOLD"], 900)
    cls = [("Barbarian", "#b5651d", "helm"), ("Bard", "#c0508a", "hood"), ("Cleric", "#e8e0c8", "helm"), ("Druid", "#4e8a3a", "hood"),
           ("Fighter", P["BLUE"], "helm"), ("Monk", "#d9a03a", None), ("Paladin", "#c9c9e0", "helm"), ("Ranger", P["GREEND"], "hood"),
           ("Rogue", "#3a3a4a", "hood"), ("Sorcerer", "#c0392b", "wizard"), ("Warlock", "#4a2a6a", "hood"), ("Wizard", P["PURPLE"], "wizard")]
    picks = {"Fighter": 1, "Cleric": 2, "Ranger": 3}
    for k, (n, c, h) in enumerate(cls):
        x, y = 14 + (k % 4) * 114, 34 + (k // 4) * 66
        p = n in picks
        o += box(x, y, 108, 60, P["PARCH"] if p else P["WOOD"], 7, P["GOLD"] if p else P["OUT"], 3 if p else 2)
        o += chibi(x + 22, y + 26, c, hat=h, s=0.62)
        o += txt(x + 44, y + 20, n.upper(), 8.5, P["OUT"] if p else P["CREAM"], 900, "start")
        o += txt(x + 44, y + 33, "HP · ATK · DEF", 6.5, P["WOODL"] if p else P["PARCHD"], 700, "start")
        if p:
            o += f'<circle cx="{x+100}" cy="{y+8}" r="9" fill="{P["GOLD"]}" stroke="{P["OUT"]}" stroke-width="2"/>' + txt(x + 100, y + 12, str(picks[n]), 9, P["OUT"], 900)
    o += wbtn(14, 236, 110, 28, P["WOODL"], "RANDOM PARTY", fs=9) + wbtn(356, 236, 110, 28, P["GOLDD"], "START", fs=11)
    o += txt(240, 255, "Fighter · Cleric · Ranger", 9, P["CREAM"], 800)
    return o


def w_death():
    o = f'<rect width="{LW}" height="{LH}" fill="{P["WOOD"]}"/>' + f'<ellipse cx="240" cy="200" rx="230" ry="50" fill="{P["WOODL"]}" opacity=".5"/>'
    # downed hero lying
    o += f'<g transform="translate(150,190) rotate(-83)">{chibi(0, 0, "#7d8a99", "#b9b2a6", "hood", 1.1)}</g>'
    o += txt(150, 150, "DOWN", 12, P["RED"], 900)
    for k in range(3):
        o += f'<circle cx="{118+k*14}" cy="128" r="5" fill="{P["GREEN"] if k < 2 else "#00000066"}" stroke="{P["OUT"]}" stroke-width="1.5"/>'
        o += f'<circle cx="{162+k*14}" cy="128" r="5" fill="{P["RED"] if k < 1 else "#00000066"}" stroke="{P["OUT"]}" stroke-width="1.5"/>'
    o += txt(140, 116, "SAVES 2 ✓  1 ✗", 8, P["CREAM"], 800)
    o += d20(320, 120, 40, P["GOLD"], "20", P["OUT"])
    o += txt(320, 186, "NATURAL 20", 16, P["GOLD"], 900) + txt(320, 204, "Vex is back up with 1 HP!", 10, P["CREAM"], 800)
    o += box(14, 14, 170, 36, "#00000077", 8) + txt(99, 30, "Death saving throw", 9, P["CREAM"], 900) + txt(99, 43, "d20: 10+ success, 1 = two failures", 7, P["PARCHD"], 700)
    o += box(330, 14, 136, 36, "#00000077", 8) + txt(398, 30, "Revives left: ●●○", 9, P["CREAM"], 900) + txt(398, 43, "3 per career, then permadeath", 7, P["PARCHD"], 700)
    return o


def w_guild():
    o = f'<rect width="{LW}" height="{LH}" fill="{P["MID"]}"/>'
    o += box(10, 10, 460, 250, P["PARCH"], 10, P["OUT"], 3) + txt(240, 32, "THE GUILD HALL", 14, P["OUT"], 900)
    o += txt(24, 54, "QUESTS", 9, P["REDD"], 900, "start")
    qs = [("Slay the Bandit Captain", "Ember Blade +2 ATK"), ("Deliver the sealed letter", "+1 map vision"), ("Hunt the Marsh Ogre", "Battle Focus")]
    for k, (a, b) in enumerate(qs):
        y = 62 + k * 30
        o += box(20, y, 214, 26, P["CREAM"], 5, P["PARCHD"], 1.5) + txt(28, y + 11, a, 7.5, P["OUT"], 900, "start") + txt(28, y + 21, "Reward: " + b, 6.5, P["GREEND"], 800, "start")
        o += wbtn(196, y + 4, 34, 18, P["GOLDD"], "TAKE", fs=6.5)
    o += txt(250, 54, "HIRE (4d6 drop lowest)", 9, P["REDD"], 900, "start")
    hires = [("Druid", "#4e8a3a", "hood", "48g"), ("Monk", "#d9a03a", None, "62g"), ("Warlock", "#4a2a6a", "hood", "35g")]
    for k, (n, c, h, g) in enumerate(hires):
        x = 250 + k * 72
        o += box(x, 62, 66, 88, P["CREAM"], 6, P["PARCHD"], 1.5) + chibi(x + 33, 92, c, hat=h, s=0.7)
        o += txt(x + 33, 126, n, 8, P["OUT"], 900) + wbtn(x + 10, 132, 46, 14, P["GREEND"], g, fs=7)
    o += txt(24, 168, "GUILD UPGRADES (banked gold, kept forever)", 9, P["REDD"], 900, "start")
    ups = [("Far Sight", "+1 vision", "40g"), ("Hardy Recruits", "+5 HP", "25g"), ("Guild Rations", "+1 potion", "30g")]
    for k, (a, b, c) in enumerate(ups):
        x = 20 + k * 150
        o += box(x, 176, 142, 34, P["CREAM"], 5, P["PARCHD"], 1.5) + txt(x + 8, 190, a, 8, P["OUT"], 900, "start") + txt(x + 8, 202, b, 7, P["WOODL"], 700, "start")
        o += wbtn(x + 96, 182, 40, 20, P["GOLDD"], c, fs=7.5)
    o += wbtn(20, 222, 120, 28, P["GREEND"], "REST · 5g", "full HP, revive, recharge", fs=9)
    o += wbtn(340, 222, 120, 28, P["WOODL"], "CLOSE", fs=10)
    return o


def w_inventory():
    o = f'<rect width="{LW}" height="{LH}" fill="{P["MID"]}"/>' + txt(240, 22, "INVENTORY", 13, P["GOLD"], 900)
    o += box(12, 32, 150, 228, P["WOOD"], 8, P["OUT"], 2)
    o += txt(22, 50, "Gold 74", 10, P["GOLD"], 900, "start")
    pots = [("Healing d8+6", 2, P["RED"]), ("Greater d10+10", 1, P["FIRE"]), ("Superior d20+15", 0, P["PURPLE"])]
    for k, (n, c, col) in enumerate(pots):
        y = 62 + k * 26
        o += f'<rect x="22" y="{y}" width="10" height="17" rx="3" fill="{col}" stroke="{P["OUT"]}" stroke-width="1.5"/>' + txt(38, y + 12, f"{n}  x{c}", 7.5, P["CREAM"], 800, "start")
    o += txt(22, 150, "CHARMS", 8.5, P["PARCHD"], 900, "start")
    for k, n in enumerate(["Hare's Foot x2", "Grave Token x1", "Wolf Fang x1", "Lucky Coin x1"]):
        o += f'<polygon points="{26},{160+k*20} {29},{166+k*20} {35},{166+k*20} {30},{170+k*20} {32},{176+k*20} {26},{172+k*20} {20},{176+k*20} {22},{170+k*20} {17},{166+k*20} {23},{166+k*20}" fill="{P["GOLD"]}"/>'
        o += txt(40, 170 + k * 20, n, 7.5, P["CREAM"], 700, "start")
    heroes = [("Bram", "Fighter", P["BLUE"], "helm", "UP", "Enspelled +2", .8), ("Vex", "Rogue", P["GREEND"], "hood", "DOWN", "None", 0), ("Ilsa", "Wizard", P["PURPLE"], "wizard", "UP", "Adamantine +1", .45)]
    for k, (n, c, col, h, st, gear, f) in enumerate(heroes):
        x = 170 + k * 102
        o += box(x, 32, 96, 228, P["WOOD"], 8, P["OUT"], 2) + chibi(x + 48, 70, col if f else "#777", hat=h, s=0.9)
        o += txt(x + 48, 108, n, 10, P["CREAM"], 900) + txt(x + 48, 120, c, 7.5, P["PARCHD"], 700)
        o += hpbar(x + 10, 128, 76, f, P["GREEN"]) + pill(x + 24, 140, 48, 14, P["GREEN"] if st == "UP" else P["RED"], st, P["OUT"], 7.5)
        for j, s in enumerate(["STR", "DEX", "CON", "INT", "WIS", "CHA"]):
            o += txt(x + 18 + (j % 3) * 30, 172 + (j // 3) * 18, s, 6.5, P["PARCHD"], 800)
        o += txt(x + 48, 222, "Gear: " + gear, 7, P["GOLD"], 800) + txt(x + 48, 238, "Revives ●●○", 7, P["CREAM"], 700)
    return o


def w_title():
    o = f'<rect width="{LW}" height="{LH}" fill="{P["BG"]}"/>'
    o += f'<ellipse cx="240" cy="290" rx="300" ry="120" fill="{P["WOOD"]}"/>'
    for k in range(10):
        a = k * 36
        o += f'<line x1="240" y1="110" x2="{240+220*math.cos(math.radians(a))}" y2="{110+150*math.sin(math.radians(a))}" stroke="{P["GOLDD"]}" stroke-width="1.2" opacity=".35"/>'
    o += f'<circle cx="240" cy="110" r="70" fill="none" stroke="{P["GOLDD"]}" stroke-width="1.2" opacity=".35"/><circle cx="240" cy="110" r="120" fill="none" stroke="{P["GOLDD"]}" stroke-width="1.2" opacity=".3"/>'
    o += d20(240, 92, 34, P["GOLD"], "20", P["OUT"])
    o += txt(240, 160, "WEB OF DICE", 30, P["CREAM"], 900)
    o += wbtn(180, 176, 120, 26, P["GOLDD"], "PLAY", fs=12) + wbtn(150, 208, 86, 22, P["WOODL"], "GUILD HALL", fs=8) + wbtn(244, 208, 86, 22, P["REDD"], "HARDCORE", fs=8)
    o += chibi(80, 225, P["BLUE"], hat="helm") + chibi(120, 232, P["GREEND"], hat="hood") + chibi(400, 228, P["PURPLE"], hat="wizard")
    return o


# ------------------------------------------------------------------ pages
wd = []
q = mkpage(wd, "Web of Dice · design brief", WC)
TG = '<div class="tags" style="--k:#f2b94b"><span>D&amp;D-STYLE DICE ROGUELITE</span><span>PARTY OF 3</span><span>WEB MAP</span><span>GODOT 4.7 · MILESTONE 3b</span></div>'


def built():
    return '<span class="tag s">IN BUILD</span>'


wd.append(f"""<section class="page cover">
<div class="kicker" style="color:{WC}">GAME DESIGN BRIEF · FROM THE LIVE PROJECT</div>
<h1 class="big">WEB OF DICE</h1>
<div class="sub">Pick 3 heroes, walk a web of places, take quests, fight with d20 duels, and bank gold at the Guild</div>
{TG}
<div class="covergrid" style="grid-template-columns:1fr 500px">
 <div>
  {panel("One-line pitch", "A mobile + PC roguelite where you walk a web of places (tavern, field, ruins…) from a Guild hub, make risky dice-driven choices, take optional quests, and survive to a major final battle.", WC)}
  {panel("Reading Key", "This brief describes the game as it exists in the repo today:", YE,
         [built() + " Built and tested in code (file references in footers)",
          sug() + " My recommendation, not in the game yet",
          '<span class="tag i">OPEN</span> Listed as unfinished in the project docs',
          "Mockups are drawn for this brief in the game's own palette (art/pal.gd); they are not screenshots"])}
 </div>
 <div class="coverart" style="flex-direction:column;zoom:.92">{lscreen(w_title(), "Title: PLAY · GUILD HALL · HARDCORE", 480)}</div>
</div>
<div class="strip">
 {panel("Loop &amp; map", "Guild, web, danger, quests (p.2)", WC)}
 {panel("Battle &amp; party", "d20 duels, 12 classes, death saves (p.3–5)", RE)}
 {panel("Economy &amp; balance", "Gold, items, Guild upgrades, Balance v3 (p.6–7)", PU)}
 {panel("Where it fits &amp; next", "vs. our concepts, mobile path, next steps (p.8–10)", GR)}
</div>
<div class="foot"><i>Web of Dice · design brief · sources: README.md, DESIGN.md, V2_REQUIREMENTS.md, BALANCE_SPEC.md, docs/game_data.json</i><span>01</span></div></section>""")

q("1. CORE LOOP &amp; THE WEB MAP", "Walk the Web. Watch the Danger. Get Home.", loop([
    ("GUILD", "Quests · rest · hire"), ("PARTY", "Pick 3 of 12"), ("WALK", "One step at a time"), ("RESOLVE", "Fight · event · shop"),
    ("QUEST", "Follow the gold route"), ("BANK", "Return to the Guild"), ("BOSS", "The Hollow King")], [WC, RE, CY, PU]) + f"""
<div class="hero" style="grid-template-columns:1fr 600px">
 <div class="herotext">
  {panel(built() + " The web", "A seeded 30-place graph you can walk in any direction. Only neighbours are clickable. Vision starts at 1 step (max 3); farther places show as fog '?'. Every place has a unique name (Old Mill Bridge, The Gilded Boar…), and used places become plain road.", WC)}
  {panel(built() + " Danger meter", "+1 per step (max 20), reset to 0 at the Guild; taverns and camps lower it. Each step rolls an ambush: 3% + 2% × danger (max 50%). From 10 danger, enemies get +15% HP and +1 damage per step.", RE)}
  {panel(built() + " Places", "Guild · Fight · Elite (never within 3 steps of the Guild) · Tavern (rest, or rumours that reveal the boss) · Camp · Shop · Event (d20 choices) · Cage (pick a lock, 60%) · Ruin · Final Battle.", PU)}
 </div>
 <div style="display:flex;flex-direction:column;gap:6px">{lscreen(w_map(), "Map: glowing neighbours, fog, a quest route in gold, the danger bar", 600)}</div>
</div>""", "Facts from docs/game_data.json (nodes, danger_meter, vision) and scripts/logic/graph.gd.")

q("2. BATTLE", "Every Roll Shows Its Odds", f"""
<div class="hero" style="grid-template-columns:600px 1fr">
 <div>{lscreen(w_battle(), "Battle: turn bar, the d20 result, odds on every button", 600)}</div>
 <div class="herotext">
  {panel(built() + " The rule", "Hit if <b>d20 + to-hit ≥ 10 + DEF</b>. Natural 20 = critical hit (damage dice doubled); natural 1 = FUMBLE (your next d20 has disadvantage). The % printed on each button is the exact chance; tests check it over 20,000 rolls.", WC)}
  {panel(built() + " A turn", "Initiative d20 sets the order. Each hero picks <b>1 Attack · 2 Skill · 3 Defend · 4 Potion · 5 Flee</b> (55%, not allowed vs the boss), plus a 6th button for hirelings. Skills recharge on a d6 roll of 5–6.", CY)}
  {panel(built() + " Enemies telegraph", "Each enemy glows, shows its target arrow and hit chance, then attacks. The Ogres, Troll, Bandit Captain and the boss attack twice. <b>The Hollow King</b> enrages at half HP (+1 hit, +2 damage) and summons a Bone Rattler.", RE)}
 </div>
</div>
<div class="note">{sug()} This is the strongest hook in the project, and it's the same one GPT picked out of Delve &amp; Dice: <b>dice you can see, with honest odds</b>. Make the d20 roll the hero of every trailer and screenshot.</div>
""", "Battle rules: README.md 'Battle rules (milestone 2)' and 'Milestone 3a'; scripts/logic/battle_rules.gd, dice.gd.")

cls_rows = [("Barbarian", "Frontline bruiser", 34, "Rage: +2 dmg, half damage taken"), ("Bard", "Support and buffs", 20, "Rousing Song: all heal 3, ally Inspired"),
            ("Cleric", "Healer and shield", 26, "Mending Light: heal 9, raises the downed"), ("Druid", "Nature caster", 24, "Entangling Roots 1d8+3 + weaken"),
            ("Fighter", "Armoured tank", 30, "Power Strike 2d8+3, stun"), ("Monk", "Quick striker", 22, "Flurry 2 × (1d6+3)"),
            ("Paladin", "Holy knight", 28, "Divine Smite +2d8"), ("Ranger", "Ranged hunter", 24, "Twin Arrows 2 × (1d8+3)"),
            ("Rogue", "Burst damage", 22, "Backstab: advantage, +2d6"), ("Sorcerer", "Area spells", 20, "Chaos Burst 2d6+1 on every foe"),
            ("Warlock", "Dark blaster", 24, "Eldritch Barrage 2 × (1d10+3), costs 3 HP"), ("Wizard", "Arcane nuker", 20, "Arcane Bolt 3d4+3, ignores armour")]
ctbl = "<table style='font-size:10.5px'><tr><th>Class</th><th>Role</th><th>HP</th><th>Signature skill</th></tr>" + "".join(
    f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in cls_rows) + "</table>"
q("3. PARTY &amp; CLASSES", "Twelve Classes, Pick Three", f"""
<div class="hero" style="grid-template-columns:1fr 480px">
 <div>{ctbl}</div>
 <div>{lscreen(w_party(), "Party select: 4 × 3 cards, order badges, RANDOM PARTY", 480)}
  <div class="note" style="margin-top:8px">{built()} Each class has a hit die, main stat, armour, one signature skill, a flaw note and 2 subclass tags (subclass skills go to hirelings only). Stats derive D&amp;D-style from six ability scores: HP = 2 × hit die + 6 + 2 × CON mod.</div>
 </div>
</div>""", "Classes: scripts/logic/classes.gd; HP values from README 'Balance v3'. All 12 are unlocked from the start (Meta.starter_classes).")

q("4. DEATH, SAVES &amp; HIRELINGS", "Heroes Fall. Some Get Back Up.", f"""
<div class="hero" style="grid-template-columns:600px 1fr">
 <div>{lscreen(w_death(), "Death save: tracker dots, the d20 verdict, revives left", 600)}</div>
 <div class="herotext">
  {panel(built() + " Down, not out", "At 0 HP a hero is DOWN. On their turn they roll a death save: 10+ success, under 10 failure, natural 1 = two failures, natural 20 = back up with 1 HP. 3 successes = stable; 3 failures = <b>dead for good</b>.", RE)}
  {panel(built() + " Revive cap", "Potions, heal skills or a rest raise a downed hero. Each hero has <b>3 revives per career</b>; going down with none left is instant death. Dead heroes take their gear with them.", PU)}
  {panel(built() + " Hirelings", "The Guild offers 3 hires per visit: random class and subclass, stats rolled 4d6-drop-lowest, 30–100 gold. Only hires get the subclass skill (a 6th button).", GR)}
 </div>
</div>
<div class="note">{sug()} Death saves are the most dramatic moment in the game. Give them the full 'Loot Roll' treatment from our concept briefs: slow the roll down, then celebrate a natural 20 with flash and sound.</div>
""", "Death rules: V2_REQUIREMENTS.md B and D; README 'Milestone 3a' and '3b' (death-save visuals in battle.gd, Character2D).")

q("5. ECONOMY, ITEMS &amp; META", "Gold, Potions, Charms, Gear and the Guild", f"""
<div class="hero" style="grid-template-columns:1fr 600px">
 <div class="herotext">
  <div class="cols2 tight">
  {panel(built() + " Potions", "Healing d8+6 (10g) · Greater d10+10 (20g) · Superior d20+15 (loot only). Shared stock; a potion can revive a downed hero.", RE)}
  {panel(built() + " Charms", "9 stackable passives: Hare's Foot +1 init, Grave Token +2 death saves, Wolf Fang +1 dmg, Lucky Coin, Iron Nail, Merchant's Seal… Lost when the run ends.", WC)}
  {panel(built() + " Gear chain", "None → Adamantine +1 → Enspelled +2 → Vorpal +3 attack. Shop 60g, or loot. Belongs to one hero; lost if that hero dies.", PU)}
  {panel(built() + " Guild upgrades", "Banked gold buys permanent upgrades: Far Sight (+1 vision), Hardy Recruits (+5 HP), Guild Rations (+1 potion). HARDCORE mode turns them off.", GR)}
  </div>
  {panel(built() + " Quests", "Slay the Bandit Captain → Ember Blade (+2 ATK) · Deliver the sealed letter → +1 vision · Reach the old ruin → 40 gold · Hunt the Marsh Ogre → Battle Focus (skills recharge on 4–6). The route to the target lights up in gold.", CY)}
 </div>
 <div style="display:flex;flex-direction:column;gap:10px">{lscreen(w_guild(), "Guild Hall: quests, hires, upgrades, rest", 600)}</div>
</div>""", "Economy: docs/game_data.json (potions, charms, gear_tiers, shop, guild_upgrades, quests); scripts/logic/data.gd, meta.gd.")

bal = [("normal near", "100%", "12%", "0.01", "4.0"), ("normal deep", "100%", "17%", "0.02", "5.2"), ("elite near", "99%", "27%", "0.13", "5.8"),
       ("elite deep", "94%", "43%", "0.54", "7.7"), ("boss (run party)", "82%", "55%", "1.00", "9.7")]
btbl = "<table><tr><th>Fight (Fighter/Cleric/Ranger)</th><th>Win</th><th>Party HP lost</th><th>Downs / fight</th><th>Rounds</th></tr>" + "".join(
    f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in bal) + "</table>"
q("6. BALANCE v3", "Tuned by Feel, Not Just Win Rate", f"""
<div class="cols2" style="grid-template-columns:1.25fr 1fr">
 <div>{btbl}
  <div class="note">{built()} After the first playtest ("enemies two-shot every hero, Eldritch Blast did 2 damage"), heroes and enemies moved to D&amp;D-style numbers, and a <b>feel report</b> now measures rounds, HP lost, downs, deaths, the largest hit and misses over 300 seeds per row.</div>
 </div>
 <div class="herotext">
  {panel("Target bands (from BALANCE_SPEC.md)", "", WC, ["Normal: 3–5 rounds, 15–35% HP lost, almost no downs", "Elite: 4–6 rounds, 35–60% lost, ~1 down", "Boss: 7–10 rounds, 50–80% lost, 55–75% win", "No single normal hit over 40% of a full-HP hero"])}
  {panel('<span class="tag i">OPEN</span> Bands not met yet', "", RE, [
      "Normal fights are too easy for healer parties (12% HP lost, 100% win)",
      "Bard/Wizard/Rogue struggles in deep elites (62% win)",
      "Only <b>10–53% of bot runs reach the Final Battle</b>; about 3.75 fights per rest place",
      "Nobody has played Balance v3 yet; it's logic and tests only"])}
 </div>
</div>""", "Numbers: README 'Balance v3' after-columns, Fighter/Cleric/Ranger party, 300 seeds per row.")

cmp_rows = [("Hook", "Visible d20 with honest odds, death saves", "Visible d20 boons and a Loot Roll", "Extract or push"),
            ("Party", "3 of 12 classes, turn-based", "3 (GPT: 1 + companion)", "1 hero"),
            ("Map", "30-place web, any direction, fog, danger", "Branching rooms per floor", "Rooms with shrines"),
            ("Combat input", "You pick every action of every hero", "Auto-battle", "Auto-combat + dodge"),
            ("Run → meta", "Bank gold at the Guild", "Gold → tavern", "Extract at a shrine"),
            ("Status", "Built, milestone 3b", "Concept", "Concept")]
mt = "<table><tr><th></th><th>Web of Dice (built)</th><th>Delve &amp; Dice (concept)</th><th>The Last Lantern (concept)</th></tr>" + "".join(
    f"<tr><td style='color:#ffc84a;font-weight:700'>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in cmp_rows) + "</table>"
q("7. WHERE IT FITS", "Web of Dice Already Is Our Dice Game", mt + f"""
<div class="cols3" style="margin-top:14px">
{panel(sug() + " It's further along than any concept", "Everything Delve &amp; Dice proposed (visible dice, D&amp;D classes, a tavern hub) exists here as working code with tests. It would be faster to build on Web of Dice than to start Delve &amp; Dice.", GR)}
{panel(sug() + " It already has 'extract or push'", "Walking back to the Guild to bank gold while danger climbs <i>is</i> The Last Lantern's extract-or-push decision. Make it explicit: show what's at risk on the map and reward the walk home.", YE)}
{panel(sug() + " The big difference: it's mid-core", "You choose every action of every hero, so it's turn-based tactics, not the auto-battle of Cup Heroes and our concepts. That depth is its identity, but it means longer sessions and a smaller mobile audience.", RE)}
</div>""", "Comparison with the Two Small Roguelites and Last Lantern briefs in this repo's docs/concepts.")

q("8. PATH TO MOBILE", "From a PC Build to a Phone", f"""
<div class="hero" style="grid-template-columns:600px 1fr">
 <div>{lscreen(w_inventory(), "Inventory: gold, potions by type, charms, hero panels", 600)}</div>
 <div class="herotext">
  {panel(built() + " Already mobile-friendly", "Touch input works and all hit areas are large. Art is drawn in code (no asset files), so it scales cleanly. The design doc names 'mobile + PC, start as a web build'.", GR)}
  {panel('<span class="tag i">OPEN</span> Landscape at 1280×720', "Phones are usually held upright for casual play. Landscape suits PC and tablets; a portrait battle layout would be a real redesign (heroes over enemies, a two-row action bar).", YE)}
  {panel(sug() + " Monetization, if any", "Keep the Cup Heroes system filter: no gems, no paid random packs, no stamina. Sell a <b>$4.99 one-time unlock</b> or a premium price, plus <b>cosmetics</b> (dice skins, hero outfits). Never sell hirelings, revives or gear, because permadeath only means something if it can't be bought back.", PU)}
 </div>
</div>""", "Mobile notes: DESIGN.md 'Platforms'; README controls (touch, large hit areas); project.godot (1280x720, canvas_items stretch).")

q("9. NEXT STEPS", "What the Project Says Is Next", f"""
<div class="mvp">
{panel('<span class="tag i">OPEN</span> From the project TODO', "", RE, [
    "Nobody has LOOKED at the 3b screens yet; check the 5 screenshot sets",
    "Balance v3 has never been played by a person",
    "Bot runs reach the boss only 10–53% of the time (too few rest places)",
    "Class unlocks exist but nothing locks yet",
    "Hire screen still the 3a version; lying pose is a rotation",
    "Screenshot/window tests disabled until the PC freezes are explained"])}
{panel(sug() + " Before more content", "", WC, [
    "<b>Playtest one full run</b> with your partner on Balance v3",
    "Add 1–2 rest places, or make the Guild walk-back safer, so ~60% of runs reach the boss",
    "Decide on mobile orientation before building more screens",
    "Write down the 'one more run' reason (the Guild unlocks list)"])}
{panel(sug() + " Keep out for now", "", GR, [
    "More classes (12 is already a lot)",
    "A wide-open world map",
    "Online features, guilds, PvP",
    "Any store work until a person has finished a run and wants another"])}
</div>
<div class="note">{sug()} <b>A clear pass/fail test:</b> after one full run, does the tester ask to play again <i>and</i> say which class they'd try next? If yes, the 12-class roster is pulling its weight. If not, cut to 6 for the mobile version.</div>
<div class="note" style="border-color:{PU}"><b>Legal note from the design doc:</b> no D&amp;D trademarks or names; build on open 5e SRD concepts with original world, creatures and names. The project already follows this (e.g. 'Arcane Bolt', 'The Hollow King').</div>
""", "TODOs: README 'TODO / known rough spots after 3b' and 'Spec bands NOT met'. Legal: DESIGN.md 'Content and legal'.")

render(wd, "Web of Dice Brief", os.path.join(HERE, "web_of_dice.html"))
print("web of dice pages", len(wd))
