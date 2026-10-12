CAPITULO = {
    "numero": 60,
    "titulo": "PantallaResultado.java: trofeo, confeti y empate",
    "antes": r"""<p class="entrada">La partida terminó y toca celebrar: trofeo, «¡Ganó Luis!», confeti de colores y el tablero final
con su raya. O, si nadie ganó, una X y una O juntas y «¡Empate!». En este capítulo armas esa pantalla y aprendes tres
herramientas nuevas: una <b>clase dentro de otra clase</b>, el azar <b>repetible</b> con una semilla fija y
<code>AffineTransform</code>, la forma de dibujar cosas giradas.</p>

<h2>Por qué existe este archivo</h2>
<p>Terminar una partida debe sentirse como un momento, no como un letrero más. El diseño dedica una pantalla entera a
la victoria (la cuarta imagen del capítulo 34). <code>PantallaResultado</code> la reproduce, y además resuelve algo
que el diseño no traía: el <b>empate</b>, que usa la misma pantalla sin trofeo ni confeti.</p>
<figure><img src="diseno/victoria.jpg"><figcaption>El diseño de la pantalla de victoria: trofeo con destellos,
confeti, título con el nombre del ganador, una frase y el tablero final con la raya.</figcaption></figure>
<p>Como en las pantallas anteriores, casi todo son piezas ya hechas: el trofeo o la X y la O son un
<code>IconoResultado</code> (capítulo 54), los textos son <code>Rotulo</code> (46), el tablero es un
<code>PanelTablero</code> (48) y la caja es una <code>Tarjeta</code> (43). Lo único nuevo es el <b>confeti</b>, y como
solo lo usa esta pantalla, se escribe aquí mismo, en una clase pequeña metida dentro de esta.</p>
<p>Hay otra diferencia con las pantallas del menú o de instrucciones: esta pantalla <b>cambia</b> cada vez. Se construye
una sola vez, vacía, y el método <code>mostrar(partida)</code> la rellena con el resultado de cada partida que termina.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>A separar lo que se construye <b>una vez</b> (constructor) de lo que se actualiza <b>cada vez</b> (un método
<code>mostrar</code>).</li>
<li>Las <b>cláusulas de guarda</b>: salir pronto con <code>return</code> para no anidar <code>if/else</code>.</li>
<li>Clases <b>anidadas</b>: <code>private static class</code> dentro de otra clase; qué significan
<code>private</code> y <code>static</code> ahí.</li>
<li>El acceso «de paquete» (sin escribir <code>public</code> ni <code>private</code>).</li>
<li>Sobrescribir un <b>gancho</b> (<code>pintarDecoracion</code>), el patrón plantilla del capítulo 27.</li>
<li><code>java.util.Random</code> con <b>semilla fija</b>: azar que siempre sale igual, y por qué aquí es justo lo que
se quiere.</li>
<li>Generar posiciones al azar y <b>rechazar</b> las que no sirven.</li>
<li><code>AffineTransform</code>, <code>translate</code> y <code>rotate</code>: girar un dibujo y dejar todo como
estaba.</li>
</ul>

<h2>Créalo</h2>
<p>En la rama <code>interfaz-neon</code>, NetBeans: clic derecho en <i>&lt;default package&gt;</i> → <i>New → Java
Class…</i> → <code>PantallaResultado</code> → <i>Finish</i>. Borra la plantilla. Con PowerShell:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
New-Item src\PantallaResultado.java
notepad src\PantallaResultado.java</pre>
<p>La clase del confeti <b>no</b> se crea como archivo aparte: va dentro de este mismo archivo, al final.</p>
""",
    "archivos": [
        {"ruta": "src/PantallaResultado.java",
         "bloques": [
             (None, r"""<p class="l"><b>L1</b> <code>java.awt.Color</code>, para los colores del confeti y de un botón.</p>
<p class="l"><b>L2</b> <code>java.awt.Dimension</code>, para un hueco de 6 píxeles.</p>
<p class="l"><b>L3</b> <code>java.awt.Graphics2D</code>, el «pincel» con el que se dibuja el confeti (capítulo 37).</p>
<p class="l"><b>L4</b> <code>java.awt.geom.AffineTransform</code>: <b>nueva</b>. Representa una transformación del sistema
de coordenadas (mover, girar, escalar). Aquí se usa para guardar «cómo estaba» el pincel antes de girarlo y poder
devolverlo a su sitio.</p>
<p class="l"><b>L5</b> <code>java.awt.geom.RoundRectangle2D</code>: un rectángulo de esquinas redondeadas. Cada papelito de
confeti es uno, pequeñito.</p>
<p class="l"><b>L6</b> <code>java.util.Random</code>: <b>nueva</b>. El generador de números al azar de Java. Está en
<code>java.util</code> (utilidades generales), no en Swing ni en AWT, porque no tiene nada que ver con gráficos: sirve
igual para barajar cartas o elegir un ganador de una rifa.</p>"""),
             ("import javax.swing.BorderFactory", r"""<p class="l"><b>L7–L9</b> Los tres de Swing que ya conoces del
capítulo 57: <code>BorderFactory</code> (márgenes), <code>Box</code> (huecos) y <code>BoxLayout</code> (columna).</p>
<p class="l"><b>L10</b> En blanco.</p>"""),
             ("public class PantallaResultado", r"""<p class="l"><b>L11–L15</b> El comentario dice qué pantalla del diseño es
(la 4), qué muestra y que también sirve para el empate. El texto de ejemplo, «¡Ganó Jugador 2!», es el del diseño.</p>
<p class="l"><b>L16</b> Hereda de <code>PantallaBase</code>: fondo, encabezado y métodos para apilar.</p>
<p class="l"><b>L17</b> En blanco.</p>"""),
             ("private static final int ANCHO_INTERIOR", r"""<p class="l"><b>L18</b> El ancho del título y de la frase, 440
píxeles. Como la tarjeta tiene 20 de margen a cada lado (L30), mide 440 + 40 = <b>480</b> de ancho. Es una constante
porque la usan dos componentes que deben alinearse.</p>
<p class="l"><b>L19</b> En blanco.</p>"""),
             ("private final IconoResultado icono", r"""<p class="l">Estos cinco atributos son las piezas que <b>cambian</b> con
cada resultado. Por eso son atributos (el método <code>mostrar</code> los tocará después) y se crean en su declaración,
antes del constructor.</p>
<p class="l"><b>L20</b> La ilustración de arriba: trofeo con destellos o X y O (capítulo 54).</p>
<p class="l"><b>L21</b> El título grande. Se crea vacío (<code>""</code>) con colores cian a azul, los del diseño;
<code>mostrar</code> pondrá el texto y los colores reales. 40 de letra, 440 × 54 píxeles. Si el nombre del ganador es muy
largo, el <code>Rotulo</code> achica la letra solo hasta que quepa (capítulo 46).</p>
<p class="l"><b>L22</b> La frase de debajo («Excelente jugada»), creada con <code>Rotulo.leyenda</code>: texto entre dos
líneas que se desvanecen.</p>
<p class="l"><b>L23</b> El tablero final, con casillas de 66 píxeles: 2 × 18 + 3 × 66 = 234 de lado. Más chico que el
de la partida (100) y más grande que el del ejemplo de instrucciones (46).</p>
<p class="l"><b>L24</b> La tarjeta. Su tipo no es <code>Tarjeta</code> sino <code>TarjetaConConfeti</code>, la clase que
se define al final de este mismo archivo (L79). Java permite usarla aquí arriba aunque esté escrita más abajo: dentro de
una clase, el orden de los miembros no importa para encontrarlos.</p>
<p class="l"><b>L25</b> En blanco.</p>"""),
             ("public PantallaResultado(", r"""<p class="l"><b>L26</b> El constructor recibe la navegación.</p>
<p class="l"><b>L27</b> Construye la base. A diferencia de <code>PantallaJuego</code>, aquí la navegación <b>no</b> se
guarda en un atributo: solo la usan las lambdas de los botones, que la recuerdan solas (capítulo 57).</p>
<p class="l"><b>L28</b> En blanco.</p>"""),
             ("tarjeta.setLayout(", r"""<p class="l"><b>L29</b> La tarjeta organiza su contenido en columna.</p>
<p class="l"><b>L30</b> Margen interior: 14 arriba, 20 a la izquierda, 18 abajo, 20 a la derecha.</p>
<p class="l"><b>L31–L33</b> De arriba abajo: ilustración, título y frase. Sin huecos entre ellos: cada componente trae su
propio alto calculado para que respiren.</p>
<p class="l"><b>L34</b> 6 píxeles antes del tablero.</p>
<p class="l"><b>L35</b> El tablero. Como no se le pone oyente ni se marca interactivo, es solo de muestra: no acepta clics.</p>
<p class="l"><b>L36</b> En blanco.</p>"""),
             ("BotonNeon jugarDeNuevo", r"""<p class="l"><b>L37–L38</b> «Jugar de nuevo»: píldora de rosa a morado, con el icono
de reiniciar, de 290 × 72. Es la acción que más se espera después de una partida, así que lleva el degradado más
llamativo.</p>
<p class="l"><b>L39</b> Pide a la navegación otra partida con los mismos jugadores y el marcador acumulado (capítulo 61).</p>
<p class="l"><b>L40–L41</b> «Menú principal»: píldora de azul a un azul índigo escrito ahí mismo,
<code>new Color(0x3A, 0x3F, 0xC8)</code>. Es el único color de todo el proyecto que no sale de <code>Tema</code>: el
diseño pedía un azul más profundo solo en este botón. Si se usara en más sitios, lo correcto sería darle nombre en
<code>Tema</code> (ejercicio 1). <code>0x3A</code> es un número en hexadecimal (capítulo 35): 58.</p>
<p class="l"><b>L42</b> Vuelve al menú.</p>
<p class="l"><b>L43</b> En blanco.</p>"""),
             ("relleno();", r"""<p class="l"><b>L44–L48</b> Resorte, tarjeta, 6 píxeles, la fila con los dos botones (6 píxeles
entre ellos) y resorte: el conjunto queda centrado en vertical.</p>
<p class="l"><b>L49</b> Fin del constructor. En este momento la pantalla existe pero está «en blanco»: título vacío,
tablero vacío. Todavía no ha terminado ninguna partida. <b>L50</b> En blanco.</p>"""),
             ("public void mostrar(Partida partida)", r"""<p class="l"><b>L51</b> Comentario: el método prepara la pantalla para la
partida que <b>acaba</b> de terminar.</p>
<p class="l"><b>L52</b> <code>public</code> porque lo llama el <code>PanelPrincipal</code> (capítulo 61) justo antes de
mostrar esta pantalla. Recibe la partida terminada.</p>
<p class="l"><b>L53</b> El tablero copia las fichas finales y encuentra la línea ganadora; por eso la raya sale sola.</p>
<p class="l"><b>L54</b> <code>empate</code> es <code>true</code> si el estado es <code>EMPATE</code>. Se guarda en una
variable porque se usa tres veces y así se lee mejor.</p>
<p class="l"><b>L55</b> La ilustración: X y O si es empate; trofeo si no.</p>
<p class="l"><b>L56</b> El confeti: <code>!empate</code> («no empate») es <code>true</code> cuando alguien ganó. Un solo
dato decide las dos cosas.</p>
<p class="l"><b>L57</b> En blanco.</p>"""),
             ("if (empate) {", r"""<p class="l"><b>L58</b> Si fue empate…</p>
<p class="l"><b>L59</b> …el título dice «¡Empate!» con un degradado de lavanda a morado (los colores «neutrales» del
Totito: no son ni de la X ni de la O).</p>
<p class="l"><b>L60</b> La frase. Se usa la versión de <code>setTexto</code> con un solo argumento: solo el texto, porque
las leyendas siempre van en lavanda.</p>
<p class="l"><b>L61</b> <code>return;</code> sale del método aquí. Es una <b>cláusula de guarda</b>: el caso especial se
resuelve arriba y se termina, y el resto del método trata el caso normal sin necesidad de un <code>else</code> que lo
envuelva. Sin este <code>return</code>, el código seguiría a la L63, buscaría al ganador (que no existe en un empate) y
fallaría con un <code>NullPointerException</code>.</p>
<p class="l"><b>L62</b> Cierra el <code>if</code>.</p>"""),
             ("Jugador ganador =", r"""<p class="l"><b>L63</b> Aquí ya sabemos que alguien ganó: se pide el ganador a la partida.</p>
<p class="l"><b>L64</b> Su color: rosa si ganó con X, azul si ganó con O. Es la línea que fallaría si se llamara a
<code>mostrar</code> con una partida sin ganador; recuerda el experimento del capítulo 59.</p>
<p class="l"><b>L65</b> El título: <code>"¡Ganó " + nombre + "!"</code>, con degradado del color aclarado al color puro.
Con «Luis», que jugó con la O, sale «¡Ganó Luis!» en azul, como en el diseño.</p>"""),
             ("if (partida.esComputadora(ganador))", r"""<p class="l"><b>L66–L67</b> Si ganó la computadora:
«La máquina no perdona».</p>
<p class="l"><b>L68–L69</b> Si no ganó la computadora pero el modo es contra la IA, entonces ganó la persona:
«¡Le ganaste a la máquina!». Con la IA Minimax del capítulo 31 esta frase prácticamente <b>nunca</b> se verá, porque esa
IA no pierde. Aun así el caso se programa: el código debe ser correcto para todas las situaciones posibles, no solo para
las probables. Si un día haces la IA más débil (capítulo 68), la frase ya estará lista.</p>
<p class="l"><b>L70–L72</b> Si no, fue una partida entre dos personas: «Excelente jugada», la frase del diseño.</p>
<p class="l">El orden de las preguntas importa: primero «¿ganó la máquina?», luego «¿era contra la máquina?». Al revés,
una victoria de la computadora diría «¡Le ganaste a la máquina!».</p>
<p class="l"><b>L73–L74</b> Cierre del método y línea en blanco.</p>"""),
             ("private static class TarjetaConConfeti", r"""<p class="l"><b>L75–L78</b> El comentario de la clase del confeti
explica su truco principal: las posiciones salen de un <code>Random</code> con semilla fija, y por eso no «bailan» al
repintar. Lo entenderás en «Cómo funciona por dentro».</p>
<p class="l"><b>L79</b> Una clase <b>dentro</b> de otra (clase anidada, capítulo 25). Palabra por palabra:</p>
<ul>
<li><code>private</code>: solo la puede usar <code>PantallaResultado</code>. Para el resto del proyecto, no existe. Es
lo correcto: nadie más necesita confeti, y así no ensucia la lista de clases.</li>
<li><code>static</code>: la clase anidada no necesita un objeto <code>PantallaResultado</code> para existir ni guarda
una referencia oculta a él. Una clase anidada <b>sin</b> <code>static</code> (una «clase interna») sí la guarda, y
puede usar los atributos de la de fuera. Aquí no hace falta, así que se pone <code>static</code>: es más simple y más
barata. Regla práctica: las clases anidadas, <code>static</code> salvo que necesites lo contrario.</li>
<li><code>extends Tarjeta</code>: es una tarjeta de cristal normal (capítulo 43) con algo más.</li>
</ul>
<p class="l"><b>L80</b> En blanco.</p>"""),
             ("private static final Color[] COLORES", r"""<p class="l"><b>L81</b> Un arreglo (capítulo 15) constante con los tres colores
del confeti: rosa, cian y morado. Está aquí y no en <code>Tema</code> porque es la «receta» del confeti, no un color
nuevo: los tres ya existen en el tema.</p>
<p class="l"><b>L82</b> Si hay que dibujar confeti. Empieza en <code>true</code>. No es <code>final</code> porque cambia
con cada resultado.</p>
<p class="l"><b>L84</b> El constructor de la clase anidada. No lleva <code>public</code> ni <code>private</code>: es acceso
<b>de paquete</b>, el que Java pone cuando no escribes nada (visible para las clases del mismo paquete). Como la clase ya
es <code>private</code>, en la práctica solo lo usa <code>PantallaResultado</code>, que además puede usar los miembros de
sus clases anidadas sea cual sea su modificador. Escribir <code>public</code> no añadiría nada.</p>
<p class="l"><b>L85</b> Llama al constructor de <code>Tarjeta</code> con el color morado del borde.</p>
<p class="l"><b>L86–L87</b> Cierre y línea en blanco.</p>"""),
             ("void setConConfeti", r"""<p class="l"><b>L88</b> Método para activar o desactivar el confeti; también de paquete.</p>
<p class="l"><b>L89</b> Guarda el valor. <code>this.conConfeti</code> es el atributo; <code>conConfeti</code>, el parámetro.</p>
<p class="l"><b>L90</b> <code>repaint()</code> pide a Swing que vuelva a dibujar la tarjeta: sin esta línea, si la pantalla
ya estaba a la vista, el confeti no aparecería o desaparecería hasta el siguiente repintado por otra causa.</p>
<p class="l"><b>L91–L92</b> Cierre y línea en blanco.</p>"""),
             ("protected void pintarDecoracion", r"""<p class="l"><b>L93</b> <code>@Override</code>: el método siguiente
sustituye a uno de la clase madre. Si te equivocas en el nombre o en los parámetros, el compilador avisa
(capítulo 23).</p>
<p class="l"><b>L94</b> <code>pintarDecoracion</code> es el <b>gancho</b> que <code>Tarjeta</code> dejó preparado en el
capítulo 43. Su <code>paintComponent</code> hace siempre lo mismo: rellena el cristal, llama a
<code>pintarDecoracion</code> y dibuja el borde de neón. En <code>Tarjeta</code> el gancho está vacío; aquí se rellena con
confeti. Es el patrón <b>plantilla</b> (capítulo 27): la madre fija los pasos y la hija completa uno. Recibe el pincel
ya preparado y la forma de la caja (para saber dónde dibujar). Como se llama <b>antes</b> de que Swing dibuje los
componentes hijos, el confeti queda <b>debajo</b> del trofeo, el título y el tablero.</p>
<p class="l"><b>L95–L97</b> Guarda: si no hay confeti (empate), se sale sin dibujar nada.</p>"""),
             ("Random azar = new Random(11);", r"""<p class="l"><b>L98</b> Crea un generador de números al azar con
<b>semilla</b> 11. Una computadora no puede tirar dados: <code>Random</code> calcula una sucesión de números que
<b>parecen</b> al azar a partir de un número inicial, la semilla. Con la misma semilla, la sucesión es siempre la misma,
en cualquier computadora. Con <code>new Random()</code> sin semilla, Java elige una distinta cada vez. El 11 no tiene nada
especial: se probaron varias y con esta el confeti quedaba bonito.</p>
<p class="l">Y se crea <b>dentro</b> del método, en cada dibujo, no como atributo: así cada vez que Swing repinta la
tarjeta, la sucesión empieza desde el principio y los papelitos caen exactamente en el mismo sitio.</p>
<p class="l"><b>L99</b> La coordenada x del centro de la caja.</p>
<p class="l"><b>L100</b> Un contador de papelitos ya dibujados.</p>
<p class="l"><b>L101</b> <code>while (colocados &lt; 22)</code>: repetir hasta tener 22 papelitos (capítulo 14). Se usa
<code>while</code> y no <code>for</code> porque no se sabe cuántas vueltas hacen falta: algunos intentos se descartan.</p>"""),
             ("double x = forma.getX()", r"""<p class="l"><b>L102</b> Una x al azar dentro de la caja.
<code>azar.nextDouble()</code> da un número entre 0 (incluido) y 1 (sin incluir). Multiplicado por el ancho menos 36,
da algo entre 0 y ese ancho; sumado al borde izquierdo más 18, queda dentro de la caja con 18 píxeles de margen a cada
lado, para que ningún papelito toque el borde de neón.</p>
<p class="l"><b>L103</b> Lo mismo para la y, con 16 píxeles de margen arriba y abajo.</p>
<p class="l"><b>L104</b> El comentario explica la regla: solo vale arriba (alrededor del trofeo) o a los lados del
tablero.</p>
<p class="l"><b>L105</b> <code>libre</code>: el punto está en la franja de arriba (los primeros 100 píxeles de la caja)
<b>o</b> lejos del centro en horizontal (más de 135 píxeles a un lado u otro). <code>Math.abs</code> da el valor absoluto:
la distancia sin signo, valga lo mismo a la izquierda que a la derecha. El tablero mide 234, o sea 117 a cada lado del
centro; 135 deja aire.</p>
<p class="l"><b>L106</b> <code>sobreTrofeo</code>: el punto está en la zona del trofeo (arriba y a menos de 60 píxeles del
centro). Ahí no se quiere confeti aunque esté «arriba».</p>"""),
             ("double angulo = ", r"""<p class="l"><b>L107</b> Un ángulo al azar entre 0 y <code>Math.PI</code>. Java mide los
ángulos en <b>radianes</b>: π radianes son 180°. ¿Por qué no hasta 360°? Porque un rectángulo girado 180° se ve igual que
sin girar: con medio giro ya salen todas las inclinaciones posibles.</p>
<p class="l"><b>L108</b> Un color al azar: <code>azar.nextInt(3)</code> da 0, 1 o 2, y se usa como índice del arreglo.
Escribir <code>COLORES.length</code> en lugar de 3 hace que, si agregas un cuarto color al arreglo, se use sin tocar
esta línea.</p>
<p class="l"><b>L109–L111</b> Si el punto no está libre o cae sobre el trofeo, <code>continue</code>: salta al principio
del <code>while</code> sin dibujar nada ni sumar al contador, y se intenta otra posición. Esta técnica se llama
<b>muestreo por rechazo</b>: generar al azar y quedarse solo con lo que cumple. Fíjate en que el ángulo y el color se
sacan <b>antes</b> del <code>continue</code>: cada intento consume siempre cuatro números del generador. No es
obligatorio, pero hay que mantener ese orden: si lo cambias, la sucesión se reparte distinto y el confeti cambia de
lugar (seguirá fijo, pero en otra posición).</p>"""),
             ("AffineTransform previo", r"""<p class="l"><b>L112</b> <code>g2.getTransform()</code> devuelve una
<b>copia</b> de la transformación actual del pincel: «dónde está ahora el origen (0,0) y cómo están girados los ejes».
Se guarda para poder volver a ella.</p>
<p class="l"><b>L113</b> <code>translate(x, y)</code> mueve el origen al punto elegido. A partir de aquí, «(0,0)» significa
el centro del papelito.</p>
<p class="l"><b>L114</b> <code>rotate(angulo)</code> gira los ejes alrededor de ese nuevo origen. En la pantalla (donde la
y crece hacia abajo) el giro va en el sentido de las agujas del reloj. El orden importa: primero mover y luego girar hace
que el papelito gire sobre sí mismo. Al revés, giraría alrededor de la esquina de la tarjeta, como un columpio, y saldría
disparado lejos.</p>
<p class="l"><b>L115</b> El papelito: un rectángulo redondeado de 7 × 14 píxeles cuya esquina está en (−3,5, −7), o sea,
<b>centrado</b> en el origen. Los dos últimos números (3, 3) son el redondeo de las esquinas. Gracias a la
transformación, se describe siempre «recto y en (0,0)», y Java se encarga de colocarlo y girarlo.</p>
<p class="l"><b>L116</b> Color del halo: el del papelito con transparencia 45 de 255 (muy tenue; capítulo 40,
<code>conAlfa</code>).</p>"""),
             ("g2.fill(new RoundRectangle2D.Double(-6", r"""<p class="l"><b>L117</b> Dibuja el halo: un rectángulo un poco más
grande (12 × 19), también centrado, muy transparente. Es el «neón» del papelito, hecho con la misma idea que los trazos
del capítulo 41: una forma ancha y tenue detrás de una fina y fuerte.</p>
<p class="l"><b>L118–L119</b> Encima, el papelito casi opaco (220 de 255).</p>
<p class="l"><b>L120</b> <code>setTransform(previo)</code> devuelve el pincel a como estaba. <b>Imprescindible.</b> Sin
esta línea, el siguiente <code>translate</code> se sumaría al anterior (ya movido y girado) y los papelitos se irían
desperdigando en espiral fuera de la tarjeta. Y hay algo peor: este mismo pincel lo usa <code>Tarjeta</code> justo después
para dibujar el borde de neón, que saldría movido y girado.</p>
<p class="l"><b>L121</b> Un papelito más. Esta línea solo se alcanza si el intento no se descartó.</p>
<p class="l"><b>L122–L125</b> Cierran el <code>while</code>, el método, la clase anidada y la clase
<code>PantallaResultado</code>.</p>"""),
         ]},
    ],
    "despues": r"""<h2>Cómo funciona por dentro</h2>
<h3>Una pantalla, muchos resultados</h3>
<p>El <code>PanelPrincipal</code> crea esta pantalla <b>una sola vez</b>, al arrancar el juego. Cada vez que termina una
partida, llama a <code>mostrar(partida)</code> y luego la hace visible. Así, con Luis ganando con la O en modo de dos
personas, <code>mostrar</code> deja: el tablero con la raya azul en la fila de arriba, el trofeo, el confeti activado,
el título «¡Ganó Luis!» de azul claro a azul y la frase «Excelente jugada». Si la siguiente partida es un empate,
el mismo objeto pasa a mostrar X y O, sin confeti, «¡Empate!» y «Nadie cedió ni una casilla». No se crea nada nuevo.</p>
<h3>El confeti, intento por intento</h3>
<p>Medimos la tarjeta en el juego real: el componente mide 480 × 458 píxeles, y la caja (descontando el margen de 10 del
halo) empieza en (10, 10) y mide 460 × 438. Su centro está en x = 240. Así van los primeros intentos con la semilla 11:</p>
<table class="tabla">
<tr><th>Intento</th><th>x</th><th>y</th><th>¿libre?</th><th>¿sobre el trofeo?</th><th>Resultado</th></tr>
<tr><td>1</td><td>337,7</td><td>199,5</td><td>no: y no es menor que 110 y |337,7 − 240| = 97,7 no pasa de 135</td><td>no</td>
<td>descartado (caería sobre el tablero)</td></tr>
<tr><td>2</td><td>413,9</td><td>142,1</td><td>sí: |413,9 − 240| = 173,9 &gt; 135</td><td>no (y no es menor que 130)</td>
<td><b>papelito 1</b>: morado, girado unos 99°</td></tr>
<tr><td>3</td><td>312,1</td><td>170,2</td><td>no</td><td>no</td><td>descartado</td></tr>
<tr><td>4</td><td>248,5</td><td>394,5</td><td>no</td><td>no</td><td>descartado</td></tr>
</table>
<p>Para colocar los 22 papelitos hacen falta <b>51 intentos</b>. Y siempre los mismos 51, con los mismos resultados,
porque la semilla es fija. Puedes comprobar que la sucesión no cambia en <code>jshell</code> (capítulo 11):</p>
<pre class="salida">jshell&gt; new java.util.Random(11).nextDouble()
$1 ==&gt; 0.7303407149712222

jshell&gt; new java.util.Random(11).nextDouble()
$2 ==&gt; 0.7303407149712222</pre>
<p>Ese 0,7303… es el primer número de la sucesión: 10 + 18 + 0,7303 × (460 − 36) = 337,7, la x del intento 1.</p>
<h3>Por qué la semilla fija</h3>
<p><code>paintComponent</code> no se llama una vez: Swing lo llama cada vez que hace falta redibujar esa zona (cuando la
ventana vuelve de estar minimizada, cuando otra ventana pasa por encima, cuando <code>setConConfeti</code> pide
<code>repaint()</code>…). Si el generador no tuviera semilla fija, cada repintado sacaría posiciones nuevas y el confeti
saltaría de un lado a otro sin motivo. Con semilla fija, el dibujo es una <b>función</b> de la caja: misma caja, mismo
confeti. Es una idea útil en general: <b>lo que se dibuja debe depender solo del estado</b>, no del momento en que se
dibuja.</p>
<h3>La transformación, paso a paso</h3>
<p>Para el papelito 1 (x = 413,9; y = 142,1; ángulo ≈ 1,74 radianes): <code>translate(413.9, 142.1)</code> lleva el origen a
ese punto; <code>rotate(1.74)</code> gira los ejes unos 99°; el rectángulo «recto en (0,0)» se dibuja, por tanto, centrado
en (413,9; 142,1) y casi vertical; <code>setTransform(previo)</code> devuelve el origen a la esquina de la tarjeta para el
siguiente. Es como dibujar en una hoja que giras con la mano: giras, dibujas recto, y vuelves a enderezar la hoja.</p>
<div class="caja cuidado"><b>Un <code>while</code> que depende del azar debe poder terminar</b> El bucle solo termina si
alguna posición resulta válida. Con la tarjeta de verdad (460 × 438) ocurre tras 51 intentos. Pero en una prueba
dibujamos la tarjeta con tamaño cero y el bucle no terminó nunca: todas las posiciones caían «sobre el trofeo». En el
juego eso no pasa, porque Swing no pinta componentes sin tamaño, pero una versión más robusta pondría también un tope
de intentos (ejercicio 4). Cada vez que escribas un bucle de «intentar hasta que salga», pregúntate: ¿y si nunca sale?</div>

<h2>Compila y prueba</h2>
<p>Compila con <i>Clean and Build</i> (Shift+F11). Para verla en la vista previa necesitas una partida terminada, así que
la línea <code>AQUI</code> se convierte en seis: se juega una partida «a mano» con <code>Partida</code> (Ana con X, Luis con
O; Luis hace tres en línea arriba) y se le pasa a la pantalla. Sustituye la línea 31 de
<code>herramientas/VistaPrevia.java</code> por:</p>
<pre class="java">            Partida demo = new Partida(new Jugador("Ana", 'X'), new Jugador("Luis", 'O'), Partida.Modo.DOS_JUGADORES);
            demo.jugar(1, 0); demo.jugar(0, 0); demo.jugar(1, 2);
            demo.jugar(0, 1); demo.jugar(2, 1); demo.jugar(0, 2);
            PantallaResultado resultado = new PantallaResultado(sinNavegacion);
            resultado.mostrar(demo);
            JPanel pantalla = resultado;   // &lt;-- AQUI</pre>
<p>Las jugadas se alternan solas (la <code>Partida</code> lleva el turno): X en (1,0), O en (0,0), X en (1,2), O en (0,1),
X en (2,1) y O en (0,2), que completa la fila de arriba. Lanza la vista previa:</p>
<pre class="ps">java -cp target\classes herramientas\VistaPrevia.java</pre>
<p>Debes ver la misma pantalla del diseño: trofeo con destellos, confeti rosa, cian y morado alrededor (nunca sobre el
tablero ni sobre el trofeo), «¡Ganó Luis!» en azul, «Excelente jugada» y la raya azul. Cierra la ventana y vuelve a
abrirla: el confeti está <b>exactamente</b> en el mismo sitio. Minimízala y restáurala: tampoco se mueve.</p>
<p>Para probar el empate, cambia las jugadas por estas nueve, que llenan el tablero sin tres en línea:</p>
<pre class="java">            demo.jugar(0, 0); demo.jugar(0, 1); demo.jugar(0, 2);
            demo.jugar(1, 1); demo.jugar(1, 0); demo.jugar(1, 2);
            demo.jugar(2, 1); demo.jugar(2, 0); demo.jugar(2, 2);</pre>
<p>Ahora deben salir la X y la O juntas, «¡Empate!» en lavanda, «Nadie cedió ni una casilla» y ningún papelito.</p>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Síntoma</th><th>Causa probable</th><th>Solución</th></tr>
<tr><td>El confeti cambia de sitio al minimizar y restaurar.</td><td>El <code>Random</code> se creó sin semilla o como
atributo.</td><td>Créalo dentro de <code>pintarDecoracion</code> con <code>new Random(11)</code>.</td></tr>
<tr><td>Los papelitos salen fuera de la tarjeta o el borde de neón aparece torcido.</td><td>Falta
<code>g2.setTransform(previo)</code>.</td><td>Agrega la L120.</td></tr>
<tr><td>No sale ningún confeti.</td><td>El método se llama distinto que el de <code>Tarjeta</code> (sin
<code>@Override</code> no te enteras).</td><td>Pon <code>@Override</code> y copia la firma exacta: <code>protected void
pintarDecoracion(Graphics2D g2, RoundRectangle2D forma)</code>.</td></tr>
<tr><td>En un empate aparece un <code>NullPointerException</code>.</td><td>Falta el <code>return;</code> de la L61.</td>
<td>Agrégalo.</td></tr>
<tr><td>La ventana se queda congelada al mostrar el resultado.</td><td>El <code>while</code> no termina: cambiaste las
condiciones de la L105–L106 y ninguna posición es válida.</td><td>Revisa las condiciones; agrega un tope de intentos.</td></tr>
</table>

<div class="caja git"><b>Git</b> Devuelve la vista previa a su estado y sube la pantalla:
<pre class="ps">git restore herramientas\VistaPrevia.java
git add src\PantallaResultado.java
git commit -m "PantallaResultado: victoria, empate y confeti"
git push
git log --oneline -3</pre></div>

<h2>Resumen</h2>
<ul>
<li><code>PantallaResultado</code> se construye una vez y <code>mostrar(partida)</code> la rellena con cada resultado:
victoria (trofeo, confeti, nombre del ganador) o empate (X y O, sin confeti).</li>
<li>Una cláusula de guarda (<code>if (empate) { …; return; }</code>) resuelve el caso especial y deja el resto plano.</li>
<li><code>TarjetaConConfeti</code> es una clase anidada <code>private static</code>: solo existe para esta pantalla y no
necesita un objeto de la clase de fuera.</li>
<li>Sobrescribe el gancho <code>pintarDecoracion</code> de <code>Tarjeta</code> (patrón plantilla).</li>
<li><code>new Random(11)</code> da siempre la misma sucesión: el confeti no «baila» al repintar.</li>
<li>Muestreo por rechazo: generar posiciones al azar y quedarse con las válidas (22 papelitos en 51 intentos).</li>
<li><code>translate</code> + <code>rotate</code> dibujan girado; <code>getTransform</code>/<code>setTransform</code> dejan el
pincel como estaba.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Azar repetible para probar:</b> en un juego de cartas, <code>new Random(semilla)</code> te deja repetir exactamente
la misma baraja para reproducir un error. En simulaciones (colas de un banco, ventas de una tienda), la semilla hace que
los resultados se puedan comparar entre versiones del programa.</li>
<li><b>Fondos y decoraciones generadas:</b> estrellas en el cielo de un juego, manchas en un fondo, árboles en un mapa:
todo «al azar», pero estable al repintar, con una semilla fija.</li>
<li><b>Dibujar girado:</b> la aguja de un velocímetro o de una brújula, las manecillas de un reloj analógico, las letras
de un texto en curva: <code>translate</code> al centro, <code>rotate</code>, dibujar recto, restaurar.</li>
<li><b>Clases anidadas privadas:</b> un componente pequeño que solo usa una pantalla (una fila especial de una tabla, una
celda con icono) puede vivir dentro de ella en lugar de en un archivo aparte.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Lleva el azul índigo del botón «Menú principal» (L41) a <code>Tema</code> con el nombre <code>INDIGO</code> y úsalo
desde ahí. ¿Por qué es mejor así?</li>
<li>Cambia la semilla 11 por otros números (1, 7, 2024) y mira el resultado en la vista previa. ¿Cambia la cantidad de
papelitos? ¿Y su posición? Explica por qué.</li>
<li>Pon 40 papelitos en vez de 22 y agrega <code>Tema.AZUL</code> al arreglo de colores. ¿Qué otra línea tuviste que
tocar para el color? (Pista: ninguna, gracias a <code>COLORES.length</code>.)</li>
<li>Agrega un tope: que el <code>while</code> se detenga también si lleva 500 intentos, aunque no haya colocado los 22.
Pista: una variable <code>intentos</code> y la condición <code>colocados &lt; 22 &amp;&amp; intentos &lt; 500</code>.</li>
<li>Reto: haz que en el empate se vean papelitos solo en lavanda y morado, más pocos (10). ¿Qué tienes que cambiar en
<code>mostrar</code> y en <code>TarjetaConConfeti</code>?</li>
</ol></div>
""",
}
