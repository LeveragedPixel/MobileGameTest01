"""Redesign of the two GPT prototype briefs (Salvage Run, The Last Lantern) in the
house style from build.py. Reuses build.py's SVG helpers + CSS."""
import math, random, os

HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "build_brief.py")).read())  # helpers, CSS, colors

CSS2 = CSS + """
.tags { display:flex; gap:8px; margin:-14px 0 18px; }
.tags span { background:#162133; border:1px solid #2a3a55; color:var(--k); font-size:10.5px; font-weight:800; padding:5px 11px; border-radius:20px; letter-spacing:.04em; }
.goal { font-size:22px; font-weight:800; color:#fff; line-height:1.25; margin:4px 0 6px; }
.tag.g { background:#1d3f5c; color:#9fd8ff; }
.rule { display:inline-block; margin-top:12px; padding:8px 16px; border-radius:20px; font-weight:900; font-size:11.5px; letter-spacing:.05em; color:#0b0f17; }
.tiers .panel h3 small { color:var(--c); font-size:12px; margin-left:6px; }
.mvp { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
.mvp .panel li { margin-bottom:7px; }
"""


def sug():
    return '<span class="tag g">SUGGESTED</span>'


def render(doc_pages, title, path):
    with open(path, "w") as f:
        f.write(f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS2}</style></head><body>{''.join(doc_pages)}</body></html>")


def mkpage(store, brand, color):
    def p(kicker, title, body, foot):
        n = len(store) + 1
        store.append(f"""<section class="page"><div class="kicker" style="color:{color}">{kicker}</div>
<h1>{title}</h1>{body}<div class="foot"><i>{brand} · {foot}</i><span>{n:02d}</span></div></section>""")
    return p


# =====================================================================
# SALVAGE RUN — space
# =====================================================================
SC = "#3fd6ff"   # accent
SB1, SB2 = "#0d1a33", "#03060f"


def stars(seed=1, n=40, h=H):
    random.seed(seed)
    return "".join(f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,h)}" r="{random.choice([0.6,0.9,1.3])}" fill="#fff" opacity="{random.choice([.4,.7,1])}"/>' for _ in range(n))


def ship(cx, cy, s=1.0, col="#3fd6ff", drones=False):
    g = f'<g transform="translate({cx},{cy}) scale({s})">'
    g += '<ellipse cx="0" cy="26" rx="7" ry="12" fill="#ff9a3c" opacity=".85"/><ellipse cx="0" cy="24" rx="3" ry="7" fill="#fff3c4"/>'
    g += f'<polygon points="0,-26 14,14 0,8 -14,14" fill="{col}" stroke="#e8fbff" stroke-width="2"/>'
    g += '<polygon points="-14,14 -24,20 -10,2" fill="#2a7fb0" stroke="#e8fbff" stroke-width="1.5"/><polygon points="14,14 24,20 10,2" fill="#2a7fb0" stroke="#e8fbff" stroke-width="1.5"/>'
    g += '<ellipse cx="0" cy="-6" rx="4" ry="7" fill="#0b2340" stroke="#e8fbff" stroke-width="1.2"/>'
    if drones:
        for dx in (-30, 30):
            g += f'<circle cx="{dx}" cy="0" r="6" fill="#b06bff" stroke="#fff" stroke-width="1.5"/><line x1="{dx}" y1="-6" x2="{dx}" y2="-60" stroke="#d2b6ff" stroke-width="2" stroke-dasharray="4 4"/>'
    return g + "</g>"


def alien(cx, cy, s=1.0, col="#ff4f6b"):
    g = f'<g transform="translate({cx},{cy}) scale({s})">'
    g += f'<path d="M-14,0 Q0,-18 14,0 L10,10 L4,4 L0,12 L-4,4 L-10,10 Z" fill="{col}" stroke="#2a0010" stroke-width="2"/>'
    g += '<circle cx="-5" cy="-3" r="2.5" fill="#fff"/><circle cx="5" cy="-3" r="2.5" fill="#fff"/>'
    return g + "</g>"


def planet(cx, cy, r, c1, c2):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c1}"/>'
            f'<path d="M{cx-r},{cy} A{r},{r} 0 0 0 {cx+r},{cy} A{r},{r*0.55} 0 0 1 {cx-r},{cy}" fill="{c2}" opacity=".6"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r*1.5}" ry="{r*0.28}" fill="none" stroke="#9fd8ff" stroke-width="2" opacity=".6"/>')


def s_hub():
    i = stars(3) + topbar(3, "860", "4", "#1f6fd1")
    i += pill(14, 52, 92, 22, "#ffffff14", "Station", "#fff", 10, "#ffffff44")
    i += pill(112, 52, 104, 22, SC, "Daily Sector", "#04202c", 9, "#fff")
    i += txt(W / 2, 100, "SECTOR 4", 22, "#fff", 900) + txt(W / 2, 118, "THE RUST BELT", 13, SC, 900)
    i += planet(150, 220, 46, "#2a5c9a", "#123058")
    # station ring
    i += '<circle cx="80" cy="190" r="28" fill="none" stroke="#9fb4d0" stroke-width="6"/><circle cx="80" cy="190" r="9" fill="#9fb4d0"/><line x1="52" y1="190" x2="108" y2="190" stroke="#9fb4d0" stroke-width="3"/>'
    i += ship(115, 300, 1.25)
    for k, x in enumerate((60, 100, 140, 180)):
        i += f'<rect x="{x-11}" y="{336-9}" width="22" height="18" rx="4" fill="{["#b06bff", SC, SC, SC][k]}" stroke="#fff" stroke-width="1.5"/>'
    i += pill(52, 360, 126, 32, SC, "LAUNCH", "#04202c", 16, "#fff", 900)
    i += bottomnav(["Shop", "Hangar", "Launch", "Research", "Nav"], 2, "#0a1324", SC)
    return phone(i, SB1, SB2, "Station hub: one big LAUNCH button")


def s_run():
    i = stars(5, 60)
    i += pill(10, 12, 64, 20, "#1f6fd1", "SHIELD 64", "#fff", 9) + pill(80, 12, 70, 20, "#ffffff22", "SECTOR 4", "#fff", 9) + pill(156, 12, 64, 20, "#ffffff22", "SCRAP 28", "#ffd76a", 9)
    i += box(10, 40, 210, 6, "#ffffff22", 3) + box(10, 40, 120, 6, "#ff4f6b", 3) + txt(W / 2, 60, "WAVE 3/6", 9, "#ffffffaa", 800)
    for x, y in [(50, 100), (110, 85), (170, 110), (80, 150), (150, 160), (190, 70), (35, 190)]:
        i += alien(x, y, 0.9)
    i += alien(115, 125, 1.5, "#ff9a3c")
    for k in range(6):
        i += f'<rect x="{113}" y="{330 - k*30}" width="4" height="14" rx="2" fill="{SC}"/>'
    i += '<path d="M90,320 Q60,240 80,170" fill="none" stroke="#ffd76a" stroke-width="2" stroke-dasharray="3 4"/><path d="M140,320 Q170,240 150,170" fill="none" stroke="#ffd76a" stroke-width="2" stroke-dasharray="3 4"/>'
    i += ship(115, 350, 1.0, drones=True)
    i += '<circle cx="190" cy="415" r="22" fill="#b06bff" stroke="#fff" stroke-width="2"/>' + txt(190, 419, "EMP", 10, "#fff", 900)
    i += '<circle cx="115" cy="425" r="26" fill="none" stroke="#ffffff55" stroke-width="2" stroke-dasharray="4 4"/>' + txt(115, 462, "DRAG TO MOVE · AUTO-FIRE", 8, "#ffffffaa", 800)
    return phone(i, "#0a1430", "#02040a", "Run screen: drag to evade, weapons auto-fire")


