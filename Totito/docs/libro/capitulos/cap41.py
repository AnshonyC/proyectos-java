# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 41,
    "titulo": "Dibujo.java: el efecto neón",
    "antes": r"""
<p class="entrada">Este es el archivo que hace que el Totito brille. Con un truco tan simple como trazar la misma línea
seis veces, cada vez más fina y más opaca, cualquier figura parece un tubo de neón encendido. Además, aquí viven las
herramientas de dibujo que comparten todos los componentes: preparar el lápiz, fijar tamaños, dibujar las fichas X y O,
escribir texto con halo, centrarlo y recortarlo.</p>

<h2>Por qué existe este archivo</h2>
<p>El diseño del Totito (capítulo 34) no tiene ni una imagen: todo son líneas luminosas sobre un fondo oscuro. Los botones
tienen bordes neón, las tarjetas también, el tablero, las fichas, los iconos, el título. Si cada uno de esos componentes
programara su propio brillo, tendríamos quince versiones ligeramente distintas del mismo efecto y, peor, quince lugares
que cambiar si el brillo resulta demasiado fuerte.</p>
<p><code>Dibujo</code> reúne en un solo lugar todo lo que <b>más de un componente</b> necesita para dibujar. Es una caja de
herramientas, como <code>Tema</code> es la caja de pinturas. A partir del capítulo 43, cada componente empezará su
<code>paintComponent</code> con <code>Dibujo.preparar(g)</code> y usará <code>Dibujo.trazoNeon(...)</code> para sus
bordes.</p>

<h2>Cómo se fabrica la luz: el truco en una imagen</h2>
<p>En el capítulo 35 viste que un neón real es un tubo muy brillante, con el centro casi blanco, rodeado de un resplandor
de su color que se desvanece hacia afuera. Una computadora no emite luz «alrededor» de una línea, pero podemos
<b>imitarla</b>: dibujamos primero una línea muy gruesa y casi transparente, encima otra un poco más fina y un poco menos
transparente, y así seis veces. Donde se superponen todas (cerca del centro) el color se acumula; en el borde exterior
solo hay una capa tenue. El ojo lo interpreta como luz que se difumina. Encima va la línea nítida.</p>
<svg viewBox="0 0 720 240" width="100%">
<rect x="0" y="0" width="720" height="240" rx="12" fill="#1C1740"/>
<rect x="48" y="38" width="404" height="164" rx="82" fill="#FF3BD4" fill-opacity="0.024"/>
<rect x="60" y="50" width="380" height="140" rx="70" fill="#FF3BD4" fill-opacity="0.043"/>
<rect x="72" y="62" width="356" height="116" rx="58" fill="#FF3BD4" fill-opacity="0.063"/>
<rect x="84" y="74" width="332" height="92" rx="46" fill="#FF3BD4" fill-opacity="0.082"/>
<rect x="96" y="86" width="308" height="68" rx="34" fill="#FF3BD4" fill-opacity="0.102"/>
<rect x="108" y="98" width="284" height="44" rx="22" fill="#FF3BD4" fill-opacity="0.122"/>
<rect x="120" y="110" width="260" height="20" rx="10" fill="#FF3BD4"/>
<g stroke="#C8BCF6" stroke-width="1">
<line x1="380" y1="38" x2="490" y2="38" stroke-dasharray="2 3"/>
<line x1="380" y1="50" x2="490" y2="50" stroke-dasharray="2 3"/>
<line x1="380" y1="62" x2="490" y2="62" stroke-dasharray="2 3"/>
<line x1="380" y1="74" x2="490" y2="74" stroke-dasharray="2 3"/>
<line x1="380" y1="86" x2="490" y2="86" stroke-dasharray="2 3"/>
<line x1="380" y1="98" x2="490" y2="98" stroke-dasharray="2 3"/>
<line x1="380" y1="120" x2="490" y2="120" stroke-dasharray="2 3"/>
</g>
<g fill="#FFFFFF" font-size="11" font-family="sans-serif">
<text x="496" y="42">capa 6 · 16.4 px · alfa 6</text>
<text x="496" y="54">capa 5 · 14.0 px · alfa 11</text>
<text x="496" y="66">capa 4 · 11.6 px · alfa 16</text>
<text x="496" y="78">capa 3 · 9.2 px · alfa 21</text>
<text x="496" y="90">capa 2 · 6.8 px · alfa 26</text>
<text x="496" y="102">capa 1 · 4.4 px · alfa 31</text>
<text x="496" y="124">línea principal · 2.0 px · alfa 255</text>
</g>
<text x="250" y="228" fill="#C8BCF6" font-size="11" text-anchor="middle" font-family="sans-serif">Corte de un trazo neón de grosor 2, ampliado 10 veces</text>
</svg>
<p>Esa figura es el <b>corte</b> de un trazo neón rosa de grosor 2, como el borde de un botón, ampliado diez veces y con
las transparencias reales. Cada banda es una de las capas que dibuja el código de este capítulo; sus números exactos
salen de dos fórmulas que verás en las líneas 82 y 84.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>Por qué se trabaja sobre una <b>copia</b> del <code>Graphics</code> (<code>create</code>/<code>dispose</code>) y qué
hace cada sugerencia de calidad (<code>RenderingHints</code>).</li>
<li>Cómo fijar el tamaño de un componente para que los <code>BoxLayout</code> no lo estiren.</li>
<li>Trazos con <code>BasicStroke</code>: grosor, puntas y esquinas redondeadas.</li>
<li>El efecto neón línea por línea, con su intensidad y su centro blanco.</li>
<li>Figuras con <code>Path2D</code> (<code>moveTo</code>/<code>lineTo</code>) y <code>Ellipse2D</code>; la compensación óptica de la X.</li>
<li>Texto con halo, la <b>línea base</b> del texto y cómo centrarlo en vertical; recortar un nombre largo con «…».</li>
<li>La cortesía de dejar el lápiz como lo encontraste (guardar y restaurar estado).</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>En la rama <code>interfaz-neon</code>: clic derecho en <i>&lt;default package&gt;</i> → <i>New → Java Class…</i> → <code>Dibujo</code> → <i>Finish</i>.</li>
<li>Borra la plantilla y escribe el código. Esta clase usa <code>Tema</code> (capítulo 40), que ya debe existir.</li>
</ol>
<pre class="ps">New-Item src\Dibujo.java</pre>
<div class="caja cuidado"><b>Un carácter especial.</b> En la línea 161 hay un <code>"…"</code>: es <b>un solo carácter</b>
(los puntos suspensivos tipográficos), no tres puntos. En Windows se escribe con Alt+0133 en el teclado numérico, o
cópialo de este libro. Para que Java lo lea bien, el archivo debe guardarse en UTF-8: NetBeans lo hace solo en este
proyecto (el <code>pom.xml</code> lo indica), y por eso los comandos de compilación llevan <code>-encoding UTF-8</code>.</div>
""",
    "archivos": [
        {"ruta": "src/Dibujo.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.BasicStroke</code>: describe cómo es un trazo: su grosor, cómo terminan las puntas
y cómo se unen las esquinas. El método <code>redondo</code> lo crea.</p>
<p class="l"><b>L2</b> <code>java.awt.Color</code>: el color (capítulo 40).</p>
<p class="l"><b>L3</b> <code>java.awt.Dimension</code>: una pareja ancho × alto. La usa <code>fijarTamano</code>.</p>
<p class="l"><b>L4</b> <code>java.awt.FontMetrics</code>: las «medidas» de una fuente: cuánto mide un texto de ancho,
cuánto sube y cuánto baja de la línea base. La usan <code>lineaBaseCentrada</code> y <code>recortar</code>.</p>
<p class="l"><b>L5</b> <code>java.awt.Graphics</code>: el «lápiz» básico que Swing entrega a cada componente en
<code>paintComponent(Graphics g)</code> (capítulo 37).</p>
<p class="l"><b>L6</b> <code>java.awt.Graphics2D</code>: la versión avanzada de ese lápiz: dibuja figuras de Java2D,
usa trazos, transparencias, degradados y suavizado. Todos los métodos de esta clase lo reciben.</p>
"""),
             ("import java.awt.Paint", r"""
<p class="l"><b>L7</b> <code>java.awt.Paint</code>: una <b>interfaz</b> que representa «cualquier cosa con la que se
puede pintar». Un <code>Color</code> es un <code>Paint</code> (pinta todo de un color), y un <code>GradientPaint</code>
también (pinta un degradado). Se usa para guardar y restaurar la pintura, y para el relleno del texto, que puede ser
un degradado.</p>
<p class="l"><b>L8</b> <code>java.awt.RenderingHints</code>: «sugerencias de dibujo», ajustes de calidad como el suavizado.
Las usa <code>preparar</code>.</p>
<p class="l"><b>L9</b> <code>java.awt.Shape</code>: interfaz que cumple <b>cualquier figura</b> geométrica: una línea, un
círculo, un rectángulo redondeado, un camino. Gracias a ella, <code>trazoNeon</code> sirve para todas: recibe un
<code>Shape</code> y no le importa cuál sea.</p>
<p class="l"><b>L10</b> <code>java.awt.Stroke</code>: interfaz de los trazos. <code>BasicStroke</code> la implementa.
<code>g.getStroke()</code> devuelve un <code>Stroke</code>, y por eso se importa para guardar el trazo previo.</p>
<p class="l"><b>L11</b> <code>java.awt.geom.Ellipse2D</code>: una elipse (o un círculo, si ancho y alto son iguales). Para
la ficha O.</p>
<p class="l"><b>L12</b> <code>java.awt.geom.Path2D</code>: un <b>camino</b>: una figura que se construye punto a punto,
como dibujar sin despegar el lápiz (o despegándolo). Para la X.</p>
<p class="l"><b>L13</b> <code>javax.swing.JComponent</code>: la clase madre de todos los componentes de Swing
(<code>JButton</code>, <code>JPanel</code>, <code>JLabel</code>…). La usa <code>fijarTamano</code> para aceptar cualquiera
de ellos. Fíjate en el paquete: <code>javax.swing</code>, no <code>java.awt</code>.</p>
"""),
             ("public final class Dibujo", r"""
<p class="l"><b>L15–L22</b> El comentario de la clase explica el truco en el que se basa toda la estética: trazar la
misma figura varias veces, «primero muy gruesa y casi transparente, y cada vez más fina y más opaca». Y aclara una
decisión: <b>no se usan imágenes</b>. Todo se dibuja con Java2D, la parte de Java que dibuja figuras. Ventajas: no hay
archivos que perder, todo se ve nítido a cualquier tamaño, y un cambio de color en <code>Tema</code> se aplica en todas
partes.</p>
<p class="l"><b>L23</b> Otra clase de utilidad, como <code>Tema</code>: <code>final</code> (nadie hereda de ella) y con
métodos <code>static</code>.</p>
<p class="l"><b>L25–L26</b> Constructor privado y vacío: nadie puede crear objetos <code>Dibujo</code>. Se usa siempre
como <code>Dibujo.algo(...)</code>.</p>
"""),
             ("public static Graphics2D preparar", r"""
<p class="l"><b>L28–L31</b> El comentario describe el contrato: devuelve una <b>copia</b> del <code>Graphics</code> con el
suavizado activado, y quien la pida <b>debe</b> llamar a <code>dispose()</code> al terminar.</p>
<p class="l"><b>L32</b> Recibe el <code>Graphics</code> que Swing pasa a <code>paintComponent</code> y devuelve un
<code>Graphics2D</code> listo para dibujar.</p>
<p class="l"><b>L33</b> Dos operaciones. <code>g.create()</code> crea una <b>copia</b> del lápiz con su mismo estado
(color, fuente, recorte, posición). Todo lo que cambies en la copia (suavizado, trazo, color, transformaciones) no afecta
al original. ¿Por qué importa? Porque Swing <b>reutiliza</b> el mismo <code>Graphics</code> para dibujar después los
bordes y los componentes hijos; si lo dejaras con un trazo de 16 píxeles o girado, los dibujaría mal. Luego,
<code>(Graphics2D)</code> es un <b>cast</b> (conversión de tipo, capítulo 12): <code>create()</code> declara que devuelve
un <code>Graphics</code>, pero en Swing ese objeto siempre es, en realidad, un <code>Graphics2D</code>. El cast le dice al
compilador «trátalo como lo que realmente es», para poder usar sus métodos avanzados.</p>
<p class="l"><b>L34</b> <code>setRenderingHint(llave, valor)</code> activa una sugerencia. <code>KEY_ANTIALIASING</code>
con <code>VALUE_ANTIALIAS_ON</code>: <b>suavizado</b> de figuras. Sin él, una línea diagonal o un círculo se ven con
«escalones», porque cada píxel está pintado o no. Con él, los píxeles del borde se pintan a medias, y el ojo ve una curva
suave. Para un neón es imprescindible: las capas transparentes con escalones parecen una sierra.</p>
<p class="l"><b>L35</b> <code>KEY_TEXT_ANTIALIASING</code>: lo mismo, pero para el texto. Es una llave aparte porque el
texto tiene su propio sistema de dibujo.</p>
"""),
             ("KEY_RENDERING", r"""
<p class="l"><b>L36</b> <code>KEY_RENDERING</code> con <code>VALUE_RENDER_QUALITY</code>: cuando Java tenga que elegir
entre rapidez y calidad (por ejemplo al mezclar colores transparentes), que elija calidad. Un juego de totito se redibuja
pocas veces por segundo; nos sobra tiempo.</p>
<p class="l"><b>L37</b> <code>KEY_STROKE_CONTROL</code> con <code>VALUE_STROKE_PURE</code>: dibuja los trazos con su
geometría <b>exacta</b>. Por defecto, Java «normaliza»: mueve las líneas hasta medio píxel para que caigan justo en la
cuadrícula de píxeles y se vean más nítidas. En un trazo suelto eso ayuda, pero en seis capas concéntricas cada una se
movería un poco distinto y el halo quedaría torcido, y los círculos se verían ligeramente achatados.</p>
<p class="l"><b>L38</b> <code>KEY_FRACTIONALMETRICS</code>: mide y coloca las letras con <b>decimales</b> en vez de
redondear cada una a píxeles enteros. Así el ancho que mide <code>stringWidth</code> coincide con lo que se dibuja, los
textos quedan bien centrados y el espaciado de <code>fuenteEspaciada</code> (capítulo 40) es regular.</p>
<p class="l"><b>L39</b> Devuelve la copia preparada. El patrón de uso, que verás en todos los componentes desde el
capítulo 43, es:</p>
<pre class="java">Graphics2D g2 = Dibujo.preparar(g);
// ... dibujar con g2 ...
g2.dispose();</pre>
<p class="l"><code>dispose()</code> libera los recursos de la copia (el sistema operativo reserva memoria para cada lápiz).
Olvidarlo una vez no rompe nada visible, pero hacerlo en un componente que se redibuja muchas veces va acumulando basura.</p>
"""),
             ("public static void fijarTamano", r"""
<p class="l"><b>L42–L45</b> Comentario: fija el tamaño preferido, el mínimo y el máximo iguales, para que los
<code>BoxLayout</code> de las pantallas no lo estiren.</p>
<p class="l"><b>L46</b> Recibe cualquier <code>JComponent</code> (un botón, un panel…) y el ancho y el alto en píxeles.
Es <code>void</code>: modifica el componente, no devuelve nada.</p>
<p class="l"><b>L47</b> Crea un solo objeto <code>Dimension</code> con las dos medidas y lo usa tres veces.</p>
<p class="l"><b>L48</b> <code>setPreferredSize</code>: el tamaño que el componente «quiere» tener. Casi todos los
<i>layouts</i> lo respetan si hay sitio.</p>
<p class="l"><b>L49</b> <code>setMinimumSize</code>: lo más pequeño que se le permite ser.</p>
<p class="l"><b>L50</b> <code>setMaximumSize</code>: lo más grande. Esta es la clave: <code>BoxLayout</code> (capítulo 37)
<b>estira</b> los componentes hasta su tamaño máximo para llenar el espacio, y el máximo de un <code>JPanel</code> por
defecto es enorme. Sin esta línea, un botón del menú diseñado de 360 píxeles se estiraría hasta todo el ancho de la
tarjeta. Con las tres medidas iguales, cada pieza conserva el tamaño del diseño (capítulo 36).</p>
"""),
             ("public static BasicStroke redondo", r"""
<p class="l"><b>L53</b> Comentario: trazo con puntas y esquinas redondeadas.</p>
<p class="l"><b>L54</b> Devuelve un <code>BasicStroke</code> del grosor pedido (en píxeles, con decimales).</p>
<p class="l"><b>L55</b> <code>new BasicStroke(grosor, terminación, unión)</code>. <code>CAP_ROUND</code>: cada punta de
la línea termina en un semicírculo (las otras opciones son <code>CAP_BUTT</code>, cortada en seco, y
<code>CAP_SQUARE</code>, con un cuadrado). <code>JOIN_ROUND</code>: donde dos segmentos se unen (la punta del chevron, las
esquinas de la puerta), la esquina se redondea (las otras son <code>JOIN_MITER</code>, en punta afilada, y
<code>JOIN_BEVEL</code>, achaflanada). Un tubo de neón real es redondo, así que sus puntas y codos también. Además, con
puntas redondeadas las capas gruesas del halo envuelven la punta de la línea como una cápsula, en lugar de terminar en un
corte recto.</p>
"""),
             ("public static void trazo(", r"""
<p class="l"><b>L58</b> Comentario: trazo simple, sin halo, para detalles pequeños o que no deben brillar (la flecha de
«Volver», los aros finos de selección).</p>
<p class="l"><b>L59</b> Recibe el lápiz, la figura (cualquier <code>Shape</code>), el color y el grosor.</p>
<p class="l"><b>L60</b> Elige el color.</p>
<p class="l"><b>L61</b> Elige el trazo redondo del grosor pedido.</p>
<p class="l"><b>L62</b> <code>g.draw(figura)</code> dibuja el <b>contorno</b> de la figura con el trazo actual.
(Su pareja, <code>g.fill(figura)</code>, rellenaría el interior.) Este método no restaura el trazo, porque se usa sobre
la copia de <code>preparar</code>, que se desecha al final.</p>
"""),
             ("public static void trazoNeon(", r"""
<p class="l"><b>L65</b> Primera versión de <code>trazoNeon</code>, con cuatro parámetros: lápiz, figura, color y grosor.</p>
<p class="l"><b>L66</b> Llama a la otra versión (L75) pasando <code>1f</code> como intensidad. Dos métodos con el mismo
nombre y distintos parámetros es la <b>sobrecarga</b> (capítulo 16). Así, quien quiere el brillo normal escribe
<code>trazoNeon(g2, forma, color, 1.8f)</code> sin pensar en la intensidad, y quien necesita ajustarla tiene la versión
larga. La versión corta no repite código: delega.</p>
"""),
             ("float grosor, float intensidad)", r"""
<p class="l"><b>L69–L74</b> Comentario con la etiqueta <code>@param</code> de Javadoc, que documenta un parámetro:
<code>intensidad</code> 1 es lo normal; menos de 1 se ve apagado (una opción no elegida); más de 1 brilla más (el ratón
encima). En el juego verás, por ejemplo, 1.5 en un botón con el ratón encima, 1.3 en el símbolo elegido de la
configuración y 0.4 en el que no está elegido.</p>
<p class="l"><b>L75</b> La versión completa, con los cinco parámetros.</p>
<p class="l"><b>L76</b> Guarda el trazo que tenía el lápiz antes de empezar. El tipo es la interfaz <code>Stroke</code>,
porque no sabemos (ni importa) qué clase concreta de trazo era.</p>
<p class="l"><b>L77</b> Guarda la pintura previa: puede ser un color o un degradado. Estas dos variables sirven para
<b>dejar el lápiz como estaba</b> al final (L100–L101). Quien llama a <code>trazoNeon</code> puede querer seguir dibujando
con su propio color y trazo, y no esperaría que un método «de ayuda» se los cambiara.</p>
"""),
             ("// Halo: de la capa", r"""
<p class="l"><b>L79</b> Comentario: el halo va de la capa más ancha y transparente a la más fina y opaca.</p>
<p class="l"><b>L80</b> <code>final int capas = 6;</code> una variable local que no cambia. Seis capas es un equilibrio:
con menos, se notan los «escalones» entre bandas; con más, cuesta más dibujar y casi no se nota la diferencia.</p>
<p class="l"><b>L81</b> Un <code>for</code> que cuenta <b>hacia atrás</b>: <code>i</code> empieza en 6 y baja hasta 1
(<code>i--</code> resta uno en cada vuelta). Hacia atrás para pintar primero la capa más ancha y terminar con la más fina, como se
construye la luz, de afuera hacia adentro. (Con capas del mismo color el orden casi no cambia el resultado, como
descubrirás en los ejercicios; pero así el código se lee en el mismo orden en que se dibuja, y si un día las capas
tuvieran colores distintos, la más fina y brillante quedaría encima.)</p>
<p class="l"><b>L82</b> El alfa de esta capa. Llamemos <code>k = capas − i</code>: vale 0 en la primera vuelta (i = 6) y 5
en la última (i = 1). La fórmula es <b>alfa = (6 + 5k) × intensidad</b>: 6, 11, 16, 21, 26, 31. Cada capa más fina es 5
puntos más opaca. (El 6 de la fórmula es el alfa de partida; que coincida con el número de capas es casualidad.)
<code>Math.round</code> redondea el resultado al entero, porque el alfa de un <code>Color</code> es un <code>int</code>.
Con intensidad 0.4 las alfas quedan en 2, 4, 6, 8, 10, 12; con 1.3, en 8, 14, 21, 27, 34, 40.</p>
<p class="l"><b>L83</b> Pone el color de la capa: el mismo color con ese alfa, gracias a <code>Tema.conAlfa</code>, que
además impide salirse de 0–255.</p>
<p class="l"><b>L84</b> El grosor de la capa: <b>grosor + i × 2.4</b>. Con un trazo de 2 px: 16.4, 14.0, 11.6, 9.2, 6.8 y
4.4. Cada capa es 2.4 px más ancha que la siguiente, es decir, sobresale 1.2 px más por cada lado. La más ancha se
extiende 7.2 px a cada lado de la línea. La <code>f</code> de <code>2.4f</code> indica un <code>float</code>.</p>
<p class="l"><b>L85</b> Traza la figura con ese color y ese grosor. Al terminar el bucle, se han dibujado seis capas
superpuestas.</p>
"""),
             ("// Linea principal.", r"""
<p class="l"><b>L88</b> Comentario: ahora la línea nítida.</p>
<p class="l"><b>L89</b> El color de la línea principal, con un alfa calculado así: <code>0.4 + 0.6 × intensidad</code>,
limitado a un máximo de 1 con <code>Math.min(1f, ...)</code>, y multiplicado por 255. Con intensidad 1: 0.4 + 0.6 = 1 →
alfa 255, totalmente opaca. Con 0.4: 0.4 + 0.24 = 0.64 → 163, algo apagada. Con 1.3: 1.18, que se limita a 1 → 255 (no
se puede ser más que opaco; el «brillo extra» de una intensidad alta lo pone el halo). El 0.4 fijo asegura que una línea
nunca desaparezca del todo aunque la intensidad sea muy baja.</p>
<p class="l"><b>L90</b> El grosor exacto que se pidió.</p>
<p class="l"><b>L91</b> Dibuja la línea encima de todo el halo.</p>
"""),
             ("// En trazos gruesos", r"""
<p class="l"><b>L93</b> Comentario: en trazos gruesos (las fichas), el centro del tubo es casi blanco, como en un neón
real, donde el gas brilla tanto que el color se «quema» hacia el blanco.</p>
<p class="l"><b>L94</b> Solo si el grosor es de 5 px o más. En un borde de 2 px, un núcleo de 0.7 px no se vería y solo
ensuciaría el color.</p>
<p class="l"><b>L95</b> El color del núcleo: el color mezclado con un 60 % de blanco (<code>Tema.aclarar</code>) y con
alfa 200 (algo transparente, para que no sea un blanco plano). Para el rosa: (255, 177, 238).</p>
<p class="l"><b>L96</b> Un trazo del 35 % del grosor: con las fichas del tablero, de 7 px, el núcleo mide unos 2.5 px.</p>
<p class="l"><b>L97</b> Dibuja el núcleo, encima de la línea principal.</p>
<p class="l"><b>L100–L101</b> Restaura el trazo y la pintura que había antes (L76–L77). <code>setPaint</code> restaura
tanto un color como un degradado, porque un <code>Color</code> también es un <code>Paint</code>.</p>
"""),
             ("public static void dibujarX", r"""
<p class="l"><b>L104</b> Comentario: una X de neón centrada en <code>(cx, cy)</code>.</p>
<p class="l"><b>L105</b> Recibe el centro, el tamaño (lado del cuadrado que ocupa la X), el color y el grosor. Las
coordenadas son <code>double</code> (decimales con más precisión que <code>float</code>), lo habitual en Java2D.</p>
<p class="l"><b>L106</b> <code>r</code>: la mitad del tamaño, la distancia del centro a cada esquina en horizontal y en
vertical.</p>
<p class="l"><b>L107</b> Crea un camino vacío. <code>Path2D.Double</code> es la variante de <code>Path2D</code> que guarda
coordenadas <code>double</code>; el punto indica que <code>Double</code> es una clase anidada dentro de
<code>Path2D</code>.</p>
<p class="l"><b>L108</b> <code>moveTo</code>: «levanta el lápiz y ponlo en» la esquina superior izquierda. Recuerda que
en la pantalla la y crece hacia <b>abajo</b> (capítulo 37): <code>cy − r</code> es arriba.</p>
<p class="l"><b>L109</b> <code>lineTo</code>: «arrastra el lápiz hasta» la esquina inferior derecha. Primera diagonal.</p>
<p class="l"><b>L110</b> Vuelve a levantar el lápiz y lo lleva a la esquina superior derecha.</p>
<p class="l"><b>L111</b> Segunda diagonal, hasta la esquina inferior izquierda. Un solo camino con dos trazos separados.</p>
<p class="l"><b>L112</b> Lo traza con efecto neón. Como es un único <code>Shape</code>, las seis capas del halo se dibujan
para las dos diagonales a la vez, y en el cruce central el brillo se acumula de forma natural.</p>
"""),
             ("public static void dibujarO", r"""
<p class="l"><b>L115</b> Comentario: una O de neón centrada en <code>(cx, cy)</code>.</p>
<p class="l"><b>L116–L117</b> <code>new Ellipse2D.Double(x, y, ancho, alto)</code> describe una elipse por el
rectángulo que la contiene: <code>(x, y)</code> es la esquina superior izquierda de ese rectángulo, no el centro. Por eso
se le resta la mitad del tamaño a <code>cx</code> y a <code>cy</code>. Con ancho igual a alto, es un círculo. Se pasa
directamente a <code>trazoNeon</code>, sin guardarla en una variable.</p>
"""),
             ("public static void dibujarFicha", r"""
<p class="l"><b>L120–L123</b> Comentario: dibuja la ficha con su color del tema, y la X algo más pequeña «para que a la
vista ocupe lo mismo que la O».</p>
<p class="l"><b>L124</b> Recibe la ficha como <code>char</code>, el centro, el tamaño y el grosor. Es el método que usan
el tablero (capítulo 48), el marcador (52), el selector de símbolo (50) y la pantalla de resultado (54).</p>
<p class="l"><b>L125–L126</b> Si es <code>'X'</code>, la dibuja rosa (<code>Tema.ROSA</code>) al 84 % del tamaño. ¿Por
qué? Por <b>compensación óptica</b>, un truco clásico de diseño: las diagonales de una X llegan hasta las esquinas del
cuadrado, mientras que un círculo deja esas esquinas vacías. Con el mismo tamaño, la X «se ve» más grande y pesada que la
O. Reducirla un 16 % las equilibra a la vista.</p>
<p class="l"><b>L127–L128</b> Si es <code>'O'</code>, un círculo azul del tamaño completo. Es <code>else if</code> y no
<code>else</code>: si llega cualquier otro carácter (por ejemplo, una casilla vacía <code>' '</code>), no se dibuja nada.
Así el tablero puede llamar a este método para las nueve casillas sin preguntar antes.</p>
"""),
             ("public static void textoNeon", r"""
<p class="l"><b>L132–L135</b> Comentario: texto con un halo de color alrededor. <code>(x, y)</code> es la <b>línea
base</b> del texto, igual que en <code>drawString</code> (lo verás en <code>lineaBaseCentrada</code>).</p>
<p class="l"><b>L136</b> Recibe el texto, la posición, el color del halo y el <b>relleno</b> de las letras, que es un
<code>Paint</code>: puede ser un color plano (el blanco del texto) o un degradado (el rosa → cian del título «TOTITO» en
el encabezado, capítulo 45).</p>
<p class="l"><b>L137</b> Guarda la pintura previa para restaurarla al final.</p>
<p class="l"><b>L138</b> El texto no es una línea, así que no se le puede aplicar <code>trazoNeon</code> directamente. El
truco aquí es otro: escribir el mismo texto varias veces, <b>desplazado</b> un poco en todas direcciones. Este bucle
recorre cuatro distancias, de 4 px a 1 px, de afuera hacia adentro.</p>
<p class="l"><b>L139</b> El alfa de cada distancia: <code>4 + (4 − radio) × 3</code>, es decir 4, 7, 10 y 13. Muy
transparente, porque se va a escribir ocho veces en cada distancia y las copias se suman.</p>
<p class="l"><b>L140</b> Un bucle interior para las <b>ocho direcciones</b>: 0°, 45°, 90°… 315°
(<code>angulo += 45</code> suma 45 en cada vuelta).</p>
<p class="l"><b>L141</b> <code>Math.toRadians</code> convierte grados a radianes, porque <code>Math.cos</code> y
<code>Math.sin</code> trabajan en radianes (360° = 2π radianes).</p>
<p class="l"><b>L142</b> Escribe el texto desplazado: <code>cos(ángulo) × radio</code> en horizontal y <code>sin(ángulo) ×
radio</code> en vertical. Con 0° el desplazamiento es (radio, 0), a la derecha; con 90°, (0, radio), hacia abajo; con
45°, unos (0.7 × radio, 0.7 × radio), en diagonal. <code>(float)</code> convierte el <code>double</code> que devuelven
<code>cos</code> y <code>sin</code> al <code>float</code> que pide <code>drawString</code>. En total son 4 × 8 = 32 copias
tenues alrededor del texto.</p>
"""),
             ("g.setPaint(relleno);", r"""
<svg viewBox="0 0 240 240" width="40%">
<rect x="0" y="0" width="240" height="240" rx="12" fill="#1C1740"/>
<g fill="none" stroke="#A05CFF" stroke-width="1" stroke-dasharray="3 3">
<circle cx="120" cy="120" r="24"/><circle cx="120" cy="120" r="48"/><circle cx="120" cy="120" r="72"/><circle cx="120" cy="120" r="96"/>
</g>
<g fill="#FF3BD4" fill-opacity="0.25">
<circle cx="216.0" cy="120.0" r="6"/><circle cx="187.9" cy="187.9" r="6"/><circle cx="120.0" cy="216.0" r="6"/><circle cx="52.1" cy="187.9" r="6"/>
<circle cx="24.0" cy="120.0" r="6"/><circle cx="52.1" cy="52.1" r="6"/><circle cx="120.0" cy="24.0" r="6"/><circle cx="187.9" cy="52.1" r="6"/>
</g>
<g fill="#FF3BD4" fill-opacity="0.45">
<circle cx="192.0" cy="120.0" r="6"/><circle cx="170.9" cy="170.9" r="6"/><circle cx="120.0" cy="192.0" r="6"/><circle cx="69.1" cy="170.9" r="6"/>
<circle cx="48.0" cy="120.0" r="6"/><circle cx="69.1" cy="69.1" r="6"/><circle cx="120.0" cy="48.0" r="6"/><circle cx="170.9" cy="69.1" r="6"/>
</g>
<g fill="#FF3BD4" fill-opacity="0.65">
<circle cx="168.0" cy="120.0" r="6"/><circle cx="153.9" cy="153.9" r="6"/><circle cx="120.0" cy="168.0" r="6"/><circle cx="86.1" cy="153.9" r="6"/>
<circle cx="72.0" cy="120.0" r="6"/><circle cx="86.1" cy="86.1" r="6"/><circle cx="120.0" cy="72.0" r="6"/><circle cx="153.9" cy="86.1" r="6"/>
</g>
<g fill="#FF3BD4" fill-opacity="0.85">
<circle cx="144.0" cy="120.0" r="6"/><circle cx="137.0" cy="137.0" r="6"/><circle cx="120.0" cy="144.0" r="6"/><circle cx="103.0" cy="137.0" r="6"/>
<circle cx="96.0" cy="120.0" r="6"/><circle cx="103.0" cy="103.0" r="6"/><circle cx="120.0" cy="96.0" r="6"/><circle cx="137.0" cy="103.0" r="6"/>
</g>
<circle cx="120" cy="120" r="7" fill="#FFFFFF"/>
</svg>
<p>Las 32 posiciones donde se escribe la copia tenue del texto (los puntos rosa, con la opacidad exagerada para que se
vean), a 1, 2, 3 y 4 píxeles en ocho direcciones, y en el centro, en blanco, la posición del texto real.</p>
<p class="l"><b>L145</b> Pone el relleno de las letras: un color o un degradado.</p>
<p class="l"><b>L146</b> Escribe el texto real, en la posición exacta, encima del halo.</p>
<p class="l"><b>L147</b> Restaura la pintura que había.</p>
"""),
             ("public static float lineaBaseCentrada", r"""
<p class="l"><b>L150</b> Comentario: calcula la línea base para que el texto quede centrado en vertical sobre
<code>yCentro</code>.</p>
<p class="l"><b>L151</b> Recibe las medidas de la fuente (<code>FontMetrics</code>, que se obtiene con
<code>g2.getFontMetrics()</code> después de elegir la fuente) y la altura donde quieres el centro del texto.</p>
<p class="l"><b>L152</b> La fórmula. <code>drawString(texto, x, y)</code> no coloca el texto por su centro ni por su
borde superior, sino por su <b>línea base</b>: la línea imaginaria sobre la que «se apoyan» las letras (la g, la p y la
y bajan de ella). <code>getAscent()</code> es cuánto suben las letras sobre la base; <code>getDescent()</code>, cuánto bajan
por debajo. El centro visual del texto está a <code>(ascent − descent) / 2</code> por encima de la base. Despejando: base =
yCentro + (ascent − descent) / 2. El <code>2f</code> obliga a dividir con decimales (con un <code>2</code> entero, 7 / 2
daría 3 y no 3.5).</p>
<pre class="texto"> y = 38  - - - - - - - - - - - - -  tope de las letras  (base − ascent = 57 − 19)
          T O T I T O   g p y
 y = 50  · · · · · · · · · · · · ·  yCentro: el centro visual del texto
 y = 57  ─────────────────────────  línea base: ahí se apoyan las letras
 y = 62  - - - - - - - - - - - - -  fondo de la g, la p, la y  (base + descent = 57 + 5)</pre>
<p class="l">Ejemplo con la fuente de nuestra prueba (negrita, 20 puntos): ascent 19, descent 5. Para centrar en
<code>yCentro = 50</code>: 50 + (19 − 5) / 2 = <b>57</b>. Si escribieras <code>drawString(texto, x, 50)</code>, el texto
quedaría 7 píxeles más arriba de lo que esperas. Este método lo usan casi todos los componentes con texto: botones,
rótulos, campo de texto, pasos de instrucciones.</p>
"""),
             ("public static String recortar", r"""
<p class="l"><b>L155</b> Comentario: recorta el texto con «…» si no cabe.</p>
<p class="l"><b>L156</b> Recibe las medidas de la fuente, el texto y el ancho máximo en píxeles. Devuelve el texto,
recortado o no. Lo usa el marcador (capítulo 52) para los nombres de los jugadores: alguien podría llamarse
«Bartolomeo Hernández».</p>
<p class="l"><b>L157–L159</b> Primero, el caso fácil: <code>fm.stringWidth(texto)</code> mide cuántos píxeles ocupa el
texto con esa fuente. Si cabe, se devuelve tal cual y el método termina.</p>
<p class="l"><b>L160</b> Una copia de trabajo que se irá acortando.</p>
<p class="l"><b>L161</b> Un <code>while</code> (capítulo 14) que sigue mientras <b>dos</b> condiciones se cumplan: que
quede más de una letra (<code>length() &gt; 1</code>; así nunca se queda vacío ni entra en un bucle sin fin) y que el
texto <b>con</b> los puntos suspensivos todavía no quepa. Se mide con el «…» incluido, porque es lo que finalmente se va a
dibujar.</p>
<p class="l"><b>L162</b> Quita la última letra: <code>substring(0, length() − 1)</code> devuelve desde la posición 0 hasta
la penúltima (el segundo número es «hasta, sin incluir»).</p>
<p class="l"><b>L164</b> Devuelve el texto recortado con el «…» al final. Un solo carácter «…» es más estrecho y más
correcto tipográficamente que tres puntos «...».</p>
<p class="l"><b>L165–L166</b> Cierran el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>El neón, número por número</h3>
<p>Sigamos <code>Dibujo.trazoNeon(g2, linea, Tema.ROSA, 2f)</code>, el borde típico de un botón. Primero, las siete
pasadas de <code>draw</code>:</p>
<table class="tabla">
<tr><th>Pasada</th><th>i</th><th>k = 6 − i</th><th>Alfa = 6 + 5k</th><th>Opacidad</th><th>Grosor = 2 + 2.4·i</th><th>Sobresale por lado</th></tr>
<tr><td>1</td><td>6</td><td>0</td><td>6</td><td>2.4 %</td><td>16.4 px</td><td>7.2 px</td></tr>
<tr><td>2</td><td>5</td><td>1</td><td>11</td><td>4.3 %</td><td>14.0 px</td><td>6.0 px</td></tr>
<tr><td>3</td><td>4</td><td>2</td><td>16</td><td>6.3 %</td><td>11.6 px</td><td>4.8 px</td></tr>
<tr><td>4</td><td>3</td><td>3</td><td>21</td><td>8.2 %</td><td>9.2 px</td><td>3.6 px</td></tr>
<tr><td>5</td><td>2</td><td>4</td><td>26</td><td>10.2 %</td><td>6.8 px</td><td>2.4 px</td></tr>
<tr><td>6</td><td>1</td><td>5</td><td>31</td><td>12.2 %</td><td>4.4 px</td><td>1.2 px</td></tr>
<tr><td>7 (principal)</td><td>—</td><td>—</td><td>255</td><td>100 %</td><td>2.0 px</td><td>0</td></tr>
</table>
<p>(No hay núcleo blanco porque el grosor, 2, es menor que 5.) Ahora, ¿qué opacidad <b>total</b> tiene cada punto según su
distancia al centro de la línea? Cuando se pinta un color con opacidad <i>a</i> encima de otro, deja pasar
<i>(1 − a)</i> de lo que había debajo; por eso las capas no se suman, se combinan: opacidad total = 1 − (1 − a₁)(1 − a₂)…</p>
<table class="tabla">
<tr><th>Distancia al centro</th><th>Capas que la cubren</th><th>Opacidad total del rosa</th></tr>
<tr><td>0 a 1 px</td><td>la línea principal</td><td>100 %</td></tr>
<tr><td>1 a 2.2 px</td><td>las seis</td><td>36.6 %</td></tr>
<tr><td>2.2 a 3.4 px</td><td>capas 2 a 6</td><td>27.8 %</td></tr>
<tr><td>3.4 a 4.6 px</td><td>capas 3 a 6</td><td>19.6 %</td></tr>
<tr><td>4.6 a 5.8 px</td><td>capas 4 a 6</td><td>12.4 %</td></tr>
<tr><td>5.8 a 7.0 px</td><td>capas 5 y 6</td><td>6.6 %</td></tr>
<tr><td>7.0 a 8.2 px</td><td>solo la 6</td><td>2.4 %</td></tr>
</table>
<p>Ahí está la «luz»: una caída suave, de 37 % a 2 % en unos 7 píxeles. Cada capa individual es casi invisible; juntas
forman un degradado. Si la intensidad es 0.4, todas las alfas bajan (2, 4, 6, 8, 10, 12 y una línea principal de 163) y el
mismo trazo se ve apagado: así se distingue una opción no elegida. Con 1.3 suben (8, 14, 21, 27, 34, 40) y brilla más.</p>

<h3>Recortar un nombre, vuelta por vuelta</h3>
<p>Con la fuente de nuestra prueba (negrita, 20 puntos) y un ancho máximo de 80 px, <code>recortar(fm, "Bartolomeo",
80)</code>:</p>
<table class="tabla">
<tr><th>Vuelta</th><th>Texto medido</th><th>Ancho</th><th>¿Sigue?</th></tr>
<tr><td>—</td><td>Bartolomeo</td><td>111</td><td>No cabe: entra al bucle</td></tr>
<tr><td>1</td><td>Bartolomeo…</td><td>131</td><td>Sí: quita la «o»</td></tr>
<tr><td>2</td><td>Bartolome…</td><td>119</td><td>Sí: quita la «e»</td></tr>
<tr><td>3</td><td>Bartolom…</td><td>108</td><td>Sí: quita la «m»</td></tr>
<tr><td>4</td><td>Bartolo…</td><td>90</td><td>Sí: quita la «o»</td></tr>
<tr><td>5</td><td>Bartol…</td><td>78</td><td>No: 78 ≤ 80. Devuelve <code>"Bartol…"</code></td></tr>
</table>
<p>En tu Windows, con Segoe UI, los anchos serán algo distintos, pero el proceso es el mismo.</p>

<h2>Compila y prueba</h2>
<p>La comprobación oficial sigue siendo que compile: <i>Run → Clean and Build Project</i> (Shift+F11) y
<code>BUILD SUCCESS</code>, o:</p>
<pre class="ps">javac -encoding UTF-8 -d out src\*.java</pre>

<h3>Prueba opcional: ver el neón en una imagen</h3>
<p>Las pantallas reales llegan en el capítulo 56, pero si no aguantas la curiosidad puedes pedirle a <code>Dibujo</code>
que pinte en una <b>imagen en memoria</b> (un <code>BufferedImage</code>) y guardarla como PNG. Crea en la raíz del
proyecto (no en <code>src</code>) el archivo temporal <code>PruebaNeon.java</code>:</p>
<pre class="ps">New-Item PruebaNeon.java</pre>
<pre class="java">import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.geom.Line2D;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;

public class PruebaNeon {
    public static void main(String[] args) throws Exception {
        BufferedImage imagen = new BufferedImage(520, 300, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = Dibujo.preparar(imagen.getGraphics());
        g2.setColor(Tema.FONDO_ARRIBA);
        g2.fillRect(0, 0, 520, 300);

        Dibujo.trazo(g2, new Line2D.Double(30, 40, 230, 40), Tema.ROSA, 2f);           // sin halo
        Dibujo.trazoNeon(g2, new Line2D.Double(290, 40, 490, 40), Tema.ROSA, 2f);      // con halo
        Dibujo.trazoNeon(g2, new Line2D.Double(30, 100, 150, 100), Tema.AZUL, 3f, 0.4f);  // apagado
        Dibujo.trazoNeon(g2, new Line2D.Double(200, 100, 320, 100), Tema.AZUL, 3f, 1f);   // normal
        Dibujo.trazoNeon(g2, new Line2D.Double(370, 100, 490, 100), Tema.AZUL, 3f, 1.3f); // encendido

        Dibujo.dibujarFicha(g2, 'X', 110, 190, 80, 7f);
        Dibujo.dibujarFicha(g2, 'O', 230, 190, 80, 7f);

        g2.setFont(Tema.fuente(Font.BOLD, 34f));
        Dibujo.textoNeon(g2, "TOTITO", 300, Dibujo.lineaBaseCentrada(g2.getFontMetrics(), 190f),
                Tema.ROSA, Tema.TEXTO);
        g2.dispose();

        ImageIO.write(imagen, "png", new File("neon.png"));
        System.out.println("Listo: abre neon.png");
    }
}</pre>
<p>Lo nuevo aquí: <code>BufferedImage</code> es una imagen guardada en memoria (520 × 300 píxeles, con transparencia:
<code>TYPE_INT_ARGB</code>); su <code>getGraphics()</code> da un lápiz que pinta en ella en vez de en la pantalla.
<code>ImageIO.write</code> la guarda como archivo PNG. <code>throws Exception</code> avisa de que guardar un archivo puede
fallar (capítulo 26). Después de un <i>Clean and Build</i>:</p>
<pre class="ps">java -cp target\classes PruebaNeon.java
Invoke-Item neon.png</pre>
<p><code>Invoke-Item</code> abre el archivo con el programa predeterminado de Windows (el visor de fotos). Verás, arriba,
la misma línea rosa sin halo y con halo; en el medio, tres líneas azules con intensidad 0.4, 1 y 1.3; abajo, una X y una
O de neón con su centro claro y el título con su resplandor. Compara las dos líneas de arriba: es la diferencia entre
«una línea de color» y «un tubo encendido». Al terminar, borra los dos archivos temporales:</p>
<pre class="ps">Remove-Item PruebaNeon.java, neon.png</pre>

<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Mensaje o síntoma</th><th>Causa y solución</th></tr>
<tr><td><code>cannot find symbol: variable Tema</code></td><td>Falta <code>Tema.java</code> (capítulo 40) o tiene otro nombre.</td></tr>
<tr><td><code>unmappable character for encoding</code>, o aparece <code>â€¦</code> en lugar de «…»</td><td>El archivo no está en UTF-8 o compilaste sin <code>-encoding UTF-8</code>. En NetBeans: clic derecho en el proyecto → <i>Properties → Sources → Encoding: UTF-8</i>.</td></tr>
<tr><td><code>incompatible types: possible lossy conversion from double to float</code></td><td>Falta la <code>f</code> de <code>2.4f</code> en la línea 84 (o en otro número con decimales). Java no convierte solo de <code>double</code> a <code>float</code>, porque podría perder precisión.</td></tr>
<tr><td><code>no suitable method found for drawString(String,double,float)</code></td><td>Falta un <code>(float)</code> en la línea 142: <code>drawString</code> acepta posiciones <code>int</code> o <code>float</code>, pero no <code>double</code>.</td></tr>
<tr><td><code>cannot find symbol: class Path2D</code></td><td>Falta el <code>import java.awt.geom.Path2D;</code> (ojo: <code>geom</code>).</td></tr>
</table>

<div class="caja git"><b>Git</b> Comprueba con <code>git status</code> que no se cuelan <code>PruebaNeon.java</code> ni
<code>neon.png</code>.
<pre class="ps">git status
git add src\Dibujo.java
git commit -m "Dibujo: efecto neon"
git push</pre>
El mensaje va sin tilde a propósito, como los comentarios del código, para evitar problemas de codificación en algunas
terminales.</div>

<h2>Resumen</h2>
<ul>
<li><code>preparar</code> crea una copia del <code>Graphics</code> con suavizado y calidad; quien la pide la libera con <code>dispose()</code>.</li>
<li><code>fijarTamano</code> iguala tamaño preferido, mínimo y máximo para que <code>BoxLayout</code> no estire.</li>
<li>El neón son seis capas del mismo trazo: alfa 6 + 5k (por la intensidad) y grosor + 2.4 px por capa, más la línea nítida y, en trazos gruesos, un núcleo casi blanco.</li>
<li>Un buen método «de ayuda» deja el lápiz como lo encontró (guarda y restaura trazo y pintura).</li>
<li>Las fichas: X con <code>Path2D</code> (al 84 % por compensación óptica) y O con <code>Ellipse2D</code>; X rosa, O azul.</li>
<li>El texto neón son 32 copias tenues desplazadas en 8 direcciones y 4 distancias, más el texto real.</li>
<li><code>drawString</code> usa la línea base; <code>lineaBaseCentrada</code> la calcula con ascent y descent. <code>recortar</code> acorta con «…».</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Sombras y resplandores en cualquier interfaz:</b> la técnica de capas transparentes cada vez más anchas sirve para una sombra suave bajo una tarjeta (en negro y desplazada hacia abajo) o para resaltar el campo de un formulario que tiene un error (en rojo).</li>
<li><b>Gráficas de datos:</b> una línea de ventas con un leve halo se lee mejor sobre un fondo oscuro; <code>Path2D</code> con <code>moveTo</code>/<code>lineTo</code> es justo lo que necesitas para unir los puntos.</li>
<li><b>Listas y tablas con nombres largos:</b> <code>recortar</code> funciona igual para el nombre de un producto en un inventario o un archivo en un explorador.</li>
<li><b>Centrar texto en cualquier botón o insignia propia:</b> la fórmula de la línea base es la misma en Android, en la web (canvas) o en un PDF.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Calcula a mano las seis alfas y los seis grosores de <code>trazoNeon(g, figura, color, 5f, 1.5f)</code>. ¿Se dibuja el
núcleo blanco? ¿De qué grosor? Pista: las alfas con 1.5 son 9, 17, 24, 32, 39, 47.</li>
<li>En <code>PruebaNeon.java</code>, dibuja un círculo grande con <code>trazoNeon</code> en <code>Tema.MORADO</code> y grosor 3,
y otro igual con <code>trazo</code>. Compara.</li>
<li>Cambia en tu prueba (no en <code>Dibujo</code>) la fuente a 50 puntos y dibuja una línea horizontal fina en
<code>yCentro</code> antes de escribir el texto con <code>lineaBaseCentrada</code>. ¿La línea pasa por el centro de las
mayúsculas?</li>
<li>¿Qué pasaría si en L81 el bucle fuera hacia arriba (<code>for (int i = 1; i &lt;= capas; i++)</code>)? ¿Cambiaría el dibujo?
Pista: al pintar varias veces el mismo color, la opacidad total es 1 − (1 − a₁)(1 − a₂)…, y una multiplicación no depende
del orden. Explica entonces por qué igual conviene escribirlo de la capa más ancha a la más fina.</li>
<li>Reto: escribe en tu prueba un método <code>sombra(Graphics2D g, Shape figura)</code> que use la misma idea del halo, en
negro, con la figura desplazada 4 píxeles hacia abajo. Pista: <code>AffineTransform.getTranslateInstance(0, 4).createTransformedShape(figura)</code>, con
<code>import java.awt.geom.AffineTransform;</code> arriba (las transformaciones las viste en el capítulo 37).</li>
</ol></div>
""",
}
