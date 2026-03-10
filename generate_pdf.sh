#!/bin/bash

echo "🔄 Construyendo archivos Markdown desde cv_data.yaml..."
python3 src/build_cv.py

echo "🔄 Generando CVs en progreso..."

# Generar PDF clásico del CV con Pandoc (Español)
pandoc src/CV_Gustavo_Juantorena.md \
    -H assets/disable_hyphens.tex \
    -V geometry:margin=1in \
    -o output/CV_Gustavo_Juantorena_ES.pdf

# Generar PDF clásico del CV con Pandoc (Inglés)
pandoc src/english/CV_Gustavo_Juantorena_EN.md \
    -H assets/disable_hyphens.tex \
    -V geometry:margin=1in \
    -o output/CV_Gustavo_Juantorena_EN.pdf

echo "✅ PDFs generados exitosamente en la carpeta 'output/':"
echo "  - output/CV_Gustavo_Juantorena_ES.pdf"
echo "  - output/CV_Gustavo_Juantorena_EN.pdf"
