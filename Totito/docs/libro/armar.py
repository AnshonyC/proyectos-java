# -*- coding: utf-8 -*-
"""Arma el libro completo en HTML a partir de capitulos/.  Uso: python3 -I armar.py salida.html"""
import glob, html, importlib.util, os, re, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
TOTITO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DISENO = os.path.join(AQUI, "diseno")
CAPS = os.path.join(AQUI, "capitulos")
SALIDA = sys.argv[1]
import json
PAGINAS = json.load(open(sys.argv[2])) if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else {}

def pag(clave):
    return '<span class="pag">%s</span>' % PAGINAS[clave] if clave in PAGINAS else ""
DIR_SALIDA = os.path.dirname(os.path.abspath(SALIDA))

sys.path.insert(0, AQUI)
from verificar import trocear  # misma logica de bloques que usan los redactores

# ---------------------------------------------------------------- partes
PARTES = [
    (1, "I", "Antes de programar",
     "Preparar la computadora, aprender a usar la terminal, instalar las herramientas y crear la carpeta del proyecto."),
    (6, "II", "Git y GitHub: el camino hasta el resultado final",
     "Cómo guardar cada paso del trabajo, volver atrás sin miedo, trabajar en equipo y publicar."),
    (11, "III", "Fundamentos de Java",
     "Las piezas del lenguaje (variables, decisiones, repeticiones, arreglos, métodos y texto), todas con ejemplos del Totito."),
    (18, "IV", "Programación orientada a objetos",
     "Clases, objetos, herencia, interfaces, patrones: cómo se organiza un programa de verdad y por qué."),
    (28, "V", "El Totito v0.1: la lógica y la primera ventana",
     "Se escribe el corazón del juego línea por línea, se prueba en la consola y se juega en una primera ventana."),
    (34, "VI", "Diseño visual",
     "Leer un diseño, entender el color, la tipografía y el espaciado, y aprender cómo dibuja Swing."),
    (38, "VII", "El Totito v1.0: la interfaz neón",
     "Cada clase de la interfaz, línea por línea, hasta tener el juego completo, funcional y estético."),
    (62, "VIII", "Probar, empaquetar y compartir",
     "Depurar, crear el .jar, el icono, el .exe, el instalador y publicarlo para el mundo."),
    (68, "IX", "Más allá del Totito",
     "Usar todo lo aprendido en otros proyectos y seguir creciendo como programador."),
]

KEYWORDS = set("""abstract boolean break byte case catch char class continue default do double else enum extends
final finally float for if implements import instanceof int interface long new null package private protected public
return short static super switch this throw throws true false try void while var record""".split())

def resaltar_java(lineas):
    salida, en_bloque = [], False
    for linea in lineas:
        res, i = [], 0
        while i < len(linea):
            if en_bloque:
                fin = linea.find("*/", i)
                if fin < 0:
                    res.append('<span class="c">%s</span>' % html.escape(linea[i:])); i = len(linea)
                else:
                    res.append('<span class="c">%s</span>' % html.escape(linea[i:fin + 2])); i = fin + 2; en_bloque = False
                continue
            if linea.startswith("//", i):
                res.append('<span class="c">%s</span>' % html.escape(linea[i:])); break
            if linea.startswith("/*", i):
                en_bloque = True; continue
            ch = linea[i]
            if ch in "\"'":
                j = i + 1
                while j < len(linea) and linea[j] != ch:
                    j += 2 if linea[j] == "\\" else 1
                res.append('<span class="s">%s</span>' % html.escape(linea[i:j + 1])); i = j + 1; continue
            m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", linea[i:])
            if m:
                w = m.group(0)
                if w in KEYWORDS:
                    res.append('<span class="k">%s</span>' % w)
                elif w[0].isupper():
                    res.append('<span class="t">%s</span>' % w)
                else:
                    res.append(w)
                i += len(w); continue
            m = re.match(r"\d+(\.\d+)?[fFdDL]?", linea[i:])
            if m and (i == 0 or not (linea[i-1].isalnum() or linea[i-1] == "_")):
                res.append('<span class="n">%s</span>' % m.group(0)); i += len(m.group(0)); continue
            if ch == "@":
                m = re.match(r"@\w+", linea[i:])
                if m:
                    res.append('<span class="a">%s</span>' % m.group(0)); i += len(m.group(0)); continue
            res.append(html.escape(ch)); i += 1
        salida.append("".join(res))
    return salida

