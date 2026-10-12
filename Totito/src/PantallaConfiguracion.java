/**
 * Pantalla 3 del diseno: nombres de los jugadores, simbolo de cada uno y
 * modo de juego, antes de empezar.
 *
 * El diseno trae un solo modo ("2 jugadores"); se agrego "Contra la IA"
 * para no perder la IA_Minimax que ya tenia el proyecto.
 */
public class PantallaConfiguracion extends PantallaBase {

    private static final int ANCHO_SECCION = 560;

    private final Navegacion navegacion;
    private final TarjetaJugador jugador1;
    private final TarjetaJugador jugador2;
    private final SelectorSimbolo selector;
    private final OpcionModo opcionDosJugadores;
    private final OpcionModo opcionContraIA;
    private Partida.Modo modo;

    public PantallaConfiguracion(Navegacion navegacion) {
        super(navegacion);
        this.navegacion = navegacion;

        jugador1 = new TarjetaJugador("Jugador 1", Tema.FRESA);
        jugador2 = new TarjetaJugador("Jugador 2", Tema.AZUL);
        selector = new SelectorSimbolo();
        opcionDosJugadores = new OpcionModo(Iconos.PERSONAS, "2 jugadores", "Turnos en el mismo equipo");
        opcionContraIA = new OpcionModo(Iconos.COMPUTADORA, "Contra la IA", "La computadora usa Minimax");
        opcionDosJugadores.setAlSeleccionar(() -> elegirModo(Partida.Modo.DOS_JUGADORES));
        opcionContraIA.setAlSeleccionar(() -> elegirModo(Partida.Modo.CONTRA_IA));

        BotonNeon comenzar = BotonNeon.pildora("Comenzar partida", Iconos.JUGAR, Tema.ROSA, Tema.MORADO, 440, 66);
        comenzar.addActionListener(e -> comenzar());
        BotonNeon volver = BotonNeon.contorno("Volver", Iconos.FLECHA_IZQUIERDA, 300, 52);
        volver.addActionListener(e -> navegacion.irAlMenu());

        relleno();
        agregar(Rotulo.seccion("JUGADORES", null, ANCHO_SECCION));
        agregar(fila(8, jugador1, jugador2));
        espacio(2);
        agregar(Rotulo.seccion("SÍMBOLOS", "Cada jugador elige su símbolo", ANCHO_SECCION));
        agregar(selector);
        espacio(4);
        agregar(Rotulo.seccion("MODO DE JUEGO", null, ANCHO_SECCION));
        agregar(fila(6, opcionDosJugadores, opcionContraIA));
        espacio(4);
        agregar(comenzar);
        agregar(volver);
        relleno();

        elegirModo(Partida.Modo.DOS_JUGADORES);
    }

    private void elegirModo(Partida.Modo nuevoModo) {
        modo = nuevoModo;
        opcionDosJugadores.setSeleccionada(nuevoModo == Partida.Modo.DOS_JUGADORES);
        opcionContraIA.setSeleccionada(nuevoModo == Partida.Modo.CONTRA_IA);
        jugador2.setComputadora(nuevoModo == Partida.Modo.CONTRA_IA);
    }

    private void comenzar() {
        char fichaJugador1 = selector.getFichaJugador1();
        char fichaJugador2 = fichaJugador1 == 'X' ? 'O' : 'X';
        navegacion.iniciarPartida(
                new Jugador(jugador1.getNombre(), fichaJugador1),
                new Jugador(jugador2.getNombre(), fichaJugador2),
                modo);
    }
}
