import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.geom.RoundRectangle2D;
import javax.swing.JFrame;
import javax.swing.SwingUtilities;

/**
 * PUNTO DE ENTRADA de la version con interfaz neon (la del diseno).
 * Para jugar, ejecutar el main de esta clase.
 *
 * La version original, con la ventana sencilla de Jugador contra IA,
 * sigue en JuegoMain y tambien se puede ejecutar.
 */
public class TotitoApp extends JFrame {

    public TotitoApp() {
        super("Juego del Totito");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(false);
        setIconImage(crearIcono());
        setContentPane(new PanelPrincipal(this::cerrar));
        pack();
        setLocationRelativeTo(null);   // centrada en la pantalla
    }

    private void cerrar() {
        dispose();
        System.exit(0);
    }

    /** Icono de la ventana (barra de tareas): el logotipo sobre fondo oscuro. */
    private static Image crearIcono() {
        BufferedImage imagen = new BufferedImage(64, 64, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = Dibujo.preparar(imagen.getGraphics());
        g2.setColor(Tema.FONDO_ARRIBA);
        g2.fill(new RoundRectangle2D.Double(0, 0, 64, 64, 16, 16));
        Iconos.LOGO.dibujar(g2, 8, 8, 48, Tema.LAVANDA);
        g2.dispose();
        return imagen;
    }

    public static void main(String[] args) {
        // Texto suavizado tambien en Linux.
        System.setProperty("awt.useSystemAAFontSettings", "on");
        SwingUtilities.invokeLater(() -> new TotitoApp().setVisible(true));
    }
}
