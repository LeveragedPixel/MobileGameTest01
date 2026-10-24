"""Dice & Dive concept brief (house style). Portrait mobile mockups."""
import os, math

HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "build_prototype_briefs.py")).read())

DA = "#ffc94a"   # gold accent
DT = "#3fd6c6"   # teal
DB1, DB2 = "#123247", "#04090f"

PIPS = {1: [], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
        5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}


def d6(cx, cy, s, face, fill="#f6efe0", held=False, rot=0, pip="#1a1020"):
    g = f'<g transform="translate({cx},{cy}) rotate({rot})">'
    if held:
        g += f'<rect x="{-s/2-5}" y="{-s/2-5}" width="{s+10}" height="{s+10}" rx="{s*0.28}" fill="none" stroke="{DA}" stroke-width="3"/>'
    g += f'<rect x="{-s/2}" y="{-s/2}" width="{s}" height="{s}" rx="{s*0.22}" fill="{fill}" stroke="#1a1020" stroke-width="2.2"/>'
    g += f'<rect x="{-s/2+2}" y="{s/2-6}" width="{s-4}" height="4" rx="2" fill="#00000022"/>'
    if face == 1:  # skull
        r = s * 0.22
        g += f'<circle cx="0" cy="{-r*0.2}" r="{r}" fill="#1a1020"/><rect x="{-r*0.6}" y="{r*0.5}" width="{r*1.2}" height="{r*0.6}" fill="#1a1020"/>'
        g += f'<circle cx="{-r*0.4}" cy="{-r*0.3}" r="{r*0.3}" fill="{fill}"/><circle cx="{r*0.4}" cy="{-r*0.3}" r="{r*0.3}" fill="{fill}"/>'
    else:
        o = s * 0.25
        for px, py in PIPS[face]:
            g += f'<circle cx="{px*o}" cy="{py*o}" r="{s*0.085}" fill="{pip}"/>'
    if held:
        g += pill(-14, s / 2 + 6, 28, 11, DA, "HELD", "#2a1a05", 6.5)
    return g + "</g>"


def topb(lvl="7", c1="340", c2="2"):
    return topbar(lvl, c1, c2, "#1f7a8a")


def nav(active=2):
    return bottomnav(["Shop", "Heroes", "Dive", "Forge", "Daily"], active, "#081620", DA)


def dd_hub():
    i = topb() + pill(14, 52, 92, 22, "#ffffff14", "Surface Camp", "#fff", 9, "#ffffff44") + pill(112, 52, 104, 22, DT, "Daily Dive 1/3", "#04201c", 9, "#fff")
    i += txt(W / 2, 98, "DEPTH RECORD 23", 18, "#fff", 900) + txt(W / 2, 116, "THE DROWNED VAULT", 11, DA, 900)
    # pit
    i += '<ellipse cx="115" cy="190" rx="92" ry="26" fill="#3a4a52" stroke="#1a2a32" stroke-width="4"/>'
    i += '<ellipse cx="115" cy="192" rx="78" ry="19" fill="#02060a"/>'
    for k, y in enumerate((214, 240, 268, 298)):
        w = 70 - k * 12
        i += f'<rect x="{115-w}" y="{y}" width="{2*w}" height="4" rx="2" fill="{DT}" opacity="{0.45-k*0.09}"/>'
    i += txt(115, 330, "▼ ▼ ▼", 12, DT, 900, op=.6)
    i += chibi(58, 168, "#a33b3b", hat="helm", s=0.9) + chibi(172, 168, "#3a3fa3", hat="wizard", s=0.9) + chibi(196, 176, "#2f6b3e", hat="hood", s=0.8)
    for k, x in enumerate((70, 100, 130, 160)):
        i += d6(x, 350, 18, [6, 6, 3, 5][k], "#f6efe0" if k else DA)
    i += pill(52, 370, 126, 32, DA, "DIVE", "#2a1a05", 17, "#fff", 900)
    i += nav(2)
    return phone(i, DB1, DB2, "Surface Camp: one big DIVE button")


