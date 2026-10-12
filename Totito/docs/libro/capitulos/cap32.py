# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 32,
    "titulo": "PruebaConsola.java: jugar contra la IA sin ventana",
    "antes": r"""
<p class="entrada">Ya tienes las tres clases de lógica, probadas una por una en <code>jshell</code>. Ahora toca comprobar que funcionan <b>juntas</b> en una partida completa. Lo harás con un programa pequeño que se juega en la terminal: escribes la fila y la columna, la IA responde y el tablero se dibuja con letras. Sin ventanas, sin colores, sin ratón: solo la lógica, a la vista.</p>

<h2>Por qué existe este archivo</h2>
<p>En el capítulo 28 lo comparamos con el banco de pruebas de un mecánico, que prueba el motor fuera del carro. Si la ventana del capítulo 33 fallara y no hubieras probado antes la lógica por separado, no sabrías si el problema está en las reglas, en la IA o en los botones. Con <code>PruebaConsola</code> descartas los dos primeros: si aquí la partida va bien, la lógica está sana.</p>
<p>Este programa tiene tres particularidades que conviene entender desde ya:</p>
<ul>
<li><b>Vive en <code>herramientas\</code>, no en <code>src\</code></b>. No forma parte del juego que se entrega: Maven solo compila lo que está en <code>src</code> (así lo dice el <code>pom.xml</code> del capítulo 5), así que esta herramienta no terminará dentro del <code>.jar</code> ni del instalador. Es para ti, el programador.</li>
<li><b>No modifica ninguna clase del juego</b>: solo las usa. Si para probar algo tuvieras que cambiar <code>Tablero</code>, la prueba ya no demostraría que <code>Tablero</code> funciona tal como está.</li>
<li><b>Se ejecuta directamente desde el código fuente</b>, con una función de Java que todavía no has usado: el modo «archivo fuente», que se explica en «Compila y prueba».</li>
</ul>

<h2>Qué vas a aprender</h2>
<ul>
<li>A escribir un programa con <code>main</code> que usa tus propias clases.</li>
<li>A leer números del teclado con <code>Scanner</code> (capítulo 17) y a detectar cuándo se acabó la entrada.</li>
<li>El ciclo principal de un juego: un <code>while (true)</code> que se repite hasta que alguien gana, con <code>continue</code> y <code>return</code> para controlarlo.</li>
<li>A dividir <code>main</code> en métodos auxiliares <code>private static</code>.</li>
<li>A dibujar con texto usando <code>System.out.println</code> y la concatenación con <code>+</code>.</li>
<li>A ejecutar un archivo <code>.java</code> sin compilarlo antes, con <code>-cp</code> para encontrar las demás clases.</li>
</ul>

<h2>Créalo</h2>
<p>La carpeta <code>herramientas</code> está fuera de <i>Source Packages</i>, así que en NetBeans se crea desde la pestaña de archivos:</p>
<ol>
<li>Abre <i>Window → Files</i> (Ctrl+2). Esta pestaña muestra las carpetas reales del disco, no la vista «lógica» de <i>Projects</i>.</li>
<li>Clic derecho sobre la carpeta <i>Totito</i> → <i>New → Folder…</i> → nombre <code>herramientas</code> → <i>Finish</i>.</li>
<li>Clic derecho sobre <i>herramientas</i> → <i>New → Other…</i> → categoría <i>Other</i> → tipo <i>Empty File</i> → <i>Next</i> → nombre <code>PruebaConsola.java</code> → <i>Finish</i>.</li>
<li>Escribe el código y guarda con Ctrl+S.</li>
</ol>
<p>Con PowerShell, desde la carpeta del proyecto, es más rápido:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
New-Item -ItemType Directory herramientas
New-Item herramientas\PruebaConsola.java</pre>
<p>La primera línea crea la carpeta (<code>-ItemType Directory</code> le dice a <code>New-Item</code> que no es un archivo) y la segunda el archivo vacío dentro. Luego ábrelo en NetBeans desde la pestaña <i>Files</i>.</p>
<div class="caja cuidado"><b>Subrayados rojos que no son errores</b> Como el archivo está fuera de <code>src</code>, puede que NetBeans no lo considere parte del proyecto y subraye en rojo <code>Tablero</code>, <code>Jugador</code> o <code>IA_Minimax</code> diciendo que no los encuentra. Si los nombres están bien escritos, ignóralo: el que manda es el comando <code>java</code> de más abajo, que sí sabe dónde buscarlas.</div>
""",
    "archivos": [
        {"ruta": "herramientas/PruebaConsola.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>import</code> le dice al compilador dónde está una clase que no es nuestra (capítulo 11). <code>java.util.Scanner</code> es la clase de Java que lee texto y números del teclado (capítulo 17); vive en el paquete <code>java.util</code>, que no se importa solo. Sin esta línea, cada <code>Scanner</code> daría <code>cannot find symbol</code>. Las clases <code>Tablero</code>, <code>Jugador</code> e <code>IA_Minimax</code> no necesitan <code>import</code>: están, como esta, en el paquete por defecto (sin paquete), y Java las encontrará en <code>target\classes</code>.</p>
<p class="l"><b>L2</b> Línea en blanco: separa los <code>import</code> del resto.</p>
"""),
             ("public class PruebaConsola", r"""
<p class="l"><b>L3–L10</b> Javadoc. Explica qué prueba (las tres clases de lógica), cuándo (antes de que exista la interfaz gráfica), cómo se juega (con la X, escribiendo fila y columna de 0 a 2) y, muy útil, <b>cómo se ejecuta</b>: el comando exacto, desde la carpeta Totito y después de compilar. Un comentario así te ahorra recordar el comando dentro de seis meses. La línea 7, con un <code>*</code> solo, es una línea en blanco dentro del comentario. El comando está escrito con <code>/</code>; en PowerShell funciona igual con <code>\</code>.</p>
<p class="l"><b>L11</b> Declara la clase pública <code>PruebaConsola</code>. Es una clase que no está pensada para crear objetos (nunca se hará <code>new PruebaConsola()</code>): solo es un contenedor para el método <code>main</code> y sus dos ayudantes, todos <code>static</code>.</p>
<p class="l"><b>L12</b> Línea en blanco.</p>
"""),
             ("public static void main", r"""
<p class="l"><b>L13</b> El método <code>main</code>, el punto de entrada (capítulo 11): cuando ejecutas el programa, Java busca exactamente esta firma y empieza por aquí. <code>public</code> para que Java pueda llamarlo desde fuera; <code>static</code> porque se ejecuta sin crear ningún objeto <code>PruebaConsola</code>; <code>void</code> porque no devuelve nada; <code>String[] args</code> recibe los textos que se escriban después del comando (aquí no se usan, pero la firma debe incluirlos).</p>
<p class="l"><b>L14</b> Crea el tablero de la partida, vacío gracias al constructor del capítulo 29. Es una variable local de <code>main</code>: existe mientras dura el programa.</p>
<p class="l"><b>L15</b> Crea al jugador humano con el nombre <code>"Tu"</code> (sin tilde, por la regla de los comentarios y textos del código) y la ficha <code>'X'</code>. En esta herramienta solo se usará su ficha.</p>
<p class="l"><b>L16</b> Crea la IA: juega con <code>'O'</code> y su rival con <code>'X'</code>. Recuerda el orden del constructor del capítulo 31: primero la ficha de la IA.</p>
<p class="l"><b>L17</b> Crea el lector de teclado. <code>System.in</code> es la «entrada estándar» del programa: lo que escribes en la terminal (o lo que le llegue por una tubería, como verás). El <code>Scanner</code> la parte en <b>palabras</b> (tokens) separadas por espacios o saltos de línea y las convierte en números cuando se le pide.</p>
<p class="l"><b>L18</b> Línea en blanco: termina la preparación y empieza el juego.</p>
"""),
             ("System.out.println(\"Totito en consola", r"""
<p class="l"><b>L19</b> Escribe las instrucciones en la terminal. <code>System.out.println</code> imprime un texto y salta de línea. Incluye un ejemplo («1 1»), porque el formato de la entrada no es evidente: dos números separados por un espacio.</p>
<p class="l"><b>L20</b> Dibuja el tablero vacío llamando al método auxiliar <code>imprimir</code> (L62). Se puede llamar sin escribir nada delante porque es un método <code>static</code> de esta misma clase.</p>
<p class="l"><b>L21</b> El <b>ciclo principal del juego</b>. <code>while (true)</code> se repite «para siempre»: la condición <code>true</code> nunca deja de cumplirse. Parece peligroso, pero la salida está dentro: los <code>return</code> de L24, L34 y L42 terminan <code>main</code> (y con él el programa) cuando se acaba la entrada o la partida. Casi todos los juegos tienen un ciclo así: leer jugada, actualizar, mostrar, comprobar si terminó, repetir.</p>
<p class="l"><b>L22</b> Pide la jugada. <code>print</code> (sin <code>ln</code>) no salta de línea, así que lo que escribas aparece a continuación de «Tu jugada: ».</p>
<p class="l"><b>L23</b> <code>teclado.hasNextInt()</code> espera a que escribas algo y responde si la siguiente palabra es un número entero, <b>sin consumirla</b>. El <code>!</code> la niega: «si lo siguiente <b>no</b> es un número…». Eso ocurre en dos casos: si escribes letras (o algo como «1,1», que es una sola palabra que no es número), o si se cerró la entrada (cuando pulsas Ctrl+Z y Enter en Windows, o cuando la entrada viene de un archivo que ya se acabó).</p>
<p class="l"><b>L24</b> En ese caso, <code>return</code> termina <code>main</code> sin error: el programa acaba limpiamente. El comentario de la línea lo explica. Sin esta comprobación, <code>nextInt()</code> lanzaría una excepción y verías un mensaje rojo de error al cerrar la entrada.</p>
<p class="l"><b>L25</b> Cierra el <code>if</code>.</p>
"""),
             ("int fila = teclado.nextInt()", r"""
<p class="l"><b>L26</b> Lee el primer número y lo guarda en <code>fila</code>. <code>nextInt()</code> sí consume la palabra.</p>
<p class="l"><b>L27</b> Lee el segundo número, la columna. Si escribiste un solo número y Enter, el programa se queda esperando el segundo (no pasa nada; escríbelo). Si el segundo no es un número, por ejemplo «1 a», aquí se produce una <code>InputMismatchException</code> y el programa se cierra con error: L23 solo comprobó la primera palabra. Para una herramienta de pruebas es aceptable; en el ejercicio 4 lo blindarás.</p>
<p class="l"><b>L28</b> Intenta marcar la casilla con la ficha del jugador (<code>humano.getFicha()</code>, es decir, <code>'X'</code>). Aquí se aprovecha el <code>boolean</code> que devuelve <code>marcarCasilla</code>: el <code>!</code> pregunta «si <b>no</b> se pudo marcar…». Fíjate en que la llamada <b>hace</b> la jugada y a la vez <b>pregunta</b> si salió bien: si la casilla es válida, la ficha ya quedó puesta al evaluar la condición.</p>
<p class="l"><b>L29</b> Si no se pudo (casilla ocupada o fuera del tablero), avisa. Es el caso «casilla ocupada» del capítulo 28, resuelto por <code>Tablero</code>; aquí solo se muestra el mensaje.</p>
<p class="l"><b>L30</b> <code>continue</code> salta directamente a la siguiente vuelta del <code>while</code>: vuelve a pedir la jugada sin que juegue la IA. Sin esta línea, una jugada inválida le daría el turno a la IA y la persona perdería su turno.</p>
<p class="l"><b>L31</b> Cierra el <code>if</code>.</p>
"""),
             ("imprimir(tablero);", r"""
<p class="l"><b>L32</b> La jugada fue válida: muestra el tablero con la nueva X.</p>
<p class="l"><b>L33</b> Llama al ayudante <code>terminoLaPartida</code> (L48), que escribe el resultado si alguien ganó o hubo empate y devuelve <code>true</code> en ese caso.</p>
<p class="l"><b>L34</b> Si terminó, <code>return</code> acaba el programa. Es importante comprobarlo <b>antes</b> de pedirle jugada a la IA: si la persona acaba de llenar la última casilla, la IA no tendría dónde jugar (devolvería <code>{-1, -1}</code> y L38 intentaría marcar en la fila −1).</p>
<p class="l"><b>L35–L36</b> Cierran el <code>if</code> y separan el turno de la persona del turno de la IA.</p>
"""),
             ("int[] jugada = ia.calcularMejorJugada", r"""
<p class="l"><b>L37</b> Turno de la IA: le pide su mejor jugada al Minimax del capítulo 31 y recibe un arreglo <code>{fila, columna}</code>. Recuerda que este método no toca el tablero.</p>
<p class="l"><b>L38</b> Coloca la O en esa casilla. Aquí sí se escribe en el tablero real. No se mira el resultado de <code>marcarCasilla</code> porque la IA solo elige casillas vacías. (La ficha <code>'O'</code> va escrita a mano, repitiendo lo que se dijo en L16; en una herramienta de pruebas se tolera, pero en el juego definitivo convendría una constante, como hace <code>JuegoMain</code> en el capítulo 33.)</p>
<p class="l"><b>L39</b> Anuncia la jugada. El operador <code>+</code> une textos con números: <code>"La IA juega en " + 0 + " " + 0</code> produce el texto <code>La IA juega en 0 0</code>. Ese <code>" "</code> del medio es necesario; sin él saldría «00».</p>
<p class="l"><b>L40</b> Muestra el tablero con la O nueva.</p>
<p class="l"><b>L41–L43</b> ¿Terminó la partida con la jugada de la IA? Si es así, sale.</p>
<p class="l"><b>L44–L46</b> Cierran el <code>while</code> (y se vuelve a L22 para el siguiente turno), el método <code>main</code> y dejan una línea en blanco.</p>
"""),
             ("private static boolean terminoLaPartida", r"""
<p class="l"><b>L47</b> Javadoc: este ayudante escribe el resultado si alguien ganó o hubo empate.</p>
<p class="l"><b>L48</b> Firma. <code>private</code>: solo lo usa esta clase. <code>static</code>: <code>main</code> es estático y no hay objeto <code>PruebaConsola</code>, así que los métodos que llama también deben serlo (un método <code>static</code> no puede llamar a uno de objeto sin crear el objeto). Devuelve <code>boolean</code> («¿terminó?») y recibe el tablero. Existe para no escribir dos veces el mismo bloque: se usa tras la jugada de la persona (L33) y tras la de la IA (L41).</p>
<p class="l"><b>L49</b> Pregunta quién ganó: <code>'X'</code>, <code>'O'</code> o <code>' '</code>.</p>
<p class="l"><b>L50</b> Si la respuesta no es <code>VACIA</code>, alguien ganó.</p>
<p class="l"><b>L51</b> Escribe «Gano X» o «Gano O»: el <code>+</code> une el texto con el <code>char</code>.</p>
<p class="l"><b>L52–L53</b> Devuelve <code>true</code> y cierra el <code>if</code>.</p>
"""),
             ("if (tablero.tableroLleno())", r"""
<p class="l"><b>L54–L56</b> Si nadie ganó pero el tablero está lleno, escribe «Empate» y devuelve <code>true</code>. Otra vez, el ganador se pregunta antes que el empate.</p>
<p class="l"><b>L57</b> Cierra el <code>if</code>.</p>
<p class="l"><b>L58</b> Ni ganador ni tablero lleno: la partida sigue, devuelve <code>false</code>.</p>
<p class="l"><b>L59–L60</b> Cierran el método y dejan una línea en blanco.</p>
"""),
             ("private static void imprimir", r"""
<p class="l"><b>L61</b> Javadoc con una muestra de cómo se ve una fila: <code>X | O |</code>.</p>
<p class="l"><b>L62</b> El ayudante que dibuja el tablero. <code>private static void</code>: interno, sin objeto, no devuelve nada (solo escribe en la terminal).</p>
<p class="l"><b>L63</b> <code>println()</code> sin nada dentro escribe una línea vacía, para separar el tablero de lo que haya arriba.</p>
<p class="l"><b>L64</b> Recorre las tres filas. Aquí basta un <code>for</code>, porque cada fila se escribe en una sola instrucción.</p>
<p class="l"><b>L65–L67</b> <b>Una sola instrucción repartida en tres líneas</b>. Java no termina una instrucción al final de la línea, sino en el <code>;</code>; partirla así la hace legible. Concatena: un espacio, la casilla de la columna 0, <code>" | "</code>, la de la columna 1, <code>" | "</code> y la de la columna 2. Para la fila con X en el centro produce <code>   | X |  </code>. Como una casilla vacía guarda un espacio (la constante <code>VACIA</code> del capítulo 29), se ve vacía sin ningún código extra: aquí se nota que elegir <code>' '</code> fue buena idea. El primer operando es un texto (<code>" "</code>), y por eso todos los <code>+</code> unen texto; si empezara con dos <code>char</code>, Java los sumaría como números.</p>
"""),
             ("if (fila < 2)", r"""
<p class="l"><b>L68–L70</b> Después de las filas 0 y 1 (no de la 2) escribe la línea separadora <code>---+---+---</code>. Sin la condición, habría una raya también debajo de la última fila.</p>
<p class="l"><b>L71</b> Cierra el <code>for</code>.</p>
<p class="l"><b>L72</b> Otra línea vacía, para separar el tablero de lo que venga después.</p>
<p class="l"><b>L73–L74</b> Cierran el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<p>Un turno completo recorre el ciclo así. Supón que el tablero está vacío y escribes <code>1 1</code>:</p>
<table class="tabla">
<tr><th>Línea</th><th>Qué pasa</th><th>Estado</th></tr>
<tr><td>L22–L23</td><td>Escribe «Tu jugada: », espera; <code>hasNextInt()</code> ve «1»: es número</td><td>—</td></tr>
<tr><td>L26–L27</td><td>Lee <code>fila = 1</code>, <code>columna = 1</code></td><td>—</td></tr>
<tr><td>L28</td><td><code>marcarCasilla(1, 1, 'X')</code> devuelve <code>true</code>; <code>!true</code> es <code>false</code>: no entra al <code>if</code></td><td>X en el centro</td></tr>
<tr><td>L32–L33</td><td>Dibuja; <code>terminoLaPartida</code> devuelve <code>false</code> (una X no gana)</td><td>—</td></tr>
<tr><td>L37</td><td>La IA calcula: las esquinas valen 0, los lados −5; devuelve <code>{0, 0}</code></td><td>—</td></tr>
<tr><td>L38–L40</td><td>Marca la O en (0,0), escribe «La IA juega en 0 0» y dibuja</td><td>X centro, O esquina</td></tr>
<tr><td>L41</td><td><code>terminoLaPartida</code> devuelve <code>false</code></td><td>—</td></tr>
<tr><td>L44 → L22</td><td>Fin de la vuelta; el <code>while</code> pide la siguiente jugada</td><td>—</td></tr>
</table>
<p>Si en la siguiente vuelta escribes <code>1 1</code> otra vez, L28 recibe <code>false</code> del tablero, L29 avisa y L30 (<code>continue</code>) vuelve a L22 sin pasar por la IA.</p>

<h2>Compila y prueba</h2>
<p>Primero compila las clases del juego: en NetBeans, <i>Run → Clean and Build Project</i> (Shift+F11). Eso deja <code>Tablero.class</code>, <code>Jugador.class</code> e <code>IA_Minimax.class</code> en <code>target\classes</code>. Luego, en PowerShell:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
java -cp target\classes herramientas\PruebaConsola.java</pre>
<p>Este comando tiene dos partes que vale la pena entender:</p>
<ul>
<li><b>Modo archivo fuente.</b> Normalmente a <code>java</code> se le da el nombre de una clase ya compilada. Desde Java 11 también acepta directamente un archivo <code>.java</code>: lo compila en la memoria, sin crear ningún <code>.class</code>, y ejecuta su <code>main</code>. Es ideal para herramientas de un solo archivo como esta: no hay que compilarlas aparte ni ensucian el proyecto.</li>
<li><b><code>-cp target\classes</code></b> (de <i>classpath</i>, «ruta de clases») le dice a Java dónde buscar las <b>otras</b> clases que usa el programa. El archivo <code>PruebaConsola.java</code> menciona <code>Tablero</code>, <code>Jugador</code> e <code>IA_Minimax</code>, pero no las contiene: están compiladas en <code>target\classes</code>. Por eso hay que hacer <i>Clean and Build</i> antes, y volver a hacerlo cada vez que cambies alguna de esas clases.</li>
</ul>
<p>Esta es una partida real (la entrada que escribimos fue <code>1 1</code>, <code>0 2</code>, <code>0 0</code>, <code>1 0</code>, <code>2 1</code> y <code>2 2</code>; la tercera es a propósito una casilla ocupada):</p>
<pre class="salida">Totito en consola. Escribe fila y columna (0 a 2), por ejemplo: 1 1

   |   |
---+---+---
   |   |
---+---+---
   |   |

Tu jugada: 1 1

   |   |
---+---+---
   | X |
---+---+---
   |   |

La IA juega en 0 0

 O |   |
---+---+---
   | X |
---+---+---
   |   |

Tu jugada: 0 2

 O |   | X
---+---+---
   | X |
---+---+---
   |   |

La IA juega en 2 0

 O |   | X
---+---+---
   | X |
---+---+---
 O |   |

Tu jugada: 0 0
Esa casilla no se puede usar. Prueba otra.
Tu jugada: 1 0

 O |   | X
---+---+---
 X | X |
---+---+---
 O |   |

La IA juega en 1 2

 O |   | X
---+---+---
 X | X | O
---+---+---
 O |   |

Tu jugada: 2 1

 O |   | X
---+---+---
 X | X | O
---+---+---
 O | X |

La IA juega en 0 1

 O | O | X
---+---+---
 X | X | O
---+---+---
 O | X |

Tu jugada: 2 2

 O | O | X
---+---+---
 X | X | O
---+---+---
 O | X | X

Empate</pre>
<p>Lee la partida como lo haría la IA:</p>
<ul>
<li>Ante la X en el centro responde en una esquina, (0,0), como predijo el capítulo 31.</li>
<li>La X juega en (0,2) y amenaza la diagonal (0,2)–(1,1)–(2,0): la IA <b>tapa</b> en (2,0). De paso, con (0,0) y (2,0) amenaza la columna 0.</li>
<li>La casilla ocupada se rechaza y se vuelve a pedir la jugada sin perder el turno (L29–L30).</li>
<li>La X tapa la columna 0 en (1,0) y con eso amenaza la fila 1: la IA tapa en (1,2). Luego la X amenaza la columna 1 y la IA tapa en (0,1).</li>
<li>Se llenan las 9 casillas sin línea: «Empate». Contra un rival que no se equivoca, es el mejor resultado posible para los dos.</li>
</ul>
<p>Y esta es otra partida real, en la que la persona se distrae (entrada: <code>0 0</code>, <code>0 1</code>, <code>2 2</code>). Solo mostramos el final:</p>
<pre class="salida">La IA juega en 0 2

 X | X | O
---+---+---
   | O |
---+---+---
   |   |

Tu jugada: 2 2

 X | X | O
---+---+---
   | O |
---+---+---
   |   | X

La IA juega en 2 0

 X | X | O
---+---+---
   | O |
---+---+---
 O |   | X

Gano O</pre>
<p>Con la O en (0,2) y en el centro, la IA amenazaba la diagonal hasta (2,0). La persona jugó en (2,2) en vez de tapar, y la IA no perdonó.</p>
<div class="caja consejo"><b>Probar sin teclear: la tubería</b> Puedes darle al programa todas las jugadas de una vez, como hicimos para obtener estas salidas: <code>"1 1", "0 2", "0 0", "1 0", "2 1", "2 2" | java -cp target\classes herramientas\PruebaConsola.java</code>. El <code>|</code> (la «tubería» de PowerShell, que pasa lo que sale de un comando a la entrada del siguiente) envía cada texto como una línea a la entrada del programa. Cuando se acaban, <code>hasNextInt()</code> devuelve <code>false</code> y el programa termina limpiamente gracias a L23–L24. Así puedes repetir una partida exacta cada vez que cambies algo en la lógica. (Con la entrada por tubería, la terminal no muestra lo que «escribiste»: verás «Tu jugada:» seguido directamente del tablero.)</div>
<h3>Cómo salir y errores típicos</h3>
<p>Para salir a mitad de partida pulsa <b>Ctrl+C</b> (interrumpe el programa) o <b>Ctrl+Z</b> y Enter (cierra la entrada; el programa termina solo en L24).</p>
<table class="tabla">
<tr><th>Mensaje o síntoma</th><th>Causa</th><th>Solución</th></tr>
<tr><td><code>error: cannot find symbol … symbol: class Tablero</code></td><td>Faltó <code>-cp target\classes</code>, o no hiciste <i>Clean and Build</i></td><td>Compila en NetBeans y escribe el comando completo</td></tr>
<tr><td><code>Error: Could not find or load main class herramientas.PruebaConsola.java</code></td><td>Ejecutaste el comando desde otra carpeta y Java no encontró el archivo</td><td><code>cd $HOME\Proyectos\Totito</code> y repite</td></tr>
<tr><td>El programa termina en silencio tras escribir la jugada</td><td>Escribiste algo que no es un número, como <code>1,1</code> o <code>uno</code></td><td>Dos números separados por un espacio: <code>1 1</code></td></tr>
<tr><td><code>InputMismatchException</code></td><td>El primer dato era número y el segundo no (<code>1 a</code>)</td><td>Vuelve a ejecutar; el ejercicio 4 lo corrige</td></tr>
<tr><td>Escribes un número y no pasa nada</td><td>El programa espera el segundo número</td><td>Escribe la columna y pulsa Enter</td></tr>
<tr><td>La IA juega mal después de cambiar <code>IA_Minimax</code></td><td>Cambiaste la clase pero no recompilaste: Java usa el <code>.class</code> viejo</td><td>Clean and Build antes de cada prueba</td></tr>
</table>

<div class="caja git"><b>Git</b> La herramienta se guarda en el repositorio (aunque no vaya en el juego, es parte del proyecto y le sirve a cualquiera que lo clone):
<pre class="ps">git add herramientas\PruebaConsola.java
git commit -m "Prueba de la logica en consola"
git push</pre>
El mensaje va sin tilde («logica») siguiendo el plan; Git acepta tildes, pero algunas terminales antiguas de Windows las muestran mal en el historial.</div>

<h2>Resumen</h2>
<ul>
<li><code>PruebaConsola</code> prueba las tres clases de lógica juntas, en una partida real, sin ninguna ventana y sin modificarlas.</li>
<li>Vive en <code>herramientas\</code>, fuera de <code>src\</code>, para que no forme parte del juego que se entrega.</li>
<li>El ciclo principal <code>while (true)</code> se controla con <code>continue</code> (repetir el turno) y <code>return</code> (terminar).</li>
<li><code>Scanner.hasNextInt()</code> comprueba sin consumir; <code>nextInt()</code> consume. Comprobar antes de leer evita errores al cerrar la entrada.</li>
<li>Los ayudantes <code>private static</code> evitan repetir código y dejan <code>main</code> legible.</li>
<li><code>java -cp target\classes archivo.java</code> compila en memoria y ejecuta un solo archivo, buscando las demás clases en <code>target\classes</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b> Probar la lógica en la terminal antes de construir la interfaz es una costumbre profesional:
<ul>
<li><b>Una calculadora de préstamos</b>: antes de diseñar la ventana, un <code>main</code> que lee monto, tasa y plazo con <code>Scanner</code> y escribe la cuota permite comprobar las fórmulas con casos conocidos.</li>
<li><b>Un sistema de inventario</b>: un menú de texto con <code>while (true)</code> («1. Agregar, 2. Vender, 3. Salir») prueba las reglas (no vender sin existencias) antes de que exista ninguna pantalla.</li>
<li><b>Herramientas de un solo archivo</b>: renombrar fotos, convertir un archivo CSV o generar datos de prueba se puede hacer con un <code>.java</code> suelto ejecutado con <code>java archivo.java</code>, sin crear un proyecto.</li>
<li><b>Pruebas repetibles</b>: guardar la entrada en un archivo y pasarla por tubería (<code>Get-Content jugadas.txt | java ...</code>) convierte una prueba manual en una que repites con un solo comando. Es el primer paso hacia las pruebas automáticas con JUnit (capítulo 69).</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Juega tres partidas intentando ganarle a la IA. Anota cómo termina cada una. ¿Pudiste ganar alguna? (No deberías.)</li>
<li>Repite con una tubería la partida de este capítulo en la que gana la O y comprueba que obtienes exactamente la misma salida.</li>
<li>Cambia, en una copia de la herramienta, el texto de L39 para que diga «La IA juega en la fila 0, columna 0». Pista: une más textos con <code>+</code>.</li>
<li>Blinda la lectura: haz que, si el segundo dato no es un número, el programa avise y vuelva a pedir la jugada en lugar de caerse. Pista: comprueba <code>teclado.hasNextInt()</code> también antes de L27 y, si falla, descarta la palabra con <code>teclado.next()</code> y usa <code>continue</code>.</li>
<li>Reto: modifica una copia para que se puedan jugar varias partidas seguidas y al final muestre un marcador («Tu: 0, IA: 2, Empates: 1»). Pista: un segundo ciclo alrededor del actual, <code>tablero.reiniciar()</code> y tres contadores.</li>
</ol></div>
""",
}
