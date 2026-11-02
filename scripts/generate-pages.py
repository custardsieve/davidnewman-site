"""Generator used to create the initial HTML pages from the WordPress content. Kept for reference — edit the HTML directly from now on.
The output is plain HTML committed to the repo; this script is not part of the site."""
import json, html, os
from pathlib import Path

ROOT = Path("/home/claude/davidnewman-site")
SITE = "https://davidnewman.com.au"
WP = "https://davidnewman.com.au/wp-content/uploads/"
E = html.escape

IMAGES = {}  # local path -> remote url


def img(local, remote, alt, cls="", eager=False, w=None, h=None):
    IMAGES["assets/img/" + local] = WP + remote
    attrs = f' class="{cls}"' if cls else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="/assets/img/{E(local)}" alt="{E(alt)}" {load}{attrs}>'


NAV = [("/work/", "Work"), ("/about/", "About"), ("/contact/", "Contact")]


def page(path, title, desc, body, active=None, og=None):
    nav = "\n".join(
        f'        <li><a href="{u}"{" aria-current=\"page\"" if u == active else ""}>{t}</a></li>' for u, t in NAV
    )
    full_title = f"{title} — David Newman Design" if title else "David Newman Design — Product Design Strategist"
    og_img = og or "/assets/img/og-default.jpg"
    doc = f"""<!doctype html>
<html lang="en-AU" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{E(full_title)}</title>
  <meta name="description" content="{E(desc)}">
  <link rel="canonical" href="{SITE}{path}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{E(full_title)}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:url" content="{SITE}{path}">
  <meta property="og:image" content="{SITE}{og_img}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#ffffff">
  <link rel="manifest" href="/manifest.webmanifest">
  <link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/icons/icon-192.png">
  <link rel="preload" href="/assets/fonts/CircularStd-Medium.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/styles.css">
  <script src="/assets/js/main.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container site-header__inner">
      <a class="brand" href="/">David Newman Design</a>
      <nav class="nav" aria-label="Main">
        <ul>
{nav}
        </ul>
      </nav>
    </div>
  </header>

  <main id="main">
{body}
  </main>

  <footer class="site-footer">
    <div class="container site-footer__inner">
      <p>Thanks for visiting.</p>
      <p><a href="mailto:hello@davidnewman.com.au">hello@davidnewman.com.au</a></p>
      <p>© <span data-year>2026</span> David Newman. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>
"""
    out = ROOT / path.lstrip("/")
    if path.endswith("/"):
        out = out / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)


# --------------------------------------------------------------------------- projects
PROJECTS = [
    dict(slug="rio-tinto", name="Rio Tinto", line="A new global frontline experience", role="Lead Product Designer",
         years="2023 – now", cover=("rio-tinto/cover.jpg", "2026/05/RioTinto-main-2-scaled.jpg"), nda=True),
    dict(slug="atlassian", name="Atlassian", line="Jira core invites", role="Senior Product Designer",
         years="2022 – 2023", cover=("atlassian/cover.jpg", "2026/04/Header-scaled.jpg")),
    dict(slug="proptrack", name="REA Group – PropTrack", line="PropTrack × ANZ valuations platform",
         role="Senior Product Designer", years="2020 – 2022", cover=("proptrack/cover.jpg", "2026/04/anz-cover-scaled.jpg")),
    dict(slug="swinburne", name="Swinburne University", line="The Swinburne student experience",
         role="UX Design Specialist", years="2019 – 2020", cover=("swinburne/cover.jpg", "2026/04/Swinburne-hero-scaled.jpg")),
    dict(slug="officeworks", name="Officeworks", line="Banner blindness", role="UX/UI Designer",
         years="2018 – 2019", cover=("officeworks/cover.jpg", "2026/05/officeworks-hero-scaled.jpg")),
]
BY_SLUG = {p["slug"]: p for p in PROJECTS}


def card(p, eager=False):
    badge = '<span class="badge">NDA</span>' if p.get("nda") else ""
    return f"""          <a class="card reveal" href="/work/{p['slug']}/">
            <div class="card__media">{img(p['cover'][0], p['cover'][1], f"{p['name']} — {p['line']}", eager=eager)}</div>
            <div class="card__body">
              <h3 class="card__title">{E(p['name'])}{badge}</h3>
              <p class="card__meta">{E(p['line'])}<br>{E(p['years'])}</p>
            </div>
          </a>"""


