"""Generates the static HTML site. Edit content here, run `python3 build.py`."""
import html, os

ORIGIN = "https://hiremeholidayparks.com.au"
IMG = ORIGIN + "/templates/hmhp/assets/images/xtr"
LOGO = ORIGIN + "/templates/hmhp/assets/images/logo.png"
HERO = IMG + "/hero-image1.jpg"
SLIDES = [IMG + f"/slide{i}.jpg" for i in range(1, 10)]
E = html.escape

NAV = [("Home", "index.html"), ("Find a Job", "jobs.html"), ("Job Seekers", "job-seekers.html"),
       ("Employers", "employers.html"), ("Services", "services.html"), ("Resources", "resources.html"),
       ("About", "about.html"), ("Contact", "contact.html")]

STATS = [("Job seekers", "3,261"), ("Employers", "784"), ("Resumes listed", "54"), ("Jobs open now", "2")]
PRICE = {"job": "$99", "job_days": 30, "resume": "$29", "resume_days": 90}

STATES = [("NSW", "New South Wales", 2), ("VIC", "Victoria", 1), ("QLD", "Queensland", 0), ("WA", "Western Australia", 0),
          ("SA", "South Australia", 0), ("TAS", "Tasmania", 0), ("NT", "Northern Territory", 0), ("ACT", "Australian Capital Territory", 0)]
STATE_NAME = {c: n for c, n, _ in STATES}
TOWNS = ["Shepparton", "Central West NSW", "Lake Macquarie", "Gold Coast", "Sunshine Coast", "Great Ocean Road"]

CATEGORIES = [("Park Manager", "key-round", 2), ("Operations Manager", "briefcase", 1), ("Management Couple", "heart-handshake", 1),
              ("Reception & Guest Services", "users", 1), ("Housekeeping & Cleaning", "bed-double", 0),
              ("Maintenance & Trades", "wrench", 1), ("Grounds & Gardens", "trees", 0), ("Café, Kiosk & Hospitality", "coffee", 0)]
TYPES = ["Full time", "Part time", "Casual", "Live-in couple", "Tender"]
BADGE = {"Full time": "badge-brand", "Part time": "badge-brand", "Casual": "badge-neutral", "Live-in couple": "badge-accent", "Tender": "badge-accent"}

# id, title, employer, location, state, type, category, posted, featured, summary, sample
JOBS = [
    dict(id="5062", title="Holiday Park Management Services — Tender Opportunity", employer="Lake Macquarie", location="Belmont & Belmont South", state="NSW", type="Tender", category="Park Manager", posted="Recently", featured=True,
         summary="Tenders are open to provide holiday park management services at two lakeside parks in Belmont and Belmont South.", sample=False),
    dict(id="4147", title="Riverview & Lakeview Caravan Parks — Long-Term Lease or Management Contract", employer="Riverview & Lakeview Caravan Parks", location="Central West", state="NSW", type="Tender", category="Operations Manager", posted="Recently", featured=True,
         summary="Tenders for a long-term lease or management contract across two regional caravan parks in Central West NSW.", sample=False),
    dict(id="s1", title="Assistant Park Manager", employer="Sample listing", location="Shepparton", state="VIC", type="Full time", category="Park Manager", posted="3 days ago", featured=False,
         summary="Support the park manager with daily operations, staff rosters and guest experience at a busy family park.", sample=True),
    dict(id="s2", title="Guest Services & Reception", employer="Sample listing", location="Hervey Bay", state="QLD", type="Casual", category="Reception & Guest Services", posted="4 days ago", featured=False,
         summary="Welcome guests, manage bookings and share local knowledge at a coastal holiday park.", sample=True),
    dict(id="s3", title="Management Couple (live-in)", employer="Sample listing", location="Murray River", state="SA", type="Live-in couple", category="Management Couple", posted="5 days ago", featured=False,
         summary="Run a riverside caravan park together, with on-site accommodation included.", sample=True),
    dict(id="s4", title="Maintenance & Grounds Person", employer="Sample listing", location="Busselton", state="WA", type="Full time", category="Maintenance & Trades", posted="1 week ago", featured=False,
         summary="Keep cabins, amenities and grounds in top shape at a beachfront park.", sample=True),
]

SERVICES = [
    dict(slug="business-plan-development", title="Business plan development", icon="line-chart",
         short="Plans that give owners, lenders and managers a clear path for growth.",
         intro="A clear, realistic business plan helps you secure finance, set priorities and measure progress. We build plans around how holiday parks actually operate.",
         inc=["Review of current trading, occupancy and revenue mix", "Market and competitor overview for your region", "Pricing, product and accommodation mix recommendations", "Financial projections and capital works priorities", "An action plan your team can follow"],
         who="Park owners, prospective buyers, councils and lessees preparing for finance, a sale or a new tender."),
    dict(slug="park-management-support", title="Park management support", icon="clipboard-check",
         short="Hands-on help with operations, staffing and the guest experience.",
         intro="Whether you're between managers, growing quickly or want a fresh set of eyes, we can support your team on the ground or remotely.",
         inc=["Interim and relief management", "Operational reviews and procedures", "Staff structure, rostering and recruitment support", "Guest experience and reputation improvements", "Systems and reporting set-up"],
         who="Owners and operators who need experienced management support for a period, or ongoing."),
    dict(slug="industry-training", title="Industry training", icon="graduation-cap",
         short="Practical training for front office, management and park teams.",
         intro="Training designed for the realities of park work, from the front desk to the management office.",
         inc=["Front office and guest service training", "Reservations and revenue basics", "Supervisor and new manager development", "Induction programs for seasonal staff", "On-site or online delivery"],
         who="Park teams, new managers and anyone moving into the industry."),
    dict(slug="park-planning-development", title="Park planning & development", icon="map",
         short="Site layouts, expansions and new builds, planned by people who run parks.",
         intro="Good planning makes a park easier to run and more enjoyable to stay in. We help you get the layout and product right before you build.",
         inc=["Site master planning and layout reviews", "Accommodation and facility mix", "Expansion and redevelopment staging", "Feasibility input for new parks", "Working alongside your architects and planners"],
         who="Owners, developers and councils planning new parks, expansions or redevelopments."),
    dict(slug="park-whs-audits", title="Park and WHS audits", icon="shield-check",
         short="Independent audits that keep guests, staff and your business safe.",
         intro="An independent audit shows you where you stand and what to fix first, in plain language.",
         inc=["Work health and safety audits", "Park operations and compliance reviews", "Risk registers and prioritised action lists", "Policy and procedure reviews", "Follow-up reviews to track progress"],
         who="Owners, operators and councils wanting confidence in safety and compliance."),
]

