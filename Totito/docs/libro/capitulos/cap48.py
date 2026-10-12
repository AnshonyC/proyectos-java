CAPITULO = {
    "numero": 48,
    "titulo": "PanelTablero.java: el tablero que dibuja y avisa",
    "antes": r"""
<p class="entrada">El corazón visual del juego: el tablero de 3 × 3 con sus casillas, la rejilla de neón, las X
rosas y las O azules, la ficha «fantasma» que anticipa tu jugada y la raya sobre la línea ganadora. Lo más importante
de este componente no es lo que hace, sino lo que <b>no</b> hace: no sabe nada de reglas ni de turnos. Solo dibuja y,
cuando haces clic, avisa a quien le interese.</p>

<h2>Por qué existe este archivo</h2>
<p>En el capítulo 33 el tablero eran nueve <code>JButton</code> en una rejilla. Cada botón, al pulsarse, marcaba la
casilla, comprobaba si había ganador y cambiaba el turno: la lógica y el dibujo estaban mezclados. Para la versión
1.0 los separamos:</p>
<ul>
<li><code>Tablero</code> y <code>Partida</code> (capítulos 29 y 38) saben las reglas.</li>
<li><code>PanelTablero</code> sabe <b>dibujar</b> un tablero y traducir un clic en «fila 2, columna 1».</li>
<li>La pantalla de juego (capítulo 59) une las dos cosas: cuando el panel avisa de un clic, le pide a la partida que
juegue ahí y después le dice al panel que muestre el tablero nuevo.</li>
</ul>
<p>Gracias a esa separación, el mismo componente sirve en <b>tres</b> lugares con tamaños distintos: el tablero de la
partida (casillas de 100 píxeles, acepta clics), el de la pantalla de victoria (casillas de 66, solo muestra la jugada
ganadora) y el pequeño ejemplo de las instrucciones (casillas de 46).</p>
<figure><img src="capturas/4-juego.png"><figcaption>El tablero de la partida: casillas, rejilla, fichas y, bajo el
ratón, la ficha fantasma de quien tiene el turno.</figcaption></figure>
<figure><img src="capturas/5-victoria.png"><figcaption>El mismo componente, más pequeño, en la pantalla de victoria,
con la raya sobre la línea ganadora.</figcaption></figure>

<h2>Qué vas a aprender</h2>
<ul>
<li>Un componente que <b>solo dibuja</b> y delega las decisiones: separar la interfaz de la lógica (capítulo 27).</li>
<li>Una <b>interfaz interna</b>, <code>OyenteCasilla</code>, y el patrón <b>observador</b> (Observer).</li>
<li>Escuchar el ratón con <code>MouseAdapter</code>: moverse, salir y apretar.</li>
<li>Convertir píxeles en fila y columna con <code>Math.floor</code>, y por qué no basta con un <i>cast</i>.</li>
<li>Calcular toda la geometría a partir de un solo número (el tamaño de casilla).</li>
<li>Pintar por <b>capas</b>: marco, casillas, rejilla, fichas, fantasma y raya.</li>
<li>Prolongar un segmento la misma distancia en cualquier dirección <b>normalizando</b> el vector.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>En la rama <code>interfaz-neon</code>: clic derecho en <i>&lt;default package&gt;</i> → <i>New → Java Class…</i> →
<code>PanelTablero</code> → <i>Finish</i>.</li>
<li>Reemplaza el esqueleto por el código.</li>
</ol>
<pre class="ps">New-Item -ItemType File src\PanelTablero.java
notepad src\PanelTablero.java</pre>
<div class="caja concepto"><b>Dependencias</b> Usa <code>Tablero</code> (capítulo 29: <code>VACIA</code> y
<code>obtenerCasilla</code>), <code>Partida.buscarLineaGanadora</code> (capítulo 38), <code>Tema</code> (40) y
<code>Dibujo</code> (41: <code>trazoNeon</code> y <code>dibujarFicha</code>).</div>
""",
    "archivos": [
        {"ruta": "src/PanelTablero.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>AlphaComposite</code>: para pintar la ficha fantasma al 28 % de opacidad.</p>
<p class="l"><b>L2</b> <code>Color</code>: el color de la rejilla y de la raya ganadora.</p>
<p class="l"><b>L3</b> <code>Cursor</code>: manita sobre las casillas jugables, flecha normal en las demás.</p>
<p class="l"><b>L4–L5</b> <code>Graphics</code> y <code>Graphics2D</code>, el pincel.</p>
"""),
             ("import java.awt.event.MouseAdapter", r"""
<p class="l"><b>L6</b> <code>java.awt.event.MouseAdapter</code>: una clase con métodos vacíos para todos los eventos
del ratón (apretar, soltar, hacer clic, entrar, salir, moverse, arrastrar, rueda). Sobrescribiremos solo tres.</p>
<p class="l"><b>L7</b> <code>java.awt.event.MouseEvent</code>: el objeto que describe un evento del ratón; lo que más
nos interesa de él es <code>getX()</code> y <code>getY()</code>, la posición del puntero dentro del componente.</p>
<p class="l"><b>L8</b> <code>Line2D</code>: las líneas de la rejilla y la raya ganadora.</p>
<p class="l"><b>L9</b> <code>RoundRectangle2D</code>: el marco y las nueve casillas.</p>
<p class="l"><b>L10</b> <code>JComponent</code>: como <code>Rotulo</code>, el tablero no contiene otros componentes;
solo dibuja.</p>
<p class="l"><b>L11</b> En blanco. Falta un import que usaremos, <code>java.util.Arrays</code>; en la línea 46 verás
otra forma de usar una clase sin importarla.</p>
"""),
             ("public class PanelTablero", r"""
<p class="l"><b>L12–L20</b> Comentario de documentación. La frase clave es «Solo DIBUJA: no sabe de reglas ni de
turnos». Describe la responsabilidad única de la clase (capítulo 27) y avisa a quien la mantenga en el futuro de que
no debe meter aquí lógica del juego.</p>
<p class="l"><b>L21</b> <code>public class PanelTablero extends JComponent {</code> declara la clase.</p>
<p class="l"><b>L22</b> En blanco.</p>
"""),
             ("public interface OyenteCasilla", r"""
<p class="l"><b>L23</b> Comentario: quien quiera enterarse de los clics implementa esta interfaz.</p>
<p class="l"><b>L24</b> <code>public interface OyenteCasilla {</code> una <b>interfaz</b> (capítulo 24) declarada
dentro de la clase; su nombre completo es <code>PanelTablero.OyenteCasilla</code>. Una interfaz es un contrato: «si
quieres que te avise, debes tener este método».</p>
<p class="l"><b>L25</b> <code>void casillaPulsada(int fila, int columna);</code> el único método del contrato. Sin
cuerpo: cada quien que implemente la interfaz decide qué hacer. Como tiene un solo método abstracto, se puede
implementar con una lambda o una referencia a método; la pantalla de juego hará
<code>tablero.setOyente(this::alPulsarCasilla)</code>.</p>
<p class="l"><b>L26–L27</b> Cierra la interfaz; línea en blanco.</p>
<div class="caja concepto"><b>El patrón observador</b> El tablero es el «observado»: algo ocurre en él (un clic). La
pantalla es el «observador»: quiere enterarse. En lugar de que el tablero conozca a la pantalla (y dependa de ella),
el tablero solo conoce el contrato <code>OyenteCasilla</code>. Es lo mismo que hace un <code>JButton</code> con
<code>ActionListener</code>: el botón no sabe qué hará tu programa, solo avisa. Ventaja práctica: en las
instrucciones y en la victoria nadie se registra como oyente, y el tablero funciona igual.</div>
"""),
             ("private static final int MARGEN", r"""
<p class="l"><b>L28</b> <code>MARGEN = 10</code>: el espacio para el halo del marco, como en la tarjeta. El comentario
al final de la línea (<code>//</code>) lo recuerda.</p>
<p class="l"><b>L29</b> <code>RELLENO = 8</code>: la distancia del borde del marco a la primera casilla. Así las
casillas no tocan el marco.</p>
<p class="l"><b>L30</b> En blanco.</p>
"""),
             ("private final char[][] fichas", r"""
<p class="l"><b>L31</b> <code>private final char[][] fichas = new char[3][3];</code> una matriz de 3 × 3 caracteres
(capítulo 15) con lo que hay que <b>dibujar</b> en cada casilla: <code>'X'</code>, <code>'O'</code> o vacío. No es el
tablero de verdad, es una <b>copia</b> para pintar. <code>final</code> se refiere a la variable: siempre apuntará a la
misma matriz, aunque su contenido cambie.</p>
<p class="l"><b>L32</b> <code>private int[] lineaGanadora;</code> si alguien ganó, cuatro números: fila y columna de
la primera casilla de la línea, y fila y columna de la última (como dice el comentario). Si nadie ganó, vale
<code>null</code>.</p>
<p class="l"><b>L33</b> <code>private OyenteCasilla oyente;</code> a quién avisar de los clics. Empieza en
<code>null</code>: nadie.</p>
<p class="l"><b>L34</b> <code>private boolean interactivo;</code> si el tablero acepta clics. Un <code>boolean</code>
sin asignar empieza en <code>false</code>: por defecto, el tablero solo muestra.</p>
"""),
             ("private char fichaFantasma", r"""
<p class="l"><b>L35</b> Comentario: la ficha que se ve transparente al pasar el ratón.</p>
<p class="l"><b>L36</b> <code>private char fichaFantasma = Tablero.VACIA;</code> qué ficha mostrar como vista previa
(la de quien tiene el turno). <code>VACIA</code> significa «ninguna».</p>
<p class="l"><b>L37–L38</b> <code>filaEncima</code> y <code>columnaEncima</code>: sobre qué casilla está el ratón.
<code>-1</code> significa «sobre ninguna»; se usa −1 porque no puede confundirse con una casilla real (0, 1 o 2).</p>
<p class="l"><b>L39</b> En blanco.</p>
"""),
             ("public PanelTablero(int tamCasilla)", r"""
<p class="l"><b>L40</b> Comentario Javadoc del parámetro: el lado de cada casilla en píxeles.</p>
<p class="l"><b>L41</b> El constructor recibe <b>un solo número</b>: el tamaño de casilla. Todo lo demás se deriva de
él.</p>
<p class="l"><b>L42</b> <code>int lado = 2 * (MARGEN + RELLENO) + 3 * tamCasilla;</code> el lado total: tres casillas
más, a cada lado, el margen y el relleno. Con casillas de 100: 2 × 18 + 300 = <b>336</b>. Con 66: 234. Con 46:
174.</p>
<p class="l"><b>L43</b> Fija ese tamaño (cuadrado) para que ningún layout lo deforme.</p>
<p class="l"><b>L44</b> Centrado horizontal en un <code>BoxLayout</code>.</p>
<p class="l"><b>L45</b> <code>for (char[] fila : fichas) {</code> un for-each (capítulo 14) que recorre las filas de la
matriz. Cada fila es a su vez un arreglo de 3 caracteres.</p>
<p class="l"><b>L46</b> <code>java.util.Arrays.fill(fila, Tablero.VACIA);</code> llena la fila con el carácter vacío.
Fíjate en que se escribe el nombre <b>completo</b> de la clase (<code>java.util.Arrays</code>) en lugar de importarla:
es válido y se usa cuando algo aparece una sola vez. ¿Por qué hace falta rellenar? Porque Java inicializa los
<code>char</code> con el carácter de código 0 (<code>'\u0000'</code>), no con un espacio. Sin este relleno, el panel
dibujaría bien (no hay X ni O), pero las comparaciones con <code>Tablero.VACIA</code> fallarían: antes de la primera
llamada a <code>mostrar</code>, ninguna casilla se resaltaría ni mostraría la manita.</p>
<p class="l"><b>L47–L48</b> Cierra el <code>for</code>; línea en blanco.</p>
"""),
             ("MouseAdapter raton", r"""
<p class="l"><b>L49</b> <code>MouseAdapter raton = new MouseAdapter() {</code> crea un oyente del ratón con una clase
anónima (como el <code>FocusAdapter</code> del capítulo 47) y lo guarda en la variable <code>raton</code>, porque hay
que registrarlo dos veces (líneas 68 y 69).</p>
<p class="l"><b>L50–L51</b> <code>mouseMoved</code>: Swing lo llama cada vez que el ratón se mueve sobre el componente
<b>sin</b> botones apretados. Puede llamarse decenas de veces por segundo.</p>
<p class="l"><b>L52</b> Le pasa la posición del puntero (en píxeles, relativos a la esquina del tablero) al método que
calcula sobre qué casilla está.</p>
<p class="l"><b>L53–L54</b> Cierre y línea en blanco.</p>
<p class="l"><b>L55–L56</b> <code>mouseExited</code>: el ratón salió del componente.</p>
<p class="l"><b>L57</b> Se pasa (−1, −1), una posición imposible, para decir «sobre ninguna casilla»: se apaga el
resaltado y desaparece la ficha fantasma. Sin esto, al sacar el ratón del tablero la última casilla quedaría
resaltada.</p>
<p class="l"><b>L58–L59</b> Cierre y línea en blanco.</p>
"""),
             ("public void mousePressed", r"""
<p class="l"><b>L60–L61</b> <code>mousePressed</code>: se apretó un botón del ratón. Se usa este y no
<code>mouseClicked</code> a propósito: «clic» en Swing exige apretar y soltar <b>sin moverse</b>; si la mano tiembla un
píxel, el clic no llega y el jugador cree que el juego no le hizo caso. Apretar responde siempre, y al instante.</p>
<p class="l"><b>L62</b> Antes de avisar, recalcula la casilla con la posición exacta del clic. Por si acaso: el ratón
pudo llegar ahí sin generar <code>mouseMoved</code> (por ejemplo, si la ventana acaba de aparecer bajo el puntero).</p>
<p class="l"><b>L63</b> <code>if (interactivo &amp;&amp; oyente != null &amp;&amp; filaEncima &gt;= 0) {</code> solo se
avisa si se cumplen las tres cosas: el tablero acepta clics, hay alguien escuchando y el clic cayó dentro de una
casilla. El <code>&amp;&amp;</code> se evalúa de izquierda a derecha y se detiene en el primer <code>false</code>.</p>
<p class="l"><b>L64</b> <code>oyente.casillaPulsada(filaEncima, columnaEncima);</code> el aviso. El tablero no sabe si
la casilla estaba libre, de quién es el turno ni si la partida terminó: eso lo decidirá el oyente.</p>
<p class="l"><b>L65–L66</b> Cierran el <code>if</code> y el método.</p>
<p class="l"><b>L67</b> <code>};</code> cierra la clase anónima y la instrucción que empezó en la línea 49.</p>
<p class="l"><b>L68</b> <code>addMouseListener(raton);</code> registra el oyente para los eventos de botones y de
entrar/salir (<code>mousePressed</code>, <code>mouseExited</code>).</p>
<p class="l"><b>L69</b> <code>addMouseMotionListener(raton);</code> lo registra <b>también</b> para el movimiento. Swing
separa los dos tipos de oyentes porque el movimiento genera muchísimos eventos y no todos los componentes los quieren.
Si olvidas esta línea, <code>mouseMoved</code> nunca se llama: no habría resaltado ni fantasma, aunque los clics sí
funcionarían.</p>
<p class="l"><b>L70–L71</b> Cierra el constructor; línea en blanco.</p>
"""),
             ("public void setOyente", r"""
<p class="l"><b>L72–L74</b> <code>setOyente</code> guarda a quién avisar. Solo hay un oyente a la vez (llamarlo otra vez
reemplaza al anterior); para este juego basta. Los componentes de Swing permiten varios con
<code>addXxxListener</code>, pero eso requiere una lista y aquí sería complicar sin necesidad.</p>
<p class="l"><b>L75</b> En blanco.</p>
"""),
             ("public void setInteractivo", r"""
<p class="l"><b>L76</b> <code>setInteractivo</code>: la pantalla de juego lo activa en el turno de una persona y lo
desactiva durante el turno de la IA y al terminar la partida.</p>
<p class="l"><b>L77</b> Guarda el valor.</p>
<p class="l"><b>L78</b> Actualiza el cursor: si el tablero deja de ser interactivo con el ratón encima, la manita debe
desaparecer en ese momento, no al mover el ratón.</p>
<p class="l"><b>L79</b> Repinta: el resaltado y el fantasma dependen de <code>interactivo</code>.</p>
<p class="l"><b>L80–L81</b> Cierre y línea en blanco.</p>
"""),
             ("public void setFichaFantasma", r"""
<p class="l"><b>L82–L84</b> <code>setFichaFantasma</code>: la pantalla de juego indica la ficha del jugador en turno
(<code>'X'</code> u <code>'O'</code>) y se repinta para que el fantasma cambie de inmediato.</p>
<p class="l"><b>L85–L86</b> Cierre y línea en blanco.</p>
"""),
             ("public void mostrar(Tablero tablero)", r"""
<p class="l"><b>L87</b> Comentario: copia el contenido del tablero para dibujarlo y busca la línea ganadora.</p>
<p class="l"><b>L88</b> <code>public void mostrar(Tablero tablero) {</code> la forma de decirle al panel «dibuja
esto». Recibe un <code>Tablero</code> de verdad (el de la lógica).</p>
<p class="l"><b>L89–L91</b> Dos <code>for</code> anidados recorren las 9 casillas y copian cada una con
<code>obtenerCasilla</code> (capítulo 29). ¿Por qué copiar en vez de guardar el tablero y leerlo al pintar? Porque así
el panel muestra exactamente lo que se le pidió, cuando se le pidió. La IA, por ejemplo, prueba jugadas en copias del
tablero; si el panel leyera un tablero que alguien está modificando, podría pintar un estado a medias.</p>
<p class="l"><b>L92–L93</b> Cierran los dos <code>for</code>.</p>
<p class="l"><b>L94</b> <code>lineaGanadora = Partida.buscarLineaGanadora(tablero);</code> (capítulo 38) devuelve
<code>{fila1, col1, fila2, col2}</code> de la primera y la última casilla de la línea ganadora, o <code>null</code>.
<code>Tablero.verificarGanador</code> solo dice <i>quién</i> ganó; para dibujar la raya hace falta saber
<i>dónde</i>.</p>
<p class="l"><b>L95</b> El cursor puede cambiar (la casilla bajo el ratón quizá ya no esté vacía).</p>
<p class="l"><b>L96</b> Repinta con el contenido nuevo.</p>
<p class="l"><b>L97–L98</b> Cierre y línea en blanco.</p>
"""),
             ("private double tamCasilla()", r"""
<p class="l"><b>L99–L100</b> <code>tamCasilla()</code> calcula el lado de una casilla a partir del ancho <b>real</b> del
componente: ancho menos márgenes y rellenos, dividido entre 3. En el tablero de 336: (336 − 36) ÷ 3 = 100. ¿Por qué
no guardar el <code>tamCasilla</code> del constructor? Porque así, si algún día un layout le diera otro tamaño, todo
seguiría encajando. Es una función de una línea, pero darle nombre hace que el resto se lea solo.</p>
<p class="l"><b>L101–L102</b> Cierre y línea en blanco.</p>
<p class="l"><b>L103–L104</b> <code>centroX(columna)</code>: la x del centro de una columna. Desde el inicio de las
casillas (<code>MARGEN + RELLENO</code> = 18) se avanzan <code>columna + 0.5</code> casillas: media casilla para la
columna 0, una y media para la 1, dos y media para la 2. Con casillas de 100: 68, 168 y 268.</p>
<p class="l"><b>L105–L106</b> Cierre y línea en blanco.</p>
<p class="l"><b>L107–L108</b> <code>centroY(fila)</code>: lo mismo en vertical. Como el tablero es cuadrado, da los
mismos números.</p>
<p class="l"><b>L109–L110</b> Cierre y línea en blanco.</p>
"""),
             ("private void actualizarCasillaEncima", r"""
<p class="l"><b>L111</b> El método que traduce una posición en píxeles a una casilla.</p>
<p class="l"><b>L112</b> El tamaño de casilla actual.</p>
<p class="l"><b>L113</b> <code>int columna = (int) Math.floor((x - MARGEN - RELLENO) / tam);</code> primero se resta el
inicio de las casillas (18), para medir desde la primera casilla y no desde el borde del componente. Luego se divide
entre el tamaño de casilla: el resultado dice «cuántas casillas completas hay a la izquierda». Por último,
<code>Math.floor</code> redondea <b>hacia abajo</b> y <code>(int)</code> lo convierte en entero. Con x = 150: (150 − 18)
÷ 100 = 1.32 → columna 1.</p>
<p class="l"><b>L114</b> Lo mismo con la y para la fila.</p>
<p class="l"><b>L115</b> <code>boolean dentro = x &gt;= 0 &amp;&amp; fila &gt;= 0 &amp;&amp; fila &lt; 3 &amp;&amp; columna
&gt;= 0 &amp;&amp; columna &lt; 3;</code> ¿cayó dentro de alguna casilla? Fila y columna deben estar entre 0 y 2. El
<code>x &gt;= 0</code> deja explícito que la señal (−1, −1) de <code>mouseExited</code> significa «fuera» (aunque la
cuenta ya daría −1, decirlo no cuesta nada y aclara la intención).</p>
<p class="l"><b>L116–L117</b> Si está dentro, la nueva casilla es la calculada; si no, −1 y −1. Operador ternario.</p>
<div class="caja cuidado"><b>¿Por qué <code>Math.floor</code> y no solo <code>(int)</code>?</b> Porque
<code>(int)</code> <b>corta</b> los decimales hacia el cero, y con números negativos eso redondea hacia arriba. Si el
ratón está en x = 10 (en el margen, a la izquierda de la primera casilla): (10 − 18) ÷ 100 = −0.08. <code>(int)
-0.08</code> da <b>0</b>: el programa creería que estás sobre la columna 0 y resaltaría una casilla que no estás
tocando. <code>Math.floor(-0.08)</code> da <b>−1.0</b>: fuera, como debe ser.</div>
"""),
             ("if (nuevaFila != filaEncima", r"""
<p class="l"><b>L118</b> <code>if (nuevaFila != filaEncima || nuevaColumna != columnaEncima) {</code> solo se hace algo
si el ratón <b>cambió de casilla</b>. Moverse dentro de la misma casilla genera decenas de eventos; repintar el tablero
entero en cada uno sería un desperdicio.</p>
<p class="l"><b>L119–L120</b> Guarda la nueva casilla.</p>
<p class="l"><b>L121</b> Pone la manita o la flecha según corresponda.</p>
<p class="l"><b>L122</b> Repinta para mover el resaltado y el fantasma.</p>
<p class="l"><b>L123–L125</b> Cierran el <code>if</code> y el método; línea en blanco.</p>
"""),
             ("private void actualizarCursor", r"""
<p class="l"><b>L126</b> Comentario: manita solo sobre casillas vacías y cuando se puede jugar.</p>
<p class="l"><b>L127</b> Declara el método.</p>
<p class="l"><b>L128–L129</b> <code>sePuedeJugar</code> es verdadero si el tablero es interactivo, el ratón está sobre
una casilla y esa casilla está vacía. El <b>orden</b> importa: si <code>filaEncima</code> es −1,
<code>fichas[-1][…]</code> lanzaría <code>ArrayIndexOutOfBoundsException</code>; pero como <code>&amp;&amp;</code> se
detiene en cuanto encuentra un <code>false</code>, a esa parte nunca se llega con −1. La expresión sigue en la línea
siguiente, que empieza con <code>&amp;&amp;</code> para que se vea que es continuación.</p>
<p class="l"><b>L130</b> Elige el cursor: manita (<code>HAND_CURSOR</code>) si se puede jugar, flecha normal
(<code>DEFAULT_CURSOR</code>) si no. Así el puntero le dice al jugador, antes de hacer clic, dónde puede jugar.</p>
<p class="l"><b>L131–L132</b> Cierre y línea en blanco.</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L133–L134</b> Sobrescribimos el dibujo. A partir de aquí se pinta por <b>capas</b>, de la de abajo a
la de arriba, igual que en un programa de dibujo: lo que se pinta después tapa a lo anterior.</p>
<p class="l"><b>L135</b> El pincel preparado.</p>
<p class="l"><b>L136</b> El tamaño de casilla, calculado una vez para todo el dibujo.</p>
<p class="l"><b>L137</b> <code>inicio</code>: donde empiezan las casillas (18).</p>
<p class="l"><b>L138</b> En blanco.</p>
"""),
             ("// Marco exterior", r"""
<p class="l"><b>L139</b> Capa 1, el marco exterior.</p>
<p class="l"><b>L140–L141</b> Un rectángulo redondeado desde (10, 10) del tamaño del componente menos los márgenes,
con arco 22.</p>
<p class="l"><b>L142–L143</b> Relleno con el fondo oscuro con alfa 150: el tablero se ve como un hueco más oscuro que
la pantalla, lo que hace resaltar las fichas de neón.</p>
<p class="l"><b>L144</b> Borde de neón morado, grosor 1.5, intensidad 0.8.</p>
<p class="l"><b>L145</b> En blanco.</p>
"""),
             ("// Casillas.", r"""
<p class="l"><b>L146</b> Capa 2, las nueve casillas.</p>
<p class="l"><b>L147–L148</b> Dos <code>for</code> anidados: filas y columnas.</p>
<p class="l"><b>L149–L150</b> Cada casilla es un rectángulo redondeado que empieza en <code>inicio + columna * tam +
4</code> (y lo mismo con la fila) y mide <code>tam - 8</code>: queda un hueco de 4 píxeles por cada lado, por donde
pasará la rejilla. Arco 14.</p>
"""),
             ("boolean resaltar", r"""
<p class="l"><b>L151–L152</b> <code>resaltar</code>: la casilla se ilumina si el tablero es interactivo, el ratón está
sobre <b>esta</b> casilla y está vacía. Sobre una casilla ocupada no se resalta, porque ahí no se puede jugar.</p>
<p class="l"><b>L153</b> Lavanda translúcida (alfa 40) si se resalta; si no, el color de casilla del tema.</p>
<p class="l"><b>L154</b> La rellena.</p>
<p class="l"><b>L155–L157</b> Cierran los dos <code>for</code>; línea en blanco.</p>
"""),
             ("// Rejilla", r"""
<p class="l"><b>L158</b> Capa 3, la rejilla: dos líneas verticales y dos horizontales.</p>
<p class="l"><b>L159</b> Lavanda con alfa 150.</p>
<p class="l"><b>L160</b> <code>for (int i = 1; i &lt; 3; i++)</code>: i vale 1 y 2, las dos divisiones interiores (0 y 3
serían los bordes, que ya tiene el marco).</p>
<p class="l"><b>L161</b> <code>p</code>: la posición de la división, <code>inicio + i * tam</code>. Con casillas de 100:
118 y 218.</p>
<p class="l"><b>L162</b> Línea vertical en x = p, desde y = MARGEN + 2 hasta el alto menos MARGEN + 2: atraviesa todo el
tablero y llega hasta el marco, como en el diseño. Neón tenue (intensidad 0.4).</p>
<p class="l"><b>L163</b> La horizontal equivalente, en y = p.</p>
<p class="l"><b>L164–L165</b> Cierra el <code>for</code>; línea en blanco.</p>
"""),
             ("// Fichas.", r"""
<p class="l"><b>L166</b> Capa 4, las fichas.</p>
<p class="l"><b>L167</b> <code>float grosor = (float) Math.max(3, tam * 0.085);</code> el grosor del trazo, proporcional
a la casilla (8.5 % de su lado) pero nunca menor que 3. Con 100: 8.5; con 66: 5.6; con 46: 3.9. Así la X del tablero
pequeño no se ve gorda ni la del grande se ve de alambre.</p>
<p class="l"><b>L168–L169</b> Recorre las nueve casillas.</p>
<p class="l"><b>L170</b> <code>Dibujo.dibujarFicha(...)</code> (capítulo 41) dibuja la ficha centrada en el centro de la
casilla, con un tamaño del 56 % de la casilla. Si el carácter no es <code>'X'</code> ni <code>'O'</code>, no dibuja
nada; por eso no hace falta preguntar si la casilla está vacía.</p>
<p class="l"><b>L171–L173</b> Cierran los <code>for</code>; línea en blanco.</p>
"""),
             ('// Ficha "fantasma"', r"""
<p class="l"><b>L174</b> Capa 5, la ficha fantasma: muestra dónde caería la jugada.</p>
<p class="l"><b>L175–L176</b> Se dibuja solo si se cumplen cuatro condiciones: tablero interactivo, ratón sobre una
casilla, casilla vacía y hay una ficha fantasma elegida. De nuevo, <code>filaEncima &gt;= 0</code> va antes que el
acceso a la matriz.</p>
<p class="l"><b>L177</b> <code>g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, 0.28f));</code> todo
lo siguiente se pintará al 28 % de opacidad (como el botón desactivado del capítulo 44).</p>
<p class="l"><b>L178</b> Dibuja la ficha del jugador en turno en la casilla bajo el ratón: igual que una real, pero
«fantasma».</p>
<p class="l"><b>L179</b> <code>g2.setComposite(AlphaComposite.SrcOver);</code> vuelve a la mezcla normal, opaca.
<code>SrcOver</code> es una constante ya preparada con opacidad 1. Sin esta línea, la raya ganadora que viene después
también saldría al 28 %.</p>
<p class="l"><b>L180–L181</b> Cierre y línea en blanco.</p>
"""),
             ("// Raya sobre", r"""
<p class="l"><b>L182</b> Capa 6, la raya sobre la línea ganadora, un poco más larga que las fichas.</p>
<p class="l"><b>L183</b> Solo si hay línea ganadora.</p>
<p class="l"><b>L184</b> <code>x1</code>: centro de la primera casilla, usando su columna (posición 1 del arreglo).</p>
<p class="l"><b>L185</b> <code>y1</code>: usando su fila (posición 0). Ojo al orden: el arreglo guarda <b>fila,
columna</b>, pero las coordenadas se escriben <b>x, y</b>; la x sale de la columna y la y de la fila.</p>
<p class="l"><b>L186–L187</b> Lo mismo para la última casilla (posiciones 3 y 2).</p>
"""),
             ("double largo = Math.hypot", r"""
<p class="l"><b>L188</b> <code>double largo = Math.hypot(x2 - x1, y2 - y1);</code> la longitud del segmento entre los
dos centros. <code>Math.hypot(a, b)</code> calcula √(a² + b²): el teorema de Pitágoras.</p>
<p class="l"><b>L189–L190</b> <code>dx</code> y <code>dy</code>: cuánto prolongar la raya por cada extremo. Primero se
<b>normaliza</b> la dirección: <code>(x2 - x1) / largo</code> y <code>(y2 - y1) / largo</code> forman un vector de
largo 1 que apunta de la primera ficha a la última. Después se multiplica por <code>tam * 0.38</code>, la distancia
que se quiere sobresalir (38 píxeles con casillas de 100). Así la raya sobresale <b>lo mismo</b> sea horizontal,
vertical o diagonal.</p>
<p class="l"><b>L191</b> El color de la raya es el de la ficha ganadora: se mira qué ficha hay en la primera casilla de
la línea y <code>Tema.colorDeFicha</code> da rosa para la X y azul para la O.</p>
<p class="l"><b>L192–L193</b> Traza la raya de <code>(x1 − dx, y1 − dy)</code> a <code>(x2 + dx, y2 + dy)</code>:
retrocede en el primer extremo y avanza en el segundo. Grosor del 6 % de la casilla (mínimo 3) e intensidad 1.4: brilla
más que nada en el tablero, porque es el momento culminante.</p>
<p class="l"><b>L194</b> Cierra el <code>if</code>.</p>
<p class="l"><b>L195</b> Libera el pincel.</p>
<p class="l"><b>L196–L197</b> Cierran el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>La geometría del tablero de la partida (casillas de 100)</h3>
<table class="tabla">
<tr><th>Elemento</th><th>Cuenta</th><th>Píxeles</th></tr>
<tr><td>Lado del componente</td><td>2 × (10 + 8) + 3 × 100</td><td>336 × 336</td></tr>
<tr><td>Marco</td><td>desde (10, 10), 336 − 20</td><td>316 × 316</td></tr>
<tr><td>Inicio de las casillas</td><td>10 + 8</td><td>18</td></tr>
<tr><td>Casilla (0, 0)</td><td>18 + 0 + 4, tamaño 100 − 8</td><td>92 × 92 en (22, 22)</td></tr>
<tr><td>Rejilla</td><td>18 + 100, 18 + 200; de 12 a 324</td><td>x = 118 y x = 218 (y lo mismo en y)</td></tr>
<tr><td>Centros</td><td>18 + 50, 18 + 150, 18 + 250</td><td>68, 168, 268</td></tr>
<tr><td>Fichas</td><td>100 × 0.56; grosor 100 × 0.085</td><td>56 píxeles, trazo de 8.5</td></tr>
</table>
<h3>Del puntero a la casilla</h3>
<table class="tabla">
<tr><th>Puntero (x, y)</th><th>(x − 18) ÷ 100</th><th>(y − 18) ÷ 100</th><th>Resultado</th></tr>
<tr><td>(150, 260)</td><td>1.32 → 1</td><td>2.42 → 2</td><td>fila 2, columna 1</td></tr>
<tr><td>(60, 60)</td><td>0.42 → 0</td><td>0.42 → 0</td><td>fila 0, columna 0</td></tr>
<tr><td>(317, 317)</td><td>2.99 → 2</td><td>2.99 → 2</td><td>fila 2, columna 2 (justo en el borde)</td></tr>
<tr><td>(320, 320)</td><td>3.02 → 3</td><td>3.02 → 3</td><td>fuera (3 no es una columna)</td></tr>
<tr><td>(10, 10)</td><td>−0.08 → −1</td><td>−0.08 → −1</td><td>fuera (con <code>(int)</code> solo, habría dado 0)</td></tr>
</table>
<h3>Un clic, de principio a fin</h3>
<ol>
<li>Es el turno de Ana (X). La pantalla de juego ha hecho <code>setInteractivo(true)</code> y
<code>setFichaFantasma('X')</code>.</li>
<li>Ana mueve el ratón hasta (150, 260). <code>mouseMoved</code> → <code>actualizarCasillaEncima(150, 260)</code> →
casilla (2, 1). Cambió, así que se pone la manita y se repinta: la casilla (2, 1) se aclara y aparece una X rosa al 28
%.</li>
<li>Ana aprieta. <code>mousePressed</code> recalcula (sigue siendo (2, 1)), comprueba las tres condiciones y llama a
<code>oyente.casillaPulsada(2, 1)</code>.</li>
<li>El oyente es la pantalla de juego (capítulo 59): le pide a <code>Partida</code> que juegue en (2, 1), y luego
llama a <code>tablero.mostrar(partida.getTablero())</code>, <code>setFichaFantasma('O')</code> y, si le toca a la IA,
<code>setInteractivo(false)</code>.</li>
<li><code>mostrar</code> copia las 9 casillas (ahora hay una X en (2, 1)), busca línea ganadora y repinta. La casilla
ya no se resalta ni muestra fantasma, porque está ocupada.</li>
</ol>
<h3>La raya ganadora, con y sin normalizar</h3>
<p>Diagonal de (0, 0) a (2, 2): centros (68, 68) y (268, 268). Largo = √(200² + 200²) = 282.8. Vector normalizado:
(200 ÷ 282.8, 200 ÷ 282.8) = (0.707, 0.707). Por 38: dx = dy = 26.9. La raya va de (41.1, 41.1) a (294.9, 294.9) y
sobresale √(26.9² + 26.9²) = <b>38</b> píxeles por cada punta.</p>
<p>Fila 0: centros (68, 68) y (268, 68). Largo 200; vector (1, 0); dx = 38, dy = 0. La raya va de (30, 68) a (306,
68): también sobresale <b>38</b>.</p>
<p>¿Y si no se normalizara (multiplicando directamente <code>x2 - x1</code> por 0.38)? En la fila, dx = 76: la raya
empezaría en x = −8, fuera del componente. En la diagonal, dx = dy = 76: sobresaldría 107 píxeles. Cada dirección
tendría una longitud distinta. Normalizar separa la <b>dirección</b> (el vector de largo 1) de la <b>distancia</b> (el
38).</p>

<h2>Compila y prueba</h2>
<p><i>Clean and Build</i> (Shift+F11) → <code>BUILD SUCCESS</code>. Se generan <code>PanelTablero.class</code>,
<code>PanelTablero$OyenteCasilla.class</code> (la interfaz interna) y <code>PanelTablero$1.class</code> (el
<code>MouseAdapter</code> anónimo).</p>
<p>La conversión de píxeles a casillas se puede comprobar sin ventana: creamos un tablero, le damos tamaño, lo hacemos
interactivo, le ponemos un oyente que imprime, y le «enviamos» clics falsos con <code>dispatchEvent</code>. Crea
<code>..\pruebas-totito\ProbarClics.java</code>:</p>
<pre class="java">import java.awt.event.MouseEvent;

public class ProbarClics {
    public static void main(String[] args) {
        PanelTablero panel = new PanelTablero(100);
        panel.setSize(336, 336);
        panel.setInteractivo(true);
        panel.setOyente((fila, columna) -&gt;
                System.out.println("Clic en fila " + fila + ", columna " + columna));
        int[][] puntos = {{150, 260}, {10, 10}, {317, 317}, {60, 60}};
        for (int[] p : puntos) {
            System.out.println("Pruebo x=" + p[0] + ", y=" + p[1]);
            panel.dispatchEvent(new MouseEvent(panel, MouseEvent.MOUSE_PRESSED,
                    0, 0, p[0], p[1], 1, false));
        }
    }
}</pre>
<p>La lambda <code>(fila, columna) -&gt; …</code> implementa <code>OyenteCasilla</code>: es el «observador» de esta
prueba. <code>new MouseEvent(...)</code> fabrica un evento de «apretar» con estos datos: el componente, el tipo de
evento, el instante (0), las teclas modificadoras (0: ninguna), la x, la y, el número de clics (1) y si abre un menú
contextual (<code>false</code>). <code>dispatchEvent</code> se lo entrega al panel como si viniera del ratón.</p>
<pre class="ps">java -cp target\classes ..\pruebas-totito\ProbarClics.java</pre>
<pre class="salida">Pruebo x=150, y=260
Clic en fila 2, columna 1
Pruebo x=10, y=10
Pruebo x=317, y=317
Clic en fila 2, columna 2
Pruebo x=60, y=60
Clic en fila 0, columna 0</pre>
<p>Fíjate en que (10, 10) no imprime nada: cayó en el margen y el panel, correctamente, no avisó.</p>
<p>Y para verlo, la foto opcional del capítulo 43 con un tablero ya jugado. Reemplaza las dos líneas de
<code>pieza</code> y del tamaño por:</p>
<pre class="java">        Tablero partida = new Tablero();
        partida.marcarCasilla(0, 0, 'X');
        partida.marcarCasilla(1, 1, 'X');
        partida.marcarCasilla(2, 2, 'X');
        partida.marcarCasilla(0, 1, 'O');
        partida.marcarCasilla(0, 2, 'O');
        PanelTablero tablero = new PanelTablero(100);
        tablero.mostrar(partida);
        JComponent pieza = tablero;
        int ancho = 336, alto = 336;</pre>
<p>Verás la rejilla, dos O azules arriba a la derecha y tres X rosas en diagonal atravesadas por una raya rosa que
sobresale un poco por cada punta.</p>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Síntoma o mensaje</th><th>Causa</th><th>Solución</th></tr>
<tr><td>Los clics funcionan, pero no hay resaltado ni fantasma</td><td>Falta <code>addMouseMotionListener</code></td><td>Línea
69</td></tr>
<tr><td>Al hacer clic en el margen se juega en la casilla de la esquina</td><td>Usaste <code>(int)</code> sin
<code>Math.floor</code></td><td>Líneas 113–114</td></tr>
<tr><td><code>ArrayIndexOutOfBoundsException: Index -1</code></td><td>Cambiaste el orden de las condiciones y se lee
<code>fichas[-1]</code></td><td><code>filaEncima &gt;= 0</code> debe ir antes</td></tr>
<tr><td>La raya ganadora sale tenue</td><td>Falta volver a <code>AlphaComposite.SrcOver</code></td><td>Línea 179</td></tr>
<tr><td>La raya va en la dirección equivocada (por ejemplo, vertical en vez de horizontal)</td><td>Confundiste fila y
columna al calcular x e y</td><td>La x sale de la columna (posiciones 1 y 3)</td></tr>
<tr><td><code>cannot find symbol: method buscarLineaGanadora</code></td><td>Falta en <code>Partida</code></td><td>Capítulo
38</td></tr>
</table>

<div class="caja git"><b>Git</b>
<pre class="ps">git status
git add src\PanelTablero.java
git commit -m "PanelTablero: tablero dibujado con clics"
git push</pre>
Con este commit terminas los componentes básicos. Si quieres ver el camino recorrido en la rama:
<code>git log --oneline main..interfaz-neon</code> muestra solo los commits de la interfaz neón, del más nuevo al más
antiguo.</div>

<h2>Resumen</h2>
<ul>
<li><code>PanelTablero</code> solo dibuja y traduce clics; las reglas viven en <code>Tablero</code> y
<code>Partida</code>, y la pantalla de juego une ambas partes.</li>
<li><code>OyenteCasilla</code> es un contrato de un solo método: el patrón observador, igual que
<code>ActionListener</code>; se implementa con una lambda o una referencia a método.</li>
<li>Un <code>MouseAdapter</code> anónimo atiende moverse, salir y apretar; se registra como oyente de ratón y de
movimiento.</li>
<li>De píxeles a casilla: restar el inicio, dividir entre el tamaño de casilla y redondear con
<code>Math.floor</code> (no basta con <code>(int)</code> para los negativos).</li>
<li>Toda la geometría sale del tamaño de casilla; por eso el mismo componente sirve con casillas de 100, 66 y 46.</li>
<li>Se pinta por capas: marco, casillas, rejilla, fichas, fantasma (con <code>AlphaComposite</code>, que luego se
restaura) y raya.</li>
<li>Normalizar un vector (dividir entre su largo) permite prolongar una línea la misma distancia en cualquier
dirección.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Cualquier juego de cuadrícula</b>: Conecta 4, Buscaminas, damas, ajedrez o batalla naval usan la misma cuenta de
píxel a casilla y el mismo panel que dibuja y avisa (capítulo 68).</li>
<li><b>Calendarios y horarios</b>: un clic en la cuadrícula de un mes se convierte en «semana 3, día 5» con la misma
división.</li>
<li><b>Observadores</b> en programas de gestión: una tabla de productos que avisa a un <code>OyenteSeleccion</code>
cuando eliges una fila, y la pantalla decide si muestra el detalle o lo edita.</li>
<li><b>Vectores normalizados</b>: flechas en un diagrama que deben terminar a la misma distancia del borde de cada
caja, o un personaje que se mueve a la misma velocidad en diagonal que en horizontal.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Calcula el lado del componente, la posición de la rejilla y los centros para el tablero de la pantalla de victoria
(casillas de 66). Pista: inicio 18, centros 18 + 33, 18 + 99, 18 + 165.</li>
<li>Con casillas de 66, ¿qué casilla corresponde al puntero (100, 200)? ¿Y a (15, 100)?</li>
<li>Agrega a <code>ProbarClics</code> el punto (320, 320) y, antes de los clics, <code>panel.setInteractivo(false)</code>
para otra vuelta. ¿Qué cambia en la salida y por qué?</li>
<li>Calcula la raya ganadora de la columna 1 (de (0, 1) a (2, 1)) con casillas de 100: sus dos extremos.</li>
<li>Reto: en una copia, cambia el oyente por una lista (<code>java.util.List&lt;OyenteCasilla&gt;</code>) con un método
<code>agregarOyente</code>, y avisa a todos en <code>mousePressed</code>. ¿Qué ventaja tendría y qué riesgo?</li>
</ol></div>
""",
}