# --------------------------------------------------------------------------- home
home = f"""    <section class="container home-hero">
      <p class="eyebrow">Hello! I'm Dave — Product Design Strategist</p>
      <h1 class="display">How might we make the digital world easier?</h1>
      <p class="home-hero__cta"><a class="cta" href="/contact/">Let's work together</a></p>
    </section>

    <section class="container section--tight">
      <div class="grid grid--aside">
        <div>{img('about/portrait.jpg', '2026/05/Profile-inverse-scaled.jpg', 'Portrait of David Newman', cls='portrait')}</div>
        <div class="grid grid--2">
          <div class="reveal">
            <h2 class="eyebrow">Skills</h2>
            <ul class="skills">
              <li>AI service design.</li><li>Design thinking.</li><li>Problem framing.</li><li>Strategic planning.</li>
              <li>UX research.</li><li>UX analysis.</li><li>Design Sprints.</li><li>Systems design.</li>
              <li>Interaction design.</li><li>Typography.</li>
            </ul>
          </div>
          <div class="reveal">
            <h2 class="eyebrow">Context</h2>
            <p class="lead">Born and raised in Sydney, I started in IT back when Unix shells were all the rage. I then spent 13 years in Europe, swapping code for colour theory and studying Fine Arts at the University of Valencia.</p>
            <p>Now I work in Strategic Product, where logic, empathy and chaos intersect. I help design products that make sense… and make people smile. Off-screen, you'll find me at the piano, cooking paellas, or turning “short” trips into decade-long adventures.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--inverse" aria-labelledby="selected">
      <div class="container">
        <h2 id="selected" class="display" style="font-size: var(--fs-xl); margin-bottom: var(--space-5);">Selected works</h2>
        <div class="cards">
{chr(10).join(card(p) for p in PROJECTS)}
        </div>
      </div>
    </section>
"""
page("/", None, "Senior Product Designer specialising in complex platforms, enterprise systems and large-scale digital products.", home)

# --------------------------------------------------------------------------- work index
work = f"""    <section class="container section--tight">
      <p class="eyebrow">My projects</p>
      <h1 class="display" style="font-size: var(--fs-xl);">Work</h1>
      <p class="lead" style="margin-top: var(--space-4);">Senior Product Designer specialising in complex platforms, enterprise systems and large-scale digital products. I've worked across SaaS, government and enterprise environments including Atlassian, Service Victoria, PropTrack and Rio Tinto, helping organisations move from delivery chaos to clear product outcomes.</p>
      <p style="margin-top: var(--space-3); color: var(--color-muted);">Known for operating comfortably in ambiguity, scaling design maturity, and cooking something Spanish.</p>
    </section>
    <section class="container section--tight">
      <div class="cards">
{chr(10).join(card(p, eager=i < 2) for i, p in enumerate(PROJECTS))}
      </div>
    </section>
"""
page("/work/", "Work", "Selected product design case studies: Rio Tinto, Atlassian, REA Group – PropTrack, Swinburne University and Officeworks.", work, active="/work/")


# --------------------------------------------------------------------------- case study builder
def gallery(slug, items, contain=False):
    cls = "gallery gallery--contain" if contain else "gallery"
    imgs = "\n".join("          " + img(f"{slug}/{l}", r, a) for l, r, a in items)
    return f'        <div class="{cls}">\n{imgs}\n        </div>'


def figure(slug, local, remote, alt, caption=None):
    cap = f"<figcaption>{E(caption)}</figcaption>" if caption else ""
    return f'        <figure class="figure">{img(f"{slug}/{local}", remote, alt)}{cap}</figure>'


def case_study(p, summary, services, company, sections, next_slugs):
    slug = p["slug"]
    toc = "\n".join(f'            <li><a href="#{sid}">{E(t)}</a></li>' for sid, t, _ in sections)
    secs = "\n".join(
        f'        <section class="cs-section" id="{sid}" aria-labelledby="{sid}-h">\n          <h2 id="{sid}-h">{E(t)}</h2>\n{content}\n        </section>'
        for sid, t, content in sections
    )
    nxt = "\n".join(card(BY_SLUG[s]) for s in next_slugs)
    body = f"""    <article>
      <header class="container cs-hero">
        <p class="eyebrow"><a href="/work/">Work</a> / {E(p['name'])}</p>
        <h1 class="cs-hero__title">{E(p['line'])}</h1>
        <p class="lead">{E(summary)}</p>
        <dl class="cs-meta">
          <div><dt>Role</dt><dd>{E(p['role'])}</dd></div>
          <div><dt>Company</dt><dd>{E(company)}</dd></div>
          <div><dt>Services</dt><dd>{E(', '.join(services))}</dd></div>
        </dl>
      </header>
      <div class="container cs-cover">{img(p['cover'][0], p['cover'][1], f"{p['name']} — {p['line']}", eager=True)}</div>
      <div class="container section">
        <div class="grid grid--aside">
          <nav class="cs-toc" aria-label="On this page">
            <ol>
{toc}
            </ol>
          </nav>
          <div>
{secs}
          </div>
        </div>
      </div>
      <section class="section section--inverse" aria-labelledby="next-h">
        <div class="container">
          <h2 id="next-h" class="eyebrow">Next projects</h2>
          <div class="next-project">
{nxt}
          </div>
        </div>
      </section>
    </article>
"""
    page(f"/work/{slug}/", p["name"], f"{p['name']} case study: {p['line']}. {summary}"[:300], body, active="/work/",
         og=f"/assets/img/{p['cover'][0]}")


