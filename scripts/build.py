"""Build static GitHub Pages HTML from the English catalogue. Standard library only."""

import argparse
import html
import json
from pathlib import Path
import re
from string import Template
from urllib.parse import urljoin
from xml.sax.saxutils import escape as xml_escape


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
CATALOGUE = json.loads((CONTENT / "projects.en.json").read_text(encoding="utf-8"))
PROJECTS = {item["id"]: item for item in CATALOGUE["projects"]}
CATEGORIES = CATALOGUE["categories"]
CATEGORY_LABEL = {item["id"]: item["label"] for item in CATEGORIES}
CONFIG = json.loads((ROOT / "site-config.js").read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";"))
BASE = CONFIG["publicBaseUrl"]
GITHUB = "https://github.com/GuanyuZooou/"
LAYOUT = Template((CONTENT / "layout.html").read_text(encoding="utf-8"))
HOME = Template((CONTENT / "home.en.html").read_text(encoding="utf-8"))


def esc(value):
    return html.escape(value, quote=True)


def link(label, url, css=""):
    cls = f' class="{esc(css)}"' if css else ""
    return f'<a{cls} href="{esc(url)}">{esc(label)}</a>'


def contact_links(css):
    if not CONFIG.get("contactApproved"):
        return ""
    return "\n".join(
        link(label, prefix + CONFIG[key], css)
        for key, label, prefix in (("email", "Email", "mailto:"), ("linkedin", "LinkedIn", ""), ("github", "GitHub", ""))
        if CONFIG.get(key)
    )


def header(home=False):
    prefix = "" if home else "index.html"
    nav = "\n".join(link(label, prefix + "#" + anchor) for anchor, label in (
        ("work", "Projects"), ("approach", "Method"), ("about", "About"), ("contact", "Contact")
    ))
    return f'''<a class="skip-link" href="#main-content">Skip to main content</a>
<header class="v2-header">
  <div class="v2-wrap v2-header-inner">
    <a class="v2-brand" href="index.html" aria-label="Guanyu Zou home">
      <span class="v2-brand-mark" aria-hidden="true">GZ</span>
      <span><strong>Guanyu Zou</strong><small>SCIENCE × APPLICATION</small></span>
    </a>
    <button type="button" class="v2-menu-toggle" aria-expanded="false" aria-controls="portfolio-navigation" hidden>Menu</button>
    <nav id="portfolio-navigation" class="v2-nav" aria-label="Main navigation">{nav}</nav>
  </div>
</header>'''


def footer():
    return f'''<footer class="v2-footer">
  <div class="v2-wrap"><span>Guanyu Zou <span class="v2-footer-separator">·</span> SCIENCE × APPLICATION</span>
    <nav aria-label="Contact links">{contact_links("")}</nav>
  </div>
</footer>'''


def page(title, description, path, body, home=False):
    return LAYOUT.substitute(
        language=esc(CATALOGUE["language"]),
        title=esc(title),
        description=esc(description),
        canonical=esc(urljoin(BASE, path)),
        social=esc(urljoin(BASE, "assets/social-preview-v2.png")),
        header=header(home),
        body="\n".join(line.rstrip() for line in body.splitlines()),
        footer=footer(),
    )


def case_path(project):
    return project["id"] + ".html"


def source_url(project, target):
    if target.startswith("https://"):
        return target
    return f'{GITHUB}{project["repo"]}/blob/{project["revision"]}/{target}'


def picture(media):
    return f'<img src="{esc(media["file"])}" alt="{esc(media["alt"])}" loading="lazy" decoding="async">'


def figure(project, media):
    source = media.get("source_url") or source_url(project, media["source"])
    return f'''<figure class="v2-case-figure">
  {link_image(media)}
  <figcaption>{esc(media["caption"])}
    <span>{link("Open full-size image", media["file"])} <span aria-hidden="true">·</span> {link("Source", source)}</span>
  </figcaption>
</figure>'''


