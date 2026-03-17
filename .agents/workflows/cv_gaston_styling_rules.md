---
description: Guía de estilo y preferencias personales para la redacción y formato del Curriculum Vitae de Gaston Bujia.
---

# Reglas de Estilo para el CV de Gaston Bujia

Al generar, editar o formatear el Curriculum Vitae de Gaston, se deben seguir estrictamente las siguientes reglas de estilo, tono y formato basadas en sus preferencias personales:

## 1. Tono y redacción
- **Idioma principal:** El CV debe estar redactado enteramente en **español** (idealmente con matices neutros/argentinos), evitando traducciones literales o "spanglish" innecesario.
- **Conceptos de la industria IT:** Se admiten excepciones al español únicamente para términos estándar de la industria tecnológica donde la traducción suena forzada.
  - *Ejemplo correcto:* "Open Source Maintainer & Developer" (aunque se prefirió adaptarlo a "Desarrollador y Colaborador Principal Open Source" para que suene más natural en el contexto del documento).
  - *Ejemplo correcto:* "Web Scraping" (no usar "Scrapeo de sitios web").
  - *Ejemplo correcto:* "Data Scientist" (no usar "Científico de Datos").
- **Concisión académica:** Evitar verbosidad. Explicar claramente el rol y el impacto sin adornos innecesarios.
- **Desambiguación:** Evitar términos ambiguos y siempre aclarar siglas en su primera aparición (ej. "SAN" -> "Sociedad Argentina de Investigación en Neurociencias (SAN)").

## 2. Formato de publicaciones y citas
- **No incluir links directos:** La cita debe ser únicamente en texto plano, sin hipervínculos a papers o preprints.
- **Formato de lista:** Las publicaciones deben estar enumeradas (1., 2., 3., ...).
- **Resaltado del autor:** El nombre "Bujia, G. E." debe estar siempre en **negrita** dentro de la lista de autores.
- **Estructura de la cita (estilo APA modificado):**
  - Autores (Año). *Título del paper*. En *Nombre de la Conferencia/Revista* (Lugar, fechas).
  - *Ejemplo:* **Bujia, G. E.**, Gauder, L., Laciana, P., Ferrer, L., & Kamienkowski, J. E. (2025). DataPruebas: An Online Platform for Data Collection. In *Simposio Argentino de Inteligencia Artificial y Ciencia de Datos (ASAID 2025)-JAIIO 54* (Universidad de Buenos Aires, 4 al 7 de agosto de 2025).

## 3. Disposición y generación del PDF
- **Herramienta de compilación:** El CV se exporta a PDF utilizando `pandoc` compilando a través de LaTeX.
- **Hyphenation:** Está prohibido que las palabras se corten con guiones al final de la línea. Para eso se usa `assets/disable_hyphens.tex` o una configuración equivalente.
- **Márgenes:** Los márgenes del documento exportado deben aprovechar el espacio. El valor recomendado actual es 1 pulgada.
- **Listas en Markdown:** Para que Pandoc compile bien las viñetas, debe haber una línea en blanco antes de iniciar una lista con asteriscos (`*`).

## 4. Estructura de secciones
- El CV está orientado a roles de industria (Data Science / AI), por lo que la experiencia relevante va por encima de la educación.
- Los proyectos Open Source mantenidos activamente (por ejemplo, *DataPruebas* y *pyxations*) deben tratarse como experiencia real.
- Evitar repetir cargos exactos contiguos. Si dos roles quedan demasiado parecidos, buscar una formulación más precisa para el de menor jerarquía o alcance.

## 5. Diseño visual
- Se prefiere un diseño clásico, sobrio y minimalista en blanco y negro basado en LaTeX estándar, por sobre alternativas más estilizadas.