def prose(*paras):
    return '        <div class="prose">\n' + "\n".join(f"          <p>{x}</p>" for x in paras) + "\n        </div>"


def callouts(items):
    inner = "\n".join(f'          <div class="callout"><h3>{E(h)}</h3><p>{t}</p></div>' for h, t in items)
    return f'        <div class="callouts">\n{inner}\n        </div>'


def metrics(items, heading=None):
    inner = "\n".join(
        f'          <div class="metric"><span class="metric__value">{E(v)}</span><span class="metric__label">{E(l)}</span></div>'
        for v, l in items)
    h = f'        <h3 class="eyebrow">{E(heading)}</h3>\n' if heading else ""
    return f'{h}        <div class="metrics">\n{inner}\n        </div>'


# ----- Officeworks
ow = BY_SLUG["officeworks"]
case_study(
    ow,
    "Banners are a critical way of communicating company initiatives, tools and business partnerships. Click-through rates were below 1% across the entire Officeworks website, and our team was asked how we might improve communication through banner placement and design.",
    ["UX research", "A/B testing", "Design system templating", "Outcomes reporting"],
    "Wesfarmers Group — Officeworks",
    [
        ("problem", "Problem", "\n".join([
            prose("Using Hotjar heatmaps, we observed that Officeworks users were not engaging with key content. I formed the hypothesis that users perceived much of the content as advertising and were therefore ignoring it. Across the website, UI elements and competing content all fought for users’ attention.",
                  "Users were often not browsing casually, but visiting the site to complete a specific task. Over time they had developed learned behaviours that prioritised elements perceived as useful — navigation, search and headlines — while ignoring content considered low value. Promotional banners became one of the strongest examples of this behaviour."),
            figure("officeworks", "persona-1.jpg", "2026/05/banner-blindness-perso-1-1-scaled.jpg", "Banner blindness research persona"),
            callouts([("Observations", "Analysis of over 300 banners, current and historical, showed a pattern among high-engagement banners: they all had minimal graphics and a simple message."),
                      ("Key findings", "Banners that don’t look like advertising have more credibility (higher click-through rates) and promote trust within a branded system.")]),
            figure("officeworks", "persona-2.jpg", "2026/05/banner-blindness-perso-2-1-scaled.jpg", "Banner analysis findings"),
            prose("<strong>Context.</strong> To understand context, I visited Officeworks stores to see how in-store initiatives were being advertised."),
            gallery("officeworks", [(f"store-{n}.jpg", f"2026/05/AAP_{n}{'-scaled' if n != '7317a' else ''}.jpg", "In-store signage at Officeworks")
                                    for n in ["7313", "7316", "7317a", "7317", "7319", "7322", "7312", "7307", "7306", "7315"]]),
        ])),
        ("solution", "Solution", "\n".join([
            prose("The first logical step was to define what specifically made something look like advertising to Officeworks customers. We did this through semi-structured user interviews. The results:"),
            '        <div class="prose"><ul><li>Small rectangular shapes in the middle of images.</li><li>Multiple typefaces.</li><li>Coloured backgrounds.</li><li>Text embedded over an image.</li></ul><p>How might we design a banner that avoids all of the above — and how would it perform?</p></div>',
            figure("officeworks", "ab-option-1.jpg", "2026/05/Officeworks-option1-scaled.jpg", "A/B test option 1: blue banner", "A/B test option 1 — Banner Blue"),
            figure("officeworks", "ab-option-2.jpg", "2026/05/Officeworks-option-2-scaled.jpg", "A/B test option 2: grey banner", "A/B test option 2 — Banner Grey"),
            figure("officeworks", "ab-control.jpg", "2026/05/Officeworks-Control-scaled.jpg", "A/B test control banner", "A/B test — Control"),
            prose("With statistical significance, our hypothesis was proven: users were ignoring banners that looked like ads. Neutral tones and simplified messaging were more effective at communicating business partnerships, tools and initiatives, and the improved brand consistency increased brand credibility."),
            '        <h3 class="eyebrow" style="margin-top: var(--space-5);">A/B test results</h3>',
            '        <div class="grid grid--3">',
            '          <div class="metric-group"><h3>Banner Blue</h3>' + metrics([("847", "Clicks"), ("$60,005", "Revenue")]) + '</div>',
            '          <div class="metric-group"><h3>Banner Grey</h3>' + metrics([("1,402", "Clicks"), ("$190,112", "Revenue")]) + '</div>',
            '          <div class="metric-group"><h3>Control</h3>' + metrics([("350", "Clicks"), ("$1,991", "Revenue")]) + '</div>',
            '        </div>',
        ])),
        ("production", "Production", "\n".join([
            prose("To ensure correct delivery across multiple areas of the business, I wrote extensive documentation for both designers and engineers. The design rules fed into a banner builder that automated banner creation, so every merchandise team could generate HTML banners in minutes, not days."),
            gallery("officeworks", [(f"banner-builder-{i}.jpg", r, "Banner builder template") for i, r in enumerate([
                "2026/05/@300x-50-1-scaled.jpg", "2026/05/copy-2@300x-50-1-scaled.jpg",
                "2026/05/copy-3@300x-50-1-scaled.jpg", "2026/05/copy@300x-50-1-scaled.jpg"], 1)], contain=True),
        ])),
    ],
    ["swinburne", "proptrack"],
)

