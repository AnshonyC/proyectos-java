# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 54,
    "titulo": "IconoResultado.java: un trofeo con destellos (y un poco de trigonometría)",
    "antes": r"""
<p class="entrada">Cuando alguien gana, la pantalla de resultado muestra arriba un trofeo cian rodeado de seis
destellos de colores; cuando hay empate, una X y una O juntas. En este capítulo construyes esa ilustración y usas,
sin miedo, el seno y el coseno: la forma más cómoda de colocar cosas <b>alrededor</b> de un centro.</p>

<h2>Por qué existe este archivo</h2>
<p>El diseño de victoria (<code>diseno/victoria.jpg</code>, capítulo 34) pone un trofeo brillante con rayitas
alrededor, como si destellara. El juego necesita además una versión para el <b>empate</b>, que el diseño no traía:
la elegimos con las dos fichas, X y O, una junto a la otra («nadie ganó, quedaron igual»).</p>
<p>La pantalla de resultado (capítulo 60) es la misma para los dos casos; solo cambian el título, la frase y esta
ilustración. Por eso <code>IconoResultado</code> es un componente con un interruptor, <code>setEmpate</code>, que
cambia lo que dibuja. El trofeo en sí ya lo tienes en <code>Iconos.TROFEO</code> (capítulo 42); aquí solo lo
colocamos y le agregamos los destellos.</p>
<figure><img src="capturas/5-victoria.png"><figcaption>Victoria: el trofeo cian con seis destellos (rosa arriba,
cian al medio, morado abajo, a cada lado).</figcaption></figure>
<figure><img src="capturas/6-empate.png"><figcaption>Empate: la misma pantalla, pero el IconoResultado dibuja una X
rosa y una O azul.</figcaption></figure>

<h2>Qué vas a aprender</h2>
<ul>
<li>A declarar arreglos constantes con valores (<code>int[]</code> y <code>Color[]</code>) y qué significa
<code>final</code> en un arreglo.</li>
<li>A colocar puntos alrededor de un centro con <code>Math.cos</code> y <code>Math.sin</code>, y por qué hay que
pasar los grados a radianes.</li>
<li>Por qué se <b>resta</b> el seno en la pantalla (la y crece hacia abajo).</li>
<li>A alternar colores con el operador módulo <code>%</code>.</li>
<li>A hacer un componente con dos «modos» de dibujo controlados por un <code>boolean</code>.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>NetBeans: <i>&lt;default package&gt;</i> → <i>New → Java Class…</i> → <code>IconoResultado</code> →
<i>Finish</i>. Borra la plantilla y escribe el código.</li>
<li>Alternativa: <code>New-Item src\IconoResultado.java</code>.</li>
</ol>
""",
    "archivos": [
        {"ruta": "src/IconoResultado.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.Color</code>: para el arreglo de colores de los destellos.</p>
<p class="l"><b>L2–L3</b> <code>Graphics</code> y <code>Graphics2D</code>: el pincel.</p>
<p class="l"><b>L4</b> <code>java.awt.geom.Line2D</code>: cada destello es un segmento de recta.</p>
<p class="l"><b>L5</b> <code>javax.swing.JComponent</code>: la base; solo dibuja.</p>
<p><code>Math</code>, que usaremos para el seno y el coseno, está en <code>java.lang</code> y no se importa.</p>
"""),
             ("public class IconoResultado", r"""
<p class="l"><b>L7–L10</b> Comentario: qué dibuja en cada caso.</p>
<p class="l"><b>L11</b> <code>public class IconoResultado extends JComponent {</code> un componente que solo
dibuja.</p>
"""),
             ("private static final int[] ANGULOS", r"""
<p class="l"><b>L13</b> Comentario: los ángulos se dan en grados.</p>
<p class="l"><b>L14</b> <code>private static final int[] ANGULOS = {145, 180, 215, 35, 0, -35};</code> un
<b>arreglo</b> de seis enteros (capítulo 15), escrito directamente con sus valores entre llaves. Son las
direcciones de los destellos, medidas como en matemáticas: 0° apunta a la derecha, 90° hacia arriba, 180° a la
izquierda, y los negativos van hacia abajo. Los tres primeros (145°, 180°, 215°) forman el abanico de la izquierda
y los tres últimos (35°, 0°, −35°) el de la derecha. Al estar en un arreglo, agregar un destello es agregar un
número.</p>
<p class="l"><b>L15</b> <code>private static final Color[] COLORES = {Tema.ROSA, Tema.CIAN, Tema.MORADO};</code>
los colores que se irán turnando. Un detalle sobre <code>final</code> en arreglos: impide que la variable
<code>COLORES</code> apunte a <b>otro</b> arreglo, pero no impide cambiar sus elementos (<code>COLORES[0] =
...</code> compilaría). Como son privados y nadie los toca, no es un problema; solo conviene saberlo.</p>
<p class="l"><b>L17</b> <code>private boolean empate;</code> el interruptor: <code>false</code> (por defecto) =
trofeo; <code>true</code> = X y O.</p>
"""),
             ("public IconoResultado()", r"""
<p class="l"><b>L19</b> El constructor.</p>
<p class="l"><b>L20</b> <code>Dibujo.fijarTamano(this, 260, 100);</code> 260 × 100. El trofeo ocupa 84 de ancho;
los destellos llegan hasta 80 píxeles a cada lado del centro y su halo un poco más, de ahí el ancho generoso.</p>
<p class="l"><b>L21</b> Centrado horizontal.</p>
<p class="l"><b>L24</b> <code>public void setEmpate(boolean empate) {</code> cambia de modo. La pantalla de
resultado lo llama cada vez que muestra un resultado: <code>icono.setEmpate(true)</code> si fue empate,
<code>false</code> si alguien ganó. Como la misma pantalla se reutiliza partida tras partida, el icono debe poder
cambiar en las dos direcciones.</p>
<p class="l"><b>L25</b> Guarda el modo.</p>
<p class="l"><b>L26</b> <code>repaint();</code> para que se vea el cambio.</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L29–L30</b> <code>paintComponent</code>: el dibujo.</p>
<p class="l"><b>L31</b> Copia suavizada del pincel.</p>
<p class="l"><b>L32</b> <code>double cx = getWidth() / 2.0;</code> centro horizontal: 130.</p>
<p class="l"><b>L33</b> <code>double cy = getHeight() / 2.0;</code> centro vertical: 50. Todo se dibuja
<b>respecto a este centro</b>; si cambiaras el tamaño del componente, el dibujo seguiría centrado.</p>
"""),
             ("if (empate) {", r"""
<p class="l"><b>L34</b> <code>if (empate) {</code> modo empate.</p>
<p class="l"><b>L35</b> <code>Dibujo.dibujarFicha(g2, 'X', cx - 40, cy, 54, 7f);</code> una X con centro 40
píxeles a la izquierda, en (90, 50), de 54 de tamaño (la X se dibuja al 84&nbsp;%, unos 45 píxeles, para que pese lo
mismo a la vista que la O, capítulo 41) y trazo de 7, grueso, con el núcleo blanco del neón.</p>
<p class="l"><b>L36</b> Una O con centro 40 píxeles a la derecha, en (170, 50), del mismo tamaño. Entre las dos
quedan unos 30 píxeles libres.</p>
<p class="l"><b>L37</b> <code>} else {</code> si no es empate, alguien ganó: trofeo con destellos.</p>
"""),
             ("for (int i = 0; i < ANGULOS.length", r"""
<p class="l"><b>L38</b> <code>for (int i = 0; i &lt; ANGULOS.length; i++) {</code> una vuelta por destello.
<code>ANGULOS.length</code> es el tamaño del arreglo (6); usarlo en vez de escribir 6 hace que el bucle se adapte
solo si agregas o quitas ángulos.</p>
<p class="l"><b>L39</b> <code>double a = Math.toRadians(ANGULOS[i]);</code> convierte el ángulo de grados a
<b>radianes</b>. <code>Math.cos</code> y <code>Math.sin</code> no trabajan en grados: trabajan en radianes, otra
forma de medir ángulos donde media vuelta (180°) vale π ≈ 3,1416. Si te saltaras la conversión,
<code>Math.cos(180)</code> tomaría «180 radianes» (unas 28,6 vueltas) y los destellos saldrían en direcciones
sin sentido.</p>
<p class="l"><b>L40</b> <code>double r1 = 58;</code> distancia desde el centro a la que <b>empieza</b> cada
destello. El trofeo mide 84 (42 hacia cada lado), así que empezar en 58 deja 16 píxeles de aire: los destellos no
tocan el trofeo.</p>
<p class="l"><b>L41</b> <code>double r2 = i % 3 == 1 ? 80 : 72;</code> distancia a la que <b>termina</b>.
<code>%</code> es el <b>módulo</b>, el resto de la división (capítulo 12): 0 % 3 = 0, 1 % 3 = 1, 2 % 3 = 2, 3 % 3 = 0,
4 % 3 = 1, 5 % 3 = 2. Vale 1 en las vueltas 1 y 4, que son los destellos de 180° y 0°, los del medio de cada
abanico: esos llegan a 80 (miden 22) y los demás a 72 (miden 14). El comentario de la línea lo dice.</p>
<p class="l"><b>L42–L44</b> <code>Line2D destello = new Line2D.Double(...)</code> crea el segmento entre dos puntos.
Cada punto se calcula igual: <b>x = cx + cos(a) · r</b> y <b>y = cy − sin(a) · r</b>. El coseno dice cuánto se avanza
en horizontal por cada píxel de distancia en esa dirección y el seno cuánto en vertical. El signo <b>menos</b> en la
y es porque en matemáticas la y crece hacia arriba y en la pantalla crece hacia <b>abajo</b> (capítulo 37): sin él,
el destello de 35° (arriba a la derecha) saldría abajo a la derecha. Primer punto con <code>r1</code>, segundo con
<code>r2</code>. La instrucción ocupa tres líneas para que se lean por separado los dos puntos.</p>
<p class="l"><b>L45</b> <code>Dibujo.trazoNeon(g2, destello, COLORES[i % COLORES.length], 3.5f, 0.8f);</code>
dibuja el destello en neón (3,5 de grosor, intensidad 0,8). El color se elige con otro módulo: <code>i % 3</code>
recorre 0, 1, 2, 0, 1, 2, así que los colores se turnan rosa, cian, morado, rosa, cian, morado. Como los ángulos
están ordenados de arriba abajo en cada lado, los dos abanicos quedan simétricos: rosa arriba, cian al medio, morado
abajo. Escribir <code>COLORES.length</code> en vez de 3 permite agregar un cuarto color sin tocar esta línea.</p>
"""),
             ("Iconos.TROFEO.dibujar", r"""
<p class="l"><b>L47</b> <code>Iconos.TROFEO.dibujar(g2, cx - 42, cy - 44, 84, Tema.CIAN);</code> el trofeo cian en
un cuadrado de 84 cuya esquina está en (88, 6). Para centrarlo bastaría <code>cy - 42</code>; con
<code>- 44</code> queda dos píxeles más arriba, un ajuste óptico: la base del trofeo es pesada y, centrado al
milímetro, parecería caído. Se dibuja <b>después</b> de los destellos para que quede encima si alguna vez se
tocaran.</p>
<p class="l"><b>L48</b> Cierra el <code>if/else</code>.</p>
<p class="l"><b>L49</b> Libera la copia del pincel.</p>
<p class="l"><b>L50–L51</b> Cierran el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>1. Los seis destellos, calculados</h3>
<p>Con el centro en (130, 50), estos son los extremos de cada destello (redondeados a un decimal):</p>
<table class="tabla">
<tr><th>i</th><th>Ángulo</th><th>cos</th><th>sin</th><th>Desde (r1 = 58)</th><th>Hasta</th><th>Color</th></tr>
<tr><td>0</td><td>145°</td><td>−0,819</td><td>0,574</td><td>(82,5; 16,7)</td><td>(71,0; 8,7) con r2 = 72</td><td>rosa</td></tr>
<tr><td>1</td><td>180°</td><td>−1</td><td>0</td><td>(72; 50)</td><td>(50; 50) con r2 = 80</td><td>cian</td></tr>
<tr><td>2</td><td>215°</td><td>−0,819</td><td>−0,574</td><td>(82,5; 83,3)</td><td>(71,0; 91,3) con r2 = 72</td><td>morado</td></tr>
<tr><td>3</td><td>35°</td><td>0,819</td><td>0,574</td><td>(177,5; 16,7)</td><td>(189,0; 8,7) con r2 = 72</td><td>rosa</td></tr>
<tr><td>4</td><td>0°</td><td>1</td><td>0</td><td>(188; 50)</td><td>(210; 50) con r2 = 80</td><td>cian</td></tr>
<tr><td>5</td><td>−35°</td><td>0,819</td><td>−0,574</td><td>(177,5; 83,3)</td><td>(189,0; 91,3) con r2 = 72</td><td>morado</td></tr>
</table>
<p>Comprueba uno a mano. Para i = 3 (35°): x = 130 + 0,819 × 58 = 130 + 47,5 = 177,5; y = 50 − 0,574 × 58 = 50 −
33,3 = 16,7. Está arriba (y pequeña) y a la derecha (x grande): correcto. Si en vez de restar sumaras, y saldría
83,3: abajo a la derecha, donde debería ir el de −35°.</p>
<svg viewBox="0 0 260 100" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="260" height="100" fill="#1C1740"></rect>
<circle cx="130" cy="50" r="58" fill="none" stroke="#C8BCF6" stroke-width="0.6" stroke-dasharray="3 3"></circle>
<rect x="88" y="6" width="84" height="84" fill="none" stroke="#2F84FF" stroke-width="0.8" stroke-dasharray="4 2"></rect>
<circle cx="130" cy="50" r="2" fill="#C8BCF6"></circle>
<line x1="82.5" y1="16.7" x2="71" y2="8.7" stroke="#FF3BD4" stroke-width="3.5" stroke-linecap="round"></line>
<line x1="72" y1="50" x2="50" y2="50" stroke="#40C8FF" stroke-width="3.5" stroke-linecap="round"></line>
<line x1="82.5" y1="83.3" x2="71" y2="91.3" stroke="#A05CFF" stroke-width="3.5" stroke-linecap="round"></line>
<line x1="177.5" y1="16.7" x2="189" y2="8.7" stroke="#FF3BD4" stroke-width="3.5" stroke-linecap="round"></line>
<line x1="188" y1="50" x2="210" y2="50" stroke="#40C8FF" stroke-width="3.5" stroke-linecap="round"></line>
<line x1="177.5" y1="83.3" x2="189" y2="91.3" stroke="#A05CFF" stroke-width="3.5" stroke-linecap="round"></line>
<text x="46" y="12" fill="#C8BCF6" font-size="8">145°</text>
<text x="22" y="53" fill="#C8BCF6" font-size="8">180°</text>
<text x="46" y="97" fill="#C8BCF6" font-size="8">215°</text>
<text x="194" y="12" fill="#C8BCF6" font-size="8">35°</text>
<text x="215" y="53" fill="#C8BCF6" font-size="8">0°</text>
<text x="194" y="97" fill="#C8BCF6" font-size="8">−35°</text>
<text x="106" y="53" fill="#C8BCF6" font-size="7">(130, 50)</text>
</svg>
<p>En el esquema, el círculo punteado es el radio 58 donde empiezan los destellos y el cuadrado azul punteado es
donde se dibuja el trofeo (88, 6, 84 × 84).</p>

<h3>2. El mismo componente, dos dibujos</h3>
<table class="tabla">
<tr><th>Llamada</th><th>empate</th><th>Qué dibuja</th></tr>
<tr><td>(recién creado)</td><td>false</td><td>trofeo con destellos</td></tr>
<tr><td><code>setEmpate(true)</code></td><td>true</td><td>X en (90, 50) y O en (170, 50)</td></tr>
<tr><td><code>setEmpate(false)</code></td><td>false</td><td>trofeo con destellos otra vez</td></tr>
</table>
<div class="caja concepto"><b>Círculos sin dolor</b> La pareja <b>(cx + cos(a)·r, cy − sin(a)·r)</b> es todo lo
que necesitas para poner cosas alrededor de un centro: las horas de un reloj, los pétalos de una flor, los rayos de
un sol, las opciones de un menú circular. Cambia <code>a</code> para girar y <code>r</code> para alejar.</div>

<h2>Compila y prueba</h2>
<p><i>Run → Clean and Build Project</i> → <code>BUILD SUCCESS</code>. El icono se verá en la pantalla de resultado
(capítulo 60) y en la pantalla de prueba del capítulo 56.</p>
<table class="tabla">
<tr><th>Problema</th><th>Causa y solución</th></tr>
<tr><td>(al verlo) los destellos salen en direcciones raras</td><td>Falta <code>Math.toRadians</code>: se están
pasando grados a <code>cos</code> y <code>sin</code>.</td></tr>
<tr><td>(al verlo) los destellos de arriba salen abajo y al revés</td><td>Sumaste el seno en la y; debe
restarse.</td></tr>
<tr><td><i>cannot find symbol: variable TROFEO</i></td><td>Tu <code>Iconos</code> no tiene ese icono; revisa el
capítulo 42.</td></tr>
<tr><td><i>illegal start of expression</i> en la línea 14</td><td>Las llaves <code>{...}</code> para dar valores
solo valen al declarar el arreglo; revisa que esté escrito como en el código.</td></tr>
</table>

<div class="caja git"><b>Git</b>
<pre class="ps">git add src\IconoResultado.java
git commit -m "IconoResultado: trofeo y empate"
git push</pre></div>

<h2>Resumen</h2>
<ul>
<li><code>IconoResultado</code> dibuja un trofeo con destellos o, con <code>setEmpate(true)</code>, una X y una O.</li>
<li>Los arreglos constantes (<code>ANGULOS</code>, <code>COLORES</code>) separan los datos del código que los usa.</li>
<li>Para colocar algo alrededor de un centro: <b>x = cx + cos(a)·r</b>, <b>y = cy − sin(a)·r</b>, con el ángulo
en radianes (<code>Math.toRadians</code>).</li>
<li>Se resta el seno porque la y de la pantalla crece hacia abajo.</li>
<li>El módulo <code>%</code> sirve para alternar (colores, filas pares e impares, turnos).</li>
<li>Usar <code>.length</code> en vez de números fijos hace que el código se adapte solo.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Relojes y medidores</b>: las 12 marcas de un reloj analógico (cada 30°) o la aguja de un velocímetro se
calculan con la misma fórmula.</li>
<li><b>Gráficas circulares</b>: las etiquetas de un gráfico de pastel se colocan en el ángulo medio de cada
porción, a un radio un poco mayor que el del pastel.</li>
<li><b>Juegos</b>: disparar en la dirección en que apunta una nave, mover enemigos en círculo o hacer una
explosión de partículas en todas direcciones.</li>
<li><b>Alternar con módulo</b>: filas de una tabla en dos tonos (<code>fila % 2</code>), repartir tareas entre tres
personas por turnos (<code>i % 3</code>), o el turno del Totito entre dos jugadores.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Calcula a mano los dos extremos de un destello a 90° (hacia arriba) con r1 = 58 y r2 = 72. ¿Cabría en un
componente de 100 de alto?</li>
<li>Agrega dos destellos más, a 160° y a 20°. ¿Qué colores les tocan con el módulo? ¿Siguen siendo simétricos los
lados? Pista: el orden del arreglo importa.</li>
<li>Cambia los destellos para que todos sean del color del ganador. Tendrás que agregar un método
<code>setColor(Color)</code> y usarlo en lugar de <code>COLORES</code>.</li>
<li>Haz un reloj: un <code>JComponent</code> que dibuje 12 rayitas alrededor de un centro, una cada 30°, con la
de las 12 más larga. Míralo con la vista previa del capítulo 56.</li>
<li>Reto: en el modo empate, dibuja un signo «=» neón entre la X y la O.</li>
</ol></div>
""",
}
