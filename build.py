# Build script for the 2K Archive static page. Edit data here and re-run.
# Future game updates: edit the data structures, run `python3 build.py`, commit + push -> Vercel auto-deploys.
# Redesign 2026-11-11 (Council-gated): layout/a11y refactor ONLY — all data literals unchanged.
# Imagery: each of the 14 assets/ PNGs is inlined exactly ONCE, as a CSS background class
# (data URIs cannot be shared between <img> tags in a single file). Logo/trophy spans carry
# role="img" + aria-label as the alt-text equivalent. index.html is GENERATED — never hand-edit it.
import html

TEAMS = {
 # key: (display, logo, caption_era, conf, color)
 'heat06':   ("'06 Heat", 'heat06.png', '2005–06', 'East', '#98002e'),
 'heat':     ("Heat", 'heat-current.png', 'Current', 'East', '#98002e'),
 'knicks12': ("'12 Knicks", 'knicks12.png', '2011–12', 'East', '#006bb6'),
 'spurs98':  ("'98 Spurs", 'spurs98.png', '1997–98', 'West', '#111111'),
 'sixers01': ("'01 76ers", 'sixers01.png', '2000–01', 'East', '#002b5c'),
 'bulls96':  ("'96 Bulls", 'bulls96.png', '1995–96', 'East', '#ce1141'),
 'lakers01': ("'01 Lakers", 'lakers01.png', '2000–01', 'West', '#552d82'),
 'cavs16':   ("'16 Cavs", 'cavs16.png', '2015–16', 'East', '#860038'),
 'clippers14':("'14 Clippers", 'clippers14.png', '2013–14', 'West', '#c8102e'),
 'mavs19':   ("'19 Mavs", 'mavs19.png', '2018–19', 'West', '#00538c'),
 'rockets19':("'19 Rockets", 'rockets19.png', '2018–19', 'West', '#ce1141'),
 'rockets':  ("Rockets", 'rockets-current.png', 'Current', 'West', '#ce1141'),
 'cavs0607': ("'06-07 Cavs", 'cavs0607.png', '2006–07', 'East', '#860038'),
}

def chip(key):
    name, logo, era, conf, color = TEAMS[key]
    return (f'<span class="chip logo-{key}" role="img" aria-label="{html.escape(name)} logo" '
            f'style="border-color:{color}"></span>')

def trophy_span(cls):
    return f'<span class="{cls} logo-trophy" role="img" aria-label="Larry O\'Brien Trophy"></span>'

def team_cell(key, player, home=None, winner=False):
    name, logo, era, conf, color = TEAMS[key]
    cap = f'{era} · {conf} · {player}' + (f' · {home}' if home else '')
    star = ' <span class="star" aria-hidden="true">★</span>' if winner else ''
    sr = '<span class="sr-only"> (winner)</span>' if winner else ''
    cls = 'team winner' if winner else 'team'
    return (f'<div class="{cls}">{chip(key)}<span class="tmeta">'
            f'<span class="tname">{html.escape(name)}{star}{sr}</span>'
            f'<span class="tcap">{cap}</span></span></div>')

def game_row(label, a, b, muted=None):
    # a,b: dicts for team_cell; muted: text for unplayed rows
    if muted:
        return (f'<div class="row muted"><span class="glabel">{label}</span>'
                f'{team_cell(**a)}<span class="vs">{html.escape(muted)}</span>{team_cell(**b)}</div>')
    return (f'<div class="row"><span class="glabel">{label}</span>'
            f'{team_cell(**a)}<span class="vs">def.</span>{team_cell(**b)}</div>')

def strip(cells):
    return '<div class="strip">' + ''.join(
        f'<div class="cell"><span class="clab">{l}</span><span class="cval">{v}</span></div>' for l, v in cells) + '</div>'

def matchup_box(left_key, right_key, center_top, center_bot):
    ln = TEAMS[left_key][0]; rn = TEAMS[right_key][0]
    return (f'<div class="mbox"><div class="mside">{chip(left_key)}<span>{ln}</span></div>'
            f'<div class="mcenter">{trophy_span("mtrophy")}'
            f'<span class="mct">{center_top}</span><span class="mcb">{center_bot}</span></div>'
            f'<div class="mside">{chip(right_key)}<span>{rn}</span></div></div>')

def wire_details(title, lines):
    # Native <details> disclosure (Council E3/E4): closed on load, non-exclusive, no JS.
    inner = ''.join(f'<p class="wline">{l}</p>' for l in lines)
    return (f'<details class="wirebox"><summary><span class="sumlab">{title} — {len(lines)} ITEMS</span></summary>'
            f'<div class="wire">{inner}</div></details>')