# ----- Swinburne
sw = BY_SLUG["swinburne"]
screens = ["2.44.36", "2.45.10", "2.45.59", "2.46.35", "2.47.12", "2.40.24", "2.41.31", "2.43.25", "2.43.49"]
case_study(
    sw,
    "Due to COVID-19, Swinburne’s students needed a platform to collaborate and stay informed. Over three months, our team of nine released an MVP that went on to win international awards.",
    ["UX research", "Rapid prototyping and coding", "Service design", "Design system build", "Outcomes reporting"],
    "Swinburne University of Technology",
    [
        ("problem", "Problem", "\n".join([
            prose("For many years the Swinburne app had gone unused, for a variety of reasons: outdated design and information, poor usability, and errors accessing content.",
                  "Student feedback suggested that adding single sign-on to all services within the app would greatly improve the experience, and customer support told us which features received the most enquiries."),
            gallery("swinburne", [("old-app-1.jpg", "2026/04/old-swinburne-app-1-1-scaled.jpg", "The previous Swinburne app"),
                                  ("old-app-2.jpg", "2026/04/old-swinburne-app-2-1-scaled.jpg", "The previous Swinburne app")], contain=True),
            callouts([("Users’ unmet needs", "Students needed to stay up to date with Canvas, the learning management system, and to download class material from the library while the physical library was closed. They also wanted reminders about upcoming classes, as managing their own time while studying from home was hard."),
                      ("Business needs", "The university needed a communication channel to inform students of regulation changes due to COVID, and a way to provide mental health, financial and academic support.")]),
            figure("swinburne", "app-features.jpg", "2026/04/App-Features-New-frame-1-scaled.jpg", "Prioritised app features"),
        ])),
        ("solution", "Solution", "\n".join([
            prose("Gathering data from the call centre, we noticed students were asking for six tools, which we prioritised as features for the first release.",
                  "Personalisation has become an integral part of designing a digital system, so we added a hello message to the MVP to build a connection with each student."),
            gallery("swinburne", [("data.jpg", "2026/04/swinburne-data-scaled.jpg", "Call centre data analysis"),
                                  ("information-architecture.jpg", "2026/04/swinburne-information-architecture-scaled.jpg", "Information architecture"),
                                  ("wireframe.jpg", "2026/04/swinburne-wireframe-scaled.jpg", "Wireframes"),
                                  ("grid-1.jpg", "2026/04/swinburne-grid-scaled.jpg", "Layout grid"),
                                  ("grid-2.jpg", "2026/04/swinburne-grid-2-scaled.jpg", "Layout grid")], contain=True),
        ])),
        ("production", "Production", "\n".join([
            prose("To create a winning experience, we designed a prioritised feature set and workflow, overlaid with analytics success and failure metrics to optimise future releases.",
                  "We created a design language system for efficiency, consistency and scale. It was based on the global brand guidelines and adapted for the best viewing on mobile devices."),
            gallery("swinburne", [("typography.jpg", "2026/04/Typography-main-1-scaled.jpg", "Design language system typography"),
                                  ("canvas-homescreen.jpg", "2026/04/Canvas-Homescreen-–-alt-right-–-1-1-scaled.jpg", "Canvas home screen")]
                    + [(f"app-screen-{i}.jpg", f"2026/04/Screen-Shot-2020-10-28-at-{t}-pm-1-scaled.jpg", "Swinburne app screen") for i, t in enumerate(screens, 1)], contain=True),
        ])),
        ("outcomes", "Outcomes", "\n".join([
            prose("After the initial soft launch, and compared with the previous year, we saw an exponential increase in daily usage and unique visitors with each new release.",
                  "The app was nominated by Modo Labs to compete in the worldwide Appademy Awards for 2020, and Swinburne received <strong>Best Overall Design</strong>. This was our MVP!"),
            figure("swinburne", "outcomes.jpg", "2026/04/outcomes-scaled.jpg", "Usage outcomes after launch"),
        ])),
    ],
    ["officeworks", "proptrack"],
)

