import java.awt.Cursor;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.geom.Ellipse2D;
import java.awt.geom.RoundRectangle2D;
import javax.swing.JComponent;

/**
 * Una opcion del "Modo de juego" (boton de radio con icono, titulo y
 * descripcion). La pantalla que la usa decide cual queda marcada: al hacer
 * clic solo se avisa con el Runnable de setAlSeleccionar().
 */
public class OpcionModo extends JComponent {

    public static final int ANCHO = 290;
    public static final int ALTO = 72;
    private static final int MARGEN = 7;

    private final Iconos.Icono icono;
    private final String titulo;
    private final String descripcion;
    private boolean seleccionada;
    private Runnable alSeleccionar;

    public OpcionModo(Iconos.Icono icono, String titulo, String descripcion) {
        this.icono = icono;
        this.titulo = titulo;
        this.descripcion = descripcion;
        Dibujo.fijarTamano(this, ANCHO, ALTO);
        setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                if (alSeleccionar != null) {
                    alSeleccionar.run();
                }
            }
        });
    }

    public void setAlSeleccionar(Runnable accion) {
        this.alSeleccionar = accion;
    }

    public void setSeleccionada(boolean seleccionada) {
        this.seleccionada = seleccionada;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = Dibujo.preparar(g);
        RoundRectangle2D forma = new RoundRectangle2D.Double(MARGEN, MARGEN,
                getWidth() - 2.0 * MARGEN, getHeight() - 2.0 * MARGEN, 22, 22);
        g2.setColor(Tema.conAlfa(Tema.MORADO, seleccionada ? 38 : 12));
        g2.fill(forma);
        Dibujo.trazoNeon(g2, forma, seleccionada ? Tema.aclarar(Tema.MORADO, 0.15f) : Tema.MORADO, 1.8f,
                seleccionada ? 1.2f : 0.35f);

        // Boton de radio.
        double cx = MARGEN + 26;
        double cy = getHeight() / 2.0;
        Ellipse2D aro = new Ellipse2D.Double(cx - 10, cy - 10, 20, 20);
        if (seleccionada) {
            Dibujo.trazoNeon(g2, aro, Tema.ROSA, 2.2f, 0.9f);
            g2.setColor(Tema.aclarar(Tema.ROSA, 0.45f));
            g2.fill(new Ellipse2D.Double(cx - 5, cy - 5, 10, 10));
        } else {
            Dibujo.trazo(g2, aro, Tema.conAlfa(Tema.LAVANDA, 110), 1.8f);
        }

        icono.dibujar(g2, MARGEN + 48, cy - 17, 34, seleccionada ? Tema.LAVANDA : Tema.TEXTO_SUAVE);

        g2.setFont(Tema.fuente(Font.BOLD, 16f));
        g2.setColor(seleccionada ? Tema.TEXTO : Tema.TEXTO_SUAVE);
        g2.drawString(titulo, MARGEN + 92, (float) cy - 3);
        g2.setFont(Tema.fuente(Font.PLAIN, 12f));
        g2.setColor(Tema.TEXTO_SUAVE);
        g2.drawString(descripcion, MARGEN + 92, (float) cy + 15);
        g2.dispose();
    }
}
