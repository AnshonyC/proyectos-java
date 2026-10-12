CAPITULO = {
    "numero": 46,
    "titulo": "Rotulo.java: títulos que se achican y secciones entre líneas",
    "antes": r"""
<p class="entrada">Los textos decorativos del Totito («Cómo jugar», «¡Ganó Luis!», «Turno de Ana», «— JUGADORES —»,
«Excelente jugada») no son etiquetas normales: llevan degradado, halo, a veces un icono o un subrayado, y las
secciones van entre dos líneas que se desvanecen. Todos salen de esta clase. Además, el título sabe <b>achicar su
letra</b> si el texto no cabe, para que un nombre largo nunca se salga de la tarjeta.</p>

<h2>Por qué existe este archivo</h2>
<p>Swing trae <code>JLabel</code> para mostrar texto, y en el capítulo 33 lo usaste. Pero un <code>JLabel</code> no
sabe pintar letras con degradado, ni con halo de neón, ni dibujar líneas a los lados. Hay dos familias de textos
decorativos en el diseño:</p>
<ul>
<li><b>Títulos</b>: grandes, con degradado de color y halo. Algunos con icono a la izquierda y subrayado («Cómo jugar»
en las instrucciones); otros solos («¡Ganó Luis!», «Turno de Ana»). Su texto puede <b>cambiar</b> durante el juego.</li>
<li><b>Secciones</b>: más pequeñas, en mayúsculas espaciadas y con una línea a cada lado que se desvanece hacia afuera
(«JUGADORES», «SÍMBOLOS», «MODO DE JUEGO»), a veces con un subtítulo debajo. Una variante, la <b>leyenda</b>, usa el
mismo dibujo con una frase normal («Excelente jugada»).</li>
</ul>
<figure><img src="capturas/3-configuracion.png"><figcaption>Tres secciones con sus líneas que se desvanecen; la de
«SÍMBOLOS» lleva subtítulo.</figcaption></figure>
<figure><img src="capturas/5-victoria.png"><figcaption>Un título («¡Ganó Luis!») y una leyenda («Excelente
jugada») entre líneas.</figcaption></figure>
<p>Las dos familias comparten mucho (centrar, halo, tamaño fijo, poder cambiar el texto), así que viven en una sola
clase con un tipo interno que decide cómo se pintan, igual que hiciste con <code>BotonNeon</code>.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>Heredar de <code>JComponent</code> (más ligero que <code>JPanel</code>) cuando el componente no tiene hijos.</li>
<li>Tres métodos de fábrica (<code>titulo</code>, <code>seccion</code>, <code>leyenda</code>) sobre un constructor
privado, y por qué una fábrica puede tocar atributos privados.</li>
<li><b>Métodos fluidos</b>: métodos que devuelven <code>this</code> para poder encadenarlos.</li>
<li>Cambiar el contenido de un componente y pedir <code>repaint()</code>; sobrecarga de <code>setTexto</code>.</li>
<li>Un bucle <code>while</code> que <b>achica la letra</b> hasta que el texto quepa, y la trampa de
<code>deriveFont</code>.</li>
<li>Líneas que se desvanecen con <code>GradientPaint</code> y el color «transparente del mismo tono».</li>
<li><code>Math.min</code> para poner un tope que se adapta al espacio.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>En la rama <code>interfaz-neon</code>: clic derecho en <i>&lt;default package&gt;</i> → <i>New → Java Class…</i>
→ <code>Rotulo</code> (sin tilde: los nombres de clase deben ser solo letras inglesas, números y <code>_</code> para
evitar problemas con archivos y herramientas) → <i>Finish</i>.</li>
<li>Reemplaza el esqueleto por el código.</li>
</ol>
<pre class="ps">New-Item -ItemType File src\Rotulo.java
notepad src\Rotulo.java</pre>
""",
    "archivos": [
        {"ruta": "src/Rotulo.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.BasicStroke</code>: el trazo de las líneas a los lados de las secciones.</p>
<p class="l"><b>L2</b> <code>java.awt.Color</code>: los colores del degradado, del icono y del subrayado.</p>
<p class="l"><b>L3</b> <code>java.awt.Font</code>: este componente guarda su propia fuente y la achica si hace
falta.</p>
<p class="l"><b>L4</b> <code>java.awt.FontMetrics</code>: medir el texto para centrarlo y para saber si cabe.</p>
<p class="l"><b>L5</b> <code>java.awt.GradientPaint</code>: el degradado de las letras, del subrayado y de las líneas
que se desvanecen.</p>
"""),
             ("import java.awt.Graphics;", r"""
<p class="l"><b>L6–L7</b> <code>Graphics</code> y <code>Graphics2D</code>, el pincel.</p>
<p class="l"><b>L8</b> <code>java.awt.geom.Line2D</code>: segmentos de recta para el subrayado y las líneas
laterales.</p>
<p class="l"><b>L9</b> <code>javax.swing.JComponent</code>: la clase base de todos los componentes de Swing. La
elegimos en vez de <code>JPanel</code> porque el rótulo <b>no contiene</b> a otros componentes: solo dibuja. Un
<code>JComponent</code> es además transparente de serie (<code>isOpaque()</code> es <code>false</code>), así que no
hace falta llamar a <code>setOpaque(false)</code>, al contrario que con <code>JPanel</code>.</p>
<p class="l"><b>L10</b> En blanco.</p>
"""),
             ("public class Rotulo", r"""
<p class="l"><b>L11–L19</b> Comentario de documentación con las variantes. Aquí sí hay tildes y guiones largos
(«Cómo», «—») porque son ejemplos de lo que se verá en pantalla; como el archivo es UTF-8, no hay problema.</p>
<p class="l"><b>L20</b> <code>public class Rotulo extends JComponent {</code> declara la clase.</p>
<p class="l"><b>L21</b> En blanco.</p>
"""),
             ("private enum Tipo", r"""
<p class="l"><b>L22</b> <code>private enum Tipo { TITULO, SECCION }</code> un enum interno escrito en una línea (cuando
es tan corto, se puede). Es <code>private</code> porque nadie de fuera lo necesita: desde fuera se elige el tipo
llamando a la fábrica adecuada. Hay tres fábricas pero solo dos tipos, porque la leyenda se dibuja exactamente igual
que una sección; solo cambian la fuente y el alto.</p>
<p class="l"><b>L23</b> En blanco.</p>
"""),
             ("private final Tipo tipo;", r"""
<p class="l"><b>L24</b> <code>private final Tipo tipo;</code> título o sección; no cambia nunca.</p>
<p class="l"><b>L25</b> <code>private final Font fuente;</code> la fuente «ideal» del rótulo. Es <code>final</code>:
cuando el texto no cabe, no se modifica este atributo; se usa una copia más pequeña solo para ese dibujo (lo verás
en la línea 109). Así, si después el texto cambia por uno corto, vuelve a verse grande.</p>
<p class="l"><b>L26</b> <code>private String texto;</code> el texto. <b>No</b> es <code>final</code>, a diferencia de
lo que viste hasta ahora: el título de victoria cambia de «¡Ganó Ana!» a «¡Empate!» sin crear un rótulo nuevo.</p>
<p class="l"><b>L27</b> <code>private String subtitulo;</code> la línea pequeña bajo una sección. Si vale
<code>null</code>, no hay subtítulo.</p>
"""),
             ("private Color desde;", r"""
<p class="l"><b>L28–L29</b> <code>desde</code> y <code>hasta</code>: los dos colores del degradado de las letras. No
son <code>final</code> porque <code>setTexto</code> puede cambiarlos (el título de victoria es azul si ganó la O y rosa
si ganó la X).</p>
<p class="l"><b>L30–L31</b> El icono opcional a la izquierda del título y su color. Valen <code>null</code> mientras
nadie llame a <code>conIcono</code>.</p>
<p class="l"><b>L32–L33</b> Los dos colores del subrayado opcional. Si <code>subrayadoDesde</code> es
<code>null</code>, no hay subrayado.</p>
<p class="l"><b>L34</b> En blanco.</p>
<p class="l">Los atributos que no se asignan en el constructor empiezan valiendo <code>null</code>: Java pone ese valor
por defecto a todo atributo de tipo objeto. Por eso «sin icono» y «sin subrayado» no necesitan ninguna línea.</p>
"""),
             ("private Rotulo(Tipo tipo", r"""
<p class="l"><b>L35</b> El constructor, <b>privado</b> (como en <code>BotonNeon</code>): se crea con las fábricas.
Recibe lo común a todas las variantes: tipo, texto, fuente, colores y tamaño.</p>
<p class="l"><b>L36–L40</b> Guarda cada dato en su atributo con <code>this.atributo = parámetro</code>.</p>
<p class="l"><b>L41</b> Centrado horizontal dentro de un <code>BoxLayout</code> vertical.</p>
<p class="l"><b>L42</b> Tamaño fijo con <code>Dibujo.fijarTamano</code>: el rótulo ocupa siempre lo mismo, aunque el
texto cambie. Así, cuando «Turno de Ana» pasa a «Turno de Luis», nada de la pantalla se mueve.</p>
<p class="l"><b>L43–L44</b> Cierre y línea en blanco.</p>
"""),
             ("public static Rotulo titulo(", r"""
<p class="l"><b>L45</b> Comentario: título grande con degradado.</p>
<p class="l"><b>L46</b> Fábrica <code>titulo</code>: texto, tamaño de letra, dos colores, ancho y alto. Ejemplo real
(capítulo 60): <code>Rotulo.titulo("", 40f, Tema.CIAN, Tema.AZUL, 440, 54)</code>, que empieza vacío y recibe su texto
al terminar la partida.</p>
<p class="l"><b>L47</b> Crea el rótulo con tipo <code>TITULO</code> y fuente negrita del tamaño pedido.</p>
<p class="l"><b>L48–L49</b> Cierre y línea en blanco.</p>
"""),
             ("public static Rotulo seccion(", r"""
<p class="l"><b>L50</b> Comentario: sección en mayúsculas espaciadas; el subtítulo puede ser <code>null</code>.</p>
<p class="l"><b>L51</b> Fábrica <code>seccion</code>: solo pide texto, subtítulo y ancho. Todo lo demás lo fija el
diseño.</p>
<p class="l"><b>L52–L53</b> Crea un rótulo de tipo <code>SECCION</code> con negrita de 17 puntos espaciada 0.3, color
lavanda (desde y hasta iguales: sin degradado visible), y un alto que depende de si hay subtítulo:
<code>subtitulo == null ? 28 : 48</code>. Con subtítulo hacen falta 20 píxeles más para la segunda línea.</p>
<p class="l"><b>L54</b> <code>r.subtitulo = subtitulo;</code> guarda el subtítulo <b>después</b> de construir. ¿Cómo
puede un método tocar el atributo privado de otro objeto? Porque <code>private</code> significa «privado de esta
<b>clase</b>», no «de este objeto»: cualquier código escrito dentro de <code>Rotulo</code> puede acceder a los
atributos privados de cualquier <code>Rotulo</code>. Se hace así para no añadir al constructor un parámetro que solo
usa una de las tres fábricas.</p>
<p class="l"><b>L55</b> Devuelve el rótulo ya completo.</p>
<p class="l"><b>L56–L57</b> Cierre y línea en blanco.</p>
"""),
             ("public static Rotulo leyenda(", r"""
<p class="l"><b>L58</b> Comentario: una frase corta entre líneas, sin mayúsculas espaciadas.</p>
<p class="l"><b>L59</b> Fábrica <code>leyenda</code>: texto y ancho.</p>
<p class="l"><b>L60–L61</b> Tipo <code>SECCION</code> (mismo dibujo: texto centrado y líneas a los lados), pero con
negrita normal de 19 puntos y alto 32. Así «Excelente jugada» se lee como una frase y no como un encabezado.</p>
<p class="l"><b>L62–L63</b> Cierre y línea en blanco.</p>
"""),
             ("public Rotulo conIcono(", r"""
<p class="l"><b>L64</b> Comentario: agrega un icono a la izquierda del título.</p>
<p class="l"><b>L65</b> <code>public Rotulo conIcono(Iconos.Icono icono, Color color) {</code> fíjate en el tipo de
retorno: <code>Rotulo</code>. Este método no es estático; se llama sobre un rótulo ya creado.</p>
<p class="l"><b>L66–L67</b> Guarda el icono y su color.</p>
<p class="l"><b>L68</b> <code>return this;</code> devuelve <b>el mismo objeto</b> sobre el que se llamó. Eso permite
encadenar llamadas en una sola expresión, como hará <code>PantallaInstrucciones</code> (capítulo 57):
<code>Rotulo.titulo("Cómo jugar", 36f, Tema.TEXTO, Tema.LAVANDA, 400, 70).conIcono(Iconos.LIBRO,
Tema.ROSA).conSubrayado(Tema.ROSA, Tema.AZUL)</code>. Cada llamada recibe el rótulo, le añade algo y lo pasa a la
siguiente; al final, la expresión entera vale el rótulo completo. A esto se le llama <b>interfaz fluida</b>.</p>
<p class="l"><b>L69–L70</b> Cierre y línea en blanco.</p>
"""),
             ("public Rotulo conSubrayado(", r"""
<p class="l"><b>L71</b> Comentario: agrega un subrayado con degradado.</p>
<p class="l"><b>L72</b> Otro método fluido, con los dos colores del subrayado.</p>
<p class="l"><b>L73–L74</b> Los guarda.</p>
<p class="l"><b>L75</b> <code>return this;</code> para seguir encadenando.</p>
<p class="l"><b>L76–L77</b> Cierre y línea en blanco.</p>
<div class="caja concepto"><b>¿Por qué no más parámetros en <code>titulo(...)</code>?</b> Habría que pasar icono,
color del icono y dos colores de subrayado <b>siempre</b>, aunque fueran <code>null</code>:
<code>Rotulo.titulo("¡Empate!", 40f, a, b, 440, 54, null, null, null, null)</code>. Con los métodos fluidos, lo
opcional se añade solo cuando se quiere, y cada añadido tiene un nombre que dice lo que hace.</div>
"""),
             ("public void setTexto(String texto) {", r"""
<p class="l"><b>L78</b> <code>public void setTexto(String texto) {</code> cambia el texto después de creado el rótulo.
Lo usan la pantalla de juego («Turno de Ana» → «Turno de Luis») y la de victoria.</p>
<p class="l"><b>L79</b> Guarda el texto nuevo.</p>
<p class="l"><b>L80</b> <code>repaint();</code> pide a Swing que vuelva a pintar el rótulo. Es imprescindible: cambiar
el atributo no cambia la pantalla por sí solo. Y no pinta en el acto: deja anotado «este componente hay que
repintarlo» y Swing lo hace en cuanto termine lo que está haciendo (capítulo 37). Si lo olvidaras, verías el texto
viejo hasta que algo más forzara un repintado (por ejemplo, pasar el ratón por encima de otro componente).</p>
<p class="l"><b>L81–L82</b> Cierre y línea en blanco.</p>
"""),
             ("public void setTexto(String texto, Color desde", r"""
<p class="l"><b>L83</b> Una segunda versión de <code>setTexto</code> con dos parámetros más: sobrecarga (capítulo 16).
Java elige cuál llamar por el número y el tipo de los argumentos.</p>
<p class="l"><b>L84–L85</b> Cambia los colores del degradado. Ejemplo (capítulo 60):
<code>titulo.setTexto("¡Empate!", Tema.LAVANDA, Tema.MORADO)</code>.</p>
<p class="l"><b>L86</b> <code>setTexto(texto);</code> en lugar de repetir las dos líneas de antes, llama a la otra
versión, que guarda el texto y pide el repintado. Si mañana <code>setTexto</code> necesitara hacer algo más, se cambia
en un solo sitio.</p>
<p class="l"><b>L87–L88</b> Cierre y línea en blanco.</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L89–L90</b> Sobrescribimos <code>paintComponent</code>.</p>
<p class="l"><b>L91</b> El pincel preparado.</p>
<p class="l"><b>L92–L96</b> Según el tipo, delega en <code>pintarTitulo</code> o en <code>pintarSeccion</code>. Los dos
métodos reciben el mismo pincel. Separarlos mantiene cada uno corto y con una sola responsabilidad.</p>
<p class="l"><b>L97</b> Libera el pincel.</p>
<p class="l"><b>L98–L99</b> Cierre y línea en blanco.</p>
"""),
             ("private void pintarTitulo", r"""
<p class="l"><b>L100</b> Declara el método que pinta los títulos.</p>
<p class="l"><b>L101</b> <code>boolean conSubrayado = subrayadoDesde != null;</code> «¿tiene subrayado?» se calcula una
vez y se guarda con un nombre que se lee como una pregunta.</p>
<p class="l"><b>L102</b> <code>Font f = fuente;</code> una variable local que <b>empieza</b> apuntando a la fuente
ideal. Si hay que achicar, cambiaremos <code>f</code>, nunca el atributo.</p>
<p class="l"><b>L103–L104</b> Pone la fuente en el pincel y pide sus medidas.</p>
<p class="l"><b>L105</b> En blanco.</p>
"""),
             ("// Si no cabe", r"""
<p class="l"><b>L106</b> Comentario: si no cabe, se reduce la letra hasta que quepa.</p>
<p class="l"><b>L107</b> <code>double extraIcono = icono == null ? 0 : fm.getAscent() + 16;</code> cuánto espacio
ocupará el icono además del texto: el icono es casi tan alto como las letras (su <i>ascenso</i>, lo que suben desde la
línea base) más 16 de hueco. Sin icono, 0.</p>
<p class="l"><b>L108</b> <code>while (fm.stringWidth(texto) + extraIcono &gt; getWidth() - 20 &amp;&amp;
f.getSize2D() &gt; 12) {</code> repite mientras se cumplan <b>dos</b> condiciones: que el texto (más el icono) sea más
ancho que el componente menos 20 píxeles (10 de respiro a cada lado, para el halo), <b>y</b> que la letra siga siendo
mayor de 12 puntos. La segunda condición es un seguro. Piensa en un componente que todavía no tiene tamaño
(<code>getWidth()</code> vale 0 antes de que el layout lo coloque): el límite sería 0 − 20 = −20, ningún texto
«cabría» nunca, y sin el seguro la letra bajaría a 1, a 0, a tamaños negativos… un bucle infinito. Con el seguro, en
el peor caso se detiene en 12, una letra todavía legible. <code>getSize2D()</code> da el tamaño de la fuente como
<code>float</code>.</p>
<p class="l"><b>L109</b> <code>f = f.deriveFont(f.getSize2D() - 1);</code> crea una fuente igual pero un punto más
pequeña. Las fuentes no se modifican: <code>deriveFont</code> devuelve una nueva. <b>Trampa</b>:
<code>deriveFont</code> tiene una versión que recibe <code>float</code> (cambia el tamaño) y otra que recibe
<code>int</code> (¡cambia el estilo!). Aquí el argumento es <code>float</code>, porque <code>getSize2D()</code> lo es;
si escribieras <code>f.deriveFont(30)</code>, Java usaría la versión del estilo y obtendrías algo inesperado. Para
tamaños, escribe siempre <code>30f</code>.</p>
<p class="l"><b>L110–L111</b> Pone la fuente nueva en el pincel y vuelve a medir. Sin estas dos líneas, la
condición del <code>while</code> seguiría usando las medidas de la letra grande, el texto «nunca cabría» y el bucle
solo pararía por el seguro: el título saldría siempre a 12 puntos, diminuto, aunque cupiera a 38.</p>
<p class="l"><b>L112</b> El hueco del icono también depende del tamaño de letra, así que se recalcula.</p>
<p class="l"><b>L113–L114</b> Cierra el <code>while</code>; línea en blanco.</p>
"""),
             ("int anchoTexto = fm.stringWidth(texto);", r"""
<p class="l"><b>L115</b> El ancho del texto con la fuente definitiva.</p>
<p class="l"><b>L116</b> <code>tamIcono</code>: el lado del icono, un 5 % mayor que el ascenso de la letra (a la vista
queda del alto de las mayúsculas). 0 si no hay icono.</p>
<p class="l"><b>L117</b> El hueco entre icono y texto: 16 o 0.</p>
<p class="l"><b>L118</b> <code>double x = (getWidth() - (tamIcono + hueco + anchoTexto)) / 2;</code> la x donde empieza
el bloque icono + hueco + texto para que quede centrado, la misma idea que en <code>BotonNeon</code>.</p>
<p class="l"><b>L119</b> La línea base que centra el texto en vertical. Si hay subrayado, el centro se sube 6
píxeles (<code>conSubrayado ? 6 : 0</code>) para que el conjunto texto + raya quede equilibrado.</p>
<p class="l"><b>L120</b> En blanco.</p>
"""),
             ("if (icono != null) {", r"""
<p class="l"><b>L121–L123</b> Si hay icono, se dibuja a la izquierda. Su y es <code>base - fm.getAscent() * 0.95</code>:
desde la línea base se sube casi todo el ascenso, de modo que el icono queda a la altura de las letras.</p>
<p class="l"><b>L124</b> <code>xTexto</code>: donde empieza el texto, después del icono y del hueco. Se convierte a
<code>float</code> porque los métodos de texto lo piden así.</p>
<p class="l"><b>L125–L126</b> Escribe el texto con halo del color <code>desde</code> y relleno con un degradado
horizontal de <code>desde</code> a <code>hasta</code> que empieza y termina exactamente en los bordes del texto (lo
mismo que «Totito» en el encabezado).</p>
<p class="l"><b>L127</b> En blanco.</p>
"""),
             ("if (conSubrayado) {", r"""
<p class="l"><b>L128</b> Solo si hay subrayado…</p>
<p class="l"><b>L129</b> …la raya va 14 píxeles por debajo de la línea base (deja sitio a las letras que bajan, como
la «j» o la «g»).</p>
<p class="l"><b>L130</b> Su pintura es un degradado de <code>subrayadoDesde</code> a <code>subrayadoHasta</code> a lo
ancho del texto: en «Cómo jugar», de rosa a azul.</p>
<p class="l"><b>L131</b> Trazo de 3 píxeles con puntas redondeadas (<code>Dibujo.redondo</code>, capítulo 41): la raya
termina en semicírculos, más suave.</p>
<p class="l"><b>L132</b> La dibuja de <code>xTexto</code> a <code>xTexto + anchoTexto</code>: exactamente el ancho del
texto, sin incluir el icono.</p>
<p class="l"><b>L133–L135</b> Cierran el <code>if</code> y el método; línea en blanco.</p>
"""),
             ("private void pintarSeccion", r"""
<p class="l"><b>L136</b> El método que pinta secciones y leyendas.</p>
<p class="l"><b>L137–L138</b> Fuente del rótulo y sus medidas. Aquí no se achica: las secciones son cortas y sus
textos los escribe el programador, no el usuario.</p>
<p class="l"><b>L139</b> Ancho del texto.</p>
<p class="l"><b>L140</b> La x que lo centra.</p>
<p class="l"><b>L141</b> <code>float base = subtitulo == null ? Dibujo.lineaBaseCentrada(fm, getHeight() / 2f) : 21;</code>
sin subtítulo, el texto se centra en vertical; con subtítulo, se fija la línea base en 21 para dejar debajo el sitio
del subtítulo.</p>
<p class="l"><b>L142</b> Escribe el texto con halo morado y relleno <code>desde</code> (lavanda). Un <code>Color</code>
también es un <code>Paint</code>, así que sirve como relleno.</p>
<p class="l"><b>L143</b> En blanco.</p>
"""),
             ("// Lineas a los lados", r"""
<p class="l"><b>L144</b> Comentario: líneas a los lados que se desvanecen hacia afuera.</p>
<p class="l"><b>L145</b> <code>yLinea</code>: la altura de las líneas. Desde la línea base se sube un 35 % del ascenso,
más o menos la mitad de las mayúsculas: las líneas quedan a media altura del texto, no a la altura de su base.</p>
<p class="l"><b>L146</b> <code>separacion = 24</code>: el aire entre el texto y cada línea.</p>
<p class="l"><b>L147</b> Comentario: 140 píxeles, o menos si no caben.</p>
<p class="l"><b>L148</b> <code>float largo = Math.min(140, (getWidth() - anchoTexto) / 2f - separacion - 16);</code>
<code>Math.min(a, b)</code> devuelve el menor de los dos. El segundo valor es el espacio libre a un lado del texto,
menos la separación, menos 16 de respiro hasta el borde. Así la línea mide 140 si hay sitio, y si no, todo lo que
quepa. Es un tope que se adapta.</p>
<p class="l"><b>L149</b> <code>linea</code>: morado con alfa 170, el color en el extremo cercano al texto.</p>
<p class="l"><b>L150</b> <code>nada</code>: <b>el mismo morado</b> con alfa 0. ¿Por qué no un transparente cualquiera,
como <code>new Color(0, 0, 0, 0)</code>? Porque el degradado mezcla los cuatro canales por separado: de morado a
«negro transparente», a mitad de camino saldría un morado <i>oscurecido</i> y semitransparente, una línea sucia. Con
el mismo tono y alfa 0, solo cambia la transparencia y el color se mantiene limpio.</p>
<p class="l"><b>L151</b> Trazo de 1.6 píxeles.</p>
"""),
             ("float finIzquierda", r"""
<p class="l"><b>L152</b> <code>finIzquierda</code>: la línea izquierda termina 24 píxeles antes del texto.</p>
<p class="l"><b>L153</b> Su degradado va de <code>nada</code> (en el extremo de afuera, <code>finIzquierda - largo</code>)
a <code>linea</code> (junto al texto): aparece desde la nada a medida que se acerca al texto.</p>
<p class="l"><b>L154</b> Dibuja la línea horizontal izquierda a la altura <code>yLinea</code>.</p>
<p class="l"><b>L155</b> <code>inicioDerecha</code>: la línea derecha empieza 24 píxeles después del texto.</p>
<p class="l"><b>L156</b> El degradado al revés: <code>linea</code> junto al texto y <code>nada</code> afuera. Así las dos
líneas se desvanecen <b>hacia afuera</b>, simétricas.</p>
<p class="l"><b>L157</b> Dibuja la línea derecha.</p>
<p class="l"><b>L158</b> En blanco.</p>
"""),
             ("if (subtitulo != null) {", r"""
<p class="l"><b>L159</b> Si hay subtítulo…</p>
<p class="l"><b>L160–L161</b> …letra normal de 14 puntos y sus medidas (otra vez: fuente nueva, medidas nuevas).</p>
<p class="l"><b>L162</b> Color lavanda suave: es información secundaria.</p>
<p class="l"><b>L163</b> Lo escribe centrado, 22 píxeles por debajo de la línea base del título de sección.</p>
<p class="l"><b>L164–L166</b> Cierran el <code>if</code>, el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>Un nombre largo en la pantalla de victoria</h3>
<p>El campo de nombre admite hasta 14 caracteres (capítulo 47). Supón que Luis escribió «Maximiliano Ro» y ganó. La
pantalla de victoria tiene un título de 440 × 54 creado con letra de 40 y llamará a
<code>titulo.setTexto("¡Ganó Maximiliano Ro!", …)</code>. Al pintarse (medidas con Liberation Sans):</p>
<table class="tabla">
<tr><th>Vuelta</th><th>Tamaño</th><th>Ancho del texto</th><th>¿Cabe en 440 − 20 = 420?</th><th>Qué hace</th></tr>
<tr><td>antes del bucle</td><td>40</td><td>433</td><td>no</td><td>entra al <code>while</code></td></tr>
<tr><td>1</td><td>39</td><td>423</td><td>no</td><td>repite</td></tr>
<tr><td>2</td><td>38</td><td>412</td><td>sí</td><td>sale del <code>while</code></td></tr>
</table>
<p>Se pinta con letra de 38, empezando en x = (440 − 412) ÷ 2 = 14. El atributo <code>fuente</code> sigue siendo de
40: si en la siguiente partida gana «Ana», el título «¡Ganó Ana!» (más corto) se verá otra vez a 40 sin hacer nada.
Con «¡Ganó Luis!» (222 píxeles) el bucle ni siquiera entra.</p>
<h3>«Cómo jugar» con icono y subrayado</h3>
<p>En las instrucciones el título mide 400 × 70, letra de 36. Medido: el texto ocupa 200 píxeles y el ascenso es 33.
Icono: 33 × 1.05 = 34.7; hueco 16; bloque 250.7; empieza en x = (400 − 250.7) ÷ 2 = 74.7. El texto empieza en 74.7 +
50.7 = 125.3. Como hay subrayado, el centro sube a 35 − 6 = 29 y la línea base queda en 29 + (33 − 8) ÷ 2 = 41.5. El
libro se dibuja en y = 41.5 − 31.4 = 10.2 y la raya rosa → azul en y = 55.5, de x = 125.3 a 325.3.</p>
<h3>Las líneas de «JUGADORES» y de «Excelente jugada»</h3>
<table class="tabla">
<tr><th>Dato</th><th>«JUGADORES» (sección, 560 × 28)</th><th>«Excelente jugada» (leyenda, 440 × 32)</th></tr>
<tr><td>Ancho del texto</td><td>154 (108 sin el espaciado de letras)</td><td>155</td></tr>
<tr><td>x del texto</td><td>(560 − 154) ÷ 2 = 203</td><td>(440 − 155) ÷ 2 = 142.5</td></tr>
<tr><td>Línea base</td><td>14 + (16 − 4) ÷ 2 = 20</td><td>16 + (18 − 4) ÷ 2 = 23</td></tr>
<tr><td>Altura de las líneas</td><td>20 − 16 × 0.35 = 14.4</td><td>23 − 18 × 0.35 = 16.7</td></tr>
<tr><td>Espacio libre a un lado</td><td>203 − 24 − 16 = 163</td><td>142.5 − 24 − 16 = 102.5</td></tr>
<tr><td><code>largo</code> = mín(140, libre)</td><td><b>140</b> (sobra espacio)</td><td><b>102.5</b> (el tope se
adapta)</td></tr>
<tr><td>Línea izquierda</td><td>de 39 a 179</td><td>de 16 a 118.5</td></tr>
<tr><td>Línea derecha</td><td>de 381 a 521</td><td>de 321.5 a 424</td></tr>
</table>
<p>En la leyenda, sin <code>Math.min</code> las líneas medirían 140 y llegarían a x = −21 y x = 461: se saldrían del
componente y se cortarían a cuchillo, justo lo que queremos evitar. Con el tope terminan a 16 píxeles de cada borde.</p>

<h2>Compila y prueba</h2>
<p><i>Clean and Build</i> (Shift+F11) → <code>BUILD SUCCESS</code>. En <code>target\classes</code> verás
<code>Rotulo.class</code> y <code>Rotulo$Tipo.class</code> (el enum interno). Los rótulos aparecerán en pantalla a
partir del capítulo 56.</p>
<p>Con la foto opcional (capítulo 43) puedes comprobar el achicado:</p>
<pre class="java">        JComponent pieza = Rotulo.titulo("¡Ganó Maximiliano Ro!", 40f, Tema.CIAN, Tema.AZUL, 440, 54);
        int ancho = 440, alto = 54;</pre>
<p>Y una sección: <code>Rotulo.seccion("SÍMBOLOS", "Cada jugador elige su símbolo", 560)</code> con
<code>ancho = 560, alto = 48</code>. Como estas líneas llevan tildes, guarda el archivo en UTF-8 (el Bloc de notas lo
hace por defecto).</p>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Síntoma</th><th>Causa</th><th>Solución</th></tr>
<tr><td>Un título largo sale diminuto aunque cabría más grande</td><td>Falta volver a medir dentro del
<code>while</code> (líneas 110–111): la condición no cambia y solo para en 12</td><td>Pon <code>g2.setFont(f)</code> y
<code>fm = g2.getFontMetrics()</code> dentro del bucle</td></tr>
<tr><td>El programa se congela al mostrar un título</td><td>Quitaste el seguro <code>f.getSize2D() &gt; 12</code></td><td>Vuelve
a ponerlo en la línea 108</td></tr>
<tr><td>El título sale en cursiva o con otro estilo</td><td><code>deriveFont</code> con un <code>int</code></td><td>Usa
un <code>float</code>: <code>f.getSize2D() - 1</code> o <code>30f</code></td></tr>
<tr><td>El texto no cambia al llamar <code>setTexto</code></td><td>Falta <code>repaint()</code></td><td>Línea 80</td></tr>
<tr><td><code>cannot assign a value to final variable texto</code></td><td>Declaraste <code>texto</code> como
<code>final</code></td><td>Quita el <code>final</code> de la línea 26</td></tr>
<tr><td>Las líneas laterales se ven grisáceas a la mitad</td><td>Usaste un transparente negro en vez de
<code>conAlfa(MORADO, 0)</code></td><td>Línea 150</td></tr>
</table>

<div class="caja git"><b>Git</b>
<pre class="ps">git status
git add src\Rotulo.java
git commit -m "Rotulo: titulos y secciones decorativas"
git push</pre></div>

<h2>Resumen</h2>
<ul>
<li><code>Rotulo</code> hereda de <code>JComponent</code> porque solo dibuja; ya es transparente de serie.</li>
<li>Tres fábricas (<code>titulo</code>, <code>seccion</code>, <code>leyenda</code>) sobre un constructor privado; una
fábrica puede tocar atributos privados porque está dentro de la clase.</li>
<li>Los métodos fluidos devuelven <code>this</code> y permiten encadenar lo opcional:
<code>.conIcono(...).conSubrayado(...)</code>.</li>
<li><code>setTexto</code> cambia el contenido y llama a <code>repaint()</code>; la versión con colores reutiliza la
otra.</li>
<li>El título achica su letra de punto en punto con un <code>while</code>, sin tocar la fuente original y con un mínimo
de 12; <code>deriveFont</code> con <code>float</code> cambia el tamaño.</li>
<li>Las líneas laterales se desvanecen con un degradado del color a ese mismo color con alfa 0, y su largo se limita
con <code>Math.min</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Textos que deben caber</b>: el nombre de un producto en una etiqueta de precio, el nombre de un cliente en un
recibo o un título en una miniatura; el mismo bucle de achicar (con un mínimo) evita que se corten.</li>
<li><b>Interfaces fluidas</b> en tus propias clases: <code>new Pedido().conCliente("Ana").conProducto("Café",
2).conEnvio()</code>, o configurar un correo con <code>.para(...).asunto(...).cuerpo(...)</code>.</li>
<li><b>Separadores elegantes</b> entre secciones de un formulario o de un menú de restaurante: texto centrado con
líneas que se desvanecen.</li>
<li><b>Componentes que cambian de texto</b> (un reloj, un contador de puntos, un estado «Conectado/Desconectado»):
setter + <code>repaint()</code>, con tamaño fijo para que nada se mueva.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Con los datos de la tabla, ¿hasta qué tamaño se achicaría «¡Ganó Maximiliano Ro!» si el título midiera 400 de
ancho? Pista: debe caber en 380; a 37 mide 401, y cada punto menos ahorra unos 11 píxeles.</li>
<li>Explica con tus palabras qué pasaría si en la línea 109 escribieras <code>fuente = fuente.deriveFont(...)</code>
(y quitaras el <code>final</code>). Pista: piensa en la partida siguiente.</li>
<li>Fotografía <code>Rotulo.leyenda("Excelente jugada", 300)</code> con <code>ancho = 300, alto = 32</code>. Calcula
antes el largo de las líneas y compruébalo en la imagen.</li>
<li>Escribe la cadena fluida para un título «Configuración» con el icono <code>Iconos.PERSONAS</code> en azul y un
subrayado de azul a morado.</li>
<li>Reto: agrega en una copia un método fluido <code>conSombra()</code> que active un booleano, y piensa dónde lo
usarías dentro de <code>pintarTitulo</code>.</li>
</ol></div>
""",
}
