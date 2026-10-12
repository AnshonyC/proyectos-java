CAPITULO = {
    "numero": 57,
    "titulo": "PantallaInstrucciones.java: «Cómo jugar»",
    "antes": r"""<p class="entrada">En este capítulo construyes la segunda pantalla del diseño: la tarjeta «Cómo jugar», con tres
pasos numerados, una X rosa y una O azul pintadas en medio de una frase, y un tablero de ejemplo dibujado con un
<code>Tablero</code> de verdad. Es la primera pantalla que se arma casi solo juntando piezas que ya hiciste.</p>

<h2>Por qué existe este archivo</h2>
<p>Quien abre el Totito por primera vez puede no conocer las reglas, o conocerlas con otro nombre (tres en raya,
tic-tac-toe, gato). El menú del capítulo 56 tiene un botón <b>Instrucciones</b>, y ese botón necesita una pantalla a
donde llevar. Esa pantalla es <code>PantallaInstrucciones</code>.</p>
<p>Fíjate en lo que <b>no</b> tiene que hacer esta clase, porque ya lo hacen otras:</p>
<ul>
<li>El fondo degradado, las X y O gigantes de adorno y el encabezado con el botón de cerrar los pone
<code>PantallaBase</code> (capítulo 55). Esta clase hereda de ella y recibe todo eso gratis.</li>
<li>La caja de cristal con borde de neón es una <code>Tarjeta</code> (capítulo 43).</li>
<li>El título grande con degradado, icono y subrayado es un <code>Rotulo</code> (capítulo 46).</li>
<li>Cada paso con su circulito numerado es un <code>PasoInstruccion</code> (capítulo 53).</li>
<li>El tablero de muestra es un <code>PanelTablero</code> (capítulo 48), y el botón «Regresar» un <code>BotonNeon</code>
(capítulo 44).</li>
</ul>
<p>Así que el trabajo de este archivo es parecido al de quien monta un mueble con las piezas ya cortadas: decidir
<b>qué</b> pieza va, <b>en qué orden</b> y <b>con qué medidas</b>. Por eso cabe en 57 líneas. Ese es el premio de los
18 capítulos anteriores: una pantalla completa y vistosa sale casi sin código nuevo.</p>
<figure><img src="diseno/instrucciones.jpg"><figcaption>El diseño original de la pantalla «Cómo jugar». Compáralo
con el código: cada cosa que ves aquí es una línea de este capítulo.</figcaption></figure>

<h2>Qué vas a aprender</h2>
<ul>
<li>A <b>componer</b> una pantalla a partir de componentes propios (composición, capítulo 21).</li>
<li>Cómo un <code>JLabel</code> de Swing entiende <b>HTML</b>: <code>&lt;b&gt;</code>, <code>&lt;br&gt;</code> y
<code>&lt;font color&gt;</code> para pintar palabras sueltas de otro color.</li>
<li>Por qué dentro de un texto de Java el HTML usa comillas simples (<code>'</code>) y no dobles.</li>
<li><code>BoxLayout</code>, <code>Box.createRigidArea</code> y <code>BorderFactory.createEmptyBorder</code> para colocar
cosas en columna con márgenes exactos.</li>
<li>El <b>encadenamiento de métodos</b> (<code>.conIcono(...).conSubrayado(...)</code>).</li>
<li>Por qué un método puede ser <code>static</code> y <code>private</code> a la vez, y cuándo conviene.</li>
<li>A <b>reutilizar la lógica</b> del juego (<code>Tablero</code>) para fabricar un dibujo de ejemplo, sin escribir
coordenadas a mano.</li>
<li>A ver la pantalla terminada con la <code>VistaPrevia</code> del capítulo 56, cambiando una sola línea.</li>
</ul>

<h2>Créalo</h2>
<p>Trabajas en la rama <code>interfaz-neon</code>, como en toda la Parte VII. Antes de empezar, confírmalo en
PowerShell, desde la carpeta del proyecto:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
git branch --show-current</pre>
<pre class="salida">interfaz-neon</pre>
<p>Si dice otra cosa, cámbiate con <code>git switch interfaz-neon</code> (capítulo 9).</p>
<p>En NetBeans:</p>
<ol>
<li>En el panel <i>Projects</i>, despliega <i>Totito → Source Packages</i>.</li>
<li>Clic derecho sobre <i>&lt;default package&gt;</i> → <i>New → Java Class…</i></li>
<li>En <i>Class Name</i> escribe <code>PantallaInstrucciones</code> (con la P y la I mayúsculas, sin tilde y sin
espacios) y pulsa <i>Finish</i>.</li>
<li>NetBeans crea el archivo con una plantilla. Borra todo su contenido y escribe el código de abajo.</li>
</ol>
<p>Alternativa con PowerShell (crea el archivo vacío y lo abre en el Bloc de notas):</p>
<pre class="ps">New-Item src\PantallaInstrucciones.java
notepad src\PantallaInstrucciones.java</pre>
<div class="caja consejo"><b>Escríbelo, no lo pegues</b> Cuando teclees el código, escribe tú mismo cada línea
aunque tardes más. Al escribir <code>Tema.</code> NetBeans te mostrará la lista de colores que creaste en el capítulo 40;
al escribir <code>BotonNeon.</code>, las fábricas del capítulo 44. Es la mejor manera de repasar sin darte cuenta.</div>
""",
    "archivos": [
        {"ruta": "src/PantallaInstrucciones.java",
         "bloques": [
             (None, r"""<p class="l"><b>L1</b> <code>import java.awt.Dimension;</code> trae la clase <code>Dimension</code>, que
guarda un par ancho × alto en píxeles. Recuerda (capítulo 11) que un <code>import</code> no copia código: solo le dice al
compilador «cuando escriba <code>Dimension</code>, me refiero a <code>java.awt.Dimension</code>». La usaremos para
los espacios en blanco entre piezas. Sin esta línea, el compilador diría <code>cannot find symbol: class Dimension</code>.</p>
<p class="l"><b>L2</b> <code>javax.swing.BorderFactory</code> es una «fábrica de bordes»: una clase con métodos
<code>static</code> que crean bordes ya hechos. Usaremos uno invisible que funciona como margen interior.</p>
<p class="l"><b>L3</b> <code>javax.swing.Box</code> fabrica piezas de relleno invisibles para los <code>BoxLayout</code>.
Ya la usaste en <code>PantallaBase</code> (capítulo 55).</p>
<p class="l"><b>L4</b> <code>javax.swing.BoxLayout</code> es el organizador que pone los componentes uno debajo de otro
(o uno al lado de otro). Lo explicó el capítulo 37.</p>
<p class="l"><b>L5</b> Línea en blanco: separa los imports del resto, solo por legibilidad.</p>
<p class="l">Fíjate en lo que <b>no</b> se importa: <code>Tarjeta</code>, <code>Rotulo</code>, <code>Tema</code>,
<code>PasoInstruccion</code>… Son clases tuyas y viven en el mismo paquete (el <i>default package</i>), así que Java
las encuentra sin <code>import</code>. Solo se importan las clases de la biblioteca de Java que se nombran en el archivo.</p>"""),
             ("public class PantallaInstrucciones", r"""<p class="l"><b>L6–L8</b> Comentario de documentación
(<code>/** … */</code>): dice qué pantalla del diseño es esta. Ocurre lo mismo en todos los archivos del proyecto: el
comentario de arriba responde «¿qué es esto?» antes de leer una sola línea de código. Los comentarios del código
fuente van sin tildes a propósito (salvo los textos que se ven en pantalla), para que nunca se rompan si alguien abre
el archivo con otra codificación.</p>
<p class="l"><b>L9</b> <code>public class PantallaInstrucciones extends PantallaBase</code>: declara la clase. Palabra
por palabra: <code>public</code>, cualquiera puede usarla (el <code>PanelPrincipal</code> del capítulo 61 la creará);
<code>class</code>, es un molde de objetos; el nombre, igual que el del archivo (Java lo exige para las clases
<code>public</code>); <code>extends PantallaBase</code>, <b>hereda</b> de la clase abstracta del capítulo 55. Gracias a
ese <code>extends</code>, una <code>PantallaInstrucciones</code> <i>es</i> un <code>JPanel</code> con fondo neón,
encabezado y los métodos <code>agregar</code>, <code>espacio</code> y <code>relleno</code>. Sin el
<code>extends</code>, tendrías que repetir aquí las 116 líneas de <code>PantallaBase</code>.</p>
<p class="l"><b>L10</b> En blanco.</p>"""),
             ("private static final int ANCHO_PASOS", r"""<p class="l"><b>L11</b> Una constante: el ancho, en
píxeles, de la columna de texto de la tarjeta (título y pasos). <code>private</code>: solo se usa dentro de este
archivo. <code>static</code>: pertenece a la clase, no a cada objeto (hay un solo 400 para todas las pantallas de
instrucciones que se creen). <code>final</code>: no se puede cambiar después. Las tres palabras juntas son la receta
de una constante en Java (capítulo 20), y su nombre va en MAYÚSCULAS_CON_GUIONES por convención.</p>
<p class="l">¿Por qué una constante y no escribir <code>400</code> cuatro veces? Porque el número aparece en el título y
en los tres pasos. Si mañana quieres la tarjeta más ancha, cambias una línea y no cuatro, y nunca se te olvida una
(capítulo 27: «números mágicos»).</p>
<p class="l"><b>L12</b> En blanco.</p>"""),
             ("public PantallaInstrucciones(", r"""<p class="l"><b>L13</b> El <b>constructor</b>: el método que se ejecuta
una vez, al hacer <code>new PantallaInstrucciones(...)</code>. Se llama igual que la clase y no tiene tipo de retorno.
Recibe un parámetro de tipo <code>Navegacion</code> (la interfaz del capítulo 39): el objeto al que esta pantalla le
pedirá «llévame al menú». La pantalla no sabe quién es ese objeto (será el <code>PanelPrincipal</code>, o la
navegación «de mentira» de la vista previa); solo sabe que cumple la interfaz. Todo lo que se ve en la pantalla se
construye dentro de este constructor, de arriba abajo.</p>
<p class="l"><b>L14</b> <code>super(navegacion);</code> llama al constructor de la clase madre,
<code>PantallaBase</code>, y le pasa la navegación (ella la necesita para que la X del encabezado llame a
<code>salir()</code>). Tiene que ser la <b>primera</b> instrucción del constructor: primero se construye la parte
heredada (el fondo, el encabezado, el panel de contenido) y después lo propio. Si la quitas, Java intentaría llamar
a un <code>super()</code> sin argumentos, que <code>PantallaBase</code> no tiene, y el compilador se quejaría:
<code>constructor PantallaBase in class PantallaBase cannot be applied to given types</code>.</p>
<p class="l"><b>L15</b> En blanco: separa «preparar la base» de «armar el contenido».</p>"""),
             ("String x =", r"""<p class="l"><b>L16</b> Crea un pedacito de <b>HTML</b> y lo guarda en una variable
<code>String</code> llamada <code>x</code>. Si sustituyes <code>Tema.hex(Tema.ROSA)</code> por lo que devuelve
(<code>"#FF3BD4"</code>, capítulo 40), el texto final es exactamente:</p>
<pre class="salida">&lt;font color='#FF3BD4'&gt;&lt;b&gt;X&lt;/b&gt;&lt;/font&gt;</pre>
<p class="l">Es decir: «la letra X, en negrita (<code>&lt;b&gt;</code>), de color rosa (<code>&lt;font color&gt;</code>)».
¿Por qué HTML? Porque el texto de cada paso se mostrará en un <code>JLabel</code> (dentro de
<code>PasoInstruccion</code>, capítulo 53), y un <code>JLabel</code> cuyo texto empieza por <code>&lt;html&gt;</code>
no lo muestra tal cual: lo interpreta como una pequeña página web. Así se puede pintar <b>una sola letra</b> de otro
color en medio de una frase blanca, cosa que con <code>setForeground</code> (que colorea todo el texto) es imposible.</p>
<p class="l">Dos detalles que parecen mínimos y no lo son. Primero, las <b>comillas simples</b> alrededor del color:
el texto de Java ya está entre comillas dobles; si el HTML también usara dobles, Java creería que el texto termina ahí.
Habría que escribir <code>\"</code> (comilla «escapada»), que es más feo. HTML acepta las dos clases de comillas, así
que se usan las simples. Segundo, el color sale de <code>Tema.hex</code> y no se escribe a mano: si un día cambias el
rosa en <code>Tema</code>, la X de las instrucciones cambia sola.</p>
<p class="l"><b>L17</b> Lo mismo para la O, en azul (<code>#2F84FF</code>). Ahora tienes dos «piezas de texto» listas
para insertar en las frases.</p>
<p class="l"><b>L18</b> En blanco.</p>"""),
             ("Tarjeta tarjeta =", r"""<p class="l"><b>L19</b> Crea la caja de cristal con borde de neón morado
(capítulo 43) y la guarda en una variable <b>local</b> llamada <code>tarjeta</code>. Local quiere decir que solo existe
dentro de este constructor: ninguna otra parte de la clase la necesita después, así que no hace falta un atributo.</p>
<p class="l"><b>L20</b> Le pone a la tarjeta un <code>BoxLayout</code> vertical. Un <code>JPanel</code> trae por
defecto un <code>FlowLayout</code>, que acomoda las cosas en fila como palabras en un renglón; nosotros queremos una
columna: título, pasos, tablero. Los dos argumentos son: el contenedor que se va a organizar (la misma
<code>tarjeta</code>; <code>BoxLayout</code> lo pide porque necesita saber a quién pertenece) y el eje,
<code>BoxLayout.Y_AXIS</code>, «de arriba abajo». Sin esta línea, los pasos quedarían uno al lado de otro y no cabrían.</p>
<p class="l"><b>L21</b> <code>BorderFactory.createEmptyBorder(20, 30, 22, 30)</code> crea un borde <b>vacío</b>, que no
se dibuja pero ocupa sitio: es el margen interior de la tarjeta. Los cuatro números van en el orden
<b>arriba, izquierda, abajo, derecha</b> (no es el orden del reloj; es el que eligió Swing y hay que
memorizarlo). Así el título no queda pegado al borde de neón. Sin esta
línea, el contenido tocaría el borde y el halo quedaría encima de las letras.</p>"""),
             ("tarjeta.add(Rotulo.titulo", r"""<p class="l"><b>L22</b> Agrega a la tarjeta un título creado con la
fábrica <code>Rotulo.titulo</code> (capítulo 46). Sus argumentos, en orden: el texto <code>"Cómo jugar"</code> (este sí
lleva tilde porque se ve en pantalla), el tamaño de letra <code>36f</code> (la <code>f</code> indica que es un
<code>float</code>, número con decimales de precisión simple, que es lo que pide el método), el color de inicio del
degradado (<code>Tema.TEXTO</code>, blanco), el color final (<code>Tema.LAVANDA</code>), el ancho
(<code>ANCHO_PASOS</code>, 400) y el alto (70 píxeles).</p>
<p class="l"><b>L23</b> <code>.conIcono(Iconos.LIBRO, Tema.ROSA)</code>: sobre el <code>Rotulo</code> recién creado,
se llama a <code>conIcono</code>, que le pone el libro rosa a la izquierda (capítulo 42) y <b>devuelve el mismo rótulo</b>
(<code>return this;</code>). Por eso se puede seguir encadenando con otro punto en la línea siguiente. Este estilo se
llama <b>encadenamiento de métodos</b> o interfaz fluida: se lee casi como una frase («un título, con icono, con
subrayado»).</p>
<p class="l"><b>L24</b> <code>.conSubrayado(Tema.ROSA, Tema.AZUL)</code> le agrega la línea de rosa a azul debajo del
texto, y el último paréntesis cierra el <code>tarjeta.add(</code> de la L22. El <code>;</code> marca el final de la
instrucción completa, que ocupa tres renglones: a Java no le importan los saltos de línea, solo el punto y coma.</p>
<p class="l"><b>L25</b> Un hueco fijo de 6 píxeles de alto entre el título y el primer paso.
<code>new Dimension(0, 6)</code> es «0 de ancho, 6 de alto», y <code>Box.createRigidArea</code> fabrica con esa medida
un componente invisible y rígido (no se estira). Es como un taco de madera entre dos libros de una estantería.</p>"""),
             ("tarjeta.add(new PasoInstruccion(1", r"""<p class="l"><b>L26–L27</b> El primer paso. Se crea un
<code>PasoInstruccion</code> (capítulo 53) con: el número <code>1</code> que irá dentro del círculo, el color del
círculo (<code>Tema.ROSA</code>), el texto y el ancho. El texto se arma pegando (con <code>+</code>, capítulo 17) cuatro
pedazos: <code>"Dos jugadores se turnan&lt;br&gt;para marcar "</code>, la <code>x</code> de la L16,
<code>" y "</code>, la <code>o</code> de la L17 y un punto. El <code>&lt;br&gt;</code> es el salto de línea de HTML:
parte la frase en dos renglones justo donde lo quiere el diseño. <code>PasoInstruccion</code> le añade al principio
<code>&lt;html&gt;</code> y al final <code>&lt;/html&gt;</code>, que es lo que activa el modo HTML del
<code>JLabel</code>. La instrucción se partió en dos renglones solo porque no cabía en uno.</p>
<p class="l"><b>L28–L29</b> El segundo paso, con círculo morado. Aquí no hay letras de colores: solo el
<code>&lt;br&gt;</code>. Fíjate en la tilde de «línea» y «símbolos»: los textos visibles llevan tildes; por eso el
proyecto compila con <code>UTF-8</code> (capítulo 5).</p>
<p class="l"><b>L30–L31</b> El tercer paso, con círculo azul. Rosa, morado y azul: los mismos tres colores de los
botones del menú (capítulo 56). Esa repetición es la que hace que todas las pantallas se sientan
del mismo juego (capítulo 36, consistencia).</p>
<p class="l">Los tres pasos se agregan <b>sin espacios entre ellos</b>: cada <code>PasoInstruccion</code> mide 54
píxeles de alto y su propio dibujo ya deja aire arriba y abajo.</p>"""),
             ("tarjeta.add(Box.createRigidArea(new Dimension(0, 10)))", r"""<p class="l"><b>L32</b> Un hueco de 10
píxeles entre el último paso y el tablero de ejemplo. Un poco más grande que el de la L25 porque separa dos «ideas»
distintas (reglas y ejemplo): en diseño, el espacio también comunica qué va junto y qué va aparte.</p>
<p class="l"><b>L33</b> Agrega el tablero de ejemplo. No se crea aquí: se llama al método
<code>tableroDeEjemplo()</code> (L47), que lo fabrica y lo devuelve, y lo que devuelve se pasa directamente a
<code>add</code>. Separarlo en un método tiene dos ventajas: el constructor se lee como un índice («título, pasos,
tablero») y los detalles del tablero quedan en un lugar con nombre propio.</p>
<p class="l"><b>L34</b> En blanco: la tarjeta está completa.</p>"""),
             ("BotonNeon regresar", r"""<p class="l"><b>L35–L36</b> Crea el botón «Regresar» con la fábrica
<code>BotonNeon.pildora</code> (capítulo 44): texto, icono de flecha a la izquierda, degradado de rosa a morado y un
tamaño de 330 × 70 píxeles. Se guarda en una variable local porque en la línea siguiente hay que conectarlo.</p>
<p class="l"><b>L37</b> <code>regresar.addActionListener(e -&gt; navegacion.irAlMenu());</code> conecta el botón con
lo que debe pasar al pulsarlo. <code>addActionListener</code> recibe un «oyente»: un objeto con un método que Swing
llamará en cada clic. En lugar de escribir una clase entera, se le pasa una <b>lambda</b> (capítulo 25):
<code>e -&gt; navegacion.irAlMenu()</code> se lee «dado el evento <code>e</code>, pide ir al menú». La
<code>e</code> (un <code>ActionEvent</code> con detalles del clic) no se usa, pero tiene que estar porque el método
del oyente la recibe.</p>
<p class="l">Un detalle fino: la lambda usa <code>navegacion</code>, el <b>parámetro</b> del constructor, no un atributo.
Esta clase no guarda la navegación en ningún atributo porque solo la necesita aquí. La lambda «se lleva» el valor del
parámetro y lo recordará aunque el constructor ya haya terminado. Java permite esto siempre que la variable no se
modifique nunca (se dice que es <i>efectivamente final</i>). Sin esta línea, el botón se vería, se iluminaría al pasar
el ratón… y no haría nada.</p>
<p class="l"><b>L38</b> En blanco.</p>"""),
             ("relleno();", r"""<p class="l"><b>L39–L43</b> Aquí se decide el orden vertical de la pantalla, con los
métodos heredados de <code>PantallaBase</code> (capítulo 55):</p>
<ul>
<li><code>relleno()</code> (L39): un resorte invisible arriba.</li>
<li><code>agregar(tarjeta)</code> (L40): la tarjeta, centrada en horizontal.</li>
<li><code>espacio(8)</code> (L41): 8 píxeles fijos entre la tarjeta y el botón.</li>
<li><code>agregar(regresar)</code> (L42): el botón.</li>
<li><code>relleno()</code> (L43): otro resorte abajo.</li>
</ul>
<p class="l">Los dos resortes se reparten por igual el espacio sobrante, y por eso el bloque «tarjeta + botón» queda
centrado en vertical. Con los números reales: el área de contenido mide 584 píxeles de alto, la tarjeta 464, el hueco
8 y el botón 70; sobran 42, y cada resorte se queda con 21. Si quitas el primer <code>relleno()</code>, todo sube y se
pega al encabezado; si quitas el segundo, todo baja.</p>
<p class="l"><b>L44</b> La llave que cierra el constructor. <b>L45</b> En blanco.</p>"""),
             ("private static PanelTablero tableroDeEjemplo", r"""<p class="l"><b>L46</b> Comentario: explica qué dibuja el
método, para no tener que deducirlo de las coordenadas.</p>
<p class="l"><b>L47</b> Declara el método. <code>private</code>: solo lo usa esta clase. <code>static</code>: no usa
ningún atributo del objeto (no hay <code>this</code> en su interior), así que puede pertenecer a la clase; ponerlo deja
claro, a quien lea, que el método no cambia nada de la pantalla. <code>PanelTablero</code> es el tipo de lo que devuelve.
Los paréntesis vacíos: no recibe nada.</p>
<p class="l"><b>L48</b> Crea un <code>Tablero</code>, <b>la clase de lógica del capítulo 29</b>, la misma que usa una
partida real. Empieza con las nueve casillas vacías.</p>
<p class="l"><b>L49–L52</b> Marca cuatro casillas con <code>marcarCasilla(fila, columna, ficha)</code>: O en (0,0), X en
(0,1), O en (0,2) y X en (1,1). Filas y columnas cuentan desde 0, así que (0,0) es la esquina de arriba a la izquierda y
(1,1) el centro. Es la posición exacta del diseño. <code>marcarCasilla</code> devuelve un <code>boolean</code> (si la
jugada valió) que aquí se ignora: sabemos que las casillas están vacías.</p>
<p class="l">¿Por qué usar un <code>Tablero</code> y no dibujar las cuatro fichas a mano? Porque así el ejemplo es
<b>exactamente</b> igual que una partida de verdad: mismas fichas, mismos colores, mismo grosor. Y si el ejemplo
tuviera tres en línea, aparecería la raya ganadora sin escribir nada (lo comprobarás en los ejercicios). Reutilizar la
lógica en lugar de imitarla es una costumbre que ahorra errores.</p>"""),
             ("PanelTablero panel = new PanelTablero(46)", r"""<p class="l"><b>L53</b> Crea el componente que dibuja
tableros (capítulo 48) con casillas de 46 píxeles. Su tamaño total sale de la fórmula de ese capítulo:
2 × (10 + 8) + 3 × 46 = 174 píxeles de lado. En la partida real las casillas miden 100; aquí 46, para que el ejemplo
quepa debajo de los pasos sin robar protagonismo.</p>
<p class="l"><b>L54</b> <code>panel.mostrar(ejemplo)</code> copia las fichas del <code>Tablero</code> al panel y busca
si hay línea ganadora (no la hay). El panel <b>no</b> se queda con el tablero: copia lo que necesita para dibujar.
Fíjate también en lo que no se hace: no se le pone oyente ni se marca como interactivo. Por defecto un
<code>PanelTablero</code> no es interactivo, así que este ejemplo no reacciona a clics ni muestra la ficha fantasma
ni la manita. Es un dibujo de muestra.</p>
<p class="l"><b>L55</b> Devuelve el panel listo a quien llamó (la L33), que lo agrega a la tarjeta. La variable
<code>ejemplo</code> deja de usarse aquí; Java la borrará de la memoria cuando quiera (el «recolector de basura»).</p>
<p class="l"><b>L56–L57</b> Cierran el método y la clase.</p>"""),
         ]},
    ],
    "despues": r"""<h2>Cómo funciona por dentro</h2>
<p>Sigamos qué pasa, en orden, cuando alguien escribe <code>new PantallaInstrucciones(nav)</code>:</p>
<ol>
<li><b>La base.</b> <code>super(nav)</code> ejecuta el constructor de <code>PantallaBase</code>: pone un
<code>BorderLayout</code>, el <code>Encabezado</code> arriba y un panel <code>contenido</code> vacío en el centro, con
<code>BoxLayout</code> vertical.</li>
<li><b>Los textos de colores.</b> Se fabrican <code>x</code> y <code>o</code>. Después de la L27, el primer paso recibe este
texto (ya con lo que añade <code>PasoInstruccion</code>):
<pre class="salida">&lt;html&gt;Dos jugadores se turnan&lt;br&gt;para marcar &lt;font color='#FF3BD4'&gt;&lt;b&gt;X&lt;/b&gt;&lt;/font&gt; y &lt;font color='#2F84FF'&gt;&lt;b&gt;O&lt;/b&gt;&lt;/font&gt;.&lt;/html&gt;</pre>
El <code>JLabel</code> lo traduce a dos renglones blancos con una X rosa y una O azul en negrita.</li>
<li><b>La tarjeta.</b> Se apilan dentro: título (70 px de alto), hueco (6), tres pasos (54 cada uno), hueco (10) y tablero
(174). Con los márgenes de la L21 (20 arriba, 22 abajo), la tarjeta mide 20 + 70 + 6 + 162 + 10 + 174 + 22 = <b>464</b>
píxeles de alto. De ancho, el <code>BoxLayout</code> toma el componente más ancho (400) y le suma los márgenes
laterales (30 + 30): <b>460</b>.</li>
<li><b>El botón</b> se crea y se conecta. Todavía no hace nada: solo recuerda que, cuando lo pulsen, debe llamar a
<code>nav.irAlMenu()</code>.</li>
<li><b>El orden.</b> Resorte, tarjeta, 8 px, botón, resorte. El constructor termina. Nada se ha dibujado aún: dibujar
lo hará Swing más tarde, cuando la pantalla se muestre, llamando a los <code>paintComponent</code> de cada pieza
(capítulo 37).</li>
</ol>
<p>Más tarde, cuando el usuario pulsa «Regresar», Swing llama a la lambda de la L37, que llama a
<code>irAlMenu()</code> de quien sea la navegación. En el juego completo (capítulo 61), eso cambia la «carta» visible
del mazo al menú. La pantalla de instrucciones no se destruye: queda guardada, lista para la próxima visita.</p>
<div class="caja concepto"><b>HTML en Swing: qué sí y qué no</b> El <code>JLabel</code>, el <code>JButton</code> y los
textos de ayuda (<i>tooltips</i>) entienden un HTML <b>antiguo y pequeño</b> (más o menos HTML 3.2): <code>&lt;b&gt;</code>,
<code>&lt;i&gt;</code>, <code>&lt;u&gt;</code>, <code>&lt;br&gt;</code>, <code>&lt;font color&gt;</code>, listas,
tablas sencillas y un CSS muy básico. No entiende JavaScript, ni CSS moderno, ni sombras. Basta con que el texto
<b>empiece</b> por <code>&lt;html&gt;</code> (sin espacios delante). Es perfecto para resaltar una palabra; para dibujos
elaborados, como el título con halo, se usa <code>Graphics2D</code> (capítulos 41 y 46).</div>

<h2>Compila y prueba</h2>
<p>Esta pantalla todavía no se puede abrir desde el menú: eso lo conecta el <code>PanelPrincipal</code> del capítulo 61.
Para verla ya, usa la <code>VistaPrevia</code> que preparaste en el capítulo 56.</p>
<ol>
<li>En NetBeans, abre <i>herramientas/VistaPrevia.java</i> (si no la ves en <i>Projects</i>, ábrela desde la pestaña
<i>Files</i>, o con <i>File → Open File…</i>).</li>
<li>Busca la línea marcada con <code>// &lt;-- AQUI</code> (es la línea 31) y cambia <code>PantallaMenu</code> por
<code>PantallaInstrucciones</code>. Debe quedar así:
<pre class="java">            JPanel pantalla = new PantallaInstrucciones(sinNavegacion);   // &lt;-- AQUI</pre></li>
<li>Guarda (Ctrl+S) y compila el proyecto: <i>Run → Clean and Build Project</i> (Shift+F11). Abajo, en la ventana
<i>Output</i>, debe aparecer <code>BUILD SUCCESS</code>.</li>
<li>En PowerShell, desde la carpeta del proyecto, lanza la vista previa:
<pre class="ps">cd $HOME\Proyectos\Totito
java -cp target\classes herramientas\VistaPrevia.java</pre></li>
</ol>
<p>Se abre una ventana titulada «Vista previa» con la pantalla «Cómo jugar», igual que esta captura:</p>
<figure><img src="capturas/2-instrucciones.png"><figcaption>La pantalla de instrucciones terminada, vista con la
VistaPrevia. Compárala con el diseño del principio del capítulo.</figcaption></figure>
<p>Comprueba: la X y la O del primer paso salen en rosa y azul; cada paso ocupa dos renglones; el tablero muestra
O X O arriba y una X en el centro; al pasar el ratón sobre el tablero <b>no</b> aparece la manita (es solo de muestra);
«Regresar» se ilumina pero no lleva a ningún sitio (la navegación de la vista previa no hace nada, a propósito); la X
del encabezado cierra la ventana.</p>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Síntoma</th><th>Causa probable</th><th>Solución</th></tr>
<tr><td><code>cannot find symbol: class PasoInstruccion</code> (o <code>Rotulo</code>, <code>Tarjeta</code>…)</td>
<td>Falta un archivo de un capítulo anterior, o lo escribiste con otro nombre.</td>
<td>Revisa que exista <code>src\PasoInstruccion.java</code> y que la clase se llame exactamente así (mayúsculas
incluidas).</td></tr>
<tr><td><code>constructor PantallaBase in class PantallaBase cannot be applied to given types</code></td>
<td>Falta <code>super(navegacion);</code> o no es la primera línea del constructor.</td>
<td>Ponla como primera instrucción.</td></tr>
<tr><td>En el primer paso se ve el texto <code>&lt;font color=…</code> tal cual.</td>
<td>El texto no llegó al <code>JLabel</code> empezando por <code>&lt;html&gt;</code>.</td>
<td>Revisa la L31 de <code>PasoInstruccion</code> (capítulo 53): <code>"&lt;html&gt;" + html + "&lt;/html&gt;"</code>.</td></tr>
<tr><td>Las tildes se ven como <code>CÃ³mo</code>.</td>
<td>El archivo no se guardó o no se compiló en UTF-8.</td>
<td>Revisa <code>project.build.sourceEncoding</code> en el <code>pom.xml</code> (capítulo 5) y, si compilas a mano,
usa <code>javac -encoding UTF-8</code>.</td></tr>
<tr><td>La vista previa sigue mostrando el menú.</td>
<td>No guardaste <code>VistaPrevia.java</code> o no recompilaste.</td>
<td>Guarda, haz <i>Clean and Build</i> y vuelve a lanzarla.</td></tr>
<tr><td><code>error: cannot find symbol … class Navegacion</code> y luego <code>error: compilation failed</code>
al lanzar la vista previa.</td><td>Ejecutaste el comando desde otra carpeta, o sin compilar antes (no existe
<code>target\classes</code>).</td>
<td>Haz <code>cd $HOME\Proyectos\Totito</code>, compila y repite.</td></tr>
</table>

<div class="caja git"><b>Git</b> La vista previa es un banco de pruebas: cambiar su línea <code>AQUI</code> es algo
temporal y no se sube en cada capítulo. Antes del commit, devuélvela a como estaba con <code>git restore</code>
(capítulo 9), que descarta los cambios no guardados en Git de ese archivo. Después sube solo la pantalla nueva.
<pre class="ps">git status
git restore herramientas\VistaPrevia.java
git add src\PantallaInstrucciones.java
git commit -m "PantallaInstrucciones: como jugar"
git push
git log --oneline -3</pre>
<code>git status</code> debe mostrar, antes del commit, <code>PantallaInstrucciones.java</code> como archivo nuevo y
<code>VistaPrevia.java</code> como modificado; después del <code>restore</code>, solo el primero. <code>git push</code> sube el commit a la rama
<code>interfaz-neon</code> de GitHub (la enlazaste con <code>-u</code> en el capítulo 38). Si prefieres seguir
viendo las instrucciones un rato, haz el <code>restore</code> más tarde: lo importante es no mezclar en este commit un
cambio que no forma parte de la pantalla.</div>

<h2>Resumen</h2>
<ul>
<li><code>PantallaInstrucciones</code> hereda de <code>PantallaBase</code> y solo decide qué piezas van y en qué orden:
tarjeta (título, tres pasos, tablero) y botón «Regresar».</li>
<li>Un <code>JLabel</code> cuyo texto empieza por <code>&lt;html&gt;</code> entiende HTML sencillo:
<code>&lt;br&gt;</code> parte renglones y <code>&lt;font color='#RRGGBB'&gt;</code> colorea palabras sueltas.</li>
<li>Dentro de un <code>String</code> de Java, el HTML usa comillas simples para no chocar con las dobles.</li>
<li><code>Tema.hex</code> convierte los colores del tema a texto <code>#RRGGBB</code>: una sola fuente de colores.</li>
<li><code>BoxLayout</code> apila, <code>createRigidArea</code> separa y <code>createEmptyBorder</code> da margen
interior (arriba, izquierda, abajo, derecha).</li>
<li>El tablero de ejemplo usa un <code>Tablero</code> real: reutilizar la lógica garantiza que el ejemplo se vea igual
que el juego.</li>
<li>La lambda del botón recuerda el parámetro <code>navegacion</code> aunque el constructor ya haya terminado.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Mensajes con formato en cualquier programa Swing:</b> en una tienda, <code>new JLabel("&lt;html&gt;Precio:
&lt;s&gt;Q150&lt;/s&gt; &lt;font color='#2F84FF'&gt;&lt;b&gt;Q120&lt;/b&gt;&lt;/font&gt;&lt;/html&gt;")</code> muestra el
precio viejo tachado y el nuevo resaltado; en un formulario, el asterisco rojo de los campos obligatorios.</li>
<li><b>Ayudas de varias líneas:</b> <code>boton.setToolTipText("&lt;html&gt;Guarda el pedido&lt;br&gt;Atajo:
Ctrl+S&lt;/html&gt;")</code>; los <i>tooltips</i> también entienden HTML.</li>
<li><b>Pantallas de ayuda o «primeros pasos»</b> en cualquier aplicación: tarjeta, pasos numerados y un ejemplo.
El esquema de este capítulo se copia tal cual.</li>
<li><b>Ejemplos generados con la lógica real:</b> un programa de ajedrez que enseña una apertura creando un tablero y
moviendo piezas con sus propias reglas; una hoja de cálculo que muestra una fórmula de ejemplo calculándola de verdad.
Si el ejemplo usa la lógica real, nunca se queda desactualizado.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Cambia la palabra «empate» del tercer paso para que salga en lavanda y en cursiva. Pista: crea una variable como
<code>x</code> con <code>Tema.hex(Tema.LAVANDA)</code> y usa <code>&lt;i&gt;</code>.</li>
<li>Agrega un cuarto paso, con círculo cian (<code>Tema.CIAN</code>): «Siempre empieza&lt;br&gt;la X.». ¿Cuántos píxeles
crece la tarjeta? Comprueba tu cuenta con la vista previa.</li>
<li>Cambia el tablero de ejemplo para que la X tenga tres en línea en la columna del centro (agrega una X en (2,1)).
¿Qué aparece sin que escribas una línea de dibujo? Explica por qué, con la L94 de <code>PanelTablero</code>.</li>
<li>Prueba qué pasa si en la L16 cambias las comillas simples por dobles sin escaparlas. Lee el error del compilador.
Luego arréglalo escapándolas con <code>\"</code>.</li>
<li>Reto: haz que el tablero de ejemplo se pueda «jugar» (que muestre la ficha fantasma al pasar el ratón). Pista:
<code>setInteractivo(true)</code> y <code>setFichaFantasma('X')</code>. ¿Por qué en el juego final <b>no</b> conviene
hacerlo?</li>
</ol></div>
""",
}