RESOURCES = [
    dict(slug="career-advice", title="Career advice", icon="lightbulb", who="Job seekers",
         short="Where a holiday park career can take you, and how to get started.",
         body=[("h2", "Why work in holiday parks?"),
               ("p", "Holiday parks are some of the most varied workplaces in Australian tourism. In a single week you might check in guests, solve a maintenance problem, help plan a school holiday program and handle the books."),
               ("p", "Many roles come with on-site accommodation, and parks are found everywhere from capital-city fringes to remote coastlines — so a park career can also be a lifestyle change."),
               ("h2", "Common career paths"),
               ("ul", ["<strong>Guest services and reception</strong> — a great entry point that teaches you how the whole park runs.",
                       "<strong>Housekeeping, maintenance and grounds</strong> — practical roles that are always in demand.",
                       "<strong>Supervisor and assistant manager</strong> — the step between team member and management.",
                       "<strong>Park manager and management couples</strong> — running the business day to day, often as a live-in role.",
                       "<strong>Operations, area and group roles</strong> — overseeing several parks for a group or brand."]),
               ("h2", "Getting started"),
               ("ol", ["Post your resume so hiring parks can find you.", "Set up job alerts for the categories and regions you're interested in.", "Consider seasonal or casual work to build experience quickly.", "Look into industry training for reservations, front office or management."]),
               ("callout", "Tip: parks value reliability and a friendly attitude as much as experience. Say so, with examples, in your resume.")]),
    dict(slug="tips-job-seekers", title="Tips for job seekers", icon="user-round-search", who="Job seekers",
         short="Write a resume park owners notice, and prepare for the interview.",
         body=[("h2", "Make your resume park-ready"),
               ("ul", ["Lead with a short summary: the role you want, where you're willing to work and when you're available.", "List hands-on skills — reservations systems, trades, cleaning standards, first aid, forklift or chemical handling.", "Mention if you're a couple applying together, and what each of you brings.", "Keep it to two pages and use plain formatting."]),
               ("h2", "Before the interview"),
               ("ul", ["Look up the park: its size, accommodation types and guest reviews.", "Prepare examples of handling a difficult guest or a busy period.", "Ask about accommodation, rosters, peak seasons and pets if relevant."]),
               ("h2", "After you apply"),
               ("p", "Follow up politely after a week if you haven't heard back. Keep your resume listing current so parks see you're still available.")]),
    dict(slug="tips-employers", title="Tips for employers", icon="hammer", who="Employers",
         short="Write clear listings and find people who stay for the season and beyond.",
         body=[("h2", "Write a listing that attracts the right people"),
               ("ul", ["Use a clear job title people search for, such as 'Park Manager' or 'Reception'.", "Say where the park is and what the area is like.", "Be upfront about hours, rosters, peak seasons and accommodation.", "Describe the team and what a normal week looks like."]),
               ("h2", "Search resumes, don't just wait"),
               ("p", "Job seekers list their resumes on the site. Search by category and location and contact good candidates directly."),
               ("h2", "Keep the people you hire"),
               ("ul", ["Give new staff a proper induction, even for casual roles.", "Check in after the first two weeks.", "Offer training and a path to more responsibility."])]),
    dict(slug="industry-contacts", title="Industry contacts", icon="phone", who="Everyone",
         short="Associations and networks across the Australian park industry.",
         body=[("p", "The holiday park industry is supported by state associations, park groups and brands, suppliers and industry media. Getting to know them is one of the best ways to build your network."),
               ("h2", "Our supporters"),
               ("ul", ['<a href="https://www.atpm.com.au" rel="noopener">ATPM</a>', '<a href="https://www.freespiritresorts.com.au" rel="noopener">FreeSpirit Resort &amp; Holiday Park Management</a>', '<a href="https://www.goseeaustralia.com.au" rel="noopener">Go See Australia</a>', '<a href="https://www.topparks.com.au" rel="noopener">Top Parks</a>', '<a href="https://www.familyparks.com.au" rel="noopener">Family Parks</a>', '<a href="https://www.accomnews.com.au" rel="noopener">Accom News</a>', '<a href="https://www.tubal.com.au" rel="noopener">Tubal</a>', '<a href="https://www.big4.com.au" rel="noopener">BIG4 Holiday Parks</a>']),
               ("callout", "Know an organisation that should be listed here? Get in touch through our contact page.")]),
    dict(slug="tips-site", title="Tips for using our site", icon="book-open", who="Everyone",
         short="Create alerts, manage listings and get the most from your account.",
         body=[("h2", "Job seekers"),
               ("ol", ["Register a free account and choose 'Job seeker'.", f"Post your resume — a {PRICE['resume_days']}-day listing is {PRICE['resume']}.", "Set up job alerts from the home page or the Find a Job page."]),
               ("h2", "Employers"),
               ("ol", ["Register and choose 'Employer'.", f"Post a job — a {PRICE['job_days']}-day listing is {PRICE['job']}.", "Search resumes and contact candidates directly."]),
               ("h2", "Managing your account"),
               ("p", "Sign in to edit or renew listings, update your details and manage alerts. You can unsubscribe from alerts at any time from the link in each email.")]),
]

SUPPORTERS = [("ATPM", "atpm.png", "https://www.atpm.com.au"), ("FreeSpirit Resort & Holiday Park Management", "fshpm.jpg", "https://www.freespiritresorts.com.au"),
              ("Go See Australia", "gsa.svg", "https://www.goseeaustralia.com.au"), ("Top Parks", "topparks.png", "https://www.topparks.com.au"),
              ("Family Parks", "fp.png", "https://www.familyparks.com.au"), ("Accom News", "accomnews.png", "https://www.accomnews.com.au"),
              ("Tubal", "tubal.png", "https://www.tubal.com.au"), ("BIG4 Holiday Parks", "big4.png", "https://www.big4.com.au")]
SOCIAL = [("Facebook", "https://www.facebook.com/hiremeholidayparks"), ("LinkedIn", "http://www.linkedin.com/company/hire-me-holiday-parks"), ("X (Twitter)", "https://twitter.com/HireMeHolidayPa")]

def ico(name, cls=""):
    return f'<i data-lucide="{name}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} aria-hidden="true"></i>'

def job_url(j): return f"job-{j['id']}.html"

# ---------------------------------------------------------------- shell
def header(active):
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if l == active else ""}>{l}</a></li>' for l, h in NAV)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar"><div class="container"><p>{PRICE['job_days']}-day job listing {PRICE['job']} · {PRICE['resume_days']}-day resume listing {PRICE['resume']}<a href="resources-tips-site.html">How it works</a></p></div></div>
<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="index.html" aria-label="Hire Me Holiday Parks home"><img src="{LOGO}" alt="Hire Me Holiday Parks"></a>
    <nav class="main-nav" aria-label="Main"><ul>{links}</ul></nav>
    <div class="header-actions">
      <a class="login" href="login.html">Login</a>
      <a class="btn btn-secondary btn-sm" href="register.html">Register</a>
      <a class="btn btn-accent btn-sm" href="post-job.html">Post a Job</a>
    </div>
    <div class="header-mobile">
      <a class="btn btn-accent btn-sm" href="post-job.html">Post a Job</a>
      <button class="icon-btn" type="button" data-drawer-open aria-label="Open menu" aria-controls="mobile-menu" aria-expanded="false">{ico("menu")}</button>
    </div>
  </div>
</header>
<div class="drawer" id="mobile-menu" aria-hidden="true">
  <div class="drawer-backdrop" data-drawer-close></div>
  <div class="drawer-panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="drawer-head"><img src="{LOGO}" alt="Hire Me Holiday Parks"><button class="icon-btn" type="button" data-drawer-close aria-label="Close menu">{ico("x")}</button></div>
    <nav aria-label="Mobile"><ul>{links}</ul></nav>
    <div class="drawer-foot">
      <a class="btn btn-accent btn-lg btn-block" href="post-job.html">Post a Job</a>
      <div class="pair"><a class="btn btn-secondary" href="login.html">Login</a><a class="btn btn-secondary" href="register.html">Register</a></div>
    </div>
  </div>
</div>'''

def footer():
    cols = [("Job seekers", [("Find jobs", "jobs.html"), ("Post your resume", "post-resume.html"), ("Career advice", "resources-career-advice.html"), ("Sign in", "login.html")]),
            ("Employers", [("Post a job", "post-job.html"), ("Search resumes", "employers.html#resumes"), ("Tips for employers", "resources-tips-employers.html"), ("Sign in", "login.html")]),
            ("Services", [(s["title"], f"service-{s['slug']}.html") for s in SERVICES]),
            ("Company", [("About us", "about.html"), ("Contact us", "contact.html"), ("Terms & conditions", ORIGIN + "/terms-of-use/")])]
    colhtml = "".join(f'<div><h3>{t}</h3><ul>{"".join(f"<li><a href={chr(34)}{h}{chr(34)}>{E(l)}</a></li>" for l, h in items)}</ul></div>' for t, items in cols)
    soc = "".join(f'<li><a href="{h}" target="_blank" rel="noopener">{n}</a></li>' for n, h in SOCIAL)
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand"><span class="logo-plate"><img src="{LOGO}" alt="Hire Me Holiday Parks"></span>
        <p>Connecting great people with fantastic job opportunities to build a stronger, more professional industry.</p></div>
      {colhtml}
    </div>
    <div class="footer-bottom"><p>© 2014–<span data-year>2026</span> Hire Me Holiday Parks. All rights reserved.</p><ul>{soc}</ul></div>
  </div>
</footer>'''

def page(filename, title, desc, active, body, bare_footer=False):
    doc = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{"" if bare_footer else footer()}
