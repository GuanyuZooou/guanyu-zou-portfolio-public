"""Check the static portfolio and its repository publication boundary."""

from collections import Counter
from html.parser import HTMLParser
import json
from ipaddress import ip_address
from pathlib import Path, PurePosixPath
import re
import struct
import subprocess
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "1ba1baf"
BASE = "https://guanyuzooou.github.io/guanyu-zou-portfolio-public/"
PROFILE_CONTACT = {
    "email": "guanyuuzouuu@outlook.com",
    "linkedin": "https://www.linkedin.com/in/guanyu-zou/",
    "github": "https://github.com/GuanyuZooou",
}
SOCIAL = "assets/social-preview-v2.png"
PUBLIC_ROOT = {
    ".gitignore", ".nojekyll", "README.md", "CHANGELOG.md", "LICENSE",
    "robots.txt", "sitemap.xml", "script.js", "site-config.js", "styles.css",
    "portfolio-v2.css", "portfolio-v2.js",
}
SOURCE_SUFFIXES = {"content": {".html", ".json"}, "docs": {".md"}, "scripts": {".py"}}
TEXT_TYPES = {".css", ".html", ".js", ".json", ".md", ".py", ".svg", ".txt", ".xml"}
LEAK_PATTERNS = {
    "local filesystem reference": r"file:\/\/|(?:[A-Z]:[\\/])(?:Users|workspace|temp)[\\/]|\/(?:home|Users|private|mnt|workspace)\/[\w.-]+|Dropbox[\\/]",
    "old private portfolio or asset reference": r"portfolio-dev|V3_with_Codex_Brief|Privacy_Review_2026|assets/(?:research|thumbnails)/",
    "credential or signed URL": r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{30,}|[?&](?:X-Amz-Signature|access_token)=",
}
MAIN = re.compile(r"<main\b[^>]*>(.*?)</main>", re.IGNORECASE | re.DOTALL)
DISCLOSURE = (
    "Detailed research findings are currently restricted. This portfolio provides a high-level overview "
    "of the work, focusing on the methodologies, technical capabilities and potential engineering applications."
)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.title_parts = []
        self.in_title = False
        self.feed(text)
        self.close()
        self.ids = Counter(attrs["id"] for _, attrs in self.elements if "id" in attrs)
        self.title = "".join(self.title_parts).strip()

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, {name: value or "" for name, value in attrs}))
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, text):
        if self.in_title:
            self.title_parts.append(text)

    def metadata(self, key):
        return [
            attrs.get("content", "") for tag, attrs in self.elements
            if tag == "meta" and (attrs.get("name") == key or attrs.get("property") == key)
        ]


def git(*arguments):
    return subprocess.check_output(["git", "-C", str(ROOT), *arguments], encoding="utf-8")


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def local_target(value, source):
    """Resolve a URL as GitHub Pages will resolve it under its repository path."""
    parsed = urlsplit(urljoin(urljoin(BASE, source), value))
    deployment = urlsplit(BASE)
    if parsed.netloc != deployment.netloc or not parsed.path.startswith(deployment.path):
        return None
    path = unquote(parsed.path.removeprefix(deployment.path))
    if not path or path.endswith("/"):
        path += "index.html"
    if "\\" in path or ".." in PurePosixPath(path).parts:
        raise ValueError("a public URL resolves outside the portfolio")
    return path, unquote(parsed.fragment)


def is_public_host(hostname):
    if not hostname or "." not in hostname or hostname.endswith((".local", ".internal", ".test", ".invalid")):
        return False
    try:
        return ip_address(hostname).is_global
    except ValueError:
        return True


def media_entries(project):
    yield from (project[key] for key in ("media", "feature_media") if key in project)
    yield from project.get("gallery", [])


def png_size(path):
    with (ROOT / path).open("rb") as image:
        header = image.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("invalid PNG header")
    return struct.unpack(">II", header[16:])