def s_pick():
    i = stars(7, 30) + topbar(3, "860", "4", "#1f6fd1")
    i += txt(W / 2, 70, "WAVE CLEARED", 15, "#ffe27a", 900) + txt(W / 2, 88, "Install a Module", 11, "#fff", 700)
    i += ship(115, 140, 1.1)
    i += box(8, 182, W - 16, 210, "#00000088", 12)
    cy = 200
    i += card(14, cy, 66, 130, "#2a1a55", "DRONE|BAY", "FREE", "#b06bff",
              '<circle cx="35" cy="236" r="9" fill="#b06bff" stroke="#fff" stroke-width="2"/><circle cx="60" cy="236" r="9" fill="#b06bff" stroke="#fff" stroke-width="2"/>')
    i += card(82, cy, 66, 130, "#0b3550", "RAIL|GUN", "120", "#3fd6ff",
              '<rect x="111" y="210" width="8" height="54" fill="#e8fbff"/><rect x="106" y="252" width="18" height="10" fill="#3fd6ff"/>')
    i += card(150, cy, 66, 130, "#55200b", "MISSILE|SWARM", "150", "#ff9a3c",
              ''.join(f'<polygon points="{170+k*12},{250} {175+k*12},{220} {180+k*12},{250}" fill="#ffd76a" stroke="#1a1020" stroke-width="1.5"/>' for k in range(3)))
    i += pill(42, 362, 92, 22, "#c0267a", "REROLL  20", "#fff", 10) + pill(140, 362, 48, 22, "#7b4fd1", "AD ▶", "#fff", 9)
    i += txt(W / 2, 420, "Synergy: Drones + Missiles = Seeker Drones", 8, SC, 700)
    return phone(i, "#0d1a33", "#03060f", "Module pick: 1 of 3, shows synergies")


def s_jump():
    i = stars(9, 50) + topbar(3, "860", "4", "#1f6fd1")
    i += txt(W / 2, 74, "SECTOR CLEARED", 16, "#ffe27a", 900)
    i += box(20, 90, 190, 64, "#ffffff10", 12, "#ffffff33")
    i += txt(W / 2, 114, "Cargo hold: 340 Scrap · 1 Data Core", 9.5, "#fff", 700)
    i += box(32, 126, 166, 10, "#ffffff22", 5) + box(32, 126, 120, 10, "#ffd76a", 5) + txt(W / 2, 148, "Hull 58%", 8.5, "#ffffffaa", 700)
    # two choices
    i += box(14, 170, 98, 190, "#0e3a2a", 14, "#57e08a", 2) + txt(63, 196, "RETURN", 13, "#57e08a", 900)
    i += '<circle cx="63" cy="250" r="26" fill="none" stroke="#9fb4d0" stroke-width="5"/><circle cx="63" cy="250" r="8" fill="#9fb4d0"/>'
    i += txt(63, 300, "Bank everything", 8.5, "#fff", 700) + txt(63, 314, "340 Scrap", 10, "#ffd76a", 900)
    i += box(118, 170, 98, 190, "#3a1030", 14, "#ff6bd6", 2) + txt(167, 196, "JUMP", 13, "#ff6bd6", 900)
    i += '<circle cx="167" cy="250" r="26" fill="#2a0a3a" stroke="#ff6bd6" stroke-width="3"/><circle cx="167" cy="250" r="14" fill="#ff6bd6" opacity=".5"/><circle cx="167" cy="250" r="5" fill="#fff"/>'
    i += txt(167, 300, "Sector 5 · harder", 8.5, "#fff", 700) + txt(167, 314, "x1.5 cargo", 10, "#ffd76a", 900)
    i += txt(167, 334, "die = lose 50%", 8, "#ff9b9b", 700)
    i += txt(W / 2, 392, "Risk / return lives in one clear screen", 8, "#ffffffaa", 600)
    return phone(i, "#140a2a", "#03060f", "Jump or Return: the risk/return beat")


def s_station():
    i = stars(11, 30) + topbar(3, "860", "4", "#1f6fd1")
    i += txt(W / 2, 70, "STATION OUTPOST-9", 15, "#fff", 900)
    mods = [(24, 92, "HANGAR", "Ships", "#1f6fd1", "Lv 2"), (124, 92, "ENGINEERING", "Modules", "#b06bff", "Lv 3"),
            (24, 196, "RESEARCH", "Alien tech", "#2a9a8a", "Lv 1"), (124, 196, "NAVIGATION", "Sectors", "#d98c2a", "Lv 1")]
    for x, y, n, d, c, l in mods:
        i += box(x, y, 82, 92, c, 12, "#fff", 2)
        i += f'<circle cx="{x+41}" cy="{y+36}" r="18" fill="#00000044" stroke="#ffffff88" stroke-width="2"/><circle cx="{x+41}" cy="{y+36}" r="6" fill="#fff"/>'
        i += txt(x + 41, y + 72, n, 8.5, "#fff", 900) + txt(x + 41, y + 84, d, 7.5, "#ffffffbb", 600)
        i += pill(x + 50, y + 4, 30, 14, "#000000aa", l, "#fff", 7)
    i += box(14, 300, W - 28, 60, "#ffffff10", 10, "#ffffff33")
    i += txt(W / 2, 320, "NEXT UNLOCK", 9, SC, 900) + txt(W / 2, 338, "Research Lv 2: Gravity Well module", 9, "#fff", 700)
    i += pill(52, 370, 126, 24, "#ffd76a", "UPGRADE · 400 SCRAP", "#2a1a05", 9)
    i += bottomnav(["Shop", "Hangar", "Launch", "Research", "Nav"], 3, "#0a1324", SC)
    return phone(i, SB1, SB2, "Station: 4 modules unlock build options")