def dd_depth():
    i = topb() + txt(W / 2, 66, "THE DIVE", 15, "#fff", 900)
    i += box(70, 80, 90, 340, "#0a1a24", 8, "#1f3a4a", 2)
    floors = list(range(1, 11))
    for k, f in enumerate(floors):
        y = 98 + k * 32
        boss = f in (5, 10)
        cur = f == 7
        c = "#8a1424" if boss else ("#ffc94a" if cur else ("#1f7a8a" if f < 7 else "#2a3a44"))
        i += f'<circle cx="115" cy="{y}" r="{12 if boss else 9}" fill="{c}" stroke="#fff" stroke-width="{3 if cur else 1.5}"/>'
        i += txt(115, y + 4, "☠" if boss else str(f), 9, "#fff", 900)
        if k:
            i += f'<line x1="115" y1="{y-23}" x2="115" y2="{y-11}" stroke="#ffffff44" stroke-width="2"/>'
        if f in (3, 6, 9):
            i += pill(162, y - 8, 56, 16, "#2f6b3e", "CAMP", "#fff", 7.5)
    i += pill(14, 210, 52, 16, DA, "YOU", "#2a1a05", 8)
    i += box(12, 428, 206, 0.1, "#000")
    i += txt(W / 2, 438, "Bosses at 5 and 10 · camps let you surface", 8, "#ffffffaa", 700)
    return phone(i, "#0d2636", DB2, "Depth map: floors, bosses, safe camps")


def dd_battle():
    i = pill(10, 12, 60, 20, "#3a8a3a", "HP 82%", "#fff", 9) + pill(76, 12, 78, 20, "#ffffff22", "FLOOR 7", "#fff", 9) + pill(160, 12, 60, 20, "#ffffff22", "340", "#ffd76a", 9)
    i += box(10, 40, 210, 6, "#ffffff22", 3) + box(10, 40, 130, 6, "#ff6b6b", 3) + txt(W / 2, 60, "WAVE 3/5", 8.5, "#ffffffaa", 800)
    # enemies top
    for x, y, c in [(60, 110, "#6a8a3a"), (115, 95, "#8a3a3a"), (170, 112, "#6a8a3a")]:
        i += f'<ellipse cx="{x}" cy="{y+22}" rx="14" ry="3" fill="#00000066"/><circle cx="{x}" cy="{y}" r="15" fill="{c}" stroke="#1a1020" stroke-width="2"/><circle cx="{x-5}" cy="{y-2}" r="2.5" fill="#ffdc4b"/><circle cx="{x+5}" cy="{y-2}" r="2.5" fill="#ffdc4b"/>'
    i += d20(115, 180, 24, DA, "20", "#2a1a05") + txt(115, 218, "CRIT! 48", 14, DA, 900)
    i += '<line x1="80" y1="270" x2="112" y2="120" stroke="#ffe27a" stroke-width="2" stroke-dasharray="4 3"/>'
    # heroes bottom
    i += chibi(70, 285, "#a33b3b", hat="helm") + chibi(115, 295, "#2f6b3e", hat="hood") + chibi(160, 285, "#3a3fa3", hat="wizard")
    i += pill(10, 330, 64, 20, DT, "AUTO ON", "#04201c", 8.5) + pill(156, 330, 64, 20, "#ffffff22", "x2 ▶▶", "#fff", 9)
    # specials
    specials = [("SMITE", "d20", "#a33b3b", 1.0), ("VOLLEY", "3d6", "#2f6b3e", 0.6), ("NOVA", "2d8", "#3a3fa3", 0.3)]
    for k, (n, d, c, ch) in enumerate(specials):
        x = 40 + k * 75
        i += f'<circle cx="{x}" cy="{400}" r="26" fill="{c}" stroke="#fff" stroke-width="2"/>'
        a = 2 * math.pi * ch - 0.0001
        ex, ey = x + 30 * math.sin(a), 400 - 30 * math.cos(a)
        i += f'<path d="M{x},{370} A30,30 0 {1 if ch > .5 else 0} 1 {ex:.1f},{ey:.1f}" fill="none" stroke="{DA}" stroke-width="4"/>'
        i += txt(x, 398, n, 8, "#fff", 900) + txt(x, 410, d, 8, "#ffe27a", 900)
    i += txt(W / 2, 450, "Tap a charged special to roll it yourself", 8, "#ffffffaa", 700)
    return phone(i, "#1a3040", "#05080c", "Battle: auto + speed, or tap specials")