# ----- PropTrack
pt = BY_SLUG["proptrack"]
case_study(
    pt,
    "PropTrack is the data arm of REA Group, created to power software for bankers and valuers in the property market. My role focused on discovery for B2B solutions for banks: identifying current challenges and unmet future needs in their valuation tools, through onsite workshops and interviews with core customers across Australia.",
    ["UX research", "Figma prototyping", "Service design", "Design system upgrade"],
    "REA Group — realestate.com.au",
    [
        ("problem", "Problem", "\n".join([
            prose("Property valuation processes between banks and valuation firms are fragmented, manual and difficult to manage at scale. Complex workflows — job requests, compliance requirements, status tracking and stakeholder communication — are often handled across disconnected systems, emails and spreadsheets. This leads to delays, reduced transparency, duplicated effort and increased operational risk.",
                  "I conducted around 16 semi-structured interviews with bank valuers and private lenders and brokers to build a current-state valuation journey for ANZ, with pain points and opportunities. This divided the work into four key pillars for delivery."),
            figure("proptrack", "experience-map.jpg", "2026/04/ANZ-Discovery-—-Final-Playback-Experience-Map-Valuation-Ordering-Experience-Map-1-scaled.jpg", "Valuation ordering experience map"),
            callouts([("Pillar 1 — Preparing the order", "Early alignment between lender or broker and borrower is critical. <br>Pains: time lost aligning expectations on property value; uncertainty around construction costs and benchmarks; inconsistent inputs leading to downstream issues."),
                      ("Pillar 2 — Ordering valuations", "Information must be accurately captured and submitted. <br>Pains: complex CDP decisioning requirements; manual document submission; missing or inconsistent information causing delays."),
                      ("Pillar 3 — Tracking progress", "Reports may be rejected due to non-value-based errors, such as address typos. <br>Pains: inefficient back-and-forth to correct minor issues; continued reliance on unclear email communication."),
                      ("Pillar 4 — Resolving report issues", "After submission, users wait for the valuation report. <br>Pains: rework required for a simple fix; inefficient back-and-forth; unclear email communication.")]),
        ])),
        ("solution", "Solution", "\n".join([
            gallery("proptrack", [("messaging-mapped.jpg", "2026/04/messaging-mapped-scaled.jpg", "Messaging mapped to progress steps"),
                                  ("notification-hierarchy.jpg", "2026/04/Notification-Hierarchy-scaled.jpg", "Notification hierarchy")], contain=True),
            prose("<strong>Customers’ unmet needs.</strong> Banks lack real-time visibility into valuation progress and quality, while valuation firms struggle with inconsistent briefs, shifting requirements and inefficient task coordination. As volume and regulatory pressure increase, these inefficiencies compound, affecting turnaround times, decision-making and customer experience. We mapped these progress steps to understand their relationships and the appropriate tasks.",
                  "I designed wireframes for a workflow-driven platform that connects all users through a shared system of record, replacing fragmented communication with structured, transparent processes. Smart forms guide users through capturing borrower estimates, cost of sale and LVR, with structured data capture aligned to CDP requirements, meaningful status updates instead of generic milestone emails, and clear indicators for blockers, actions and timelines."),
            gallery("proptrack", [(f"stage-{n}.jpg", f"2026/04/Stage-{n}-scaled.jpg", f"Wireframe stage {n}") for n in [1, 2, 3, 4]], contain=True),
            prose("These were turned into clickable prototypes and shown to the customer and end users, with every hypothesis validated or disproved. Everyone said the process gave them better visibility and more confidence during valuation processing."),
        ])),
        ("production", "Production", "\n".join([
            prose("I created high-fidelity screens and added new components to the REA design system: tables with expandable content and search, sort and filter capabilities. By transforming a fragmented, manual process into a connected workflow, the platform lets lenders, brokers and valuers work with greater clarity, speed and confidence — ultimately improving the lending experience for internal teams and borrowers alike.",
                  "This project highlighted the importance of designing for complex, multi-stakeholder workflows. Rather than focusing on individual features, success came from reducing ambiguity, improving shared understanding, and creating a single source of truth across the valuation lifecycle."),
            gallery("proptrack", [("home.jpg", "2026/04/home-scaled.jpg", "Platform home screen"),
                                  ("table.jpg", "2026/04/Table-2.jpg", "Expandable table component"),
                                  ("step-1.jpg", "2026/04/step-1-scaled.jpg", "Order flow step 1")], contain=True),
            metrics([("2.2", "Hours saved per task in processing time"), ("14+", "Hours saved per lender"), ("32%", "Reduction in email correspondence")], heading="Metrics observed"),
        ])),
    ],
    ["officeworks", "swinburne"],
)

