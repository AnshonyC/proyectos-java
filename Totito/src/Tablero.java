/**
 * Representa el tablero de 3x3 del juego Totito.
 * Se encarga unicamente del estado del juego (casillas, validaciones,
 * deteccion de victoria/empate). No conoce nada de la interfaz grafica
 * ni de la logica de la IA.
 */
public class Tablero {

    public static final char VACIA = ' ';

    private char[][] casillas;

    public Tablero() {
        casillas = new char[3][3];
        reiniciar();
    }

    /** Deja el tablero vacio, listo para una nueva partida. */
    public void reiniciar() {
        for (int fila = 0; fila < 3; fila++) {
            for (int columna = 0; columna < 3; columna++) {
                casillas[fila][columna] = VACIA;
            }
        }
    }

    /**
     * Intenta colocar una ficha en la posicion indicada.
     * Retorna false si la posicion esta fuera de rango o ya esta ocupada,
     * evitando asi tiros duplicados o invalidos.
     */
    public boolean marcarCasilla(int fila, int columna, char ficha) {
        if (fila < 0 || fila > 2 || columna < 0 || columna > 2) {
            return false;
        }
        if (casillas[fila][columna] != VACIA) {
            return false;
        }
        casillas[fila][columna] = ficha;
        return true;
    }

    public char obtenerCasilla(int fila, int columna) {
        return casillas[fila][columna];
    }

    /** Retorna true si ya no quedan casillas vacias. */
    public boolean tableroLleno() {
        for (int fila = 0; fila < 3; fila++) {
            for (int columna = 0; columna < 3; columna++) {
                if (casillas[fila][columna] == VACIA) {
                    return false;
                }
            }
        }
        return true;
    }

    /**
     * Revisa las 3 filas, 3 columnas y 2 diagonales.
     * Retorna la ficha ganadora ('X' u 'O') o VACIA si nadie ha ganado aun.
     */
    public char verificarGanador() {
        for (int i = 0; i < 3; i++) {
            if (casillas[i][0] != VACIA && casillas[i][0] == casillas[i][1] && casillas[i][1] == casillas[i][2]) {
                return casillas[i][0];
            }
            if (casillas[0][i] != VACIA && casillas[0][i] == casillas[1][i] && casillas[1][i] == casillas[2][i]) {
                return casillas[0][i];
            }
        }
        if (casillas[0][0] != VACIA && casillas[0][0] == casillas[1][1] && casillas[1][1] == casillas[2][2]) {
            return casillas[0][0];
        }
        if (casillas[0][2] != VACIA && casillas[0][2] == casillas[1][1] && casillas[1][1] == casillas[2][0]) {
            return casillas[0][2];
        }
        return VACIA;
    }

    /** Crea una copia independiente del tablero, usada por el algoritmo Minimax
     *  para simular jugadas sin afectar la partida real. */
    public Tablero obtenerCopia() {
        Tablero copia = new Tablero();
        for (int fila = 0; fila < 3; fila++) {
            for (int columna = 0; columna < 3; columna++) {
                copia.casillas[fila][columna] = this.casillas[fila][columna];
            }
        }
        return copia;
    }
}
