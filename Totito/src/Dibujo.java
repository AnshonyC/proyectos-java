import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Paint;
import java.awt.RenderingHints;
import java.awt.Shape;
import java.awt.Stroke;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Path2D;
import javax.swing.JComponent;

/**
 * Herramientas de dibujo que comparten todos los componentes de la interfaz.
 *
 * El efecto "neon" es un truco sencillo: se traza la misma figura varias
 * veces, primero muy gruesa y casi transparente, y cada vez mas fina y mas
 * opaca. El ojo lo interpreta como luz que se difumina alrededor del trazo.
 * No se usan imagenes: todo (fichas, iconos, botones) se dibuja con Java2D.
 */
public final class Dibujo {

    private Dibujo() {
    }

    /**
     * Devuelve una copia del Graphics con el suavizado (antialiasing)
     * activado. Quien la pida debe llamar dispose() al terminar.
     */
    public static Graphics2D preparar(Graphics g) {
        Graphics2D g2 = (Graphics2D) g.create();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        g2.setRenderingHint(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);
        g2.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE);
        g2.setRenderingHint(RenderingHints.KEY_FRACTIONALMETRICS, RenderingHints.VALUE_FRACTIONALMETRICS_ON);
        return g2;
    }

    /**
     * Fija el tamano de un componente (preferido, minimo y maximo iguales)
     * para que los BoxLayout de las pantallas no lo estiren.
     */
    public static void fijarTamano(JComponent componente, int ancho, int alto) {
        Dimension tamano = new Dimension(ancho, alto);
        componente.setPreferredSize(tamano);
        componente.setMinimumSize(tamano);
        componente.setMaximumSize(tamano);
    }

    /** Trazo con puntas y esquinas redondeadas. */
    public static BasicStroke redondo(float grosor) {
        return new BasicStroke(grosor, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND);
    }

    /** Trazo simple, sin halo. */
    public static void trazo(Graphics2D g, Shape figura, Color color, float grosor) {
        g.setColor(color);
        g.setStroke(redondo(grosor));
        g.draw(figura);
    }

    public static void trazoNeon(Graphics2D g, Shape figura, Color color, float grosor) {
        trazoNeon(g, figura, color, grosor, 1f);
    }

    /**
     * Traza la figura con halo de neon.
     *
     * @param intensidad 1 = normal; menos de 1 se ve apagado (opcion no
     *                   elegida); mas de 1 brilla mas (raton encima).
     */
    public static void trazoNeon(Graphics2D g, Shape figura, Color color, float grosor, float intensidad) {
        Stroke trazoPrevio = g.getStroke();
        Paint pinturaPrevia = g.getPaint();

        // Halo: de la capa mas ancha y transparente a la mas fina y opaca.
        final int capas = 6;
        for (int i = capas; i >= 1; i--) {
            int alfa = Math.round((6 + (capas - i) * 5) * intensidad);
            g.setColor(Tema.conAlfa(color, alfa));
            g.setStroke(redondo(grosor + i * 2.4f));
            g.draw(figura);
        }

        // Linea principal.
        g.setColor(Tema.conAlfa(color, Math.round(255 * Math.min(1f, 0.4f + 0.6f * intensidad))));
        g.setStroke(redondo(grosor));
        g.draw(figura);

        // En trazos gruesos (las fichas) el centro del "tubo" es casi blanco.
        if (grosor >= 5) {
            g.setColor(Tema.conAlfa(Tema.aclarar(color, 0.6f), 200));
            g.setStroke(redondo(grosor * 0.35f));
            g.draw(figura);
        }

        g.setStroke(trazoPrevio);
        g.setPaint(pinturaPrevia);
    }

    /** Dibuja una X de neon centrada en (cx, cy). */
    public static void dibujarX(Graphics2D g, double cx, double cy, double tam, Color color, float grosor) {
        double r = tam / 2;
        Path2D equis = new Path2D.Double();
        equis.moveTo(cx - r, cy - r);
        equis.lineTo(cx + r, cy + r);
        equis.moveTo(cx + r, cy - r);
        equis.lineTo(cx - r, cy + r);
        trazoNeon(g, equis, color, grosor);
    }

    /** Dibuja una O de neon centrada en (cx, cy). */
    public static void dibujarO(Graphics2D g, double cx, double cy, double tam, Color color, float grosor) {
        trazoNeon(g, new Ellipse2D.Double(cx - tam / 2, cy - tam / 2, tam, tam), color, grosor);
    }

    /**
     * Dibuja la ficha ('X' u 'O') con su color del tema. La X se hace un
     * poco mas pequena para que a la vista ocupe lo mismo que la O.
     */
    public static void dibujarFicha(Graphics2D g, char ficha, double cx, double cy, double tam, float grosor) {
        if (ficha == 'X') {
            dibujarX(g, cx, cy, tam * 0.84, Tema.ROSA, grosor);
        } else if (ficha == 'O') {
            dibujarO(g, cx, cy, tam, Tema.AZUL, grosor);
        }
    }

    /**
     * Escribe texto con un halo de color alrededor.
     * (x, y) es la linea base del texto, como en drawString.
     */
    public static void textoNeon(Graphics2D g, String texto, float x, float y, Color halo, Paint relleno) {
        Paint previo = g.getPaint();
        for (int radio = 4; radio >= 1; radio--) {
            g.setColor(Tema.conAlfa(halo, 4 + (4 - radio) * 3));
            for (int angulo = 0; angulo < 360; angulo += 45) {
                double rad = Math.toRadians(angulo);
                g.drawString(texto, x + (float) (Math.cos(rad) * radio), y + (float) (Math.sin(rad) * radio));
            }
        }
        g.setPaint(relleno);
        g.drawString(texto, x, y);
        g.setPaint(previo);
    }

    /** Linea base para que el texto quede centrado en vertical sobre yCentro. */
    public static float lineaBaseCentrada(FontMetrics fm, float yCentro) {
        return yCentro + (fm.getAscent() - fm.getDescent()) / 2f;
    }

    /** Recorta el texto con "…" si no cabe en el ancho dado. */
    public static String recortar(FontMetrics fm, String texto, int anchoMaximo) {
        if (fm.stringWidth(texto) <= anchoMaximo) {
            return texto;
        }
        String recortado = texto;
        while (recortado.length() > 1 && fm.stringWidth(recortado + "…") > anchoMaximo) {
            recortado = recortado.substring(0, recortado.length() - 1);
        }
        return recortado + "…";
    }
}