# ----- Atlassian
at = BY_SLUG["atlassian"]
case_study(
    at,
    "Invite flows were designed for individual invitations. It’s easy to find and invite one person, but the features fall short when inviting a group — and previous research suggested that people starting a new project or board tend to invite whole teams.",
    ["Design sprint", "Prototyping", "Usability testing", "Design and flow", "Measurement"],
    "Atlassian — Growth team",
    [
        ("problem", "Problem", "\n".join([
            prose("When a team manager needs to invite several or all of their team members, they often switch to tools like Slack to make sure no one is missed. Relying on memory for names and emails leads to mistakes.",
                  "How might we help users quickly find their team and feel confident they’re inviting the right people, while building a solution that scales across the Atlassian platform?"),
            gallery("atlassian", [("interaction-design.svg", "2026/07/Jira-INTERACTION-DESIGN.svg", "Interaction design exploration"),
                                  ("spar.svg", "2026/07/Jira-SPAR.svg", "SPAR analysis"),
                                  ("user-flow.svg", "2026/07/Jira-USER-FLOW.svg", "User flow")], contain=True),
        ])),
        ("solution", "Solution", "\n".join([
            prose("Once we understood the pain points in the current flow and the system’s limitations, I designed a solution using Atlassian Design System components, ensuring consistency and scalability across the platform.",
                  "We tested the solution with five Jira admins to validate usability, alignment and understanding of the key concepts. Their feedback was incorporated, and all changes were prioritised with Product Management to align with broader product goals."),
            gallery("atlassian", [(f"core-invites-{n}.svg", f"2026/07/Core-invites-{n}.svg", f"Core invites design {n}") for n in [1, 2, 3, 4]], contain=True),
        ])),
        ("outcomes", "Outcomes", "\n".join([
            prose("With a Growth team mindset, we measured outcomes tied to the pain points identified across the Atlassian ecosystem. Key metrics included Monthly Active Users (MAU), which gave insight into retention and, compared with Daily Active Users (DAU), showed the frequency and consistency of engagement. We also tracked Direct Access (DA) — users joining teams via invitation rather than requesting access — as a signal of improved onboarding efficiency."),
            metrics([("+2%", "Monthly active users"), ("+5%", "Daily active users"), ("+22%", "Direct access"), ("2.9", "Users per site")], heading="A/B test results"),
            prose("<strong>Conclusion.</strong> Low MAU with high DAU indicates a small but highly engaged segment that uses this feature frequently.",
                  "From an admin perspective, user management remains a significant burden, accounting for around 48% of activity in the admin portal (by visit volume, not time spent). From a user perspective, streamlining access approvals saved an estimated 8 hours of end-user time per tenant, and enabled an average of 2.5 additional users per site to gain access more efficiently."),
        ])),
    ],
    ["officeworks", "swinburne"],
)

# ----- Rio Tinto (NDA placeholder — real content is NOT stored in this repo)
rt = BY_SLUG["rio-tinto"]
rt_body = f"""    <article>
      <header class="container cs-hero">
        <p class="eyebrow"><a href="/work/">Work</a> / Rio Tinto <span class="badge">NDA</span></p>
        <h1 class="cs-hero__title">A new global frontline experience.</h1>
        <p class="lead">Rio Tinto’s Digital Products team builds world-class products through human-centred value measurement and data-driven, intelligent technologies. As Lead Product Designer, I helped grow the team from 4 to 40 by establishing a clear vision, a strong team culture, a research hub and empowering tools.</p>
        <dl class="cs-meta">
          <div><dt>Role</dt><dd>Lead Product Designer</dd></div>
          <div><dt>Company</dt><dd>Rio Tinto — Digital Products</dd></div>
          <div><dt>Years</dt><dd>2023 – now</dd></div>
        </dl>
      </header>
      <div class="container cs-cover">{img(rt['cover'][0], rt['cover'][1], 'Rio Tinto — a new global frontline experience', eager=True)}</div>
      <div class="container section">
        <div class="nda">
          <h2 style="font-size: var(--fs-lg); margin-bottom: var(--space-3);">This case study is under NDA</h2>
          <p>The full case study is shared privately. <a href="/contact/">Drop me a line</a> and I’ll send you access.</p>
        </div>
      </div>
    </article>
"""
page("/work/rio-tinto/", "Rio Tinto", "Rio Tinto case study (under NDA): a new global frontline experience.", rt_body, active="/work/",
     og=f"/assets/img/{rt['cover'][0]}")

