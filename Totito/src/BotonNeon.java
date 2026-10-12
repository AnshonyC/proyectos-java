import java.awt.AlphaComposite;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.GradientPaint;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.Line2D;
import java.awt.geom.RoundRectangle2D;
import javax.swing.JButton;

/**
 * Boton con borde de neon. Es un JButton normal (se usa con
 * addActionListener), solo que se dibuja a mano.
 *
 * Se crea con los metodos de fabrica, uno por cada forma del diseno:
 * menu(...), pildora(...), contorno(...) e icono(...).
 */
public class BotonNeon extends JButton {

    /** Las formas de boton que aparecen en el diseno. */
    public enum Estilo {
        /** Boton ancho del menu principal:  icono | Texto   › */
        MENU,
        /** Pildora rellena con degradado ("Comenzar partida", "Jugar de nuevo"). */
        PILDORA,
        /** Pildora solo con borde ("Volver", "Reiniciar"). */
        CONTORNO,
        /** Cuadrado pequeno con solo un icono (la X de cerrar). */
        ICONO
    }

    /** Espacio alrededor de la forma para que el halo no se corte. */
    private static final int MARGEN = 9;

    private final Estilo estilo;
    private final Iconos.Icono icono;
    private final Color color;
    private final Color colorFinal;

    private BotonNeon(String texto, Iconos.Icono icono, Color color, Color colorFinal,
                      Estilo estilo, int ancho, int alto) {
        super(texto);
        this.estilo = estilo;
        this.icono = icono;
        this.color = color;
        this.colorFinal = colorFinal;

        // Se apaga todo lo que Swing dibuja por defecto: lo pinta paintComponent.
        setContentAreaFilled(false);
        setBorderPainted(false);
        setFocusPainted(false);
        setOpaque(false);
        setRolloverEnabled(true);

        setForeground(Tema.TEXTO);
        setFont(Tema.fuente(Font.BOLD, estilo == Estilo.MENU ? 25f : 19f));
        setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        setAlignmentX(CENTER_ALIGNMENT);
        Dibujo.fijarTamano(this, ancho, alto);
    }

    /** Boton grande del menu principal. */
    public static BotonNeon menu(String texto, Iconos.Icono icono, Color color) {
        return new BotonNeon(texto, icono, color, color, Estilo.MENU, 384, 88);
    }

    /** Pildora rellena con un degradado de "desde" a "hasta". */
    public static BotonNeon pildora(String texto, Iconos.Icono icono, Color desde, Color hasta, int ancho, int alto) {
        return new BotonNeon(texto, icono, desde, hasta, Estilo.PILDORA, ancho, alto);
    }

    /** Pildora oscura con borde morado. */
    public static BotonNeon contorno(String texto, Iconos.Icono icono, int ancho, int alto) {
        return new BotonNeon(texto, icono, Tema.MORADO, Tema.MORADO, Estilo.CONTORNO, ancho, alto);
    }