<script src="assets/lucide.min.js"></script>
<script src="assets/main.js"></script>
</body>
</html>
'''
    with open(filename, "w") as f: f.write(doc)

# ---------------------------------------------------------------- partials
def crumbs(items):
    lis = "".join(f'<li><a href="{h}">{E(l)}</a></li>' if h else f'<li aria-current="page">{E(l)}</li>' for l, h in items)
    return f'<nav aria-label="Breadcrumb"><ol class="breadcrumb">{lis}</ol></nav>'

def page_hero(title, lead, trail, image=None, actions=""):
    if image:
        return f'''<section class="page-hero page-hero-media"><img src="{image}" alt=""><div class="container">{crumbs(trail)}<h1>{E(title)}</h1><p class="lead">{lead}</p>{actions}</div></section>'''
    return f'''<section class="page-hero"><div class="container">{crumbs(trail)}<h1>{E(title)}</h1><p class="lead">{lead}</p>{actions}</div></section>'''

def section_head(title, intro="", action=None, hid=""):
    a = f'<a class="text-link" href="{action[1]}">{action[0]} {ico("arrow-right")}</a>' if action else ""
    return f'<div class="section-head"><div><h2 id="{hid}">{E(title)}</h2>{f"<p>{intro}</p>" if intro else ""}</div>{a}</div>'

def search_panel(form_attr="data-job-search", with_ids="h"):
    cats = "".join(f'<option value="{E(c)}">{E(c)}</option>' for c, _, _ in CATEGORIES)
    states = "".join(f'<option value="{n}"></option>' for _, n, _ in STATES)
    return f'''<form class="search-panel" role="search" aria-label="Search jobs" {form_attr}>
  <div class="search-grid">
    <label class="field-wrap"><span class="sr-only">Keywords</span>{ico("search")}<input class="field" name="keywords" placeholder="Job title or keyword"></label>
    <label class="field-wrap"><span class="sr-only">Location</span>{ico("map-pin")}<input class="field" name="location" list="{with_ids}-locations" placeholder="Town, region or state"><datalist id="{with_ids}-locations">{states}</datalist></label>
    <label class="field-wrap"><span class="sr-only">Job category</span>{ico("layout-grid")}<select class="field" name="category"><option value="">All categories</option>{cats}</select>{ico("chevron-down", "chev")}</label>
    <button class="btn btn-primary btn-lg" type="submit">{ico("search")} Find Jobs</button>
  </div>
</form>'''

def job_card(j):
    return f'''<article class="job-card">
  <div class="job-card-top"><span class="featured-flag">{ico("star")} Featured</span><span class="badge {BADGE[j['type']]}">{j['type']}</span></div>
  <h3><a href="{job_url(j)}">{E(j['title'])}</a></h3>
  <p>{E(j['summary'])}</p>
  <div class="job-card-foot"><span class="meta">{ico("map-pin")} {E(j['location'])}, {j['state']}</span><span class="text-link">View job {ico("arrow-up-right")}</span></div>
</article>'''

def job_row(j):
    return f'''<li class="job-row" data-title="{E(j['title'])}" data-category="{E(j['category'])}" data-location="{E(j['location'])}" data-state="{j['state']}" data-state-name="{STATE_NAME[j['state']]}" data-type="{j['type']}">
  <div><h3><a href="{job_url(j)}">{E(j['title'])}</a></h3>
    <p class="metas muted"><span class="meta">{ico("map-pin")}{E(j['location'])}, {j['state']}</span><span class="meta">{ico("tag")}{E(j['category'])}</span></p></div>
  <div class="right"><span class="badge {BADGE[j['type']]}">{j['type']}</span><span class="posted">{j['posted']}</span>{ico("chevron-right", "chev")}</div>
</li>'''

def checklist(items):
    return '<ul class="checklist">' + "".join(f'<li><span class="tick">{ico("check")}</span><span>{i}</span></li>' for i in items) + "</ul>"

def alerts_section():
    return f'''<section class="section" aria-labelledby="alerts-title"><div class="container">
  <div class="alerts-box">
    <div>{ico("bell-ring")}<h2 id="alerts-title" class="h2-lg">Sign up for job alerts</h2><p class="lead">Get new holiday park jobs straight to your inbox. You can unsubscribe at any time.</p></div>
    <div>
      <form class="form" data-validate data-success="alert-done">
        <div><label class="label" for="alert-email">Email address</label>
          <span class="field-wrap">{ico("mail")}<input class="field" id="alert-email" type="email" name="email" autocomplete="email" placeholder="you@example.com" required data-label="Email address"></span></div>
        <fieldset><legend class="label">How often?</legend>
          <div class="segmented">
            <label><input type="radio" name="frequency" value="Daily"><span>Daily</span></label>
            <label><input type="radio" name="frequency" value="Weekly" checked><span>Weekly</span></label>
            <label><input type="radio" name="frequency" value="Monthly"><span>Monthly</span></label>
          </div></fieldset>
        <div><button class="btn btn-primary btn-lg" type="submit">Create alert</button></div>
      </form>
      <div class="success" id="alert-done" role="status" tabindex="-1" hidden>{ico("check-circle-2")}
        <div><p><strong>Alert created</strong></p><p class="soft mt-2">We'll email <span data-fill="frequency"></span> updates to <span data-fill="email"></span>. Check your inbox to confirm.</p></div></div>
    </div>
  </div>
</div></section>'''

def supporters_section():
    lis = "".join(f'<li><a href="{h}" target="_blank" rel="noopener" title="{E(n)}"><img src="{IMG}/{f}" alt="{E(n)}" loading="lazy"></a></li>' for n, f, h in SUPPORTERS)
    return f'<section class="supporters" aria-labelledby="sup-title"><div class="container"><h2 id="sup-title">Proudly supported by</h2><ul>{lis}</ul></div></section>'

def cta(title="Ready for your next season?", text="Find your place in the park industry, or find the people who'll make your park great.",
        a=("Find a Job", "jobs.html"), b=("Post a Job", "post-job.html")):
    return f'''<section class="cta-wrap" aria-labelledby="cta-title"><div class="container"><div class="cta-band">
  <div><h2 id="cta-title">{E(title)}</h2><p>{E(text)}</p></div>
  <div class="btn-row"><a class="btn btn-inverse btn-lg" href="{a[1]}">{a[0]}</a><a class="btn btn-outline-inverse btn-lg" href="{b[1]}">{b[0]}</a></div>
</div></div></section>'''

def service_list():
    return '<ul class="service-list">' + "".join(
        f'<li><a href="service-{s["slug"]}.html">{ico(s["icon"], "s-ico")}<span class="s-body"><strong>{E(s["title"])}</strong><span class="d">{E(s["short"])}</span></span>{ico("arrow-up-right", "arrow")}</a></li>'
        for s in SERVICES) + "</ul>"

def resources_block():
    lead, rest = RESOURCES[0], RESOURCES[1:]
    cards = "".join(f'<li><a class="res-card" href="resources-{r["slug"]}.html">{ico(r["icon"])}<p class="who">{r["who"]}</p><h3>{E(r["title"])}</h3><p class="d">{E(r["short"])}</p></a></li>' for r in rest)
    return f'''<div class="res-layout">
  <a class="res-lead" href="resources-{lead["slug"]}.html">{ico(lead["icon"])}<div><p class="who">{lead["who"]}</p><h3>{lead["title"]}</h3><p class="d">{lead["short"]}</p><p class="go">Read the guide</p></div></a>
  <ul class="res-grid">{cards}</ul>
</div>'''

def split(sid, title, lead, points, btns, image, reverse=False, note="", sand=False, heading="h2"):
    b = "".join(f'<a class="btn {cls} btn-lg" href="{h}">{l}</a>' for l, h, cls in btns)
    return f'''<section class="section{" section-sand" if sand else ""}" id="{sid}" aria-labelledby="{sid}-title"><div class="container">
  <div class="split{" reverse" if reverse else ""}">
    <div class="split-media"><img src="{image}" alt="" loading="lazy"></div>
    <div><{heading} id="{sid}-title" class="h2-lg">{E(title)}</{heading}><p class="lead">{lead}</p>{checklist(points)}<div class="btn-row">{b}</div>{f'<p class="price-note">{note}</p>' if note else ""}</div>
  </div>
