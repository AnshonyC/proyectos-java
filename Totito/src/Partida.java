/**
 * Una serie de partidas entre dos jugadores: el tablero, de quien es el
 * turno, quien gano y el marcador acumulado.
 *
 * Reutiliza tal cual las clases originales del proyecto:
 * - Tablero: guarda las casillas y sabe si hay ganador o empate.
 * - Jugador: nombre y ficha de cada participante.
 * - IA_Minimax: decide la jugada de la computadora en el modo contra la IA.
 *
 * No sabe nada de la interfaz grafica: la pantalla le pide jugar una
 * casilla y despues le pregunta como quedo. Asi las reglas se pueden
 * probar, o usar desde otra interfaz, sin abrir ninguna ventana.
 */
public class Partida {

    /** Los dos modos que se eligen en la pantalla de configuracion. */
    public enum Modo {
        /** Dos personas se turnan en el mismo equipo. */
        DOS_JUGADORES,
        /** El Jugador 2 es la computadora (IA_Minimax). */
        CONTRA_IA
    }

    /** Como va la partida actual. */
    public enum Estado { EN_CURSO, VICTORIA, EMPATE }

    /** Ficha que abre cada partida, como en el totito de siempre. */
    public static final char FICHA_INICIAL = 'X';

    private final Tablero tablero = new Tablero();
    private final Jugador[] jugadores;
    private final Modo modo;
    /** Solo existe en el modo contra la IA; la IA siempre es el Jugador 2. */
    private final IA_Minimax ia;
    private final int[] victorias = new int[2];
    private int empates;

    /** Indice (0 o 1) del jugador al que le toca. */
    private int turno;
    private Estado estado;
    private Jugador ganador;

    public Partida(Jugador jugador1, Jugador jugador2, Modo modo) {
        if (jugador1.getFicha() == jugador2.getFicha()) {
            throw new IllegalArgumentException("Los dos jugadores no pueden usar la misma ficha");
        }
        this.jugadores = new Jugador[]{jugador1, jugador2};
        this.modo = modo;
        this.ia = modo == Modo.CONTRA_IA ? new IA_Minimax(jugador2.getFicha(), jugador1.getFicha()) : null;
        reiniciar();
    }

    /** Limpia el tablero para jugar otra vez. El marcador se conserva. */
    public void reiniciar() {
        tablero.reiniciar();
        estado = Estado.EN_CURSO;
        ganador = null;
        turno = jugadores[0].getFicha() == FICHA_INICIAL ? 0 : 1;
    }

    /**
     * Coloca la ficha del jugador en turno en (fila, columna).
     * Devuelve false si la jugada no vale (partida terminada o casilla
     * ocupada); en ese caso no cambia nada.
     */
    public boolean jugar(int fila, int columna) {
        if (estado != Estado.EN_CURSO) {
            return false;
        }
        if (!tablero.marcarCasilla(fila, columna, jugadores[turno].getFicha())) {
            return false;
        }
        if (tablero.verificarGanador() != Tablero.VACIA) {
            estado = Estado.VICTORIA;
            ganador = jugadores[turno];
            victorias[turno]++;
        } else if (tablero.tableroLleno()) {
            estado = Estado.EMPATE;
            empates++;
        } else {
            turno = 1 - turno;
        }
        return true;
    }

    /** true si la partida sigue y le toca mover a la computadora. */
    public boolean esTurnoDeIA() {
        return ia != null && turno == 1 && estado == Estado.EN_CURSO;
    }

    /** Le pide a IA_Minimax su mejor jugada y la aplica. */
    public void jugarTurnoIA() {
        if (!esTurnoDeIA()) {
            return;
        }
        int[] jugada = ia.calcularMejorJugada(tablero);
        jugar(jugada[0], jugada[1]);
    }

    /** true si ese jugador es la computadora. */
    public boolean esComputadora(Jugador jugador) {
        return ia != null && jugador == jugadores[1];
    }

    public Tablero getTablero() {
        return tablero;
    }

    public Jugador getJugador(int indice) {
        return jugadores[indice];
    }

    public Jugador getJugadorEnTurno() {
        return jugadores[turno];
    }

    public Modo getModo() {
        return modo;
    }

    public Estado getEstado() {
        return estado;
    }

    /** El ganador de la ultima partida, o null si no hay (en curso o empate). */
    public Jugador getGanador() {
        return ganador;
    }

    public int getVictorias(int indice) {
        return victorias[indice];
    }

    public int getEmpates() {
        return empates;
    }

    /**
     * Dice DONDE esta la linea ganadora, para que la interfaz dibuje la
     * raya: {filaInicio, columnaInicio, filaFin, columnaFin}, o null si
     * nadie ha ganado. Revisa lo mismo que Tablero.verificarGanador()
     * (3 filas, 3 columnas y 2 diagonales), pero devolviendo posiciones.
     */
    public static int[] buscarLineaGanadora(Tablero tablero) {
        int[][] lineas = {
            {0, 0, 0, 1, 0, 2}, {1, 0, 1, 1, 1, 2}, {2, 0, 2, 1, 2, 2},   // filas
            {0, 0, 1, 0, 2, 0}, {0, 1, 1, 1, 2, 1}, {0, 2, 1, 2, 2, 2},   // columnas
            {0, 0, 1, 1, 2, 2}, {0, 2, 1, 1, 2, 0}                        // diagonales
        };
        for (int[] l : lineas) {
            char a = tablero.obtenerCasilla(l[0], l[1]);
            if (a != Tablero.VACIA
                    && a == tablero.obtenerCasilla(l[2], l[3])
                    && a == tablero.obtenerCasilla(l[4], l[5])) {
                return new int[]{l[0], l[1], l[4], l[5]};
            }
        }
        return null;
    }
}