    /** Boton cuadrado sin texto. Ponerle setToolTipText para que se entienda. */
    public static BotonNeon icono(Iconos.Icono icono, Color color) {
        return new BotonNeon("", icono, color, color, Estilo.ICONO, 58, 58);
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = Dibujo.preparar(g);
        if (!isEnabled()) {
            g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, 0.4f));
        }
        boolean resaltado = getModel().isRollover() && isEnabled();
        boolean pulsado = getModel().isArmed() && getModel().isPressed();

        double ancho = getWidth() - 2.0 * MARGEN;
        double alto = getHeight() - 2.0 * MARGEN;
        double arco = switch (estilo) {
            case MENU -> 30;
            case ICONO -> 16;
            default -> alto;        // pildora: extremos totalmente redondos
        };
        RoundRectangle2D forma = new RoundRectangle2D.Double(MARGEN, MARGEN, ancho, alto, arco, arco);

        pintarRelleno(g2, forma, resaltado);
        Color borde = estilo == Estilo.PILDORA ? Tema.aclarar(color, 0.2f) : color;
        Dibujo.trazoNeon(g2, forma, borde, 2f, resaltado ? 1.5f : 1f);
        if (pulsado) {
            g2.setColor(new Color(0, 0, 0, 60));
            g2.fill(forma);
        }

        if (estilo == Estilo.MENU) {
            pintarContenidoMenu(g2, forma);
        } else {
            pintarContenidoCentrado(g2, forma);
        }
        g2.dispose();
    }

    private void pintarRelleno(Graphics2D g2, RoundRectangle2D forma, boolean resaltado) {
        float x0 = (float) forma.getX();
        float x1 = (float) (forma.getX() + forma.getWidth());
        switch (estilo) {
            case MENU -> g2.setPaint(new GradientPaint(
                    x0, 0, Tema.conAlfa(color, resaltado ? 95 : 65),
                    x1, 0, Tema.conAlfa(Tema.FONDO_ABAJO, 120)));
            case PILDORA -> g2.setPaint(new GradientPaint(
                    x0, 0, Tema.conAlfa(color, resaltado ? 255 : 225),
                    x1, 0, Tema.conAlfa(colorFinal, resaltado ? 255 : 225)));
            default -> g2.setPaint(Tema.conAlfa(color, resaltado ? 60 : 30));
        }
        g2.fill(forma);

        if (estilo == Estilo.PILDORA) {
            // Reflejo de "cristal" en la mitad de arriba.
            float y0 = (float) forma.getY();
            g2.setPaint(new GradientPaint(0, y0, new Color(255, 255, 255, 50),
                    0, y0 + (float) forma.getHeight() / 2, new Color(255, 255, 255, 0)));
            g2.fill(forma);
        }
    }

    /** Distribucion del menu: icono a la izquierda, divisor, texto y flechita. */
    private void pintarContenidoMenu(Graphics2D g2, RoundRectangle2D forma) {
        double x = forma.getX();
        double y = forma.getY();
        double ancho = forma.getWidth();
        double alto = forma.getHeight();

        double tamIcono = alto * 0.5;
        double divisor = x + ancho * 0.27;
        icono.dibujar(g2, x + ancho * 0.135 - tamIcono / 2, y + (alto - tamIcono) / 2, tamIcono,
                Tema.aclarar(color, 0.15f));

        g2.setColor(new Color(255, 255, 255, 45));
        g2.setStroke(new BasicStroke(1.5f));
        g2.draw(new Line2D.Double(divisor, y + alto * 0.22, divisor, y + alto * 0.78));

        g2.setFont(getFont());
        g2.setColor(getForeground());
        FontMetrics fm = g2.getFontMetrics();
        g2.drawString(getText(), (float) (divisor + 30), Dibujo.lineaBaseCentrada(fm, (float) (y + alto / 2)));

        double tamFlecha = alto * 0.3;
        Iconos.CHEVRON.dibujar(g2, x + ancho - 28 - tamFlecha, y + (alto - tamFlecha) / 2, tamFlecha,
                Tema.aclarar(color, 0.2f));
    }

    /** Distribucion de pildoras e iconos: icono + texto centrados como un bloque. */
    private void pintarContenidoCentrado(Graphics2D g2, RoundRectangle2D forma) {
        double alto = forma.getHeight();
        double cy = forma.getY() + alto / 2;
        String texto = getText();

        if (texto == null || texto.isEmpty()) {
            double t = alto * 0.5;
            icono.dibujar(g2, forma.getCenterX() - t / 2, cy - t / 2, t, color);
            return;
        }

        g2.setFont(getFont());
        FontMetrics fm = g2.getFontMetrics();
        double tamIcono = icono == null ? 0 : alto * 0.44;
        double hueco = icono == null ? 0 : 16;
        double total = tamIcono + hueco + fm.stringWidth(texto);
        double x = forma.getCenterX() - total / 2;
        if (icono != null) {
            icono.dibujar(g2, x, cy - tamIcono / 2, tamIcono, Tema.TEXTO);
        }
        g2.setColor(getForeground());
        g2.drawString(texto, (float) (x + tamIcono + hueco), Dibujo.lineaBaseCentrada(fm, (float) cy));
    }
}