</div></section>'''

def cat_grid():
    return '<ul class="cat-grid">' + "".join(
        f'<li><a class="cat-tile" href="jobs.html?category={E(c).replace(" ", "+").replace("&amp;", "%26")}"><span class="icon-chip">{ico(i)}</span><span><strong>{E(c)}</strong><span class="count">{"No open roles" if n == 0 else f"{n} open role" + ("s" if n > 1 else "")}</span></span></a></li>'
        for c, i, n in CATEGORIES) + "</ul>"

def state_grid():
    return '<ul class="state-grid">' + "".join(
        f'<li><a href="jobs.html?state={c}"><span><span class="code">{c}</span>{n}</span><span class="n">{k}</span></a></li>' for c, n, k in STATES) + "</ul>"

def faq(items):
    return '<div class="faq">' + "".join(f'<details><summary>{E(q)} {ico("plus")}</summary><p>{a}</p></details>' for q, a in items) + "</div>"

# ================================================================ PAGES
os.makedirs(".", exist_ok=True)

# ---- Home
stats = "".join(f"<div><dt>{l}</dt><dd>{v}</dd></div>" for l, v in STATS)
home = f'''
<section class="hero" aria-labelledby="hero-title">
  <div class="hero-media"><div class="container"><img class="hero-photo" src="{HERO}" alt="" fetchpriority="high"></div></div>
  <div class="container hero-search"><div class="hero-box">
    <h1 id="hero-title">Connecting great people with fantastic job opportunities to build a stronger, more professional industry.</h1>
    <p class="hero-sub">Holiday park, caravan park and resort jobs across Australia.</p>
    {search_panel()}</div></div>
</section>

<section class="stats" aria-label="Our community"><div class="container"><div class="stats-inner">
  <p>Our community of park owners, managers and people who love working where others holiday.</p><dl>{stats}</dl>
</div></div></section>

<section class="section" aria-labelledby="featured-title"><div class="container">
  {section_head("Featured jobs", "Management roles, tenders and positions highlighted by hiring parks.", ("View all jobs", "jobs.html"), "featured-title")}
  <div class="grid-2">{"".join(job_card(j) for j in JOBS if j["featured"])}</div>
</div></section>

<section class="section section-sand" aria-labelledby="latest-title"><div class="container">
  {section_head("Latest jobs", "The newest roles from parks around the country.", None, "latest-title")}
  <ul class="job-list">{"".join(job_row(j) for j in JOBS)}</ul>
  <div class="flex-center mt-8"><a class="btn btn-secondary" href="jobs.html">View all jobs</a></div>
</div></section>

<section class="section" aria-labelledby="cat-title"><div class="container">
  {section_head("Browse jobs by category", "From the front desk to the whole park — find the kind of work that suits you.", ("All categories", "jobs.html"), "cat-title")}
  {cat_grid()}
</div></section>

<section class="section section-sand" aria-labelledby="loc-title"><div class="container">
  {section_head("Browse jobs by location", "Coastal, country, river or outback — parks are hiring all over Australia.", None, "loc-title")}
  <div class="loc-layout">{state_grid()}
    <div><h3 class="h3-small">Popular towns and regions</h3>
      <ul class="chips">{"".join(f'<li><a class="chip" href="jobs.html?location={t.replace(" ", "+")}">{ico("map-pin")}{t}</a></li>' for t in TOWNS)}</ul>
      <p class="soft mt-6">Many roles include on-site accommodation — ideal for couples and people ready for a sea or tree change.</p></div>
  </div>
</div></section>

{split("job-seekers", "For job seekers", "Whether it's your first season or your next management role, find work with parks that value good people.",
       ["Roles only from holiday parks, caravan parks and resorts", "List your resume so parks can find you", "Job alerts for the categories and regions you choose"],
       [("Post your resume", "post-resume.html", "btn-primary"), ("Find a Job", "jobs.html", "btn-secondary")], SLIDES[1],
       note=f"<strong>{PRICE['resume']}</strong> for a {PRICE['resume_days']}-day resume listing")}
{split("employers", "For employers", "Reach an audience that already knows the industry — people looking for park work, not just any job.",
       ["Advertise to thousands of registered park job seekers", "Search resumes from people ready to start", "Advertise management contracts, leases and tenders"],
       [("Post a Job", "post-job.html", "btn-primary"), ("Search resumes", "employers.html#resumes", "btn-secondary")], SLIDES[3], reverse=True, sand=True,
       note=f"<strong>{PRICE['job']}</strong> for a {PRICE['job_days']}-day job listing")}

<section class="section" id="services" aria-labelledby="svc-title"><div class="container"><div class="services-layout">
  <div class="sticky"><h2 id="svc-title" class="h2-lg">Support beyond recruitment</h2>
    <p class="lead mt-4">Our team has run, planned and audited parks. We help owners and managers build stronger, more professional businesses.</p>
    <a class="btn btn-secondary mt-8" href="services.html">Explore our services</a></div>
  {service_list()}
</div></div></section>

<section class="section section-sand" id="resources" aria-labelledby="res-title"><div class="container">
  {section_head("Resources and advice", "Practical guides for building a career, or a team, in the park industry.", ("All resources", "resources.html"), "res-title")}
  {resources_block()}
</div></section>

{alerts_section()}
{supporters_section()}
{cta()}
'''
page("index.html", "Hire Me Holiday Parks — Holiday park jobs across Australia",
     "Connecting great people with fantastic job opportunities across Australia's holiday park industry.", "Home", home)

# ---- Jobs listing
type_checks = "".join(f'<div class="check"><label><input type="checkbox" name="type" value="{t}"> {t}</label></div>' for t in TYPES)
state_checks = "".join(f'<div class="check"><label><input type="checkbox" name="state" value="{c}"> {n}</label><span class="muted">{k}</span></div>' for c, n, k in STATES)
cats_opts = "".join(f'<option value="{E(c)}">{E(c)}</option>' for c, _, _ in CATEGORIES)
jobs_body = f'''
{page_hero("Find a job", "Holiday park, caravan park and resort roles across Australia.", [("Home", "index.html"), ("Find a Job", None)])}
<section class="section" style="padding-top:40px"><div class="container">
<form data-job-filter aria-label="Filter jobs">
  <div class="with-sidebar">
    <aside>
      <button class="btn btn-secondary btn-block filter-toggle" type="button" data-filter-toggle aria-controls="filters" aria-expanded="false">{ico("sliders-horizontal")} Filters</button>
      <div class="filters sidebar-sticky" id="filters"><div class="filter-card">
        <div class="filter-group"><h3>Search</h3>
          <div class="form" style="gap:12px">
            <label class="field-wrap"><span class="sr-only">Keywords</span>{ico("search")}<input class="field" name="keywords" placeholder="Keyword"></label>
            <label class="field-wrap"><span class="sr-only">Location</span>{ico("map-pin")}<input class="field" name="location" placeholder="Town or state"></label>
            <label class="field-wrap"><span class="sr-only">Category</span>{ico("layout-grid")}<select class="field" name="category"><option value="">All categories</option>{cats_opts}</select>{ico("chevron-down", "chev")}</label>
            <button class="btn btn-primary btn-block" type="submit">Update results</button>
          </div></div>
        <div class="filter-group"><h3>Job type</h3>{type_checks}</div>
        <div class="filter-group"><h3>State</h3>{state_checks}</div>
        <div class="filter-group"><button class="btn btn-secondary btn-sm btn-block" type="reset" data-reset>Clear filters</button></div>
      </div></div>
    </aside>
    <div>
      <div class="results-bar"><p><strong data-result-count>{len(JOBS)} jobs</strong> <span class="muted">found</span></p>
        <label class="field-wrap"><span class="sr-only">Sort by</span><select class="field"><option>Newest first</option><option>Featured first</option><option>Title A–Z</option></select>{ico("chevron-down", "chev")}</label></div>
      <ul class="job-list" data-job-results>{"".join(job_row(j) for j in JOBS)}</ul>
      <div class="empty" data-empty hidden>{ico("search-x")}<h2 class="h3-small">No jobs match these filters</h2><p class="soft mt-2">Try a wider location, fewer filters, or set up a job alert and we'll email you when a match is posted.</p></div>
      <nav class="pagination" aria-label="Pagination"><span aria-current="page">1</span><a href="#">2</a><a href="#" aria-label="Next page">{ico("chevron-right")}</a></nav>
    </div>
  </div>