def verify():
    issues = []
    catalogue = json.loads(read("content/projects.en.json"))
    config = json.loads(read("site-config.js").split("=", 1)[1].strip().removesuffix(";"))
    if config.get("publicBaseUrl") != BASE or not config.get("contactApproved"):
        issues.append("site-config.js: unexpected public URL or absent contact approval")
    for key, value in PROFILE_CONTACT.items():
        if config.get(key) != value:
            issues.append(f"site-config.js: {key} differs from the approved public contact")

    projects = catalogue["projects"]
    expected_pages = {"index.html", *(f'{project["id"]}.html' for project in projects)}
    existing = {path.name for path in ROOT.glob("*.html")}
    if existing != expected_pages:
        issues.append(f"catalogue/page mismatch: missing {sorted(expected_pages - existing)}, extra {sorted(existing - expected_pages)}")
    page_names = expected_pages & existing
    texts = {name: read(name) for name in page_names}
    pages = {name: Page(text) for name, text in texts.items()}

    baseline_paths = git("ls-tree", "-r", "--name-only", BASELINE).splitlines()
    baseline_assets = {name for name in baseline_paths if name.startswith("assets/")}
    baseline_cases = {name for name in baseline_paths if name.endswith(".html") and name != "index.html"}
    legacy_cases = {f'{project["id"]}.html' for project in projects if project.get("legacy")}
    if legacy_cases != baseline_cases:
        issues.append(f"legacy case routes must match {BASELINE}: {sorted(baseline_cases)}")
    media = {}
    for project in projects:
        for entry in media_entries(project):
            path = entry.get("file", "")
            if not re.fullmatch(r"assets/projects/[a-z0-9][a-z0-9-]*\.(?:png|webp|jpe?g|svg)", path):
                issues.append(f'{project["id"]}: invalid public media path {path!r}')
            if not all(entry.get(key, "").strip() for key in ("alt", "caption", "license")):
                issues.append(f"{path}: media requires alt text, caption and recorded licence")
            if not (entry.get("source") or entry.get("source_url")):
                issues.append(f"{path}: missing media provenance")
            if path in media and entry != media[path]:
                issues.append(f"{path}: inconsistent catalogue records")
            media[path] = entry

    allowed_assets = baseline_assets | set(media) | {SOCIAL}
    actual_assets = {path.relative_to(ROOT).as_posix() for path in (ROOT / "assets").rglob("*") if path.is_file()}
    if actual_assets != allowed_assets:
        issues.append(f"asset allowlist mismatch: missing {sorted(allowed_assets - actual_assets)}, extra {sorted(actual_assets - allowed_assets)}")
    if SOCIAL in actual_assets and png_size(SOCIAL) != (1200, 630):
        issues.append(f"{SOCIAL}: expected 1200 × 630 pixels")

    public_paths = expected_pages | allowed_assets | PUBLIC_ROOT
    tracked = set(git("ls-files", "-z", "--cached", "--others", "--exclude-standard").split("\0")) - {""}
    unexpected = []
    for path_string in sorted(tracked):
        path = PurePosixPath(path_string)
        source = path.parts[0] in SOURCE_SUFFIXES and path.suffix in SOURCE_SUFFIXES[path.parts[0]]
        if not source and path_string not in public_paths:
            unexpected.append(path_string)
        candidate = ROOT / path
        if candidate.is_symlink() or (candidate.exists() and not candidate.resolve().is_relative_to(ROOT)):
            issues.append(f"{path}: symlinks and paths that escape the checkout are outside the publication boundary")
            continue
        if candidate.is_file() and path.suffix in TEXT_TYPES and path_string != "scripts/verify.py":
            text = candidate.read_text(encoding="utf-8")
            for label, pattern in LEAK_PATTERNS.items():
                if re.search(pattern, text, flags=re.IGNORECASE):
                    issues.append(f"{path}: potential {label}")
    if unexpected:
        issues.append(f"unapproved files eligible for commit/publication: {unexpected}")

    seen_images = set()
    catalogue_alt_used = set()
    internal = 0
    external = set()
    canonicals = set()
    for name, page in pages.items():
        expected_url = urljoin(BASE, "" if name == "index.html" else name)
        canonicals.add(expected_url)
        values = [
            attrs.get("href", "") for tag, attrs in page.elements
            if tag == "link" and "canonical" in attrs.get("rel", "").split()
        ]
        if values != [expected_url]:
            issues.append(f"{name}: canonical must be {expected_url}")
        for key, expected in {
            "og:type": "website",
            "og:title": page.title,
            "og:url": expected_url,
            "og:image": urljoin(BASE, SOCIAL),
            "og:image:width": "1200",
            "og:image:height": "630",
            "twitter:card": "summary_large_image",
            "twitter:title": page.title,
            "twitter:image": urljoin(BASE, SOCIAL),
        }.items():
            if page.metadata(key) != [expected]:
                issues.append(f"{name}: incorrect or duplicate {key}")
        description = page.metadata("description")
        if len(description) != 1 or not description[0].strip():
            issues.append(f"{name}: missing or duplicate description")
        if not page.title or page.metadata("twitter:description") != description or page.metadata("og:description") != description:
            issues.append(f"{name}: missing title or mismatched share description")
        image_alt = page.metadata("og:image:alt")
        if len(image_alt) != 1 or not image_alt[0].strip():
            issues.append(f"{name}: missing social image description")
        if any("noindex" in value.lower() for value in page.metadata("robots")):
            issues.append(f"{name}: unexpected noindex")
        if len([tag for tag, _ in page.elements if tag == "h1"]) != 1:
            issues.append(f"{name}: expected one h1")
        if any(count != 1 for count in page.ids.values()):
            issues.append(f"{name}: duplicate anchor ids")
        if name in {"index.html", "fem.html", "ml.html", "imaging.html"} and DISCLOSURE not in texts[name]:
            issues.append(f"{name}: approved Research Disclosure text is missing")

        for tag, attrs in page.elements:
            if tag == "img":
                if not attrs.get("alt", "").strip() or not attrs.get("src", "").strip():
                    issues.append(f"{name}: image missing descriptive alt or src")
            if tag == "base":
                issues.append(f"{name}: an HTML base element would change link resolution")
            references = [(key, attrs[key]) for key in ("href", "src", "poster", "action") if key in attrs]
            if "srcset" in attrs:
                references.extend(("src", item.split()[0]) for item in attrs["srcset"].split(",") if item.strip())
            for key, value in references:
                parsed = urlsplit(value)
                if not value or parsed.scheme not in {"", "https", "mailto"} or value.startswith("//"):
                    issues.append(f"{name}: unsupported or empty link {value!r}")
                    continue
                if parsed.scheme == "mailto":
                    if value != "mailto:" + PROFILE_CONTACT["email"]:
                        issues.append(f"{name}: unexpected email contact")
                    continue
                target = local_target(value, name)
                if target is None:
                    if key != "href" or not is_public_host(parsed.hostname) or parsed.username or parsed.password:
                        issues.append(f"{name}: unsupported external resource {value!r}")
                    else:
                        external.add(value)
                    continue
                internal += 1
                path, fragment = target
                if path not in public_paths or not (ROOT / path).is_file():
                    issues.append(f"{name}: internal {key} {value!r} targets a missing or unapproved file")
                if path in pages and fragment and fragment not in pages[path].ids:
                    issues.append(f"{name}: internal link {value!r} targets an unknown anchor")
                if tag in {"img", "source"} and key == "src":
                    seen_images.add(path)
                    if path not in allowed_assets:
                        issues.append(f"{name}: image outside the approved asset set: {path}")
                    if tag == "img" and path in media and attrs.get("alt") == media[path].get("alt"):
                        catalogue_alt_used.add(path)

    if set(media) - seen_images:
        issues.append(f"unused catalogue media: {sorted(set(media) - seen_images)}")
    if set(media) - catalogue_alt_used:
        issues.append(f"media without a rendered catalogue description: {sorted(set(media) - catalogue_alt_used)}")
    for name in sorted(baseline_cases):
        old_body = MAIN.search(git("show", f"{BASELINE}:{name}"))
        new_body = MAIN.search(texts.get(name, ""))
        if not old_body or not new_body or old_body.group(1).strip() != new_body.group(1).strip():
            issues.append(f"{name}: public research body differs from {BASELINE}")

    sitemap = ROOT / "sitemap.xml"
    if sitemap.is_file():
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locations = [element.text for element in ElementTree.parse(sitemap).getroot().findall(f"{namespace}url/{namespace}loc")]
        if Counter(locations) != Counter(canonicals):
            issues.append("sitemap.xml: locations must match the unique page canonicals")
    else:
        issues.append("sitemap.xml: missing")

    if issues:
        raise SystemExit("Portfolio verification failed:\n- " + "\n- ".join(issues))
    print(f"Verified {len(pages)} pages, {internal} internal references, {len(external)} distinct external links, and {len(actual_assets)} approved assets.")
    print(f"Confirmed metadata, sitemap, publication boundary and unchanged legacy bodies from {BASELINE}. External link availability is a separate check.")


if __name__ == "__main__":
    verify()
