#!/usr/bin/env python3
"""Builds index.html for pittner/dream-home-vision-board.

A single-purpose page for the "dream home vision board" / "home goals 2027" search intent (home plans
are made in December and January): 36 home goals in 6 groups (dream home, declutter and organise,
renovate and fix, cozy and beautiful, garden and outdoors, home money and calm), each with why it
matters and a first step; one click opens the free maker prefilled as a phone lock screen. Plus 12
questions, a 45-minute plan, a box for your own goal, and FAQ.
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/dream-home-vision-board/"
SRC = "ghpages_home"
CAMPAIGN = "home_2027"

# (group, [(goal, why it matters, a first step for this week)])
GROUPS = [
    ("Dream home", [
        ("Buy my first home", "A home you own is a plan with a number and a date, not a wish.", "Write the price range, the area and the month you want to start viewing"),
        ("Move to a home with more light", "Light changes your mood every single morning.", "List the three things your next home must have and the one you will not accept"),
        ("Find a place closer to what matters", "Less time commuting is more time for the people and things you love.", "Measure your weekly commute in hours and write the number down"),
        ("Rent a home I actually love", "Renting does not mean living in a place that drains you.", "Save one search with your must-haves on a rental site today"),
        ("Know exactly what my dream home looks like", "A clear picture makes every decision faster, from viewings to paint.", "Collect five photos of rooms you love and look for what they share"),
        ("Make this home feel like mine", "You do not have to move to feel at home; you have to make it yours.", "Pick the one room that feels least like you and write why"),
    ]),
    ("Declutter and organise", [
        ("Declutter one room per month", "Twelve rooms in a year is a calmer house without a crazy weekend.", "Choose the January room and put it in your calendar"),
        ("Own fewer, better things", "Every thing you keep is a thing you clean, store and move.", "Fill one bag with things you have not used in a year"),
        ("Have a place for everything", "Searching for keys and chargers is a small daily stress you can delete.", "Pick the three things you lose most and give each a fixed spot"),
        ("Clear the paper pile for good", "Paper chaos hides bills, deadlines and money you are owed.", "Set up one box for incoming paper and sort it every Sunday"),
        ("Keep the kitchen counter clear", "A clear counter makes cooking feel easy instead of a chore.", "Remove everything you did not use this week from the counter"),
        ("Stop buying things I do not need", "The best decluttering is the stuff that never comes in.", "Wait 7 days before every non-food purchase this month"),
    ]),
    ("Renovate and fix", [
        ("Finish the one project I keep postponing", "An unfinished project quietly drains you every time you walk past it.", "Write the next physical step and the date you will do it"),
        ("Renovate the kitchen or bathroom", "These two rooms change how the whole home feels and what it is worth.", "Get one quote or price list so the project has a real number"),
        ("Paint a room", "Paint is the cheapest big change you can make in a weekend.", "Buy three sample pots and test them on the wall"),
        ("Learn to fix small things myself", "A drill and a few videos save money and waiting for help.", "Fix one small thing this week: a hinge, a tap, a loose handle"),
        ("Make the home more energy efficient", "Lower bills every month and a warmer home in winter.", "Check where the draughts are and seal one window or door"),
        ("Make a home maintenance calendar", "Small checks every season prevent the big, expensive repairs.", "List four seasonal jobs, one per quarter, and add them to your calendar"),
    ]),
    ("Cozy and beautiful", [
        ("Create a reading corner", "A spot made for slowing down invites you to actually slow down.", "Choose the corner and move one chair and one lamp there"),
        ("Make the bedroom a calm place", "Better sleep starts with a room that only means rest.", "Take work, laundry and screens out of the bedroom for one week"),
        ("Bring plants into every room", "Living things make a home feel alive and cared for.", "Buy one easy plant for the room you spend most time in"),
        ("Hang art and photos I love", "Walls with your story make a house feel like your home.", "Print three photos from 2026 and choose where they go"),
        ("Light the home warmly in the evening", "Warm lamps instead of a ceiling light change the whole evening.", "Replace one cold bulb with a warm one tonight"),
        ("Make one room guest-ready", "A home where friends can stay is a home people come back to.", "Make a list of what a guest would need and buy the first missing thing"),
    ]),
    ("Garden and outdoors", [
        ("Grow some of my own food", "Even herbs on a windowsill change how you cook.", "Buy one pot of basil or seeds for something you eat every week"),
        ("Make the balcony a place I use", "A small outdoor space is a free extra room for half the year.", "Clear it and add one comfortable seat"),
        ("Plant a garden that blooms all year", "Something in flower every month gives you a reason to step outside.", "Note which months your garden looks empty now"),
        ("Eat outside more often", "A meal outside feels like a small holiday at home.", "Plan the first outdoor breakfast for the next sunny weekend"),
        ("Start composting", "Less waste out, better soil in.", "Find out where your food scraps can go and set up one container"),
        ("Make the entrance welcoming", "The first thing you see when you come home sets the mood.", "Clean the door area and add one plant or a new mat"),
    ]),
    ("Home money and calm", [
        ("Save for a home deposit", "A deposit is the gate to buying, and it only grows if you feed it.", "Open a separate deposit pot and set an automatic monthly amount"),
        ("Pay off what I owe on the home faster", "Every extra payment is interest you never pay.", "Check what a small extra monthly payment would save"),
        ("Cut the monthly home bills", "Energy, internet and insurance often cost more than they need to.", "Compare one bill with two other providers this week"),
        ("Have an emergency fund for repairs", "A broken boiler is a problem, not a crisis, when the money is there.", "Set a target of one month of housing costs and start with a first amount"),
        ("Share home chores fairly", "A home feels calmer when one person is not carrying everything.", "Write all weekly chores on one list and decide together who does what"),
        ("Make Sunday reset a habit", "Thirty minutes on Sunday makes the whole week feel lighter.", "Pick a 30-minute Sunday slot and set a repeating reminder"),
    ]),
]

QUESTIONS = [
    "Which room in my home made me happiest in 2026, and why?",
    "Which room do I avoid or feel stressed in?",
    "What do I tolerate at home that I could fix in a weekend?",
    "Do I want to move in 2027, or make this place better?",
    "What does home need to give me: calm, space, light or people?",
    "Which unfinished project do I walk past every day?",
    "How much did my home cost me per month in 2026, all in?",
    "What would I get rid of if I moved tomorrow?",
    "Who do I want to welcome into my home more often?",
    "Which home chore causes the most tension, and with whom?",
    "What is one small change that would make every morning easier?",
    "If 2027 goes really well, what does my home look like by next December?",
]

PLAN = [
    ("10 minutes: walk through your home.", "Go room by room with your phone and note what gives you energy and what drains it."),
    ("15 minutes: answer the questions.", "Go through the 12 questions below. Short, honest answers are enough; nobody else reads them."),
    ("10 minutes: pick three home goals.", "Not ten. One big goal, one small fix and one thing that makes home cozier."),
    ("10 minutes: make it visible.", "Turn your main home goal and its first step into a phone lock screen, so you see it every day until it is done."),
]

FAQ = [
    ("What should go on a dream home vision board?",
     "Put the home goal in your own words, a first step you can do this week, and your reason why. "
     "This page has 36 home goals in 6 groups (dream home, declutter and organise, renovate and fix, cozy and beautiful, garden and outdoors, home money and calm), each with a first step, so you can pick three and make them visible."),
    ("Does a home vision board actually work?",
     "A board does not paint the walls by itself, but seeing the goal every day keeps it in front of you when you decide how to spend your weekends and money. "
     "The habit that works best is putting it on your phone lock screen."),
    ("How many home goals should I set for 2027?",
     "Three is enough: one big goal, one small fix and one thing that makes home cozier. Fewer goals get done more often."),
    ("How do I save for my dream home?",
     "Know the real number (deposit, fees, moving), divide it by the months left and save that amount automatically every payday, before you spend on anything else."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to your phone lock screen or print it."),
    ("Can I make a full home vision board with all my goals?",
     "Yes. Start from your goals in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dream Home Vision Board 2027: %%COUNT%% Home Goals with a First Step + Free Lock Screen</title>
<meta name="description" content="%%COUNT%% home goals for 2027 (dream home, declutter and organise, renovate and fix, cozy and beautiful, garden, home money and calm), each with a first step for this week, %%NQ%% questions and a 45-minute plan. Free lock screen maker.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Dream home vision board 2027 - %%COUNT%% home goals with a first step and a free lock screen">
<meta property="og:description" content="Buying, decluttering, renovating and cozy home goals with a first step, %%NQ%% questions, and a lock screen in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Dream home vision board 2027: %%COUNT%% home goals with a first step for this week</h1>
  <p class="lede">Most home plans stay on Pinterest because there is no date, no budget and no first step. Below are %%COUNT%% home goals for 2027, from buying your first home to a calm bedroom and a clear kitchen counter, each with why it matters and a first step you can do this week, plus %%NQ%% questions to find out what your home really needs. Press a goal and it opens in a free maker with the first step under it: save it as your phone lock screen and see it every day until it is done.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% questions &middot; 45-minute plan &middot; lock screen in one click &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your goal?</h2>
  <div class="row">
    <div><label for="ownGoal">My home goal for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. Finish the bathroom by summer" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Get one quote this week" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to your phone or print it.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% questions before you choose your home goals</h2>
  <p>Answer them alone, with a notebook, in 15 minutes. Be honest, nobody else reads it. The answers that surprise you point to the goals that will actually stick.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Plan your home year in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with all my goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full dream home vision board</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/travel-vision-board/">travel vision board</a>,
  <a href="https://pittner.github.io/self-care-vision-board/">self care vision board</a>,
  <a href="https://pittner.github.io/money-vision-board/">money vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-weight-loss/">weight loss vision board</a>,
  <a href="https://pittner.github.io/new-year-resolutions-2027/">new year's resolutions 2027</a>,
  <a href="https://pittner.github.io/vision-board-for-career/">career vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-small-business/">small business vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/dream-home-vision-board">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