def dd_boon():
    i = topb() + txt(W / 2, 70, "FLOOR CLEARED", 15, "#ffe27a", 900) + txt(W / 2, 88, "Pick a Dice Boon", 11, "#fff", 700)
    i += chibi(80, 140, "#a33b3b", hat="helm", s=0.8) + chibi(115, 145, "#2f6b3e", hat="hood", s=0.8) + chibi(150, 140, "#3a3fa3", hat="wizard", s=0.8)
    i += box(8, 182, W - 16, 210, "#00000088", 12)
    cy = 200
    i += card(14, cy, 66, 130, "#6b1020", "EXPLODING|SIXES", "FREE", "#ff8a3c", d6(47, cy + 36, 30, 6, "#ffd27a"))
    i += card(82, cy, 66, 130, "#1f4a5a", "LOADED|DIE", "120", "#3fd6c6", d6(115, cy + 36, 30, 5, "#bff4ee") + '<circle cx="128" cy="222" r="6" fill="#3a3a3a"/>')
    i += card(150, cy, 66, 130, "#3a2a5a", "LUCKY|SEVENS", "150", "#b06bff", d6(172, cy + 36, 22, 3) + d6(194, cy + 42, 22, 4))
    i += pill(42, 362, 92, 22, "#c0267a", "REROLL  20", "#fff", 10) + pill(140, 362, 48, 22, "#7b4fd1", "AD ▶", "#fff", 9)
    i += txt(W / 2, 420, "Boons change how YOUR dice behave", 8, "#ffffffaa", 600)
    return phone(i, "#173548", DB2, "Boon pick: upgrades that bend the dice")


def tray(i_extra, dice, title, sub, bottom):
    i = topb() + txt(W / 2, 70, title, 18, DA, 900) + txt(W / 2, 88, sub, 10, "#fff", 700)
    i += box(16, 104, W - 32, 196, "#5a3a1e", 18, "#2b1a0b", 5) + box(28, 116, W - 56, 172, "#1f4a3a", 12, "#12301f", 3)
    for (x, y, f, held, rot, col) in dice:
        i += d6(x, y, 34, f, col, held, rot)
    return i + i_extra + bottom


def dd_roll():
    dice = [(62, 160, 4, True, -6, "#f6efe0"), (112, 150, 4, True, 8, "#f6efe0"), (165, 170, 4, False, -12, "#f6efe0"),
            (82, 240, 2, False, 14, "#f6efe0"), (148, 245, 6, False, -4, "#f6efe0")]
    extra = box(36, 310, 158, 32, "#00000099", 8, DA) + txt(W / 2, 324, "THREE OF A KIND", 10, "#fff", 900) + txt(W / 2, 337, "x4 · 120 → 480 coins", 9, "#ffe27a", 900)
    bottom = pill(16, 356, 96, 28, "#c0267a", "REROLL (1 left)", "#fff", 9, "#fff") + pill(118, 356, 96, 28, DA, "LOCK IN", "#2a1a05", 11, "#fff")
    bottom += txt(W / 2, 404, "Tap dice to HOLD, reroll the rest", 8.5, "#ffffffaa", 700)
    return phone(tray(extra, dice, "DIVE ROLL", "Boss chest: 120 coins → 5 dice", bottom), "#173548", DB2, "Dive Roll: hold, reroll, score the combo")


def dd_divedeeper():
    i = topb() + txt(W / 2, 72, "PUSH YOUR LUCK?", 16, DA, 900)
    i += box(20, 88, 190, 54, "#ffffff10", 12, "#ffffff33") + txt(W / 2, 108, "Banked so far: 480 coins (x4)", 9.5, "#fff", 800)
    i += txt(W / 2, 126, "Dive roll: 5 fresh dice", 8.5, "#ffffffaa", 700)
    i += box(14, 152, 98, 210, "#0e3a2a", 14, "#57e08a", 2) + txt(63, 176, "SURFACE", 12, "#57e08a", 900)
    i += d6(63, 222, 36, 6, "#bff4cf") + txt(63, 272, "Keep it all", 9, "#fff", 700) + txt(63, 290, "480", 14, "#ffd76a", 900)
    i += box(118, 152, 98, 210, "#3a1030", 14, "#ff6bd6", 2) + txt(167, 176, "DIVE DEEPER", 11, "#ff6bd6", 900)
    i += d6(152, 216, 26, 1, "#ffd0f0", rot=-10) + d6(182, 232, 26, 5, rot=12)
    i += txt(167, 272, "Add the next combo", 8, "#fff", 700) + txt(167, 290, "x4 + next combo", 10, "#ffd76a", 900)
    i += txt(167, 312, "2+ skulls = lose", 8, "#ff9b9b", 800) + txt(167, 324, "the dive bonus", 8, "#ff9b9b", 800) + txt(167, 344, "risk 19.6%", 9, "#ff9b9b", 900)
    i += txt(W / 2, 392, "Base reward is never lost: only the extra", 8, "#ffffffaa", 700)
    return phone(i, "#2a1438", DB2, "Dive Deeper: the push-your-luck beat")


