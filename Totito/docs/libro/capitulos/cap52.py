# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 52,
    "titulo": "PanelMarcador.java: el marcador que se lee de la partida",
    "antes": r"""
<p class="entrada">Durante la partida, arriba del tablero, hay un marcador: una ficha por jugador con su símbolo, su
nombre y sus victorias, y en el centro los empates. La ficha de quien tiene el turno brilla. En este capítulo lo
construyes y descubres una idea muy útil: el marcador <b>no guarda números</b>, los lee de la
<code>Partida</code> cada vez que se dibuja.</p>

<h2>Por qué existe este archivo</h2>
<p>La pantalla de juego no estaba en el diseño original (solo había menú, instrucciones, configuración y victoria,
capítulo 34), así que la diseñamos con las mismas piezas y colores. El jugador necesita saber, de un vistazo,
<b>quién es quién</b> (qué ficha tiene cada nombre), <b>cómo va la serie</b> (victorias y empates) y <b>a quién le
toca</b>. Todo eso cabe en una franja de 590 × 82 píxeles.</p>
<p>Los datos ya existen: <code>Partida</code> (capítulo 38) sabe los jugadores, las victorias, los empates, el
estado y quién tiene el turno. El marcador solo tiene que <b>mostrarlos</b>. Separar «quién sabe los datos» (la
lógica) de «quién los muestra» (la interfaz) es la idea de modelo y vista del capítulo 27.</p>
<figure><img src="capturas/4-juego.png"><figcaption>El PanelMarcador arriba de la pantalla de juego: Ana (X) a la
izquierda, encendida porque es su turno; Luis (O) a la derecha, apagado; «EMPATES 0» en el centro.</figcaption></figure>

<h2>Qué vas a aprender</h2>
<ul>
<li>A hacer un componente que muestra un <b>modelo</b> (la <code>Partida</code>) sin copiar sus datos.</li>
<li>A protegerse de un modelo que todavía no existe (<code>partida == null</code>).</li>
<li>A comparar con <code>==</code> referencias de objetos y valores de un <code>enum</code>.</li>
<li>A repartir un ancho en tres zonas (izquierda, centro, derecha) con cuentas sencillas.</li>
<li><code>String.valueOf</code>, la fuente con letras espaciadas de <code>Tema</code> y el recorte de nombres largos
con «…».</li>
</ul>

<h2>El plano del marcador, en píxeles</h2>
<p>Mide <b>590 × 82</b>. El centro reserva 104 píxeles para los empates; lo que sobra se reparte en dos fichas de
(590 − 104) / 2 = <b>243</b>.</p>
<table class="tabla">
<tr><th>Zona</th><th>De x a x</th><th>Contenido</th></tr>
<tr><td>Ficha del Jugador 1</td><td>0 – 243</td><td>caja (8, 8) de 227 × 66; símbolo con centro (42, 41); nombre y victorias desde x = 72</td></tr>
<tr><td>Centro</td><td>243 – 347</td><td>«EMPATES» (línea base 32) y el número (línea base 62), centrados en x = 295</td></tr>
<tr><td>Ficha del Jugador 2</td><td>347 – 590</td><td>caja (355, 8) de 227 × 66; símbolo con centro (389, 41); textos desde x = 419</td></tr>
</table>

<h2>Créalo</h2>
<ol>
<li>NetBeans: <i>&lt;default package&gt;</i> → <i>New → Java Class…</i> → <code>PanelMarcador</code> →
<i>Finish</i>. Borra la plantilla y escribe el código.</li>
<li>Alternativa: <code>New-Item src\PanelMarcador.java</code>.</li>
</ol>
<p>Necesitas <code>Partida</code> (capítulo 38) y <code>Jugador</code> (capítulo 30).</p>
""",
    "archivos": [
        {"ruta": "src/PanelMarcador.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.Color</code>: el color de cada ficha.</p>
<p class="l"><b>L2</b> <code>java.awt.Font</code>: constantes <code>BOLD</code> y <code>PLAIN</code>.</p>
<p class="l"><b>L3</b> <code>java.awt.FontMetrics</code>: medir textos para centrarlos y recortarlos.</p>
<p class="l"><b>L4–L5</b> <code>Graphics</code> y <code>Graphics2D</code>: el pincel.</p>
<p class="l"><b>L6</b> <code>java.awt.geom.RoundRectangle2D</code>: la caja redondeada de cada jugador.</p>
<p class="l"><b>L7</b> <code>javax.swing.JComponent</code>: la base. El marcador solo dibuja.</p>
"""),
             ("public class PanelMarcador", r"""
<p class="l"><b>L9–L13</b> Comentario: qué muestra y la regla del brillo.</p>
<p class="l"><b>L14</b> <code>public class PanelMarcador extends JComponent {</code> se llama «Panel» porque
ocupa una franja de la pantalla, pero es un <code>JComponent</code> que se dibuja entero: no contiene etiquetas ni
otros componentes. Una sola clase dibujándolo todo es más fácil de alinear al píxel que seis
<code>JLabel</code>.</p>
"""),
             ("private static final int ANCHO", r"""
<p class="l"><b>L16</b> <code>ANCHO = 590</code>: casi todo el ancho de la ventana (640), con 25 de aire a cada
lado. Es el mismo ancho que el letrero «Turno de…» de la pantalla de juego, para que todo quede alineado.</p>
<p class="l"><b>L17</b> <code>ALTO = 82</code>: una ficha de 66 más 8 de halo arriba y abajo.</p>
<p class="l"><b>L18</b> <code>ANCHO_CENTRO = 104</code>: la columna de los empates. Lo bastante ancha para la
palabra «EMPATES» (unos 70 píxeles) con aire.</p>
<p class="l"><b>L20</b> <code>private Partida partida;</code> la partida que se muestra. No es <code>final</code>
porque cambia: cada vez que empieza una partida nueva se muestra otra. Empieza en <code>null</code>: al crear la
pantalla de juego todavía no hay partida.</p>
"""),
             ("public PanelMarcador()", r"""
<p class="l"><b>L22</b> El constructor, sin parámetros.</p>
<p class="l"><b>L23</b> Tamaño fijo de 590 × 82.</p>
<p class="l"><b>L24</b> Centrado en horizontal dentro de la columna de la pantalla.</p>
<p class="l"><b>L27</b> <code>public void mostrar(Partida partida) {</code> le dice al marcador qué partida
mostrar. La pantalla de juego (capítulo 59) lo llama después de cada jugada.</p>
<p class="l"><b>L28</b> <code>this.partida = partida;</code> guarda <b>una referencia</b> a la partida, no una
copia de sus números (capítulo 18). El marcador y la pantalla miran el mismo objeto: si la partida cambia, el
marcador lo verá en su próximo dibujo.</p>
<p class="l"><b>L29</b> <code>repaint();</code> pide redibujar ya, con lo que haya ahora en la partida.</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L32–L33</b> <code>paintComponent</code>: el dibujo.</p>
<p class="l"><b>L34–L36</b> <code>if (partida == null) { return; }</code> si todavía no hay partida, no dibuja
nada y sale. Sin esta guarda, la línea 39 haría <code>partida.getEstado()</code> sobre <code>null</code> y Swing
mostraría un <code>NullPointerException</code> en la consola en cada repintado (por ejemplo, si la pantalla de
juego se viera antes de empezar una partida). Fíjate en que va <b>antes</b> de crear la copia del pincel: si
saliéramos después, quedaría una copia sin liberar.</p>
<p class="l"><b>L37</b> Copia suavizada del pincel.</p>
"""),
             ("int anchoFicha", r"""
<p class="l"><b>L38</b> <code>int anchoFicha = (getWidth() - ANCHO_CENTRO) / 2;</code> ancho de cada ficha: (590 −
104) / 2 = <b>243</b>.</p>
<p class="l"><b>L39</b> <code>boolean enCurso = partida.getEstado() == Partida.Estado.EN_CURSO;</code> ¿se está
jugando? <code>Partida.Estado</code> es el <code>enum</code> del capítulo 38 (<code>EN_CURSO</code>,
<code>VICTORIA</code>, <code>EMPATE</code>). Los valores de un <code>enum</code> se comparan con <code>==</code>
sin miedo, porque de cada uno existe un único objeto (capítulo 26). Se calcula una vez, fuera del bucle, porque no
cambia entre vuelta y vuelta.</p>
<p class="l"><b>L40</b> <code>for (int i = 0; i &lt; 2; i++) {</code> dos vueltas: <code>i = 0</code> es el Jugador
1 e <code>i = 1</code> el Jugador 2 (los índices que usa <code>Partida</code>).</p>
<p class="l"><b>L41</b> <code>Jugador jugador = partida.getJugador(i);</code> el jugador de esta vuelta.</p>
<p class="l"><b>L42</b> <code>boolean tieneTurno = enCurso &amp;&amp; partida.getJugadorEnTurno() == jugador;</code>
brilla si la partida sigue <b>y</b> (<code>&amp;&amp;</code>) es su turno. Aquí <code>==</code> compara
<b>referencias</b>: pregunta si son <i>el mismo objeto</i> <code>Jugador</code>, no si se llaman igual (capítulo
18). Es lo correcto: si los dos se llamaran «Ana», compararlos por nombre los confundiría. El
<code>enCurso</code> hace que, cuando la partida termina, ninguna ficha brille.</p>
<p class="l"><b>L43</b> <code>int x = i == 0 ? 0 : getWidth() - anchoFicha;</code> dónde empieza la ficha: el
Jugador 1 en x = 0 y el Jugador 2 en 590 − 243 = <b>347</b>, pegado a la derecha.</p>
<p class="l"><b>L44</b> Llama al ayudante que pinta la ficha con todo lo que necesita: el pincel, la x, el ancho,
el jugador, sus victorias y si tiene el turno.</p>
"""),
             ("// Empates en el centro.", r"""
<p class="l"><b>L47</b> Comentario: ahora los empates.</p>
<p class="l"><b>L48</b> <code>float centro = getWidth() / 2f;</code> el centro horizontal, 295.</p>
<p class="l"><b>L49</b> <code>Tema.fuenteEspaciada(Font.BOLD, 11f, 0.2f)</code>: negrita pequeña de 11 puntos con
las letras separadas un 20&nbsp;% (capítulo 40), el mismo estilo de rótulo que «J U G A D O R E S».</p>
<p class="l"><b>L50</b> Medidas de esa fuente (después del <code>setFont</code>).</p>
<p class="l"><b>L51</b> Color apagado: es una etiqueta, no un dato.</p>
<p class="l"><b>L52</b> <code>g2.drawString("EMPATES", centro - fm.stringWidth("EMPATES") / 2f, 32);</code> centra la
palabra restando la mitad de su ancho al centro: con unos 69 píxeles de ancho empieza en x ≈ 260,5. Línea base en
y = 32. Es la misma idea que (ancho − texto) / 2 del capítulo 50, escrita desde el centro.</p>
"""),
             ("g2.setFont(Tema.fuente(Font.BOLD, 24f));", r"""
<p class="l"><b>L53</b> Para el número, negrita grande de 24 puntos: es el dato que interesa.</p>
<p class="l"><b>L54</b> <code>fm = g2.getFontMetrics();</code> hay que volver a pedir las medidas: las de la línea
50 eran de la fuente pequeña. Se reutiliza la misma variable <code>fm</code>.</p>
<p class="l"><b>L55</b> <code>String empates = String.valueOf(partida.getEmpates());</code>
<code>String.valueOf</code> convierte el número (un <code>int</code>) en texto: 3 → <code>"3"</code>. Hace falta
porque <code>drawString</code> y <code>stringWidth</code> trabajan con textos.</p>
<p class="l"><b>L56</b> En lavanda, más claro que la etiqueta.</p>
<p class="l"><b>L57</b> El número centrado en x = 295 con línea base 62.</p>
<p class="l"><b>L58</b> Libera la copia del pincel.</p>
"""),
             ("private void pintarJugador", r"""
<p class="l"><b>L61</b> <code>private void pintarJugador(Graphics2D g2, int x, int ancho, Jugador jugador, int
victorias, boolean tieneTurno) {</code> un ayudante con seis parámetros. Se usa dos veces (una por jugador), por eso
existe: el dibujo de una ficha se escribe una sola vez.</p>
<p class="l"><b>L62</b> <code>Color color = Tema.colorDeFicha(jugador.getFicha());</code> el color sale de la
<b>ficha</b>, no de la posición: si el Jugador 1 eligió la O, su ficha de la izquierda será azul.</p>
<p class="l"><b>L63</b> La caja: desde (x + 8, 8), de (243 − 16) × (82 − 16) = <b>227 × 66</b>, esquinas de 22. Para
el Jugador 1 empieza en (8, 8); para el Jugador 2, en (355, 8).</p>
<p class="l"><b>L64</b> Relleno del color de la ficha: alfa 45 si tiene el turno, 14 si no.</p>
<p class="l"><b>L65</b> Rellena.</p>
<p class="l"><b>L66</b> Borde de neón de 1,8: intensidad 1,3 (brilla) con el turno, 0,35 (casi apagado) sin él.</p>
"""),
             ("double cy = getHeight() / 2.0;", r"""
<p class="l"><b>L68</b> El centro vertical: 82 / 2,0 = 41.</p>
<p class="l"><b>L69</b> <code>Dibujo.dibujarFicha(g2, jugador.getFicha(), x + 8 + 34, cy, 28, 4.5f);</code> el
símbolo del jugador, con centro en (42, 41) para el Jugador 1 (8 de halo + 34 hacia adentro), de 28 píxeles y trazo
de 4,5. Como el trazo es menor que 5, no lleva el centro blanco: a este tamaño se vería como un borrón.</p>
"""),
             ("int xTexto", r"""
<p class="l"><b>L71</b> <code>int xTexto = x + 8 + 64;</code> los textos empiezan en x = 72 (o 419 para el Jugador
2), a la derecha del símbolo.</p>
<p class="l"><b>L72</b> Nombre en negrita de 17 puntos.</p>
<p class="l"><b>L73</b> Las medidas de esa fuente (las necesita el recorte).</p>
<p class="l"><b>L74</b> Blanco.</p>
<p class="l"><b>L75</b> <code>Dibujo.recortar(fm, jugador.getNombre(), ancho - 16 - 64 - 12)</code> (capítulo 41)
devuelve el nombre tal cual si cabe en 243 − 16 − 64 − 12 = <b>151</b> píxeles, o recortado con «…» si no.
<code>CampoTexto</code> ya limita los nombres a 14 letras (capítulo 47), pero 14 letras anchas pueden no caber:
«WALTER MORALES» mide unos 162 píxeles y se mostraría «WALTER MORA…». Sin el recorte, el nombre invadiría la zona
de los empates. Se escribe con la línea base en 41 − 2 = 39.</p>
<p class="l"><b>L76–L77</b> Letra normal de 13 puntos en color apagado.</p>
<p class="l"><b>L78</b> <code>"Victorias: " + victorias</code>: al unir un texto con un <code>int</code>, Java
convierte el número en texto solo. Línea base en 41 + 17 = 58.</p>
<p class="l"><b>L79–L80</b> Cierran el método y la clase. Este ayudante no llama a <code>dispose()</code>: el
pincel no es suyo, se lo prestó <code>paintComponent</code>, que es quien lo libera en la línea 58.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>1. Una traza con valores</h3>
<p>Ana juega con X (Jugador 1) y Luis con O (Jugador 2). Llevan varias partidas: Ana ha ganado 2, Luis 1 y hubo 3
empates. La partida actual está en curso y le toca a Luis. La pantalla de juego llama a
<code>marcador.mostrar(partida)</code>. Al dibujar:</p>
<table class="tabla">
<tr><th>Paso</th><th>Valores</th></tr>
<tr><td>Guarda inicial</td><td><code>partida</code> no es <code>null</code>: se sigue.</td></tr>
<tr><td>L38–L39</td><td><code>anchoFicha</code> = 243; <code>enCurso</code> = true.</td></tr>
<tr><td>Vuelta i = 0</td><td>jugador = Ana; <code>getJugadorEnTurno()</code> es Luis, distinto objeto →
<code>tieneTurno</code> = false; x = 0; victorias = 2. Ficha rosa apagada (alfa 14, intensidad 0,35), X en (42, 41),
«Ana» y «Victorias: 2» desde x = 72.</td></tr>
<tr><td>Vuelta i = 1</td><td>jugador = Luis; es el mismo objeto que el del turno → <code>tieneTurno</code> = true;
x = 347; victorias = 1. Ficha azul encendida (alfa 45, intensidad 1,3), O en (389, 41), «Luis» y «Victorias: 1» desde
x = 419.</td></tr>
<tr><td>Centro</td><td>«EMPATES» centrado en 295; <code>String.valueOf(3)</code> = "3" debajo.</td></tr>
</table>
<p>Luis juega y gana. <code>Partida</code> cambia su estado a <code>VICTORIA</code> y suma la victoria. La pantalla
vuelve a llamar a <code>mostrar</code>: ahora <code>enCurso</code> es false, así que <b>ninguna</b> ficha brilla, y
la de Luis dice «Victorias: 2». El marcador no tuvo que «enterarse» de nada: leyó la partida otra vez.</p>

<h3>2. Por qué no copiar los números</h3>
<p>Otra forma de hacerlo sería que el marcador tuviera campos <code>victorias1</code>, <code>victorias2</code>,
<code>empates</code> y métodos para cambiarlos. Entonces, cada vez que alguien gana, habría que acordarse de
actualizar <b>dos</b> sitios: la partida y el marcador. El día que se olvide uno, el marcador mentirá. Leyendo de
la única fuente de verdad (la <code>Partida</code>), eso no puede pasar.</p>
<div class="caja concepto"><b>Una sola fuente de verdad</b> Cada dato debe vivir en un solo lugar. Las vistas lo
leen; no lo copian. Es la misma idea del selector de símbolos (capítulo 50), pero a mayor escala: aquí el dato
vive en otra clase.</div>

<h2>Compila y prueba</h2>
<p><i>Run → Clean and Build Project</i> → <code>BUILD SUCCESS</code>. El marcador se verá en la pantalla de juego
(capítulo 59). En la pantalla de prueba del capítulo 56 podrás verlo con una partida inventada.</p>
<table class="tabla">
<tr><th>Problema</th><th>Causa y solución</th></tr>
<tr><td><i>cannot find symbol: method getJugadorEnTurno()</i> (u otro de <code>Partida</code>)</td><td>Tu
<code>Partida</code> no tiene ese método o se llama distinto. Compara con el capítulo 38.</td></tr>
<tr><td><i>cannot find symbol: variable Estado</i></td><td>Escribe <code>Partida.Estado.EN_CURSO</code>: el
<code>enum</code> está declarado dentro de <code>Partida</code>.</td></tr>
<tr><td>(al usarlo) <code>NullPointerException</code> en <code>paintComponent</code></td><td>Falta la guarda de
las líneas 34–36, o está después de usar <code>partida</code>.</td></tr>
</table>

<div class="caja git"><b>Git</b>
<pre class="ps">git add src\PanelMarcador.java
git commit -m "PanelMarcador: marcador de la partida"
git push</pre></div>

<h2>Resumen</h2>
<ul>
<li>El marcador guarda una <b>referencia</b> a la <code>Partida</code> y lee sus datos en cada dibujo.</li>
<li>La guarda <code>partida == null</code> evita errores cuando aún no hay partida.</li>
<li>Los valores de un <code>enum</code> y la identidad de objetos se comparan con <code>==</code>.</li>
<li>El ancho se reparte: centro fijo de 104 y dos fichas de (590 − 104) / 2.</li>
<li>Un ayudante privado pinta cada ficha; el color sale de la ficha del jugador.</li>
<li>Los nombres largos se recortan con «…» para no invadir otras zonas.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Marcadores deportivos</b>: local, visitante y tiempo en el centro, leyendo un objeto <code>Partido</code>.</li>
<li><b>Paneles de resumen</b>: en un inventario, «Productos», «Agotados» y «Valor total» leyendo de la lista de
productos en cada repintado, en vez de llevar contadores aparte.</li>
<li><b>Resaltar al activo</b>: en un chat, el contacto que está escribiendo; en un juego por turnos, el jugador
actual; en un reproductor, la canción que suena.</li>
<li><b>Recortar textos</b>: nombres de archivo largos en una lista o títulos de productos en una tarjeta, con
<code>Dibujo.recortar</code> o la misma idea.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Si <code>ANCHO_CENTRO</code> fuera 140, ¿cuánto mediría cada ficha y dónde empezaría la del Jugador 2?</li>
<li>Cambia «Victorias: n» por «n victorias», cuidando el singular: «1 victoria».</li>
<li>Agrega debajo del número de empates el total de partidas jugadas (victorias de los dos + empates).</li>
<li>Explica qué pasaría si en la línea 42 se comparara por nombre
(<code>partida.getJugadorEnTurno().getNombre().equals(jugador.getNombre())</code>) y los dos jugadores escribieran
«Ana». ¿Y si los dos dejaran el nombre vacío? Pista: recuerda qué devuelve <code>getNombre()</code> de la tarjeta
(capítulo 49).</li>
<li>Reto: cuando la partida termine con victoria, haz que brille la ficha del <b>ganador</b> (usa
<code>partida.getGanador()</code>).</li>
</ol></div>
""",
}
