import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;

/**
 * Punto de entrada y controlador del juego. Construye la interfaz en
 * Swing, mantiene el turno actual y coordina las llamadas entre el
 * Tablero (estado/reglas) y la IA_Minimax (decision de la maquina).
 */
public class JuegoMain extends JFrame {

    private static final char FICHA_JUGADOR = 'X';
    private static final char FICHA_IA = 'O';

    private static final Color COLOR_FONDO = new Color(0xED, 0xEE, 0xF0);
    private static final Color COLOR_CASILLA = Color.WHITE;
    private static final Color COLOR_X = new Color(0x18, 0x5F, 0xA5);
    private static final Color COLOR_O = new Color(0x99, 0x3C, 0x1D);
    private static final Color COLOR_BORDE = new Color(0xD3, 0xD1, 0xC7);

    private final Tablero tablero;
    private final Jugador jugador;
    private final IA_Minimax ia;
    private final JButton[][] botones;
    private final JLabel etiquetaEstado;

    private boolean turnoJugador;
    private boolean juegoTerminado;

    public JuegoMain() {
        super("Totito - Minimax AI");

        tablero = new Tablero();
        jugador = new Jugador("Jugador", FICHA_JUGADOR);
        ia = new IA_Minimax(FICHA_IA, FICHA_JUGADOR);
        botones = new JButton[3][3];

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(false);
        getContentPane().setBackground(COLOR_FONDO);
        setLayout(new BorderLayout(0, 16));
        ((JPanel) getContentPane()).setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        etiquetaEstado = crearEtiquetaEstado();
        add(etiquetaEstado, BorderLayout.NORTH);
        add(crearPanelTablero(), BorderLayout.CENTER);
        add(crearBotonReiniciar(), BorderLayout.SOUTH);

        turnoJugador = true;
        juegoTerminado = false;

        pack();
        setLocationRelativeTo(null);
        setVisible(true);
    }

    private JLabel crearEtiquetaEstado() {
        JLabel etiqueta = new JLabel("Tu turno (X)", SwingConstants.CENTER);
        etiqueta.setFont(new Font("SansSerif", Font.BOLD, 16));
        etiqueta.setOpaque(true);
        etiqueta.setBackground(Color.WHITE);
        etiqueta.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(COLOR_BORDE, 1),
                BorderFactory.createEmptyBorder(10, 10, 10, 10)));
        return etiqueta;
    }

    private JPanel crearPanelTablero() {
        JPanel panelTablero = new JPanel(new GridLayout(3, 3, 4, 4));
        panelTablero.setBackground(COLOR_BORDE);
        panelTablero.setBorder(BorderFactory.createLineBorder(COLOR_BORDE, 1));

        for (int fila = 0; fila < 3; fila++) {
            for (int columna = 0; columna < 3; columna++) {
                JButton boton = new JButton("");
                boton.setFont(new Font("SansSerif", Font.BOLD, 48));
                boton.setBackground(COLOR_CASILLA);
                boton.setFocusPainted(false);
                boton.setBorderPainted(false);
                boton.setOpaque(true);
                boton.setPreferredSize(new Dimension(100, 100));

                final int f = fila;
                final int c = columna;
                boton.addActionListener((ActionEvent e) -> manejarClicCasilla(f, c));

                botones[fila][columna] = boton;
                panelTablero.add(boton);
            }
        }
        return panelTablero;
    }

    private JButton crearBotonReiniciar() {
        JButton botonReiniciar = new JButton("Nueva partida / Reiniciar");
        botonReiniciar.setFont(new Font("SansSerif", Font.PLAIN, 14));
        botonReiniciar.setFocusPainted(false);
        botonReiniciar.addActionListener((ActionEvent e) -> reiniciarPartida());
        return botonReiniciar;
    }

    /** Maneja el clic del jugador humano sobre una casilla. */
    private void manejarClicCasilla(int fila, int columna) {
        if (juegoTerminado || !turnoJugador) {
            return;
        }
        if (!tablero.marcarCasilla(fila, columna, jugador.getFicha())) {
            return;
        }

        actualizarBoton(fila, columna);
        if (verificarFinDePartida()) {
            return;
        }

        turnoJugador = false;
        etiquetaEstado.setText("Turno de la IA (O)");

        // Pequena pausa para que el cambio de turno se sienta natural
        // antes de que la IA responda.
        Timer temporizador = new Timer(350, null);
        temporizador.addActionListener(e -> {
            turnoIA();
            temporizador.stop();
        });
        temporizador.setRepeats(false);
        temporizador.start();
    }

    /** Le pide a la IA su mejor jugada segun Minimax y la aplica al tablero. */
    private void turnoIA() {
        int[] jugada = ia.calcularMejorJugada(tablero);
        if (jugada[0] == -1) {
            return;
        }
        tablero.marcarCasilla(jugada[0], jugada[1], FICHA_IA);
        actualizarBoton(jugada[0], jugada[1]);

        if (verificarFinDePartida()) {
            return;
        }

        turnoJugador = true;
        etiquetaEstado.setText("Tu turno (X)");
    }

    private void actualizarBoton(int fila, int columna) {
        char ficha = tablero.obtenerCasilla(fila, columna);
        JButton boton = botones[fila][columna];
        boton.setText(String.valueOf(ficha));
        boton.setForeground(ficha == FICHA_JUGADOR ? COLOR_X : COLOR_O);
        boton.setEnabled(false);
    }

    /** Revisa si hay ganador o empate y actualiza la interfaz en consecuencia. */
    private boolean verificarFinDePartida() {
        char ganador = tablero.verificarGanador();
        if (ganador != Tablero.VACIA) {
            juegoTerminado = true;
            etiquetaEstado.setText(ganador == FICHA_JUGADOR ? "Ganaste (X)" : "Gana la IA (O)");
            deshabilitarTodasLasCasillas();
            return true;
        }
        if (tablero.tableroLleno()) {
            juegoTerminado = true;
            etiquetaEstado.setText("Empate");
            return true;
        }
        return false;
    }

    private void deshabilitarTodasLasCasillas() {
        for (int fila = 0; fila < 3; fila++) {
            for (int columna = 0; columna < 3; columna++) {
                botones[fila][columna].setEnabled(false);
            }
        }
    }

    /** Reinicia el tablero y la interfaz para una nueva partida. */
    private void reiniciarPartida() {
        tablero.reiniciar();
        juegoTerminado = false;
        turnoJugador = true;
        etiquetaEstado.setText("Tu turno (X)");

        for (int fila = 0; fila < 3; fila++) {
            for (int columna = 0; columna < 3; columna++) {
                botones[fila][columna].setText("");
                botones[fila][columna].setEnabled(true);
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(JuegoMain::new);
    }
}
