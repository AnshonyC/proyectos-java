# -*- coding: utf-8 -*-
"""Verifica un capitulo del libro.  Uso: python3 -I verificar.py capNN.py|capNN.html"""
import html.parser, importlib.util, os, re, sys

TOTITO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ES_COMENTARIO = ("/**", "*", "//", "*/", "@Override", "@FunctionalInterface", "<!--")
CLASES_OK = {"capitulo", "num", "entrada", "tabla", "java", "ps", "salida", "texto", "caja", "concepto",
             "consejo", "cuidado", "aplica", "ejercicio", "git", "hito", "l"}
VACIOS = {"br", "img", "hr", "path", "circle", "rect", "line", "polyline", "polygon", "ellipse", "stop", "use"}

def trocear(lineas, bloques):
    inicios, desde = [], 0
    for marcador, nota in bloques:
        if marcador is None:
            inicios.append((0, nota)); continue
        idx = next((k for k in range(desde, len(lineas)) if marcador in lineas[k]), None)
        if idx is None:
            raise ValueError("MARCADOR NO ENCONTRADO: %r (buscando desde la linea %d)" % (marcador, desde + 1))
        k = idx
        piso = inicios[-1][0] + 1 if inicios else 0
        while k - 1 >= piso and lineas[k - 1].strip().startswith(ES_COMENTARIO):
            k -= 1
        inicios.append((k, nota)); desde = idx + 1
    if not inicios:
        raise ValueError("sin bloques")
    if inicios[0][0] != 0:
        inicios[0] = (0, inicios[0][1])
    trozos = []
    for n, (ini, nota) in enumerate(inicios):
        fin = inicios[n + 1][0] if n + 1 < len(inicios) else len(lineas)
        trozos.append((ini, fin, nota))
    return trozos

class Revisor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.pila = []; self.errores = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == "class":
                for c in v.split():
                    if c not in CLASES_OK:
                        self.errores.append("clase no permitida: %r en <%s>" % (c, tag))
            if k == "style" and tag not in ("svg",) and not self.en_svg():
                self.errores.append("estilo en linea no permitido en <%s>" % tag)
        if tag not in VACIOS:
            self.pila.append(tag)
    def en_svg(self):
        return "svg" in self.pila
    def handle_endtag(self, tag):
        if tag in VACIOS:
            return
        if not self.pila or self.pila[-1] != tag:
            self.errores.append("cierre inesperado </%s> (abierto: %s)" % (tag, self.pila[-3:]))
            if tag in self.pila:
                while self.pila and self.pila.pop() != tag:
                    pass
        else:
            self.pila.pop()
    def handle_startendtag(self, tag, attrs):
        pass

def revisar_html(texto, donde):
    r = Revisor(); r.feed(texto); r.close()
    errores = ["%s: %s" % (donde, e) for e in r.errores]
    if r.pila:
        errores.append("%s: etiquetas sin cerrar: %s" % (donde, r.pila))
    return errores

def main(ruta):
    errores, avisos = [], []
    if ruta.endswith(".html"):
        texto = open(ruta, encoding="utf-8").read()
        errores += revisar_html(texto, os.path.basename(ruta))
        if not re.search(r'<section class="capitulo" id="(cap\d\d|ap[A-E])">', texto):
            errores.append('falta <section class="capitulo" id="capNN" o "apX">')
        for c in ("aplica", "ejercicio"):
            if 'caja %s' % c not in texto:
                errores.append("falta la caja obligatoria '%s'" % c)
        palabras = len(re.sub(r"<[^>]+>", " ", texto).split())
    else:
        spec = importlib.util.spec_from_file_location("cap", ruta)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        cap = mod.CAPITULO
        for k in ("numero", "titulo", "antes", "archivos", "despues"):
            if k not in cap:
                errores.append("falta la clave %r" % k)
        palabras = 0
        for k in ("antes", "despues"):
            errores += revisar_html(cap.get(k, ""), k)
            palabras += len(re.sub(r"<[^>]+>", " ", cap.get(k, "")).split())
        for c in ("aplica", "ejercicio"):
            if 'caja %s' % c not in cap.get("despues", ""):
                errores.append("falta la caja obligatoria '%s' en 'despues'" % c)
        for a in cap.get("archivos", []):
            ruta_codigo = os.path.join(TOTITO, a["ruta"])
            lineas = open(ruta_codigo, encoding="utf-8").read().split("\n")
            if lineas and lineas[-1] == "":
                lineas.pop()
            try:
                trozos = trocear(lineas, a["bloques"])
            except ValueError as e:
                errores.append("%s: %s" % (a["ruta"], e)); continue
            print("== %s (%d lineas, %d bloques)" % (a["ruta"], len(lineas), len(trozos)))
            for ini, fin, nota in trozos:
                utiles = sum(1 for k in range(ini, fin) if lineas[k].strip() not in ("", "}", "{", "*", "*/", "/**"))
                marca = ""
                if utiles > 10:
                    marca = "  <-- DEMASIADO LARGO (%d lineas con contenido; maximo ~8)" % utiles
                    avisos.append("%s L%d-%d largo" % (a["ruta"], ini + 1, fin))
                nums = re.findall(r"<b>L(\d+)", nota)
                fuera = [n for n in nums if not (ini + 1 <= int(n) <= fin)]
                if fuera:
                    errores.append("%s: bloque L%d-%d cita lineas fuera de rango: %s" % (a["ruta"], ini + 1, fin, fuera))
                print("  L%d-%d%s" % (ini + 1, fin, marca))
                errores += revisar_html(nota, "%s L%d" % (a["ruta"], ini + 1))
                palabras += len(re.sub(r"<[^>]+>", " ", nota).split())
    print("\nPalabras aprox.: %d" % palabras)
    for a in avisos:
        print("AVISO:", a)
    for e in errores:
        print("ERROR:", e)
    print("OK" if not errores else "HAY %d ERRORES" % len(errores))
    sys.exit(1 if errores else 0)

if __name__ == "__main__":
    main(sys.argv[1])