def link_image(media):
    return f'<a href="{esc(media["file"])}" aria-label="{esc("Open full-size image: " + media["alt"])}">{picture(media)}</a>'


def featured_card(project):
    media = project.get("feature_media") or project["media"]
    copy = project["featured_copy"]
    title = esc(project["title"])
    actions = [f'<a href="{case_path(project)}" aria-label="Case study: {title}">Case study</a>']
    if project.get("demo"):
        actions.append(f'<a href="{esc(project["demo"])}" aria-label="Live demo: {title}">Live demo</a>')
    return f'''<article class="v2-feature-card">
  <div class="v2-feature-image">{picture(media)}</div>
  <div class="v2-feature-body">
    <h3>{title}</h3>
    <p class="v2-feature-problem">{esc(copy["problem"])}</p>
    <p class="v2-feature-proof">{esc(copy["proof"])}</p>
    <div class="v2-feature-actions">{"".join(actions)}</div>
  </div>
</article>'''

def row(project):
    return f'''<li class="v2-project-row">
  <div><h4>{link(project["title"], case_path(project))}</h4><p>{esc(project["summary"])}</p></div>
  <span class="v2-project-state">{esc(project["status"])}</span>
</li>'''


def home_page():
    groups = []
    for category in CATEGORIES:
        key = category["id"]
        anchor = "lab" if key == "innovation" else key
        label = esc(category["label"])
        projects = "\n".join(row(p) for p in PROJECTS.values() if p["category"] == key)
        groups.append(f'''<section class="v2-project-group" data-project-group="{key}" id="{anchor}" aria-labelledby="{key}-heading">
  <div class="v2-project-group-intro">
    <h3 id="{key}-heading">
      <span data-category-label>{label}</span>
      <button type="button" class="v2-category-toggle" aria-expanded="true" aria-controls="{key}-projects" hidden>{label}<span aria-hidden="true"></span></button>
    </h3>
    <p>{esc(category["description"])}</p>
  </div>
  <ul id="{key}-projects">{projects}</ul>
</section>''')
    body = HOME.substitute(
        featured="\n".join(featured_card(PROJECTS[key]) for key in CATALOGUE["featured"]),
        groups="\n".join(groups),
        contacts=contact_links("v2-button"),
    )
    return page(CATALOGUE["title"], CATALOGUE["description"], "", body, home=True)