def dd_class():
    i = topb() + txt(W / 2, 70, "PALADIN · LV 4", 15, "#fff", 900)
    i += chibi(W / 2, 116, "#c9c9e0", hat="helm", s=1.3)
    i += box(10, 160, W - 20, 120, "#00000077", 12)
    i += txt(22, 180, "ATTACK DIE", 9, DA, 900, "start") + d6(190, 178, 22, 6, DA) + txt(150, 183, "d8", 11, "#fff", 900)
    i += txt(22, 208, "SPECIAL · DIVINE SMITE", 9, DA, 900, "start") + txt(22, 222, "Roll d20: 15+ heals party, 20 = x3", 8, "#fff", 600, "start")
    i += txt(22, 246, "MANUAL BONUS", 9, DT, 900, "start") + txt(22, 260, "Tap at full charge: +1 to the roll", 8, "#fff", 600, "start")
    i += box(10, 290, W - 20, 90, "#00000077", 12) + txt(W / 2, 308, "DICE FORGE", 10, DA, 900)
    for k, (d, on) in enumerate([("d6", True), ("d8", True), ("d10", False), ("d12", False)]):
        x = 40 + k * 50
        i += f'<rect x="{x-17}" y="320" width="34" height="34" rx="8" fill="{DA if on else "#2a3a44"}" stroke="#fff" stroke-width="1.5"/>' + txt(x, 342, d, 10, "#2a1a05" if on else "#888", 900)
    i += txt(W / 2, 372, "Upgrade the die, not just the numbers", 8, "#ffffffbb", 700)
    i += nav(1)
    return phone(i, DB1, DB2, "Hero screen: attack die, special, forge")


def dd_shop():
    i = topb() + txt(W / 2, 66, "THE QUARTERMASTER", 14, DA, 900)
    i += box(12, 80, W - 24, 128, "#1f6a7a", 14, "#fff", 2)
    i += txt(24, 104, "DIVER'S", 14, "#fff", 900, "start") + txt(24, 120, "SUPPORT PACK", 14, "#ffe27a", 900, "start")
    for k, l in enumerate(["No forced ads", "Brass dice set", "+1 Dive Roll reroll"]):
        i += txt(24, 142 + k * 14, "• " + l, 9, "#fff", 600, "start")
    i += d6(180, 122, 34, 6, DA) + pill(130, 176, 80, 24, "#3ac46a", "$4.99", "#fff", 12, "#fff") + txt(30, 194, "ONE TIME", 8, "#ffffffaa", 700, "start")
    i += box(12, 218, 104, 120, "#5a1f6a", 12, "#fff", 2) + d6(48, 262, 28, 5, "#ff9ad6") + d6(82, 268, 28, 3, "#9af0ff")
    i += txt(64, 304, "DICE SKINS", 9, "#fff", 900) + pill(26, 312, 76, 18, "#3ac46a", "$0.99", "#fff", 10)
    i += box(124, 218, 94, 120, "#3a2a1a", 12, "#fff", 2) + chibi(171, 262, "#c9c9e0", hat="helm", s=0.9)
    i += txt(171, 304, "HERO OUTFIT", 9, "#fff", 900) + pill(134, 312, 74, 18, "#3ac46a", "$1.99", "#fff", 10)
    i += txt(W / 2, 362, "No gems · no packs · no stamina", 8.5, "#ffffffbb", 700)
    i += nav(0)
    return phone(i, DB1, DB2, "Shop: a support pack and cosmetics")


dd = []
q = mkpage(dd, "Dice &amp; Dive · concept brief", DA)
TGS = '<div class="tags" style="--k:#ffc94a"><span>DUNGEON DIVE</span><span>AUTO-BATTLE + MANUAL SPECIALS</span><span>DICE-ROLL REWARD GAME</span><span>PORTRAIT MOBILE · UNITY</span></div>'

