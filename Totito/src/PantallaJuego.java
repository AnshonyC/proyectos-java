import java.awt.Color;
import javax.swing.Timer;

/**
 * Pantalla de la partida: marcador, de quien es el turno y el tablero.
 * (El diseno no trae esta pantalla; se hizo con el mismo estilo.)
 *
 * Hace el papel que tenia JuegoMain en la version original: recibe los
 * clics, se los pasa a la Partida y, en el modo contra la IA, espera un
 * momento y hace jugar a la computadora. Cuando la partida termina deja
 * ver la raya ganadora un instante y pasa a la pantalla de resultado.
 */
public class PantallaJuego extends PantallaBase {

    /** Pausa antes de que juegue la IA, para que el cambio de turno se note. */
    private static final int PAUSA_IA_MS = 450;
    /** Tiempo que se ve la raya ganadora antes de cambiar de pantalla. */
    private static final int PAUSA_RESULTADO_MS = 1200;

    private final Navegacion navegacion;
    private final PanelMarcador marcador = new PanelMarcador();
    private final Rotulo turno = Rotulo.titulo("", 26f, Tema.TEXTO, Tema.TEXTO, 590, 44);
    private final PanelTablero tablero = new PanelTablero(100);

    private Partida partida;
    /** Temporizador en espera (jugada de la IA o paso al resultado), o null. */
    private Timer pendiente;

    public PantallaJuego(Navegacion navegacion) {
        super(navegacion);
        this.navegacion = navegacion;
        tablero.setOyente(this::alPulsarCasilla);

        BotonNeon reiniciar = BotonNeon.contorno("Reiniciar", Iconos.REINICIAR, 250, 66);
        reiniciar.addActionListener(e -> {
            partida.reiniciar();
            comenzar(partida);
        });
        BotonNeon menu = BotonNeon.pildora("Menú principal", Iconos.CASA, Tema.AZUL, Tema.MORADO, 270, 66);
        menu.addActionListener(e -> {
            cancelarPendiente();
            navegacion.irAlMenu();
        });

        relleno();
        agregar(marcador);
        espacio(2);
        agregar(turno);
        agregar(tablero);
        espacio(6);
        agregar(fila(8, reiniciar, menu));
        relleno();
    }

    /** Muestra la partida (nueva o reiniciada) y, si empieza la IA, la pone a jugar. */
    public void comenzar(Partida partida) {
        cancelarPendiente();
        this.partida = partida;
        actualizar();
        programarTurnoIA();
    }

    private void alPulsarCasilla(int fila, int columna) {
        if (pendiente != null || partida.esTurnoDeIA()) {
            return;   // mientras la IA "piensa" no se aceptan clics
        }
        if (partida.jugar(fila, columna)) {
            despuesDeJugada();
        }
    }

    private void despuesDeJugada() {
        actualizar();
        if (partida.getEstado() == Partida.Estado.EN_CURSO) {
            programarTurnoIA();
        } else {
            esperar(PAUSA_RESULTADO_MS, () -> navegacion.mostrarResultado(partida));
        }
    }

    private void programarTurnoIA() {
        if (partida.esTurnoDeIA()) {
            esperar(PAUSA_IA_MS, () -> {
                partida.jugarTurnoIA();
                despuesDeJugada();
            });
        }
    }

    /** Ejecuta la accion una sola vez, dentro de "ms" milisegundos. */
    private void esperar(int ms, Runnable accion) {
        cancelarPendiente();
        pendiente = new Timer(ms, e -> {
            pendiente = null;
            accion.run();
        });
        pendiente.setRepeats(false);
        pendiente.start();
    }

    /** Evita que un temporizador viejo actue sobre una partida que ya se reinicio o se dejo. */
    private void cancelarPendiente() {
        if (pendiente != null) {
            pendiente.stop();
            pendiente = null;
        }
    }

    /** Refresca tablero, marcador y el letrero del turno segun la partida. */
    private void actualizar() {
        tablero.mostrar(partida.getTablero());
        marcador.mostrar(partida);

        Jugador enTurno = partida.getJugadorEnTurno();
        boolean enCurso = partida.getEstado() == Partida.Estado.EN_CURSO;
        tablero.setInteractivo(enCurso && !partida.esTurnoDeIA());
        tablero.setFichaFantasma(enTurno.getFicha());

        switch (partida.getEstado()) {
            case EN_CURSO -> {
                Color color = Tema.colorDeFicha(enTurno.getFicha());
                String texto = partida.esTurnoDeIA()
                        ? "La computadora está pensando…"
                        : "Turno de " + enTurno.getNombre();
                turno.setTexto(texto, Tema.aclarar(color, 0.35f), color);
            }
            case VICTORIA -> {
                Color color = Tema.colorDeFicha(partida.getGanador().getFicha());
                turno.setTexto("¡Tres en línea!", Tema.aclarar(color, 0.35f), color);
            }
            case EMPATE -> turno.setTexto("¡Empate!", Tema.LAVANDA, Tema.MORADO);
        }
    }
}
