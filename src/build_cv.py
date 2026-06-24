import argparse
import glob
import os
import subprocess
import unicodedata

import yaml
from jinja2 import Environment, FileSystemLoader
from pylatexenc.latex2text import LatexNodes2Text
from pybtex.database import parse_file


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
DATA_FILE = os.path.join(SRC_DIR, "cv_data.yaml")
PUBLICATIONS_FILE = os.path.join(SRC_DIR, "publications.bib")
PROFILES_DIR = os.path.join(SRC_DIR, "profiles")
ACADEMIC_TEMPLATE_FILE = "cv_template.md.j2"
INDUSTRY_TEMPLATE_FILE = "cv_industry_template.md.j2"
CV_BASENAME = "CV_Gaston_Bujia"
ENGLISH_DIR = os.path.join(SRC_DIR, "english")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
HEADER_TEX = os.path.join(ROOT_DIR, "assets", "disable_hyphens.tex")
ACADEMIC_MARGIN = "1in"
INDUSTRY_MARGIN = "0.75in"
LATEX_TO_TEXT = LatexNodes2Text()
EXCLUDED_PUBLICATION_TYPES = {"phdthesis", "mastersthesis"}


def latex_to_text(value):
    if not value:
        return ""
    return LATEX_TO_TEXT.latex_to_text(value).strip()


def normalize_text(value):
    plain = latex_to_text(value)
    normalized = unicodedata.normalize("NFKD", plain)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch)).lower()


def format_initials(name_parts):
    initials = []
    for part in name_parts:
        text = latex_to_text(part)
        for token in text.replace("-", " ").split():
            initials.append(f"{token[0].upper()}.")
    return " ".join(initials)


def format_person(person):
    last_name = " ".join(latex_to_text(part) for part in person.last_names)
    initials = format_initials(person.first_names + person.middle_names)
    rendered = f"{last_name}, {initials}" if initials else last_name

    if "bujia" in normalize_text(last_name):
        return f"**{rendered}**"
    return rendered


def format_authors(persons):
    rendered = []
    for person in persons:
        if normalize_text(" ".join(person.last_names)) == "others":
            rendered.append("et al.")
            continue
        rendered.append(format_person(person))

    if not rendered:
        return ""
    if rendered[-1] == "et al.":
        if len(rendered) == 1:
            return rendered[0]
        return f"{', '.join(rendered[:-1])}, et al."
    if len(rendered) == 1:
        return rendered[0]
    if len(rendered) == 2:
        return f"{rendered[0]} & {rendered[1]}"
    return f"{', '.join(rendered[:-1])}, & {rendered[-1]}"


def format_venue(entry):
    fields = entry.fields
    venue = latex_to_text(
        fields.get("journal") or fields.get("booktitle") or fields.get("school") or ""
    )
    if not venue:
        return ""

    details = []
    volume = latex_to_text(fields.get("volume"))
    number = latex_to_text(fields.get("number"))
    pages = latex_to_text(fields.get("pages")).replace("--", "-")

    if volume and number:
        details.append(f"{volume}({number})")
    elif volume:
        details.append(volume)

    if pages:
        details.append(pages)

    if details:
        return f"**{venue}**, {', '.join(details)}"
    return f"**{venue}**"


def format_publication(entry, lang):
    authors = format_authors(entry.persons.get("author", []))
    year = latex_to_text(entry.fields.get("year")) or "s. f."
    title = latex_to_text(entry.fields.get("title")).rstrip(".")
    venue = format_venue(entry)
    preposition = "In" if lang == "en" else "En"

    if venue:
        return f"{authors} ({year}). *{title}.* {preposition} {venue}."
    return f"{authors} ({year}). *{title}.*"


def build_publications():
    if not os.path.exists(PUBLICATIONS_FILE):
        return []

    bibliography = parse_file(PUBLICATIONS_FILE)
    publications = []
    has_selected_entries = any(
        normalize_text(entry.fields.get("selected")) == "true"
        for entry in bibliography.entries.values()
    )

    for entry in bibliography.entries.values():
        if entry.type.lower() in EXCLUDED_PUBLICATION_TYPES:
            continue
        if has_selected_entries and normalize_text(entry.fields.get("selected")) != "true":
            continue

        year_text = latex_to_text(entry.fields.get("year"))
        try:
            year = int(year_text)
        except (TypeError, ValueError):
            year = 0

        title = latex_to_text(entry.fields.get("title"))
        publications.append(
            {
                "year": year,
                "title": title,
                "en": format_publication(entry, "en"),
                "es": format_publication(entry, "es"),
            }
        )

    publications.sort(key=lambda item: (-item["year"], item["title"].lower()))
    return [{"en": item["en"], "es": item["es"]} for item in publications]


