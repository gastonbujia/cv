import os
import unicodedata

import yaml
from jinja2 import Environment, FileSystemLoader
from pylatexenc.latex2text import LatexNodes2Text
from pybtex.database import parse_file


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SRC_DIR, "cv_data.yaml")
PUBLICATIONS_FILE = os.path.join(SRC_DIR, "publications.bib")
TEMPLATE_FILE = "cv_template.md.j2"
CV_BASENAME = "CV_Gaston_Bujia"
OUT_ES = os.path.join(SRC_DIR, f"{CV_BASENAME}.md")
OUT_EN = os.path.join(SRC_DIR, "english", f"{CV_BASENAME}_EN.md")
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


def build_cvs():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    data["publications"] = build_publications()

    env = Environment(loader=FileSystemLoader(SRC_DIR))
    template = env.get_template(TEMPLATE_FILE)

    md_es = template.render(lang="es", **data)
    with open(OUT_ES, "w", encoding="utf-8") as f:
        f.write(md_es)
    print(f"Generated Spanish CV: {OUT_ES}")

    md_en = template.render(lang="en", **data)
    os.makedirs(os.path.dirname(OUT_EN), exist_ok=True)
    with open(OUT_EN, "w", encoding="utf-8") as f:
        f.write(md_en)
    print(f"Generated English CV: {OUT_EN}")


if __name__ == "__main__":
    build_cvs()