dd.append(f"""<section class="page cover">
<div class="kicker" style="color:{DA}">GAME CONCEPT BRIEF · OCTOBER 2026</div>
<h1 class="big">DICE &amp; DIVE</h1>
<div class="sub">Dive a dungeon floor by floor with a party of heroes, then roll your loot as real dice for combos and multipliers</div>
{TGS}
<div class="covergrid">
 <div>
  {panel("Design goal", '<span class="goal">Cup Heroes\' loop, but every reward is a dice roll you control.</span><br>Auto-battle for players who want to relax, tap-to-roll specials for players who want to play.', DA)}
  {panel("Reading Key", "", YE,
         [tag("S") + " From a cited source (Sources page)",
          tag("P") + " Design proposal: ours to change",
          '<span class="tag i">TUNE</span> A starting number to tune in playtests',
          "Combo odds are computed exactly for 5 six-sided dice. All art is placeholder SVG"])}
 </div>
 <div class="coverart">{dd_hub()}{dd_roll()}</div>
</div>
<div class="strip">
 {panel("Not a copy", "What we keep and change from Cup Heroes (p.2)", RE)}
 {panel("The run", "Dive, fight, boons (p.3–5)", CY)}
 {panel("The Dive Roll", "The minigame, odds and tuning (p.6–7)", DA)}
 {panel("Meta &amp; build", "Heroes, store, Unity build order (p.8–10)", GR)}
</div>
<div class="foot"><i>Dice &amp; Dive · concept brief · builds on the Cup Heroes teardown and the Delve &amp; Dice, Last Lantern and Web of Dice briefs</i><span>01</span></div></section>""")

rows = [("Run shape", "Chapters of waves", "A <b>dive</b>: floors downward, bosses every 5, camps to surface from"),
        ("Fights", "Auto-battle", "Auto-battle + <b>x2 speed</b>, plus optional <b>tap-to-roll class specials</b>"),
        ("Upgrade picks", "3 cards: stat boosts", "3 cards that <b>change how dice behave</b> (exploding 6s, loaded die…)"),
        ("Reward minigame", "Balls through a pachinko board", "<b>Dive Roll</b>: roll 5 dice, hold, reroll, score combos"),
        ("Risk", "None in the minigame", "<b>Dive Deeper</b>: re-roll for more, but 2+ skulls costs the bonus"),
        ("Hero growth", "Levels, gear, pets, ascension", "Levels + a <b>Dice Forge</b> (d6 → d8 → d10 → d12 attack die)"),
        ("Currencies", "4+ (coins, gems, tokens, pass points)", "<b>2</b>: Coins and Forge Shards"),
        ("Store", "Gems, packs, timed bundles, pass", "<b>About 4 items</b>: support pack, cosmetics, optional ads")]
