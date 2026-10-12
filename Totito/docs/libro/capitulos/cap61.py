CAPITULO = {
    "numero": 61,
    "titulo": "PanelPrincipal.java y TotitoApp.java: el juego completo",
    "antes": r"""<p class="entrada">Tienes cinco pantallas que funcionan cada una por su cuenta, pero nadie las une: el botón «Jugar»
del menú pide «llévame a la configuración» y nadie lo escucha. En este capítulo escribes las dos últimas clases del
Totito: <code>PanelPrincipal</code>, que guarda las cinco pantallas como un mazo de cartas y cambia de una a otra, y
<code>TotitoApp</code>, la ventana y su <code>main</code>. Al terminar pulsarás F6 y jugarás el Totito v1.0 completo, lo
probarás de punta a punta y lo publicarás en <code>main</code> con un Pull Request y la etiqueta <code>v1.0.0</code>.</p>

<h2>Por qué existen estos dos archivos</h2>
<p>Desde el capítulo 39, cada pantalla recibe un objeto <code>Navegacion</code> y le pide cosas: <code>irAlMenu()</code>,
<code>iniciarPartida(...)</code>, <code>salir()</code>… Hasta ahora ese objeto era la navegación «de mentira» de la vista
previa, que no hacía nada. Falta la de verdad: <b>alguien que tenga todas las pantallas y sepa cambiar de una a
otra</b>. Ese es <code>PanelPrincipal</code>. Además guarda la <code>Partida</code> en curso, porque tres momentos
distintos la necesitan: empezar, mostrar el resultado y jugar de nuevo.</p>
<p>Y falta lo más básico: una <b>ventana</b> donde poner todo y un <code>main</code> por donde empiece el programa. Ese
es <code>TotitoApp</code>. Recuerda que el <code>pom.xml</code> del capítulo 5 ya decía
<code>&lt;exec.mainClass&gt;TotitoApp&lt;/exec.mainClass&gt;</code>: desde entonces, el botón <i>Run Project</i> (F6)
esperaba esta clase. Hoy por fin existe.</p>
<p>¿Por qué dos clases y no una? Porque hacen cosas distintas:</p>
<table class="tabla">
<tr><th>Clase</th><th>Es un…</th><th>Se ocupa de…</th><th>No sabe…</th></tr>
<tr><td><code>PanelPrincipal</code></td><td><code>JPanel</code></td><td>las pantallas, el cambio entre ellas y la partida
en curso</td><td>que existe una ventana, ni cómo se cierra el programa</td></tr>
<tr><td><code>TotitoApp</code></td><td><code>JFrame</code> (ventana)</td><td>el título, el icono, el tamaño fijo, centrar,
cerrar y arrancar</td><td>nada de pantallas ni de partidas</td></tr>
</table>
<p>Que <code>PanelPrincipal</code> sea un panel y no la ventana tiene una ventaja enorme: se puede crear <b>sin abrir
ninguna ventana</b>. Así se probó el flujo completo del juego en un servidor sin pantalla, y así se generaron las
capturas de este libro, dibujando el panel en una imagen.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li><code>CardLayout</code>: varias pantallas en el mismo sitio, una visible a la vez.</li>
<li><code>implements</code>: cumplir una interfaz (<code>Navegacion</code>) con todos sus métodos, y el error que da si
falta uno.</li>
<li>Pasar <code>this</code> a otros objetos para que te avisen.</li>
<li>Un <code>Runnable</code> como «qué hacer al salir», decidido desde fuera.</li>
<li><code>JFrame</code>: título, cierre, tamaño fijo, <code>pack()</code>, centrar y el icono de la ventana dibujado con
código en una <code>BufferedImage</code>.</li>
<li>El método <code>main</code> definitivo y <code>SwingUtilities.invokeLater</code>: por qué la ventana se crea en el
hilo de Swing.</li>
<li>Ejecutar el proyecto completo con F6, probarlo con una lista de pruebas manuales y publicarlo: Pull Request, merge y
etiqueta <code>v1.0.0</code>.</li>
</ul>

<h2>Créalos</h2>
<p>En la rama <code>interfaz-neon</code> (compruébalo con <code>git branch --show-current</code>), crea las dos clases en
NetBeans: clic derecho en <i>Source Packages → &lt;default package&gt;</i> → <i>New → Java Class…</i> →
<code>PanelPrincipal</code> → <i>Finish</i>; y otra vez para <code>TotitoApp</code>. Borra las plantillas. Con
PowerShell:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
New-Item src\PanelPrincipal.java, src\TotitoApp.java
notepad src\PanelPrincipal.java</pre>
<p>Escribe primero <code>PanelPrincipal</code>: <code>TotitoApp</code> lo usa, y así NetBeans no te marcará errores
mientras escribes.</p>
""",
    "archivos": [
        {"ruta": "src/PanelPrincipal.java",
         "bloques": [
             (None, r"""<p class="l"><b>L1</b> <code>java.awt.CardLayout</code>: el organizador «mazo de cartas» del capítulo 37.
Pone todos los componentes en el mismo sitio, uno encima de otro, y solo deja ver uno.</p>
<p class="l"><b>L2</b> <code>java.awt.Dimension</code>, para el tamaño del panel.</p>
<p class="l"><b>L3</b> <code>javax.swing.JPanel</code>: la clase de la que hereda.</p>
<p class="l"><b>L4</b> En blanco.</p>"""),
             ("public class PanelPrincipal", r"""<p class="l"><b>L5–L12</b> El comentario resume las tres cosas que hace
(contener las pantallas, cambiar de una a otra, guardar la partida) y explica la decisión de que sea un panel y no la
ventana.</p>
<p class="l"><b>L13</b> <code>public class PanelPrincipal extends JPanel implements Navegacion</code>. Dos palabras clave
en la misma línea:</p>
<ul>
<li><code>extends JPanel</code>: <b>es</b> un panel de Swing (herencia, capítulo 22). Se puede poner dentro de una ventana.</li>
<li><code>implements Navegacion</code>: <b>cumple</b> la interfaz del capítulo 39 (capítulo 24). Es una promesa al
compilador: «tengo los siete métodos de <code>Navegacion</code>». Si falta uno, no compila:
<code>PanelPrincipal is not abstract and does not override abstract method salir() in Navegacion</code>. Una clase solo
puede heredar de una clase (<code>extends</code>), pero puede implementar varias interfaces.</li>
</ul>
<p class="l">Gracias al <code>implements</code>, un <code>PanelPrincipal</code> se puede entregar en cualquier lugar donde
se pida una <code>Navegacion</code>. Eso es lo que hará con las cinco pantallas.</p>
<p class="l"><b>L14</b> En blanco.</p>"""),
             ("public static final int ANCHO", r"""<p class="l"><b>L15</b> El comentario explica de dónde sale el tamaño: debe caber
en una pantalla de 1366 × 768, muy común en laptops, contando la barra de título de la ventana y la barra de tareas de
Windows (capítulo 36).</p>
<p class="l"><b>L16–L17</b> Ancho y alto del juego: 640 × 690 píxeles. Son <code>public</code> (además de
<code>static final</code>) porque son un dato útil para otras clases: una herramienta o una prueba que quiera dibujar el
panel en una imagen del tamaño correcto lo lee de aquí, sin repetir el número.</p>
<p class="l"><b>L18</b> En blanco.</p>"""),
             ("private static final String MENU", r"""<p class="l"><b>L19–L23</b> Los <b>nombres de las cartas</b>.
<code>CardLayout</code> identifica cada pantalla por un texto: al agregarla se le da un nombre, y para mostrarla se pide
por ese nombre. Se guardan en constantes por una razón muy práctica: si escribieras <code>"configuracion"</code> en un
sitio y <code>"configuración"</code> (con tilde) en otro, el programa compilaría, pero el botón no haría nada, sin error
ni aviso. Con constantes, un error de escritura en el nombre de la constante <b>no compila</b>, y el compilador te lo
señala. Es la regla de los «textos mágicos» (capítulo 27).</p>
<p class="l"><b>L24</b> En blanco.</p>"""),
             ("private final CardLayout cartas", r"""<p class="l"><b>L25</b> El organizador. Se guarda en un atributo porque cada
cambio de pantalla le pide <code>show</code> a él; si solo hicieras <code>setLayout(new CardLayout())</code> sin guardarlo,
tendrías que recuperarlo con <code>(CardLayout) getLayout()</code> cada vez.</p>
<p class="l"><b>L26–L27</b> Las dos pantallas a las que <code>PanelPrincipal</code> tiene que <b>darles datos</b>: a la de
juego, la partida (<code>comenzar</code>); a la de resultado, la partida terminada (<code>mostrar</code>). Por eso se
guardan en atributos. El menú, las instrucciones y la configuración no necesitan nada después de crearse: no hacen falta
atributos para ellas.</p>
<p class="l"><b>L28</b> Qué hacer cuando alguien pide salir. Es un <code>Runnable</code> que llega desde fuera
(<code>TotitoApp</code> decide qué significa «salir»). El panel no sabe de ventanas ni de <code>System.exit</code>.</p>
<p class="l"><b>L29</b> La partida en curso. Empieza en <code>null</code> y no es <code>final</code>: cada «Comenzar
partida» crea una nueva.</p>
<p class="l"><b>L30</b> En blanco.</p>"""),
             ("public PanelPrincipal(Runnable alSalir)", r"""<p class="l"><b>L31</b> Comentario con la etiqueta
<code>@param</code>: en la documentación de Java (Javadoc), describe un parámetro. NetBeans la muestra cuando pasas el
ratón por encima de una llamada al constructor.</p>
<p class="l"><b>L32</b> El constructor recibe la acción de salir.</p>
<p class="l"><b>L33</b> La guarda en el atributo.</p>
<p class="l"><b>L34</b> <code>setLayout(cartas)</code>: este panel organizará a sus hijos como un mazo de cartas. Debe
hacerse <b>antes</b> de agregar las pantallas, porque <code>CardLayout</code> anota el nombre de cada carta en el momento
de agregarla.</p>
<p class="l"><b>L35</b> El tamaño preferido: 640 × 690. Es lo que <code>pack()</code>, en <code>TotitoApp</code>, usará
para dar tamaño a la ventana.</p>
<p class="l"><b>L36</b> En blanco.</p>"""),
             ("pantallaJuego = new PantallaJuego(this)", r"""<p class="l"><b>L37–L38</b> Crea las dos pantallas que se guardan en
atributos. A cada una se le pasa <code>this</code>, «yo mismo», como su <code>Navegacion</code>. Desde ese momento, cuando
la pantalla de juego llame a <code>navegacion.mostrarResultado(...)</code>, estará llamando al método de la L75 de este
objeto. La pantalla no sabe que habla con un <code>PanelPrincipal</code>: solo ve la interfaz. Eso es el bajo
acoplamiento del capítulo 27.</p>
<p class="l"><b>L39</b> <code>add(new PantallaMenu(this), MENU)</code> crea el menú y lo agrega al mazo con el nombre
<code>"menu"</code>. El segundo argumento de <code>add</code> es la «restricción» del organizador: en un
<code>BorderLayout</code> sería <code>BorderLayout.NORTH</code>; en un <code>CardLayout</code>, el nombre de la carta.</p>
<p class="l"><b>L40–L41</b> Las instrucciones y la configuración, igual: se crean, se agregan con su nombre y no se
guardan en ningún atributo (el mazo las conserva).</p>
<p class="l"><b>L42–L43</b> Se agregan las dos pantallas que ya existían.</p>
<p class="l"><b>L44</b> Muestra el menú. La primera carta agregada ya sería la visible, pero escribirlo deja claro con qué
pantalla arranca el juego, y si algún día cambias el orden de los <code>add</code>, sigue arrancando en el menú.</p>
<p class="l">Las cinco pantallas se crean <b>todas al arrancar</b> y viven mientras dure el programa. Cambiar de pantalla
no crea ni destruye nada: solo cambia cuál se ve. Por eso es instantáneo y por eso, al volver a la configuración, siguen
escritos los nombres de la partida anterior.</p>
<p class="l"><b>L45–L46</b> Cierre y línea en blanco.</p>"""),
             ("public Partida getPartida()", r"""<p class="l"><b>L47–L50</b> Un <i>getter</i> (capítulo 19) que da la partida en
curso, o <code>null</code> si todavía no se jugó ninguna. Ninguna pantalla lo usa: existe para poder mirar desde fuera
qué está pasando, por ejemplo desde una prueba automática (capítulo 69) que simula clics y luego comprueba el marcador.
Las pruebas del flujo completo que se hicieron para este libro lo usan.</p>
<p class="l"><b>L51</b> En blanco.</p>"""),
             ("public void irAlMenu()", r"""<p class="l"><b>L52</b> <code>@Override</code>: este método cumple uno de la interfaz
<code>Navegacion</code>. Con interfaces, <code>@Override</code> también protege: si escribieras <code>irAlmenu</code> (con
<i>m</i> minúscula), el compilador diría que no sobrescribe nada.</p>
<p class="l"><b>L53–L55</b> Ir al menú es una sola línea: <code>cartas.show(this, MENU)</code>. El primer argumento es el
contenedor cuyas cartas se cambian (este panel), y el segundo, el nombre de la carta. Lo usan «Regresar», «Volver» y los
dos botones «Menú principal».</p>
<p class="l"><b>L56</b> En blanco.</p>"""),
             ("public void irAInstrucciones()", r"""<p class="l"><b>L57–L60</b> Mostrar las instrucciones (botón
«Instrucciones» del menú).</p>
<p class="l"><b>L62–L65</b> Mostrar la configuración (botón «Jugar» del menú). Fíjate en que «Jugar» no empieza a jugar:
lleva a la pantalla donde se eligen los jugadores.</p>
<p class="l"><b>L61, L66</b> Líneas en blanco entre métodos.</p>"""),
             ("public void iniciarPartida(", r"""<p class="l"><b>L67–L68</b> Lo llama la configuración al pulsar «Comenzar partida»
(capítulo 58), con los dos jugadores y el modo.</p>
<p class="l"><b>L69</b> Crea una <code>Partida</code> <b>nueva</b>: tablero vacío y marcador en cero. Si ya había una
partida, la referencia vieja se pierde y Java la borrará de la memoria cuando quiera.</p>
<p class="l"><b>L70</b> Se la entrega a la pantalla de juego, que la muestra y, si abre la IA, programa su jugada
(capítulo 59).</p>
<p class="l"><b>L71</b> Y la hace visible. El orden de las L70 y L71 importa: primero se prepara la pantalla y después se
muestra. Al revés, durante un instante podría verse el tablero de la partida anterior.</p>
<p class="l"><b>L72–L73</b> Cierre y línea en blanco.</p>"""),
             ("public void mostrarResultado(", r"""<p class="l"><b>L74–L75</b> Lo llama la pantalla de juego 1,2 segundos después
de que termina la partida. El parámetro se llama <code>partidaTerminada</code> y no <code>partida</code> para no
confundirse con el atributo (aunque en la práctica sean el mismo objeto) y para que el nombre diga qué se espera.</p>
<p class="l"><b>L76</b> La pantalla de resultado se rellena con esa partida (capítulo 60).</p>
<p class="l"><b>L77</b> Y se muestra.</p>
<p class="l"><b>L78–L79</b> Cierre y línea en blanco.</p>"""),
             ("public void jugarDeNuevo()", r"""<p class="l"><b>L80–L81</b> Lo llama «Jugar de nuevo» en la pantalla de resultado.</p>
<p class="l"><b>L82</b> <code>partida.reiniciar()</code> limpia el tablero de la <b>misma</b> partida: mismos jugadores,
mismo modo y el marcador <b>acumulado</b> (capítulo 38). Esa es la diferencia con <code>iniciarPartida</code>, que crea
una nueva con el marcador en cero.</p>
<p class="l"><b>L83–L84</b> Se la vuelve a dar a la pantalla de juego y se muestra el tablero.</p>
<p class="l"><b>L85–L86</b> Cierre y línea en blanco.</p>"""),
             ("public void salir()", r"""<p class="l"><b>L87–L89</b> Lo llaman el botón «Salir» del menú y la X del encabezado de
cualquier pantalla. <code>alSalir.run()</code> ejecuta la acción que llegó en el constructor. El panel no decide
<b>cómo</b> se sale: en el juego, <code>TotitoApp</code> cerrará la ventana y el programa; en una prueba se le puede pasar
<code>() -&gt; {}</code>, una acción vacía, para que «Salir» no cierre nada mientras se prueba.</p>
<p class="l"><b>L90–L91</b> Cierran el método y la clase.</p>"""),
         ]},
        {"ruta": "src/TotitoApp.java",
         "bloques": [
             (None, r"""<p class="l"><b>L1</b> <code>java.awt.Graphics2D</code>: el pincel, para dibujar el icono.</p>
<p class="l"><b>L2</b> <code>java.awt.Image</code>: <b>nueva</b>. La clase general de las imágenes en Java. Es lo que pide
<code>setIconImage</code>.</p>
<p class="l"><b>L3</b> <code>java.awt.image.BufferedImage</code>: <b>nueva</b>. Una imagen que vive en la memoria, con sus
píxeles accesibles, sobre la que se puede dibujar igual que sobre un componente. Es una clase hija de
<code>Image</code>.</p>
<p class="l"><b>L4</b> <code>java.awt.geom.RoundRectangle2D</code>: el rectángulo redondeado del fondo del icono.</p>
<p class="l"><b>L5</b> <code>javax.swing.JFrame</code>: la ventana de Swing (capítulo 33), con barra de título, botones de
minimizar y cerrar, y borde.</p>
<p class="l"><b>L6</b> <code>javax.swing.SwingUtilities</code>: utilidades de Swing; de aquí sale <code>invokeLater</code>.</p>
<p class="l"><b>L7</b> En blanco.</p>"""),
             ("public class TotitoApp", r"""<p class="l"><b>L8–L14</b> El comentario dice, en mayúsculas para que nadie lo
pase por alto, que este es el <b>punto de entrada</b>: el <code>main</code> que hay que ejecutar para jugar. Y recuerda que
la versión v0.1 (<code>JuegoMain</code>, capítulo 33) sigue en el proyecto y también se puede ejecutar (con clic derecho →
<i>Run File</i>). No se borró: es la historia del proyecto y demuestra que la lógica sirve para dos interfaces
distintas.</p>
<p class="l"><b>L15</b> <code>TotitoApp extends JFrame</code>: la clase <b>es</b> una ventana.</p>
<p class="l"><b>L16</b> En blanco.</p>"""),
             ("public TotitoApp()", r"""<p class="l"><b>L17</b> El constructor, sin parámetros.</p>
<p class="l"><b>L18</b> <code>super("Juego del Totito")</code> llama al constructor de <code>JFrame</code> que recibe el
<b>título</b> de la ventana: es el texto de la barra de arriba y el que se ve al pasar el ratón por el botón de la barra de
tareas.</p>
<p class="l"><b>L19</b> Qué hacer cuando el usuario pulsa la X de la <b>ventana</b> (la de Windows, arriba a la derecha):
<code>EXIT_ON_CLOSE</code>, terminar el programa. Si no lo pones, un <code>JFrame</code> usa
<code>HIDE_ON_CLOSE</code>: esconde la ventana pero el programa sigue vivo, invisible, gastando memoria. En NetBeans lo
notarías porque el botón rojo de «parar» seguiría encendido.</p>
<p class="l"><b>L20</b> <code>setResizable(false)</code>: el usuario no puede cambiar el tamaño ni maximizar. El diseño es
de tamaño fijo y las pantallas no están pensadas para estirarse; agrandar la ventana solo dejaría márgenes vacíos.</p>
<p class="l"><b>L21</b> Pone el icono de la ventana (el de la barra de título y la barra de tareas). El icono lo fabrica el
método <code>crearIcono()</code> de la L33.</p>"""),
             ("setContentPane(new PanelPrincipal", r"""<p class="l"><b>L22</b> Esta línea arma todo el juego. De dentro hacia
fuera: <code>this::cerrar</code> es una referencia al método <code>cerrar()</code> de esta ventana (capítulo 25) y cumple
<code>Runnable</code> porque <code>cerrar</code> no recibe nada ni devuelve nada. <code>new PanelPrincipal(...)</code> crea
el panel con las cinco pantallas y le dice «para salir, llama a mi <code>cerrar</code>». <code>setContentPane</code> pone
ese panel como contenido de la ventana: todo lo que hay dentro del borde y bajo la barra de título.</p>
<p class="l"><b>L23</b> <code>pack()</code> da a la ventana el tamaño justo para que su contenido tenga su tamaño preferido
(640 × 690), y le suma la barra de título y los bordes. Sin <code>pack()</code> (ni <code>setSize</code>), la ventana
aparecería diminuta, del tamaño de la barra de título.</p>
<p class="l"><b>L24</b> <code>setLocationRelativeTo(null)</code> centra la ventana en la pantalla (el comentario de la línea
lo dice). Con un componente en lugar de <code>null</code>, la centraría sobre ese componente. Va <b>después</b> de
<code>pack()</code> porque para centrar hay que conocer el tamaño.</p>
<p class="l">Fíjate en lo que <b>no</b> hace el constructor: no muestra la ventana (<code>setVisible(true)</code>). Eso lo hace
<code>main</code>. Construir y mostrar son pasos separados: primero se deja todo listo y después se enseña, ya completo.
<code>JuegoMain</code> lo hacía dentro del constructor; aquí se ordenó mejor.</p>
<p class="l"><b>L25–L26</b> Cierre y línea en blanco.</p>"""),
             ("private void cerrar()", r"""<p class="l"><b>L27</b> Método privado: solo lo usa esta clase (a través de la
referencia <code>this::cerrar</code>, que se le entregó al panel).</p>
<p class="l"><b>L28</b> <code>dispose()</code> cierra la ventana y libera los recursos que el sistema operativo le había dado
(memoria de la pantalla, el «identificador» de ventana de Windows).</p>
<p class="l"><b>L29</b> <code>System.exit(0)</code> termina el programa entero: la máquina virtual de Java se apaga. El
<code>0</code> es el «código de salida»: por convención, 0 significa «terminó bien» y cualquier otro número, un error. Lo
leen los programas que lanzan a otros (un script de PowerShell puede consultarlo en <code>$LASTEXITCODE</code>).</p>
<p class="l"><b>L30–L31</b> Cierre y línea en blanco.</p>
<p class="l">Hay tres maneras de cerrar el Totito y las tres acaban igual: el botón «Salir» del menú y la X del encabezado
llaman a <code>navegacion.salir()</code> → <code>alSalir.run()</code> → <code>cerrar()</code>; la X de la ventana de Windows
usa el <code>EXIT_ON_CLOSE</code> de la L19.</p>"""),
             ("private static Image crearIcono()", r"""<p class="l"><b>L32</b> Comentario: es el icono de la ventana y de la barra
de tareas, el logotipo sobre fondo oscuro.</p>
<p class="l"><b>L33</b> <code>private static</code>: no usa nada del objeto (se llama incluso antes de que la ventana esté
terminada). Devuelve una <code>Image</code>.</p>
<p class="l"><b>L34</b> Crea una imagen en memoria de 64 × 64 píxeles. El tercer argumento,
<code>BufferedImage.TYPE_INT_ARGB</code>, dice cómo se guarda cada píxel: un número entero (<code>INT</code>) con cuatro
partes, <b>A</b>lfa (transparencia), <b>R</b>ojo, <b>G</b> (verde) y <b>B</b> (azul) (capítulo 35). Con canal alfa, los
píxeles que no se pinten quedan <b>transparentes</b>: así las esquinas del rectángulo redondeado no salen negras.</p>
<p class="l"><b>L35</b> <code>imagen.getGraphics()</code> da un pincel para dibujar <b>sobre la imagen</b>. Se le pasa a
<code>Dibujo.preparar</code> (capítulo 41), que lo convierte en <code>Graphics2D</code> con el suavizado activado, igual
que en todos los <code>paintComponent</code> del juego. A partir de aquí, dibujar en una imagen es idéntico a dibujar en un
componente.</p>"""),
             ("g2.setColor(Tema.FONDO_ARRIBA)", r"""<p class="l"><b>L36–L37</b> Rellena un cuadrado de 64 × 64 con esquinas
redondeadas (arco de 16) del color de fondo del juego, el morado casi negro de <code>Tema</code>.</p>
<p class="l"><b>L38</b> Dibuja el logotipo del encabezado (el tablerito con X y O, capítulo 42) en lavanda, en un cuadrado
de 48 píxeles que empieza en (8, 8): quedan 8 píxeles de margen a cada lado (8 + 48 + 8 = 64).</p>
<p class="l"><b>L39</b> Libera el pincel.</p>
<p class="l"><b>L40</b> Devuelve la imagen. El método promete devolver una <code>Image</code> y entrega una
<code>BufferedImage</code>: vale, porque una <code>BufferedImage</code> <b>es</b> una <code>Image</code> (polimorfismo,
capítulo 23). Windows la reduce solo a 16 o 32 píxeles para la barra de título y la de tareas.</p>
<p class="l">¿Por qué dibujar el icono con código y no cargar un archivo <code>.png</code>? Porque así no hay ningún archivo
que se pueda perder o que haya que empaquetar: el icono viaja dentro del propio código. El icono del <b>archivo</b>
<code>.exe</code> (el que se ve en el Explorador y en el instalador) es otra cosa, un <code>.ico</code>, y se hace en el
capítulo 64.</p>
<p class="l"><b>L41–L42</b> Cierre y línea en blanco.</p>"""),
             ("public static void main", r"""<p class="l"><b>L43</b> El método <code>main</code> (capítulo 11): por aquí empieza el
programa. <code>public</code> para que Java lo encuentre, <code>static</code> porque todavía no existe ningún objeto,
<code>void</code> porque no devuelve nada y <code>String[] args</code> por los argumentos de la línea de comandos (aquí no se
usan).</p>
<p class="l"><b>L44–L45</b> Activa el texto suavizado según la configuración del sistema (la propiedad
<code>awt.useSystemAAFontSettings</code>). En Windows Java ya lo hace por su cuenta; en Linux sin esta línea las letras se
verían dentadas. Va <b>primero</b> porque Java la lee una sola vez, al preparar sus gráficos; si se pusiera después de crear
la ventana, ya no tendría efecto.</p>
<p class="l"><b>L46</b> <code>SwingUtilities.invokeLater(() -&gt; new TotitoApp().setVisible(true))</code>. La lambda dice qué
hacer: crear la ventana y mostrarla. <code>invokeLater</code> no lo hace en el acto: lo <b>pone en la fila del hilo de
Swing</b>, el EDT (capítulos 37 y 59), que lo ejecutará en cuanto pueda. ¿Por qué? Porque <code>main</code> corre en otro
hilo, el hilo <i>main</i>, y Swing exige que sus componentes se creen y se toquen solo desde el EDT. Crear la ventana
directamente en <code>main</code> suele funcionar… hasta el día que no, con errores de dibujo raros e imposibles de
repetir.</p>
<p class="l"><b>L47–L48</b> Cierran <code>main</code> y la clase. Curiosidad: <code>main</code> termina en cuanto deja la tarea
en la fila, una fracción de segundo después de empezar. El programa no se acaba porque el EDT sigue vivo mientras haya una
ventana abierta, esperando clics. Termina con <code>System.exit(0)</code>.</p>"""),
         ]},
    ],
    "despues": r"""<h2>Cómo funciona por dentro</h2>
<h3>Del F6 al menú</h3>
<ol>
<li>Java ejecuta <code>TotitoApp.main</code> en el hilo <i>main</i>: activa el suavizado y deja en la fila del EDT la tarea
«crear y mostrar la ventana». <code>main</code> termina.</li>
<li>El EDT toma la tarea: <code>new TotitoApp()</code> → <code>super("Juego del Totito")</code> → cierre, tamaño fijo,
icono (se dibuja la imagen de 64 × 64).</li>
<li><code>new PanelPrincipal(this::cerrar)</code>: <code>CardLayout</code>, 640 × 690, y se crean las cinco pantallas.
Cada una ejecuta su constructor (y el de <code>PantallaBase</code>, con su encabezado), crea sus botones, tarjetas y
rótulos. Se agregan al mazo con sus nombres y se elige <code>"menu"</code>.</li>
<li><code>pack()</code> calcula la ventana: 640 × 690 más la barra de título y los bordes. <code>setLocationRelativeTo(null)</code>
la centra.</li>
<li><code>setVisible(true)</code>: la ventana aparece y Swing llama a los <code>paintComponent</code> del menú. El EDT queda
esperando eventos.</li>
</ol>
<h3>Quién llama a quién</h3>
<p>Toda la navegación del juego cabe en esta tabla. La columna del medio es siempre un método de <code>Navegacion</code>,
implementado en <code>PanelPrincipal</code>:</p>
<table class="tabla">
<tr><th>El usuario pulsa…</th><th>La pantalla llama a…</th><th><code>PanelPrincipal</code> hace…</th><th>Se ve</th></tr>
<tr><td>«Jugar» (menú)</td><td><code>irAConfiguracion()</code></td><td><code>show(CONFIGURACION)</code></td><td>Configuración</td></tr>
<tr><td>«Instrucciones» (menú)</td><td><code>irAInstrucciones()</code></td><td><code>show(INSTRUCCIONES)</code></td><td>Cómo jugar</td></tr>
<tr><td>«Regresar», «Volver», «Menú principal»</td><td><code>irAlMenu()</code></td><td><code>show(MENU)</code></td><td>Menú</td></tr>
<tr><td>«Comenzar partida»</td><td><code>iniciarPartida(j1, j2, modo)</code></td><td>nueva <code>Partida</code>,
<code>comenzar</code>, <code>show(JUEGO)</code></td><td>Tablero vacío, marcador 0</td></tr>
<tr><td>(nadie: pasan 1,2 s tras el final)</td><td><code>mostrarResultado(partida)</code></td><td><code>mostrar</code>,
<code>show(RESULTADO)</code></td><td>Victoria o empate</td></tr>
<tr><td>«Jugar de nuevo»</td><td><code>jugarDeNuevo()</code></td><td><code>reiniciar</code>, <code>comenzar</code>,
<code>show(JUEGO)</code></td><td>Tablero vacío, marcador conservado</td></tr>
<tr><td>«Salir» o la X del encabezado</td><td><code>salir()</code></td><td><code>alSalir.run()</code> →
<code>cerrar()</code></td><td>Se cierra el juego</td></tr>
</table>
<p>Ninguna pantalla conoce a otra. El menú no sabe que existe una <code>PantallaConfiguracion</code>: solo dice «quiero ir
a la configuración». Si mañana agregas una pantalla de «Opciones», tocas <code>Navegacion</code>,
<code>PanelPrincipal</code> y el botón que lleve a ella; ninguna otra pantalla se entera.</p>
<h3>Una tarde de partidas</h3>
<p>Ana (X) y Luis (O) en modo de dos personas. Ana gana la primera: <code>mostrarResultado</code> enseña «¡Ganó Ana!». Pulsan
«Jugar de nuevo»: <code>partida.reiniciar()</code> limpia el tablero; el marcador dice Ana 1, Luis 0, Empates 0. La segunda
termina en empate: Ana 1, Luis 0, Empates 1. Vuelven al menú y empiezan otra vez desde «Jugar»: como
<code>iniciarPartida</code> crea una <code>Partida</code> nueva, todo vuelve a cero. Esa es la diferencia, en la práctica,
entre «Jugar de nuevo» y «Comenzar partida».</p>

<h2>Ejecuta el juego completo</h2>
<ol>
<li>Guarda los dos archivos y haz <i>Run → Clean and Build Project</i> (Shift+F11). Debe terminar en
<code>BUILD SUCCESS</code>.</li>
<li>Pulsa <b>F6</b> (<i>Run → Run Project</i>). NetBeans lee <code>exec.mainClass</code> en el <code>pom.xml</code>, que
desde el capítulo 5 dice <code>TotitoApp</code>, y ejecuta su <code>main</code>. Ya no hace falta <i>Run File</i> ni la
vista previa: este es el juego.</li>
<li>Si quieres hacerlo sin NetBeans, desde PowerShell:
<pre class="ps">cd $HOME\Proyectos\Totito
java -cp target\classes TotitoApp</pre>
o compilando a mano, sin Maven:
<pre class="ps">javac -encoding UTF-8 -d out src\*.java
java -cp out TotitoApp</pre></li>
</ol>
<p>Se abre una ventana de 640 × 690 centrada, titulada «Juego del Totito», con el icono del tablerito en la barra de tareas
y el menú de tres botones.</p>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Síntoma</th><th>Causa probable</th><th>Solución</th></tr>
<tr><td><code>PanelPrincipal is not abstract and does not override abstract method … in Navegacion</code></td><td>Falta uno de
los siete métodos o tiene otro nombre o parámetros.</td><td>Compáralos con <code>Navegacion.java</code> (capítulo 39).</td></tr>
<tr><td><code>Error: Could not find or load main class TotitoApp</code></td><td>No se compiló (hubo errores) o la clase se
llama distinto.</td><td>Mira la ventana <i>Output</i>, corrige y repite <i>Clean and Build</i>.</td></tr>
<tr><td>F6 abre la ventana vieja de la v0.1.</td><td>Cambiaste <code>exec.mainClass</code> a <code>JuegoMain</code>.</td>
<td>Déjalo en <code>TotitoApp</code> (capítulo 5).</td></tr>
<tr><td>La ventana aparece diminuta.</td><td>Falta <code>pack()</code> o <code>setPreferredSize</code> en el panel.</td>
<td>Revisa la L23 de <code>TotitoApp</code> y la L35 de <code>PanelPrincipal</code>.</td></tr>
<tr><td>Al cerrar con la X de Windows, NetBeans sigue mostrando el programa en ejecución.</td><td>Falta
<code>EXIT_ON_CLOSE</code>.</td><td>Agrega la L19.</td></tr>
<tr><td>Un botón no lleva a ninguna parte.</td><td>Escribiste el nombre de la carta como texto suelto (con una letra
distinta) en lugar de usar la constante.</td><td>Usa siempre <code>MENU</code>, <code>JUEGO</code>…</td></tr>
</table>

<h2>Lista de pruebas manuales</h2>
<p>Antes de publicar una versión se prueba <b>todo el recorrido</b>, no solo la parte que se acaba de escribir. Sigue esta
lista en orden, marcando cada fila. Si algo falla, anótalo, corrígelo, haz <i>Clean and Build</i> y vuelve a empezar la
lista (el capítulo 62 explica cómo usar el depurador cuando la causa no es evidente).</p>
<table class="tabla">
<tr><th>#</th><th>Qué hacer</th><th>Qué debe pasar</th></tr>
<tr><td>1</td><td>Abrir el juego con F6.</td><td>Ventana centrada, título «Juego del Totito», icono en la barra de tareas,
menú con «Jugar», «Instrucciones» y «Salir». No se puede cambiar de tamaño ni maximizar.</td></tr>
<tr><td>2</td><td>Pasar el ratón por los botones del menú.</td><td>Cada uno se ilumina y aparece la manita.</td></tr>
<tr><td>3</td><td>«Instrucciones», y luego «Regresar».</td><td>La tarjeta «Cómo jugar» con la X rosa y la O azul; el tablero
de ejemplo no reacciona al ratón. «Regresar» vuelve al menú.</td></tr>
<tr><td>4</td><td>«Jugar».</td><td>Configuración con «2 jugadores» marcado y la X elegida para el Jugador 1.</td></tr>
<tr><td>5</td><td>Escribir «Ana» y «Luis»; elegir la O y luego otra vez la X; pulsar «Contra la IA» y después «2 jugadores».</td>
<td>La leyenda de símbolos cambia; con «Contra la IA» la tarjeta 2 dice «Computadora» y no deja escribir; al volver,
reaparece «Luis». Siempre hay una sola opción de modo marcada.</td></tr>
<tr><td>6</td><td>«Comenzar partida» (2 jugadores, Ana con X).</td><td>Marcador «Ana — Victorias: 0», «Empates 0», «Luis —
Victorias: 0»; letrero rosa «Turno de Ana». Al pasar el ratón por una casilla vacía se ve una X transparente.</td></tr>
<tr><td>7</td><td>Jugar una X, luego hacer clic en esa misma casilla.</td><td>Aparece la X y el turno pasa a Luis (letrero
azul, fantasma O). El segundo clic, sobre una casilla ocupada, no hace nada.</td></tr>
<tr><td>8</td><td>Llevar la partida a una victoria de Ana.</td><td>Raya rosa sobre las tres X y «¡Tres en línea!» durante un
segundo y poco; luego la pantalla de victoria: trofeo, confeti, «¡Ganó Ana!», «Excelente jugada», tablero final con la
raya.</td></tr>
<tr><td>9</td><td>«Jugar de nuevo».</td><td>Tablero vacío; el marcador conserva «Ana — Victorias: 1». Empieza la X.</td></tr>
<tr><td>10</td><td>Jugar hasta llenar el tablero sin tres en línea.</td><td>«¡Empate!» en el letrero y, tras la pausa, la
pantalla de empate: X y O, «Nadie cedió ni una casilla», sin confeti. Al jugar de nuevo, «Empates 1».</td></tr>
<tr><td>11</td><td>A mitad de una partida, «Reiniciar».</td><td>Tablero vacío; el marcador no cambia.</td></tr>
<tr><td>12</td><td>Ganar y, durante el segundo de la raya, pulsar «Menú principal» (o «Reiniciar»).</td><td>Se queda en el menú
(o en el tablero vacío). <b>No</b> salta a la pantalla de resultado. Es la prueba de <code>cancelarPendiente</code>
(capítulo 59).</td></tr>
<tr><td>13</td><td>Menú → «Jugar»: los nombres siguen escritos. Elegir la O para Ana y «Contra la IA»; «Comenzar partida».</td>
<td>Marcador en cero (partida nueva). «La computadora está pensando…» en rosa y el tablero no acepta clics; a
medio segundo aparece la X de la computadora y el letrero pasa a «Turno de Ana».</td></tr>
<tr><td>14</td><td>Jugar contra la IA hasta el final, varias veces.</td><td>La IA nunca pierde: o gana («¡Ganó Computadora!»,
«La máquina no perdona») o empata. Hacer clic durante su pausa no pone fichas.</td></tr>
<tr><td>15</td><td>«Salir» en el menú. Abrir otra vez y cerrar con la X del encabezado. Abrir otra vez y cerrar con la X de la
ventana.</td><td>Las tres veces el programa termina (en NetBeans, el proceso deja de aparecer como en ejecución).</td></tr>
</table>
<figure><img src="capturas/3-configuracion.png"><figcaption>Prueba 5: configuración con «2 jugadores» elegido.</figcaption></figure>
<figure><img src="capturas/4-juego.png"><figcaption>Prueba 6–7: partida en curso, turno de Ana (X). La ficha del jugador
en turno brilla más en el marcador.</figcaption></figure>
<figure><img src="capturas/5-victoria.png"><figcaption>Prueba 8: pantalla de victoria, con trofeo, confeti y la raya
ganadora.</figcaption></figure>
<figure><img src="capturas/6-empate.png"><figcaption>Prueba 10: pantalla de empate, sin trofeo ni confeti.</figcaption></figure>

<div class="caja hito"><b>Hito: Totito v1.0</b> Tienes un juego completo y con diseño propio: menú, instrucciones,
configuración con nombres, símbolos y dos modos, partida con marcador, una IA que no pierde y pantallas de victoria y
empate con confeti. Más de 3000 líneas de Java escritas y entendidas una por una, sin una sola imagen ni biblioteca externa:
todo dibujado con código. Compara la ventana gris de la v0.1 (capítulo 33) con esta: la lógica (<code>Tablero</code>,
<code>Jugador</code>, <code>IA_Minimax</code>) es <b>la misma</b>. Todo lo demás es interfaz.</div>

<div class="caja git"><b>Git: commit, Pull Request y v1.0.0</b> Es el cierre de la rama <code>interfaz-neon</code>, con el
flujo del capítulo 10. Primero, el commit de este capítulo y la subida de la rama (comprueba antes con
<code>git status</code> que la vista previa está como la dejaste en el capítulo 56: si aparece modificada, usa
<code>git restore herramientas\VistaPrevia.java</code>):
<pre class="ps">git status
git add src\PanelPrincipal.java src\TotitoApp.java
git commit -m "PanelPrincipal y TotitoApp: el juego completo"
git push -u origin interfaz-neon</pre>
El <code>-u</code> ya lo pusiste en el capítulo 38; repetirlo no hace daño y asegura el enlace. Ahora escribe la descripción
del Pull Request en un archivo <b>fuera</b> del proyecto, para que no acabe en un commit por accidente:
<pre class="ps">notepad $HOME\pr-interfaz.md</pre>
<pre class="texto">## Que cambia
Toda la interfaz neon del Totito: menu, instrucciones, configuracion,
partida y pantalla de resultado, con sus componentes (BotonNeon,
Tarjeta, Rotulo, PanelTablero...). La logica (Tablero, Jugador,
IA_Minimax) no se toco; Partida la une con la interfaz.

## Por que
Pasar de la ventana basica de la v0.1.0 al diseno final (v1.0.0).

## Como probarlo
1. Clean and Build en NetBeans y Run (F6).
2. Seguir la lista de pruebas manuales del capitulo 61 (15 pruebas).

## Capturas
Ver las imagenes del capitulo 61.</pre>
Abre el PR, de <code>interfaz-neon</code> hacia <code>main</code>, y revísalo:
<pre class="ps">gh pr create --base main --head interfaz-neon --title "Interfaz neon completa (v1.0.0)" --body-file $HOME\pr-interfaz.md
gh pr view --web
gh pr diff</pre>
<code>gh pr create</code> imprime la dirección del PR (por ejemplo <code>…/totito/pull/1</code>). Para una descripción corta
puedes usar <code>--body "texto"</code> en lugar de <code>--body-file</code>. En la página, revisa la pestaña
<i>Commits</i> (un commit por capítulo, del 38 al 61) y <i>Files changed</i> (todos los archivos nuevos). Deja un comentario
con lo que probaste, por ejemplo <code>gh pr comment --body "Lista de pruebas del capitulo 61: 15 de 15 OK en Windows 11"</code>.
Cuando estés conforme, fusiona con commit de fusión (<code>--merge</code>), para conservar un commit por capítulo, y
borra la rama al terminar (<code>--delete-branch</code>); el capítulo 10 compara las tres formas de fusionar:
<pre class="ps">gh pr merge --merge --delete-branch
git switch main
git pull
git log --oneline --graph -5</pre>
Sin número, <code>gh pr merge</code> fusiona el PR de la rama en la que estás. Con <code>--delete-branch</code>, borra la rama
<code>interfaz-neon</code> en GitHub y en tu PC (su historia ya está en <code>main</code>) y te deja en <code>main</code>; el
<code>git switch main</code> y el <code>git pull</code> son una comprobación que no hace daño: aseguran que tu
<code>main</code> tiene el commit de fusión creado en GitHub. El <code>log</code> lo muestra arriba («Merge pull request #1 from
…/interfaz-neon») uniendo las dos líneas. Por último, la etiqueta de la versión, anotada como en el capítulo 9, y súbela:
<pre class="ps">git tag -a v1.0.0 -m "Totito 1.0.0: interfaz neon"
git push --tags
git tag</pre>
<code>git tag</code> debe listar <code>v0.1.0</code> y <code>v1.0.0</code>. En GitHub, el PR aparece como <b>Merged</b> y la
etiqueta, en la sección <i>Tags</i>. Si en <code>git branch -a</code> aún ves
<code>remotes/origin/interfaz-neon</code>, <code>git fetch --prune</code> limpia esa referencia (capítulo 10). Los mensajes
de commit y de la etiqueta van sin tildes, como todos los del plan (capítulo 8). La publicación con el instalador (<i>Release</i>) llega en el capítulo 67.</div>

<h2>Resumen</h2>
<ul>
<li><code>PanelPrincipal</code> es un <code>JPanel</code> con <code>CardLayout</code>: las cinco pantallas se crean al
arrancar y <code>cartas.show(this, NOMBRE)</code> elige cuál se ve.</li>
<li>Implementa <code>Navegacion</code> y se pasa a sí mismo (<code>this</code>) a cada pantalla: ninguna pantalla conoce a
otra.</li>
<li>Guarda la <code>Partida</code>: <code>iniciarPartida</code> crea una nueva (marcador a cero) y <code>jugarDeNuevo</code>
reinicia la misma (marcador conservado).</li>
<li>Los nombres de las cartas son constantes: un error de escritura no compila en lugar de fallar en silencio.</li>
<li><code>TotitoApp</code> es la ventana: título, <code>EXIT_ON_CLOSE</code>, tamaño fijo, icono dibujado en una
<code>BufferedImage</code>, <code>pack()</code> y centrado.</li>
<li>El panel no sabe salir: recibe un <code>Runnable</code> (<code>this::cerrar</code>) que decide la ventana.</li>
<li><code>main</code> crea la ventana con <code>SwingUtilities.invokeLater</code>, en el hilo de Swing.</li>
<li>Antes de publicar se prueba todo el recorrido; luego PR, merge con commit de fusión y etiqueta <code>v1.0.0</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Asistentes de varios pasos:</b> instalar un programa, registrar un cliente, hacer un pedido. Cada paso es una
pantalla, un <code>CardLayout</code> las guarda y un objeto central (como <code>PanelPrincipal</code>) decide cuál sigue.
Las pantallas solo dicen «siguiente» o «atrás».</li>
<li><b>Aplicaciones con menú lateral:</b> un sistema de inventario con «Productos», «Ventas» y «Reportes» es exactamente un
mazo de cartas con un nombre por sección.</li>
<li><b>Separar el «qué» del «cómo» con un <code>Runnable</code>:</b> un panel de «Cerrar sesión» que recibe qué hacer al
cerrar; en la aplicación real vuelve a la pantalla de acceso, en las pruebas no hace nada.</li>
<li><b>El esqueleto de cualquier programa Swing:</b> una clase ventana (<code>JFrame</code>) mínima con su
<code>main</code> e <code>invokeLater</code>, y todo lo demás en paneles que se pueden probar sin ventana. Y antes de cada
versión: lista de pruebas manuales, PR, merge y etiqueta.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Cambia el título de la ventana a «Totito neón — v1.0». ¿Dónde se ve el cambio?</li>
<li>Quita <code>setResizable(false)</code>, ejecuta y maximiza la ventana. Describe qué pasa con las pantallas y explica por
qué el diseño de tamaño fijo era la mejor opción. Vuelve a ponerlo.</li>
<li>Cambia el fondo del icono de la ventana a <code>Tema.MORADO</code> y el logotipo a blanco. Mira la barra de tareas.</li>
<li>Haz que el juego arranque directamente en la configuración, sin pasar por el menú. ¿Cuál es la única línea que
cambias? Después déjalo como estaba.</li>
<li>Reto: agrega una sexta pantalla, «Acerca de», con tu nombre y la versión, accesible desde un cuarto botón del menú.
Necesitarás: un método nuevo en <code>Navegacion</code> (por ejemplo <code>irAcercaDe()</code>), una constante y un
<code>add</code> en <code>PanelPrincipal</code>, la clase de la pantalla (hereda de <code>PantallaBase</code>) y el botón.
Cuando el compilador se queje de la vista previa (su navegación de mentira también implementa <code>Navegacion</code>),
agrégale el método vacío. Hazlo en una rama nueva y ábrele su propio PR.</li>
</ol></div>
""",
}
