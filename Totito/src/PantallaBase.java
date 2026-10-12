import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GradientPaint;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RadialGradientPaint;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Path2D;
import java.awt.geom.Point2D;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JComponent;
import javax.swing.JPanel;

/**
 * Base de todas las pantallas: pinta el fondo (degradado, X y O gigantes,
 * puntitos), pone el Encabezado arriba y deja un panel "contenido" en
 * columna (BoxLayout vertical) donde cada pantalla agrega lo suyo.
 *
 * Para crear una pantalla nueva: extender esta clase y, en el constructor,
 * usar agregar(), espacio() y relleno() en el orden en que se quieren ver
 * las cosas de arriba abajo.
 */
public abstract class PantallaBase extends JPanel {

    private final JPanel contenido;

    protected PantallaBase(Navegacion navegacion) {
        super(new BorderLayout());
        add(new Encabezado(navegacion::salir), BorderLayout.NORTH);

        contenido = new JPanel();
        contenido.setOpaque(false);
        contenido.setLayout(new BoxLayout(contenido, BoxLayout.Y_AXIS));
        contenido.setBorder(BorderFactory.createEmptyBorder(0, 0, 10, 0));
        add(contenido, BorderLayout.CENTER);
    }

    /** Agrega un componente centrado debajo del anterior. */
    protected void agregar(JComponent componente) {
        componente.setAlignmentX(CENTER_ALIGNMENT);
        contenido.add(componente);
    }

    /** Separacion vertical fija, en pixeles. */
    protected void espacio(int alto) {
        contenido.add(Box.createRigidArea(new Dimension(0, alto)));
    }

    /** Espacio elastico: poner uno al principio y otro al final centra todo en vertical. */
    protected void relleno() {
        contenido.add(Box.createVerticalGlue());
    }

    /** Pone varios componentes uno al lado del otro, separados por "hueco" pixeles. */
    protected static JPanel fila(int hueco, JComponent... componentes) {
        JPanel fila = new JPanel();
        fila.setOpaque(false);
        fila.setLayout(new BoxLayout(fila, BoxLayout.X_AXIS));
        for (int i = 0; i < componentes.length; i++) {
            if (i > 0) {
                fila.add(Box.createRigidArea(new Dimension(hueco, 0)));
            }
            fila.add(componentes[i]);
        }
        fila.setMaximumSize(fila.getPreferredSize());
        return fila;
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = Dibujo.preparar(g);
        int ancho = getWidth();
        int alto = getHeight();

        g2.setPaint(new GradientPaint(0, 0, Tema.FONDO_ARRIBA, 0, alto, Tema.FONDO_ABAJO));
        g2.fillRect(0, 0, ancho, alto);
        // Resplandor morado suave en el centro.
        g2.setPaint(new RadialGradientPaint(new Point2D.Float(ancho / 2f, alto * 0.55f), ancho * 0.65f,
                new float[]{0f, 1f},
                new Color[]{Tema.conAlfa(Tema.MORADO, 40), Tema.conAlfa(Tema.MORADO, 0)}));
        g2.fillRect(0, 0, ancho, alto);

        // Adornos: X y O grandes y desvaidas a los lados, y rejillas de puntos.
        g2.setColor(Tema.DECORACION);
        g2.setStroke(Dibujo.redondo(20f));
        g2.draw(equis(ancho * 0.07, alto * 0.5, 100));
        g2.draw(new Ellipse2D.Double(ancho * 0.94 - 60, alto * 0.36 - 60, 120, 120));
        g2.draw(new Ellipse2D.Double(ancho * 0.07 - 56, alto * 0.82 - 56, 112, 112));
        g2.draw(equis(ancho * 0.93, alto * 0.72, 90));
        pintarPuntos(g2, ancho * 0.04, alto * 0.22);
        pintarPuntos(g2, ancho * 0.88, alto * 0.88);
        g2.dispose();
    }

    private static Path2D equis(double cx, double cy, double tam) {
        double r = tam / 2;
        Path2D equis = new Path2D.Double();
        equis.moveTo(cx - r, cy - r);
        equis.lineTo(cx + r, cy + r);
        equis.moveTo(cx + r, cy - r);
        equis.lineTo(cx - r, cy + r);
        return equis;
    }

    private static void pintarPuntos(Graphics2D g2, double x, double y) {
        g2.setColor(Tema.conAlfa(Tema.LAVANDA, 45));
        for (int fila = 0; fila < 3; fila++) {
            for (int columna = 0; columna < 3; columna++) {
                g2.fill(new Ellipse2D.Double(x + columna * 18, y + fila * 18, 6, 6));
            }
        }
    }
}
