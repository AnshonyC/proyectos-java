# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 29,
    "titulo": "Tablero.java: el estado y las reglas del juego",
    "antes": r"""
<p class="entrada">Escribes la primera clase del juego: el tablero de 3×3. Guarda qué hay en cada casilla, rechaza las jugadas que no valen y sabe decir si alguien ganó o si hay empate. Todo lo demás (la IA, la terminal de pruebas y las ventanas) se apoya en ella, así que vale la pena entender cada línea.</p>

<h2>Por qué existe este archivo</h2>
<p>En el capítulo 28 decidimos que el <b>estado</b> del juego (qué hay en cada casilla) y sus <b>reglas</b> (qué jugada vale, quién ganó) vivirían en una sola clase que no sabe nada de ventanas ni de inteligencia artificial. Esa clase es <code>Tablero</code>. Hace el papel del árbitro con la hoja de anotaciones: no juega, no decide, no dibuja; solo anota y vigila.</p>
<p>Tenerlo separado resuelve tres problemas concretos del Totito:</p>
<ul>
<li><b>Una sola fuente de verdad.</b> Si la ventana y la IA guardaran cada una su propia copia de las casillas, tarde o temprano no coincidirían. Con <code>Tablero</code> hay un único lugar donde está «lo que de verdad pasó».</li>
<li><b>Las reglas se escriben una vez.</b> La ventana de este libro, la terminal de pruebas, la IA y la interfaz neón de la Parte VII preguntan «¿quién ganó?» al mismo método. Si algún día hubiera un error en esa regla, se corrige en un solo sitio.</li>
<li><b>Se prueba sin interfaz.</b> Como no necesita ventanas, lo puedes probar en segundos con <code>jshell</code>, como harás al final del capítulo.</li>
</ul>

<h2>Qué vas a aprender</h2>
<ul>
<li>A escribir una clase completa con un atributo privado, una constante pública, un constructor y seis métodos.</li>
<li>A usar una matriz <code>char[][]</code> para representar algo del mundo real (capítulo 15 en acción).</li>
<li>A validar datos antes de usarlos y a devolver <code>boolean</code> para avisar si algo salió bien.</li>
<li>A recorrer una matriz con dos <code>for</code> anidados y a salir antes de tiempo con <code>return</code>.</li>
<li>A combinar condiciones con <code>&amp;&amp;</code> y <code>||</code>, y por qué el orden de las condiciones importa (evaluación en cortocircuito).</li>
<li>A crear una <b>copia independiente</b> de un objeto, y por qué una simple asignación no copia nada.</li>
<li>A probar una clase con <code>jshell</code> sin escribir un programa aparte.</li>
</ul>

<h2>Créalo</h2>
<p>Abre el proyecto Totito en NetBeans (capítulo 5). Luego:</p>
<ol>
<li>En la ventana <i>Projects</i> despliega <i>Totito → Source Packages</i>.</li>
<li>Haz clic derecho en <i>&lt;default package&gt;</i> y elige <i>New → Java Class…</i></li>
<li>En <i>Class Name</i> escribe <code>Tablero</code> (con T mayúscula; Java distingue mayúsculas de minúsculas) y pulsa <i>Finish</i>.</li>
<li>NetBeans abre un archivo con una plantilla: un comentario de licencia, otro con <code>@author</code> y una clase vacía. Selecciona todo (<b>Ctrl+A</b>) y bórralo: vas a escribir el archivo completo tal como aparece abajo.</li>
<li>Guarda con <b>Ctrl+S</b>.</li>
</ol>
<p>Si prefieres la terminal, desde la carpeta del proyecto:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
New-Item src\Tablero.java</pre>
<p><code>New-Item</code> crea el archivo vacío dentro de <code>src</code>. Ábrelo con NetBeans (aparece solo en <i>&lt;default package&gt;</i>) o con el editor que uses, escribe el código y guárdalo con codificación UTF-8.</p>
<div class="caja consejo"><b>Escríbelo, no lo pegues</b> Teclear el código línea por línea parece lento, pero es la forma más rápida de aprenderlo: tus dedos notan dónde van los paréntesis, los puntos y comas y las llaves, y los errores que cometas al copiar te enseñarán a leer los mensajes del compilador. Mientras escribes, NetBeans te avisará con un subrayado rojo si algo no cuadra.</div>
<div class="caja concepto"><b>Por qué los comentarios del código no llevan tildes</b> Verás que los comentarios dicen «unicamente» o «deteccion». Es una costumbre prudente: un archivo con tildes guardado con una codificación distinta de la que espera el compilador produce errores como <code>unmappable character</code>. Sin tildes en el código, el archivo funciona igual en cualquier computadora. Los textos que el usuario <i>ve</i> en pantalla sí pueden llevarlas, siempre que el proyecto compile en UTF-8, como el nuestro (capítulo 5).</div>
<p>A continuación está el archivo completo, partido en bloques. Debajo de cada bloque se explica cada línea.</p>
""",
    "archivos": [
        {"ruta": "src/Tablero.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1–L6</b> Un <b>comentario de documentación</b> (Javadoc). Empieza con <code>/**</code>, termina con <code>*/</code>, y las líneas de en medio comienzan con <code>*</code> solo por estética. El compilador lo ignora por completo: está para las personas. Dice tres cosas: qué representa la clase (el tablero de 3×3), de qué se encarga (estado, validaciones, victoria y empate) y, muy importante, de qué <b>no</b> se encarga (interfaz e IA). Esa última frase es una promesa de diseño: si algún día alguien quisiera meter aquí un color o un botón, el comentario le recuerda que ese no es su lugar. Al estar justo encima de la clase, NetBeans lo muestra como ayuda cuando pasas el ratón sobre la palabra <code>Tablero</code> en otro archivo.</p>
<p class="l"><b>L7</b> Declara la clase. <code>public</code> significa que cualquier otra clase del proyecto puede usarla (la IA y las ventanas lo necesitan). <code>class</code> anuncia que lo que sigue es un molde para crear objetos (capítulo 18). <code>Tablero</code> es su nombre, que <b>tiene</b> que coincidir con el del archivo <code>Tablero.java</code>; si no, el compilador responde <code>class Tablero is public, should be declared in a file named…</code>. La llave <code>{</code> abre el cuerpo de la clase, que se cierra en la línea 92: todo lo que hay entre ambas llaves pertenece al tablero.</p>
<p class="l"><b>L8</b> Línea en blanco: no hace nada, solo separa visualmente. Las usaremos para agrupar ideas, como los párrafos de un texto.</p>
"""),
             ("public static final char VACIA", r"""
<p class="l"><b>L9</b> Una <b>constante</b>: un valor con nombre que nunca cambia. Palabra por palabra:</p>
<ul>
<li><code>public</code>: se puede leer desde fuera. La IA y las ventanas escribirán <code>Tablero.VACIA</code> para preguntar si una casilla está libre.</li>
<li><code>static</code>: pertenece a la <b>clase</b>, no a cada objeto. Hay un solo <code>VACIA</code> para todos los tableros que existan, y se usa con el nombre de la clase (<code>Tablero.VACIA</code>) sin necesidad de crear un tablero (capítulo 20).</li>
<li><code>final</code>: una vez asignado, no se puede cambiar. Si alguien escribiera <code>Tablero.VACIA = '-';</code> el compilador lo rechazaría con <code>cannot assign a value to final variable VACIA</code>.</li>
<li><code>char</code>: el tipo, un solo carácter (capítulo 12).</li>
<li><code>VACIA</code>: el nombre. Las constantes se escriben en MAYÚSCULAS por convención, para reconocerlas de un vistazo.</li>
<li><code>= ' '</code>: el valor, un espacio en blanco entre <b>comillas simples</b>. En Java las comillas simples encierran un <code>char</code> y las dobles un <code>String</code>; <code>" "</code> sería un texto, no un carácter, y no se podría guardar en un <code>char</code>.</li>
<li><code>;</code>: el punto y coma termina la instrucción, como el punto final de una oración.</li>
</ul>
<p class="l">¿Por qué un espacio y no otra cosa? Porque al imprimir el tablero en la terminal (capítulo 32) una casilla vacía se verá vacía, sin código extra. ¿Y por qué darle nombre en vez de escribir <code>' '</code> en todas partes? Porque <code>casillas[1][1] == VACIA</code> se lee como una frase («¿la casilla está vacía?»), mientras que <code>casillas[1][1] == ' '</code> obliga a adivinar qué significa ese espacio. Es la regla de «nada de números (ni caracteres) mágicos» del capítulo 27. Y si un día quisieras usar <code>'-'</code> como vacía, cambiarías una sola línea.</p>
"""),
             ("private char[][] casillas", r"""
<p class="l"><b>L11</b> El <b>atributo</b> que guarda el estado del juego: las 9 casillas. <code>private</code> significa que solo el código de esta clase puede tocarlo; ninguna otra clase puede escribir <code>tablero.casillas[1][1] = 'X'</code> y saltarse las reglas (por ejemplo, poner una ficha en una casilla ocupada). Esa protección es el <b>encapsulamiento</b> del capítulo 19: los demás solo pueden cambiar el tablero a través de <code>marcarCasilla</code>, que comprueba todo antes. <code>char[][]</code> es el tipo: una matriz (un arreglo de arreglos) de caracteres; los dos pares de corchetes indican dos dimensiones, filas y columnas. <code>casillas</code> es el nombre.</p>
<p class="l">Fíjate en que esta línea <b>declara</b> la variable pero no crea la matriz: de momento <code>casillas</code> vale <code>null</code> (no apunta a nada). La matriz se crea en el constructor. Tampoco lleva <code>static</code>: cada tablero tiene sus propias casillas, y eso será esencial para la IA, que crea muchas copias del tablero para imaginar jugadas sin tocar el verdadero.</p>
"""),
             ("public Tablero()", r"""
<p class="l"><b>L13</b> El <b>constructor</b>: el código que se ejecuta automáticamente cada vez que alguien escribe <code>new Tablero()</code>. Se reconoce porque se llama igual que la clase y no tiene tipo de retorno (ni siquiera <code>void</code>). Es <code>public</code> para que otras clases puedan crear tableros. Los paréntesis vacíos indican que no recibe parámetros: todo tablero nuevo empieza igual. Su trabajo es dejar el objeto listo para usarse (capítulo 20).</p>
<p class="l"><b>L14</b> Crea la matriz de 3 filas por 3 columnas y la guarda en el atributo. <code>new char[3][3]</code> pide a Java memoria para 9 caracteres. Java llena cada <code>char</code> nuevo con el carácter de código 0 (<code>'\u0000'</code>), que no es un espacio, sino un carácter invisible «nulo». Por eso no basta con esta línea: si la dejáramos así, las casillas no serían iguales a <code>VACIA</code> y el juego pensaría que están ocupadas.</p>
<p class="l"><b>L15</b> Llama al método <code>reiniciar()</code> de este mismo objeto, que pone <code>VACIA</code> en las 9 casillas. Podríamos haber copiado aquí los dos <code>for</code> de <code>reiniciar</code>, pero entonces habría dos copias del mismo código; si un día cambiara la forma de vaciar el tablero, habría que acordarse de cambiar ambas. Llamar al método evita esa repetición (el principio «no te repitas»). Sin esta línea, un tablero recién creado tendría casillas con <code>'\u0000'</code>: <code>marcarCasilla</code> las vería ocupadas y nadie podría jugar.</p>
<p class="l"><b>L16</b> Cierra el constructor.</p>
"""),
             ("public void reiniciar()", r"""
<p class="l"><b>L18</b> Javadoc de una sola línea para el método que sigue: dice qué hace y para qué («listo para una nueva partida»).</p>
<p class="l"><b>L19</b> Declara el método <code>reiniciar</code>. <code>public</code>: lo usarán el constructor y también los botones de «Nueva partida» de las ventanas. <code>void</code> significa que no devuelve ningún valor: hace su trabajo (vaciar) y termina. Los paréntesis vacíos: no necesita datos de fuera.</p>
<p class="l"><b>L20</b> Un ciclo <code>for</code> (capítulo 14) que recorre las filas. <code>int fila = 0</code> crea un contador que empieza en 0; <code>fila &lt; 3</code> es la condición para seguir (0, 1 y 2 sí; 3 ya no); <code>fila++</code> suma 1 al terminar cada vuelta. Usamos el nombre <code>fila</code> y no <code>i</code> para que el código se lea solo.</p>
<p class="l"><b>L21</b> Un segundo <code>for</code>, <b>dentro</b> del primero, para las columnas. Por cada fila, recorre las columnas 0, 1 y 2. En total el cuerpo se ejecuta 3 × 3 = 9 veces, una por casilla, en este orden: [0][0], [0][1], [0][2], [1][0]… [2][2]. Es el patrón de dos ciclos anidados que usarás en casi todos los métodos de este archivo.</p>
<p class="l"><b>L22</b> La única instrucción real: pone <code>VACIA</code> en la casilla de esa fila y esa columna. El <code>=</code> asigna (guarda) un valor; no compara.</p>
<p class="l"><b>L23–L25</b> Cierran, en orden, el <code>for</code> de columnas, el <code>for</code> de filas y el método. Cada <code>{</code> tiene su <code>}</code>; la sangría (los espacios a la izquierda) ayuda a ver qué llave cierra qué. Si falta una, el compilador dice <code>reached end of file while parsing</code>.</p>
"""),
             ("public boolean marcarCasilla", r"""
<p class="l"><b>L27–L31</b> Javadoc del método más usado del juego. Dice que <i>intenta</i> colocar una ficha (puede no lograrlo), cuándo devuelve <code>false</code> y por qué existe esa comprobación: para evitar tiros duplicados (dos fichas en la misma casilla) o inválidos (fuera del tablero).</p>
<p class="l"><b>L32</b> La firma del método. <code>public</code>: lo llaman la ventana, la terminal y la IA. <code>boolean</code>: devuelve <code>true</code> o <code>false</code>, es decir, responde «¿se pudo?». Recibe tres <b>parámetros</b> (capítulo 16), separados por comas, cada uno con su tipo: <code>int fila</code>, <code>int columna</code> y <code>char ficha</code> (la letra que se va a poner, <code>'X'</code> u <code>'O'</code>). El tablero no decide qué ficha poner: se la dicen. Por eso no sabe quién juega, tal como planeamos.</p>
<p class="l"><b>L33</b> Primera validación: ¿la posición existe? <code>||</code> significa «o»: la condición es verdadera si <b>cualquiera</b> de las cuatro partes lo es. Se lee: «si la fila es menor que 0, o mayor que 2, o la columna es menor que 0, o mayor que 2». Una fila 3 o una columna −1 no existen en un tablero de 3×3.</p>
<p class="l"><b>L34</b> <code>return false;</code> termina el método en ese mismo instante y entrega <code>false</code> a quien lo llamó. Lo que hay debajo ya no se ejecuta. ¿Qué pasaría sin esta validación? La línea 36 intentaría leer <code>casillas[5][0]</code> y Java detendría el programa con una excepción <code>ArrayIndexOutOfBoundsException</code> («índice fuera de los límites»). Con ella, un dato equivocado (por ejemplo, alguien que escribe «5 5» en la terminal) produce un simple «no se pudo» en vez de un programa caído.</p>
<p class="l"><b>L35</b> Cierra el <code>if</code>.</p>
"""),
             ("if (casillas[fila][columna] != VACIA)", r"""
<p class="l"><b>L36</b> Segunda validación: ¿la casilla está libre? <code>!=</code> significa «distinto de». Si lo que hay en la casilla no es <code>VACIA</code>, alguien ya jugó ahí. Comparar dos <code>char</code> con <code>==</code> o <code>!=</code> es correcto, porque son valores simples (con un <code>String</code> habría que usar <code>equals</code>, capítulo 17). Esta comprobación va <b>después</b> de la de L33 a propósito: solo es seguro leer <code>casillas[fila][columna]</code> cuando ya sabemos que la posición existe.</p>
<p class="l"><b>L37</b> Si está ocupada, se niega y termina sin tocar nada. Esto implementa la regla «no se puede marcar una casilla ocupada» del capítulo 28. Sin esta línea, un clic sobre una X la convertiría en O.</p>
<p class="l"><b>L38</b> Cierra el <code>if</code>.</p>
<p class="l"><b>L39</b> Si el programa llegó hasta aquí, las dos validaciones pasaron: la posición existe y está libre. Ahora sí, guarda la ficha en la casilla. Es la <b>única</b> línea de todo el proyecto que pone fichas en el tablero, y está protegida por las anteriores.</p>
<p class="l"><b>L40</b> Devuelve <code>true</code>: «listo, se colocó». Quien llamó usa esta respuesta para decidir qué hacer: la ventana, por ejemplo, solo cambia de turno si la jugada se aceptó.</p>
<p class="l"><b>L41</b> Cierra el método. Este patrón (validar primero y salir con <code>return</code> si algo está mal, y dejar el trabajo real al final) se llama <b>cláusula de guarda</b>. Evita anidar un <code>if</code> dentro de otro y deja el «camino feliz» en las últimas líneas, fácil de encontrar.</p>
"""),
             ("public char obtenerCasilla", r"""
<p class="l"><b>L43</b> Un método de consulta: devuelve un <code>char</code>, lo que hay en una casilla. Como <code>casillas</code> es privado, esta es la forma permitida de que los demás <i>lean</i> el tablero sin poder <i>escribir</i> en él. Es como el escaparate de una tienda: se puede mirar, no tocar.</p>
<p class="l"><b>L44</b> <code>return</code> entrega el contenido de esa casilla: <code>'X'</code>, <code>'O'</code> o <code>' '</code>. A diferencia de <code>marcarCasilla</code>, no valida la posición: quien lo llama siempre recorre filas y columnas de 0 a 2, así que nunca se sale. Si alguien pidiera <code>obtenerCasilla(3, 3)</code>, Java lanzaría <code>ArrayIndexOutOfBoundsException</code>, y está bien que así sea: sería un error de programación que conviene ver de inmediato, no un dato del usuario.</p>
<p class="l"><b>L45</b> Cierra el método.</p>
"""),
             ("public boolean tableroLleno", r"""
<p class="l"><b>L47</b> Javadoc: devuelve <code>true</code> si no quedan casillas vacías. Así se detecta el empate (junto con «nadie ganó»).</p>
<p class="l"><b>L48</b> Firma: <code>public</code>, devuelve <code>boolean</code>, sin parámetros. El nombre es una pregunta que se responde con sí o no, como conviene a un método <code>boolean</code>: <code>if (tablero.tableroLleno())</code> se lee «si el tablero está lleno».</p>
<p class="l"><b>L49–L50</b> Los mismos dos <code>for</code> anidados de <code>reiniciar</code>: recorren las 9 casillas.</p>
<p class="l"><b>L51</b> <code>==</code> compara (no asigna): «¿esta casilla es igual a <code>VACIA</code>?».</p>
<p class="l"><b>L52</b> Basta con encontrar <b>una</b> casilla vacía para saber que el tablero no está lleno, así que el método responde <code>false</code> y termina en ese momento, aunque los ciclos no hayan acabado. <code>return</code> no solo sale del <code>if</code> ni del <code>for</code>: sale de todo el método. En un tablero vacío, el método responde en la primera vuelta, sin mirar las otras 8 casillas.</p>
<p class="l"><b>L53–L55</b> Cierran el <code>if</code> y los dos <code>for</code>.</p>
<p class="l"><b>L56</b> Si los dos ciclos terminaron sin encontrar ninguna casilla vacía (es decir, el <code>return false</code> nunca se ejecutó), el tablero está lleno: devuelve <code>true</code>. Esta línea es obligatoria: un método que promete devolver <code>boolean</code> tiene que devolver algo por <b>todos</b> los caminos. Sin ella, el compilador diría <code>missing return statement</code>.</p>
<p class="l"><b>L57</b> Cierra el método.</p>
"""),
             ("public char verificarGanador", r"""
<p class="l"><b>L59–L62</b> Javadoc: el método revisa las 8 líneas (3 filas, 3 columnas, 2 diagonales) y devuelve la ficha ganadora o <code>VACIA</code> si nadie ha ganado.</p>
<p class="l"><b>L63</b> Firma: devuelve un <code>char</code>. Fíjate en la decisión de diseño: en vez de devolver <code>boolean</code> («¿hay ganador?»), devuelve <b>quién</b> ganó. Así una sola llamada responde dos preguntas: si el resultado es <code>VACIA</code>, nadie; si es <code>'X'</code> u <code>'O'</code>, ese. El tablero sigue sin saber quién es la persona y quién la IA: solo devuelve una letra.</p>
<p class="l"><b>L64</b> Un solo <code>for</code> con un contador <code>i</code> que vale 0, 1 y 2. Aquí <code>i</code> hace doble trabajo: en L65 es el número de <b>fila</b> que se revisa y en L68 el número de <b>columna</b>. Es el patrón que vimos en el capítulo 28: en la fila <i>i</i> el primer índice queda fijo; en la columna <i>i</i>, el segundo.</p>
<p class="l"><b>L65</b> Revisa la fila <code>i</code>. Tiene tres condiciones unidas con <code>&amp;&amp;</code> («y»): las tres deben cumplirse.</p>
<ul>
<li><code>casillas[i][0] != VACIA</code>: la primera casilla de la fila no está vacía. Es la protección del capítulo 28: sin ella, una fila de tres espacios cumpliría las otras dos condiciones y el método declararía ganador a <code>' '</code>.</li>
<li><code>casillas[i][0] == casillas[i][1]</code>: la primera es igual a la del medio.</li>
<li><code>casillas[i][1] == casillas[i][2]</code>: la del medio es igual a la última. Si la primera es igual a la segunda y la segunda a la tercera, las tres son iguales; por eso no hace falta comparar la primera con la tercera.</li>
</ul>
<p class="l">Java evalúa <code>&amp;&amp;</code> de izquierda a derecha y en <b>cortocircuito</b>: si la primera parte es falsa, ni siquiera mira las demás, porque el resultado ya no puede ser verdadero. Con una fila vacía, la comparación se detiene en la primera condición. Es más rápido y, en otros programas, evita errores (por ejemplo, <code>texto != null &amp;&amp; texto.isEmpty()</code> no falla nunca gracias a ese orden).</p>
<p class="l"><b>L66</b> Si las tres casillas son iguales y no vacías, devuelve la ficha de cualquiera de ellas (la primera): esa es la ganadora. El método termina aquí; las demás líneas no se revisan.</p>
<p class="l"><b>L67</b> Cierra el <code>if</code> de la fila (el ciclo sigue abierto).</p>
"""),
             ("if (casillas[0][i] != VACIA", r"""
<p class="l"><b>L68</b> En la misma vuelta del ciclo revisa la <b>columna</b> <code>i</code>. Ahora el índice que cambia es el primero (fila 0, 1, 2) y el que queda fijo es el segundo (<code>i</code>). Por lo demás es idéntica a L65: no vacía, primera igual a la del medio, la del medio igual a la última. Así, con 3 vueltas se revisan 3 filas y 3 columnas: 6 de las 8 líneas.</p>
<p class="l"><b>L69</b> Si la columna es ganadora, devuelve su ficha.</p>
<p class="l"><b>L70–L71</b> Cierran el <code>if</code> de la columna y el <code>for</code>. Al llegar aquí sabemos que ninguna fila ni columna tiene tres en línea.</p>
"""),
             ("if (casillas[0][0] != VACIA", r"""
<p class="l"><b>L72</b> La diagonal principal: [0][0], [1][1] y [2][2], de la esquina de arriba a la izquierda a la de abajo a la derecha. En ella fila y columna son iguales, pero como es una sola línea se escribe directamente, sin ciclo. Mismo esquema de tres condiciones.</p>
<p class="l"><b>L73</b> Devuelve la ficha de la esquina, que es la ganadora.</p>
<p class="l"><b>L74</b> Cierra el <code>if</code>.</p>
"""),
             ("if (casillas[0][2] != VACIA", r"""
<p class="l"><b>L75</b> La diagonal secundaria: [0][2], [1][1] y [2][0], de la esquina de arriba a la derecha a la de abajo a la izquierda. Aquí fila + columna siempre suma 2. Las dos diagonales comparten el centro [1][1]; por eso el centro es la casilla más valiosa del totito: participa en 4 líneas (su fila, su columna y las dos diagonales), más que cualquier otra.</p>
<p class="l"><b>L76</b> Devuelve la ficha de esa esquina.</p>
<p class="l"><b>L77</b> Cierra el <code>if</code>.</p>
<p class="l"><b>L78</b> Si el método llega hasta aquí, ninguna de las 8 líneas está completa: devuelve <code>VACIA</code>, que en este contexto significa «nadie ha ganado». Igual que en <code>tableroLleno</code>, sin este <code>return</code> final el compilador protestaría con <code>missing return statement</code>.</p>
<p class="l"><b>L79</b> Cierra el método.</p>
"""),
             ("public Tablero obtenerCopia", r"""
<p class="l"><b>L81–L82</b> Javadoc: el método crea una copia <b>independiente</b>, pensada para que la IA (capítulo 31) pueda «imaginar» jugadas sin tocar la partida real.</p>
<p class="l"><b>L83</b> Firma: devuelve un <code>Tablero</code>. Un método puede devolver cualquier tipo, también objetos de su propia clase.</p>
<p class="l"><b>L84</b> Crea un tablero nuevo con <code>new Tablero()</code>. Esto ejecuta el constructor (L13): la copia nace con su <b>propia</b> matriz de 3×3, vacía, en otro lugar de la memoria.</p>
<p class="l"><b>L85–L86</b> Los dos <code>for</code> de siempre, para recorrer las 9 casillas.</p>
<p class="l"><b>L87</b> Copia el contenido de cada casilla del tablero original a la casilla equivalente de la copia. Dos detalles:</p>
<ul>
<li><code>this</code> significa «este objeto», el tablero sobre el que se llamó el método (capítulo 20). <code>this.casillas</code> son las casillas del original; aquí se podría omitir <code>this.</code>, pero escribirlo deja clarísimo cuál es cuál frente a <code>copia.casillas</code>.</li>
<li><code>copia.casillas</code> accede al atributo <b>privado</b> de otro objeto. Es legal porque <code>private</code> protege a nivel de <b>clase</b>, no de objeto: el código de <code>Tablero</code> puede ver las casillas de cualquier <code>Tablero</code>. Fuera de esta clase, esa línea no compilaría.</li>
</ul>
<p class="l"><b>L88–L89</b> Cierran los dos <code>for</code>.</p>
<p class="l"><b>L90</b> Devuelve la copia terminada: otro tablero con las mismas fichas, pero con su propia matriz.</p>
<p class="l"><b>L91–L92</b> Cierran el método y, con la última llave, la clase entera (la que se abrió en L7).</p>
<div class="caja cuidado"><b>¿Por qué no basta con <code>Tablero copia = this;</code>?</b> Porque las variables de objetos guardan <b>referencias</b> (direcciones), no el objeto (capítulo 18). <code>Tablero copia = this;</code> crearía un segundo nombre para el <i>mismo</i> tablero, como dos llaves de la misma casa: lo que la IA «imaginara» en la copia aparecería en la partida real. Por la misma razón tampoco serviría copiar la matriz con <code>copia.casillas = this.casillas;</code>: las dos variables apuntarían a la misma matriz. Hay que crear objetos nuevos y copiar los valores uno por uno, que es exactamente lo que hacen L84 a L89.</div>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<p>Sigamos con lápiz y papel lo que hace el tablero en una partida concreta. A esto se le llama hacer una <b>traza</b>: ejecutar el código «a mano», anotando el valor de cada variable.</p>
<h3>Traza 1: marcar casillas</h3>
<table class="tabla">
<tr><th>Llamada</th><th>¿L33 (fuera de rango)?</th><th>¿L36 (ocupada)?</th><th>Resultado</th></tr>
<tr><td><code>new Tablero()</code></td><td colspan="2">L14 crea la matriz; L15 pone <code>' '</code> en las 9 casillas</td><td>tablero vacío</td></tr>
<tr><td><code>marcarCasilla(1, 1, 'X')</code></td><td>no (1 está entre 0 y 2)</td><td>no (hay <code>' '</code>)</td><td><code>true</code>; el centro ahora tiene X</td></tr>
<tr><td><code>marcarCasilla(1, 1, 'O')</code></td><td>no</td><td><b>sí</b> (hay <code>'X'</code>)</td><td><code>false</code> en L37; nada cambia</td></tr>
<tr><td><code>marcarCasilla(3, 0, 'O')</code></td><td><b>sí</b> (<code>fila &gt; 2</code>)</td><td>no se llega a mirar</td><td><code>false</code> en L34; nada cambia</td></tr>
</table>
<h3>Traza 2: verificarGanador con un tablero dado</h3>
<p>Supón este tablero (la O hizo columna en el centro):</p>
<pre class="salida"> X | O | X
---+---+---
   | O | X
---+---+---
   | O |  </pre>
<p>Así recorre el método las líneas, en orden:</p>
<table class="tabla">
<tr><th>Paso</th><th>Línea revisada</th><th>Casillas</th><th>Qué pasa</th></tr>
<tr><td><code>i = 0</code>, L65</td><td>fila 0</td><td>X, O, X</td><td>No vacía, pero <code>'X' == 'O'</code> es falso: el <code>&amp;&amp;</code> se corta ahí</td></tr>
<tr><td><code>i = 0</code>, L68</td><td>columna 0</td><td>X, ␣, ␣</td><td>No vacía, pero <code>'X' == ' '</code> es falso</td></tr>
<tr><td><code>i = 1</code>, L65</td><td>fila 1</td><td>␣, O, X</td><td>La primera casilla <b>es</b> <code>VACIA</code>: se corta en la primera condición</td></tr>
<tr><td><code>i = 1</code>, L68</td><td>columna 1</td><td>O, O, O</td><td>No vacía, O == O, O == O: <b>las tres se cumplen</b>; L69 devuelve <code>'O'</code></td></tr>
</table>
<p>El método termina en la cuarta comprobación: ni siquiera llega a la columna 2 (que tiene X, X, ␣) ni a las diagonales. Con un tablero vacío, en cambio, recorre las 8 líneas, todas se cortan en la primera condición, y L78 devuelve <code>' '</code>.</p>
<h3>Traza 3: la copia es independiente</h3>
<p>Con el tablero anterior en la variable <code>t</code>:</p>
<ol>
<li><code>Tablero c = t.obtenerCopia();</code> crea un tablero nuevo y copia las 9 casillas. Ahora hay <b>dos</b> objetos en memoria, con las mismas letras.</li>
<li><code>c.marcarCasilla(2, 2, 'X')</code> devuelve <code>true</code> y pone X en la esquina de <code>c</code>.</li>
<li><code>c.obtenerCasilla(2, 2)</code> devuelve <code>'X'</code>, pero <code>t.obtenerCasilla(2, 2)</code> sigue devolviendo <code>' '</code>: el original no se enteró.</li>
</ol>
<p>Eso es justo lo que necesitará la IA: probar jugadas en copias y dejar intacta la partida.</p>

<h2>Compila y prueba</h2>
<p>Primero compila: <i>Run → Clean and Build Project</i> (<b>Shift+F11</b>). En la ventana <i>Output</i> de NetBeans deberías ver, al final, <code>BUILD SUCCESS</code>. El archivo compilado queda en <code>target\classes\Tablero.class</code>. Como el proyecto todavía no tiene un programa con <code>main</code> para esta versión, no pulses <i>Run</i>: probaremos la clase con <code>jshell</code>, la consola interactiva de Java del capítulo 11.</p>
<p>Abre PowerShell y escribe:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
jshell</pre>
<p>Dentro de <code>jshell</code>, el comando <code>/open</code> lee un archivo de código y lo carga como si lo hubieras escrito a mano. Escribe estas líneas una por una (usa la barra normal <code>/</code> en la ruta; Java la entiende también en Windows):</p>
<pre class="salida">jshell&gt; /open src/Tablero.java

jshell&gt; Tablero t = new Tablero();
t ==&gt; Tablero@6574b225

jshell&gt; t.marcarCasilla(1, 1, 'X')
$3 ==&gt; true

jshell&gt; t.marcarCasilla(1, 1, 'O')
$4 ==&gt; false

jshell&gt; t.marcarCasilla(3, 0, 'O')
$5 ==&gt; false

jshell&gt; t.marcarCasilla(0, 0, 'O')
$6 ==&gt; true

jshell&gt; t.marcarCasilla(0, 2, 'X')
$7 ==&gt; true

jshell&gt; t.marcarCasilla(2, 0, 'X')
$8 ==&gt; true

jshell&gt; t.verificarGanador()
$9 ==&gt; 'X'

jshell&gt; t.tableroLleno()
$10 ==&gt; false

jshell&gt; Tablero c = t.obtenerCopia();
c ==&gt; Tablero@6a2bcfcb

jshell&gt; c.reiniciar();

jshell&gt; c.obtenerCasilla(1, 1)
$13 ==&gt; ' '

jshell&gt; t.obtenerCasilla(1, 1)
$14 ==&gt; 'X'

jshell&gt; t.obtenerCasilla(3, 3)
|  Exception java.lang.ArrayIndexOutOfBoundsException: Index 3 out of bounds for length 3
|        at Tablero.obtenerCasilla (#1:38)
|        at (#15:1)

jshell&gt; /exit
|  Goodbye</pre>
<p>Esta sesión se ejecutó de verdad. Qué comprobaste en cada paso:</p>
<ul>
<li><code>Tablero@6574b225</code> es la forma en que Java muestra un objeto que no sabe describirse: el nombre de la clase, una arroba y un número que identifica al objeto. En tu computadora el número será otro, y está bien.</li>
<li>Los <code>$3</code>, <code>$4</code>… son variables temporales que <code>jshell</code> crea para guardar cada resultado.</li>
<li>Se rechazó la casilla ocupada (<code>$4</code>) y la casilla fuera del tablero (<code>$5</code>) sin que nada fallara.</li>
<li>Las X en [0][2], [1][1] y [2][0] forman la diagonal secundaria: <code>verificarGanador()</code> devolvió <code>'X'</code>.</li>
<li>Vaciar la copia <code>c</code> no tocó el original <code>t</code>: la copia es independiente.</li>
<li><code>obtenerCasilla(3, 3)</code> sí falla, porque ese método no valida (L44). El mensaje dice el tipo de error, el índice culpable (3) y el tamaño del arreglo (3). <code>#1:38</code> significa «fragmento 1 (el archivo que abriste), línea 38 contando desde la línea de la clase»; en el archivo real es la L44.</li>
</ul>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Mensaje o síntoma</th><th>Causa</th><th>Solución</th></tr>
<tr><td><code>incompatible types: String cannot be converted to char</code></td><td>Escribiste <code>"X"</code> o <code>" "</code> con comillas dobles</td><td>Un <code>char</code> va entre comillas simples: <code>'X'</code>, <code>' '</code></td></tr>
<tr><td><code>missing return statement</code></td><td>Falta el <code>return</code> final de <code>tableroLleno</code> (L56) o de <code>verificarGanador</code> (L78)</td><td>Todo método que devuelve algo debe hacerlo por todos los caminos</td></tr>
<tr><td><code>class Tablero is public, should be declared in a file named Tablero.java</code></td><td>El archivo se llama distinto (por ejemplo <code>tablero.java</code>)</td><td>Renómbralo con la misma mayúscula que la clase</td></tr>
<tr><td><code>reached end of file while parsing</code></td><td>Falta una <code>}</code></td><td>Usa <i>Source → Format</i> (Alt+Shift+F) en NetBeans: la sangría torcida delata la llave que falta</td></tr>
<tr><td>Nadie puede jugar: todas las casillas dicen «ocupada»</td><td>Borraste <code>reiniciar();</code> del constructor (L15)</td><td>Las casillas quedaron con <code>'\u0000'</code>; vuelve a llamar a <code>reiniciar()</code></td></tr>
<tr><td>En el primer turno «gana» el espacio</td><td>Falta la condición <code>!= VACIA</code> en alguna línea de <code>verificarGanador</code></td><td>Cada línea debe empezar comprobando que su primera casilla no esté vacía</td></tr>
<tr><td><code>cannot find symbol</code> en <code>jshell</code></td><td>No ejecutaste <code>/open</code>, o lo hiciste desde otra carpeta</td><td>Sal con <code>/exit</code>, entra a la carpeta del proyecto y repite</td></tr>
</table>

<div class="caja git"><b>Git</b> Tu primera clase está escrita y probada: guárdala en el historial con el mensaje del plan. Desde la carpeta del proyecto:
<pre class="ps">git status
git add src\Tablero.java
git commit -m "Tablero: estado y reglas del juego"
git push</pre>
<code>git status</code> debe mostrar <code>src/Tablero.java</code> como archivo nuevo (<i>untracked</i>) y nada más; la carpeta <code>target\</code> no aparece porque el <code>.gitignore</code> del capítulo 5 la excluye. Agregamos el archivo por su nombre, en lugar de <code>git add .</code>, para que el commit contenga exactamente lo que dice su mensaje.</div>

<h2>Resumen</h2>
<ul>
<li><code>Tablero</code> guarda el estado (una matriz privada <code>char[3][3]</code>) y aplica las reglas; no sabe nada de interfaz ni de IA.</li>
<li><code>VACIA</code> es una constante <code>public static final</code>: un solo valor, compartido, que no cambia y que da nombre a la casilla vacía.</li>
<li>El constructor crea la matriz y llama a <code>reiniciar()</code>, porque Java no llena los <code>char</code> con espacios sino con <code>'\u0000'</code>.</li>
<li><code>marcarCasilla</code> valida rango y ocupación con cláusulas de guarda y avisa con <code>true</code> o <code>false</code>; es el único lugar donde se ponen fichas.</li>
<li><code>verificarGanador</code> revisa filas y columnas en un mismo ciclo y las diagonales aparte; cada línea exige primero que no esté vacía, y <code>&amp;&amp;</code> se corta en cuanto algo es falso.</li>
<li><code>obtenerCopia</code> crea un objeto nuevo y copia valor por valor; asignar una referencia no copia nada.</li>
<li><code>jshell</code> con <code>/open</code> permite probar una clase sin escribir ningún programa.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b> El patrón «clase que guarda el estado y protege sus reglas» aparece en todas partes:
<ul>
<li><b>Una sala de cine</b>: una clase <code>Sala</code> con <code>boolean[10][15]</code> de asientos y un método <code>reservar(fila, asiento)</code> que devuelve <code>false</code> si el asiento no existe o ya está ocupado. Es <code>marcarCasilla</code> con otro nombre.</li>
<li><b>Un parqueo</b>: <code>String[] plazas</code> con <code>null</code> como «libre», un método <code>estaLleno()</code> idéntico en idea a <code>tableroLleno()</code> y uno <code>buscarPlaca(placa)</code>.</li>
<li><b>Una hoja de cálculo o un juego de buscaminas</b>: matrices recorridas con dos <code>for</code> anidados, igual que aquí.</li>
<li><b>Simular sin riesgo</b>: un sistema de inventario puede hacer una copia del stock para calcular «¿qué pasaría si vendo este pedido?» antes de confirmarlo, igual que la IA con <code>obtenerCopia()</code>.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>En <code>jshell</code>, crea un tablero, llénalo de modo que termine en empate y comprueba que <code>tableroLleno()</code> devuelve <code>true</code> y <code>verificarGanador()</code> devuelve <code>' '</code>. Pista: X O X / X O O / O X X.</li>
<li>Haz a mano la traza de <code>verificarGanador()</code> para el tablero O X X / ␣ O X / ␣ ␣ O. ¿En qué paso termina y qué devuelve?</li>
<li>Agrega (en una copia aparte del archivo, no en tu proyecto) un método <code>public int contarVacias()</code> que devuelva cuántas casillas vacías quedan. Pista: un contador <code>int</code> que empieza en 0 y dos <code>for</code>.</li>
<li>¿Qué pasaría si en L33 se usara <code>&amp;&amp;</code> en lugar de <code>||</code>? Prueba mentalmente con <code>marcarCasilla(5, 1, 'X')</code>.</li>
<li>Reto: reescribe <code>verificarGanador</code> para un tablero de 4×4 donde se gana con 4 en línea. Pista: un <code>for</code> para filas y columnas que compare 4 casillas, y las dos diagonales con otro <code>for</code>.</li>
</ol></div>
""",
}
