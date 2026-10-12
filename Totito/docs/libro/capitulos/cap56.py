# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 56,
    "titulo": "PantallaMenu.java y la VistaPrevia: por fin se ve el diseño",
    "antes": r"""
<p class="entrada">Desde el capítulo 38 llevas construyendo piezas que todavía no has visto juntas: colores, trazos de neón,
iconos, botones, tarjetas, un fondo. En este capítulo escribes la primera pantalla completa, el menú principal, y
una pequeña herramienta que la abre en una ventana. Cuando ejecutes un solo comando, <b>todo eso aparecerá junto
por primera vez</b>, y podrás ponerlo al lado de la imagen de diseño del capítulo 34.</p>

<h2>Por qué existen estos dos archivos</h2>
<h3>PantallaMenu.java</h3>
<p>Es la pantalla 1 del diseño (<code>diseno/menu.jpg</code>): una tarjeta de cristal morada con tres botones
grandes, «Jugar» (rosa), «Instrucciones» (azul) y «Salir» (morado), sobre el fondo común y bajo el encabezado. Gracias
a todo lo anterior, la pantalla entera cabe en <b>34 líneas</b>: el fondo y el encabezado los pone
<code>PantallaBase</code> (capítulo 55), los botones los fabrica <code>BotonNeon</code> (capítulo 44) y la tarjeta
es una <code>Tarjeta</code> (capítulo 43). Esta pantalla solo <b>ensambla</b>. Así se ve cuando el trabajo previo
está bien repartido.</p>
<h3>herramientas/VistaPrevia.java</h3>
<p>Para ver el juego completo hacen falta <code>PanelPrincipal</code>, que reúne las cinco pantallas, y
<code>TotitoApp</code>, que abre la ventana; los escribirás en el capítulo 61, cuando existan todas las pantallas.
Pero esperar hasta entonces para ver algo sería un error: si una medida está mal o un color no convence, conviene
descubrirlo <b>ahora</b>, con una sola pantalla, y no al final, con cinco. <code>VistaPrevia</code> es un banco de
pruebas: abre <b>una</b> pantalla suelta en una ventana del mismo tamaño que la del juego.</p>
<p>Hay un detalle: toda pantalla necesita una <code>Navegacion</code> (capítulo 39) para saber adónde ir cuando se
pulsa un botón, y la de verdad (<code>PanelPrincipal</code>) todavía no existe. La solución es fabricar una
<b>navegación de mentira</b>: un objeto que tiene todos los métodos de <code>Navegacion</code> pero no hace nada
(salvo cerrar). Así la pantalla se puede construir y mirar sin el resto del juego.</p>
<p>Como <code>VistaPrevia</code> es una herramienta para ti y no parte del juego, vive en la carpeta
<code>herramientas\</code>, junto a <code>PruebaConsola.java</code> (capítulo 32), y <b>no</b> en
<code>src\</code>. Maven solo compila <code>src\</code> (lo dice el <code>pom.xml</code>), así que la herramienta
no acabará dentro del <code>.jar</code> ni del <code>.exe</code> que repartirás.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>Lo poco que cuesta una pantalla cuando las piezas están bien hechas: herencia, métodos de fábrica y ayudantes.</li>
<li><code>addActionListener</code> con una lambda que llama a la navegación.</li>
<li>Una tarjeta con <code>BoxLayout</code>, margen interior con borde vacío y separaciones fijas.</li>
<li>Una <b>clase anónima que implementa una interfaz</b> y para qué sirve un «doble de prueba».</li>
<li><code>SwingUtilities.invokeLater</code>, <code>JFrame</code>, <code>pack()</code>,
<code>setLocationRelativeTo</code> y <code>EXIT_ON_CLOSE</code>.</li>
<li>A ejecutar un archivo <code>.java</code> suelto con el classpath del proyecto: <code>java -cp target\classes
herramientas\VistaPrevia.java</code>.</li>
<li>A comparar tu resultado con el diseño.</li>
</ul>

<h2>Créalo</h2>
<h3>PantallaMenu.java</h3>
<ol>
<li>NetBeans: <i>&lt;default package&gt;</i> → <i>New → Java Class…</i> → <code>PantallaMenu</code> →
<i>Finish</i>. Borra la plantilla y escribe el código.</li>
<li>Alternativa: <code>New-Item src\PantallaMenu.java</code>.</li>
</ol>
<h3>herramientas\VistaPrevia.java</h3>
<p>La carpeta <code>herramientas</code> está fuera de <code>src</code>, así que no aparece en <i>Source
Packages</i>. Créala como hiciste con <code>PruebaConsola.java</code> en el capítulo 32:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
New-Item herramientas\VistaPrevia.java</pre>
<p>Después ábrela en NetBeans desde la ventana <i>Files</i> (menú <i>Window → Files</i>, o Ctrl+2): despliega
<i>Totito → herramientas</i> y haz doble clic en <code>VistaPrevia.java</code>. Escribe el código y guarda.
NetBeans puede subrayar en rojo los nombres de tus clases (<code>Navegacion</code>, <code>PantallaMenu</code>…)
porque este archivo no está en una carpeta de código del proyecto; es normal y no impide ejecutarlo.</p>
""",
    "archivos": [
        {"ruta": "src/PantallaMenu.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.Dimension</code>: el tamaño de las separaciones entre botones.</p>
<p class="l"><b>L2</b> <code>javax.swing.BorderFactory</code>: el borde vacío que hace de margen interior de la
tarjeta.</p>
<p class="l"><b>L3</b> <code>javax.swing.Box</code>: para fabricar las separaciones rígidas.</p>
<p class="l"><b>L4</b> <code>javax.swing.BoxLayout</code>: para apilar los botones en columna dentro de la
tarjeta.</p>
<p>No hace falta importar nada para el fondo, el encabezado ni los botones: todo eso son clases tuyas del mismo
paquete, y lo de Swing que usan ya lo importaron ellas.</p>
"""),
             ("public class PantallaMenu", r"""
<p class="l"><b>L6–L8</b> Comentario: qué pantalla del diseño es y qué contiene.</p>
<p class="l"><b>L9</b> <code>public class PantallaMenu extends PantallaBase {</code> hereda de la base abstracta:
desde esta línea, la pantalla ya «tiene» fondo con degradado y adornos, encabezado con botón de cerrar y una
columna centrada lista para recibir cosas. No es abstracta, así que de esta sí se pueden crear objetos.</p>
"""),
             ("public PantallaMenu(", r"""
<p class="l"><b>L11</b> <code>public PantallaMenu(Navegacion navegacion) {</code> el constructor recibe la
navegación. Es <code>public</code> porque la crearán <code>VistaPrevia</code> (hoy) y <code>PanelPrincipal</code>
(capítulo 61).</p>
<p class="l"><b>L12</b> <code>super(navegacion);</code> construye primero la parte <code>PantallaBase</code>:
<code>BorderLayout</code>, encabezado arriba (con <code>navegacion::salir</code> para su X) y el panel de contenido
en el centro. Tiene que ser la primera línea. Si la quitaras, Java intentaría llamar a un constructor sin
parámetros de <code>PantallaBase</code>, que no existe, y el compilador daría el error <i>constructor PantallaBase in
class PantallaBase cannot be applied to given types</i>.</p>
"""),
             ("BotonNeon jugar", r"""
<p class="l"><b>L14</b> <code>BotonNeon jugar = BotonNeon.menu("Jugar", Iconos.JUGAR, Tema.ROSA);</code> pide a la
<b>fábrica</b> de <code>BotonNeon</code> (capítulo 44) un botón de estilo menú: 384 × 88, con el icono de
«reproducir» a la izquierda, una rayita divisoria, el texto «Jugar» en negrita de 25 y la flechita a la derecha, todo
en rosa. No hacemos <code>new BotonNeon(...)</code> porque su constructor es privado: los métodos de fábrica
(<code>menu</code>, <code>pildora</code>, <code>contorno</code>, <code>icono</code>) garantizan que cada botón sale
con las medidas del diseño.</p>
<p class="l"><b>L15</b> <code>jugar.addActionListener(e -&gt; navegacion.irAConfiguracion());</code> qué hacer al
pulsarlo. <code>addActionListener</code> recibe un <code>ActionListener</code>, una interfaz con un solo método,
<code>actionPerformed(ActionEvent e)</code>; por eso se puede escribir como lambda (capítulo 25). La lambda recibe
el evento <code>e</code> (no lo usamos, pero hay que nombrarlo) y pide a la navegación ir a la configuración. Fíjate:
el menú no sabe qué es la configuración ni cómo se muestra; solo lo <b>pide</b>. Dentro de la lambda se usa el
parámetro <code>navegacion</code> del constructor: una lambda puede usar variables de fuera mientras no cambien de
valor (son «efectivamente finales»), y esta nunca cambia. Por eso la pantalla no necesita guardarla en un campo.</p>
<p class="l"><b>L16–L17</b> Lo mismo para «Instrucciones»: icono de libro, color azul, y al pulsarlo
<code>irAInstrucciones()</code>.</p>
<p class="l"><b>L18–L19</b> Y «Salir»: icono de puerta con flecha, color morado, y al pulsarlo
<code>salir()</code>. Los tres colores siguen el diseño: rosa para la acción principal, azul y morado para las
secundarias.</p>
"""),
             ("Tarjeta tarjeta", r"""
<p class="l"><b>L21</b> <code>Tarjeta tarjeta = new Tarjeta(Tema.MORADO);</code> la caja de cristal con borde de
neón morado y esquinas de 30 (capítulo 43).</p>
<p class="l"><b>L22</b> <code>tarjeta.setLayout(new BoxLayout(tarjeta, BoxLayout.Y_AXIS));</code> una
<code>Tarjeta</code> es un <code>JPanel</code> y nace con <code>FlowLayout</code>; lo cambiamos por un
<code>BoxLayout</code> vertical para que los botones queden uno debajo del otro. Cada botón ya tiene alineación
centrada (lo hace <code>BotonNeon</code>), así que quedan centrados en la tarjeta.</p>
<p class="l"><b>L23</b> <code>tarjeta.setBorder(BorderFactory.createEmptyBorder(34, 28, 34, 28));</code> margen
interior: 34 arriba y abajo, 28 a los lados. Los 10 primeros píxeles de cada lado son el espacio para el halo de la
tarjeta (<code>Tarjeta.MARGEN</code>), así que entre la caja visible y los botones quedan 18 a los lados y 24 arriba y
abajo.</p>
<p class="l"><b>L24</b> Agrega el botón «Jugar».</p>
<p class="l"><b>L25</b> <code>tarjeta.add(Box.createRigidArea(new Dimension(0, 14)));</code> una separación fija de
14 píxeles. No usamos <code>espacio()</code> porque ese método agrega al contenido de la pantalla, no a la tarjeta.
Y es una <i>rigid area</i> y no un <i>strut</i> por lo que viste en el experimento del capítulo 55: justo aquí, un
<i>strut</i> estiraría la tarjeta a todo el ancho de la ventana.</p>
<p class="l"><b>L26–L28</b> «Instrucciones», otra separación de 14 y «Salir». Con esto, la tarjeta mide de ancho 28 +
384 + 28 = <b>440</b> y de alto 34 + 88 + 14 + 88 + 14 + 88 + 34 = <b>360</b>. Nadie escribió esos números: salen
solos de los botones, las separaciones y el borde.</p>
"""),
             ("relleno();", r"""
<p class="l"><b>L30</b> <code>relleno();</code> un espacio elástico arriba…</p>
<p class="l"><b>L31</b> <code>agregar(tarjeta);</code> …la tarjeta, centrada…</p>
<p class="l"><b>L32</b> <code>relleno();</code> …y otro espacio elástico abajo. Los dos se reparten el sobrante: la
tarjeta queda en el centro vertical de la zona de contenido. Estas tres líneas se leen como una lista de lo que hay
en la pantalla, de arriba abajo; para eso se escribió <code>PantallaBase</code>.</p>
<p class="l"><b>L33–L34</b> Cierran el constructor y la clase. La pantalla no tiene ningún método más: todo su
trabajo es armarse.</p>
"""),
         ]},
        {"ruta": "herramientas/VistaPrevia.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.Dimension</code>: el tamaño de la ventana.</p>
<p class="l"><b>L2</b> <code>javax.swing.JFrame</code>: la <b>ventana</b> de Swing, con barra de título, bordes y
los botones de minimizar, maximizar y cerrar del sistema operativo. Ya la usaste en <code>JuegoMain</code> (capítulo
33).</p>
<p class="l"><b>L3</b> <code>javax.swing.JPanel</code>: el tipo de la variable que guarda la pantalla.</p>
<p class="l"><b>L4</b> <code>javax.swing.SwingUtilities</code>: una caja de herramientas de métodos
<code>static</code> para Swing; usaremos <code>invokeLater</code>.</p>
"""),
             ("public class VistaPrevia", r"""
<p class="l"><b>L6–L15</b> Comentario de la clase, que funciona como instrucciones de uso: qué hace (abre una
pantalla suelta), por qué existe (todavía no hay <code>PanelPrincipal</code> ni <code>TotitoApp</code>), qué
esperar (los botones que cambian de pantalla no hacen nada, salvo cerrar), cómo ver otra pantalla (cambiar la línea
marcada con <code>&lt;-- AQUI</code>) y cómo ejecutarla. En el comando del comentario las rutas llevan
<code>/</code>; en Windows Java acepta tanto <code>/</code> como <code>\</code>.</p>
<p class="l"><b>L16</b> <code>public class VistaPrevia {</code> una clase sin <code>extends</code>: no es un
componente, solo el lugar donde vive el <code>main</code>.</p>
"""),
             ("public static void main", r"""
<p class="l"><b>L18</b> <code>public static void main(String[] args) {</code> el punto de entrada de cualquier
programa Java (capítulo 11): lo primero que se ejecuta.</p>
<p class="l"><b>L19</b> <code>SwingUtilities.invokeLater(() -&gt; {</code> todo lo que sigue, hasta la línea 40,
va dentro de una lambda que se entrega a <code>invokeLater</code>. Recuerda la regla del capítulo 37: Swing no es
seguro para usar desde varios hilos a la vez, y todos los componentes deben crearse y tocarse desde un hilo
especial, el <b>hilo de eventos</b> (EDT). El <code>main</code> corre en otro hilo, el principal.
<code>invokeLater</code> pone la lambda en la cola del hilo de eventos y vuelve enseguida; el <code>main</code>
termina, pero el programa sigue vivo mientras haya una ventana abierta. Es el mismo arranque que tendrá
<code>TotitoApp</code>.</p>
"""),
             ("Navegacion sinNavegacion", r"""
<p class="l"><b>L20</b> Comentario: una navegación «de mentira»; cada método existe, pero no hace nada.</p>
<p class="l"><b>L21</b> <code>Navegacion sinNavegacion = new Navegacion() {</code> aquí pasa algo que parece
prohibido: <code>new</code> de una <b>interfaz</b>. Una interfaz no se puede instanciar sola (no tiene código), pero
con llaves detrás se crea una <b>clase anónima</b> que la implementa en ese mismo momento (capítulo 25): una clase
sin nombre, de usar y tirar, cuyo único objeto se guarda en <code>sinNavegacion</code>. La clase anónima está
obligada a escribir <b>todos</b> los métodos de la interfaz; si faltara uno, el compilador diría <i>&lt;anonymous
VistaPrevia$1&gt; is not abstract and does not override abstract method ...</i>.</p>
<p class="l"><b>L22</b> <code>@Override public void irAlMenu() { }</code> la anotación, la firma y el cuerpo en una
sola línea. Las llaves vacías <code>{ }</code> son un cuerpo sin instrucciones: el método existe, se puede llamar, y
no hace nada. Se escribe en una línea porque no hay nada que leer dentro.</p>
<p class="l"><b>L23–L24</b> Lo mismo para <code>irAInstrucciones</code> e <code>irAConfiguracion</code>. Por eso,
en la vista previa, pulsar «Jugar» o «Instrucciones» no hace nada: el botón llama al método, y el método está
vacío.</p>
<p class="l"><b>L25</b> <code>iniciarPartida(Jugador j1, Jugador j2, Partida.Modo modo)</code>: al implementar un
método, los <b>tipos</b> de los parámetros deben coincidir exactamente con los de la interfaz; los <b>nombres</b> no
(aquí <code>j1</code> en vez de <code>jugador1</code>, por brevedad). Como menciona <code>Jugador</code> y
<code>Partida</code>, esas clases tienen que estar compiladas: lo están desde los capítulos 30 y 38.</p>
<p class="l"><b>L26–L27</b> <code>mostrarResultado</code> y <code>jugarDeNuevo</code>, vacíos.</p>
<p class="l"><b>L28</b> <code>@Override public void salir() { System.exit(0); }</code> el único que sí hace algo:
<code>System.exit(0)</code> termina el programa (el 0 le dice al sistema operativo «terminé bien»). Así, el botón
«Salir» y la X del encabezado cierran la vista previa, como harán en el juego.</p>
<p class="l"><b>L29</b> <code>};</code> la llave cierra la clase anónima y el punto y coma cierra la instrucción
que empezó en la línea 21 (<code>Navegacion sinNavegacion = ...</code>). Olvidar ese <code>;</code> es un error muy
común con las clases anónimas.</p>
<p>A un objeto así, que se hace pasar por el verdadero para poder probar otra cosa, se le llama <b>doble de
prueba</b> (en inglés, <i>stub</i> o <i>fake</i>). Lo volverás a ver cuando escribas pruebas automáticas (capítulo
69).</p>
"""),
             ("JPanel pantalla", r"""
<p class="l"><b>L31</b> <code>JPanel pantalla = new PantallaMenu(sinNavegacion);   // &lt;-- AQUI</code> crea la
pantalla que se quiere ver y le pasa la navegación de mentira. La variable es de tipo <code>JPanel</code>, no
<code>PantallaMenu</code>: como toda pantalla <i>es un</i> <code>JPanel</code> (<code>PantallaMenu</code> →
<code>PantallaBase</code> → <code>JPanel</code>), a la derecha del <code>=</code> se puede poner cualquiera y el
resto del programa no cambia (polimorfismo, capítulo 23). Por eso es <b>la línea que se cambia</b> para ver otra
pantalla, y el comentario <code>// &lt;-- AQUI</code> la señala para encontrarla rápido.</p>
<p class="l"><b>L32</b> <code>pantalla.setPreferredSize(new Dimension(640, 690));</code> le da a la pantalla el
mismo tamaño que tendrá la ventana del juego (capítulo 36; en el capítulo 61 será
<code>PanelPrincipal.ANCHO</code> × <code>ALTO</code>). Sin esta línea, la ventana tomaría el tamaño que la pantalla
«prefiere» por su contenido: 440 × 466, justo la tarjeta y el encabezado, sin aire alrededor. No se parecería al
juego.</p>
"""),
             ("JFrame ventana", r"""
<p class="l"><b>L34</b> <code>JFrame ventana = new JFrame("Vista previa");</code> crea la ventana (aún invisible)
con ese título en su barra.</p>
<p class="l"><b>L35</b> <code>ventana.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);</code> al cerrar la ventana
con la X del sistema, termina el programa. Lo normal en un <code>JFrame</code> es solo <b>esconderla</b>: el
programa seguiría vivo, invisible, y PowerShell quedaría esperando hasta que pulsaras Ctrl+C.</p>
<p class="l"><b>L36</b> <code>ventana.setContentPane(pantalla);</code> la pantalla pasa a ser <b>todo</b> el
contenido de la ventana (el «panel de contenido», lo que hay debajo de la barra de título).</p>
<p class="l"><b>L37</b> <code>ventana.pack();</code> ajusta el tamaño de la ventana al tamaño preferido de su
contenido: 640 × 690 más lo que midan la barra de título y los bordes de Windows.</p>
<p class="l"><b>L38</b> <code>ventana.setLocationRelativeTo(null);</code> la centra en la pantalla del monitor.
Con <code>null</code> significa «respecto a nada», es decir, al centro de la pantalla.</p>
<p class="l"><b>L39</b> <code>ventana.setVisible(true);</code> la muestra. Va al final a propósito: si se mostrara
antes de <code>pack()</code>, se vería un instante diminuta en una esquina y luego saltaría a su sitio.</p>
<p class="l"><b>L40</b> <code>});</code> cierra la lambda (<code>}</code>) y la llamada a <code>invokeLater</code>
(<code>);</code>).</p>
<p class="l"><b>L41–L42</b> Cierran <code>main</code> y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Ejecuta la vista previa: el momento de la verdad</h2>
<ol>
<li><b>Compila el proyecto.</b> En NetBeans, <i>Run → Clean and Build Project</i> (Shift+F11). Espera
<code>BUILD SUCCESS</code>. Esto deja todas las clases de <code>src\</code> compiladas en la carpeta
<code>target\classes</code>.</li>
<li><b>Abre PowerShell en la carpeta del proyecto</b>:
<pre class="ps">cd $HOME\Proyectos\Totito</pre></li>
<li><b>Ejecuta la vista previa</b>:
<pre class="ps">java -cp target\classes herramientas\VistaPrevia.java</pre></li>
</ol>
<p>Qué significa cada parte del comando:</p>
<table class="tabla">
<tr><th>Parte</th><th>Qué hace</th></tr>
<tr><td><code>java</code></td><td>el lanzador de Java que instalaste en el capítulo 4.</td></tr>
<tr><td><code>-cp target\classes</code></td><td><i>classpath</i>: dónde buscar las clases ya compiladas. Ahí están
<code>PantallaMenu</code>, <code>Tema</code>, <code>BotonNeon</code> y todas las demás.</td></tr>
<tr><td><code>herramientas\VistaPrevia.java</code></td><td>un archivo <b>fuente</b>, no compilado. Desde Java 11, si
le das a <code>java</code> un <code>.java</code>, lo compila en memoria y lo ejecuta en el acto (lo hiciste con
<code>PruebaConsola</code> en el capítulo 32). No queda ningún <code>.class</code> de la herramienta en tu
proyecto.</td></tr>
</table>
<p>Se abre una ventana titulada «Vista previa» con el menú del Totito. Ponla al lado de la captura del juego
terminado y de la imagen de diseño:</p>
<figure><img src="capturas/1-menu.png"><figcaption>Lo que debes ver: el menú del Totito construido con Java2D. Si
la tuya se parece a esta, todo lo de los capítulos 40 a 56 funciona.</figcaption></figure>
<figure><img src="diseno/menu.jpg"><figcaption>El diseño original del capítulo 34, para comparar.</figcaption></figure>

<div class="caja hito"><b>Hito: ¡ya se ve!</b> Es la primera pantalla de la versión 1.0 del Totito. Todo lo que
ves lo dibuja tu código, sin una sola imagen: el degradado y el resplandor del fondo, las X y O gigantes y los
puntitos (<code>PantallaBase</code>), el logotipo, el título con degradado rosa-cian y el lema
(<code>Encabezado</code>), la caja de cristal (<code>Tarjeta</code>), los tres botones con su icono, su divisor y
su flechita (<code>BotonNeon</code> e <code>Iconos</code>), y el brillo de neón de cada borde
(<code>Dibujo.trazoNeon</code>). Haz una captura con <i>Win+Shift+S</i> y guárdala: dentro de unos capítulos te
gustará recordar este momento.</div>

<h3>Pruébala</h3>
<ul>
<li>Pasa el ratón por encima de cada botón: brilla más (el efecto <i>rollover</i> de <code>BotonNeon</code>,
capítulo 44) y el puntero se vuelve una manito.</li>
<li>Pulsa «Jugar» o «Instrucciones»: <b>no pasa nada</b>, y es correcto. El botón llama a
<code>irAConfiguracion()</code> o a <code>irAInstrucciones()</code> de la navegación de mentira, que están vacíos.</li>
<li>Pulsa «Salir» o la X rosa del encabezado: el programa termina (<code>System.exit(0)</code>). Cerrar con la X de
la ventana también lo termina (<code>EXIT_ON_CLOSE</code>).</li>
<li>Agranda la ventana o maximízala: la tarjeta sigue centrada (los dos <code>relleno()</code>) y los adornos del
fondo se recolocan, porque sus posiciones son proporciones del tamaño.</li>
</ul>

<h3>Lo que es igual y lo que no</h3>
<p>Compara las dos imágenes con calma, como un diseñador (capítulo 34). La <b>estructura</b> es la misma: encabezado
con logotipo, título y lema; tarjeta morada centrada; tres botones con icono, divisor, texto y flecha; los mismos
colores; los adornos en los mismos sitios. Las <b>diferencias</b> también tienen explicación:</p>
<ul>
<li><b>La letra.</b> El diseño usa una fuente redondeada y gruesa. <code>Tema</code> (capítulo 40) busca primero
«Nunito», «Poppins» o «Montserrat» y, si no están instaladas, usa «Segoe UI», que es la de Windows. Si instalas
la fuente gratuita Nunito (de Google Fonts) y vuelves a ejecutar, el menú se acercará más al diseño. Ojo: en las
computadoras de otras personas que no la tengan, el juego usará Segoe UI.</li>
<li><b>Las proporciones.</b> La imagen de diseño es cuadrada; la ventana del juego mide 640 × 690 para caber en
pantallas de portátil (capítulo 36).</li>
<li><b>El brillo.</b> Un diseño hecho como imagen puede tener halos más suaves; nuestro neón son seis trazos
superpuestos (capítulo 41), que se acercan mucho con muy poco código.</li>
</ul>

<h2>Cómo funciona por dentro</h2>
<p>Esto es lo que pasa, en orden, desde que pulsas Enter hasta que ves la ventana:</p>
<ol>
<li><code>java</code> compila <code>VistaPrevia.java</code> en memoria. Cada vez que el código nombra una clase tuya
(<code>Navegacion</code>, <code>PantallaMenu</code>…), la busca en <code>target\classes</code>.</li>
<li>Arranca <code>main</code>, que entrega una lambda a <code>invokeLater</code> y termina.</li>
<li>El hilo de eventos ejecuta la lambda: crea la navegación de mentira y llama a
<code>new PantallaMenu(sinNavegacion)</code>.</li>
<li>El constructor de <code>PantallaMenu</code> llama a <code>super(navegacion)</code>: <code>PantallaBase</code> pone
el <code>BorderLayout</code>, crea el <code>Encabezado</code> (que a su vez crea su <code>BotonNeon</code> de cerrar)
y el panel de contenido con su <code>BoxLayout</code>.</li>
<li>De vuelta en <code>PantallaMenu</code>: se fabrican los tres botones, se conectan sus acciones, se arma la
tarjeta y se agregan relleno, tarjeta y relleno.</li>
<li>Se crea la ventana, se le pone la pantalla de 640 × 690, <code>pack()</code>, centrado y
<code>setVisible(true)</code>.</li>
<li>Swing acomoda todo (llama a los <code>doLayout</code>) y luego lo pinta, de atrás hacia delante.</li>
</ol>
<p>Las posiciones que resultan (comprobadas dibujando la pantalla):</p>
<table class="tabla">
<tr><th>Componente</th><th>x</th><th>y</th><th>Ancho × alto</th><th>Por qué</th></tr>
<tr><td>Encabezado</td><td>0</td><td>0</td><td>640 × 96</td><td><code>NORTH</code> del <code>BorderLayout</code></td></tr>
<tr><td>Botón cerrar</td><td>566</td><td>19</td><td>58 × 58</td><td><code>doLayout</code> del encabezado (capítulo 45)</td></tr>
<tr><td>Contenido</td><td>0</td><td>96</td><td>640 × 594</td><td><code>CENTER</code></td></tr>
<tr><td>Tarjeta</td><td>100</td><td>208</td><td>440 × 360</td><td>centrada; rellenos de 112 arriba y abajo</td></tr>
<tr><td>Jugar</td><td>128</td><td>242</td><td>384 × 88</td><td>208 + 34 de margen</td></tr>
<tr><td>Instrucciones</td><td>128</td><td>344</td><td>384 × 88</td><td>242 + 88 + 14</td></tr>
<tr><td>Salir</td><td>128</td><td>446</td><td>384 × 88</td><td>344 + 88 + 14</td></tr>
</table>
<p>Y el orden de pintado: primero el fondo de <code>PantallaBase</code> (degradado, resplandor, adornos); encima, el
encabezado (su caja translúcida, el logotipo, el título, el lema y su botón); luego la tarjeta (cristal y borde);
por último, cada botón. Cada capa tapa en parte a la anterior; por eso los adornos quedan detrás de todo.</p>

<h2>Compila y prueba: si algo sale mal</h2>
<table class="tabla">
<tr><th>Mensaje</th><th>Causa y solución</th></tr>
<tr><td><i>error: cannot find symbol ... class PantallaMenu</i> (o <code>Navegacion</code>)</td><td>No hiciste
<i>Clean and Build</i>, falló, o no estás en la carpeta del proyecto (la ruta <code>target\classes</code> es
relativa). Comprueba con <code>Get-ChildItem target\classes</code> que estén los <code>.class</code>.</td></tr>
<tr><td><i>Error: Could not find or load main class …VistaPrevia.java</i> (con <i>ClassNotFoundException</i>)</td><td>Java no encontró el archivo y lo tomó por un nombre de clase: PowerShell no está en
<code>$HOME\Proyectos\Totito</code>, o el archivo está en otra carpeta o con otro nombre.</td></tr>
<tr><td><i>java : El término 'java' no se reconoce…</i></td><td>Java no está en el PATH: vuelve al capítulo 4 (y
cierra y abre PowerShell después de instalar).</td></tr>
<tr><td><i>is not abstract and does not override abstract method irAlMenu()</i> (u otro)</td><td>Falta un método en
la navegación de mentira o su firma no coincide con la interfaz del capítulo 39.</td></tr>
<tr><td><i>';' expected</i> cerca de la línea 29</td><td>Falta el <code>;</code> después de la llave que cierra la
clase anónima: <code>};</code>.</td></tr>
<tr><td>Cambié algo en <code>src</code> y la vista previa sigue igual</td><td>La vista previa usa lo compilado en
<code>target\classes</code>. Tras cambiar cualquier archivo de <code>src</code>, vuelve a compilar (Shift+F11). Los
cambios en <code>VistaPrevia.java</code>, en cambio, no necesitan compilar el proyecto.</td></tr>
</table>
<div class="caja consejo"><b>El ciclo de trabajo de aquí en adelante</b> Cambias algo en NetBeans → Shift+F11 → en
PowerShell, flecha arriba (↑) para recuperar el último comando → Enter. En segundos ves el resultado.</div>
<div class="caja cuidado"><b>No uses Run Project (F6) para esto</b> El proyecto está configurado para arrancar
<code>TotitoApp</code> (en el <code>pom.xml</code>), que escribirás en el capítulo 61. Hasta entonces, F6 no sirve
para ver pantallas sueltas; para eso está la vista previa.</div>

<div class="caja git"><b>Git</b> Este capítulo suma dos archivos, y van juntos porque la herramienta nace para ver
esta pantalla:
<pre class="ps">git status
git add src\PantallaMenu.java herramientas\VistaPrevia.java
git commit -m "PantallaMenu y VistaPrevia: primera pantalla visible"
git push</pre>
Recuerda que <code>target\</code> está en el <code>.gitignore</code>: los <code>.class</code> nunca se suben, solo el
código fuente.</div>

<h2>Cambiar la línea AQUI para ver otras pantallas</h2>
<p>En cada uno de los próximos capítulos escribirás una pantalla nueva y la verás cambiando <b>solo</b> la línea
31. Por ejemplo, en el capítulo 57:</p>
<pre class="java">JPanel pantalla = new PantallaInstrucciones(sinNavegacion);   // &lt;-- AQUI</pre>
<p>Guardas, compilas el proyecto si cambiaste algo en <code>src</code>, y ejecutas el mismo comando. Las pantallas
de juego y de resultado necesitan además una partida para mostrar algo interesante; en sus capítulos (59 y 60) se
indica qué escribir.</p>
<div class="caja consejo"><b>¿Hago commit de la línea cambiada?</b> Es una herramienta: puedes dejar la línea
apuntando a la última pantalla que hiciste y subirla con el commit de ese capítulo, o devolverla al menú con
<code>git restore herramientas\VistaPrevia.java</code> (capítulo 9). Lo importante es no mezclar en un mismo commit
cambios que no tienen relación.</div>

<h3>Extra: ver juntas las piezas de los capítulos 49 a 54</h3>
<p>Las seis piezas de los capítulos 49 a 54 todavía no tienen pantalla. Puedes verlas ya con una pantalla de
prueba. En el modo de archivo fuente, un <code>.java</code> puede tener <b>varias clases</b>; la primera debe ser
la del <code>main</code>. Así que, <b>después</b> de hacer el commit de arriba, agrega esta clase al final de
<code>VistaPrevia.java</code>, debajo de la última llave:</p>
<pre class="java">class PantallaPrueba extends PantallaBase {

    PantallaPrueba(Navegacion navegacion) {
        super(navegacion);
        TarjetaJugador ia = new TarjetaJugador("Jugador 2", Tema.AZUL);
        ia.setComputadora(true);
        OpcionModo opcion = new OpcionModo(Iconos.PERSONAS, "2 jugadores", "Turnos en el mismo equipo");
        opcion.setSeleccionada(true);
        PanelMarcador marcador = new PanelMarcador();
        marcador.mostrar(new Partida(new Jugador("Ana", 'X'), new Jugador("Luis", 'O'), Partida.Modo.DOS_JUGADORES));

        relleno();
        agregar(fila(8, new TarjetaJugador("Jugador 1", Tema.FRESA), ia));
        agregar(new SelectorSimbolo());
        agregar(fila(6, opcion, new IconoResultado()));
        agregar(marcador);
        agregar(new PasoInstruccion(1, Tema.ROSA, "Dos jugadores se turnan&lt;br&gt;para marcar X y O.", 400));
        relleno();
    }
}</pre>
<p>Y cambia la línea AQUI por:</p>
<pre class="java">JPanel pantalla = new PantallaPrueba(sinNavegacion);   // &lt;-- AQUI</pre>
<p>Ejecuta el mismo comando. Verás, de arriba abajo: las dos tarjetas de jugador (la segunda ya convertida en
«Computadora», con su chip y la caja bloqueada), el selector de símbolos, una opción de modo marcada junto al
trofeo con destellos, el marcador de Ana contra Luis con Ana encendida (la X empieza) y un paso de instrucciones.
Todo cabe justo en los 640 × 690. Prueba a escribir en la caja del Jugador 1 (no deja pasar de 14 letras), a pulsar
la O del selector (cambian el brillo y la leyenda) y a pulsar la opción de modo (no pasa nada: nadie le dio un
callback, capítulo 51).</p>
<p>Cuando termines, devuelve el archivo a como estaba en el commit:</p>
<pre class="ps">git restore herramientas\VistaPrevia.java</pre>

<h2>Resumen</h2>
<ul>
<li><code>PantallaMenu</code> hereda de <code>PantallaBase</code> y solo ensambla: tres botones de fábrica, una
tarjeta con <code>BoxLayout</code>, borde vacío y separaciones rígidas, y <code>relleno / agregar /
relleno</code>.</li>
<li>Cada botón llama a la <code>Navegacion</code> con una lambda; la pantalla no conoce a las demás.</li>
<li><code>VistaPrevia</code> abre una pantalla suelta con una navegación de mentira, una clase anónima que
implementa la interfaz con métodos vacíos (un doble de prueba).</li>
<li>Los componentes de Swing se crean en el hilo de eventos con <code>SwingUtilities.invokeLater</code>.</li>
<li><code>JFrame</code> + <code>setContentPane</code> + <code>pack</code> + <code>setLocationRelativeTo(null)</code>
+ <code>setVisible(true)</code>, en ese orden, y <code>EXIT_ON_CLOSE</code> para que cerrar termine el programa.</li>
<li>Se ejecuta con <code>java -cp target\classes herramientas\VistaPrevia.java</code> tras compilar el proyecto.</li>
<li>Para ver otra pantalla se cambia solo la línea marcada <code>// &lt;-- AQUI</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Bancos de prueba de interfaz</b>: en cualquier aplicación de escritorio, una clase como
<code>VistaPrevia</code> que abra una ventana o un formulario suelto (la ficha de un cliente, una factura) sin
iniciar sesión ni conectarse a la base de datos. En el desarrollo web existe lo mismo a lo grande (herramientas como
Storybook).</li>
<li><b>Dobles de prueba</b>: una «pasarela de pago de mentira» que siempre aprueba, un «enviador de correos» que
solo escribe en la consola, un «sensor» que devuelve temperaturas inventadas. Permiten probar una parte sin tener
lista (o sin arriesgar) la otra.</li>
<li><b>Arranque correcto de Swing</b>: todo programa Swing debería empezar con
<code>SwingUtilities.invokeLater</code>, como aquí.</li>
<li><b>Pantallas que solo ensamblan</b>: cuando tienes una base y componentes reutilizables, una pantalla nueva de
otro proyecto (el menú de una calculadora o de un inventario) son unas pocas líneas.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>En la navegación de mentira, haz que <code>irAConfiguracion()</code> escriba «Ir a configuración» en la consola
(<code>System.out.println</code>) y lo mismo con <code>irAInstrucciones()</code>. Pulsa los botones y comprueba en
PowerShell que cada uno llama al método correcto.</li>
<li>Cambia la separación entre botones de 14 a 24. ¿Cuánto mide ahora la tarjeta de alto? ¿Y cada relleno?</li>
<li>Agrega un cuarto botón «Créditos» (por ejemplo con <code>Iconos.LIBRO</code> y <code>Tema.CIAN</code>) que de
momento no haga nada. Calcula antes el nuevo alto de la tarjeta y comprueba que cabe en los 584 píxeles útiles.</li>
<li>Quita el primer <code>relleno()</code> de <code>PantallaMenu</code> y ejecuta. ¿Dónde queda la tarjeta y por
qué? Luego déjalo como estaba.</li>
<li>Cambia el tamaño de la línea 32 a 800 × 690. ¿Qué se mueve y qué no? Explícalo con lo que sabes de
<code>relleno()</code> y de las posiciones proporcionales del fondo.</li>
</ol></div>
""",
}
