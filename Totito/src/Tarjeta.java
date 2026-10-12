import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.RoundRectangle2D;
import javax.swing.JPanel;

/**
 * Panel "de cristal": rectangulo redondeado semitransparente con borde de
 * neon. Es la caja que envuelve el menu, las instrucciones, las tarjetas de
 * jugador y el resultado. Se le agregan componentes como a cualquier JPanel.
 *
 * Las subclases pueden sobrescribir pintarDecoracion() para dibujar algo
 * encima del fondo y debajo de los componentes (por ejemplo, confeti).
 */
public class Tarjeta extends JPanel {

    /** Espacio entre el borde del componente y la caja, para que quepa el halo. */
    public static final int MARGEN = 10;

    private final Color color;
    private final int arco;

    public Tarjeta(Color color) {
        this(color, 30);
    }

    public Tarjeta(Color color, int arco) {
        this.color = color;
        this.arco = arco;
        setOpaque(false);
        setAlignmentX(CENTER_ALIGNMENT);
    }

    /** La caja redondeada, ya descontado el margen del halo. */
    protected RoundRectangle2D forma() {
        return new RoundRectangle2D.Double(MARGEN, MARGEN,
                getWidth() - 2.0 * MARGEN, getHeight() - 2.0 * MARGEN, arco, arco);
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = Dibujo.preparar(g);
        RoundRectangle2D forma = forma();
        g2.setColor(Tema.SUPERFICIE);
        g2.fill(forma);
        g2.setColor(Tema.conAlfa(color, 12));
        g2.fill(forma);
        pintarDecoracion(g2, forma);
        Dibujo.trazoNeon(g2, forma, color, 1.8f);
        g2.dispose();
    }

    /** Gancho para las subclases. Por defecto no dibuja nada. */
    protected void pintarDecoracion(Graphics2D g2, RoundRectangle2D forma) {
    }
}
