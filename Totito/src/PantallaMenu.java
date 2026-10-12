import java.awt.Dimension;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;

/**
 * Pantalla 1 del diseno: menu principal con Jugar, Instrucciones y Salir.
 */
public class PantallaMenu extends PantallaBase {

    public PantallaMenu(Navegacion navegacion) {
        super(navegacion);

        BotonNeon jugar = BotonNeon.menu("Jugar", Iconos.JUGAR, Tema.ROSA);
        jugar.addActionListener(e -> navegacion.irAConfiguracion());
        BotonNeon instrucciones = BotonNeon.menu("Instrucciones", Iconos.LIBRO, Tema.AZUL);
        instrucciones.addActionListener(e -> navegacion.irAInstrucciones());
        BotonNeon salir = BotonNeon.menu("Salir", Iconos.SALIR, Tema.MORADO);
        salir.addActionListener(e -> navegacion.salir());

        Tarjeta tarjeta = new Tarjeta(Tema.MORADO);
        tarjeta.setLayout(new BoxLayout(tarjeta, BoxLayout.Y_AXIS));
        tarjeta.setBorder(BorderFactory.createEmptyBorder(34, 28, 34, 28));
        tarjeta.add(jugar);
        tarjeta.add(Box.createRigidArea(new Dimension(0, 14)));
        tarjeta.add(instrucciones);
        tarjeta.add(Box.createRigidArea(new Dimension(0, 14)));
        tarjeta.add(salir);

        relleno();
        agregar(tarjeta);
        relleno();
    }
}