# --------------------------------------------------------------------------- about / résumé
EXP = [
    ("2023 – now", "Lead Product Designer", "Rio Tinto", "riotinto.com", "https://www.riotinto.com/", "rio-tinto",
     "Rio Tinto is a mining company with a vision to find better ways to provide the materials the world needs. I’m part of the Digital Products team, driving world-class product development and product thinking through human-centred value measurement and data-driven, intelligent technologies. As Lead, I was brought in to develop team capabilities as it grew from 4 to 40 members — establishing a clear vision, fostering a strong team culture, building a research hub and creating empowering tools."),
    ("2022 – 2023", "Senior Product Designer", "Atlassian", "atlassian.com", "https://www.atlassian.com/", "atlassian",
     "Atlassian helps teams unlock their full potential. I worked on the Growth team, using A/B testing to validate hypotheses for products across the business, following “The Atlassian Way”: Wonder, Explore, Make, Measure. Within a specialised team of four, we explored the problem space through research and quickly created solutions with a high likelihood of achieving the desired outcome — spanning research, strategy and detailed UI design to global standards."),
    ("2020 – 2022", "Senior Product Designer", "REA Group — PropTrack", "proptrack.com.au", "https://www.proptrack.com.au/", "proptrack",
     "PropTrack is the data arm of REA, powering software for bankers and valuers in the property market. My role focused on discovery for B2B solutions for banks, identifying current challenges and unmet future needs in their valuation tools, through onsite workshops with key stakeholders and extensive interviews with core customers across Australia."),
    ("2020 – 2021", "Senior Product Designer", "Service Victoria — Department of Premier and Cabinet", "service.vic.gov.au", "https://service.vic.gov.au/", None,
     "Service Victoria is a government agency designed to deliver digital services quickly and effectively. I was part of a newly formed team, “The Three Amigos” (business analyst, solution architect and product designer), assessing the feasibility, viability and desirability of incoming products through design sprints, rapid prototyping and usability testing. One of our projects received an honourable mention at the Premier’s Awards."),
    ("2019 – 2020", "UX Design Specialist", "Swinburne University", "swinburne.edu.au", "https://www.swinburne.edu.au/", "swinburne",
     "Swinburne is a world-class technology university, ranked among the top 300 globally. I was brought in to help deliver Adobe Experience Manager as a CMS, but when COVID hit, the Vice-Chancellor launched a task force to digitise classrooms. As part of an eight-person team, I helped design and build the official Swinburne app, integrated with the university’s LMS. It launched in just three months and won several global design awards."),
    ("2018 – 2019", "UX/UI Designer", "Officeworks", "officeworks.com.au", "https://www.officeworks.com.au/", "officeworks",
     "Officeworks is Australia’s leading retailer of office products for home, business and education, with over 150 stores nationwide. In the Conversion Rate Optimisation team, we used A/B testing to evaluate value early in discovery, developing MVPs and using Adobe Target to rapidly deliver and measure outcomes — combining qualitative and quantitative findings to recommend the best solutions and persuade stakeholders of their value."),
]
exp_html = "\n".join(f"""          <li class="reveal">
            <p class="timeline__when">{E(w)}</p>
            <div>
              <h3>{E(role)}</h3>
              <p class="timeline__org">{E(org)} · <a href="{url}" rel="noopener">{E(site)}</a></p>
              <p>{E(desc)}</p>
              {f'<p><a class="cta" style="font-size: var(--fs-sm);" href="/work/{cs}/">Read the case study</a></p>' if cs else ''}
            </div>
          </li>""" for w, role, org, site, url, cs, desc in EXP)