def unplayed_details(reason, rows_html, count):
    # Grouped unplayed-games disclosure; summary carries the verbatim reason (Council E4).
    return (f'<details class="unplayed"><summary><span class="sumlab">UNPLAYED GAMES — {count} · </span>'
            f'<span class="sumreason">{html.escape(reason)}</span></summary>'
            f'<div class="results">{rows_html}</div></details>')

H2H = ('HEAD-TO-HEAD', 'Lucian 13 – 2 Josiah')

# ---- THE ROUNDS ----
rounds_rows = ''.join([
    game_row('R1', dict(key='heat06', player='Lucian', home='Home', winner=True),
                   dict(key='knicks12', player='Josiah', home='Away')),
    game_row('R2', dict(key='spurs98', player='Josiah', home='Home', winner=True),
                   dict(key='sixers01', player='Lucian', home='Away')),
    game_row('R3', dict(key='lakers01', player='Josiah', home='Away', winner=True),
                   dict(key='bulls96', player='Lucian', home='Home')),
    game_row('R4', dict(key='rockets', player='Lucian', home='Home', winner=True),
                   dict(key='heat', player='Josiah', home='Away')),
])
rounds = (strip([('ROUNDS', 'Tied 2 – 2'), H2H, ('WIN RATE', 'Lucian 87%'), ('STREAK', 'Lucian W12'), ('TROPHY', 'Unclaimed')])
    + '<h2 class="headline">ROUNDS DEADLOCKED AT 2-2</h2>'
    + '<div class="mbox"><div class="mcenter solo">' + trophy_span("mtrophy")
      + '<span class="mct">ROUNDS — TIED 2-2</span><span class="mcb">TROPHY UNCLAIMED</span></div></div>'
    + f'<div class="results">{rounds_rows}</div>')

# ---- FINALS 1 ----
def f1_row(g, home_side):
    a = dict(key='clippers14', player='Josiah', home='Home' if home_side == 'j' else 'Away')
    b = dict(key='cavs16', player='Lucian', home='Home' if home_side == 'l' else 'Away', winner=True)
    return game_row(g, a, b)
f1_played = ''.join([f1_row('G1', 'j'), f1_row('G2', 'j'), f1_row('G3', 'l'), f1_row('G4', 'l')])
f1_unplayed = ''.join(game_row(f'G{n}', dict(key='clippers14', player='Josiah'), dict(key='cavs16', player='Lucian'), muted='Not needed — series ended 4-0') for n in (5, 6, 7))
finals1 = (strip([('SERIES', 'Lucian 4 – 0 Josiah'), ('CHAMPION', 'Lucian'), H2H, ('FINALS TITLES', 'Lucian 2 · Josiah 0'), ('TROPHY', 'Claimed')])
    + '<h2 class="headline">CAVS SWEEP CLIPPERS</h2>'
    + matchup_box('clippers14', 'cavs16', 'FINALS 1 — CHAMPION', 'LUCIAN')
    + f'<div class="results">{f1_played}</div>'
    + unplayed_details('Not needed — series ended 4-0', f1_unplayed, 3))

# ---- FINALS 2 ----
def f2_row(g):
    return game_row(g, dict(key='mavs19', player='Lucian', winner=True), dict(key='rockets19', player='Josiah'))
f2_played = ''.join(f2_row(f'G{n}') for n in (1, 2, 3, 4))
f2_unplayed = ''.join(game_row(f'G{n}', dict(key='mavs19', player='Lucian'), dict(key='rockets19', player='Josiah'), muted='Not needed — series ended 4-0') for n in (5, 6, 7))
finals2 = (strip([('SERIES', 'Lucian 4 – 0 Josiah'), ('CHAMPION', 'Lucian'), H2H, ('FINALS TITLES', 'Lucian 2 · Josiah 0'), ('TROPHY', 'Claimed')])
    + '<h2 class="headline">MAVS SWEEP ROCKETS, LUCIAN REPEATS AS CHAMPION</h2>'
    + matchup_box('mavs19', 'rockets19', 'FINALS 2 — CHAMPION', 'LUCIAN')
    + f'<div class="results">{f2_played}</div>'
    + unplayed_details('Not needed — series ended 4-0', f2_unplayed, 3)
    + wire_details('FROM THE WIRE', ['HALFTIME — Rockets lead by 12', 'MAVS WIN GAME 1', 'HALFTIME — Mavs lead by 16',
                             'MAVS WIN GAME 2 — SERIES 2-0', 'MAVS WIN GAME 3 — SERIES 3-0', 'MAVS WIN GAME 4 — SERIES 2 CHAMPIONS']))

