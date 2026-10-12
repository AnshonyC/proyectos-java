/**
 * Agente de Inteligencia Artificial que decide su jugada usando el
 * algoritmo Minimax: explora recursivamente el arbol de todas las
 * partidas posibles a partir del estado actual, asumiendo que la IA
 * siempre maximiza su resultado y el jugador siempre lo minimiza.
 * Como el Totito es un juego de suma cero con pocos estados posibles,
 * el arbol se puede recorrer por completo, garantizando que la IA
 * nunca pierda (gana o empata en todas las partidas).
 */
public class IA_Minimax {

    private final char fichaIA;
    private final char fichaJugador;

    public IA_Minimax(char fichaIA, char fichaJugador) {
        this.fichaIA = fichaIA;
        this.fichaJugador = fichaJugador;
    }

    /**
     * Evalua cada casilla vacia disponible, simula la jugada en una copia
     * del tablero y se queda con la de mayor puntaje segun Minimax.
     * Retorna {fila, columna} de la mejor jugada encontrada.
     */
    public int[] calcularMejorJugada(Tablero tablero) {
        int mejorValor = Integer.MIN_VALUE;
        int[] mejorJugada = new int[]{-1, -1};

        for (int fila = 0; fila < 3; fila++) {
            for (int columna = 0; columna < 3; columna++) {
                if (tablero.obtenerCasilla(fila, columna) == Tablero.VACIA) {
                    Tablero copia = tablero.obtenerCopia();
                    copia.marcarCasilla(fila, columna, fichaIA);
                    int valor = minimax(copia, 0, false);
                    if (valor > mejorValor) {
                        mejorValor = valor;
                        mejorJugada[0] = fila;
                        mejorJugada[1] = columna;
                    }
                }
            }
        }
        return mejorJugada;
    }

    /**
     * Funcion recursiva Minimax.
     * - Caso base: si el tablero ya tiene un ganador o esta lleno, retorna
     *   el puntaje de esa hoja del arbol (+10 si gana la IA, -10 si gana
     *   el jugador, 0 si es empate). Se resta/suma la profundidad para que
     *   la IA prefiera ganar rapido y perder (si fuera inevitable) tarde.
     * - Caso recursivo: prueba cada casilla vacia, simula la jugada del
     *   turno correspondiente y llama a minimax con el turno contrario.
     *   Si es turno de la IA (esMax = true) se queda con el valor MAXIMO
     *   entre las opciones; si es turno del jugador (esMax = false) se
     *   queda con el valor MINIMO, ya que se asume que el jugador tambien
     *   jugara de forma optima en su contra.
     */
    private int minimax(Tablero tablero, int profundidad, boolean esMax) {
        char ganador = tablero.verificarGanador();
        if (ganador == fichaIA) {
            return 10 - profundidad;
        }
        if (ganador == fichaJugador) {
            return profundidad - 10;
        }
        if (tablero.tableroLleno()) {
            return 0;
        }

        if (esMax) {
            int mejor = Integer.MIN_VALUE;
            for (int fila = 0; fila < 3; fila++) {
                for (int columna = 0; columna < 3; columna++) {
                    if (tablero.obtenerCasilla(fila, columna) == Tablero.VACIA) {
                        Tablero copia = tablero.obtenerCopia();
                        copia.marcarCasilla(fila, columna, fichaIA);
                        mejor = Math.max(mejor, minimax(copia, profundidad + 1, false));
                    }
                }
            }
            return mejor;
        } else {
            int menor = Integer.MAX_VALUE;
            for (int fila = 0; fila < 3; fila++) {
                for (int columna = 0; columna < 3; columna++) {
                    if (tablero.obtenerCasilla(fila, columna) == Tablero.VACIA) {
                        Tablero copia = tablero.obtenerCopia();
                        copia.marcarCasilla(fila, columna, fichaJugador);
                        menor = Math.min(menor, minimax(copia, profundidad + 1, true));
                    }
                }
            }
            return menor;
        }
    }
}
