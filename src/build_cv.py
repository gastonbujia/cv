import yaml
from jinja2 import Environment, FileSystemLoader
import os

# Define paths relative to this script
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SRC_DIR, "cv_data.yaml")
TEMPLATE_FILE = "cv_template.md.j2"
OUT_ES = os.path.join(SRC_DIR, "CV_Gustavo_Juantorena_2026.md")
OUT_EN = os.path.join(SRC_DIR, "english", "CV_Gustavo_Juantorena_2026_EN.md")

def build_cvs():
    # Load YAML data
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(SRC_DIR))
    template = env.get_template(TEMPLATE_FILE)

    # Render Spanish CV
    md_es = template.render(lang="es", **data)
    with open(OUT_ES, "w", encoding="utf-8") as f:
        f.write(md_es)
    print(f"✅ Generated Spanish CV: {OUT_ES}")

    # Render English CV
    md_en = template.render(lang="en", **data)
    # Ensure english dir exists (it does, but good practice)
    os.makedirs(os.path.dirname(OUT_EN), exist_ok=True)
    with open(OUT_EN, "w", encoding="utf-8") as f:
        f.write(md_en)
    print(f"✅ Generated English CV: {OUT_EN}")

if __name__ == "__main__":
    build_cvs()
