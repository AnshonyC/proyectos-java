# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 42,
    "titulo": "Iconos.java: iconos dibujados con código",
    "antes": r"""
<p class="entrada">El triángulo de «Jugar», el libro de «Instrucciones», la casa, el trofeo, el logotipo… El Totito no
tiene ni un solo archivo de imagen para sus iconos: los trece se dibujan con figuras geométricas. En este capítulo
aprendes a diseñar un icono en coordenadas relativas, a guardarlo en una constante gracias a una lambda, y la geometría
(con seno, coseno y operaciones entre áreas) que hay detrás de los más elaborados.</p>

<h2>Por qué existe este archivo</h2>
<p>El diseño (capítulo 34) usa iconos en casi todos los botones. La forma habitual de ponerlos sería guardar trece
archivos PNG en el proyecto y cargarlos. Para el Totito eso tiene tres problemas:</p>
<ul>
<li><b>Tamaños:</b> el mismo logotipo aparece en el encabezado, a 48 píxeles en el icono de la ventana y a 256 en
el icono del programa instalado (capítulo 64). Una imagen PNG ampliada se ve borrosa; reducida, pierde detalle.</li>
<li><b>Colores:</b> el mismo libro se ve rosa en un sitio y azul en otro; la persona, en el color de cada jugador. Con PNG
harían falta varias copias de cada icono.</li>
<li><b>Estilo:</b> los iconos deben brillar con el mismo neón de <code>Dibujo</code> (capítulo 41). Una imagen plana no
puede.</li>
</ul>
<p>Dibujarlos con código resuelve los tres: un icono es una <b>receta</b> («un triángulo con estas esquinas, con halo y
relleno degradado») que se puede cocinar a cualquier tamaño y en cualquier color. Es la misma idea que los formatos
vectoriales como SVG, que seguramente has visto en la web.</p>

<h2>Cómo se diseña un icono en coordenadas relativas</h2>
<p>Todos los iconos siguen <b>una regla</b>, escrita en el comentario de la clase: cada icono se dibuja dentro de un
cuadrado de lado <code>t</code> cuya esquina superior izquierda es <code>(x, y)</code>, y <b>todas las medidas son
fracciones de <code>t</code></b>. Así se diseña uno:</p>
<ol>
<li><b>Boceto en cuadrícula.</b> Dibuja el icono en papel cuadriculado, dentro de un cuadrado de 10 × 10 cuadritos (o de
100 × 100 en un programa de dibujo). Deja un pequeño margen alrededor.</li>
<li><b>Marca los puntos clave:</b> las esquinas de las líneas, los centros de los círculos, los extremos de las curvas.</li>
<li><b>Léelos como fracciones.</b> Un punto a 24 cuadritos de 100 desde la izquierda y a 14 desde arriba es
<code>(0.24, 0.14)</code>.</li>
<li><b>Tradúcelos a código:</b> la x real es <code>x + t * 0.24</code> y la y real, <code>y + t * 0.14</code>.</li>
<li><b>Elige la técnica:</b> trazo simple, trazo neón, relleno, o una combinación.</li>
<li><b>Pruébalo a varios tamaños,</b> de 20 a 100 píxeles: un detalle de 0.02 · t desaparece en un icono pequeño.</li>
</ol>
<svg viewBox="0 0 260 250" width="55%">
<rect x="0" y="0" width="260" height="250" rx="12" fill="#1C1740"/>
<g stroke="#C8BCF6" stroke-opacity="0.25" stroke-width="1">
<line x1="30" y1="20" x2="30" y2="220"/><line x1="30" y1="20" x2="230" y2="20"/>
<line x1="50" y1="20" x2="50" y2="220"/><line x1="30" y1="40" x2="230" y2="40"/>
<line x1="70" y1="20" x2="70" y2="220"/><line x1="30" y1="60" x2="230" y2="60"/>
<line x1="90" y1="20" x2="90" y2="220"/><line x1="30" y1="80" x2="230" y2="80"/>
<line x1="110" y1="20" x2="110" y2="220"/><line x1="30" y1="100" x2="230" y2="100"/>
<line x1="130" y1="20" x2="130" y2="220"/><line x1="30" y1="120" x2="230" y2="120"/>
<line x1="150" y1="20" x2="150" y2="220"/><line x1="30" y1="140" x2="230" y2="140"/>
<line x1="170" y1="20" x2="170" y2="220"/><line x1="30" y1="160" x2="230" y2="160"/>
<line x1="190" y1="20" x2="190" y2="220"/><line x1="30" y1="180" x2="230" y2="180"/>
<line x1="210" y1="20" x2="210" y2="220"/><line x1="30" y1="200" x2="230" y2="200"/>
<line x1="230" y1="20" x2="230" y2="220"/><line x1="30" y1="220" x2="230" y2="220"/>
</g>
<rect x="30" y="20" width="200" height="200" fill="none" stroke="#C8BCF6" stroke-width="1.5"/>
<polygon points="78,48 202,120 78,192" fill="#FF3BD4" fill-opacity="0.35" stroke="#FF3BD4" stroke-width="3" stroke-linejoin="round"/>
<g fill="#FFFFFF"><circle cx="78" cy="48" r="4"/><circle cx="202" cy="120" r="4"/><circle cx="78" cy="192" r="4"/></g>
<g fill="#FFFFFF" font-size="11" font-family="monospace">
<text x="84" y="42">(0.24, 0.14)</text>
<text x="210" y="110" text-anchor="end">(0.86, 0.5)</text>
<text x="84" y="206">(0.24, 0.86)</text>
</g>
<g fill="#C8BCF6" font-size="10" font-family="sans-serif"><text x="30" y="236">x</text><text x="222" y="236">x + t</text><text x="4" y="24">y</text><text x="0" y="222">y+t</text></g>
</svg>
<p>El icono <code>JUGAR</code> en su cuadrícula de 10 × 10: tres puntos, tres fracciones de <code>t</code>. Si el botón lo
pide a 20 píxeles, la punta derecha queda en <code>x + 17.2</code>; si lo pide a 84, en <code>x + 72.24</code>. La forma
es la misma.</p>

<h2>Los trece iconos</h2>
<table class="tabla">
<tr><th>Constante</th><th>Qué dibuja</th><th>Dónde aparece</th><th>Técnica principal</th></tr>
<tr><td><code>JUGAR</code></td><td>Triángulo «reproducir»</td><td>Jugar (menú), Comenzar partida</td><td>Neón + relleno degradado</td></tr>
<tr><td><code>LIBRO</code></td><td>Libro abierto</td><td>Instrucciones, título «Cómo jugar»</td><td>Curvas <code>quadTo</code></td></tr>
<tr><td><code>SALIR</code></td><td>Puerta con flecha</td><td>Salir</td><td>Camino de líneas</td></tr>
<tr><td><code>CHEVRON</code></td><td>Flechita «›»</td><td>Derecha de los botones del menú</td><td>Dos segmentos</td></tr>
<tr><td><code>FLECHA_IZQUIERDA</code></td><td>Flecha «←»</td><td>Volver, Regresar</td><td>Trazo simple</td></tr>
<tr><td><code>CASA</code></td><td>Casa</td><td>Menú principal</td><td>Relleno + <code>Area.subtract</code></td></tr>
<tr><td><code>REINICIAR</code></td><td>Dos flechas en círculo</td><td>Reiniciar, Jugar de nuevo</td><td><code>Arc2D</code> + seno y coseno</td></tr>
<tr><td><code>PERSONA</code></td><td>Silueta</td><td>Tarjeta de jugador</td><td><code>Area.intersect</code>, referencia a método</td></tr>
<tr><td><code>PERSONAS</code></td><td>Dos siluetas</td><td>Opción «2 jugadores»</td><td>Reutiliza <code>persona</code></td></tr>
<tr><td><code>COMPUTADORA</code></td><td>Chip</td><td>Opción «Contra la IA», tarjeta de la IA</td><td>Bucle para las patas</td></tr>
<tr><td><code>TROFEO</code></td><td>Copa con estrella</td><td>Pantalla de victoria</td><td><code>Area.add</code>, estrella con trigonometría</td></tr>
<tr><td><code>LOGO</code></td><td>Rejilla del totito</td><td>Encabezado, ventana, icono del programa</td><td>Líneas «a mano» + neón</td></tr>
<tr><td><code>CERRAR</code></td><td>X de cerrar</td><td>Esquina del encabezado</td><td>Dos diagonales con neón</td></tr>
</table>

<h2>Qué vas a aprender</h2>
<ul>
<li>Las <b>interfaces funcionales</b> (<code>@FunctionalInterface</code>) y por qué permiten escribir cada icono como una <b>lambda</b>.</li>
<li>Guardar comportamiento en una constante: <code>public static final Icono JUGAR = (g, x, y, t, c) -&gt; { ... };</code></li>
<li>Las <b>referencias a métodos</b> (<code>Iconos::persona</code>).</li>
<li><code>Path2D</code> con <code>moveTo</code>, <code>lineTo</code>, <code>quadTo</code> (curvas) y <code>closePath</code>.</li>
<li>Rellenos con degradado (<code>GradientPaint</code>), rectángulos redondeados y arcos (<code>Arc2D</code>).</li>
<li>Geometría constructiva: sumar, restar e intersecar figuras con <code>Area</code>.</li>
<li>Seno y coseno aplicados: puntas de flecha que siguen un círculo y una estrella de cinco puntas.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>En la rama <code>interfaz-neon</code>: clic derecho en <i>&lt;default package&gt;</i> → <i>New → Java Class…</i> → <code>Iconos</code> → <i>Finish</i>.</li>
<li>Borra la plantilla y escribe el código. Usa <code>Dibujo</code> (capítulo 41) y <code>Tema</code> (40).</li>
</ol>
<pre class="ps">New-Item src\Iconos.java</pre>
<div class="caja consejo">Es el archivo más largo hasta ahora (268 líneas), pero muy repetitivo: casi todo son
<code>moveTo</code> y <code>lineTo</code> con fracciones. Escríbelo icono por icono y compila (Shift+F11) después de cada
uno: si te equivocas, sabrás exactamente dónde.</div>
""",
    "archivos": [
        {"ruta": "src/Iconos.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.Color</code>: el color con que se pide cada icono.</p>
<p class="l"><b>L2</b> <code>java.awt.GradientPaint</code>: una «pintura» en degradado lineal entre dos puntos y dos
colores. Es un <code>Paint</code> (capítulo 41). Rellena el triángulo de <code>JUGAR</code>, la copa del trofeo y las
siluetas.</p>
<p class="l"><b>L3</b> <code>java.awt.Graphics2D</code>: el lápiz con que se dibuja.</p>
<p class="l"><b>L4</b> <code>java.awt.Shape</code>: la interfaz de las figuras; el método <code>estrella</code> devuelve un
<code>Shape</code>.</p>
"""),
             ("import java.awt.geom.Arc2D", r"""
<p class="l"><b>L5</b> <code>java.awt.geom.Arc2D</code>: un <b>arco</b>, un trozo del borde de una elipse, definido por su
ángulo de inicio y cuántos grados recorre. Para <code>REINICIAR</code>.</p>
<p class="l"><b>L6</b> <code>java.awt.geom.Area</code>: una región del plano que se puede <b>combinar</b> con otras:
sumar (<code>add</code>), restar (<code>subtract</code>) o quedarse con lo común (<code>intersect</code>). Para la casa, el
pie del trofeo y la silueta.</p>
<p class="l"><b>L7</b> <code>java.awt.geom.Ellipse2D</code>: círculos y elipses (capítulo 41).</p>
<p class="l"><b>L8</b> <code>java.awt.geom.Path2D</code>: caminos punto a punto (capítulo 41). El más usado del archivo.</p>
<p class="l"><b>L9</b> <code>java.awt.geom.Rectangle2D</code>: un rectángulo con coordenadas decimales.</p>
<p class="l"><b>L10</b> <code>java.awt.geom.RoundRectangle2D</code>: un rectángulo con las esquinas redondeadas. Para el chip,
la puerta de la casa y el pie del trofeo.</p>
"""),
             ("public final class Iconos", r"""
<p class="l"><b>L12–L20</b> El comentario de la clase es su manual: iconos hechos con figuras geométricas, sin archivos;
cada uno se dibuja en un cuadrado de lado <code>t</code> que empieza en <code>(x, y)</code>; todas las medidas son
fracciones de <code>t</code>, «así el mismo icono sirve a cualquier tamaño»; y para crear uno nuevo basta con agregar otra
constante siguiendo el patrón. Quien abra este archivo dentro de un año sabe en diez segundos cómo funciona.</p>
<p class="l"><b>L21</b> Otra clase de utilidad <code>final</code>. Esta vez lo que guarda no son colores ni métodos, sino
<b>objetos</b>: trece constantes de tipo <code>Icono</code>.</p>
"""),
             ("public interface Icono", r"""
<p class="l"><b>L23</b> Comentario: «un icono sabe dibujarse en el cuadrado (x, y, tam, tam) con el color dado». Esa es
toda la definición de icono que necesita el juego.</p>
<p class="l"><b>L24</b> <code>@FunctionalInterface</code> es una <b>anotación</b> (como <code>@Override</code>): una
etiqueta para el compilador. Declara que esta interfaz tiene <b>un solo método abstracto</b>, y el compilador lo vigila:
si alguien le agregara un segundo método, daría error. Las interfaces con un solo método se llaman <i>funcionales</i> y
tienen un superpoder: se pueden implementar con una <b>lambda</b> (capítulo 25).</p>
<p class="l"><b>L25</b> Una interfaz <b>anidada</b> dentro de la clase: su nombre completo es <code>Iconos.Icono</code>. Así
la usan los botones: <code>BotonNeon.menu("Jugar", Iconos.JUGAR, Tema.ROSA)</code> recibe un parámetro de tipo
<code>Iconos.Icono</code>. Anidarla deja claro que «icono» es un concepto de esta clase.</p>
<p class="l"><b>L26</b> El único método: <code>dibujar</code>, con el lápiz, la esquina <code>(x, y)</code>, el
<code>tam</code>año y el color. Como en <code>Navegacion</code> (capítulo 39), termina en <code>;</code>: no dice cómo,
solo qué.</p>
<p class="l"><b>L27</b> Cierra la interfaz.</p>
"""),
             ("private Iconos()", r"""
<p class="l"><b>L29–L30</b> Constructor privado: no se crean objetos <code>Iconos</code>; se usan sus constantes.</p>
"""),
             ("JUGAR =", r"""
<p class="l"><b>L32</b> Comentario: el triángulo «reproducir» de los botones Jugar y Comenzar partida.</p>
<p class="l"><b>L33</b> Aquí está la idea central del archivo. <code>public static final Icono JUGAR</code> declara una
constante de tipo <code>Icono</code>, y lo que se le asigna es una <b>lambda</b>: <code>(g, x, y, t, c) -&gt; { ... }</code>.
Se lee «dados g, x, y, t y c, haz esto». La lambda es una forma corta de escribir un objeto que implementa la única función
de <code>Icono</code>: su cuerpo <b>es</b> el método <code>dibujar</code>. Los tipos de los parámetros no se escriben:
Java los deduce de <code>dibujar</code> (<code>g</code> es un <code>Graphics2D</code>, <code>x</code>, <code>y</code> y
<code>t</code> son <code>double</code>, <code>c</code> es un <code>Color</code>). Los nombres sí son nuestros: se eligió
<code>t</code> (de tamaño) y <code>c</code> (de color) para que las fórmulas sean cortas. El código de dentro <b>no se
ejecuta ahora</b>: se guarda, y se ejecutará cada vez que alguien llame a <code>Iconos.JUGAR.dibujar(...)</code>.</p>
<p class="l"><b>L34</b> Un camino vacío para el triángulo.</p>
<p class="l"><b>L35</b> Primera esquina, arriba a la izquierda: <code>(0.24, 0.14)</code>.</p>
<p class="l"><b>L36</b> Línea hasta la punta derecha, a media altura: <code>(0.86, 0.5)</code>.</p>
<p class="l"><b>L37</b> Línea hasta la esquina de abajo a la izquierda: <code>(0.24, 0.86)</code>.</p>
<p class="l"><b>L38</b> <code>closePath()</code> cierra la figura con una línea de vuelta al primer punto. Es mejor que un
<code>lineTo</code> al inicio, porque así la esquina de cierre se <b>une</b> con el estilo del trazo (redondeada) en vez de
quedar como dos puntas sueltas superpuestas. Fíjate en que el triángulo no está centrado en el cuadrado: su caja va de 0.24
a 0.86 (centro en 0.55). Es <b>compensación óptica</b>, como la X de <code>dibujarFicha</code>: el peso visual de un
triángulo está en su lado ancho; si su caja estuviera centrada, parecería corrido a la izquierda.</p>
"""),
             ("Dibujo.trazoNeon(g, triangulo", r"""
<p class="l"><b>L39</b> Primero el halo: el contorno del triángulo con neón, grosor del 10 % de <code>t</code> e intensidad
0.6 (un brillo discreto). <code>(float) (t * 0.1)</code>: como <code>t</code> es <code>double</code>, el producto también;
<code>trazoNeon</code> pide un <code>float</code> y hay que convertirlo.</p>
<p class="l"><b>L40–L41</b> Después, el relleno. <code>new GradientPaint(x1, y1, color1, x2, y2, color2)</code> crea un
degradado lineal: en el punto 1 el color es <code>color1</code>, en el punto 2 es <code>color2</code>, y en medio se mezclan.
Aquí va de la esquina superior izquierda del cuadrado (un poco aclarado con <code>Tema.aclarar(c, 0.25f)</code>) a la
esquina inferior derecha (el color puro): un degradado <b>diagonal</b>, como si la luz viniera de arriba a la izquierda.
Los <code>(float)</code> son porque este constructor pide <code>float</code>. <code>setPaint</code> lo pone como pintura
actual.</p>
<p class="l"><b>L42</b> <code>g.fill(triangulo)</code> rellena el interior. El orden importa: el relleno cubre la mitad
interior del halo y solo queda visible el resplandor de afuera. Si se rellenara primero, el halo semitransparente quedaría
encima y ensuciaría el degradado.</p>
<p class="l"><b>L43</b> <code>};</code> la llave cierra la lambda y el punto y coma cierra la instrucción de asignación de
la constante (es una declaración <code>JUGAR = ...;</code>, aunque ocupe once líneas).</p>
"""),
             ("LIBRO =", r"""
<p class="l"><b>L45–L46</b> Comentario y comienzo del libro abierto (Instrucciones / Cómo jugar).</p>
<p class="l"><b>L47</b> <code>cx</code>: la x del centro del cuadrado, donde estará el lomo. Con <code>t = 100</code> y
<code>x = 0</code>, vale 50. Guardar medidas que se repiten en variables locales hace las líneas siguientes más
legibles.</p>
<p class="l"><b>L48</b> <code>arriba</code>: la altura del borde superior de las páginas, al 20 % (20).</p>
<p class="l"><b>L49</b> <code>abajo</code>: la del borde inferior, al 84 % (84).</p>
<p class="l"><b>L50</b> Un único camino para las dos páginas y el lomo.</p>
"""),
             ("// Pagina izquierda", r"""
<p class="l"><b>L51</b> Comentario: la página izquierda.</p>
<p class="l"><b>L52</b> Empieza en lo alto del lomo: <code>(cx, arriba + 0.06t)</code> = (50, 26).</p>
<p class="l"><b>L53</b> <code>quadTo(controlX, controlY, finX, finY)</code> dibuja una <b>curva cuadrática de Bézier</b>:
va del punto actual al punto final, pero «atraída» hacia un punto de control por el que no pasa, como una cuerda que se
estira hacia un imán. Aquí va de (50, 26) a la esquina superior izquierda (6, 22), atraída hacia (30, 14), que está más
arriba: el borde superior de la página se curva hacia arriba, como una hoja abierta.</p>
<p class="l"><b>L54</b> Una línea recta hacia abajo por el borde izquierdo, hasta (6, 76).</p>
<p class="l"><b>L55</b> Otra curva, de vuelta al pie del lomo (50, 84), atraída hacia (30, 70): el borde inferior de la
página. El libro está «abierto», con las páginas que bajan hacia el centro.</p>
"""),
             ("// Pagina derecha", r"""
<p class="l"><b>L56–L60</b> La página derecha es la izquierda reflejada: mismas alturas, pero con <code>cx + 0.2t</code> en
los puntos de control y <code>x + 0.94t</code> en el borde (94 = 100 − 6). <code>moveTo</code> (L57) levanta el lápiz y
vuelve a lo alto del lomo para empezar la segunda página. Para reflejar algo horizontalmente en un cuadrado, cada fracción
<code>f</code> se convierte en <code>1 − f</code>.</p>
"""),
             ("// Lomo", r"""
<p class="l"><b>L61–L63</b> El lomo: una línea vertical en el centro, de arriba abajo.</p>
<p class="l"><b>L64</b> Todo el camino con neón, grosor 7.5 % de <code>t</code>, intensidad normal. Un icono puramente de
líneas, sin relleno.</p>
"""),
             ("SALIR =", r"""
<p class="l"><b>L67</b> Comentario: puerta con una flecha que sale.</p>
<p class="l"><b>L68–L69</b> La lambda y el camino.</p>
<p class="l"><b>L70–L75</b> El marco de la puerta, como un corchete «[» abierto a la derecha. Empieza en (0.55, 0.3), sube a
(0.55, 0.12), va a la izquierda hasta (0.14, 0.12), baja hasta (0.14, 0.88), va a la derecha hasta (0.55, 0.88) y sube
hasta (0.55, 0.7). Entre las alturas 0.3 y 0.7 del lado derecho queda un <b>hueco</b>: por ahí sale la flecha. Cinco
segmentos seguidos sin levantar el lápiz, y gracias a <code>JOIN_ROUND</code> las cuatro esquinas quedan redondeadas.</p>
"""),
             ("puerta.moveTo(x + t * 0.36", r"""
<p class="l"><b>L76–L77</b> Levanta el lápiz y dibuja el cuerpo de la flecha: una línea horizontal a media altura, de 0.36
(dentro de la puerta) a 0.9 (fuera).</p>
<p class="l"><b>L78–L80</b> La punta: de (0.74, 0.34) a la punta (0.9, 0.5) y de ahí a (0.74, 0.66). Una «V» acostada
que apunta a la derecha.</p>
<p class="l"><b>L81</b> Todo con neón, grosor 7.5 % de <code>t</code>.</p>
"""),
             ("CHEVRON =", r"""
<p class="l"><b>L84</b> Comentario: la flechita «›» del lado derecho de los botones del menú.</p>
<p class="l"><b>L85–L89</b> Dos segmentos en ángulo: de (0.32, 0.16) a la punta (0.68, 0.5) y de ahí a (0.32, 0.84).</p>
<p class="l"><b>L90</b> Neón más grueso (13 % de <code>t</code>) porque el chevron se dibuja pequeño, e intensidad 0.7 para que
acompañe sin competir con el texto del botón.</p>
"""),
             ("FLECHA_IZQUIERDA =", r"""
<p class="l"><b>L93</b> Comentario: flecha hacia la izquierda (Volver / Regresar).</p>
<p class="l"><b>L94–L97</b> El cuerpo, de derecha (0.88) a izquierda (0.14) a media altura, y el primer lado de la punta,
de (0.42, 0.22) a la punta (0.14, 0.5).</p>
<p class="l"><b>L98–L100</b> L98 es la continuación: de la punta a (0.42, 0.78), el otro lado.</p>
<p class="l"><b>L101</b> Este icono usa <code>Dibujo.trazo</code>, <b>sin</b> halo: va dentro de botones de contorno y de
píldoras que ya tienen su propio brillo, y un segundo halo los ensuciaría.</p>
"""),
             ("CASA =", r"""
<p class="l"><b>L104–L105</b> Comentario y comienzo de la casa (Menú principal).</p>
<p class="l"><b>L106</b> Este icono es <b>relleno</b>, no de líneas: fija el color una vez para todo lo que sigue.</p>
<p class="l"><b>L107–L111</b> El techo: un triángulo con la punta en (0.5, 0.1) y la base de (0.92, 0.48) a (0.08, 0.48),
cerrado con <code>closePath</code>.</p>
"""),
             ("g.setStroke(Dibujo.redondo((float) (t * 0.08)));", r"""
<p class="l"><b>L112</b> Un trazo redondo grueso (8 % de <code>t</code>).</p>
<p class="l"><b>L113</b> Dibuja el <b>contorno</b> del techo con ese trazo. ¿Para qué, si después se rellena? Porque el trazo
redondo <b>suaviza las esquinas</b> del triángulo y lo engorda un poco: un triángulo solo rellenado tendría puntas
afiladas, que a tamaño pequeño se ven agresivas.</p>
<p class="l"><b>L114</b> Rellena el interior. Contorno redondeado más relleno: un techo de esquinas suaves.</p>
"""),
             ("Area cuerpo = new Area(new Rectangle2D", r"""
<p class="l"><b>L115</b> El cuerpo de la casa. <code>new Rectangle2D.Double(x, y, ancho, alto)</code> es un rectángulo de
(0.2, 0.44) con 0.6 de ancho y 0.46 de alto. Empieza en 0.44, un poco por encima de la base del techo (0.48), para que no
quede una rendija entre los dos. Se envuelve en un <code>new Area(...)</code>: un <code>Area</code> es una región que se
puede combinar con otras.</p>
<p class="l"><b>L116–L117</b> <code>cuerpo.subtract(...)</code> <b>resta</b> otra región: la puerta, un rectángulo redondeado
de (0.41, 0.6) con 0.18 de ancho y 0.32 de alto. <code>RoundRectangle2D.Double</code> recibe además el ancho y el alto del
redondeo de las esquinas (0.05 · t). Restar es como recortar con tijeras: donde estaba la puerta, el cuerpo queda vacío y
se ve el fondo a través. La puerta llega hasta 0.92, más abajo que el cuerpo (0.9), y por eso el recorte queda abierto por
abajo, como una puerta de verdad.</p>
<p class="l"><b>L118</b> Rellena el cuerpo ya recortado. <code>Area</code> también es un <code>Shape</code>, así que
<code>fill</code> lo acepta.</p>
"""),
             ("REINICIAR =", r"""
<p class="l"><b>L121</b> Comentario: dos flechas en círculo (Jugar de nuevo / Reiniciar). Es el icono con más geometría;
sigue la explicación con la figura que hay más abajo, en «Cómo funciona por dentro».</p>
<p class="l"><b>L122–L124</b> El centro del cuadrado <code>(cx, cy)</code>.</p>
<p class="l"><b>L125</b> El radio del círculo: 34 % de <code>t</code>. Con <code>t = 100</code>, 34: deja sitio para que las
puntas de flecha no se salgan del cuadrado.</p>
<p class="l"><b>L126–L127</b> Color y trazo redondo del 10 % de <code>t</code> para los arcos.</p>
<p class="l"><b>L128</b> Un <i>for-each</i> sobre un arreglo escrito en el momento: <code>new int[]{30, 210}</code>. El bucle
se ejecuta dos veces, con <code>inicio</code> = 30 y con <code>inicio</code> = 210: una por cada flecha. 210 = 30 + 180: la
segunda es la primera girada media vuelta.</p>
<p class="l"><b>L129</b> <code>new Arc2D.Double(x, y, ancho, alto, inicio, extensión, tipo)</code>. Los cuatro primeros
números son el rectángulo que contiene la circunferencia <b>completa</b> (de <code>cx − r</code> a <code>cx + r</code>).
<code>inicio</code> es el ángulo en grados donde empieza el arco, y <code>120</code> cuántos grados recorre. En
<code>Arc2D</code> los ángulos funcionan como en matemáticas: 0° es la derecha (las 3 del reloj), 90° es arriba y crecen en
sentido <b>antihorario</b>. Así, el primer arco va de 30° a 150° pasando por arriba, y el segundo de 210° a 330° pasando por
abajo. Entre ellos quedan dos huecos de 60°. <code>Arc2D.OPEN</code> indica que solo se dibuja la curva (con
<code>CHORD</code> se cerraría con una línea recta, y con <code>PIE</code> como una porción de pastel).</p>
"""),
             ("// Punta de flecha", r"""
<p class="l"><b>L130</b> Comentario: una punta de flecha al final del arco, apuntando en el sentido del giro.</p>
<p class="l"><b>L131</b> <code>a</code>: el ángulo donde <b>termina</b> el arco (inicio + 120), pasado a radianes. Para el
primer arco, 150°.</p>
<p class="l"><b>L132</b> La x del punto donde termina el arco: <code>cx + r · cos(a)</code>. El coseno da cuánto se avanza en
horizontal al recorrer un ángulo sobre un círculo de radio 1. Con <code>t = 100</code>: 50 + 34 · cos 150° = 50 − 29.44 =
<b>20.56</b>.</p>
<p class="l"><b>L133</b> La y: <code>cy − r · sin(a)</code>. ¿Por qué con <b>menos</b>? En matemáticas la y crece hacia
arriba, pero en la pantalla crece hacia abajo (capítulo 37). Como <code>Arc2D</code> mide sus ángulos al estilo matemático,
para que nuestro punto coincida con el final del arco hay que invertir el signo. 50 − 34 · 0.5 = <b>33</b>. El punto
<code>P = (20.56, 33)</code> queda arriba a la izquierda, justo donde termina el arco.</p>
<p class="l"><b>L134–L135</b> La <b>dirección tangente</b>: hacia dónde se movería un punto que siguiera recorriendo el
círculo en sentido antihorario. Matemáticamente es la derivada de la posición, <code>(−sin a, −cos a)</code> con la y ya
invertida. Para 150°: (−0.5, 0.866): hacia la izquierda y hacia abajo. Tiene sentido: pasado el punto de las 10 del reloj,
girando al revés de las agujas, se baja hacia las 9.</p>
<p class="l"><b>L136–L137</b> La <b>dirección radial</b>: del centro hacia afuera, pasando por P. Es
<code>(cos a, −sin a)</code>: para 150°, (−0.866, −0.5). La tangente y la radial son perpendiculares, como la vía del tren
(tangente) y los durmientes (radiales).</p>
"""),
             ("double largo", r"""
<p class="l"><b>L138–L139</b> El tamaño de la punta: 17 % de <code>t</code> de largo (hacia adelante) y 14 % de ancho
(hacia cada lado).</p>
<p class="l"><b>L140</b> Un camino para el triángulo de la punta.</p>
<p class="l"><b>L141</b> La <b>punta</b>: desde P, avanza <code>largo</code> en la dirección tangente. Con
<code>t = 100</code>: (20.56 − 0.5 · 17, 33 + 0.866 · 17) = <b>(12.06, 47.72)</b>.</p>
<p class="l"><b>L142</b> Primera esquina de la base: desde P, <code>ancho</code> hacia afuera (sumando la radial):
(20.56 − 0.866 · 14, 33 − 0.5 · 14) = <b>(8.43, 26)</b>.</p>
<p class="l"><b>L143</b> Segunda esquina: <code>ancho</code> hacia adentro (restando la radial): <b>(32.68, 40)</b>. La base
queda atravesada sobre el arco, centrada en P, de modo que la punta continúa la línea con naturalidad.</p>
<p class="l"><b>L144–L145</b> Cierra el triángulo y lo rellena con el color actual.</p>
<p class="l"><b>L146–L147</b> Cierran el <code>for</code> y la lambda. En la segunda vuelta (<code>inicio</code> = 210) todo
se repite con 330°: P = (79.44, 67), la punta en (87.94, 52.28), apuntando hacia arriba a la derecha. Las dos flechas
persiguen en círculo, en sentido antihorario.</p>
"""),
             ("PERSONA =", r"""
<p class="l"><b>L149</b> Comentario: silueta de persona (tarjetas de jugador).</p>
<p class="l"><b>L150</b> Esta constante no usa una lambda sino una <b>referencia a método</b> (capítulo 25):
<code>Iconos::persona</code> significa «el método <code>persona</code> de la clase <code>Iconos</code>». Funciona porque
<code>persona</code> (L243) recibe exactamente lo mismo que <code>dibujar</code>: un <code>Graphics2D</code>, tres
<code>double</code> y un <code>Color</code>. Se usa aquí porque la silueta se necesita también como método normal, para
reutilizarla en <code>PERSONAS</code>. Equivale a escribir <code>(g, x, y, t, c) -&gt; persona(g, x, y, t, c)</code>.</p>
"""),
             ("PERSONAS =", r"""
<p class="l"><b>L152–L153</b> Comentario: dos personas (opción de 2 jugadores).</p>
<p class="l"><b>L154</b> La persona de <b>atrás</b>: más pequeña (52 % de <code>t</code>), desplazada a la derecha (0.42) y
un poco más abajo (0.26), y semitransparente (alfa 170). La transparencia y el tamaño crean profundidad: lo lejano se ve
más pequeño y más apagado.</p>
<p class="l"><b>L155</b> La persona de <b>adelante</b>: más grande (66 %), a la izquierda, color pleno. Se dibuja después
para que quede encima de la otra. Un icono compuesto de otros dos, reutilizando un método en lugar de copiar su código.</p>
"""),
             ("COMPUTADORA =", r"""
<p class="l"><b>L158–L159</b> Comentario y comienzo del chip (opción contra la IA).</p>
<p class="l"><b>L160</b> Un grosor común para todos los trazos del chip: 7 % de <code>t</code>.</p>
<p class="l"><b>L161–L162</b> El cuerpo del chip: un rectángulo redondeado de 0.6 × 0.6 a partir de (0.2, 0.2), con esquinas
de 0.16, trazado sin halo. La instrucción ocupa dos líneas; el <code>;</code> está al final de la segunda.</p>
<p class="l"><b>L163</b> El núcleo: un cuadrado redondeado más pequeño, en el centro (de 0.37 a 0.63), <b>relleno</b>. Un
detalle sutil: aquí no se elige color. <code>g.fill</code> usa el color actual, que es <code>c</code> porque
<code>Dibujo.trazo</code> lo acaba de poner en L161. Funciona, pero es una dependencia escondida: si un día se cambiara el
orden de estas líneas, el núcleo saldría de otro color. Tenlo en cuenta en tus propios iconos.</p>
"""),
             ("Path2D patas", r"""
<p class="l"><b>L164</b> Un solo camino para las doce patitas.</p>
<p class="l"><b>L165</b> Un <code>for</code> con <code>i</code> = 0, 1 y 2: tres patas por lado.</p>
<p class="l"><b>L166</b> La posición de la pata a lo largo del lado: <code>0.34 + 0.16 · i</code>, es decir 0.34, 0.50 y
0.66 (por <code>t</code>). Las tres quedan centradas en el chip (la del medio en 0.5) y repartidas por igual.</p>
<p class="l"><b>L167–L168</b> Pata de <b>arriba</b>: vertical, en la x <code>p</code>, de 0.05 a 0.19 (justo hasta el borde
del chip, que empieza en 0.2).</p>
<p class="l"><b>L169–L170</b> Pata de <b>abajo</b>: la misma x, de 0.81 a 0.95.</p>
"""),
             ("patas.moveTo(x + t * 0.05", r"""
<p class="l"><b>L171–L172</b> Pata de la <b>izquierda</b>: horizontal, ahora en la altura <code>p</code>, de 0.05 a 0.19.
Fíjate en que es la de arriba con x e y intercambiadas.</p>
<p class="l"><b>L173–L174</b> Pata de la <b>derecha</b>, de 0.81 a 0.95.</p>
<p class="l"><b>L175</b> Fin del bucle: 3 vueltas × 4 patas = 12 segmentos en el mismo camino.</p>
<p class="l"><b>L176</b> Se trazan todas de una vez. Un bucle para lo que se repite: si el diseño pidiera cuatro patas por
lado, bastaría cambiar el 3 y el 0.16.</p>
"""),
             ("TROFEO =", r"""
<p class="l"><b>L179</b> Comentario: trofeo con estrella (pantalla de victoria).</p>
<p class="l"><b>L180–L181</b> La lambda y el camino de la copa.</p>
<p class="l"><b>L182–L183</b> El borde superior de la copa: una recta de (0.24, 0.08) a (0.76, 0.08).</p>
<p class="l"><b>L184</b> Baja por el lado derecho, un poco hacia adentro, hasta (0.73, 0.36).</p>
<p class="l"><b>L185</b> Una curva hasta el fondo de la copa (0.5, 0.6), atraída hacia (0.69, 0.58): el lado derecho se
redondea.</p>
<p class="l"><b>L186</b> La curva simétrica del lado izquierdo, hasta (0.27, 0.36). Simetría: 0.69 ↔ 0.31, 0.73 ↔ 0.27.</p>
<p class="l"><b>L187</b> Cierra la copa subiendo al punto inicial.</p>
"""),
             ("Path2D asas", r"""
<p class="l"><b>L189</b> Un camino aparte para las asas, porque se dibujarán distinto (solo trazo, sin relleno).</p>
<p class="l"><b>L190–L192</b> Asa izquierda: sale del borde de la copa (0.25, 0.16), va recta hacia afuera hasta (0.1, 0.16) y
vuelve a la copa con una curva que baja hasta (0.31, 0.46), atraída hacia (0.08, 0.42): una oreja redondeada.</p>
<p class="l"><b>L193–L195</b> Asa derecha, reflejada: cada x se convierte en 1 − x (0.25 → 0.75, 0.1 → 0.9, 0.08 → 0.92,
0.31 → 0.69).</p>
"""),
             ("Area pie", r"""
<p class="l"><b>L197</b> El pie del trofeo se arma como un <code>Area</code>. Primera pieza: el tallo, un rectángulo
estrecho de (0.45, 0.58), 0.1 de ancho y 0.16 de alto.</p>
<p class="l"><b>L198</b> <code>pie.add(...)</code> <b>suma</b> (une) una segunda pieza: una base intermedia, rectángulo
redondeado de 0.34 de ancho a la altura 0.72.</p>
<p class="l"><b>L199</b> Y una tercera: la base ancha, de 0.48 de ancho, a la altura 0.8. ¿Por qué unir en un
<code>Area</code> en vez de rellenar las tres figuras por separado? Porque así el pie es <b>una sola figura</b>: se rellena
una vez, con un solo degradado continuo, y si se trazara su contorno, no se verían las líneas internas donde se tocan las
piezas.</p>
"""),
             ("Dibujo.trazoNeon(g, copa", r"""
<p class="l"><b>L201</b> El contorno de la copa con neón. El grosor es <b>fijo</b>, 1.5 píxeles, no proporcional a
<code>t</code>: es solo un filo luminoso alrededor del relleno, con intensidad 0.9.</p>
<p class="l"><b>L202</b> Las asas con neón, estas sí proporcionales (6 % de <code>t</code>).</p>
<p class="l"><b>L203</b> Un degradado <b>vertical</b>: los dos puntos tienen la misma x (0) y distinta y, de arriba
(<code>y</code>, color aclarado un 35 %) hasta abajo (<code>y + t</code>, color puro). Brillo arriba, color pleno abajo,
como un metal iluminado desde arriba.</p>
<p class="l"><b>L204–L205</b> Rellena la copa y el pie con ese mismo degradado. Como el degradado se definió para todo el
cuadrado, las dos piezas comparten la misma luz, como si fueran un solo objeto.</p>
<p class="l"><b>L206</b> El color de la estrella: el fondo oscuro (<code>FONDO_ABAJO</code>) con alfa 190. Una estrella
oscura sobre la copa clara parece grabada o calada en el metal.</p>
<p class="l"><b>L207</b> Rellena una estrella centrada en (0.5, 0.32), en la parte ancha de la copa, con radio exterior 0.11
y radio interior 0.045. El método <code>estrella</code> está en L252.</p>
"""),
             ("LOGO =", r"""
<p class="l"><b>L210</b> Comentario: el logotipo del encabezado, la rejilla del totito con dos O y una X. Es también el
icono de la ventana (capítulo 61) y el del programa instalado (capítulo 64).</p>
<p class="l"><b>L211–L212</b> Un grosor fino común: 4.5 % de <code>t</code>.</p>
<p class="l"><b>L213</b> El camino de la rejilla «#».</p>
<p class="l"><b>L214–L215</b> Primera línea vertical: de (0.37, 0.04) a (0.35, 0.96). Fíjate en que la x cambia de 0.37 a
0.35: la línea está ligeramente <b>inclinada</b>. Es a propósito: como un totito dibujado a mano con tiza, le da un aire
juguetón. Un logo perfectamente recto se vería más frío.</p>
<p class="l"><b>L216–L217</b> Segunda vertical, también inclinada (0.65 → 0.63).</p>
"""),
             ("rejilla.moveTo(x + t * 0.04, y + t * 0.36)", r"""
<p class="l"><b>L218–L221</b> Las dos horizontales, con la misma inclinación leve (0.36 → 0.34 y 0.66 → 0.64).</p>
<p class="l"><b>L222</b> La rejilla con neón tenue (intensidad 0.6), en el color que se pida (en el juego, lavanda).</p>
<p class="l"><b>L223</b> Una O en la casilla de arriba a la izquierda: un círculo de 0.18 de diámetro. Esta vez el color no
es <code>c</code>, sino <code>Tema.MORADO</code> fijo: las fichas del logo son siempre moradas, se pida en el color que se
pida la rejilla.</p>
<p class="l"><b>L224</b> Otra O, en la casilla de arriba a la derecha (con la y ligeramente distinta, 0.07: el mismo toque
«a mano»).</p>
"""),
             ("Path2D equis = new Path2D.Double();", r"""
<p class="l"><b>L225–L229</b> Una X pequeña en la casilla de abajo a la izquierda: dos diagonales en un cuadrado de 0.16 de
lado (de 0.09 a 0.25 en x, de 0.75 a 0.91 en y). Es la misma técnica que <code>dibujarX</code> del capítulo 41.</p>
<p class="l"><b>L230</b> La X con neón morado tenue. El logo resume el juego: la rejilla y unas fichas de partida en
curso.</p>
"""),
             ("CERRAR =", r"""
<p class="l"><b>L233</b> Comentario: la X de cerrar de la esquina del encabezado.</p>
<p class="l"><b>L234–L239</b> Dos diagonales, de (0.22, 0.22) a (0.78, 0.78) y de (0.78, 0.22) a (0.22, 0.78). El margen de
0.22 hace que la X sea más pequeña que el botón redondo que la contiene.</p>
<p class="l"><b>L240</b> Neón grueso (11 % de <code>t</code>) con intensidad 0.8. Es la misma idea que la ficha X, pero como
icono: el botón la recibe con el color que quiera (rosa, en el encabezado).</p>
"""),
             ("private static void persona", r"""
<p class="l"><b>L243</b> El método privado de la silueta. Tiene la misma firma que <code>Icono.dibujar</code>, y por eso
<code>Iconos::persona</code> encaja en una constante <code>Icono</code> (L150). Es <code>private</code>: desde fuera se usa a
través de <code>PERSONA</code>.</p>
<p class="l"><b>L244</b> Un degradado vertical, de un color algo aclarado arriba a uno puro abajo, como en el trofeo.</p>
<p class="l"><b>L245</b> La cabeza: un círculo de 0.4 de diámetro en (0.3, 0.04), es decir, con centro en (0.5, 0.24).</p>
<p class="l"><b>L246</b> El cuerpo empieza siendo un círculo <b>grande</b>: diámetro 0.84, desde (0.08, 0.5); su centro queda
en (0.5, 0.92), cerca del borde inferior.</p>
<p class="l"><b>L247</b> <code>cuerpo.intersect(...)</code> se queda solo con la parte <b>común</b> al círculo y a un
rectángulo que va de la altura 0.5 a la 0.96. Del círculo sobrevive la parte de arriba, cortada en recto por abajo: una
<b>cúpula</b> de base plana, como unos hombros. Sin el recorte, el cuerpo sería un círculo entero que se saldría del
cuadrado.</p>
<p class="l"><b>L248</b> Rellena el cuerpo con el mismo degradado de la cabeza.</p>
"""),
             ("private static Shape estrella", r"""
<p class="l"><b>L251</b> Comentario: estrella de cinco puntas centrada en <code>(cx, cy)</code>.</p>
<p class="l"><b>L252</b> A diferencia de los iconos, este ayudante recibe el <b>centro</b> y dos radios, y en vez de dibujar,
<b>devuelve</b> la figura (<code>Shape</code>). Así quien lo llama decide si la rellena, la traza o la combina.</p>
<p class="l"><b>L253</b> El camino de la estrella.</p>
<p class="l"><b>L254</b> Una estrella de cinco puntas es un polígono de <b>diez</b> vértices: cinco puntas (lejos del
centro) y cinco «valles» entre ellas (cerca del centro).</p>
<p class="l"><b>L255</b> <code>i % 2</code> es el resto de dividir <code>i</code> entre 2: 0 para los pares, 1 para los
impares. Los vértices pares usan el radio exterior (puntas) y los impares el interior (valles). Así se alternan.</p>
<p class="l"><b>L256</b> El ángulo de cada vértice: <code>−π/2 + i · π/5</code>. <code>Math.PI</code> es π (180° en
radianes), así que <code>π/5</code> son 36°: diez vértices × 36° = una vuelta. Empieza en <code>−π/2</code> (−90°) para que
la primera punta quede <b>arriba</b>.</p>
<p class="l"><b>L257–L258</b> La posición del vértice: centro más radio por coseno (horizontal) y por seno (vertical). Aquí
la y se <b>suma</b>, no se resta como en <code>REINICIAR</code>: no hay que coincidir con ningún <code>Arc2D</code>, así que
se usa directamente la convención de la pantalla (y hacia abajo). Con ella, −90° apunta hacia arriba, porque
<code>sin(−90°) = −1</code> resta altura.</p>
"""),
             ("if (i == 0)", r"""
<p class="l"><b>L259–L263</b> El primer vértice (<code>i == 0</code>) usa <code>moveTo</code> para colocar el lápiz; los
otros nueve, <code>lineTo</code>, para unirlos en orden. Sin este <code>if</code>, un <code>lineTo</code> sin un
<code>moveTo</code> previo daría un error al construir el camino.</p>
<p class="l"><b>L265</b> Cierra el polígono del último valle a la primera punta.</p>
<p class="l"><b>L266</b> Devuelve la figura terminada.</p>
<p class="l"><b>L267–L268</b> Cierran el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>Del botón a la lambda</h3>
<p>Cuando cargas la clase <code>Iconos</code>, Java crea trece objetos, uno por constante; cada uno «guarda» el código de su
lambda sin ejecutarlo. Más adelante, el botón «Jugar» del menú (capítulo 44) recibe <code>Iconos.JUGAR</code> y, en su
<code>paintComponent</code>, hace algo como:</p>
<pre class="java">icono.dibujar(g2, 40, 25, 30, Tema.ROSA);</pre>
<p>En ese momento se ejecuta, por fin, el cuerpo de la lambda, con <code>x = 40</code>, <code>y = 25</code>,
<code>t = 30</code> y <code>c = ROSA</code>. El triángulo queda con esquinas en (47.2, 29.2), (65.8, 40) y (47.2, 50.8). El
botón no sabe qué icono le tocó: solo sabe que es un <code>Icono</code> y que se dibuja con <code>dibujar</code>. Es el patrón
<b>Strategy</b> del capítulo 27: el «cómo dibujar» se pasa como un objeto intercambiable.</p>
<p>¿Por qué no trece clases (<code>class IconoJugar implements Icono</code>…)? Funcionaría, pero serían trece archivos con
mucho código repetido. ¿Y un método con un <code>switch</code> por nombre (<code>dibujar("jugar", ...)</code>)? Un error
de tipeo en el nombre solo se descubriría al ejecutar; con constantes, el compilador lo detecta.</p>

<h3>La geometría de REINICIAR, con números</h3>
<svg viewBox="-5 -5 110 110" width="60%">
<rect x="-5" y="-5" width="110" height="110" rx="4" fill="#1C1740"/>
<circle cx="50" cy="50" r="34" fill="none" stroke="#C8BCF6" stroke-opacity="0.35" stroke-width="0.6" stroke-dasharray="1.5 1.5"/>
<path d="M 79.44 33 A 34 34 0 0 0 20.56 33" fill="none" stroke="#C8BCF6" stroke-width="4" stroke-linecap="round"/>
<path d="M 20.56 67 A 34 34 0 0 0 79.44 67" fill="none" stroke="#C8BCF6" stroke-width="4" stroke-linecap="round"/>
<polygon points="12.06,47.72 8.43,26 32.68,40" fill="#FF3BD4" fill-opacity="0.85"/>
<polygon points="87.94,52.28 91.57,74 67.32,60" fill="#C8BCF6"/>
<line x1="50" y1="50" x2="20.56" y2="33" stroke="#A05CFF" stroke-width="0.6" stroke-dasharray="1.5 1"/>
<line x1="50" y1="50" x2="84" y2="50" stroke="#A05CFF" stroke-width="0.6" stroke-dasharray="1.5 1"/>
<line x1="20.56" y1="33" x2="12.06" y2="47.72" stroke="#2F84FF" stroke-width="1.2"/>
<line x1="8.43" y1="26" x2="32.68" y2="40" stroke="#40C8FF" stroke-width="1.2"/>
<circle cx="20.56" cy="33" r="1.6" fill="#FFFFFF"/>
<circle cx="50" cy="50" r="1.2" fill="#FFFFFF"/>
<g font-size="4.2" font-family="sans-serif">
<text x="23" y="31" fill="#FFFFFF">P (20.56, 33)</text>
<text x="52" y="47" fill="#A05CFF">150°</text>
<text x="81" y="31" fill="#C8BCF6">30°</text>
<text x="1" y="55" fill="#2F84FF">punta</text>
<text x="1" y="22" fill="#40C8FF">radial</text>
<text x="52" y="56" fill="#FFFFFF">(cx, cy)</text>
</g>
</svg>
<p>Con <code>x = y = 0</code> y <code>t = 100</code> (centro (50, 50), radio 34, largo 17, ancho 14). La primera flecha
(en rosa en la figura) termina a 150°; la línea azul es la dirección tangente y la cian, la radial:</p>
<table class="tabla">
<tr><th>Cálculo</th><th>Fórmula</th><th>Arco 1 (inicio 30°)</th><th>Arco 2 (inicio 210°)</th></tr>
<tr><td>Ángulo final <code>a</code></td><td>inicio + 120</td><td>150°</td><td>330°</td></tr>
<tr><td>cos a, sin a</td><td></td><td>−0.866, 0.5</td><td>0.866, −0.5</td></tr>
<tr><td>Punto final P</td><td>(cx + r·cos a, cy − r·sin a)</td><td>(20.56, 33)</td><td>(79.44, 67)</td></tr>
<tr><td>Tangente</td><td>(−sin a, −cos a)</td><td>(−0.5, 0.866)</td><td>(0.5, −0.866)</td></tr>
<tr><td>Radial</td><td>(cos a, −sin a)</td><td>(−0.866, −0.5)</td><td>(0.866, 0.5)</td></tr>
<tr><td>Punta</td><td>P + tangente · 17</td><td>(12.06, 47.72)</td><td>(87.94, 52.28)</td></tr>
<tr><td>Base 1</td><td>P + radial · 14</td><td>(8.43, 26)</td><td>(91.57, 74)</td></tr>
<tr><td>Base 2</td><td>P − radial · 14</td><td>(32.68, 40)</td><td>(67.32, 60)</td></tr>
</table>
<p>Fíjate en la última columna: todos los números son los de la primera reflejados respecto al centro (20.56 ↔ 79.44,
33 ↔ 67). Es lógico: la segunda flecha es la primera girada 180°.</p>

<h3>Sumar, restar e intersecar</h3>
<svg viewBox="0 0 380 175" width="100%">
<rect x="0" y="0" width="380" height="175" rx="12" fill="#1C1740"/>
<polygon points="70,20 112,58 28,58" fill="#C8BCF6" stroke="#C8BCF6" stroke-width="8" stroke-linejoin="round"/>
<path d="M40 54 H100 V100 H79 V72.5 Q79 70 76.5 70 H63.5 Q61 70 61 72.5 V100 H40 Z" fill="#C8BCF6"/>
<rect x="61" y="70" width="18" height="32" rx="2.5" fill="none" stroke="#FF3BD4" stroke-width="1.2" stroke-dasharray="3 2"/>
<g transform="translate(110,-60) scale(1.6)">
<rect x="45" y="58" width="10" height="16" fill="#40C8FF"/>
<rect x="33" y="72" width="34" height="8" rx="2" fill="#40C8FF"/>
<rect x="26" y="80" width="48" height="11" rx="2.5" fill="#40C8FF"/>
<g fill="none" stroke="#FFFFFF" stroke-width="0.6" stroke-dasharray="2 1.5">
<rect x="45" y="58" width="10" height="16"/><rect x="33" y="72" width="34" height="8" rx="2"/><rect x="26" y="80" width="48" height="11" rx="2.5"/>
</g>
</g>
<circle cx="310" cy="34" r="20" fill="#2F84FF"/>
<circle cx="310" cy="102" r="42" fill="none" stroke="#FF3BD4" stroke-width="1.2" stroke-dasharray="3 2"/>
<rect x="260" y="60" width="100" height="46" fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-dasharray="3 2"/>
<path d="M268.2 106 A 42 42 0 1 1 351.8 106 Z" fill="#2F84FF"/>
<g fill="#FFFFFF" font-size="11" text-anchor="middle" font-family="sans-serif">
<text x="70" y="160">subtract: restar</text><text x="190" y="160">add: unir</text><text x="310" y="160">intersect: lo común</text>
</g>
</svg>
<table class="tabla">
<tr><th>Operación</th><th>Qué hace</th><th>En el Totito</th></tr>
<tr><td><code>a.add(b)</code></td><td>Unión: lo que está en <code>a</code> o en <code>b</code>.</td><td>El pie del trofeo: tallo + base media + base ancha, una sola figura.</td></tr>
<tr><td><code>a.subtract(b)</code></td><td>Diferencia: lo que está en <code>a</code> y no en <code>b</code>.</td><td>La casa: el cuerpo menos la puerta (en rosa, la figura que se resta).</td></tr>
<tr><td><code>a.intersect(b)</code></td><td>Intersección: solo lo que está en los dos.</td><td>La silueta: un círculo grande (rosa) recortado por un rectángulo (blanco).</td></tr>
<tr><td><code>a.exclusiveOr(b)</code></td><td>Lo que está en uno solo de los dos.</td><td>No se usa; sirve, por ejemplo, para un anillo dibujado como dos círculos.</td></tr>
</table>
<p>Ojo: estas operaciones <b>modifican</b> el <code>Area</code> sobre el que se llaman (<code>cuerpo</code> cambia) y no
devuelven nada.</p>

<h3>La estrella de cinco puntas</h3>
<svg viewBox="0 0 200 200" width="40%">
<rect x="0" y="0" width="200" height="200" rx="12" fill="#1C1740"/>
<circle cx="100" cy="100" r="80" fill="none" stroke="#C8BCF6" stroke-opacity="0.4" stroke-dasharray="3 3"/>
<circle cx="100" cy="100" r="32" fill="none" stroke="#C8BCF6" stroke-opacity="0.4" stroke-dasharray="3 3"/>
<polygon points="100.0,20.0 118.8,74.1 176.1,75.3 130.4,109.9 147.0,164.7 100.0,132.0 53.0,164.7 69.6,109.9 23.9,75.3 81.2,74.1" fill="#40C8FF" fill-opacity="0.8" stroke="#FFFFFF" stroke-width="1"/>
<g font-size="11" font-family="sans-serif">
<text x="100" y="14" fill="#FF3BD4" text-anchor="middle">0</text>
<text x="125" y="70" fill="#FFFFFF" text-anchor="middle">1</text>
<text x="186" y="76" fill="#FF3BD4" text-anchor="middle">2</text>
<text x="140" y="117" fill="#FFFFFF" text-anchor="middle">3</text>
<text x="153" y="177" fill="#FF3BD4" text-anchor="middle">4</text>
<text x="100" y="146" fill="#FFFFFF" text-anchor="middle">5</text>
<text x="47" y="177" fill="#FF3BD4" text-anchor="middle">6</text>
<text x="60" y="117" fill="#FFFFFF" text-anchor="middle">7</text>
<text x="14" y="76" fill="#FF3BD4" text-anchor="middle">8</text>
<text x="75" y="70" fill="#FFFFFF" text-anchor="middle">9</text>
</g></svg>
<p>Los diez vértices de <code>estrella(0, 0, 10, 4)</code> (radio exterior 10, interior 4), en el orden en que los recorre
el bucle:</p>
<table class="tabla">
<tr><th>i</th><th>Radio</th><th>Ángulo</th><th>(cos · r, sin · r)</th><th>i</th><th>Radio</th><th>Ángulo</th><th>(cos · r, sin · r)</th></tr>
<tr><td>0</td><td>10</td><td>−90°</td><td>(0, −10)</td><td>5</td><td>4</td><td>90°</td><td>(0, 4)</td></tr>
<tr><td>1</td><td>4</td><td>−54°</td><td>(2.35, −3.24)</td><td>6</td><td>10</td><td>126°</td><td>(−5.88, 8.09)</td></tr>
<tr><td>2</td><td>10</td><td>−18°</td><td>(9.51, −3.09)</td><td>7</td><td>4</td><td>162°</td><td>(−3.80, 1.24)</td></tr>
<tr><td>3</td><td>4</td><td>18°</td><td>(3.80, 1.24)</td><td>8</td><td>10</td><td>198°</td><td>(−9.51, −3.09)</td></tr>
<tr><td>4</td><td>10</td><td>54°</td><td>(5.88, 8.09)</td><td>9</td><td>4</td><td>234°</td><td>(−2.35, −3.24)</td></tr>
</table>
<p>Recuerda que en la pantalla una y negativa es <b>arriba</b>: el vértice 0, (0, −10), es la punta superior. En el trofeo
la estrella se pide con radios 0.11 · t y 0.045 · t (proporción 0.41); en la estrella «perfecta» de una bandera la
proporción es de 0.38. Cuanto más pequeño el radio interior, más afiladas las puntas.</p>

<h2>Compila y prueba</h2>
<p>La comprobación de este capítulo: <i>Run → Clean and Build Project</i> (Shift+F11) con <code>BUILD SUCCESS</code>, o:</p>
<pre class="ps">javac -encoding UTF-8 -d out src\*.java</pre>
<p>Con esto terminan los cimientos. A partir del capítulo 43 empiezas a construir componentes que usan
<code>Tema</code>, <code>Dibujo</code> e <code>Iconos</code>, y en el 56 verás todo junto en la primera pantalla.</p>

<h3>Prueba opcional: el muestrario de iconos</h3>
<p>Igual que en el capítulo 41, puedes pintar los trece iconos en una imagen. Crea en la raíz del proyecto el archivo
temporal <code>MuestraIconos.java</code>:</p>
<pre class="java">import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;

public class MuestraIconos {
    public static void main(String[] args) throws Exception {
        BufferedImage imagen = new BufferedImage(780, 240, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = Dibujo.preparar(imagen.getGraphics());
        g2.setColor(Tema.FONDO_ARRIBA);
        g2.fillRect(0, 0, 780, 240);
        Iconos.Icono[] iconos = {Iconos.JUGAR, Iconos.LIBRO, Iconos.SALIR, Iconos.CHEVRON,
            Iconos.FLECHA_IZQUIERDA, Iconos.CASA, Iconos.REINICIAR, Iconos.PERSONA, Iconos.PERSONAS,
            Iconos.COMPUTADORA, Iconos.TROFEO, Iconos.LOGO, Iconos.CERRAR};
        for (int k = 0; k &lt; iconos.length; k++) {
            int x = 20 + (k % 7) * 108;
            int y = 20 + (k / 7) * 110;
            iconos[k].dibujar(g2, x, y, 84, Tema.LAVANDA);
        }
        g2.dispose();
        ImageIO.write(imagen, "png", new File("iconos.png"));
        System.out.println("Listo: abre iconos.png");
    }
}</pre>
<p>Fíjate en <code>Iconos.Icono[]</code>: un arreglo de iconos, que se recorre llamando a <code>dibujar</code> sin saber
cuál es cada uno. <code>k % 7</code> da la columna (0 a 6) y <code>k / 7</code> (división entera) la fila.</p>
<pre class="ps">java -cp target\classes MuestraIconos.java
Invoke-Item iconos.png
Remove-Item MuestraIconos.java, iconos.png</pre>
<p>(Ejecuta la última línea después de mirar la imagen.) Deberías ver dos filas de iconos lavanda: triángulo, libro, puerta,
chevron, flecha, casa y flechas circulares arriba; persona, personas, chip, trofeo, logotipo y X de cerrar abajo.</p>

<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Mensaje</th><th>Causa y solución</th></tr>
<tr><td><code>incompatible types: incompatible parameter types in lambda expression</code></td><td>La lambda no coincide con <code>dibujar</code>: revisa que tenga exactamente cinco parámetros <code>(g, x, y, t, c)</code> y que no devuelva nada.</td></tr>
<tr><td><code>possible lossy conversion from double to float</code></td><td>Falta un <code>(float)</code> al pasar <code>t * 0.1</code> a <code>trazoNeon</code> o a <code>GradientPaint</code>.</td></tr>
<tr><td><code>';' expected</code> después de <code>}</code></td><td>Falta el <code>;</code> que cierra la asignación de la constante: <code>};</code></td></tr>
<tr><td><code>incompatible types: invalid method reference</code></td><td>La firma de <code>persona</code> no coincide con la de <code>dibujar</code> (mismo orden y tipos de parámetros).</td></tr>
</table>

<div class="caja git"><b>Git</b> Último commit de los cimientos.
<pre class="ps">git status
git add src\Iconos.java
git commit -m "Iconos dibujados con codigo"
git push
git log --oneline -6</pre>
El <code>log</code> debe mostrar tus cinco commits de la rama <code>interfaz-neon</code> (Partida, Navegacion, Tema, Dibujo,
Iconos) encima del último de <code>main</code>.</div>

<h2>Resumen</h2>
<ul>
<li>Los iconos son recetas de figuras, no imágenes: nítidos a cualquier tamaño, en cualquier color y con el mismo neón.</li>
<li>Regla común: un cuadrado de lado <code>t</code> en <code>(x, y)</code>, y todas las medidas como fracciones de <code>t</code>, sacadas de un boceto en cuadrícula.</li>
<li><code>Icono</code> es una interfaz funcional; cada icono es una constante con una lambda (o una referencia a método, <code>Iconos::persona</code>).</li>
<li><code>Path2D</code> (<code>moveTo</code>, <code>lineTo</code>, <code>quadTo</code>, <code>closePath</code>), <code>Arc2D</code>, <code>RoundRectangle2D</code> y <code>GradientPaint</code> construyen casi todo.</li>
<li><code>Area</code> combina figuras: <code>add</code> (trofeo), <code>subtract</code> (casa), <code>intersect</code> (silueta).</li>
<li>Seno y coseno dan puntos sobre un círculo; la tangente y la radial orientan las puntas de flecha; la estrella alterna dos radios cada 36°.</li>
<li>La y de la pantalla crece hacia abajo: con ángulos «de matemáticas» (<code>Arc2D</code>) se resta el seno.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Iconos para cualquier aplicación de escritorio:</b> una barra de herramientas (guardar, abrir, imprimir) con iconos que cambian de color en modo oscuro sin duplicar archivos.</li>
<li><b>Indicadores y medidores:</b> un velocímetro o una barra de progreso circular es un <code>Arc2D</code> cuya extensión depende de un valor (por ejemplo, <code>360 * porcentaje</code>), con una aguja calculada con seno y coseno.</li>
<li><b>Formas a medida con <code>Area</code>:</b> una tarjeta con una muesca, un globo de diálogo (rectángulo redondeado + triángulo), una llave o una dona (círculo menos círculo).</li>
<li><b>Lambdas como «piezas intercambiables»:</b> cualquier lista de acciones (los filtros de una app de fotos, las reglas de descuento de una tienda) se puede guardar como constantes de una interfaz funcional.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Con <code>t = 50</code>, <code>x = 10</code> e <code>y = 20</code>, calcula las tres esquinas del triángulo de
<code>JUGAR</code>. Pista: la primera es (10 + 50 · 0.24, 20 + 50 · 0.14) = (22, 27).</li>
<li>Diseña en papel cuadriculado un icono de «pausa» (dos barras verticales) y escríbelo como una constante
<code>PAUSA</code> en tu archivo de prueba (no en <code>Iconos</code>), con <code>RoundRectangle2D</code> y <code>g.fill</code>.
Agrégalo al muestrario.</li>
<li>Cambia en tu prueba el <code>120</code> del arco por <code>150</code> y el <code>+ 120</code> del ángulo por <code>+ 150</code>.
¿Qué le pasa al icono? ¿Y si inviertes el signo de la tangente?</li>
<li>Escribe una estrella de seis puntas cambiando el 10 y el <code>Math.PI / 5</code>. Pista: 12 vértices, cada 30°.</li>
<li>Reto: diseña un icono de «engranaje» como un <code>Area</code>: un círculo, al que le <code>add</code> ocho rectángulos
pequeños (los dientes) girados con <code>AffineTransform.getRotateInstance</code>, y al que le <code>subtract</code> un círculo
central.</li>
</ol></div>
""",
}
