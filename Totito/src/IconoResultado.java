import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.Line2D;
import javax.swing.JComponent;

/**
 * La ilustracion de arriba de la pantalla de resultado: un trofeo con
 * destellos si alguien gano, o una X y una O juntas si hubo empate.
 */
public class IconoResultado extends JComponent {

    /** Angulos (en grados) de los destellos alrededor del trofeo. */
    private static final int[] ANGULOS = {145, 180, 215, 35, 0, -35};
    private static final Color[] COLORES = {Tema.ROSA, Tema.CIAN, Tema.MORADO};

    private boolean empate;

    public IconoResultado() {
        Dibujo.fijarTamano(this, 260, 100);
        setAlignmentX(CENTER_ALIGNMENT);
    }

    public void setEmpate(boolean empate) {
        this.empate = empate;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = Dibujo.preparar(g);
        double cx = getWidth() / 2.0;
        double cy = getHeight() / 2.0;
        if (empate) {
            Dibujo.dibujarFicha(g2, 'X', cx - 40, cy, 54, 7f);
            Dibujo.dibujarFicha(g2, 'O', cx + 40, cy, 54, 7f);
        } else {
            for (int i = 0; i < ANGULOS.length; i++) {
                double a = Math.toRadians(ANGULOS[i]);
                double r1 = 58;
                double r2 = i % 3 == 1 ? 80 : 72;   // el destello del medio es mas largo
                Line2D destello = new Line2D.Double(
                        cx + Math.cos(a) * r1, cy - Math.sin(a) * r1,
                        cx + Math.cos(a) * r2, cy - Math.sin(a) * r2);
                Dibujo.trazoNeon(g2, destello, COLORES[i % COLORES.length], 3.5f, 0.8f);
            }
            Iconos.TROFEO.dibujar(g2, cx - 42, cy - 44, 84, Tema.CIAN);
        }
        g2.dispose();
    }
}