def s_hangar():
    i = stars(13, 30) + topbar(3, "860", "4", "#1f6fd1")
    i += txt(W / 2, 70, "HANGAR", 15, "#fff", 900)
    ships = [("INTERCEPTOR", "Fast · crit", "#3fd6ff", True), ("CARRIER", "Drones", "#b06bff", True),
             ("LANCER", "Piercing", "#ff9a3c", False), ("BASTION", "Shield retaliate", "#57e08a", False)]
    for k, (n, d, c, on) in enumerate(ships):
        x, y = 14 + (k % 2) * 104, 86 + (k // 2) * 150
        i += box(x, y, 98, 140, "#ffffff12" if on else "#ffffff08", 12, c if on else "#444", 2)
        i += ship(x + 49, y + 52, 0.9, c if on else "#555")
        i += txt(x + 49, y + 106, n, 9, "#fff" if on else "#777", 900) + txt(x + 49, y + 120, d, 7.5, "#ffffffaa", 600)
        if not on:
            i += pill(x + 24, y + 126, 50, 12, "#000", "2 DATA CORES", "#ffd76a", 6)
    i += txt(W / 2, 402, "4 archetypes max at launch", 8.5, SC, 700)
    i += bottomnav(["Shop", "Hangar", "Launch", "Research", "Nav"], 1, "#0a1324", SC)
    return phone(i, SB1, SB2, "Hangar: 4 ship archetypes, earned in play")


def s_tractor():
    i = stars(15, 40) + topbar(3, "860", "4", "#1f6fd1")
    i += txt(W / 2, 70, "TRACTOR SORT", 19, SC, 900) + txt(W / 2, 88, "Cargo: 340 Scrap", 10, "#fff", 700)
    i += box(10, 100, W - 20, 300, "#06102a", 10, "#1f3a66", 2)
    random.seed(2)
    for row, y in enumerate(range(130, 300, 34)):
        for k in range(6 if row % 2 else 5):
            x = 30 + k * 36 + (0 if row % 2 else 18)
            i += f'<circle cx="{x}" cy="{y}" r="4" fill="#9fb4d0"/>'
    for k in range(24):
        x, y = random.randint(26, 204), random.randint(110, 330)
        i += f'<polygon points="{x},{y-4} {x+5},{y} {x},{y+4} {x-5},{y}" fill="{random.choice(["#ffd76a","#9fb4d0","#b06bff"])}"/>'
    labels = [("x2", "#d9a03a"), ("x5", "#b03a8a"), ("x3", "#3ac46a"), ("x1", "#555"), ("x3", "#3ac46a"), ("x2", "#d9a03a")]
    for k, (l, c) in enumerate(labels):
        x = 14 + k * 34
        i += box(x, 340, 32, 50, c, 6, "#fff", 1.5) + txt(x + 16, 370, l, 11, "#fff", 900)
    i += '<path d="M95,96 L135,96 L125,112 L105,112 Z" fill="#3fd6ff" opacity=".8"/>'
    i += box(60, 404, 110, 28, "#00000099", 8, SC) + txt(W / 2, 423, "340 → 1,180", 13, "#ffe27a", 900)
    return phone(i, "#0d1a33", "#03060f", "Tractor Sort: a Plinko board for cargo")


def s_shop():
    i = stars(17, 30) + topbar(3, "860", "4", "#1f6fd1")
    i += txt(W / 2, 66, "SUPPLY DEPOT", 15, SC, 900)
    i += box(12, 80, W - 24, 128, "#1f4fa0", 14, "#fff", 2)
    i += txt(24, 104, "PILOT'S", 14, "#fff", 900, "start") + txt(24, 120, "SUPPORT PACK", 14, "#ffe27a", 900, "start")
    for k, l in enumerate(["No forced ads", "Gold-trim ship skin", "1,000 Scrap head start"]):
        i += txt(24, 142 + k * 14, "• " + l, 9, "#fff", 600, "start")
    i += ship(182, 128, 0.8, "#ffd76a")
    i += pill(130, 176, 80, 24, "#3ac46a", "$4.99", "#fff", 12, "#fff")
    i += txt(30, 194, "ONE TIME", 8, "#ffffffaa", 700, "start")
    i += box(12, 218, 104, 120, "#5a1f6a", 12, "#fff", 2) + ship(64, 262, 0.75, "#ff6bd6")
    i += txt(64, 304, "NEBULA SKIN", 9, "#fff", 900) + pill(26, 312, 76, 18, "#3ac46a", "$1.99", "#fff", 10)
    i += box(124, 218, 94, 120, "#0b3550", 12, "#fff", 2)
    i += ''.join(f'<rect x="{150+k*14}" y="{240}" width="6" height="40" rx="3" fill="{c}"/>' for k, c in enumerate(["#3fd6ff", "#ff6bd6", "#57e08a"]))
    i += txt(171, 304, "TRAIL FX", 9, "#fff", 900) + pill(134, 312, 74, 18, "#3ac46a", "$2.99", "#fff", 10)
    i += txt(W / 2, 362, "No paywall on core power", 8.5, "#ffffffbb", 700)
    i += bottomnav(["Shop", "Hangar", "Launch", "Research", "Nav"], 0, "#0a1324", SC)
    return phone(i, SB1, SB2, "Shop: support pack + cosmetics only")


def s_map():
    i = stars(19, 50) + topbar(3, "860", "4", "#1f6fd1")
    i += txt(W / 2, 70, "NAVIGATION", 15, "#fff", 900)
    pts = [(60, 400, "1", True), (150, 340, "2", True), (80, 270, "3", True), (160, 200, "4", True), (90, 130, "5", False)]
    for a in range(len(pts) - 1):
        i += f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[a+1][0]}" y2="{pts[a+1][1]}" stroke="#3fd6ff66" stroke-width="3" stroke-dasharray="6 5"/>'
    names = ["Dock Ring", "Ice Field", "Wreck Yard", "Rust Belt", "The Maw"]
    for k, (x, y, n, on) in enumerate(pts):
        i += planet(x, y, 18, ["#3a8a6a", "#6ab0d8", "#8a6a4a", "#b0542a", "#5a1f6a"][k], "#000")
        i += txt(x, y + 34, names[k], 8.5, "#fff" if on else "#888", 800)
        if k == 3:
            i += f'<circle cx="{x}" cy="{y}" r="26" fill="none" stroke="#ffe27a" stroke-width="3"/>'
    i += pill(130, 120, 80, 18, "#000000aa", "BOSS · 2 CORES", "#ff9b9b", 7)
    return phone(i, "#0a1430", "#02040a", "Sectors are chapter nodes, not a star map")


sr = []
p = mkpage(sr, "Salvage Run · prototype concept", SC)
SR_TAGS = '<div class="tags" style="--k:#3fd6ff"><span>10–12 MINUTE RUNS</span><span>AUTO-FIRE</span><span>RISK / RETURN</span><span>PORTRAIT</span></div>'

sr.append(f"""<section class="page cover">
<div class="kicker" style="color:{SC}">PROTOTYPE BRIEF · REDESIGNED EDITION</div>
<h1 class="big">SALVAGE RUN</h1>
<div class="sub">A portrait space roguelite: launch, blast through a sector, grab salvage, and decide whether to jump deeper or go home</div>
{SR_TAGS}
<div class="covergrid">
 <div>
  {panel("Design goal", '<span class="goal">Build ridiculous ship synergies with minimal controls.</span><br>Get the feel of exploring space without building a giant space game.', SC)}
  {panel("Reading Key", "This edition keeps the original brief's ideas and adds detail:", YE,
         ["Untagged: from the original brief",
          sug() + " My addition or fix, for you to accept or reject",
          tag("S") + " Checked against a cited source (page 8)",
          "All art is placeholder SVG drawn for this brief"])}
 </div>
 <div class="coverart">{s_hub()}{s_run()}</div>
</div>
<div class="strip">
 {panel("Loop", "Launch · Engage · Upgrade · Salvage · Return (p.2–3)", SC)}
 {panel("Meta", "The station and its 4 modules (p.4)", PU)}
 {panel("Economy &amp; store", "Three resources, light monetization (p.5–6)", YE)}
 {panel("MVP &amp; research", "What to build first, and why (p.7–8)", GR)}
</div>
<div class="foot"><i>Salvage Run · prototype concept · redesigned from the original GPT brief</i><span>01</span></div></section>""")

