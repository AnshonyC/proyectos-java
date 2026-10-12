# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 39,
    "titulo": "Navegacion.java: el contrato entre pantallas",
    "antes": r"""
<p class="entrada">El Totito v1.0 tiene cinco pantallas y cada una tiene botones que llevan a otra. En este capítulo
escribes un archivo de solo 26 líneas, sin una sola instrucción ejecutable, que decide cómo se comunican todas ellas:
una <b>interfaz</b> que funciona como contrato.</p>

<h2>Por qué existe este archivo</h2>
<p>Mira las imágenes del diseño (capítulo 34). El menú tiene «Jugar», «Instrucciones» y «Salir». Las instrucciones tienen
«Regresar». La configuración tiene «Volver» y «Comenzar partida». El juego tiene «Menú principal». El resultado tiene
«Jugar de nuevo» y «Menú principal». Cada botón <b>cambia de pantalla</b>.</p>
<p>La forma ingenua de programarlo sería que cada pantalla guarde una referencia a las pantallas a las que puede ir: el
menú conoce a la configuración y a las instrucciones; la configuración conoce al juego y al menú; el juego conoce al
resultado y al menú… En poco tiempo todas se conocen entre sí. Eso se llama <b>acoplamiento</b> (capítulo 27) y trae
problemas muy concretos:</p>
<ul>
<li>Para construir el menú necesitarías antes la configuración, que necesita el juego, que necesita el resultado, que
necesita el menú… un círculo sin principio.</li>
<li>Si cambias cómo se pasa de una pantalla a otra (por ejemplo, para añadir una animación), tienes que tocar las cinco.</li>
<li>No puedes ver una pantalla suelta para revisarla (lo que hará <code>VistaPrevia</code> en el capítulo 56) sin crear
también todas las demás.</li>
</ul>
<p>La solución: <b>ninguna pantalla conoce a las otras</b>. Cada una solo conoce un «contrato», la interfaz
<code>Navegacion</code>, que dice qué se puede pedir: «quiero ir al menú», «quiero empezar una partida con estos
jugadores», «quiero salir». Quién atiende esos pedidos y cómo lo hace es asunto de una sola clase,
<code>PanelPrincipal</code> (capítulo 61), que <i>implementa</i> el contrato.</p>

<svg viewBox="0 0 720 300" width="100%">
<rect x="0" y="0" width="720" height="300" fill="#1C1740"/>
<text x="160" y="22" fill="#FF3BD4" font-size="14" text-anchor="middle" font-family="sans-serif">Sin interfaz: todas se conocen</text>
<g stroke="#FF3BD4" stroke-width="1.5" stroke-opacity="0.6">
<line x1="160" y1="70" x2="255" y2="139"/><line x1="160" y1="70" x2="219" y2="251"/>
<line x1="160" y1="70" x2="101" y2="251"/><line x1="160" y1="70" x2="65" y2="139"/>
<line x1="255" y1="139" x2="219" y2="251"/><line x1="255" y1="139" x2="101" y2="251"/>
<line x1="255" y1="139" x2="65" y2="139"/><line x1="219" y1="251" x2="101" y2="251"/>
<line x1="219" y1="251" x2="65" y2="139"/><line x1="101" y1="251" x2="65" y2="139"/>
</g>
<g fill="#2B2363" stroke="#C8BCF6" stroke-width="1.5">
<rect x="115" y="56" width="90" height="28" rx="8"/><rect x="210" y="125" width="90" height="28" rx="8"/>
<rect x="174" y="237" width="90" height="28" rx="8"/><rect x="56" y="237" width="90" height="28" rx="8"/>
<rect x="20" y="125" width="90" height="28" rx="8"/>
</g>
<g fill="#FFFFFF" font-size="12" text-anchor="middle" font-family="sans-serif">
<text x="160" y="74">Menú</text><text x="255" y="143">Instrucciones</text><text x="219" y="255">Configuración</text>
<text x="101" y="255">Juego</text><text x="65" y="143">Resultado</text>
</g>
<line x1="350" y1="30" x2="350" y2="280" stroke="#A05CFF" stroke-width="1" stroke-dasharray="4 4"/>
<text x="535" y="22" fill="#2F84FF" font-size="14" text-anchor="middle" font-family="sans-serif">Con la interfaz Navegacion</text>
<g stroke="#2F84FF" stroke-width="1.5">
<line x1="385" y1="68" x2="535" y2="135"/><line x1="460" y1="68" x2="535" y2="135"/>
<line x1="535" y1="68" x2="535" y2="135"/><line x1="610" y1="68" x2="535" y2="135"/>
<line x1="685" y1="68" x2="535" y2="135"/>
</g>
<g fill="#2B2363" stroke="#C8BCF6" stroke-width="1.5">
<rect x="352" y="40" width="66" height="28" rx="8"/><rect x="427" y="40" width="66" height="28" rx="8"/>
<rect x="502" y="40" width="66" height="28" rx="8"/><rect x="577" y="40" width="66" height="28" rx="8"/>
<rect x="652" y="40" width="66" height="28" rx="8"/>
</g>
<g fill="#FFFFFF" font-size="10" text-anchor="middle" font-family="sans-serif">
<text x="385" y="58">Menú</text><text x="460" y="58">Instruc.</text><text x="535" y="58">Config.</text>
<text x="610" y="58">Juego</text><text x="685" y="58">Resultado</text>
</g>
<rect x="455" y="135" width="160" height="32" rx="8" fill="#1C1740" stroke="#2F84FF" stroke-width="2"/>
<text x="535" y="156" fill="#2F84FF" font-size="13" text-anchor="middle" font-family="sans-serif">«interfaz» Navegacion</text>
<line x1="535" y1="167" x2="535" y2="230" stroke="#A05CFF" stroke-width="1.5" stroke-dasharray="5 4"/>
<text x="545" y="203" fill="#A05CFF" font-size="11" font-family="sans-serif">implementa</text>
<rect x="465" y="230" width="140" height="32" rx="8" fill="#2B2363" stroke="#A05CFF" stroke-width="2"/>
<text x="535" y="251" fill="#FFFFFF" font-size="13" text-anchor="middle" font-family="sans-serif">PanelPrincipal</text>
</svg>
<p>A la izquierda, cinco pantallas con diez relaciones cruzadas. A la derecha, cinco pantallas que solo dependen de
<code>Navegacion</code>, y una sola clase que sabe cambiar de pantalla.</p>
<p>Una comparación de la vida diaria: en un restaurante, el cliente no entra a la cocina a buscar al cocinero; le dice al
mesero «quiero la cuenta» o «tráigame el postre». El menú de cosas que puedes pedir es el <b>contrato</b>; el mesero lo
<b>implementa</b>. Si mañana cambian al mesero, o la cocina se reorganiza, el cliente sigue pidiendo igual.</p>

<h2>Repaso exprés: qué es una interfaz</h2>
<p>Lo viste a fondo en el capítulo 24. En resumen:</p>
<ul>
<li>Una <code>interface</code> es una lista de métodos <b>sin cuerpo</b>: dice <i>qué</i> se puede hacer, no <i>cómo</i>.</li>
<li>Una clase la cumple con <code>implements</code>: <code>class PanelPrincipal extends JPanel implements Navegacion</code>.
Desde ese momento el compilador la obliga a escribir <b>todos</b> los métodos de la interfaz, cada uno marcado con
<code>@Override</code>.</li>
<li>Una variable puede tener como tipo una interfaz: <code>Navegacion navegacion</code>. Puede guardar cualquier objeto
cuya clase la implemente, y al llamar <code>navegacion.irAlMenu()</code> se ejecuta el método de la clase real de ese
objeto (enlace dinámico, capítulo 23).</li>
<li>No se puede hacer <code>new Navegacion()</code> a secas: un contrato no es un objeto; hace falta alguien que lo cumpla.</li>
</ul>

<h2>Qué vas a aprender</h2>
<ul>
<li>A diseñar una interfaz a partir de lo que necesitan sus usuarios (las pantallas), no de cómo se va a implementar.</li>
<li>Por qué los métodos de una interfaz no llevan <code>public</code> ni llaves.</li>
<li>Cómo se pasan datos a través del contrato (<code>iniciarPartida</code> con jugadores y modo).</li>
<li>Qué es la <b>inversión de dependencias</b>: las pantallas dependen de una abstracción, no de otra clase concreta.</li>
<li>Por qué esto permite tener una navegación «de mentira» para probar pantallas sueltas.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>Comprueba que sigues en la rama <code>interfaz-neon</code> (<code>git branch</code>).</li>
<li>En NetBeans: clic derecho en <i>Source Packages → &lt;default package&gt;</i> → <i>New → Java Interface…</i>
(si no aparece en la lista corta, está en <i>New → Other… → Java → Java Interface</i>).</li>
<li>Nombre: <code>Navegacion</code>, sin tilde (los nombres de clases e interfaces del proyecto no llevan tildes ni
eñes, para evitar problemas de codificación en archivos y en Git). <i>Finish</i>.</li>
<li>Borra la plantilla y escribe el código de abajo.</li>
</ol>
<p>Con PowerShell:</p>
<pre class="ps">New-Item src\Navegacion.java</pre>
<div class="caja concepto"><b>El orden de los capítulos importa.</b> <code>Navegacion</code> menciona a
<code>Jugador</code> y a <code>Partida</code> (con su <code>Partida.Modo</code>). Por eso llega justo después de
<code>Partida</code>: si la escribieras antes, el proyecto no compilaría.</div>
""",
    "archivos": [
        {"ruta": "src/Navegacion.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1–L7</b> Comentario de documentación. L2–L3 enumeran lo que una pantalla puede pedir y quién lo cumple
(<code>PanelPrincipal</code>). L5–L6 explican el <b>porqué</b>: «ninguna pantalla conoce a las demás». Dejar escrito el
motivo de una decisión de diseño es tan importante como el código: evita que alguien, más adelante, «simplifique»
haciendo que una pantalla llame directo a otra.</p>
<p class="l"><b>L8</b> <code>public interface Navegacion</code>: declara una interfaz pública (se usa desde todas las
pantallas). La palabra <code>interface</code> ocupa el lugar de <code>class</code>. El archivo, como con las clases, debe
llamarse igual: <code>Navegacion.java</code>. Fíjate en que no hay <code>import</code>: <code>Jugador</code> y
<code>Partida</code> están en el mismo «paquete por defecto» (<i>default package</i>), así que se ven sin importarlos.</p>
"""),
             ("void irAlMenu", r"""
<p class="l"><b>L10</b> Primer método del contrato: «llévame al menú». Tres detalles que lo distinguen de un método de
clase:</p>
<ul>
<li>No lleva <code>public</code>: en una interfaz, todos los métodos son públicos automáticamente. Escribirlo no sería un
error, pero es redundante.</li>
<li>No lleva <code>abstract</code>, aunque lo es: un método de interfaz sin cuerpo es abstracto por definición.</li>
<li>Termina en <code>;</code> en lugar de llaves con código: solo se declara la <b>firma</b> (tipo de retorno, nombre y
parámetros). El cuerpo lo escribirá <code>PanelPrincipal</code>.</li>
</ul>
<p class="l">Es <code>void</code> porque quien lo pide no espera respuesta: pide el cambio y listo. Lo usan
<code>PantallaInstrucciones</code> («Regresar»), <code>PantallaConfiguracion</code> («Volver»),
<code>PantallaJuego</code> y <code>PantallaResultado</code> («Menú principal»).</p>
<p class="l"><b>L12</b> «Llévame a las instrucciones». Lo pide el botón «Instrucciones» del menú. El nombre empieza con un
verbo en infinitivo (<code>ir</code>), como todos los del contrato: un método es una acción.</p>
<p class="l"><b>L14</b> «Llévame a la configuración». Lo pide el botón «Jugar» del menú: antes de jugar hay que escribir
los nombres y elegir modo.</p>
<p class="l">Las líneas en blanco entre métodos (L11, L13, L15) solo dan aire para leer.</p>
"""),
             ("void iniciarPartida", r"""
<p class="l"><b>L16</b> Comentario: este método no solo cambia de pantalla, también <b>crea una partida nueva</b> con el
marcador en cero.</p>
<p class="l"><b>L17</b> El único método que transporta datos hacia adentro: los dos jugadores (con los nombres y fichas
escritos en la configuración) y el modo elegido. <code>Partida.Modo</code> es el enum anidado del capítulo 38; se escribe
con el nombre de la clase delante porque está declarado dentro de <code>Partida</code>. Lo llama el botón «Comenzar
partida» de <code>PantallaConfiguracion</code> (capítulo 58). La configuración no crea la <code>Partida</code> ella
misma: solo entrega los ingredientes. Quién la crea y dónde la guarda es decisión de <code>PanelPrincipal</code>, que la
necesitará para «Jugar de nuevo».</p>
"""),
             ("void mostrarResultado", r"""
<p class="l"><b>L19</b> Comentario: pantalla de victoria o de empate.</p>
<p class="l"><b>L20</b> La pantalla de juego lo llama cuando la partida terminó, pasando la partida para que la pantalla
de resultado sepa quién ganó, cómo quedó el tablero y si el ganador es la computadora. Fíjate en que el tipo del
parámetro es <code>Partida</code>, una clase que no tiene nada de Swing: las pantallas se pasan entre sí <b>datos del
modelo</b>, no componentes visuales.</p>
"""),
             ("void jugarDeNuevo", r"""
<p class="l"><b>L22–L23</b> «Otra partida con los mismos jugadores, conservando el marcador». Por eso no recibe
parámetros: <code>PanelPrincipal</code> ya tiene guardada la partida y le basta con llamar a su
<code>reiniciar()</code> (capítulo 38). Compáralo con <code>iniciarPartida</code>: dos métodos distintos para dos
intenciones distintas, «empezar de cero» y «la revancha».</p>
<p class="l"><b>L25</b> «Cierra el juego». Lo piden el botón «Salir» del menú y la X del encabezado (capítulo 45). Las
pantallas no llaman a <code>System.exit</code> ni cierran la ventana: ni siquiera saben que existe una ventana. Lo que
pase al salir lo decide quien implementa el contrato.</p>
<p class="l"><b>L26</b> Cierra la interfaz. Siete métodos, ningún atributo, ninguna línea que «haga» algo, y sin embargo
este archivo ordena la arquitectura completa del juego.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<p>Una interfaz no se ejecuta: se cumple. Para ver el mecanismo completo hay que adelantar un poco de los capítulos 56 y
61. No los escribas todavía; solo míralos.</p>
<p>Así recibe una pantalla el contrato (simplificado de <code>PantallaMenu</code>, capítulo 56):</p>
<pre class="java">public PantallaMenu(Navegacion navegacion) {
    ...
    jugar.addActionListener(e -&gt; navegacion.irAConfiguracion());
    salir.addActionListener(e -&gt; navegacion.salir());
}</pre>
<p>Y así lo cumple <code>PanelPrincipal</code> (capítulo 61):</p>
<pre class="java">public class PanelPrincipal extends JPanel implements Navegacion {
    ...
    add(new PantallaMenu(this), MENU);    // "this" es un PanelPrincipal, que ES una Navegacion
    ...
    @Override
    public void irAConfiguracion() {
        cartas.show(this, CONFIGURACION);  // CardLayout muestra la "carta" de la configuración
    }
}</pre>
<p>Sigamos el clic en «Jugar», paso a paso:</p>
<ol>
<li>Al arrancar, <code>PanelPrincipal</code> crea el menú con <code>new PantallaMenu(this)</code>. El parámetro
<code>navegacion</code> del menú queda apuntando al objeto <code>PanelPrincipal</code>. El menú lo ve solo como «una
<code>Navegacion</code>»; no sabe que en realidad es un panel con un <code>CardLayout</code>.</li>
<li>El usuario pulsa «Jugar». Swing ejecuta la lambda del botón: <code>navegacion.irAConfiguracion()</code>.</li>
<li>Java mira la clase real del objeto (<code>PanelPrincipal</code>) y ejecuta <b>su</b> <code>irAConfiguracion()</code>:
enlace dinámico.</li>
<li><code>cartas.show(this, "configuracion")</code> oculta el menú y muestra la configuración.</li>
</ol>
<p>Este es el mapa completo de quién pide qué:</p>
<table class="tabla">
<tr><th>Pantalla</th><th>Botón</th><th>Pide</th></tr>
<tr><td>Menú (cap. 56)</td><td>Jugar · Instrucciones · Salir</td><td><code>irAConfiguracion()</code> · <code>irAInstrucciones()</code> · <code>salir()</code></td></tr>
<tr><td>Instrucciones (cap. 57)</td><td>Regresar</td><td><code>irAlMenu()</code></td></tr>
<tr><td>Configuración (cap. 58)</td><td>Volver · Comenzar partida</td><td><code>irAlMenu()</code> · <code>iniciarPartida(j1, j2, modo)</code></td></tr>
<tr><td>Juego (cap. 59)</td><td>Menú principal · (fin de la partida)</td><td><code>irAlMenu()</code> · <code>mostrarResultado(partida)</code></td></tr>
<tr><td>Resultado (cap. 60)</td><td>Jugar de nuevo · Menú principal</td><td><code>jugarDeNuevo()</code> · <code>irAlMenu()</code></td></tr>
<tr><td>Todas (encabezado, cap. 45 y 55)</td><td>La X de cerrar</td><td><code>salir()</code></td></tr>
</table>
<p>Y aquí está el premio del diseño: en el capítulo 56, <code>VistaPrevia</code> mostrará <b>una sola</b> pantalla
pasándole una navegación «de mentira», una clase anónima (capítulo 25) en la que cada método existe pero no hace nada.
La pantalla no nota la diferencia, porque solo conoce el contrato. Esto tiene nombre: <b>inversión de dependencias</b>.
Las piezas de detalle (las pantallas) no dependen de otra pieza de detalle (el panel con cartas), sino de una abstracción
(la interfaz), y cualquiera que la cumpla sirve.</p>

<h2>Compila y prueba</h2>
<p>Una interfaz no tiene nada que ejecutar. La prueba es que compile: <i>Run → Clean and Build Project</i> (Shift+F11) y
<code>BUILD SUCCESS</code> en la ventana <i>Output</i>. Con PowerShell:</p>
<pre class="ps">javac -encoding UTF-8 -d out src\*.java</pre>

<h3>Prueba opcional: cumplir el contrato desde la consola</h3>
<p>Para sentir cómo funciona una interfaz, crea un archivo temporal en la carpeta raíz del proyecto (no en
<code>src</code>) con una <code>Navegacion</code> que, en vez de cambiar de pantalla, escribe en la consola:</p>
<pre class="ps">New-Item ProbarNavegacion.java</pre>
<pre class="java">public class ProbarNavegacion {

    /** Una Navegacion que solo escribe en la consola lo que le piden. */
    static class NavegacionDeConsola implements Navegacion {
        @Override public void irAlMenu() { System.out.println("-&gt; ir al menu"); }
        @Override public void irAInstrucciones() { System.out.println("-&gt; ir a instrucciones"); }
        @Override public void irAConfiguracion() { System.out.println("-&gt; ir a configuracion"); }
        @Override public void iniciarPartida(Jugador j1, Jugador j2, Partida.Modo modo) {
            System.out.println("-&gt; partida: " + j1.getNombre() + " vs " + j2.getNombre() + " (" + modo + ")");
        }
        @Override public void mostrarResultado(Partida partida) { System.out.println("-&gt; resultado: " + partida.getEstado()); }
        @Override public void jugarDeNuevo() { System.out.println("-&gt; jugar de nuevo"); }
        @Override public void salir() { System.out.println("-&gt; salir"); }
    }

    /** Hace de "pantalla de menu": solo conoce la interfaz Navegacion. */
    static void pulsarBotonesDelMenu(Navegacion navegacion) {
        navegacion.irAConfiguracion();
        navegacion.irAInstrucciones();
        navegacion.salir();
    }

    public static void main(String[] args) {
        Navegacion navegacion = new NavegacionDeConsola();
        pulsarBotonesDelMenu(navegacion);
        navegacion.iniciarPartida(new Jugador("Ana", 'X'), new Jugador("Beto", 'O'), Partida.Modo.DOS_JUGADORES);
    }
}</pre>
<p>Tras un <i>Clean and Build</i>:</p>
<pre class="ps">java -cp target\classes ProbarNavegacion.java</pre>
<pre class="salida">-&gt; ir a configuracion
-&gt; ir a instrucciones
-&gt; salir
-&gt; partida: Ana vs Beto (DOS_JUGADORES)</pre>
<p><code>pulsarBotonesDelMenu</code> es igual que el menú real: recibe «alguna» <code>Navegacion</code> y le pide cosas.
Con <code>PanelPrincipal</code> cambiaría de pantalla; con esta clase, escribe texto. Ahora borra la línea de
<code>salir()</code> dentro de <code>NavegacionDeConsola</code> y vuelve a ejecutarlo: el compilador protesta porque el
contrato no se cumple completo.</p>
<pre class="salida">error: NavegacionDeConsola is not abstract and does not override abstract method salir() in Navegacion</pre>
<p>Ese error es la interfaz haciendo su trabajo. Al terminar, borra el archivo:</p>
<pre class="ps">Remove-Item ProbarNavegacion.java</pre>

<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Mensaje</th><th>Causa y solución</th></tr>
<tr><td><code>interface abstract methods cannot have body</code></td><td>Pusiste llaves <code>{ }</code> en lugar de <code>;</code> al final de un método. En la interfaz solo va la firma.</td></tr>
<tr><td><code>cannot find symbol: class Partida</code></td><td>Falta <code>Partida.java</code> (capítulo 38) o tiene otro nombre.</td></tr>
<tr><td><code>cannot find symbol: class Modo</code></td><td>Escribiste <code>Modo modo</code> en vez de <code>Partida.Modo modo</code>. Fuera de <code>Partida</code>, el enum lleva el nombre de la clase delante.</td></tr>
</table>

<div class="caja git"><b>Git</b> Segundo commit de la rama. Como en el capítulo anterior usaste <code>-u</code>, ahora
basta <code>git push</code>.
<pre class="ps">git status
git add src\Navegacion.java
git commit -m "Navegacion: contrato entre pantallas"
git push</pre>
Con <code>git log --oneline -3</code> verás tus dos commits de la rama encima del último de <code>main</code>.</div>

<h2>Resumen</h2>
<ul>
<li><code>Navegacion</code> es una interfaz: siete métodos sin cuerpo que dicen qué puede pedir una pantalla.</li>
<li>En una interfaz los métodos son públicos y abstractos sin escribirlo, y terminan en <code>;</code>.</li>
<li>Las pantallas reciben una <code>Navegacion</code> y la llaman; ninguna conoce a las demás.</li>
<li><code>PanelPrincipal</code> (capítulo 61) la implementa con <code>implements Navegacion</code> y un <code>CardLayout</code>.</li>
<li><code>iniciarPartida</code> y <code>mostrarResultado</code> pasan datos del modelo (jugadores, modo, partida), nunca componentes visuales.</li>
<li>Gracias al contrato se puede probar una pantalla suelta con una navegación «de mentira» (capítulo 56).</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b> Cada vez que varias piezas necesitan «pedirle algo» a un
coordinador, define primero el contrato:
<ul>
<li><b>Un asistente de instalación</b> (Siguiente, Atrás, Cancelar): cada paso recibe un <code>NavegadorAsistente</code> con <code>siguiente()</code>, <code>anterior()</code> y <code>cancelar()</code>, sin conocer los otros pasos.</li>
<li><b>Una app de tienda</b> con catálogo, carrito y pago: el catálogo pide <code>irAlCarrito()</code> y no sabe si el carrito es una pantalla, una ventana emergente o una página web.</li>
<li><b>Un sistema de avisos</b>: una interfaz <code>Notificador</code> con <code>enviar(mensaje)</code> que pueden cumplir una clase de correo, otra de WhatsApp y otra «de mentira» que imprime en consola para las pruebas.</li>
<li><b>Videojuegos</b>: los niveles piden <code>terminarNivel(puntos)</code> o <code>volverAlMenu()</code> a un gestor de escenas.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Sin mirar el capítulo, escribe de memoria los siete métodos de <code>Navegacion</code> y qué pantalla llama a cada uno.</li>
<li>En <code>ProbarNavegacion.java</code>, escribe un método <code>pulsarBotonesDelResultado(Navegacion n)</code> que haga
lo que hacen los dos botones de la pantalla de resultado, y ejecútalo.</li>
<li>Imagina que el diseño agrega una pantalla de «Créditos» accesible desde el menú. ¿Qué método agregarías a la
interfaz? ¿Qué clases dejarían de compilar hasta que lo implementen? Pista: todas las que dicen
<code>implements Navegacion</code>.</li>
<li>Convierte <code>NavegacionDeConsola</code> en una clase anónima (capítulo 25): <code>Navegacion n = new Navegacion() { ... };</code>.
Es exactamente lo que hará <code>VistaPrevia</code>.</li>
<li>Reto: diseña en papel una interfaz <code>Reproductor</code> para una app de música (qué métodos, qué parámetros,
qué devuelve cada uno) y dos clases que podrían implementarla.</li>
</ol></div>
""",
}