# ---- SERIES 3 ----
def s3_row(g):
    return game_row(g, dict(key='spurs98', player='Josiah'), dict(key='cavs0607', player='Lucian', winner=True))
s3_played = ''.join(s3_row(f'G{n}') for n in (1, 2, 3))
s3_unplayed = ''.join(game_row(f'G{n}', dict(key='spurs98', player='Josiah'), dict(key='cavs0607', player='Lucian'), muted='Not played yet — series to be continued') for n in (4, 5, 6, 7))
series3 = (strip([('SERIES', 'Lucian 3 – 0 Josiah'), ('STATUS', 'On hold — to be continued'), ('CHAMPION', 'None'), H2H, ('TROPHY', 'Unclaimed')])
    + '<h2 class="headline">ROBINSON\'S BEST WASN\'T ENOUGH</h2>'
    + matchup_box('spurs98', 'cavs0607', 'FINALS 3 — ON HOLD AT 3-0', 'NO CHAMPION YET')
    + f'<div class="results">{s3_played}</div>'
    + unplayed_details('Not played yet — series to be continued', s3_unplayed, 4)
    + wire_details('GAME RECAPS', ['JAMES, CAVS TAKE GAME 1 FROM SPURS', 'JAMES, CAVS REPEL SPURS\' RALLY FOR 2-0 LEAD', 'JAMES, CAVS BURY SPURS FOR 3-0 LEAD'])
    + wire_details('FROM THE WIRE', ['CAVS WIN GAME 1 — SERIES 1-0', 'CAVS HANDLE SPURS AGAIN, GO UP 2-0', 'CAVS ROUT SPURS, ONE WIN FROM THE SWEEP']))

# ---- RÉSUMÉS (aligned shared grid; fixed label column; max 3 most-used teams) ----
def resume(name, trophies, playstyle, overall, finals, rounds_rec, winrate, most_used):
    t = ''.join(trophy_span("mini-trophy") for _ in range(trophies))
    mu = ' · '.join(f'{chip(k)} {TEAMS[k][0]} ({c})' for k, c in most_used)
    rows = [('Playstyle', f'<span class="pstyle">{playstyle}</span>'), ('Overall', overall), ('Finals', finals), ('Rounds', rounds_rec), ('Win rate', winrate), ('Most used', mu)]
    body = ''.join(f'<div class="rrow{" mu" if l == "Most used" else " ps" if l == "Playstyle" else ""}"><span class="rlab">{l}</span><span class="rval">{v}</span></div>' for l, v in rows)
    return (f'<section class="resume"><div class="rname"><h2>{name}</h2><span class="trophies">{t}</span></div>{body}</section>')

resumes = ('<div class="resumes">'
    + resume('LUCIAN', 2, 'UNSELFISH · RELENTLESS · SUFFOCATING', '13 – 2', '2 – 0 · Titles: 2', '2 – 2', '87%', [('cavs16', 4), ('mavs19', 4), ('cavs0607', 3)])
    + resume('JOSIAH', 0, 'BIG-CENTRIC · RESILIENT · FADING', '2 – 13', '0 – 2 · Titles: 0', '2 – 2', '13%', [('spurs98', 4), ('clippers14', 4), ('rockets19', 4)])
    + '</div>')