p("1. CORE LOOP", "Launch. Fight. Salvage. Decide.", loop([
    ("LAUNCH", "Pick ship"), ("ENGAGE", "Short battle"), ("UPGRADE", "1 of 3 modules"),
    ("SALVAGE", "Collect scrap"), ("DECIDE", "Jump or return"), ("RETURN", "Bank rewards")], [SC, PU, YE, GR]) + f"""
<div class="hero">
 <div class="herotext">
  <p class="pitch">A small game that feels like part of a much bigger universe.</p>
  {panel("Why it works", "", SC, ["Ship builds are easy to read at a glance", "The space theme naturally supports modular upgrades", "Risk/return gives each run tension"])}
  {panel("Prototype rule", "No open-world exploration. \"Space\" is a sequence of compact encounters: each sector is 6 waves, a boss, then a decision.", RE)}
  {panel(sug() + " Make risk/return a real screen", "The original lists 'risk/return' as a pillar but never shows where it happens. Proposal: after each sector boss, <b>Jump</b> (next sector harder, cargo x1.5, die and lose 50%) or <b>Return</b> (bank everything). One screen, one decision.", YE)}
 </div>
 <div class="shots2">{s_map()}{s_jump()}</div>
</div>""", "Inspired by Cup Heroes' action → choice → reward → upgrade loop.")

p("2. RUN SCREEN", "Minimal Control. Maximum Build Expression.", f"""
<div class="hero rev">
 <div class="shots2">{s_run()}{s_pick()}</div>
 <div class="herotext">
  <p class="pitch">Moving the ship matters, but the spectacle comes from upgrade combinations.</p>
  {panel("Moment-to-moment", "", SC, ["Drag the ship to evade; it never needs a fire button", "Weapons auto-fire", "One active ability on a cooldown (e.g. EMP)", "Short enemy waves of about 40–60 seconds"])}
  {panel("Build examples", "", PU, [
      "<b>Drone carrier</b>: orbiting drones that each fire their own shots",
      "<b>Crit missile swarm</b>: crits launch homing missiles",
      "<b>Piercing railgun</b>: one slow beam that hits a whole column",
      "<b>Shield retaliation</b>: absorbing damage fires a nova"])}
  {panel(sug() + " Show synergies on the card", "Module cards should name their combos (\"Drones + Missiles = Seeker Drones\"). That's how builds become 'ridiculous' without a codex.", YE)}
 </div>
</div>""", "Combat readability and three-card picks borrowed from Cup Heroes (pages 5 of the teardown).")

p("3. META LOOP", "The Station Is the Home Screen.", f"""
<div class="hero">
 <div class="herotext">
  <p class="pitch">Permanent upgrades unlock new build directions instead of just raising stats.</p>
  <div class="cols2 tight">
  {panel("Hangar", "Ships: 4 archetypes, each starting from a different build.", SC)}
  {panel("Engineering", "Modules: adds new cards to the upgrade pool.", PU)}
  {panel("Research", "Alien tech: rare, game-changing modules (needs Data Cores).", GR)}
  {panel("Navigation", "Sectors: unlocks the next chapter node and its modifiers.", YE)}
  </div>
  {panel("Launch scope", "", RE, ["1 station screen", "4 ship archetypes max", "No trading simulation", "No large star map; sectors are chapter nodes"])}
 </div>
 <div class="shots2">{s_station()}{s_hangar()}</div>
</div>""", "Salvage → station modules → new build options.")

p("4. ECONOMY", "Keep the Economy Readable.", f"""
<div class="hero">
 <div class="herotext">
  <p class="pitch">The player should understand every resource on sight.</p>
  <div class="cols3" style="gap:10px">
  {panel("Scrap", "", SC, ["Earned every run", "Station upgrades", "Main progression currency"])}
  {panel("Data Cores", "", PU, ["Bosses / anomalies", "Unlock ships and advanced tech", "Rare progression"])}
  {panel("Credits (optional)", "", YE, ["Premium / rewarded", "Cosmetics and rerolls", "Not required to progress"])}
  </div>
  <div class="cols2 tight">
  {panel("Retention", "", GR, ["Daily sector", "Weekly anomaly", "Ship mastery", "Rotating cosmetic"])}
  {panel("Avoid", "", RE, ["Fuel timers", "Lootbox ships", "Too many material types", "Aggressive timed bundles"])}
  </div>
  <div class="note">{sug()} <b>Drop Credits entirely</b> and price cosmetics in dollars, which leaves 2 currencies. A premium currency is the first step toward Cup Heroes-style exchange-rate pressure. {sug()} <b>Tractor Sort</b> (right) is a tactile cargo multiplier; Space Rock Breaker already pairs space mining with a Plinko board (page 8).</div>
 </div>
 <div class="shots2">{s_tractor()}{s_jump()}</div>
</div>""", "Economy pattern: run cargo → banked Scrap → station; rare Data Cores gate new ships.")

p("5. MONETIZATION", "Monetize Lightly. Keep the Game First.", f"""
<div class="hero">
 <div class="herotext tiers">
  <p class="pitch">A compact model inspired by mobile roguelites, without Cup Heroes-level pressure.</p>
  {panel("1 · Rewarded Ads <small>optional</small>", "Revive, reroll or reward boost. The player chooses the moment. " + sug() + " Cap them at about 3 per run.", SC)}
  {panel("2 · One-Time Support Pack <small>$3.99–$5.99</small>", "No forced ads, a cosmetic and starter currency.", GR)}
  {panel("3 · Cosmetics <small>$1.99–$4.99</small>", "Ship skins, trail effects, visual themes.", PU)}
  {panel("4 · Later: Mini Pass <small>$4.99 / season</small>", "Only after retention is proven. " + sug() + " Keep the premium track cosmetic.", YE)}
  <span class="rule" style="background:{SC}">RULE: NO PAYWALL ON CORE POWER</span>
 </div>
 <div class="shots2">{s_shop()}{s_pick()}</div>
</div>""", "Price ranges are from the original brief; they sit within the $0.99–$3.99 IAP range Soul Knight uses (Adapty estimate).")

p("6. MVP", "Small Enough to Actually Finish.", f"""
<p class="pitch">The prototype's job is to prove the loop before any content pipeline exists. {sug()} The list below is ship-specific (the original repeated the same list in both briefs).</p>
<div class="mvp">
{panel("Build First", "", SC, ["1 ship (Interceptor)", "1 sector (Rust Belt) of 6 waves", "8–10 modules, including 2 synergy pairs", "3 enemy archetypes: swarmer, shooter, tank", "1 boss encounter", "The Jump / Return screen", "1 station screen with 2 working modules"])}
{panel("Add After Fun", "", GR, ["3 more ships (Carrier, Lancer, Bastion)", "2 more sectors", "Daily sector + weekly anomaly", "Tractor Sort multiplier", "Cosmetics", "Rewarded ads", "Support pack"])}
{panel("Do Not Build Yet", "", RE, ["Guilds", "PvP", "Dozens of ships", "Complex crafting", "Large battle pass", "Live economy events", "An open star map"])}
</div>
<span class="rule" style="background:{SC}">TARGET: A PLAYABLE LOOP BEFORE A CONTENT PIPELINE</span>
<div class="note">{sug()} <b>A clear pass/fail test for the prototype:</b> does picking a module change how you move within 2 waves? If not, the builds aren't expressive enough, and more content won't fix that.</div>
""", "Scope deliberately mirrors the original brief's Build / Add / Don't columns.")

