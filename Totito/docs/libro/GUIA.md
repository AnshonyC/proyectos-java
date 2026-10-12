# Guía para redactar el libro «Java desde cero con el Totito»

Libro en español para aprender **desde cero absoluto** Java, programación orientada a objetos (POO),
diseño de interfaces y color, Git/GitHub y distribución de programas, usando como ejemplo de
principio a fin el **Juego del Totito** (tres en raya / tic-tac-toe) con interfaz neón en Swing.
El lector termina con un totito funcional y estético, instalado como `.exe` y publicado en GitHub.

El dueño pidió explícitamente: que se explique **cada línea de código**, **por qué** se crea cada
archivo, la **lógica** detrás de todo, el **diseño** y cómo se implementa, instalación con comandos
de **PowerShell**, Git/GitHub con **buenas prácticas**, exportar a **.exe con icono e instalador**,
y **cómo aplicar cada conocimiento en otros proyectos**. No importa cuántas páginas tenga.

## Regla de oro (pedido textual del dueño)

«La idea es entender exactamente **cómo, por qué y para qué** sirvió cada cosa, **por mínima que
sea**»: qué es una clase, una función (método), una llamada, un parámetro, un `;`, una llave, un
`import`… Nada se da por sabido. Cada concepto se explica con el Totito y luego con un ejemplo de la
vida diaria o de otro programa. Mejor de más que de menos.

## Lector

- Nunca programó. Usa **Windows 10/11** y **PowerShell**. Ha usado una computadora, nada más.
- Tutear («tú»), español neutro latinoamericano (Guatemala: el juego se llama «totito»).
- Tono cercano y claro, sin relleno. Explicar el **porqué** de las cosas, no solo el cómo.
- La primera vez que aparece un término técnico: definirlo en una frase.

## Código de referencia (NO MODIFICAR NADA AHÍ)

El proyecto terminado está en
`Totito/`:

- `src/*.java` — el juego (clases sin paquete, «default package»).
- `herramientas/PruebaConsola.java`, `herramientas/VistaPrevia.java`, `herramientas/GeneradorIcono.java`
  — utilidades que se ejecutan con `java -cp target/classes herramientas/X.java`.
- `pom.xml`, `README.md`, `recursos/totito.ico`, `recursos/totito.png`.
- Documento previo con explicaciones por bloque (sirve de referencia, pero el libro es MÁS detallado):
  `(notas del PDF de integración, ya no disponible)`.

Hay JDK 21, Maven y `jshell` instalados en este servidor (Linux): **compila y ejecuta** cada
programa de ejemplo completo que escribas para comprobar que funciona (en una carpeta tuya dentro de
`Totito/docs/libro/pruebas/<tu-parte>/`).
Los comandos de Windows/PowerShell no se pueden probar aquí: escríbelos con mucho cuidado.

## Datos fijos (todos los capítulos deben coincidir)

- Carpeta del proyecto del lector: `C:\Users\<tu-usuario>\Proyectos\Totito` (en PowerShell: `$HOME\Proyectos\Totito`).
  Todos los comandos del proyecto se ejecutan **desde esa carpeta**.
