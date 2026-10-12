CAPITULO = {
    "numero": 44,
    "titulo": "BotonNeon.java: un botón de verdad, dibujado a mano",
    "antes": r"""
<p class="entrada">Todos los botones del Totito v1.0 salen de esta clase: los tres grandes del menú, las píldoras
de colores («Comenzar partida», «Menú principal»), las de solo borde («Volver», «Reiniciar») y la X cuadrada de
cerrar. Es el archivo más instructivo de la parte: heredas de <code>JButton</code> para no perder nada de lo que un
botón ya sabe hacer, y solo cambias cómo se ve.</p>

<h2>Por qué existe este archivo</h2>
<p>En el capítulo 33 usaste <code>JButton</code> tal cual: un rectángulo gris con texto negro. Funciona, pero no se
parece en nada al diseño. Repasa las capturas: hay cuatro <b>formas</b> de botón distintas, y cada una aparece varias
veces.</p>
<table class="tabla">
<tr><th>Estilo</th><th>Aspecto</th><th>Dónde aparece</th><th>Tamaño</th></tr>
<tr><td><code>MENU</code></td><td>ancho, icono a la izquierda, línea divisoria, texto y una flechita</td><td>Jugar,
Instrucciones, Salir</td><td>384 × 88</td></tr>
<tr><td><code>PILDORA</code></td><td>extremos redondos, relleno con degradado y reflejo</td><td>Comenzar partida, Menú
principal, Jugar de nuevo, Regresar</td><td>lo decide la pantalla (p. ej. 270 × 66)</td></tr>
<tr><td><code>CONTORNO</code></td><td>píldora oscura con borde morado</td><td>Volver, Reiniciar</td><td>lo decide la
pantalla</td></tr>
<tr><td><code>ICONO</code></td><td>cuadrado pequeño con un solo icono</td><td>la X de cerrar del encabezado</td><td>58
× 58</td></tr>
</table>
<figure><img src="capturas/4-juego.png"><figcaption>En la pantalla de juego conviven tres estilos: la X de cerrar
(ICONO), «Reiniciar» (CONTORNO) y «Menú principal» (PILDORA).</figcaption></figure>
<p>Podríamos haber hecho cuatro clases, una por estilo. Pero las cuatro comparten casi todo: el margen para el halo,
el borde de neón, el brillo al pasar el ratón, el oscurecido al apretar, el texto blanco en negrita. Lo que cambia es
el redondeo, el relleno y cómo se reparte el contenido. Por eso es <b>una</b> clase con un <code>enum</code> que dice
qué estilo es, y unos pocos <code>switch</code> e <code>if</code> que eligen lo que cambia.</p>
<p>¿Y por qué heredar de <code>JButton</code> en lugar de dibujar un rectángulo y escuchar clics a mano? Porque un
botón hace muchas cosas que no se ven: avisa a los <code>ActionListener</code> al soltar el clic, se puede activar con
la barra espaciadora cuando tiene el foco, sabe si el ratón está encima, si se está apretando, si está desactivado,
muestra un <i>tooltip</i>… Heredando lo conservamos todo y escribimos solo la parte visual.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>Heredar de un componente de Swing y <b>apagar</b> lo que pinta por defecto.</li>
<li>Un <b>constructor privado</b> y <b>métodos de fábrica</b> estáticos (<code>menu</code>, <code>pildora</code>,
<code>contorno</code>, <code>icono</code>): por qué se hace y qué ventajas tiene.</li>
<li>Un <code>enum</code> dentro de una clase.</li>
<li>El <b>modelo</b> del botón (<code>ButtonModel</code>): <i>rollover</i>, <i>armed</i> y <i>pressed</i>.</li>
<li>El <code>switch</code> de expresión con flechas <code>-&gt;</code> y el operador ternario <code>? :</code>.</li>
<li>Transparencia global con <code>AlphaComposite</code> y degradados con <code>GradientPaint</code>.</li>
<li>Cómo repartir el contenido de un botón con proporciones, medido con <code>FontMetrics</code>, con las cuentas en
píxeles del botón del menú.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>Asegúrate de estar en la rama <code>interfaz-neon</code> (<code>git branch</code>).</li>
<li>En NetBeans: clic derecho en <i>Source Packages → &lt;default package&gt;</i> → <i>New → Java Class…</i></li>
<li><i>Class Name</i>: <code>BotonNeon</code> (B y N mayúsculas, sin tilde ni espacios) → <i>Finish</i>.</li>
<li>Borra el esqueleto que genera NetBeans y escribe el código completo de abajo.</li>
</ol>
<p>Con PowerShell, desde la carpeta Totito:</p>
<pre class="ps">New-Item -ItemType File src\BotonNeon.java
notepad src\BotonNeon.java</pre>
<div class="caja concepto"><b>Dependencias</b> Este archivo usa <code>Tema</code> (capítulo 40), <code>Dibujo</code>
(capítulo 41) e <code>Iconos</code> (capítulo 42). En particular, necesita la interfaz <code>Iconos.Icono</code> y el
icono <code>Iconos.CHEVRON</code> (la flechita <code>›</code>).</div>
""",
    "archivos": [
        {"ruta": "src/BotonNeon.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.AlphaComposite</code>: la regla que decide cómo se mezcla lo que pintas con lo
que ya había. La usaremos para dibujar el botón entero al 40 % de opacidad cuando esté desactivado.</p>
<p class="l"><b>L2</b> <code>java.awt.BasicStroke</code>: el «trazo», es decir, el grosor y la forma de las puntas de
una línea. Lo necesitamos para la línea divisoria del botón del menú.</p>
<p class="l"><b>L3</b> <code>java.awt.Color</code>: colores con alfa, como en la tarjeta.</p>
<p class="l"><b>L4</b> <code>java.awt.Cursor</code>: la forma del puntero del ratón. Pondremos la manita sobre los
botones.</p>
<p class="l"><b>L5</b> <code>java.awt.Font</code>: una fuente con su familia, estilo y tamaño. Usaremos sus
constantes <code>Font.BOLD</code> (negrita).</p>
<p class="l"><b>L6</b> <code>java.awt.FontMetrics</code>: las «medidas» de una fuente: cuánto ocupa un texto a lo
ancho, cuánto sube y baja respecto de la línea base. Sin medir no se puede centrar.</p>
"""),
             ("import java.awt.GradientPaint", r"""
<p class="l"><b>L7</b> <code>java.awt.GradientPaint</code>: una «pintura» que pasa suavemente de un color a otro
entre dos puntos (degradado lineal, capítulo 37).</p>
<p class="l"><b>L8–L9</b> <code>Graphics</code> y <code>Graphics2D</code>: el pincel básico y el avanzado, como en
<code>Tarjeta</code>.</p>
<p class="l"><b>L10</b> <code>java.awt.geom.Line2D</code>: un segmento de recta con coordenadas decimales. Será la
línea divisoria.</p>
<p class="l"><b>L11</b> <code>java.awt.geom.RoundRectangle2D</code>: el rectángulo redondeado, la figura de todos los
botones.</p>
<p class="l"><b>L12</b> <code>javax.swing.JButton</code>: el botón de Swing, del que heredamos.</p>
<p class="l"><b>L13</b> En blanco. Fíjate en que <b>no</b> importamos <code>ButtonModel</code>, aunque lo usaremos:
solo hace falta importar una clase si escribes su nombre en el código, y nosotros llamaremos a
<code>getModel().isRollover()</code> sin nombrar nunca el tipo.</p>
"""),
             ("public class BotonNeon", r"""
<p class="l"><b>L14–L20</b> Comentario de documentación: es un <code>JButton</code> normal, se usa con
<code>addActionListener</code>, pero se dibuja a mano; y se crea con cuatro métodos de fábrica.</p>
<p class="l"><b>L21</b> <code>public class BotonNeon extends JButton {</code>: <code>BotonNeon</code> <b>es un</b>
<code>JButton</code> (capítulo 22). Cualquier código que espere un <code>JButton</code> acepta un
<code>BotonNeon</code>, y todo lo heredado funciona igual: <code>addActionListener</code>,
<code>setToolTipText</code>, <code>setEnabled</code>, el teclado…</p>
<p class="l"><b>L22</b> En blanco.</p>
"""),
             ("public enum Estilo", r"""
<p class="l"><b>L23</b> Comentario: estas son las formas de botón del diseño.</p>
<p class="l"><b>L24</b> <code>public enum Estilo {</code> declara un <b>enum</b> (capítulo 26): un tipo con una lista
cerrada de valores posibles. Está <b>dentro</b> de <code>BotonNeon</code>, así que su nombre completo es
<code>BotonNeon.Estilo</code>. Lo ponemos aquí porque solo tiene sentido para los botones. Se eligió un enum y no,
por ejemplo, un <code>int</code> (0 = menú, 1 = píldora…) porque con un enum es imposible pasar un estilo que no
existe, y el código se lee solo: <code>Estilo.MENU</code> dice más que <code>0</code>.</p>
<p class="l"><b>L25</b> Comentario dibujado: el botón del menú tiene icono, separador, texto y flechita. El carácter
<code>›</code> está en un comentario, así que no afecta al programa.</p>
<p class="l"><b>L26</b> <code>MENU,</code> primer valor. Los valores se separan con comas.</p>
"""),
             ("PILDORA,", r"""
<p class="l"><b>L27–L28</b> <code>PILDORA</code>: la píldora rellena con degradado.</p>
<p class="l"><b>L29–L30</b> <code>CONTORNO</code>: la píldora que solo tiene borde.</p>
<p class="l"><b>L31–L32</b> <code>ICONO</code>: el cuadrado con un solo icono. Es el último valor, por eso no lleva
coma.</p>
<p class="l"><b>L33–L34</b> Cierra el enum; línea en blanco.</p>
"""),
             ("private static final int MARGEN", r"""
<p class="l"><b>L35</b> Comentario: espacio alrededor de la forma para que el halo no se corte.</p>
<p class="l"><b>L36</b> <code>private static final int MARGEN = 9;</code> el mismo motivo que en <code>Tarjeta</code>
(capítulo 43): el borde del botón tiene grosor 2, su capa de halo más ancha mide 2 + 6 × 2.4 = 16.4 píxeles y sobresale
8.2 hacia afuera. Con 9 cabe. Aquí es <code>private</code> porque nadie de fuera necesita conocerlo.</p>
<p class="l"><b>L37</b> En blanco.</p>
"""),
             ("private final Estilo estilo;", r"""
<p class="l"><b>L38</b> <code>private final Estilo estilo;</code> cada botón recuerda cuál de las cuatro formas es.
Es <code>final</code>: un botón no cambia de forma después de creado.</p>
<p class="l"><b>L39</b> <code>private final Iconos.Icono icono;</code> el dibujo del botón (triángulo de «jugar»,
casita, libro…). Su tipo es la interfaz <code>Icono</code> que está dentro de <code>Iconos</code> (capítulo 42): todo
lo que sabe dibujarse en un cuadrado. Puede ser <code>null</code> si un botón no lleva icono.</p>
<p class="l"><b>L40</b> <code>private final Color color;</code> el color principal: el del borde y, en las píldoras,
el inicio del degradado.</p>
<p class="l"><b>L41</b> <code>private final Color colorFinal;</code> el color donde termina el degradado de la
píldora. En los demás estilos vale lo mismo que <code>color</code>.</p>
<p class="l"><b>L42</b> En blanco.</p>
"""),
             ("private BotonNeon(String texto", r"""
<p class="l"><b>L43–L44</b> El constructor recibe siete datos. Es <b><code>private</code></b>: ninguna otra clase
puede escribir <code>new BotonNeon(...)</code>; si lo intenta, el compilador dirá <i>BotonNeon(...) has private access
in BotonNeon</i>. La única forma de crear un botón será a través de los cuatro métodos de fábrica de las líneas 65 a
84, que sí son públicos. La declaración ocupa dos líneas porque es larga; la segunda línea se alinea con la primera
para que se lea mejor.</p>
<p class="l"><b>L45</b> <code>super(texto);</code> llama al constructor de la clase madre, <code>JButton(String)</code>,
que guarda el texto del botón. <code>super(...)</code> es a la clase madre lo que <code>this(...)</code> es a la propia
clase, y también debe ser la primera instrucción. Gracias a esta línea, más tarde <code>getText()</code> devolverá ese
texto.</p>
<p class="l"><b>L46–L49</b> Guardan en los atributos el estilo, el icono y los dos colores. Del ancho y el alto no se
guarda nada: se usan unas líneas más abajo para fijar el tamaño y después el botón los consulta con
<code>getWidth()</code> y <code>getHeight()</code>.</p>
<p class="l"><b>L50</b> En blanco.</p>
"""),
             ("// Se apaga todo", r"""
<p class="l"><b>L51</b> Comentario que explica el grupo siguiente: apagamos todo lo que Swing dibuja por su cuenta,
porque lo pintaremos nosotros.</p>
<p class="l"><b>L52</b> <code>setContentAreaFilled(false);</code> que el aspecto (<i>Look and Feel</i>) de Swing no
rellene el fondo del botón con su gris o su degradado.</p>
<p class="l"><b>L53</b> <code>setBorderPainted(false);</code> que no dibuje su borde de siempre.</p>
<p class="l"><b>L54</b> <code>setFocusPainted(false);</code> que no dibuje el recuadro punteado alrededor del texto
cuando el botón tiene el foco del teclado.</p>
<p class="l"><b>L55</b> <code>setOpaque(false);</code> como en la tarjeta: el botón no cubre su rectángulo entero
(margen y esquinas), así que Swing debe pintar primero lo que hay detrás.</p>
<p class="l"><b>L56</b> <code>setRolloverEnabled(true);</code> pide que el botón lleve la cuenta de si el ratón está
encima («rollover»). Algunos aspectos de Swing lo traen apagado; sin esta línea, <code>isRollover()</code> podría ser
siempre <code>false</code> y el botón no brillaría al pasar el ratón.</p>
<p class="l"><b>L57</b> En blanco.</p>
<p class="l">Un detalle honesto: como vamos a sobrescribir <code>paintComponent</code> sin llamar a
<code>super</code>, Swing ya no pintaría ni su fondo ni su texto. <code>setOpaque(false)</code> sí es imprescindible
(Swing lo consulta para saber si debe pintar lo que hay detrás); las otras tres líneas no cambian lo que ves hoy, pero
dejan escrita la intención y te protegen si algún día alguien añade un <code>super.paintComponent(g)</code>.</p>
"""),
             ("setForeground(Tema.TEXTO);", r"""
<p class="l"><b>L58</b> <code>setForeground(Tema.TEXTO);</code> el color «de primer plano» (el del texto) será
blanco. Lo guardamos en la propiedad estándar de Swing y no en un atributo propio para leerlo después con
<code>getForeground()</code>, como haría cualquier componente.</p>
<p class="l"><b>L59</b> <code>setFont(Tema.fuente(Font.BOLD, estilo == Estilo.MENU ? 25f : 19f));</code> elige la
letra: negrita, de 25 puntos en los botones del menú y de 19 en los demás. La expresión <code>condición ? A : B</code>
es el <b>operador ternario</b> (capítulo 13): un <code>if/else</code> que devuelve un valor. Se lee «¿el estilo es
MENU? entonces 25, si no 19».</p>
<p class="l"><b>L60</b> <code>setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));</code> al pasar por encima,
el puntero se convierte en una manita, la señal universal de «esto se puede pulsar».
<code>getPredefinedCursor</code> es un método estático que devuelve uno de los cursores que trae el sistema.</p>
<p class="l"><b>L61</b> <code>setAlignmentX(CENTER_ALIGNMENT);</code> centrado horizontal dentro de un
<code>BoxLayout</code> vertical, como la tarjeta.</p>
<p class="l"><b>L62</b> <code>Dibujo.fijarTamano(this, ancho, alto);</code> (capítulo 41) pone el tamaño preferido,
el mínimo y el máximo iguales, para que ningún layout estire ni encoja el botón. <code>this</code> es el botón que se
está construyendo.</p>
<p class="l"><b>L63–L64</b> Cierra el constructor; línea en blanco.</p>
"""),
             ("public static BotonNeon menu(", r"""
<p class="l"><b>L65</b> Comentario: botón grande del menú principal.</p>
<p class="l"><b>L66</b> <code>public static BotonNeon menu(String texto, Iconos.Icono icono, Color color) {</code> es
un <b>método de fábrica</b>: un método <code>static</code> (se llama sobre la clase, sin tener un botón todavía) que
crea y devuelve un objeto. Se usa así: <code>BotonNeon.menu("Jugar", Iconos.JUGAR, Tema.ROSA)</code>.</p>
<p class="l"><b>L67</b> <code>return new BotonNeon(texto, icono, color, color, Estilo.MENU, 384, 88);</code> llama al
constructor privado (desde dentro de la clase sí se puede) con lo que el menú siempre necesita: el mismo color como
inicio y fin, el estilo <code>MENU</code> y el tamaño del diseño, 384 × 88. Quien crea un botón del menú no tiene que
saber ni recordar esas medidas.</p>
<p class="l"><b>L68–L69</b> Cierre y línea en blanco.</p>
"""),
             ("public static BotonNeon pildora(", r"""
<p class="l"><b>L70</b> Comentario: píldora con degradado de «desde» a «hasta».</p>
<p class="l"><b>L71</b> Fábrica de la píldora. Aquí sí pide dos colores (<code>desde</code>, <code>hasta</code>) y el
tamaño, porque cada pantalla usa una píldora distinta: «Comenzar partida» de 440 × 66 rosa → morado, «Menú
principal» de 270 × 66 azul → morado…</p>
<p class="l"><b>L72</b> Crea el botón con estilo <code>PILDORA</code>, pasando los dos colores tal cual.</p>
<p class="l"><b>L73–L74</b> Cierre y línea en blanco.</p>
"""),
             ("public static BotonNeon contorno(", r"""
<p class="l"><b>L75</b> Comentario: píldora oscura con borde morado.</p>
<p class="l"><b>L76</b> Fábrica del contorno: no pide color, porque en el diseño estos botones son siempre
morados.</p>
<p class="l"><b>L77</b> Fija <code>Tema.MORADO</code> en los dos colores y el estilo <code>CONTORNO</code>.</p>
<p class="l"><b>L78–L79</b> Cierre y línea en blanco.</p>
"""),
             ("public static BotonNeon icono(", r"""
<p class="l"><b>L80</b> Comentario: botón sin texto; conviene ponerle un <i>tooltip</i> (el globito de ayuda que
aparece al dejar el ratón quieto encima) para que se entienda qué hace.</p>
<p class="l"><b>L81</b> Fábrica del botón cuadrado: solo icono y color.</p>
<p class="l"><b>L82</b> Texto vacío <code>""</code>, estilo <code>ICONO</code> y 58 × 58. Más adelante,
<code>pintarContenidoCentrado</code> reconocerá el texto vacío y dibujará solo el icono.</p>
<p class="l"><b>L83–L84</b> Cierre y línea en blanco.</p>
<div class="caja concepto"><b>¿Por qué fábricas y no un constructor público?</b> Compara
<code>new BotonNeon("Jugar", Iconos.JUGAR, Tema.ROSA, Tema.ROSA, BotonNeon.Estilo.MENU, 384, 88)</code> con
<code>BotonNeon.menu("Jugar", Iconos.JUGAR, Tema.ROSA)</code>. La fábrica: (1) tiene un <b>nombre</b> que dice qué
obtienes; (2) pide solo los datos que tienen sentido para ese estilo; (3) impide combinaciones absurdas, como un
<code>ICONO</code> de 384 × 88 o un <code>CONTORNO</code> rosa que no está en el diseño; (4) concentra las medidas del
diseño en un solo lugar. Es la idea de <i>Factory</i> del capítulo 27. La propia biblioteca de Java lo hace:
<code>List.of(...)</code>, <code>Cursor.getPredefinedCursor(...)</code> o <code>BorderFactory.createEmptyBorder(...)</code>
son fábricas.</div>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L85–L86</b> <code>@Override protected void paintComponent(Graphics g)</code>: reemplazamos el
dibujo del botón (capítulo 23). Swing lo llamará cuando aparezca y cada vez que cambie su estado: el ratón entra o sale,
se aprieta, se suelta.</p>
<p class="l"><b>L87</b> Pedimos el pincel preparado con suavizado (capítulo 41).</p>
<p class="l"><b>L88</b> <code>if (!isEnabled()) {</code>: <code>isEnabled()</code> es heredado y dice si el botón
está activo; <code>!</code> lo niega. Entramos si está <b>desactivado</b>.</p>
<p class="l"><b>L89</b> <code>g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, 0.4f));</code>
cambia la regla de mezcla del pincel: «pinta encima de lo que hay (<code>SRC_OVER</code>), pero todo al 40 % de
opacidad». A partir de aquí, cada relleno, borde y letra que pintemos con <code>g2</code> saldrá desvaído, sin
tener que tocar ni un color. Es la manera estándar de decir «este botón no se puede usar». En el Totito ningún
<code>BotonNeon</code> se llega a desactivar, pero un componente reutilizable debe verse bien en todos sus
estados.</p>
<p class="l"><b>L90</b> Cierra el <code>if</code>.</p>
<p class="l"><b>L91</b> <code>boolean resaltado = getModel().isRollover() &amp;&amp; isEnabled();</code>. Todo botón
de Swing guarda su estado en un objeto aparte, su <b>modelo</b> (<code>ButtonModel</code>), que se obtiene con
<code>getModel()</code>. <code>isRollover()</code> es <code>true</code> mientras el ratón está encima. Exigimos además
que esté activo: un botón desactivado no debe «encenderse».</p>
<p class="l"><b>L92</b> <code>boolean pulsado = getModel().isArmed() &amp;&amp; getModel().isPressed();</code>.
<i>Pressed</i> significa «el botón del ratón está apretado sobre este botón»; <i>armed</i>, «y si lo sueltas ahora,
el clic contará». Si aprietas y, sin soltar, arrastras el ratón fuera, sigue <i>pressed</i> pero deja de estar
<i>armed</i>. Al exigir los dos, el botón se ve hundido solo cuando soltar lo activaría: exactamente lo que el usuario
espera.</p>
<p class="l"><b>L93</b> En blanco.</p>
"""),
             ("double ancho = getWidth()", r"""
<p class="l"><b>L94</b> <code>double ancho = getWidth() - 2.0 * MARGEN;</code> ancho de la figura: el del botón menos
el margen de cada lado. En el botón del menú, 384 − 18 = 366.</p>
<p class="l"><b>L95</b> Lo mismo para el alto: 88 − 18 = 70.</p>
<p class="l"><b>L96</b> <code>double arco = switch (estilo) {</code> es un <b><code>switch</code> de expresión</b>
(Java 14 en adelante, capítulo 13): en lugar de ejecutar instrucciones, <b>produce un valor</b>, que se guarda en
<code>arco</code>. Elige cuánto se redondean las esquinas según el estilo.</p>
<p class="l"><b>L97</b> <code>case MENU -&gt; 30;</code> si es <code>MENU</code>, el arco vale 30 (esquinas de radio
15). Con la flecha <code>-&gt;</code> no hace falta <code>break</code>: solo se ejecuta ese caso. Dentro del
<code>switch</code> se escribe <code>MENU</code> a secas, sin <code>Estilo.</code>, porque Java ya sabe de qué enum
se trata.</p>
<p class="l"><b>L98</b> <code>case ICONO -&gt; 16;</code> el cuadrado de cerrar tiene esquinas más discretas.</p>
<p class="l"><b>L99</b> <code>default -&gt; alto;</code> para todo lo demás (<code>PILDORA</code> y
<code>CONTORNO</code>) el arco es igual al alto. Si el diámetro de la esquina es la altura entera, cada extremo es un
semicírculo completo: eso es una píldora. El comentario lo recuerda.</p>
<p class="l"><b>L100</b> <code>};</code> cierra el <code>switch</code>. Lleva punto y coma porque toda la línea 96 es
una asignación (<code>double arco = …;</code>) y las asignaciones terminan en <code>;</code>. Olvidarlo es un error
muy común.</p>
<p class="l"><b>L101</b> Crea la figura del botón: empieza en (9, 9), mide <code>ancho × alto</code> y redondea con
<code>arco</code>.</p>
<p class="l"><b>L102</b> En blanco.</p>
"""),
             ("pintarRelleno(g2, forma, resaltado);", r"""
<p class="l"><b>L103</b> <code>pintarRelleno(g2, forma, resaltado);</code> primera capa: el interior. Va en un
método aparte (línea 119) para que <code>paintComponent</code> se lea como una lista de pasos.</p>
<p class="l"><b>L104</b> <code>Color borde = estilo == Estilo.PILDORA ? Tema.aclarar(color, 0.2f) : color;</code>
elige el color del borde. En las píldoras, el relleno ya es de <code>color</code> casi opaco; un borde del mismo color
no se notaría, así que se aclara un 20 % hacia el blanco (capítulo 40). En los demás estilos el borde es el color
tal cual.</p>
<p class="l"><b>L105</b> <code>Dibujo.trazoNeon(g2, forma, borde, 2f, resaltado ? 1.5f : 1f);</code> segunda capa: el
borde de neón de 2 píxeles. El último número es la <b>intensidad</b> (capítulo 41): con el ratón encima vale 1.5 y el
halo es un 50 % más opaco; si no, 1. Ese cambio es todo el efecto de «se enciende al pasar el ratón».</p>
<p class="l"><b>L106</b> <code>if (pulsado) {</code> tercera capa, solo mientras se aprieta.</p>
<p class="l"><b>L107</b> <code>g2.setColor(new Color(0, 0, 0, 60));</code> negro con alfa 60 (un 24 %).</p>
<p class="l"><b>L108</b> Rellena la figura con ese negro translúcido: el botón se oscurece, como si se hundiera.</p>
<p class="l"><b>L109–L110</b> Cierra el <code>if</code>; línea en blanco.</p>
"""),
             ("if (estilo == Estilo.MENU) {", r"""
<p class="l"><b>L111</b> Última capa, el contenido (icono y texto). El botón del menú tiene una distribución propia…</p>
<p class="l"><b>L112</b> …que dibuja <code>pintarContenidoMenu</code> (línea 143).</p>
<p class="l"><b>L113–L114</b> <code>} else {</code> en los otros tres estilos…</p>
<p class="l"><b>L115</b> …el icono y el texto van centrados como un bloque (línea 169).</p>
<p class="l"><b>L116</b> Cierra el <code>if/else</code>.</p>
<p class="l"><b>L117</b> <code>g2.dispose();</code> liberamos la copia del pincel. Como el <code>AlphaComposite</code>
de la línea 89 se puso en la copia, muere con ella y no afecta a nada más.</p>
<p class="l"><b>L118</b> Cierra <code>paintComponent</code>.</p>
"""),
             ("private void pintarRelleno", r"""
<p class="l"><b>L119</b> <code>private void pintarRelleno(Graphics2D g2, RoundRectangle2D forma, boolean resaltado)
{</code> método auxiliar: <code>private</code> porque es un detalle interno del botón; <code>void</code> porque no
devuelve nada, solo pinta. Recibe lo que necesita como parámetros en lugar de recalcularlo.</p>
<p class="l"><b>L120</b> <code>float x0 = (float) forma.getX();</code> borde izquierdo de la figura. El
<code>(float)</code> es un <b>casting</b> (capítulo 12): <code>getX()</code> devuelve <code>double</code> y
<code>GradientPaint</code> pide <code>float</code>; convertir de <code>double</code> a <code>float</code> puede
perder precisión, así que Java exige que lo pidas explícitamente.</p>
<p class="l"><b>L121</b> Borde derecho: x más ancho. En el menú, x0 = 9 y x1 = 375.</p>
<p class="l"><b>L122</b> <code>switch (estilo) {</code> esta vez es un <code>switch</code> <b>de instrucción</b> (no
devuelve nada), pero con flechas: cada caso ejecuta su instrucción y no «se cae» al siguiente.</p>
"""),
             ("case MENU -> g2.setPaint", r"""
<p class="l"><b>L123–L125</b> <code>case MENU -&gt; g2.setPaint(new GradientPaint(x0, 0, …, x1, 0, …));</code>. Un
<code>GradientPaint</code> recibe dos puntos con su color: (x0, 0) con el primero y (x1, 0) con el segundo. Como los
dos tienen la misma y, el degradado es <b>horizontal</b>. A la izquierda, el color del botón con alfa 65 (95 si el
ratón está encima: un poco más vivo); a la derecha, el fondo oscuro <code>FONDO_ABAJO</code> con alfa 120. Por eso
el botón «Jugar» es rosado a la izquierda y se apaga hacia la flecha. <code>setPaint</code> es como
<code>setColor</code>, pero acepta cualquier pintura, no solo colores lisos.</p>
<p class="l"><b>L126–L128</b> <code>case PILDORA</code>: degradado horizontal de <code>color</code> a
<code>colorFinal</code>, casi opacos (alfa 225; 255 con el ratón encima). Así «Menú principal» pasa de azul a
morado.</p>
<p class="l"><b>L129</b> <code>default -&gt; g2.setPaint(Tema.conAlfa(color, resaltado ? 60 : 30));</code> el
contorno y el icono: un relleno liso muy tenue de su color (alfa 30), que sube a 60 con el ratón.</p>
<p class="l"><b>L130</b> Cierra el <code>switch</code>.</p>
<p class="l"><b>L131</b> <code>g2.fill(forma);</code> rellena la figura con la pintura que haya quedado elegida. Un
solo <code>fill</code> para los tres casos: el <code>switch</code> solo decide <i>con qué</i>.</p>
<p class="l"><b>L132</b> En blanco.</p>
"""),
             ("if (estilo == Estilo.PILDORA) {", r"""
<p class="l"><b>L133</b> Solo para las píldoras…</p>
<p class="l"><b>L134</b> …un reflejo de cristal en la mitad de arriba, como dice el comentario.</p>
<p class="l"><b>L135</b> <code>float y0 = (float) forma.getY();</code> el borde superior de la figura.</p>
<p class="l"><b>L136–L137</b> Un degradado <b>vertical</b> (ahora cambia la y y la x se queda en 0): empieza en
<code>y0</code> con blanco de alfa 50 y termina a media altura con blanco de alfa 0, totalmente transparente. Un
<code>GradientPaint</code> normal, más allá de su segundo punto, sigue con el último color; así que de la mitad para
abajo el «blanco» es invisible.</p>
<p class="l"><b>L138</b> Rellena toda la figura con ese reflejo: arriba se ve un brillo blanquecino que se desvanece,
abajo nada. Es el detalle que hace que la píldora parezca de vidrio.</p>
<p class="l"><b>L139–L141</b> Cierra el <code>if</code>, cierra el método y una línea en blanco.</p>
"""),
             ("private void pintarContenidoMenu", r"""
<p class="l"><b>L142</b> Comentario: icono a la izquierda, divisor, texto y flechita.</p>
<p class="l"><b>L143</b> Declara el método que reparte el contenido del botón del menú.</p>
<p class="l"><b>L144–L147</b> Copia en variables cortas la posición y el tamaño de la figura (x = 9, y = 9, ancho =
366, alto = 70 en el menú). No es obligatorio, pero las fórmulas de abajo quedan mucho más legibles que con
<code>forma.getWidth()</code> por todas partes.</p>
<p class="l"><b>L148</b> En blanco.</p>
"""),
             ("double tamIcono = alto * 0.5;", r"""
<p class="l"><b>L149</b> <code>double tamIcono = alto * 0.5;</code> el icono ocupa la mitad del alto: 35 píxeles. Se
expresa como proporción, no como número fijo, para que el icono crezca si alguien hace el botón más alto.</p>
<p class="l"><b>L150</b> <code>double divisor = x + ancho * 0.27;</code> la línea divisoria cae al 27 % del ancho:
9 + 98.8 = 107.8. Ese porcentaje se midió sobre la imagen del diseño.</p>
<p class="l"><b>L151–L152</b> Dibuja el icono (capítulo 42: <code>dibujar(g, x, y, tam, color)</code> lo pinta dentro
del cuadrado de lado <code>tam</code> con esquina en <code>(x, y)</code>). Su centro horizontal es
<code>x + ancho * 0.135</code>, la mitad del 27 %: así queda centrado en el hueco a la izquierda del divisor. Se resta
<code>tamIcono / 2</code> para pasar del centro a la esquina. En vertical, <code>y + (alto - tamIcono) / 2</code> lo
centra. El color es el del botón aclarado un 15 %, para que resalte sobre el relleno.</p>
<p class="l"><b>L153</b> En blanco.</p>
"""),
             ("g2.setColor(new Color(255, 255, 255, 45));", r"""
<p class="l"><b>L154</b> La línea divisoria será blanca con alfa 45: apenas una insinuación.</p>
<p class="l"><b>L155</b> <code>g2.setStroke(new BasicStroke(1.5f));</code> trazo de 1.5 píxeles de grosor.</p>
<p class="l"><b>L156</b> <code>g2.draw(new Line2D.Double(divisor, y + alto * 0.22, divisor, y + alto * 0.78));</code>
una línea vertical (misma x en los dos extremos) que va del 22 % al 78 % del alto: no toca los bordes, como en el
diseño.</p>
<p class="l"><b>L157</b> En blanco.</p>
"""),
             ("g2.setFont(getFont());", r"""
<p class="l"><b>L158</b> <code>g2.setFont(getFont());</code> el pincel escribirá con la fuente que pusimos en el
constructor (línea 59). Hay que decírselo: el pincel no sabe qué fuente tiene el botón.</p>
<p class="l"><b>L159</b> Color del texto: el <i>foreground</i>, blanco.</p>
<p class="l"><b>L160</b> <code>FontMetrics fm = g2.getFontMetrics();</code> las medidas de esa fuente en ese pincel.
Se piden <b>después</b> de <code>setFont</code>; si no, medirías otra letra.</p>
<p class="l"><b>L161</b> <code>g2.drawString(getText(), (float) (divisor + 30), Dibujo.lineaBaseCentrada(fm, (float)
(y + alto / 2)));</code> escribe el texto. Empieza 30 píxeles a la derecha del divisor (alineado a la izquierda, no
centrado: así los tres botones del menú tienen el texto en la misma columna). La y de <code>drawString</code> no es la
parte de arriba de las letras sino su <b>línea base</b>, donde se apoyan; <code>lineaBaseCentrada</code> (capítulo 41)
calcula la línea base que deja el texto centrado en vertical sobre el centro del botón.</p>
<p class="l"><b>L162</b> En blanco.</p>
"""),
             ("double tamFlecha", r"""
<p class="l"><b>L163</b> La flechita mide el 30 % del alto: 21 píxeles.</p>
<p class="l"><b>L164–L165</b> Dibuja <code>Iconos.CHEVRON</code> pegado a la derecha: su esquina izquierda está a 28
píxeles del borde derecho más su propio tamaño. Color: el del botón aclarado un 20 %.</p>
<p class="l"><b>L166–L167</b> Cierra el método; línea en blanco.</p>
"""),
             ("private void pintarContenidoCentrado", r"""
<p class="l"><b>L168</b> Comentario: para píldoras e iconos, icono y texto centrados como un bloque.</p>
<p class="l"><b>L169</b> Declara el método.</p>
<p class="l"><b>L170</b> El alto de la figura.</p>
<p class="l"><b>L171</b> <code>double cy = forma.getY() + alto / 2;</code> la y del centro de la figura; todo se
centrará respecto a ella.</p>
<p class="l"><b>L172</b> <code>String texto = getText();</code> el texto del botón (lo guardó <code>super(texto)</code>
en la línea 45).</p>
<p class="l"><b>L173</b> En blanco.</p>
"""),
             ("if (texto == null || texto.isEmpty())", r"""
<p class="l"><b>L174</b> <code>if (texto == null || texto.isEmpty()) {</code> ¿no hay texto? Es el caso del botón
<code>ICONO</code>. Se comprueba primero <code>null</code> y luego vacío; el <code>||</code> (o lógico) es «en
cortocircuito»: si lo primero es cierto, lo segundo no se evalúa. Al revés, si <code>texto</code> fuera
<code>null</code>, <code>texto.isEmpty()</code> lanzaría <code>NullPointerException</code>.</p>
<p class="l"><b>L175</b> El icono ocupará la mitad del alto.</p>
<p class="l"><b>L176</b> Lo dibuja centrado: <code>getCenterX()</code> da la x del centro de la figura; se resta media
anchura para obtener la esquina. Usa el color del botón (la X rosa del encabezado).</p>
<p class="l"><b>L177</b> <code>return;</code> termina el método aquí: no hay texto que dibujar. Salir pronto así
evita meter el resto del método dentro de un <code>else</code>.</p>
<p class="l"><b>L178–L179</b> Cierra el <code>if</code>; línea en blanco.</p>
"""),
             ("g2.setFont(getFont());", r"""
<p class="l"><b>L180–L181</b> Fuente del botón y sus medidas, igual que en el menú.</p>
<p class="l"><b>L182</b> <code>double tamIcono = icono == null ? 0 : alto * 0.44;</code> si hay icono, mide el 44 %
del alto; si no, 0.</p>
<p class="l"><b>L183</b> El hueco entre icono y texto: 16 píxeles, o 0 si no hay icono (no tendría sentido dejar un
hueco antes del texto).</p>
<p class="l"><b>L184</b> <code>double total = tamIcono + hueco + fm.stringWidth(texto);</code> el ancho del
<b>bloque</b> icono + hueco + texto. <code>stringWidth</code> mide en píxeles cuánto ocupa el texto con esa fuente.</p>
<p class="l"><b>L185</b> <code>double x = forma.getCenterX() - total / 2;</code> donde empieza el bloque para que
quede centrado: el centro menos la mitad del bloque. Centrar el bloque entero, y no el texto solo, es lo que hace que
el conjunto «casita + Menú principal» se vea equilibrado.</p>
"""),
             ("if (icono != null) {", r"""
<p class="l"><b>L186–L188</b> Si hay icono, se dibuja al principio del bloque, centrado en vertical, siempre en
blanco (<code>Tema.TEXTO</code>), porque sobre una píldora de color un icono de color no se vería.</p>
<p class="l"><b>L189</b> Color del texto.</p>
<p class="l"><b>L190</b> Escribe el texto a continuación del icono y del hueco, con la línea base centrada en
<code>cy</code>.</p>
<p class="l"><b>L191–L192</b> Cierran el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>El botón «Jugar» del menú, píxel a píxel</h3>
<p><code>PantallaMenu</code> (capítulo 56) hará <code>BotonNeon.menu("Jugar", Iconos.JUGAR, Tema.ROSA)</code>. La
fábrica llama al constructor con estilo <code>MENU</code> y tamaño 384 × 88; el constructor pone letra negrita de 25
puntos y fija ese tamaño. Cuando Swing lo pinta:</p>
<table class="tabla">
<tr><th>Qué</th><th>Cuenta</th><th>Resultado (píxeles)</th></tr>
<tr><td>Figura</td><td>(9, 9), 384 − 18 por 88 − 18, arco 30</td><td>366 × 70 en (9, 9)</td></tr>
<tr><td>Tamaño del icono</td><td>70 × 0.5</td><td>35 × 35</td></tr>
<tr><td>Esquina del icono</td><td>x: 9 + 366 × 0.135 − 17.5; y: 9 + (70 − 35) ÷ 2</td><td>(40.9, 26.5)</td></tr>
<tr><td>Divisor</td><td>x: 9 + 366 × 0.27; de y = 9 + 15.4 a y = 9 + 54.6</td><td>x = 107.8, de 24.4 a 63.6</td></tr>
<tr><td>Inicio del texto</td><td>107.8 + 30</td><td>x = 137.8</td></tr>
<tr><td>Línea base del texto</td><td>centro 44 + (ascenso 23 − descenso 6) ÷ 2</td><td>y = 52.5</td></tr>
<tr><td>Flechita</td><td>tamaño 70 × 0.3; x: 9 + 366 − 28 − 21; y: 9 + (70 − 21) ÷ 2</td><td>21 × 21 en (326, 33.5)</td></tr>
</table>
<p>El ascenso y el descenso de la fuente los medí con Liberation Sans (la fuente que elige <code>Tema</code> en
Linux). En Windows, con Segoe UI, salen uno o dos píxeles distintos; por eso el código nunca escribe «52.5» a mano:
siempre <b>mide</b>.</p>
<h3>Qué pasa cuando el ratón entra, aprieta y suelta</h3>
<ol>
<li><b>El ratón entra</b> en el botón. Swing (no nosotros) pone <code>rollover = true</code> en el modelo. El modelo
avisa de que cambió y el botón se repinta solo. Ahora <code>resaltado</code> es <code>true</code>: el relleno rosa sube
de alfa 65 a 95 y el halo del borde se pinta con intensidad 1.5. El botón «se enciende».</li>
<li><b>Aprieta</b> el botón izquierdo: el modelo pasa a <code>pressed = true</code> y <code>armed = true</code>. Nuevo
repintado, ahora con <code>pulsado</code>: encima del borde se pinta el negro de alfa 60.</li>
<li><b>Arrastra fuera sin soltar</b>: <code>armed</code> pasa a <code>false</code> (y <code>rollover</code> también).
El botón deja de verse hundido. Si suelta ahí, no pasa nada.</li>
<li><b>Suelta dentro</b>: el modelo dispara el evento de acción; <code>JButton</code> llama a cada
<code>ActionListener</code> (por ejemplo, el que lleva a la configuración). Nosotros no escribimos nada de eso: lo
heredamos.</li>
</ol>
<h3>La píldora «Menú principal» de 270 × 66</h3>
<p>Figura: (9, 9), 252 × 48, arco = 48 (extremos semicirculares de radio 24). Centro: x = 135, y = 33. Icono: 48 ×
0.44 = 21.1 píxeles; hueco 16; el texto mide 134 píxeles en negrita de 19 puntos (Liberation Sans). Bloque: 21.1 + 16
+ 134 = 171.1; empieza en 135 − 85.6 = 49.4. La casita va de 49.4 a 70.5 y el texto empieza en 86.6. Si el texto
fuera más largo, el bloque entero se correría a la izquierda para seguir centrado.</p>

<h2>Compila y prueba</h2>
<p>Todavía no hay pantalla donde ver el botón (llegará en el capítulo 56). Compila con <i>Run → Clean and Build
Project</i> (Shift+F11) y comprueba <code>BUILD SUCCESS</code>. Luego mira qué se generó:</p>
<pre class="ps">Get-ChildItem target\classes\BotonNeon*.class | Select-Object Name</pre>
<pre class="salida">Name
----
BotonNeon$Estilo.class
BotonNeon.class</pre>
<p>Hay <b>dos</b> archivos: el enum que declaraste dentro de la clase se compila en su propio
<code>.class</code>, con el nombre de la clase de fuera, un <code>$</code> y el suyo. Lo verás con cada clase
interna.</p>
<p>Si hiciste la foto opcional del capítulo 43, cambia estas dos líneas de
<code>..\pruebas-totito\FotoComponente.java</code>:</p>
<pre class="java">        JComponent pieza = BotonNeon.menu("Jugar", Iconos.JUGAR, Tema.ROSA);
        int ancho = 384, alto = 88;</pre>
<p>y ejecuta de nuevo <code>java -cp target\classes ..\pruebas-totito\FotoComponente.java</code>. Verás el botón rosa
con su triángulo, el divisor, «Jugar» y la flechita, como en la captura del menú. Para ver el estado «ratón encima»,
añade debajo de la línea de <code>pieza</code>: <code>((BotonNeon) pieza).getModel().setRollover(true);</code></p>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Mensaje</th><th>Causa</th><th>Solución</th></tr>
<tr><td><code>';' expected</code> en la línea 100</td><td>Falta el <code>;</code> después de la llave que cierra el
<code>switch</code> de expresión</td><td>Debe ser <code>};</code></td></tr>
<tr><td><code>call to super must be first statement in constructor</code></td><td>Pusiste algo antes de
<code>super(texto)</code></td><td><code>super(...)</code> va primero</td></tr>
<tr><td><code>BotonNeon(...) has private access in BotonNeon</code></td><td>Alguna clase escribe <code>new
BotonNeon(...)</code></td><td>Usa las fábricas: <code>BotonNeon.menu(...)</code>, etc.</td></tr>
<tr><td><code>cannot find symbol: variable CHEVRON</code></td><td><code>Iconos.java</code> no tiene ese icono o se
llama distinto</td><td>Revisa el capítulo 42</td></tr>
<tr><td><code>the switch expression does not cover all possible input values</code></td><td>Borraste el
<code>default</code></td><td>Un <code>switch</code> de expresión debe dar valor para todos los casos</td></tr>
<tr><td>(en pantalla, más adelante) el botón no brilla al pasar el ratón</td><td>Falta
<code>setRolloverEnabled(true)</code></td><td>Línea 56</td></tr>
</table>

<div class="caja git"><b>Git</b> Commit del botón, en la rama <code>interfaz-neon</code>:
<pre class="ps">git status
git add src\BotonNeon.java
git commit -m "BotonNeon: boton neon con cuatro estilos"
git push</pre>
El mensaje no lleva tildes por costumbre: algunas terminales antiguas las muestran mal en el historial.</div>

<h2>Resumen</h2>
<ul>
<li>Heredar de <code>JButton</code> conserva todo el comportamiento (clics, teclado, tooltip, estados) y permite
cambiar solo el dibujo.</li>
<li>Antes de dibujar a mano se apagan el relleno, el borde y el recuadro de foco de Swing, y el botón se declara no
opaco.</li>
<li>Constructor privado + métodos de fábrica estáticos: nombres claros, parámetros justos y medidas del diseño en un
solo lugar.</li>
<li>El enum <code>Estilo</code> elige entre cuatro formas; un <code>switch</code> de expresión decide el arco y otro
de instrucción el relleno.</li>
<li>El modelo del botón dice si el ratón está encima (<i>rollover</i>) y si un clic se completaría
(<i>armed</i> + <i>pressed</i>); de ahí salen el brillo y el oscurecido.</li>
<li><code>AlphaComposite</code> atenúa todo lo que se pinta después; <code>GradientPaint</code> crea degradados
horizontales o verticales según sus dos puntos.</li>
<li>El contenido se reparte con proporciones del alto y del ancho y se centra midiendo con <code>FontMetrics</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Botones de marca</b>: en la app de una tienda o un restaurante, una clase <code>BotonMarca</code> con fábricas
<code>primario(...)</code>, <code>secundario(...)</code> y <code>peligro(...)</code> («Eliminar», en rojo) mantiene
coherente el aspecto de decenas de pantallas.</li>
<li><b>Fábricas estáticas</b> en tus propias clases de datos: <code>Fecha.hoy()</code>,
<code>Dinero.quetzales(25.50)</code>, <code>Usuario.invitado()</code> se leen mejor que constructores con muchos
parámetros.</li>
<li><b>Estados visuales</b>: cualquier control (un interruptor, una pestaña, un elemento de lista) se dibuja leyendo
su estado: normal, ratón encima, apretado, desactivado. El patrón de este botón sirve para todos.</li>
<li><b>Enum + switch</b> para variantes: los tamaños de una camiseta (S, M, L) que deciden un precio, o los tipos de
celda de un Buscaminas que deciden un color.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Calcula a mano la figura y el arco de <code>BotonNeon.contorno("Volver", Iconos.FLECHA_IZQUIERDA, 300, 52)</code>.
¿Cuál es el radio de sus extremos? Pista: líneas 94–101.</li>
<li>En la foto opcional, fotografía el botón desactivado: añade <code>pieza.setEnabled(false);</code>. ¿Qué línea del
código produce el cambio?</li>
<li>Agrega un quinto estilo a mano, sin cambiar el archivo del proyecto (hazlo en una copia): ¿en qué lugares tendrías
que tocar para que <code>Estilo.CUADRADO</code> tenga arco 0? Pista: hay un <code>switch</code> de expresión y otro de
instrucción.</li>
<li>¿Qué pasaría si en la línea 92 se usara solo <code>getModel().isPressed()</code>? Describe la situación en la que
se notaría.</li>
<li>Reto: escribe en papel una fábrica nueva, <code>public static BotonNeon peligro(String texto, int ancho, int
alto)</code>, que cree una píldora de rosa a fresa. ¿Qué constantes de <code>Tema</code> usarías?</li>
</ol></div>
""",
}