# One CSS class per asset — each PNG inlined exactly once (see header note).
LOGO_CSS = '\n'.join(
    [f'.logo-{k}{{background-image:url("assets/{v[1]}")}}' for k, v in TEAMS.items()]
    + ['.logo-trophy{background-image:url("assets/trophy.png")}'])

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fff;color:#111;font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;-webkit-text-size-adjust:100%}
.wrap{max-width:880px;margin:0 auto;padding:20px 16px 40px}
header{text-align:center;border-bottom:3px double #111;padding-bottom:10px;margin-bottom:14px}
header h1{font-family:Georgia,'Times New Roman',serif;font-size:34px;letter-spacing:1px}
header .sub{font-size:12px;letter-spacing:2.5px;color:#444;margin-top:4px;text-transform:uppercase}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
__LOGOS__
.chip{display:inline-block;width:38px;height:38px;border:2px solid #999;background-color:#fff;background-size:contain;background-repeat:no-repeat;background-position:center;flex:none}
.mtrophy{display:block;width:27px;height:52px;background-size:contain;background-repeat:no-repeat;background-position:center}
.mini-trophy{display:inline-block;width:11px;height:22px;background-size:contain;background-repeat:no-repeat;background-position:center}
.resumes{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px}
.resume{border:1px solid #111;padding:12px 14px}
.rname{display:flex;align-items:center;gap:8px;height:34px;border-bottom:1px solid #ddd;margin-bottom:8px}
.rname h2{font-family:Georgia,serif;font-size:22px;letter-spacing:1px}
.trophies{display:inline-flex;gap:3px;align-items:center}
.rrow{display:grid;grid-template-columns:86px 1fr;align-items:center;min-height:30px;border-bottom:1px solid #eee;font-size:14px}
.rrow:last-child{border-bottom:none}
.rrow.mu{min-height:46px;align-items:start;padding-top:5px}
.rlab{color:#595959;font-size:11px;letter-spacing:1.2px;text-transform:uppercase}
.rval{font-weight:600;font-size:13.5px;display:flex;align-items:center;gap:5px;flex-wrap:wrap}
.pstyle{font-variant:small-caps;letter-spacing:1.2px;font-size:13px;line-height:1.35}
.rval .chip{width:26px;height:26px}
nav.tabs{display:flex;border-bottom:2px solid #111;position:sticky;top:0;background:#fff;z-index:5}
nav.tabs button{flex:1;background:none;border:none;border-right:1px solid #ddd;padding:12px 4px;font-size:14px;font-weight:700;letter-spacing:.5px;cursor:pointer;min-height:48px;color:#111;font-family:inherit}
nav.tabs button:last-child{border-right:none}
nav.tabs button[aria-selected="true"]{box-shadow:inset 0 -4px 0 #c8102e}
nav.tabs button:focus-visible{outline:3px solid #005fcc;outline-offset:-3px}
.panel{padding-top:14px}
html.js .panel{display:none}
html.js .panel.active{display:block}
.panel:focus-visible{outline:3px solid #005fcc;outline-offset:2px}
.strip{display:grid;grid-template-columns:repeat(5,1fr);border:1px solid #ddd;margin-bottom:14px}
.strip .cell{padding:7px 10px;border-right:1px solid #eee;display:flex;flex-direction:column}
.strip .cell:last-child{border-right:none}
.clab{font-size:11px;letter-spacing:1.5px;color:#595959;text-transform:uppercase}
.cval{font-size:14px;font-weight:700}
.headline{font-family:Georgia,serif;font-size:30px;line-height:1.15;margin:4px 0 12px}
.mbox{display:flex;align-items:center;justify-content:space-between;gap:10px;border:1px solid #111;padding:12px 14px;margin-bottom:14px}
.mside{display:flex;flex-direction:column;align-items:center;gap:6px;font-weight:700;font-size:14px;min-width:86px;text-align:center}
.mcenter{display:flex;flex-direction:column;align-items:center;gap:2px;text-align:center}
.mcenter.solo{margin:0 auto}
.mct{font-size:11px;letter-spacing:1.5px;color:#595959;text-transform:uppercase}
.mcb{font-weight:800;font-size:15px}
.results{border-top:1px solid #111}
.row{display:grid;grid-template-columns:34px 1fr auto 1fr;align-items:center;gap:8px;padding:7px 2px;border-bottom:1px solid #e5e5e5;min-height:52px}
.glabel{font-weight:800;font-size:13px;color:#444}
.team{display:flex;align-items:center;gap:8px;min-width:0}
.team:last-child{justify-content:flex-end;text-align:right}
.team:last-child .tmeta{align-items:flex-end}
.tmeta{display:flex;flex-direction:column;min-width:0}
.tname{font-weight:600;font-size:14px;white-space:nowrap}
.team.winner .tname{font-weight:800}
.tcap{font-size:11px;color:#595959;white-space:nowrap}
.star{color:#8a6508}
.vs{font-size:12px;color:#595959;font-style:italic;text-align:center}
.row.muted{background:#fafafa}
.row.muted .tname,.row.muted .glabel{color:#595959}
details.wirebox,details.unplayed{margin-top:16px;border:1px solid #ddd}
details.unplayed .results{border-top:1px solid #eee}
summary{cursor:pointer;min-height:48px;display:flex;align-items:center;gap:9px;padding:10px 14px;font-size:12px;font-weight:700;color:#111;list-style:none}
summary::-webkit-details-marker{display:none}
summary::before{content:"";flex:none;width:0;height:0;border-left:7px solid #111;border-top:4.5px solid transparent;border-bottom:4.5px solid transparent}
details[open ]>summary::before{transform:rotate(90deg)}
summary:focus-visible{outline:3px solid #005fcc;outline-offset:-3px}
.sumlab{letter-spacing:1.5px}
.sumreason{letter-spacing:0}
.wire{padding:2px 14px 10px}
.wline{font-family:Georgia,serif;font-weight:700;font-size:15px;padding:5px 0;border-bottom:1px solid #f0f0f0}
.wline:last-child{border-bottom:none}
footer{margin-top:22px;border-top:1px solid #ddd;padding-top:8px;font-size:11px;color:#595959;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
@media (max-width:640px){
  header h1{font-size:27px}
  .headline{font-size:24px}
  .resumes{gap:10px}
  .resume{padding:9px 10px}
  .rname{height:32px}
  .rname h2{font-size:19px}
  .rrow{grid-template-columns:57px 1fr;min-height:32px}
  .rrow.ps{min-height:64px}
  .rrow.mu{min-height:168px}
  .rlab{letter-spacing:0;text-transform:none}
  .rval{font-size:12.5px}
  nav.tabs button{font-size:12px;padding:10px 2px}
  .strip{grid-template-columns:repeat(3,1fr)}
  .strip .cell{border-bottom:1px solid #eee}
  .strip .cell:nth-child(3n){border-right:none}
  .row{grid-template-columns:26px 1fr auto 1fr;gap:5px}
  .tname{font-size:13px;white-space:normal}
  .tcap{white-space:normal}
  .vs{max-width:104px;white-space:normal}
  .chip{width:32px;height:32px}
  .mside{min-width:64px;font-size:13px}
}
@media (prefers-reduced-motion: reduce){*,*::before,*::after{transition:none!important;animation:none!important;scroll-behavior:auto!important}}
""".replace('__LOGOS__', LOGO_CSS)

JS = """
(function(){
var tabs=Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
function activate(tab,focus){
  tabs.forEach(function(t){
    var on=(t===tab);
    t.setAttribute('aria-selected',on?'true':'false');
    t.tabIndex=on?0:-1;
    document.getElementById(t.getAttribute('aria-controls')).classList.toggle('active',on);
  });
  if(focus)tab.focus();
}
tabs.forEach(function(t,i){
  t.addEventListener('click',function(){activate(t,false);});
  t.addEventListener('keydown',function(e){
    var j=null;
    if(e.key==='ArrowRight')j=(i+1)%tabs.length;
    else if(e.key==='ArrowLeft')j=(i-1+tabs.length)%tabs.length;
    else if(e.key==='Home')j=0;
    else if(e.key==='End')j=tabs.length-1;
    if(j!==null){e.preventDefault();activate(tabs[j],true);}
  });
});
})();
"""

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>2K Archive — Lucian vs Josiah</title>
<script>document.documentElement.classList.add('js');</script>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header><h1>2K ARCHIVE</h1><div class="sub">Lucian vs Josiah · NBA 2K Head-to-Head Record</div></header>
{resumes}
<nav class="tabs" role="tablist" aria-label="Archive sections">
<button role="tab" id="tab-rounds" aria-controls="rounds" aria-selected="true">The Rounds</button>
<button role="tab" id="tab-finals1" aria-controls="finals1" aria-selected="false" tabindex="-1">Finals 1</button>
<button role="tab" id="tab-finals2" aria-controls="finals2" aria-selected="false" tabindex="-1">Finals 2</button>
<button role="tab" id="tab-series3" aria-controls="series3" aria-selected="false" tabindex="-1">Finals 3</button>
</nav>
<section class="panel active" id="rounds" role="tabpanel" aria-labelledby="tab-rounds" tabindex="0">{rounds}</section>
<section class="panel" id="finals1" role="tabpanel" aria-labelledby="tab-finals1" tabindex="0">{finals1}</section>
<section class="panel" id="finals2" role="tabpanel" aria-labelledby="tab-finals2" tabindex="0">{finals2}</section>
<section class="panel" id="series3" role="tabpanel" aria-labelledby="tab-series3" tabindex="0">{series3}</section>
<footer><span>Read-only archive — the live tracker is where games are recorded.</span><span>Logos: SportsLogoHistory.com · Lucian's reference files</span></footer>
</div>
<script>{JS}</script>
</body>
</html>"""

# Inline each logo asset exactly ONCE as a data URI inside its CSS class ->
# single self-contained UTF-8 index.html (GitHub connector snapshot pushes
# accept UTF-8 text only, no binaries). No asset bytes are duplicated.
import base64, os
for fn in sorted(os.listdir('assets')):
    with open(f'assets/{fn}', 'rb') as fh:
        uri = 'data:image/png;base64,' + base64.b64encode(fh.read()).decode()
    page = page.replace(f'url("assets/{fn}")', f'url("{uri}")')
assert 'assets/' not in page, 'uninlined asset remains'

with open('index.html', 'w') as f:
    f.write(page)
print('index.html bytes:', len(page))
