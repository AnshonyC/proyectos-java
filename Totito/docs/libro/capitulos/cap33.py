# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 33,
    "titulo": "JuegoMain.java: la primera ventana",
    "antes": r"""
<p class="entrada">Llegó el momento de jugar con el ratón. En este capítulo construyes una ventana con Swing, la biblioteca gráfica que trae Java: nueve botones en una rejilla, un letrero que dice de quién es el turno y un botón para reiniciar. Por dentro, la ventana no sabe ninguna regla: se las pregunta a <code>Tablero</code> y le pide las jugadas a <code>IA_Minimax</code>. Al terminar tendrás el <b>Totito v0.1</b>, el primer programa completo del libro.</p>

<h2>Por qué existe este archivo</h2>
<p>Las tres clases de lógica funcionan, pero nadie quiere jugar escribiendo coordenadas. Falta la parte que una persona ve y toca: la <b>interfaz gráfica</b>. <code>JuegoMain</code> tiene dos trabajos, que en el capítulo 28 decidimos dejar juntos por ser la primera ventana:</p>
<ul>
<li><b>Vista</b>: construye la ventana, los botones y el letrero, y los actualiza (pone una X, cambia el mensaje, desactiva casillas).</li>
<li><b>Controlador</b>: dirige la partida. Sabe de quién es el turno, recibe los clics, llama a <code>Tablero</code> para marcar y comprobar el final, y le pide su jugada a la IA.</li>
</ul>
<p>Es, además, el <b>punto de entrada</b> de la versión 0.1: tiene el método <code>main</code> que arranca todo. Su diseño es deliberadamente sencillo, gris y blanco, sin dibujos: aquí importa que el juego funcione. En la Parte VII construirás una interfaz nueva, la neón, con otras clases (<code>Partida</code> se quedará con el papel de controlador y varias pantallas con el de vista); <code>JuegoMain</code> <b>no se borra</b>: se conserva en el proyecto como la versión sencilla, y se podrá seguir abriendo siempre.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>A crear una ventana heredando de <code>JFrame</code> (<code>extends</code> y <code>super</code>, capítulo 22).</li>
<li>Los componentes básicos de Swing: <code>JButton</code>, <code>JLabel</code> y <code>JPanel</code>, y una matriz de botones <code>JButton[3][3]</code> paralela a la matriz del tablero.</li>
<li>Dos administradores de diseño (<i>layouts</i>): <code>BorderLayout</code> (norte, centro, sur) y <code>GridLayout</code> (rejilla de 3×3).</li>
<li>A usar colores (<code>Color</code> con valores hexadecimales), fuentes (<code>Font</code>), bordes y márgenes (<code>BorderFactory</code>).</li>
<li>A reaccionar a los clics con <code>ActionListener</code> escrito como lambda (capítulo 25), y por qué hacen falta las variables <code>final int f</code> y <code>c</code>.</li>
<li>A esperar sin congelar la ventana con un <code>Timer</code> de Swing de 350 milisegundos.</li>
<li>El operador ternario <code>? :</code> y <code>SwingUtilities.invokeLater</code> para arrancar Swing en su hilo.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>En NetBeans: clic derecho sobre <i>Source Packages → &lt;default package&gt;</i> → <i>New → Java Class…</i></li>
<li><i>Class Name</i>: <code>JuegoMain</code> → <i>Finish</i>.</li>
<li>Borra la plantilla, escribe el archivo y guarda con Ctrl+S.</li>
</ol>
<pre class="ps">cd $HOME\Proyectos\Totito
New-Item src\JuegoMain.java</pre>
<div class="caja concepto"><b>Swing en dos frases</b> Swing es la biblioteca de Java para ventanas de escritorio: viene incluida en el JDK (paquete <code>javax.swing</code>), así que no hay que instalar nada. Una interfaz Swing es un árbol de <b>componentes</b> (botones, letreros) metidos en <b>contenedores</b> (paneles, ventanas), y cada contenedor reparte su espacio según su <i>layout</i>. En el capítulo 37 verás cómo dibuja Swing por dentro; aquí basta con usar sus piezas.</div>
""",
    "archivos": [
        {"ruta": "src/JuegoMain.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> Importa <b>todas</b> las clases del paquete <code>javax.swing</code>: el asterisco significa «todas las de este paquete». Usaremos <code>JFrame</code>, <code>JButton</code>, <code>JLabel</code>, <code>JPanel</code>, <code>BorderFactory</code>, <code>SwingConstants</code>, <code>SwingUtilities</code> y <code>Timer</code>; importarlas una por una serían ocho líneas. El asterisco no hace el programa más lento ni más grande: solo le dice al compilador dónde buscar.</p>
<p class="l"><b>L2</b> Importa todas las clases de <code>java.awt</code>, la biblioteca gráfica más antigua sobre la que se apoya Swing. De ahí salen <code>Color</code>, <code>Font</code>, <code>Dimension</code>, <code>BorderLayout</code> y <code>GridLayout</code>.</p>
<p class="l"><b>L3</b> Importa una sola clase, <code>ActionEvent</code>, del subpaquete <code>java.awt.event</code>. Hay que importarla aparte porque el asterisco de L2 no incluye los subpaquetes: <code>java.awt.*</code> no trae <code>java.awt.event.ActionEvent</code>. Es el objeto que describe un clic.</p>
<p class="l"><b>L4</b> Línea en blanco.</p>
"""),
             ("public class JuegoMain extends JFrame", r"""
<p class="l"><b>L5–L9</b> Javadoc: la clase es el punto de entrada y el controlador; construye la interfaz en Swing, lleva el turno y coordina a <code>Tablero</code> (estado y reglas) con <code>IA_Minimax</code> (decisión).</p>
<p class="l"><b>L10</b> Declara la clase y, con <code>extends JFrame</code>, la hace <b>heredar</b> de <code>JFrame</code> (capítulo 22). <code>JFrame</code> es la clase de Swing que representa una ventana con barra de título, botones de minimizar y cerrar, y borde. Al heredar, un <code>JuegoMain</code> <b>es</b> una ventana: tiene todos los métodos de <code>JFrame</code> (<code>setVisible</code>, <code>pack</code>, <code>add</code>…) y los podemos llamar directamente, como si fueran nuestros.</p>
<p class="l"><b>L11</b> Línea en blanco.</p>
"""),
             ("FICHA_JUGADOR = 'X'", r"""
<p class="l"><b>L12</b> Constante con la ficha de la persona. <code>private static final</code>: solo la usa esta clase, es una para todas las ventanas y no cambia. Darle nombre evita repetir <code>'X'</code> por el código (a diferencia de <code>PruebaConsola</code>, que escribía <code>'O'</code> a mano).</p>
<p class="l"><b>L13</b> Constante con la ficha de la IA.</p>
<p class="l"><b>L14</b> Línea en blanco.</p>
"""),
             ("COLOR_FONDO = new Color", r"""
<p class="l"><b>L15</b> El color de fondo de la ventana. <code>Color</code> es la clase de <code>java.awt</code> que representa un color; <code>new Color(rojo, verde, azul)</code> lo crea mezclando las tres luces, cada una de 0 a 255 (en el capítulo 35 verás la teoría del color). Los números están escritos en <b>hexadecimal</b>, con el prefijo <code>0x</code>: <code>0xED</code> es 237. Así se pueden copiar tal cual de un programa de diseño, donde este gris claro se escribiría <code>#EDEEF0</code>.</p>
<p class="l"><b>L16</b> El color de las casillas: <code>Color.WHITE</code>, una constante ya preparada en la clase <code>Color</code> (como <code>Color.BLACK</code> o <code>Color.RED</code>).</p>
<p class="l"><b>L17</b> Azul para la X (<code>#185FA5</code>).</p>
<p class="l"><b>L18</b> Rojo ladrillo para la O (<code>#993C1D</code>).</p>
<p class="l"><b>L19</b> Gris beige para los bordes y las líneas del tablero (<code>#D3D1C7</code>).</p>
<p class="l"><b>L20</b> Línea en blanco. Los cinco colores están juntos, con nombre, al principio del archivo: si quieres cambiar la paleta, todo está en un solo sitio. Es la idea que la Parte VII llevará más lejos con la clase <code>Tema</code>.</p>
"""),
             ("private final Tablero tablero", r"""
<p class="l"><b>L21</b> El tablero de la partida. <code>private final</code>: se crea una vez en el constructor y la variable no vuelve a apuntar a otro tablero (el tablero sí cambia por dentro al marcar casillas; <code>final</code> fija la referencia, no el contenido). Aquí se ve la <b>composición</b> del capítulo 21: la ventana <i>tiene un</i> tablero.</p>
<p class="l"><b>L22</b> El jugador humano (capítulo 30).</p>
<p class="l"><b>L23</b> La IA (capítulo 31).</p>
<p class="l"><b>L24</b> Una matriz de botones de 3×3, <b>paralela</b> a la matriz de casillas del tablero: <code>botones[1][1]</code> es el botón que se ve en el centro y corresponde a <code>casillas[1][1]</code>. Así, cuando la IA juega en (fila, columna), sabemos qué botón actualizar sin buscarlo. <code>JButton</code> es la clase de Swing para un botón.</p>
<p class="l"><b>L25</b> El letrero de estado («Tu turno (X)», «Ganaste (X)»…). <code>JLabel</code> es un componente que muestra texto que el usuario no puede editar.</p>
<p class="l"><b>L26</b> Línea en blanco.</p>
"""),
             ("private boolean turnoJugador", r"""
<p class="l"><b>L27</b> ¿Le toca a la persona? Es un dato que cambia durante la partida, por eso no es <code>final</code>. Sirve para ignorar los clics mientras la IA «piensa».</p>
<p class="l"><b>L28</b> ¿Terminó la partida? Sirve para ignorar clics tras una victoria o un empate. Estos dos <code>boolean</code> son el <b>estado de la partida</b>, distinto del estado del tablero: <code>Tablero</code> no sabe de turnos, y por eso este control vive aquí.</p>
<p class="l"><b>L29</b> Línea en blanco.</p>
"""),
             ("public JuegoMain()", r"""
<p class="l"><b>L30</b> El constructor. Construye toda la ventana; terminarlo equivale a tenerla en pantalla.</p>
<p class="l"><b>L31</b> <code>super(...)</code> llama al constructor de la clase padre, <code>JFrame</code>, pasándole el texto de la barra de título. Tiene que ser la <b>primera</b> instrucción del constructor: el «padre» se construye antes que el «hijo». Si la pusieras más abajo, el compilador diría <code>call to super must be first statement in constructor</code>.</p>
<p class="l"><b>L32</b> Línea en blanco.</p>
"""),
             ("tablero = new Tablero()", r"""
<p class="l"><b>L33</b> Crea el tablero vacío y lo guarda en el atributo <code>final</code>.</p>
<p class="l"><b>L34</b> Crea al jugador con el nombre <code>"Jugador"</code> y la ficha de la constante. En esta versión el nombre no se muestra; en la 1.0 lo escribirá la persona.</p>
<p class="l"><b>L35</b> Crea la IA: su ficha primero, la del rival después, como pide el constructor del capítulo 31.</p>
<p class="l"><b>L36</b> Crea la matriz para 9 botones. Ojo: <code>new JButton[3][3]</code> crea las 9 <b>posiciones</b>, todas con <code>null</code>; los botones de verdad se crean después, uno por uno, en <code>crearPanelTablero</code>.</p>
<p class="l"><b>L37</b> Línea en blanco: aquí termina la lógica y empieza la ventana.</p>
"""),
             ("setDefaultCloseOperation", r"""
<p class="l"><b>L38</b> Qué hacer al pulsar la X de cerrar: <code>JFrame.EXIT_ON_CLOSE</code> termina el programa. Sin esta línea, el comportamiento por defecto es solo <b>ocultar</b> la ventana: desaparecería, pero Java seguiría funcionando en segundo plano.</p>
<p class="l"><b>L39</b> Impide cambiar el tamaño de la ventana arrastrando sus bordes. El diseño está pensado para un tamaño fijo; estirado, los botones se deformarían.</p>
<p class="l"><b>L40</b> Pinta el fondo. Un <code>JFrame</code> no muestra sus componentes directamente: los coloca en un panel interior llamado <b>panel de contenido</b> (<i>content pane</i>), que se obtiene con <code>getContentPane()</code>. Por eso el color se pone ahí.</p>
<p class="l"><b>L41</b> Elige el <i>layout</i>: <code>BorderLayout</code> reparte el espacio en cinco zonas, norte, sur, este, oeste y centro. Los números <code>(0, 16)</code> son la separación horizontal y vertical entre zonas, en píxeles: 16 píxeles entre el letrero, el tablero y el botón. <code>setLayout</code> llamado sobre el <code>JFrame</code> se aplica, en realidad, a su panel de contenido.</p>
<p class="l"><b>L42</b> Un margen de 20 píxeles por los cuatro lados (arriba, izquierda, abajo, derecha), para que nada quede pegado al borde. <code>BorderFactory.createEmptyBorder</code> crea un borde invisible, solo espacio. El detalle raro es <code>(JPanel)</code>: <code>getContentPane()</code> está declarado para devolver un <code>Container</code> genérico, que no tiene el método <code>setBorder</code>; pero el panel de contenido de un <code>JFrame</code> es, en realidad, un <code>JPanel</code>. El <b>cast</b> <code>(JPanel)</code> le dice al compilador «trátalo como <code>JPanel</code>», y los paréntesis de fuera hacen que el cast se aplique antes de llamar a <code>setBorder</code>.</p>
<p class="l"><b>L43</b> Línea en blanco.</p>
"""),
             ("etiquetaEstado = crearEtiquetaEstado()", r"""
<p class="l"><b>L44</b> Crea el letrero con un método auxiliar (L57) y lo guarda en el atributo, porque luego habrá que cambiarle el texto.</p>
<p class="l"><b>L45</b> <code>add</code> mete el letrero en la ventana, en la zona <code>BorderLayout.NORTH</code> (arriba). El norte ocupa todo el ancho y solo el alto que el componente necesita.</p>
<p class="l"><b>L46</b> Crea el panel con los 9 botones y lo pone en el <code>CENTER</code>, la zona que se queda con el espacio restante. No se guarda en ningún atributo porque no se vuelve a necesitar el panel (los botones sí, y ya están en <code>botones</code>).</p>
<p class="l"><b>L47</b> Crea el botón de reiniciar y lo pone abajo (<code>SOUTH</code>). Delegar cada parte en un método <code>crear…</code> mantiene el constructor corto: se lee como un índice de la ventana.</p>
<p class="l"><b>L48</b> Línea en blanco.</p>
"""),
             ("turnoJugador = true;", r"""
<p class="l"><b>L49</b> Empieza la persona: la X siempre abre.</p>
<p class="l"><b>L50</b> La partida no ha terminado. (Un <code>boolean</code> que es atributo ya vale <code>false</code> por defecto, pero escribirlo deja clara la intención.)</p>
<p class="l"><b>L51</b> Línea en blanco.</p>
"""),
             ("pack();", r"""
<p class="l"><b>L52</b> <code>pack()</code> calcula el tamaño de la ventana a partir del tamaño preferido de lo que contiene: 9 botones de 100×100, las separaciones, el letrero, el botón y los márgenes. El panel de contenido queda de unos 350 × 450 píxeles (lo medimos), más la barra de título que añade Windows. Sin <code>pack()</code> ni un tamaño fijo, la ventana aparecería diminuta, de 0×0.</p>
<p class="l"><b>L53</b> Centra la ventana en la pantalla. <code>setLocationRelativeTo</code> la centra respecto a otro componente; <code>null</code> significa «respecto a la pantalla». Va después de <code>pack()</code> porque para centrar hay que conocer el tamaño.</p>
<p class="l"><b>L54</b> Muestra la ventana. Hasta este momento todo se construyó «en la memoria», sin verse. Va al final a propósito: si se mostrara antes, la persona vería la ventana armarse a trozos.</p>
<p class="l"><b>L55–L56</b> Cierran el constructor y dejan una línea en blanco.</p>
"""),
             ("private JLabel crearEtiquetaEstado", r"""
<p class="l"><b>L57</b> Método auxiliar <code>private</code> que fabrica y devuelve el letrero (<code>JLabel</code>).</p>
<p class="l"><b>L58</b> Crea el letrero con el texto inicial y lo centra: <code>SwingConstants.CENTER</code> es una constante de Swing que indica la alineación horizontal del texto. Sin ella, el texto quedaría pegado a la izquierda.</p>
<p class="l"><b>L59</b> Fuente: <code>new Font(nombre, estilo, tamaño)</code>. <code>"SansSerif"</code> es un nombre lógico que Java traduce a la fuente sin remates del sistema (en Windows, normalmente Arial); <code>Font.BOLD</code>, negrita; 16, el tamaño en puntos.</p>
<p class="l"><b>L60</b> <code>setOpaque(true)</code>: un <code>JLabel</code> es transparente por defecto y no pinta su fondo. Sin esta línea, el <code>setBackground</code> de la línea siguiente no tendría ningún efecto visible.</p>
"""),
             ("etiqueta.setBackground(Color.WHITE)", r"""
<p class="l"><b>L61</b> Fondo blanco, para que el letrero parezca una tarjeta sobre el gris de la ventana.</p>
<p class="l"><b>L62–L64</b> Una sola instrucción en tres líneas que pone un borde <b>compuesto</b>: <code>createCompoundBorder(exterior, interior)</code> combina dos bordes. El exterior es una línea de 1 píxel del color de los bordes; el interior, un relleno invisible de 10 píxeles por lado (<i>padding</i>), para que el texto no toque la línea. Termina con <code>)));</code>: cada paréntesis cierra una llamada.</p>
<p class="l"><b>L65</b> Devuelve el letrero terminado a quien lo pidió (L44).</p>
<p class="l"><b>L66–L67</b> Cierran el método y dejan una línea en blanco.</p>
"""),
             ("private JPanel crearPanelTablero", r"""
<p class="l"><b>L68</b> Método que fabrica el panel del tablero y sus 9 botones.</p>
<p class="l"><b>L69</b> Crea un <code>JPanel</code> (un contenedor rectangular, sin ventana propia) con un <code>GridLayout(3, 3, 4, 4)</code>: una rejilla de 3 filas y 3 columnas, con 4 píxeles de separación horizontal y vertical. <code>GridLayout</code> hace todas las celdas del mismo tamaño y las llena en orden de lectura: el primer componente que se agregue va arriba a la izquierda; el cuarto, al principio de la segunda fila. Es justo el orden de nuestros dos <code>for</code>.</p>
<p class="l"><b>L70</b> El fondo del panel es gris beige. Como los botones son blancos y entre ellos hay 4 píxeles de separación, por esos huecos se ve el fondo: así aparecen las <b>líneas del totito</b> sin dibujar ninguna línea.</p>
<p class="l"><b>L71</b> Un borde de 1 píxel del mismo color alrededor de la rejilla, para cerrar el contorno.</p>
<p class="l"><b>L72</b> Línea en blanco.</p>
"""),
             ("for (int fila = 0; fila < 3; fila++)", r"""
<p class="l"><b>L73–L74</b> Los dos <code>for</code> anidados: un botón por casilla, en orden de lectura.</p>
<p class="l"><b>L75</b> Crea un botón sin texto (<code>""</code>, texto vacío): una casilla libre se ve en blanco.</p>
<p class="l"><b>L76</b> Fuente grande, negrita de 48 puntos, para que la X y la O llenen la casilla.</p>
<p class="l"><b>L77</b> Fondo blanco.</p>
"""),
             ("boton.setFocusPainted(false)", r"""
<p class="l"><b>L78</b> No dibujar el recuadro de <b>foco</b>, el rectángulo punteado que Swing pinta alrededor del botón que acaba de recibir un clic. Sin esta línea, la última casilla pulsada quedaría marcada con ese rectángulo.</p>
<p class="l"><b>L79</b> No dibujar el borde en relieve del botón: queremos casillas planas.</p>
<p class="l"><b>L80</b> Que el botón pinte su fondo de forma opaca, para que el blanco de L77 se vea siempre.</p>
<p class="l"><b>L81</b> Tamaño preferido de 100×100 píxeles. <code>Dimension</code> es una clase que solo guarda un ancho y un alto. Es el dato que usa <code>pack()</code> (L52) para calcular el tamaño de la ventana.</p>
<p class="l"><b>L82</b> Línea en blanco.</p>
"""),
             ("final int f = fila", r"""
<p class="l"><b>L83–L84</b> Copias de <code>fila</code> y <code>columna</code> en dos variables <code>final</code>. Parecen inútiles, pero sin ellas el programa no compila. La lambda de L85 se ejecutará mucho después, cuando alguien haga clic, y para entonces el ciclo ya habrá terminado. Java exige que las variables locales que usa una lambda no cambien nunca (que sean <code>final</code> o «efectivamente finales»), para que la lambda pueda guardarse una copia segura de su valor. <code>fila</code> y <code>columna</code> cambian en cada vuelta (<code>fila++</code>), así que no sirven; <code>f</code> y <code>c</code> se crean nuevas en cada vuelta y no cambian, así que cada botón se queda con <b>sus</b> coordenadas. Si escribieras <code>manejarClicCasilla(fila, columna)</code> en la lambda, el compilador diría <code>local variables referenced from a lambda expression must be final or effectively final</code>.</p>
<p class="l"><b>L85</b> Conecta el botón con el código que debe ejecutarse al pulsarlo. <code>addActionListener</code> registra un <b>oyente</b> (<i>listener</i>): un objeto al que Swing avisará cada vez que se pulse el botón. El oyente debe cumplir la interfaz <code>ActionListener</code>, que tiene un único método, <code>actionPerformed(ActionEvent e)</code>; por eso se puede escribir como <b>lambda</b> (capítulo 25): <code>(ActionEvent e) -&gt; manejarClicCasilla(f, c)</code> significa «cuando ocurra el evento <code>e</code>, llama a <code>manejarClicCasilla</code> con estas coordenadas». El parámetro <code>e</code> trae datos del clic que aquí no necesitamos. Esta línea <b>no</b> llama a <code>manejarClicCasilla</code> ahora: solo deja dicho qué hacer después.</p>
<p class="l"><b>L86</b> Línea en blanco.</p>
"""),
             ("botones[fila][columna] = boton", r"""
<p class="l"><b>L87</b> Guarda el botón en su posición de la matriz, para poder cambiarlo más tarde (ponerle la X, desactivarlo).</p>
<p class="l"><b>L88</b> Lo agrega al panel. Por el <code>GridLayout</code>, el primer botón agregado queda arriba a la izquierda y el noveno abajo a la derecha: coinciden con la matriz.</p>
<p class="l"><b>L89–L90</b> Cierran los dos <code>for</code>.</p>
<p class="l"><b>L91</b> Devuelve el panel con sus 9 botones (lo recibe L46).</p>
<p class="l"><b>L92–L93</b> Cierran el método y dejan una línea en blanco.</p>
"""),
             ("private JButton crearBotonReiniciar", r"""
<p class="l"><b>L94</b> Método que fabrica el botón de reiniciar.</p>
<p class="l"><b>L95</b> Crea el botón con su texto.</p>
<p class="l"><b>L96</b> Fuente normal (<code>Font.PLAIN</code>) de 14 puntos: más discreta que el letrero, porque es una acción secundaria.</p>
<p class="l"><b>L97</b> Sin recuadro de foco, como las casillas.</p>
<p class="l"><b>L98</b> Al pulsarlo, se llama a <code>reiniciarPartida()</code>. Aquí la lambda no usa variables locales, así que no hacen falta copias <code>final</code>.</p>
<p class="l"><b>L99</b> Devuelve el botón (lo recibe L47).</p>
<p class="l"><b>L100–L101</b> Cierran el método y dejan una línea en blanco.</p>
"""),
             ("private void manejarClicCasilla", r"""
<p class="l"><b>L102</b> Javadoc: este método atiende el clic de la persona en una casilla.</p>
<p class="l"><b>L103</b> Lo llama la lambda de L85 con las coordenadas del botón pulsado. Es <code>private</code>: solo lo usa esta ventana.</p>
<p class="l"><b>L104</b> Primera guarda: si la partida terminó <b>o</b> no es el turno de la persona, el clic se ignora. Cubre dos casos del capítulo 28: clic con la partida terminada y clic mientras la IA «piensa» (durante los 350 ms de espera).</p>
<p class="l"><b>L105–L106</b> <code>return</code> sale sin hacer nada; cierra el <code>if</code>.</p>
<p class="l"><b>L107</b> Intenta marcar con la ficha del jugador. Si <code>Tablero</code> responde <code>false</code> (casilla ocupada), se ignora el clic. En la práctica no debería pasar, porque las casillas ocupadas se desactivan (L152), pero la regla la impone el tablero y la ventana respeta su respuesta: dos protecciones son mejor que una.</p>
<p class="l"><b>L108–L109</b> Sale si no se pudo; cierra el <code>if</code>.</p>
<p class="l"><b>L110</b> Línea en blanco: si llegamos aquí, la X ya está en el tablero.</p>
"""),
             ("actualizarBoton(fila, columna);", r"""
<p class="l"><b>L111</b> Refleja la jugada en el botón: le pone la X y lo desactiva (L147).</p>
<p class="l"><b>L112–L114</b> ¿Terminó la partida con esta jugada? <code>verificarFinDePartida</code> (L156) actualiza el letrero si es así. En ese caso, <code>return</code>: la IA no debe jugar.</p>
<p class="l"><b>L115</b> Línea en blanco.</p>
<p class="l"><b>L116</b> Pasa el turno a la IA. Desde este momento L104 ignora los clics de la persona.</p>
<p class="l"><b>L117</b> Cambia el letrero. <code>setText</code> reemplaza el texto de un <code>JLabel</code>; Swing redibuja solo esa parte de la ventana.</p>
<p class="l"><b>L118</b> Línea en blanco.</p>
"""),
             ("Timer temporizador = new Timer", r"""
<p class="l"><b>L119–L120</b> Comentario: una pausa para que el cambio de turno se sienta natural. Si la IA respondiera en el mismo instante, la X y la O aparecerían a la vez y parecería que el programa jugó por ti.</p>
<p class="l"><b>L121</b> Crea un temporizador de Swing (<code>javax.swing.Timer</code>) de 350 milisegundos (0,35 segundos). El segundo argumento sería el oyente; se pasa <code>null</code> porque se agrega en la línea siguiente. ¿Por qué no simplemente «dormir» 350 ms con <code>Thread.sleep(350)</code>? Porque todo el código de los clics se ejecuta en un único hilo, el <b>hilo de eventos</b> de Swing (el EDT, capítulo 37), que es también el que dibuja la ventana. Si lo durmieras, la ventana se congelaría: ni siquiera se vería la X recién puesta hasta después de la pausa. El <code>Timer</code> no bloquea nada: deja seguir al hilo y, pasado el tiempo, le pide que ejecute el oyente.</p>
<p class="l"><b>L122</b> Agrega el oyente como lambda. Esta vez el cuerpo tiene dos instrucciones, así que va entre llaves <code>{ }</code>. Aquí <code>e</code> se escribe sin tipo: Java lo deduce. La lambda usa la variable local <code>temporizador</code>; se permite porque nunca se le asigna otro valor (es efectivamente final).</p>
<p class="l"><b>L123</b> Cuando pasen los 350 ms: juega la IA.</p>
<p class="l"><b>L124</b> Detiene el temporizador para que no se repita.</p>
<p class="l"><b>L125</b> Cierra la lambda y la llamada a <code>addActionListener</code>: <code>});</code>.</p>
"""),
             ("temporizador.setRepeats(false)", r"""
