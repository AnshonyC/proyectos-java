# -*- coding: utf-8 -*-
CAPITULO = {
    "numero": 53,
    "titulo": "PasoInstruccion.java: un paso numerado con texto HTML",
    "antes": r"""
<p class="entrada">La pantalla «Cómo jugar» explica las reglas en tres pasos numerados: un círculo de neón con el
número y, a la derecha, una frase de dos líneas donde la X sale en rosa y la O en azul. En este capítulo construyes
ese paso combinando dos técnicas: el círculo lo <b>dibujas tú</b> y el texto lo pone un <code>JLabel</code> que
entiende <b>HTML</b>.</p>

<h2>Por qué existe este archivo</h2>
<p>En el diseño <code>diseno/instrucciones.jpg</code> (capítulo 34) los tres pasos tienen la misma forma y solo
cambian el número, el color del círculo y el texto. Tres cosas iguales con datos distintos: una clase y tres
objetos.</p>
<p>La parte difícil es el texto. Tiene <b>dos líneas</b> y, dentro de la frase, la X y la O tienen <b>otro color</b>
y van en negrita. Con <code>drawString</code> tendrías que partir la frase en trozos, medir cada uno con
<code>FontMetrics</code>, cambiar de color entre trozo y trozo y calcular a mano dónde empieza la segunda línea. Un
<code>JLabel</code> de Swing ya sabe hacer todo eso si le das el texto en HTML, el mismo lenguaje de las páginas
web. Así que cada herramienta hace lo que mejor sabe: <code>Graphics2D</code> el círculo de neón, y
<code>JLabel</code> el texto con formato.</p>
<figure><img src="capturas/2-instrucciones.png"><figcaption>Los tres PasoInstruccion dentro de la tarjeta «Cómo
jugar»: círculos rosa, morado y azul, y en el primero la X rosa y la O azul dentro de la frase.</figcaption></figure>

<h2>Qué vas a aprender</h2>
<ul>
<li>A crear un <code>JPanel</code> sin gestor de distribución pasando <code>null</code> a su constructor.</li>
<li>Por qué un panel que se dibuja a medias debe ser <b>no opaco</b> (<code>setOpaque(false)</code>).</li>
<li>Qué es un <code>JLabel</code> y cómo mostrar texto con formato usando HTML (<code>&lt;br&gt;</code>,
<code>&lt;b&gt;</code>, <code>&lt;font color&gt;</code>).</li>
<li>A combinar dibujo propio y componentes de Swing en un mismo panel.</li>
<li>A centrar un número dentro de un círculo, en horizontal y en vertical.</li>
</ul>

<h2>El plano de un paso, en píxeles</h2>
<p>Cada paso mide <b>ancho × 54</b>; el ancho lo decide la pantalla (en «Cómo jugar» es 400).</p>
<table class="tabla">
<tr><th>Parte</th><th>Posición (con ancho 400)</th></tr>
<tr><td>Círculo de neón</td><td>rectángulo envolvente (8, 8) de 38 × 38; centro en (27, 27)</td></tr>
<tr><td>Número</td><td>centrado en el círculo; para «1», x ≈ 22 y línea base ≈ 33,5</td></tr>
<tr><td>Texto (<code>JLabel</code>)</td><td>rectángulo (68, 0) de 332 × 54, con el texto centrado en vertical</td></tr>
</table>

<h2>Créalo</h2>
<ol>
<li>NetBeans: <i>&lt;default package&gt;</i> → <i>New → Java Class…</i> → <code>PasoInstruccion</code> →
<i>Finish</i>. Borra la plantilla y escribe el código.</li>
<li>Alternativa: <code>New-Item src\PasoInstruccion.java</code>.</li>
</ol>
""",
    "archivos": [
        {"ruta": "src/PasoInstruccion.java",
         "bloques": [
             (None, r"""
<p class="l"><b>L1</b> <code>java.awt.Color</code>: el color del círculo.</p>
<p class="l"><b>L2</b> <code>java.awt.Font</code>: para <code>Font.PLAIN</code> (texto) y <code>Font.BOLD</code>
(número).</p>
<p class="l"><b>L3</b> <code>java.awt.FontMetrics</code>: medir el número para centrarlo.</p>
<p class="l"><b>L4–L5</b> <code>Graphics</code> y <code>Graphics2D</code>: el pincel.</p>
<p class="l"><b>L6</b> <code>java.awt.geom.Ellipse2D</code>: el círculo.</p>
<p class="l"><b>L7</b> <code>javax.swing.JLabel</code>: la <b>etiqueta</b> de Swing, un componente que muestra un
texto (y opcionalmente una imagen) que el usuario no puede editar. Es el componente de texto más usado: títulos,
rótulos de formularios, mensajes.</p>
<p class="l"><b>L8</b> <code>javax.swing.JPanel</code>: esta vez sí heredamos de un panel, porque el paso
<b>contiene</b> otro componente (el <code>JLabel</code>).</p>
"""),
             ("public class PasoInstruccion", r"""
<p class="l"><b>L10–L14</b> Comentario de la clase. Explica por qué el texto es HTML: para colorear la X y la O
y partir la línea. En la línea 13 verás <code>&amp;lt;br&amp;gt;</code> en vez de <code>&lt;br&gt;</code>: los
comentarios <code>/** */</code> se pueden convertir en documentación web con la herramienta <code>javadoc</code>, y
allí un <code>&lt;br&gt;</code> escrito tal cual se interpretaría como un salto de línea en vez de mostrarse. Con
<code>&amp;lt;</code> («menor que») y <code>&amp;gt;</code> («mayor que») se muestra el texto literal.</p>
<p class="l"><b>L15</b> <code>public class PasoInstruccion extends JPanel {</code> un panel, porque tendrá un hijo
(la etiqueta). Recuerda la regla del capítulo 50: <code>JPanel</code> si contiene, <code>JComponent</code> si solo
dibuja.</p>
"""),
             ("private static final int ALTO", r"""
<p class="l"><b>L17</b> <code>ALTO = 54</code>: alto de cada paso; caben dos líneas de texto de 17 puntos con
aire.</p>
<p class="l"><b>L18</b> <code>DIAMETRO = 38</code>: tamaño del círculo.</p>
<p class="l"><b>L20</b> <code>private final int numero;</code> el número que va dentro del círculo (1, 2 o 3).
Se guarda porque <code>paintComponent</code> lo necesita cada vez que dibuja.</p>
<p class="l"><b>L21</b> <code>private final Color color;</code> el color del círculo. El texto, en cambio, no se
guarda en ningún campo: se le entrega a la etiqueta y ella lo recuerda.</p>
"""),
             ("public PasoInstruccion(", r"""
<p class="l"><b>L23</b> <code>public PasoInstruccion(int numero, Color color, String html, int ancho) {</code>
cuatro parámetros: número, color, el texto en HTML y el ancho del paso. El ancho viene de fuera porque depende de
la pantalla: la tarjeta de «Cómo jugar» usa 400 para todos.</p>
<p class="l"><b>L24</b> <code>super(null);</code> llama al constructor <code>JPanel(LayoutManager)</code>
pasándole <code>null</code>: el panel nace <b>sin</b> gestor de distribución. Es lo mismo que el
<code>setLayout(null)</code> del capítulo 49, pero en un solo paso (lo hiciste igual en <code>Encabezado</code>,
capítulo 45). Sin gestor, la etiqueta se colocará exactamente donde digamos con <code>setBounds</code>. Si quitaras
esta línea, el <code>FlowLayout</code> por defecto ignoraría nuestro <code>setBounds</code> y pondría la etiqueta
centrada arriba con su tamaño preferido.</p>
<p class="l"><b>L25–L26</b> Guardan el número y el color.</p>
<p class="l"><b>L27</b> <code>setOpaque(false);</code> un <code>JPanel</code> nace <b>opaco</b>: le promete a Swing
que pintará todos sus píxeles, y Swing, confiado, no pinta lo que hay detrás. Nuestro paso solo dibuja un círculo y
un número; el resto debe dejar ver la tarjeta de cristal. Con <code>setOpaque(false)</code> le decimos a Swing «soy
transparente, pinta primero lo de atrás». Sin esta línea, Swing creería que el paso cubre todo su
rectángulo y, cuando repintara solo el paso, no repintaría la tarjeta de detrás: en las zonas que no dibujamos
podrían quedar manchas o restos de dibujos anteriores. Y si además llamaras a <code>super.paintComponent</code>, el
panel opaco se rellenaría con su color de fondo por defecto (un gris claro) y taparía el cristal.</p>
<p class="l"><b>L28</b> <code>setAlignmentX(CENTER_ALIGNMENT);</code> centrado horizontal. Aquí no es un detalle:
la pantalla de instrucciones mete los pasos directamente en su tarjeta con <code>tarjeta.add</code>, sin pasar por
<code>PantallaBase.agregar</code> (capítulo 55), que es la que centra; así que el paso tiene que pedirlo él.</p>
<p class="l"><b>L29</b> Tamaño fijo: <code>ancho</code> × 54.</p>
"""),
             ("JLabel texto", r"""
<p class="l"><b>L31</b> <code>JLabel texto = new JLabel("&lt;html&gt;" + html + "&lt;/html&gt;");</code> crea la
etiqueta. Si el texto de un <code>JLabel</code> empieza por <code>&lt;html&gt;</code>, Swing lo interpreta como HTML
sencillo (más o menos el de las páginas web de los años noventa): <code>&lt;br&gt;</code> parte la línea,
<code>&lt;b&gt;</code> pone negrita, <code>&lt;font color='#FF3BD4'&gt;</code> cambia el color. Lo envolvemos aquí
para que quien crea el paso escriba solo el contenido. Es una variable <b>local</b>, no un campo: después de
agregarla no la volvemos a tocar.</p>
<p class="l"><b>L32</b> <code>texto.setFont(Tema.fuente(Font.PLAIN, 17f));</code> fuente base de la etiqueta:
normal de 17 puntos. Las etiquetas <code>&lt;b&gt;</code> del HTML ponen en negrita solo su trozo.</p>
<p class="l"><b>L33</b> <code>texto.setForeground(Tema.TEXTO);</code> color base del texto: blanco. Los trozos con
<code>&lt;font color&gt;</code> lo sustituyen.</p>
<p class="l"><b>L34</b> <code>texto.setBounds(DIAMETRO + 30, 0, ancho - DIAMETRO - 30, ALTO);</code> coloca la
etiqueta: empieza en x = 38 + 30 = <b>68</b> (el círculo acaba en 8 + 38 = 46, así que quedan 22 de aire), arriba
del todo, con 400 − 68 = <b>332</b> de ancho y todo el alto (54). Un <code>JLabel</code> centra su texto en
vertical por defecto, así que las dos líneas quedan a media altura del paso, alineadas con el círculo.</p>
<p class="l"><b>L35</b> <code>add(texto);</code> mete la etiqueta en el panel. Sin esta línea el texto no
aparecería.</p>
"""),
             ("protected void paintComponent", r"""
<p class="l"><b>L38–L39</b> <code>paintComponent</code>: dibujamos el círculo y el número. No llamamos a
<code>super.paintComponent</code>: en un panel no opaco solo pintaría el fondo, que no queremos. La etiqueta no
hay que dibujarla: Swing pinta los hijos después de <code>paintComponent</code>.</p>
<p class="l"><b>L40</b> Copia suavizada del pincel.</p>
<p class="l"><b>L41</b> <code>double y = (getHeight() - DIAMETRO) / 2.0;</code> la y del círculo para que quede
centrado en vertical: (54 − 38) / 2 = <b>8</b>.</p>
<p class="l"><b>L42</b> <code>Dibujo.trazoNeon(g2, new Ellipse2D.Double(8, y, DIAMETRO, DIAMETRO), color, 2f, 0.9f);</code>
el círculo de neón: rectángulo envolvente desde (8, 8) de 38 × 38, trazo de 2 e intensidad 0,9. La x es 8 (y no
0) para que el halo, que se extiende varios píxeles hacia fuera, no se corte en el borde izquierdo del panel.</p>
"""),
             ("g2.setFont", r"""
<p class="l"><b>L43</b> Número en negrita de 18 puntos.</p>
<p class="l"><b>L44</b> Medidas de esa fuente.</p>
<p class="l"><b>L45</b> <code>String n = String.valueOf(numero);</code> el número como texto: 1 → "1".</p>
<p class="l"><b>L46</b> Blanco.</p>
<p class="l"><b>L47</b> <code>g2.drawString(n, 8 + (DIAMETRO - fm.stringWidth(n)) / 2f, Dibujo.lineaBaseCentrada(fm, getHeight() / 2f));</code>
centra el número en las dos direcciones. En horizontal: el círculo empieza en 8 y mide 38; si «1» mide unos 10
píxeles, x = 8 + (38 − 10) / 2 = <b>22</b>. En vertical, <code>Dibujo.lineaBaseCentrada</code> (capítulo 41)
calcula la línea base para que las letras queden centradas sobre y = 27: suma al centro la mitad de lo que sube la
fuente menos lo que baja (con ascenso 17 y descenso 4, 27 + 6,5 = <b>33,5</b>). Con un número de dos cifras («10»)
la misma línea lo seguiría centrando, porque mide su ancho real.</p>
<p class="l"><b>L48</b> Libera la copia del pincel.</p>
<p class="l"><b>L49–L50</b> Cierran el método y la clase.</p>
"""),
         ]},
    ],
    "despues": r"""
<h2>Cómo funciona por dentro</h2>
<h3>1. El texto que recibe la etiqueta</h3>
<p>En el capítulo 57, la pantalla de instrucciones prepara dos trocitos de HTML con los colores del tema
(<code>Tema.hex</code>, capítulo 40, convierte un <code>Color</code> en texto «#RRGGBB»):</p>
<pre class="java">String x = "&lt;font color='" + Tema.hex(Tema.ROSA) + "'&gt;&lt;b&gt;X&lt;/b&gt;&lt;/font&gt;";
String o = "&lt;font color='" + Tema.hex(Tema.AZUL) + "'&gt;&lt;b&gt;O&lt;/b&gt;&lt;/font&gt;";
tarjeta.add(new PasoInstruccion(1, Tema.ROSA,
        "Dos jugadores se turnan&lt;br&gt;para marcar " + x + " y " + o + ".", ANCHO_PASOS));</pre>
<p>Con <code>Tema.hex(Tema.ROSA)</code> = "#FF3BD4" y <code>Tema.hex(Tema.AZUL)</code> = "#2F84FF", la línea 31 del
paso construye este texto final:</p>
<pre class="texto">&lt;html&gt;Dos jugadores se turnan&lt;br&gt;para marcar &lt;font color='#FF3BD4'&gt;&lt;b&gt;X&lt;/b&gt;&lt;/font&gt; y &lt;font color='#2F84FF'&gt;&lt;b&gt;O&lt;/b&gt;&lt;/font&gt;.&lt;/html&gt;</pre>
<p>Y la etiqueta lo muestra así: en la primera línea «Dos jugadores se turnan»; en la segunda «para marcar», una
<b>X</b> rosa en negrita, «y», una <b>O</b> azul en negrita y un punto. Todo en blanco y 17 puntos salvo lo que el
HTML cambia.</p>

<h3>2. Quién pinta qué, y en qué orden</h3>
<ol>
<li>Como el paso no es opaco, Swing pinta primero lo que hay detrás (la tarjeta de cristal).</li>
<li><code>paintComponent</code> del paso: círculo de neón en (8, 8) y el número centrado.</li>
<li>Swing pinta el hijo: el <code>JLabel</code> en (68, 0), con su HTML.</li>
</ol>
<p>Los tres pasos, uno debajo de otro, ocupan 3 × 54 = 162 píxeles dentro de la tarjeta.</p>

<div class="caja cuidado"><b>HTML y texto del usuario</b> El HTML en un <code>JLabel</code> es cómodo, pero nunca
metas ahí <b>sin limpiar</b> un texto que escribió el usuario. Si alguien se llama «&lt;b&gt;Ana», la etiqueta lo
interpretaría como formato. Aquí no pasa porque los textos de los pasos los escribimos nosotros. Si algún día
necesitas mostrar texto del usuario en HTML, sustituye antes <code>&lt;</code> por <code>&amp;lt;</code> y
<code>&gt;</code> por <code>&amp;gt;</code>.</div>

<h2>Compila y prueba</h2>
<p><i>Run → Clean and Build Project</i> → <code>BUILD SUCCESS</code>. Los pasos se verán en la pantalla de
instrucciones (capítulo 57) y uno de ellos en la pantalla de prueba del capítulo 56.</p>
<table class="tabla">
<tr><th>Problema</th><th>Causa y solución</th></tr>
<tr><td>(al verlo) aparecen las etiquetas <code>&lt;br&gt;</code> escritas en vez de saltar de línea</td><td>El
texto no empieza exactamente por <code>&lt;html&gt;</code>. Revisa la línea 31.</td></tr>
<tr><td>(al verlo) manchas o restos de dibujo alrededor del círculo, sobre todo al repintar</td><td>Falta <code>setOpaque(false)</code>.</td></tr>
<tr><td>(al verlo) el texto sale arriba y centrado, encima del círculo</td><td>Falta <code>super(null)</code>: el
<code>FlowLayout</code> por defecto ignora el <code>setBounds</code>.</td></tr>
<tr><td>(al verlo) el halo del círculo se ve cortado a la izquierda</td><td>Pusiste el círculo en x = 0; déjalo en
8.</td></tr>
</table>

<div class="caja git"><b>Git</b>
<pre class="ps">git add src\PasoInstruccion.java
git commit -m "PasoInstruccion: paso numerado"
git push</pre></div>

<h2>Resumen</h2>
<ul>
<li><code>PasoInstruccion</code> es un <code>JPanel</code> sin gestor (<code>super(null)</code>) que contiene un
<code>JLabel</code> colocado con <code>setBounds</code>.</li>
<li>Un panel que no pinta todos sus píxeles debe ser no opaco: <code>setOpaque(false)</code>.</li>
<li>Un <code>JLabel</code> cuyo texto empieza por <code>&lt;html&gt;</code> entiende HTML sencillo: saltos de línea,
negrita, colores.</li>
<li>Se combinan las dos técnicas: dibujo propio para lo decorativo, componentes de Swing para el texto con
formato.</li>
<li>Para centrar un número en un círculo: en horizontal con <code>stringWidth</code>, en vertical con
<code>lineaBaseCentrada</code>.</li>
</ul>

<div class="caja aplica"><b>Aplícalo fuera del Totito</b>
<ul>
<li><b>Asistentes paso a paso</b>: la instalación de un programa, el registro de una cuenta o el pago en una
tienda («1 Carrito, 2 Envío, 3 Pago»), cada paso con su círculo numerado.</li>
<li><b>Recetas y manuales</b>: los pasos de una receta de cocina o de un tutorial, con palabras clave resaltadas en
negrita o en color.</li>
<li><b>Mensajes con formato</b>: «Total a pagar: <b>Q150.00</b>» o una advertencia con una palabra en rojo, con
<code>&lt;html&gt;</code> en una etiqueta, sin dibujar a mano.</li>
<li><b>Paneles mixtos</b>: un icono dibujado a mano junto a componentes normales (una tarjeta de contacto con su
inicial en un círculo y el nombre en un <code>JLabel</code>).</li>
</ul></div>

<div class="caja ejercicio"><b>Ejercicios</b>
<ol>
<li>Si <code>DIAMETRO</code> fuera 44, ¿dónde empezaría el círculo (y) y dónde la etiqueta (x)? ¿Cuánto mediría
de ancho la etiqueta con un paso de 400?</li>
<li>Haz que el número se escriba del mismo color que el círculo en vez de blanco.</li>
<li>Cuando tengas la pantalla del capítulo 57, cambia el texto del paso 2 para que «línea de 3» salga en cursiva
(<code>&lt;i&gt;</code>…<code>&lt;/i&gt;</code>).</li>
<li>Con la vista previa del capítulo 56, quita <code>setOpaque(false)</code> y agrega
<code>super.paintComponent(g);</code> como primera línea de <code>paintComponent</code>. ¿Qué aparece detrás del
paso y por qué? Después deja el archivo como estaba.</li>
<li>Reto: agrega un parámetro <code>boolean hecho</code> y, si es <code>true</code>, dibuja dentro del círculo una
palomita (✓) con dos líneas en lugar del número, como en un asistente donde ese paso ya se completó.</li>
</ol></div>
""",
}
