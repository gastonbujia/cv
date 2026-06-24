# CV Automation Pipeline

This repository contains the source data and scripts for generating perfectly synchronized bi-lingual (English and Spanish) versions of Gaston Bujia's CV.

The pipeline separates content data from layout and design, ensuring that as new experiences are added, both language versions and PDF files are updated seamlessly and accurately without duplication of effort.

The active generation flow is Markdown -> Pandoc -> LaTeX -> PDF. The generated Markdown files are build artifacts and should not be edited manually.

## Repository Structure

- `src/cv_data.yaml`: **The source of truth** for shared facts: contact info, the full experience pool, education, skills, academic headers, and the shared industry section labels (`industry_headers`).
- `src/publications.bib`: Source of truth for the publications list.
- `src/profiles/*.yaml`: **One file per industry profile** (e.g. `data_science.yaml`). Each declares how that profile presents the shared data: its `slug` (used in the output filename), title, summary, which experience items to show and in what order (`experience_ids`), key projects, and the teaching/publications brief. Add a new profile by dropping a new file here — no code changes needed.
- `src/cv_template.md.j2`: Jinja2 template for the academic CV.
- `src/cv_industry_template.md.j2`: Jinja2 template shared by all industry profiles.
- `src/build_cv.py`: Python script that reads the YAML data and `publications.bib`, discovers every profile, renders the Markdown files **and** invokes Pandoc to produce the PDFs. Use `--md-only` to skip the PDF step.
- `generate_pdf.sh` / `generate_pdf.ps1`: Thin wrappers that check for `python`/`pandoc` and run `build_cv.py`.
- `src/CV_Gaston_Bujia.md` / `src/english/CV_Gaston_Bujia_EN.md`: Auto-generated academic Markdown (ES / EN).
- `src/CV_Gaston_Bujia_<slug>.md` / `src/english/CV_Gaston_Bujia_<slug>_EN.md`: Auto-generated industry Markdown per profile (ES / EN).
- `output/`: Directory where the final PDF files are generated (`CV_Gaston_Bujia_EN/ES.pdf` and `CV_Gaston_Bujia_<slug>_EN/ES.pdf`).
- `src/previous/`: Historical LaTeX material kept only as reference. It is not part of the current build.

The generated Markdown files are build artifacts — never edit them by hand. To change content, edit `cv_data.yaml`, `publications.bib`, or the relevant profile, then re-run the build.

## Requirements

The generation pipeline requires Python 3 and Pandoc. To install the required Python libraries, run:

```bash
pip install -r requirements.txt
```

## Modifying the CV Data

To update or add new items to the CV, you **do not** need to edit the separate Markdown files manually.

1. Open `src/cv_data.yaml`.
2. Locate the section you wish to update (e.g., `experience`, `education`, `skills`).
3. Add or modify the data. For text that varies by language, ensure both `en` and `es` keys are populated.
4. Save the file.

Publications are maintained separately in `src/publications.bib` and injected automatically during the build.

### Adding an industry profile

To create a new tailored industry CV (EN + ES), copy an existing file in `src/profiles/` and adjust it:

1. Set a unique `slug` (e.g. `MLEngineer`); it becomes the output filename `CV_Gaston_Bujia_<slug>_EN/ES.pdf`.
2. Write the profile-specific `title` and `profile` summary in both languages.
3. List the `experience_ids` to show, in the order you want them (they reference `experience[].id` in `cv_data.yaml`).
4. Fill in `key_projects` and `teaching_publications_brief`.

Re-run the build and the new profile's PDFs appear automatically — no code or script changes required.

*Example item format:*
```yaml
  - id: "new_job"
    title:
      en: "Senior Data Scientist"
      es: "Data Scientist Semi-Senior"
    company:
      en: "Example Corp"
      es: "Example Corp"
...
```

## Generating the Final CVs

To generate both the Markdown updates and compile the new PDFs, simply execute the main shell script from the repository root:

```bash
./generate_pdf.sh
```

This command will:
1. Run `build_cv.py` to rewrite the `.md` files based on the latest `cv_data.yaml`.
2. Execute Pandoc to convert the newly built Markdown files into high-quality PDFs placed in the `output/` directory.

On Windows/PowerShell, use:

```powershell
python -m pip install -r requirements.txt
.\generate_pdf.ps1
```

## Automated CI/CD (GitHub Actions)

This repository includes a GitHub Actions workflow (`.github/workflows/generate_cv.yml`) that completely automates CV generation.

Whenever a push is made to the `main` branch containing changes to `src/cv_data.yaml` (or the generation scripts), GitHub Actions will automatically:
1. Setup a Python environment and install the required dependencies (`pyyaml`, `jinja2`).
2. Install Pandoc and LaTeX essentials.
3. Execute `./generate_pdf.sh` to build fresh Markdown files and PDFs.
4. Auto-commit and push the newly generated files back to the repository.

You simply edit the data, push your commit, and let GitHub handle the rest!