</form>
</div></section>
{alerts_section()}
'''
page("jobs.html", "Find a job — Hire Me Holiday Parks", "Search holiday park, caravan park and resort jobs across Australia.", "Find a Job", jobs_body)

# ---- Job detail pages
for j in JOBS:
    similar = [x for x in JOBS if x["id"] != j["id"]][:3]
    sample_note = '<p class="callout">This is a sample listing to demonstrate the layout.</p>' if j["sample"] else ""
    body = f'''
<section class="page-hero"><div class="container">
  {crumbs([("Home", "index.html"), ("Find a Job", "jobs.html"), (j["title"], None)])}
  <div class="btn-row" style="gap:8px">{'<span class="featured-flag">' + ico("star") + ' Featured</span>' if j["featured"] else ""}<span class="badge {BADGE[j['type']]}">{j['type']}</span></div>
  <h1 class="mt-4" style="max-width:900px">{E(j['title'])}</h1>
  <div class="detail-meta"><span class="meta">{ico("building-2")}{E(j['employer'])}</span><span class="meta">{ico("map-pin")}{E(j['location'])}, {STATE_NAME[j['state']]}</span><span class="meta">{ico("tag")}{E(j['category'])}</span><span class="meta">{ico("clock")}Posted {j['posted'].lower()}</span></div>
</div></section>
<section class="section" style="padding-top:48px"><div class="container"><div class="with-sidebar side-right">
  <article class="prose">
    {sample_note}
    <h2 style="margin-top:0">About the opportunity</h2>
    <p>{E(j['summary'])}</p>
    <p>The full listing, including selection criteria and how to respond, is supplied by the employer. <!-- Replace with the listing body from the job board. --></p>
    <h2>What's involved</h2>
    <ul><li>Day-to-day operation of the park and its facilities</li><li>Guest experience, bookings and reporting</li><li>Working with the owner or council to meet agreed standards</li></ul>
    <h2>How to apply</h2>
    <p>Use the <strong>Apply now</strong> button to send your application and resume through Hire Me Holiday Parks. Make sure your resume is up to date before you apply.</p>
  </article>
  <aside><div class="sidebar-sticky"><div class="summary-card">
    <dl><div><dt>Employer</dt><dd>{E(j['employer'])}</dd></div><div><dt>Location</dt><dd>{E(j['location'])}, {j['state']}</dd></div><div><dt>Job type</dt><dd>{j['type']}</dd></div><div><dt>Category</dt><dd>{E(j['category'])}</dd></div></dl>
    <a class="btn btn-primary btn-lg btn-block" href="login.html">Apply now</a>
    <a class="btn btn-secondary btn-block mt-2" href="#">{ico("bookmark")} Save job</a>
    <div class="share"><a class="icon-btn" href="#" aria-label="Share by email">{ico("mail")}</a><a class="icon-btn" href="#" aria-label="Share on Facebook">{ico("facebook")}</a><a class="icon-btn" href="#" aria-label="Share on LinkedIn">{ico("linkedin")}</a><a class="icon-btn" href="#" aria-label="Copy link">{ico("link")}</a></div>
  </div></div></aside>
</div></div></section>
<section class="section section-sand"><div class="container">
  {section_head("Similar jobs", "", ("View all jobs", "jobs.html"))}
  <ul class="job-list">{"".join(job_row(x) for x in similar)}</ul>
</div></section>
'''
    page(job_url(j), f"{j['title']} — Hire Me Holiday Parks", j["summary"], "Find a Job", body)

# ---- Job seekers
js_body = f'''
{page_hero("For job seekers", "Find work with holiday parks, caravan parks and resorts that value good people — from your first season to your next management role.",
           [("Home", "index.html"), ("Job Seekers", None)], SLIDES[1],
           '<div class="btn-row"><a class="btn btn-inverse btn-lg" href="jobs.html">Find a Job</a><a class="btn btn-outline-inverse btn-lg" href="post-resume.html">Post your resume</a></div>')}
<section class="section"><div class="container">
  {section_head("How it works")}
  <ol class="steps">
    <li><h3>Create a free account</h3><p>Register as a job seeker to apply for roles, save jobs and manage alerts.</p></li>
    <li><h3>Post your resume</h3><p>Parks search listed resumes and contact people directly. Listings run for {PRICE['resume_days']} days.</p></li>
    <li><h3>Apply and get alerts</h3><p>Apply online and get new jobs in your chosen categories and regions by email.</p></li>
  </ol>
</div></section>
<section class="section section-sand"><div class="container"><div class="split">
  <div><h2 class="h2-lg">List your resume</h2><p class="lead">Let hiring parks find you. It's the quickest way to be seen by owners and managers looking for staff right now.</p>
    {checklist(["Visible to registered employers for " + str(PRICE['resume_days']) + " days", "Edit or update it any time", "Include your availability, preferred regions and whether you're applying as a couple"])}</div>
  <div class="price-card emph"><p class="h3-small">Resume listing</p><p class="amount">{PRICE['resume']}<small>/ {PRICE['resume_days']} days</small></p>
    {checklist(["One resume listing", "Searchable by employers", "Free job alerts"])}<a class="btn btn-primary btn-lg btn-block" href="post-resume.html">Post your resume</a></div>
</div></div></section>
<section class="section" aria-labelledby="cat-title"><div class="container">
  {section_head("Browse jobs by category", "", ("All jobs", "jobs.html"), "cat-title")}{cat_grid()}
</div></section>
<section class="section section-sand"><div class="container">
  {section_head("Guides for job seekers", "", ("All resources", "resources.html"))}
  <ul class="res-grid">{"".join(f'<li><a class="res-card" href="resources-{r["slug"]}.html">{ico(r["icon"])}<p class="who">{r["who"]}</p><h3>{r["title"]}</h3><p class="d">{r["short"]}</p></a></li>' for r in RESOURCES if r["who"] in ("Job seekers",))}</ul>
</div></section>
<section class="section"><div class="container">
  {section_head("Questions from job seekers")}
  {faq([("Do I need experience to work in a holiday park?", "Not always. Reception, housekeeping and grounds roles are often open to people new to the industry, especially for the busy seasons."),
        ("Do jobs include accommodation?", "Many do, particularly management and live-in couple roles. The listing will say whether accommodation is included."),
        ("Can my partner and I apply together?", "Yes. Look for 'Live-in couple' roles, and mention in your resume that you're applying together and what each of you brings."),
        ("How do I stop job alerts?", "Every alert email includes an unsubscribe link, or you can manage alerts from your account.")])}
</div></section>
{alerts_section()}
{cta("Your next season starts here", "Browse current roles or list your resume so parks can find you.", ("Find a Job", "jobs.html"), ("Post your resume", "post-resume.html"))}
'''
page("job-seekers.html", "For job seekers — Hire Me Holiday Parks", "Find holiday park work and list your resume.", "Job Seekers", js_body)

# ---- Employers
emp_body = f'''
{page_hero("For employers", "Reach people who are looking for park work — not just any job. Advertise roles, tenders and management contracts across Australia.",
           [("Home", "index.html"), ("Employers", None)], SLIDES[3],
           '<div class="btn-row"><a class="btn btn-inverse btn-lg" href="post-job.html">Post a Job</a><a class="btn btn-outline-inverse btn-lg" href="#resumes">Search resumes</a></div>')}
<section class="section"><div class="container">
  <div class="feature-grid">
    <div class="feature">{ico("target")}<h3>An industry audience</h3><p>Thousands of registered job seekers interested specifically in holiday parks.</p></div>
    <div class="feature">{ico("file-search")}<h3>Search resumes</h3><p>Browse listed resumes and contact people who are ready to start.</p></div>
    <div class="feature">{ico("file-signature")}<h3>More than jobs</h3><p>Advertise tenders, leases and management contracts alongside staff roles.</p></div>
  </div>
</div></section>
<section class="section section-sand"><div class="container">
  {section_head("Simple pricing", "One listing, one price. No subscriptions.")}
  <div class="grid-2" style="max-width:880px">
    <div class="price-card emph"><p class="h3-small">Job listing</p><p class="amount">{PRICE['job']}<small>/ {PRICE['job_days']} days</small></p>
      {checklist(["Listed on Find a Job and in category and location pages", "Sent to matching job alert subscribers", "Suitable for staff roles, tenders and contracts"])}<a class="btn btn-primary btn-lg btn-block" href="post-job.html">Post a Job</a></div>
    <div class="price-card" id="resumes"><p class="h3-small">Resume search</p><p class="amount" style="font-size:32px;margin-top:20px">Included</p>
      {checklist(["Browse resumes listed by job seekers", "Filter by category and location", "Contact candidates directly"])}<a class="btn btn-secondary btn-lg btn-block" href="{ORIGIN}/resumes/">Search resumes</a></div>
  </div>