def resaltar_xml(lineas):
    out = []
    for l in lineas:
        e = html.escape(l)
        e = re.sub(r"(&lt;!--.*?--&gt;)", r'<span class="c">\1</span>', e)
        e = re.sub(r"(&lt;/?)([\w.:-]+)", r'\1<span class="k">\2</span>', e)
        out.append(e)
    return out

# ---------------------------------------------------------------- imagenes
IMAGENES = os.path.join(DIR_SALIDA, "img")
os.makedirs(IMAGENES, exist_ok=True)
FUENTES_IMG = {
    "diseno/": DISENO,
    "capturas/": os.path.join(TOTITO, "docs", "capturas"),
    "recursos/": os.path.join(TOTITO, "recursos"),
}
faltantes = []

def mapear_img(m):
    src = m.group(1)
    for prefijo, carpeta in FUENTES_IMG.items():
        if src.startswith(prefijo):
            origen = os.path.join(carpeta, src[len(prefijo):])
            if os.path.exists(origen):
                destino = prefijo.rstrip("/") + "-" + os.path.basename(origen)
                shutil.copy(origen, os.path.join(IMAGENES, destino))
                return '<img src="img/%s"' % destino
    faltantes.append(src)
    return m.group(0)

def procesar_fragmento(texto):
    # Codigo Java de ejemplo
    def java(m):
        crudo = html.unescape(m.group(1)).strip("\n")
        return '<pre class="java">%s</pre>' % "\n".join(resaltar_java(crudo.split("\n")))
    texto = re.sub(r'<pre class="java">(.*?)</pre>', java, texto, flags=re.S)
    # PowerShell: prompt en cada comando (no en comentarios ni en continuaciones con `)
    def ps(m):
        lineas = m.group(1).strip("\n").split("\n")
        out, sigue = [], False
        for l in lineas:
            t = l.strip()
            if t.startswith("#"):
                out.append('<span class="c">%s</span>' % l)
            elif sigue or not t:
                out.append(l)
            else:
                out.append('<span class="prompt">PS&gt; </span>' + l)
            sigue = t.endswith("`")
        return '<pre class="ps">%s</pre>' % "\n".join(out)
    texto = re.sub(r'<pre class="ps">(.*?)</pre>', ps, texto, flags=re.S)
    texto = re.sub(r'<img src="([^"]+)"', mapear_img, texto)
    # Cajas vacias (apendices)
    texto = re.sub(r'<div class="caja (aplica|ejercicio)">\s*</div>', "", texto)
    return texto

def render_py(ruta):
    spec = importlib.util.spec_from_file_location("cap", ruta)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    cap = mod.CAPITULO
    num = cap["numero"]
    partes = ['<section class="capitulo" id="cap%02d"><h1><span class="num">Capítulo %d</span>%s</h1>'
              % (num, num, html.escape(cap["titulo"]))]
    partes.append(procesar_fragmento(cap["antes"]))
    for a in cap["archivos"]:
        ruta_codigo = os.path.join(TOTITO, a["ruta"])
        lineas = open(ruta_codigo, encoding="utf-8").read().split("\n")
        if lineas and lineas[-1] == "":
            lineas.pop()
        res = resaltar_xml(lineas) if a["ruta"].endswith(".xml") else resaltar_java(lineas)
        partes.append('<h2 class="archivo">El código: <code>%s</code> <span class="lineas">%d líneas</span></h2>'
                      % (a["ruta"].replace("/", "\\"), len(lineas)))
        for ini, fin, nota in trocear(lineas, a["bloques"]):
            filas = "".join('<tr><td class="ln">%d</td><td class="cd">%s</td></tr>' % (k + 1, res[k] or "&nbsp;")
                            for k in range(ini, fin))
            rango = "Línea %d" % (ini + 1) if fin - ini == 1 else "Líneas %d–%d" % (ini + 1, fin)
            largo = " largo" if fin - ini > 40 else ""
            partes.append('<div class="bloque%s"><table class="codigo">%s</table><div class="nota">'
                          '<span class="rango">%s</span>%s</div></div>' % (largo, filas, rango, procesar_fragmento(nota)))
    partes.append(procesar_fragmento(cap["despues"]))
    partes.append("</section>")
    return num, cap["titulo"], "".join(partes)