p("7. RESEARCH ANCHORS", "Why Space Made the Cut (and What's Unproven)", f"""
<div class="cols3">
{panel("StarVaders", tag("S") + " Released April 2025 on PC. Steam: <b>Overwhelmingly Positive</b>, ~3.7K reviews across languages in snapshots I found. A compact sci-fi roguelite deckbuilder.", SC)}
{panel("Space Rock Breaker", tag("S") + " $2.99 on Steam (Dec 2025). Mine asteroids, <b>process ore through a Plinko machine</b>, upgrade. Rated Overwhelmingly Positive in one listing. A September 2026 article reports a <b>mobile version in pre-registration</b>.", PU)}
{panel("Sensor Tower: State of Gaming 2026", tag("S") + " Mobile game IAP revenue reached <b>$82B</b> in 2025 (+1%). Most of it goes to the top 1% of publishers (92.5% of IAP revenue).", YE)}
</div>
<div class="note"><b>Corrections to the original brief:</b> it cites StarVaders at '93%+ with 4K+ reviews'. The snapshots I found show ~3.7K reviews and up to 98% positive, so the direction holds but I'd quote it as 'Overwhelmingly Positive'. Space Rock Breaker is a stronger anchor than the original says: it's small, cheap, space-themed, uses a Plinko reward board, and is moving to mobile.</div>
<div class="note" style="border-color:{RE}"><b>The gap:</b> all of these are <b>PC/Steam</b> signals. In my earlier research I found <b>no mobile revenue data for space roguelites</b>. Treat space as the less-proven of the two directions on mobile, and let a prototype or an early store test answer it.</div>
<ol class='srcs' style='margin-top:14px;columns:2'><li>Steam store: StarVaders<br><a href='https://store.steampowered.com/app/2417280/'>https://store.steampowered.com/app/2417280/</a></li><li>OpenCritic: StarVaders reviews<br><a href='https://opencritic.com/game/18471/-/reviews'>https://opencritic.com/game/18471/-/reviews</a></li><li>Automaton: Space Rock Breaker launch (Plinko ore processing)<br><a href='https://automaton-media.com/articles/newsjp/space-rock-breaker-20251224-388202/'>https://automaton-media.com/articles/newsjp/space-rock-breaker-20251224-388202/</a></li><li>MuMu Player: Space Rock Breaker details<br><a href='https://www.mumuplayer.com/blog/space-rock-breaker-release-date.html'>https://www.mumuplayer.com/blog/space-rock-breaker-release-date.html</a></li><li>Sensor Tower: State of Gaming 2026 press release<br><a href='https://sensortower.com/press/press-release-sensor-tower-state-of-gaming-gaming-drove-52-billion-downloads-82b-iap-revenue-on-mobile-and-12b-premium-revenue-on-steam'>https://sensortower.com/press/press-release-sensor-tower-state-of-gaming-gaming-drove-52-billion-downloads-82b-iap-revenue-on-mobile-and-12b-premium-revenue-on-steam</a></li><li>Adapty: Soul Knight IAP pricing estimate<br><a href='https://adapty.io/paywall-library/soul-knight/'>https://adapty.io/paywall-library/soul-knight/</a></li></ol>
""", "Sources checked October 2026; figures are snapshots and change over time. Figures are third-party estimates or snapshots, not developer disclosures.")

# =====================================================================
# THE LAST LANTERN — dungeon
# =====================================================================
LC = "#ffb03a"
LB1, LB2 = "#1f1510", "#07050a"


def lantern(cx, cy, s=1.0, glow=True):
    g = f'<g transform="translate({cx},{cy}) scale({s})">'
    if glow:
        g += '<circle cx="0" cy="4" r="22" fill="#ffb03a" opacity=".25"/>'
    g += '<path d="M-6,-16 A6,6 0 0 1 6,-16" fill="none" stroke="#c9a46a" stroke-width="2"/>'
    g += '<rect x="-9" y="-14" width="18" height="4" rx="1" fill="#8a6a3a" stroke="#1a1008" stroke-width="1.5"/>'
    g += '<rect x="-8" y="-10" width="16" height="22" rx="3" fill="#ffd27a" stroke="#1a1008" stroke-width="2"/>'
    g += '<ellipse cx="0" cy="2" rx="3.5" ry="6" fill="#fff6d8"/>'
    g += '<rect x="-9" y="12" width="18" height="4" rx="1" fill="#8a6a3a" stroke="#1a1008" stroke-width="1.5"/>'
    return g + "</g>"


def lgrad(gid, r=1.0):
    return (f'<defs><radialGradient id="{gid}" cx="0.5" cy="0.62" r="{0.55*r}">'
            '<stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".7" stop-color="#000" stop-opacity=".55"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".95"/></radialGradient></defs>')


def floor_tiles(y0=60, y1=440):
    out = ""
    for r, y in enumerate(range(y0, y1, 34)):
        for k, x in enumerate(range(-17 if r % 2 else 0, W, 34)):
            out += f'<rect x="{x}" y="{y}" width="33" height="33" fill="{"#3a2c22" if (r+k)%2 else "#33261d"}"/>'
    return out


def skel(cx, cy, s=1.0, col="#d8d0c0"):
    g = f'<g transform="translate({cx},{cy}) scale({s})">'
    g += '<ellipse cx="0" cy="26" rx="12" ry="3" fill="#00000077"/>'
    g += f'<rect x="-7" y="4" width="14" height="20" rx="4" fill="#5a4a3a" stroke="#120a06" stroke-width="2"/>'
    g += f'<circle cx="0" cy="-6" r="11" fill="{col}" stroke="#120a06" stroke-width="2"/>'
    g += '<circle cx="-4" cy="-7" r="3" fill="#ff4f4f"/><circle cx="4" cy="-7" r="3" fill="#ff4f4f"/>'
    return g + "</g>"


def l_hub():
    i = topbar(5, "640", "2", "#b8742a")
    i += pill(14, 52, 92, 22, "#ffffff14", "Town", "#fff", 10, "#ffffff44")
    i += pill(112, 52, 104, 22, LC, "Daily Descent", "#2a1505", 9, "#fff")
    i += txt(W / 2, 98, "THE UNDERCRYPT", 19, "#fff", 900) + txt(W / 2, 116, "BEST DEPTH: FLOOR 7", 11, LC, 900)
    i += '<path d="M40,330 L40,180 L80,150 L80,130 L100,130 L100,150 L130,150 L130,130 L150,130 L150,150 L190,180 L190,330 Z" fill="#241a14" stroke="#4a3a2a" stroke-width="3"/>'
    i += '<path d="M85,330 L85,230 A30,30 0 0 1 145,230 L145,330 Z" fill="#050305"/>'
    i += '<circle cx="115" cy="285" r="50" fill="#ffb03a" opacity=".12"/>'
    i += chibi(115, 290, "#6a4a8a", hat="hood", s=1.1) + lantern(136, 286, 0.8)
    i += txt(W / 2, 352, "Lantern oil: ▮▮▮▮▮▮", 10, LC, 800)
    i += pill(52, 362, 126, 32, LC, "DESCEND", "#2a1505", 16, "#fff", 900)
    i += bottomnav(["Shop", "Town", "Descend", "Heroes", "Daily"], 2, "#160f0a", LC)
    return phone(i, LB1, LB2, "Town hub: one big DESCEND button")