</div></section>
<section class="section"><div class="container">
  {section_head("How to post a job")}
  <ol class="steps">
    <li><h3>Register as an employer</h3><p>Create your free employer account with your park's details.</p></li>
    <li><h3>Write your listing</h3><p>Add the role, location, job type and how to apply. Our tips can help.</p></li>
    <li><h3>Publish and hear back</h3><p>Your listing goes live for {PRICE['job_days']} days and reaches alert subscribers.</p></li>
  </ol>
</div></section>
<section class="section section-sand" aria-labelledby="svc-title"><div class="container"><div class="services-layout">
  <div class="sticky"><h2 id="svc-title" class="h2-lg">Need more than a new hire?</h2><p class="lead mt-4">From business plans to WHS audits, our services help parks run better.</p><a class="btn btn-secondary mt-8" href="services.html">View services</a></div>
  {service_list()}
</div></div></section>
<section class="section"><div class="container">
  {section_head("Questions from employers")}
  {faq([("How long does a listing run?", f"Job listings run for {PRICE['job_days']} days from the day they're published."),
        ("Can I advertise a tender or management contract?", "Yes. Choose 'Tender' as the job type so it's easy for operators and managers to find."),
        ("Can I edit a listing after it's live?", "Yes, sign in to your employer account to edit or close a listing at any time."),
        ("Do you help with recruitment beyond advertising?", "Our park management support service can help with staffing structure and recruitment. Contact us to talk it through.")])}
</div></section>
{supporters_section()}
{cta("Find the people who'll make your park great", "Post your job today and reach job seekers who know the industry.", ("Post a Job", "post-job.html"), ("Contact us", "contact.html"))}
'''
page("employers.html", "For employers — Hire Me Holiday Parks", "Advertise holiday park jobs, tenders and contracts.", "Employers", emp_body)

# ---- Post a job form
opts = lambda xs: "".join(f'<option>{E(x)}</option>' for x in xs)
post_job = f'''
{page_hero("Post a job", f"A {PRICE['job_days']}-day listing is {PRICE['job']}. Fill in the details below — you can edit the listing any time after it's live.", [("Home", "index.html"), ("Employers", "employers.html"), ("Post a Job", None)])}
<section class="section" style="padding-top:48px"><div class="container"><div class="with-sidebar side-right">
  <div>
    <form class="form form-card" data-validate data-success="job-done">
      <div class="form-section"><h2>The role</h2><div class="form">
        <div><label class="label" for="pj-title">Job title</label><input class="field" id="pj-title" required data-label="Job title" placeholder="e.g. Park Manager"><p class="hint">Use a title people search for.</p></div>
        <div class="form-row">
          <div><label class="label" for="pj-cat">Category</label><select class="field" id="pj-cat" required data-label="Category"><option value="">Choose a category</option>{opts([c for c, _, _ in CATEGORIES])}</select></div>
          <div><label class="label" for="pj-type">Job type</label><select class="field" id="pj-type" required data-label="Job type"><option value="">Choose a job type</option>{opts(TYPES)}</select></div>
        </div>
        <div><label class="label" for="pj-desc">Description</label><textarea class="field" id="pj-desc" required data-label="Description" placeholder="What the role involves, the park, rosters, accommodation…"></textarea></div>
      </div></div>
      <div class="form-section"><h2>Location</h2><div class="form-row">
        <div><label class="label" for="pj-town">Town or region</label><input class="field" id="pj-town" required data-label="Town or region"></div>
        <div><label class="label" for="pj-state">State</label><select class="field" id="pj-state" required data-label="State"><option value="">Choose a state</option>{opts([n for _, n, _ in STATES])}</select></div>
      </div></div>
      <div class="form-section"><h2>Your park</h2><div class="form">
        <div class="form-row">
          <div><label class="label" for="pj-park">Park or business name</label><input class="field" id="pj-park" required data-label="Park name"></div>
          <div><label class="label" for="pj-contact">Contact name</label><input class="field" id="pj-contact" required data-label="Contact name" autocomplete="name"></div>
        </div>
        <div class="form-row">
          <div><label class="label" for="pj-email">Email for applications</label><input class="field" id="pj-email" type="email" required data-label="Email" autocomplete="email"></div>
          <div><label class="label" for="pj-phone">Phone <span class="opt">(optional)</span></label><input class="field" id="pj-phone" type="tel" autocomplete="tel"></div>
        </div>
        <label class="check"><input type="checkbox" id="pj-terms" required data-label="Agreement"> I agree to the <a class="text-link" href="{ORIGIN}/terms-of-use/">terms &amp; conditions</a></label>
      </div></div>
      <div><button class="btn btn-primary btn-lg" type="submit">Continue to payment</button></div>
    </form>
    <div class="success" id="job-done" role="status" tabindex="-1" hidden>{ico("check-circle-2")}<div><p><strong>Listing saved</strong></p><p class="soft mt-2">Complete payment to publish your job. We'll email a receipt to <span data-fill="email"></span>.</p></div></div>
  </div>
  <aside><div class="sidebar-sticky"><div class="summary-card">
    <p class="h3-small">Job listing</p><p class="amount" style="font-family:var(--font-display);font-size:40px;font-weight:600">{PRICE['job']}</p><p class="muted">{PRICE['job_days']} days · includes job alerts</p>
    {checklist(["Edit any time", "Tenders and contracts welcome"])}
    <p class="soft mt-6" style="font-size:15px">Need help writing it? Read our <a class="text-link" href="resources-tips-employers.html">tips for employers</a>.</p>
  </div></div></aside>
</div></div></section>
'''
page("post-job.html", "Post a job — Hire Me Holiday Parks", "Advertise a holiday park job.", "Employers", post_job)

# ---- Post a resume form
post_resume = f'''
{page_hero("Post your resume", f"A {PRICE['resume_days']}-day resume listing is {PRICE['resume']}. Parks can search it and contact you directly.", [("Home", "index.html"), ("Job Seekers", "job-seekers.html"), ("Post your resume", None)])}
<section class="section" style="padding-top:48px"><div class="container"><div class="with-sidebar side-right">
  <div>
    <form class="form form-card" data-validate data-success="res-done">
      <div class="form-section"><h2>About you</h2><div class="form">
        <div class="form-row">
          <div><label class="label" for="pr-name">Full name</label><input class="field" id="pr-name" required data-label="Full name" autocomplete="name"></div>
          <div><label class="label" for="pr-email">Email</label><input class="field" id="pr-email" type="email" required data-label="Email" autocomplete="email"></div>
        </div>
        <div class="form-row">
          <div><label class="label" for="pr-phone">Phone <span class="opt">(optional)</span></label><input class="field" id="pr-phone" type="tel" autocomplete="tel"></div>
          <div><label class="label" for="pr-couple">Applying as</label><select class="field" id="pr-couple"><option>An individual</option><option>A couple</option></select></div>
        </div>
      </div></div>
      <div class="form-section"><h2>What you're looking for</h2><div class="form">
        <div><label class="label" for="pr-headline">Headline</label><input class="field" id="pr-headline" required data-label="Headline" placeholder="e.g. Experienced park manager, available from March"></div>
        <div class="form-row">
          <div><label class="label" for="pr-cat">Preferred category</label><select class="field" id="pr-cat" required data-label="Category"><option value="">Choose a category</option>{opts([c for c, _, _ in CATEGORIES])}</select></div>
          <div><label class="label" for="pr-state">Preferred state</label><select class="field" id="pr-state"><option>Anywhere in Australia</option>{opts([n for _, n, _ in STATES])}</select></div>
        </div>
        <fieldset><legend class="label">Job types</legend><div class="chips" style="margin-top:0">{"".join(f'<label class="check chip"><input type="checkbox" name="rtype" value="{t}" style="margin-top:0"> {t}</label>' for t in TYPES[:4])}</div></fieldset>
        <div><label class="label" for="pr-summary">Summary</label><textarea class="field" id="pr-summary" required data-label="Summary" placeholder="Your experience, skills and availability"></textarea></div>
        <div><span class="label">Resume file <span class="opt">(optional)</span></span><label class="file-drop">{ico("upload")}<span>Upload a PDF or Word document</span><input type="file" class="sr-only" accept=".pdf,.doc,.docx"></label></div>
      </div></div>
      <label class="check"><input type="checkbox" id="pr-terms" required data-label="Agreement"> I agree to the <a class="text-link" href="{ORIGIN}/terms-of-use/">terms &amp; conditions</a></label>
      <div><button class="btn btn-primary btn-lg" type="submit">Continue to payment</button></div>
    </form>
    <div class="success" id="res-done" role="status" tabindex="-1" hidden>{ico("check-circle-2")}<div><p><strong>Resume saved</strong></p><p class="soft mt-2">Complete payment to publish it. We'll email a receipt to <span data-fill="email"></span>.</p></div></div>
  </div>
  <aside><div class="sidebar-sticky"><div class="summary-card">
    <p class="h3-small">Resume listing</p><p class="amount" style="font-family:var(--font-display);font-size:40px;font-weight:600">{PRICE['resume']}</p><p class="muted">{PRICE['resume_days']} days · searchable by employers</p>
    <p class="soft mt-6" style="font-size:15px">Not sure what to include? Read our <a class="text-link" href="resources-tips-job-seekers.html">tips for job seekers</a>.</p>
  </div></div></aside>
