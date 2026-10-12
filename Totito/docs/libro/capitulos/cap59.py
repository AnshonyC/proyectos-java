CAPITULO = {
    "numero": 59,
    "titulo": "PantallaJuego.java: el controlador de la partida",
    "antes": r"""<p class="entrada">Esta es la pantalla donde de verdad se juega: marcador, letrero de turno, tablero y dos botones.
Pero lo importante no se ve: es el <b>controlador</b> que recibe cada clic, se lo pasa a la <code>Partida</code>, refresca
la pantalla y, cuando le toca a la computadora, espera un instante y la hace jugar, sin congelar la ventana. Aquí
aprenderás la diferencia entre <code>javax.swing.Timer</code> y <code>Thread.sleep</code>, y un error de los que solo
aparecen cuando alguien pulsa un botón en el peor momento.</p>

<h2>Por qué existe este archivo</h2>
<p>En la v0.1 (capítulo 33), <code>JuegoMain</code> hacía de todo: creaba la ventana, los nueve botones del tablero,
guardaba de quién era el turno, decidía cuándo jugaba la IA y escribía el letrero. Funcionaba, pero mezclaba tres
trabajos. En la v1.0 esos trabajos están repartidos:</p>
<table class="tabla">
<tr><th>Trabajo</th><th>En la v0.1</th><th>En la v1.0</th></tr>
<tr><td>Reglas: turnos, quién ganó, marcador</td><td><code>JuegoMain</code></td><td><code>Partida</code> (capítulo 38)</td></tr>
<tr><td>Dibujar el tablero y detectar en qué casilla se hizo clic</td><td><code>JuegoMain</code> (nueve <code>JButton</code>)</td>
<td><code>PanelTablero</code> (capítulo 48)</td></tr>
<tr><td>Dibujar el marcador</td><td>no existía</td><td><code>PanelMarcador</code> (capítulo 52)</td></tr>
<tr><td><b>Conectar todo</b>: clic → regla → dibujo; pausas; turno de la IA</td><td><code>JuegoMain</code></td>
<td><b><code>PantallaJuego</code></b> (este capítulo)</td></tr>
</table>
<p>A ese último papel se le llama <b>controlador</b>: la pieza del medio en el esquema modelo-vista-controlador del
capítulo 27. El <b>modelo</b> (<code>Partida</code>) sabe las reglas pero no sabe dibujar; las <b>vistas</b>
(<code>PanelTablero</code>, <code>PanelMarcador</code>, <code>Rotulo</code>) saben dibujar pero no saben las reglas. El
controlador escucha a las vistas, le pide cosas al modelo y le dice a las vistas qué mostrar. Es como el mesero de un
restaurante: el cliente (el usuario) no entra a la cocina (la lógica) ni la cocina sale al salón; el mesero lleva y
trae.</p>
<p>El diseño original no traía esta pantalla: se hizo con el mismo estilo que las demás (y el comentario del archivo lo
dice).</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>El papel de un <b>controlador</b> y por qué conviene separarlo de las reglas y del dibujo.</li>
<li>Atributos que se inicializan en su propia declaración, y cuándo se ejecuta esa inicialización.</li>
<li>Referencias a métodos (<code>this::alPulsarCasilla</code>) para cumplir una interfaz.</li>
<li>Lambdas con bloque (<code>e -&gt; { …; …; }</code>).</li>
<li><code>javax.swing.Timer</code>: ejecutar algo <b>más tarde</b> sin congelar la ventana. Por qué
<code>Thread.sleep</code> la congela.</li>
<li><code>Runnable</code> como «acción para después».</li>
<li><code>cancelarPendiente</code>: el error que evita, demostrado con un experimento.</li>
<li>Por qué importa el <b>orden</b> de dos líneas dentro del temporizador.</li>
<li><code>switch</code> con flechas sobre un <code>enum</code>.</li>
<li>Una <b>línea de tiempo en milisegundos</b> de una partida contra la IA.</li>
</ul>

<h2>Créalo</h2>
<p>En la rama <code>interfaz-neon</code>, NetBeans: clic derecho en <i>&lt;default package&gt;</i> → <i>New → Java
Class…</i> → <code>PantallaJuego</code> → <i>Finish</i>. Borra la plantilla. O con PowerShell:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
New-Item src\PantallaJuego.java
notepad src\PantallaJuego.java</pre>
<p>Usa <code>Partida</code> (38), <code>PanelMarcador</code> (52), <code>PanelTablero</code> (48), <code>Rotulo</code> (46),
<code>BotonNeon</code> (44), <code>Iconos</code> (42) y <code>Tema</code> (40).</p>
""",
    "archivos": [
        {"ruta": "src/PantallaJuego.java",
         "bloques": [
             (None, r"""<p class="l"><b>L1</b> <code>java.awt.Color</code>: la clase de los colores (capítulo 35). Aquí se
necesita porque el letrero de turno guarda un color en una variable.</p>
<p class="l"><b>L2</b> <code>import javax.swing.Timer;</code> el temporizador de Swing, protagonista del capítulo. Ojo: Java
tiene <b>otra</b> clase llamada <code>Timer</code>, en <code>java.util</code>, que funciona distinto (lo verás más abajo).
Por eso se importa con su nombre completo y no con un comodín. Si importaras <code>java.util.*</code> y
<code>javax.swing.*</code> a la vez, al escribir <code>Timer</code> el compilador diría
<code>reference to Timer is ambiguous</code>: no sabría cuál de las dos quieres.</p>
<p class="l"><b>L3</b> En blanco.</p>"""),
             ("public class PantallaJuego", r"""<p class="l"><b>L4–L12</b> Comentario de documentación. Las líneas 5–6
dicen qué muestra la pantalla y que no venía en el diseño. Las líneas 8–11 explican su papel: el que tenía
<code>JuegoMain</code>. Resume en cuatro renglones todo lo que hace el archivo: recibir clics, pasarlos a la
<code>Partida</code>, hacer jugar a la IA tras una pausa y, al terminar, dejar ver la raya ganadora antes de cambiar de
pantalla.</p>
<p class="l"><b>L13</b> La clase hereda de <code>PantallaBase</code> (capítulo 55), como todas las pantallas.</p>
<p class="l"><b>L14</b> En blanco.</p>"""),
             ("private static final int PAUSA_IA_MS", r"""<p class="l"><b>L15–L16</b> Primera constante: 450 milisegundos
(casi medio segundo) de pausa antes de que juegue la computadora. El sufijo <code>_MS</code> en el nombre recuerda la
unidad; sin él, alguien podría pensar que son segundos. ¿Por qué una pausa? Porque Minimax decide en muy poco tiempo:
sin pausa, la ficha de la IA aparecería en el mismo instante que la tuya, y parecería que el programa jugó por ti. Con
450 ms se alcanza a ver tu ficha, el letrero cambia a «La computadora está pensando…» y luego llega la respuesta. La
v0.1 usaba 350; aquí se subió un poco porque el letrero nuevo necesita un instante para leerse.</p>
<p class="l"><b>L17–L18</b> Segunda constante: 1200 ms (1,2 segundos) que se deja ver la raya ganadora sobre el tablero
antes de pasar a la pantalla de resultado. Si fuera 0, el usuario nunca vería <b>cómo</b> terminó la partida.</p>
<p class="l"><b>L19</b> En blanco.</p>"""),
             ("private final Navegacion navegacion;", r"""<p class="l"><b>L20</b> La navegación, guardada en un atributo
porque se usará al terminar cada partida (<code>mostrarResultado</code>) y al pulsar «Menú principal».</p>
<p class="l"><b>L21</b> El marcador (capítulo 52). Fíjate en el <code>= new PanelMarcador()</code> en la misma línea: el
atributo se <b>inicializa en su declaración</b>. Java ejecuta estas inicializaciones al construir el objeto, justo
después de <code>super(...)</code> y antes del resto del constructor. Por eso el constructor (L29) ya puede usarlo.</p>
<p class="l"><b>L22</b> El letrero del turno: un <code>Rotulo</code> de título (capítulo 46), con texto vacío
(<code>""</code>) por ahora, letra de 26, colores blancos provisionales y 590 × 44 píxeles. El texto y los colores reales
los pondrá <code>actualizar()</code> en cada jugada. La variable se llama <code>turno</code> aunque es un letrero:
dice de quién es el turno.</p>
<p class="l"><b>L23</b> El tablero grande, con casillas de 100 píxeles: 2 × (10 + 8) + 3 × 100 = 336 de lado (capítulo 48).</p>
<p class="l">Los tres son <code>final</code>: la pantalla siempre usa los mismos tres componentes; lo que cambia es lo que
muestran.</p>
<p class="l"><b>L24</b> En blanco.</p>"""),
             ("private Partida partida;", r"""<p class="l"><b>L25</b> La partida que se está mostrando. <b>No</b> es
<code>final</code> y no tiene valor inicial: empieza en <code>null</code> y la entrega <code>comenzar()</code> (L56) desde
fuera. La misma pantalla mostrará muchas partidas a lo largo del día, así que esta referencia cambia.</p>
<p class="l"><b>L26–L27</b> El temporizador que está esperando para hacer algo (la jugada de la IA o el paso al
resultado), o <code>null</code> si no hay ninguno. Guardarlo en un atributo permite dos cosas: <b>saber</b> si hay algo
pendiente (para no aceptar clics mientras tanto) y <b>cancelarlo</b> si el usuario se va. Es la pieza clave del
capítulo.</p>
<p class="l"><b>L28</b> En blanco.</p>"""),
             ("public PantallaJuego(", r"""<p class="l"><b>L29</b> El constructor.</p>
<p class="l"><b>L30</b> Construye la base: fondo y encabezado.</p>
<p class="l"><b>L31</b> Guarda la navegación en el atributo.</p>
<p class="l"><b>L32</b> <code>tablero.setOyente(this::alPulsarCasilla);</code> conecta el tablero con esta pantalla.
<code>setOyente</code> espera un <code>OyenteCasilla</code> (la interfaz de un solo método
<code>casillaPulsada(int fila, int columna)</code> del capítulo 48). En vez de crear una clase que la implemente, se
pasa una <b>referencia a método</b> (capítulo 25): <code>this::alPulsarCasilla</code> significa «cuando llamen a
<code>casillaPulsada(f, c)</code>, ejecuta mi método <code>alPulsarCasilla(f, c)</code>». Java lo acepta porque los dos
métodos reciben lo mismo (dos <code>int</code>) y devuelven lo mismo (nada). Sin esta línea, los clics llegarían al
tablero y morirían ahí: el panel no tendría a quién avisar.</p>
<p class="l"><b>L33</b> En blanco.</p>"""),
             ("BotonNeon reiniciar", r"""<p class="l"><b>L34</b> El botón «Reiniciar»: de contorno (acción secundaria), con el icono
de flechas en círculo.</p>
<p class="l"><b>L35</b> Se conecta con una <b>lambda con bloque</b>: después de la flecha no hay una sola expresión
sino un bloque entre llaves, con varias instrucciones, cada una con su <code>;</code>.</p>
<p class="l"><b>L36</b> <code>partida.reiniciar()</code> limpia el tablero de <b>la misma</b> partida y conserva el
marcador (capítulo 38). Ojo: usa el atributo <code>partida</code> tal como esté en el momento del clic, no en el momento
de crear el botón (cuando todavía era <code>null</code>). La lambda lee el atributo cada vez que se ejecuta.</p>
<p class="l"><b>L37</b> Vuelve a «comenzar» esa misma partida: cancela cualquier pausa pendiente, refresca la pantalla y,
si la IA abre, la pone a jugar. Reutilizar <code>comenzar</code> evita escribir dos veces lo mismo.</p>
<p class="l"><b>L38</b> Cierra el bloque de la lambda (<code>}</code>) y el paréntesis de <code>addActionListener</code>
(<code>)</code>), y termina la instrucción (<code>;</code>).</p>"""),
             ("BotonNeon menu", r"""<p class="l"><b>L39</b> «Menú principal»: píldora de azul a morado con el icono de la casa.</p>
<p class="l"><b>L40–L43</b> Al pulsarlo, primero <code>cancelarPendiente()</code> y después <code>irAlMenu()</code>. El
orden importa y lo entenderás del todo en la L101: si hubiera una jugada de la IA o un paso al resultado esperando,
quedaría «vivo» y actuaría cuando el usuario ya está en el menú.</p>
<p class="l"><b>L44</b> En blanco.</p>"""),
             ("relleno();", r"""<p class="l"><b>L45–L52</b> El orden en pantalla, de arriba abajo, con los métodos de
<code>PantallaBase</code>: resorte, marcador, 2 píxeles, letrero de turno, tablero, 6 píxeles, la fila con los dos botones
separados por 8 píxeles, y resorte. Es la pantalla que verás en la captura del capítulo 61.</p>
<p class="l"><b>L53</b> Cierra el constructor. Fíjate en que el constructor <b>no</b> recibe ninguna partida: la pantalla
se construye una sola vez, vacía, y luego se le dan partidas con <code>comenzar</code>. <b>L54</b> En blanco.</p>"""),
             ("public void comenzar(", r"""<p class="l"><b>L55</b> Comentario: qué hace el método.</p>
<p class="l"><b>L56</b> <code>public</code> porque lo llama desde fuera el <code>PanelPrincipal</code> (capítulo 61), al
iniciar una partida y al «jugar de nuevo». Es la puerta de entrada de la pantalla.</p>
<p class="l"><b>L57</b> Lo primero: cancelar cualquier temporizador que hubiera quedado de una partida anterior.</p>
<p class="l"><b>L58</b> Guarda la partida. <code>this.partida</code> es el atributo; <code>partida</code>, el parámetro.</p>
<p class="l"><b>L59</b> Pasa el estado de la partida a los componentes (tablero, marcador, letrero).</p>
<p class="l"><b>L60</b> Si la partida la abre la computadora, programa su jugada. Si la abre una persona, no hace nada y
se queda esperando clics.</p>
<p class="l"><b>L61–L62</b> Cierre y línea en blanco.</p>"""),
             ("private void alPulsarCasilla", r"""<p class="l"><b>L63</b> El método que el tablero llama en cada clic sobre
una casilla (gracias a la L32). Recibe fila y columna (0 a 2).</p>
<p class="l"><b>L64–L66</b> Una <b>guarda</b>: si hay algo pendiente (<code>pendiente != null</code>) o es turno de la IA,
se sale del método con <code>return</code> sin hacer nada. El <code>||</code> es «o» (capítulo 13): basta con que una
de las dos sea cierta. ¿Cuándo pasa? Durante los 450 ms en que la IA «piensa» y durante los 1200 ms en que se muestra la
raya ganadora. Sin esta guarda, un usuario rápido podría poner una ficha en el turno de la computadora. El comentario al
final de la L65 lo explica en la misma línea.</p>
<p class="l"><b>L67</b> Intenta la jugada en la <code>Partida</code>. <code>jugar</code> devuelve <code>true</code> si
valió y <code>false</code> si no (casilla ocupada o partida terminada; capítulo 38). Fíjate en que la pantalla <b>no</b>
comprueba si la casilla está libre: esa regla es de la lógica, y la pantalla le pregunta.</p>
<p class="l"><b>L68</b> Solo si la jugada valió, se sigue con lo que toca después. Si no valió (clic en una casilla
ocupada), no pasa nada: ni sonido ni error, simplemente se ignora.</p>
<p class="l"><b>L69–L71</b> Cierres y línea en blanco.</p>"""),
             ("private void despuesDeJugada", r"""<p class="l"><b>L72</b> Lo que pasa después de <b>cualquier</b> jugada válida, sea
de una persona o de la IA. Tenerlo en un solo método garantiza que las dos clases de jugada se traten igual.</p>
<p class="l"><b>L73</b> Refresca la pantalla con la ficha nueva.</p>
<p class="l"><b>L74–L75</b> Si la partida sigue, quizá ahora le toque a la IA: <code>programarTurnoIA</code> lo comprueba
y, si es así, programa su jugada.</p>
<p class="l"><b>L76–L77</b> Si terminó (victoria o empate), espera <code>PAUSA_RESULTADO_MS</code> y después pide a la
navegación que muestre el resultado. La acción se escribe como lambda sin parámetros, <code>() -&gt; …</code>: es un
<code>Runnable</code>, «algo para ejecutar luego». Ese «luego» lo decide <code>esperar</code>.</p>
<p class="l"><b>L78–L80</b> Cierres y línea en blanco.</p>"""),
             ("private void programarTurnoIA", r"""<p class="l"><b>L81</b> Programa la jugada de la computadora, si le toca.</p>
<p class="l"><b>L82</b> <code>partida.esTurnoDeIA()</code> (capítulo 38) es <code>true</code> solo si hay IA, el turno es
del Jugador 2 y la partida sigue. En modo de dos personas, siempre es <code>false</code> y este método no hace nada.</p>
<p class="l"><b>L83–L86</b> Espera 450 ms y entonces ejecuta un bloque de dos pasos: que la <code>Partida</code> haga jugar
a la IA (<code>jugarTurnoIA</code> pide la jugada a <code>IA_Minimax</code> y la aplica) y, después,
<code>despuesDeJugada()</code>, <b>exactamente igual que tras un clic</b>. Así la jugada de la IA refresca la pantalla
y, si gana o empata, programa el paso al resultado, sin código repetido.</p>
<p class="l">Fíjate en la cadena: <code>despuesDeJugada</code> llama a <code>programarTurnoIA</code>, que (más tarde) llama
a <code>despuesDeJugada</code>. No es un bucle infinito porque después de jugar la IA el turno pasa a la persona, y
<code>esTurnoDeIA()</code> da <code>false</code>.</p>
<p class="l"><b>L87–L89</b> Cierres y línea en blanco.</p>"""),
             ("private void esperar(", r"""<p class="l"><b>L90</b> Comentario: «una sola vez, dentro de <i>ms</i> milisegundos».</p>
<p class="l"><b>L91</b> El método recibe cuánto esperar y qué hacer después (un <code>Runnable</code>).</p>
<p class="l"><b>L92</b> Primero cancela cualquier espera anterior: solo puede haber <b>una</b> cosa pendiente a la vez.</p>
<p class="l"><b>L93</b> <code>new Timer(ms, e -&gt; { … })</code> crea un temporizador de Swing. Primer argumento: cada
cuántos milisegundos «suena». Segundo: un <code>ActionListener</code> (la misma clase de oyente que los botones) con lo
que hay que hacer cuando suene. El temporizador se guarda en el atributo <code>pendiente</code>.</p>
<p class="l"><b>L94</b> Cuando suena, lo primero es marcar que ya no hay nada pendiente: <code>pendiente = null</code>. Esta
línea va <b>antes</b> de la siguiente por una razón precisa que verás en «Cómo funciona por dentro».</p>
<p class="l"><b>L95</b> <code>accion.run()</code> ejecuta la acción que se pasó (la jugada de la IA o el cambio a la
pantalla de resultado). <code>run</code> es el único método de <code>Runnable</code>.</p>
<p class="l"><b>L96</b> Cierra la lambda y el paréntesis de <code>new Timer(</code>.</p>"""),
             ("pendiente.setRepeats(false);", r"""<p class="l"><b>L97</b> Por defecto, un <code>Timer</code> de Swing se repite:
sonaría cada 450 ms para siempre (sirve para animaciones o relojes). <code>setRepeats(false)</code> lo convierte en
«de un solo disparo». Sin esta línea, la IA intentaría jugar cada 450 ms y el paso al resultado se repetiría sin fin.</p>
<p class="l"><b>L98</b> <code>start()</code> lo pone en marcha. Crear un <code>Timer</code> no lo arranca: hasta esta línea
solo existe, como un despertador sin activar. Y <code>start()</code> <b>no espera</b>: vuelve al instante, y el programa
sigue con lo que tenga que hacer. La espera la lleva el temporizador por su cuenta.</p>
<p class="l"><b>L99–L100</b> Cierre y línea en blanco.</p>"""),
             ("private void cancelarPendiente", r"""<p class="l"><b>L101</b> El comentario resume el error que evita: que un
temporizador viejo actúe sobre una partida que ya se reinició o se abandonó.</p>
<p class="l"><b>L102</b> Método privado, sin parámetros ni resultado.</p>
<p class="l"><b>L103</b> Solo si hay algo pendiente (si no, <code>pendiente.stop()</code> sobre <code>null</code> lanzaría un
<code>NullPointerException</code>).</p>
<p class="l"><b>L104</b> <code>stop()</code> desactiva el temporizador: si todavía no había sonado, ya no sonará nunca.
Es la línea que hace el trabajo.</p>
<p class="l"><b>L105</b> Y se olvida la referencia, para que <code>pendiente == null</code> vuelva a significar «no hay nada
esperando» y la guarda de la L64 deje pasar los clics.</p>
<p class="l"><b>L106–L108</b> Cierres y línea en blanco. Se llama desde tres sitios: <code>comenzar</code> (L57), el botón
de menú (L41) y <code>esperar</code> (L92).</p>"""),
             ("private void actualizar()", r"""<p class="l"><b>L109–L110</b> El método que traslada el estado de la
<code>Partida</code> a la pantalla. Se llama después de cada cambio. Es el único sitio que «pinta» datos; así nunca
quedan a medias (tablero nuevo con marcador viejo).</p>
<p class="l"><b>L111</b> El tablero copia las nueve casillas y busca la raya ganadora (capítulo 48).</p>
<p class="l"><b>L112</b> El marcador recibe la partida entera (lee de ella nombres, fichas, victorias, empates y de quién
es el turno).</p>
<p class="l"><b>L114</b> Variable local con el jugador al que le toca. Se guarda en una variable porque se usa tres veces.</p>
<p class="l"><b>L115</b> <code>enCurso</code>: <code>true</code> si la partida no ha terminado.</p>
<p class="l"><b>L116</b> El tablero solo acepta clics (y muestra la manita) si la partida sigue <b>y</b> no es turno de la
IA. <code>&amp;&amp;</code> es «y»; <code>!</code> es «no». Es una segunda protección, ahora visual: además de la guarda
de la L64, el tablero deja de ofrecer jugadas. Las dos juntas se llaman defensa en profundidad.</p>
<p class="l"><b>L117</b> La ficha «fantasma» que se ve transparente bajo el ratón es la del jugador en turno.</p>"""),
             ("switch (partida.getEstado())", r"""<p class="l"><b>L119</b> Un <code>switch</code> sobre el estado
(capítulo 13): según cuál de los tres valores del <code>enum</code> sea, se ejecuta una rama. Dentro de un
<code>switch</code> sobre un <code>enum</code>, los casos se escriben con el nombre corto (<code>EN_CURSO</code>, no
<code>Partida.Estado.EN_CURSO</code>): Java ya sabe de qué <code>enum</code> se trata.</p>
<p class="l"><b>L120</b> <code>case EN_CURSO -&gt; { … }</code>: la forma con flecha. A diferencia del <code>switch</code>
clásico, no hace falta <code>break</code>: al terminar la rama, termina el <code>switch</code>. Como la rama tiene varias
instrucciones, van entre llaves.</p>
<p class="l"><b>L121</b> El color de la ficha del jugador en turno: rosa si es X, azul si es O.</p>
<p class="l"><b>L122–L124</b> El texto, con el ternario: si es turno de la IA, «La computadora está pensando…» (el
<code>…</code> es un solo carácter, los puntos suspensivos tipográficos); si no, «Turno de» más el nombre.</p>
<p class="l"><b>L125</b> Pone el texto en el letrero con un degradado de una versión aclarada del color (35 % hacia el
blanco, <code>Tema.aclarar</code>, capítulo 40) al color puro.</p>
<p class="l"><b>L126</b> Cierra la rama.</p>"""),
             ("case VICTORIA", r"""<p class="l"><b>L127–L130</b> Si alguien ganó: el color es el de la ficha del ganador y el
texto, «¡Tres en línea!». La variable <code>color</code> se vuelve a declarar aquí sin conflicto porque cada par de
llaves es un ámbito distinto (capítulo 16). Este letrero solo se ve durante la pausa de 1,2 s, junto a la raya.</p>
<p class="l"><b>L131</b> Si hubo empate: «¡Empate!» de lavanda a morado. Es una sola instrucción, así que no necesita
llaves.</p>
<p class="l"><b>L132–L134</b> Cierran el <code>switch</code>, el método y la clase.</p>"""),
         ]},
    ],
    "despues": r"""<h2>Cómo funciona por dentro</h2>
<h3>El hilo de Swing es una fila</h3>
<p>Recuerda el capítulo 37: todo lo de Swing (atender clics, ejecutar oyentes, repintar) lo hace <b>un solo hilo</b>, el
<i>Event Dispatch Thread</i> o EDT. Imagínalo como una cajera de banco con una fila: atiende una tarea, luego la
siguiente. Un clic es una tarea; un <code>repaint()</code> no pinta en el acto, sino que <b>pone en la fila</b> la tarea
«pintar»; el sonido de un <code>Timer</code> también es una tarea en la fila. Mientras la cajera está ocupada con una
tarea, las demás esperan.</p>
<h3>Por qué no <code>Thread.sleep</code></h3>
<p>La forma ingenua de «esperar medio segundo» sería esta:</p>
<pre class="java">// MAL: congela la ventana
private void alPulsarCasilla(int fila, int columna) {
    partida.jugar(fila, columna);
    actualizar();                 // pide repintar... pero solo lo pone en la fila
    try {
        Thread.sleep(450);        // el EDT se duerme 450 ms
    } catch (InterruptedException e) {
        return;
    }
    partida.jugarTurnoIA();
    actualizar();
}</pre>
<p><code>Thread.sleep(450)</code> duerme <b>al hilo que lo ejecuta</b>, y ese hilo es el EDT, la cajera. Durante esos
450 ms nadie repinta, nadie atiende clics, los botones no se iluminan. Peor: el repintado que pidió el primer
<code>actualizar()</code> sigue en la fila, así que tu ficha <b>no aparece</b> hasta que el método termina, y para
entonces la IA ya jugó. Verías las dos fichas aparecer juntas, que es justo lo que la pausa quería evitar. Con esperas
de varios segundos, Windows llega a poner «(No responde)» en la barra de título. Además, <code>sleep</code> obliga a escribir
un <code>try/catch</code> (capítulo 26) para una excepción que aquí no tiene sentido.</p>
<p><code>javax.swing.Timer</code> hace lo contrario: <code>start()</code> vuelve al instante, la cajera queda libre
(repinta tu ficha, cambia el letrero) y un hilo auxiliar de Swing cuenta el tiempo. Cuando se cumple, ese hilo <b>pone
en la fila del EDT</b> la acción. Así la acción se ejecuta en el EDT, donde es seguro tocar componentes. El
<code>java.util.Timer</code>, en cambio, ejecutaría la acción en su propio hilo, fuera del EDT, y tocar Swing desde ahí
provoca errores raros e intermitentes. Por eso la L2 importa el de Swing con su nombre completo.</p>
<div class="caja concepto"><b>La regla de oro de Swing</b> Nunca hagas esperar al EDT (ni <code>sleep</code>, ni bucles
largos, ni descargas) y nunca toques componentes desde otro hilo. Para «más tarde», <code>javax.swing.Timer</code>; para
«esto tarda mucho», <code>SwingWorker</code> (capítulo 69).</div>

<h3>Línea de tiempo de una jugada contra la IA</h3>
<p>Ana eligió la O y el modo «Contra la IA» (capítulo 58). La X es de la computadora y la X siempre empieza. Esta tabla
sigue lo que pasa, milisegundo a milisegundo, desde que se pulsa «Comenzar partida». Los tiempos de Ana son un ejemplo
(ella hace clic a los 2 y a los 4 segundos); las pausas son las reales del código. Las jugadas de la IA son las que
Minimax elige de verdad en esta situación: las obtuvimos ejecutando el juego.</p>
<table class="tabla">
<tr><th>t (ms)</th><th>Qué pasa (método)</th><th>Qué se ve</th><th><code>pendiente</code></th></tr>
<tr><td>0</td><td><code>iniciarPartida</code> crea la <code>Partida</code> (turno de la IA) y llama a <code>comenzar</code>:
<code>cancelarPendiente</code> (nada), <code>actualizar</code>, <code>programarTurnoIA</code> → <code>esperar(450)</code>
crea y arranca T1.</td><td>Tablero vacío, sin manita. Letrero rosa «La computadora está pensando…».</td><td>T1</td></tr>
<tr><td>200</td><td>Ana, impaciente, hace clic en el centro. El tablero no es interactivo (L116): ni siquiera avisa.</td>
<td>Nada cambia.</td><td>T1</td></tr>
<tr><td>450</td><td>Suena T1 (en el EDT): <code>pendiente = null</code>; <code>jugarTurnoIA</code> (Minimax elige la
esquina (0,0)); <code>despuesDeJugada</code> → <code>actualizar</code>; la partida sigue y le toca a Ana, así que
<code>programarTurnoIA</code> no hace nada.</td><td>Aparece la X arriba a la izquierda. Letrero azul «Turno de Ana».
Vuelve la manita.</td><td>null</td></tr>
<tr><td>2000</td><td>Ana hace clic en (1,1). <code>alPulsarCasilla</code>: la guarda deja pasar;
<code>jugar(1,1)</code> vale; <code>despuesDeJugada</code> → <code>actualizar</code> → <code>programarTurnoIA</code> →
<code>esperar(450)</code> crea T2.</td><td>La O azul en el centro, <b>al instante</b>. Letrero «La computadora está
pensando…».</td><td>T2</td></tr>
<tr><td>2450</td><td>Suena T2: la IA juega (0,1).</td><td>Segunda X arriba. «Turno de Ana».</td><td>null</td></tr>
<tr><td>4000</td><td>Ana hace clic en (2,0) (no ve que debía tapar (0,2)). Se programa T3.</td><td>La O abajo a la
izquierda. «La computadora está pensando…».</td><td>T3</td></tr>
<tr><td>4450</td><td>Suena T3: la IA juega (0,2) y hace tres en línea. <code>despuesDeJugada</code>: el estado ya no es
<code>EN_CURSO</code>, así que <code>esperar(1200)</code> crea T4.</td><td>Tercera X, raya rosa sobre la fila de arriba,
letrero «¡Tres en línea!». Tablero sin manita.</td><td>T4</td></tr>
<tr><td>5650</td><td>Suena T4: <code>navegacion.mostrarResultado(partida)</code>.</td><td>Pantalla de resultado: «¡Ganó
Computadora!», «La máquina no perdona» (capítulo 60).</td><td>null</td></tr>
</table>
<p>Un matiz honesto: a los tiempos de la IA hay que sumarles lo que tarda Minimax en decidir. Con el tablero vacío
(la primera jugada) revisa todas las partidas posibles y, en una computadora normal, tarda desde unas decenas de
milisegundos hasta un par de décimas; con fichas ya puestas, menos de un milisegundo. Ese cálculo ocurre <b>en el EDT</b>
(dentro de T1), así que durante ese instante la ventana tampoco se repinta. No se nota porque el tablero ya está
bloqueado y el letrero ya dice «pensando», pero en un juego con una IA más lenta (ajedrez, por ejemplo) habría que
calcular en otro hilo con <code>SwingWorker</code>.</p>

<h3>El error que evita <code>cancelarPendiente</code></h3>
<p>Imagina que borras la línea <code>pendiente.stop();</code> (L104). Todo parece funcionar… hasta que alguien pulsa un
botón durante una pausa. Lo comprobamos con un experimento (una copia del archivo sin esa línea, y clics simulados a
tiempos exactos). Ana y Luis juegan en modo de dos personas; Ana gana a los 500 ms, y se programa T4 para dentro de
1200 ms (sonará a los 1700). En las salidas, cada línea empieza con el tiempo en que se observó; la línea
«estado VICTORIA» la escribe una comprobación programada a los 700 ms.</p>
<p><b>Caso 1: Ana pulsa «Menú principal» a los 1000 ms.</b> Con el código bueno, el menú aparece y ahí se queda. Sin el
<code>stop()</code>:</p>
<pre class="salida">t=  724 ms estado VICTORIA
t= 1021 ms pulso Menu
t= 1027 ms pantalla visible: PantallaMenu
t= 1728 ms pantalla visible: PantallaResultado</pre>
<p>Siete décimas después de llegar al menú, la pantalla salta sola al resultado de una partida que Ana ya había dejado.
Para el usuario parece un fantasma.</p>
<p><b>Caso 2: Ana pulsa «Reiniciar» a los 1000 ms</b> (quiere la revancha ya). El tablero se limpia, pero T4 sigue vivo
y a los 1700 ms llama a <code>mostrarResultado</code> con una partida <b>en curso</b>, sin ganador:</p>
<pre class="salida">Exception in thread "AWT-EventQueue-0" java.lang.NullPointerException: Cannot invoke "Jugador.getFicha()" because "ganador" is null
	at PantallaResultado.mostrar(PantallaResultado.java:64)
	at PanelPrincipal.mostrarResultado(PanelPrincipal.java:76)
	at PantallaJuego.lambda$despuesDeJugada$2(PantallaJuego.java:77)
	at PantallaJuego.lambda$esperar$4(PantallaJuego.java:95)
	at java.desktop/javax.swing.Timer.fireActionPerformed(Timer.java:311)
	...</pre>
<p>Lee la pila de llamadas (capítulo 16) de abajo arriba: el <code>Timer</code> disparó la lambda de <code>esperar</code>
(L95), que ejecutó la de <code>despuesDeJugada</code> (L77), que llamó a <code>mostrarResultado</code>. Fíjate también en
el nombre del hilo, <code>AWT-EventQueue-0</code>: es el EDT, la prueba de que la acción del <code>Timer</code> corre en
el hilo de Swing.</p>
<p>Con <code>cancelarPendiente</code>, los dos casos están cubiertos: «Menú principal» lo llama antes de irse (L41) y
«Reiniciar» lo llama a través de <code>comenzar</code> (L57). Es un error típico de toda interfaz con esperas: <b>una
acción programada debe poder cancelarse si cambia el contexto</b> para el que se programó.</p>

<h3>Por qué <code>pendiente = null</code> va antes de <code>accion.run()</code></h3>
<p>Las líneas 94 y 95 parecen intercambiables. No lo son. Cuando la IA gana, la acción de T3 (la jugada) llama, dentro
de <code>accion.run()</code>, a <code>esperar(1200)</code>, que guarda <b>T4</b> en <code>pendiente</code>. Si la línea
<code>pendiente = null</code> estuviera <b>después</b> de <code>accion.run()</code>, borraría esa referencia a T4 recién
creada. T4 seguiría vivo, pero nadie lo podría cancelar: <code>cancelarPendiente</code> vería <code>null</code> y no
haría nada. Lo comprobamos moviendo la línea: al pulsar «Menú principal» durante la pausa, la pantalla volvía a saltar al
resultado. (Es la partida contra la IA de la línea de tiempo, con los clics de Ana a los 1000 y 2000 ms: la IA gana a
los 2475 ms y Ana pulsa «Menú principal» a los 3151.)</p>
<pre class="salida">t= 2475 ms PantallaJuego VICTORIA
t= 3151 ms pulso Menu
t= 3154 ms PantallaMenu VICTORIA
t= 3737 ms PantallaResultado VICTORIA</pre>
<p>Moraleja: cuando una acción puede programar otra, «limpiar» el estado va <b>antes</b> de ejecutarla.</p>

<h2>Compila y prueba</h2>
<p>Compila con <i>Clean and Build</i> (Shift+F11): debe decir <code>BUILD SUCCESS</code>. Pero esta pantalla, a diferencia
de las anteriores, <b>no sirve en la vista previa tal cual</b>. Si cambias la línea <code>AQUI</code> por
<code>new PantallaJuego(sinNavegacion)</code>, verás el tablero vacío, sin marcador ni letrero (no hay partida que
mostrar: <code>PanelMarcador</code> no dibuja nada si su partida es <code>null</code>), los clics no hacen nada (el tablero
no es interactivo) y «Reiniciar» lanza un <code>NullPointerException</code> en la consola, porque <code>partida</code> es
<code>null</code>. Es lo esperado: una pantalla de juego sin partida no tiene nada que hacer. La verás funcionando de
verdad en el capítulo 61, cuando el <code>PanelPrincipal</code> le entregue partidas.</p>
<div class="caja consejo"><b>Si no puedes esperar</b> Puedes darle una partida en la vista previa. Sustituye la línea
<code>AQUI</code> por estas tres:
<pre class="java">            PantallaJuego juego = new PantallaJuego(sinNavegacion);
            juego.comenzar(new Partida(new Jugador("Ana", 'X'), new Jugador("Luis", 'O'), Partida.Modo.DOS_JUGADORES));
            JPanel pantalla = juego;   // &lt;-- AQUI</pre>
Compila y lanza la vista previa: ya se puede jugar, con marcador, letrero y ficha fantasma. Al ganar, verás la raya y el
letrero «¡Tres en línea!», pero no cambiará de pantalla (la navegación de mentira no hace nada). Prueba también
<code>Partida.Modo.CONTRA_IA</code> y dale a Ana la O: la computadora abrirá tras medio segundo. Al terminar, deja la vista
previa como estaba con <code>git restore herramientas\VistaPrevia.java</code>.</div>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Síntoma</th><th>Causa probable</th><th>Solución</th></tr>
<tr><td><code>reference to Timer is ambiguous</code></td><td>Importaste <code>java.util.*</code> y <code>javax.swing.*</code>.</td>
<td>Importa <code>javax.swing.Timer</code> por su nombre.</td></tr>
<tr><td>La IA juega una y otra vez, o la pantalla de resultado «parpadea».</td><td>Falta <code>setRepeats(false)</code>.</td>
<td>Agrega la L97.</td></tr>
<tr><td>La IA nunca juega.</td><td>Falta <code>pendiente.start()</code>, o <code>programarTurnoIA</code> no se llama en
<code>comenzar</code>.</td><td>Revisa las L60 y L98.</td></tr>
<tr><td>Se puede jugar en el turno de la IA.</td><td>Falta la guarda de la L64 o la condición de la L116.</td>
<td>Revísalas.</td></tr>
<tr><td><code>incompatible types: invalid method reference</code> en la L32.</td><td><code>alPulsarCasilla</code> no recibe
exactamente dos <code>int</code>.</td><td>Revisa su firma en la L63.</td></tr>
</table>

<div class="caja git"><b>Git</b> Si usaste el truco de la vista previa, devuélvela primero. Luego, el commit de la pantalla:
<pre class="ps">git restore herramientas\VistaPrevia.java
git add src\PantallaJuego.java
git commit -m "PantallaJuego: el controlador de la partida"
git push
git log --oneline -3</pre></div>

<h2>Resumen</h2>
<ul>
<li><code>PantallaJuego</code> es el <b>controlador</b>: recibe clics del <code>PanelTablero</code>, se los pasa a la
<code>Partida</code> y refresca tablero, marcador y letrero con <code>actualizar()</code>.</li>
<li>Toda jugada válida, de persona o de IA, pasa por <code>despuesDeJugada()</code>: un solo camino.</li>
<li><code>javax.swing.Timer</code> ejecuta una acción más tarde, en el EDT, sin bloquearlo; con
<code>setRepeats(false)</code> suena una sola vez.</li>
<li><code>Thread.sleep</code> en el EDT congela la ventana: nada se repinta ni responde hasta que despierta.</li>
<li><code>pendiente</code> sirve para bloquear clics mientras hay algo programado y para cancelarlo con
<code>cancelarPendiente()</code>.</li>
<li>Sin cancelar, una acción vieja puede saltar de pantalla sola o fallar sobre una partida reiniciada.</li>
<li><code>pendiente = null</code> va antes de <code>accion.run()</code>, porque la acción puede programar otra espera.</li>
<li>El <code>switch</code> con flechas sobre el <code>enum</code> <code>Estado</code> elige el letrero sin
<code>break</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Mensajes que desaparecen solos:</b> «Guardado» que se oculta a los 2 segundos con un <code>Timer</code> de un solo
disparo. Si el usuario guarda otra vez antes, cancela el anterior (igual que <code>cancelarPendiente</code>) para que no
se oculte el mensaje nuevo antes de tiempo.</li>
<li><b>Búsqueda mientras se escribe:</b> esperar 300 ms después de la última tecla antes de buscar; cada tecla nueva
cancela la espera anterior. Es la misma técnica y evita cien búsquedas por palabra.</li>
<li><b>Relojes, cronómetros y animaciones:</b> un <code>Timer</code> que sí se repite (sin <code>setRepeats(false)</code>),
por ejemplo cada 1000 ms para un reloj o cada 16 ms para una animación a 60 cuadros por segundo.</li>
<li><b>Cualquier juego por turnos o aplicación con pantallas:</b> separar modelo (reglas), vistas (dibujo) y controlador
(conexión). Un juego de cartas, un cajero de supermercado o un formulario de varios pasos se organizan igual.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Cambia <code>PAUSA_IA_MS</code> a 0 y luego a 2000. Juega contra la IA con cada valor. ¿Cuál se siente mejor y por
qué? Vuelve a 450.</li>
<li>Rehaz en papel la línea de tiempo de este capítulo suponiendo que Ana eligió la X (empieza ella) y hace clic a los
1000 y 3000 ms. ¿Cuándo existe <code>pendiente</code> y cuándo es <code>null</code>?</li>
<li>Escribe en un programa aparte, con <code>JFrame</code>, un botón que al pulsarlo cambie su texto a «Espera…» y,
2 segundos después, a «¡Listo!», usando <code>javax.swing.Timer</code>. Después hazlo con <code>Thread.sleep</code> y
observa la diferencia. Pista: con <code>sleep</code> nunca verás «Espera…».</li>
<li>Haz que el letrero, en el turno de una persona, diga también con qué ficha juega: «Turno de Ana (O)». ¿Qué línea
cambias?</li>
<li>Reto: agrega un botón «Deshacer» que no haga nada mientras haya algo pendiente. ¿Qué condición reutilizarías? (No hace
falta que deshaga de verdad; piensa solo en cuándo debe estar activo.)</li>
</ol></div>
""",
}