def titulo_html(texto):
    m = re.search(r'<h1><span class="num">[^<]*</span>(.*?)</h1>', texto, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else "?"

# ---------------------------------------------------------------- recorrer capitulos
capitulos = {}
for ruta in sorted(glob.glob(os.path.join(CAPS, "cap*.*"))):
    m = re.match(r"cap(\d\d)\.(html|py)$", os.path.basename(ruta))
    if not m:
        continue
    n = int(m.group(1))
    if m.group(2) == "py":
        num, titulo, cuerpo = render_py(ruta)
    else:
        cuerpo = procesar_fragmento(open(ruta, encoding="utf-8").read())
        titulo = titulo_html(cuerpo)
    capitulos[n] = (titulo, cuerpo)

apendices = []
for letra in "ABCDE":
    ruta = os.path.join(CAPS, "ap%s.html" % letra)
    if os.path.exists(ruta):
        cuerpo = procesar_fragmento(open(ruta, encoding="utf-8").read())
        apendices.append((letra, titulo_html(cuerpo), cuerpo))

# ---------------------------------------------------------------- indice y cuerpo
indice, cuerpo = [], []
for i, (inicio, romano, nombre, desc) in enumerate(PARTES):
    fin = PARTES[i + 1][0] if i + 1 < len(PARTES) else 100
    nums = [n for n in sorted(capitulos) if inicio <= n < fin]
    if not nums:
        continue
    indice.append('<li class="parte"><a href="#parte%s">Parte %s · %s</a><ol>' % (romano, romano, nombre))
    indice.extend('<li><a href="#cap%02d"><span>%d</span>%s%s</a></li>' % (n, n, html.escape(capitulos[n][0]), pag(str(n))) for n in nums)
    indice.append("</ol></li>")
    cuerpo.append('<section class="separador" id="parte%s"><div class="romano">Parte %s</div><div class="nombre">%s</div>'
                  '<p>%s</p><ul>%s</ul></section>' % (romano, romano, nombre, desc,
                  "".join("<li>%d · %s</li>" % (n, html.escape(capitulos[n][0])) for n in nums)))
    cuerpo.extend(capitulos[n][1] for n in nums)
if apendices:
    indice.append('<li class="parte"><a href="#apendices">Apéndices</a><ol>')
    indice.extend('<li><a href="#ap%s"><span>%s</span>%s%s</a></li>' % (l, l, html.escape(t), pag(l)) for l, t, _ in apendices)
    indice.append("</ol></li>")
    cuerpo.append('<section class="separador" id="apendices"><div class="romano">Apéndices</div>'
                  '<div class="nombre">Para tener a mano</div><p>Chuletas, atajos, errores comunes y glosario.</p></section>')
    cuerpo.extend(c for _, _, c in apendices)

plantilla = open(os.path.join(AQUI, "plantilla_libro.html"), encoding="utf-8").read()
plantilla = procesar_fragmento(plantilla)
doc = plantilla.replace("{{INDICE}}", "".join(indice)).replace("{{CUERPO}}", "".join(cuerpo))
open(SALIDA, "w", encoding="utf-8").write(doc)
print("Capítulos:", len(capitulos), "· apéndices:", len(apendices), "· faltan:", sorted(set(range(1, 70)) - set(capitulos)))
if faltantes:
    print("IMÁGENES NO ENCONTRADAS:", sorted(set(faltantes)))
