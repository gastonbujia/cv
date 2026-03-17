#!/bin/bash

CV_BASENAME="CV_Gaston_Bujia"

echo "Construyendo archivos Markdown desde cv_data.yaml..."
python3 src/build_cv.py

echo "Generando CVs en progreso..."

pandoc "src/${CV_BASENAME}.md" \
    -H assets/disable_hyphens.tex \
    -V geometry:margin=1in \
    -o "output/${CV_BASENAME}_ES.pdf"

pandoc "src/english/${CV_BASENAME}_EN.md" \
    -H assets/disable_hyphens.tex \
    -V geometry:margin=1in \
    -o "output/${CV_BASENAME}_EN.pdf"

echo "PDFs generados exitosamente en la carpeta 'output/':"
echo "  - output/${CV_BASENAME}_ES.pdf"
echo "  - output/${CV_BASENAME}_EN.pdf"
