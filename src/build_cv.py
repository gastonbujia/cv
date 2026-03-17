import os

import yaml
from jinja2 import Environment, FileSystemLoader


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SRC_DIR, "cv_data.yaml")
TEMPLATE_FILE = "cv_template.md.j2"
CV_BASENAME = "CV_Gaston_Bujia"
OUT_ES = os.path.join(SRC_DIR, f"{CV_BASENAME}.md")
OUT_EN = os.path.join(SRC_DIR, "english", f"{CV_BASENAME}_EN.md")


def build_cvs():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

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
