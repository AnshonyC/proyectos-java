# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 50,
    "titulo": "SelectorSimbolo.java: elegir X u O",
    "antes": r"""
<p class="entrada">Antes de empezar, el Jugador 1 elige si juega con X o con O. En este capítulo construyes el
selector de dos cajas que aparece bajo «SÍMBOLOS»: un componente que se dibuja entero a mano, que sabe en qué caja
cayó un clic y que muestra debajo una frase para que no quede duda de quién juega con qué.</p>

<h2>Por qué existe este archivo</h2>
<p>En la versión 0.1 (capítulo 33) el jugador humano era siempre X. En la versión neón se puede elegir. El diseño
(<code>diseno/configuracion.jpg</code>) lo resuelve con <b>dos cajas</b>: una con una X rosa y otra con una O azul;
la elegida brilla y lleva marcado un circulito debajo, la otra se ve apagada. Es lo que en las interfaces se llama un
<b>botón de radio</b> (<i>radio button</i>): un grupo de opciones donde solo una puede estar marcada, como los
botones de las radios antiguas, donde al hundir una emisora saltaba la anterior.</p>
<p>Swing trae <code>JRadioButton</code>, pero su aspecto es el del sistema operativo (un circulito gris con un texto
al lado) y no se parece en nada al diseño. Por eso hacemos un componente propio que se dibuja con las herramientas
de <code>Dibujo</code> (capítulo 41) y que responde al ratón por su cuenta.</p>
<p>La regla que guarda es mínima: <b>la caja marcada es la ficha del Jugador 1</b>; el Jugador 2 se queda con la
otra. Así nunca pueden quedar los dos con la misma ficha (que es justo lo que <code>Partida</code> prohíbe con una
excepción, capítulo 38).</p>
<figure><img src="capturas/3-configuracion.png"><figcaption>El selector, en el centro bajo «SÍMBOLOS»: la X está
elegida (brilla y tiene el circulito marcado) y la O está apagada.</figcaption></figure>

<h2>Qué vas a aprender</h2>
<ul>
<li>A heredar de <code>JComponent</code>, la clase más básica de Swing, cuando solo hace falta dibujar.</li>
<li>A escuchar el ratón con <code>MouseAdapter</code> y una <b>clase anónima</b>, y a saber en qué zona cayó el
clic con <code>Rectangle.contains</code> (eso se llama <i>hit testing</i>, «prueba de impacto»).</li>
<li>A cambiar el cursor a la «manito» con <code>Cursor</code>.</li>
<li>A medir texto con <code>FontMetrics</code> para centrarlo.</li>
<li>A volver semitransparente todo lo que se dibuja con <code>AlphaComposite</code>, y por qué hay que dejarlo
como estaba.</li>
<li>A dibujar un botón de radio con dos <code>Ellipse2D</code>.</li>
<li>El tipo <code>char</code> en acción: recorrer <code>{'X', 'O'}</code> y unir un <code>char</code> a un
texto.</li>
</ul>

<h2>El plano del selector, en píxeles</h2>
<p>El componente mide <b>434 × 120</b>. Arriba, dos «zonas» de 120 × 98 separadas por 34 píxeles; abajo, una franja
de 22 píxeles para la leyenda.</p>
<table class="tabla">
<tr><th>Parte</th><th>Caja X</th><th>Caja O</th></tr>
<tr><td>Zona sensible al clic</td><td>(80, 0) de 120 × 98</td><td>(234, 0) de 120 × 98</td></tr>
<tr><td>Caja redondeada visible</td><td>(88, 8) de 104 × 82</td><td>(242, 8) de 104 × 82</td></tr>
<tr><td>Centro de la ficha</td><td>(140, 40,8)</td><td>(294, 40,8)</td></tr>
<tr><td>Aro del botón de radio</td><td>círculo de 16 con centro (140, 75)</td><td>círculo de 16 con centro (294, 75)</td></tr>
<tr><td>Leyenda</td><td colspan="2">centrada, línea base en y = 115</td></tr>
</table>

<h2>Créalo</h2>
<ol>
<li>En NetBeans: clic derecho en <i>Source Packages → &lt;default package&gt;</i> → <i>New → Java Class…</i></li>
<li><i>Class Name</i>: <code>SelectorSimbolo</code> → <i>Finish</i>.</li>
<li>Borra la plantilla y escribe el código de abajo.</li>
</ol>
<p>Alternativa: <code>New-Item src\SelectorSimbolo.java</code> desde la carpeta del proyecto y edítalo en UTF-8.
Importante: la línea 71 lleva un punto medio «·»; si el archivo no se guarda en UTF-8, el compilador protestará por ese carácter.
NetBeans y el <code>pom.xml</code> del capítulo 5 ya trabajan en UTF-8.</p>
""",
    "archivos": [
        {"ruta": "src/SelectorSimbolo.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.AlphaComposite</code>: la regla con que se mezcla lo que se pinta con lo que
ya había debajo. La usaremos para dibujar la ficha no elegida a media transparencia.</p>
<p class="l"><b>L2</b> <code>java.awt.Color</code>: para guardar el color de cada ficha.</p>
<p class="l"><b>L3</b> <code>java.awt.Cursor</code>: la forma del puntero del ratón (flecha, manito, reloj…).</p>
<p class="l"><b>L4</b> <code>java.awt.Font</code>: por la constante <code>Font.PLAIN</code> de la leyenda.</p>
<p class="l"><b>L5</b> <code>java.awt.FontMetrics</code>: las «medidas» de una fuente: cuánto mide de ancho un
texto, cuánto sube y baja. Sirve para centrar la leyenda.</p>
<p class="l"><b>L6–L7</b> <code>Graphics</code> y <code>Graphics2D</code>: el pincel que recibe
<code>paintComponent</code> y su versión ampliada (capítulo 37).</p>
<p class="l"><b>L8</b> <code>java.awt.Rectangle</code>: un rectángulo con coordenadas enteras (x, y, ancho, alto).
Lo usamos para describir la zona de cada caja y preguntarle si un punto cae dentro.</p>
"""),
             ("import java.awt.event.MouseAdapter", r"""
<p class="l"><b>L9</b> <code>java.awt.event.MouseAdapter</code>: del paquete <code>event</code> (eventos). Es una
clase «adaptadora» que ya implementa todos los métodos de escucha del ratón, vacíos; heredando de ella solo
escribimos el que nos interesa.</p>
<p class="l"><b>L10</b> <code>java.awt.event.MouseEvent</code>: el objeto que describe un evento del ratón (dónde
fue, qué botón, cuántos clics).</p>
<p class="l"><b>L11</b> <code>java.awt.geom.Ellipse2D</code>: elipses y círculos, para el botón de radio.</p>
<p class="l"><b>L12</b> <code>java.awt.geom.RoundRectangle2D</code>: rectángulos con esquinas redondeadas, para las
cajas.</p>
<p class="l"><b>L13</b> <code>javax.swing.JComponent</code>: la clase base de casi todo Swing. Fíjate en que
empieza por <code>javax.swing</code> y no por <code>java.awt</code>: Swing es la capa moderna construida encima de
AWT (capítulo 37).</p>
"""),
             ("public class SelectorSimbolo", r"""
<p class="l"><b>L15–L19</b> Comentario de la clase: qué son las dos cajas, la regla («la marcada es del Jugador
1») y para qué está la leyenda.</p>
<p class="l"><b>L20</b> <code>public class SelectorSimbolo extends JComponent {</code> el selector hereda de
<code>JComponent</code> y no de <code>JPanel</code>. ¿Por qué? Un <code>JPanel</code> está pensado para
<b>contener</b> otros componentes y, por defecto, es opaco y se pinta un fondo gris. Nuestro selector no contiene
nada: solo dibuja. <code>JComponent</code> es lo mínimo: no pinta fondo ni nada por su cuenta, es transparente
y nos deja el lienzo libre. Regla práctica: <b>JPanel si vas a meter hijos, JComponent si solo vas a
dibujar</b>.</p>
"""),
             ("private static final int ANCHO_CAJA", r"""
<p class="l"><b>L22</b> <code>private static final int ANCHO_CAJA = 120;</code> ancho de la zona de cada caja.
<code>private</code> porque ninguna otra clase necesita saberlo.</p>
<p class="l"><b>L23</b> <code>ALTO_CAJA = 98</code>: alto de la zona de cada caja (la ficha arriba y el circulito
abajo).</p>
<p class="l"><b>L24</b> <code>HUECO = 34</code>: separación horizontal entre las dos cajas.</p>
<p class="l"><b>L25</b> <code>ALTO_LEYENDA = 22</code>: franja de abajo para la frase.</p>
"""),
             ("private char fichaJugador1", r"""
<p class="l"><b>L27</b> <code>private char fichaJugador1 = 'X';</code> el <b>único estado</b> del selector: qué
ficha eligió el Jugador 1. Es un <code>char</code> (un solo carácter, entre comillas simples, capítulo 12), el mismo
tipo que usa <code>Tablero</code> para sus casillas. Empieza en <code>'X'</code>, que es lo habitual. Todo lo
demás (qué caja brilla, qué dice la leyenda) se <b>deduce</b> de este dato al dibujar; no hay nada más que
mantener sincronizado.</p>
"""),
             ("public SelectorSimbolo()", r"""
<p class="l"><b>L29</b> El constructor, sin parámetros: todos los selectores son iguales.</p>
<p class="l"><b>L30</b> <code>Dibujo.fijarTamano(this, 2 * ANCHO_CAJA + HUECO + 160, ALTO_CAJA + ALTO_LEYENDA);</code>
fija el tamaño en (240 + 34 + 160) × (98 + 22) = <b>434 × 120</b>. Las dos cajas con su hueco ocupan 274 píxeles; los
160 restantes son <b>holgura</b>: 80 libres a cada lado. Con la fuente de Windows la leyenda mide unos 250 píxeles y
cabe de sobra, pero si alguien cambia la frase, la fuente o el idioma («Player 1 plays with X…»), hay sitio. Ahí no
se dibuja nada.</p>
<p class="l"><b>L31</b> <code>setAlignmentX(CENTER_ALIGNMENT);</code> le dice al <code>BoxLayout</code> de la
pantalla que lo centre en horizontal. <code>CENTER_ALIGNMENT</code> es una constante (vale 0.5) que se hereda de
<code>Component</code>, por eso se escribe sin prefijo. <code>PantallaBase.agregar</code> (capítulo 55) también lo
hace, pero así el componente se centra aunque alguien lo agregue de otra forma.</p>
<p class="l"><b>L32</b> <code>setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));</code> al pasar el ratón
por encima, el puntero se convierte en la <b>manito</b> de los enlaces. Es una pista visual: «esto se puede
pulsar». <code>getPredefinedCursor</code> es un método <code>static</code> que devuelve uno de los cursores que trae
el sistema; <code>HAND_CURSOR</code> es la constante que dice cuál.</p>
"""),
             ("addMouseListener", r"""
<p class="l"><b>L33</b> <code>addMouseListener(new MouseAdapter() {</code> registra un «oyente» que Swing avisará
cada vez que pase algo con el ratón sobre este componente. Lo que va entre llaves es una <b>clase anónima</b>
(capítulo 25): una clase sin nombre que hereda de <code>MouseAdapter</code> y se crea en el mismo sitio donde se
usa. La interfaz <code>MouseListener</code> tiene cinco métodos (<code>mouseClicked</code>,
<code>mousePressed</code>, <code>mouseReleased</code>, <code>mouseEntered</code>, <code>mouseExited</code>);
gracias al adaptador solo escribimos uno.</p>
<p class="l"><b>L34–L35</b> <code>@Override public void mousePressed(MouseEvent e)</code> se ejecuta en el instante
en que se <b>hunde</b> el botón del ratón. Elegimos <code>mousePressed</code> y no <code>mouseClicked</code> porque
<code>mouseClicked</code> solo llega si el botón se hunde y se suelta sin mover el ratón; si la mano tiembla un
píxel, el clic «no cuenta». Con <code>mousePressed</code> la respuesta es inmediata y nunca falla.</p>
<p class="l"><b>L36</b> <code>if (caja('X').contains(e.getPoint())) {</code> <code>e.getPoint()</code> devuelve
el punto donde se pulsó, medido desde la esquina superior izquierda de <b>este</b> componente.
<code>caja('X')</code> devuelve el rectángulo de la caja X y <code>contains</code> responde <code>true</code> si el
punto está dentro. Desde la clase anónima podemos llamar a <code>caja</code> como si estuviéramos en el selector:
una clase anónima ve los métodos del objeto que la creó.</p>
<p class="l"><b>L37</b> Si cayó en la caja X, el Jugador 1 elige X.</p>
<p class="l"><b>L38–L39</b> <code>} else if (...)</code>: si no, se prueba la caja O; si cae ahí, elige O.</p>
<p class="l"><b>L40–L42</b> Si el clic cayó fuera de las dos cajas (en el hueco del medio, en la holgura de los
lados o sobre la leyenda), no pasa nada: no hay <code>else</code> final. Luego se cierran el <code>if</code>, el
método, la clase anónima (<code>}</code>) y la llamada a <code>addMouseListener</code> (<code>);</code>): esa
combinación <code>});</code> es típica de las clases anónimas pasadas como argumento.</p>
"""),
             ("public char getFichaJugador1", r"""
