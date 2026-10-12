# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 38,
    "titulo": "Partida.java: turnos, estado y marcador",
    "antes": r"""
<p class="entrada">Empieza la Parte VII: aquí el Totito deja de ser la ventana gris de la v0.1 y se convierte en
el juego neón de cinco pantallas. Antes de dibujar un solo píxel hay que ordenar la casa: sacar las reglas de
<code>JuegoMain</code> y guardarlas en una clase propia, <code>Partida</code>, que no sabe nada de ventanas.</p>

<h2>Bienvenido a la Parte VII</h2>
<p>En la Parte V construiste la lógica (<code>Tablero</code>, <code>Jugador</code>, <code>IA_Minimax</code>) y una
primera ventana con Swing básico (<code>JuegoMain</code>, etiqueta <code>v0.1.0</code>). En la Parte VI aprendiste a leer
un diseño, la teoría del color, la tipografía y cómo dibuja Swing. Ahora juntas todo. Los 24 capítulos de esta parte
siguen un orden pensado para que <b>cada archivo nuevo solo use cosas que ya existen</b>:</p>
<table class="tabla">
<tr><th>Capítulos</th><th>Qué se construye</th><th>Se ve algo en pantalla</th></tr>
<tr><td>38–42</td><td>Los cimientos: la lógica de la partida (<code>Partida</code>), el contrato entre pantallas
(<code>Navegacion</code>), los colores y fuentes (<code>Tema</code>), el efecto neón (<code>Dibujo</code>) y los iconos
(<code>Iconos</code>).</td><td>Todavía no: solo se compila.</td></tr>
<tr><td>43–54</td><td>Los componentes reutilizables: tarjetas, botones, encabezado, rótulos, campo de texto, tablero,
marcador…</td><td>Todavía no.</td></tr>
<tr><td>55–60</td><td>Las cinco pantallas. En el capítulo 56 aparece <code>VistaPrevia</code>.</td><td><b>Sí, desde el 56.</b></td></tr>
<tr><td>61</td><td><code>PanelPrincipal</code> y <code>TotitoApp</code>: todo junto, versión <code>v1.0.0</code>.</td><td>El juego completo.</td></tr>
</table>
<p>Durante varios capítulos vas a escribir código sin ver nada nuevo en la pantalla. Es normal y es a propósito: es
como poner los cimientos y las tuberías de una casa antes de pintar las paredes. Cada capítulo termina con el proyecto
<b>compilando</b>, y esa es tu prueba de que vas bien.</p>

<h2>Primero: una rama nueva para la interfaz</h2>
<p>En el capítulo 9 viste qué es una <b>rama</b> (branch): una línea de trabajo paralela dentro del mismo repositorio. Hasta
ahora todo lo hiciste en <code>main</code>. La interfaz neón es un cambio grande que va a durar 24 capítulos; si lo hicieras
directamente en <code>main</code>, durante semanas tu rama principal tendría un juego a medio construir. La buena práctica es:</p>
<ul>
<li><code>main</code> se queda como está: con la <code>v0.1.0</code> que funciona.</li>
<li>Todo el trabajo nuevo va en una rama llamada <code>interfaz-neon</code>, con un commit por capítulo.</li>
<li>Cuando la interfaz esté terminada y probada (capítulo 61), se abre un <b>Pull Request</b> de
<code>interfaz-neon</code> hacia <code>main</code>, se revisa y se fusiona. Entonces nace la <code>v1.0.0</code>.</li>
</ul>
<p>Abre PowerShell en la carpeta del proyecto y crea la rama:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
git switch main
git pull
git status
git switch -c interfaz-neon
git branch</pre>
<table class="tabla">
<tr><th>Comando</th><th>Qué hace y por qué</th></tr>
<tr><td><code>cd $HOME\Proyectos\Totito</code></td><td>Te pone en la carpeta del proyecto. Todos los comandos de Git se ejecutan desde ahí.</td></tr>
<tr><td><code>git switch main</code></td><td>Se asegura de que estás en <code>main</code>: la rama nueva nacerá de donde estés parado.</td></tr>
<tr><td><code>git pull</code></td><td>Trae de GitHub lo que haya en <code>main</code> que no tengas (por si trabajaste desde otra computadora). Si dice <code>Already up to date.</code>, no había nada.</td></tr>
<tr><td><code>git status</code></td><td>Debe decir <code>nothing to commit, working tree clean</code>. Si hay cambios sin guardar, haz commit o deséchalos antes (capítulo 9).</td></tr>
<tr><td><code>git switch -c interfaz-neon</code></td><td><code>-c</code> significa <i>create</i>: crea la rama <code>interfaz-neon</code> y te cambia a ella de una vez.</td></tr>
<tr><td><code>git branch</code></td><td>Lista las ramas; el asterisco marca en la que estás. Debe verse <code>* interfaz-neon</code>.</td></tr>
</table>
<p>NetBeans no necesita que hagas nada: trabaja con los archivos de la carpeta, y Git ya los dejó en la rama nueva (que
por ahora es idéntica a <code>main</code>). Si NetBeans estaba abierto, no hace falta cerrarlo.</p>
<div class="caja cuidado"><b>Antes de cada capítulo de esta parte</b> comprueba con <code>git branch</code> que sigues en
<code>interfaz-neon</code>. Si por error haces commits en <code>main</code>, el plan del Pull Request del capítulo 61 se
complica.</div>

<h2>Por qué existe este archivo</h2>
<p>Abre <code>src/JuegoMain.java</code> (capítulo 33) y fíjate en qué cosas hace esa clase. Hace <b>dos trabajos
mezclados</b>:</p>
<ol>
<li><b>Interfaz:</b> crea la ventana, los nueve botones, la etiqueta de estado, los colores, el temporizador.</li>
<li><b>Reglas de la partida:</b> de quién es el turno (<code>turnoJugador</code>), si el juego terminó
(<code>juegoTerminado</code>), qué pasa al marcar una casilla, cuándo juega la IA, cómo se detecta el final.</li>
</ol>
<p>Para la v0.1, con una sola pantalla, esa mezcla era aceptable. La v1.0 tiene cinco pantallas: el menú, las
instrucciones, la configuración, el juego y el resultado. La pantalla de juego necesita las reglas para saber quién
juega; la de resultado necesita saber quién ganó y el marcador; el marcador tiene que sobrevivir a «Jugar de nuevo». Si
las reglas siguieran dentro de una ventana, cada pantalla tendría que meterse en esa ventana o copiar las reglas. Copiar
reglas es la receta de un error clásico: arreglas un fallo en una copia y la otra sigue rota.</p>
<p>La solución es una <b>refactorización</b>: cambiar cómo está organizado el código <b>sin cambiar lo que hace</b>. Se toma
la parte de reglas de <code>JuegoMain</code>, se la mejora un poco (dos jugadores, modo de juego, marcador) y se la mueve a
una clase nueva, <code>Partida</code>, que <b>no importa nada de Swing</b>. Es el principio de responsabilidad única y la
separación entre lógica e interfaz del capítulo 27: <code>Partida</code> es el <i>modelo</i>; las pantallas son la
<i>vista</i>.</p>

<h3>Qué pasó de JuegoMain a Partida</h3>
<table class="tabla">
<tr><th>En JuegoMain (v0.1)</th><th>En Partida (v1.0)</th><th>Por qué cambió</th></tr>
<tr><td><code>boolean turnoJugador</code> (true = humano, false = IA)</td><td><code>int turno</code> (0 = Jugador 1, 1 = Jugador 2)</td><td>Ahora puede haber dos humanos; un número sirve de índice en el arreglo de jugadores.</td></tr>
<tr><td><code>boolean juegoTerminado</code></td><td><code>Estado estado</code> (<code>EN_CURSO</code>, <code>VICTORIA</code>, <code>EMPATE</code>)</td><td>Un booleano dice «terminó», pero no «cómo». La pantalla de resultado necesita saberlo.</td></tr>
<tr><td>Constantes <code>FICHA_JUGADOR = 'X'</code> y <code>FICHA_IA = 'O'</code></td><td>Dos objetos <code>Jugador</code> con la ficha que eligió cada uno, y <code>FICHA_INICIAL = 'X'</code></td><td>En la v1.0 cada jugador elige su símbolo en la configuración.</td></tr>
<tr><td>Siempre contra la IA</td><td><code>Modo modo</code> (<code>DOS_JUGADORES</code> o <code>CONTRA_IA</code>)</td><td>El diseño tiene las dos opciones.</td></tr>
<tr><td>Las comprobaciones de <code>manejarClicCasilla</code> y de <code>verificarFinDePartida</code></td><td>El método <code>jugar(fila, columna)</code></td><td>Una sola puerta de entrada para cualquier jugada, humana o de la IA.</td></tr>
<tr><td><code>turnoIA()</code></td><td><code>esTurnoDeIA()</code> y <code>jugarTurnoIA()</code></td><td>La pausa de 350 ms (un <code>Timer</code>) es cosa de la interfaz y se queda en la pantalla de juego (capítulo 59).</td></tr>
<tr><td>La parte de reglas de <code>reiniciarPartida()</code></td><td><code>reiniciar()</code></td><td>Limpiar los botones es de la interfaz; limpiar el tablero y el estado, de la partida.</td></tr>
<tr><td>(no existía)</td><td>Marcador: <code>victorias[]</code> y <code>empates</code></td><td>Lo pide el diseño de la pantalla de juego.</td></tr>
<tr><td>(no existía)</td><td><code>buscarLineaGanadora()</code></td><td>Para dibujar la raya sobre las tres fichas ganadoras.</td></tr>
</table>
<p>Lo que <b>no</b> pasa a <code>Partida</code>: botones, etiquetas, colores, fuentes, el temporizador. Todo eso irá a
<code>PanelTablero</code> (capítulo 48), <code>PanelMarcador</code> (52) y <code>PantallaJuego</code> (59).</p>

<h3>Las clases originales no se tocan</h3>
<p><code>Tablero</code>, <code>Jugador</code> e <code>IA_Minimax</code> se quedan <b>exactamente como las escribiste</b>: ni
una línea cambia. <code>Partida</code> las <i>usa</i> (composición, capítulo 21: una partida <b>tiene un</b> tablero, dos
jugadores y, a veces, una IA). Hay buenas razones para no tocarlas:</p>
<ul>
<li>Ya están probadas (con <code>PruebaConsola</code>, capítulo 32). Cada cambio en código que funciona es una ocasión de romperlo.</li>
<li>Es el principio «abierto a extensión, cerrado a modificación»: se agrega comportamiento nuevo con clases nuevas.</li>
<li>Por eso <code>buscarLineaGanadora</code> vive en <code>Partida</code> y no en <code>Tablero</code>, aunque «encajaría» allí.</li>
</ul>
<p><code>JuegoMain</code> tampoco se borra: sigue compilando y funcionando como la v0.1. Queda en el proyecto como recuerdo
de dónde partiste y para comparar. El juego nuevo arrancará desde otra clase, <code>TotitoApp</code> (capítulo 61).</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>Cómo se hace una refactorización: separar reglas e interfaz.</li>
<li><code>enum</code> anidados (<code>Partida.Modo</code>, <code>Partida.Estado</code>) para valores fijos con nombre.</li>
<li>Atributos <code>final</code> inicializados en la declaración o en el constructor.</li>
<li>Validar en el constructor y lanzar una excepción (<code>IllegalArgumentException</code>).</li>
<li>El operador ternario <code>? :</code>, el truco <code>turno = 1 - turno</code> y el contador <code>victorias[turno]++</code>.</li>
<li>Por qué un método «devuelve <code>false</code> y no cambia nada» es una forma segura de rechazar una jugada.</li>
<li>Getters de solo lectura y un método <code>static</code> con una tabla de datos (las 8 líneas del totito).</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>Comprueba que estás en la rama <code>interfaz-neon</code> (<code>git branch</code>).</li>
<li>En NetBeans, en el panel <i>Projects</i>, despliega <i>Totito → Source Packages</i>.</li>
<li>Clic derecho en <i>&lt;default package&gt;</i> → <i>New → Java Class…</i></li>
<li>En <i>Class Name</i> escribe <code>Partida</code> (con P mayúscula: el nombre del archivo y el de la clase deben coincidir). Clic en <i>Finish</i>.</li>
<li>NetBeans abre un archivo con una plantilla (un comentario con <code>@author</code> y una clase vacía). <b>Borra todo</b> y escribe el código de abajo.</li>
</ol>
<p>Alternativa con PowerShell (desde la carpeta del proyecto), y luego abrirlo en NetBeans o en VS Code:</p>
<pre class="ps">New-Item src\Partida.java</pre>
<div class="caja consejo">Escríbelo a mano en vez de copiarlo y pegarlo. Teclear te obliga a leer cada símbolo, y los
errores de compilación que cometas (y corrijas) te enseñan más que el código perfecto.</div>
""",
    "archivos": [
        {"ruta": "src/Partida.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1–L13</b> Un comentario de documentación (Javadoc): empieza con <code>/**</code>, termina con
<code>*/</code> y cada línea intermedia suele empezar con <code>*</code> por estética. El compilador lo ignora; es para las
personas. Dice qué es la clase («una serie de partidas»: no una sola, porque el marcador se acumula), qué clases
originales reutiliza y la regla más importante del archivo (L10–L12): <b>no sabe nada de la interfaz gráfica</b>. Fíjate
en que los comentarios del código no llevan tildes: así se evitan problemas si alguien abre el archivo con otra
codificación. Si borraras el comentario, el programa funcionaría igual, pero dentro de seis meses no recordarías por qué
existe esta clase.</p>
<p class="l"><b>L14</b> Declara la clase. <code>public</code>: cualquier otra clase del proyecto puede usarla (la usarán
<code>PanelPrincipal</code>, <code>PantallaJuego</code>, <code>PanelMarcador</code>…). <code>class Partida</code>: el
molde de los objetos «partida». La llave <code>{</code> abre el cuerpo, que se cierra en la última línea del archivo
(L160). Observa que <b>no hay ningún <code>import</code></b> arriba: no usa nada de <code>javax.swing</code> ni de
<code>java.awt</code>. Esa ausencia es la prueba de que la lógica está separada de la interfaz.</p>
"""),
             ("public enum Modo", r"""
<p class="l"><b>L16</b> Comentario corto de una línea en formato Javadoc: explica el enum que viene.</p>
<p class="l"><b>L17</b> <code>enum</code> (capítulo 26) declara un tipo con una lista <b>cerrada</b> de valores con
nombre. Está <b>dentro</b> de <code>Partida</code> (anidado), así que su nombre completo es <code>Partida.Modo</code>: se
lee «el modo de una partida». Es <code>public</code> para que la pantalla de configuración pueda escribir
<code>Partida.Modo.CONTRA_IA</code>.</p>
<p class="l"><b>L18–L21</b> Los dos valores posibles, separados por coma, cada uno con su comentario.
<code>DOS_JUGADORES</code>: dos personas en la misma computadora. <code>CONTRA_IA</code>: el Jugador 2 es la máquina.
Se escriben en MAYÚSCULAS porque son constantes. ¿Por qué no usar un <code>boolean contraIA</code> o un número
(<code>1</code>, <code>2</code>)? Con un número alguien podría pasar un <code>7</code> y el compilador no se quejaría;
con un enum, solo existen estos dos valores, y el código se lee solo: <code>modo == Modo.CONTRA_IA</code>.</p>
<p class="l"><b>L22</b> Cierra el enum.</p>
"""),
             ("public enum Estado", r"""
<p class="l"><b>L24</b> Comentario: el estado de la partida <b>actual</b> (no de la serie).</p>
<p class="l"><b>L25</b> Otro enum, escrito en una sola línea porque sus valores no necesitan comentario:
<code>EN_CURSO</code> (se sigue jugando), <code>VICTORIA</code> (alguien hizo tres en línea), <code>EMPATE</code> (tablero
lleno sin ganador). Reemplaza al <code>boolean juegoTerminado</code> de <code>JuegoMain</code>: un booleano solo tenía
dos casos y aquí hay tres. Las pantallas preguntan <code>partida.getEstado()</code> y, con un <code>switch</code>, deciden
qué letrero mostrar (capítulo 59).</p>
"""),
             ("public static final char FICHA_INICIAL", r"""
<p class="l"><b>L27</b> Comentario: la X abre cada partida, «como en el totito de siempre».</p>
<p class="l"><b>L28</b> Una <b>constante</b> (capítulo 20). <code>public</code>: visible desde fuera.
<code>static</code>: pertenece a la clase, no a cada objeto (hay una sola <code>FICHA_INICIAL</code>, aunque haya muchas
partidas). <code>final</code>: no se puede cambiar después. <code>char</code>: un solo carácter, entre comillas simples
<code>'X'</code>. Ponerle nombre a ese <code>'X'</code> evita un «número mágico» (capítulo 27): si un día quieres que
abra la O, cambias esta línea y nada más.</p>
"""),
             ("private final Tablero tablero = new Tablero();", r"""
<p class="l"><b>L30</b> El tablero de la partida. <code>private</code>: nadie de afuera puede tocar el atributo
directamente (encapsulamiento, capítulo 19). <code>final</code>: la variable siempre apunta al <b>mismo</b> objeto
<code>Tablero</code>; su contenido (las casillas) sí cambia, pero nunca se reemplaza por otro tablero.
<code>= new Tablero()</code>: se crea en la misma declaración. Java ejecuta estas inicializaciones <b>antes</b> del cuerpo
del constructor, así que cuando el constructor empiece, el tablero ya existe.</p>
<p class="l"><b>L31</b> Un arreglo con los dos jugadores. Sin <code>= ...</code>: se le dará valor en el constructor.
Un atributo <code>final</code> sin valor obliga a que <b>todo</b> constructor se lo asigne exactamente una vez; si se te
olvida, el compilador da el error <code>variable jugadores might not have been initialized</code>. Es una red de seguridad
gratuita. ¿Por qué un arreglo y no dos atributos <code>jugador1</code> y <code>jugador2</code>? Porque con
<code>turno</code> valiendo 0 o 1, <code>jugadores[turno]</code> da directamente al jugador en turno, sin <code>if</code>.</p>
<p class="l"><b>L32</b> El modo elegido. Tampoco cambia durante la serie: para cambiar de modo hay que volver a la
configuración, que crea una <code>Partida</code> nueva.</p>
<p class="l"><b>L33–L34</b> La inteligencia artificial del capítulo 31. El comentario avisa de algo importante: en el
modo de dos jugadores este atributo vale <code>null</code> (no hay objeto). Otros métodos lo comprueban con
<code>ia != null</code>.</p>
<p class="l"><b>L35</b> El marcador de victorias: <code>new int[2]</code> crea un arreglo de dos enteros, ambos en 0 (Java
llena de ceros los arreglos de números). <code>victorias[0]</code> son las del Jugador 1 y <code>victorias[1]</code> las
del Jugador 2. Va en paralelo con <code>jugadores</code>: el mismo índice, la misma persona.</p>
<p class="l"><b>L36</b> Cuántas partidas terminaron empatadas. Un atributo <code>int</code> sin valor empieza en 0. No es
<code>final</code> porque irá creciendo.</p>
"""),
             ("private int turno;", r"""
<p class="l"><b>L38–L39</b> A quién le toca: 0 o 1, el índice dentro de <code>jugadores</code>. No es <code>final</code>
porque cambia en cada jugada. Desde aquí empiezan los atributos que describen la partida <b>actual</b>; los de arriba
describen la <b>serie</b> completa.</p>
<p class="l"><b>L40</b> El estado de la partida actual (un valor del enum <code>Estado</code>).</p>
<p class="l"><b>L41</b> Quién ganó la partida actual, o <code>null</code> si sigue en curso o fue empate. Guardar el
<code>Jugador</code> (y no solo su ficha) permite a la pantalla de resultado escribir su nombre: «¡Ganó Ana!».</p>
"""),
             ("public Partida(Jugador jugador1", r"""
<p class="l"><b>L43</b> El <b>constructor</b> (capítulo 20): tiene el mismo nombre que la clase y no lleva tipo de
retorno. Se ejecuta con <code>new Partida(ana, beto, Partida.Modo.DOS_JUGADORES)</code>. Recibe tres parámetros: los dos
jugadores y el modo. Quien lo llamará es <code>PanelPrincipal</code> (capítulo 61), con lo que se eligió en la pantalla de
configuración.</p>
<p class="l"><b>L44</b> Una <b>validación</b>: si los dos jugadores tienen la misma ficha, la partida no tendría sentido
(¿de quién serían las X?). <code>getFicha()</code> es el getter de <code>Jugador</code> (capítulo 30) y
<code>==</code> compara dos <code>char</code>.</p>
<p class="l"><b>L45</b> <code>throw</code> lanza una excepción (capítulo 26) y corta el constructor en seco: la partida
<b>no llega a existir</b>. <code>IllegalArgumentException</code> es la excepción estándar de Java para «me pasaste un
argumento que no vale», y el texto explica el motivo. ¿Por qué no simplemente ignorarlo? Porque un objeto construido con
datos imposibles produciría errores raros mucho después, lejos de la causa. Es mejor fallar pronto y con un mensaje claro.
La pantalla de configuración nunca permitirá esa combinación (capítulo 50), así que esta línea es un seguro contra
errores de programación, no contra el usuario.</p>
<p class="l"><b>L47</b> Crea el arreglo y lo llena en una sola expresión: <code>new Jugador[]{jugador1, jugador2}</code>.
<code>this.jugadores</code> se refiere al atributo de L31; <code>this</code> significa «este objeto». Aquí no hay
parámetro con el mismo nombre, así que <code>this.</code> no es obligatorio, pero deja claro que se está asignando un
atributo.</p>
<p class="l"><b>L48</b> Guarda el modo. Aquí <code>this.</code> <b>sí</b> es obligatorio: el parámetro también se llama
<code>modo</code> y, sin <code>this</code>, la línea <code>modo = modo</code> se asignaría el parámetro a sí mismo y el
atributo quedaría sin valor (el compilador lo detectaría por ser <code>final</code>).</p>
<p class="l"><b>L49</b> El <b>operador ternario</b>: <code>condición ? valorSiSí : valorSiNo</code>. Se lee: «si el modo
es contra la IA, crea una <code>IA_Minimax</code>; si no, <code>null</code>». Fíjate en el orden de los argumentos:
<code>IA_Minimax(fichaIA, fichaJugador)</code> (capítulo 31) recibe primero la ficha de la máquina. Como la IA siempre es
el Jugador 2, va <code>jugador2.getFicha()</code> primero. Si los invirtieras, la IA jugaría con las fichas al revés y
pensaría que tus jugadas son suyas.</p>
<p class="l"><b>L50</b> Llama a <code>reiniciar()</code> (L54) para dejar el tablero vacío, el estado en curso y el primer
turno decidido. Así el constructor no repite ese código: hay un solo lugar donde se prepara una partida.</p>
"""),
             ("public void reiniciar()", r"""
<p class="l"><b>L53</b> Comentario: limpia el tablero, pero <b>conserva el marcador</b>. Es lo que hace el botón
«Jugar de nuevo».</p>
<p class="l"><b>L54</b> Método <code>public</code> (lo llaman las pantallas) y <code>void</code> (no devuelve nada; solo
cambia el estado del objeto).</p>
<p class="l"><b>L55</b> Delegación: no se reinventa cómo vaciar casillas, se le pide al <code>Tablero</code> con su propio
método <code>reiniciar()</code> (capítulo 29).</p>
<p class="l"><b>L56</b> La partida vuelve a estar en curso. <code>Estado.EN_CURSO</code> se escribe sin
<code>Partida.</code> delante porque estamos dentro de la clase.</p>
<p class="l"><b>L57</b> Borra al ganador anterior. Sin esta línea, al empezar la segunda partida
<code>getGanador()</code> seguiría devolviendo al ganador de la primera.</p>
<p class="l"><b>L58</b> ¿Quién abre? Otro ternario: si la ficha del Jugador 1 es la <code>FICHA_INICIAL</code> (X), turno
0; si no, turno 1. Ejemplo: si Ana (Jugador 1) eligió la O y Beto la X, empieza Beto. Así se respeta la regla «siempre
abre la X» sin importar quién la tenga. Fíjate en que <code>victorias</code> y <code>empates</code> no aparecen: el
marcador no se toca.</p>
"""),
             ("public boolean jugar(", r"""
<p class="l"><b>L61–L65</b> El comentario documenta el <b>contrato</b> del método: qué hace (coloca la ficha del jugador
en turno), qué devuelve y una garantía importante: «en ese caso no cambia nada». Quien llama sabe que una jugada
rechazada no deja la partida a medias.</p>
<p class="l"><b>L66</b> <b>El corazón de la clase.</b> Recibe la fila y la columna (de 0 a 2) y devuelve un
<code>boolean</code>: <code>true</code> si la jugada se hizo, <code>false</code> si no. No recibe la ficha: la decide
la partida según el turno. Así es imposible que una pantalla juegue la ficha equivocada.</p>
<p class="l"><b>L67–L69</b> Primera condición de rechazo: si la partida ya terminó, no se aceptan más jugadas.
<code>!=</code> significa «distinto de». <code>return false;</code> sale del método inmediatamente; nada de lo que
sigue se ejecuta. Esta técnica (salir pronto ante los casos inválidos) se llama <i>cláusula de guarda</i> y evita
anidar <code>if</code> dentro de <code>if</code>.</p>
<p class="l"><b>L70</b> Segunda guarda, que además <b>hace</b> la jugada. <code>jugadores[turno].getFicha()</code> es la
ficha de quien tiene el turno. <code>tablero.marcarCasilla(...)</code> (capítulo 29) intenta colocarla y devuelve
<code>false</code> si la casilla está fuera de rango u ocupada. El <code>!</code> invierte el resultado: «si NO se pudo
marcar…».</p>
<p class="l"><b>L71</b> …devuelve <code>false</code>. Como <code>marcarCasilla</code> no cambia nada cuando falla, la
garantía del comentario se cumple.</p>
"""),
             ("if (tablero.verificarGanador() != Tablero.VACIA)", r"""
<p class="l"><b>L73</b> Si llegamos aquí, la ficha ya está puesta. <code>verificarGanador()</code> (capítulo 29) revisa
las 8 líneas y devuelve la ficha ganadora o <code>Tablero.VACIA</code> (un espacio) si nadie ganó. «Distinto de vacía»
significa «alguien ganó». Y ese alguien solo puede ser quien acaba de jugar: antes de esta jugada nadie había ganado
(si no, la guarda de L67 la habría rechazado).</p>
<p class="l"><b>L74</b> La partida pasa a <code>VICTORIA</code>.</p>
<p class="l"><b>L75</b> El ganador es el jugador en turno. Fíjate en que <code>turno</code> <b>no</b> se cambia: queda
apuntando al ganador.</p>
<p class="l"><b>L76</b> Suma uno a sus victorias. <code>victorias[turno]++</code> es lo mismo que
<code>victorias[turno] = victorias[turno] + 1</code>.</p>
"""),
             ("} else if (tablero.tableroLleno())", r"""
<p class="l"><b>L77</b> Si nadie ganó, ¿se llenó el tablero? <code>else if</code> solo se evalúa cuando la condición
anterior fue falsa. El orden importa: si la novena ficha completa una línea, es victoria, no empate; por eso se pregunta
primero por el ganador.</p>
<p class="l"><b>L78–L79</b> Empate: cambia el estado y suma uno a <code>empates</code> (el <code>++</code> de un
atributo).</p>
<p class="l"><b>L80–L81</b> Si no hubo ni victoria ni empate, la partida sigue y el turno pasa al otro.
<code>turno = 1 - turno</code> es un truco aritmético: si <code>turno</code> vale 0, queda 1 − 0 = 1; si vale 1, queda
1 − 1 = 0. Alterna sin necesidad de <code>if</code>.</p>
<p class="l"><b>L82–L84</b> Cierra el <code>if</code> y devuelve <code>true</code>: la jugada se aplicó. Cierra el método.</p>
"""),
             ("public boolean esTurnoDeIA", r"""
<p class="l"><b>L86–L87</b> Pregunta si la computadora debe mover ahora. Devuelve <code>true</code> solo si se cumplen
<b>las tres</b> condiciones a la vez (<code>&amp;&amp;</code> es el «y» lógico).</p>
<p class="l"><b>L88</b> <code>ia != null</code>: hay IA (modo contra la IA). <code>turno == 1</code>: le toca al Jugador 2,
que es la IA. <code>estado == Estado.EN_CURSO</code>: la partida no terminó. El orden también importa: Java evalúa de
izquierda a derecha y se detiene en el primer <code>false</code> (evaluación en cortocircuito). La pantalla de juego usa
este método para bloquear los clics del humano mientras «piensa» la máquina (capítulo 59).</p>
"""),
             ("public void jugarTurnoIA", r"""
<p class="l"><b>L91–L92</b> Pide a la IA su jugada y la aplica.</p>
<p class="l"><b>L93–L95</b> Guarda: si no le toca a la IA, no hace nada (<code>return;</code> sin valor, porque el método
es <code>void</code>). Protege contra una llamada a destiempo, por ejemplo un temporizador que dispara cuando la
partida ya terminó.</p>
<p class="l"><b>L96</b> <code>calcularMejorJugada</code> (capítulo 31) recibe el tablero y devuelve un arreglo
<code>{fila, columna}</code>. Como la guarda aseguró que la partida sigue en curso, siempre hay al menos una casilla
vacía, así que la jugada es válida (en <code>JuegoMain</code> se comprobaba el caso <code>-1</code>; aquí no hace falta, y
aunque llegara, <code>marcarCasilla</code> lo rechazaría por estar fuera de rango).</p>
<p class="l"><b>L97</b> Aplica la jugada con <b>el mismo</b> <code>jugar()</code> que usa el humano. Así la IA no tiene
reglas especiales: cambia el turno, detecta victorias y suma al marcador exactamente igual. Un solo camino para todas las
jugadas significa un solo lugar donde pueden estar los errores.</p>
"""),
             ("public boolean esComputadora", r"""
<p class="l"><b>L100–L101</b> Dice si un jugador es la computadora.</p>
<p class="l"><b>L102</b> Hay IA y el jugador es el segundo. Aquí <code>==</code> compara <b>referencias</b>: pregunta si
es <i>el mismo objeto</i>, no si tiene el mismo nombre (capítulo 18). Es justo lo que queremos: si alguien escribiera
«Computadora» como nombre del Jugador 1, no lo confundiríamos. La pantalla de resultado lo usa para escribir «La máquina
no perdona» cuando gana la IA (capítulo 60).</p>
"""),
             ("public Tablero getTablero()", r"""
<p class="l"><b>L105–L107</b> Getter (capítulo 19): da acceso al tablero para que la interfaz lo dibuje. Ojo: devuelve el
tablero real, no una copia; las pantallas lo usan solo para leer con <code>obtenerCasilla</code>. Para jugar deben pasar
por <code>jugar()</code>.</p>
<p class="l"><b>L109–L111</b> El jugador en la posición 0 o 1. Lo usa el marcador (capítulo 52) para escribir los dos
nombres.</p>
<p class="l"><b>L113–L115</b> Quién tiene el turno, para el letrero «Turno de Ana».</p>
<p class="l"><b>L117–L119</b> El modo de juego. Hay getters, pero <b>ningún setter</b>: desde afuera se puede consultar la
partida, pero solo se puede modificar con <code>jugar</code>, <code>jugarTurnoIA</code> y <code>reiniciar</code>, que
respetan las reglas.</p>
"""),
             ("public Estado getEstado()", r"""
<p class="l"><b>L121–L123</b> Cómo va la partida.</p>
<p class="l"><b>L125–L128</b> El ganador. El comentario advierte que puede ser <code>null</code>, así que quien lo use
debe mirar antes el estado. Documentar cuándo un método devuelve <code>null</code> evita el famoso
<code>NullPointerException</code>.</p>
<p class="l"><b>L130–L132</b> Victorias del jugador 0 o 1.</p>
<p class="l"><b>L134–L136</b> Número de empates. Estos dos getters alimentan el marcador «Ana 2 · Empates 1 · Beto 0».</p>
"""),
             ("public static int[] buscarLineaGanadora", r"""
<p class="l"><b>L138–L143</b> Explica el método: además de saber <b>que</b> alguien ganó, la interfaz necesita saber
<b>dónde</b> está la línea para dibujar la raya neón sobre las tres fichas. Devuelve un arreglo de cuatro números
<code>{filaInicio, columnaInicio, filaFin, columnaFin}</code> o <code>null</code>.</p>
<p class="l"><b>L144</b> Es <code>static</code>: no usa ningún atributo de la partida, solo el <code>Tablero</code> que
recibe. Por eso se llama <code>Partida.buscarLineaGanadora(tablero)</code>, sin objeto. Le sirve a
<code>PanelTablero</code> (capítulo 48), que solo tiene un tablero en la mano, no una partida. Devuelve
<code>int[]</code>: un arreglo de enteros.</p>
"""),
             ("int[][] lineas = {", r"""
<p class="l"><b>L145</b> Una <b>tabla de datos</b>: un arreglo de arreglos (capítulo 15). Cada fila describe una línea
ganadora con seis números, tres pares (fila, columna).</p>
<p class="l"><b>L146</b> Las tres filas. <code>{0, 0, 0, 1, 0, 2}</code> son las casillas (0,0), (0,1) y (0,2): la fila
de arriba. El comentario <code>// filas</code> al final de la línea ayuda a leer la tabla.</p>
<p class="l"><b>L147</b> Las tres columnas: <code>{0, 0, 1, 0, 2, 0}</code> es (0,0), (1,0), (2,0), la columna izquierda.</p>
<p class="l"><b>L148</b> Las dos diagonales: de arriba-izquierda a abajo-derecha y de arriba-derecha a abajo-izquierda.</p>
<p class="l"><b>L149</b> Cierra la tabla. Comparado con los <code>if</code> de <code>verificarGanador</code>, una tabla es
más fácil de revisar: ves las 8 líneas de un vistazo y un error salta a la vista. Esta técnica (datos en vez de
<code>if</code> repetidos) se llama <i>programación dirigida por tablas</i>.</p>
"""),
             ("for (int[] l : lineas)", r"""
<p class="l"><b>L150</b> Un <i>for-each</i> (capítulo 14): «para cada línea <code>l</code> de la tabla». En cada vuelta,
<code>l</code> es uno de los arreglos de seis números.</p>
<p class="l"><b>L151</b> Lee la ficha de la primera casilla de esa línea y la guarda en <code>a</code>.</p>
<p class="l"><b>L152–L154</b> Una condición repartida en tres líneas para que se lea mejor (los <code>&amp;&amp;</code>
al inicio de cada línea indican que continúa). Hay ganador en esta línea si la primera casilla no está vacía <b>y</b> es
igual a la segunda <b>y</b> es igual a la tercera. Comprobar primero que no está vacía es esencial: tres casillas vacías
también son «iguales».</p>
<p class="l"><b>L155</b> Encontrada: devuelve la primera casilla (<code>l[0], l[1]</code>) y la última
(<code>l[4], l[5]</code>). La del medio no hace falta: para dibujar una raya basta con sus dos extremos.</p>
<p class="l"><b>L158</b> Si el bucle termina sin encontrar nada, nadie ha ganado: <code>null</code>.</p>
<p class="l"><b>L159–L160</b> Cierran el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<p><code>Partida</code> es una pequeña <b>máquina de estados</b>: la partida está en curso hasta que una jugada la lleva a
victoria o a empate; desde ahí solo <code>reiniciar()</code> la devuelve a «en curso». Mientras tanto, el marcador se
acumula.</p>
<pre class="texto">                 jugar() válida, nadie gana
                ┌──────────────┐
                ▼              │
  reiniciar() ► EN_CURSO ──────┘
                │      │
     3 en línea │      │ tablero lleno
                ▼      ▼
           VICTORIA   EMPATE ── reiniciar() ──► EN_CURSO
           (victorias[turno]++)  (empates++)</pre>
<p>Sigamos una partida con valores concretos. Ana es el Jugador 1 y eligió la <b>O</b>; Beto es el Jugador 2 y tiene la
<b>X</b>; modo <code>DOS_JUGADORES</code>.</p>
<table class="tabla">
<tr><th>Llamada</th><th>Qué pasa dentro</th><th>turno</th><th>estado</th><th>Devuelve</th></tr>
<tr><td><code>new Partida(ana, beto, DOS_JUGADORES)</code></td><td>Fichas distintas: pasa la validación. <code>ia = null</code>. <code>reiniciar()</code>: la ficha de Ana no es X, así que abre Beto.</td><td>1</td><td>EN_CURSO</td><td>—</td></tr>
<tr><td><code>jugar(0, 0)</code></td><td>Beto pone X en (0,0). Nadie gana, no está lleno: <code>turno = 1 - 1 = 0</code>.</td><td>0</td><td>EN_CURSO</td><td>true</td></tr>
<tr><td><code>jugar(1, 1)</code></td><td>Ana pone O en el centro. Turno a Beto.</td><td>1</td><td>EN_CURSO</td><td>true</td></tr>
<tr><td><code>jugar(0, 1)</code></td><td>Beto: X en (0,1). Turno a Ana.</td><td>0</td><td>EN_CURSO</td><td>true</td></tr>
<tr><td><code>jugar(2, 2)</code></td><td>Ana: O en (2,2). Turno a Beto.</td><td>1</td><td>EN_CURSO</td><td>true</td></tr>
<tr><td><code>jugar(0, 0)</code></td><td><code>marcarCasilla</code> falla: la casilla ya tiene X. No cambia nada.</td><td>1</td><td>EN_CURSO</td><td>false</td></tr>
<tr><td><code>jugar(0, 2)</code></td><td>Beto: X en (0,2). <code>verificarGanador()</code> devuelve X: VICTORIA, <code>ganador = beto</code>, <code>victorias[1]</code> pasa a 1.</td><td>1</td><td>VICTORIA</td><td>true</td></tr>
<tr><td><code>buscarLineaGanadora(tablero)</code></td><td>La primera fila de la tabla (0,0)(0,1)(0,2) tiene tres X.</td><td>—</td><td>—</td><td><code>{0, 0, 0, 2}</code></td></tr>
<tr><td><code>jugar(2, 0)</code></td><td>La guarda de L67 la rechaza: la partida terminó.</td><td>1</td><td>VICTORIA</td><td>false</td></tr>
<tr><td><code>reiniciar()</code></td><td>Tablero vacío, ganador <code>null</code>, vuelve a abrir Beto. <code>victorias</code> sigue en {0, 1}.</td><td>1</td><td>EN_CURSO</td><td>—</td></tr>
</table>
<p>En el modo <code>CONTRA_IA</code> la diferencia es que, después de cada jugada del humano,
<code>esTurnoDeIA()</code> devuelve <code>true</code> y la pantalla llama a <code>jugarTurnoIA()</code>, que termina
llamando al mismo <code>jugar()</code>. La partida no sabe ni le importa que haya una pausa de por medio: eso es asunto de
la interfaz.</p>

<h2>Compila y prueba</h2>
<p>Todavía no hay ninguna pantalla nueva que mirar (la primera aparece en el capítulo 56). Lo que compruebas hoy es que el
proyecto <b>compila</b>:</p>
<ol>
<li>Guarda el archivo (Ctrl+S).</li>
<li><i>Run → Clean and Build Project</i> (Shift+F11).</li>
<li>En la ventana <i>Output</i>, abajo, debe aparecer <code>BUILD SUCCESS</code>.</li>
</ol>
<p>Sin NetBeans, desde PowerShell (compila todo <code>src</code> en la carpeta <code>out</code>, que está en el
<code>.gitignore</code>):</p>
<pre class="ps">javac -encoding UTF-8 -d out src\*.java</pre>
<p>Si no aparece ningún mensaje, compiló bien.</p>

<h3>Prueba opcional: jugar una partida «a ciegas»</h3>
<p>Como <code>Partida</code> no necesita ventanas, puedes probarla con un programa de consola. Crea un archivo
<b>temporal</b> en la carpeta raíz del proyecto (no en <code>src</code>, para que no forme parte del juego):</p>
<pre class="ps">New-Item ProbarPartida.java</pre>
<p>Ábrelo con el Bloc de notas (<code>notepad ProbarPartida.java</code>) y escribe:</p>
<pre class="java">public class ProbarPartida {
    public static void main(String[] args) {
        Jugador ana = new Jugador("Ana", 'O');
        Jugador beto = new Jugador("Beto", 'X');
        Partida p = new Partida(ana, beto, Partida.Modo.DOS_JUGADORES);
        System.out.println("Empieza: " + p.getJugadorEnTurno().getNombre());
        p.jugar(0, 0);   // Beto (X)
        p.jugar(1, 1);   // Ana (O)
        p.jugar(0, 1);   // Beto (X)
        p.jugar(2, 2);   // Ana (O)
        System.out.println("Casilla ocupada? " + p.jugar(0, 0));
        p.jugar(0, 2);   // Beto (X) gana
        System.out.println("Estado: " + p.getEstado());
        System.out.println("Ganador: " + p.getGanador().getNombre());
        System.out.println("Marcador: Ana " + p.getVictorias(0) + " - Beto " + p.getVictorias(1));
        System.out.println("Linea: " + java.util.Arrays.toString(Partida.buscarLineaGanadora(p.getTablero())));
        System.out.println("Otra jugada? " + p.jugar(2, 0));
        p.reiniciar();
        System.out.println("Tras reiniciar: " + p.getEstado() + ", marcador Beto " + p.getVictorias(1));
    }
}</pre>
<p>Después de un <i>Clean and Build</i> (que deja las clases compiladas en <code>target\classes</code>), ejecútalo así,
igual que <code>PruebaConsola</code> en el capítulo 32:</p>
<pre class="ps">java -cp target\classes ProbarPartida.java</pre>
<pre class="salida">Empieza: Beto
Casilla ocupada? false
Estado: VICTORIA
Ganador: Beto
Marcador: Ana 0 - Beto 1
Linea: [0, 0, 0, 2]
Otra jugada? false
Tras reiniciar: EN_CURSO, marcador Beto 1</pre>
<p>Es exactamente la traza de la tabla de arriba. Cuando termines, borra el archivo para que no se cuele en el commit:</p>
<pre class="ps">Remove-Item ProbarPartida.java</pre>

<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Mensaje</th><th>Causa y solución</th></tr>
<tr><td><code>class Partida is public, should be declared in a file named Partida.java</code></td><td>El archivo se llama distinto que la clase (por ejemplo <code>partida.java</code>). Renómbralo: en Java las mayúsculas cuentan.</td></tr>
<tr><td><code>cannot find symbol: class Tablero</code></td><td>Falta <code>Tablero.java</code> en <code>src</code> o tiene otro nombre. Debe estar desde el capítulo 29.</td></tr>
<tr><td><code>variable jugadores might not have been initialized</code></td><td>Borraste o escribiste mal la línea 47. Un atributo <code>final</code> debe recibir valor en el constructor.</td></tr>
<tr><td><code>';' expected</code></td><td>Falta un punto y coma al final de la línea indicada (o de la anterior).</td></tr>
<tr><td><code>: expected</code> en la línea 49</td><td>Al ternario le faltan los dos puntos: debe ser <code>? new IA_Minimax(...) : null;</code>.</td></tr>
<tr><td><code>variable modo might not have been initialized</code></td><td>Escribiste <code>modo = modo;</code> sin <code>this.</code> en la línea 48: el parámetro se asigna a sí mismo y el atributo <code>final</code> queda vacío.</td></tr>
</table>

<div class="caja git"><b>Git</b> Primer commit de la rama <code>interfaz-neon</code>. Como la rama todavía no existe en
GitHub, el primer <code>push</code> lleva <code>-u origin interfaz-neon</code>: crea la rama remota y la deja
«enlazada» con la tuya, de modo que en los próximos capítulos baste con <code>git push</code>.
<pre class="ps">git branch
git status
git add src\Partida.java
git commit -m "Partida: turnos y marcador"
git push -u origin interfaz-neon</pre>
<code>git status</code> debe mostrar solo <code>src/Partida.java</code> como archivo nuevo (si aparece
<code>ProbarPartida.java</code>, bórralo antes). En GitHub, en la página del repositorio, el selector de ramas mostrará
ahora <code>interfaz-neon</code>; puede aparecer un aviso amarillo ofreciendo abrir un Pull Request: ignóralo por ahora, se
abrirá en el capítulo 61.</div>

<h2>Resumen</h2>
<ul>
<li>La Parte VII se trabaja en la rama <code>interfaz-neon</code>; <code>main</code> conserva la v0.1.0 hasta el Pull Request del capítulo 61.</li>
<li>Refactorizar es reorganizar el código sin cambiar lo que hace: las reglas salieron de <code>JuegoMain</code> y viven en <code>Partida</code>, que no usa Swing.</li>
<li><code>Tablero</code>, <code>Jugador</code> e <code>IA_Minimax</code> no cambian; <code>Partida</code> los compone.</li>
<li>Los enums <code>Modo</code> y <code>Estado</code> reemplazan booleanos y números sueltos por valores con nombre.</li>
<li><code>jugar()</code> es la única puerta para cualquier jugada: rechaza con <code>false</code> sin cambiar nada, o aplica la jugada y actualiza estado, ganador, marcador y turno.</li>
<li>El marcador (<code>victorias</code>, <code>empates</code>) sobrevive a <code>reiniciar()</code>.</li>
<li><code>buscarLineaGanadora</code> usa una tabla con las 8 líneas para decir dónde dibujar la raya.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b> Separar «las reglas» de «la pantalla» es lo primero que se hace
en casi cualquier programa serio:
<ul>
<li><b>Una caja registradora:</b> una clase <code>Venta</code> con <code>agregarProducto()</code>, <code>total()</code> y un estado (<code>ABIERTA</code>, <code>PAGADA</code>, <code>ANULADA</code>) que no sabe si la muestra una ventana, una página web o un ticket impreso.</li>
<li><b>Un juego de Conecta 4:</b> una clase <code>PartidaConecta4</code> con <code>soltarFicha(columna)</code> que devuelve <code>false</code> si la columna está llena, y la misma idea de turno <code>1 - turno</code>.</li>
<li><b>Un sistema de préstamos de biblioteca:</b> un enum <code>EstadoLibro { DISPONIBLE, PRESTADO, PERDIDO }</code> y un método <code>prestar()</code> que lanza <code>IllegalArgumentException</code> si el libro no está disponible.</li>
<li><b>Cualquier programa con «otra vez»:</b> distinguir lo que se reinicia (el tablero, el carrito) de lo que se acumula (el marcador, el historial de ventas).</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>En <code>ProbarPartida.java</code>, crea una partida <code>CONTRA_IA</code> en la que tú tengas la X, juega el centro
<code>(1, 1)</code> y llama a <code>jugarTurnoIA()</code>. Imprime el tablero con dos <code>for</code> y
<code>obtenerCasilla</code>. ¿Dónde jugó la IA? Pista: Minimax responde a un centro con una esquina.</li>
<li>Intenta crear <code>new Partida(new Jugador("A", 'X'), new Jugador("B", 'X'), Partida.Modo.DOS_JUGADORES)</code>
dentro de un <code>try/catch</code> e imprime <code>e.getMessage()</code>. ¿Qué texto sale?</li>
<li>Agrega en tu prueba (no en <code>Partida</code>) una serie de jugadas que termine en empate y comprueba que
<code>getEmpates()</code> vale 1 y <code>getGanador()</code> es <code>null</code>.</li>
<li>Piensa: si cambiaras <code>FICHA_INICIAL</code> a <code>'O'</code>, ¿qué línea de <code>reiniciar()</code> cambia su
resultado y quién abriría en la traza de este capítulo?</li>
<li>Reto: escribe en papel cómo agregarías un método <code>getPartidasJugadas()</code> que devuelva el total de partidas
terminadas, usando solo los atributos que ya existen. Pista: victorias de los dos más empates.</li>
</ol></div>
""",
}
