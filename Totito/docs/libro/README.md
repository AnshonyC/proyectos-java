# Fuentes del libro «Java desde cero con el Totito»

El PDF terminado está en [`../Libro_Java_desde_cero_con_el_Totito.pdf`](../Libro_Java_desde_cero_con_el_Totito.pdf).
Esta carpeta guarda todo lo necesario para corregirlo o ampliarlo.

| Archivo | Qué es |
|---|---|
| `capitulos/capNN.html` | Capítulos de teoría o de pasos (fragmentos HTML) |
| `capitulos/capNN.py` | Capítulos de código línea por línea: texto + notas por bloque del archivo real de `Totito/` |
| `capitulos/apA.html` … `apE.html` | Apéndices |
| `GUIA.md` | Guía de estilo y formato con la que se escribió todo (reglas, datos fijos, índice) |
| `plantilla_libro.html` | Portada, prólogo, índice y estilos (CSS) del libro |
| `armar.py` | Une todo en un solo HTML |
| `verificar.py` | Revisa un capítulo: HTML bien cerrado, clases permitidas y que los números de línea coincidan con el código |
| `paginas.py` | Calcula en qué página empieza cada capítulo (para el índice) |
| `diseno/` | Las cuatro imágenes de diseño originales |

Los capítulos `.py` **no copian el código**: lo leen de `Totito/src` y `Totito/herramientas`. Si cambias una
clase, corre `verificar.py` sobre su capítulo para ver si hay que ajustar los marcadores o las notas.

## Regenerar el PDF

Hace falta Python 3, Google Chrome (o Chromium) y `pdftotext` (poppler). Desde la carpeta `Totito/docs/libro`:

```bash
python3 verificar.py capitulos/cap29.py          # revisar un capítulo
python3 armar.py salida/libro.html               # 1.ª pasada (sin números en el índice)
google-chrome --headless --no-pdf-header-footer --print-to-pdf=salida/libro.pdf salida/libro.html
python3 paginas.py salida/libro.pdf salida/paginas.json
python3 armar.py salida/libro.html salida/paginas.json   # 2.ª pasada, con números de página
google-chrome --headless --no-pdf-header-footer --print-to-pdf=salida/libro.pdf salida/libro.html
```

`salida/` se puede borrar después; no se sube a Git.
