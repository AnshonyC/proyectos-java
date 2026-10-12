import java.awt.Color;
import java.awt.Font;
import java.awt.GraphicsEnvironment;
import java.awt.font.TextAttribute;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

/**
 * Paleta de colores y tipografia de la interfaz "neon".
 *
 * Toda la interfaz toma sus colores y fuentes de aqui: para cambiar el
 * aspecto del juego basta con tocar esta clase, no hay colores sueltos
 * repartidos por las pantallas.
 */
public final class Tema {

    /** Fondo de la ventana: degradado de arriba hacia abajo. */
    public static final Color FONDO_ARRIBA = new Color(0x1C, 0x17, 0x40);
    public static final Color FONDO_ABAJO = new Color(0x0E, 0x0B, 0x24);
    /** X y O gigantes y desvaidas que adornan el fondo. */
    public static final Color DECORACION = new Color(0x5B, 0x35, 0xC2, 70);

    /** Color de la X (en todo el juego la X es rosa). */
    public static final Color ROSA = new Color(0xFF, 0x3B, 0xD4);
    /** Tarjeta del Jugador 1: un rosa mas rojizo, como en el diseno. */
    public static final Color FRESA = new Color(0xFF, 0x3D, 0x82);
    /** Color de la O (en todo el juego la O es azul). */
    public static final Color AZUL = new Color(0x2F, 0x84, 0xFF);
    public static final Color CIAN = new Color(0x40, 0xC8, 0xFF);
    public static final Color MORADO = new Color(0xA0, 0x5C, 0xFF);
    public static final Color LAVANDA = new Color(0xC8, 0xBC, 0xF6);

    public static final Color TEXTO = Color.WHITE;
    public static final Color TEXTO_SUAVE = new Color(0xA8, 0x9B, 0xE2);
    /** Relleno de las tarjetas "de cristal": semitransparente a proposito. */
    public static final Color SUPERFICIE = new Color(0x2B, 0x23, 0x63, 125);
    /** Fondo de cada casilla del tablero. */
    public static final Color CASILLA = new Color(0x2E, 0x28, 0x5A, 170);

    /**
     * Fuentes preferidas, en orden. Se usa la primera que exista en el
     * equipo (Windows suele tener Segoe UI; Linux, DejaVu o Liberation).
     * Si no hay ninguna, Java usa "SansSerif", que existe siempre.
     */
    private static final List<String> FAMILIAS = Arrays.asList(
            "Nunito", "Poppins", "Montserrat", "Segoe UI", "Helvetica Neue",
            "Ubuntu", "Arial", "Liberation Sans", "DejaVu Sans");

    private static final String FAMILIA = elegirFamilia();

    private Tema() {
    }

    /** Fuente de la interfaz. estilo = Font.PLAIN o Font.BOLD. */
    public static Font fuente(int estilo, float tamano) {
        return new Font(FAMILIA, estilo, 12).deriveFont(tamano);
    }

    /** Fuente con las letras separadas, para titulos tipo "J U G A D O R E S". */
    public static Font fuenteEspaciada(int estilo, float tamano, float espaciado) {
        return fuente(estilo, tamano).deriveFont(Map.of(TextAttribute.TRACKING, espaciado));
    }

    /** La X siempre es rosa y la O siempre es azul, la juegue quien la juegue. */
    public static Color colorDeFicha(char ficha) {
        return ficha == 'X' ? ROSA : AZUL;
    }

    /** El mismo color con otra transparencia (0 = invisible, 255 = opaco). */
    public static Color conAlfa(Color color, int alfa) {
        return new Color(color.getRed(), color.getGreen(), color.getBlue(),
                Math.max(0, Math.min(255, alfa)));
    }

    /** Mezcla el color con blanco: factor 0 lo deja igual, 1 lo vuelve blanco. */
    public static Color aclarar(Color color, float factor) {
        int r = Math.round(color.getRed() + (255 - color.getRed()) * factor);
        int g = Math.round(color.getGreen() + (255 - color.getGreen()) * factor);
        int b = Math.round(color.getBlue() + (255 - color.getBlue()) * factor);
        return new Color(r, g, b, color.getAlpha());
    }

    /** "#RRGGBB", para usar los colores del tema dentro de texto HTML de un JLabel. */
    public static String hex(Color color) {
        return String.format("#%02X%02X%02X", color.getRed(), color.getGreen(), color.getBlue());
    }

    private static String elegirFamilia() {
        try {
            List<String> instaladas = Arrays.asList(
                    GraphicsEnvironment.getLocalGraphicsEnvironment().getAvailableFontFamilyNames());
            for (String familia : FAMILIAS) {
                if (instaladas.contains(familia)) {
                    return familia;
                }
            }
        } catch (RuntimeException e) {
            // Sin acceso a las fuentes del sistema: se usa la generica.
        }
        return Font.SANS_SERIF;
    }
}