<p class="l"><b>L126</b> Le dice al temporizador que se dispare <b>una sola vez</b>. Por defecto, un <code>Timer</code> se repite cada 350 ms indefinidamente. Con esta línea, el <code>stop()</code> de L124 sobra; tener ambas es una protección doble que no hace daño.</p>
<p class="l"><b>L127</b> Arranca la cuenta. El método termina aquí mismo, sin esperar: la ventana queda libre para redibujarse con la X y el letrero «Turno de la IA (O)».</p>
<p class="l"><b>L128–L129</b> Cierran el método y dejan una línea en blanco.</p>
"""),
             ("private void turnoIA", r"""
<p class="l"><b>L130</b> Javadoc: pide a la IA su mejor jugada según Minimax y la aplica al tablero.</p>
<p class="l"><b>L131</b> El método que ejecuta el temporizador.</p>
<p class="l"><b>L132</b> Pide la jugada (capítulo 31). La primera vez son unas 55 000 a 64 000 llamadas a <code>minimax</code>, centésimas de segundo; durante ese momento la ventana no responde, pero es tan breve que no se nota.</p>
<p class="l"><b>L133–L135</b> Comprueba el centinela <code>{-1, -1}</code>: si la IA no encontró jugada (tablero lleno), no hace nada. No debería ocurrir, porque <code>verificarFinDePartida</code> se comprueba antes, pero protege contra un <code>ArrayIndexOutOfBoundsException</code> en L149 (<code>botones[-1]</code>).</p>
<p class="l"><b>L136</b> Marca la O en el tablero real con la constante <code>FICHA_IA</code>.</p>
<p class="l"><b>L137</b> Refleja la jugada en su botón.</p>
<p class="l"><b>L138</b> Línea en blanco.</p>
"""),
             ("if (verificarFinDePartida())", r"""
