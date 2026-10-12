# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 31,
    "titulo": "El algoritmo Minimax e IA_Minimax.java",
    "antes": r"""
<p class="entrada">Este es el capítulo más interesante de la Parte V: vas a escribir una inteligencia artificial que juega al totito sin perder jamás. No usa trucos ni una lista de jugadas aprendidas de memoria; usa una idea de 1928, el algoritmo <b>Minimax</b>, que imagina todas las partidas posibles y elige la jugada que mejor resultado garantiza. Primero entenderás la idea a fondo, con dibujos y números; después, el código línea por línea resultará casi una traducción.</p>

<h2>Por qué existe este archivo</h2>
<p>En el capítulo 28 decidimos que la decisión de la computadora merecía su propia clase. Hay dos razones. La primera es que es la parte más difícil del programa, y aislada se entiende mejor y no ensucia a las demás. La segunda es que la ventana no necesita saber <i>cómo</i> piensa la IA: solo le pide «dame tu jugada» y recibe una fila y una columna. Si un día quisieras una IA más fácil (una que a veces se equivoque, para que los niños puedan ganar), escribirías otra clase con el mismo método y la ventana ni se enteraría.</p>
<p><code>IA_Minimax</code> solo depende de <code>Tablero</code>: usa <code>obtenerCasilla</code> para ver qué casillas están libres, <code>obtenerCopia</code> y <code>marcarCasilla</code> para imaginar jugadas, y <code>verificarGanador</code> y <code>tableroLleno</code> para saber cuándo una partida imaginada terminó. Todo eso ya lo escribiste en el capítulo 29.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>Qué es un juego de suma cero y por qué el totito se puede «resolver» por completo.</li>
<li>Qué es un árbol de juego, y cómo se puntúan sus hojas y se suben los valores con MAX y MIN.</li>
<li>Por qué el puntaje resta la profundidad.</li>
<li>Cómo funciona la <b>recursión</b> en un caso real: un método que se llama a sí mismo con un problema más pequeño.</li>
<li>Cuántas partidas de totito existen y cuánto trabajo hace la IA.</li>
<li>Por qué esta IA no puede perder.</li>
<li>Detalles de Java: métodos <code>private</code>, devolver un arreglo <code>int[]</code>, <code>Integer.MIN_VALUE</code>, <code>Math.max</code> y <code>Math.min</code>.</li>
</ul>

<h2>La idea: pensar como un jugador que nunca se equivoca</h2>
<p>Cuando juegas totito con alguien, haces sin darte cuenta algo así: «si pongo aquí, él puede poner allá y me gana; mejor pongo acá, porque entonces él tiene que tapar y yo gano por el otro lado». Es decir, <b>imaginas</b> tu jugada, imaginas la respuesta del otro, imaginas tu respuesta a su respuesta… y eliges la jugada que mejor te deja. Las personas solo podemos imaginar dos o tres jugadas hacia adelante. Una computadora puede imaginar <b>todas</b> hasta el final de la partida, porque en el totito no son tantas. Minimax es ese razonamiento, escrito con precisión.</p>

<h2>Qué clase de juego es el totito</h2>
<p>Minimax funciona en juegos con estas características, y el totito las cumple todas:</p>
<table class="tabla">
<tr><th>Característica</th><th>Qué significa</th><th>En el totito</th></tr>
<tr><td>De dos jugadores, por turnos</td><td>Primero uno, luego el otro</td><td>X y O se alternan</td></tr>
<tr><td>De <b>suma cero</b></td><td>Lo que uno gana, el otro lo pierde: si a uno le va +10, al otro le va −10. No hay forma de que ganen los dos</td><td>Gana X, gana O o empatan</td></tr>
<tr><td>De <b>información perfecta</b></td><td>Los dos ven todo; no hay cartas ocultas</td><td>El tablero está a la vista</td></tr>
<tr><td><b>Determinista</b></td><td>No hay azar, ni dados ni cartas</td><td>Cada jugada tiene un resultado fijo</td></tr>
<tr><td>Finito</td><td>Siempre termina</td><td>Como mucho 9 jugadas</td></tr>
</table>
<p>El ajedrez, las damas y el Conecta 4 también son así. El póker no (hay cartas ocultas y azar), ni el parqués (hay dados). La idea de «suma cero» es la clave: como un solo número describe cómo va la partida, la IA puede querer que ese número sea lo más <b>alto</b> posible, sabiendo que su rival quiere que sea lo más <b>bajo</b> posible. De ahí el nombre: uno <b>max</b>imiza y el otro <b>min</b>imiza.</p>

<h2>El árbol de juego</h2>
<p>Todas las partidas que pueden salir de una posición se dibujan como un <b>árbol</b> (uno al revés, con la raíz arriba). Vocabulario que usaremos:</p>
<ul>
<li><b>Nodo</b>: una posición del tablero.</li>
<li><b>Raíz</b>: la posición actual, donde la IA tiene que decidir.</li>
<li><b>Rama</b>: una jugada, que lleva de un nodo a otro.</li>
<li><b>Hijos</b> de un nodo: las posiciones que salen de él con una jugada.</li>
<li><b>Hoja</b>: una posición donde la partida terminó (alguien ganó o el tablero se llenó). No tiene hijos.</li>
<li><b>Profundidad</b>: cuántas jugadas se han imaginado desde la raíz.</li>
</ul>
<p>Veamos un árbol real, de una posición a pocas jugadas del final. Le toca a la IA (O) y quedan cuatro casillas libres: (1,1), (1,2), (2,0) y (2,2).</p>
<pre class="salida"> O | X | X
---+---+---
 O |   |
---+---+---
   | X |  </pre>
<p>Antes de mirar el dibujo, piénsalo tú: la O tiene dos fichas en la columna 0, así que si juega en (2,0) gana ya. Pero también hay un peligro: la X tiene (0,1) y (2,1), y si la O no tapa el centro, la X gana por la columna 1. Este es el árbol completo que explora Minimax, con lo más importante desplegado (la casilla morada de cada tablero es la jugada que llevó hasta él):</p>
<svg viewBox="0 0 1040 640" width="100%" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Arbol de juego de Minimax">
<rect x="0" y="0" width="1040" height="640" rx="16" fill="#1C1740"/>
<text x="16" y="70" font-family="DejaVu Sans, Arial, sans-serif" font-size="15" fill="#A05CFF" text-anchor="start" font-weight="bold">Raíz</text>
<text x="16" y="89" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="start">calcularMejorJugada</text>
<text x="16" y="235" font-family="DejaVu Sans, Arial, sans-serif" font-size="15" fill="#A05CFF" text-anchor="start" font-weight="bold">Nivel 1 · MIN</text>
<text x="16" y="254" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="start">minimax(copia, 0, false)</text>
<text x="16" y="415" font-family="DejaVu Sans, Arial, sans-serif" font-size="15" fill="#A05CFF" text-anchor="start" font-weight="bold">Nivel 2 · MAX</text>
<text x="16" y="434" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="start">profundidad 1</text>
<text x="16" y="565" font-family="DejaVu Sans, Arial, sans-serif" font-size="15" fill="#A05CFF" text-anchor="start" font-weight="bold">Nivel 3</text>
<text x="16" y="584" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="start">profundidad 2</text>
<rect x="558" y="24" width="84" height="84" rx="6" fill="#2A2357" stroke="#A05CFF" stroke-width="1.5"/>
<line x1="586" y1="27" x2="586" y2="105" stroke="#C8BCF6" stroke-width="1"/>
<line x1="561" y1="52" x2="639" y2="52" stroke="#C8BCF6" stroke-width="1"/>
<line x1="614" y1="27" x2="614" y2="105" stroke="#C8BCF6" stroke-width="1"/>
<line x1="561" y1="80" x2="639" y2="80" stroke="#C8BCF6" stroke-width="1"/>
<text x="572" y="44.16" font-family="DejaVu Sans, Arial, sans-serif" font-size="17.36" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="600" y="44.16" font-family="DejaVu Sans, Arial, sans-serif" font-size="17.36" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="628" y="44.16" font-family="DejaVu Sans, Arial, sans-serif" font-size="17.36" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="572" y="72.16" font-family="DejaVu Sans, Arial, sans-serif" font-size="17.36" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="600" y="100.16" font-family="DejaVu Sans, Arial, sans-serif" font-size="17.36" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="660" y="54" font-family="DejaVu Sans, Arial, sans-serif" font-size="15" fill="#C8BCF6" text-anchor="start" font-weight="bold">Le toca a la IA (O): MAX</text>
<text x="660" y="76" font-family="DejaVu Sans, Arial, sans-serif" font-size="14" fill="#C8BCF6" text-anchor="start">se queda con el MAYOR de abajo: 10</text>
<text x="660" y="98" font-family="DejaVu Sans, Arial, sans-serif" font-size="14" fill="#FF3BD4" text-anchor="start" font-weight="bold">y juega en (2,0)</text>
<line x1="600" y1="108" x2="260" y2="178" stroke="#A05CFF" stroke-width="1.6"/>
<text x="260" y="194" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#C8BCF6" text-anchor="middle">O en (1,1)</text>
<rect x="224" y="200" width="72" height="72" rx="6" fill="#2A2357" stroke="#A05CFF" stroke-width="1.5"/>
<rect x="250" y="226" width="20" height="20" rx="4" fill="#A05CFF" fill-opacity="0.35"/>
<line x1="248" y1="203" x2="248" y2="269" stroke="#C8BCF6" stroke-width="1"/>
<line x1="227" y1="224" x2="293" y2="224" stroke="#C8BCF6" stroke-width="1"/>
<line x1="272" y1="203" x2="272" y2="269" stroke="#C8BCF6" stroke-width="1"/>
<line x1="227" y1="248" x2="293" y2="248" stroke="#C8BCF6" stroke-width="1"/>
<text x="236" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="260" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="284" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="236" y="241.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="260" y="241.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="260" y="265.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="260" y="292" font-family="DejaVu Sans, Arial, sans-serif" font-size="14" fill="#C8BCF6" text-anchor="middle" font-weight="bold">MIN → 8</text>
<line x1="600" y1="108" x2="500" y2="178" stroke="#A05CFF" stroke-width="1.6"/>
<text x="500" y="194" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#C8BCF6" text-anchor="middle">O en (1,2)</text>
<rect x="464" y="200" width="72" height="72" rx="6" fill="#2A2357" stroke="#A05CFF" stroke-width="1.5"/>
<rect x="514" y="226" width="20" height="20" rx="4" fill="#A05CFF" fill-opacity="0.35"/>
<line x1="488" y1="203" x2="488" y2="269" stroke="#C8BCF6" stroke-width="1"/>
<line x1="467" y1="224" x2="533" y2="224" stroke="#C8BCF6" stroke-width="1"/>
<line x1="512" y1="203" x2="512" y2="269" stroke="#C8BCF6" stroke-width="1"/>
<line x1="467" y1="248" x2="533" y2="248" stroke="#C8BCF6" stroke-width="1"/>
<text x="476" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="500" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="524" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="476" y="241.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="524" y="241.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="500" y="265.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="500" y="292" font-family="DejaVu Sans, Arial, sans-serif" font-size="14" fill="#C8BCF6" text-anchor="middle" font-weight="bold">MIN → −9</text>
<line x1="600" y1="108" x2="700" y2="178" stroke="#A05CFF" stroke-width="1.6"/>
<text x="700" y="194" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#C8BCF6" text-anchor="middle">O en (2,0)</text>
<rect x="664" y="200" width="72" height="72" rx="6" fill="#2A2357" stroke="#A05CFF" stroke-width="1.5"/>
<rect x="666" y="250" width="20" height="20" rx="4" fill="#A05CFF" fill-opacity="0.35"/>
<line x1="688" y1="203" x2="688" y2="269" stroke="#C8BCF6" stroke-width="1"/>
<line x1="667" y1="224" x2="733" y2="224" stroke="#C8BCF6" stroke-width="1"/>
<line x1="712" y1="203" x2="712" y2="269" stroke="#C8BCF6" stroke-width="1"/>
<line x1="667" y1="248" x2="733" y2="248" stroke="#C8BCF6" stroke-width="1"/>
<text x="676" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="700" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="724" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="676" y="241.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="676" y="265.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="700" y="265.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="700" y="292" font-family="DejaVu Sans, Arial, sans-serif" font-size="14" fill="#FF3BD4" text-anchor="middle" font-weight="bold">¡gana O! 10 − 0 = 10</text>
<line x1="600" y1="108" x2="920" y2="178" stroke="#A05CFF" stroke-width="1.6"/>
<text x="920" y="194" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#C8BCF6" text-anchor="middle">O en (2,2)</text>
<rect x="884" y="200" width="72" height="72" rx="6" fill="#2A2357" stroke="#A05CFF" stroke-width="1.5"/>
<rect x="934" y="250" width="20" height="20" rx="4" fill="#A05CFF" fill-opacity="0.35"/>
<line x1="908" y1="203" x2="908" y2="269" stroke="#C8BCF6" stroke-width="1"/>
<line x1="887" y1="224" x2="953" y2="224" stroke="#C8BCF6" stroke-width="1"/>
<line x1="932" y1="203" x2="932" y2="269" stroke="#C8BCF6" stroke-width="1"/>
<line x1="887" y1="248" x2="953" y2="248" stroke="#C8BCF6" stroke-width="1"/>
<text x="896" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="920" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="944" y="217.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="896" y="241.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="920" y="265.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="944" y="265.28" font-family="DejaVu Sans, Arial, sans-serif" font-size="14.88" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="920" y="292" font-family="DejaVu Sans, Arial, sans-serif" font-size="14" fill="#C8BCF6" text-anchor="middle" font-weight="bold">MIN → −9</text>
<line x1="260" y1="300" x2="165" y2="370" stroke="#2F84FF" stroke-width="1.3"/>
<text x="165" y="385" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">X en (1,2)</text>
<rect x="136" y="390" width="58" height="58" rx="6" fill="#2A2357" stroke="#A05CFF" stroke-width="1.5"/>
<rect x="176.667" y="411.333" width="15.3333" height="15.3333" rx="4" fill="#A05CFF" fill-opacity="0.35"/>
<line x1="155.333" y1="393" x2="155.333" y2="445" stroke="#C8BCF6" stroke-width="1"/>
<line x1="139" y1="409.333" x2="191" y2="409.333" stroke="#C8BCF6" stroke-width="1"/>
<line x1="174.667" y1="393" x2="174.667" y2="445" stroke="#C8BCF6" stroke-width="1"/>
<line x1="139" y1="428.667" x2="191" y2="428.667" stroke="#C8BCF6" stroke-width="1"/>
<text x="145.667" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="165" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="184.333" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="145.667" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="165" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="184.333" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="165" y="442.587" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="165" y="466" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#C8BCF6" text-anchor="middle" font-weight="bold">MAX → 8</text>
<line x1="260" y1="300" x2="260" y2="370" stroke="#2F84FF" stroke-width="1.3"/>
<text x="260" y="385" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">X en (2,0)</text>
<rect x="231" y="390" width="58" height="58" rx="6" fill="#2A2357" stroke="#A05CFF" stroke-width="1.5"/>
<rect x="233" y="430.667" width="15.3333" height="15.3333" rx="4" fill="#A05CFF" fill-opacity="0.35"/>
<line x1="250.333" y1="393" x2="250.333" y2="445" stroke="#C8BCF6" stroke-width="1"/>
<line x1="234" y1="409.333" x2="286" y2="409.333" stroke="#C8BCF6" stroke-width="1"/>
<line x1="269.667" y1="393" x2="269.667" y2="445" stroke="#C8BCF6" stroke-width="1"/>
<line x1="234" y1="428.667" x2="286" y2="428.667" stroke="#C8BCF6" stroke-width="1"/>
<text x="240.667" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="260" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="279.333" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="240.667" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="260" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="240.667" y="442.587" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="260" y="442.587" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="260" y="466" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#C8BCF6" text-anchor="middle" font-weight="bold">MAX → 8</text>
<line x1="260" y1="300" x2="355" y2="370" stroke="#2F84FF" stroke-width="1.3"/>
<text x="355" y="385" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">X en (2,2)</text>
<rect x="326" y="390" width="58" height="58" rx="6" fill="#2A2357" stroke="#A05CFF" stroke-width="1.5"/>
<rect x="366.667" y="430.667" width="15.3333" height="15.3333" rx="4" fill="#A05CFF" fill-opacity="0.35"/>
<line x1="345.333" y1="393" x2="345.333" y2="445" stroke="#C8BCF6" stroke-width="1"/>
<line x1="329" y1="409.333" x2="381" y2="409.333" stroke="#C8BCF6" stroke-width="1"/>
<line x1="364.667" y1="393" x2="364.667" y2="445" stroke="#C8BCF6" stroke-width="1"/>
<line x1="329" y1="428.667" x2="381" y2="428.667" stroke="#C8BCF6" stroke-width="1"/>
<text x="335.667" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="355" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="374.333" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="335.667" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="355" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="355" y="442.587" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="374.333" y="442.587" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="355" y="466" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#C8BCF6" text-anchor="middle" font-weight="bold">MAX → 8</text>
<line x1="500" y1="300" x2="480" y2="370" stroke="#2F84FF" stroke-width="1.3"/>
<text x="480" y="385" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">X en (1,1)</text>
<rect x="451" y="390" width="58" height="58" rx="6" fill="#2A2357" stroke="#A05CFF" stroke-width="1.5"/>
<rect x="472.333" y="411.333" width="15.3333" height="15.3333" rx="4" fill="#A05CFF" fill-opacity="0.35"/>
<line x1="470.333" y1="393" x2="470.333" y2="445" stroke="#C8BCF6" stroke-width="1"/>
<line x1="454" y1="409.333" x2="506" y2="409.333" stroke="#C8BCF6" stroke-width="1"/>
<line x1="489.667" y1="393" x2="489.667" y2="445" stroke="#C8BCF6" stroke-width="1"/>
<line x1="454" y1="428.667" x2="506" y2="428.667" stroke="#C8BCF6" stroke-width="1"/>
<text x="460.667" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="480" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="499.333" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="460.667" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="480" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="499.333" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="480" y="442.587" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="480" y="466" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#2F84FF" text-anchor="middle" font-weight="bold">gana X: −9</text>
<line x1="920" y1="300" x2="865" y2="370" stroke="#2F84FF" stroke-width="1.3"/>
<text x="865" y="385" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">X en (1,1)</text>
<rect x="836" y="390" width="58" height="58" rx="6" fill="#2A2357" stroke="#A05CFF" stroke-width="1.5"/>
<rect x="857.333" y="411.333" width="15.3333" height="15.3333" rx="4" fill="#A05CFF" fill-opacity="0.35"/>
<line x1="855.333" y1="393" x2="855.333" y2="445" stroke="#C8BCF6" stroke-width="1"/>
<line x1="839" y1="409.333" x2="891" y2="409.333" stroke="#C8BCF6" stroke-width="1"/>
<line x1="874.667" y1="393" x2="874.667" y2="445" stroke="#C8BCF6" stroke-width="1"/>
<line x1="839" y1="428.667" x2="891" y2="428.667" stroke="#C8BCF6" stroke-width="1"/>
<text x="845.667" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="865" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="884.333" y="403.92" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="845.667" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="865" y="423.253" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="865" y="442.587" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#2F84FF" text-anchor="middle" font-weight="bold">X</text>
<text x="884.333" y="442.587" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.9867" fill="#FF3BD4" text-anchor="middle" font-weight="bold">O</text>
<text x="865" y="466" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#2F84FF" text-anchor="middle" font-weight="bold">gana X: −9</text>
<line x1="500" y1="300" x2="590" y2="396" stroke="#2F84FF" stroke-width="1.1" stroke-dasharray="4 4"/>
<text x="590" y="414" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">X en (2,0) → 8</text>
<text x="590" y="432" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">X en (2,2) → 8</text>
<text x="590" y="452" font-family="DejaVu Sans, Arial, sans-serif" font-size="11" fill="#A05CFF" text-anchor="middle">(otras respuestas)</text>
<line x1="920" y1="300" x2="975" y2="396" stroke="#2F84FF" stroke-width="1.1" stroke-dasharray="4 4"/>
<text x="975" y="414" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">X en (1,2) → 8</text>
<text x="975" y="432" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">X en (2,0) → 8</text>
<text x="975" y="452" font-family="DejaVu Sans, Arial, sans-serif" font-size="11" fill="#A05CFF" text-anchor="middle">(otras respuestas)</text>
<line x1="165" y1="472" x2="165" y2="548" stroke="#C8BCF6" stroke-width="1" stroke-dasharray="3 3"/>
<text x="165" y="566" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">O completa</text>
<text x="165" y="584" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">una línea:</text>
<text x="165" y="604" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#FF3BD4" text-anchor="middle" font-weight="bold">10 − 2 = 8</text>
<line x1="260" y1="472" x2="260" y2="548" stroke="#C8BCF6" stroke-width="1" stroke-dasharray="3 3"/>
<text x="260" y="566" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">O completa</text>
<text x="260" y="584" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">una línea:</text>
<text x="260" y="604" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#FF3BD4" text-anchor="middle" font-weight="bold">10 − 2 = 8</text>
<line x1="355" y1="472" x2="355" y2="548" stroke="#C8BCF6" stroke-width="1" stroke-dasharray="3 3"/>
<text x="355" y="566" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">O completa</text>
<text x="355" y="584" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="#C8BCF6" text-anchor="middle">una línea:</text>
<text x="355" y="604" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#FF3BD4" text-anchor="middle" font-weight="bold">10 − 2 = 8</text>
<text x="1020" y="616" font-family="DejaVu Sans, Arial, sans-serif" font-size="13" fill="#C8BCF6" text-anchor="end">MIN se queda con el menor · MAX con el mayor</text>
</svg>
<p>Cómo leerlo:</p>
<ul>
<li><b>Nivel 1</b>: las cuatro jugadas posibles de la O. Una de ellas, (2,0), termina la partida en el acto: es una hoja.</li>
<li><b>Nivel 2</b>: para cada jugada de la O, las respuestas posibles de la X. Si la O jugó en (1,2) o en (2,2), la X tiene una respuesta que gana: el centro.</li>
<li><b>Nivel 3</b>: si la O jugó en el centro (1,1), haga lo que haga la X, la O completa una línea en su siguiente turno, porque con (0,0), (1,0) y (1,1) amenaza tres líneas a la vez y la X solo puede tapar una.</li>
<li>Las ramas punteadas resumen respuestas que no cambian el resultado (más abajo verás por qué).</li>
</ul>

<h2>Puntuar las hojas</h2>
<p>Para que una computadora compare jugadas necesita números. Minimax da un <b>puntaje</b> a cada hoja, siempre desde el punto de vista de la IA:</p>
<table class="tabla">
<tr><th>Cómo terminó la partida imaginada</th><th>Puntaje</th><th>En el código</th></tr>
<tr><td>Gana la IA</td><td>+10 (menos la profundidad)</td><td><code>10 - profundidad</code></td></tr>
<tr><td>Gana el jugador</td><td>−10 (más la profundidad)</td><td><code>profundidad - 10</code></td></tr>
<tr><td>Empate</td><td>0</td><td><code>0</code></td></tr>
</table>
<p>¿Por qué 10? Podría ser cualquier número mayor que la profundidad máxima posible (9 jugadas), para que una victoria valga siempre más que 0 aunque se le reste la profundidad, y una derrota siempre menos que 0. Con 10 basta y los números quedan fáciles de leer. Olvida un momento la resta; enseguida la explicamos.</p>

<h2>MAX y MIN: subir los valores</h2>
<p>Las hojas tienen puntaje, pero las posiciones intermedias no. Minimax se lo calcula «subiendo» desde abajo con una regla muy simple:</p>
<ul>
<li>En un nodo donde le toca a la <b>IA</b> (nivel <b>MAX</b>), su valor es el <b>mayor</b> de los valores de sus hijos: la IA elegirá lo que más le conviene.</li>
<li>En un nodo donde le toca al <b>jugador</b> (nivel <b>MIN</b>), su valor es el <b>menor</b> de los valores de sus hijos: suponemos que el jugador elegirá lo que <i>peor</i> le deja a la IA.</li>
</ul>
<p>Suponer que el rival juega perfecto puede parecer pesimista, pero es lo que da la garantía: si la IA elige pensando en la mejor respuesta del rival, cualquier respuesta peor solo puede mejorarle las cosas. Es como cruzar la calle mirando a ambos lados aunque casi nunca venga un carro.</p>
<p>Apliquemos la regla al árbol, de abajo hacia arriba:</p>
<table class="tabla">
<tr><th>Nodo</th><th>Le toca a</th><th>Valores de sus hijos</th><th>Regla</th><th>Valor del nodo</th></tr>
<tr><td>Tras O(1,1) y X(1,2)</td><td>IA (MAX)</td><td>O(2,0) gana: 8 · O(2,2) gana: 8</td><td>mayor</td><td>8</td></tr>
<tr><td>Tras O(1,1) y X(2,0)</td><td>IA (MAX)</td><td>8 · 8</td><td>mayor</td><td>8</td></tr>
<tr><td>Tras O(1,1) y X(2,2)</td><td>IA (MAX)</td><td>8 · 8</td><td>mayor</td><td>8</td></tr>
<tr><td>Tras O(1,1)</td><td>jugador (MIN)</td><td>8 · 8 · 8</td><td>menor</td><td><b>8</b></td></tr>
<tr><td>Tras O(1,2)</td><td>jugador (MIN)</td><td>X(1,1) gana: −9 · X(2,0): 8 · X(2,2): 8</td><td>menor</td><td><b>−9</b></td></tr>
<tr><td>Tras O(2,0)</td><td>(hoja)</td><td>gana la O en el acto</td><td>—</td><td><b>10</b></td></tr>
<tr><td>Tras O(2,2)</td><td>jugador (MIN)</td><td>X(1,1) gana: −9 · X(1,2): 8 · X(2,0): 8</td><td>menor</td><td><b>−9</b></td></tr>
<tr><td>Raíz</td><td>IA (MAX)</td><td>8 · −9 · 10 · −9</td><td>mayor</td><td><b>10</b> → juega en (2,0)</td></tr>
</table>
<p>Fíjate en el nodo «tras O(1,2)»: dos de las tres respuestas de la X le darían 8 a la IA, pero hay una (el centro) que le da −9. MIN se queda con −9 porque un buen jugador elegiría esa. Por eso las ramas punteadas del dibujo no importan: aunque valgan 8, el mínimo ya es −9.</p>

<h2>Por qué restar la profundidad</h2>
<p>Mira otra vez el nivel 1: jugar en el centro (1,1) también lleva a una victoria segura, solo que una jugada más tarde. Si todas las victorias valieran 10 a secas, las jugadas (1,1) y (2,0) valdrían lo mismo, y la IA, que recorre las casillas de arriba abajo y se queda con la primera que encuentra con el mejor valor, elegiría (1,1): ganaría, sí, pero dando un rodeo innecesario. Restando la profundidad, ganar ahora vale <code>10 − 0 = 10</code> y ganar dentro de dos jugadas vale <code>10 − 2 = 8</code>, y la IA prefiere lo rápido.</p>
<p>No es una suposición: probamos las dos versiones con esta misma posición. Con el código del libro, la IA responde <code>2 0</code>; con una copia modificada que devuelve 10 y −10 sin restar la profundidad, responde <code>1 1</code>.</p>
<p>Del lado de las derrotas pasa lo simétrico: perder pronto vale <code>0 − 10 = −10</code>, perder más tarde vale, por ejemplo, <code>3 − 10 = −7</code>, que es mayor. Si alguna vez la derrota fuera inevitable, la IA elegiría el camino más largo, el que más oportunidades le da al rival de equivocarse. Es lo que haría un buen jugador humano: no rendirse antes de tiempo.</p>

<h2>La recursión, paso a paso</h2>
<p>¿Cómo se programa «imaginar todas las partidas»? Con <b>recursión</b> (capítulo 16): un método que se llama a sí mismo para resolver una versión más pequeña del mismo problema. El método <code>minimax</code> recibe un tablero y responde «¿cuánto vale esta posición?». Para responder:</p>
<ol>
<li><b>Caso base</b>: si la partida ya terminó (hay ganador o está lleno), el valor se sabe directamente: +10, −10 o 0, con la profundidad. No hace falta llamar a nadie.</li>
<li><b>Caso recursivo</b>: si no terminó, prueba cada casilla libre en una copia del tablero y se pregunta <b>a sí mismo</b> «¿cuánto vale esta nueva posición?», con el turno cambiado y la profundidad aumentada en 1. Con todas las respuestas, se queda con la mayor (si le toca a la IA) o con la menor (si le toca al jugador).</li>
</ol>
<p>Cada llamada tiene una casilla libre menos que la anterior, así que tarde o temprano se llega a un tablero terminado: el caso base siempre se alcanza y la recursión siempre termina. Así se ve la primera rama de nuestro ejemplo, tal como la recorre el programa (cada sangría es una llamada más profunda, que se apila encima de la anterior en la pila de llamadas):</p>
<pre class="texto">calcularMejorJugada(raíz)
 ├─ prueba O en (1,1): minimax(tablero1, 0, false)          [MIN]
 │   ├─ prueba X en (1,2): minimax(tablero2, 1, true)        [MAX]
 │   │   ├─ prueba O en (2,0): minimax(tablero3, 2, false)
 │   │   │     caso base: ganó la O → devuelve 10 − 2 = 8
 │   │   ├─ prueba O en (2,2): minimax(tablero4, 2, false)
 │   │   │     caso base: ganó la O → devuelve 8
 │   │   └─ mejor = max(8, 8) = 8 → devuelve 8
 │   ├─ prueba X en (2,0): ... → devuelve 8
 │   ├─ prueba X en (2,2): ... → devuelve 8
 │   └─ menor = min(8, 8, 8) = 8 → devuelve 8
 │   valor 8 es mayor que el mejor hasta ahora → mejorJugada = (1,1)
 ├─ prueba O en (1,2): ... → devuelve −9    (−9 &gt; 8? no)
 ├─ prueba O en (2,0): minimax(tablero, 0, false)
 │     caso base: ganó la O → devuelve 10 − 0 = 10
 │   10 &gt; 8? sí → mejorJugada = (2,0)
 ├─ prueba O en (2,2): ... → devuelve −9    (−9 &gt; 10? no)
 └─ devuelve {2, 0}</pre>
<p>Para recorrer este árbol, el programa hace 29 llamadas a <code>minimax</code>. Ninguna «sabe» el resultado de antemano: cada una solo sabe aplicar las dos reglas (caso base o caso recursivo), y el resultado correcto aparece al combinar las respuestas. Esa es la magia de la recursión.</p>

<h2>¿Cuántas partidas posibles hay?</h2>
<p>Si la IA imagina todas las partidas, ¿cuántas son? Las contamos con un pequeño programa aparte (no forma parte del proyecto) que juega todas las combinaciones de jugadas legales, deteniéndose cuando alguien gana:</p>
<table class="tabla">
<tr><th>Dato</th><th>Cantidad</th></tr>
<tr><td>Partidas distintas posibles (secuencias completas de jugadas)</td><td><b>255 168</b></td></tr>
<tr><td>… que gana la X (la que empieza)</td><td>131 184</td></tr>
<tr><td>… que gana la O</td><td>77 904</td></tr>
<tr><td>… que terminan en empate</td><td>46 080</td></tr>
<tr><td>Posiciones distintas que pueden aparecer en un tablero real</td><td>5 478</td></tr>
<tr><td>Llamadas a <code>minimax</code> para responder a la primera jugada de la persona</td><td>entre 55 504 (si abrió en el centro) y 63 904 (si abrió en un lado)</td></tr>
<tr><td>Llamadas si la IA tuviera que elegir con el tablero vacío</td><td>549 945</td></tr>
</table>
<p>Parecen muchas, pero una computadora actual hace millones de operaciones sencillas por segundo: en nuestras pruebas, la primera respuesta de la IA tardó entre 15 y 50 milésimas de segundo. A partir de la segunda, con menos casillas libres, el árbol se encoge muchísimo y la respuesta es prácticamente instantánea.</p>
<div class="caja concepto"><b>¿Y el ajedrez?</b> En ajedrez se calcula que hay más partidas posibles (un 1 seguido de unos 120 ceros) que átomos en el universo observable. Ningún computador puede recorrer ese árbol entero. Los programas de ajedrez usan Minimax, pero con dos cambios: se detienen a cierta profundidad y, en lugar de +10/−10/0, <b>estiman</b> qué tan buena es la posición (material, control del centro…); y usan la <b>poda alfa-beta</b>, una mejora que evita explorar ramas que ya se sabe que no van a cambiar la decisión, como las ramas punteadas de nuestro dibujo. El totito es tan pequeño que no necesita ninguna de las dos cosas.</div>

<h2>Por qué la IA nunca pierde</h2>
<p>El totito es un juego <b>resuelto</b>: se sabe que, si los dos jugadores juegan perfecto, siempre termina en empate. Dicho en idioma Minimax, el valor del tablero vacío es 0. Eso significa que la persona no tiene ninguna forma de <i>obligar</i> a la IA a perder. Y Minimax, por construcción, encuentra en cada turno una jugada cuyo valor garantizado es el máximo posible: como ese máximo nunca es negativo (siempre existe al menos el camino al empate), la IA nunca elige una jugada que la lleve a perder. Si la persona juega perfecto, empate; si se equivoca una vez en algún momento decisivo, la IA lo aprovecha y gana.</p>
<p>Como tampoco esto es para creerlo a ciegas, lo comprobamos: otro programa de prueba hizo jugar a la IA contra <b>todas</b> las secuencias posibles de jugadas de una persona que empieza con X. Resultado: <b>569 partidas distintas; la IA ganó 386, empató 183 y perdió 0</b>.</p>

<h2>Créalo</h2>
<ol>
<li>En NetBeans: clic derecho sobre <i>Source Packages → &lt;default package&gt;</i> → <i>New → Java Class…</i></li>
<li><i>Class Name</i>: <code>IA_Minimax</code> (con guion bajo y las mayúsculas exactas) → <i>Finish</i>.</li>
<li>Borra la plantilla y escribe el archivo. Guarda con Ctrl+S.</li>
</ol>
<pre class="ps">cd $HOME\Proyectos\Totito
New-Item src\IA_Minimax.java</pre>
<div class="caja consejo"><b>Sobre el nombre</b> Por convención, los nombres de clases en Java se escriben con mayúscula inicial y sin guiones bajos (<code>IaMinimax</code>). Este proyecto conserva el nombre <code>IA_Minimax</code> que tenía el código original; es válido y se entiende bien, pero en tus proyectos nuevos prefiere el estilo convencional. Lo importante es elegir uno y ser consistente.</div>
""",
    "archivos": [
        {"ruta": "src/IA_Minimax.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1–L9</b> Javadoc de la clase. Resume todo lo que vimos en la teoría: la IA explora recursivamente el árbol de todas las partidas posibles desde la posición actual; supone que ella maximiza su resultado y que el jugador lo minimiza; y, como el totito es de suma cero y con pocos estados, recorre el árbol completo y por eso nunca pierde. Un buen comentario de clase cuenta la <b>idea</b>, no repite el código.</p>
<p class="l"><b>L10</b> Declara la clase pública <code>IA_Minimax</code>. Su cuerpo va hasta la L97.</p>
<p class="l"><b>L11</b> Línea en blanco.</p>
"""),
             ("private final char fichaIA", r"""
<p class="l"><b>L12</b> Atributo con la ficha con la que juega la IA. <code>private</code>: nadie de fuera la toca. <code>final</code>: se asigna en el constructor y no cambia; una IA no cambia de bando a mitad de partida. ¿Por qué guardarla en vez de escribir <code>'O'</code> en todo el código? Porque así la misma clase sirve si la IA juega con X; en la Parte VII, la clase <code>Partida</code> crea la IA con la ficha que el usuario dejó libre en la pantalla de configuración.</p>
<p class="l"><b>L13</b> La ficha del rival. La IA la necesita para dos cosas: reconocer cuándo ganó el jugador (puntaje negativo) y simular sus jugadas en el árbol.</p>
<p class="l"><b>L14</b> Línea en blanco.</p>
"""),
             ("public IA_Minimax(char fichaIA", r"""
<p class="l"><b>L15</b> El constructor: recibe las dos fichas. El orden importa y es fácil equivocarse: <b>primero la de la IA, luego la del jugador</b>. En la versión 0.1 se crea así: <code>new IA_Minimax('O', 'X')</code>.</p>
<p class="l"><b>L16–L17</b> Guardan cada parámetro en su atributo con <code>this.</code>, igual que en <code>Jugador</code> (capítulo 30): el parámetro tapa al atributo del mismo nombre y <code>this</code> lo desempata.</p>
<p class="l"><b>L18–L19</b> Cierran el constructor y dejan una línea en blanco.</p>
<div class="caja cuidado"><b>Fichas al revés</b> Si escribes <code>new IA_Minimax('X', 'O')</code> cuando la persona juega con X, el programa compila y funciona… pero la IA cree que es la X: elige la mejor jugada <i>para la persona</i> y la juega con la ficha O. El resultado es una IA que parece tonta. Como ambos parámetros son <code>char</code>, el compilador no puede detectar el cambio: es un error de lógica, no de sintaxis.</div>
"""),
             ("public int[] calcularMejorJugada", r"""
<p class="l"><b>L20–L24</b> Javadoc del método público. Dice qué hace (evalúa cada casilla vacía en una copia y se queda con la de mayor puntaje) y qué devuelve: <code>{fila, columna}</code>.</p>
<p class="l"><b>L25</b> La firma. <code>public</code>: es lo único que las demás clases necesitan llamar. Devuelve <code>int[]</code>, un <b>arreglo de enteros</b>: un método en Java solo puede devolver un valor, y aquí necesitamos dos números (fila y columna), así que los metemos en un arreglo de dos posiciones. Recibe el <code>Tablero</code> de la partida real. Este método es la <b>raíz</b> del árbol: el primer nivel MAX.</p>
<p class="l"><b>L26</b> <code>mejorValor</code> guardará el mejor puntaje encontrado hasta ahora. Empieza en <code>Integer.MIN_VALUE</code>, el <code>int</code> más pequeño que existe (−2 147 483 648). <code>Integer</code> es una clase de Java que acompaña al tipo <code>int</code> y guarda datos útiles sobre él, como su mínimo y su máximo. ¿Por qué no empezar en 0? Porque si todas las jugadas valieran menos de 0 (por ejemplo, −9 y −7), ninguna superaría al 0 y la IA no elegiría nada. Con el mínimo posible, la primera jugada evaluada siempre lo supera.</p>
<p class="l"><b>L27</b> <code>mejorJugada</code> es un arreglo de dos enteros con valor inicial <code>{-1, -1}</code>. <code>new int[]{-1, -1}</code> crea el arreglo y lo llena en el mismo paso. El −1 es un <b>valor centinela</b>: una casilla que no existe, que significa «todavía no encontré ninguna jugada». Si el tablero estuviera lleno, el método devolvería <code>{-1, -1}</code>, y por eso la ventana del capítulo 33 comprueba <code>jugada[0] == -1</code> antes de usarla.</p>
<p class="l"><b>L28</b> Línea en blanco.</p>
"""),
             ("for (int fila = 0; fila < 3; fila++) {", r"""
<p class="l"><b>L29–L30</b> Los dos <code>for</code> anidados de siempre: recorren las 9 casillas en orden, de izquierda a derecha y de arriba abajo.</p>
<p class="l"><b>L31</b> Solo interesan las casillas libres. <code>tablero.obtenerCasilla(fila, columna)</code> consulta el tablero real (sin modificarlo) y <code>Tablero.VACIA</code> es la constante del capítulo 29, usada con el nombre de la clase porque es <code>static</code>.</p>
<p class="l"><b>L32</b> Crea una copia del tablero real. Esta línea es la que hace posible «imaginar»: lo que pase en <code>copia</code> no afecta a la partida. Sin ella, si la IA escribiera directamente en <code>tablero</code>, cada jugada imaginada quedaría marcada de verdad y el tablero se llenaría de fichas fantasma.</p>
<p class="l"><b>L33</b> En la copia, coloca la ficha de la IA en esa casilla: «¿y si juego aquí?». No hace falta mirar el <code>boolean</code> que devuelve <code>marcarCasilla</code>, porque L31 ya garantizó que la casilla está libre.</p>
"""),
             ("int valor = minimax(copia, 0, false)", r"""
<p class="l"><b>L34</b> Pregunta a <code>minimax</code> cuánto vale la posición que resulta. Le pasa tres datos: la copia con la jugada hecha; profundidad <code>0</code>, porque es la primera jugada imaginada; y <code>false</code>, porque después de que juega la IA le toca al jugador, que es MIN. El resultado (por ejemplo 8, −9 o 10) se guarda en <code>valor</code>.</p>
<p class="l"><b>L35</b> ¿Esta jugada es mejor que la mejor que tenía? Se usa <code>&gt;</code> estricto: si dos jugadas valen lo mismo, se queda con la <b>primera</b> que encontró en el recorrido. Por eso la IA es predecible: ante la X en el centro, todas las esquinas valen 0 y elige siempre (0,0), la primera.</p>
<p class="l"><b>L36–L38</b> Si es mejor, guarda su valor y sus coordenadas: <code>mejorJugada[0]</code> es la fila y <code>mejorJugada[1]</code> la columna. Los arreglos empiezan en el índice 0 (capítulo 15).</p>
<p class="l"><b>L39–L42</b> Cierran el <code>if</code> de L35, el <code>if</code> de L31 y los dos <code>for</code>.</p>
<p class="l"><b>L43</b> Devuelve el arreglo con la mejor jugada. Quien llamó lo usará así: <code>int[] jugada = ia.calcularMejorJugada(tablero);</code> y luego <code>jugada[0]</code>, <code>jugada[1]</code>.</p>
<p class="l"><b>L44–L45</b> Cierran el método y dejan una línea en blanco.</p>
<div class="caja concepto"><b>¿Por qué este método no es igual a <code>minimax</code>?</b> Hace casi lo mismo que la rama MAX de <code>minimax</code>, pero con una diferencia: <code>minimax</code> devuelve un <b>número</b> (cuánto vale una posición), y aquí necesitamos una <b>jugada</b> (dónde poner la ficha). Por eso este método recuerda, además del mejor valor, en qué casilla lo encontró.</div>
"""),
             ("private int minimax(", r"""
<p class="l"><b>L46–L58</b> El Javadoc describe exactamente las dos partes de la recursión que estudiaste: el <b>caso base</b> (si hay ganador o el tablero está lleno, devolver +10, −10 o 0 ajustados por la profundidad, para que la IA prefiera ganar rápido y, si fuera inevitable, perder tarde) y el <b>caso recursivo</b> (probar cada casilla vacía con la ficha de quien tiene el turno y llamar a <code>minimax</code> con el turno contrario, quedándose con el máximo si juega la IA y con el mínimo si juega el jugador, porque se supone que este también juega de forma óptima).</p>
<p class="l"><b>L59</b> La firma del método recursivo. Es <code>private</code>: es un detalle interno de cómo piensa la IA; las demás clases no tienen por qué llamarlo, y así se podría cambiar sin romper nada fuera. Devuelve un <code>int</code>, el valor de la posición. Recibe:</p>
<ul>
<li><code>Tablero tablero</code>: la posición imaginada que se va a evaluar (siempre una copia, nunca la partida real).</li>
<li><code>int profundidad</code>: cuántas jugadas se han imaginado desde la raíz.</li>
<li><code>boolean esMax</code>: <code>true</code> si en esta posición le toca a la IA (MAX), <code>false</code> si le toca al jugador (MIN).</li>
</ul>
"""),
             ("char ganador = tablero.verificarGanador()", r"""
<p class="l"><b>L60</b> Empieza el <b>caso base</b>. Pregunta al tablero si alguien ganó y guarda la respuesta en una variable local: <code>'X'</code>, <code>'O'</code> o <code>' '</code>. Guardarla evita llamar dos veces a <code>verificarGanador</code> (una para cada <code>if</code>).</p>
<p class="l"><b>L61–L62</b> Si ganó la IA: <code>return 10 - profundidad;</code>. Una victoria inmediata (profundidad 0) vale 10; una dentro de dos jugadas, 8. El <code>return</code> termina esta llamada y entrega el valor a la llamada de arriba.</p>
<p class="l"><b>L63</b> Cierra el <code>if</code>.</p>
<p class="l"><b>L64–L65</b> Si ganó el jugador: <code>return profundidad - 10;</code>. Perder en la siguiente jugada (profundidad 1) vale −9; perder más tarde vale menos negativo, por ejemplo −7 a profundidad 3.</p>
<p class="l"><b>L66</b> Cierra el <code>if</code>.</p>
<p class="l"><b>L67–L68</b> Si nadie ganó y el tablero está lleno, es empate: vale 0. El orden de estos <code>if</code> es el del capítulo 28: primero «¿hay ganador?» y después «¿está lleno?», porque una línea completada con la novena ficha es victoria, no empate.</p>
<p class="l"><b>L69–L70</b> Cierran el <code>if</code> y dejan una línea en blanco. Si el programa llega a la L71, la partida imaginada sigue abierta: toca el caso recursivo.</p>
"""),
             ("if (esMax) {", r"""
<p class="l"><b>L71</b> ¿A quién le toca? <code>if (esMax)</code> equivale a <code>if (esMax == true)</code>, pero más corto: una variable <code>boolean</code> ya es una condición.</p>
<p class="l"><b>L72</b> Rama de la IA (MAX). <code>mejor</code> empieza en el valor más bajo posible, por la misma razón que <code>mejorValor</code> en L26: cualquier valor real lo superará.</p>
<p class="l"><b>L73–L74</b> Recorre las 9 casillas.</p>
<p class="l"><b>L75</b> Solo las casillas vacías de <b>este</b> tablero imaginado.</p>
"""),
             ("Tablero copia = tablero.obtenerCopia();", r"""
<p class="l"><b>L76</b> Una copia nueva del tablero imaginado, para no estropearlo: lo necesitamos intacto para probar la siguiente casilla en la próxima vuelta del ciclo.</p>
<p class="l"><b>L77</b> Pone la ficha de la IA en la copia: «la IA juega aquí».</p>
<p class="l"><b>L78</b> El corazón del algoritmo, y la <b>llamada recursiva</b>: <code>minimax</code> se llama a sí mismo con la copia, la profundidad aumentada en 1 y <code>false</code> (después de la IA le toca al jugador). Mientras esa llamada trabaja (y hace a su vez sus propias llamadas), esta espera en la pila. Cuando vuelve con un número, <code>Math.max(mejor, ...)</code> devuelve el mayor de los dos y lo guarda en <code>mejor</code>. <code>Math</code> es una clase de Java con operaciones matemáticas; <code>max</code> y <code>min</code> son métodos <code>static</code>, por eso se llaman con el nombre de la clase y sin <code>new</code>. No necesita <code>import</code> porque está en <code>java.lang</code>, el paquete que Java importa siempre.</p>
<p class="l"><b>L79–L81</b> Cierran el <code>if</code> y los dos <code>for</code>.</p>
<p class="l"><b>L82</b> Devuelve el máximo de todos los hijos: lo mejor que puede conseguir la IA desde esta posición si juega perfecto. Nunca devuelve <code>Integer.MIN_VALUE</code>, porque si no quedara ninguna casilla vacía el caso base (tablero lleno) habría respondido antes.</p>
"""),
             ("} else {", r"""
<p class="l"><b>L83</b> <code>else</code> («si no») es la otra rama del <code>if</code> de L71: se ejecuta cuando <code>esMax</code> es <code>false</code>, es decir, cuando le toca al jugador (MIN).</p>
<p class="l"><b>L84</b> <code>menor</code> empieza en <code>Integer.MAX_VALUE</code>, el <code>int</code> más grande (2 147 483 647): al buscar el mínimo, el valor inicial debe ser tan alto que cualquier resultado real quede por debajo.</p>
<p class="l"><b>L85–L87</b> Recorre las casillas y se queda con las vacías, igual que en la rama MAX.</p>
"""),
             ("Tablero copia = tablero.obtenerCopia();", r"""
<p class="l"><b>L88</b> Copia el tablero imaginado.</p>
<p class="l"><b>L89</b> Ahora la ficha que se coloca es la del <b>jugador</b>: «¿y si el jugador responde aquí?».</p>
<p class="l"><b>L90</b> Llamada recursiva con profundidad + 1 y <code>true</code>, porque después del jugador le toca otra vez a la IA. <code>Math.min</code> se queda con el menor: el jugador, se supone, elegirá la respuesta que peor le deje a la IA.</p>
<p class="l"><b>L91–L93</b> Cierran el <code>if</code> y los dos <code>for</code>.</p>
<p class="l"><b>L94</b> Devuelve el mínimo: lo peor que le puede pasar a la IA desde esta posición si el jugador juega perfecto.</p>
<p class="l"><b>L95–L97</b> Cierran el <code>else</code>, el método <code>minimax</code> y la clase.</p>
<div class="caja concepto"><b>Las dos ramas son simétricas</b> Compara L72–L82 con L84–L94: solo cambian cuatro cosas. El valor inicial (<code>MIN_VALUE</code> o <code>MAX_VALUE</code>), la ficha que se coloca (<code>fichaIA</code> o <code>fichaJugador</code>), el turno siguiente (<code>false</code> o <code>true</code>) y la operación (<code>max</code> o <code>min</code>). Se podrían fusionar en una sola rama con variables, pero escritas por separado se entiende mucho mejor que una refleja a la otra.</div>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>Traza: la IA responde a una apertura en el centro</h3>
<p>La persona juega primero en el centro (1,1). La IA llama a <code>calcularMejorJugada</code>, que prueba las 8 casillas libres y pide a <code>minimax</code> el valor de cada una. Estos son los valores reales que calcula (los obtuvimos imprimiéndolos con un programa de prueba):</p>
<table class="tabla">
<tr><th>Casilla probada por la IA</th><th>Valor de <code>minimax</code></th><th>¿Supera a <code>mejorValor</code>?</th><th><code>mejorJugada</code> después</th></tr>
<tr><td>(0,0) esquina</td><td>0</td><td>sí (0 &gt; −2 147 483 648)</td><td>{0, 0}</td></tr>
<tr><td>(0,1) lado</td><td>−5</td><td>no</td><td>{0, 0}</td></tr>
<tr><td>(0,2) esquina</td><td>0</td><td>no (0 no es mayor que 0)</td><td>{0, 0}</td></tr>
<tr><td>(1,0) lado</td><td>−5</td><td>no</td><td>{0, 0}</td></tr>
<tr><td>(1,2) lado</td><td>−5</td><td>no</td><td>{0, 0}</td></tr>
<tr><td>(2,0) esquina</td><td>0</td><td>no</td><td>{0, 0}</td></tr>
<tr><td>(2,1) lado</td><td>−5</td><td>no</td><td>{0, 0}</td></tr>
<tr><td>(2,2) esquina</td><td>0</td><td>no</td><td>{0, 0}</td></tr>
</table>
<p>Cómo se interpretan esos números:</p>
<ul>
<li><b>0 en las esquinas</b>: si la IA responde en una esquina y los dos juegan perfecto, empate.</li>
<li><b>−5 en los lados</b>: si la IA responde en un lado, la persona puede forzar la victoria. El valor dice incluso cuándo: <code>5 − 10 = −5</code>, es decir, ganaría con la quinta jugada imaginada (su cuarta ficha), tras obligar a la O a tapar y montar una doble amenaza.</li>
<li>Gana la primera esquina, (0,0), por el <code>&gt;</code> estricto de L35.</li>
</ul>
<p>Es exactamente lo que enseñan los manuales de estrategia del totito («si el rival abre en el centro, responde en una esquina»), solo que la IA lo descubrió sola, sin que nadie se lo programara.</p>
<h3>Qué pasa en la memoria</h3>
<p>Cada llamada a <code>minimax</code> crea sus propias variables locales (<code>ganador</code>, <code>mejor</code> o <code>menor</code>, <code>fila</code>, <code>columna</code>, <code>copia</code>) en un espacio nuevo de la <b>pila de llamadas</b>. Cuando la llamada termina con <code>return</code>, ese espacio se libera y la llamada de abajo continúa justo donde se había quedado. Como un tablero tiene como mucho 9 casillas, la pila nunca tiene más de 10 llamadas apiladas a la vez, aunque en total se hagan decenas de miles. Las copias del tablero que ya no se usan las recoge solo el <b>recolector de basura</b> de Java, el mecanismo que libera la memoria de los objetos a los que ya nadie apunta.</p>

<h2>Compila y prueba</h2>
<p>Compila con <i>Run → Clean and Build Project</i> (Shift+F11): debe terminar en <code>BUILD SUCCESS</code>. Luego, en PowerShell, desde la carpeta del proyecto, abre <code>jshell</code> y carga las dos clases. El orden importa: primero <code>Tablero</code>, porque <code>IA_Minimax</code> la usa.</p>
<pre class="ps">cd $HOME\Proyectos\Totito
jshell</pre>
<pre class="salida">jshell&gt; /open src/Tablero.java

jshell&gt; /open src/IA_Minimax.java

jshell&gt; IA_Minimax ia = new IA_Minimax('O', 'X');
ia ==&gt; IA_Minimax@68837a77

jshell&gt; Tablero t = new Tablero();
t ==&gt; Tablero@327471b5

jshell&gt; t.marcarCasilla(0, 0, 'O'); t.marcarCasilla(0, 1, 'X'); t.marcarCasilla(0, 2, 'X');
$5 ==&gt; true
$6 ==&gt; true
$7 ==&gt; true

jshell&gt; t.marcarCasilla(1, 0, 'O'); t.marcarCasilla(2, 1, 'X');
$8 ==&gt; true
$9 ==&gt; true

jshell&gt; ia.calcularMejorJugada(t)
$10 ==&gt; int[2] { 2, 0 }

jshell&gt; Tablero b = new Tablero();
b ==&gt; Tablero@4909b8da

jshell&gt; b.marcarCasilla(0, 0, 'X'); b.marcarCasilla(1, 1, 'O'); b.marcarCasilla(0, 1, 'X');
$12 ==&gt; true
$13 ==&gt; true
$14 ==&gt; true

jshell&gt; ia.calcularMejorJugada(b)
$15 ==&gt; int[2] { 0, 2 }

jshell&gt; Tablero c = new Tablero();
c ==&gt; Tablero@34b7bfc0

jshell&gt; c.marcarCasilla(1, 1, 'X')
$17 ==&gt; true

jshell&gt; ia.calcularMejorJugada(c)
$18 ==&gt; int[2] { 0, 0 }

jshell&gt; c.obtenerCasilla(0, 0)
$19 ==&gt; ' '

jshell&gt; /exit
|  Goodbye</pre>
<p>Tres pruebas, tres comportamientos distintos (sesión real):</p>
<ul>
<li><code>t</code> es la posición del árbol de este capítulo: la IA elige <code>{2, 0}</code>, la victoria inmediata, y no (1,1), la victoria lenta.</li>
<li><code>b</code>: la X amenaza la fila 0 con (0,0) y (0,1). La IA <b>tapa</b> en (0,2). Nadie le enseñó a tapar: lo hace porque cualquier otra casilla lleva a una hoja de −9.</li>
<li><code>c</code>: ante la X en el centro, responde en la esquina (0,0), como predijo la traza.</li>
<li>Después de calcular, <code>c.obtenerCasilla(0, 0)</code> sigue vacía: <code>calcularMejorJugada</code> <b>no toca</b> el tablero que recibe, solo copias. Poner la ficha es trabajo de quien la llama.</li>
</ul>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Síntoma</th><th>Causa</th><th>Solución</th></tr>
<tr><td><code>StackOverflowError</code></td><td>Falta o está mal el caso base (L60–L69): la recursión nunca se detiene y la pila se desborda</td><td>Revisa que los tres <code>return</code> del caso base estén antes del <code>if (esMax)</code></td></tr>
<tr><td>El tablero real se llena de fichas que nadie jugó</td><td>Se marcó en <code>tablero</code> en lugar de en <code>copia</code> (L33, L77 o L89)</td><td>Toda jugada imaginada va en una copia</td></tr>
<tr><td>La IA no tapa ni ataca; parece jugar para el rival</td><td>Fichas invertidas en el constructor, o <code>true</code> y <code>false</code> intercambiados en L34, L78 o L90</td><td>Constructor: <code>(fichaIA, fichaJugador)</code>. Tras jugar la IA va <code>false</code>; tras el jugador, <code>true</code></td></tr>
<tr><td>La IA devuelve <code>{-1, -1}</code> en mitad de la partida</td><td><code>mejorValor</code> empieza en 0 en lugar de <code>Integer.MIN_VALUE</code>, y todas las jugadas valían menos</td><td>Empieza siempre con el peor valor posible</td></tr>
<tr><td>La IA gana, pero «da vueltas» antes de rematar</td><td>Se quitó la profundidad de L62 o L65</td><td>Vuelve a <code>10 - profundidad</code> y <code>profundidad - 10</code></td></tr>
<tr><td><code>cannot find symbol: class Tablero</code> en <code>jshell</code></td><td>Abriste <code>IA_Minimax.java</code> antes que <code>Tablero.java</code></td><td>Primero <code>/open src/Tablero.java</code></td></tr>
</table>

<div class="caja git"><b>Git</b> La IA está escrita y probada:
<pre class="ps">git add src\IA_Minimax.java
git commit -m "IA con el algoritmo Minimax"
git push</pre>
Ya tienes en GitHub toda la lógica del juego: tres commits, uno por clase. Si entras a tu repositorio <code>totito</code> en el navegador verás la carpeta <code>src</code> con los tres archivos.</div>

<h2>Resumen</h2>
<ul>
<li>Minimax sirve para juegos de dos jugadores, por turnos, de suma cero, con información perfecta y sin azar, como el totito.</li>
<li>Imagina el árbol de todas las partidas: puntúa las hojas desde el punto de vista de la IA (+10, −10, 0) y sube los valores con el mayor en los turnos de la IA (MAX) y el menor en los del jugador (MIN).</li>
<li>Restar la profundidad hace que la IA prefiera ganar pronto y, si tuviera que perder, perder tarde.</li>
<li>La recursión tiene un caso base (partida terminada) y un caso recursivo (probar cada casilla y llamarse con el turno contrario); siempre termina porque cada llamada tiene una casilla libre menos.</li>
<li>Hay 255 168 partidas posibles; responder a la primera jugada cuesta entre 55 504 y 63 904 llamadas, unas centésimas de segundo.</li>
<li>Como el totito bien jugado es empate, una IA que recorre el árbol completo nunca pierde: contra todas las secuencias posibles de jugadas, 0 derrotas.</li>
<li><code>calcularMejorJugada</code> devuelve <code>{fila, columna}</code> en un <code>int[]</code>, empieza con <code>Integer.MIN_VALUE</code> y un centinela <code>{-1, -1}</code>, y nunca modifica el tablero real.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b> Minimax y la recursión aparecen en muchos lugares:
<ul>
<li><b>Otros juegos de mesa</b>: Conecta 4, damas, Othello o el juego de los palillos (Nim) usan la misma clase con otro tablero. En los grandes, se limita la profundidad (por ejemplo, 6 jugadas), se cambia el +10/−10 por una función que estime la posición y se añade la poda alfa-beta.</li>
<li><b>Decidir con el peor caso en mente</b>: planificar inventario o rutas suponiendo «¿qué es lo peor que puede pasar con cada opción?» y elegir la opción cuyo peor caso es el mejor. Es el mismo razonamiento MIN/MAX.</li>
<li><b>Recorrer estructuras con forma de árbol</b>: las carpetas de tu disco (una carpeta contiene carpetas), un organigrama, un menú con submenús o los comentarios con respuestas en una red social se recorren con un método recursivo con caso base («no tiene hijos») y caso recursivo («recorre cada hijo»).</li>
<li><b>Simular sin tocar los datos reales</b>: copiar el estado, probar una acción y medir el resultado, como hace la IA con <code>obtenerCopia()</code>, sirve para un «¿y si…?» en una hoja de presupuestos o en un sistema de reservas.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Dibuja el árbol de esta posición, donde le toca a la O con dos casillas libres: X O X / X O O / ␣ X ␣. Puntúa las hojas y sube los valores. ¿Qué casilla elige la IA? Comprueba tu respuesta en <code>jshell</code>.</li>
<li>En <code>jshell</code>, pon una X en la esquina (0,0) y pide la jugada de la IA. ¿Responde en el centro? Explica con la idea de los valores 0 y −5 por qué una esquina no sirve como respuesta.</li>
<li>Agrega a una copia de la clase un contador <code>private int llamadas</code> que se incremente al inicio de <code>minimax</code>, y un método para consultarlo. Comprueba que, tras una apertura en el centro, la IA hace 55 504 llamadas.</li>
<li>Haz una «IA fácil»: una clase <code>IA_Aleatoria</code> con el mismo método <code>public int[] calcularMejorJugada(Tablero tablero)</code> que elija una casilla vacía al azar. Pista: guarda las casillas libres en una lista y usa <code>new java.util.Random().nextInt(cantidad)</code>.</li>
<li>Reto: investiga la poda alfa-beta y agrégala a <code>minimax</code> con dos parámetros más, <code>alfa</code> y <code>beta</code>. Con el contador del ejercicio 3, compara cuántas llamadas se ahorran. La jugada elegida debe ser la misma.</li>
</ol></div>
""",
}