def load_profiles():
    """Load every industry profile defined in src/profiles/*.yaml."""
    profiles = []
    for path in sorted(glob.glob(os.path.join(PROFILES_DIR, "*.yaml"))):
        with open(path, "r", encoding="utf-8") as f:
            profile = yaml.safe_load(f)
        if not profile or not profile.get("slug"):
            raise ValueError(f"Profile '{path}' is missing a 'slug' field.")
        profiles.append(profile)
    return profiles


def build_industry_context(profile, industry_headers):
    """Merge shared industry headers with the per-profile content into the
    `industry` object expected by cv_industry_template.md.j2."""
    return {
        "metadata": profile["metadata"],
        "title": profile["title"],
        "profile": profile["profile"],
        "headers": industry_headers,
        "experience_ids": profile["experience_ids"],
        "skill_groups": profile.get("skill_groups", []),
        "key_projects": profile["key_projects"],
        "teaching_publications_brief": profile["teaching_publications_brief"],
    }


def collect_outputs(data):
    """Build the full list of render jobs: academic (EN/ES) plus one industry
    CV per language for every profile under src/profiles/."""
    industry_headers = data.get("industry_headers", {})
    outputs = []

    for lang, suffix in (("es", ""), ("en", "_EN")):
        md_dir = ENGLISH_DIR if lang == "en" else SRC_DIR
        outputs.append({
            "template": ACADEMIC_TEMPLATE_FILE,
            "lang": lang,
            "context": data,
            "md_path": os.path.join(md_dir, f"{CV_BASENAME}{suffix}.md"),
            "pdf_path": os.path.join(OUTPUT_DIR, f"{CV_BASENAME}_{lang.upper()}.pdf"),
            "margin": ACADEMIC_MARGIN,
            "label": f"{lang.upper()} academic CV",
        })

    for profile in load_profiles():
        slug = profile["slug"]
        industry = build_industry_context(profile, industry_headers)
        context = {**data, "industry": industry}
        for lang, suffix in (("es", ""), ("en", "_EN")):
            md_dir = ENGLISH_DIR if lang == "en" else SRC_DIR
            outputs.append({
                "template": INDUSTRY_TEMPLATE_FILE,
                "lang": lang,
                "context": context,
                "md_path": os.path.join(md_dir, f"{CV_BASENAME}_{slug}{suffix}.md"),
                "pdf_path": os.path.join(OUTPUT_DIR, f"{CV_BASENAME}_{slug}_{lang.upper()}.pdf"),
                "margin": INDUSTRY_MARGIN,
                "label": f"{lang.upper()} industry CV ({slug})",
            })

    return outputs


def render_markdown(env, job):
    template = env.get_template(job["template"])
    rendered = template.render(lang=job["lang"], **job["context"])
    os.makedirs(os.path.dirname(job["md_path"]), exist_ok=True)
    with open(job["md_path"], "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Generated Markdown {job['label']}: {job['md_path']}")


def render_pdf(job):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    subprocess.run(
        [
            "pandoc",
            job["md_path"],
            "-H", HEADER_TEX,
            "-V", f"geometry:margin={job['margin']}",
            "-o", job["pdf_path"],
        ],
        check=True,
    )
    print(f"Generated PDF {job['label']}: {job['pdf_path']}")


def build_cvs(md_only=False):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    data["publications"] = build_publications()

    env = Environment(loader=FileSystemLoader(SRC_DIR))
    outputs = collect_outputs(data)

    for job in outputs:
        render_markdown(env, job)

    if md_only:
        return

    for job in outputs:
        render_pdf(job)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Gaston Bujia's CVs.")
    parser.add_argument(
        "--md-only",
        action="store_true",
        help="Only render the Markdown files; skip the Pandoc PDF step.",
    )
    args = parser.parse_args()
    build_cvs(md_only=args.md_only)