<p class="l"><b>L139–L141</b> Si la IA ganó (o llenó la última casilla), termina; el letrero ya lo anunció.</p>
<p class="l"><b>L142</b> Línea en blanco.</p>
<p class="l"><b>L143</b> Devuelve el turno a la persona: L104 vuelve a aceptar clics.</p>
<p class="l"><b>L144</b> Actualiza el letrero.</p>
<p class="l"><b>L145–L146</b> Cierran el método y dejan una línea en blanco.</p>
"""),
             ("private void actualizarBoton", r"""
<p class="l"><b>L147</b> Método que pone en un botón la ficha que dice el tablero.</p>
<p class="l"><b>L148</b> Lee la ficha <b>del tablero</b>, no de un parámetro: el tablero es la fuente de verdad (capítulo 29) y la ventana solo lo refleja.</p>
<p class="l"><b>L149</b> Toma el botón correspondiente de la matriz paralela.</p>
<p class="l"><b>L150</b> Le pone la letra como texto. <code>setText</code> necesita un <code>String</code> y <code>ficha</code> es un <code>char</code>: <code>String.valueOf(ficha)</code> convierte el carácter <code>'X'</code> en el texto <code>"X"</code>.</p>
<p class="l"><b>L151</b> Elige el color del texto con el <b>operador ternario</b> <code>condición ? siA : siNo</code>, un <code>if/else</code> en miniatura que devuelve un valor: si la ficha es la de la persona, azul; si no, rojo ladrillo. <code>setForeground</code> fija el color del texto.</p>
<p class="l"><b>L152</b> Desactiva el botón: ya no responde a clics y Swing lo dibuja «apagado». Así una casilla ocupada no se puede volver a pulsar.</p>
<p class="l"><b>L153–L154</b> Cierran el método y dejan una línea en blanco.</p>
<div class="caja cuidado"><b>¿Por qué las fichas se ven grises?</b> Cuando pruebes la ventana notarás que la X y la O no salen azul y roja, sino gris. No es un error tuyo: el aspecto por defecto de Swing (llamado <i>Metal</i>) pinta el texto de <b>todo</b> botón desactivado con su propio color gris (<code>#999999</code>), sin importar el <code>setForeground</code>. Lo comprobamos dibujando un botón como estos en una imagen: activo, el texto sale <code>#185FA5</code>; desactivado, <code>#999999</code>. Las líneas L151 y L152 «compiten», y gana la segunda. Es una lección valiosa: un componente estándar decide parte de su aspecto por su cuenta. Por eso en la Parte VII el tablero neón no usará botones, sino un panel que dibuja cada casilla con su propio código (<code>PanelTablero</code>, capítulo 48), donde el color lo decides tú.</div>
"""),
             ("private boolean verificarFinDePartida", r"""
<p class="l"><b>L155</b> Javadoc: revisa si hay ganador o empate y actualiza la interfaz.</p>
<p class="l"><b>L156</b> Devuelve <code>true</code> si la partida terminó.</p>
<p class="l"><b>L157</b> Pregunta al tablero quién ganó. La ventana no sabe detectar una línea: se lo pregunta a quien sabe.</p>
<p class="l"><b>L158</b> Si hay ganador…</p>
<p class="l"><b>L159</b> …marca la partida como terminada (L104 ignorará los clics).</p>
<p class="l"><b>L160</b> Escribe el resultado con otro operador ternario: «Ganaste (X)» o «Gana la IA (O)». En la práctica solo verás el segundo.</p>
<p class="l"><b>L161</b> Desactiva las casillas que quedaban libres, para que se vea que ya no se puede jugar.</p>
<p class="l"><b>L162–L163</b> Devuelve <code>true</code> y cierra el <code>if</code>.</p>
"""),
             ("if (tablero.tableroLleno())", r"""
<p class="l"><b>L164–L167</b> Si no hay ganador pero el tablero está lleno: partida terminada, letrero «Empate», <code>true</code>. Aquí no hace falta desactivar casillas: con el tablero lleno, las nueve ya se desactivaron una a una en L152. Y, como siempre, primero se preguntó por el ganador.</p>
<p class="l"><b>L168</b> Cierra el <code>if</code>.</p>
<p class="l"><b>L169</b> La partida sigue: <code>false</code>.</p>
<p class="l"><b>L170–L171</b> Cierran el método y dejan una línea en blanco.</p>
"""),
             ("private void deshabilitarTodasLasCasillas", r"""
<p class="l"><b>L172</b> Método que desactiva los 9 botones.</p>
<p class="l"><b>L173–L174</b> Recorre la matriz de botones.</p>
<p class="l"><b>L175</b> Desactiva cada uno. Desactivar uno que ya lo estaba no tiene ningún efecto, así que no hace falta preguntar antes.</p>
<p class="l"><b>L176–L179</b> Cierran los dos <code>for</code> y el método, y dejan una línea en blanco.</p>
"""),
             ("private void reiniciarPartida", r"""
<p class="l"><b>L180</b> Javadoc: deja tablero e interfaz listos para otra partida.</p>
<p class="l"><b>L181</b> El método que llama el botón de reiniciar (L98).</p>
<p class="l"><b>L182</b> Vacía el tablero con el método del capítulo 29. Se reutiliza el mismo objeto: no hace falta crear un tablero nuevo (y no se podría asignar otro, porque el atributo es <code>final</code>).</p>
<p class="l"><b>L183–L184</b> La partida vuelve a estar abierta y empieza la persona.</p>
<p class="l"><b>L185</b> Letrero inicial.</p>
<p class="l"><b>L186</b> Línea en blanco.</p>
"""),
             ("for (int fila = 0; fila < 3; fila++)", r"""
<p class="l"><b>L187–L188</b> Recorre los 9 botones.</p>
<p class="l"><b>L189</b> Borra la letra del botón.</p>
<p class="l"><b>L190</b> Lo vuelve a activar para que acepte clics.</p>
<p class="l"><b>L191–L194</b> Cierran los dos <code>for</code> y el método, y dejan una línea en blanco. El color de texto de L151 no se restablece porque no hace falta: se vuelve a fijar en cada jugada.</p>
<div class="caja cuidado"><b>Un detalle que puedes mejorar</b> Si pulsas «Reiniciar» justo en los 350 ms en que la IA está esperando, el temporizador sigue en marcha: al cumplirse, <code>turnoIA()</code> juega una O en el tablero recién vaciado, y la IA abre la partida nueva. No rompe nada, pero no es lo que esperarías. Es el tipo de caso límite que aparece al mezclar tiempo e interfaz; en el ejercicio 4 lo corriges. La versión 1.0 (<code>PantallaJuego</code>, capítulo 59) lo evita guardando el temporizador en un atributo y deteniéndolo cuando la partida se reinicia o se abandona.</div>
"""),
             ("public static void main", r"""
<p class="l"><b>L195</b> El punto de entrada del programa (capítulo 11).</p>
<p class="l"><b>L196</b> Arranca la ventana en el hilo correcto. Swing exige que sus componentes se creen y se modifiquen solo desde el hilo de eventos (EDT); <code>main</code>, en cambio, se ejecuta en otro hilo, el principal. <code>SwingUtilities.invokeLater(...)</code> pone una tarea en la cola del EDT para que la ejecute «en cuanto pueda». La tarea es <code>JuegoMain::new</code>, una <b>referencia a constructor</b> (capítulo 25): una forma corta de escribir la lambda <code>() -&gt; new JuegoMain()</code>. Al ejecutarse, crea la ventana, y el constructor la muestra (L54). No hace falta guardar el objeto en una variable: Swing mantiene viva la ventana mientras esté abierta. Si escribieras directamente <code>new JuegoMain();</code>, casi siempre funcionaría, pero no es seguro y puede causar fallos raros e intermitentes.</p>
<p class="l"><b>L197–L198</b> Cierran <code>main</code> y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<p>Sigamos una partida desde el arranque hasta el primer turno completo. Los números entre paréntesis son las líneas.</p>
<ol>
<li><b>Arranque.</b> Java ejecuta <code>main</code> (L195). <code>invokeLater</code> encarga al hilo de eventos crear un <code>JuegoMain</code>. El constructor llama a <code>super</code> (título), crea <code>Tablero</code>, <code>Jugador</code>, <code>IA_Minimax</code> y la matriz de botones (L33–L36), arma la ventana (L38–L47), fija <code>turnoJugador = true</code>, la empaqueta, la centra y la muestra (L52–L54). <code>main</code> termina, pero el programa sigue vivo porque hay una ventana abierta.</li>
<li><b>Espera.</b> No hay ningún ciclo <code>while</code> como en <code>PruebaConsola</code>. El hilo de eventos de Swing es el ciclo: espera a que pase algo (un clic, un temporizador) y ejecuta el oyente correspondiente. Este estilo se llama <b>programación orientada a eventos</b>.</li>
<li><b>Clic en el centro.</b> Swing ejecuta la lambda del botón (1,1), que llama a <code>manejarClicCasilla(1, 1)</code>. L104: partida abierta y turno de la persona, sigue. L107: <code>marcarCasilla(1, 1, 'X')</code> devuelve <code>true</code>. L111: el botón muestra «X» y se desactiva. L112: <code>verificarGanador()</code> da <code>' '</code> y el tablero no está lleno, sigue. L116–L117: <code>turnoJugador = false</code>, letrero «Turno de la IA (O)». L121–L127: arranca el temporizador y el método termina. La ventana se redibuja.</li>
<li><b>Clic impaciente.</b> Si en esos 350 ms haces clic en otra casilla, L104 ve <code>turnoJugador == false</code> y sale sin hacer nada.</li>
<li><b>Responde la IA.</b> A los 350 ms, el temporizador ejecuta su lambda: <code>turnoIA()</code>. L132: la IA devuelve <code>{0, 0}</code> (la esquina, capítulo 31). L136–L137: la O queda en el tablero y en el botón (0,0). L139: la partida sigue. L143–L144: <code>turnoJugador = true</code>, letrero «Tu turno (X)».</li>
</ol>
<table class="tabla">
<tr><th>Momento</th><th><code>turnoJugador</code></th><th><code>juegoTerminado</code></th><th>Letrero</th><th>Botones activos</th></tr>
<tr><td>Ventana recién abierta</td><td><code>true</code></td><td><code>false</code></td><td>Tu turno (X)</td><td>9</td></tr>
<tr><td>Tras tu clic en (1,1)</td><td><code>false</code></td><td><code>false</code></td><td>Turno de la IA (O)</td><td>8</td></tr>
<tr><td>Tras la O en (0,0)</td><td><code>true</code></td><td><code>false</code></td><td>Tu turno (X)</td><td>7</td></tr>
<tr><td>La IA completa una línea</td><td><code>false</code></td><td><code>true</code></td><td>Gana la IA (O)</td><td>0</td></tr>
<tr><td>Tras «Nueva partida / Reiniciar»</td><td><code>true</code></td><td><code>false</code></td><td>Tu turno (X)</td><td>9</td></tr>
</table>
<div class="caja concepto"><b>La ventana pregunta, el tablero responde</b> Busca en <code>JuegoMain</code> alguna comparación de tres casillas: no hay ninguna. Todas las reglas se consultan a <code>Tablero</code> (<code>marcarCasilla</code>, <code>verificarGanador</code>, <code>tableroLleno</code>) y todas las decisiones de la máquina a <code>IA_Minimax</code>. La ventana solo traduce: de clics a llamadas, y de respuestas a textos y botones. Gracias a eso, en la Parte VII podrás cambiar toda la interfaz sin tocar ni una regla.</div>

<h2>Compila y prueba</h2>
<p>Como el <code>pom.xml</code> apunta a <code>TotitoApp</code>, que no existirá hasta el capítulo 61, el botón <i>Run Project</i> (F6) todavía no sirve. No cambies el <code>pom.xml</code>: ejecuta la ventana de una de estas dos formas.</p>
<ul>
<li><b>Desde NetBeans</b>: en <i>Projects</i>, clic derecho sobre <code>JuegoMain.java</code> → <i>Run File</i> (o, con el archivo abierto en el editor, <b>Shift+F6</b>). NetBeans compila lo necesario y ejecuta el <code>main</code> de ese archivo.</li>
<li><b>Desde PowerShell</b>, después de <i>Clean and Build</i> (Shift+F11):</li>
</ul>
<pre class="ps">cd $HOME\Proyectos\Totito
java -cp target\classes JuegoMain</pre>
<p>Aquí, a diferencia del capítulo 32, se le da a <code>java</code> el <b>nombre de la clase</b> (sin <code>.java</code>), porque <code>JuegoMain</code> sí está en <code>src</code> y Maven ya la compiló en <code>target\classes</code>.</p>
<p>Debería aparecer, centrada en la pantalla, una ventana pequeña titulada «Totito - Minimax AI»: arriba un letrero blanco que dice «Tu turno (X)», en medio una rejilla de 3×3 casillas blancas separadas por líneas gris beige sobre un fondo gris claro, y abajo el botón «Nueva partida / Reiniciar». No se puede estirar. Haz esta lista de pruebas, que sale de la tabla de casos del capítulo 28:</p>
<table class="tabla">
<tr><th>Prueba</th><th>Qué debe pasar</th></tr>
<tr><td>Clic en el centro</td><td>Aparece una X; el letrero dice «Turno de la IA (O)»; poco después aparece una O en una esquina y vuelve «Tu turno (X)»</td></tr>
<tr><td>Clic en una casilla ocupada</td><td>Nada: está desactivada</td></tr>
<tr><td>Clic rápido en otra casilla mientras espera la IA</td><td>Nada: se ignora (L104)</td></tr>
<tr><td>Jugar bien hasta el final</td><td>Las nueve casillas se llenan y el letrero dice «Empate»</td></tr>
<tr><td>Descuidarse (no tapar una amenaza)</td><td>La IA completa la línea: «Gana la IA (O)» y se desactivan todas las casillas</td></tr>
<tr><td>Pulsar «Nueva partida / Reiniciar»</td><td>Las casillas se vacían y se activan; «Tu turno (X)»</td></tr>
<tr><td>Cerrar con la X de la ventana</td><td>El programa termina (en NetBeans, la ejecución se detiene en la ventana <i>Output</i>)</td></tr>
</table>
<p>Recuerda que las fichas se verán grises por lo que explicamos en la línea 152.</p>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Mensaje o síntoma</th><th>Causa</th><th>Solución</th></tr>
<tr><td>Al pulsar F6: <code>ClassNotFoundException: TotitoApp</code> o un error de <code>exec</code></td><td><i>Run Project</i> busca <code>TotitoApp</code>, que aún no existe</td><td>Usa <i>Run File</i> (Shift+F6) sobre <code>JuegoMain.java</code></td></tr>
<tr><td><code>local variables referenced from a lambda expression must be final or effectively final</code></td><td>La lambda de L85 usa <code>fila</code> y <code>columna</code> en vez de <code>f</code> y <code>c</code></td><td>Copia las coordenadas en variables <code>final</code> dentro del ciclo</td></tr>
<tr><td><code>call to super must be first statement in constructor</code></td><td>Algo va antes de <code>super(...)</code></td><td><code>super</code> debe ser la primera línea</td></tr>
<tr><td><code>cannot find symbol: class ActionEvent</code></td><td>Falta el <code>import</code> de L3</td><td>El asterisco de <code>java.awt.*</code> no incluye <code>java.awt.event</code></td></tr>
<tr><td>Todas las casillas reaccionan como si fueran la misma</td><td>Las coordenadas de la lambda no son las del botón</td><td>Revisa L83–L85</td></tr>
<tr><td>La ventana sale diminuta</td><td>Falta <code>pack()</code> o está después de <code>setVisible</code></td><td><code>pack()</code>, luego <code>setLocationRelativeTo</code>, luego <code>setVisible(true)</code></td></tr>
<tr><td>Al cerrar la ventana, NetBeans sigue mostrando el programa en ejecución</td><td>Falta <code>setDefaultCloseOperation</code> (L38)</td><td>Detén el programa con el cuadro rojo de <i>Output</i> y agrega la línea</td></tr>
<tr><td>La IA responde al instante y no se ve la X sola</td><td>Se quitó el <code>Timer</code>, o se cambió por <code>Thread.sleep</code></td><td>Usa <code>javax.swing.Timer</code>, que no congela la ventana</td></tr>
</table>

<div class="caja hito"><b>Hito: Totito v0.1 jugable</b> Tienes un juego completo: una ventana donde juegas con el ratón contra una inteligencia artificial que nunca pierde. Detrás hay cuatro clases con responsabilidades claras, probadas por separado con <code>jshell</code> y juntas con <code>PruebaConsola</code>. Todo lo que viene a partir de aquí (colores neón, pantallas, animaciones, instalador) se construye sobre esta base, y la lógica ya no cambiará.</div>

<div class="caja git"><b>Git</b> Último commit de la Parte V, y la primera <b>etiqueta</b> de versión (capítulo 9). Una etiqueta es un nombre fijo para un commit concreto: dentro de unos meses podrás volver exactamente a «la versión 0.1» aunque el proyecto haya cambiado mucho.
<pre class="ps">git add src\JuegoMain.java
git commit -m "Primera ventana jugable (Swing basico)"
git push
git tag -a v0.1.0 -m "Totito v0.1: logica y primera ventana"
git push origin v0.1.0
git log --oneline</pre>
<code>git tag -a</code> crea una etiqueta anotada (con autor, fecha y mensaje) sobre el último commit. <code>git push</code> no sube las etiquetas: hay que enviarlas aparte, con <code>git push origin v0.1.0</code>. El número sigue el versionado semántico que verás en el capítulo 67: 0.1.0 indica una primera versión funcional, todavía no la definitiva. <code>git log --oneline</code> debe mostrar, encima del historial anterior, tus cinco commits de esta parte, y el último marcado con algo como <code>(HEAD -&gt; main, tag: v0.1.0, origin/main)</code>. En GitHub, la etiqueta aparece en la sección <i>Tags</i> del repositorio <code>totito</code>.</div>

<h2>Qué pasará con JuegoMain</h2>
<p>En la Parte VII construirás, en una rama aparte (<code>interfaz-neon</code>), la interfaz definitiva: menú, instrucciones, configuración de nombres y símbolos, partida y pantalla de victoria, todo dibujado con estilo neón. Esa interfaz tendrá su propio punto de entrada, <code>TotitoApp</code>, y repartirá los dos trabajos de <code>JuegoMain</code>: el control de la partida irá a <code>Partida</code> y la vista a varias pantallas. Usará <code>Tablero</code>, <code>Jugador</code> e <code>IA_Minimax</code> exactamente como están hoy.</p>
<p><code>JuegoMain</code> se queda en <code>src</code>: no estorba, documenta de dónde viene el proyecto y es un ejemplo pequeño y completo de Swing al que puedes volver. Seguirá funcionando con <i>Run File</i> o con <code>java -cp target\classes JuegoMain</code> incluso cuando el juego principal sea la versión neón.</p>

<h2>Resumen</h2>
<ul>
<li><code>JuegoMain</code> hereda de <code>JFrame</code>: es una ventana. <code>super(...)</code> pone el título y debe ir primero.</li>
<li>La interfaz se arma con un <code>BorderLayout</code> (letrero al norte, tablero al centro, botón al sur) y un <code>GridLayout(3, 3, 4, 4)</code> cuyas separaciones dejan ver el fondo como líneas del totito.</li>
<li>Una matriz <code>JButton[3][3]</code> paralela a la del tablero conecta cada casilla con su botón.</li>
<li>Los clics se atienden con lambdas que implementan <code>ActionListener</code>; las variables que usan deben ser <code>final</code> o efectivamente finales.</li>
<li>Dos <code>boolean</code> (<code>turnoJugador</code>, <code>juegoTerminado</code>) llevan el estado de la partida y filtran los clics.</li>
<li>Un <code>javax.swing.Timer</code> de 350 ms hace esperar a la IA sin congelar la ventana; <code>Thread.sleep</code> la congelaría.</li>
<li>Swing se arranca con <code>SwingUtilities.invokeLater(JuegoMain::new)</code>, en su hilo de eventos.</li>
<li>Se ejecuta con <i>Run File</i> (Shift+F6) o <code>java -cp target\classes JuegoMain</code>; la versión se marca con la etiqueta <code>v0.1.0</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b> Esta ventana es el esqueleto de muchísimos programas de escritorio:
<ul>
<li><b>Buscaminas o Conecta 4</b>: una matriz de botones paralela a la matriz del modelo, un <code>GridLayout</code> y un oyente por botón con sus coordenadas en variables <code>final</code>. Solo cambian el tamaño y las reglas que se consultan.</li>
<li><b>Una calculadora</b>: <code>BorderLayout</code> con la pantalla al norte y un <code>GridLayout(4, 4)</code> de botones al centro; cada botón, una lambda.</li>
<li><b>Un formulario de registro</b>: letrero de estado que cambia con <code>setText</code> («Guardado», «Falta el correo»), botones que se desactivan mientras se guarda y un <code>Timer</code> para borrar el mensaje a los pocos segundos.</li>
<li><b>Cualquier interfaz</b>: la regla «la ventana pregunta, el modelo responde» (vista y controlador sin reglas de negocio) vale igual para una app Android o una página web.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Cambia la espera de la IA a 1000 ms y luego a 0. ¿Qué diferencia notas al jugar? Deja el valor que te parezca más natural.</li>
<li>Cambia el título de la ventana y los colores <code>COLOR_FONDO</code> y <code>COLOR_BORDE</code> por otros en hexadecimal. ¿Cuántas líneas tuviste que tocar?</li>
<li>Haz que las fichas se vean de color: en <code>actualizarBoton</code>, en lugar de desactivar el botón, déjalo activo y confía en las guardas de <code>manejarClicCasilla</code>. Pista: comenta L152 y comprueba que un clic en una casilla ocupada sigue sin hacer nada gracias a L107. ¿Qué tendrías que cambiar en <code>deshabilitarTodasLasCasillas</code>?</li>
<li>Corrige el detalle del botón «Reiniciar» durante la espera. Pista: convierte <code>temporizador</code> en un atributo y, en <code>reiniciarPartida</code>, si no es <code>null</code>, llama a <code>temporizador.stop()</code>.</li>
<li>Reto: agrega un segundo letrero al sur, debajo del botón de reiniciar, con un marcador «Tú: 0 · IA: 0 · Empates: 0» que se actualice al terminar cada partida. Pista: tres contadores <code>int</code> y un <code>JPanel</code> con <code>BorderLayout</code> para poner dos cosas en la zona sur.</li>
</ol></div>
""",
}
