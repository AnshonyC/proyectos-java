# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 49,
    "titulo": "TarjetaJugador.java: la tarjeta del nombre",
    "antes": r"""
<p class="entrada">En la pantalla de configuración cada jugador tiene su propia tarjeta: un icono, su título
(«Jugador 1» o «Jugador 2») con una rayita de color que se desvanece y una caja para escribir el nombre. En este
capítulo construyes esa tarjeta reutilizando la <code>Tarjeta</code> de cristal del capítulo 43, y le enseñas un
truco: convertirse en la tarjeta de la «Computadora» cuando se elige jugar contra la IA, sin perder lo que el
usuario había escrito.</p>

<h2>Por qué existe este archivo</h2>
<p>Mira la imagen de diseño <code>diseno/configuracion.jpg</code> (la analizaste en el capítulo 34) o la captura
del resultado final que tienes abajo. Arriba, bajo el rótulo «JUGADORES», hay <b>dos tarjetas casi iguales</b>:
la de la izquierda en rosa fresa y la de la derecha en azul. Las dos tienen exactamente las mismas partes:</p>
<ul>
<li>una caja de cristal con borde de neón (eso ya lo sabe hacer <code>Tarjeta</code>, capítulo 43);</li>
<li>un icono de persona;</li>
<li>un título en negrita y, debajo, una raya del color de la tarjeta que se va volviendo transparente;</li>
<li>la palabrita «Nombre»;</li>
<li>una caja de texto redondeada para escribir el nombre (eso ya lo sabe hacer <code>CampoTexto</code>, capítulo 47).</li>
</ul>
<p>Cuando algo aparece <b>dos veces igual</b> y solo cambian unos datos (el título y el color), es la señal de que
hace falta una <b>clase</b>: un molde del que salen las dos tarjetas (capítulo 18). Si dibujaras cada tarjeta a
mano dentro de la pantalla, tendrías el mismo código copiado dos veces y cualquier arreglo habría que hacerlo en
los dos sitios.</p>
<p>Además, la tarjeta tiene una responsabilidad propia: cuando en «MODO DE JUEGO» se elige «Contra la IA», la
tarjeta del Jugador 2 debe cambiar su icono por un chip, poner «Computadora» en la caja y bloquearla para que nadie
escriba. Y si luego se vuelve a «2 jugadores», debe devolver el nombre que el usuario había escrito. Ese
comportamiento vive aquí, dentro de la tarjeta, y la pantalla solo tiene que decirle «ahora eres la computadora» o
«ahora eres humano».</p>
<figure><img src="capturas/3-configuracion.png"><figcaption>Las dos TarjetaJugador están arriba, bajo «JUGADORES».
La pantalla completa la armarás en el capítulo 58.</figcaption></figure>

<h2>Qué vas a aprender</h2>
<ul>
<li>A <b>heredar de una clase tuya</b> (<code>TarjetaJugador extends Tarjeta</code>), que a su vez hereda de
<code>JPanel</code>: una cadena de herencia de tres pisos.</li>
<li>A elegir cuál constructor de la clase padre se usa con <code>super(color, 26)</code>.</li>
<li>A colocar un componente hijo <b>a mano</b>, sin gestor de distribución, sobrescribiendo
<code>doLayout()</code>.</li>
<li>A <b>recordar un dato</b> para devolverlo después (el nombre guardado) y a protegerte de llamadas repetidas
con una <b>cláusula de guarda</b>.</li>
<li>Los métodos de texto <code>getText()</code>, <code>trim()</code>, <code>isEmpty()</code> y el operador
ternario <code>? :</code> en un caso real.</li>
<li>A dibujar <b>encima</b> de lo que pinta la clase padre llamando primero a
<code>super.paintComponent(g)</code>, y a pintar una línea con un degradado que termina en transparente.</li>
</ul>

<h2>El plano de la tarjeta, en píxeles</h2>
<p>Antes de leer el código conviene tener el plano. La tarjeta mide <b>290 × 150 píxeles</b>. Como toda
<code>Tarjeta</code>, deja un margen de 10 píxeles (<code>MARGEN</code>) alrededor para que quepa el halo de neón,
así que la caja visible empieza en (10, 10). Estas son las posiciones que calcula el código (las comprobarás línea
por línea):</p>
<table class="tabla">
<tr><th>Parte</th><th>Dónde queda</th><th>Quién la dibuja</th></tr>
<tr><td>Caja de cristal y borde de neón</td><td>de (10, 10) a (280, 140), esquinas de radio 26</td><td><code>Tarjeta</code> (la clase padre)</td></tr>
<tr><td>Icono (persona o chip)</td><td>cuadrado de 42 × 42 con esquina en (32, 20)</td><td><code>paintComponent</code> de esta clase</td></tr>
<tr><td>Título «Jugador 1»</td><td>empieza en x = 98, línea base en y = 46</td><td><code>paintComponent</code></td></tr>
<tr><td>Raya de color</td><td>de (98, 58) a (238, 58), 3 píxeles de grosor</td><td><code>paintComponent</code></td></tr>
<tr><td>Palabra «Nombre»</td><td>empieza en x = 28, línea base en y = 80</td><td><code>paintComponent</code></td></tr>
<tr><td>Caja de texto</td><td>rectángulo (22, 84) de 246 × 46</td><td>se coloca en <code>doLayout</code>; se pinta sola (<code>CampoTexto</code>)</td></tr>
</table>

<h2>Créalo</h2>
<ol>
<li>Comprueba que estás en la rama de trabajo: en PowerShell, desde la carpeta del proyecto
(<code>cd $HOME\Proyectos\Totito</code>), <code>git branch --show-current</code> debe responder
<code>interfaz-neon</code> (la creaste en el capítulo 38).</li>
<li>En NetBeans, en la ventana <i>Projects</i>, abre <i>Source Packages</i>, haz clic derecho en
<i>&lt;default package&gt;</i> → <i>New</i> → <i>Java Class…</i></li>
<li>En <i>Class Name</i> escribe <code>TarjetaJugador</code> (con T y J mayúsculas: el nombre del archivo y el de
la clase deben ser idénticos) y pulsa <i>Finish</i>.</li>
<li>NetBeans abre un archivo con una plantilla (un comentario de licencia y una clase vacía). <b>Bórralo todo</b>
(Ctrl+A y Supr) y escribe el código de abajo. Escribirlo tú, en vez de pegarlo, te obliga a mirar cada línea.</li>
</ol>
<p>Alternativa sin NetBeans: desde la carpeta del proyecto, <code>New-Item src\TarjetaJugador.java</code> crea el
archivo vacío; ábrelo con cualquier editor (por ejemplo <code>code src\TarjetaJugador.java</code> si instalaste
Visual Studio Code) y guárdalo en UTF-8.</p>
<p>Para escribir esta clase necesitas que ya existan <code>Tema</code> (capítulo 40), <code>Dibujo</code> (41),
<code>Iconos</code> (42), <code>Tarjeta</code> (43) y <code>CampoTexto</code> (47).</p>
""",
    "archivos": [
        {"ruta": "src/TarjetaJugador.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>import java.awt.Color;</code> trae la clase <code>Color</code> del paquete
<code>java.awt</code> (las herramientas gráficas básicas de Java). La usamos para guardar el color de la tarjeta
(fresa o azul) y para recibirlo en el constructor. Sin este <code>import</code>, al escribir <code>Color</code> el
compilador diría <i>cannot find symbol</i>: no sabría a qué <code>Color</code> te refieres.</p>
<p class="l"><b>L2</b> <code>java.awt.Font</code>: la clase de las fuentes. Aquí solo la nombramos para usar sus
constantes <code>Font.BOLD</code> (negrita) y <code>Font.PLAIN</code> (normal) al pedirle una fuente a
<code>Tema.fuente</code> (capítulo 40).</p>
<p class="l"><b>L3</b> <code>java.awt.GradientPaint</code>: una «pintura» que pasa suavemente de un color a otro
entre dos puntos (capítulo 37). Con ella pintamos la raya que se desvanece bajo el título.</p>
<p class="l"><b>L4</b> <code>java.awt.Graphics</code>: el «pincel» que Swing nos presta en
<code>paintComponent(Graphics g)</code>. Lo necesitamos porque aparece en la firma de ese método.</p>
<p class="l"><b>L5</b> <code>java.awt.Graphics2D</code>: la versión ampliada del pincel, con degradados, grosores
de trazo y figuras geométricas. <code>Dibujo.preparar</code> nos devuelve uno (capítulo 41).</p>
<p class="l"><b>L6</b> <code>java.awt.geom.Line2D</code>: la figura «segmento de recta» del subpaquete
<code>geom</code> (geometría). La usamos para la raya bajo el título.</p>
<p class="l"><b>L7</b> Línea en blanco: separa los imports del resto, solo por orden visual.</p>
<p>Fíjate en lo que <b>no</b> se importa: <code>Tarjeta</code>, <code>CampoTexto</code>, <code>Dibujo</code>,
<code>Iconos</code> y <code>Tema</code> son clases tuyas que viven en el mismo paquete sin nombre (el
<i>default package</i>), y las clases de un mismo paquete se ven entre sí sin <code>import</code> (capítulo 11).
Tampoco hace falta importar <code>JPanel</code>: no lo nombramos en ningún momento, lo heredamos a través de
<code>Tarjeta</code>.</p>
"""),
             ("public class TarjetaJugador", r"""
<p class="l"><b>L8–L12</b> Comentario de documentación (empieza con <code>/**</code>). No lo ejecuta nadie: es
para quien lea el código. Resume para qué sirve la clase y avisa del caso especial del modo «Contra la IA», con una
pista de dónde está resuelto (<code>setComputadora</code>). Va sin tildes porque así están escritos todos los
comentarios del proyecto.</p>
<p class="l"><b>L13</b> <code>public class TarjetaJugador extends Tarjeta {</code> declara la clase.
<code>public</code>: cualquier otra clase puede usarla (la pantalla de configuración lo hará).
<code>extends Tarjeta</code>: <b>hereda</b> de tu <code>Tarjeta</code> del capítulo 43 (herencia, capítulo 22).
Eso significa que una <code>TarjetaJugador</code> <i>es una</i> <code>Tarjeta</code>: ya nace sabiendo pintar la
caja de cristal con borde de neón, ya es transparente, ya está centrada y ya tiene la constante
<code>MARGEN</code>. Y como <code>Tarjeta</code> hereda de <code>JPanel</code>, también es un panel de Swing al
que se le pueden meter componentes. Es una cadena: <code>JPanel</code> → <code>Tarjeta</code> →
<code>TarjetaJugador</code>. La llave <code>{</code> abre el cuerpo de la clase, que se cierra en la línea 85.</p>
<p class="l"><b>L14</b> Línea en blanco para respirar.</p>
"""),
             ("public static final int ANCHO", r"""
<p class="l"><b>L15</b> <code>public static final int ANCHO = 290;</code> el ancho de la tarjeta.
<code>static</code>: pertenece a la clase, no a cada tarjeta (hay un solo 290 para todas). <code>final</code>: no
puede cambiar nunca; es una <b>constante</b> (capítulo 20). <code>public</code>: otras clases pueden leerla, por
ejemplo para calcular cuánto ocupan dos tarjetas juntas. ¿Por qué 290? Dos tarjetas más 8 píxeles de separación
suman 588, que cabe con holgura en la ventana de 640 de ancho (capítulo 36).</p>
<p class="l"><b>L16</b> <code>ALTO = 150</code>: el alto. Da sitio para dos «pisos»: arriba icono y título, abajo
la caja de texto de 46 píxeles.</p>
<p class="l"><b>L17</b> <code>public static final String NOMBRE_IA = "Computadora";</code> el texto que se pone en
la caja cuando el Jugador 2 es la IA. Tenerlo en una constante con nombre evita escribir la palabra «suelta» (un
<i>número mágico</i>, o aquí un texto mágico, capítulo 27): si mañana quieres que diga «CPU», cambias una sola
línea.</p>
<p class="l"><b>L18</b> En blanco.</p>
"""),
             ("private final String titulo;", r"""
<p class="l"><b>L19</b> <code>private final String titulo;</code> un <b>campo</b> (una variable que pertenece a cada
objeto): el título de esta tarjeta, «Jugador 1» o «Jugador 2». <code>private</code>: solo esta clase lo toca
(encapsulamiento, capítulo 19). <code>final</code>: se asigna una vez, en el constructor, y ya no cambia.</p>
<p class="l"><b>L20</b> <code>private final Color color;</code> el color de esta tarjeta. ¿No lo tenía ya
<code>Tarjeta</code>? Sí, pero allí es <code>private</code>, y lo privado del padre <b>no es visible</b> en el hijo.
Por eso la hija guarda su propia copia: la necesita para pintar el icono y la raya del título.</p>
<p class="l"><b>L21</b> <code>private final CampoTexto campo;</code> la caja de texto (capítulo 47). Es
<code>final</code> porque la tarjeta tiene siempre la misma caja; lo que cambia es su contenido.</p>
<p class="l"><b>L22</b> <code>private boolean esComputadora;</code> recuerda si la tarjeta está ahora en «modo
computadora». No lleva <code>final</code> porque cambia. Tampoco lleva valor inicial: los campos de tipo
<code>boolean</code> empiezan solos en <code>false</code> (los numéricos en 0 y los objetos en <code>null</code>).
Ojo: eso vale para campos, no para variables locales dentro de un método, que hay que inicializar siempre.</p>
<p class="l"><b>L23</b> Comentario de documentación de una sola línea sobre el campo siguiente.</p>
<p class="l"><b>L24</b> <code>private String nombreGuardado = "";</code> la «memoria» de la tarjeta: aquí se guarda
lo que el usuario había escrito antes de pasar al modo IA, para devolvérselo al volver. Empieza como texto vacío
<code>""</code> y no como <code>null</code>: un texto vacío siempre se puede usar sin miedo; un <code>null</code>
puede provocar un <code>NullPointerException</code> si alguien llama a uno de sus métodos (capítulo 18). Es una
precaución barata.</p>
"""),
             ("public TarjetaJugador(String titulo", r"""
<p class="l"><b>L26</b> <code>public TarjetaJugador(String titulo, Color color) {</code> el <b>constructor</b>: se
ejecuta al hacer <code>new TarjetaJugador("Jugador 1", Tema.FRESA)</code>. Tiene el mismo nombre que la clase y no
devuelve nada (ni siquiera <code>void</code>). Recibe dos <b>parámetros</b>: el título y el color.</p>
<p class="l"><b>L27</b> <code>super(color, 26);</code> llama al constructor de la clase padre. <code>Tarjeta</code>
tiene dos constructores: <code>Tarjeta(Color)</code>, que usa esquinas de radio 30, y
<code>Tarjeta(Color, int)</code>, que deja elegir el radio. Al pasar dos argumentos Java elige el segundo
(sobrecarga, capítulo 16). Elegimos 26 porque esta tarjeta es más pequeña que la del menú y unas esquinas tan
redondas como las grandes se verían desproporcionadas. Esta llamada <b>tiene que ser la primera línea</b> del
constructor: el padre se construye antes que el hijo, igual que los cimientos van antes que las paredes. Ahí dentro
se guardan el color y el radio, y se hace <code>setOpaque(false)</code> y el centrado horizontal.</p>
<p class="l"><b>L28</b> <code>this.titulo = titulo;</code> copia el parámetro al campo. El parámetro y el campo
se llaman igual; <code>this.titulo</code> es el campo del objeto y <code>titulo</code> a secas es el parámetro
(capítulo 20). Sin esta línea el campo <code>final</code> quedaría sin asignar y el compilador protestaría:
<i>variable titulo might not have been initialized</i>.</p>
<p class="l"><b>L29</b> Lo mismo con el color.</p>
<p class="l"><b>L30</b> <code>setLayout(null);</code> quita el gestor de distribución. Un <code>JPanel</code> nace
con un <code>FlowLayout</code>, que pone los hijos en fila centrados arriba, cada uno de su tamaño preferido
(capítulo 37). Nosotros queremos la caja de texto en un sitio exacto (pegada abajo y casi a todo lo ancho), así que
la colocaremos a mano en <code>doLayout()</code>. El comentario al final de la línea lo dice. En rigor, como más
abajo sobrescribimos <code>doLayout()</code>, el <code>FlowLayout</code> ya no tendría ocasión de actuar; esta
línea deja escrito para quien lea que aquí no manda ningún gestor, y evita sorpresas si algún día se quita el
<code>doLayout()</code>.</p>
<p class="l"><b>L31</b> <code>campo = new CampoTexto(titulo, color);</code> crea la caja de texto. El primer
argumento de <code>CampoTexto</code> es el <b>texto de ayuda</b> (el gris que se ve cuando está vacía, capítulo
47): usamos el propio título, así la caja vacía dice «Jugador 1». El segundo es el color de su borde.</p>
<p class="l"><b>L32</b> <code>add(campo);</code> mete la caja dentro de la tarjeta. Sin esta línea la caja
existiría en memoria pero nunca aparecería: un componente solo se ve si está dentro de un contenedor visible.</p>
<p class="l"><b>L33</b> <code>Dibujo.fijarTamano(this, ANCHO, ALTO);</code> fija los tamaños preferido, mínimo y
máximo en 290 × 150 (capítulo 41). <code>this</code> es «esta misma tarjeta». Así el <code>BoxLayout</code> de la
pantalla no la estira ni la encoge.</p>
"""),
             ("public void doLayout()", r"""
<p class="l"><b>L36</b> <code>@Override</code> avisa al compilador de que el método siguiente <b>reemplaza</b> uno
heredado (capítulo 23). Si te equivocaras en el nombre (por ejemplo <code>dolayout</code>), el compilador daría
error en vez de crear en silencio un método nuevo que nadie llamaría.</p>
<p class="l"><b>L37</b> <code>public void doLayout() {</code> es el método que Swing llama cuando un contenedor
tiene que acomodar a sus hijos: al mostrarse por primera vez, al cambiar de tamaño o tras un
<code>revalidate()</code>. La versión heredada le pide el trabajo al gestor de distribución; la nuestra lo hace a
mano. Tiene que ser <code>public</code> porque el original lo es, y al sobrescribir no se puede reducir la
visibilidad.</p>
<p class="l"><b>L38</b> <code>campo.setBounds(x, y, ancho, alto)</code> coloca la caja en un rectángulo exacto,
medido desde la esquina superior izquierda de la tarjeta. Con la tarjeta de 290 × 150:</p>
<ul>
<li><b>x</b> = <code>MARGEN + 12</code> = 10 + 12 = <b>22</b>: el margen del halo y 12 píxeles de aire.</li>
<li><b>y</b> = <code>getHeight() - MARGEN - 10 - 46</code> = 150 − 10 − 10 − 46 = <b>84</b>: desde abajo se quitan
el margen del halo, 10 de aire y los 46 que mide la caja. Así la caja queda pegada al fondo.</li>
<li><b>ancho</b> = <code>getWidth() - 2 * MARGEN - 24</code> = 290 − 20 − 24 = <b>246</b>: lo que queda tras quitar
los dos márgenes y 12 de aire a cada lado.</li>
<li><b>alto</b> = <b>46</b>.</li>
</ul>
<p>¿Por qué calcular con <code>getWidth()</code> y <code>getHeight()</code> en vez de escribir 22, 84, 246?
Porque si un día cambias <code>ALTO</code> a 170, la caja seguirá pegada abajo sin tocar esta línea. Las medidas
salen del tamaño real, no de números copiados.</p>
"""),
             ("public String getNombre()", r"""
<p class="l"><b>L41</b> Comentario: explica qué devuelve el método, incluido el caso especial.</p>
<p class="l"><b>L42</b> <code>public String getNombre() {</code> un <i>getter</i> (capítulo 19): devuelve un
<code>String</code>. La pantalla de configuración lo llamará al pulsar «Comenzar partida» para crear el
<code>Jugador</code>.</p>
<p class="l"><b>L43</b> <code>String nombre = campo.getText().trim();</code> son dos llamadas encadenadas.
<code>campo.getText()</code> devuelve lo escrito en la caja; sobre ese texto se llama a <code>.trim()</code>, que
devuelve una copia sin los espacios del principio y del final. Si el usuario escribió <code>"  Ana  "</code>,
<code>nombre</code> vale <code>"Ana"</code>. Sin el <code>trim</code>, el marcador mostraría espacios raros y un
nombre hecho solo de espacios pasaría por válido.</p>
<p class="l"><b>L44</b> <code>return nombre.isEmpty() ? titulo : nombre;</code> el operador ternario (capítulo
13): <i>condición</i> <code>?</code> <i>valor si sí</i> <code>:</code> <i>valor si no</i>. <code>isEmpty()</code> es
<code>true</code> si el texto tiene 0 letras. Si el usuario no escribió nada (o solo espacios), se devuelve el
título («Jugador 1»); si escribió algo, eso. Gracias a esta línea <b>nunca</b> hay un jugador sin nombre: la pantalla
de victoria nunca dirá «¡Ganó !».</p>
"""),
             ("public void setComputadora", r"""
<p class="l"><b>L47</b> Comentario: qué significan <code>true</code> y <code>false</code> en este método.</p>
<p class="l"><b>L48</b> <code>public void setComputadora(boolean computadora) {</code> cambia la tarjeta entre
«humano» y «computadora». <code>void</code>: no devuelve nada, solo hace cosas.</p>
<p class="l"><b>L49–L51</b> Una <b>cláusula de guarda</b>: si el modo pedido es el que ya tiene
(<code>computadora == esComputadora</code>), <code>return;</code> sale del método enseguida sin hacer nada.
¿Por qué importa? La pantalla de configuración llama a este método <b>cada vez</b> que se toca una opción de modo,
aunque sea la que ya estaba marcada. Sin la guarda, pedir «computadora» dos veces seguidas guardaría
«Computadora» como si fuera el nombre del usuario (la segunda vez la caja ya dice «Computadora»), y al volver a
«2 jugadores» el nombre real se habría perdido. Lo verás paso a paso en «Cómo funciona por dentro».</p>
"""),
             ("esComputadora = computadora;", r"""
<p class="l"><b>L52</b> <code>esComputadora = computadora;</code> anota el nuevo modo en el campo. Aquí no hace
falta <code>this.</code> porque el campo y el parámetro tienen nombres distintos.</p>
<p class="l"><b>L53</b> <code>if (computadora) {</code> si pasamos a modo IA…</p>
<p class="l"><b>L54</b> <code>nombreGuardado = campo.getText();</code> …primero guardamos lo que hubiera escrito
(aunque sea vacío). El orden importa: si se cambiara el texto antes de guardarlo, se guardaría «Computadora».</p>
<p class="l"><b>L55</b> <code>campo.setText(NOMBRE_IA);</code> pone «Computadora» en la caja. Así, cuando la
pantalla llame a <code>getNombre()</code>, el Jugador 2 se llamará «Computadora» sin código extra.</p>
<p class="l"><b>L56–L57</b> <code>} else {</code> si volvemos a modo humano, <code>campo.setText(nombreGuardado)</code>
devuelve lo que el usuario había escrito.</p>
<p class="l"><b>L59</b> <code>campo.setEnabled(!computadora);</code> habilita o bloquea la caja. El
<code>!</code> es el «no» lógico: si <code>computadora</code> es <code>true</code>, se pasa <code>false</code>
(bloqueada) y al revés. Una caja deshabilitada no deja escribir ni recibir el foco, y <code>CampoTexto</code> la
dibuja más apagada (texto lavanda y relleno más tenue, capítulo 47). Sin esta línea podrías borrar «Computadora» y
llamar «Pepe» a la IA.</p>
<p class="l"><b>L60</b> <code>repaint();</code> pide a Swing que vuelva a dibujar la tarjeta. El icono (persona o
chip) lo pintamos nosotros según <code>esComputadora</code>, y Swing no tiene manera de saber que ese campo
cambió. Sin <code>repaint()</code>, el icono seguiría siendo la persona hasta que algo más provocara un redibujado
(pasar el ratón, mover la ventana). <code>repaint()</code> no dibuja en el acto: deja anotado el encargo y Swing lo
hace en cuanto puede, en el hilo de eventos (capítulo 37).</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L63</b> <code>@Override</code>: vamos a reemplazar <code>paintComponent</code>, que ya reemplazó
<code>Tarjeta</code>.</p>
<p class="l"><b>L64</b> <code>protected void paintComponent(Graphics g) {</code> el método donde un componente se
dibuja (capítulo 37). <code>protected</code>: lo pueden ver la propia clase, sus hijas y las clases del mismo
paquete; es la visibilidad que tiene el original en <code>JComponent</code>. Swing lo llama solo; tú nunca lo
llamas directamente (para eso está <code>repaint()</code>).</p>
<p class="l"><b>L65</b> <code>super.paintComponent(g);</code> ejecuta primero la versión del padre, la de
<code>Tarjeta</code>: el relleno de cristal y el borde de neón. Todo lo que dibujemos después queda <b>encima</b>,
como capas de pintura. Si quitaras esta línea, verías el icono y los textos flotando sobre el fondo de la pantalla,
sin caja. Fíjate en que la llamada usa el mismo <code>g</code>: <code>Tarjeta</code> trabaja con una copia que ella
misma descarta al terminar, así que <code>g</code> nos llega intacto.</p>
<p class="l"><b>L66</b> <code>Graphics2D g2 = Dibujo.preparar(g);</code> pide una copia del pincel con el
suavizado activado (capítulo 41). Trabajar con una copia hace que nuestros cambios de fuente, color o trazo no
«contaminen» el pincel que Swing usará luego para pintar la caja de texto.</p>
"""),
             ("Iconos.Icono icono", r"""
<p class="l"><b>L68</b> <code>Iconos.Icono icono = esComputadora ? Iconos.COMPUTADORA : Iconos.PERSONA;</code>
elige qué icono dibujar. <code>Iconos.Icono</code> es la interfaz que definiste dentro de <code>Iconos</code>
(capítulo 42); una variable de ese tipo puede guardar cualquiera de los iconos (cada uno es una lambda que sabe
dibujarse). Con el ternario: si la tarjeta es la de la computadora, el chip; si no, la persona.</p>
<p class="l"><b>L69</b> <code>icono.dibujar(g2, MARGEN + 22, MARGEN + 10, 42, color);</code> dibuja el icono
elegido dentro de un cuadrado de 42 píxeles cuya esquina superior izquierda está en (10 + 22, 10 + 10) =
<b>(32, 20)</b>, con el color de la tarjeta. No nos importa cómo se dibuja cada icono: solo que sabe hacerlo
(eso es polimorfismo, capítulo 23).</p>
"""),
             ("g2.setFont(Tema.fuente(Font.BOLD", r"""
<p class="l"><b>L71</b> <code>g2.setFont(Tema.fuente(Font.BOLD, 21f));</code> elige la fuente del título: la
familia del tema, en negrita, de 21 puntos. La <code>f</code> de <code>21f</code> dice que es un
<code>float</code> (número con decimales de precisión simple), que es lo que pide <code>Tema.fuente</code>.</p>
<p class="l"><b>L72</b> <code>g2.setColor(Tema.TEXTO);</code> color del texto: blanco (<code>Tema.TEXTO</code>).</p>
<p class="l"><b>L73</b> <code>float xTitulo = MARGEN + 88;</code> el título empieza en x = 98, a la derecha del
icono (que termina en 32 + 42 = 74) con 24 píxeles de aire. Es <code>float</code> porque se usará con
<code>drawString</code> y <code>Line2D.Float</code>, que aceptan coordenadas con decimales.</p>
<p class="l"><b>L74</b> <code>float base = MARGEN + 36;</code> la <b>línea base</b> del título en y = 46. Recuerda
(capítulo 37): la <i>y</i> de <code>drawString</code> no es la parte de arriba de las letras, sino la línea sobre la
que «se apoyan» (las letras como la g o la j bajan de ella).</p>
<p class="l"><b>L75</b> <code>g2.drawString(titulo, xTitulo, base);</code> escribe «Jugador 1» en (98, 46).</p>
<p class="l"><b>L76</b> <code>g2.setPaint(new GradientPaint(xTitulo, 0, color, xTitulo + 140, 0,
Tema.conAlfa(color, 0)));</code> prepara un <b>degradado</b>: en x = 98 el color de la tarjeta y en x = 238 el mismo
color con alfa 0 (totalmente transparente). Como las dos y son 0, el degradado es horizontal (la y no cambia nada).
Se usa <code>setPaint</code> y no <code>setColor</code> porque un degradado no es un color: es una
<i>pintura</i> (<code>Paint</code>), y un color es solo la pintura más simple.</p>
<p class="l"><b>L77</b> <code>g2.setStroke(Dibujo.redondo(3f));</code> trazo de 3 píxeles con puntas redondas.</p>
<p class="l"><b>L78</b> <code>g2.draw(new Line2D.Float(xTitulo, base + 12, xTitulo + 140, base + 12));</code>
dibuja el segmento de (98, 58) a (238, 58), 12 píxeles por debajo de la línea base. Con el degradado, la raya nace
intensa bajo la «J» y se desvanece hacia la derecha, como en el diseño. <code>Line2D.Float</code> es la versión de
<code>Line2D</code> que guarda sus coordenadas como <code>float</code>; el punto entre los dos nombres indica que
<code>Float</code> es una clase declarada <i>dentro</i> de <code>Line2D</code>.</p>
"""),
             ("g2.setFont(Tema.fuente(Font.PLAIN", r"""
<p class="l"><b>L80</b> Fuente normal (no negrita) de 13 puntos para la etiqueta pequeña.</p>
<p class="l"><b>L81</b> Otra vez color blanco. Hay que volver a llamar a <code>setColor</code> porque la línea 76 dejó puesta
la pintura del degradado; sin esta línea, «Nombre» se escribiría con el degradado y casi no se vería.</p>
<p class="l"><b>L82</b> <code>g2.drawString("Nombre", MARGEN + 18, MARGEN + 70);</code> escribe «Nombre» en
(28, 80), justo encima de la caja de texto, que empieza en y = 84.</p>
<p class="l"><b>L83</b> <code>g2.dispose();</code> libera la copia del pincel (capítulo 41). Hay que hacerlo con
toda copia creada con <code>create()</code>; si no, se acumulan recursos del sistema en cada redibujado.</p>
<p class="l"><b>L84–L85</b> Cierran el método y la clase. Ojo: <code>paintComponent</code> no pinta la caja de
texto. Swing pinta primero el componente (<code>paintComponent</code>), después su borde y por último sus hijos;
por eso <code>CampoTexto</code> aparece encima de todo sin que hagamos nada.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>1. Lo que pasa al crear una tarjeta</h3>
<p>La pantalla de configuración (capítulo 58) hará <code>new TarjetaJugador("Jugador 2", Tema.AZUL)</code>. En ese
momento ocurre, en este orden:</p>
<ol>
<li><code>super(Tema.AZUL, 26)</code>: se construye la parte <code>Tarjeta</code> (y antes, la parte
<code>JPanel</code>): color azul, radio 26, transparente, centrada.</li>
<li>Se guardan <code>titulo = "Jugador 2"</code> y <code>color = AZUL</code>.</li>
<li>Se quita el gestor de distribución y se crea un <code>CampoTexto</code> con ayuda «Jugador 2» y borde azul.</li>
<li>La caja se mete en la tarjeta y la tarjeta queda fijada en 290 × 150.</li>
</ol>
<p>Todavía no se ha dibujado nada. Cuando la tarjeta se muestre, Swing llamará a <code>doLayout()</code> (la caja
queda en (22, 84) con 246 × 46) y después a <code>paintComponent</code>.</p>

<h3>2. Las capas de un dibujo</h3>
<table class="tabla">
<tr><th>Orden</th><th>Qué se pinta</th><th>Quién</th></tr>
<tr><td>1</td><td>Relleno de cristal y tinte de color</td><td><code>Tarjeta.paintComponent</code> (por el <code>super</code>)</td></tr>
<tr><td>2</td><td>Borde de neón de la caja</td><td><code>Tarjeta.paintComponent</code></td></tr>
<tr><td>3</td><td>Icono, título, raya y «Nombre»</td><td><code>TarjetaJugador.paintComponent</code></td></tr>
<tr><td>4</td><td>La caja de texto con su contenido</td><td>Swing, al pintar los hijos</td></tr>
</table>

<h3>3. El viaje de un nombre (traza de setComputadora)</h3>
<p>Supón que en la tarjeta del Jugador 2 el usuario escribe «Luis» y luego juega con las opciones de modo. Así
cambian los datos:</p>
<table class="tabla">
<tr><th>Acción</th><th>esComputadora</th><th>nombreGuardado</th><th>Texto de la caja</th><th>¿Se puede escribir?</th><th>getNombre()</th></tr>
<tr><td>Recién creada</td><td>false</td><td>""</td><td>"" (se ve la ayuda gris «Jugador 2»)</td><td>sí</td><td>"Jugador 2"</td></tr>
<tr><td>Escribe «Luis»</td><td>false</td><td>""</td><td>"Luis"</td><td>sí</td><td>"Luis"</td></tr>
<tr><td><code>setComputadora(true)</code></td><td>true</td><td>"Luis"</td><td>"Computadora"</td><td>no</td><td>"Computadora"</td></tr>
<tr><td><code>setComputadora(true)</code> otra vez</td><td colspan="5">la guarda (L49) ve que no hay cambio y sale: nada se toca</td></tr>
<tr><td><code>setComputadora(false)</code></td><td>false</td><td>"Luis"</td><td>"Luis"</td><td>sí</td><td>"Luis"</td></tr>
</table>
<p>Ahora imagina la misma secuencia <b>sin</b> la guarda: en el segundo <code>setComputadora(true)</code>, la línea
54 guardaría el texto actual de la caja, que ya es «Computadora». Al volver a humano, la caja diría «Computadora» y
«Luis» se habría perdido. Tres líneas de guarda evitan ese error tan difícil de ver.</p>

<h3>4. Qué devuelve getNombre en cada caso</h3>
<table class="tabla">
<tr><th>Texto escrito</th><th>Después de trim()</th><th>¿isEmpty()?</th><th>Devuelve</th></tr>
<tr><td><code>"Ana"</code></td><td><code>"Ana"</code></td><td>no</td><td><code>"Ana"</code></td></tr>
<tr><td><code>"  Ana  "</code></td><td><code>"Ana"</code></td><td>no</td><td><code>"Ana"</code></td></tr>
<tr><td><code>""</code></td><td><code>""</code></td><td>sí</td><td><code>"Jugador 1"</code></td></tr>
<tr><td><code>"    "</code></td><td><code>""</code></td><td>sí</td><td><code>"Jugador 1"</code></td></tr>
</table>

<h2>Compila y prueba</h2>
<p>Pulsa <i>Run → Clean and Build Project</i> (Shift+F11). En la ventana <i>Output</i> debe aparecer
<code>BUILD SUCCESS</code>. Desde PowerShell, sin NetBeans, también puedes comprobarlo así:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
javac -encoding UTF-8 -d out src\*.java</pre>
<p>Si no sale ningún mensaje, compiló bien (<code>out\</code> está en tu <code>.gitignore</code>, no se sube).</p>
<p>Todavía <b>no puedes verla</b>: ninguna pantalla la usa aún. La verás completa en el capítulo 58, dentro de la
pantalla de configuración. Si no quieres esperar tanto, en el capítulo 56 aprenderás a abrir una
<b>vista previa</b>, y allí hay un apartado que muestra en una pantalla de prueba todas las piezas de los capítulos
49 a 54, incluida esta tarjeta en sus dos modos.</p>
<p>Errores típicos:</p>
<table class="tabla">
<tr><th>Mensaje</th><th>Causa y solución</th></tr>
<tr><td><i>cannot find symbol: class Tarjeta</i> (o <code>CampoTexto</code>, <code>Iconos</code>…)</td><td>Falta
esa clase o tiene otro nombre. Revisa que existan en <code>src</code> los archivos de los capítulos 40 a 47 con
las mayúsculas exactas.</td></tr>
<tr><td><i>constructor Tarjeta in class Tarjeta cannot be applied to given types</i></td><td>Tu
<code>Tarjeta</code> no tiene el constructor de dos parámetros <code>(Color, int)</code>. Revísalo en el capítulo
43.</td></tr>
<tr><td><i>call to super must be first statement in constructor</i></td><td>Pusiste algo antes de
<code>super(color, 26);</code>. Debe ser la primera línea del constructor.</td></tr>
<tr><td><i>attempting to assign weaker access privileges; was public</i></td><td>Escribiste
<code>doLayout()</code> sin <code>public</code> (o con <code>protected</code>).</td></tr>
<tr><td><i>class TarjetaJugador is public, should be declared in a file named TarjetaJugador.java</i></td><td>El
nombre del archivo no coincide con el de la clase (cuidado con mayúsculas).</td></tr>
</table>

<div class="caja git"><b>Git</b> Una pieza nueva, un commit (seguimos en la rama <code>interfaz-neon</code>):
<pre class="ps">git status
git add src\TarjetaJugador.java
git commit -m "TarjetaJugador: tarjeta para el nombre"
git push</pre>
<code>git status</code> debe mostrar el archivo nuevo en rojo («Untracked») antes del <code>add</code>. El
<code>push</code> sube el commit a tu rama en GitHub (el enlace con la rama remota lo hiciste en el capítulo
38).</div>

<h2>Resumen</h2>
<ul>
<li><code>TarjetaJugador</code> hereda de <code>Tarjeta</code>: aprovecha la caja de cristal y solo agrega lo
suyo. Con <code>super(color, 26)</code> elige el constructor del padre.</li>
<li>Lo privado del padre no se ve en la hija; por eso la hija guarda su propio <code>color</code>.</li>
<li>Con <code>setLayout(null)</code> y <code>doLayout()</code> el hijo se coloca a mano con
<code>setBounds</code>, calculando desde el tamaño real.</li>
<li><code>getNombre()</code> limpia espacios con <code>trim()</code> y nunca devuelve un nombre vacío.</li>
<li><code>setComputadora</code> guarda lo escrito, bloquea la caja y lo devuelve al volver; la cláusula de guarda
evita perder datos con llamadas repetidas.</li>
<li>Primero <code>super.paintComponent(g)</code> y luego lo propio: se dibuja por capas.</li>
<li>Tras cambiar un dato que afecta al dibujo, <code>repaint()</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Formularios con tarjetas</b>: una tarjeta «Datos de envío» con título, icono y campos, que hereda de una
tarjeta base común a toda la aplicación (mismo borde, mismo fondo).</li>
<li><b>Bloquear y recordar</b>: en una tienda en línea, la casilla «Usar la misma dirección de facturación»
bloquea los campos y pone la dirección de envío; al desmarcarla, devuelve lo que el cliente había escrito. Es
exactamente <code>setComputadora</code>.</li>
<li><b>Valores por defecto</b>: un editor de textos que llama «Documento sin título» al archivo cuyo nombre se dejó
vacío, como <code>getNombre()</code> devuelve el título.</li>
<li><b>Cláusulas de guarda</b>: en cualquier método que cambie de estado («conectar», «abrir», «activar»), un
«si ya está así, no hagas nada» evita efectos dobles.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Calcula a mano dónde quedaría la caja de texto si <code>ALTO</code> fuera 170. Pista: solo cambia la
<i>y</i> (170 − 10 − 10 − 46).</li>
<li>Cambia la raya del título para que vaya del color de la tarjeta a <code>Tema.CIAN</code> en vez de a
transparente. ¿Qué pintura tienes que cambiar y en qué argumento?</li>
<li>Agrega un método <code>public void setNombre(String nombre)</code> que escriba el nombre en la caja. Úsalo para
que el Jugador 1 empiece con tu nombre (lo podrás ver con la vista previa del capítulo 56).</li>
<li>Haz que <code>getNombre()</code> devuelva el nombre con la primera letra en mayúscula: «ana» → «Ana». Pista:
<code>nombre.substring(0, 1).toUpperCase() + nombre.substring(1)</code>, y cuidado con el texto vacío.</li>
<li>Explica con una tabla como la de la traza qué pasaría sin la guarda de las líneas 49–51 con la secuencia:
escribir «Sofía», <code>setComputadora(true)</code>, <code>setComputadora(true)</code>,
<code>setComputadora(false)</code>.</li>
</ol></div>
""",
}