</div></div></section>
'''
page("post-resume.html", "Post your resume — Hire Me Holiday Parks", "List your resume for holiday park employers.", "Job Seekers", post_resume)

# ---- Services overview
svc_body = f'''
{page_hero("Services", "Support beyond recruitment. Our team has run, planned and audited parks, and we help owners and managers build stronger, more professional businesses.", [("Home", "index.html"), ("Services", None)], SLIDES[5])}
<section class="section"><div class="container"><div class="services-layout">
  <div class="sticky"><h2 class="h2-lg">How we can help</h2><p class="lead mt-4">Choose one service or combine them. Every engagement starts with a conversation about your park and what you want to achieve.</p><a class="btn btn-primary mt-8" href="contact.html">Talk to us about your park</a></div>
  {service_list()}
</div></div></section>
<section class="section section-sand"><div class="container">
  {section_head("Who we work with")}
  <div class="feature-grid">
    <div class="feature">{ico("home")}<h3>Owners and operators</h3><p>Independent parks and family businesses wanting to grow or run more smoothly.</p></div>
    <div class="feature">{ico("landmark")}<h3>Councils and land managers</h3><p>Public land parks preparing tenders, leases and management contracts.</p></div>
    <div class="feature">{ico("building")}<h3>Buyers and developers</h3><p>People planning to buy, build or redevelop a park.</p></div>
  </div>
</div></section>
{cta("Let's talk about your park", "Tell us what you're working on and we'll suggest where to start.", ("Contact us", "contact.html"), ("Find a Job", "jobs.html"))}
'''
page("services.html", "Services — Hire Me Holiday Parks", "Business planning, management support, training, park planning and audits for holiday parks.", "Services", svc_body)

for s in SERVICES:
    others = [o for o in SERVICES if o["slug"] != s["slug"]]
    body = f'''
{page_hero(s["title"], E(s["intro"]), [("Home", "index.html"), ("Services", "services.html"), (s["title"], None)])}
<section class="section" style="padding-top:56px"><div class="container"><div class="with-sidebar side-right">
  <div class="prose">
    <h2 style="margin-top:0">What's included</h2>
    <ul>{"".join(f"<li>{E(i)}</li>" for i in s["inc"])}</ul>
    <h2>Who it's for</h2><p>{E(s["who"])}</p>
    <h2>How it works</h2>
    <ol><li>We start with a conversation about your park and goals.</li><li>We agree the scope, timing and cost in writing.</li><li>We do the work, on-site or remotely, and keep you updated.</li><li>You receive clear recommendations and next steps.</li></ol>
  </div>
  <aside><div class="sidebar-sticky"><div class="summary-card">
    <span class="icon-chip">{ico(s["icon"])}</span>
    <h2 class="mt-4" style="font-size:22px">Talk to us about {E(s["title"].lower())}</h2>
    <p class="soft mt-2" style="font-size:15px">Tell us a little about your park and we'll be in touch.</p>
    <a class="btn btn-primary btn-lg btn-block mt-6" href="contact.html?topic={s['slug']}">Make an enquiry</a>
  </div></div></aside>
</div></div></section>
<section class="section section-sand"><div class="container">
  {section_head("Other services", "", ("All services", "services.html"))}
  <ul class="service-list">{"".join(f'<li><a href="service-{o["slug"]}.html">{ico(o["icon"], "s-ico")}<span class="s-body"><strong>{E(o["title"])}</strong><span class="d">{E(o["short"])}</span></span>{ico("arrow-up-right", "arrow")}</a></li>' for o in others)}</ul>
</div></section>
'''
    page(f"service-{s['slug']}.html", f"{s['title']} — Hire Me Holiday Parks", s["short"], "Services", body)

# ---- Resources
res_body = f'''
{page_hero("Resources", "Practical guides for building a career, or a team, in Australia's holiday park industry.", [("Home", "index.html"), ("Resources", None)])}
<section class="section"><div class="container">{resources_block()}</div></section>
{alerts_section()}
'''
page("resources.html", "Resources — Hire Me Holiday Parks", "Career advice, tips for job seekers and employers, and industry contacts.", "Resources", res_body)

def render_blocks(blocks):
    out = []
    for kind, val in blocks:
        if kind in ("h2", "h3", "p"): out.append(f"<{kind}>{E(val)}</{kind}>")
        elif kind in ("ul", "ol"): out.append(f"<{kind}>" + "".join(f"<li>{v}</li>" for v in val) + f"</{kind}>")
        elif kind == "callout": out.append(f'<p class="callout">{E(val)}</p>')
    return "".join(out)

for r in RESOURCES:
    others = [o for o in RESOURCES if o["slug"] != r["slug"]]
    body = f'''
{page_hero(r["title"], E(r["short"]), [("Home", "index.html"), ("Resources", "resources.html"), (r["title"], None)])}
<section class="section" style="padding-top:56px"><div class="container"><div class="with-sidebar side-right">
  <article class="prose">{render_blocks(r["body"]).replace("<h2>", '<h2>', 1)}</article>
  <aside><div class="sidebar-sticky"><div class="summary-card">
    <p class="h3-small">More guides</p>
    <ul class="form mt-4" style="gap:12px">{"".join(f'<li><a class="text-link" href="resources-{o["slug"]}.html">{o["title"]}</a></li>' for o in others)}</ul>
    <hr style="border:0;border-top:1px solid var(--line);margin:20px 0">
    <a class="btn btn-primary btn-block" href="jobs.html">Find a Job</a><a class="btn btn-secondary btn-block mt-2" href="post-job.html">Post a Job</a>
  </div></div></aside>
</div></div></section>
'''
    page(f"resources-{r['slug']}.html", f"{r['title']} — Hire Me Holiday Parks", r["short"], "Resources", body)

# ---- About
about = f'''
{page_hero("About Hire Me Holiday Parks", "A specialist job board for Australia's holiday park, caravan park and resort industry — connecting great people with fantastic job opportunities since 2014.", [("Home", "index.html"), ("About", None)], SLIDES[6])}
<section class="section"><div class="container"><div class="split">
  <div class="prose">
    <h2 style="margin-top:0">Why we exist</h2>
    <p>Holiday parks need people who understand the work: busy school holidays, early starts, guests who become regulars, and teams that often live on site. General job sites weren't built for that.</p>
    <p>Hire Me Holiday Parks brings job seekers and parks together in one place, so the right people find the right roles — and the industry becomes stronger and more professional as a result.</p>
    <h2>More than a job board</h2>
    <p>Alongside recruitment, our team offers business planning, management support, training, park planning and audits. <a href="services.html">See our services</a>.</p>
  </div>
  <div class="split-media"><img src="{SLIDES[7]}" alt="" loading="lazy"></div>
</div></div></section>
<section class="stats section-sand" style="padding:56px 0" aria-label="Our community"><div class="container"><div class="stats-inner" style="border:0;padding:0">
  <p>Our community today</p><dl>{stats}</dl></div></div></section>
