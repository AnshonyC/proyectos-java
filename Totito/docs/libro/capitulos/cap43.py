CAPITULO = {
    "numero": 43,
    "titulo": "Tarjeta.java: el panel de cristal",
    "antes": r"""
<p class="entrada">Construyes la primera pieza visible de la interfaz neón: la «tarjeta», una caja redondeada y
semitransparente con borde de luz que envuelve el menú, las instrucciones, los datos de cada jugador y la pantalla de
victoria. Es un archivo cortito, pero en él aparecen tres ideas que vas a usar en todos los componentes que siguen:
dejar espacio para el halo, pintar en capas y ofrecer un «gancho» para que otras clases añadan su propio dibujo.</p>

<h2>Por qué existe este archivo</h2>
<p>Mira el diseño del menú (capítulo 34): los tres botones no flotan sueltos sobre el fondo, están dentro de un
recuadro morado con esquinas redondeadas, un poco más claro que el fondo y con un borde que brilla. Ese mismo recuadro
se repite en la pantalla de instrucciones, en las dos tarjetas de «Jugador 1» y «Jugador 2» y en la ventana de
victoria. Cuando algo se repite cuatro veces, se convierte en una clase: así se dibuja en un solo lugar, se corrige en
un solo lugar y todas las pantallas lo comparten.</p>
<figure><img src="capturas/1-menu.png"><figcaption>La tarjeta morada que envuelve los tres botones del menú es un
objeto <code>Tarjeta</code>.</figcaption></figure>
<p>La palabra «cristal» viene de su aspecto: el relleno es <b>semitransparente</b>, así que deja ver un poco de lo que
hay detrás (las X y O gigantes del fondo), como un vidrio esmerilado. En el capítulo 35 viste que eso se logra con el
canal <b>alfa</b> de un color.</p>
<p>Hay una segunda razón para que esta clase exista: algunas pantallas necesitan una tarjeta <i>casi</i> igual, pero
con algo extra. La pantalla de victoria (capítulo 60) quiere confeti dentro de la tarjeta; la tarjeta de cada jugador
(capítulo 49) quiere un icono, un título y una caja de texto. En lugar de copiar y pegar el código de la tarjeta en
cada sitio, esas clases <b>heredan</b> de <code>Tarjeta</code> (capítulo 22) y solo añaden lo suyo.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>Cómo crear un componente propio <b>heredando de <code>JPanel</code></b> y dibujándolo tú en
<code>paintComponent</code> (repaso práctico de los capítulos 22, 23 y 37).</li>
<li>Qué significa <code>setOpaque(false)</code> y por qué un componente transparente lo necesita.</li>
<li>Por qué cada componente neón deja un <b>margen</b> alrededor de su forma: el halo se dibuja por fuera, y lo que
cae fuera del componente se pierde.</li>
<li>La clase <code>RoundRectangle2D</code> (rectángulo con esquinas redondeadas) y sus seis números.</li>
<li>Dos constructores que se llaman entre sí con <code>this(...)</code>.</li>
<li>La palabra <code>protected</code> y el patrón <b>Template Method</b> (método plantilla) con un método «gancho»
que no hace nada.</li>
<li>Cómo se mezclan dos rellenos semitransparentes, calculado con números reales.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>Comprueba que estás en la rama de la interfaz: en PowerShell, desde <code>$HOME\Proyectos\Totito</code>, escribe
<code>git branch</code>; la rama marcada con <code>*</code> debe ser <code>interfaz-neon</code> (la creaste en el
capítulo 38). Si no, cámbiate con <code>git switch interfaz-neon</code>.</li>
<li>En NetBeans, en el panel <i>Projects</i>, despliega <i>Totito → Source Packages</i>.</li>
<li>Clic derecho en <i>&lt;default package&gt;</i> → <i>New → Java Class…</i></li>
<li>En <i>Class Name</i> escribe <code>Tarjeta</code> (con T mayúscula, exactamente así) y pulsa <i>Finish</i>.</li>
<li>NetBeans abre un archivo con un esqueleto (<code>public class Tarjeta { }</code> y quizá un comentario de
licencia). Bórralo todo con <i>Ctrl+A</i> y <i>Supr</i>, y escribe el código de abajo.</li>
</ol>
<p>Alternativa sin NetBeans, desde PowerShell en la carpeta del proyecto:</p>
<pre class="ps">New-Item -ItemType File src\Tarjeta.java
notepad src\Tarjeta.java</pre>
<div class="caja consejo"><b>Escríbelo tú, no lo pegues</b> Teclear el código obliga a leer cada palabra, y los
errores que cometas al teclear (una llave de menos, un punto y coma olvidado) son exactamente los que necesitas
aprender a reconocer. NetBeans te ayudará subrayando en rojo lo que no entiende.</div>
<div class="caja concepto"><b>Lo que esta clase usa de capítulos anteriores</b> <code>Tarjeta</code> se apoya en dos
clases que ya escribiste: <code>Tema</code> (capítulo 40), que guarda los colores, y <code>Dibujo</code> (capítulo
41), que sabe preparar el pincel y trazar bordes de neón. Si alguna de las dos falta o tiene errores, esta tampoco
compilará.</div>
""",
    "archivos": [
        {"ruta": "src/Tarjeta.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>import java.awt.Color;</code> trae la clase <code>Color</code>, que representa un color
con sus cuatro canales: rojo, verde, azul y alfa (transparencia). La tarjeta guarda el color de su borde en una
variable de este tipo. Recuerda (capítulo 11) que un <code>import</code> no copia código: solo le dice al compilador
«cuando escriba <code>Color</code>, me refiero a <code>java.awt.Color</code>». Sin esta línea, el compilador diría
<i>cannot find symbol: class Color</i>.</p>
<p class="l"><b>L2</b> <code>java.awt.Graphics</code> es el «pincel» básico que Swing le entrega a cada componente
cuando hay que pintarlo. Lo necesitamos porque es el tipo del parámetro de <code>paintComponent</code>.</p>
<p class="l"><b>L3</b> <code>java.awt.Graphics2D</code> es el pincel avanzado: el mismo objeto, pero visto con más
capacidades (formas con decimales, trazos gruesos, degradados, suavizado). En el capítulo 37 viste que Swing siempre
entrega en realidad un <code>Graphics2D</code>; <code>Dibujo.preparar</code> hace la conversión por nosotros.</p>
<p class="l"><b>L4</b> <code>java.awt.geom.RoundRectangle2D</code> es la figura «rectángulo con esquinas redondeadas».
Está en el paquete <code>java.awt.geom</code> (de <i>geometry</i>, geometría), donde viven las figuras de Java2D:
líneas, elipses, rectángulos, curvas.</p>
<p class="l"><b>L5</b> <code>javax.swing.JPanel</code> es el panel de Swing: un contenedor rectangular al que se le
pueden agregar otros componentes. La tarjeta <b>es</b> un panel, así que la necesitamos para heredar de ella. Fíjate en
la <code>x</code> de <code>javax</code>: Swing nació como «extensión» de Java, y su paquete conservó ese nombre.</p>
<p class="l"><b>L6</b> Línea en blanco: separa los imports de la clase. Al compilador no le importa; a quien lee, sí.</p>
"""),
             ("public class Tarjeta", r"""
<p class="l"><b>L7–L14</b> Comentario de documentación (empieza con <code>/**</code>). Explica para qué sirve la
clase y avisa a quien la herede que existe <code>pintarDecoracion()</code>. Los comentarios del código fuente no llevan
tildes a propósito: así el archivo no da problemas aunque alguien lo abra con una codificación distinta de UTF-8.</p>
<p class="l"><b>L15</b> <code>public class Tarjeta extends JPanel {</code> declara la clase. <code>public</code>: la
pueden usar todas las demás clases del proyecto. <code>extends JPanel</code>: <b>hereda</b> de
<code>JPanel</code> (capítulo 22). Eso significa que una <code>Tarjeta</code> ya sabe hacer todo lo que hace un panel
sin que escribamos nada: tener tamaño y posición, contener botones, usar un layout, recibir clics, repintarse. Nosotros
solo cambiamos <i>cómo se ve</i>. La llave <code>{</code> abre el cuerpo de la clase, que se cierra en la línea 56.</p>
<p class="l"><b>L16</b> En blanco, por legibilidad.</p>
"""),
             ("public static final int MARGEN", r"""
<p class="l"><b>L17</b> Comentario de una línea que documenta la constante.</p>
<p class="l"><b>L18</b> <code>public static final int MARGEN = 10;</code> crea una constante (capítulo 20):
<code>static</code> porque pertenece a la clase y no a cada tarjeta (todas usan el mismo margen), <code>final</code>
porque nunca cambia, <code>public</code> porque otras clases la consultan (por ejemplo <code>TarjetaJugador</code>,
para colocar su caja de texto respetando ese margen). Vale 10 píxeles. ¿Por qué 10 y no 0? Porque el borde de neón no
es una línea fina: <code>Dibujo.trazoNeon</code> (capítulo 41) lo dibuja seis veces más, cada vez más gruesa y más
transparente. Con el grosor de 1.8 que usa la tarjeta, la capa más ancha mide 1.8 + 6 × 2.4 = 16.2 píxeles, y como un
trazo se reparte a partes iguales a cada lado de la línea, sobresale 8.1 píxeles <b>hacia afuera</b>. Swing no deja
pintar fuera del rectángulo del componente: si la caja empezara en el píxel 0, la mitad exterior del halo se
recortaría y el brillo se vería «cortado a cuchillo». Con 10 píxeles de margen cabe entero y sobran casi 2.</p>
<p class="l"><b>L19</b> En blanco.</p>
"""),
             ("private final Color color;", r"""
<p class="l"><b>L20</b> <code>private final Color color;</code> es un <b>atributo</b>: cada tarjeta guarda su propio
color de borde (morado en el menú, fresa o azul en las tarjetas de jugador). <code>private</code>: solo esta clase lo
toca (encapsulamiento, capítulo 19). <code>final</code>: se asigna una vez en el constructor y ya no cambia; si por
error intentaras cambiarlo después, el compilador te detendría.</p>
<p class="l"><b>L21</b> <code>private final int arco;</code> guarda cuánto se redondean las esquinas, en píxeles.
Es un <code>int</code> (número entero) porque nadie necesita medio píxel de redondeo.</p>
<p class="l"><b>L22</b> En blanco.</p>
"""),
             ("public Tarjeta(Color color) {", r"""
<p class="l"><b>L23</b> Primer <b>constructor</b> (capítulo 20): el que se usa cuando solo se indica el color, por
ejemplo <code>new Tarjeta(Tema.MORADO)</code> en el menú. Un constructor se llama igual que la clase y no tiene tipo
de retorno.</p>
<p class="l"><b>L24</b> <code>this(color, 30);</code> no crea otra tarjeta: llama <b>al otro constructor</b> de esta
misma clase (el de la línea 27), pasándole el color recibido y un arco de 30 píxeles. Es la forma de decir «si no me
dices el redondeo, usa 30». Así la lógica de inicializar está escrita una sola vez. Regla de Java: la llamada
<code>this(...)</code> tiene que ser la primera instrucción del constructor.</p>
<p class="l"><b>L25–L26</b> Cierra el constructor y deja una línea en blanco.</p>
"""),
             ("public Tarjeta(Color color, int arco)", r"""
<p class="l"><b>L27</b> Segundo constructor, el completo: recibe el color y el arco. Lo usa directamente
<code>TarjetaJugador</code> (capítulo 49), que quiere esquinas un poco menos redondas: <code>super(color, 26)</code>.
Tener dos constructores con el mismo nombre y distintos parámetros es <b>sobrecarga</b> (capítulo 16).</p>
<p class="l"><b>L28</b> <code>this.color = color;</code> guarda el parámetro en el atributo. Hay dos cosas llamadas
<code>color</code>: el parámetro (que vive solo mientras corre el constructor) y el atributo (que vive tanto como la
tarjeta). <code>this.color</code> significa «el atributo de este objeto»; <code>color</code> a secas es el parámetro,
porque el nombre más cercano gana.</p>
<p class="l"><b>L29</b> Lo mismo con el arco.</p>
<p class="l"><b>L30</b> <code>setOpaque(false);</code> es la línea más importante del constructor. Un componente
<b>opaco</b> promete a Swing: «yo pinto cada píxel de mi rectángulo, no hace falta pintar lo que hay detrás». Un
<code>JPanel</code> es opaco por defecto y rellena su fondo de gris. Nuestra tarjeta tiene esquinas redondeadas (las
puntas del rectángulo quedan sin pintar), un margen vacío y un relleno semitransparente: <b>no</b> cubre todo. Con
<code>false</code> le decimos la verdad a Swing, y entonces Swing pinta primero el fondo de la pantalla y después la
tarjeta encima. Sin esta línea verías un rectángulo gris (o manchas de basura gráfica) en las esquinas y en el
margen.</p>
<p class="l"><b>L31</b> <code>setAlignmentX(CENTER_ALIGNMENT);</code> pide que, si la tarjeta está dentro de un
<code>BoxLayout</code> vertical (capítulo 37), quede centrada horizontalmente. <code>CENTER_ALIGNMENT</code> es una
constante (vale <code>0.5f</code>: «a la mitad») que <code>Tarjeta</code> heredó de <code>Component</code>, el
antepasado de todos los componentes; por eso se escribe sin prefijo.</p>
<p class="l"><b>L32–L33</b> Cierra el constructor y una línea en blanco.</p>
"""),
             ("protected RoundRectangle2D forma()", r"""
<p class="l"><b>L34</b> Comentario: este método da la caja ya descontando el margen del halo.</p>
<p class="l"><b>L35</b> <code>protected RoundRectangle2D forma() {</code> declara un método que <b>devuelve</b> la
figura de la tarjeta. <code>protected</code> es un nivel de acceso intermedio: lo pueden usar esta clase y sus
<b>subclases</b> (las que heredan de ella), pero no cualquier clase. Se eligió porque a las hijas les interesa (por
ejemplo, para saber dónde cae el borde), pero al resto del programa no. Se hizo un método aparte, y no una línea dentro
de <code>paintComponent</code>, para que la forma se calcule en un solo lugar.</p>
<p class="l"><b>L36–L37</b> <code>return new RoundRectangle2D.Double(MARGEN, MARGEN, getWidth() - 2.0 * MARGEN,
getHeight() - 2.0 * MARGEN, arco, arco);</code> crea y devuelve la figura. <code>RoundRectangle2D.Double</code> es la
versión de la figura que guarda sus medidas en <code>double</code> (con decimales); existe también
<code>.Float</code>. Sus seis números son: <b>x</b> e <b>y</b> de la esquina superior izquierda (10, 10: dejamos el
margen), <b>ancho</b> y <b>alto</b> (el tamaño del componente menos un margen a cada lado, por eso
<code>2.0 *</code>), y el <b>ancho y alto del arco</b> de las esquinas. Ojo: el arco es el <i>diámetro</i> de la
curva; con 30 la esquina se redondea con un radio de 15 píxeles. <code>getWidth()</code> y <code>getHeight()</code>
son métodos heredados de <code>JPanel</code> que dan el tamaño actual del componente. Se escribe <code>2.0</code> y
no <code>2</code> para que la cuenta se haga con decimales (capítulo 12). La instrucción ocupa dos líneas solo para no
salirse del ancho de la pantalla: para Java termina en el <code>;</code>.</p>
<p class="l"><b>L38–L39</b> Cierra el método; línea en blanco.</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L40</b> <code>@Override</code> es una <b>anotación</b>: le avisa al compilador «el método de abajo
reemplaza a uno que heredé». Si escribieras mal el nombre (<code>paintComponet</code>), sin la anotación tendrías un
método nuevo que nadie llama, y la tarjeta saldría invisible sin ningún error; con ella, el compilador protesta.</p>
<p class="l"><b>L41</b> <code>protected void paintComponent(Graphics g) {</code> es el método que Swing llama cada
vez que hay que dibujar la tarjeta: cuando aparece la ventana, cuando cambia de tamaño, cuando algo pide
<code>repaint()</code>. Nosotros nunca lo llamamos directamente (capítulo 37). Recibe <code>g</code>, el pincel ya
colocado de modo que (0, 0) es la esquina superior izquierda de la tarjeta. Es <code>protected</code> porque así está
declarado en <code>JComponent</code>; al sobrescribir no se puede restringir más el acceso. Fíjate en que <b>no</b>
llamamos a <code>super.paintComponent(g)</code>: lo único que haría es rellenar el fondo gris, y no lo queremos.</p>
<p class="l"><b>L42</b> <code>Graphics2D g2 = Dibujo.preparar(g);</code> pide a <code>Dibujo</code> (capítulo 41)
una <b>copia</b> del pincel, convertida a <code>Graphics2D</code> y con el suavizado (antialiasing) activado. Pintamos
siempre con la copia, nunca con <code>g</code>, para no dejarle cambios (color, grosor) al siguiente componente que
Swing pinte con ese mismo pincel.</p>
<p class="l"><b>L43</b> <code>RoundRectangle2D forma = forma();</code> pide la figura y la guarda en una variable
local. Que la variable y el método se llamen igual no es problema: Java distingue el método por los paréntesis. Se
guarda en una variable porque se usa cuatro veces y así se calcula una sola vez.</p>
"""),
             ("g2.setColor(Tema.SUPERFICIE);", r"""
<p class="l"><b>L44</b> <code>g2.setColor(Tema.SUPERFICIE);</code> moja el pincel en el color de superficie de la
paleta: un morado oscuro (<code>#2B2363</code>) con alfa 125 de 255, o sea, aproximadamente un 49 % opaco. Ese es el
«cristal».</p>
<p class="l"><b>L45</b> <code>g2.fill(forma);</code> rellena la figura con ese color. <code>fill</code> pinta el
interior; <code>draw</code> pintaría solo el contorno.</p>
<p class="l"><b>L46</b> <code>g2.setColor(Tema.conAlfa(color, 12));</code> toma el color propio de la tarjeta (por
ejemplo, el morado de los bordes) con alfa 12: casi invisible, un 5 %. <code>Tema.conAlfa</code> (capítulo 40) devuelve
el mismo color con otra transparencia.</p>
<p class="l"><b>L47</b> Rellena la misma figura <b>otra vez</b>, encima. Esta segunda capa es un «tinte»: hace que la
tarjeta fresa del Jugador 1 se vea levemente rosada y la del Jugador 2 levemente azulada, aunque las dos usen la misma
superficie. Más abajo, en «Cómo funciona por dentro», está la cuenta exacta de cómo se mezclan las dos capas.</p>
"""),
             ("pintarDecoracion(g2, forma);", r"""
<p class="l"><b>L48</b> <code>pintarDecoracion(g2, forma);</code> llama al método «gancho» de la línea 54. En esta
clase no hace nada, pero una subclase puede reemplazarlo para dibujar algo <b>después del relleno y antes del
borde</b>. El orden importa: en Swing lo que se pinta después queda encima. El confeti de la pantalla de victoria se
pinta aquí, así que queda sobre el cristal y debajo del brillo del borde.</p>
<p class="l"><b>L49</b> <code>Dibujo.trazoNeon(g2, forma, color, 1.8f);</code> traza el borde de neón alrededor de la
figura: seis capas de halo y la línea principal de 1.8 píxeles (capítulo 41). La <code>f</code> de <code>1.8f</code>
indica que el número es <code>float</code>, el tipo que pide el método; sin ella Java lo tomaría como
<code>double</code> y daría error de tipos.</p>
<p class="l"><b>L50</b> <code>g2.dispose();</code> libera la copia del pincel que pedimos en la línea 42. Quien crea
una copia con <code>create()</code> debe liberarla; si no, el programa acumula recursos gráficos sin usar. Nota que se
libera <code>g2</code>, nunca <code>g</code>: ese es de Swing.</p>
<p class="l"><b>L51–L52</b> Cierra <code>paintComponent</code>; línea en blanco.</p>
<p class="l">¿Y los botones que van dentro de la tarjeta? No los pintamos nosotros. Después de
<code>paintComponent</code>, Swing llama a <code>paintChildren</code>, que pinta a los hijos encima. Por eso el
borde de la tarjeta nunca tapa los botones.</p>
"""),
             ("protected void pintarDecoracion", r"""
<p class="l"><b>L53</b> Comentario: es un gancho para subclases y por defecto no dibuja nada.</p>
<p class="l"><b>L54</b> <code>protected void pintarDecoracion(Graphics2D g2, RoundRectangle2D forma) {</code> declara
el gancho. Recibe el pincel ya preparado y la figura, para que la subclase sepa dónde dibujar. Es
<code>protected</code> porque está pensado para que lo sobrescriban las hijas, no para que lo llame cualquiera.</p>
<p class="l"><b>L55</b> <code>}</code> El cuerpo está vacío a propósito: un método que no hace nada es perfectamente
válido. Si una subclase no lo sobrescribe, la tarjeta se ve normal.</p>
<p class="l"><b>L56</b> Cierra la clase.</p>
<div class="caja concepto"><b>Template Method (método plantilla)</b> <code>paintComponent</code> fija una
<i>plantilla</i> de pasos que nadie puede desordenar: superficie, tinte, <b>decoración</b>, borde. Las subclases solo
rellenan el hueco que se les dejó. Es el patrón Template Method del capítulo 27. La ventaja: <code>TarjetaConConfeti</code>
(capítulo 60) no tiene que saber nada de superficies ni de neón, y si un día cambias el borde de todas las tarjetas,
lo cambias aquí y el confeti sigue funcionando.</div>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<p>Sigamos a la tarjeta del menú principal desde que se crea hasta que aparece. En el capítulo 56,
<code>PantallaMenu</code> hará <code>new Tarjeta(Tema.MORADO)</code>, le pondrá un borde interior de 34 píxeles arriba
y abajo y 28 a los lados, y le meterá tres botones de 384 × 88 separados por 14 píxeles. El <code>BoxLayout</code>
sumará: ancho 28 + 384 + 28 = <b>440</b>; alto 34 + 88 + 14 + 88 + 14 + 88 + 34 = <b>360</b>.</p>
<ol>
<li><code>new Tarjeta(Tema.MORADO)</code> entra al constructor de la línea 23, que llama a
<code>this(Tema.MORADO, 30)</code>. Se guardan <code>color</code> = morado <code>#A05CFF</code> y <code>arco</code> =
30, y la tarjeta se declara transparente.</li>
<li>Cuando la ventana se muestra, Swing llama a <code>paintComponent</code>. <code>forma()</code> devuelve un
rectángulo redondeado en <b>x = 10, y = 10</b>, de <b>420 × 340</b> (440 − 20 y 360 − 20), con esquinas de radio
15.</li>
<li>Supongamos que el fondo detrás de un punto del centro es <code>#1C1740</code>, o sea (28, 23, 64). Al rellenar
con la superficie (43, 35, 99) con alfa 125, cada canal queda en «el 49 % del color nuevo más el 51 % del que había»:
rojo = 43 × 0.49 + 28 × 0.51 ≈ 35; verde ≈ 29; azul = 99 × 0.49 + 64 × 0.51 ≈ 81. Resultado: (35, 29, 81).</li>
<li>Encima, el tinte morado (160, 92, 255) con alfa 12, un 4.7 %: rojo = 160 × 0.047 + 35 × 0.953 ≈ 41; verde ≈ 32;
azul = 255 × 0.047 + 81 × 0.953 ≈ 89. El centro de la tarjeta queda en (41, 32, 89): un violeta oscuro, un poco más
claro y más morado que el fondo. Lo comprobé pintando la tarjeta en una imagen y leyendo ese píxel: (41, 32, 90). La
diferencia de 1 es redondeo.</li>
<li><code>pintarDecoracion</code> no hace nada.</li>
<li><code>trazoNeon</code> dibuja el borde: la capa más ancha mide 16.2 píxeles y llega hasta 8.1 píxeles por fuera de
la figura, es decir, hasta el píxel 10 − 8.1 ≈ 2 del componente. Los píxeles 0 y 1 quedan libres.</li>
<li>Swing pinta los tres botones encima (<code>paintChildren</code>).</li>
</ol>
<p>Ahora imagina que hubieras puesto <code>MARGEN = 0</code>. La figura empezaría en el píxel 0, y la mitad exterior
del halo (8 píxeles) caería fuera del componente, donde Swing no deja pintar. El borde se vería como una línea dura,
sin brillo hacia afuera. Hice la prueba: con margen 10, el píxel 3 desde el borde izquierdo tiene color (36, 27, 75),
un resplandor tenue; sin margen, ese resplandor sencillamente no existe.</p>
<table class="tabla">
<tr><th>Medida</th><th>Valor en la tarjeta del menú</th><th>De dónde sale</th></tr>
<tr><td>Tamaño del componente</td><td>440 × 360</td><td>lo calcula el <code>BoxLayout</code> con los botones</td></tr>
<tr><td>Caja de cristal</td><td>420 × 340, en (10, 10)</td><td><code>forma()</code>: tamaño − 2 × MARGEN</td></tr>
<tr><td>Radio de las esquinas</td><td>15 px</td><td>arco 30 ÷ 2</td></tr>
<tr><td>Halo hacia afuera</td><td>8.1 px</td><td>(1.8 + 6 × 2.4) ÷ 2</td></tr>
</table>

<h2>Compila y prueba</h2>
<p>Todavía no hay ninguna pantalla que use la tarjeta: la primera ventana con el diseño neón aparece en el capítulo 56,
con la <code>VistaPrevia</code>. Lo que sí puedes (y debes) comprobar ahora es que el archivo compila:</p>
<ol>
<li>En NetBeans, <i>Run → Clean and Build Project</i> (Shift+F11). En la ventana <i>Output</i> debe aparecer
<code>BUILD SUCCESS</code>.</li>
<li>Comprueba que se generó el archivo compilado:</li>
</ol>
<pre class="ps">Get-ChildItem target\classes\Tarjeta*.class</pre>
<pre class="salida">    Directorio: C:\Users\tu-usuario\Proyectos\Totito\target\classes

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        12/10/2026     10:15           1564 Tarjeta.class</pre>
<p>(La fecha y el tamaño exacto pueden variar.) Si prefieres no usar NetBeans: <code>javac -encoding UTF-8 -d out
src\*.java</code> debe terminar sin mensajes.</p>
<h3>Opcional: una foto de tu componente</h3>
<p>Si no aguantas la curiosidad, hay un truco para ver la tarjeta sin tener todavía una ventana: pedirle al
componente que se pinte dentro de una imagen y guardarla como PNG. Lo haremos en un archivo <b>fuera</b> del proyecto,
para no subirlo a Git por accidente. Desde la carpeta Totito:</p>
<pre class="ps">New-Item -ItemType Directory -Force ..\pruebas-totito | Out-Null
notepad ..\pruebas-totito\FotoComponente.java</pre>
<p>Bloc de notas preguntará si quieres crear el archivo: di que sí y escribe esto:</p>
<pre class="java">import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.JComponent;

public class FotoComponente {
    public static void main(String[] args) throws Exception {
        JComponent pieza = new Tarjeta(Tema.MORADO);
        int ancho = 440, alto = 360;

        pieza.setSize(ancho, alto);
        pieza.doLayout();
        BufferedImage foto = new BufferedImage(ancho, alto, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = foto.createGraphics();
        g.setColor(Tema.FONDO_ARRIBA);
        g.fillRect(0, 0, ancho, alto);
        pieza.paint(g);
        g.dispose();
        ImageIO.write(foto, "png", new File("../pruebas-totito/foto.png"));
        System.out.println("Listo: " + new File("../pruebas-totito/foto.png").getCanonicalPath());
    }
}</pre>
<p>Qué hace, en pocas palabras: crea el componente (<code>pieza</code>), le da un tamaño a mano con
<code>setSize</code> (normalmente lo haría el layout de la pantalla), le pide que coloque a sus hijos con
<code>doLayout</code>, crea una imagen en memoria del mismo tamaño (<code>BufferedImage</code>, del paquete
<code>java.awt.image</code>), toma el pincel de esa imagen, la pinta del color de fondo del Totito, le dice al
componente «píntate aquí» con <code>paint(g)</code> (que a su vez llama a <code>paintComponent</code> y a
<code>paintChildren</code>) y guarda la imagen con <code>ImageIO.write</code>. El <code>throws Exception</code> es
porque escribir un archivo puede fallar (capítulo 26). Java acepta la barra <code>/</code> en las rutas también en
Windows. Ejecútalo, después de haber compilado con Clean and Build, y abre la foto:</p>
<pre class="ps">java -cp target\classes ..\pruebas-totito\FotoComponente.java
Invoke-Item ..\pruebas-totito\foto.png</pre>
<pre class="salida">Listo: C:\Users\tu-usuario\Proyectos\pruebas-totito\foto.png</pre>
<p><code>Invoke-Item</code> abre el archivo con el programa que Windows tenga asociado a los PNG (normalmente
Fotos). Verás un rectángulo violeta con esquinas redondeadas y un borde morado que brilla hacia afuera. En los capítulos
siguientes solo tendrás que cambiar las dos líneas de <code>pieza</code> y del tamaño para fotografiar cada
componente nuevo.</p>
<div class="caja consejo"><b>Por qué funciona ese <code>java</code> con un .java</b> Desde Java 11, <code>java</code>
puede ejecutar directamente un archivo fuente de una sola clase: lo compila en memoria y lo corre. Con <code>-cp
target\classes</code> le dices dónde están las clases del Totito ya compiladas (<code>Tarjeta</code>, <code>Tema</code>,
<code>Dibujo</code>). Es el mismo truco que usará <code>VistaPrevia</code> en el capítulo 56.</div>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Mensaje</th><th>Causa probable</th><th>Solución</th></tr>
<tr><td><code>cannot find symbol: variable Dibujo</code> o <code>Tema</code></td><td>Falta <code>Dibujo.java</code> o
<code>Tema.java</code>, o tienen errores</td><td>Repasa los capítulos 40 y 41; compila hasta que ellos estén
bien</td></tr>
<tr><td><code>class Tarjeta is public, should be declared in a file named Tarjeta.java</code></td><td>El archivo se
llama distinto (por ejemplo <code>tarjeta.java</code>)</td><td>Renómbralo: el nombre del archivo y el de la clase deben
ser idénticos, mayúsculas incluidas</td></tr>
<tr><td><code>method does not override or implement a method from a supertype</code></td><td>Escribiste mal
<code>paintComponent</code> o sus parámetros</td><td>Compara letra por letra con la línea 41</td></tr>
<tr><td><code>incompatible types: possible lossy conversion from double to float</code></td><td>Olvidaste la
<code>f</code> en <code>1.8f</code></td><td>Agrégala</td></tr>
<tr><td>(en la foto) esquinas grises</td><td>Falta <code>setOpaque(false)</code></td><td>Revisa la línea 30</td></tr>
</table>

<div class="caja git"><b>Git</b> Un componente terminado y compilando es un buen momento para un commit. Desde la
carpeta Totito, en la rama <code>interfaz-neon</code>:
<pre class="ps">git switch interfaz-neon
git status
git add src\Tarjeta.java
git commit -m "Tarjeta: panel de cristal"
git push</pre>
<code>git status</code> debe mostrar <code>src/Tarjeta.java</code> como archivo nuevo (y nada de
<code>pruebas-totito</code>, que está fuera del proyecto). Si <code>git push</code> te dice que la rama no tiene
«upstream», es que en el capítulo 38 no la publicaste: usa una vez <code>git push -u origin interfaz-neon</code>.</div>

<h2>Resumen</h2>
<ul>
<li><code>Tarjeta</code> hereda de <code>JPanel</code>: contiene componentes como cualquier panel, pero se dibuja a
mano en <code>paintComponent</code>.</li>
<li><code>setOpaque(false)</code> avisa a Swing de que el componente no cubre todo su rectángulo; sin él aparecen
esquinas grises.</li>
<li>Los componentes con neón dejan un <code>MARGEN</code> vacío alrededor de su figura porque el halo se dibuja hacia
afuera (8.1 px en la tarjeta) y lo que sale del componente se recorta.</li>
<li><code>RoundRectangle2D.Double(x, y, ancho, alto, arcoAncho, arcoAlto)</code>: el arco es el diámetro de la
esquina.</li>
<li>Las capas se pintan de abajo hacia arriba: superficie, tinte, decoración, borde; después Swing pinta a los
hijos.</li>
<li><code>this(...)</code> encadena constructores; <code>protected</code> abre un método solo a las subclases.</li>
<li><code>pintarDecoracion</code> es un gancho vacío: el patrón Template Method permite a las subclases añadir dibujo
sin tocar la plantilla.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Tarjetas de un panel de control</b>: en una aplicación de ventas, cada indicador («Ventas de hoy», «Clientes
nuevos») puede ser una subclase de una tarjeta común que dibuja fondo, sombra y borde; cada hija solo pinta su número
en su gancho.</li>
<li><b>Cualquier efecto que sobresale</b> (sombras, resplandores, insignias que asoman por la esquina) necesita un
margen interno en el componente, igual que el halo. Si alguna vez ves una sombra «cortada», es esto.</li>
<li><b>Template Method en otros lugares</b>: un generador de reportes con los pasos fijos encabezado → cuerpo → pie,
donde cada tipo de reporte solo sobrescribe <code>cuerpo()</code>; o un juego con un ciclo fijo leer teclado →
actualizar → dibujar, donde cada nivel solo cambia <code>actualizar()</code>.</li>
<li><b>Paneles translúcidos</b> sobre una imagen o un mapa (la leyenda de un mapa, una ventana de ayuda flotante) se
hacen igual: no opacos y con un color de alfa bajo.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Cambia en la foto opcional <code>new Tarjeta(Tema.MORADO)</code> por <code>new Tarjeta(Tema.AZUL, 60)</code>.
¿Qué cambió y por qué? Pista: mira las líneas 27 y 37.</li>
<li>Calcula, sin ejecutar nada, qué figura devuelve <code>forma()</code> para una tarjeta de 290 × 150 (el tamaño de
<code>TarjetaJugador</code>). Pista: tamaño menos 2 × 10.</li>
<li>En una copia de la foto, crea una subclase anónima que sobrescriba el gancho:
<code>new Tarjeta(Tema.ROSA) { @Override protected void pintarDecoracion(java.awt.Graphics2D g2,
java.awt.geom.RoundRectangle2D f) { g2.setColor(Tema.ROSA); g2.fillOval(200, 160, 40, 40); } }</code>. Fotografíala:
¿el círculo queda encima o debajo del borde? ¿Por qué?</li>
<li>Comenta temporalmente <code>setOpaque(false)</code> (con <code>//</code> al principio), compila y vuelve a sacar la
foto. Describe lo que ves en las esquinas y explica el motivo. Después quita el comentario.</li>
<li>Reto: ¿qué <code>MARGEN</code> mínimo haría falta si el borde se trazara con grosor 4 en lugar de 1.8? Pista: la
capa más ancha es grosor + 6 × 2.4, y sobresale la mitad.</li>
</ol></div>
""",
}
