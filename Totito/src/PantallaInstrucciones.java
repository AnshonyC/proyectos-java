import java.awt.Dimension;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;

/**
 * Pantalla 2 del diseno: "Cómo jugar", tres pasos y un tablero de ejemplo.
 */
public class PantallaInstrucciones extends PantallaBase {

    private static final int ANCHO_PASOS = 400;

    public PantallaInstrucciones(Navegacion navegacion) {
        super(navegacion);

        String x = "<font color='" + Tema.hex(Tema.ROSA) + "'><b>X</b></font>";
        String o = "<font color='" + Tema.hex(Tema.AZUL) + "'><b>O</b></font>";

        Tarjeta tarjeta = new Tarjeta(Tema.MORADO);
        tarjeta.setLayout(new BoxLayout(tarjeta, BoxLayout.Y_AXIS));
        tarjeta.setBorder(BorderFactory.createEmptyBorder(20, 30, 22, 30));
        tarjeta.add(Rotulo.titulo("Cómo jugar", 36f, Tema.TEXTO, Tema.LAVANDA, ANCHO_PASOS, 70)
                .conIcono(Iconos.LIBRO, Tema.ROSA)
                .conSubrayado(Tema.ROSA, Tema.AZUL));
        tarjeta.add(Box.createRigidArea(new Dimension(0, 6)));
        tarjeta.add(new PasoInstruccion(1, Tema.ROSA,
                "Dos jugadores se turnan<br>para marcar " + x + " y " + o + ".", ANCHO_PASOS));
        tarjeta.add(new PasoInstruccion(2, Tema.MORADO,
                "Gana quien forme una<br>línea de 3 símbolos.", ANCHO_PASOS));
        tarjeta.add(new PasoInstruccion(3, Tema.AZUL,
                "Si el tablero se llena<br>sin línea, hay empate.", ANCHO_PASOS));
        tarjeta.add(Box.createRigidArea(new Dimension(0, 10)));
        tarjeta.add(tableroDeEjemplo());

        BotonNeon regresar = BotonNeon.pildora("Regresar", Iconos.FLECHA_IZQUIERDA,
                Tema.ROSA, Tema.MORADO, 330, 70);
        regresar.addActionListener(e -> navegacion.irAlMenu());

        relleno();
        agregar(tarjeta);
        espacio(8);
        agregar(regresar);
        relleno();
    }

    /** El mismo dibujo del diseno: O X O en la fila de arriba y una X al centro. */
    private static PanelTablero tableroDeEjemplo() {
        Tablero ejemplo = new Tablero();
        ejemplo.marcarCasilla(0, 0, 'O');
        ejemplo.marcarCasilla(0, 1, 'X');
        ejemplo.marcarCasilla(0, 2, 'O');
        ejemplo.marcarCasilla(1, 1, 'X');
        PanelTablero panel = new PanelTablero(46);
        panel.mostrar(ejemplo);
        return panel;
    }
}