<section class="section"><div class="container">
  {section_head("What we believe")}
  <div class="feature-grid">
    <div class="feature">{ico("heart-handshake")}<h3>Good people make good parks</h3><p>Guest experience starts with the team. Hiring well matters.</p></div>
    <div class="feature">{ico("map")}<h3>Every region counts</h3><p>From the coast to the outback, every park deserves access to great staff.</p></div>
    <div class="feature">{ico("graduation-cap")}<h3>Careers, not just jobs</h3><p>Park work can be a long, rewarding career. We help people grow into it.</p></div>
  </div>
</div></section>
{supporters_section()}
{cta()}
'''
page("about.html", "About us — Hire Me Holiday Parks", "Australia's specialist job board for the holiday park industry.", "About", about)

# ---- Contact
topics = [("general", "General enquiry"), ("job-seeker", "Job seeker support"), ("employer", "Employer or listing support")] + [(s["slug"], s["title"]) for s in SERVICES]
contact = f'''
{page_hero("Contact us", "Questions about a listing, your account or our services? Send us a message and we'll get back to you.", [("Home", "index.html"), ("Contact", None)])}
<section class="section" style="padding-top:56px"><div class="container"><div class="with-sidebar side-right">
  <div>
    <form class="form form-card" data-validate data-success="contact-done">
      <div class="form-row">
        <div><label class="label" for="c-name">Name</label><input class="field" id="c-name" required data-label="Name" autocomplete="name"></div>
        <div><label class="label" for="c-email">Email</label><input class="field" id="c-email" type="email" required data-label="Email" autocomplete="email"></div>
      </div>
      <div class="form-row">
        <div><label class="label" for="c-phone">Phone <span class="opt">(optional)</span></label><input class="field" id="c-phone" type="tel" autocomplete="tel"></div>
        <div><label class="label" for="c-topic">Topic</label><select class="field" id="c-topic">{"".join(f'<option value="{v}">{E(l)}</option>' for v, l in topics)}</select></div>
      </div>
      <div><label class="label" for="c-park">Park or business <span class="opt">(optional)</span></label><input class="field" id="c-park"></div>
      <div><label class="label" for="c-msg">Message</label><textarea class="field" id="c-msg" required data-label="Message"></textarea></div>
      <div><button class="btn btn-primary btn-lg" type="submit">Send message</button></div>
    </form>
    <div class="success" id="contact-done" role="status" tabindex="-1" hidden>{ico("check-circle-2")}<div><p><strong>Message sent</strong></p><p class="soft mt-2">Thanks — we'll reply to <span data-fill="email"></span>.</p></div></div>
  </div>
  <aside><div class="sidebar-sticky"><div class="summary-card">
    <ul class="contact-list">
      <!-- Add the business email and phone number here -->
      <li>{ico("life-buoy")}<div><strong>Help with the site</strong><a href="resources-tips-site.html">Tips for using our site</a></div></li>
      <li>{ico("briefcase")}<div><strong>Advertising a role</strong><a href="employers.html">Employer information</a></div></li>
      <li>{ico("user-round")}<div><strong>Looking for work</strong><a href="job-seekers.html">Job seeker information</a></div></li>
      <li>{ico("share-2")}<div><strong>Follow us</strong>{" · ".join(f'<a href="{h}" target="_blank" rel="noopener">{n}</a>' for n, h in SOCIAL[:2])}</div></li>
    </ul>
  </div></div></aside>
</div></div></section>
<script>(function(){{var t=new URLSearchParams(location.search).get("topic");var s=document.getElementById("c-topic");if(t&&s)s.value=t;}})();</script>
'''
page("contact.html", "Contact us — Hire Me Holiday Parks", "Get in touch with Hire Me Holiday Parks.", "Contact", contact)

# ---- Login
login = f'''
<div class="auth-wrap">
  <div class="auth-media"><img src="{HERO}" alt=""><div class="inner"><h2>Welcome back</h2><p>Manage your listings, applications and job alerts.</p></div></div>
  <div class="auth-form"><div>
    <h1>Sign in</h1><p class="lead">New here? <a class="text-link" href="register.html">Create an account</a></p>
    <form class="form mt-8" data-validate data-success="login-done">
      <div><label class="label" for="l-email">Email</label><input class="field" id="l-email" type="email" required data-label="Email" autocomplete="email"></div>
      <div><label class="label" for="l-pass">Password</label><input class="field" id="l-pass" type="password" required data-label="Password" autocomplete="current-password"></div>
      <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap"><label class="check"><input type="checkbox"> Keep me signed in</label><a class="text-link" href="#">Forgot password?</a></div>
      <button class="btn btn-primary btn-lg btn-block" type="submit">Sign in</button>
    </form>
    <div class="success mt-8" id="login-done" role="status" tabindex="-1" hidden>{ico("check-circle-2")}<div><p><strong>Signed in</strong></p><p class="soft mt-2">Connect this form to your authentication service.</p></div></div>
  </div></div>
</div>
'''
page("login.html", "Sign in — Hire Me Holiday Parks", "Sign in to your account.", "", login, bare_footer=True)

# ---- Register
register = f'''
<div class="auth-wrap">
  <div class="auth-media"><img src="{SLIDES[2]}" alt=""><div class="inner"><h2>Join Australia's holiday park community</h2><p>Register free to apply for jobs, post listings and get job alerts.</p></div></div>
  <div class="auth-form"><div>
    <h1>Create an account</h1><p class="lead">Already registered? <a class="text-link" href="login.html">Sign in</a></p>
    <form class="form mt-8" data-validate data-success="reg-done">
      <fieldset><legend class="label">I'm a…</legend><div class="role-switch">
        <label><input type="radio" name="role" value="seeker" checked><span><strong>Job seeker</strong><small>Find work and post a resume</small></span></label>
        <label><input type="radio" name="role" value="employer"><span><strong>Employer</strong><small>Post jobs and search resumes</small></span></label>
      </div></fieldset>
      <div class="form-row">
        <div><label class="label" for="r-first">First name</label><input class="field" id="r-first" required data-label="First name" autocomplete="given-name"></div>
        <div><label class="label" for="r-last">Last name</label><input class="field" id="r-last" required data-label="Last name" autocomplete="family-name"></div>
      </div>
      <div><label class="label" for="r-email">Email</label><input class="field" id="r-email" type="email" required data-label="Email" autocomplete="email"></div>
      <div><label class="label" for="r-pass">Password</label><input class="field" id="r-pass" type="password" required data-label="Password" autocomplete="new-password"><p class="hint">At least 8 characters.</p></div>
      <div><label class="label" for="r-pass2">Confirm password</label><input class="field" id="r-pass2" type="password" required data-label="Password confirmation" data-match="r-pass" autocomplete="new-password"></div>
      <label class="check"><input type="checkbox" id="r-terms" required data-label="Agreement"> I agree to the <a class="text-link" href="{ORIGIN}/terms-of-use/">terms &amp; conditions</a></label>
      <label class="check"><input type="checkbox" checked> Email me job alerts and site news</label>
      <button class="btn btn-primary btn-lg btn-block" type="submit">Create account</button>
    </form>
    <div class="success mt-8" id="reg-done" role="status" tabindex="-1" hidden>{ico("check-circle-2")}<div><p><strong>Account created</strong></p><p class="soft mt-2">We've sent a confirmation link to <span data-fill="email"></span>.</p></div></div>
  </div></div>
</div>
'''
page("register.html", "Register — Hire Me Holiday Parks", "Create a job seeker or employer account.", "", register, bare_footer=True)

# ---- 404
nf = f'''
<section class="section"><div class="container center" style="max-width:640px">
  <p class="muted">Error 404</p><h1 class="mt-4" style="font-size:44px">We couldn't find that page</h1>
  <p class="lead mt-4" style="margin-left:auto;margin-right:auto">The link may be old or the listing may have closed. Try searching current jobs instead.</p>
  <div class="btn-row mt-8" style="justify-content:center"><a class="btn btn-primary btn-lg" href="jobs.html">Find a Job</a><a class="btn btn-secondary btn-lg" href="index.html">Go to home</a></div>
</div></section>
'''
page("404.html", "Page not found — Hire Me Holiday Parks", "Page not found.", "", nf)
print("built")
