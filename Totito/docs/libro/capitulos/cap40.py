# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 40,
    "titulo": "Tema.java: la paleta de colores y las fuentes",
    "antes": r"""
<p class="entrada">Todos los colores neón del Totito y todas sus fuentes salen de un solo archivo. En este capítulo
traduces a código la teoría del color del capítulo 35 y la tipografía del 36: trece colores con nombre, una lista de
fuentes de respaldo y cinco pequeñas herramientas para trabajar con colores.</p>

<h2>Por qué existe este archivo</h2>
<p>Vuelve a mirar <code>JuegoMain</code> (capítulo 33): sus colores eran constantes privadas dentro de la propia ventana
(<code>COLOR_FONDO</code>, <code>COLOR_X</code>…). Con una sola clase visual, eso funcionaba. La v1.0 tendrá unas veinte
clases que dibujan: botones, tarjetas, rótulos, el tablero, el marcador, cinco pantallas… Si cada una escribiera su propio
<code>new Color(0xFF, 0x3B, 0xD4)</code>, tarde o temprano alguien teclearía <code>0x3C</code> en vez de
<code>0x3B</code> y habría dos rosas casi iguales que el ojo nota como «algo raro» sin saber qué. Y cambiar el rosa por
otro obligaría a buscarlo en veinte archivos.</p>
<p><code>Tema</code> es la <b>única fuente de verdad</b> del aspecto del juego. Funciona como la carta de colores de una
marca o el muestrario de una tienda de pintura: todos pintan con los mismos frascos, y si mañana cambias un frasco, cambia
en todas partes. El comentario de la clase lo dice así: «para cambiar el aspecto del juego basta con tocar esta clase».</p>

<h2>La paleta completa</h2>
<p>En el capítulo 35 viste de dónde salen estos colores: el fondo es un morado casi negro (modo oscuro), los acentos son
colores saturados y luminosos (el neón), y la transparencia (alfa) crea las superficies «de cristal». Esta es la paleta
tal como queda en el código:</p>
<svg viewBox="0 0 720 250" width="100%">
<rect x="0" y="0" width="720" height="250" rx="12" fill="#0E0B24"/>
<g stroke="#C8BCF6" stroke-width="1">
<rect x="20" y="20" width="80" height="56" rx="10" fill="#1C1740"/>
<rect x="120" y="20" width="80" height="56" rx="10" fill="#0E0B24"/>
<rect x="220" y="20" width="80" height="56" rx="10" fill="#5B35C2" fill-opacity="0.27"/>
<rect x="320" y="20" width="80" height="56" rx="10" fill="#FF3BD4"/>
<rect x="420" y="20" width="80" height="56" rx="10" fill="#FF3D82"/>
<rect x="520" y="20" width="80" height="56" rx="10" fill="#2F84FF"/>
<rect x="620" y="20" width="80" height="56" rx="10" fill="#40C8FF"/>
<rect x="20" y="135" width="80" height="56" rx="10" fill="#A05CFF"/>
<rect x="120" y="135" width="80" height="56" rx="10" fill="#C8BCF6"/>
<rect x="220" y="135" width="80" height="56" rx="10" fill="#FFFFFF"/>
<rect x="320" y="135" width="80" height="56" rx="10" fill="#A89BE2"/>
<rect x="420" y="135" width="80" height="56" rx="10" fill="#2B2363" fill-opacity="0.49"/>
<rect x="520" y="135" width="80" height="56" rx="10" fill="#2E285A" fill-opacity="0.67"/>
</g>
<g fill="#FFFFFF" font-size="11" text-anchor="middle" font-family="sans-serif">
<text x="60" y="92">FONDO_ARRIBA</text><text x="160" y="92">FONDO_ABAJO</text><text x="260" y="92">DECORACION</text>
<text x="360" y="92">ROSA</text><text x="460" y="92">FRESA</text><text x="560" y="92">AZUL</text><text x="660" y="92">CIAN</text>
<text x="60" y="207">MORADO</text><text x="160" y="207">LAVANDA</text><text x="260" y="207">TEXTO</text>
<text x="360" y="207">TEXTO_SUAVE</text><text x="460" y="207">SUPERFICIE</text><text x="560" y="207">CASILLA</text>
</g>
<g fill="#C8BCF6" font-size="10" text-anchor="middle" font-family="monospace">
<text x="60" y="106">#1C1740</text><text x="160" y="106">#0E0B24</text><text x="260" y="106">#5B35C2 · 70</text>
<text x="360" y="106">#FF3BD4</text><text x="460" y="106">#FF3D82</text><text x="560" y="106">#2F84FF</text><text x="660" y="106">#40C8FF</text>
<text x="60" y="221">#A05CFF</text><text x="160" y="221">#C8BCF6</text><text x="260" y="221">#FFFFFF</text>
<text x="360" y="221">#A89BE2</text><text x="460" y="221">#2B2363 · 125</text><text x="560" y="221">#2E285A · 170</text>
</g>
</svg>
<table class="tabla">
<tr><th>Constante</th><th>Hex · alfa</th><th>Papel en el diseño</th><th>Dónde se usa (capítulo)</th></tr>
<tr><td><code>FONDO_ARRIBA</code> / <code>FONDO_ABAJO</code></td><td>#1C1740 / #0E0B24</td><td>Degradado vertical del fondo de todas las pantallas.</td><td><code>PantallaBase</code> (55)</td></tr>
<tr><td><code>DECORACION</code></td><td>#5B35C2 · 70 (27 %)</td><td>Las X y O gigantes y desvaídas del fondo.</td><td><code>PantallaBase</code> (55)</td></tr>
<tr><td><code>ROSA</code></td><td>#FF3BD4</td><td><b>La X</b>; botón Jugar; X de cerrar.</td><td>Fichas (41), menú (56), encabezado (45)</td></tr>
<tr><td><code>FRESA</code></td><td>#FF3D82</td><td>Tarjeta del Jugador 1 (un rosa más rojizo, como en el diseño).</td><td>Configuración (58)</td></tr>
<tr><td><code>AZUL</code></td><td>#2F84FF</td><td><b>La O</b>; botón Instrucciones.</td><td>Fichas (41), menú (56)</td></tr>
<tr><td><code>CIAN</code></td><td>#40C8FF</td><td>Trofeo y título de victoria; degradado del título.</td><td>Resultado (54, 60), encabezado (45)</td></tr>
<tr><td><code>MORADO</code></td><td>#A05CFF</td><td>Botón Salir, bordes de tarjeta, el logo, el empate.</td><td>Varios</td></tr>
<tr><td><code>LAVANDA</code></td><td>#C8BCF6</td><td>Rejilla del tablero, rótulos, logo, contornos suaves.</td><td>Tablero (48), rótulos (46)</td></tr>
<tr><td><code>TEXTO</code></td><td>#FFFFFF</td><td>Texto principal.</td><td>Todo</td></tr>
<tr><td><code>TEXTO_SUAVE</code></td><td>#A89BE2</td><td>Texto secundario (descripciones, ayudas).</td><td>Varios</td></tr>
<tr><td><code>SUPERFICIE</code></td><td>#2B2363 · 125 (49 %)</td><td>Relleno «de cristal» de las tarjetas.</td><td><code>Tarjeta</code> (43)</td></tr>
<tr><td><code>CASILLA</code></td><td>#2E285A · 170 (67 %)</td><td>Fondo de cada casilla del tablero.</td><td><code>PanelTablero</code> (48)</td></tr>
</table>
<p>¿Se lee bien todo esto? Con la fórmula de contraste del capítulo 35 (WCAG), sobre <code>FONDO_ARRIBA</code>: el blanco
da 16.9:1, <code>LAVANDA</code> 9.6:1, <code>TEXTO_SUAVE</code> 6.8:1, <code>ROSA</code> 5.5:1, <code>AZUL</code> 4.7:1
y <code>MORADO</code> 4.4:1. Todo lo que es texto supera el mínimo de 4.5:1; el morado, que queda un pelo por debajo, se
usa en bordes, iconos y títulos grandes, donde basta con 3:1.</p>

<h2>Las fuentes y su respaldo</h2>
<p>El diseño usa una fuente redondeada y amable, del estilo de <i>Nunito</i> o <i>Poppins</i> (capítulo 36). El problema:
Java dibuja con las fuentes <b>instaladas en la computadora donde se ejecuta</b>, y no sabes cuáles tendrá cada jugador.
La solución de <code>Tema</code> es una <b>lista de preferencias</b>: prueba las fuentes en orden y se queda con la
primera que exista. Si no encuentra ninguna, usa <code>"SansSerif"</code>, una fuente <i>lógica</i> que Java garantiza
siempre (en Windows la traduce a Arial). En un Windows típico ganará <i>Segoe UI</i>, la fuente de la propia interfaz de
Windows.</p>
<div class="caja consejo"><b>¿Quieres ver el Totito con Nunito?</b> Es una fuente gratuita de Google Fonts. Descárgala de
<code>fonts.google.com</code>, abre el <code>.ttf</code> de la variante normal y de la negrita, y pulsa <i>Instalar para
todos los usuarios</i>. La próxima vez que arranque el juego, <code>Tema</code> la encontrará primero en la lista, sin
cambiar una línea de código. Recuerda que en la computadora de otra persona se verá con su propia fuente de respaldo.</div>

<h2>Qué vas a aprender</h2>
<ul>
<li>Las <b>clases de utilidad</b>: <code>final</code>, constructor privado y todo <code>static</code>.</li>
<li><code>java.awt.Color</code> con y sin alfa, y los literales hexadecimales <code>0x1C</code>.</li>
<li><code>List</code>, <code>Arrays.asList</code> y <code>Map.of</code>, con sus tipos genéricos <code>&lt;String&gt;</code>.</li>
<li>El orden en que Java inicializa los atributos <code>static</code> (y la trampa silenciosa que esconde).</li>
<li><code>Font</code>, <code>deriveFont</code> (y por qué <code>deriveFont(20)</code> no hace lo que parece), y el espaciado de letras con <code>TextAttribute.TRACKING</code>.</li>
<li>Limitar un valor a un rango con <code>Math.max</code> y <code>Math.min</code>; mezclar colores con una fórmula.</li>
<li><code>String.format</code> con <code>%02X</code>, y <code>try/catch</code> como respaldo.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>En la rama <code>interfaz-neon</code>: clic derecho en <i>&lt;default package&gt;</i> → <i>New → Java Class…</i></li>
<li>Nombre: <code>Tema</code>. <i>Finish</i>. Borra la plantilla y escribe el código.</li>
</ol>
<pre class="ps">New-Item src\Tema.java</pre>
""",
    "archivos": [
        {"ruta": "src/Tema.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>import</code> le dice al compilador dónde buscar una clase que no está en el proyecto, para
poder escribir su nombre corto. <code>java.awt.Color</code> representa un color con sus componentes rojo, verde, azul y
alfa (RGBA, capítulo 35). Es la clase más usada del archivo: cada constante de la paleta es un <code>Color</code>.</p>
<p class="l"><b>L2</b> <code>java.awt.Font</code>: una fuente concreta, es decir, una familia (por ejemplo «Segoe UI»),
un estilo (normal, negrita, cursiva) y un tamaño. Los métodos <code>fuente</code> y <code>fuenteEspaciada</code> la
crean.</p>
<p class="l"><b>L3</b> <code>java.awt.GraphicsEnvironment</code>: describe el entorno gráfico del equipo (pantallas y
fuentes instaladas). Se usa una sola vez, en <code>elegirFamilia</code>, para preguntar qué fuentes hay.</p>
<p class="l"><b>L4</b> <code>java.awt.font.TextAttribute</code>: las «llaves» de los atributos avanzados de texto
(subrayado, ancho, espaciado…). Aquí se usa <code>TextAttribute.TRACKING</code>, el espaciado entre letras. Fíjate en que
está en un subpaquete, <code>java.awt.font</code>, distinto de <code>java.awt</code>.</p>
<p class="l"><b>L5</b> <code>java.util.Arrays</code>: utilidades para arreglos. Se usa su método
<code>Arrays.asList(...)</code>, que convierte una serie de valores (o un arreglo) en una lista.</p>
<p class="l"><b>L6</b> <code>java.util.List</code>: una <b>lista</b>, una colección ordenada de elementos. A diferencia
de un arreglo, trae métodos útiles como <code>contains</code> («¿está este elemento?»).</p>
<p class="l"><b>L7</b> <code>java.util.Map</code>: un <b>mapa</b> o diccionario, que asocia llaves con valores (como
«palabra → definición»). Se usa para decirle a una fuente «espaciado → 0.3».</p>
<p class="l">¿Por qué importar clase por clase y no <code>import java.awt.*;</code> como hizo <code>JuegoMain</code>? Ambas
formas funcionan; importarlas una a una deja a la vista exactamente qué usa el archivo y evita choques de nombres (por
ejemplo, existe un <code>java.awt.List</code> y un <code>java.util.List</code>: con dos asteriscos, Java no sabría cuál
quieres).</p>
"""),
             ("public final class Tema", r"""
<p class="l"><b>L9–L15</b> Comentario de la clase: qué guarda (paleta y tipografía de la interfaz «neón») y la regla de uso:
no debe haber colores sueltos repartidos por las pantallas.</p>
<p class="l"><b>L16</b> <code>public final class Tema</code>. <code>final</code> en una clase significa que <b>nadie
puede heredar de ella</b> (capítulo 22): no tiene sentido una «subclase de Tema». Junto con el constructor privado de L52
la convierte en una <b>clase de utilidad</b>, como <code>Math</code> de Java: un lugar donde agrupar constantes y métodos
<code>static</code>, que se usan con el nombre de la clase (<code>Tema.ROSA</code>, <code>Tema.conAlfa(...)</code>) sin
crear objetos.</p>
"""),
             ("FONDO_ARRIBA", r"""
<p class="l"><b>L18</b> Comentario: los dos colores siguientes forman el degradado del fondo, de arriba hacia abajo.</p>
<p class="l"><b>L19</b> <code>public static final Color</code>: una constante pública (<code>public</code>), de la clase
y no de cada objeto (<code>static</code>), que no se puede reasignar (<code>final</code>). Por convención, las constantes
se escriben en MAYÚSCULAS con guiones bajos. <code>new Color(0x1C, 0x17, 0x40)</code> crea el color con rojo, verde y azul
entre 0 y 255. El prefijo <code>0x</code> indica un número escrito en <b>hexadecimal</b>: <code>0x1C</code> es 28,
<code>0x17</code> es 23 y <code>0x40</code> es 64. Se escribe así para que coincida letra por letra con el
<code>#1C1740</code> del diseño y puedas comparar sin calcular. Es el morado oscuro de arriba.</p>
<p class="l"><b>L20</b> El color de abajo, #0E0B24, casi negro. El degradado de uno a otro (capítulo 55) da profundidad,
como un cielo de noche.</p>
"""),
             ("public static final Color DECORACION", r"""
<p class="l"><b>L21</b> Comentario: las X y O gigantes y desvaídas que adornan el fondo.</p>
<p class="l"><b>L22</b> Aquí el constructor de <code>Color</code> recibe <b>cuatro</b> números: el cuarto es el
<b>alfa</b>, la opacidad, de 0 (invisible) a 255 (opaco). 70 de 255 es un 27 %: se ve el morado #5B35C2, pero dejando
pasar el fondo. Un adorno debe acompañar sin competir con los botones; con alfa 255 las X y O del fondo gritarían.</p>
"""),
             ("public static final Color ROSA", r"""
<p class="l"><b>L24–L25</b> El rosa neón #FF3BD4. El comentario establece una regla de todo el juego: <b>la X siempre es
rosa</b>, la juegue quien la juegue. Así el jugador reconoce su ficha por el color en cualquier pantalla.</p>
<p class="l"><b>L26–L27</b> <code>FRESA</code>, #FF3D82: un rosa más rojizo para la tarjeta del Jugador 1, porque así lo
pide el diseño. Es casi igual a <code>ROSA</code> en rojo y verde; lo que cambia es el azul (0x82 en vez de 0xD4), y eso lo
aleja del morado y lo acerca al rojo.</p>
"""),
             ("public static final Color AZUL", r"""
<p class="l"><b>L28–L29</b> El azul #2F84FF: <b>la O siempre es azul</b>. Rosa y azul están lejos en el círculo
cromático, de modo que X y O se distinguen de un vistazo, incluso de reojo.</p>
<p class="l"><b>L30</b> <code>CIAN</code>, #40C8FF: un azul verdoso más claro, para el trofeo y el título de victoria.
Con el rosa forma el degradado del título «TOTITO».</p>
<p class="l"><b>L31</b> <code>MORADO</code>, #A05CFF: el color «puente» entre el rosa y el azul; botón Salir, bordes, el
empate.</p>
<p class="l"><b>L32</b> <code>LAVANDA</code>, #C8BCF6: un morado muy claro y poco saturado, para líneas y textos
decorativos que deben verse sin brillar tanto como los neones.</p>
"""),
             ("public static final Color TEXTO =", r"""
<p class="l"><b>L34</b> El texto principal es blanco. <code>Color.WHITE</code> es una constante que ya trae la clase
<code>Color</code> (equivale a <code>new Color(255, 255, 255)</code>). ¿Para qué darle otro nombre? Porque las pantallas
piden «el color del texto», no «blanco»: si un día el texto pasa a ser crema, se cambia aquí.</p>
<p class="l"><b>L35</b> <code>TEXTO_SUAVE</code>, #A89BE2: para lo secundario (descripciones, ayudas, leyendas). Menos
contraste que el blanco, pero todavía cómodo de leer (6.8:1). Así se crea jerarquía: lo importante, blanco; lo
accesorio, lavanda apagado.</p>
"""),
             ("SUPERFICIE", r"""
<p class="l"><b>L36–L37</b> <code>SUPERFICIE</code>, el relleno de las tarjetas: #2B2363 con alfa 125 (49 %). El
comentario dice «semitransparente a propósito»: a través de la tarjeta se adivina el fondo y sus X y O gigantes. Ese es el
efecto «cristal» (en diseño se le llama <i>glassmorphism</i>).</p>
<p class="l"><b>L38–L39</b> <code>CASILLA</code>, #2E285A con alfa 170 (67 %): más opaca que las tarjetas, porque las
fichas neón se lucen mejor sobre un fondo más firme.</p>
"""),
             ("private static final List<String> FAMILIAS", r"""
<p class="l"><b>L41–L45</b> Comentario que explica la estrategia de las fuentes: preferencias en orden, la primera que
exista gana; si ninguna, «SansSerif».</p>
<p class="l"><b>L46</b> <code>private</code>: es un detalle interno; nadie fuera de <code>Tema</code> necesita la lista.
<code>List&lt;String&gt;</code> se lee «lista de textos»: lo que va entre <code>&lt; &gt;</code> es el <b>tipo de los
elementos</b> (genéricos). Gracias a eso, Java no te dejaría meter un número en la lista por error.
<code>Arrays.asList(...)</code> crea una lista con los valores que le pases, en ese orden.</p>
<p class="l"><b>L47</b> Las preferidas: <i>Nunito</i>, <i>Poppins</i> y <i>Montserrat</i> (redondeadas, como el diseño;
rara vez vienen instaladas), luego <i>Segoe UI</i> (Windows) y <i>Helvetica Neue</i> (Mac).</p>
<p class="l"><b>L48</b> Respaldo: <i>Ubuntu</i> (Linux Ubuntu), <i>Arial</i> (casi universal), <i>Liberation Sans</i> y
<i>DejaVu Sans</i> (otros Linux). El paréntesis y el <code>;</code> cierran la llamada que empezó en L46: una instrucción
puede ocupar varias líneas; el <code>;</code> marca dónde termina.</p>
"""),
             ("private static final String FAMILIA =", r"""
<p class="l"><b>L50</b> La familia elegida, calculada <b>una sola vez</b> llamando a <code>elegirFamilia()</code> (L89).
Preguntarle al sistema por sus fuentes es lento (puede tardar decenas de milisegundos); hacerlo cada vez que un botón se
dibuja sería un desperdicio. Al ser <code>static final</code>, el cálculo ocurre al <b>cargar la clase</b>: la primera vez
que cualquier parte del programa use <code>Tema</code>.</p>
<div class="caja cuidado"><b>El orden de estas dos líneas importa.</b> Java inicializa los atributos <code>static</code>
de arriba hacia abajo, en el orden en que están escritos. <code>FAMILIAS</code> (L46) debe ir <b>antes</b> que
<code>FAMILIA</code> (L50). Si los invirtieras, <code>elegirFamilia()</code> se ejecutaría cuando <code>FAMILIAS</code>
todavía vale <code>null</code>; el <code>for</code> lanzaría un <code>NullPointerException</code>, el <code>catch</code> de
L98 lo atraparía en silencio y el juego usaría siempre «SansSerif» sin ningún mensaje de error. Lo comprobamos: con el
orden invertido, el resultado es «SansSerif» aunque tengas Segoe UI instalada.</div>
"""),
             ("private Tema()", r"""
<p class="l"><b>L52–L53</b> Constructor <code>private</code> y vacío. Al ser privado, nadie fuera de la clase puede
escribir <code>new Tema()</code>; el compilador lo prohíbe. ¿Por qué escribirlo? Porque si una clase no declara ningún
constructor, Java le regala uno público invisible, y alguien podría crear objetos <code>Tema</code> que no sirven para
nada. Así se deja claro que es una clase de utilidad.</p>
"""),
             ("public static Font fuente(", r"""
<p class="l"><b>L55</b> Comentario: <code>estilo</code> es <code>Font.PLAIN</code> (normal) o <code>Font.BOLD</code>
(negrita). Son constantes <code>int</code> de la clase <code>Font</code> (0 y 1).</p>
<p class="l"><b>L56</b> Método <code>public static</code> que devuelve un <code>Font</code>. Se usará así:
<code>Tema.fuente(Font.BOLD, 20f)</code>. El tamaño es un <code>float</code> (número con decimales; la <code>f</code> al
final de <code>20f</code> indica que es <code>float</code>) porque el diseño usa tamaños como 10.5 o 17.</p>
<p class="l"><b>L57</b> Dos pasos en una línea. <code>new Font(FAMILIA, estilo, 12)</code> crea la fuente; su constructor
solo acepta tamaños <b>enteros</b>, así que se usa un 12 provisional. Luego <code>.deriveFont(tamano)</code> crea una copia
con el tamaño exacto en <code>float</code>.</p>
<div class="caja cuidado"><b>La trampa de deriveFont.</b> <code>Font</code> tiene dos versiones de <code>deriveFont</code>
con un solo número: <code>deriveFont(float tamaño)</code> y <code>deriveFont(int estilo)</code>. Si escribes
<code>deriveFont(20)</code> (un <code>int</code>), Java elige la segunda: intenta cambiar el <b>estilo</b> y la fuente se
queda en tamaño 12. Lo comprobamos: <code>new Font("Dialog", Font.PLAIN, 12).deriveFont(20).getSize()</code> devuelve 12.
Por eso <code>tamano</code> es <code>float</code> y en el código siempre verás <code>20f</code>, con <code>f</code>.</div>
"""),
             ("public static Font fuenteEspaciada", r"""
<p class="l"><b>L60</b> Comentario: fuente con las letras separadas, para títulos como «J U G A D O R E S».</p>
<p class="l"><b>L61</b> Recibe además el <code>espaciado</code>, una fracción del tamaño de la letra: 0.3 significa
«añade entre cada par de letras un 30 % del tamaño».</p>
<p class="l"><b>L62</b> Reutiliza <code>fuente(...)</code> (no repite su código) y le aplica atributos.
<code>Map.of(TextAttribute.TRACKING, espaciado)</code> crea un mapa de una sola entrada: llave
<code>TRACKING</code> (el espaciado entre letras, en la jerga tipográfica <i>tracking</i>, capítulo 36), valor
<code>espaciado</code>. <code>deriveFont(Map)</code> devuelve una fuente nueva con esos atributos. Con 17 puntos y 0.3,
cada letra gana unos 5 píxeles de aire: en nuestra prueba, «JUGADORES» pasó de 108 a 154 píxeles de ancho.</p>
"""),
             ("public static Color colorDeFicha", r"""
<p class="l"><b>L65</b> Comentario: la regla de oro del color de las fichas.</p>
<p class="l"><b>L66–L67</b> Recibe una ficha (<code>'X'</code> u <code>'O'</code>) y devuelve su color con un ternario.
Cualquier otro carácter devuelve <code>AZUL</code>; en la práctica solo llegan X u O. Al tener la regla en un único método,
el marcador, el letrero de turno, la tarjeta del jugador y la pantalla de resultado la cumplen sin repetirla.</p>
"""),
             ("public static Color conAlfa", r"""
<p class="l"><b>L70</b> Comentario: el mismo color, con otra transparencia.</p>
<p class="l"><b>L71</b> Recibe un color y un alfa nuevo. Es la herramienta más usada por el efecto neón (capítulo 41),
que dibuja capas del mismo color con alfas 6, 11, 16…</p>
<p class="l"><b>L72</b> Un <code>Color</code> no se puede modificar (es <i>inmutable</i>): para «cambiarle» el alfa hay que
crear uno nuevo. <code>getRed()</code>, <code>getGreen()</code> y <code>getBlue()</code> leen los componentes del color
original.</p>
<p class="l"><b>L73</b> El cuarto argumento <b>limita</b> el alfa al rango 0–255: <code>Math.min(255, alfa)</code> se queda
con el menor (si alfa es 300, da 255) y <code>Math.max(0, ...)</code> con el mayor (si es −5, da 0). ¿Por qué? Porque el
constructor de <code>Color</code> no perdona: con un alfa de 300 lanza
<code>IllegalArgumentException: Color parameter outside of expected range: Alpha</code> y el componente no se dibuja. Al
multiplicar alfas por una «intensidad» es fácil pasarse; esta línea lo hace imposible. A esta técnica se le llama
<i>sujetar</i> un valor (en inglés, <i>clamp</i>).</p>
"""),
             ("public static Color aclarar", r"""
<p class="l"><b>L76</b> Comentario: mezcla con blanco; factor 0 = igual, factor 1 = blanco.</p>
<p class="l"><b>L77</b> Recibe el color y el <code>factor</code> de mezcla (0 a 1).</p>
<p class="l"><b>L78</b> La fórmula de la mezcla para el rojo: <code>rojo + (255 − rojo) × factor</code>. <code>255 −
rojo</code> es lo que le falta al rojo para llegar al máximo; se recorre esa fracción del camino. <code>Math.round</code>
redondea al entero más cercano (al multiplicar por un <code>float</code> el resultado tiene decimales, y un componente de
color debe ser entero). Ejemplo con <code>ROSA</code> (255, 59, 212) y factor 0.6: rojo 255 + 0 × 0.6 = 255.</p>
<p class="l"><b>L79</b> Lo mismo para el verde: 59 + (255 − 59) × 0.6 = 59 + 117.6 = 176.6 → 177.</p>
<p class="l"><b>L80</b> Y para el azul: 212 + 43 × 0.6 = 237.8 → 238. Resultado: (255, 177, 238), un rosa pálido. Es el
«centro casi blanco» de las fichas neón (capítulo 41) y el lado claro de los degradados de los iconos (42).</p>
<p class="l"><b>L81</b> Crea el color mezclado conservando el alfa original con <code>getAlpha()</code>.</p>
"""),
             ("public static String hex", r"""
<p class="l"><b>L84</b> Comentario: para usar los colores del tema dentro de texto HTML de un <code>JLabel</code>.</p>
<p class="l"><b>L85–L86</b> Convierte un color al texto <code>"#RRGGBB"</code>. <code>String.format</code> (capítulo 17)
rellena una plantilla: cada <code>%02X</code> es un hueco que se llena con un número escrito en hexadecimal
(<code>X</code>, con letras mayúsculas), de al menos 2 cifras (<code>2</code>) y con ceros a la izquierda si hacen falta
(<code>0</code>). Sin el <code>02</code>, el azul de <code>FONDO_ABAJO</code> (0x0E) saldría como <code>E</code> y el
texto quedaría mal. <code>Tema.hex(Tema.ROSA)</code> devuelve <code>"#FF3BD4"</code>. Lo usa la pantalla de instrucciones
(capítulo 57) para pintar la X rosa y la O azul en medio de una frase.</p>
"""),
             ("private static String elegirFamilia", r"""
<p class="l"><b>L89</b> Método privado que devuelve el nombre de una familia de fuentes. Se llama una sola vez, desde
L50.</p>
<p class="l"><b>L90</b> <code>try</code> abre un bloque «protegido»: si algo dentro lanza una excepción, en vez de
detener el programa, Java salta al <code>catch</code> (L98). Capítulo 26.</p>
<p class="l"><b>L91–L92</b> Pide la lista de fuentes instaladas. <code>GraphicsEnvironment.getLocalGraphicsEnvironment()</code>
devuelve el entorno gráfico de esta computadora, y su <code>getAvailableFontFamilyNames()</code> un arreglo
<code>String[]</code> con los nombres de todas las familias (en Windows suelen ser más de cien). Se envuelve con
<code>Arrays.asList</code> para poder usar <code>contains</code>.</p>
<p class="l"><b>L93</b> Recorre las preferidas <b>en orden</b>: primero Nunito, luego Poppins…</p>
<p class="l"><b>L94–L95</b> Si esa familia está instalada, la devuelve y el método termina ahí. Como el orden de
<code>FAMILIAS</code> es el de preferencia, la primera encontrada es la mejor disponible.</p>
"""),
             ("} catch (RuntimeException e)", r"""
<p class="l"><b>L98</b> <code>catch (RuntimeException e)</code> atrapa cualquier excepción «no comprobada» que haya
ocurrido en el <code>try</code>. Preguntar por las fuentes del sistema casi nunca falla, pero hay entornos raros
(servidores sin pantalla mal configurados, permisos restringidos) en los que podría. Un problema con las fuentes no debe
impedir que el juego arranque.</p>
<p class="l"><b>L99–L100</b> El <code>catch</code> está vacío a propósito, y el comentario lo dice. Un <code>catch</code>
vacío <b>sin</b> explicación es una mala práctica (esconde errores); con el comentario, cualquiera entiende que es una
decisión: si falla, seguimos con el respaldo.</p>
<p class="l"><b>L101</b> Si no se encontró ninguna preferida, o si hubo un error, se devuelve <code>Font.SANS_SERIF</code>,
una constante que vale <code>"SansSerif"</code>: una fuente <i>lógica</i> que no es un archivo concreto, sino un nombre que
Java traduce a una fuente real del sistema y que existe siempre.</p>
<p class="l"><b>L102–L103</b> Cierran el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<p><code>Tema</code> no se crea con <code>new</code>: se <b>carga</b>. La primera vez que el programa escriba algo como
<code>Tema.ROSA</code>, la máquina virtual de Java carga la clase y ejecuta, de arriba abajo, las inicializaciones de sus
atributos <code>static</code>. Así ocurre en un Windows típico:</p>
<ol>
<li>L19–L39: se crean los trece objetos <code>Color</code>.</li>
<li>L46: se crea la lista <code>FAMILIAS</code> con nueve nombres.</li>
<li>L50: <code>elegirFamilia()</code> pide las fuentes instaladas y recorre la lista: «Nunito», no está; «Poppins», no;
«Montserrat», no; «Segoe UI», <b>sí</b>. <code>FAMILIA</code> queda en <code>"Segoe UI"</code> para siempre.</li>
</ol>
<p>A partir de ahí, cada llamada es un cálculo pequeño:</p>
<table class="tabla">
<tr><th>Llamada</th><th>Resultado</th></tr>
<tr><td><code>Tema.fuente(Font.BOLD, 20f)</code></td><td>Segoe UI, negrita, 20 puntos</td></tr>
<tr><td><code>Tema.fuenteEspaciada(Font.BOLD, 17f, 0.3f)</code></td><td>Segoe UI, negrita, 17 puntos, ~5 px extra entre letras</td></tr>
<tr><td><code>Tema.colorDeFicha('O')</code></td><td><code>AZUL</code> (47, 132, 255)</td></tr>
<tr><td><code>Tema.conAlfa(Tema.ROSA, 31)</code></td><td>(255, 59, 212) con alfa 31 (12 % de opacidad)</td></tr>
<tr><td><code>Tema.conAlfa(Tema.ROSA, 300)</code></td><td>(255, 59, 212) con alfa 255: el 300 se recortó</td></tr>
<tr><td><code>Tema.aclarar(Tema.ROSA, 0.6f)</code></td><td>(255, 177, 238)</td></tr>
<tr><td><code>Tema.aclarar(Tema.AZUL, 0.6f)</code></td><td>(172, 206, 255)</td></tr>
<tr><td><code>Tema.hex(Tema.AZUL)</code></td><td><code>"#2F84FF"</code></td></tr>
</table>

<h2>Compila y prueba</h2>
<p>Como en los capítulos anteriores, aún no hay nada que ver: <i>Run → Clean and Build Project</i> (Shift+F11) y
<code>BUILD SUCCESS</code>, o en PowerShell:</p>
<pre class="ps">javac -encoding UTF-8 -d out src\*.java</pre>

<h3>Prueba opcional: ¿qué fuente eligió tu computadora?</h3>
<p>Crea un archivo temporal en la raíz del proyecto (no en <code>src</code>):</p>
<pre class="ps">New-Item ProbarTema.java</pre>
<pre class="java">import java.awt.Color;
import java.awt.Font;

public class ProbarTema {
    public static void main(String[] args) {
        System.out.println("Fuente elegida: " + Tema.fuente(Font.PLAIN, 12f).getFamily());
        System.out.println("ROSA en hex: " + Tema.hex(Tema.ROSA));
        System.out.println("Color de la O: " + Tema.hex(Tema.colorDeFicha('O')));
        Color halo = Tema.conAlfa(Tema.ROSA, 31);
        System.out.println("ROSA con alfa 31: " + halo + " alfa=" + halo.getAlpha());
        System.out.println("ROSA aclarado 60%: " + Tema.aclarar(Tema.ROSA, 0.6f));
        System.out.println("Alfa 300 se recorta a: " + Tema.conAlfa(Tema.ROSA, 300).getAlpha());
        Font titulo = Tema.fuenteEspaciada(Font.BOLD, 17f, 0.3f);
        System.out.println("Fuente espaciada: " + titulo.getSize2D() + " pt, negrita=" + titulo.isBold());
    }
}</pre>
<pre class="ps">java -cp target\classes ProbarTema.java</pre>
<pre class="salida">Fuente elegida: Segoe UI
ROSA en hex: #FF3BD4
Color de la O: #2F84FF
ROSA con alfa 31: java.awt.Color[r=255,g=59,b=212] alfa=31
ROSA aclarado 60%: java.awt.Color[r=255,g=177,b=238]
Alfa 300 se recorta a: 255
Fuente espaciada: 17.0 pt, negrita=true</pre>
<p>La primera línea depende de tu equipo: en Windows lo normal es <code>Segoe UI</code>; si instalaste Nunito, dirá
<code>Nunito</code>. (Fíjate en que el texto de un <code>Color</code> no muestra el alfa; por eso se imprime aparte con
<code>getAlpha()</code>.) Al terminar:</p>
<pre class="ps">Remove-Item ProbarTema.java</pre>

<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Mensaje o síntoma</th><th>Causa y solución</th></tr>
<tr><td><code>cannot find symbol: class TextAttribute</code></td><td>Falta o está mal el <code>import java.awt.font.TextAttribute;</code> (ojo: <code>font</code> en minúscula).</td></tr>
<tr><td><code>reference to List is ambiguous</code></td><td>Importaste <code>java.awt.*</code> y <code>java.util.*</code> a la vez. Importa las clases una por una, como en el código.</td></tr>
<tr><td><code>illegal character: '#'</code> o <code>hexadecimal numbers must contain at least one hexadecimal digit</code></td><td>Escribiste <code>#1C</code> (como en el diseño) o una letra que no existe en hexadecimal (<code>0xG2</code>). En Java el hexadecimal empieza con <code>0x</code> y solo usa 0–9 y A–F.</td></tr>
<tr><td>Más adelante, todo el texto sale en una fuente «de sistema»</td><td>Revisa que <code>FAMILIAS</code> esté declarada antes que <code>FAMILIA</code>.</td></tr>
</table>

<div class="caja git"><b>Git</b>
<pre class="ps">git status
git add src\Tema.java
git commit -m "Tema: paleta de colores y fuentes"
git push</pre>
</div>

<h2>Resumen</h2>
<ul>
<li><code>Tema</code> es la única fuente de verdad del aspecto: trece colores con nombre y dos métodos de fuentes.</li>
<li>Es una clase de utilidad: <code>final</code>, constructor privado y todo <code>static</code>.</li>
<li><code>new Color(r, g, b, alfa)</code> con literales <code>0x</code> que coinciden con el hex del diseño; el alfa crea el cristal y los adornos.</li>
<li>La fuente se elige una vez, de una lista de preferencias, con <code>"SansSerif"</code> como respaldo garantizado.</li>
<li>Los <code>static</code> se inicializan en orden de aparición; <code>FAMILIAS</code> antes que <code>FAMILIA</code>.</li>
<li><code>deriveFont</code> con <code>float</code> cambia el tamaño; con <code>int</code>, el estilo.</li>
<li><code>conAlfa</code> sujeta el alfa a 0–255; <code>aclarar</code> mezcla con blanco; <code>hex</code> da el texto <code>#RRGGBB</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b> Una clase de tema es de lo primero que vale la pena crear en
cualquier interfaz:
<ul>
<li><b>Modo claro y modo oscuro:</b> dos clases (o dos objetos) con los mismos nombres de color y valores distintos; la aplicación elige uno al arrancar.</li>
<li><b>La identidad de una empresa:</b> en un sistema de inventario o de facturación, los colores y el logo de la marca en un único archivo; si la empresa cambia de imagen, se toca un solo lugar.</li>
<li><b>Páginas web:</b> la misma idea son las «variables CSS» (<code>--color-primario: #FF3BD4;</code>) que verás en cualquier sitio moderno.</li>
<li><b>Respaldo de recursos:</b> la lista de preferencias con un valor garantizado al final sirve para fuentes, idiomas («español de Guatemala → español → inglés») o servidores de respaldo.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Calcula a mano <code>Tema.aclarar(Tema.AZUL, 0.5f)</code> y compruébalo con <code>ProbarTema</code>. Pista: AZUL es (47, 132, 255).</li>
<li>¿Qué devuelve <code>Tema.hex(Tema.FONDO_ABAJO)</code>? Escríbelo antes de probarlo y explica por qué hace falta el <code>02</code> de <code>%02X</code>.</li>
<li>En tu archivo de prueba, imprime <code>Tema.fuente(Font.PLAIN, 12f).deriveFont(20).getSize()</code> y luego con
<code>20f</code>. Explica la diferencia.</li>
<li>Escribe en tu prueba un método <code>oscurecer(Color c, float factor)</code> que mezcle con negro en vez de con
blanco. Pista: el objetivo ya no es 255, sino 0: <code>rojo − rojo × factor</code>.</li>
<li>Reto: crea una paleta alternativa «retro verde» (fondo casi negro, fichas verde fósforo y ámbar). Pruébala cambiando
los valores en una <b>copia</b> de <code>Tema.java</code> fuera del proyecto y piensa: ¿cuántos archivos del juego habría
que tocar para aplicarla? (Respuesta esperada: uno.)</li>
</ol></div>
""",
}