def l_run():
    gid = "lg_run"
    i = lgrad(gid) + floor_tiles()
    i += skel(60, 150, 0.9) + skel(175, 170, 0.9) + skel(45, 260, 0.8) + skel(190, 280, 0.9, "#a0c0a0")
    i += '<line x1="118" y1="300" x2="178" y2="182" stroke="#ffe27a" stroke-width="2" stroke-dasharray="4 4"/>'
    i += chibi(115, 320, "#a33b3b", hat="helm") + lantern(140, 318, 0.75)
    i += f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{gid})"/>'
    i += pill(10, 12, 60, 20, "#3a8a3a", "HP 82", "#fff", 9) + pill(76, 12, 78, 20, "#ffffff22", "ROOM 7", "#fff", 9) + pill(160, 12, 60, 20, "#ffffff22", "GOLD 43", "#ffd76a", 9)
    i += box(10, 40, 210, 8, "#ffffff22", 4) + box(10, 40, 128, 8, LC, 4) + txt(W / 2, 62, "LANTERN OIL · light shrinks as it drains", 8, "#ffd27a", 700)
    i += '<circle cx="190" cy="415" r="22" fill="#5b3fd1" stroke="#fff" stroke-width="2"/>' + txt(190, 419, "DODGE", 8.5, "#fff", 900)
    i += txt(95, 420, "AUTO ATTACK", 10, "#ffffffaa", 900)
    return phone(i, "#2a1e16", "#07050a", "Run screen: auto-combat inside the lantern's light")


def l_pick():
    i = topbar(5, "640", "2", "#b8742a")
    i += txt(W / 2, 70, "ROOM CLEARED", 15, "#ffe27a", 900) + txt(W / 2, 88, "Choose an Upgrade", 11, "#fff", 700)
    i += chibi(115, 140, "#a33b3b", hat="helm", s=0.9) + lantern(138, 140, 0.6)
    i += box(8, 182, W - 16, 210, "#00000088", 12)
    cy = 200
    i += card(14, cy, 66, 130, "#1f4a1f", "POISON|BLADE", "FREE", "#4e8a5a",
              '<path d="M47,212 C38,228 38,240 47,248 C56,240 56,228 47,212 Z" fill="#8fe36a" stroke="#1a1020" stroke-width="2"/>')
    i += card(82, cy, 66, 130, "#1f2f5a", "RICOCHET", "90", "#4fb6ff",
              '<polyline points="98,250 112,215 124,245 134,212" fill="none" stroke="#e8fbff" stroke-width="3"/>')
    i += card(150, cy, 66, 130, "#4a3a1a", "SHIELD|BASH", "120", "#d9a03a",
              '<path d="M183,212 L199,218 L197,236 C195,244 189,248 183,250 C177,248 171,244 169,236 L167,218 Z" fill="#c9c9c9" stroke="#1a1020" stroke-width="2"/>')
    i += pill(42, 362, 92, 22, "#c0267a", "REROLL  20", "#fff", 10) + pill(140, 362, 48, 22, "#7b4fd1", "AD ▶", "#fff", 9)
    i += txt(W / 2, 420, "Upgrade picks after key rooms", 8, "#ffffffaa", 600)
    return phone(i, "#2a1e16", "#0a0608", "Upgrade pick: 1 of 3 after key rooms")


def l_extract():
    i = topbar(5, "640", "2", "#b8742a")
    i += txt(W / 2, 74, "LANTERN SHRINE", 16, LC, 900) + txt(W / 2, 92, "A safe room. Rest or press on?", 9.5, "#fff", 600)
    i += '<circle cx="115" cy="140" r="34" fill="#ffb03a" opacity=".18"/>' + lantern(115, 140, 1.6)
    i += box(20, 184, 190, 40, "#ffffff10", 10, "#ffffff33") + txt(W / 2, 202, "Run loot: 340 Gold · 1 Relic", 9.5, "#fff", 700) + txt(W / 2, 216, "HP 46/100 · Oil 30%", 8.5, "#ffffffaa", 700)
    i += box(14, 236, 98, 150, "#1a3a22", 14, "#57e08a", 2) + txt(63, 260, "EXTRACT", 12, "#57e08a", 900)
    i += txt(63, 300, "Bank it all", 9, "#fff", 700) + txt(63, 318, "340 Gold", 11, "#ffd76a", 900) + txt(63, 334, "+1 Relic", 9, "#d2b6ff", 800)
    i += box(118, 236, 98, 150, "#3a1a10", 14, "#ff6b4a", 2) + txt(167, 260, "PUSH", 12, "#ff6b4a", 900)
    i += txt(167, 284, "Floor 8", 9, "#fff", 700) + txt(167, 300, "loot x1.5", 11, "#ffd76a", 900)
    i += txt(167, 318, "oil keeps draining", 8, "#ffb0a0", 700) + txt(167, 334, "die = lose 50%", 8, "#ff9b9b", 700)
    i += txt(W / 2, 412, "This screen IS the game's tension", 8.5, "#ffffffaa", 600)
    return phone(i, "#2a1a10", "#07050a", "Extract or Push at a Lantern Shrine")


def l_town():
    i = topbar(5, "640", "2", "#b8742a")
    i += txt(W / 2, 70, "EMBERFALL · TOWN", 15, "#fff", 900)
    blds = [(24, 92, "BLACKSMITH", "Weapons", "#8a4a2a", "Lv 2"), (124, 92, "ALCHEMIST", "Potions", "#3a7a5a", "Lv 1"),
            (24, 196, "GUILD", "Heroes", "#5a3a8a", "Lv 1"), (124, 196, "MAP ROOM", "Biomes", "#2a5a8a", "Lv 1")]
    for x, y, n, d, c, l in blds:
        i += box(x, y, 82, 92, c, 12, "#fff", 2)
        i += f'<polygon points="{x+14},{y+46} {x+41},{y+18} {x+68},{y+46}" fill="#00000055"/><rect x="{x+20}" y="{y+46}" width="42" height="16" fill="#00000044"/>'
        i += f'<rect x="{x+36}" y="{y+50}" width="10" height="12" fill="#ffd27a"/>'
        i += txt(x + 41, y + 76, n, 8.5, "#fff", 900) + txt(x + 41, y + 87, d, 7.5, "#ffffffbb", 600)
        i += pill(x + 50, y + 4, 30, 14, "#000000aa", l, "#fff", 7)
    i += box(14, 300, W - 28, 60, "#ffffff10", 10, "#ffffff33")
    i += txt(W / 2, 320, "NEXT UNLOCK", 9, LC, 900) + txt(W / 2, 338, "Blacksmith Lv 3: Chain-Lightning weapon", 8.5, "#fff", 700)
    i += pill(52, 370, 126, 24, "#ffd76a", "UPGRADE · 300 GOLD", "#2a1a05", 9)
    i += bottomnav(["Shop", "Town", "Descend", "Heroes", "Daily"], 1, "#160f0a", LC)
    return phone(i, LB1, LB2, "Town: 4 buildings unlock new options")