about = f"""    <section class="container home-hero">
      <p class="eyebrow">About</p>
      <h1 class="display" style="font-size: var(--fs-xl);">Hi, I'm Dave. How might we make the digital world easier?</h1>
    </section>
    <section class="container section--tight">
      <div class="grid grid--aside">
        <div>{img('about/portrait.jpg', '2026/05/Profile-inverse-scaled.jpg', 'Portrait of David Newman', cls='portrait')}</div>
        <div class="prose">
          <p>Born and raised in Sydney, I started in IT back when Unix shells were all the rage. I then spent 13 years in Europe, swapping code for colour theory and studying Fine Arts at the University of Valencia.</p>
          <p>Now I work in Strategic Product, where logic, empathy and chaos intersect. I help design products that make sense… and make people smile. Off-screen, you’ll find me at the piano, cooking paellas, or turning “short” trips into decade-long adventures.</p>
          <p><a class="button" href="/assets/david-newman-cv.pdf" download>Download CV (PDF)</a></p>
        </div>
      </div>
    </section>
    <section class="container section" aria-labelledby="exp-h">
      <h2 id="exp-h" class="eyebrow">Experience</h2>
      <ol class="timeline">
{exp_html}
      </ol>
    </section>
    <section class="container section--tight">
      <div class="grid grid--3">
        <div>
          <h2 class="eyebrow">Skills</h2>
          <ul class="plain-list">
            <li>AI service design</li><li>Product design thinking</li><li>Problem framing (Cynefin)</li><li>Strategic planning</li>
            <li>UX research — SFIA level 6</li><li>UX analysis — SFIA level 5</li><li>UX design — SFIA level 6</li>
            <li>Design Sprints</li><li>Interaction design</li><li>Typography</li>
          </ul>
        </div>
        <div>
          <h2 class="eyebrow">Education</h2>
          <ul class="plain-list">
            <li><strong>2017</strong><br>B.A. Communication Design (UX Design) — Monash University, Victoria, Australia</li>
            <li><strong>2010</strong><br>B.A. Fine Arts — Escola d’Art i Superior de Disseny, Valencia, Spain</li>
          </ul>
        </div>
        <div>
          <h2 class="eyebrow">Certificates</h2>
          <ul class="plain-list">
            <li><strong>2010</strong><br>CEFR C1 (advanced) Diploma in Spanish</li>
            <li><strong>2005</strong><br>MCSE (Microsoft Certified Solutions Expert), Canberra</li>
            <li><strong>2005</strong><br>CompTIA A+ certified, Canberra</li>
          </ul>
        </div>
      </div>
    </section>
"""
page("/about/", "About", "David Newman — Senior Product Designer. Experience at Rio Tinto, Atlassian, REA Group, Service Victoria, Swinburne University and Officeworks.", about, active="/about/")

# --------------------------------------------------------------------------- contact
contact = """    <section class="container home-hero">
      <p class="eyebrow">Contact</p>
      <h1 class="display" style="font-size: var(--fs-xl);">Let's work together.</h1>
    </section>
    <section class="container section--tight">
      <div class="grid grid--2">
        <div class="stack">
          <div>
            <h2 class="eyebrow">Say hello</h2>
            <p class="lead"><a href="mailto:hello@davidnewman.com.au">hello@davidnewman.com.au</a></p>
          </div>
          <div>
            <h2 class="eyebrow">Based in</h2>
            <p>Sunshine Coast, Queensland · Melbourne, Victoria</p>
          </div>
          <!-- TODO: add your LinkedIn URL
          <div>
            <h2 class="eyebrow">Elsewhere</h2>
            <p><a href="https://www.linkedin.com/in/YOUR-PROFILE/" rel="noopener">LinkedIn</a></p>
          </div> -->
        </div>
        <!-- Form posts to Formspree. Replace FORM_ID after creating a form at formspree.io -->
        <form class="form" action="https://formspree.io/f/FORM_ID" method="POST">
          <div class="field"><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="message">Message</label><textarea id="message" name="message" required></textarea></div>
          <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
          <p><button class="button" type="submit">Send message</button></p>
        </form>
      </div>
    </section>
"""
page("/contact/", "Contact", "Get in touch with David Newman, Product Design Strategist.", contact, active="/contact/")

# --------------------------------------------------------------------------- 404 + offline
nf = """    <section class="container home-hero">
      <p class="eyebrow">404</p>
      <h1 class="display" style="font-size: var(--fs-xl);">This page took a “short” trip and never came back.</h1>
      <p class="lead" style="margin-top: var(--space-4);">Try the <a href="/work/">work</a> page, or head <a href="/">home</a>.</p>
    </section>
"""
page("/404.html", "Page not found", "Page not found.", nf)
off = """    <section class="container home-hero">
      <p class="eyebrow">Offline</p>
      <h1 class="display" style="font-size: var(--fs-xl);">You're offline.</h1>
      <p class="lead" style="margin-top: var(--space-4);">Pages you've already visited are still available. Reconnect to see the rest.</p>
    </section>
"""
page("/offline.html", "Offline", "You are offline.", off)

# --------------------------------------------------------------------------- asset manifest for the pull script
IMAGES["assets/img/og-default.jpg"] = WP + "2026/05/Profile-inverse-scaled.jpg"
for f in ["Book", "BookItalic", "Medium", "Bold", "Black"]:
    IMAGES[f"assets/fonts/CircularStd-{f}.woff2"] = WP + f"fonts/CircularStd-{f}.woff2"
(ROOT / "scripts" / "assets.json").write_text(json.dumps(dict(sorted(IMAGES.items())), indent=2, ensure_ascii=False) + "\n")
print("pages written; assets:", len(IMAGES))
