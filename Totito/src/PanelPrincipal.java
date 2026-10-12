import java.awt.CardLayout;
import java.awt.Dimension;
import javax.swing.JPanel;

/**
 * Contiene todas las pantallas y muestra una a la vez (CardLayout, como
 * un mazo de cartas). Implementa Navegacion: es quien cambia de pantalla
 * cuando una de ellas lo pide, y quien guarda la Partida en curso.
 *
 * Es un JPanel y no la ventana, asi se puede probar o dibujar en una
 * imagen sin abrir una ventana real.
 */
public class PanelPrincipal extends JPanel implements Navegacion {

    /** Tamano de la ventana. Cabe en pantallas de 1366x768. */
    public static final int ANCHO = 640;
    public static final int ALTO = 690;

    private static final String MENU = "menu";
    private static final String INSTRUCCIONES = "instrucciones";
    private static final String CONFIGURACION = "configuracion";
    private static final String JUEGO = "juego";
    private static final String RESULTADO = "resultado";

    private final CardLayout cartas = new CardLayout();
    private final PantallaJuego pantallaJuego;
    private final PantallaResultado pantallaResultado;
    private final Runnable alSalir;
    private Partida partida;

    /** @param alSalir que hacer al pulsar Salir o la X (cerrar la ventana). */
    public PanelPrincipal(Runnable alSalir) {
        this.alSalir = alSalir;
        setLayout(cartas);
        setPreferredSize(new Dimension(ANCHO, ALTO));

        pantallaJuego = new PantallaJuego(this);
        pantallaResultado = new PantallaResultado(this);
        add(new PantallaMenu(this), MENU);
        add(new PantallaInstrucciones(this), INSTRUCCIONES);
        add(new PantallaConfiguracion(this), CONFIGURACION);
        add(pantallaJuego, JUEGO);
        add(pantallaResultado, RESULTADO);
        cartas.show(this, MENU);
    }

    /** La partida en curso (null si aun no se ha empezado ninguna). */
    public Partida getPartida() {
        return partida;
    }

    @Override
    public void irAlMenu() {
        cartas.show(this, MENU);
    }

    @Override
    public void irAInstrucciones() {
        cartas.show(this, INSTRUCCIONES);
    }

    @Override
    public void irAConfiguracion() {
        cartas.show(this, CONFIGURACION);
    }

    @Override
    public void iniciarPartida(Jugador jugador1, Jugador jugador2, Partida.Modo modo) {
        partida = new Partida(jugador1, jugador2, modo);
        pantallaJuego.comenzar(partida);
        cartas.show(this, JUEGO);
    }

    @Override
    public void mostrarResultado(Partida partidaTerminada) {
        pantallaResultado.mostrar(partidaTerminada);
        cartas.show(this, RESULTADO);
    }

    @Override
    public void jugarDeNuevo() {
        partida.reiniciar();
        pantallaJuego.comenzar(partida);
        cartas.show(this, JUEGO);
    }

    @Override
    public void salir() {
        alSalir.run();
    }
}