def l_heroes():
    i = topbar(5, "640", "2", "#b8742a")
    i += txt(W / 2, 70, "THE GUILD", 15, "#fff", 900)
    heroes = [("WARDEN", "Shield · melee", "#a33b3b", "helm", True), ("ROGUE", "Poison · crits", "#2f6b3e", "hood", True),
              ("PYRE", "Fire · AoE", "#3a3fa3", "wizard", False), ("TINKER", "Turrets", "#8a6a2a", "goggles", False)]
    for k, (n, d, c, h, on) in enumerate(heroes):
        x, y = 14 + (k % 2) * 104, 86 + (k // 2) * 150
        i += box(x, y, 98, 140, "#ffffff12" if on else "#ffffff06", 12, LC if on else "#444", 2)
        i += chibi(x + 49, y + 50, c if on else "#444", "#f2c9a0" if on else "#666", h, 1.1)
        i += txt(x + 49, y + 106, n, 9, "#fff" if on else "#777", 900) + txt(x + 49, y + 120, d, 7.5, "#ffffffaa", 600)
        if not on:
            i += pill(x + 24, y + 126, 50, 12, "#000", "3 RELICS", "#d2b6ff", 6.5)
    i += txt(W / 2, 402, "Heroes unlock with Relics, never cash", 8.5, LC, 700)
    i += bottomnav(["Shop", "Town", "Descend", "Heroes", "Daily"], 3, "#160f0a", LC)
    return phone(i, LB1, LB2, "Guild: heroes unlock with Relics")


def l_shop():
    i = topbar(5, "640", "2", "#b8742a")
    i += txt(W / 2, 66, "THE PEDDLER", 15, LC, 900)
    i += box(12, 80, W - 24, 128, "#8a4a1a", 14, "#fff", 2)
    i += txt(24, 104, "LAMPLIGHTER'S", 14, "#fff", 900, "start") + txt(24, 120, "SUPPORT PACK", 14, "#ffe27a", 900, "start")
    for k, l in enumerate(["No forced ads", "Brass lantern skin", "500 Gold head start"]):
        i += txt(24, 142 + k * 14, "• " + l, 9, "#fff", 600, "start")
    i += lantern(182, 128, 1.4)
    i += pill(130, 176, 80, 24, "#3ac46a", "$4.99", "#fff", 12, "#fff")
    i += txt(30, 194, "ONE TIME", 8, "#ffffffaa", 700, "start")
    i += box(12, 218, 104, 120, "#3a2a5a", 12, "#fff", 2) + chibi(64, 262, "#e8e0c8", hat="wizard")
    i += txt(64, 304, "HERO OUTFIT", 9, "#fff", 900) + pill(26, 312, 76, 18, "#3ac46a", "$1.99", "#fff", 10)
    i += box(124, 218, 94, 120, "#1f3a4a", 12, "#fff", 2)
    i += '<circle cx="171" cy="262" r="22" fill="#6bd6ff" opacity=".35"/>' + lantern(171, 262, 1.0, glow=False)
    i += txt(171, 304, "FLAME COLOR", 9, "#fff", 900) + pill(134, 312, 74, 18, "#3ac46a", "$0.99", "#fff", 10)
    i += txt(W / 2, 362, "No paywall on core power", 8.5, "#ffffffbb", 700)
    i += bottomnav(["Shop", "Town", "Descend", "Heroes", "Daily"], 0, "#160f0a", LC)
    return phone(i, LB1, LB2, "Shop: support pack + cosmetics only")


ll = []
q = mkpage(ll, "The Last Lantern · prototype concept", LC)
LL_TAGS = '<div class="tags" style="--k:#ffb03a"><span>8–15 MINUTE RUNS</span><span>AUTO-COMBAT</span><span>EXTRACT OR PUSH</span><span>PORTRAIT</span></div>'

ll.append(f"""<section class="page cover">
<div class="kicker" style="color:{LC}">PROTOTYPE BRIEF · REDESIGNED EDITION</div>
<h1 class="big">THE LAST LANTERN</h1>
<div class="sub">A portrait dungeon-crawler roguelite: descend room by room, grow stronger, and decide when to get out alive</div>
{LL_TAGS}
<div class="covergrid">
 <div>
  {panel("Design goal", '<span class="goal">Fast choices, visible power growth, low content burden.</span><br>Built for a small team and light monetization.', LC)}
  {panel("Reading Key", "This edition keeps the original brief's ideas and adds detail:", YE,
         ["Untagged: from the original brief",
          sug() + " My addition or fix, for you to accept or reject",
          tag("S") + " Checked against a cited source (page 8)",
          "All art is placeholder SVG drawn for this brief"])}
 </div>
 <div class="coverart">{l_hub()}{l_run()}</div>
</div>
<div class="strip">
 {panel("Loop", "Enter · Fight · Pick · Risk · Extract (p.2–3)", LC)}
 {panel("Meta", "The town and its 4 buildings (p.4)", PU)}
 {panel("Economy &amp; store", "Three currencies max, light monetization (p.5–6)", YE)}
 {panel("MVP &amp; research", "What to build first, and why (p.7–8)", GR)}
</div>
<div class="foot"><i>The Last Lantern · prototype concept · redesigned from the original GPT brief</i><span>01</span></div></section>""")

q("1. CORE LOOP", "One Run. Five Beats.", loop([
    ("ENTER", "Choose hero"), ("FIGHT", "Auto-combat"), ("PICK", "1 of 3 upgrades"),
    ("RISK", "Go deeper?"), ("EXTRACT", "Bank loot")], [LC, RE, PU, YE, GR]) + f"""
<div class="hero">
 <div class="herotext">
  <p class="pitch">The whole game should make sense to a new player in under a minute.</p>
  {panel("Why it works", "", LC, ["Frequent decision points", "Power increases every few rooms", "Extraction creates tension without needing a complex story"])}
  {panel("Prototype rule", "If the run isn't fun with one hero and one biome, stop adding content.", RE)}
  {panel(sug() + " Make the lantern the mechanic", "The name promises a lantern, but the original never uses one. Proposal: <b>Lantern Oil</b> drains each room. As it drains, the light shrinks and more enemies spawn in the dark. Shrines let you extract. Oil is the soft timer behind 'go deeper?', and it gives the game a visual identity in screenshots.", YE)}
 </div>
 <div class="shots2">{l_run()}{l_extract()}</div>
</div>""", "Inspired by Cup Heroes' action → choice → reward → upgrade loop; extraction adds the push-your-luck layer.")

q("2. RUN SCREEN", "Combat Should Be Readable at a Glance.", f"""
<div class="hero rev">
 <div class="shots2">{l_run()}{l_pick()}</div>
 <div class="herotext">
  <p class="pitch">The player barely moves; the decisions happen between bursts of combat.</p>
  {panel("Moment-to-moment", "", LC, ["Hero auto-attacks", "A small dodge or active ability", "Enemies arrive in short waves", "Upgrade choice after key rooms"])}
  {panel("Run tension", "", RE, ["Health carries forward between rooms", "Loot grows as the run continues", "Player can extract at safe rooms (Lantern Shrines)", "Death loses a portion of run loot " + sug() + " (suggest 50%)"])}
  {panel("Upgrade examples", "Poison Blade (damage over time) · Ricochet (attacks bounce to 2 more enemies) · Shield Bash (blocking stuns). Each hero has 1–2 upgrade families it leans toward.", PU)}
 </div>
</div>""", "Fixed: 'Richochet' → 'Ricochet'. Three-card picks borrowed from the Cup Heroes teardown (page 5).")

q("3. META LOOP", "The Town Is the Retention Layer.", f"""
<div class="hero">
 <div class="herotext">
  <p class="pitch">Permanent progress should unlock options without making earlier runs pointless.</p>
  <div class="cols2 tight">
  {panel("Blacksmith", "Weapons: adds new weapon types to the upgrade pool.", RE)}
  {panel("Alchemist", "Potions: one consumable slot per run.", GR)}
  {panel("Guild", "Heroes: unlocked with Relics.", PU)}
  {panel("Map Room", "Biomes: the next dungeon and its modifiers.", CY)}
  </div>
  {panel("Launch scope", "", LC, ["1 town screen", "4 upgrade buildings", "No crafting grid", "No inventory micromanagement", "Unlock more choices instead of flat +100% power"])}
 </div>
 <div class="shots2">{l_town()}{l_heroes()}</div>
</div>""", "Run loot → town buildings → permanent unlocks.")

q("4. ECONOMY", "Three Currencies Maximum.", f"""
<div class="hero">
 <div class="herotext">
  <p class="pitch">Avoid the visual and mental overload of a mature free-to-play economy.</p>
  <div class="cols3" style="gap:10px">
  {panel("Gold", "", LC, ["Earned in runs", "Town upgrades", "Common / plentiful"])}
  {panel("Relics", "", PU, ["Bosses / milestones", "Unlock heroes and rare systems", "Slow / meaningful"])}
  {panel("Gems (optional)", "", CY, ["Premium / rewarded", "Cosmetics, rerolls", "Never required for core progression"])}
  </div>
  <div class="cols2 tight">
  {panel("Retention", "", GR, ["Daily challenge", "Weekly dungeon modifier", "Short unlock goals", "Hero mastery"])}
  {panel("Avoid", "", RE, ["Energy timers", "Forced ad spam", "Five overlapping currencies", "Constant offer popups"])}
  </div>
  <div class="note">{sug()} <b>Drop Gems</b> and price cosmetics in dollars, which leaves 2 currencies. {sug()} Lantern Oil is <i>not</i> a currency: it resets every run and is never sold, so it can't become an energy system by the back door.</div>
 </div>
 <div class="shots2">{l_extract()}{l_heroes()}</div>
</div>""", "Economy pattern: run loot is banked on extract; Relics gate heroes; nothing sells power.")

q("5. MONETIZATION", "Monetize Lightly. Keep the Game First.", f"""
<div class="hero">
 <div class="herotext tiers">
  <p class="pitch">A compact model inspired by mobile roguelites, without Cup Heroes-level pressure.</p>
  {panel("1 · Rewarded Ads <small>optional</small>", "Revive, reroll or reward boost. The player chooses the moment. " + sug() + " Never offer a revive ad <i>after</i> a failed Push; it undermines the extract decision.", LC)}
  {panel("2 · One-Time Support Pack <small>$3.99–$5.99</small>", "No forced ads, a cosmetic and starter currency.", GR)}
  {panel("3 · Cosmetics <small>$1.99–$4.99</small>", "Hero outfits, lantern skins, flame colors.", PU)}
  {panel("4 · Later: Mini Pass <small>$4.99 / season</small>", "Only after retention is proven.", YE)}
  <span class="rule" style="background:{LC}">RULE: NO PAYWALL ON CORE POWER</span>
 </div>
 <div class="shots2">{l_shop()}{l_pick()}</div>
</div>""", "Comparable light model on mobile: Soul Knight sells $0.99–$3.99 unlocks (Adapty estimate).")

q("6. MVP", "Small Enough to Actually Finish.", f"""
<p class="pitch">The prototype's job is to prove the loop before any content pipeline exists. {sug()} The list below is dungeon-specific (the original repeated the same list in both briefs).</p>
<div class="mvp">
{panel("Build First", "", LC, ["1 hero (Warden)", "1 biome (the Undercrypt) of about 8 rooms", "8–10 run upgrades", "3 enemy archetypes: rusher, archer, brute", "1 boss encounter", "Lantern Oil + 1 Shrine extract screen", "1 town screen with 2 working buildings"])}
{panel("Add After Fun", "", GR, ["3 more heroes (Rogue, Pyre, Tinker)", "2 more biomes", "Daily challenge + weekly modifier", "Cosmetics", "Rewarded ads", "Support pack"])}
{panel("Do Not Build Yet", "", RE, ["Guilds (social)", "PvP", "50 characters", "Complex crafting", "Large battle pass", "Live economy events"])}
</div>
<span class="rule" style="background:{LC}">TARGET: A PLAYABLE LOOP BEFORE A CONTENT PIPELINE</span>
<div class="note">{sug()} <b>A clear pass/fail test for the prototype:</b> do testers hesitate at the Shrine? If everyone always extracts (or always pushes), the risk numbers are wrong. Tune those before adding content.</div>
""", "Scope deliberately mirrors the original brief's Build / Add / Don't columns.")

q("7. RESEARCH ANCHORS", "Why the Dungeon Crawler Made the Cut", f"""
<div class="cols3">
{panel("Hades II", tag("S") + " Full launch September 25, 2025. Steam: <b>Overwhelmingly Positive (~95%)</b>, ~114K reviews in late-2025 snapshots; peak of <b>112,947</b> concurrent players (SteamDB, via wnhub).", LC)}
{panel("Mobile dungeon crawlers at small scale", tag("S") + " <b>Soul Knight</b>: $0.99–$3.99 IAPs, ~$400K/month (Adapty estimate). <b>Shattered Pixel Dungeon</b>: solo developer, no ads or IAP, cosmetic supporter extras (Flathub).", GR)}
{panel("Roguelikes growing on mobile", tag("S") + " AppMagic: roguelike titles grew <b>26.2% year over year</b> in 2025, while RPG revenue overall fell 17%. Sensor Tower: <b>$82B</b> mobile IAP in 2025.", PU)}
</div>
<div class="note"><b>Corrections to the original brief:</b> it cites Hades II with '124K+ reviews'. The snapshots I could find show ~114K in late 2025, so 124K is plausible by now, but I couldn't confirm it. More importantly, Hades II is a premium console/PC game made by an experienced studio. It shows that players love the genre, not that it can be sold on mobile with light monetization. The mobile examples in the middle panel are better evidence for the model you want.</div>
<div class="note" style="border-color:{GR}"><b>Why this one is the safer bet:</b> unlike space, dungeon crawlers have mobile evidence at <i>both</i> ends: heavy (Archero 2) and light (Soul Knight, Shattered Pixel Dungeon). The extract-or-push hook and the lantern visual are what will make it stand out.</div>
<ol class='srcs' style='margin-top:14px;columns:2'><li>wnhub.io: Hades 2 peaks above 112,000 players on Steam (SteamDB)<br><a href='https://wnhub.io/news/stores-and-publishing/item-48951'>https://wnhub.io/news/stores-and-publishing/item-48951</a></li><li>GameGeeker: Hades II Steam review snapshot<br><a href='https://gamegeeker.com/games/hades-ii?market=PL'>https://gamegeeker.com/games/hades-ii?market=PL</a></li><li>Outlook Respawn: Hades 2 OpenCritic 95<br><a href='https://respawn.outlookindia.com/gaming/gaming-news/hades-2-opencritic-score-hits-95-joins-in-elite-tier'>https://respawn.outlookindia.com/gaming/gaming-news/hades-2-opencritic-score-hits-95-joins-in-elite-tier</a></li><li>Adapty: Soul Knight revenue/IAP estimate<br><a href='https://adapty.io/paywall-library/soul-knight/'>https://adapty.io/paywall-library/soul-knight/</a></li><li>Flathub: Shattered Pixel Dungeon<br><a href='https://flathub.org/sv/apps/com.shatteredpixel.shatteredpixeldungeon'>https://flathub.org/sv/apps/com.shatteredpixel.shatteredpixeldungeon</a></li><li>AppMagic 2025 monetization report (summary)<br><a href='https://gamedevreports.substack.com/p/appmagic-mobile-games-monetization'>https://gamedevreports.substack.com/p/appmagic-mobile-games-monetization</a></li></ol>
""", "Sources checked October 2026; figures are snapshots and change over time. Figures are third-party estimates or snapshots, not developer disclosures.")

render(sr, "Salvage Run Brief", os.path.join(HERE, "salvage_run.html"))
render(ll, "The Last Lantern Brief", os.path.join(HERE, "last_lantern.html"))
print(len(sr), len(ll))
