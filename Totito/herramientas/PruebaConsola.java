import java.util.Scanner;

/**
 * Prueba de las clases de logica (Tablero, Jugador e IA_Minimax) en la
 * consola, antes de que exista la interfaz grafica. Se juega con la X
 * contra la IA escribiendo la fila y la columna (de 0 a 2).
 *
 * Ejecutar desde la carpeta Totito, despues de compilar el proyecto:
 *   java -cp target/classes herramientas/PruebaConsola.java
 */
public class PruebaConsola {

    public static void main(String[] args) {
        Tablero tablero = new Tablero();
        Jugador humano = new Jugador("Tu", 'X');
        IA_Minimax ia = new IA_Minimax('O', 'X');
        Scanner teclado = new Scanner(System.in);

        System.out.println("Totito en consola. Escribe fila y columna (0 a 2), por ejemplo: 1 1");
        imprimir(tablero);
        while (true) {
            System.out.print("Tu jugada: ");
            if (!teclado.hasNextInt()) {
                return;   // se cerro la entrada: terminar sin error
            }
            int fila = teclado.nextInt();
            int columna = teclado.nextInt();
            if (!tablero.marcarCasilla(fila, columna, humano.getFicha())) {
                System.out.println("Esa casilla no se puede usar. Prueba otra.");
                continue;
            }
            imprimir(tablero);
            if (terminoLaPartida(tablero)) {
                return;
            }

            int[] jugada = ia.calcularMejorJugada(tablero);
            tablero.marcarCasilla(jugada[0], jugada[1], 'O');
            System.out.println("La IA juega en " + jugada[0] + " " + jugada[1]);
            imprimir(tablero);
            if (terminoLaPartida(tablero)) {
                return;
            }
        }
    }

    /** Escribe el resultado si alguien gano o si hubo empate. */
    private static boolean terminoLaPartida(Tablero tablero) {
        char ganador = tablero.verificarGanador();
        if (ganador != Tablero.VACIA) {
            System.out.println("Gano " + ganador);
            return true;
        }
        if (tablero.tableroLleno()) {
            System.out.println("Empate");
            return true;
        }
        return false;
    }

    /** Dibuja el tablero con caracteres:  X | O |   */
    private static void imprimir(Tablero tablero) {
        System.out.println();
        for (int fila = 0; fila < 3; fila++) {
            System.out.println(" " + tablero.obtenerCasilla(fila, 0)
                    + " | " + tablero.obtenerCasilla(fila, 1)
                    + " | " + tablero.obtenerCasilla(fila, 2));
            if (fila < 2) {
                System.out.println("---+---+---");
            }
        }
        System.out.println();
    }
}
