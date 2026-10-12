CAPITULO = {
    "numero": 47,
    "titulo": "CampoTexto.java: la caja para escribir el nombre",
    "antes": r"""
<p class="entrada">En la pantalla de configuración cada jugador escribe su nombre en una caja redondeada con borde
de neón. Cuando está vacía muestra «Jugador 1» en gris, el borde brilla más mientras escribes y no deja pasar de 14
letras. En este capítulo construyes esa caja heredando de <code>JTextField</code>, y descubres cómo interceptar lo que
el usuario escribe <i>antes</i> de que llegue al texto.</p>

<h2>Por qué existe este archivo</h2>
<p>Un <code>JTextField</code> normal es un rectángulo blanco con borde gris: desentona por completo sobre el fondo
oscuro. Y tiene un problema más serio: deja escribir cualquier cantidad de letras. Si alguien se llamara «María
Fernanda de los Ángeles», el nombre no cabría en el marcador de la partida (capítulo 52) ni en «¡Ganó …!» (aunque
<code>Rotulo</code> achica la letra, todo tiene un límite). La solución más limpia no es recortar el nombre después,
sino <b>no dejar escribirlo</b>: así el usuario ve en el momento hasta dónde llega.</p>
<figure><img src="capturas/3-configuracion.png"><figcaption>Las dos cajas de nombre, con el texto de ayuda «Jugador 1»
y «Jugador 2» en gris.</figcaption></figure>
<p>Quien usará esta clase es <code>TarjetaJugador</code> (capítulo 49), que pone un <code>CampoTexto</code> dentro de
cada tarjeta de jugador.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>Heredar de <code>JTextField</code> y cambiar su aspecto sin perder escribir, borrar, seleccionar, copiar, pegar ni
mover el cursor.</li>
<li>Los colores propios de un campo de texto: del texto, del texto desactivado, del cursor, de la selección.</li>
<li>Usar un <b>borde vacío</b> para decidir dónde empieza el texto.</li>
<li>Escuchar el foco con un <code>FocusAdapter</code> en una clase anónima.</li>
<li>Pintar un <b>texto de ayuda</b> (<i>placeholder</i>).</li>
<li>El <b>orden de pintado</b>: por qué aquí <code>super.paintComponent(g)</code> va <b>al final</b>.</li>
<li>El modelo de texto (<code>Document</code>) y un <code>DocumentFilter</code> que limita a 14 caracteres, probado con
cuatro casos reales.</li>
<li>Clases internas <code>static</code> y excepciones declaradas con <code>throws</code>.</li>
</ul>

<h2>Créalo</h2>
<ol>
<li>En la rama <code>interfaz-neon</code>: clic derecho en <i>&lt;default package&gt;</i> → <i>New → Java Class…</i> →
<code>CampoTexto</code> → <i>Finish</i>.</li>
<li>Reemplaza el esqueleto por el código.</li>
</ol>
<pre class="ps">New-Item -ItemType File src\CampoTexto.java
notepad src\CampoTexto.java</pre>
""",
    "archivos": [
        {"ruta": "src/CampoTexto.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>Color</code>: colores del borde, del texto, del cursor y de la selección.</p>
<p class="l"><b>L2</b> <code>Font</code>: por <code>Font.PLAIN</code> (letra normal, sin negrita).</p>
<p class="l"><b>L3</b> <code>FontMetrics</code>: para centrar en vertical el texto de ayuda.</p>
<p class="l"><b>L4–L5</b> <code>Graphics</code> y <code>Graphics2D</code>, el pincel.</p>
<p class="l"><b>L6</b> <code>java.awt.event.FocusAdapter</code>: una clase con métodos vacíos para reaccionar al foco
(cuando el campo empieza o deja de recibir el teclado). El paquete <code>java.awt.event</code> reúne todo lo
relacionado con eventos.</p>
<p class="l"><b>L7</b> <code>java.awt.event.FocusEvent</code>: el objeto que describe un cambio de foco; es el
parámetro de esos métodos.</p>
<p class="l"><b>L8</b> <code>RoundRectangle2D</code>: la caja redondeada.</p>
"""),
             ("import javax.swing.BorderFactory", r"""
<p class="l"><b>L9</b> <code>javax.swing.BorderFactory</code>: una fábrica de bordes. La usaremos para crear un borde
<b>vacío</b>, que no se ve pero ocupa espacio.</p>
<p class="l"><b>L10</b> <code>javax.swing.JTextField</code>: el campo de texto de una línea, del que heredamos.</p>
<p class="l"><b>L11</b> <code>javax.swing.text.AbstractDocument</code>: la clase base de los «documentos» de texto. En
Swing, el texto de un campo no vive en el campo, sino en un objeto aparte, su <b>documento</b> (el modelo, como el
<code>ButtonModel</code> del botón). <code>AbstractDocument</code> es la que permite instalarle un filtro. El paquete
<code>javax.swing.text</code> agrupa todo lo de edición de texto.</p>
<p class="l"><b>L12</b> <code>AttributeSet</code>: atributos de estilo de un trozo de texto (negrita, color…). Un
campo sencillo no los usa, pero forman parte de los métodos que vamos a sobrescribir.</p>
<p class="l"><b>L13</b> <code>BadLocationException</code>: la excepción que lanzan los documentos si se les pide
trabajar en una posición que no existe (por ejemplo, insertar en la letra 50 de un texto de 10).</p>
<p class="l"><b>L14</b> <code>DocumentFilter</code>: un «portero» que intercepta cada cambio del documento antes de que
ocurra y puede dejarlo pasar, modificarlo o rechazarlo.</p>
<p class="l"><b>L15</b> En blanco.</p>
"""),
             ("public class CampoTexto", r"""
<p class="l"><b>L16–L21</b> Comentario de documentación: caja redondeada, texto de ayuda gris cuando está vacía y
límite de <code>MAXIMO</code> caracteres para que el nombre quepa en el marcador y en la pantalla de victoria.</p>
<p class="l"><b>L22</b> <code>public class CampoTexto extends JTextField {</code>: un <code>CampoTexto</code> <b>es
un</b> <code>JTextField</code>. Se conservan gratis el cursor que parpadea, las flechas, Inicio/Fin, seleccionar con
el ratón o con Shift, Ctrl+C / Ctrl+V, las tildes y la ñ del teclado… Todo eso costaría cientos de
líneas hacerlo a mano.</p>
<p class="l"><b>L23</b> En blanco.</p>
"""),
             ("public static final int MAXIMO", r"""
<p class="l"><b>L24</b> <code>public static final int MAXIMO = 14;</code> el largo máximo del nombre. Es público por
si otra clase necesita saberlo (por ejemplo, para mostrar «máximo 14 letras»). ¿Por qué 14? Es lo que cabe con
holgura en la tarjeta del marcador y, con el achicado de <code>Rotulo</code>, en «¡Ganó …!» (capítulo 46: «¡Ganó
Maximiliano Ro!» bajó solo de 40 a 38 puntos).</p>
<p class="l"><b>L25</b> Comentario: espacio para el halo del borde.</p>
<p class="l"><b>L26</b> <code>MARGEN = 5</code>: menor que el 10 de la tarjeta. Con un borde de 1.6 la capa de halo
más ancha sobresaldría 8 píxeles, así que las tres capas más externas se recortan un poco. Es un compromiso
aceptable: son las más transparentes (alfa de 4 a 19 sobre 255, según tenga o no el foco) y, a cambio, la caja
aprovecha mejor el poco espacio que tiene dentro de la tarjeta.</p>
<p class="l"><b>L27</b> En blanco.</p>
"""),
             ("private final Color color;", r"""
<p class="l"><b>L28</b> El color del campo (fresa para el Jugador 1, azul para el Jugador 2): borde, relleno y
selección.</p>
<p class="l"><b>L29</b> <code>ayuda</code>: el texto de ayuda («Jugador 1»). Se guarda porque se pinta cada vez que el
campo está vacío.</p>
<p class="l"><b>L30</b> En blanco.</p>
"""),
             ("public CampoTexto(String ayuda", r"""
<p class="l"><b>L31</b> El constructor recibe el texto de ayuda y el color. No hay <code>super(...)</code> escrito:
cuando no lo pones, Java llama solo al constructor sin parámetros de la madre, <code>JTextField()</code>, que crea un
campo vacío.</p>
<p class="l"><b>L32–L33</b> Guarda los dos datos.</p>
<p class="l"><b>L34</b> <code>setOpaque(false);</code> el campo no pintará su fondo blanco. Es clave por partida doble:
la caja es redondeada (sus esquinas deben dejar ver el fondo) y, como verás en la línea 73, cuando Swing pinte el texto
no debe borrar antes nuestra caja.</p>
<p class="l"><b>L35</b> <code>setForeground(Tema.TEXTO);</code> texto blanco.</p>
<p class="l"><b>L36</b> <code>setDisabledTextColor(Tema.TEXTO_SUAVE);</code> el color del texto cuando el campo está
<b>desactivado</b>. Ocurre en la tarjeta del Jugador 2 cuando eliges jugar contra la IA: el campo muestra
«Computadora» y no deja escribir (capítulo 49). Lavanda suave dice «esto no se puede editar».</p>
<p class="l"><b>L37</b> <code>setCaretColor(Tema.TEXTO);</code> el color del cursor de escritura (la rayita que
parpadea, en inglés <i>caret</i>). Por defecto es negro: sobre nuestro fondo oscuro sería invisible y el usuario no
sabría dónde está escribiendo.</p>
"""),
             ("setSelectionColor", r"""
<p class="l"><b>L38</b> <code>setSelectionColor(Tema.conAlfa(color, 120));</code> el fondo del texto seleccionado
(cuando lo marcas con el ratón): el color del campo semitransparente, en lugar del azul de Windows.</p>
<p class="l"><b>L39</b> <code>setSelectedTextColor(Tema.TEXTO);</code> el texto seleccionado sigue en blanco, legible
sobre ese fondo.</p>
<p class="l"><b>L40</b> Letra normal de 17 puntos.</p>
<p class="l"><b>L41</b> <code>setBorder(BorderFactory.createEmptyBorder(MARGEN + 4, MARGEN + 14, MARGEN + 4, MARGEN +
10));</code> un borde <b>vacío</b> de 9 píxeles arriba, 19 a la izquierda, 9 abajo y 15 a la derecha (el orden es
arriba, izquierda, abajo, derecha). No se dibuja nada, pero Swing usa los bordes para saber dónde <b>no</b> poner el
texto: el texto empieza en x = 19 (5 del margen del halo + 14 de respiro dentro de la caja). Sin esta línea, el texto
quedaría pegado al borde de neón o incluso encima de él.</p>
<p class="l"><b>L42</b> <code>((AbstractDocument) getDocument()).setDocumentFilter(new LimiteDeLargo());</code> instala
el portero. Por partes: <code>getDocument()</code> devuelve el documento del campo con el tipo general
<code>Document</code> (una interfaz), que no tiene <code>setDocumentFilter</code>. Pero sabemos que el documento de un
<code>JTextField</code> es un <code>PlainDocument</code>, que hereda de <code>AbstractDocument</code>; con
<code>(AbstractDocument)</code> se lo decimos al compilador (un <i>cast</i> de referencias, capítulo 22). Los paréntesis
de fuera son necesarios para que el cast se aplique antes del punto. Por último, se crea un filtro
<code>LimiteDeLargo</code> (línea 77) y se instala.</p>
"""),
             ("// Al entrar o salir", r"""
<p class="l"><b>L43</b> Comentario: al entrar o salir del campo cambia el brillo del borde.</p>
<p class="l"><b>L44</b> <code>addFocusListener(new FocusAdapter() {</code> registra un «oyente» del foco. El
<b>foco</b> es quién recibe el teclado: solo un componente a la vez. <code>new FocusAdapter() { … }</code> crea una
<b>clase anónima</b> (capítulo 25): una subclase de <code>FocusAdapter</code> sin nombre, escrita y usada en el mismo
sitio. <code>FocusAdapter</code> implementa la interfaz <code>FocusListener</code> con métodos vacíos, así que solo
sobrescribimos los que nos interesan.</p>
<p class="l"><b>L45–L46</b> <code>focusGained</code>: Swing lo llama cuando el campo <b>recibe</b> el foco (haces clic
en él o llegas con Tab).</p>
<p class="l"><b>L47</b> <code>repaint();</code> pide repintar el campo, para que el borde se encienda y desaparezca el
texto de ayuda. ¿Por qué hace falta? Al cambiar el foco, Swing se ocupa de mostrar u ocultar el cursor (y repinta ese
rectángulo diminuto), pero no sabe que nuestro borde depende del foco. Sin esta línea, el borde seguiría apagado hasta que otra cosa forzara un repintado.
Nota: dentro de la clase anónima, <code>repaint()</code> se refiere al del campo, porque la clase anónima no tiene uno
propio y Java lo busca en la clase de fuera.</p>
<p class="l"><b>L48–L49</b> Cierra el método; línea en blanco.</p>
"""),
             ("public void focusLost", r"""
<p class="l"><b>L50–L51</b> <code>focusLost</code>: cuando el campo <b>pierde</b> el foco (haces clic en otro lado o
pulsas Tab).</p>
<p class="l"><b>L52</b> Repinta para apagar el borde y, si quedó vacío, volver a mostrar el texto de ayuda.</p>
<p class="l"><b>L53</b> Cierra el método.</p>
<p class="l"><b>L54</b> <code>});</code> la llave cierra la clase anónima; el paréntesis cierra la llamada a
<code>addFocusListener(</code>; el punto y coma termina la instrucción. Este trío es típico de las clases anónimas y es
fácil equivocarse al teclearlo.</p>
<p class="l"><b>L55–L56</b> Cierra el constructor; línea en blanco.</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L57–L58</b> Sobrescribimos el dibujo del campo.</p>
<p class="l"><b>L59</b> Una copia preparada del pincel.</p>
<p class="l"><b>L60–L61</b> La caja: desde (5, 5), tamaño menos los márgenes, esquinas con arco 18.</p>
<p class="l"><b>L62</b> <code>g2.setColor(Tema.conAlfa(color, isEnabled() ? 26 : 12));</code> relleno muy tenue del
color del campo: alfa 26 si está activo y 12 (todavía más apagado) si está desactivado.</p>
<p class="l"><b>L63</b> Rellena la caja.</p>
<p class="l"><b>L64</b> <code>Dibujo.trazoNeon(g2, forma, color, 1.6f, hasFocus() ? 1.2f : 0.6f);</code> el borde de
neón. <code>hasFocus()</code> (heredado) dice si este campo tiene el foco ahora mismo: si lo tiene, intensidad 1.2
(brilla); si no, 0.6 (tenue). Así el usuario ve de un vistazo en qué caja está escribiendo.</p>
<p class="l"><b>L65</b> En blanco.</p>
"""),
             ("if (getText().isEmpty()", r"""
<p class="l"><b>L66</b> <code>if (getText().isEmpty() &amp;&amp; !hasFocus()) {</code> el texto de ayuda se pinta solo
si el campo está vacío <b>y</b> no tiene el foco. Al hacer clic, desaparece y queda el cursor; si sales sin escribir,
vuelve.</p>
<p class="l"><b>L67</b> La fuente del campo (la ayuda se ve con la misma letra que tendrá el nombre).</p>
<p class="l"><b>L68</b> Color lavanda suave: se nota que es una pista y no un texto escrito.</p>
<p class="l"><b>L69</b> Las medidas de la fuente, para centrar en vertical.</p>
<p class="l"><b>L70</b> <code>g2.drawString(ayuda, getInsets().left, …)</code> escribe la ayuda. <code>getInsets()</code>
devuelve el espacio que ocupa el borde vacío de la línea 41; su <code>left</code> vale 19. Es la misma x donde Swing
pondrá el texto real, así que cuando empiezas a escribir, las letras nacen justo donde estaba la ayuda. La línea base
se centra en la mitad del alto.</p>
<p class="l"><b>L71</b> Cierra el <code>if</code>.</p>
<p class="l"><b>L72</b> <code>g2.dispose();</code> liberamos <b>nuestra</b> copia del pincel antes de seguir.</p>
<p class="l"><b>L73</b> <code>super.paintComponent(g);</code> y ahora sí, le pedimos a <code>JTextField</code> que haga
su parte: pinta la selección, el texto y el cursor. Tres detalles importantes:</p>
<p class="l">— Va <b>al final</b> porque en Swing lo último que se pinta queda encima. Si fuera la primera línea, nuestro
relleno y nuestro borde se pintarían después, <b>sobre</b> el texto y la selección, velándolos.</p>
<p class="l">— Se le pasa <code>g</code>, el pincel original, no <code>g2</code> (que ya liberamos). Así Swing pinta con
su configuración de siempre.</p>
<p class="l">— Funciona gracias a <code>setOpaque(false)</code>: un campo opaco empezaría rellenando todo su rectángulo
con el color de fondo, y borraría la caja que acabamos de dibujar.</p>
<p class="l">Es justo lo contrario que en <code>Tarjeta</code> y <code>BotonNeon</code>, donde no llamábamos a
<code>super</code>: allí no queríamos nada de lo que pinta Swing; aquí queremos el texto y el cursor, pero
<b>encima</b> de lo nuestro.</p>
<p class="l"><b>L74–L75</b> Cierra el método; línea en blanco.</p>
"""),
             ("private static class LimiteDeLargo", r"""
<p class="l"><b>L76</b> Comentario: impide que el texto pase de <code>MAXIMO</code> caracteres.</p>
<p class="l"><b>L77</b> <code>private static class LimiteDeLargo extends DocumentFilter {</code> una <b>clase
interna</b> (declarada dentro de otra). <code>private</code>: solo la usa <code>CampoTexto</code>. <code>static</code>:
no necesita un <code>CampoTexto</code> concreto para existir ni para trabajar (solo usa la constante
<code>MAXIMO</code>, que también es estática). Una clase interna sin <code>static</code> guardaría una referencia
oculta al objeto de fuera; aquí no hace falta. Hereda de <code>DocumentFilter</code>, cuyos métodos, si no se
sobrescriben, dejan pasar todo tal cual.</p>
<p class="l"><b>L78–L80</b> Sobrescribimos <code>insertString</code>, el método que el documento llama cuando se quiere
<b>insertar</b> texto en una posición. Parámetros: <code>fb</code> (un «paso directo» al documento, abajo lo
explico), <code>offset</code> (la posición donde se inserta, contando desde 0), <code>texto</code> (lo que se quiere
insertar) y <code>attr</code> (atributos de estilo). La línea 80, <code>throws BadLocationException</code>, avisa de que
el método puede lanzar esa excepción (capítulo 26); es obligatorio declararla porque los métodos que llamamos dentro
también la declaran.</p>
<p class="l"><b>L81</b> <code>replace(fb, offset, 0, texto, attr);</code> insertar es lo mismo que «reemplazar 0
caracteres en esa posición por el texto nuevo». Así toda la lógica del límite se escribe una sola vez, en
<code>replace</code>.</p>
<p class="l"><b>L82–L83</b> Cierra el método; línea en blanco.</p>
"""),
             ("public void replace(", r"""
<p class="l"><b>L84–L86</b> Sobrescribimos <code>replace</code>: el documento lo llama cuando se quiere reemplazar
<code>largo</code> caracteres a partir de <code>offset</code> por <code>texto</code>. Cubre casi todo: escribir una
letra (reemplaza la selección, que puede ser de 0 caracteres), pegar, escribir sobre una selección,
<code>setText(...)</code>. <code>FilterBypass</code> es una clase que vive dentro de <code>DocumentFilter</code> (se
escribe sin prefijo porque la heredamos): a través de ella el filtro cambia el documento <b>sin</b> volver a pasar por
el filtro. Si el filtro cambiara el documento de la forma normal, se llamaría a sí mismo una y otra vez.</p>
<p class="l"><b>L87–L89</b> <code>if (texto == null) { texto = ""; }</code> el documento puede llamar a
<code>replace</code> con <code>null</code> para indicar «solo borrar, no insertar nada». Lo convertimos en cadena vacía
para que las líneas siguientes (que llaman a <code>texto.length()</code>) no fallen con
<code>NullPointerException</code>.</p>
"""),
             ("int disponible", r"""
<p class="l"><b>L90</b> <code>int disponible = MAXIMO - (fb.getDocument().getLength() - largo);</code> la cuenta
clave: cuántos caracteres caben. <code>getLength()</code> es el largo actual; a eso se le resta lo que se va a
reemplazar (<code>largo</code>), porque esos caracteres desaparecerán. Lo que queda es lo que <b>sobrevivirá</b>; y
<code>MAXIMO</code> menos eso es el hueco disponible.</p>
<p class="l"><b>L91</b> <code>if (texto.length() &gt; disponible) {</code> ¿lo que se quiere meter es más largo que el
hueco?</p>
<p class="l"><b>L92</b> <code>texto = texto.substring(0, Math.max(0, disponible));</code> entonces se recorta: se
queda con los primeros <code>disponible</code> caracteres. <code>Math.max(0, …)</code> es un seguro: si
<code>disponible</code> fuera negativo (no debería, porque el texto nunca supera 14, pero el código defensivo no
cuesta nada), <code>substring(0, -1)</code> lanzaría una excepción; con el seguro se queda en 0, cadena vacía.</p>
<p class="l"><b>L93</b> Cierra el <code>if</code>.</p>
<p class="l"><b>L94</b> <code>super.replace(fb, offset, largo, texto, attr);</code> hace el reemplazo de verdad, ya con
el texto recortado (o intacto, si cabía). La versión de <code>DocumentFilter</code> lo pasa al documento por el
<code>FilterBypass</code>. Sin esta línea, el campo no aceptaría <b>ninguna</b> letra: el portero no dejaría pasar a
nadie.</p>
<p class="l"><b>L95–L97</b> Cierran el método, la clase interna y la clase <code>CampoTexto</code>.</p>
<p class="l">¿Y borrar? Borrar con Retroceso o Supr pasa por otro método del filtro, <code>remove</code>, que no
sobrescribimos: borrar nunca hace el texto más largo, así que se deja pasar siempre.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>Las medidas dentro de la tarjeta del jugador</h3>
<p><code>TarjetaJugador</code> (290 × 150) colocará el campo en (22, 84) con <b>246 × 46</b>. Entonces la caja va de
(5, 5) a (241, 41): 236 × 36 con esquinas de radio 9. El borde vacío deja el texto entre x = 19 y x = 246 − 15 = 231. El
texto de ayuda «Jugador 1» (76 píxeles de ancho en letra de 17) se escribe en x = 19 con la línea base en 23 + (16 −
4) ÷ 2 = 29.</p>
<h3>El portero en acción: cuatro casos reales</h3>
<p>Probé estos cuatro casos con el código del capítulo (los resultados son los que imprimió Java):</p>
<table class="tabla">
<tr><th>Situación</th><th>Llamada que recibe el filtro</th><th>Cuenta de <code>disponible</code></th><th>Resultado</th></tr>
<tr><td>Campo vacío; el programa hace <code>setText("Maximiliano Rodriguez")</code> (21 letras) o el usuario lo
pega</td><td><code>replace(fb, 0, 0, "Maximiliano Rodriguez")</code></td><td>14 − (0 − 0) = 14</td><td>«Maximiliano
Ro»</td></tr>
<tr><td>Ya hay 14 letras y el usuario teclea una más al final</td><td><code>replace(fb, 14, 0, "x")</code></td><td>14 −
(14 − 0) = 0</td><td>no cambia nada: la letra no entra</td></tr>
<tr><td>Hay «Ana» y se pega «bel Cristina de» (15) después de la a</td><td><code>insertString(fb, 3, "bel Cristina
de")</code> → <code>replace(fb, 3, 0, …)</code></td><td>14 − (3 − 0) = 11</td><td>«Anabel Cristin»</td></tr>
<tr><td>Hay «Ana Lucia», se selecciona «Ana» y se escribe encima «Mariana»</td><td><code>replace(fb, 0, 3,
"Mariana")</code></td><td>14 − (9 − 3) = 8</td><td>«Mariana Lucia» (cabe entero)</td></tr>
</table>
<p>El último caso muestra por qué se resta <code>largo</code>: las tres letras seleccionadas van a desaparecer, así que
no cuentan para el límite. Si no se restaran, el hueco sería 14 − 9 = 5 y «Mariana» se quedaría en «Maria».</p>
<h3>El orden de pintado, capa por capa</h3>
<ol>
<li>Swing ve que el campo no es opaco y pinta primero lo que hay detrás (la tarjeta del jugador).</li>
<li>Nuestro <code>paintComponent</code>: relleno tenue, borde de neón (brillante si tiene el foco) y, si está vacío y
sin foco, la ayuda en gris.</li>
<li><code>super.paintComponent(g)</code>: <code>JTextField</code> pinta la selección, el texto blanco y el cursor
blanco, encima de todo lo anterior.</li>
</ol>

<h2>Compila y prueba</h2>
<p><i>Clean and Build</i> (Shift+F11) → <code>BUILD SUCCESS</code>. En <code>target\classes</code> aparecen
<b>tres</b> archivos: <code>CampoTexto.class</code>, <code>CampoTexto$LimiteDeLargo.class</code> (la clase interna con
nombre) y <code>CampoTexto$1.class</code> (la clase anónima del foco: como no tiene nombre, Java la numera).</p>
<p>El límite se puede comprobar <b>sin ventana</b>: un campo de texto funciona aunque nadie lo vea. Crea
<code>..\pruebas-totito\ProbarCampo.java</code> (fuera del proyecto, como la foto del capítulo 43):</p>
<pre class="ps">notepad ..\pruebas-totito\ProbarCampo.java</pre>
<pre class="java">public class ProbarCampo {
    public static void main(String[] args) {
        CampoTexto campo = new CampoTexto("Jugador 1", Tema.ROSA);
        campo.setText("Maximiliano Rodriguez");
        System.out.println("Quedo: " + campo.getText());
        System.out.println("Letras: " + campo.getText().length());
    }
}</pre>
<pre class="ps">java -cp target\classes ..\pruebas-totito\ProbarCampo.java</pre>
<pre class="salida">Quedo: Maximiliano Ro
Letras: 14</pre>
<p>Si sale el nombre completo con 21 letras, el filtro no está instalado: revisa la línea 42 y la 94.</p>
<p>Para verlo, la foto opcional con <code>JComponent pieza = new CampoTexto("Jugador 1", Tema.FRESA);</code> y
<code>int ancho = 246, alto = 46;</code> muestra la caja vacía con la ayuda en gris. (Una foto no tiene foco, así que
siempre verás el borde tenue.) El campo funcionando de verdad, con el cursor y el brillo al hacer clic, lo verás en la
pantalla de configuración (capítulo 58).</p>
<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Síntoma o mensaje</th><th>Causa</th><th>Solución</th></tr>
<tr><td>No se ve el texto que escribes</td><td><code>super.paintComponent(g)</code> está al principio (tu relleno lo
tapa) o falta <code>setOpaque(false)</code> (Swing borra tu caja)</td><td>Líneas 73 y 34</td></tr>
<tr><td>No se ve el cursor</td><td>Falta <code>setCaretColor</code></td><td>Línea 37</td></tr>
<tr><td>No se puede escribir nada</td><td>Falta <code>super.replace(...)</code> en el filtro</td><td>Línea 94</td></tr>
<tr><td><code>unreported exception BadLocationException; must be caught or declared to be thrown</code></td><td>Falta
el <code>throws</code></td><td>Líneas 80 y 86</td></tr>
<tr><td><code>cannot find symbol: class FilterBypass</code></td><td>La clase interna no hereda de
<code>DocumentFilter</code></td><td>Revisa <code>extends DocumentFilter</code> en la línea 77</td></tr>
<tr><td><code>';' expected</code> cerca de la línea 54</td><td>Falta el <code>});</code> completo</td><td>Llave,
paréntesis y punto y coma</td></tr>
</table>

<div class="caja git"><b>Git</b>
<pre class="ps">git status
git add src\CampoTexto.java
git commit -m "CampoTexto: caja de texto con limite"
git push</pre>
<code>ProbarCampo.java</code> está en <code>..\pruebas-totito</code>, fuera del repositorio: <code>git status</code>
no lo mostrará.</div>

<h2>Resumen</h2>
<ul>
<li>Heredar de <code>JTextField</code> conserva toda la edición; solo cambiamos colores, márgenes y dibujo.</li>
<li>El cursor, la selección y el texto desactivado tienen sus propios colores; en fondo oscuro hay que ponerlos.</li>
<li>Un borde vacío decide dónde empieza el texto; <code>getInsets()</code> lo consulta.</li>
<li>Un <code>FocusAdapter</code> anónimo pide <code>repaint()</code> al entrar y salir, para encender el borde y
mostrar u ocultar la ayuda.</li>
<li>Primero lo nuestro, después <code>super.paintComponent(g)</code>: así el texto queda encima; requiere
<code>setOpaque(false)</code>.</li>
<li>El texto vive en un documento; un <code>DocumentFilter</code> instalado en él intercepta cada cambio. La cuenta
<code>MAXIMO − (largo actual − largo reemplazado)</code> da el hueco disponible.</li>
<li><code>FilterBypass</code> modifica el documento sin volver a pasar por el filtro.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Campos con formato</b>: un <code>DocumentFilter</code> que solo deja pasar dígitos sirve para un número de
teléfono de 8 cifras, un NIT, un PIN de 4 números o una cantidad en una caja registradora.</li>
<li><b>Mayúsculas automáticas</b>: el mismo filtro puede convertir el texto con <code>toUpperCase()</code> antes de
<code>super.replace</code>, útil para placas de vehículos o códigos de producto.</li>
<li><b>Texto de ayuda</b> en formularios: «correo@ejemplo.com», «Buscar producto…», «Contraseña (mínimo 8)».</li>
<li><b>Límites que respetan la base de datos</b>: si una columna admite 50 caracteres, limitar el campo a 50 evita
errores al guardar.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Completa la tabla del portero con este caso: hay «Luis» (4 letras), se selecciona todo y se pega «Fernando
Alejandro» (18). ¿Qué cuenta hace el filtro y qué queda?</li>
<li>Amplía <code>ProbarCampo</code> para reproducir los cuatro casos de la tabla. Pista:
<code>campo.getDocument().insertString(3, "bel Cristina de", null)</code>, <code>campo.select(0, 3)</code> y
<code>campo.replaceSelection("Mariana")</code>; el <code>main</code> necesitará <code>throws Exception</code>.</li>
<li>En una copia del filtro, haz que solo acepte letras y espacios. Pista: recorre <code>texto</code> con un
<code>for</code> y arma una cadena nueva con los caracteres que cumplan <code>Character.isLetter(c) || c == ' '</code>.</li>
<li>¿Qué pasaría si quitaras la condición <code>!hasFocus()</code> de la línea 66? Describe lo que vería el
usuario al hacer clic en el campo vacío.</li>
<li>Reto: explica por qué la clase anónima de la línea 44 podría reemplazarse por una que implemente
<code>FocusListener</code> directamente, y qué tendrías que escribir de más.</li>
</ol></div>
""",
}
