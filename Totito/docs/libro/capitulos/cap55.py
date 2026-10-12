# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 55,
    "titulo": "PantallaBase.java: el molde de todas las pantallas",
    "antes": r"""
<p class="entrada">Las cinco pantallas del Totito comparten el mismo fondo morado con X y O gigantes, el mismo
encabezado arriba y la misma forma de colocar las cosas: una columna centrada. En este capítulo escribes una
<b>clase abstracta</b> que hace todo eso una sola vez, para que cada pantalla solo tenga que decir <i>qué</i> pone
y en qué orden.</p>

<h2>Por qué existe este archivo</h2>
<p>Mira las cuatro imágenes de diseño (capítulo 34): menú, instrucciones, configuración y victoria. Cambia el
centro, pero hay tres cosas que se repiten <b>idénticas</b> en todas:</p>
<ol>
<li>El <b>fondo</b>: un degradado de morado oscuro a casi negro, un resplandor violeta suave en el centro, dos X y
dos O enormes y desvaídas que asoman por los lados, y dos rejillas de puntitos.</li>
<li>El <b>encabezado</b> con el logotipo, «Juego del Totito», el lema y el botón de cerrar (ya lo construiste en
el capítulo 45).</li>
<li>La <b>distribución</b>: el contenido va en una columna, centrado en horizontal y, casi siempre, también en
vertical.</li>
</ol>
<p>Si cada pantalla pintara su fondo y pusiera su encabezado, tendrías cinco copias del mismo código. Con
<code>PantallaBase</code> eso se escribe una vez y cada pantalla <b>hereda</b> (capítulo 22). Pero nadie debería
crear una «pantalla base» a secas, porque una pantalla sin contenido no tiene sentido: por eso la clase es
<b>abstracta</b> (capítulo 24). Es un molde para hacer moldes.</p>
<p>Además, <code>PantallaBase</code> esconde la parte más delicada de Swing, los gestores de distribución
(<code>BorderLayout</code> y <code>BoxLayout</code>, capítulo 37), detrás de cuatro métodos con nombres en
español: <code>agregar</code>, <code>espacio</code>, <code>relleno</code> y <code>fila</code>. Con ellos, armar una
pantalla es casi como escribir una lista de arriba abajo.</p>
<figure><img src="capturas/2-instrucciones.png"><figcaption>El fondo que pinta PantallaBase se ve en todas las
pantallas: la X grande a la izquierda, la O arriba a la derecha y abajo a la izquierda, la X abajo a la derecha y
las rejillas de puntos en dos esquinas. El encabezado también lo pone PantallaBase.</figcaption></figure>

<h2>Qué vas a aprender</h2>
<ul>
<li>Qué es una clase <code>abstract</code> sin métodos abstractos y por qué tiene sentido.</li>
<li>Un constructor <code>protected</code>.</li>
<li><code>BorderLayout</code>: regiones <code>NORTH</code> y <code>CENTER</code>.</li>
<li><code>BoxLayout</code> en vertical y en horizontal, y los «rellenos invisibles» de la clase <code>Box</code>:
<i>rigid area</i>, <i>strut</i> y <i>glue</i>. Por qué usamos <i>rigid area</i> y no <i>strut</i> (con un
experimento).</li>
<li><code>BorderFactory.createEmptyBorder</code> como margen interior.</li>
<li>Métodos con número variable de argumentos (<code>JComponent... componentes</code>).</li>
<li>Una referencia a método (<code>navegacion::salir</code>) en un caso real.</li>
<li>El fondo: <code>GradientPaint</code>, <code>RadialGradientPaint</code>, <code>Path2D</code> y posiciones
proporcionales.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>NetBeans: <i>&lt;default package&gt;</i> → <i>New → Java Class…</i> → <code>PantallaBase</code> →
<i>Finish</i>. La palabra <code>abstract</code> la escribirás tú en el código.</li>
<li>Borra la plantilla y escribe el código.</li>
<li>Alternativa: <code>New-Item src\PantallaBase.java</code>.</li>
</ol>
<p>Necesitas <code>Navegacion</code> (capítulo 39), <code>Tema</code> (40), <code>Dibujo</code> (41) y
<code>Encabezado</code> (45).</p>
""",
    "archivos": [
        {"ruta": "src/PantallaBase.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.BorderLayout</code>: el gestor de distribución de las cinco regiones
(norte, sur, este, oeste y centro). Con él ponemos el encabezado arriba y el contenido debajo.</p>
<p class="l"><b>L2</b> <code>java.awt.Color</code>: para el arreglo de colores del resplandor.</p>
<p class="l"><b>L3</b> <code>java.awt.Dimension</code>: un par ancho × alto; lo piden los rellenos invisibles.</p>
<p class="l"><b>L4</b> <code>java.awt.GradientPaint</code>: el degradado lineal del fondo (de arriba abajo).</p>
<p class="l"><b>L5–L6</b> <code>Graphics</code> y <code>Graphics2D</code>: el pincel.</p>
<p class="l"><b>L7</b> <code>java.awt.RadialGradientPaint</code>: un degradado <b>circular</b>, que cambia de color
desde un centro hacia fuera. Es el resplandor violeta.</p>
"""),
             ("import java.awt.geom.Ellipse2D", r"""
<p class="l"><b>L8</b> <code>java.awt.geom.Ellipse2D</code>: las O del fondo y los puntitos.</p>
<p class="l"><b>L9</b> <code>java.awt.geom.Path2D</code>: un «camino» de líneas; con él se hacen las X del fondo.</p>
<p class="l"><b>L10</b> <code>java.awt.geom.Point2D</code>: un punto (x, y); lo pide el degradado radial para su
centro.</p>
"""),
             ("import javax.swing.BorderFactory", r"""
<p class="l"><b>L11</b> <code>javax.swing.BorderFactory</code>: una «fábrica» de bordes (capítulo 27, patrón
<i>Factory</i>): en vez de hacer <code>new</code> de una clase de borde concreta, se le pide el borde con un método
<code>static</code>. Usaremos un borde vacío como margen.</p>
<p class="l"><b>L12</b> <code>javax.swing.Box</code>: un contenedor con <code>BoxLayout</code> que, sobre todo,
trae métodos <code>static</code> para fabricar rellenos invisibles (espacios fijos y espacios elásticos).</p>
<p class="l"><b>L13</b> <code>javax.swing.BoxLayout</code>: el gestor que apila componentes en una columna o en una
fila.</p>
<p class="l"><b>L14</b> <code>javax.swing.JComponent</code>: el tipo de lo que se puede agregar.</p>
<p class="l"><b>L15</b> <code>javax.swing.JPanel</code>: <code>PantallaBase</code> es un panel, y el contenido y
las filas también.</p>
"""),
             ("public abstract class PantallaBase", r"""
<p class="l"><b>L17–L25</b> Comentario de la clase, con dos párrafos. El primero dice qué hace (fondo, encabezado,
columna). El segundo es un <b>manual de uso</b>: para crear una pantalla, heredar de esta clase y llamar a
<code>agregar</code>, <code>espacio</code> y <code>relleno</code> en el orden en que se quieren ver las cosas. Un
comentario así ahorra tiempo a quien llegue después (incluido tú dentro de seis meses).</p>
<p class="l"><b>L26</b> <code>public abstract class PantallaBase extends JPanel {</code>
<code>abstract</code> significa que <b>no se pueden crear objetos</b> de esta clase directamente:
<code>new PantallaBase(nav)</code> daría el error <i>PantallaBase is abstract; cannot be instantiated</i>. Solo
sirve como base de otras clases (<code>PantallaMenu extends PantallaBase</code>). Fíjate en que no tiene ningún
método abstracto (sin cuerpo): está completa. Se declara abstracta solo para dejar claro, y hacer cumplir, que
es un molde y no una pantalla. Hereda de <code>JPanel</code> porque es un contenedor: tendrá el encabezado y el
contenido como hijos.</p>
"""),
             ("private final JPanel contenido;", r"""
<p class="l"><b>L28</b> <code>private final JPanel contenido;</code> el panel central donde cada pantalla pone sus
cosas. Es <code>private</code>: las subclases no lo tocan directamente, solo a través de <code>agregar</code>,
<code>espacio</code> y <code>relleno</code>. Así nadie puede, por ejemplo, cambiarle el gestor de distribución por
error.</p>
"""),
             ("protected PantallaBase(Navegacion", r"""
<p class="l"><b>L30</b> <code>protected PantallaBase(Navegacion navegacion) {</code> el constructor.
<code>protected</code>: solo lo pueden llamar las subclases (con <code>super(navegacion)</code>) y las clases del
mismo paquete. Como la clase es abstracta, de todos modos nadie podría usarlo con <code>new</code>; el
<code>protected</code> lo deja escrito. Recibe la <code>Navegacion</code> (capítulo 39) porque el encabezado necesita
saber qué hacer al pulsar la X.</p>
<p class="l"><b>L31</b> <code>super(new BorderLayout());</code> construye la parte <code>JPanel</code> con un
<code>BorderLayout</code> como gestor. Recuerda (capítulo 37): <code>BorderLayout</code> reparte el panel en
<code>NORTH</code>, <code>SOUTH</code>, <code>EAST</code>, <code>WEST</code> y <code>CENTER</code>. Lo de
<code>NORTH</code> recibe todo el ancho y <b>su alto preferido</b>; lo de <code>CENTER</code> se queda con todo lo
que sobra. Exactamente lo que queremos: encabezado arriba con su alto justo y el resto para el contenido.</p>
<p class="l"><b>L32</b> <code>add(new Encabezado(navegacion::salir), BorderLayout.NORTH);</code> crea el
encabezado y lo pone arriba. El constructor de <code>Encabezado</code> pide un <code>Runnable</code> (qué hacer al
cerrar, capítulo 45); <code>navegacion::salir</code> es una <b>referencia a método</b> (capítulo 25): «un
<code>Runnable</code> cuyo <code>run()</code> llama a <code>navegacion.salir()</code>». Es lo mismo que escribir
<code>() -&gt; navegacion.salir()</code>, más corto. El encabezado mide 96 de alto (su <code>ALTO</code>), así que
ocupa la franja de y = 0 a y = 96.</p>
"""),
             ("contenido = new JPanel();", r"""
<p class="l"><b>L34</b> <code>contenido = new JPanel();</code> crea el panel central.</p>
<p class="l"><b>L35</b> <code>contenido.setOpaque(false);</code> transparente, para que se vea el fondo que pinta
<code>PantallaBase</code>. Sin esta línea, el centro de todas las pantallas sería un rectángulo gris liso.</p>
<p class="l"><b>L36</b> <code>contenido.setLayout(new BoxLayout(contenido, BoxLayout.Y_AXIS));</code> le pone un
<code>BoxLayout</code> vertical: los hijos se apilan de arriba abajo, cada uno en su propia «planta», en el orden en
que se agregan. Fíjate en que <code>BoxLayout</code> pide en su constructor <b>el mismo panel</b> al que se le pone:
un <code>BoxLayout</code> está atado a un único contenedor y no se puede compartir (si lo intentaras, saldría el
error <i>BoxLayout can't be shared</i>). <code>Y_AXIS</code> es el eje vertical; <code>X_AXIS</code> sería en
fila.</p>
<p class="l"><b>L37</b> <code>contenido.setBorder(BorderFactory.createEmptyBorder(0, 0, 10, 0));</code> un borde
<b>vacío</b>: no se ve, solo reserva espacio. Los cuatro números son arriba, izquierda, abajo y derecha (en ese
orden). Deja 10 píxeles libres abajo, para que lo último de la columna nunca toque el borde de la ventana.</p>
<p class="l"><b>L38</b> <code>add(contenido, BorderLayout.CENTER);</code> el contenido va al centro y ocupa todo
lo que dejó el encabezado: con la ventana de 640 × 690, un rectángulo de <b>640 × 594</b> que empieza en y = 96.</p>
"""),
             ("protected void agregar(", r"""
<p class="l"><b>L41</b> Comentario: agrega un componente centrado debajo del anterior.</p>
<p class="l"><b>L42</b> <code>protected void agregar(JComponent componente) {</code> el método que más usarán las
pantallas. <code>protected</code>: para las subclases. Recibe un <code>JComponent</code> (y no un
<code>Component</code> más general) porque <code>setAlignmentX</code> está definido en <code>JComponent</code>.</p>
<p class="l"><b>L43</b> <code>componente.setAlignmentX(CENTER_ALIGNMENT);</code> en un <code>BoxLayout</code>
vertical, cada componente se alinea en horizontal según su <i>alignmentX</i> (0 = izquierda, 0,5 = centro, 1 =
derecha). Si unos estuvieran a 0 y otros a 0,5, <code>BoxLayout</code> haría cosas raras (los alinearía entre sí
por esos puntos, no respecto a la ventana). Poniéndolos todos al centro, la columna queda centrada siempre. Así la
pantalla no tiene que acordarse de hacerlo.</p>
<p class="l"><b>L44</b> <code>contenido.add(componente);</code> lo mete en la columna, debajo del último que se
agregó.</p>
"""),
             ("protected void espacio(", r"""
<p class="l"><b>L47</b> Comentario: separación vertical fija.</p>
<p class="l"><b>L48</b> <code>protected void espacio(int alto) {</code> deja un hueco de <code>alto</code> píxeles
en la columna.</p>
<p class="l"><b>L49</b> <code>contenido.add(Box.createRigidArea(new Dimension(0, alto)));</code>
<code>Box.createRigidArea</code> fabrica un componente <b>invisible y rígido</b>: su tamaño mínimo, preferido y
máximo son el mismo, 0 de ancho × <code>alto</code> de alto. No dibuja nada; solo ocupa sitio. ¿Por qué no usar
<code>Box.createVerticalStrut(alto)</code>, que parece hecho justo para esto? Lo verás con un experimento en «Cómo
funciona por dentro»: el <i>strut</i> tiene un ancho máximo <b>ilimitado</b>, y eso puede hacer que el contenedor
que lo tiene se estire a lo ancho. La <i>rigid area</i> de ancho 0 no tiene ese efecto secundario. La propia
documentación de Java recomienda <i>rigid areas</i> en lugar de <i>struts</i>.</p>
"""),
             ("protected void relleno()", r"""
<p class="l"><b>L52</b> Comentario: espacio elástico; uno al principio y otro al final centran todo en
vertical.</p>
<p class="l"><b>L53</b> <code>protected void relleno() {</code> agrega un relleno elástico.</p>
<p class="l"><b>L54</b> <code>contenido.add(Box.createVerticalGlue());</code> el <i>glue</i> («pegamento») es un
componente invisible de tamaño preferido 0, pero que <b>se puede estirar</b> en vertical sin límite (su alto máximo
es enorme). Cuando a la columna le sobra espacio, <code>BoxLayout</code> se lo da a los componentes que pueden
crecer; los nuestros tienen tamaño fijo (capítulo 41), así que el sobrante se lo llevan los <i>glue</i>, a partes
iguales. Con uno antes y otro después del contenido, el contenido queda en el medio. Con uno solo arriba, el
contenido se iría abajo; sin ninguno, se quedaría pegado arriba.</p>
"""),
             ("protected static JPanel fila(", r"""
<p class="l"><b>L57</b> Comentario: pone varios componentes uno al lado del otro.</p>
<p class="l"><b>L58</b> <code>protected static JPanel fila(int hueco, JComponent... componentes) {</code> tres
cosas nuevas. <code>static</code>: no usa nada del objeto (ni <code>contenido</code> ni el fondo), solo fabrica un
panel y lo devuelve; la pantalla decide dónde ponerlo, normalmente con <code>agregar(fila(...))</code>. Devuelve un
<code>JPanel</code>. Y <code>JComponent... componentes</code> (con tres puntos) es un parámetro de <b>número
variable de argumentos</b> (<i>varargs</i>): se puede llamar con dos componentes, con tres o con los que sea:
<code>fila(8, jugador1, jugador2)</code>. Dentro del método, <code>componentes</code> es un arreglo normal
(<code>JComponent[]</code>). Solo puede haber uno así y tiene que ser el último parámetro.</p>
<p class="l"><b>L59</b> <code>JPanel fila = new JPanel();</code> el panel de la fila. Que la variable se llame igual
que el método no es un problema: Java distingue variables y métodos.</p>
<p class="l"><b>L60</b> Transparente, para que se vea el fondo.</p>
"""),
             ("fila.setLayout", r"""
<p class="l"><b>L61</b> <code>fila.setLayout(new BoxLayout(fila, BoxLayout.X_AXIS));</code> un
<code>BoxLayout</code> <b>horizontal</b>: los hijos se ponen de izquierda a derecha.</p>
<p class="l"><b>L62</b> <code>for (int i = 0; i &lt; componentes.length; i++) {</code> recorre los componentes
recibidos. Se usa un <code>for</code> con índice (y no un <i>for-each</i>) porque hace falta saber si es el primero.</p>
<p class="l"><b>L63–L65</b> <code>if (i &gt; 0)</code>: antes de cada componente <b>menos el primero</b>, un hueco
rígido de <code>hueco</code> píxeles de ancho y 0 de alto. Así los huecos quedan solo <b>entre</b> componentes: con
dos componentes, un hueco; con tres, dos. Si pusieras el hueco después de cada uno, sobraría uno al final y la fila
quedaría descentrada.</p>
<p class="l"><b>L66</b> Agrega el componente.</p>
<p class="l"><b>L68</b> <code>fila.setMaximumSize(fila.getPreferredSize());</code> fija el tamaño máximo de la fila
igual a su tamaño preferido: la fila no se dejará estirar. Con las tarjetas de 290 de ancho y 8 de hueco, la fila
prefiere 588 × 150 y se queda en eso. Con nuestros componentes de tamaño fijo no se estiraría de todos modos, pero
esta línea protege el día que metas en una fila algo que sí se estira: por ejemplo, un <code>JTextField</code> normal
tiene un tamaño máximo prácticamente infinito, y sin esta línea la fila entera ocuparía todo el ancho y alto
disponibles en la columna.</p>
<p class="l"><b>L69</b> Devuelve la fila ya armada.</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L72–L73</b> <code>paintComponent</code>: el fondo. No llama a <code>super.paintComponent</code>
porque vamos a cubrir cada píxel nosotros. <code>PantallaBase</code> sigue siendo <b>opaca</b> (un
<code>JPanel</code> lo es por defecto), y está bien: le promete a Swing que pintará todo su rectángulo, y lo
cumple.</p>
<p class="l"><b>L74</b> Copia suavizada del pincel.</p>
<p class="l"><b>L75–L76</b> El ancho y el alto reales (640 × 690 en la ventana del juego). Se guardan en variables
porque se usan muchas veces. Ojo: es el tamaño de toda la pantalla, encabezado incluido; el fondo se ve también
detrás del encabezado, que es translúcido.</p>
"""),
             ("g2.setPaint(new GradientPaint", r"""
<p class="l"><b>L78</b> <code>g2.setPaint(new GradientPaint(0, 0, Tema.FONDO_ARRIBA, 0, alto, Tema.FONDO_ABAJO));</code>
un degradado vertical: en (0, 0) el morado oscuro <code>#1C1740</code> y en (0, 690) el casi negro
<code>#0E0B24</code>. Como las dos x son 0, solo cambia de arriba abajo.</p>
<p class="l"><b>L79</b> <code>g2.fillRect(0, 0, ancho, alto);</code> rellena toda la pantalla con ese degradado.</p>
<p class="l"><b>L80</b> Comentario: resplandor morado en el centro.</p>
<p class="l"><b>L81</b> <code>new RadialGradientPaint(new Point2D.Float(ancho / 2f, alto * 0.55f), ancho * 0.65f, ...)</code>
crea un degradado circular con centro en (320, 379,5), un poco por debajo de la mitad (donde suele estar el
contenido), y radio 640 × 0,65 = <b>416</b>. <code>Point2D.Float</code> es un punto con coordenadas
<code>float</code>.</p>
<p class="l"><b>L82</b> <code>new float[]{0f, 1f}</code>: las <b>paradas</b> del degradado, en fracciones del
radio: 0 = el centro y 1 = el borde del círculo. Deben ir de menor a mayor.</p>
<p class="l"><b>L83</b> <code>new Color[]{Tema.conAlfa(Tema.MORADO, 40), Tema.conAlfa(Tema.MORADO, 0)}</code>: el
color de cada parada. En el centro, morado con alfa 40 (muy tenue); en el borde, morado con alfa 0 (invisible).
Entre medias, Java va mezclando. Pasado el radio, se usa el último color (invisible).</p>
<p class="l"><b>L84</b> Rellena otra vez toda la pantalla, ahora con el resplandor. Como sus colores son
transparentes, se <b>suma</b> encima del degradado anterior: el centro queda un poco más violeta y los bordes
igual.</p>
"""),
             ("// Adornos:", r"""
<p class="l"><b>L86</b> Comentario: los adornos del fondo.</p>
<p class="l"><b>L87</b> <code>g2.setColor(Tema.DECORACION);</code> un morado <code>#5B35C2</code> con alfa 70:
visible, pero apagado, para que no compita con el contenido.</p>
<p class="l"><b>L88</b> <code>g2.setStroke(Dibujo.redondo(20f));</code> trazo grueso de 20 píxeles con puntas
redondas: las X y las O del fondo son «gordas», como en el diseño.</p>
"""),
             ("g2.draw(equis(ancho * 0.07", r"""
<p class="l"><b>L89</b> <code>g2.draw(equis(ancho * 0.07, alto * 0.5, 100));</code> una X de 100 píxeles con
centro en (44,8; 345): a la izquierda, a media altura. Sus brazos van de x = −5,2 a 94,8, así que asoma cortada por
el borde izquierdo, como en el diseño. Las posiciones son <b>proporciones</b> del tamaño (7&nbsp;% del ancho, 50&nbsp;%
del alto) y no píxeles fijos: si la ventana cambiara de tamaño, los adornos se recolocarían solos.</p>
<p class="l"><b>L90</b> Una O de 120 de diámetro con centro en (601,6; 248,4): arriba a la derecha. El rectángulo
envolvente empieza en centro − 60, por eso se resta 60 a cada coordenada. Llega hasta x = 661,6 y el borde derecho
la corta.</p>
<p class="l"><b>L91</b> Una O de 112 con centro en (44,8; 565,8): abajo a la izquierda, también cortada.</p>
<p class="l"><b>L92</b> Una X de 90 con centro en (595,2; 496,8): abajo a la derecha.</p>
<p class="l"><b>L93</b> Rejilla de puntos arriba a la izquierda, empezando en (25,6; 151,8).</p>
<p class="l"><b>L94</b> Otra abajo a la derecha, en (563,2; 607,2).</p>
<p class="l"><b>L95</b> Libera la copia del pincel. Después de este método, Swing pinta los hijos encima: el
encabezado y el contenido. Por eso los adornos quedan <b>detrás</b> de todo.</p>
"""),
             ("private static Path2D equis", r"""
<p class="l"><b>L98</b> <code>private static Path2D equis(double cx, double cy, double tam) {</code> un ayudante
que <b>devuelve la forma</b> de una X (no la dibuja). <code>static</code> porque solo hace cuentas con lo que
recibe. Devolver la forma deja que quien la pide decida cómo pintarla (aquí, con el trazo de 20 y el color de
decoración).</p>
<p class="l"><b>L99</b> <code>double r = tam / 2;</code> la mitad del tamaño: cuánto se aleja cada punta del
centro.</p>
<p class="l"><b>L100</b> <code>Path2D equis = new Path2D.Double();</code> un camino vacío. Un <code>Path2D</code>
es como un dibujo hecho con un lápiz: se le dan órdenes de «mueve el lápiz» y «traza una línea».</p>
<p class="l"><b>L101</b> <code>moveTo(cx - r, cy - r)</code>: levanta el lápiz y lo pone en la esquina superior
izquierda, sin dibujar.</p>
<p class="l"><b>L102</b> <code>lineTo(cx + r, cy + r)</code>: traza hasta la esquina inferior derecha. Primera
diagonal.</p>
<p class="l"><b>L103</b> <code>moveTo(cx + r, cy - r)</code>: levanta el lápiz y va a la esquina superior
derecha.</p>
<p class="l"><b>L104</b> <code>lineTo(cx - r, cy + r)</code>: traza hasta la inferior izquierda. Segunda diagonal.
Dos trazos separados en un solo camino forman la X.</p>
<p class="l"><b>L105</b> Devuelve el camino. Si te suena, es porque <code>Dibujo.dibujarX</code> (capítulo 41)
hace lo mismo por dentro; la diferencia es que aquella lo dibuja con neón y esta solo devuelve la forma.</p>
"""),
             ("private static void pintarPuntos", r"""
<p class="l"><b>L108</b> <code>private static void pintarPuntos(Graphics2D g2, double x, double y) {</code> dibuja
una rejilla de 3 × 3 puntitos con su esquina en (x, y).</p>
<p class="l"><b>L109</b> Color lavanda con alfa 45: puntos muy discretos.</p>
<p class="l"><b>L110–L111</b> Dos bucles <code>for</code> anidados (capítulo 14): <code>fila</code> de 0 a 2 y,
para cada fila, <code>columna</code> de 0 a 2. En total, 3 × 3 = 9 vueltas. (Esta <code>fila</code> es una variable
local del bucle, nada que ver con el método <code>fila</code>.)</p>
<p class="l"><b>L112</b> Un círculo de 6 píxeles en (x + columna × 18, y + fila × 18): los puntos quedan a 18
píxeles uno de otro. La rejilla entera ocupa 36 + 6 = 42 píxeles de lado.</p>
<p class="l"><b>L113–L116</b> Cierran los bucles, el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>1. Cómo se reparte la ventana</h3>
<p>Veamos con números qué pasa cuando una pantalla usa este molde. El menú del capítulo 56 hace, en su constructor:
<code>super(navegacion)</code>, luego <code>relleno()</code>, <code>agregar(tarjeta)</code> y
<code>relleno()</code>, donde la tarjeta mide 440 × 360. Con la ventana de 640 × 690 (medidas comprobadas
dibujando la pantalla):</p>
<table class="tabla">
<tr><th>Pieza</th><th>Quién la coloca</th><th>Rectángulo (x, y, ancho × alto)</th></tr>
<tr><td>Encabezado</td><td><code>BorderLayout.NORTH</code></td><td>(0, 0) 640 × 96</td></tr>
<tr><td>contenido</td><td><code>BorderLayout.CENTER</code></td><td>(0, 96) 640 × 594</td></tr>
<tr><td>Relleno de arriba</td><td><code>BoxLayout</code> vertical</td><td>alto 112</td></tr>
<tr><td>Tarjeta del menú</td><td><code>BoxLayout</code>, centrada</td><td>(100, 208) 440 × 360</td></tr>
<tr><td>Relleno de abajo</td><td><code>BoxLayout</code></td><td>alto 112</td></tr>
<tr><td>Borde vacío</td><td><code>createEmptyBorder</code></td><td>los últimos 10 píxeles</td></tr>
</table>
<p>Las cuentas: al contenido le quedan 594 − 10 (borde) = 584 de alto. La tarjeta ocupa 360. Sobran 584 − 360 = 224,
que <code>BoxLayout</code> reparte entre los dos <i>glue</i>: 112 cada uno. Por eso la tarjeta empieza en 96 + 112 =
208. En horizontal, la tarjeta no se estira (su máximo es 440) y, con alineación al centro, queda en (640 − 440) / 2
= 100.</p>
<svg viewBox="0 0 640 690" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="640" height="690" fill="#1C1740"></rect>
<rect x="4" y="4" width="632" height="88" fill="none" stroke="#A05CFF" stroke-width="3"></rect>
<text x="20" y="56" fill="#C8BCF6" font-size="24">NORTH: Encabezado (640 × 96)</text>
<rect x="4" y="100" width="632" height="586" fill="none" stroke="#2F84FF" stroke-width="3" stroke-dasharray="10 6"></rect>
<text x="20" y="135" fill="#2F84FF" font-size="22">CENTER: contenido (BoxLayout vertical)</text>
<line x1="320" y1="150" x2="320" y2="200" stroke="#C8BCF6" stroke-width="3" stroke-dasharray="6 4"></line>
<text x="335" y="185" fill="#C8BCF6" font-size="22">relleno(): 112</text>
<rect x="100" y="208" width="440" height="360" rx="30" fill="none" stroke="#FF3BD4" stroke-width="4"></rect>
<text x="190" y="380" fill="#FF3BD4" font-size="26">agregar(tarjeta)</text>
<text x="230" y="415" fill="#FF3BD4" font-size="22">440 × 360</text>
<line x1="320" y1="574" x2="320" y2="672" stroke="#C8BCF6" stroke-width="3" stroke-dasharray="6 4"></line>
<text x="335" y="630" fill="#C8BCF6" font-size="22">relleno(): 112</text>
<text x="335" y="672" fill="#C8BCF6" font-size="18">borde vacío: 10</text>
</svg>

<h3>2. El experimento: rigid area contra strut</h3>
<p>Para comprobar por qué <code>espacio()</code> usa <code>createRigidArea</code>, se dibujó el menú (en el
servidor donde se probó este libro) cambiando, dentro de la tarjeta, el separador
<code>Box.createRigidArea(new Dimension(0, 14))</code> por <code>Box.createVerticalStrut(14)</code>. Estos son los
tamaños máximos que informa Java:</p>
<table class="tabla">
<tr><th>Relleno</th><th>Tamaño máximo</th></tr>
<tr><td><code>Box.createRigidArea(new Dimension(0, 14))</code></td><td>0 × 14</td></tr>
<tr><td><code>Box.createVerticalStrut(14)</code></td><td><b>32767</b> × 14</td></tr>
<tr><td><code>Box.createVerticalGlue()</code></td><td>0 × 32767</td></tr>
</table>
<p>Un <code>BoxLayout</code> vertical calcula el ancho máximo de su panel como el mayor ancho máximo de sus hijos.
Con <i>rigid areas</i>, el mayor es el de los botones (384) más los márgenes: la tarjeta no puede pasar de 440. Con
el <i>strut</i>, el mayor es 32767: la tarjeta «se deja» estirar, y el <code>BoxLayout</code> de la columna la estiró
hasta <b>640</b>, todo el ancho de la ventana, con su borde de neón pegado a los lados. Los botones seguían en su
sitio, pero la caja de cristal ya no se parecía al diseño. Un relleno «invisible» cambió el aspecto de algo
visible: por eso aquí se usan siempre <i>rigid areas</i>.</p>

<h3>3. ¿Por qué una clase abstracta y no una interfaz?</h3>
<p>Una interfaz (como <code>Navegacion</code>) solo dice <b>qué métodos</b> debe tener una clase; no puede guardar
campos como <code>contenido</code> ni pintar un fondo ni tener constructor. <code>PantallaBase</code> sí necesita
todo eso: estado (el panel central), código compartido (fondo, ayudantes) y un constructor que arma el esqueleto.
Cuando lo que se comparte es <b>código y estado</b>, se usa una clase base; cuando es solo un <b>contrato</b>, una
interfaz (capítulo 24).</p>

<h2>Compila y prueba</h2>
<p><i>Run → Clean and Build Project</i> → <code>BUILD SUCCESS</code>. <code>PantallaBase</code> no se puede ver
sola (es abstracta); la verás en el próximo capítulo, que es <b>el momento en que todo lo que llevas construido
aparece por primera vez en pantalla</b>.</p>
<table class="tabla">
<tr><th>Problema</th><th>Causa y solución</th></tr>
<tr><td><i>PantallaBase is abstract; cannot be instantiated</i></td><td>Intentaste hacer
<code>new PantallaBase(...)</code>. Crea una subclase (como <code>PantallaMenu</code>).</td></tr>
<tr><td><i>constructor Encabezado in class Encabezado cannot be applied to given types</i></td><td>Tu
<code>Encabezado</code> no recibe un <code>Runnable</code>; revisa el capítulo 45.</td></tr>
<tr><td><i>BoxLayout can't be shared</i> (al ejecutar)</td><td>Le pasaste a <code>new BoxLayout(...)</code> un panel
distinto del que lo usa: debe ser <code>new BoxLayout(contenido, ...)</code> para <code>contenido</code> y
<code>new BoxLayout(fila, ...)</code> para <code>fila</code>.</td></tr>
<tr><td><i>varargs parameter must be the last parameter</i></td><td>Pusiste <code>JComponent...</code> antes de
<code>int hueco</code>.</td></tr>
<tr><td>(al verlo) el centro de la pantalla sale gris</td><td>Falta <code>contenido.setOpaque(false)</code>.</td></tr>
</table>

<div class="caja git"><b>Git</b>
<pre class="ps">git add src\PantallaBase.java
git commit -m "PantallaBase: fondo, encabezado y columna"
git push</pre></div>

<h2>Resumen</h2>
<ul>
<li><code>PantallaBase</code> es abstracta: no se instancia; las pantallas heredan de ella.</li>
<li>Con <code>BorderLayout</code>, el encabezado va en <code>NORTH</code> (su alto preferido) y el contenido en
<code>CENTER</code> (el resto).</li>
<li>El contenido es un <code>BoxLayout</code> vertical transparente; <code>agregar</code> centra y apila.</li>
<li><code>espacio</code> usa <i>rigid areas</i> (tamaño fijo en todo sentido); los <i>struts</i> tienen un máximo
ilimitado que puede estirar al contenedor.</li>
<li><code>relleno</code> usa <i>glue</i>: dos <i>glue</i> alrededor del contenido lo centran en vertical.</li>
<li><code>fila</code> arma un <code>BoxLayout</code> horizontal con huecos solo entre componentes y fija su máximo.</li>
<li>El fondo: degradado lineal, resplandor radial y adornos en posiciones proporcionales.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Una base para todas las ventanas</b>: en un sistema de inventario, <code>VentanaBase</code> con el logotipo
de la empresa, el usuario conectado y la misma barra de abajo; cada ventana (productos, ventas, clientes) solo
agrega lo suyo.</li>
<li><b>Métodos con nombres de tu dominio</b>: esconder <code>BoxLayout</code> y compañía detrás de
<code>agregar</code>, <code>espacio</code> o <code>fila</code> hace que los formularios se escriban rápido y sin
errores, en cualquier aplicación de escritorio.</li>
<li><b>Fondos con identidad</b>: el degradado más un resplandor y unos adornos desvaídos sirven para la pantalla de
inicio de cualquier juego o aplicación (una calculadora neón, un reproductor de música).</li>
<li><b>Varargs</b>: métodos como <code>sumar(int... numeros)</code> o <code>enviarA(String... correos)</code>, que
aceptan cuantos valores haga falta.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Si la tarjeta del menú midiera 440 × 400, ¿cuánto mediría cada relleno y en qué y empezaría la tarjeta?</li>
<li>Cambia el borde vacío del contenido para que también deje 20 píxeles a izquierda y derecha. ¿Afecta al menú?
¿Por qué?</li>
<li>Agrega una tercera rejilla de puntos arriba a la derecha (por ejemplo, en el 85&nbsp;% del ancho y el 15&nbsp;%
del alto) y comprueba con la vista previa del capítulo 56 que no tapa el encabezado.</li>
<li>Escribe un método <code>protected void espacioElastico(int minimo)</code> que agregue un relleno que nunca sea
menor que <code>minimo</code>. Pista: <code>new Box.Filler(min, pref, max)</code> con tres <code>Dimension</code>.</li>
<li>Reto: <code>equis</code> repite lo que hace <code>Dibujo.dibujarX</code> por dentro. Propón un cambio en
<code>Dibujo</code> (por ejemplo, un método público <code>formaX</code> que devuelva el <code>Path2D</code>) para que
las dos clases lo compartan. ¿Qué otras clases tendrías que cambiar?</li>
</ol></div>
""",
}
