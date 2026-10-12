# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 30,
    "titulo": "Jugador.java: nombre y ficha",
    "antes": r"""
<p class="entrada">La clase más corta del juego: 22 líneas que guardan el nombre de un jugador y su ficha. Precisamente por ser tan pequeña es perfecta para ver con calma tres ideas que usarás en todos tus programas: atributos <code>final</code>, el constructor que recibe datos con <code>this</code>, y los <i>getters</i> que dejan leer sin dejar cambiar.</p>

<h2>Por qué existe este archivo</h2>
<p>En el capítulo 28 subrayamos el sustantivo «jugador» y vimos que tiene dos datos que siempre van juntos: un <b>nombre</b> y una <b>ficha</b>. Podríamos guardarlos en variables sueltas (<code>String nombre1</code>, <code>char ficha1</code>, <code>String nombre2</code>, <code>char ficha2</code>…), pero eso tiene problemas que crecen con el programa:</p>
<ul>
<li>Nada impide mezclar el nombre del jugador 1 con la ficha del jugador 2.</li>
<li>Para pasarle «un jugador» a un método habría que pasar dos parámetros, y si mañana el jugador tuviera también un color o una foto, habría que cambiar todas las llamadas.</li>
<li>En la Parte VII, la clase <code>Partida</code> guardará un arreglo <code>Jugador[]</code> de dos jugadores y el marcador mostrará <code>jugador.getNombre()</code> de cada uno. Con variables sueltas no habría forma de tener «una lista de jugadores».</li>
</ul>
<p>Una clase que solo agrupa datos se llama a veces <b>clase de datos</b> u <b>objeto de valor</b>. Es como un gafete de identificación: tiene el nombre y el número de quien lo porta, y nada más. No sabe jugar, ni conoce las reglas, ni la pantalla. Esa simplicidad es una virtud: es imposible que tenga errores de lógica, porque no tiene lógica.</p>
<p>En la versión 0.1 el <code>Jugador</code> se usa poco (la ventana y la terminal solo le piden la ficha), pero lo creamos ya porque es parte del modelo del juego, y en la versión 1.0 los nombres que escriba la persona en la pantalla de configuración viajarán dentro de objetos <code>Jugador</code> sin que esta clase cambie.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>A declarar atributos <code>private final</code>, que se asignan una sola vez y quedan protegidos.</li>
<li>A escribir un constructor con parámetros y a usar <code>this</code> cuando un parámetro se llama igual que un atributo.</li>
<li>A escribir <i>getters</i> (métodos <code>getAlgo()</code>) y por qué aquí no hay <i>setters</i>.</li>
<li>Qué es un objeto <b>inmutable</b> y por qué es más seguro.</li>
<li>Qué es el tipo <code>String</code> como atributo, comparado con <code>char</code>.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>En NetBeans, en <i>Projects</i>, clic derecho sobre <i>Source Packages → &lt;default package&gt;</i> → <i>New → Java Class…</i></li>
<li><i>Class Name</i>: <code>Jugador</code> → <i>Finish</i>.</li>
<li>Borra la plantilla (Ctrl+A y Supr) y escribe el archivo de abajo. Guarda con Ctrl+S.</li>
</ol>
<p>O desde PowerShell, en la carpeta del proyecto:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
New-Item src\Jugador.java</pre>
<div class="caja consejo"><b>Que NetBeans escriba por ti (cuando ya entiendes)</b> NetBeans puede generar el constructor y los getters: escribe solo los dos atributos, pulsa <b>Alt+Insert</b> dentro de la clase y elige <i>Constructor…</i> y luego <i>Getter…</i>, marcando los atributos. El resultado es casi idéntico al de este capítulo. Úsalo cuando ya sepas escribirlos a mano: una herramienta ahorra tiempo, pero no sustituye entender lo que genera.</div>
""",
    "archivos": [
        {"ruta": "src/Jugador.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1–L4</b> Comentario de documentación. Dice qué representa la clase (al jugador humano: su nombre y su ficha) y deja claro lo que <b>no</b> hace: «sin logica de juego». Igual que en <code>Tablero</code>, esa frase protege el diseño: si alguien pensara en añadir aquí «comprobar si el jugador ganó», el comentario le recuerda que eso es trabajo del tablero. (En la versión 1.0 la clase también representará a la computadora y al segundo jugador humano; el código no cambia, porque un nombre y una ficha sirven para cualquiera.)</p>
<p class="l"><b>L5</b> Declara la clase pública <code>Jugador</code>, en el archivo <code>Jugador.java</code>. La llave abre su cuerpo, que se cierra en L22.</p>
<p class="l"><b>L6</b> Línea en blanco para separar la declaración de los atributos.</p>
"""),
             ("private final String nombre", r"""
<p class="l"><b>L7</b> Primer atributo: el nombre del jugador. Palabra por palabra:</p>
<ul>
<li><code>private</code>: solo esta clase puede leerlo o escribirlo directamente. Los demás tendrán que pedirlo con <code>getNombre()</code>.</li>
<li><code>final</code>: se le puede asignar un valor <b>una sola vez</b>, y debe hacerse en el constructor. Después nadie, ni siquiera la propia clase, puede cambiarlo. Un atributo <code>final</code> que no se asigna en el constructor es un error de compilación: <code>variable nombre might not have been initialized</code>.</li>
<li><code>String</code>: el tipo, una cadena de texto de cualquier largo (capítulo 17). Se escribe con mayúscula porque <code>String</code> es una clase, no un tipo primitivo como <code>char</code> o <code>int</code>. Un nombre como «Ana» necesita varios caracteres, así que no cabe en un <code>char</code>.</li>
<li><code>nombre</code>: el nombre del atributo.</li>
</ul>
<p class="l"><b>L8</b> Segundo atributo: la ficha, <code>'X'</code> u <code>'O'</code>. Es un <code>char</code>, el mismo tipo que usan las casillas del <code>Tablero</code>; así la ficha del jugador se puede pasar directamente a <code>marcarCasilla</code> y comparar con <code>verificarGanador()</code> sin conversiones. También es <code>private final</code>.</p>
<p class="l"><b>L9</b> Línea en blanco.</p>
<div class="caja concepto"><b>Inmutable</b> Como los dos atributos son <code>final</code> y no hay ningún método que los cambie, un <code>Jugador</code> es <b>inmutable</b>: una vez creado, sus datos no cambian nunca. Ventaja práctica: lo puedes pasar a cualquier método o guardar en cualquier lista con la tranquilidad de que nadie lo modificará a tus espaldas. Si un jugador quisiera cambiar de nombre, se crea un <code>Jugador</code> nuevo. Los <code>String</code> de Java son inmutables por la misma razón.</div>
"""),
             ("public Jugador(String nombre, char ficha)", r"""
<p class="l"><b>L10</b> El constructor. Se llama igual que la clase y no tiene tipo de retorno. A diferencia del de <code>Tablero</code>, este recibe dos <b>parámetros</b>: <code>String nombre</code> y <code>char ficha</code>. Eso significa que no se puede crear un jugador «en blanco»: hay que escribir <code>new Jugador("Ana", 'X')</code>, con sus dos datos y en ese orden. Como al declarar un constructor con parámetros Java ya no crea el constructor vacío automático, <code>new Jugador()</code> daría un error. Es una forma de obligar a que todo jugador nazca completo.</p>
<p class="l"><b>L11</b> Guarda el nombre recibido en el atributo. Aquí hay un detalle importante: dentro del constructor existen <b>dos</b> cosas llamadas <code>nombre</code>, el parámetro (L10) y el atributo (L7). Cuando dos variables se llaman igual, gana la más cercana: el parámetro «tapa» al atributo (se dice que lo <b>sombrea</b>). Para referirse al atributo se escribe <code>this.nombre</code>, «el <code>nombre</code> de este objeto». La línea se lee: «el nombre de este jugador es igual al nombre que me pasaron».</p>
<p class="l">¿Qué pasaría si escribieras <code>nombre = nombre;</code> sin <code>this</code>? Asignarías el parámetro a sí mismo, que no sirve de nada, y el atributo quedaría sin valor. Como es <code>final</code>, el compilador se da cuenta y lo rechaza con <code>variable nombre might not have been initialized</code>. Sin <code>final</code>, el programa compilaría y el nombre sería <code>null</code>: un error silencioso. Esta es una ventaja extra de <code>final</code>: atrapa errores.</p>
<p class="l"><b>L12</b> Lo mismo con la ficha: el atributo <code>this.ficha</code> recibe el valor del parámetro <code>ficha</code>.</p>
<p class="l"><b>L13</b> Cierra el constructor. A partir de aquí, los dos atributos <code>final</code> ya tienen su valor definitivo.</p>
<p class="l"><b>L14</b> Línea en blanco.</p>
"""),
             ("public String getNombre()", r"""
<p class="l"><b>L15</b> Un <b>getter</b> (del inglés <i>get</i>, «obtener»): un método público cuyo único trabajo es devolver un atributo privado. Devuelve <code>String</code> y no recibe nada. El nombre sigue una convención de Java: <code>get</code> + el nombre del atributo con mayúscula inicial. Muchas herramientas (y muchos programadores) buscan los datos de un objeto por esa forma, así que conviene respetarla.</p>
<p class="l"><b>L16</b> Devuelve el nombre. Como un <code>String</code> no se puede modificar, entregarlo es seguro: quien lo reciba no puede cambiar el nombre del jugador. Aquí no hace falta <code>this.</code> porque no hay ningún parámetro que tape al atributo; <code>return this.nombre;</code> sería equivalente.</p>
<p class="l"><b>L17–L18</b> Cierra el método y deja una línea en blanco.</p>
"""),
             ("public char getFicha()", r"""
<p class="l"><b>L19</b> El getter de la ficha: público, devuelve <code>char</code>. Es el que usarán la terminal de pruebas (<code>humano.getFicha()</code>) y la ventana (<code>jugador.getFicha()</code>) para saber qué letra poner en el tablero.</p>
<p class="l"><b>L20</b> Devuelve la ficha. Un <code>char</code> se entrega como copia del valor, así que tampoco hay riesgo.</p>
<p class="l"><b>L21–L22</b> Cierran el método y la clase.</p>
<div class="caja concepto"><b>¿Y los setters?</b> Un <b>setter</b> sería un método como <code>public void setFicha(char ficha)</code> que permite cambiar un atributo desde fuera. Aquí no hay ninguno, a propósito: un jugador no debería cambiar de ficha a mitad de partida, y los atributos son <code>final</code>, así que ni siquiera se podría escribir. La regla práctica del capítulo 19: <b>no escribas un setter solo porque puedes</b>. Agrega uno únicamente cuando el programa necesite de verdad cambiar ese dato, y entonces valida el valor nuevo dentro del setter.</div>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<p>Sigamos qué pasa en la memoria con esta línea, que escribirás en el capítulo 32:</p>
<pre class="java">Jugador humano = new Jugador("Tu", 'X');</pre>
<ol>
<li><code>new Jugador</code> reserva memoria para un objeto con dos atributos: <code>nombre</code> (de momento sin valor) y <code>ficha</code>.</li>
<li>Se ejecuta el constructor con <code>nombre = "Tu"</code> y <code>ficha = 'X'</code> como parámetros.</li>
<li>L11: <code>this.nombre</code> pasa a apuntar al texto <code>"Tu"</code>.</li>
<li>L12: <code>this.ficha</code> pasa a valer <code>'X'</code>.</li>
<li>El constructor termina y <code>new</code> devuelve la <b>referencia</b> al objeto, que se guarda en la variable <code>humano</code>.</li>
<li>Más tarde, <code>humano.getFicha()</code> ejecuta L20 y devuelve <code>'X'</code>, que se pasa a <code>tablero.marcarCasilla(fila, columna, 'X')</code>.</li>
</ol>
<table class="tabla">
<tr><th>Expresión</th><th>Valor</th><th>Por qué</th></tr>
<tr><td><code>new Jugador("Ana", 'X').getNombre()</code></td><td><code>"Ana"</code></td><td>L16 devuelve el atributo asignado en L11</td></tr>
<tr><td><code>new Jugador("Ana", 'X').getFicha()</code></td><td><code>'X'</code></td><td>L20 devuelve el atributo asignado en L12</td></tr>
<tr><td><code>new Jugador('X', "Ana")</code></td><td>no compila</td><td>Los argumentos deben ir en el orden y con los tipos de L10</td></tr>
<tr><td><code>new Jugador()</code></td><td>no compila</td><td>No existe un constructor sin parámetros</td></tr>
<tr><td><code>ana.nombre</code> (desde otra clase)</td><td>no compila</td><td><code>nombre</code> es <code>private</code></td></tr>
</table>
<div class="caja consejo"><b>¿Debería validar la ficha?</b> Ahora mismo nada impide crear <code>new Jugador("Ana", 'Z')</code>. En el Totito no pasa porque las fichas las ponemos nosotros en el código, nunca las escribe el usuario. En un programa donde los datos vienen de fuera, el constructor debería comprobarlos y lanzar una excepción si no valen, por ejemplo <code>if (ficha != 'X' &amp;&amp; ficha != 'O') throw new IllegalArgumentException("Ficha invalida: " + ficha);</code> (capítulo 26). Así ningún objeto podría nacer en un estado imposible. A esa garantía se le llama <b>invariante</b> (capítulo 19).</div>
<div class="caja concepto"><b>Para cuando sepas más: los <i>records</i></b> Desde Java 16 existe una forma abreviada de escribir clases de datos inmutables: <code>record Jugador(String nombre, char ficha) {}</code>. Esa sola línea genera los atributos <code>private final</code>, el constructor y los métodos de acceso. La diferencia es que esos métodos se llaman <code>nombre()</code> y <code>ficha()</code>, no <code>getNombre()</code> y <code>getFicha()</code>. En el libro usamos la clase clásica porque muestra cada pieza por separado y porque es lo que encontrarás en la mayoría del código Java existente.</div>

<h2>Compila y prueba</h2>
<p>Compila con <i>Run → Clean and Build Project</i> (Shift+F11) y busca <code>BUILD SUCCESS</code>. Luego pruébala en <code>jshell</code> desde la carpeta del proyecto:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
jshell</pre>
<pre class="salida">jshell&gt; /open src/Jugador.java

jshell&gt; Jugador ana = new Jugador("Ana", 'X');
ana ==&gt; Jugador@6615435c

jshell&gt; Jugador compu = new Jugador("Computadora", 'O');
compu ==&gt; Jugador@2d3fcdbd

jshell&gt; ana.getNombre()
$4 ==&gt; "Ana"

jshell&gt; ana.getFicha()
$5 ==&gt; 'X'

jshell&gt; compu.getNombre() + " juega con " + compu.getFicha()
$6 ==&gt; "Computadora juega con O"

jshell&gt; ana.nombre
|  Error:
|  nombre has private access in Jugador
|  ana.nombre
|  ^--------^

jshell&gt; ana.setFicha('O')
|  Error:
|  cannot find symbol
|    symbol:   method setFicha(char)
|  ana.setFicha('O')
|  ^----------^

jshell&gt; /exit
|  Goodbye</pre>
<p>Qué demuestra esta sesión (ejecutada de verdad; los números después de la arroba cambiarán en tu computadora):</p>
<ul>
<li>Hay dos objetos <code>Jugador</code> distintos, cada uno con sus datos: <code>ana</code> y <code>compu</code> no se mezclan.</li>
<li>Los getters devuelven lo que se pasó al constructor. En <code>$6</code>, el operador <code>+</code> une textos y convierte el <code>char</code> en texto automáticamente.</li>
<li>Leer el atributo directamente está prohibido (<code>private access</code>): el encapsulamiento funciona.</li>
<li>No hay forma de cambiar la ficha: el método <code>setFicha</code> no existe.</li>
</ul>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Mensaje</th><th>Causa</th><th>Solución</th></tr>
<tr><td><code>variable nombre might not have been initialized</code></td><td>Escribiste <code>nombre = nombre;</code> sin <code>this.</code>, o borraste una asignación del constructor</td><td>Usa <code>this.nombre = nombre;</code></td></tr>
<tr><td><code>cannot assign a value to final variable ficha</code></td><td>Intentaste cambiar un atributo <code>final</code> fuera del constructor</td><td>Es lo esperado: crea otro <code>Jugador</code></td></tr>
<tr><td><code>constructor Jugador in class Jugador cannot be applied to given types</code></td><td>Llamaste a <code>new Jugador</code> con otros datos, en otro orden o sin ellos</td><td>Siempre <code>new Jugador(texto, 'letra')</code></td></tr>
<tr><td><code>incompatible types: String cannot be converted to char</code></td><td>Pasaste la ficha como <code>"X"</code></td><td>Comillas simples: <code>'X'</code></td></tr>
</table>

<div class="caja git"><b>Git</b> Segundo commit de la Parte V:
<pre class="ps">git add src\Jugador.java
git commit -m "Jugador: nombre y ficha"
git push</pre>
Comprueba con <code>git log --oneline</code> que aparecen, uno encima del otro, este commit y el de <code>Tablero</code>.</div>

<h2>Resumen</h2>
<ul>
<li><code>Jugador</code> agrupa dos datos que siempre van juntos, nombre y ficha, sin ninguna lógica de juego.</li>
<li><code>private final</code> protege los atributos y obliga a asignarlos una sola vez, en el constructor.</li>
<li>Un constructor con parámetros impide crear objetos incompletos; <code>this.atributo = parametro</code> resuelve el choque de nombres.</li>
<li>Los getters permiten leer sin modificar; no se escriben setters si no hacen falta.</li>
<li>Un objeto sin forma de cambiar se llama inmutable y se puede compartir sin miedo.</li>
<li>La ficha es un <code>char</code>, el mismo tipo que las casillas, para encajar directamente con <code>Tablero</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b> Casi todos los programas tienen clases de datos como esta:
<ul>
<li><b>Una tienda</b>: <code>Producto(String codigo, String nombre, double precio)</code> con getters. Si el precio cambia, se crea un producto nuevo o se agrega un setter que valide que no sea negativo.</li>
<li><b>Un sistema escolar</b>: <code>Estudiante(String carne, String nombre)</code>; el carné, que nunca cambia, va como <code>final</code>.</li>
<li><b>Una app de mapas</b>: <code>Coordenada(double latitud, double longitud)</code>, inmutable, que se puede pasar a cien métodos sin riesgo.</li>
<li><b>Cualquier respuesta de un servicio web</b>: los datos que llegan (un usuario, un pedido) se guardan en clases de datos o en <i>records</i>.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>En <code>jshell</code>, crea tres jugadores y escribe una expresión que muestre «Ana (X) contra Luis (O)» usando solo getters.</li>
<li>Quita <code>this.</code> de L11 en una copia del archivo y compílala. Copia el mensaje de error y explica con tus palabras por qué aparece.</li>
<li>Agrega a una copia de la clase un atributo <code>private int victorias</code> (sin <code>final</code>), un getter y un método <code>sumarVictoria()</code> que le sume 1. ¿Sigue siendo inmutable la clase?</li>
<li>Agrega al constructor la validación de la ficha con <code>IllegalArgumentException</code> que viste arriba y comprueba en <code>jshell</code> que <code>new Jugador("Ana", 'Z')</code> lanza la excepción.</li>
<li>Reto: escribe la clase <code>Producto</code> con código, nombre y precio, inmutable, y un método <code>conPrecio(double nuevo)</code> que devuelva un <code>Producto</code> <b>nuevo</b> con el precio cambiado. Pista: <code>return new Producto(codigo, nombre, nuevo);</code></li>
</ol></div>
""",
}
