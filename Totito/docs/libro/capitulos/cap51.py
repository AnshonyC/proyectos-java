# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 51,
    "titulo": "OpcionModo.java: una opción que avisa pero no decide",
    "antes": r"""
<p class="entrada">Bajo «MODO DE JUEGO» hay dos opciones: «2 jugadores» y «Contra la IA». Cada una es una tarjetita
con un botón de radio, un icono, un título y una descripción. En este capítulo la construyes y aprendes una idea
que vas a usar toda tu vida de programador: el componente <b>avisa</b> que lo pulsaron con un
<code>Runnable</code>, y es la pantalla la que <b>decide</b> qué hacer.</p>

<h2>Por qué existe este archivo</h2>
<p>El diseño original (<code>diseno/configuracion.jpg</code>) solo traía el modo «2 jugadores». Pero el proyecto ya
tenía una IA invencible desde el capítulo 31 y sería una pena perderla, así que en la pantalla de configuración
agregamos una segunda opción, «Contra la IA», con el mismo estilo. Como las dos opciones son iguales salvo por sus
datos (icono, título, descripción), se hace una clase y se crean dos objetos.</p>
<p>El problema interesante es el del <b>grupo</b>: si pulsas «Contra la IA», debe marcarse esa y
<b>desmarcarse</b> la otra. Una opción sola no puede saberlo, porque no conoce a su compañera. Por eso
<code>OpcionModo</code> no se marca a sí misma: al recibir el clic solo dice «me pulsaron» y la pantalla, que
conoce a las dos, marca una y desmarca la otra.</p>
<figure><img src="capturas/3-configuracion.png"><figcaption>Abajo, bajo «MODO DE JUEGO», las dos OpcionModo: «2
jugadores» marcada (aro rosa con punto, borde brillante) y «Contra la IA» sin marcar.</figcaption></figure>

<h2>Qué vas a aprender</h2>
<ul>
<li>Qué es un <b>callback</b> (una «llamada de vuelta»): darle a un objeto un trozo de código para que lo ejecute
cuando ocurra algo.</li>
<li>La interfaz <code>Runnable</code> y su método <code>run()</code>, y cómo una lambda se convierte en un
<code>Runnable</code>.</li>
<li>Por qué se comprueba <code>!= null</code> antes de usar algo opcional.</li>
<li>A separar <b>quién detecta</b> un evento de <b>quién decide</b> qué hacer con él.</li>
<li>A dibujar un componente con dos aspectos (marcado y sin marcar) usando el operador ternario.</li>
</ul>

<h2>El plano de una opción, en píxeles</h2>
<p>Cada opción mide <b>290 × 72</b>. Deja un margen de 7 píxeles para el halo.</p>
<table class="tabla">
<tr><th>Parte</th><th>Posición</th><th>Marcada</th><th>Sin marcar</th></tr>
<tr><td>Caja redondeada</td><td>(7, 7) de 276 × 58, esquinas 22</td><td>relleno morado alfa 38, borde brillante</td><td>relleno alfa 12, borde tenue</td></tr>
<tr><td>Aro del radio</td><td>círculo de 20 con centro (33, 36)</td><td>neón rosa con punto de 10</td><td>aro lavanda simple</td></tr>
<tr><td>Icono</td><td>cuadrado de 34 en (55, 19)</td><td>lavanda</td><td>lavanda apagado</td></tr>
<tr><td>Título</td><td>x = 99, línea base 33</td><td>blanco, negrita 16</td><td>lavanda apagado</td></tr>
<tr><td>Descripción</td><td>x = 99, línea base 51</td><td colspan="2">lavanda apagado, 12 puntos</td></tr>
</table>

<h2>Créalo</h2>
<ol>
<li>NetBeans: clic derecho en <i>&lt;default package&gt;</i> → <i>New → Java Class…</i> → <code>OpcionModo</code>
→ <i>Finish</i>.</li>
<li>Borra la plantilla y escribe el código.</li>
</ol>
<p>Alternativa: <code>New-Item src\OpcionModo.java</code>.</p>
""",
    "archivos": [
        {"ruta": "src/OpcionModo.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.Cursor</code>: para poner la manito al pasar el ratón (como en el
selector del capítulo 50).</p>
<p class="l"><b>L2</b> <code>java.awt.Font</code>: por <code>Font.BOLD</code> y <code>Font.PLAIN</code>.</p>
<p class="l"><b>L3–L4</b> <code>Graphics</code> y <code>Graphics2D</code>: el pincel de
<code>paintComponent</code> y su versión ampliada.</p>
"""),
             ("import java.awt.event.MouseAdapter", r"""
<p class="l"><b>L5–L6</b> <code>MouseAdapter</code> y <code>MouseEvent</code>: para escuchar el clic (capítulo
50).</p>
<p class="l"><b>L7</b> <code>java.awt.geom.Ellipse2D</code>: los círculos del botón de radio.</p>
<p class="l"><b>L8</b> <code>java.awt.geom.RoundRectangle2D</code>: la caja redondeada.</p>
<p class="l"><b>L9</b> <code>javax.swing.JComponent</code>: la clase base; la opción solo dibuja, no contiene
hijos.</p>
<p>¿Y <code>Runnable</code>? No se importa: está en el paquete <code>java.lang</code>, que Java importa solo en
todos los archivos (igual que <code>String</code>, <code>Math</code> o <code>System</code>).</p>
"""),
             ("public class OpcionModo", r"""
<p class="l"><b>L11–L15</b> Comentario de la clase. La última frase es la clave del diseño: «La pantalla que la
usa decide cuál queda marcada: al hacer clic solo se avisa con el Runnable».</p>
<p class="l"><b>L16</b> <code>public class OpcionModo extends JComponent {</code> hereda de
<code>JComponent</code>: transparente, sin fondo propio, lienzo libre.</p>
"""),
             ("public static final int ANCHO", r"""
<p class="l"><b>L18</b> <code>ANCHO = 290</code>: igual que una <code>TarjetaJugador</code>, para que las dos
filas de la pantalla de configuración tengan el mismo ancho visual.</p>
<p class="l"><b>L19</b> <code>ALTO = 72</code>: bastante más bajita, solo una línea de contenido.</p>
<p class="l"><b>L20</b> <code>private static final int MARGEN = 7;</code> espacio para el halo. Es otra constante
distinta de <code>Tarjeta.MARGEN</code> (10): <code>OpcionModo</code> no hereda de <code>Tarjeta</code> y su borde
es más fino, así que le basta menos. Cada clase puede tener su propio <code>MARGEN</code> privado sin chocar.</p>
"""),
             ("private final Iconos.Icono icono;", r"""
<p class="l"><b>L22</b> <code>private final Iconos.Icono icono;</code> el icono de la opción (personas o chip,
capítulo 42).</p>
<p class="l"><b>L23–L24</b> El título («2 jugadores») y la descripción («Turnos en el mismo equipo»).</p>
<p class="l"><b>L25</b> <code>private boolean seleccionada;</code> si está marcada. Empieza en <code>false</code>
(valor por defecto de un campo <code>boolean</code>).</p>
<p class="l"><b>L26</b> <code>private Runnable alSeleccionar;</code> el <b>callback</b>: el trozo de código que hay
que ejecutar cuando pulsen la opción. <code>Runnable</code> es la interfaz más simple de Java: un solo método,
<code>void run()</code>, sin parámetros ni resultado. Una variable de tipo <code>Runnable</code> guarda «algo que se
puede ejecutar». Empieza en <code>null</code> (nadie ha dicho todavía qué hacer). El nombre se lee como una frase:
«al seleccionar, ejecuta esto».</p>
"""),
             ("public OpcionModo(", r"""
<p class="l"><b>L28</b> <code>public OpcionModo(Iconos.Icono icono, String titulo, String descripcion) {</code> el
constructor recibe los tres datos que diferencian una opción de otra. El <code>Runnable</code> no va aquí: se pone
después con <code>setAlSeleccionar</code>, porque la acción suele referirse a cosas de la pantalla que quizá aún
no existen en el momento de crear la opción.</p>
<p class="l"><b>L29–L31</b> Guardan los parámetros en los campos (<code>this.</code> distingue el campo del
parámetro, capítulo 20).</p>
<p class="l"><b>L32</b> Tamaño fijo de 290 × 72 (capítulo 41).</p>
<p class="l"><b>L33</b> La manito como cursor: se puede pulsar.</p>
"""),
             ("addMouseListener", r"""
<p class="l"><b>L34</b> <code>addMouseListener(new MouseAdapter() {</code> un oyente del ratón como clase anónima
(capítulo 50).</p>
<p class="l"><b>L35–L36</b> <code>mousePressed</code>: se ejecuta en cuanto se hunde el botón. Aquí no hace falta
<i>hit testing</i>: cualquier punto de la opción cuenta.</p>
<p class="l"><b>L37</b> <code>if (alSeleccionar != null) {</code> comprueba que alguien haya configurado la acción.
<code>!=</code> significa «distinto de». Sin esta comprobación, si nadie llamó a <code>setAlSeleccionar</code>,
la línea siguiente intentaría ejecutar <code>run()</code> sobre <code>null</code> y el programa lanzaría un
<code>NullPointerException</code> en cada clic. Así, una opción sin acción simplemente no hace nada.</p>
<p class="l"><b>L38</b> <code>alSeleccionar.run();</code> ejecuta el callback. Fíjate en lo que <b>no</b> hace:
no llama a <code>setSeleccionada(true)</code>. La opción solo avisa; marcarla es cosa de la pantalla.</p>
<p class="l"><b>L39–L43</b> Cierran el <code>if</code>, el método, la clase anónima, la llamada
(<code>});</code>) y el constructor.</p>
"""),
             ("public void setAlSeleccionar", r"""
<p class="l"><b>L44</b> <code>public void setAlSeleccionar(Runnable accion) {</code> recibe la acción. Quien lo
llama suele pasar una <b>lambda</b> (capítulo 25). En la pantalla de configuración (capítulo 58) se verá así:
<code>opcionContraIA.setAlSeleccionar(() -&gt; elegirModo(Partida.Modo.CONTRA_IA));</code>. La lambda
<code>() -&gt; ...</code> no recibe nada y hace una cosa: encaja exactamente con <code>run()</code>, así que Java la
convierte en un <code>Runnable</code>.</p>
<p class="l"><b>L45</b> La guarda en el campo, para ejecutarla en el futuro, cuando llegue el clic.</p>
<p class="l"><b>L48</b> <code>public void setSeleccionada(boolean seleccionada) {</code> marca o desmarca la
opción. Lo llama la pantalla.</p>
<p class="l"><b>L49</b> Guarda el nuevo estado.</p>
<p class="l"><b>L50</b> <code>repaint();</code> el aspecto depende de <code>seleccionada</code>, así que hay que
redibujar.</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L53–L54</b> <code>@Override protected void paintComponent(Graphics g)</code>: el dibujo. Sin
<code>super.paintComponent</code>, porque un <code>JComponent</code> transparente no tiene fondo que pintar.</p>
<p class="l"><b>L55</b> Copia suavizada del pincel.</p>
<p class="l"><b>L56–L57</b> <code>new RoundRectangle2D.Double(MARGEN, MARGEN, getWidth() - 2.0 * MARGEN,
getHeight() - 2.0 * MARGEN, 22, 22)</code>: la caja, desde (7, 7) con 290 − 14 = 276 de ancho y 72 − 14 = 58 de
alto, esquinas de 22. La instrucción ocupa dos líneas: Java no termina una instrucción al final de la línea sino en
el <code>;</code>, así que se puede partir donde convenga para leerla mejor. El <code>2.0</code> (con decimal) hace
que la cuenta se haga en <code>double</code>, que es lo que pide <code>RoundRectangle2D.Double</code>.</p>
"""),
             ("g2.setColor(Tema.conAlfa(Tema.MORADO", r"""
<p class="l"><b>L58</b> <code>g2.setColor(Tema.conAlfa(Tema.MORADO, seleccionada ? 38 : 12));</code> relleno
morado translúcido: alfa 38 si está marcada, 12 si no. A diferencia del selector de símbolos, aquí todas las
opciones son moradas; lo que las distingue es la intensidad.</p>
<p class="l"><b>L59</b> Rellena la caja.</p>
<p class="l"><b>L60–L61</b> Borde de neón de 1,8 píxeles. Dos ternarios en una llamada: el color
(<code>Tema.aclarar(Tema.MORADO, 0.15f)</code>, un morado un 15&nbsp;% más claro, (174, 116, 255), si está marcada;
el morado normal si no) y la intensidad (1,2 o 0,35). Partir la llamada en dos líneas con la sangría extra deja
claro que la segunda línea es continuación de la primera.</p>
"""),
             ("// Boton de radio.", r"""
<p class="l"><b>L63</b> Comentario: el botón de radio.</p>
<p class="l"><b>L64</b> <code>double cx = MARGEN + 26;</code> centro del aro en x = 33, cerca del borde
izquierdo.</p>
<p class="l"><b>L65</b> <code>double cy = getHeight() / 2.0;</code> centro vertical: 72 / 2,0 = 36. Dividir entre
<code>2.0</code> en vez de <code>2</code> da un resultado con decimales; con un alto impar no se perdería el medio
píxel. Esta <code>cy</code> sirve de referencia para todo lo demás (icono y textos).</p>
<p class="l"><b>L66</b> El aro: círculo de 20 píxeles cuyo rectángulo envolvente empieza en (23, 26).</p>
"""),
             ("if (seleccionada) {", r"""
<p class="l"><b>L67–L68</b> Si está marcada, el aro se traza en neón <b>rosa</b> (grosor 2,2, intensidad 0,9). El
rosa resalta sobre la caja morada: la mirada va directa a la opción elegida.</p>
<p class="l"><b>L69</b> <code>Tema.aclarar(Tema.ROSA, 0.45f)</code>: rosa mezclado un 45&nbsp;% con blanco, (255,
147, 231).</p>
<p class="l"><b>L70</b> El punto central: círculo de 10 píxeles desde (28, 31).</p>
<p class="l"><b>L71–L72</b> Si no, un aro sin halo en lavanda transparente (alfa 110), de 1,8: la opción vacía.</p>
<p class="l"><b>L73</b> Cierra el <code>if</code>.</p>
"""),
             ("icono.dibujar(", r"""
<p class="l"><b>L75</b> <code>icono.dibujar(g2, MARGEN + 48, cy - 17, 34, seleccionada ? Tema.LAVANDA : Tema.TEXTO_SUAVE);</code>
el icono en un cuadrado de 34 cuya esquina está en (55, 19): restarle 17 (la mitad de 34) a <code>cy</code> lo
centra en vertical. Lavanda si está marcada, lavanda apagado si no.</p>
"""),
             ("g2.setFont(Tema.fuente(Font.BOLD, 16f));", r"""
<p class="l"><b>L77</b> Título en negrita de 16 puntos.</p>
<p class="l"><b>L78</b> Blanco si está marcada, apagado si no: así la opción no elegida «retrocede».</p>
<p class="l"><b>L79</b> <code>g2.drawString(titulo, MARGEN + 92, (float) cy - 3);</code> en x = 99, con la línea
base en 36 − 3 = 33, un poco por encima del centro. <code>(float) cy</code> es un <b>cast</b> (conversión,
capítulo 12): <code>cy</code> es <code>double</code> y <code>drawString</code> pide <code>float</code>; Java no
convierte solo de <code>double</code> a <code>float</code> porque podría perder precisión, así que hay que pedirlo
explícitamente.</p>
<p class="l"><b>L80–L81</b> Descripción: letra normal de 12 puntos, siempre en lavanda apagado.</p>
<p class="l"><b>L82</b> En x = 99, línea base 36 + 15 = 51: título arriba del centro, descripción abajo; juntos
quedan centrados en la caja.</p>
<p class="l"><b>L83</b> Libera la copia del pincel.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>1. El viaje de un clic, de la opción a la pantalla y de vuelta</h3>
<p>En el capítulo 58 la pantalla de configuración creará las dos opciones y les dará sus callbacks. Supón que el
modo actual es «2 jugadores» y el usuario pulsa «Contra la IA»:</p>
<ol>
<li>Swing llama a <code>mousePressed</code> de <code>opcionContraIA</code>.</li>
<li>Como <code>alSeleccionar</code> no es <code>null</code>, se ejecuta <code>alSeleccionar.run()</code>.</li>
<li>Ese <code>run()</code> es la lambda <code>() -&gt; elegirModo(Partida.Modo.CONTRA_IA)</code>: el control
<b>vuelve</b> a la pantalla (de ahí el nombre <i>callback</i>, «llamada de vuelta»).</li>
<li><code>elegirModo</code> llama a <code>opcionDosJugadores.setSeleccionada(false)</code>,
<code>opcionContraIA.setSeleccionada(true)</code> y <code>jugador2.setComputadora(true)</code> (capítulo 49).</li>
<li>Cada <code>setSeleccionada</code> hace <code>repaint()</code>; Swing redibuja las dos opciones: la de la IA
con aro rosa y borde brillante, la otra apagada. La tarjeta del Jugador 2 pasa a «Computadora».</li>
</ol>
<table class="tabla">
<tr><th>Momento</th><th>opcionDosJugadores.seleccionada</th><th>opcionContraIA.seleccionada</th></tr>
<tr><td>Recién creadas</td><td>false</td><td>false</td></tr>
<tr><td>La pantalla llama a <code>elegirModo(DOS_JUGADORES)</code> al final de su constructor</td><td>true</td><td>false</td></tr>
<tr><td>Clic en «Contra la IA»</td><td>false</td><td>true</td></tr>
<tr><td>Otro clic en «Contra la IA»</td><td>false</td><td>true (se vuelve a poner lo mismo; nada cambia)</td></tr>
<tr><td>Clic en «2 jugadores»</td><td>true</td><td>false</td></tr>
</table>

<h3>2. ¿Y si la opción se marcara sola?</h3>
<p>Supón que en <code>mousePressed</code> escribieras <code>setSeleccionada(true)</code>. Al pulsar «Contra la IA»
se marcaría… pero «2 jugadores» <b>también seguiría marcada</b>, porque nadie le dice que se desmarque. Tendrías
dos radios encendidos, que es justo lo que un grupo de radio no permite. Para arreglarlo, cada opción tendría que
conocer a la otra, y si mañana agregas una tercera («IA fácil»), a las otras dos. Con el callback, cada opción solo
se conoce a sí misma y la regla «solo una marcada» vive en un único sitio: la pantalla.</p>
<div class="caja concepto"><b>Detectar no es decidir</b> Este reparto de papeles es el patrón
<b>Observador</b> en pequeño (capítulo 27): el componente es «observado» y avisa; quien lo observa reacciona.
<code>JButton.addActionListener</code> funciona igual. La diferencia es que un botón admite una lista de oyentes y
nuestra opción solo uno, que es todo lo que necesitamos.</div>

<h2>Compila y prueba</h2>
<p><i>Run → Clean and Build Project</i> → <code>BUILD SUCCESS</code>. Las opciones se verán en el capítulo 58 (y en
la pantalla de prueba del capítulo 56).</p>
<table class="tabla">
<tr><th>Problema</th><th>Causa y solución</th></tr>
<tr><td><i>incompatible types: possible lossy conversion from double to float</i></td><td>Falta el
<code>(float)</code> delante de <code>cy</code> en <code>drawString</code>.</td></tr>
<tr><td><i>cannot find symbol: variable PERSONAS</i> (más adelante, en la pantalla)</td><td>Tu <code>Iconos</code>
no tiene ese icono o se llama distinto; revisa el capítulo 42.</td></tr>
<tr><td>(al usarla) pulsar no hace nada</td><td>No se llamó a <code>setAlSeleccionar</code>; gracias al
<code>!= null</code> no hay error, pero tampoco acción.</td></tr>
</table>

<div class="caja git"><b>Git</b>
<pre class="ps">git add src\OpcionModo.java
git commit -m "OpcionModo: opcion de modo de juego"
git push</pre></div>

<h2>Resumen</h2>
<ul>
<li><code>OpcionModo</code> es una tarjetita con botón de radio, icono, título y descripción, dibujada a mano.</li>
<li>Al pulsarla no se marca sola: ejecuta un <code>Runnable</code> (callback) que le dio la pantalla.</li>
<li><code>Runnable</code> tiene un único método, <code>run()</code>; una lambda sin parámetros encaja en él.</li>
<li>Lo opcional se comprueba con <code>!= null</code> antes de usarlo.</li>
<li>La regla del grupo («solo una marcada») vive en la pantalla, que conoce a todas las opciones.</li>
<li>Los ternarios permiten dibujar los dos aspectos (marcada y no) con el mismo código.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Planes y suscripciones</b>: tarjetas «Básico / Pro / Empresa» donde se elige una; cada tarjeta avisa y la
página decide (y actualiza el precio total).</li>
<li><b>Ajustes</b>: «Notificaciones: todas / solo menciones / ninguna». Las opciones ni se conocen entre ellas.</li>
<li><b>Callbacks por todas partes</b>: un componente «Descargar» que recibe un <code>Runnable</code> para cuando
termine la descarga; un temporizador (<code>javax.swing.Timer</code>) que ejecuta una acción cada segundo; un
botón «Guardar» reutilizable que guarda cosas distintas según quién lo use.</li>
<li><b>Componentes reutilizables</b>: como la opción no sabe nada del Totito, puedes copiar
<code>OpcionModo.java</code> a otro proyecto y usarla tal cual con otros textos.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Calcula dónde quedaría el aro (centro) si la opción midiera 80 de alto en vez de 72.</li>
<li>Haz que el título se vuelva rosa cuando la opción esté marcada.</li>
<li>Agrega un efecto al pasar el ratón: un campo <code>boolean encima</code>, que <code>mouseEntered</code> y
<code>mouseExited</code> pongan en <code>true</code>/<code>false</code> (con <code>repaint()</code>), y usa una
intensidad de borde de 0,7 cuando esté encima pero no marcada.</li>
<li>Responde sin ejecutar: ¿qué pasa si quitas el <code>if (alSeleccionar != null)</code> y nadie llama a
<code>setAlSeleccionar</code>? ¿En qué momento exacto fallaría?</li>
<li>Reto: cambia la opción para que se marque sola en <code>mousePressed</code> y, con la pantalla de prueba del
capítulo 56, comprueba que con dos opciones pueden quedar las dos marcadas. Luego deshaz el cambio.</li>
</ol></div>
""",
}