ct = "<table><tr><th></th><th>Cup Heroes (observed)</th><th>Dice &amp; Dive</th></tr>" + "".join(
    f"<tr><td style='color:#ffc84a;font-weight:700'>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows) + "</table>"
q("1. NOT A 1:1 COPY", "Same Rhythm, Different Game", ct + f"""
<div class="cols3" style="margin-top:12px">
{panel("Keep the rhythm", "Action → choice → reward → upgrade → return. Short fights on one readable screen. One big button per screen. This is genre structure, not Cup Heroes' property.", GR)}
{panel("Replace the signature", "Cup Heroes' identity is its cup-and-ball board. Ours is <b>dice you hold and reroll</b>: the player makes a decision instead of only watching physics.", DA)}
{panel("Add what they don't have", "A push-your-luck dive, class specials you can play by hand, and dice that grow with the hero. These are the three things a screenshot should show.", PU)}
</div>""", "Cup Heroes column from the supplied teardown (pages 2–8). Comparison rows are design proposals.")

q("2. THE DIVE", "Go Deeper. Know When to Surface.", loop([
    ("DIVE", "Start at floor 1"), ("FIGHT", "Auto waves"), ("BOON", "Pick 1 of 3"), ("BOSS", "Every 5 floors"),
    ("DIVE ROLL", "Roll the chest"), ("CAMP", "Surface or go on"), ("FORGE", "Spend at the top")], [DA, RE, PU, CY]) + f"""
<div class="hero">
 <div class="herotext">
  {panel(tag("P") + " Structure", "Each floor is 3–5 short waves. A boss every 5th floor opens a chest that you resolve with the <b>Dive Roll</b>. Camps on floors 3, 6, 9… let you <b>surface</b> and bank everything.", DA)}
  {panel(tag("P") + " The tension", "Coins you carry are at risk: wiping out keeps <b>50%</b> <span class='tag i'>TUNE</span>. Banked coins are safe. So every camp asks: surface now, or push for the next boss chest?", RE)}
  {panel(tag("P") + " Depth record", "Your deepest floor is the headline number on the home screen and in the daily leaderboard. It's the 'one more run' hook.", GR)}
  <div class="note">This is the extract-or-push idea from The Last Lantern, and what Web of Dice already does with the Guild walk-back, here as the main structure.</div>
 </div>
 <div class="shots2">{dd_depth()}{dd_divedeeper()}</div>
</div>""", "Floor counts, camp spacing and the 50% keep rate are starting values.")

q("3. COMBAT", "Auto for Some, Hands-On for Others", f"""
<div class="hero rev">
 <div class="shots2">{dd_battle()}{dd_class()}</div>
 <div class="herotext">
  {panel(tag("P") + " Auto mode (default)", "Heroes fight on their own. <b>x1 / x2 speed</b> toggle (x3 as a later unlock). Specials fire automatically when charged. Fully playable one-handed or while half-watching.", CY)}
  {panel(tag("P") + " Manual specials", "Each class has one special with its own dice (Paladin: Smite d20, Ranger: Volley 3d6, Wizard: Nova 2d8). In manual mode <b>you tap it</b> at full charge, choose the moment, and the roll gets <b>+1</b> <span class='tag i'>TUNE</span>. Auto players lose a little; nobody is forced to tap.", DA)}
  {panel(tag("P") + " Dice on screen", "Every hit shows its die result. A natural 20 or max roll gets a gold flash, big number and screen shake. Damage numbers read as dice, not just stats.", PU)}
  {panel(tag("P") + " Party", "3 heroes, 4 classes at launch: <b>Fighter, Rogue, Cleric, Wizard</b> (GPT's scope cut: four good classes beat eight shallow ones).", GR)}
 </div>
</div>""", "Speed toggle and auto-battle observed in the Cup Heroes teardown (page 5 shows a speed control).")

q("4. DICE BOONS", "Upgrades That Bend the Dice", f"""
<div class="hero">
 <div class="herotext">
  <p class="pitch">Cup Heroes' cards add numbers. Ours change the <i>rules of the dice</i>, so builds feel different, not just bigger.</p>
  {panel(tag("P") + " Example boons", "", DA, [
      "<b>Exploding Sixes</b>: a 6 rolls again and adds",
      "<b>Loaded Die</b>: your lowest die each roll gets +1",
      "<b>Lucky Sevens</b>: any two dice summing to 7 heal the party",
      "<b>Snake Eyes</b>: skulls (1s) deal damage instead of missing",
      "<b>High Roller</b>: +50% damage on max rolls, −1 to all others",
      "<b>Steady Hand</b>: one extra Hold-and-reroll in the Dive Roll"])}
  {panel(tag("P") + " Run economy", "Coins earned in fights buy boons (prices on the cards, one free pick). Reroll the offer for 20 coins or one optional ad, as in Cup Heroes.", CY)}
  <div class="note">Boons should also touch the <b>Dive Roll</b> (Steady Hand, Exploding Sixes), so the build you made in combat changes the minigame. That's how the two halves of the game feed each other.</div>
 </div>
 <div class="shots2">{dd_boon()}{dd_battle()}</div>
</div>""", "Three-card pick with paid reroll observed in the Cup Heroes teardown (page 5).")

odds = [("Nothing", "6.2%", "x1"), ("Pair", "46.3%", "x2"), ("Two pair", "23.1%", "x3"), ("Three of a kind", "15.4%", "x4"),
        ("Straight (1–5 or 2–6)", "3.1%", "x6"), ("Full house", "3.9%", "x6"), ("Four of a kind", "1.9%", "x10"), ("Five of a kind: JACKPOT", "0.08%", "x25")]
ot = "<table style='font-size:11px'><tr><th>Combo (5 dice, one roll)</th><th>Chance</th><th>Multiplier</th></tr>" + "".join(
    f"<tr><td><b>{a}</b></td><td>{b}</td><td style='color:#ffc94a;font-weight:800'>{c}</td></tr>" for a, b, c in odds) + "</table>"
q("5. THE DIVE ROLL", "The Minigame: Roll Your Loot", f"""
<div class="hero">
 <div class="herotext">
  {panel(tag("P") + " How it works", "", DA, [
      "A boss chest becomes <b>5 dice</b> (more with boons)",
      "<b>Throw</b>: swipe up to toss them into the tray",
      "<b>Hold</b> any dice by tapping, then <b>reroll</b> the rest once",
      "<b>Lock in</b>: the best combo multiplies the chest",
      "Optional: <b>Dive Deeper</b> for more (next page)"])}
  {ot}
  <div class="note" style="font-size:11px">Odds are exact for one throw of 5d6 (all 7,776 outcomes counted). The average multiplier on one throw is about <b>x2.9</b>, before holding and rerolling, which raises it. <span class="tag i">TUNE</span> multipliers in playtests.</div>
 </div>
 <div class="shots2">{dd_roll()}{dd_divedeeper()}</div>
</div>""", "Combo odds computed for this brief; multipliers are proposals. Combo names are generic dice-game terms (avoid trademarked game names).")

q("6. DIALING IN THE MINIGAME", "Where the Feel Comes From", f"""
<div class="cols3">
{panel(tag("P") + " Dive Deeper (push your luck)", "", RE, [
    "After locking in, choose <b>Surface</b> (keep it) or <b>Dive Deeper</b>",
    "Dive: roll 5 fresh dice; their combo multiplier is <b>added</b> on top",
    "<b>2 or more skulls (1s)</b> = bust: lose the dive bonus, keep the base",
    "Bust chance per dive: <b>19.6%</b> (exact, 5d6)",
    "Cap at 3 dives <span class='tag i'>TUNE</span>"])}
{panel(tag("P") + " Juice checklist", "", DA, [
    "Real tumbling dice: 3D dice in a 2D scene, or physics on 2D sprites",
    "Slow-motion on the last die to settle",
    "Held dice lift and glow gold",
    "Combo name stamps on screen; multiplier counts up",
    "Distinct sound per combo tier; JACKPOT gets the big one",
    "Haptic tick on each die landing"])}
{panel(tag("P") + " Prototype tests", "", GR, [
    "Does holding feel like a real choice? Watch whether testers hesitate",
    "Is a pair (46%) still exciting? If not, make pairs x1.5 and spread the rewards upward",
    "Does Dive Deeper get chosen about half the time? If almost always or never, retune the bust rule",
    "Time per Dive Roll: target 8–12 seconds"])}
</div>
<div class="note">{tag("S")} <b>Why this can work:</b> Balatro, a roguelike built on scoring poker hands, made about $4.4M on mobile in its first two months as a $9.99 premium game (AppMagic via PocketGamer.biz). Players clearly enjoy building and scoring combos. {tag("S")} Space Rock Breaker shows a small game built around a Plinko-style reward board can find an audience; our version swaps the board for dice.</div>
""", "Bust rate computed exactly (5d6, 2+ ones). Everything else on this page is to tune in a prototype.")

q("7. META &amp; ECONOMY", "Two Currencies. Dice That Grow.", f"""
<div class="hero">
 <div class="herotext">
  <div class="cols2 tight">
  {panel(tag("P") + " Coins", "Earned in fights and the Dive Roll. Banked when you surface. Spent on hero levels and boons.", DA)}
  {panel(tag("P") + " Forge Shards", "From bosses and five-of-a-kind jackpots. Spent in the Dice Forge.", PU)}
  {panel(tag("P") + " Dice Forge", "Upgrade each hero's attack die: <b>d6 → d8 → d10 → d12</b>. Bigger dice mean bigger rolls, and the upgrade is visible on every hit.", CY)}
  {panel(tag("P") + " Retention", "Daily Dive (seeded floor set + leaderboard), a 7-day calendar, depth-record milestones that unlock heroes.", GR)}
  </div>
  {panel("Kept out on purpose", "", RE, ["Premium gems", "Random paid packs or shards", "Stamina or energy", "Countdown bundles", "Forced interstitial ads"])}
 </div>
 <div class="shots2">{dd_class()}{dd_hub()}</div>
</div>""", "Same system filter as the Two Small Roguelites brief (page 4).")

q("8. MONETIZATION", "Small, Fair, Optional", f"""
<div class="hero">
 <div class="herotext tiers">
  {panel("1 · Rewarded ads <small>optional</small>", "One extra Dive Roll reroll, one revive per dive, or a boon-offer refresh. Capped per day.", CY)}
  {panel("2 · Diver's Support Pack <small>$4.99 one-time</small>", "No forced ads, a brass dice set, +1 permanent Dive Roll reroll.", GR)}
  {panel("3 · Cosmetics <small>$0.99–$1.99</small>", "Dice skins (the most visible item in the game) and hero outfits.", PU)}
  {panel("4 · Later: Dive Pass <small>$3.99 / season</small>", "Only after retention is proven; premium track cosmetic only.", YE)}
  <span class="rule" style="background:{DA}">RULE: NO PAYWALL ON CORE POWER</span>
  <div class="note">{tag("S")} Comparable light model: Soul Knight sells $0.99–$3.99 unlocks (Adapty estimate, ~$400K/month). {tag("I")} Dice skins suit this game unusually well, because the dice are on screen in every fight and every reward.</div>
 </div>
 <div class="shots2">{dd_shop()}{dd_roll()}</div>
</div>""", "Store items are proposals; benchmarks from the Two Small Roguelites brief sources.")

q("9. BUILD ORDER IN UNITY", "Minigame First, Everything Else After", f"""
<div class="mvp">
{panel("Step 1 · The Dive Roll scene", "", DA, [
    "Standalone scene: 5 dice, throw, hold, reroll, lock in",
    "Combo detection + multiplier count-up",
    "Dive Deeper with the skull bust rule",
    "Debug panel: dice count, multipliers, bust rule live-editable",
    "<b>Pass:</b> testers play it 10 times in a row without being asked"])}
{panel("Step 2 · One floor of combat", "", CY, [
    "3 heroes vs waves, auto-battle, x2 speed",
    "One manual special (Paladin Smite) to test tap-to-roll",
    "3-card boon pick with 6 boons",
    "One boss → opens the Dive Roll",
    "<b>Pass:</b> a full floor-to-chest loop in under 4 minutes"])}
{panel("Step 3 · Only then", "", GR, [
    "The dive structure (camps, surfacing, depth record)",
    "Dice Forge and hero levels",
    "4 classes",
    "Daily Dive",
    "Store and ads last"])}
</div>
<div class="note"><b>Message to start the new chat with:</b> "We're building Dice &amp; Dive in Unity (2D, portrait). Read the attached brief. Start with Step 1 only: a standalone Dive Roll scene with 5 dice, hold and reroll, combo detection, multipliers from the odds table, and a Dive Deeper button with the 2+ skulls bust rule. Put every number in one ScriptableObject so we can tune it live."</div>
""", "Scope follows the agreed rule: prototype the core pleasure before any meta or store.")

srcs = [("Cup Heroes Game Design Inspiration Brief (user-supplied teardown)", ""),
        ("PocketGamer.biz: Balatro nears $4.4M on mobile", "https://www.pocketgamer.biz/balatro-nears-44m-on-mobile-amid-a-sudden-spending-surge/"),
        ("Automaton: Space Rock Breaker (Plinko-based ore processing)", "https://automaton-media.com/articles/newsjp/space-rock-breaker-20251224-388202/"),
        ("Adapty: Soul Knight IAP pricing and revenue estimate", "https://adapty.io/paywall-library/soul-knight/"),
        ("PocketGamer.biz: Archero 2 makes $32.8M in its first 30 days", "https://www.pocketgamer.biz/archero-2-makes-328m-in-first-30-days-from-player-spending"),
        ("AppMagic 2025 monetization report (summary): roguelikes +26.2% YoY", "https://gamedevreports.substack.com/p/appmagic-mobile-games-monetization")]
sl = "<ol class='srcs' style='columns:1'>" + "".join(f"<li>{t}" + (f"<br><a href='{u}'>{u}</a>" if u else "") + "</li>" for t, u in srcs) + "</ol>"
q("10. SOURCES &amp; RISKS", "What's Proven, What's a Bet", f"""
<div class="cols2">
 <div>{sl}
  <div class="note small">Combo odds and the bust rate were computed for this brief by counting all 7,776 outcomes of 5 six-sided dice. Market figures are third-party estimates, not developer disclosures.</div>
 </div>
 <div class="herotext">
  {panel("Risks", "", RE, [
      "<b>Combo scoring may feel too familiar</b> (any dice-poker game). Mitigation: the boons that bend dice and the Dive Deeper risk are ours",
      "<b>Real dice physics on mobile</b> is fiddly: dice can stack, clip or take too long to settle. Prototype it first",
      "<b>Manual specials could make auto feel bad.</b> Keep the manual bonus small (+1)",
      "<b>The name</b>: check 'Dice &amp; Dive' in the app stores before investing in art"])}
  {panel("Not proven yet", "", YE, ["That auto-battle players want a hold/reroll decision at all", "That 19.6% bust is the right amount of fear", "The x2–x25 multiplier curve"])}
 </div>
</div>""", "Every number marked TUNE is a starting point for playtests, not a final value.")

render(dd, "Dice & Dive Brief", os.path.join(HERE, "dice_and_dive.html"))
print("dice&dive pages", len(dd))
