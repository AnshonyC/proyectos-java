CAPITULO = {
    "numero": 45,
    "titulo": "Encabezado.java: la barra superior y un layout hecho a mano",
    "antes": r"""
<p class="entrada">La barra de arriba, con el logotipo, el título «Juego del Totito», el lema y la X de cerrar,
aparece idéntica en las cinco pantallas. En este capítulo la construyes una sola vez y aprendes una técnica muy útil:
prescindir del layout y colocar a mano el único componente real que tiene, recalculando su posición cada vez que la
barra cambia de tamaño.</p>

<h2>Por qué existe este archivo</h2>
<p>Mira cualquiera de las capturas: la franja superior es siempre la misma. Si cada pantalla la dibujara por su
cuenta, tendrías cinco copias del mismo código y, el día que quisieras cambiar el lema, cinco lugares que corregir (y
uno que se te olvidaría). Así que es un componente propio, <code>Encabezado</code>, que <code>PantallaBase</code>
(capítulo 55) colocará arriba de todas las pantallas con una sola línea.</p>
<figure><img src="capturas/2-instrucciones.png"><figcaption>El encabezado: logotipo a la izquierda, título en dos
colores con halo, lema en letras separadas y la X de cerrar a la derecha.</figcaption></figure>
<p>Casi todo el encabezado es <b>dibujo</b>: la caja, el logotipo, el título y el lema no reaccionan al ratón, así que
se pintan en <code>paintComponent</code> como en la tarjeta. Solo la X necesita ser un componente de verdad, porque hay
que poder pulsarla, debe brillar al pasar el ratón y mostrar un tooltip. Para eso ya tienes <code>BotonNeon.icono</code>
(capítulo 44).</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>Crear un panel <b>sin layout</b> (<code>super(null)</code>) y colocar a su hijo sobrescribiendo
<code>doLayout()</code>.</li>
<li>Cómo pide su tamaño un componente que va en el norte de un <code>BorderLayout</code>.</li>
<li>Recibir «qué hacer» como parámetro con la interfaz <code>Runnable</code> y una lambda.</li>
<li>Centrar un título formado por <b>dos partes</b> con estilos distintos, midiendo cada una.</li>
<li>Rellenar texto con un <b>degradado</b> en lugar de un color liso.</li>
<li>Letras espaciadas (<i>tracking</i>) y por qué hay que volver a medir al cambiar de fuente.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>En la rama <code>interfaz-neon</code>, en NetBeans: clic derecho en <i>&lt;default package&gt;</i> → <i>New →
Java Class…</i> → <code>Encabezado</code> → <i>Finish</i>.</li>
<li>Sustituye el esqueleto por el código de abajo.</li>
</ol>
<pre class="ps">New-Item -ItemType File src\Encabezado.java
notepad src\Encabezado.java</pre>
<div class="caja cuidado"><b>Tildes y símbolos dentro del código</b> La línea 72 contiene «DIVERSIÓN», «CLÁSICO» y
el punto «•». El archivo debe guardarse en <b>UTF-8</b>. NetBeans lo hace solo (el <code>pom.xml</code> lo indica con
<code>project.build.sourceEncoding</code>) y el Bloc de notas de Windows 10/11 también guarda en UTF-8 por defecto.
Si alguna vez ves «DIVERSIÃ“N» en pantalla, el archivo se guardó o se compiló con otra codificación: vuelve a
guardarlo como UTF-8 y compila con <code>-encoding UTF-8</code>.</div>
""",
    "archivos": [
        {"ruta": "src/Encabezado.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.Dimension</code>: un par ancho × alto. Lo usaremos para decir qué alto queremos
tener.</p>
<p class="l"><b>L2</b> <code>java.awt.Font</code>: por la constante <code>Font.BOLD</code> (negrita).</p>
<p class="l"><b>L3</b> <code>java.awt.FontMetrics</code>: para medir el título y el lema y poder centrarlos.</p>
<p class="l"><b>L4</b> <code>java.awt.GradientPaint</code>: dos degradados, el del fondo de la caja y el de la palabra
«Totito».</p>
<p class="l"><b>L5–L6</b> <code>Graphics</code> y <code>Graphics2D</code>: el pincel, como siempre.</p>
<p class="l"><b>L7</b> <code>RoundRectangle2D</code>: la caja redondeada de la barra.</p>
<p class="l"><b>L8</b> <code>javax.swing.JPanel</code>: el encabezado es un panel porque <b>contiene</b> otro
componente (el botón). Si no contuviera nada, bastaría con <code>JComponent</code>, como verás en
<code>Rotulo</code>.</p>
<p class="l"><b>L9</b> En blanco.</p>
<p class="l">¿Y <code>Runnable</code>, que usaremos en la línea 23? No se importa: está en el paquete
<code>java.lang</code>, que Java importa siempre de forma automática (por eso tampoco importas nunca
<code>String</code> ni <code>Math</code>).</p>
"""),
             ("public class Encabezado", r"""
<p class="l"><b>L10–L13</b> Comentario de documentación: barra común a todas las pantallas.</p>
<p class="l"><b>L14</b> <code>public class Encabezado extends JPanel {</code> el encabezado es un panel.</p>
<p class="l"><b>L15</b> En blanco.</p>
"""),
             ("public static final int ALTO", r"""
<p class="l"><b>L16</b> <code>public static final int ALTO = 96;</code> el alto fijo de la barra, en píxeles. Es
<code>public</code> para que otras clases puedan descontarlo si calculan cuánto espacio queda debajo.</p>
<p class="l"><b>L17</b> <code>MARGEN = 10</code>: espacio para el halo de la caja, con el mismo razonamiento que en la
tarjeta (capítulo 43). <code>private</code>: es un detalle interno.</p>
<p class="l"><b>L18</b> <code>LADO_BOTON = 58</code>: el lado del botón cuadrado de cerrar. Tiene que coincidir con el
58 × 58 que fija <code>BotonNeon.icono</code>. Darle nombre evita que el 58 aparezca «mágico» varias veces en
<code>doLayout</code> (los «números mágicos» del capítulo 27).</p>
<p class="l"><b>L19</b> En blanco.</p>
"""),
             ("private final BotonNeon botonCerrar;", r"""
<p class="l"><b>L20</b> <code>private final BotonNeon botonCerrar;</code> guardamos el botón en un atributo porque lo
necesitamos en dos momentos distintos: al crearlo (constructor) y al colocarlo (<code>doLayout</code>). Una variable
local del constructor moriría al terminar este.</p>
<p class="l"><b>L21</b> En blanco.</p>
"""),
             ("public Encabezado(Runnable alCerrar)", r"""
<p class="l"><b>L22</b> Comentario Javadoc con la etiqueta <code>@param</code>: documenta el parámetro
<code>alCerrar</code>, «qué hacer al pulsar la X».</p>
<p class="l"><b>L23</b> <code>public Encabezado(Runnable alCerrar) {</code>. <code>Runnable</code> es una interfaz de
Java con un único método, <code>run()</code>, sin parámetros y sin resultado: representa «una acción». Al pedir un
<code>Runnable</code>, el encabezado no decide qué pasa al cerrar; lo decide quien lo crea. <code>PantallaBase</code>
le pasará <code>navegacion::salir</code> (una referencia a método, capítulo 25), y en una prueba podrías pasarle
<code>() -&gt; { }</code>, una acción que no hace nada. Así el encabezado no depende de la navegación: bajo
acoplamiento (capítulo 27).</p>
<p class="l"><b>L24</b> <code>super(null);</code> llama al constructor <code>JPanel(LayoutManager)</code> con
<code>null</code>: «este panel <b>no tiene layout</b>». Sin layout, nadie colocará al botón por nosotros; lo haremos en
<code>doLayout()</code>. Lo explica el comentario de la misma línea. ¿Por qué no un layout normal? Porque el encabezado
tiene un solo hijo y su posición es una cuenta sencilla (pegado a la derecha, centrado en vertical); con un layout
habría que pelear con bordes y alineaciones para conseguir lo mismo.</p>
<p class="l"><b>L25</b> <code>setOpaque(false);</code> la caja es translúcida y tiene márgenes: que Swing pinte el fondo
de la pantalla detrás.</p>
<p class="l"><b>L26</b> <code>setPreferredSize(new Dimension(0, ALTO));</code> el tamaño que el encabezado «prefiere»:
0 de ancho y 96 de alto. El ancho da igual: en el norte de un <code>BorderLayout</code> (así lo pondrá
<code>PantallaBase</code>) el componente se estira a todo el ancho de la pantalla y solo se respeta su alto
preferido. Por eso el comentario dice que el ancho lo decide el <code>BorderLayout</code>.</p>
<p class="l"><b>L27</b> En blanco.</p>
"""),
             ("botonCerrar = BotonNeon.icono", r"""
<p class="l"><b>L28</b> <code>botonCerrar = BotonNeon.icono(Iconos.CERRAR, Tema.ROSA);</code> crea el botón cuadrado
de 58 × 58 con la X rosa (fábrica del capítulo 44) y lo guarda en el atributo.</p>
<p class="l"><b>L29</b> <code>setToolTipText("Cerrar el juego");</code> el globito de ayuda que aparece si dejas el
ratón quieto encima de la X. Un botón con solo un icono lo necesita: no todo el mundo adivina qué hace una X.</p>
<p class="l"><b>L30</b> <code>botonCerrar.addActionListener(e -&gt; alCerrar.run());</code> cuando se pulse el botón,
se ejecutará la acción recibida. <code>e -&gt; …</code> es una lambda (capítulo 25) que implementa
<code>ActionListener</code>: <code>e</code> es el evento del clic, que aquí no usamos. Dentro, <code>alCerrar.run()</code>
«ejecuta la acción». La lambda puede usar el parámetro <code>alCerrar</code> aunque el constructor ya haya terminado
cuando llegue el clic: Java lo guarda junto con la lambda (lo «captura»).</p>
<p class="l"><b>L31</b> <code>add(botonCerrar);</code> agrega el botón como hijo del panel. Sin esta línea el botón
existiría en memoria pero nunca aparecería en pantalla ni recibiría clics.</p>
<p class="l"><b>L32–L33</b> Cierra el constructor; línea en blanco.</p>
"""),
             ("public void doLayout()", r"""
<p class="l"><b>L34–L35</b> <code>@Override public void doLayout()</code>. Swing llama a <code>doLayout()</code> de un
contenedor cuando tiene que colocar a sus hijos: al mostrarse por primera vez y cada vez que cambia de tamaño. La
versión heredada se lo pide al layout; como no tenemos, no haría nada. La reemplazamos para colocar el botón
nosotros. La ventaja frente a poner la posición fija en el constructor: aquí <code>getWidth()</code> ya tiene el ancho
real, y si la ventana cambiara de ancho, el botón seguiría pegado a la derecha.</p>
<p class="l"><b>L36–L37</b> <code>botonCerrar.setBounds(x, y, ancho, alto)</code> coloca y dimensiona al hijo de una
vez, en coordenadas del encabezado. La x es <code>getWidth() - MARGEN - LADO_BOTON - 6</code>: desde el borde derecho
se retrocede el margen del halo, el lado del botón y 6 píxeles más de ajuste óptico para que no quede pegado al borde de
la caja. La y es <code>(getHeight() - LADO_BOTON) / 2</code>: centrado en vertical. Con un encabezado de 640 × 96: x =
640 − 10 − 58 − 6 = <b>566</b>, y = (96 − 58) ÷ 2 = <b>19</b>.</p>
<p class="l"><b>L38–L39</b> Cierra el método; línea en blanco.</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L40–L41</b> Sobrescribimos el dibujo del panel.</p>
<p class="l"><b>L42</b> El pincel preparado.</p>
<p class="l"><b>L43</b> <code>int ancho = getWidth();</code> el ancho se usa cinco veces abajo; guardarlo en una
variable ahorra llamadas y hace las fórmulas más cortas.</p>
<p class="l"><b>L44</b> En blanco.</p>
"""),
             ("// Caja translucida", r"""
<p class="l"><b>L45</b> Comentario: caja translúcida con borde suave.</p>
<p class="l"><b>L46–L47</b> La caja: desde (10, 10), ancho total menos los dos márgenes, alto menos los dos márgenes,
esquinas con arco 26 (radio 13). En 640 × 96: 620 × 76.</p>
<p class="l"><b>L48–L49</b> Un degradado <b>vertical</b> (las dos x son 0): arriba, en y = 10, lavanda con alfa 22;
abajo, en y = 86, lavanda con alfa 8. La caja es un poco más clara arriba que abajo, como un cristal iluminado desde
arriba. Con alfas tan bajos apenas se nota, y esa es la idea: que se intuya la caja sin competir con el título.</p>
<p class="l"><b>L50</b> Rellena la caja con ese degradado.</p>
<p class="l"><b>L51</b> <code>Dibujo.trazoNeon(g2, caja, Tema.MORADO, 1.2f, 0.45f);</code> el borde: morado, fino (1.2)
y con intensidad 0.45, es decir, bastante apagado. La barra es un marco, no el protagonista; si brillara como los
botones, distraería.</p>
<p class="l"><b>L52</b> En blanco.</p>
"""),
             ("double ladoLogo", r"""
<p class="l"><b>L53</b> El logotipo será un cuadrado de 52 píxeles.</p>
<p class="l"><b>L54</b> <code>Iconos.LOGO.dibujar(...)</code> (capítulo 42) lo pinta con la esquina en x = MARGEN + 20 =
30 y centrado en vertical: (96 − 52) ÷ 2 = 22. Color lavanda.</p>
<p class="l"><b>L55</b> En blanco.</p>
"""),
             ("// Titulo:", r"""
<p class="l"><b>L56</b> Comentario: «Juego del » en blanco y «Totito» con degradado de rosa a cian.</p>
<p class="l"><b>L57</b> <code>g2.setFont(Tema.fuente(Font.BOLD, 36f));</code> letra negrita de 36 puntos para el
título.</p>
<p class="l"><b>L58</b> Las medidas de esa fuente.</p>
<p class="l"><b>L59–L60</b> El título se parte en dos cadenas porque cada parte se pinta distinto. Fíjate en el
<b>espacio al final</b> de <code>"Juego del "</code>: es el que separa «del» de «Totito». Si lo quitas, se lee
«Juego delTotito».</p>
<p class="l"><b>L61</b> <code>float anchoTitulo = fm.stringWidth(parte1) + fm.stringWidth(parte2);</code> el ancho del
título completo es la suma de las dos partes. <code>stringWidth</code> devuelve <code>int</code>; la suma se guarda en
un <code>float</code> (Java convierte de <code>int</code> a <code>float</code> sin pedir permiso porque no se pierde
nada importante).</p>
<p class="l"><b>L62</b> <code>float x = (ancho - anchoTitulo) / 2f;</code> donde empieza el título para quedar centrado
en la barra. El <code>2f</code> asegura una división con decimales. Se centra respecto al ancho <b>total</b>, no al
espacio entre el logo y la X: como el logotipo y el botón ocupan más o menos lo mismo a cada lado, el resultado se ve
centrado.</p>
<p class="l"><b>L63</b> <code>float base = MARGEN + 44;</code> la línea base del título, en y = 54. Es un valor fijo
porque el título no se centra en la barra: va en la parte de arriba y deja sitio al lema debajo.</p>
"""),
             ("Dibujo.textoNeon(g2, parte1", r"""
<p class="l"><b>L64</b> <code>Dibujo.textoNeon(g2, parte1, x, base, Tema.LAVANDA, Tema.TEXTO);</code> (capítulo 41)
escribe «Juego del » con un halo lavanda alrededor y relleno blanco. El último parámetro es de tipo
<code>Paint</code>: acepta un color liso o un degradado.</p>
<p class="l"><b>L65</b> <code>float x2 = x + fm.stringWidth(parte1);</code> la segunda parte empieza justo donde
termina la primera.</p>
<p class="l"><b>L66–L67</b> Escribe «Totito» con halo rosa y, como relleno, un <code>GradientPaint</code> horizontal
que va de rosa en <code>x2</code> a cian en <code>x2 + ancho de "Totito"</code>. Que el degradado empiece y termine
exactamente en los bordes de la palabra es lo que hace que la T sea completamente rosa y la o final completamente cian.
Si lo hicieras de 0 al ancho de la barra, la palabra solo mostraría un pedacito del degradado. Así se rellena
<b>texto</b> con degradado: se elige un <code>Paint</code> en vez de un <code>Color</code> y se escribe.</p>
<p class="l"><b>L68</b> En blanco.</p>
"""),
             ("// Lema con letras", r"""
<p class="l"><b>L69</b> Comentario: el lema, con letras separadas.</p>
<p class="l"><b>L70</b> <code>Tema.fuenteEspaciada(Font.BOLD, 10.5f, 0.28f)</code> (capítulo 40): negrita pequeña de
10.5 puntos con un espaciado extra entre letras (<i>tracking</i>) de 0.28 veces el tamaño de la letra. Las mayúsculas
pequeñas y separadas son un recurso clásico para los textos secundarios: se leen como un adorno ordenado.</p>
<p class="l"><b>L71</b> <code>fm = g2.getFontMetrics();</code> volvemos a pedir las medidas. Es imprescindible: el
<code>fm</code> anterior medía la letra de 36 puntos; si lo reutilizaras, el lema se centraría mal. Aquí se reutiliza
la variable (sin <code>FontMetrics</code> delante) porque ya existe.</p>
<p class="l"><b>L72</b> El texto del lema. Los dos espacios a cada lado de los puntos «•» separan mejor las tres
ideas.</p>
<p class="l"><b>L73</b> Color lavanda suave para el lema: menos contraste que el título, porque es menos importante
(jerarquía visual, capítulo 36).</p>
<p class="l"><b>L74</b> Lo escribe centrado (<code>(ancho - ancho del lema) / 2f</code>) con la línea base 24 píxeles
por debajo de la del título: y = 78. Aquí basta <code>drawString</code>: el lema no lleva halo.</p>
<p class="l"><b>L75</b> Libera la copia del pincel.</p>
<p class="l"><b>L76–L77</b> Cierran el método y la clase. El botón de cerrar no se pinta aquí: Swing lo pinta encima
después, con <code>paintChildren</code>.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<p>En el capítulo 55, <code>PantallaBase</code> hará <code>add(new Encabezado(navegacion::salir),
BorderLayout.NORTH)</code>. La ventana del Totito mide 640 de ancho, así que el <code>BorderLayout</code> le da al
encabezado <b>640 × 96</b>: todo el ancho y el alto que pidió. Entonces:</p>
<ol>
<li>Swing llama a <code>doLayout()</code>: el botón de cerrar queda en <b>(566, 19)</b> con 58 × 58. Su figura visible,
descontado su propio margen de 9, ocupa de x = 575 a 615 y de y = 28 a 68.</li>
<li>Swing llama a <code>paintComponent</code>. La caja va de (10, 10) a (630, 86).</li>
<li>El logotipo ocupa de (30, 22) a (82, 74).</li>
<li>Título (medido con Liberation Sans; en Windows con Segoe UI cambia unos píxeles): «Juego del » mide 178 y
«Totito» 100; total 278. Empieza en x = (640 − 278) ÷ 2 = <b>181</b>. «Totito» empieza en 181 + 178 = <b>359</b> y su
degradado va de rosa en 359 a cian en 459. Línea base en y = 54.</li>
<li>Lema: mide unos 410 píxeles con el espaciado; empieza en (640 − 410) ÷ 2 = <b>115</b>, con línea base en y =
78.</li>
<li>Swing pinta el botón de cerrar encima.</li>
<li>Cuando el usuario pulsa la X: el botón dispara su evento, la lambda llama a <code>alCerrar.run()</code> y eso
ejecuta <code>navegacion.salir()</code>, que cerrará el juego (capítulo 61).</li>
</ol>
<p>Si un día la ventana midiera 800 de ancho, solo cambiarían los números que dependen de <code>getWidth()</code>: la
caja llegaría a 790, el título empezaría en 261, el lema en 195 y el botón en 726. Nada está escrito para 640: todo
se calcula. Esa es la ventaja de colocar en <code>doLayout</code> y de medir en lugar de adivinar.</p>
<svg viewBox="0 0 640 96" width="100%">
<rect x="0" y="0" width="640" height="96" fill="#1C1740"/>
<rect x="10" y="10" width="620" height="76" rx="13" fill="none" stroke="#A05CFF" stroke-width="1.5"/>
<rect x="30" y="22" width="52" height="52" fill="none" stroke="#C8BCF6" stroke-dasharray="4 3"/>
<text x="56" y="52" fill="#C8BCF6" font-size="10" text-anchor="middle">logo</text>
<rect x="181" y="21" width="278" height="40" fill="none" stroke="#C8BCF6" stroke-dasharray="4 3"/>
<text x="270" y="50" fill="#FFFFFF" font-size="22" text-anchor="middle">Juego del</text>
<text x="409" y="50" fill="#FF3BD4" font-size="22" text-anchor="middle">Totito</text>
<line x1="181" y1="54" x2="459" y2="54" stroke="#2F84FF" stroke-width="1"/>
<text x="320" y="80" fill="#C8BCF6" font-size="9" text-anchor="middle">lema: x = 115, base y = 78</text>
<rect x="566" y="19" width="58" height="58" fill="none" stroke="#FF3BD4" stroke-dasharray="4 3"/>
<text x="595" y="52" fill="#FF3BD4" font-size="10" text-anchor="middle">(566,19)</text>
<text x="181" y="16" fill="#C8BCF6" font-size="9">x = 181</text>
<text x="462" y="58" fill="#2F84FF" font-size="9">base y = 54</text>
</svg>
<p>Las líneas punteadas son las cajas que acabamos de calcular; la azul es la línea base del título.</p>

<h2>Compila y prueba</h2>
<p><i>Run → Clean and Build Project</i> (Shift+F11) → <code>BUILD SUCCESS</code>. El encabezado aparecerá en pantalla
cuando exista <code>PantallaBase</code> y la <code>VistaPrevia</code> (capítulos 55 y 56).</p>
<p>Con la foto opcional del capítulo 43, cambia las dos líneas de <code>pieza</code> y del tamaño por:</p>
<pre class="java">        JComponent pieza = new Encabezado(() -&gt; { });
        int ancho = 640, alto = 96;</pre>
<p><code>() -&gt; { }</code> es un <code>Runnable</code> que no hace nada: para una foto no hace falta que la X cierre
algo. La línea <code>pieza.doLayout()</code> del programa es la que coloca el botón de cerrar; sin ella, el botón
quedaría en (0, 0) con tamaño 0 y no saldría en la foto. Ejecuta
<code>java -cp target\classes ..\pruebas-totito\FotoComponente.java</code> y abre la imagen: deberías ver la barra igual
que en las capturas.</p>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Síntoma</th><th>Causa</th><th>Solución</th></tr>
<tr><td>«DIVERSIÃ“N» o «CLÃSICO»</td><td>Archivo guardado o compilado sin UTF-8</td><td>Guardar como UTF-8;
<code>javac -encoding UTF-8</code></td></tr>
<tr><td>La X no aparece</td><td>Falta <code>add(botonCerrar)</code> o <code>doLayout</code> está mal escrito (sin
<code>@Override</code> no te avisaría)</td><td>Líneas 31 y 34–37</td></tr>
<tr><td>El título se ve «Juego delTotito»</td><td>Falta el espacio final de <code>"Juego del "</code></td><td>Línea
59</td></tr>
<tr><td>El lema sale descentrado</td><td>Falta volver a medir (<code>fm = g2.getFontMetrics()</code>)</td><td>Línea
71</td></tr>
<tr><td><code>cannot find symbol: variable LOGO</code></td><td>Falta el icono en <code>Iconos</code></td><td>Capítulo
42</td></tr>
</table>

<div class="caja git"><b>Git</b>
<pre class="ps">git status
git add src\Encabezado.java
git commit -m "Encabezado: barra superior"
git push</pre></div>

<h2>Resumen</h2>
<ul>
<li>El encabezado es un <code>JPanel</code> porque contiene un componente real: la X de cerrar.</li>
<li><code>super(null)</code> crea un panel sin layout; <code>doLayout()</code> sobrescrito coloca al hijo con
<code>setBounds</code> cada vez que cambia el tamaño.</li>
<li>En el norte de un <code>BorderLayout</code> solo cuenta el alto preferido; el ancho lo pone el layout.</li>
<li>Recibir un <code>Runnable</code> deja la decisión de «qué hacer» a quien crea el componente.</li>
<li>Un título en dos estilos se centra midiendo cada parte y sumando; la segunda empieza donde termina la
primera.</li>
<li>Para rellenar texto con degradado se usa un <code>GradientPaint</code> que empieza y termina en los bordes de la
palabra.</li>
<li>Cada vez que cambias de fuente hay que volver a pedir el <code>FontMetrics</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Barra común de una aplicación</b>: el logo de la empresa, el nombre del usuario conectado y un botón «Cerrar
sesión» en todas las ventanas de un sistema de inventario, con un <code>Runnable</code> para lo que haga ese
botón.</li>
<li><b>Layout a mano con <code>doLayout</code></b>: una insignia de notificaciones pegada a la esquina de un icono, o
un botón «×» dentro de un campo de búsqueda, que deben seguir en su sitio al cambiar el tamaño.</li>
<li><b>Títulos con dos tonos</b>: «Mi<b>Tienda</b>», «Total: <b>Q 250.00</b>»; se miden las partes, se suman y se
centra el conjunto.</li>
<li><b>Acciones como parámetro</b>: un diálogo de confirmación genérico que recibe un <code>Runnable</code> con lo que
debe hacer si el usuario dice «Sí».</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Calcula dónde quedaría el botón de cerrar si el encabezado midiera 500 × 96. Pista: línea 36.</li>
<li>Cambia en una copia el degradado de «Totito» para que vaya de 0 a <code>ancho</code> (todo el ancho de la barra)
y fotografíalo. ¿Qué colores se ven ahora en la palabra? Explica por qué.</li>
<li>En una copia, quita la línea 71 y fotografía el encabezado. Mide a ojo cuánto se desplazó el lema.</li>
<li>Haz que el lema diga solo «SIEMPRE UN CLÁSICO». ¿Hay que tocar algo más para que siga centrado? ¿Por qué no?</li>
<li>Reto: agrega a mano (en una copia) un segundo botón, <code>BotonNeon.icono(Iconos.CASA, Tema.AZUL)</code>, a la
izquierda de la X. ¿Qué tendrías que añadir al constructor y a <code>doLayout</code>?</li>
</ol></div>
""",
}
