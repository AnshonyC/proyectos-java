import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.GradientPaint;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.RoundRectangle2D;
import javax.swing.JPanel;

/**
 * Barra superior comun a todas las pantallas: logotipo, el titulo
 * "Juego del Totito", el lema y el boton de cerrar.
 */
public class Encabezado extends JPanel {

    public static final int ALTO = 96;
    private static final int MARGEN = 10;
    private static final int LADO_BOTON = 58;

    private final BotonNeon botonCerrar;

    /** @param alCerrar que hacer al pulsar la X (normalmente, cerrar el juego). */
    public Encabezado(Runnable alCerrar) {
        super(null);    // sin layout: el unico hijo (el boton) se coloca en doLayout()
        setOpaque(false);
        setPreferredSize(new Dimension(0, ALTO));   // el ancho lo decide el BorderLayout

        botonCerrar = BotonNeon.icono(Iconos.CERRAR, Tema.ROSA);
        botonCerrar.setToolTipText("Cerrar el juego");
        botonCerrar.addActionListener(e -> alCerrar.run());
        add(botonCerrar);
    }

    @Override
    public void doLayout() {
        botonCerrar.setBounds(getWidth() - MARGEN - LADO_BOTON - 6, (getHeight() - LADO_BOTON) / 2,
                LADO_BOTON, LADO_BOTON);
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = Dibujo.preparar(g);
        int ancho = getWidth();

        // Caja translucida con borde suave.
        RoundRectangle2D caja = new RoundRectangle2D.Double(MARGEN, MARGEN,
                ancho - 2.0 * MARGEN, getHeight() - 2.0 * MARGEN, 26, 26);
        g2.setPaint(new GradientPaint(0, MARGEN, Tema.conAlfa(Tema.LAVANDA, 22),
                0, getHeight() - MARGEN, Tema.conAlfa(Tema.LAVANDA, 8)));
        g2.fill(caja);
        Dibujo.trazoNeon(g2, caja, Tema.MORADO, 1.2f, 0.45f);

        double ladoLogo = 52;
        Iconos.LOGO.dibujar(g2, MARGEN + 20, (getHeight() - ladoLogo) / 2, ladoLogo, Tema.LAVANDA);

        // Titulo: "Juego del " en blanco y "Totito" con degradado rosa -> cian.
        g2.setFont(Tema.fuente(Font.BOLD, 36f));
        FontMetrics fm = g2.getFontMetrics();
        String parte1 = "Juego del ";
        String parte2 = "Totito";
        float anchoTitulo = fm.stringWidth(parte1) + fm.stringWidth(parte2);
        float x = (ancho - anchoTitulo) / 2f;
        float base = MARGEN + 44;
        Dibujo.textoNeon(g2, parte1, x, base, Tema.LAVANDA, Tema.TEXTO);
        float x2 = x + fm.stringWidth(parte1);
        Dibujo.textoNeon(g2, parte2, x2, base, Tema.ROSA,
                new GradientPaint(x2, 0, Tema.ROSA, x2 + fm.stringWidth(parte2), 0, Tema.CIAN));

        // Lema con letras separadas.
        g2.setFont(Tema.fuenteEspaciada(Font.BOLD, 10.5f, 0.28f));
        fm = g2.getFontMetrics();
        String lema = "ESTRATEGIA  •  DIVERSIÓN  •  SIEMPRE UN CLÁSICO";
        g2.setColor(Tema.TEXTO_SUAVE);
        g2.drawString(lema, (ancho - fm.stringWidth(lema)) / 2f, base + 24);
        g2.dispose();
    }
}
