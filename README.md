# CV Automation Pipeline

This repository contains the source data and scripts for generating perfectly synchronized bi-lingual (English and Spanish) versions of Gustavo Juantorena's CV.

The pipeline separates content data from layout and design, ensuring that as new experiences are added, both language versions and PDF files are updated seamlessly and accurately without duplication of effort.

## Repository Structure

- `src/cv_data.yaml`: **The source of truth.** All CV content resides here.
- `src/cv_template.md.j2`: The Jinja2 template dictating the layout of the Markdown file.
- `src/build_cv.py`: Python script that reads the YAML data and renders the template to produce the English and Spanish Markdown files.
- `generate_pdf.sh`: Main executable script. Runs the Python build and then uses Pandoc to generate the final PDFs.
- `src/CV_Gustavo_Juantorena_2026.md`: Auto-generated Spanish Markdown output.
- `src/english/CV_Gustavo_Juantorena_2026_EN.md`: Auto-generated English Markdown output.
- `output/`: Directory where the final PDF files are generated.

## Requirements

The generation pipeline requires Python 3 and Pandoc. To install the required Python libraries, run:

```bash
pip install pyyaml jinja2
```

## Modifying the CV Data

To update or add new items to the CV, you **do not** need to edit the separate Markdown files manually. 

1. Open `src/cv_data.yaml`.
2. Locate the section you wish to update (e.g., `experience`, `education`, `skills`).
3. Add or modify the data. For text that varies by language, ensure both `en` and `es` keys are populated.
4. Save the file.

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
