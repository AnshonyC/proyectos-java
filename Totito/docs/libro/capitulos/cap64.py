# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 64,
    "titulo": "El icono del programa: GeneradorIcono.java y el formato .ico",
    "antes": r"""
<p class="entrada">Todo programa serio se reconoce por su icono: en el escritorio, en la barra de tareas, en el menú Inicio. En este capítulo fabricas el del Totito con un programa Java que dibuja el logotipo de neón y lo guarda en dos archivos, <code>recursos\totito.png</code> y <code>recursos\totito.ico</code>, armando este último byte a byte porque Java no sabe escribir ese formato.</p>

<figure><img src="recursos/totito.png"><figcaption>El icono del Totito (512×512 píxeles), generado por GeneradorIcono.java a partir del mismo logotipo que se ve en el encabezado del juego.</figcaption></figure>

<h2>Por qué existe este archivo</h2>
<p>En el capítulo 65, jpackage va a crear <code>Totito.exe</code>. Un <code>.exe</code> de Windows lleva su icono <b>guardado dentro</b>, y jpackage lo toma de la opción <code>--icon recursos\totito.ico</code>. Si no le das uno, le pone el icono genérico de Java (una taza de café) y tu juego se ve como cualquier otro programa sin terminar.</p>
<p>Ese icono tiene que estar en formato <b>.ico</b>, el formato de iconos de Windows. Podrías dibujarlo en un programa de diseño y convertirlo con una página web, y al final del capítulo te explico cómo. Pero el Totito ya tiene su logotipo dibujado con código en <code>Iconos.LOGO</code> (capítulo 42) y sus colores en <code>Tema</code> (capítulo 40). Lo más coherente, y lo más instructivo, es que un programita reutilice ese mismo dibujo para fabricar el icono. Ventajas:</p>
<ul>
<li><b>Es idéntico al logotipo del juego</b>: mismos trazos, mismo neón, mismos colores.</li>
<li><b>Se puede repetir</b>: si mañana cambias un color en <code>Tema</code>, vuelves a ejecutar el generador y el icono se actualiza solo.</li>
<li><b>Aprendes cómo es un archivo binario por dentro</b>, algo que te servirá para entender cualquier formato: imágenes, sonidos, documentos.</li>
</ul>
<p>Igual que <code>PruebaConsola</code> (capítulo 32) y <code>VistaPrevia</code> (capítulo 56), este archivo vive en <code>herramientas\</code>, no en <code>src\</code>: es una herramienta para ti, la persona que desarrolla, y no debe viajar dentro del juego. Por eso Maven no la compila ni la mete en el <code>.jar</code>.</p>
<p>¿Y la ventana del juego? <code>TotitoApp</code> ya dibuja su propio icono de 64 píxeles con el método <code>crearIcono()</code> (capítulo 61) y lo pone con <code>setIconImage</code>. Ese icono solo existe mientras el juego está abierto. El <code>.ico</code> de este capítulo es para lo que Windows muestra <b>sin</b> abrir el juego: el archivo <code>Totito.exe</code>, los accesos directos y el instalador.</p>

<h2>Qué vas a aprender</h2>
<ul>
<li>Qué es un <b>archivo binario</b> y cómo está organizado un <code>.ico</code>: cabecera, entradas de directorio y las imágenes.</li>
<li>Qué es un <b>byte</b>, cómo se escriben números en hexadecimal y qué significa <b>little-endian</b>.</li>
<li>Los operadores de bits <code>&amp;</code> (Y) y <code>&gt;&gt;</code> (desplazamiento a la derecha).</li>
<li>Escribir archivos con <code>FileOutputStream</code> y <code>DataOutputStream</code>, y en memoria con <code>ByteArrayOutputStream</code>.</li>
<li><b>try-with-resources</b> para cerrar archivos sin olvidos.</li>
<li><code>BufferedImage</code> como lienzo invisible, <code>ImageIO</code> para guardar PNG y cómo <b>reducir una imagen a la mitad</b> repetidas veces para que quede nítida.</li>
<li>Arreglos de arreglos (<code>byte[][]</code>), el operador ternario y el bucle <code>do-while</code> en un caso real.</li>
</ul>

<h2>Qué es un .ico por dentro</h2>
<p>Un archivo de imagen, de texto o de lo que sea es, en el fondo, una fila larguísima de <b>bytes</b>. Un byte es un número del 0 al 255 (8 bits). Un archivo de texto usa esos números para representar letras; un archivo de imagen los usa para colores y medidas. Lo que convierte esa fila de números en un «icono» es un <b>formato</b>: un acuerdo que dice qué significa cada byte según su posición.</p>
<p>Windows no usa un solo tamaño de icono: usa 16×16 píxeles en la barra de título, 24 o 32 en la barra de tareas, 48 en las carpetas con vista «iconos medianos» y hasta 256 en «iconos extra grandes». Si solo le dieras uno grande, Windows lo achicaría a su manera y se vería borroso. Por eso un <code>.ico</code> es un <b>paquete con el mismo dibujo en varios tamaños</b>, y Windows elige el que necesita en cada lugar.</p>
<p>El formato tiene tres partes, una detrás de otra:</p>
<svg viewBox="0 0 640 170" width="100%">
<rect x="0" y="0" width="640" height="170" rx="10" fill="#1C1740"/>
<rect x="15" y="40" width="70" height="60" rx="6" fill="#FF3BD4"/>
<text x="50" y="66" fill="#1C1740" font-size="13" text-anchor="middle" font-family="sans-serif">Cabecera</text>
<text x="50" y="84" fill="#1C1740" font-size="12" text-anchor="middle" font-family="sans-serif">6 bytes</text>
<rect x="95" y="40" width="40" height="60" rx="4" fill="#2F84FF"/>
<rect x="140" y="40" width="40" height="60" rx="4" fill="#2F84FF"/>
<rect x="185" y="40" width="40" height="60" rx="4" fill="#2F84FF"/>
<text x="250" y="75" fill="#C8BCF6" font-size="16" text-anchor="middle" font-family="sans-serif">...</text>
<rect x="275" y="40" width="40" height="60" rx="4" fill="#2F84FF"/>
<text x="205" y="125" fill="#C8BCF6" font-size="12" text-anchor="middle" font-family="sans-serif">7 entradas de 16 bytes (una por tamaño)</text>
<rect x="325" y="40" width="40" height="60" rx="4" fill="#A05CFF"/>
<rect x="370" y="40" width="50" height="60" rx="4" fill="#A05CFF"/>
<text x="445" y="75" fill="#C8BCF6" font-size="16" text-anchor="middle" font-family="sans-serif">...</text>
<rect x="470" y="40" width="155" height="60" rx="4" fill="#A05CFF"/>
<text x="475" y="125" fill="#C8BCF6" font-size="12" text-anchor="middle" font-family="sans-serif">7 imágenes PNG, de la de 16 px a la de 256 px</text>
<text x="15" y="25" fill="#C8BCF6" font-size="12" font-family="sans-serif">byte 0</text>
<text x="325" y="25" fill="#C8BCF6" font-size="12" font-family="sans-serif">byte 118</text>
<text x="560" y="25" fill="#C8BCF6" font-size="12" font-family="sans-serif">byte 57148</text>
</svg>
<table class="tabla">
<tr><th>Parte</th><th>Tamaño</th><th>Qué contiene</th></tr>
<tr><td><b>Cabecera</b> (<i>header</i>)</td><td>6 bytes</td><td>Tres números de 2 bytes: un 0 reservado, un 1 que significa «esto es un icono» (un 2 sería un cursor del ratón) y la cantidad de imágenes</td></tr>
<tr><td><b>Directorio</b>: una entrada por imagen</td><td>16 bytes cada una</td><td>Ancho, alto, colores de paleta, un reservado, planos, bits por píxel, <b>cuántos bytes</b> mide la imagen y <b>en qué byte</b> del archivo empieza</td></tr>
<tr><td><b>Imágenes</b></td><td>Lo que midan</td><td>Cada imagen completa. Desde Windows Vista, cada una puede ser un PNG entero metido tal cual</td></tr>
</table>
<p>El directorio funciona como el índice de un libro: «el capítulo de 48 píxeles mide 3153 bytes y empieza en el byte 3599». Así Windows puede saltar directo a la imagen que necesita sin leer las demás.</p>

<h3>Little-endian: los números «al revés»</h3>
<p>Un byte solo llega hasta 255. Para guardar números más grandes se juntan varios bytes: con 2 bytes se llega a 65 535 y con 4 a más de cuatro mil millones. Pero hay que acordar <b>en qué orden</b> se escriben esos bytes.</p>
<p>Piensa en el número 662 escrito en <b>hexadecimal</b> (base 16, capítulo 35): <code>0x0296</code>. Con 4 bytes es <code>00 00 02 96</code>. Hay dos costumbres:</p>
<ul>
<li><b>Big-endian</b> («el extremo grande primero»): se escribe como lo lees, <code>00 00 02 96</code>. Es lo que hace Java por defecto.</li>
<li><b>Little-endian</b> («el extremo pequeño primero»): se escribe empezando por el byte menos importante, <code>96 02 00 00</code>. Es lo que usan los procesadores Intel y AMD, y por eso los formatos nacidos en Windows, como <code>.ico</code>.</li>
</ul>
<p>Es como escribir una fecha: en Guatemala escribimos día/mes/año (lo pequeño primero) y en otros países año/mes/día (lo grande primero). Las dos formas son válidas, pero si lees una con la costumbre de la otra, te equivocas de fecha. El formato <code>.ico</code> exige little-endian, y como Java escribe big-endian, el generador tiene dos métodos propios, <code>corto</code> y <code>entero</code>, que escriben los bytes en el orden que Windows espera.</p>

<h2>Créalo</h2>
<p>El archivo va en la carpeta <code>herramientas</code>, que ya creaste en el capítulo 32. Desde PowerShell, en la carpeta del proyecto:</p>
<pre class="ps">cd $HOME\Proyectos\Totito
New-Item herramientas\GeneradorIcono.java</pre>
<p>Para editarlo en NetBeans: como <code>herramientas</code> no es una carpeta de código fuente del proyecto Maven, no aparece en la pestaña <i>Projects</i>. Abre la pestaña <i>Files</i> (<i>Window → Files</i>, Ctrl+2), despliega <code>Totito → herramientas</code> y haz doble clic en <code>GeneradorIcono.java</code>. Escribe el código que sigue. NetBeans puede marcar en rojo <code>Dibujo</code>, <code>Tema</code> e <code>Iconos</code> porque no sabe que se compilarán juntos; no hagas caso: lo que manda es el comando con que lo ejecutarás.</p>
""",
    "archivos": [
        {"ruta": "herramientas/GeneradorIcono.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1–L5</b> Los <code>import</code> de la parte gráfica (capítulo 11: un <code>import</code> le dice a Java el nombre completo de una clase que vas a usar con su nombre corto). <code>GradientPaint</code> es el degradado del fondo; <code>Graphics2D</code>, el pincel con que se dibuja (capítulo 37); <code>RenderingHints</code>, las opciones de calidad del pincel; <code>RoundRectangle2D</code>, el rectángulo de esquinas redondeadas que hace de fondo del icono; <code>BufferedImage</code>, una imagen en la memoria de la computadora sobre la que se puede dibujar sin que exista ninguna ventana. Todos vienen del módulo <code>java.desktop</code> de Java, el mismo que usa Swing.</p>
"""),
             ("import java.io.ByteArrayOutputStream", r"""
<p class="l"><b>L6–L10</b> Las clases del paquete <code>java.io</code> (<i>input/output</i>, entrada y salida), que sirven para leer y escribir bytes. Un <b>flujo</b> (<i>stream</i>) es como una manguera de bytes: tú echas bytes por un extremo y salen por el otro, hacia un archivo o hacia la memoria. <code>FileOutputStream</code> es una manguera que desemboca en un archivo del disco; <code>ByteArrayOutputStream</code>, una que desemboca en un arreglo de bytes en la memoria; <code>DataOutputStream</code> se enchufa delante de otra manguera y añade métodos cómodos como <code>writeByte</code>. <code>File</code> representa una ruta (un archivo o carpeta, exista o no) e <code>IOException</code> es la excepción que se lanza cuando algo falla al leer o escribir (disco lleno, sin permisos…).</p>
<p class="l"><b>L11</b> <code>ImageIO</code>, del paquete <code>javax.imageio</code>, sabe convertir una <code>BufferedImage</code> en un PNG o un JPG. No sabe escribir <code>.ico</code>: por eso existe este programa.</p>
"""),
             ("public class GeneradorIcono", r"""
<p class="l"><b>L13–L25</b> Un comentario de documentación (<code>/** ... */</code>, capítulo 11) que resume todo lo que vas a leer: qué archivos crea, qué es un <code>.ico</code>, por qué se arma a mano y cómo se ejecuta. Sin tildes, como todos los comentarios del proyecto, para evitar problemas de codificación. La línea 24 trae el comando con barras <code>/</code>; en Windows también funciona con <code>\</code>, que es lo que usarás en PowerShell. Fíjate en «despues de compilar el proyecto»: el generador usa <code>Dibujo</code>, <code>Tema</code> e <code>Iconos</code>, que tienen que estar ya compilados en <code>target\classes</code>.</p>
<p class="l"><b>L26</b> La clase. <code>public</code> y con el mismo nombre que el archivo, como exige Java (capítulo 62, error 6). No hereda de nada: no es una ventana, solo un programa con <code>main</code>.</p>
"""),
             ("private static final int[] TAMANOS", r"""
<p class="l"><b>L28</b> Los siete tamaños (en píxeles de lado) que llevará el <code>.ico</code>: los que Windows usa en distintos lugares. <code>private</code> porque nadie de fuera la necesita; <code>static</code> porque pertenece a la clase y no a un objeto (aquí nunca se hace <code>new GeneradorIcono()</code>); <code>final</code> porque no cambia: es una <b>constante</b> (capítulo 20). Por convención va en MAYÚSCULAS y sin eñe (<code>TAMANOS</code>, no <code>TAMAÑOS</code>), porque aunque Java acepta la ñ en nombres, evitarla ahorra sustos con codificaciones. Si quisieras añadir el de 20 píxeles, solo lo agregarías a esta lista: todo lo demás se adapta solo, porque el resto del código usa <code>TAMANOS.length</code> en vez de un 7 escrito a mano.</p>
<p class="l"><b>L30</b> El método <code>main</code>, la puerta de entrada (capítulo 11). Lo nuevo es <code>throws IOException</code>: escribir archivos puede fallar y Java obliga a decidir qué hacer. Aquí la decisión es «no lo atrapo; si falla, que el programa se detenga y muestre el stack trace». Para una herramienta que ejecutas tú, es razonable: si el disco está lleno, quieres enterarte, no que el programa siga como si nada.</p>
<p class="l"><b>L31</b> Una ruta <b>relativa</b>, <code>recursos</code>: relativa a la carpeta desde donde ejecutas el comando. Por eso hay que ejecutarlo desde la carpeta <code>Totito</code>; si lo ejecutaras desde otra, crearía una carpeta <code>recursos</code> donde estés.</p>
<p class="l"><b>L32</b> <code>mkdirs()</code> crea la carpeta si no existe (y las carpetas padre que falten). Si ya existe, no hace nada y no da error. Sin esta línea, la primera vez que lo ejecutes en un proyecto sin <code>recursos</code>, el <code>FileOutputStream</code> fallaría con «el sistema no puede encontrar la ruta especificada».</p>
"""),
             ("BufferedImage grande = dibujar(1024)", r"""
<p class="l"><b>L34</b> Dibuja el icono una sola vez, <b>grande</b>: 1024×1024 píxeles. Todo lo demás se obtiene achicando esta imagen. ¿Por qué tan grande, si el mayor tamaño del <code>.ico</code> es 256? Porque al reducir una imagen, cada píxel pequeño resulta del promedio de varios grandes, y eso suaviza los bordes del neón mucho mejor que dibujar directamente en pequeño. Es lo mismo que pasa con una foto: una tomada en alta resolución y luego achicada se ve mejor que una tomada directamente en baja.</p>
<p class="l"><b>L35</b> Una sola línea con tres llamadas anidadas; se leen de adentro hacia afuera. Primero <code>reducir(grande, 512)</code> crea una copia de 512×512; después <code>new File(carpeta, "totito.png")</code> forma la ruta <code>recursos\totito.png</code> (el constructor de dos argumentos junta carpeta y nombre con la barra correcta de cada sistema); por último <code>ImageIO.write(imagen, "png", archivo)</code> guarda la imagen en formato PNG. Este PNG de 512 sirve para el README, para la página del release y para otros sistemas (en Linux, jpackage pide el icono en PNG). Es la imagen del principio del capítulo.</p>
"""),
             ("byte[][] pngs", r"""
<p class="l"><b>L37</b> Un <b>arreglo de arreglos</b> de bytes (capítulo 15). <code>new byte[7][]</code> crea 7 «cajones» vacíos, sin decir aún cuánto mide cada uno, porque cada PNG medirá distinto (el de 16 píxeles ocupa unos cientos de bytes; el de 256, decenas de miles). <code>pngs[0]</code> será el PNG de 16 px, <code>pngs[1]</code> el de 24, etc., en el mismo orden que <code>TAMANOS</code>.</p>
<p class="l"><b>L38</b> Un <code>for</code> clásico (capítulo 14) que recorre los siete tamaños con el índice <code>i</code> de 0 a 6.</p>
<p class="l"><b>L39</b> Un <code>ByteArrayOutputStream</code> es un «archivo en la memoria»: todo lo que se escriba en él se va acumulando en un arreglo de bytes que crece solo. Lo usamos porque necesitamos el PNG <b>como bytes</b>, no como archivo suelto: más adelante hay que saber cuánto mide cada uno para escribir el directorio, y luego meterlos todos en el <code>.ico</code>.</p>
<p class="l"><b>L40</b> Achica la imagen grande al tamaño de esta vuelta y la escribe como PNG <b>dentro</b> de <code>bytes</code>. Es el mismo <code>ImageIO.write</code> de la línea 35, pero con una manguera hacia la memoria en vez de hacia un archivo: el método no sabe ni le importa adónde van los bytes. Esa es la gracia de los flujos.</p>
<p class="l"><b>L41–L42</b> <code>toByteArray()</code> entrega una copia de los bytes acumulados, que se guarda en el cajón <code>i</code>. Al terminar el bucle, <code>pngs</code> tiene los siete PNG listos en memoria.</p>
"""),
             ("try (DataOutputStream ico", r"""
<p class="l"><b>L44–L45</b> Aquí se abre el archivo <code>recursos\totito.ico</code> y se usa <b>try-with-resources</b> (capítulo 26): la variable declarada entre los paréntesis del <code>try</code> se <b>cierra automáticamente</b> al salir del bloque, tanto si todo sale bien como si ocurre una excepción. Cerrar un archivo es importante: hasta que se cierra, parte de lo escrito puede estar todavía en la memoria y no en el disco, y Windows lo mantiene bloqueado. Sin try-with-resources tendrías que escribir un <code>finally { ico.close(); }</code> y acordarte siempre. Fíjate en el «encadenado»: <code>new FileOutputStream(...)</code> crea la manguera al archivo (si ya existía, lo reemplaza) y <code>new DataOutputStream(...)</code> se pone delante para darnos <code>writeByte</code> y <code>write</code>. La línea 45 es la continuación de la 44: Java no termina una instrucción hasta el <code>;</code> o, como aquí, hasta la llave <code>{</code> del bloque.</p>
<p class="l"><b>L46</b> Comentario: los tres números de la cabecera.</p>
<p class="l"><b>L47–L49</b> La cabecera de 6 bytes, con tres números de 2 bytes escritos por el método <code>corto</code> (línea 102) en little-endian: <code>0</code> (reservado, siempre cero), <code>1</code> (tipo: icono) y <code>TAMANOS.length</code>, que vale 7. En el archivo real quedan así: <code>00 00 01 00 07 00</code>. Fíjate en el 1: se escribe <code>01 00</code>, el byte pequeño primero.</p>
"""),
             ("int posicion = 6", r"""
<p class="l"><b>L50–L51</b> Para escribir cada entrada del directorio hay que decir <b>en qué byte empieza</b> su imagen. Las imágenes van después de la cabecera (6 bytes) y de las 7 entradas (16 bytes cada una), así que la primera imagen empieza en el byte <code>6 + 16 × 7 = 118</code>. La variable <code>posicion</code> lleva la cuenta de dónde empieza la imagen que toca.</p>
<p class="l"><b>L52</b> Otro recorrido de los siete tamaños, ahora para escribir sus entradas.</p>
<p class="l"><b>L53</b> El <b>operador ternario</b> (capítulo 13): <code>condición ? valorSiSí : valorSiNo</code>. Si el tamaño es 256 o más, <code>lado</code> vale 0; si no, vale el tamaño. ¿Por qué? El ancho y el alto se guardan en un solo byte, que llega hasta 255. El 256 no cabe, y el formato acordó que «0 significa 256». Es como un cuentakilómetros de tres cifras que, al pasar de 999, vuelve a 000.</p>
"""),
             ("ico.writeByte(lado);", r"""
<p class="l"><b>L54–L55</b> Los dos primeros bytes de la entrada: ancho y alto. Los iconos son cuadrados, así que es el mismo número. <code>writeByte</code> escribe un solo byte: los 8 bits más bajos del número que recibe.</p>
<p class="l"><b>L56</b> Cantidad de colores de la paleta. Las imágenes antiguas de 16 o 256 colores usaban una «paleta», una lista fija de colores; las nuestras son de color completo con transparencia, así que va un 0 («sin paleta»).</p>
<p class="l"><b>L57</b> Un byte reservado: el formato pide que valga 0. Reservado significa «guardado para un uso futuro que nunca llegó»; hay que escribirlo igual para que todo lo demás quede en su posición.</p>
<p class="l"><b>L58</b> Planos de color: 1. Es un dato heredado de hardware de hace décadas; hoy siempre vale 1. Se escribe con <code>corto</code> porque ocupa 2 bytes.</p>
<p class="l"><b>L59</b> Bits por píxel: 32. Cada píxel usa 8 bits para el rojo, 8 para el verde, 8 para el azul y 8 para la <b>transparencia</b> (el canal alfa del capítulo 35). La transparencia es la que permite que las esquinas redondeadas del icono dejen ver el escritorio de fondo.</p>
"""),
             ("entero(ico, pngs[i].length)", r"""
<p class="l"><b>L60</b> Cuántos bytes mide esta imagen, en 4 bytes little-endian (método <code>entero</code>, línea 107). <code>pngs[i].length</code> es el largo del arreglo de bytes de ese PNG. Para el de 16 px son 662 bytes, que quedan escritos como <code>96 02 00 00</code>.</p>
<p class="l"><b>L61</b> En qué byte del archivo empieza esta imagen, también en 4 bytes. Para la primera, 118: <code>76 00 00 00</code> (0x76 es 118 en hexadecimal).</p>
<p class="l"><b>L62–L63</b> La siguiente imagen empezará justo donde termina esta: se suma su tamaño. Es una <b>suma acumulada</b>, como cuando apilas libros y anotas a qué altura empieza cada uno. Después de esta línea se cierra el <code>for</code>: en total se escribieron 7 × 16 = 112 bytes de directorio.</p>
"""),
             ("for (byte[] png : pngs)", r"""
<p class="l"><b>L64–L66</b> Por fin, las imágenes. Un <b>for-each</b> (capítulo 14): «para cada arreglo de bytes <code>png</code> dentro de <code>pngs</code>». <code>ico.write(png)</code> vuelca el PNG entero, tal cual, uno detrás de otro y en el mismo orden en que se escribieron sus entradas. Por eso las posiciones calculadas antes coinciden.</p>
<p class="l"><b>L67</b> La llave que cierra el <code>try</code>. Al pasar por aquí, Java llama solo a <code>ico.close()</code>: el archivo queda completo en el disco y desbloqueado.</p>
<p class="l"><b>L68</b> Un mensaje para que sepas que terminó. Sin él, el programa acabaría en silencio y no sabrías si hizo algo.</p>
"""),
             ("private static BufferedImage dibujar", r"""
<p class="l"><b>L71</b> Comentario de documentación del método: qué dibuja.</p>
<p class="l"><b>L72</b> Un método <code>private static</code> que recibe el lado en píxeles y <b>devuelve</b> (capítulo 16) la imagen dibujada.</p>
<p class="l"><b>L73</b> Crea un lienzo vacío de <code>lado × lado</code> píxeles. <code>TYPE_INT_ARGB</code> dice cómo se guarda cada píxel: un <code>int</code> con <b>A</b>lfa (transparencia), <b>R</b>ojo, <b>G</b>reen (verde) y <b>B</b>lue (azul). Una imagen nueva de este tipo empieza totalmente transparente, que es lo que queremos para las esquinas.</p>
<p class="l"><b>L74</b> Pide el pincel de la imagen (<code>getGraphics()</code>) y se lo pasa a <code>Dibujo.preparar</code> (capítulo 41), que devuelve un <code>Graphics2D</code> con el suavizado de bordes y la calidad alta activados. Es el mismo ajuste que usan todos los componentes del juego: por eso el icono tiene el mismo aspecto.</p>
<p class="l"><b>L75</b> Elige como «pintura» un <b>degradado vertical</b> (capítulo 35): desde el punto (0, 0) con <code>Tema.FONDO_ARRIBA</code> (<code>#1C1740</code>) hasta el punto (0, <code>lado</code>) con <code>Tema.FONDO_ABAJO</code> (<code>#0E0B24</code>). Son los mismos colores del fondo de las pantallas del juego.</p>
<p class="l"><b>L76</b> Rellena con ese degradado un rectángulo redondeado que ocupa toda la imagen. Los dos últimos números son el ancho y el alto del arco de las esquinas: 42 % del lado. Así queda la forma de «baldosa redondeada» de los iconos modernos. Lo que queda fuera del redondeo sigue transparente.</p>
"""),
             ("double margen", r"""
<p class="l"><b>L77</b> Un margen del 17 % del lado alrededor del logotipo, para que no toque los bordes. Con <code>lado = 1024</code>, son 174,08 píxeles.</p>
<p class="l"><b>L78</b> <code>scale</code> cambia la escala del pincel (capítulo 37, transformaciones): desde aquí, todo lo que se dibuje se multiplica por <code>lado / 256.0</code>, que con 1024 es 4. Una línea de 2 unidades saldrá de 8 píxeles. ¿Por qué? Los iconos de <code>Iconos</code> usan trazos de neón cuyo grosor y halo están pensados para tamaños de pantalla normales; si dibujaras el logotipo directamente a 1024, los trazos quedarían finísimos. Dibujándolo en un «mundo» de 256 unidades y ampliándolo, conserva sus proporciones. El <code>256.0</code> lleva <code>.0</code> para que la división sea con decimales: <code>1024 / 256</code> da 4 de todos modos, pero con un lado como 1000, la división entera daría 3 y deformaría todo.</p>
<p class="l"><b>L79</b> Como ahora todo se multiplica por 4, el margen hay que expresarlo en las nuevas unidades: 174,08 × 256 / 1024 = 43,52 unidades.</p>
<p class="l"><b>L80</b> Dibuja el logotipo del Totito (el tablero con la O, la O y la X, capítulo 42) en la posición (<code>m</code>, <code>m</code>), con un tamaño de <code>256 − 2m</code> unidades (el cuadrado que queda dentro de los márgenes) y en color lavanda (<code>#C8BCF6</code>). Es <b>la misma constante</b> <code>Iconos.LOGO</code> que usa el encabezado del juego: reutilización pura.</p>
<p class="l"><b>L81–L82</b> <code>dispose()</code> libera el pincel (capítulo 37: todo <code>Graphics</code> que creas tú, lo liberas tú) y se devuelve la imagen terminada.</p>
"""),
             ("private static BufferedImage reducir", r"""
<p class="l"><b>L85</b> El comentario resume la idea: achicar a la mitad una y otra vez en lugar de un solo salto. Abajo, en «Cómo funciona por dentro», verás por qué.</p>
<p class="l"><b>L86</b> Recibe una imagen y el lado deseado; devuelve otra imagen de ese tamaño. La original no se modifica.</p>
<p class="l"><b>L87</b> <code>actual</code> es la imagen de la que se parte en cada paso. Al principio, la original.</p>
<p class="l"><b>L88</b> <code>tamano</code> lleva el lado de la imagen que se va a crear. Empieza con el lado de la original (1024).</p>
<p class="l"><b>L89</b> Un bucle <b>do-while</b> (capítulo 14): primero hace y después pregunta. Se eligió así porque al menos una reducción hay que hacer siempre.</p>
<p class="l"><b>L90</b> El nuevo tamaño es la mitad del actual, <b>pero nunca menos que el objetivo</b>: <code>Math.max</code> devuelve el mayor de los dos. Con objetivo 24, la secuencia es 512, 256, 128, 64, 32 y entonces <code>max(24, 16)</code> da 24: el último paso no llega a la mitad, se queda justo en 24.</p>
<p class="l"><b>L91</b> Un lienzo nuevo, transparente, de ese tamaño.</p>
"""),
             ("Graphics2D g2 = menor.createGraphics()", r"""
<p class="l"><b>L92</b> El pincel del lienzo pequeño. <code>createGraphics()</code> es igual que <code>getGraphics()</code> pero ya devuelve un <code>Graphics2D</code>.</p>
<p class="l"><b>L93</b> Pide <b>interpolación bicúbica</b>: al achicar, cada píxel nuevo se calcula mirando los 16 píxeles vecinos (4×4) de la imagen anterior y mezclándolos con suavidad. La opción por defecto («vecino más próximo») tomaría solo uno y dejaría bordes en escalera.</p>
<p class="l"><b>L94</b> Dibuja la imagen <code>actual</code> estirada (en este caso, encogida) para que ocupe de (0, 0) a (<code>tamano</code>, <code>tamano</code>). El último argumento, <code>null</code>, es un «observador» que se usa con imágenes que se cargan poco a poco desde internet; aquí no hace falta.</p>
<p class="l"><b>L95–L96</b> Libera el pincel, y la imagen recién achicada pasa a ser la <code>actual</code> para la próxima vuelta.</p>
<p class="l"><b>L97</b> Se repite mientras el tamaño sea mayor que el objetivo. Cuando llega a él, sale.</p>
<p class="l"><b>L98</b> Devuelve la última imagen, que ya mide exactamente <code>lado</code>.</p>
"""),
             ("private static void corto", r"""
<p class="l"><b>L101</b> El comentario explica el porqué: el formato guarda los números en little-endian.</p>
<p class="l"><b>L102</b> Escribe un número en 2 bytes, el pequeño primero. Recibe el flujo donde escribir y el valor. Puede lanzar <code>IOException</code>, igual que <code>writeByte</code>, así que lo declara con <code>throws</code>.</p>
<p class="l"><b>L103</b> El byte <b>bajo</b>. <code>&amp;</code> es el <b>Y a nivel de bits</b>: compara bit por bit y solo deja en 1 los que están en 1 en ambos números. <code>0xFF</code> es 255, es decir, <code>11111111</code> en binario: ocho unos. Así que <code>valor &amp; 0xFF</code> se queda solo con los 8 bits de la derecha y borra el resto. Es como una plantilla de cartón con una ventana que solo deja ver las dos últimas cifras de un número. Con 662 (<code>0x0296</code>), da <code>0x96</code> (150).</p>
<p class="l"><b>L104</b> El byte <b>alto</b>. <code>&gt;&gt; 8</code> <b>desplaza</b> los bits 8 lugares a la derecha: los 8 de la derecha se caen y los demás bajan. Equivale a dividir entre 256 sin decimales. Con 662: <code>662 &gt;&gt; 8</code> da 2, y <code>&amp; 0xFF</code> asegura que quede en un byte. Se escriben <code>96</code> y luego <code>02</code>: little-endian.</p>
<p class="l"><b>L105</b> Cierre del método. ¿Por qué no usar <code>salida.writeShort(valor)</code>, que ya existe en <code>DataOutputStream</code>? Porque escribe en big-endian (<code>02 96</code>) y Windows leería 38 402 en vez de 662.</p>
"""),
             ("private static void entero", r"""
<p class="l"><b>L107</b> Escribe un número en 4 bytes little-endian, reutilizando <code>corto</code>.</p>
<p class="l"><b>L108</b> Primero la mitad baja: <code>valor &amp; 0xFFFF</code> deja los 16 bits de la derecha (<code>0xFFFF</code> son dieciséis unos) y <code>corto</code> los escribe en dos bytes.</p>
<p class="l"><b>L109</b> Después la mitad alta: desplaza 16 bits y se queda con esos 16. Para números pequeños como 662, la mitad alta es 0 y se escriben <code>00 00</code>. En total: <code>96 02 00 00</code>, del byte menos importante al más importante. Dividir un problema (4 bytes) en dos problemas que ya sabes resolver (2 bytes) es una técnica que usarás toda tu vida como programador.</p>
<p class="l"><b>L110–L111</b> Cierre del método y de la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>La reducción paso a paso</h3>
<p>El programa dibuja una sola imagen de 1024 píxeles y de ella saca todas las demás. Esta es la secuencia real de tamaños que recorre <code>reducir</code> para cada objetivo:</p>
<table class="tabla">
<tr><th>Objetivo</th><th>Pasos de reducción</th><th>Cantidad de pasos</th></tr>
<tr><td>512 (PNG)</td><td>1024 → 512</td><td>1</td></tr>
<tr><td>256</td><td>1024 → 512 → 256</td><td>2</td></tr>
<tr><td>128</td><td>1024 → 512 → 256 → 128</td><td>3</td></tr>
<tr><td>64</td><td>… → 128 → 64</td><td>4</td></tr>
<tr><td>48</td><td>… → 128 → 64 → 48</td><td>5</td></tr>
<tr><td>32</td><td>… → 64 → 32</td><td>5</td></tr>
<tr><td>24</td><td>… → 64 → 32 → 24</td><td>6</td></tr>
<tr><td>16</td><td>… → 64 → 32 → 16</td><td>6</td></tr>
</table>
<p>¿Por qué no un solo salto de 1024 a 16? La interpolación bicúbica mira 16 píxeles vecinos por cada píxel nuevo. Al pasar de 1024 a 16, cada píxel nuevo representa un cuadro de 64×64 = 4096 píxeles originales, y el algoritmo solo mira 16 de ellos: se salta casi todo. Una línea de neón delgada puede caer justo entre los píxeles mirados y desaparecer, o salir cortada a trozos. Al reducir a la mitad, cada píxel nuevo resume un cuadrado de 2×2, y los 16 vecinos que mira la bicúbica cubren de sobra esos 4: no se pierde nada. Cada paso conserva la información del anterior, como cuando doblas una hoja por la mitad varias veces en lugar de arrugarla de golpe.</p>

<h3>El archivo resultante, byte a byte</h3>
<p>Ejecuté el generador y examiné el <code>.ico</code> resultante. Así empiezan sus primeros bytes, en hexadecimal (cada pareja de cifras es un byte):</p>
<pre class="salida">00 00 01 00 07 00                                  ← cabecera: reservado 0, tipo 1, 7 imágenes
10 10 00 00 01 00 20 00 96 02 00 00 76 00 00 00    ← entrada 1: 16×16, 32 bits, 662 bytes, en el byte 118
18 18 00 00 01 00 20 00 aa 04 00 00 0c 03 00 00    ← entrada 2: 24×24, 1194 bytes, en el byte 780
...
00 00 00 00 01 00 20 00 df 80 00 00 5e 5e 00 00    ← entrada 7: 0 = 256×256, 32991 bytes, en el byte 24158
89 50 4e 47 0d 0a 1a 0a ...                        ← byte 118: empieza el primer PNG</pre>
<p>Compruébalo tú mismo con la entrada 1: <code>10</code> en hexadecimal es 16 (ancho y alto); <code>20</code> es 32 (bits por píxel); <code>96 02</code> leído al revés es <code>0x0296</code> = 662; <code>76</code> es 118. Y en el byte 118 aparece <code>89 50 4e 47</code>: los cuatro primeros bytes de todo archivo PNG, que en letras se leen «‰PNG». Es la «firma» del formato; por ella los programas reconocen un PNG aunque le cambies la extensión.</p>
<p>La tabla completa del directorio, con la suma acumulada de <code>posicion</code>:</p>
<table class="tabla">
<tr><th>Imagen</th><th>Tamaño del PNG (bytes)</th><th>Empieza en el byte</th><th>Cuenta</th></tr>
<tr><td>16×16</td><td>662</td><td>118</td><td>6 + 16 × 7</td></tr>
<tr><td>24×24</td><td>1 194</td><td>780</td><td>118 + 662</td></tr>
<tr><td>32×32</td><td>1 625</td><td>1 974</td><td>780 + 1 194</td></tr>
<tr><td>48×48</td><td>3 153</td><td>3 599</td><td>1 974 + 1 625</td></tr>
<tr><td>64×64</td><td>4 507</td><td>6 752</td><td>3 599 + 3 153</td></tr>
<tr><td>128×128</td><td>12 899</td><td>11 259</td><td>6 752 + 4 507</td></tr>
<tr><td>256×256</td><td>32 991</td><td>24 158</td><td>11 259 + 12 899</td></tr>
</table>
<p>El archivo termina en 24 158 + 32 991 = <b>57 149 bytes</b>, unos 56 KB, que es justo lo que mide <code>totito.ico</code>. Los números exactos de los PNG pueden variar un poco en tu equipo (dependen de cómo comprime <code>ImageIO</code>), pero la estructura es idéntica.</p>

<h2>Compila y prueba</h2>
<ol>
<li>Compila el proyecto en NetBeans: <i>Run → Clean and Build Project</i> (Shift+F11). Esto deja <code>Tema</code>, <code>Dibujo</code> e <code>Iconos</code> compilados en <code>target\classes</code>.</li>
<li>En PowerShell, desde la carpeta del proyecto, ejecuta el generador:</li>
</ol>
<pre class="ps">cd $HOME\Proyectos\Totito
java -cp target\classes herramientas\GeneradorIcono.java</pre>
<p>Este comando usa el <b>modo de archivo fuente</b> de Java (desde Java 11, y ya lo usaste en el capítulo 32): <code>java</code> recibe un <code>.java</code> en vez de una clase, lo compila en la memoria y lo ejecuta sin dejar ningún <code>.class</code>. La opción <code>-cp target\classes</code> le dice dónde encontrar las clases del juego que el generador usa. Tarda unos segundos (dibujar a 1024 píxeles con neón tiene su trabajo) y responde:</p>
<pre class="salida">Listo: recursos/totito.ico y recursos/totito.png</pre>
<p>Comprueba los archivos:</p>
<pre class="ps">Get-ChildItem recursos</pre>
<pre class="salida">Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        12/10/2026     14:33          57149 totito.ico
-a----        12/10/2026     14:33          74741 totito.png</pre>
<p>Ahora míralos con los ojos:</p>
<ul>
<li>Abre la carpeta con <code>explorer recursos</code>. En la vista <i>Iconos grandes</i>, el Explorador muestra <code>totito.ico</code> con el dibujo del Totito: está usando la imagen de 256 o la de 48 del paquete.</li>
<li>Cambia la vista a <i>Iconos pequeños</i>: ahora Windows elige la de 16 o la de 24. Si se ve nítida y no un borrón, la reducción por mitades hizo su trabajo.</li>
<li>Doble clic en <code>totito.png</code> abre la imagen de 512 en la aplicación Fotos.</li>
</ul>
<p>Comprobé en este libro que el programa, ejecutado dos veces, produce archivos <b>idénticos byte a byte</b> a los del proyecto de referencia: dibujar con código es reproducible.</p>

<h3>Errores típicos</h3>
<table class="tabla">
<tr><th>Lo que ves</th><th>Por qué</th><th>Solución</th></tr>
<tr><td><code>error: cannot find symbol ... symbol: variable Dibujo</code> (y lo mismo con <code>Tema</code> e <code>Iconos</code>)</td><td>Ejecutaste sin <code>-cp target\classes</code>, o sin haber compilado antes</td><td>Clean and Build, y el comando completo con <code>-cp</code></td></tr>
<tr><td><code>Error: Could not find or load main class herramientas.GeneradorIcono.java</code></td><td>No estás en la carpeta <code>Totito</code>: Java no encuentra el archivo y cree que le diste el nombre de una clase</td><td><code>cd $HOME\Proyectos\Totito</code></td></tr>
<tr><td>La carpeta <code>recursos</code> aparece en otro lugar</td><td>Lo ejecutaste desde otra carpeta: la ruta es relativa</td><td>Borra esa carpeta y ejecuta desde <code>Totito</code></td></tr>
<tr><td>El Explorador sigue mostrando un icono viejo</td><td>Windows guarda una caché de iconos y a veces tarda en refrescarla</td><td>Pulsa F5 en el Explorador; si persiste, no importa: el archivo es correcto</td></tr>

</table>

<h2>Alternativas: otras formas de conseguir un .ico</h2>
<p>En otros proyectos no tendrás un logotipo dibujado con código. Estas son las vías habituales, de la más sencilla a la más profesional:</p>
<ul>
<li><b>Un convertidor en línea.</b> Hay muchas páginas que convierten PNG a ICO (busca «png to ico»). Sube un PNG cuadrado, de 256×256 o mayor, con fondo transparente, y marca todos los tamaños que ofrezca (16, 24, 32, 48, 64, 128, 256). Cuidado: sube solo imágenes tuyas y que no sean privadas, y descarga solo el <code>.ico</code>; si la página te pide instalar algo, ciérrala.</li>
<li><b>GIMP</b> (gratuito; busca su identificador con <code>winget search GIMP</code> e instálalo con <code>winget install --id &lt;el-id-que-aparezca&gt; -e</code>, o descárgalo de gimp.org). Abre tu PNG, y por cada tamaño crea una capa con la imagen reducida (<i>Capa → Escalar capa</i>). Luego <i>Archivo → Exportar como…</i>, escribe <code>totito.ico</code> y GIMP guarda <b>cada capa como una imagen del icono</b>; en el cuadro de exportación puedes marcar que la de 256 se guarde comprimida (PNG). Es exactamente lo que hace nuestro programa, a mano.</li>
<li><b>ImageMagick</b>, un programa de línea de comandos para imágenes (<code>winget install --id ImageMagick.ImageMagick -e</code>). Con una sola orden genera todos los tamaños:
<pre class="ps">magick recursos\totito.png -define icon:auto-resize=256,128,64,48,32,24,16 recursos\totito.ico</pre>
Comprueba que funcione en tu equipo antes de confiar en él para un proyecto.</li>
<li><b>Un diseñador.</b> Para un producto comercial, un icono hecho a mano por alguien que sepa, con versiones especiales para 16 y 32 píxeles (a esos tamaños a veces conviene simplificar el dibujo, no solo achicarlo).</li>
</ul>
<div class="caja consejo"><b>Reglas de un buen icono.</b> Que se reconozca a 16 píxeles (pocos detalles, trazos gruesos); que tenga contraste con fondos claros y oscuros (el Totito usa una baldosa oscura propia para no depender del fondo del escritorio); cuadrado y con transparencia en lo que no es dibujo; y coherente con el programa (los mismos colores de la interfaz, capítulo 35).</div>

<div class="caja git"><b>Git</b> El icono y su generador son parte del proyecto: cualquiera que clone el repositorio debe poder fabricar el <code>.exe</code> con su icono. Según el plan del libro, este es el commit del capítulo:
<pre class="ps">git status
git add herramientas\GeneradorIcono.java recursos\totito.ico recursos\totito.png
git commit -m "Icono del programa"
git push</pre>
¿No dijimos en el capítulo 63 que los archivos generados no se suben? Aquí hacemos una excepción razonable: el <code>.ico</code> y el <code>.png</code> son pequeños, cambian casi nunca y los necesitan otros pasos (jpackage, el README, la página del release). Obligar a cada persona a ejecutar el generador antes de empaquetar sería un paso más para equivocarse. El <code>.jar</code>, en cambio, cambia en cada compilación: ese sí se queda fuera.</div>

<div class="caja hito"><b>Hito</b> El Totito tiene cara propia: un <code>totito.ico</code> con siete tamaños, listo para que jpackage lo grabe dentro de <code>Totito.exe</code> en el próximo capítulo.</div>

<h2>Resumen</h2>
<ul>
<li>Un <code>.ico</code> es un paquete con el mismo dibujo en varios tamaños: cabecera de 6 bytes, una entrada de 16 bytes por imagen y luego las imágenes (aquí, PNG completos).</li>
<li>Cada entrada dice ancho, alto, bits por píxel, cuánto mide la imagen y en qué byte empieza; el ancho 256 se guarda como 0.</li>
<li>El formato usa <b>little-endian</b> (el byte pequeño primero); Java escribe big-endian, por eso existen <code>corto</code> y <code>entero</code>, hechos con <code>&amp; 0xFF</code> y <code>&gt;&gt; 8</code>.</li>
<li><code>ByteArrayOutputStream</code> escribe en la memoria; <code>FileOutputStream</code> en un archivo; <code>DataOutputStream</code> añade métodos cómodos encima de cualquiera.</li>
<li>try-with-resources cierra el archivo automáticamente, incluso si hay un error.</li>
<li>Se dibuja una vez en grande (1024 px) y se reduce a la mitad repetidas veces con interpolación bicúbica para que los tamaños pequeños queden nítidos.</li>
<li>Se ejecuta con <code>java -cp target\classes herramientas\GeneradorIcono.java</code> desde la carpeta del proyecto, después de compilar.</li>
<li>Alternativas: convertidores en línea, GIMP (una capa por tamaño) o ImageMagick.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>El icono de cualquier programa tuyo</b>: copia <code>GeneradorIcono</code>, cambia solo el método <code>dibujar</code> por tu propio dibujo (o por <code>ImageIO.read(new File("logo.png"))</code> para partir de una imagen) y obtendrás un <code>.ico</code> correcto con siete tamaños. El resto del programa no depende de qué dibujes.</li>
<li><b>Miniaturas para una galería o una tienda</b>: el método <code>reducir</code> sirve tal cual para generar miniaturas nítidas de fotos de productos, de la misma forma que los sitios web generan las imágenes pequeñas de su catálogo.</li>
<li><b>Leer o escribir otros formatos binarios</b>: los archivos <code>.bmp</code>, <code>.wav</code> (sonido) y <code>.zip</code> también son little-endian, con una cabecera y bloques con posiciones. Con <code>corto</code>, <code>entero</code> y la idea de «posición acumulada» puedes fabricar un <code>.wav</code> con un pitido para el Totito o entender cómo está hecho un archivo cualquiera.</li>
<li><b>Herramientas de desarrollo propias</b>: cualquier tarea repetitiva de tu proyecto (generar datos de prueba, redimensionar imágenes, renombrar archivos) puede ser un programa en <code>herramientas\</code> que se ejecuta con <code>java -cp target\classes</code>. Queda guardado en Git y documentado, en vez de depender de que te acuerdes de los pasos.</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Calcula a mano cómo se escribe en little-endian, con 4 bytes, el número 24158 (la posición de la imagen de 256). Comprueba tu respuesta con la última entrada del volcado hexadecimal de este capítulo. Pista: 24158 = 0x5E5E.</li>
<li>Añade el tamaño 20 a <code>TAMANOS</code> (entre 16 y 24), ejecuta el generador y comprueba que el <code>.ico</code> creció. ¿Cuántos bytes mide ahora el directorio? ¿En qué byte empieza la primera imagen? Después deshaz el cambio con <code>git restore herramientas\GeneradorIcono.java</code> y vuelve a ejecutar el generador.</li>
<li>Cambia temporalmente <code>Tema.LAVANDA</code> por <code>Tema.ROSA</code> en la línea 80, genera el icono y míralo. Prueba también con <code>Tema.CIAN</code>. Luego restaura con <code>git restore</code> y vuelve a generar. Pista: después de cada cambio en <code>herramientas</code> no hace falta recompilar el proyecto, pero si cambias <code>Tema.java</code> sí.</li>
<li>Escribe en <code>herramientas\</code> un programa <code>LeerIco.java</code> que abra <code>recursos\totito.ico</code>, lea la cabecera y las siete entradas, e imprima para cada una «ancho × alto, tamaño, posición». Pista: <code>byte[] d = java.nio.file.Files.readAllBytes(java.nio.file.Path.of("recursos", "totito.ico"));</code> y, para leer 2 bytes little-endian en la posición <code>p</code>: <code>(d[p] &amp; 0xFF) | ((d[p + 1] &amp; 0xFF) &lt;&lt; 8)</code>.</li>
<li>Reto: modifica una copia del generador para que, en lugar de reducir por mitades, haga un solo salto (<code>tamano = lado;</code> en la línea 90). Genera ambos iconos, ábrelos en vista de iconos pequeños y compara la imagen de 16 píxeles. Explica la diferencia con lo que leíste en «Cómo funciona por dentro».</li>
</ol></div>
""",
}
