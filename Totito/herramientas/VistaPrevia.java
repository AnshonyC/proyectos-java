import java.awt.Dimension;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;

/**
 * Abre UNA pantalla suelta en una ventana, para verla mientras se
 * construye la interfaz, antes de que existan PanelPrincipal y TotitoApp.
 * Los botones que cambian de pantalla no hacen nada (salvo cerrar).
 *
 * Para ver otra pantalla, cambiar la linea marcada con  <-- AQUI.
 *
 * Ejecutar desde la carpeta Totito, despues de compilar el proyecto:
 *   java -cp target/classes herramientas/VistaPrevia.java
 */
public class VistaPrevia {

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            // Una Navegacion "de mentira": cada metodo existe pero no hace nada.
            Navegacion sinNavegacion = new Navegacion() {
                @Override public void irAlMenu() { }
                @Override public void irAInstrucciones() { }
                @Override public void irAConfiguracion() { }
                @Override public void iniciarPartida(Jugador j1, Jugador j2, Partida.Modo modo) { }
                @Override public void mostrarResultado(Partida partida) { }
                @Override public void jugarDeNuevo() { }
                @Override public void salir() { System.exit(0); }
            };

            JPanel pantalla = new PantallaMenu(sinNavegacion);   // <-- AQUI
            pantalla.setPreferredSize(new Dimension(640, 690));

            JFrame ventana = new JFrame("Vista previa");
            ventana.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            ventana.setContentPane(pantalla);
            ventana.pack();
            ventana.setLocationRelativeTo(null);
            ventana.setVisible(true);
        });
    }
}