def anchor(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def case_page(project):
    category = project["category"]
    group = "lab" if category == "innovation" else category
    actions = [link("GitHub repository", GITHUB + project["repo"], "v2-button")]
    if project.get("demo"):
        actions.insert(0, link("Open live demo", project["demo"], "v2-button v2-button-primary"))
    media = [project["media"]] if "media" in project else []
    media += project.get("gallery", [])
    sections = []
    for section in project["sections"]:
        citations = [link(label, source_url(project, source)) for label, source in section.get("evidence", [])]
        evidence = '<ul class="v2-evidence-links">' + "".join(f"<li>{item}</li>" for item in citations) + "</ul>" if citations else ""
        sections.append(f'''<section class="v2-case-section" id="{anchor(section["title"])}">
  <h2>{esc(section["title"])}</h2>
  <p>{esc(section["text"])}</p>
  {evidence}
</section>''')
    side_links = "".join(f'<li>{link(s["title"], "#" + anchor(s["title"]))}</li>' for s in project["sections"])
    tags = "".join(f"<li>{esc(tag)}</li>" for tag in project["stack"])
    related = ""
    if project.get("related"):
        other = PROJECTS[project["related"]]
        relation = "Companion skill for applying the method" if category == "knowledge" and project["id"] == "writing-method" else "Companion skill for extracting methods"
        related = f'<aside class="v2-related"><p class="v2-kicker">{relation}</p>{link(other["title"], case_path(other))}</aside>'
    body = f'''<header class="v2-case-header">
  <div class="v2-wrap">
    {link(CATEGORY_LABEL[category], "index.html#" + group, "v2-text-link")}
    <p class="v2-kicker">{esc(project["status"])}</p>
    <h1>{esc(project["title"])}</h1>
    <p class="v2-lead">{esc(project["summary"])}</p>
    <ul class="v2-tags" aria-label="Technologies and methods">{tags}</ul>
    <div class="v2-actions">{"".join(actions)}</div>
  </div>
</header>
<div class="v2-wrap v2-case-content">
  <aside class="v2-case-aside"><p class="v2-kicker">In this case</p><nav aria-label="Case sections"><ul>{side_links}</ul></nav>
    <p class="v2-reviewed">Source snapshot <time datetime="{esc(project["updated"])}">{esc(project["updated"])}</time></p>
  </aside>
  <div class="v2-case-main">
    <p class="v2-case-outcome">{esc(project["outcome"])}</p>
    {figure(project, media[0]) if media else ""}
    {"".join(sections)}
    {"".join(figure(project, image) for image in media[1:])}
    {related}
  </div>
</div>'''
    return page(project["title"] + " | Guanyu Zou", project["summary"], case_path(project), body)


DOCTORAL_CASES = (
    ("fem.html", "FEM"),
    ("ml.html", "Scientific ML"),
    ("imaging.html", "3D imaging"),
)


def doctoral_navigation(current):
    overview = link("Doctoral research", "index.html#doctoral-research")
    cases = []
    for target, label in DOCTORAL_CASES:
        attributes = ' aria-current="page"' if target == current else ""
        cases.append(f'<a href="{target}"{attributes}>{label}</a>')
    return (
        '<nav class="v2-research-nav" aria-label="Doctoral research">'
        f'<div class="v2-wrap">{overview}<ul>'
        + "".join(f"<li>{item}</li>" for item in cases)
        + "</ul></div></nav>"
    )


def legacy_page(path):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'<a class="skip-link".*?</header>', lambda _: header(), text, count=1, flags=re.S)
    if path.name in dict(DOCTORAL_CASES):
        # Replace a previous generated trail before inserting the current one.
        text = re.sub(r'<nav class="v2-research-nav".*?</nav>', "", text, count=1, flags=re.S)
        text = text.replace("</header>", "</header>" + doctoral_navigation(path.name), 1)
    text = re.sub(r'<footer class="(?:footer|v2-footer)".*?</footer>', lambda _: footer(), text, count=1, flags=re.S)
    if "portfolio-v2.css" not in text:
        text = text.replace("</head>", '<link rel="stylesheet" href="portfolio-v2.css"><script src="portfolio-v2.js" defer></script></head>', 1)
    text = text.replace("assets/social-preview.png", "assets/social-preview-v2.png")
    text = text.replace('property="og:site_name" content="Guanyu Zou | Research &amp; Engineering Portfolio"', 'property="og:site_name" content="Guanyu Zou · Research &amp; Technology"')
    text = text.replace('content="Guanyu Zou — multiphysics simulation, scientific machine learning and 3D microstructure analysis"', 'content="Guanyu Zou, research and technology portfolio"')
    return text


def build(check):
    outputs = {"index.html": home_page()}
    for project in PROJECTS.values():
        name = case_path(project)
        outputs[name] = legacy_page(ROOT / name) if project.get("legacy") else case_page(project)
    urls = [urljoin(BASE, "" if name == "index.html" else name) for name in outputs]
    outputs["sitemap.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{xml_escape(url)}</loc></url>\n" for url in urls
    ) + "</urlset>\n"
    stale = []
    for name, text in outputs.items():
        path = ROOT / name
        if check:
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                stale.append(name)
        else:
            path.write_text(text, encoding="utf-8", newline="\n")
    if stale:
        raise SystemExit(f"Run python scripts/build.py. Stale outputs: {', '.join(stale)}")
    print(f"{'Verified' if check else 'Built'} {len(outputs) - 1} HTML pages and sitemap.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check that generated files are current.")
    build(parser.parse_args().check)