- Herramientas e instalación con winget (IDs verificados en el repositorio oficial winget-pkgs):
  - JDK: `winget install --id EclipseAdoptium.Temurin.21.JDK -e` (Java 21 LTS de Eclipse Temurin)
  - Git: `winget install --id Git.Git -e`
  - GitHub CLI: `winget install --id GitHub.cli -e`
  - NetBeans: `winget install --id Apache.NetBeans -e --skip-dependencies` (versión 25; trae Maven integrado). El `--skip-dependencies` evita que winget instale además BellSoft.LibericaJDK.23, que el paquete declara como dependencia; se instala primero el JDK Temurin 21.
  - Hasta el capítulo 61 no existe `TotitoApp` (la clase de `exec.mainClass`): antes de eso, cada clase con `main` se ejecuta con clic derecho → *Run File* (Shift+F6) en NetBeans, o con `java -cp target\classes Clase` (y las de `herramientas\` con `java -cp target\classes herramientas\X.java`).
  - Opcionales: `Microsoft.VisualStudioCode`, `Microsoft.WindowsTerminal`
  - Para el instalador: `winget install --id WiXToolset.WiXToolset -e` (WiX 3.14; jpackage del JDK 21 usa WiX 3)
  - Alternativa de instalador: `winget install --id JRSoftware.InnoSetup -e`
  - Tras instalar hay que **cerrar y volver a abrir PowerShell** para que se actualice el PATH.
- El proyecto es Maven con `<sourceDirectory>src</sourceDirectory>` (ver `pom.xml`): las clases van en
  `src\` sin paquete. En NetBeans aparecen en *Source Packages → &lt;default package&gt;*.
  Crear una clase en NetBeans: clic derecho en *&lt;default package&gt;* → *New → Java Class…* → nombre → *Finish*.
  Compilar: *Run → Clean and Build Project* (Shift+F11). Ejecutar: *Run → Run Project* (F6).
- Compilar sin NetBeans: `javac -encoding UTF-8 -d out src\*.java` y `java -cp out TotitoApp`.
- `.gitignore` del lector (se crea en el capítulo 5):
  ```
  target/
  out/
  dist/
  *.class
  nbproject/private/
  .idea/
  .vscode/
  Thumbs.db
  desktop.ini
  ```
- Repositorio del lector en GitHub: `totito` (en su cuenta). Rama principal `main`.
- **Plan de commits del libro** (la Parte II lo presenta y cada capítulo lo aplica):
  | Cap. | Qué se sube | Mensaje |
  |---|---|---|
  | 5 | pom.xml, .gitignore, README.md | `Estructura inicial del proyecto Totito` |
  | 8 | (primer push y repo en GitHub) | — |
  | 29 | src/Tablero.java | `Tablero: estado y reglas del juego` |
  | 30 | src/Jugador.java | `Jugador: nombre y ficha` |
  | 31 | src/IA_Minimax.java | `IA con el algoritmo Minimax` |
  | 32 | herramientas/PruebaConsola.java | `Prueba de la logica en consola` |
  | 33 | src/JuegoMain.java | `Primera ventana jugable (Swing basico)` + etiqueta `v0.1.0` |
  | 38–61 | en la rama `interfaz-neon`, un commit por capítulo (`Partida: turnos y marcador`, `Tema: paleta de colores`, …) | |
  | 61 | Pull Request `interfaz-neon` → `main`, merge, etiqueta `v1.0.0` | |
  | 64 | recursos/totito.ico y .png, herramientas/GeneradorIcono.java | `Icono del programa` |
  | 67 | Release `v1.0.0` en GitHub con el instalador | — |
- Comandos de empaquetado (capítulos 63–66), probados con jpackage del JDK 21:
  ```powershell
  # 1) jar (desde NetBeans: Clean and Build). Queda en target\Totito-1.0-SNAPSHOT.jar
  # 2) carpeta de entrada solo con el jar
  New-Item -ItemType Directory -Force dist\entrada | Out-Null
  Copy-Item target\Totito-1.0-SNAPSHOT.jar dist\entrada\
  # 3) programa portable (carpeta con Totito.exe y su propio Java), ~54 MB
  jpackage --type app-image --name Totito --input dist\entrada `
    --main-jar Totito-1.0-SNAPSHOT.jar --main-class TotitoApp `
    --icon recursos\totito.ico --app-version 1.0.0 --vendor "Tu Nombre" `
    --description "Juego del Totito" --add-modules java.desktop `
    --jlink-options "--strip-debug --no-man-pages --no-header-files --compress=zip-6" `
    --dest dist\app
  # 4) instalador (requiere WiX 3.14)
  jpackage --type exe --name Totito --input dist\entrada `
    --main-jar Totito-1.0-SNAPSHOT.jar --main-class TotitoApp `
    --icon recursos\totito.ico --app-version 1.0.0 --vendor "Tu Nombre" `
    --description "Juego del Totito" --add-modules java.desktop `
    --jlink-options "--strip-debug --no-man-pages --no-header-files --compress=zip-6" `
    --win-shortcut --win-menu --win-menu-group "Juegos" --win-dir-chooser `
    --win-upgrade-uuid 6f1c2a52-6a8e-4c39-9d0b-2f5d7d1a7e31 --dest dist\instalador
  ```
  `jdeps --print-module-deps target\Totito-1.0-SNAPSHOT.jar` imprime `java.base,java.desktop`.

## Formato de entrega

Escribe tus archivos en `Totito/docs/libro/capitulos/`.
Un archivo por capítulo, con el número de dos dígitos: `cap05.html` o `cap29.py`.

### Capítulos de teoría o de pasos → `capNN.html`

Fragmento HTML (sin `<html>`, `<head>` ni `<body>`), que empieza así:
```html
<section class="capitulo" id="cap05">
<h1><span class="num">Capítulo 5</span>Crear el proyecto Totito</h1>
<p class="entrada">Una o dos frases: qué se logra en este capítulo y por qué importa.</p>
...
</section>
```
Elementos disponibles (no inventes otras clases; no uses estilos en línea):
- `<h2>`, `<h3>`, `<p>`, `<ul>`, `<ol>`, `<b>`, `<i>`, `<code>` (código en línea), `<table class="tabla">` con `<th>`/`<td>`.
- Código Java de ejemplo: `<pre class="java">` … `</pre>` (escapa `<`, `>` y `&` como `&lt;` `&gt;` `&amp;`; el resaltado lo pone el armador).
- Comandos de PowerShell: `<pre class="ps">` una línea por comando, SIN escribir el `PS>` (lo pone el armador). Los comentarios con `#`.
- Salida que muestra la terminal o el programa: `<pre class="salida">`.
- Otro texto de archivo (XML, .gitignore, Markdown, .iss): `<pre class="texto">`.
- Cajas:
  - `<div class="caja concepto"><b>Título</b> texto…</div>` — idea clave.
  - `<div class="caja consejo">` — buena práctica / truco.
  - `<div class="caja cuidado">` — error común o advertencia.
  - `<div class="caja aplica"><b>Aplícalo fuera del Totito</b> …</div>` — **obligatoria al final de cada capítulo**: cómo se usa lo aprendido en otros proyectos reales (con 2–4 ejemplos concretos).
  - `<div class="caja ejercicio"><b>Ejercicios</b><ol>…</ol></div>` — **obligatoria al final**: 3–5 ejercicios graduados; añade «Pista:» cuando ayude.
  - `<div class="caja git"><b>Git</b> …</div>` — el commit/acción de Git del capítulo (con su `<pre class="ps">`).
  - `<div class="caja hito"><b>Hito</b> …</div>` — cuando el lector logra algo visible.
- Diagramas: tablas o listas; si hace falta un dibujo, SVG en línea sencillo (`<svg>` con `viewBox`, ancho máx. 100%), colores de la paleta del Totito (#FF3BD4 rosa, #2F84FF azul, #A05CFF morado, #1C1740 fondo, #C8BCF6 lavanda).
- Al final de cada capítulo: `<h2>Resumen</h2>` con 4–8 viñetas, luego la caja **aplica** y la caja **ejercicio**.

### Capítulos de código línea por línea → `capNN.py`

```python
CAPITULO = {
    "numero": 29,
    "titulo": "Tablero.java: el estado del juego",
    "antes": """<p class="entrada">…</p> <h2>Por qué existe este archivo</h2> … <h2>Qué vas a aprender</h2> …
               <h2>Créalo</h2> (pasos exactos en NetBeans) …""",
    "archivos": [
        {"ruta": "src/Tablero.java",          # relativa a la carpeta Totito
         "bloques": [
             (None, """<p class="l"><b>L1–L6</b> …</p>"""),
             ("public class Tablero", """<p class="l"><b>L7</b> …</p>"""),
             ...
         ]},
    ],
    "despues": """<h2>Compila y prueba</h2> … <div class="caja git">…</div> <h2>Resumen</h2> …
                 <div class="caja aplica">…</div> <div class="caja ejercicio">…</div>""",
}
```
Reglas de los `bloques`:
- El armador muestra el archivo **completo** con números de línea, partido en bloques; tu nota va debajo de cada bloque.
- Cada bloque empieza en la primera línea (después del bloque anterior) que **contiene** el texto del
  marcador; `None` = inicio del archivo. Los comentarios que estén justo encima del marcador se
  incluyen automáticamente en ese bloque. Los comentarios del código fuente NO llevan tildes:
  copia el marcador tal cual está en el archivo.
- **Bloques pequeños: máximo ~8 líneas con contenido.** El objetivo es explicar CADA línea.
- Dentro de la nota, un `<p class="l"><b>L23</b> …</p>` por línea (o `<b>L23–L25</b>` para líneas
  triviales seguidas, como llaves de cierre o imports). Di qué hace la línea, **por qué** está, y qué
  pasaría si no estuviera cuando sea instructivo. Explica cada palabra nueva de Java la primera vez
  (`public`, `static`, `final`, `new`, `this`, `@Override`…). Las llaves `}` sueltas y líneas en
  blanco no necesitan explicación propia (agrúpalas).
- Los números de línea deben coincidir con el archivo real: **verifica con el script**:
  `python3 -I Totito/docs/libro/verificar.py capNN.py`
  Imprime cada bloque con sus números reales; corrige hasta que no haya errores ni bloques demasiado largos.
- Un capítulo puede tener varios archivos (p. ej. PantallaMenu + VistaPrevia).

## Contenido obligatorio de cada capítulo de código

1. **Por qué existe** el archivo y qué problema resuelve en el Totito.
2. **Qué vas a aprender** (conceptos de Java/POO/diseño que aparecen).
3. **Créalo**: pasos exactos (NetBeans y alternativa con PowerShell `New-Item src\X.java`).
4. El código explicado línea por línea (bloques).
5. **Cómo funciona por dentro**: la lógica en conjunto, con un ejemplo concreto con valores (traza).
6. **Compila y prueba**: qué hacer y qué debería verse; errores típicos y su solución.
7. **Git**: el commit del capítulo según el plan.
8. Resumen, «Aplícalo fuera del Totito» y ejercicios.

## Verificación final antes de terminar

- Para `.py`: `python3 -I …/libro/verificar.py capNN.py` sin errores.
- Para `.html`: `python3 -I …/libro/verificar.py capNN.html` (comprueba que el HTML esté bien cerrado y use solo las clases permitidas).
- Responde al final con: lista de archivos creados, número aproximado de palabras, y cualquier
  duda o dato que no pudiste verificar.

## Índice completo del libro (cada parte la escribe un redactor distinto)

Usa estos números al hacer referencias cruzadas («como viste en el capítulo 19…»). No repitas a
fondo lo que otro capítulo explica: resúmelo en una frase y remite a él.

**Parte I — Antes de programar** (html)
1. Cómo usar este libro (qué se construye, cómo leerlo, convenciones, la ruta del Totito de v0.1 a v1.0 y el .exe)
2. Tu computadora: requisitos y características (mínimos/recomendados, cómo ver los de tu PC, 64 bits, espacio, permisos de administrador)
3. La terminal: PowerShell desde cero (abrir, rutas, cd, ls/Get-ChildItem, mkdir/New-Item, copiar, mover, borrar con cuidado, Tab, historial, variables $HOME, $env:Path)
4. Instalar las herramientas (winget; JDK, Git, GitHub CLI, NetBeans; verificar con java -version, git --version, gh --version; PATH y JAVA_HOME; problemas típicos; instalación manual alternativa)
5. Crear el proyecto Totito (carpetas, pom.xml explicado línea por línea, .gitignore, README.md, abrir en NetBeans y recorrer la interfaz de NetBeans, primer Clean and Build)

**Parte II — Git y GitHub: el camino hasta el resultado final** (html)
6. Qué es el control de versiones y cómo piensa Git (repositorio, área de preparación, commit, historial, HEAD, ramas; analogías)
7. Configurar Git y GitHub (cuenta, verificación en dos pasos, git config, gh auth login, HTTPS vs SSH)
8. El primer repositorio del Totito (git init, status, add, commit, log, gh repo create, push; el plan de commits del libro)
9. El trabajo diario con Git (commits pequeños, buenos mensajes, diff, ramas, merge, conflictos paso a paso, deshacer: restore/revert/reset con cuidado, stash, tags)
10. Colaborar y publicar en GitHub (pull requests, revisiones, issues, colaboradores, forks, README y licencia, releases, qué NO subir nunca, buenas prácticas resumidas)

**Parte III — Fundamentos de Java** (html; todos los ejemplos sacados del Totito)
11. Cómo funciona Java (código fuente, javac, bytecode, JVM, el método main, jshell para experimentar, anatomía de un archivo .java: import, clase, llaves, punto y coma, comentarios)
12. Variables, tipos y operadores (int, double, boolean, char, String; declarar/asignar; aritmética; comparación; casting; constantes)
13. Decisiones (if/else, operadores lógicos, switch clásico y de expresión)
14. Repeticiones (for, for anidados para recorrer el tablero, while, do-while, break/continue, for-each)
15. Arreglos y matrices (int[], char[][], índices, recorrer, copiar)
16. Métodos: funciones, parámetros, retorno, llamadas y pila de llamadas, alcance de variables, sobrecarga, recursión
17. Texto y entrada (String, métodos de String, concatenación, String.format, Scanner)

**Parte IV — Programación orientada a objetos** (html; con el Totito)
18. Clases y objetos (molde y galleta; new; referencias; null)
19. Encapsulamiento (private/public, getters/setters, invariantes)
20. Constructores, this, static y final
21. Composición y relaciones entre clases (tiene-un; Partida tiene Tablero; diagramas de clases)
22. Herencia (extends, super, JButton→BotonNeon, Tarjeta→TarjetaJugador; cuándo NO heredar)
23. Polimorfismo y sobrescritura (@Override, paintComponent, enlace dinámico)
24. Clases abstractas e interfaces (PantallaBase, Navegacion, OyenteCasilla)
25. Lambdas, referencias a métodos, clases anónimas e internas (Iconos, ActionListener, this::cerrar)
26. Enums y excepciones (Partida.Modo, Estado; IllegalArgumentException; try/catch/finally; try-with-resources)
27. Principios de diseño, patrones y buenas prácticas de código (responsabilidad única, bajo acoplamiento, alta cohesión, separar lógica e interfaz/MVC, Observer, Factory, Template Method, Strategy; nombres, comentarios, formato, números mágicos)

**Parte V — El Totito v0.1: la lógica y la primera ventana** (py, línea por línea)
28. Plan de la lógica (html: qué clases, por qué esas, diagrama, orden de construcción)
29. Tablero.java · 30. Jugador.java · 31. El algoritmo Minimax e IA_Minimax.java · 32. PruebaConsola.java · 33. JuegoMain.java (primera ventana Swing, hito v0.1.0)

**Parte VI — Diseño visual** (html)
34. Del boceto al código: leer un diseño (las 4 imágenes de diseño: menú, instrucciones, configuración, victoria; inventario de componentes repetidos; jerarquía)
35. Teoría del color para programadores (RGB, hexadecimal, alfa, HSB, paletas, contraste y accesibilidad, significado del color, degradados, modo oscuro, cómo se fabrica el neón)
36. Tipografía, espaciado, alineación y consistencia (fuentes, tamaños, pesos, espaciado de letras, márgenes, rejilla, la ventana de 640×690)
37. Cómo dibuja Swing (componentes y contenedores, layouts BorderLayout/BoxLayout/CardLayout/null, el hilo de eventos EDT, paintComponent y repaint, Graphics2D, coordenadas, formas, trazos, degradados, transparencia, transformaciones)

**Parte VII — El Totito v1.0: la interfaz neón** (py, línea por línea; se trabaja en la rama interfaz-neon)
38. Partida.java · 39. Navegacion.java · 40. Tema.java · 41. Dibujo.java · 42. Iconos.java
43. Tarjeta.java · 44. BotonNeon.java · 45. Encabezado.java · 46. Rotulo.java · 47. CampoTexto.java · 48. PanelTablero.java
49. TarjetaJugador.java · 50. SelectorSimbolo.java · 51. OpcionModo.java · 52. PanelMarcador.java · 53. PasoInstruccion.java · 54. IconoResultado.java
55. PantallaBase.java · 56. PantallaMenu.java y la VistaPrevia (herramientas/VistaPrevia.java; primera vez que se VE el diseño)
57. PantallaInstrucciones.java · 58. PantallaConfiguracion.java · 59. PantallaJuego.java · 60. PantallaResultado.java · 61. PanelPrincipal.java y TotitoApp.java (hito v1.0.0, PR a main)

**Parte VIII — Probar, empaquetar y compartir** (html; 64 puede ser py)
62. Probar y depurar (depurador de NetBeans, puntos de interrupción, errores frecuentes de compilación y ejecución, lista de pruebas manuales)
63. El archivo .jar (qué es, manifiesto, ejecutarlo)
64. El icono del programa (GeneradorIcono.java línea por línea; formato .ico)
65. jpackage: una carpeta portable con Totito.exe (y comprimirla para compartir)
66. El instalador .exe (WiX + jpackage --type exe; accesos directos, menú, actualización; alternativa con Inno Setup y su script .iss)
67. Publicar: versiones (SemVer), etiquetas, GitHub Releases con gh, aviso SmartScreen y firma de código

**Parte IX — Más allá del Totito** (html)
68. Aplica lo aprendido: cinco proyectos guiados (Conecta 4, Buscaminas, gestor de tareas, calculadora neón, inventario de una tienda), qué reutilizar del Totito en cada uno
69. Siguientes pasos (pruebas con JUnit, paquetes, JavaFX, bases de datos con JDBC, aplicaciones web con Spring Boot, Android)

**Apéndices** (html): A. Chuleta de PowerShell · B. Chuleta de Git · C. Atajos de NetBeans · D. Errores comunes y su solución · E. Glosario
(archivos `apA.html` … `apE.html`, con `<section class="capitulo" id="apA">`; en apéndices las cajas aplica/ejercicio no son obligatorias, pon `<div class="caja aplica"></div><div class="caja ejercicio"></div>` vacías si no aplican — el armador las omite si están vacías).

## Imágenes disponibles

Puedes insertar imágenes con `<figure><img src="RUTA"><figcaption>Texto</figcaption></figure>`
(sin clases ni estilos; el armador las incrusta). Rutas válidas:
- Diseño original: `diseno/menu.jpg`, `diseno/instrucciones.jpg`, `diseno/configuracion.jpg`, `diseno/victoria.jpg`
  (están en `Totito/docs/libro/diseno/`, míralas con la herramienta de leer imágenes).
- Capturas del resultado: `capturas/1-menu.png`, `capturas/2-instrucciones.png`, `capturas/3-configuracion.png`,
  `capturas/4-juego.png`, `capturas/5-victoria.png`, `capturas/6-empate.png` (en `…/repo/Totito/docs/capturas/`).
- Icono: `recursos/totito.png`.
