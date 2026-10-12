CAPITULO = {
    "numero": 58,
    "titulo": "PantallaConfiguracion.java: jugadores, símbolos y modo",
    "antes": r"""<p class="entrada">Antes de jugar hay que saber quién juega, con qué ficha y contra quién. Esta pantalla lo
pregunta, guarda las respuestas en los componentes de los capítulos 49 a 51 y, al pulsar «Comenzar partida», las
convierte en dos objetos <code>Jugador</code> y un <code>Partida.Modo</code>. Es el puente entre lo que el usuario
elige con el ratón y los datos con los que trabaja la lógica.</p>

<h2>Por qué existe este archivo</h2>
<p>En la versión v0.1 (capítulo 33) todo estaba fijo: tú eras la X, la IA era la O, y no había nombres. El diseño de la
versión neón trae una pantalla de configuración con tres secciones: <b>JUGADORES</b> (dos tarjetas para escribir
nombres), <b>SÍMBOLOS</b> (elegir X u O) y <b>MODO DE JUEGO</b>. Esa pantalla es <code>PantallaConfiguracion</code>.</p>
<figure><img src="diseno/configuracion.jpg"><figcaption>El diseño de la configuración. Trae un solo modo de juego,
«2 jugadores».</figcaption></figure>
<p>El diseño solo trae el modo «2 jugadores». Pero el proyecto ya tenía una IA que nunca pierde (la del capítulo 31) y
sería una pena tirarla. Por eso el código agrega una segunda opción, «Contra la IA», junto a la primera. Es una decisión
de diseño que conviene anotar (y el comentario del archivo la anota): cuando te apartas del boceto, deja escrito
por qué.</p>
<p>Esta clase tiene dos responsabilidades, y ninguna más:</p>
<ol>
<li><b>Mostrar</b> las preguntas en el orden del diseño.</li>
<li><b>Traducir</b> las respuestas a objetos de la lógica cuando el usuario pulsa «Comenzar partida», y entregárselas
a la <code>Navegacion</code>.</li>
</ol>
<p>Lo que <b>no</b> hace: no crea la <code>Partida</code> (eso lo hace <code>PanelPrincipal</code>, capítulo 61), no
dibuja nada a mano (cada componente se dibuja solo) y no sabe nada de turnos ni de reglas.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>Por qué este archivo <b>no tiene ni un <code>import</code></b>.</li>
<li>Cuándo un componente se guarda en un <b>atributo</b> (y no en una variable local): cuando hay que consultarlo
<b>después</b> de que el constructor terminó.</li>
<li>Atributos <code>final</code> que se asignan en el constructor, y uno que no es <code>final</code> porque cambia.</li>
<li>Dos clases de lambdas: <code>() -&gt; …</code> (un <code>Runnable</code>, sin datos) y <code>e -&gt; …</code> (un
<code>ActionListener</code>, que recibe el evento).</li>
<li>Una <b>única fuente de verdad</b>: el atributo <code>modo</code> decide, y la apariencia se deriva de él.</li>
<li>Cómo pasar expresiones <code>boolean</code> (<code>a == b</code>) directamente como argumentos.</li>
<li>El operador ternario para calcular la ficha contraria.</li>
<li>Usar la vista previa con un pequeño truco para ver en la consola lo que la pantalla entrega.</li>
</ul>

<h2>Créalo</h2>
<p>Comprueba que sigues en la rama <code>interfaz-neon</code> (<code>git branch --show-current</code>). En NetBeans: clic
derecho en <i>Source Packages → &lt;default package&gt;</i> → <i>New → Java Class…</i> → <i>Class Name</i>:
<code>PantallaConfiguracion</code> → <i>Finish</i>. Borra la plantilla y escribe el código. Con PowerShell:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
New-Item src\PantallaConfiguracion.java
notepad src\PantallaConfiguracion.java</pre>
<p>Necesitas los componentes de los capítulos anteriores: <code>TarjetaJugador</code> (49), <code>SelectorSimbolo</code>
(50), <code>OpcionModo</code> (51), <code>Rotulo</code> (46), <code>BotonNeon</code> (44), <code>Iconos</code> (42) y,
por supuesto, <code>Partida</code> (38) y <code>Jugador</code> (30).</p>
""",
    "archivos": [
        {"ruta": "src/PantallaConfiguracion.java",
         "bloques": [
             (None, r"""<p class="l"><b>L1–L7</b> El comentario de documentación. Las líneas 2–3 dicen qué es la pantalla;
las 5–6 explican la decisión de diseño de agregar «Contra la IA». Ese tipo de comentario es el más valioso: el código
dice <i>qué</i> hace, pero no puede decir <i>por qué</i> se apartó del boceto.</p>
<p class="l">Fíjate en lo que falta antes del comentario: <b>no hay ningún <code>import</code></b>. ¿Cómo es posible, si
esta clase usa botones, rótulos y tarjetas? Porque todas las clases que nombra (<code>TarjetaJugador</code>,
<code>BotonNeon</code>, <code>Tema</code>, <code>Iconos</code>, <code>Partida</code>, <code>Jugador</code>…) son
<b>tuyas</b> y están en el mismo paquete. Las clases de Swing (<code>JButton</code>, <code>BoxLayout</code>…) se
usan, pero escondidas dentro de esos componentes y de <code>PantallaBase</code>; este archivo nunca escribe su nombre.
Es una señal de buen diseño: la pantalla habla el «idioma del Totito», no el de Swing.</p>
<p class="l"><b>L8</b> La clase hereda de <code>PantallaBase</code>, igual que el menú y las instrucciones: fondo,
encabezado y los métodos <code>agregar</code>, <code>espacio</code>, <code>relleno</code> y <code>fila</code> vienen de
regalo.</p>
<p class="l"><b>L9</b> En blanco.</p>"""),
             ("private static final int ANCHO_SECCION", r"""<p class="l"><b>L10</b> El ancho (560 píxeles) de los tres títulos de
sección, con sus líneas que se desvanecen a los lados. Es una constante (<code>private static final</code>, capítulo 20)
porque se usa tres veces y las tres deben coincidir; si fueran distintas, las líneas decorativas no quedarían
alineadas.</p>
<p class="l"><b>L11</b> En blanco.</p>"""),
             ("private final Navegacion navegacion;", r"""<p class="l"><b>L12</b> Un <b>atributo</b> para la navegación. En
<code>PantallaInstrucciones</code> (capítulo 57) no hacía falta, porque solo se usaba dentro del constructor. Aquí sí:
el método <code>comenzar()</code> (L61) la necesita cuando el usuario pulsa el botón, mucho después de que el constructor
terminó. Regla práctica: <b>si algo se usa fuera del constructor, se guarda en un atributo</b>.</p>
<p class="l"><b>L13–L14</b> Las dos tarjetas donde se escriben los nombres. Son atributos porque al final hay que
<b>leer</b> lo que el usuario escribió en ellas (<code>getNombre()</code>), y porque <code>elegirModo</code> convierte la
segunda en «Computadora».</p>
<p class="l"><b>L15</b> El selector X/O del capítulo 50. Atributo porque <code>comenzar()</code> le preguntará qué ficha
eligió el Jugador 1.</p>
<p class="l"><b>L16–L17</b> Las dos opciones de modo. Atributos porque <code>elegirModo</code> tiene que marcar una y
desmarcar la otra cada vez.</p>
<p class="l">Todos estos son <code>final</code>: se asignan una vez, en el constructor, y la referencia no cambia nunca
(la pantalla siempre tiene las mismas dos tarjetas). Un atributo <code>final</code> sin valor en su declaración se
llama «final en blanco»: Java exige que el constructor le dé valor exactamente una vez, y si olvidas uno, no compila
(<code>variable jugador1 might not have been initialized</code>). Es una red de seguridad gratis.</p>
<p class="l"><b>L18</b> <code>private Partida.Modo modo;</code> guarda el modo elegido. Su tipo es el <code>enum</code>
<code>Modo</code> que vive <b>dentro</b> de <code>Partida</code> (capítulo 38), por eso se escribe
<code>Partida.Modo</code>. Este <b>no</b> es <code>final</code>: cambia cada vez que el usuario pulsa una opción.</p>
<p class="l"><b>L19</b> En blanco.</p>"""),
             ("public PantallaConfiguracion(", r"""<p class="l"><b>L20</b> El constructor recibe la navegación, como todas
las pantallas.</p>
<p class="l"><b>L21</b> <code>super(navegacion);</code> construye primero la parte heredada (siempre la primera
instrucción; capítulo 57).</p>
<p class="l"><b>L22</b> <code>this.navegacion = navegacion;</code> copia el parámetro al atributo. Las dos variables se
llaman igual; <code>this.navegacion</code> es «el atributo de este objeto» y <code>navegacion</code> a secas es el
parámetro (capítulo 20). Si escribieras <code>navegacion = navegacion;</code>, asignarías el parámetro a sí mismo, el
atributo quedaría sin valor y, por ser <code>final</code>, el compilador te avisaría.</p>
<p class="l"><b>L23</b> En blanco.</p>"""),
             ("jugador1 = new TarjetaJugador", r"""<p class="l"><b>L24</b> Crea la tarjeta del Jugador 1 con su título y el
color <code>Tema.FRESA</code> (el rosa rojizo del diseño, capítulo 40). Como el atributo es <code>final</code>, esta es
la única asignación que tendrá.</p>
<p class="l"><b>L25</b> La tarjeta del Jugador 2, en azul.</p>
<p class="l"><b>L26</b> El selector de símbolo. Empieza con la X marcada para el Jugador 1 (así lo programaste en el
capítulo 50).</p>"""),
             ("opcionDosJugadores = new OpcionModo", r"""<p class="l"><b>L27</b> La opción «2 jugadores»: icono de dos
personas, título y una descripción corta.</p>
<p class="l"><b>L28</b> La opción «Contra la IA», con el icono de la computadora y la frase «La computadora usa
Minimax», para que quede claro que no es una IA cualquiera.</p>
<p class="l"><b>L29</b> <code>setAlSeleccionar</code> (capítulo 51) recibe un <code>Runnable</code>: «algo que se puede
ejecutar», una acción sin datos de entrada ni de salida. La lambda <code>() -&gt; elegirModo(Partida.Modo.DOS_JUGADORES)</code>
tiene los paréntesis <b>vacíos</b> porque <code>Runnable</code> no recibe nada; compárala con <code>e -&gt; …</code> de los
botones, que sí reciben el evento. La <code>OpcionModo</code> no decide nada: solo avisa «me pulsaron» y es la pantalla
la que decide qué significa eso. Así el mismo componente sirve para cualquier lista de opciones.</p>
<p class="l"><b>L30</b> Lo mismo para la otra opción, con <code>CONTRA_IA</code>.</p>
<p class="l"><b>L31</b> En blanco.</p>"""),
             ("BotonNeon comenzar", r"""<p class="l"><b>L32</b> El botón principal: píldora de 440 × 66 píxeles, degradado de rosa
a morado, icono de «play». Es el más grande y el más colorido de la pantalla porque es la acción principal (capítulo 34:
jerarquía visual).</p>
<p class="l"><b>L33</b> Al pulsarlo se llama a <code>comenzar()</code>, el método privado de la L61. La lambda no hace el
trabajo ella misma: delega en un método con nombre. Así la línea se lee sola y el método se puede explicar aparte.</p>
<p class="l"><b>L34</b> «Volver»: un botón de contorno (sin relleno), más pequeño. Es la acción secundaria y por eso se
ve más discreta.</p>
<p class="l"><b>L35</b> Vuelve al menú. Aquí la lambda usa el parámetro <code>navegacion</code>; también funcionaría con
<code>this.navegacion</code>, porque ambos apuntan al mismo objeto.</p>
<p class="l"><b>L36</b> En blanco.</p>"""),
             ("relleno();", r"""<p class="l"><b>L37</b> Resorte de arriba (centra el conjunto en vertical, capítulo 57).</p>
<p class="l"><b>L38</b> El título de sección «JUGADORES» (capítulo 46: <code>Rotulo.seccion</code> escribe el texto con las letras
separadas y líneas a los lados). El segundo argumento, <code>null</code>, significa «sin subtítulo».</p>
<p class="l"><b>L39</b> <code>fila(8, jugador1, jugador2)</code> es el método de <code>PantallaBase</code> que pone
componentes <b>uno al lado del otro</b>, con 8 píxeles de hueco. Recibe la cantidad de componentes que quieras gracias a
los <code>...</code> de su declaración (parámetros variables, capítulo 55). Devuelve un panel, y ese panel se agrega.</p>
<p class="l"><b>L40</b> 2 píxeles de separación. Es poco porque las tarjetas ya traen un margen de 10 para su halo.</p>
<p class="l"><b>L41</b> «SÍMBOLOS» con el subtítulo «Cada jugador elige su símbolo».</p>
<p class="l"><b>L42</b> El selector X/O.</p>
<p class="l"><b>L43</b> 4 píxeles de aire.</p>"""),
             ("agregar(Rotulo.seccion(\"MODO DE JUEGO\"", r"""<p class="l"><b>L44</b> «MODO DE JUEGO».</p>
<p class="l"><b>L45</b> Las dos opciones lado a lado, con 6 píxeles entre ellas.</p>
<p class="l"><b>L46</b> 4 píxeles antes de los botones.</p>
<p class="l"><b>L47–L48</b> «Comenzar partida» y, debajo, «Volver». No hay <code>espacio()</code> entre ellos: los botones
traen un margen de 9 píxeles para su halo (capítulo 44) que ya los separa.</p>
<p class="l"><b>L49</b> Resorte de abajo. El orden de estas trece líneas (L37–L49) es <b>exactamente</b> el orden del
diseño, de arriba abajo. Si quieres mover una sección, mueves sus líneas.</p>
<p class="l"><b>L50</b> En blanco.</p>"""),
             ("elegirModo(Partida.Modo.DOS_JUGADORES);", r"""<p class="l"><b>L51</b> Deja elegido el modo «2 jugadores» al
abrir la pantalla. Sin esta línea, <code>modo</code> valdría <code>null</code> (el valor por defecto de un atributo de
tipo objeto), ninguna opción se vería marcada, y si el usuario pulsara «Comenzar partida» sin tocar nada, se crearía
una partida con modo <code>null</code>. Se llama a <code>elegirModo</code> y no se asigna <code>modo</code> a mano para
que también se marque la opción visualmente: un solo método mantiene todo en orden.</p>
<p class="l">¿Por qué al <b>final</b> del constructor? Porque <code>elegirModo</code> usa <code>opcionDosJugadores</code>,
<code>opcionContraIA</code> y <code>jugador2</code>. Si la pusieras antes de la L24, esos atributos todavía serían
<code>null</code> y el programa fallaría con un <code>NullPointerException</code> al abrir.</p>
<p class="l"><b>L52</b> Cierra el constructor. <b>L53</b> En blanco.</p>"""),
             ("private void elegirModo", r"""<p class="l"><b>L54</b> Método privado que cambia el modo. Recibe el modo nuevo;
<code>void</code> porque no devuelve nada, solo cambia cosas.</p>
<p class="l"><b>L55</b> Guarda el modo en el atributo. Este es el <b>dato</b>; todo lo demás es apariencia que se deriva
de él.</p>
<p class="l"><b>L56</b> <code>nuevoModo == Partida.Modo.DOS_JUGADORES</code> es una expresión que vale <code>true</code> o
<code>false</code>, y ese valor se pasa directamente a <code>setSeleccionada</code>. Es lo mismo que escribir un
<code>if</code> con dos ramas, pero en una línea. Los valores de un <code>enum</code> se comparan con <code>==</code>
sin problema, porque cada constante existe una sola vez en memoria (capítulo 26).</p>
<p class="l"><b>L57</b> Lo mismo para la otra opción. Como las dos comparaciones son opuestas, siempre queda
<b>exactamente una</b> marcada; es imposible que queden las dos encendidas o las dos apagadas.</p>
<p class="l"><b>L58</b> Si el modo es contra la IA, la tarjeta del Jugador 2 se convierte en la de la computadora
(capítulo 49: guarda lo que hubieras escrito, pone «Computadora» y bloquea el campo); si no, vuelve a ser humana y te
devuelve tu texto.</p>
<p class="l"><b>L59–L60</b> Cierre y línea en blanco.</p>"""),
             ("private void comenzar()", r"""<p class="l"><b>L61</b> Se ejecuta al pulsar «Comenzar partida» (L33). Es el momento
de la verdad: leer todo y entregarlo.</p>
<p class="l"><b>L62</b> Pregunta al selector qué ficha eligió el Jugador 1 y la guarda en un <code>char</code> local.</p>
<p class="l"><b>L63</b> El Jugador 2 recibe la ficha contraria con el operador ternario (capítulo 13):
«si la del 1 es <code>'X'</code>, entonces <code>'O'</code>; si no, <code>'X'</code>». Calcularla así hace
<b>imposible</b> que los dos tengan la misma ficha. Esto importa: el constructor de <code>Partida</code> lanza una
<code>IllegalArgumentException</code> si se repiten (capítulo 38). La pantalla previene el error en lugar de tener que
atraparlo.</p>
<p class="l"><b>L64</b> Llama a <code>iniciarPartida</code> de la navegación. Los argumentos ocupan tres renglones solo por
comodidad de lectura.</p>
<p class="l"><b>L65</b> Primer argumento: un <code>Jugador</code> nuevo (capítulo 30) con el nombre que devuelve la
tarjeta y su ficha. <code>getNombre()</code> ya se encarga de quitar espacios de los bordes y de usar «Jugador 1» si el
campo quedó vacío (capítulo 49).</p>
<p class="l"><b>L66</b> Segundo argumento: el Jugador 2. En modo contra la IA, su nombre será «Computadora».</p>
<p class="l"><b>L67</b> Tercer argumento: el modo, y se cierra el paréntesis de la L64.</p>
<p class="l"><b>L68–L69</b> Cierran el método y la clase. Fíjate en que la pantalla <b>no</b> crea la
<code>Partida</code>: solo entrega los ingredientes. Quien la crea (el <code>PanelPrincipal</code>) es quien la
guardará y se la pasará a la pantalla de juego y, más tarde, a la de resultado.</p>"""),
         ]},
    ],
    "despues": r"""<h2>Cómo funciona por dentro</h2>
<p>Sigamos a Ana, que quiere jugar contra la computadora y prefiere la O.</p>
<table class="tabla">
<tr><th>Ana hace…</th><th>Se ejecuta…</th><th>Estado después</th></tr>
<tr><td>Abre la pantalla.</td><td>Constructor; al final, <code>elegirModo(DOS_JUGADORES)</code>.</td>
<td><code>modo = DOS_JUGADORES</code>; «2 jugadores» marcada; selector en X.</td></tr>
<tr><td>Escribe <code>  Ana </code> (con espacios) en la tarjeta 1.</td><td>Nada de esta clase: el texto queda dentro
del <code>CampoTexto</code>.</td><td>Igual.</td></tr>
<tr><td>Escribe <code>Beto</code> en la tarjeta 2.</td><td>Nada.</td><td>Igual.</td></tr>
<tr><td>Pulsa la caja de la O.</td><td><code>SelectorSimbolo.setFichaJugador1('O')</code> (capítulo 50).</td>
<td>El selector guarda <code>'O'</code>; la leyenda dice «Jugador 1 juega con O · Jugador 2 con X».</td></tr>
<tr><td>Pulsa «Contra la IA».</td><td>Runnable de la L30 → <code>elegirModo(CONTRA_IA)</code>.</td>
<td><code>modo = CONTRA_IA</code>; se marca «Contra la IA» y se desmarca la otra; la tarjeta 2 guarda «Beto», muestra
«Computadora» y se bloquea.</td></tr>
<tr><td>Pulsa «Comenzar partida».</td><td><code>comenzar()</code>.</td>
<td><code>fichaJugador1 = 'O'</code>, <code>fichaJugador2 = 'X'</code>; se llama a
<code>iniciarPartida(Jugador("Ana",'O'), Jugador("Computadora",'X'), CONTRA_IA)</code>.</td></tr>
</table>
<p>Si antes de comenzar Ana se arrepiente y vuelve a «2 jugadores», la tarjeta 2 recupera «Beto». Y si deja la tarjeta
1 vacía, el jugador se llamará «Jugador 1».</p>
<p>¿Quién empieza esa partida? La regla está en <code>Partida</code> (capítulo 38): <b>siempre empieza la X</b>. Como
Ana eligió la O, la X es de la computadora, y la computadora abrirá la partida. Esta pantalla no tiene que saberlo:
solo entrega los datos. Lo verás funcionar en el capítulo 59.</p>
<div class="caja concepto"><b>Una sola fuente de verdad</b> El modo elegido vive en <b>un</b> sitio: el atributo
<code>modo</code>. Las dos opciones marcadas y la tarjeta de la computadora no «recuerdan» nada por su cuenta: siempre
se ponen de acuerdo con <code>modo</code> a través de <code>elegirModo</code>. Si cada componente guardara su propia idea
del modo, tarde o temprano se desincronizarían (dos opciones marcadas a la vez, o «Computadora» en modo de dos
personas). Este principio se usa en toda interfaz seria: un dato, un dueño, y la pantalla lo refleja.</div>

<h2>Compila y prueba</h2>
<ol>
<li>Abre <i>herramientas/VistaPrevia.java</i> y cambia la línea <code>// &lt;-- AQUI</code>:
<pre class="java">            JPanel pantalla = new PantallaConfiguracion(sinNavegacion);   // &lt;-- AQUI</pre></li>
<li>Para <b>ver</b> lo que entrega la pantalla, cambia también, temporalmente, el método <code>iniciarPartida</code> de la
navegación de mentira (la línea 25) para que escriba en la consola lo que recibe:
<pre class="java">                @Override public void iniciarPartida(Jugador j1, Jugador j2, Partida.Modo modo) {
                    System.out.println(j1.getNombre() + " (" + j1.getFicha() + ") contra "
                            + j2.getNombre() + " (" + j2.getFicha() + "), modo " + modo);
                }</pre></li>
<li>Guarda, compila con <i>Clean and Build</i> (Shift+F11) y lanza la vista previa:
<pre class="ps">java -cp target\classes herramientas\VistaPrevia.java</pre></li>
<li>Repite la historia de Ana: escribe «Ana», elige la O, pulsa «Contra la IA» y luego «Comenzar partida». En
PowerShell debe aparecer:
<pre class="salida">Ana (O) contra Computadora (X), modo CONTRA_IA</pre></li>
<li>Vuelve a «2 jugadores», deja los nombres vacíos, elige la X y pulsa «Comenzar partida» otra vez:
<pre class="salida">Jugador 1 (X) contra Jugador 2 (O), modo DOS_JUGADORES</pre></li>
</ol>
<p>Comprueba también que: solo una opción de modo está marcada a la vez; al elegir «Contra la IA» el campo del Jugador 2
no deja escribir; al volver a «2 jugadores» reaparece lo que habías escrito; «Volver» no hace nada (la navegación de
mentira no va a ningún sitio).</p>
<div class="caja consejo"><b>Imprimir para entender</b> El <code>System.out.println</code> que pusiste en la vista previa
es la herramienta de depuración más antigua y todavía una de las más útiles: cuando no sabes qué datos viajan de una
clase a otra, imprímelos justo donde llegan. En el capítulo 62 verás el depurador de NetBeans, que hace lo mismo sin
tocar el código.</div>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Síntoma</th><th>Causa probable</th><th>Solución</th></tr>
<tr><td><code>variable navegacion might not have been initialized</code></td><td>Falta la L22 o está mal escrita
(<code>navegacion = navegacion</code>).</td><td>Escribe <code>this.navegacion = navegacion;</code>.</td></tr>
<tr><td><code>NullPointerException</code> al abrir la pantalla.</td><td>Moviste <code>elegirModo(...)</code> antes de crear
las opciones o las tarjetas.</td><td>Déjala como última línea del constructor.</td></tr>
<tr><td>Ninguna opción de modo aparece marcada.</td><td>Falta la L51.</td><td>Agrégala.</td></tr>
<tr><td><code>cannot find symbol: variable Modo</code></td><td>Escribiste <code>Modo.CONTRA_IA</code> sin
<code>Partida.</code> delante.</td><td>El enum está dentro de <code>Partida</code>: <code>Partida.Modo.CONTRA_IA</code>.</td></tr>
<tr><td><code>IllegalArgumentException: Los dos jugadores no pueden usar la misma ficha</code></td><td>Cambiaste la L63 y
ahora los dos reciben la misma ficha.</td><td>Vuelve al ternario original.</td></tr>
</table>

<div class="caja git"><b>Git</b> Devuelve la vista previa a como estaba (deshace los dos cambios temporales) y sube la
pantalla:
<pre class="ps">git restore herramientas\VistaPrevia.java
git add src\PantallaConfiguracion.java
git commit -m "PantallaConfiguracion: jugadores, simbolos y modo"
git push
git log --oneline -3</pre></div>

<h2>Resumen</h2>
<ul>
<li><code>PantallaConfiguracion</code> muestra tres secciones (jugadores, símbolos, modo) y, al comenzar, crea dos
<code>Jugador</code> y entrega el <code>Partida.Modo</code> a la navegación.</li>
<li>No tiene <code>import</code>: solo usa clases propias del Totito.</li>
<li>Lo que se consulta después del constructor se guarda en atributos; lo que no, en variables locales.</li>
<li>Los atributos <code>final</code> sin valor inicial obligan a asignarlos en el constructor: una red de seguridad.</li>
<li><code>() -&gt; …</code> es un <code>Runnable</code> (sin datos); <code>e -&gt; …</code> es un oyente de botón (recibe el
evento).</li>
<li><code>elegirModo</code> es la única puerta para cambiar el modo y mantiene sincronizados el dato y la apariencia.</li>
<li>La ficha del Jugador 2 se calcula como la contraria: así nunca se repiten.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Cualquier formulario:</b> registro de clientes, pedido de una tienda, alta de un empleado. El patrón es idéntico:
componentes en atributos, un botón «Guardar» que lee todo, crea un objeto de datos (<code>Cliente</code>,
<code>Pedido</code>) y se lo entrega a otra parte del programa.</li>
<li><b>Valores por defecto razonables:</b> si un campo queda vacío, usa uno sensato (como «Jugador 1») en lugar de
fallar. En una factura, «Consumidor final» si no hay NIT.</li>
<li><b>Opciones que cambian otras:</b> en una app de envíos, elegir «Recoger en tienda» bloquea el campo de dirección,
igual que «Contra la IA» bloquea el nombre del Jugador 2. Un solo método (como <code>elegirModo</code>) mantiene todo
coherente.</li>
<li><b>Prevenir en vez de atrapar:</b> calcular la ficha contraria evita una excepción. En un formulario de fechas,
ofrecer solo fechas válidas evita tener que avisar de un error después.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b><ol>
<li>Cambia el modo que viene elegido al abrir la pantalla para que sea «Contra la IA». ¿Qué línea tocas? ¿Qué le pasa a
la tarjeta del Jugador 2?</li>
<li>Haz que, en modo contra la IA, la computadora se llame «Totito-Bot». Pista: el nombre viene de una constante de
<code>TarjetaJugador</code> (capítulo 49).</li>
<li>Escribe en papel qué imprimiría la vista previa si el Jugador 1 se llama «Luis», elige la O y el modo es
«2 jugadores» con la tarjeta 2 vacía. Compruébalo.</li>
<li>Agrega un tercer botón de modo, «Contra la IA (fácil)», que por ahora haga lo mismo que «Contra la IA». ¿Qué tienes
que cambiar en <code>elegirModo</code> para que siga habiendo una sola opción marcada? Pista: ahora son tres comparaciones.</li>
<li>Reto: impide que los dos jugadores tengan el mismo nombre. Si coinciden, que al segundo se le agregue « (2)». ¿En qué
método lo pondrías y por qué?</li>
</ol></div>
""",
}