<p class="l"><b>L45–L47</b> <code>getFichaJugador1()</code>: la pantalla de configuración lo consulta al pulsar
«Comenzar partida» (capítulo 58) para crear los dos <code>Jugador</code>.</p>
<p class="l"><b>L49</b> <code>public void setFichaJugador1(char ficha) {</code> cambia la elección. Es
<code>public</code> para que también se pueda cambiar desde fuera (por ejemplo, si un día la pantalla quisiera
recordar la última elección).</p>
<p class="l"><b>L50</b> Guarda la nueva ficha.</p>
<p class="l"><b>L51</b> <code>repaint();</code> pide redibujar: ha cambiado qué caja brilla y lo que dice la
leyenda. Sin esta línea el dato cambiaría, pero la pantalla seguiría mostrando la elección anterior: el usuario
creería que su clic no funcionó.</p>
"""),
             ("private Rectangle caja(", r"""
<p class="l"><b>L54</b> Comentario: el método devuelve la zona de cada caja en píxeles.</p>
<p class="l"><b>L55</b> <code>private Rectangle caja(char ficha) {</code> un método <b>ayudante</b>: privado,
pensado para usarse solo aquí dentro. Lo usan dos sitios distintos, el ratón (¿dónde cayó el clic?) y el dibujo
(¿dónde pinto la caja?). Que los dos pregunten al <b>mismo</b> método garantiza que la zona que se ve y la zona que
responde al clic coinciden siempre.</p>
<p class="l"><b>L56</b> <code>int x = (getWidth() - 2 * ANCHO_CAJA - HUECO) / 2;</code> la x donde empieza la caja
X para que el par quede centrado: (434 − 240 − 34) / 2 = 160 / 2 = <b>80</b>. Se calcula con
<code>getWidth()</code>, el ancho real, y no con el 434 escrito a mano: si el tamaño cambiara, las cajas seguirían
centradas. Ojo: es una división entre enteros, así que si diera decimales se descartarían (capítulo 12).</p>
<p class="l"><b>L57–L59</b> Si se pide la caja O, se corre a la derecha el ancho de una caja más el hueco:
80 + 120 + 34 = <b>234</b>. <code>+=</code> es «súmale a lo que ya tiene».</p>
<p class="l"><b>L60</b> <code>return new Rectangle(x, 0, ANCHO_CAJA, ALTO_CAJA);</code> crea y devuelve el
rectángulo: arriba del todo (y = 0), de 120 × 98.</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L63–L64</b> <code>@Override protected void paintComponent(Graphics g)</code>: aquí se dibuja el
selector. No llamamos a <code>super.paintComponent(g)</code>: en un <code>JComponent</code> que no es opaco no hay
fondo que pintar, así que no haría nada útil.</p>
<p class="l"><b>L65</b> La copia suavizada del pincel (capítulo 41).</p>
<p class="l"><b>L66</b> <code>for (char ficha : new char[]{'X', 'O'}) {</code> un <i>for-each</i> (capítulo 14)
sobre un arreglo creado ahí mismo con dos elementos. En la primera vuelta <code>ficha</code> vale
<code>'X'</code> y en la segunda <code>'O'</code>. Es una forma corta de decir «haz esto para la X y para la O» sin
copiar la línea dos veces.</p>
<p class="l"><b>L67</b> <code>pintarCaja(g2, ficha, ficha == fichaJugador1);</code> pinta una caja. El tercer
argumento es una comparación que se evalúa a <code>true</code> o <code>false</code>: ¿esta ficha es la elegida? Con
<code>'X'</code> elegida, la caja X recibe <code>true</code> y la O <code>false</code>.</p>
"""),
             ("char fichaJugador2 =", r"""
<p class="l"><b>L70</b> <code>char fichaJugador2 = fichaJugador1 == 'X' ? 'O' : 'X';</code> la ficha del Jugador 2
es «la otra». Es una variable <b>local</b>: existe solo mientras se ejecuta este método.</p>
<p class="l"><b>L71</b> Arma la leyenda uniendo textos y caracteres con <code>+</code>. Cuando a un
<code>String</code> le sumas un <code>char</code>, el carácter se pega como letra: el resultado es «Jugador 1 juega
con X   ·   Jugador 2 con O». Cuidado: <code>'X' + 'O'</code> sin ningún texto delante <b>no</b> da «XO», da el
número 167 (la suma de sus códigos, 88 + 79), porque dos <code>char</code> se suman como números (capítulo 17).</p>
<p class="l"><b>L72</b> Fuente normal de 13 puntos.</p>
<p class="l"><b>L73</b> <code>FontMetrics fm = g2.getFontMetrics();</code> pide las medidas de la fuente que
<b>acabamos</b> de poner. Por eso va después de <code>setFont</code>: si fuera antes, mediría con la fuente
anterior.</p>
<p class="l"><b>L74</b> Color <code>TEXTO_SUAVE</code>, el lavanda apagado de los textos secundarios.</p>
<p class="l"><b>L75</b> <code>g2.drawString(leyenda, (getWidth() - fm.stringWidth(leyenda)) / 2f, getHeight() - 5);</code>
<code>fm.stringWidth(leyenda)</code> dice cuántos píxeles ocupa la frase (unos 252 en la prueba de este libro). Para
centrar algo se resta su ancho al ancho disponible y se divide entre dos: (434 − 252) / 2 = <b>91</b>. Se divide
entre <code>2f</code> (un <code>float</code>) para no perder el medio píxel si sale impar. La línea base va en
120 − 5 = <b>115</b>, cerca del borde inferior.</p>
<p class="l"><b>L76</b> Libera la copia del pincel.</p>
"""),
             ("private void pintarCaja", r"""
<p class="l"><b>L79</b> <code>private void pintarCaja(Graphics2D g2, char ficha, boolean elegida) {</code> dibuja
una caja completa. Recibe el pincel ya preparado, qué ficha es y si está elegida.</p>
<p class="l"><b>L80</b> <code>Rectangle r = caja(ficha);</code> la zona de esta caja (el mismo rectángulo que usa
el ratón).</p>
<p class="l"><b>L81</b> <code>Color color = Tema.colorDeFicha(ficha);</code> rosa para la X, azul para la O
(capítulo 40). La X es rosa la juegue quien la juegue.</p>
<p class="l"><b>L82</b> <code>RoundRectangle2D forma = new RoundRectangle2D.Double(r.x + 8, r.y + 8, r.width - 16,
r.height - 16, 20, 20);</code> la caja visible, 8 píxeles hacia adentro por cada lado para que el halo de neón quepa
dentro de la zona sin cortarse. Para la X: (88, 8) de 104 × 82, con esquinas de 20. <code>r.x</code>,
<code>r.width</code>… son campos públicos de <code>Rectangle</code> que se leen directamente.</p>
<p class="l"><b>L83</b> <code>g2.setColor(Tema.conAlfa(color, elegida ? 40 : 14));</code> el relleno: el color de
la ficha muy transparente, alfa 40 si está elegida y apenas 14 si no. Así la elegida se ve «encendida».</p>
<p class="l"><b>L84</b> Rellena la caja.</p>
<p class="l"><b>L85</b> <code>Dibujo.trazoNeon(g2, forma, color, 2f, elegida ? 1.3f : 0.4f);</code> el borde de
neón de 2 píxeles; con intensidad 1.3 brilla más de lo normal, con 0.4 se ve casi apagado (capítulo 41).</p>
"""),
             ("// La ficha no elegida", r"""
<p class="l"><b>L87</b> Comentario: la ficha no elegida se ve apagada.</p>
<p class="l"><b>L88–L90</b> Si la caja no está elegida, <code>g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, 0.5f));</code>
cambia la <b>regla de mezcla</b> del pincel. <code>SRC_OVER</code> es la regla normal, «lo nuevo encima de lo
viejo»; el <code>0.5f</code> añade una transparencia del 50&nbsp;% a <b>todo</b> lo que se dibuje a partir de ahora,
sea del color que sea. ¿Por qué no basta con usar un color transparente? Porque la ficha la dibuja
<code>Dibujo.dibujarFicha</code>, que elige sus propios colores y alfas para el halo; nosotros no le pasamos ningún
color. El <i>composite</i> afecta a todo por igual, como mirar a través de un vidrio ahumado.</p>
<p class="l"><b>L91</b> <code>double cx = r.getCenterX();</code> la x del centro de la caja: 80 + 60 =
<b>140</b> para la X. <code>getCenterX()</code> devuelve un <code>double</code>.</p>
<p class="l"><b>L92</b> <code>double cy = r.y + 8 + (r.height - 16) * 0.4;</code> la y del centro de la ficha: no
en el centro exacto de la caja sino al 40&nbsp;% de su alto, para dejar sitio abajo al botón de radio: 0 + 8 +
82 × 0,4 = <b>40,8</b>.</p>
<p class="l"><b>L93</b> <code>Dibujo.dibujarFicha(g2, ficha, cx, cy, (r.height - 16) * 0.44, 6.5f);</code> dibuja
la X o la O centrada en (140, 40,8), de 82 × 0,44 ≈ <b>36</b> píxeles y trazo de 6,5. Como el trazo pasa de 5, lleva
el centro casi blanco del «tubo» de neón (capítulo 41).</p>
<p class="l"><b>L94</b> <code>g2.setComposite(AlphaComposite.SrcOver);</code> devuelve el pincel a la normalidad
(<code>SrcOver</code> es la regla normal sin transparencia extra, ya fabricada). <b>Esta línea es crucial</b>: sin
ella, el 50&nbsp;% seguiría activo para todo lo demás. Como el bucle pinta primero la X y luego la O, si la elegida
fuera la O, su caja se pintaría también a medias y las dos se verían apagadas; y la leyenda saldría a medias
también.</p>
"""),
             ("// Boton de radio", r"""
<p class="l"><b>L96</b> Comentario: ahora el botón de radio.</p>
<p class="l"><b>L97</b> <code>double cyRadio = r.y + r.height - 8 - 15;</code> centro vertical del circulito: 98 −
8 − 15 = <b>75</b>, cerca del borde inferior de la caja visible (que termina en 90).</p>
<p class="l"><b>L98</b> <code>Ellipse2D aro = new Ellipse2D.Double(cx - 8, cyRadio - 8, 16, 16);</code> una elipse se
define por el rectángulo que la envuelve: esquina (132, 67), 16 de ancho y 16 de alto. Ancho igual a alto = círculo
de 16 de diámetro con centro en (140, 75).</p>
<p class="l"><b>L99–L100</b> Si está elegida, el aro se traza con neón del color de la ficha (grosor 2, intensidad
0,8).</p>
<p class="l"><b>L101</b> <code>Tema.aclarar(color, 0.5f)</code>: el color de la ficha mezclado a medias con blanco.
Para el rosa (255, 59, 212) da (255, 157, 234), un rosa claro que se lee como «luz».</p>
<p class="l"><b>L102</b> Rellena un círculo de 9 píxeles en el centro del aro: (140 − 4,5, 75 − 4,5) de 9 × 9. Es el
«punto» que indica que la opción está marcada.</p>
<p class="l"><b>L103–L104</b> Si no está elegida, solo un aro simple, sin halo, en lavanda transparente (alfa 120)
de 1,8 píxeles: el circulito vacío de una opción sin marcar. <code>Dibujo.trazo</code> es el trazo sin neón del
capítulo 41.</p>
<p class="l"><b>L105–L107</b> Cierran el <code>if</code>, el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>1. Un clic, paso a paso</h3>
<p>El selector está en la pantalla con la X elegida. El usuario pulsa sobre la O, en el punto (300, 60) del
selector.</p>
<ol>
<li>Swing detecta el botón hundido y, como registramos un oyente, llama a <code>mousePressed</code> con un
<code>MouseEvent</code> cuyo punto es (300, 60).</li>
<li><code>caja('X')</code> devuelve (80, 0, 120, 98): de x = 80 a x = 199. 300 no está ahí → <code>false</code>.</li>
<li><code>caja('O')</code> devuelve (234, 0, 120, 98): de 234 a 353 y de 0 a 97. (300, 60) sí está →
<code>true</code>.</li>
<li><code>setFichaJugador1('O')</code> guarda la O y llama a <code>repaint()</code>.</li>
<li>Un instante después Swing llama a <code>paintComponent</code>: la caja X se pinta apagada (alfa 14, intensidad
0,4, ficha al 50&nbsp;%, aro vacío), la O encendida, y la leyenda pasa a decir «Jugador 1 juega con O · Jugador 2 con
X».</li>
</ol>
<p>Otros clics: en (215, 50), que es el hueco entre cajas, ninguna zona lo contiene y no pasa nada. En (140, 110),
sobre la leyenda, tampoco: la zona de las cajas termina en y = 97.</p>

<h3>2. Un solo dato, todo lo demás se deduce</h3>
<table class="tabla">
<tr><th>fichaJugador1</th><th>Caja que brilla</th><th>fichaJugador2</th><th>Leyenda</th></tr>
<tr><td><code>'X'</code></td><td>X (rosa)</td><td><code>'O'</code></td><td>Jugador 1 juega con X · Jugador 2 con O</td></tr>
<tr><td><code>'O'</code></td><td>O (azul)</td><td><code>'X'</code></td><td>Jugador 1 juega con O · Jugador 2 con X</td></tr>
</table>
<p>No hay un campo «caja X encendida» ni un campo «texto de la leyenda»: si los hubiera, habría que mantenerlos
de acuerdo con <code>fichaJugador1</code> y tarde o temprano alguno quedaría desfasado. Guardar el mínimo y calcular
el resto al dibujar es una de las buenas prácticas más rentables (capítulo 27).</p>

<h3>3. Por qué una zona sirve para todo</h3>
<p><code>caja()</code> la usan el ratón y el dibujo. Imagina que el dibujo usara sus propios números y alguien
moviera las cajas 20 píxeles a la derecha solo en el dibujo: el usuario pulsaría sobre la O dibujada y el programa,
con las zonas viejas, entendería otra cosa. Con un único método, mover las cajas mueve también la zona sensible.</p>

<h2>Compila y prueba</h2>
<p><i>Run → Clean and Build Project</i> (Shift+F11) debe terminar en <code>BUILD SUCCESS</code>. El selector se verá
en la pantalla de configuración (capítulo 58); antes, con la pantalla de prueba de la vista previa del capítulo 56,
podrás pulsar las cajas y ver cómo cambian.</p>
<table class="tabla">
<tr><th>Problema</th><th>Causa y solución</th></tr>
<tr><td><i>unclosed character literal</i></td><td>Usaste comillas dobles o tipográficas en una ficha: debe ser
<code>'X'</code> con comillas simples rectas.</td></tr>
<tr><td><i>incompatible types: String cannot be converted to char</i></td><td>Escribiste <code>"X"</code> (texto)
donde va <code>'X'</code> (carácter).</td></tr>
<tr><td><i>method does not override or implement a method from a supertype</i></td><td>Error de nombre en
<code>mousePressed</code> o en su parámetro. Copia la firma exacta: <code>public void mousePressed(MouseEvent e)</code>.</td></tr>
<tr><td>(al verlo) las dos cajas se ven apagadas cuando eliges la O</td><td>Falta la línea 94, que devuelve el
<i>composite</i> a la normalidad.</td></tr>
<tr><td><i>unmappable character (0xB7) for encoding UTF-8</i></td><td>El archivo se guardó en otra codificación
(ANSI o Windows-1252) y el punto medio «·» de la línea 71 no es UTF-8 válido. Vuelve a guardarlo en UTF-8 (en NetBeans,
<i>Project Properties → Sources → Encoding</i> debe decir UTF-8).</td></tr>
</table>

<div class="caja git"><b>Git</b>
<pre class="ps">git add src\SelectorSimbolo.java
git commit -m "SelectorSimbolo: elegir X u O"
git push</pre></div>

<h2>Resumen</h2>
<ul>
<li>Para un componente que solo dibuja, se hereda de <code>JComponent</code>; para uno que contiene otros, de
<code>JPanel</code>.</li>
<li>El ratón se escucha con <code>addMouseListener</code> y una clase anónima que hereda de
<code>MouseAdapter</code>; <code>mousePressed</code> responde al instante.</li>
<li><code>Rectangle.contains(punto)</code> dice si un clic cayó en una zona (<i>hit testing</i>). Usa el mismo
método para la zona que se dibuja y la que responde.</li>
<li><code>FontMetrics.stringWidth</code> mide un texto; centrar es (disponible − ancho) / 2.</li>
<li><code>AlphaComposite</code> vuelve semitransparente todo lo que se dibuje después; siempre hay que restaurarlo
con <code>AlphaComposite.SrcOver</code>.</li>
<li>Guarda el mínimo estado (<code>fichaJugador1</code>) y deduce lo demás al dibujar.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Selectores visuales</b>: elegir la talla (S, M, L) en una tienda, el tema claro u oscuro de una aplicación
con una miniatura de cada uno, o el método de pago con su logotipo. Siempre: una caja por opción, una elegida y
el resto apagadas.</li>
<li><b>Hit testing en juegos y mapas</b>: en un Buscaminas o un Conecta 4 dibujados a mano, un
<code>Rectangle</code> por casilla y <code>contains</code> para saber cuál se pulsó; en un plano de un cine, para
saber qué butaca se eligió.</li>
<li><b>Elementos desactivados</b>: <code>AlphaComposite</code> al 40–50&nbsp;% es la forma rápida de mostrar un botón
o una opción no disponible (<code>BotonNeon</code> lo hace así cuando está deshabilitado, capítulo 44).</li>
<li><b>Texto centrado</b>: la fórmula (ancho − ancho del texto) / 2 sirve para títulos, etiquetas de botones o el
precio en una etiqueta de producto.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Si <code>HUECO</code> fuera 60, ¿en qué x empezarían las cajas X y O? Haz la cuenta con la fórmula de la línea
56 (el ancho total también cambia).</li>
<li>Cambia la leyenda para que diga «Tú: X · Rival: O». Pista: solo la línea 71.</li>
<li>Haz que <code>setFichaJugador1</code> rechace cualquier ficha que no sea <code>'X'</code> u <code>'O'</code>
lanzando <code>IllegalArgumentException</code> (capítulo 26).</li>
<li>Haz que la manito aparezca solo sobre las cajas y no sobre los huecos. Pista:
<code>addMouseMotionListener(new MouseAdapter() { ... mouseMoved(MouseEvent e) ... })</code> y, según
<code>contains</code>, <code>setCursor</code> con <code>HAND_CURSOR</code> o con <code>Cursor.getDefaultCursor()</code>.</li>
<li>Reto: agrega una tercera caja con un triángulo como ficha especial. ¿Qué tendrías que cambiar en
<code>caja()</code>, en el bucle de la línea 66 y en <code>fijarTamano</code>?</li>
</ol></div>
""",
}
