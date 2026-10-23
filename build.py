"""Builds shawsuraj.com.
Writes dist/ (Vercel site, full HTML documents) and preview/ (Claude artifact preview).
Each page in src/pages has a first line of JSON metadata, then its HTML."""
import json, os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
CSS = open(os.path.join(SRC, "styles.css")).read()
JS = open(os.path.join(SRC, "app.js")).read()

GSAP = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>')
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700;12..96,800'
         '&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap">')
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23141b30'/%3E"
        "%3Ccircle cx='22' cy='22' r='7' fill='%231c7a50'/%3E%3Ccircle cx='42' cy='22' r='7' fill='%230c6f80'/%3E%3Ccircle cx='22' cy='42' r='7' fill='%23b8402b'/%3E%3Ccircle cx='42' cy='42' r='7' fill='%23a8660b'/%3E%3C/svg%3E")

PAGES = [("index", "Story"), ("guardian", "Guardian"), ("builder", "Builder"), ("researcher", "Researcher"), ("human", "Human")]
DOTS = {"guardian": "guard", "builder": "build", "researcher": "research", "human": "human"}

def nav(current):
    items = []
    for slug, name in PAGES:
        cur = ' aria-current="page"' if slug == current else ""
        dot = f'<i style="background:var(--{DOTS[slug]})"></i>' if slug in DOTS else ""
        items.append(f'<a href="{slug}.html"{cur}>{dot}{name}</a>')
    items.append('<a class="cta" href="#contact">Contact</a>')
    return ('<a class="skip" href="#main">Skip to content</a>\n<header class="top"><div class="wrap">'
            '<a class="mark" href="index.html" aria-label="Suraj Shaw, home">shaw <span class="dots" aria-hidden="true"><i></i><i></i><i></i><i></i></span></a>'
            '<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>'
            f'<nav class="nav" id="site-nav" aria-label="Site">{"".join(items)}</nav></div></header>')

FOOTER = '''<footer class="contact" id="contact"><div class="wrap">
<p class="label">Contact</p>
<h2>Last orders <span class="dots" aria-hidden="true"><i></i><i></i><i></i><i></i></span></h2>
<div class="mailrow"><a class="mail" id="mail" href="mailto:shaw@shawsuraj.com">shaw@shawsuraj.com</a><button class="copy" id="copy" type="button">Copy</button></div>
<ul class="elsewhere">
<li><a href="https://www.linkedin.com/in/shawsuraj/" target="_blank" rel="noopener me"><b>LinkedIn</b><span>in/shawsuraj</span></a></li>
<li><a href="https://github.com/shawsuraj" target="_blank" rel="noopener me"><b>GitHub</b><span>shawsuraj</span></a></li>
<li><a href="https://orcid.org/0009-0002-4482-8013" target="_blank" rel="noopener me"><b>ORCID</b><span>0009-0002-4482-8013</span></a></li>
<li><a href="https://www.instagram.com/shawsuraj/" target="_blank" rel="noopener me"><b>Instagram</b><span>@shawsuraj</span></a></li>
<li><a href="https://twitter.com/shawsurajss" target="_blank" rel="noopener me"><b>X</b><span>@shawsurajss</span></a></li>
</ul>
<div class="foot"><span>Suraj Shaw · London · Four worlds, one person.</span>
<nav aria-label="Worlds"><a href="guardian.html">Guardian</a><a href="builder.html">Builder</a><a href="researcher.html">Researcher</a><a href="human.html">Human</a></nav>
<span>Built by hand. No trackers.</span></div>
</div></footer>'''

LD = {"@context": "https://schema.org", "@type": "Person", "name": "Suraj Shaw", "alternateName": "Shaw", "url": "https://shawsuraj.com",
      "email": "mailto:shaw@shawsuraj.com", "jobTitle": "Computer Science student, founder and researcher",
      "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"},
      "alumniOf": [{"@type": "CollegeOrUniversity", "name": "University of Westminster"}, {"@type": "CollegeOrUniversity", "name": "Brunel University London"}],
      "sameAs": ["https://www.linkedin.com/in/shawsuraj/", "https://github.com/shawsuraj", "https://orcid.org/0009-0002-4482-8013",
                 "https://www.instagram.com/shawsuraj/", "https://twitter.com/shawsurajss", "https://worldchaosmap.app"]}

def head(meta, slug, full):
    url = "https://shawsuraj.com/" + ("" if slug == "index" else slug)
    h = [f'<title>{meta["title"]}</title>', '<meta name="claude:viewport-fit-sides" content="cover">',
         f'<meta name="description" content="{meta["desc"]}">', FONTS, f'<link rel="icon" href="{ICON}">']
    if full:
        h += [f'<link rel="canonical" href="{url}">', '<meta property="og:type" content="profile">',
              f'<meta property="og:title" content="{meta["title"]}">', f'<meta property="og:description" content="{meta["desc"]}">',
              f'<meta property="og:url" content="{url}">', '<meta property="og:image" content="https://shawsuraj.com/assets/og.jpg">', '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">', '<meta property="og:image:alt" content="Suraj Shaw. I build systems by day and make drinks by night.">',
              '<meta name="twitter:card" content="summary_large_image">', '<meta name="twitter:site" content="@shawsurajss">',
              '<meta name="theme-color" content="#eceee9" media="(prefers-color-scheme: light)">',
              '<meta name="theme-color" content="#0f1322" media="(prefers-color-scheme: dark)">']
        if slug == "index":
            h.append('<script type="application/ld+json">' + json.dumps(LD) + '</script>')
    h.append(f"<style>{CSS}</style>")
    return "\n".join(h)

def page(slug, full):
    raw = open(os.path.join(SRC, "pages", slug + ".html")).read()
    first, body = raw.split("\n", 1)
    meta = json.loads(first)
    content = f'{nav(slug)}\n<main id="main">\n{body}\n</main>\n{FOOTER}\n{GSAP}\n<script>{JS}</script>'
    if full:
        # clean URLs for the live site: index.html -> /, guardian.html -> /guardian
        content = re.sub(r'href="index\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1) or ""}"', content)
        content = re.sub(r'href="(guardian|builder|researcher|human)\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1)}{m.group(2) or ""}"', content)
        return (f'<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
                f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head(meta, slug, True)}\n</head>\n'
                f'<body class="{meta["body"]}">\n<script>document.body.className="{meta["body"]}";</script>\n{content}\n</body>\n</html>\n')
    # artifact preview: index has no wrapper, other pages need their own document
    if slug == "index":
        return head(meta, slug, False) + f'\n<script>document.body.className="{meta["body"]}";</script>\n' + content
    return (f'<!doctype html>\n<html lang="en-GB"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head(meta, slug, False)}</head>'
            f'<body class="{meta["body"]}">\n{content}\n</body></html>\n')

for target, full in (("dist", True), ("preview", False)):
    out = os.path.join(ROOT, target)
    os.makedirs(out, exist_ok=True)
    for slug, _ in PAGES:
        open(os.path.join(out, slug + ".html"), "w").write(page(slug, full))
    for d in ("assets", "cv"):
        shutil.copytree(os.path.join(ROOT, d), os.path.join(out, d), dirs_exist_ok=True)
    if full:
        for f in ("vercel.json", "robots.txt", "sitemap.xml"):
            shutil.copy(os.path.join(ROOT, f), out)
print("built")
