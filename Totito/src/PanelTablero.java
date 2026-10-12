import java.awt.AlphaComposite;
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.geom.Line2D;
import java.awt.geom.RoundRectangle2D;
import javax.swing.JComponent;

/**
 * Dibuja un Tablero de 3x3 con fichas de neon y, si alguien gano, la raya
 * sobre las tres fichas de la linea ganadora.
 *
 * Solo DIBUJA: no sabe de reglas ni de turnos. Cuando el usuario hace clic
 * en una casilla avisa al OyenteCasilla y es la pantalla quien decide que
 * hacer. Se usa en tres sitios: la partida (interactivo), la pantalla de
 * victoria y el ejemplo de las instrucciones (solo de muestra).
 */
public class PanelTablero extends JComponent {

    /** Quien quiera enterarse de los clics implementa esta interfaz. */
    public interface OyenteCasilla {
        void casillaPulsada(int fila, int columna);
    }

    private static final int MARGEN = 10;   // espacio para el halo del borde
    private static final int RELLENO = 8;   // del borde a la primera casilla

    private final char[][] fichas = new char[3][3];
    private int[] lineaGanadora;            // {fila1, col1, fila2, col2} o null
    private OyenteCasilla oyente;
    private boolean interactivo;
    /** Ficha que se ve transparente al pasar el raton (la del jugador en turno). */
    private char fichaFantasma = Tablero.VACIA;
    private int filaEncima = -1;
    private int columnaEncima = -1;

    /** @param tamCasilla lado de cada casilla en pixeles. */
    public PanelTablero(int tamCasilla) {
        int lado = 2 * (MARGEN + RELLENO) + 3 * tamCasilla;
        Dibujo.fijarTamano(this, lado, lado);
        setAlignmentX(CENTER_ALIGNMENT);
        for (char[] fila : fichas) {
            java.util.Arrays.fill(fila, Tablero.VACIA);
        }

        MouseAdapter raton = new MouseAdapter() {
            @Override
            public void mouseMoved(MouseEvent e) {
                actualizarCasillaEncima(e.getX(), e.getY());
            }

            @Override
            public void mouseExited(MouseEvent e) {
                actualizarCasillaEncima(-1, -1);
            }

            @Override
            public void mousePressed(MouseEvent e) {
                actualizarCasillaEncima(e.getX(), e.getY());
                if (interactivo && oyente != null && filaEncima >= 0) {
                    oyente.casillaPulsada(filaEncima, columnaEncima);
                }
            }
        };
        addMouseListener(raton);
        addMouseMotionListener(raton);
    }

    public void setOyente(OyenteCasilla oyente) {
        this.oyente = oyente;
    }

    public void setInteractivo(boolean interactivo) {
        this.interactivo = interactivo;
        actualizarCursor();
        repaint();
    }

    public void setFichaFantasma(char ficha) {
        this.fichaFantasma = ficha;
        repaint();
    }

    /** Copia el contenido del tablero para dibujarlo y busca la linea ganadora. */
    public void mostrar(Tablero tablero) {
        for (int fila = 0; fila < 3; fila++) {
            for (int columna = 0; columna < 3; columna++) {
                fichas[fila][columna] = tablero.obtenerCasilla(fila, columna);
            }
        }
        lineaGanadora = Partida.buscarLineaGanadora(tablero);
        actualizarCursor();
        repaint();
    }

    private double tamCasilla() {
        return (getWidth() - 2.0 * (MARGEN + RELLENO)) / 3.0;
    }

    private double centroX(int columna) {
        return MARGEN + RELLENO + (columna + 0.5) * tamCasilla();
    }

    private double centroY(int fila) {
        return MARGEN + RELLENO + (fila + 0.5) * tamCasilla();
    }

    private void actualizarCasillaEncima(int x, int y) {
        double tam = tamCasilla();
        int columna = (int) Math.floor((x - MARGEN - RELLENO) / tam);
        int fila = (int) Math.floor((y - MARGEN - RELLENO) / tam);
        boolean dentro = x >= 0 && fila >= 0 && fila < 3 && columna >= 0 && columna < 3;
        int nuevaFila = dentro ? fila : -1;
        int nuevaColumna = dentro ? columna : -1;
        if (nuevaFila != filaEncima || nuevaColumna != columnaEncima) {
            filaEncima = nuevaFila;
            columnaEncima = nuevaColumna;
            actualizarCursor();
            repaint();
        }
    }

    /** Manita solo sobre casillas vacias y cuando se puede jugar. */
    private void actualizarCursor() {
        boolean sePuedeJugar = interactivo && filaEncima >= 0
                && fichas[filaEncima][columnaEncima] == Tablero.VACIA;
        setCursor(Cursor.getPredefinedCursor(sePuedeJugar ? Cursor.HAND_CURSOR : Cursor.DEFAULT_CURSOR));
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = Dibujo.preparar(g);
        double tam = tamCasilla();
        double inicio = MARGEN + RELLENO;

        // Marco exterior.
        RoundRectangle2D marco = new RoundRectangle2D.Double(MARGEN, MARGEN,
                getWidth() - 2.0 * MARGEN, getHeight() - 2.0 * MARGEN, 22, 22);
        g2.setColor(Tema.conAlfa(Tema.FONDO_ABAJO, 150));
        g2.fill(marco);
        Dibujo.trazoNeon(g2, marco, Tema.MORADO, 1.5f, 0.8f);

        // Casillas.
        for (int fila = 0; fila < 3; fila++) {
            for (int columna = 0; columna < 3; columna++) {
                RoundRectangle2D casilla = new RoundRectangle2D.Double(
                        inicio + columna * tam + 4, inicio + fila * tam + 4, tam - 8, tam - 8, 14, 14);
                boolean resaltar = interactivo && fila == filaEncima && columna == columnaEncima
                        && fichas[fila][columna] == Tablero.VACIA;
                g2.setColor(resaltar ? Tema.conAlfa(Tema.LAVANDA, 40) : Tema.CASILLA);
                g2.fill(casilla);
            }
        }

        // Rejilla: las dos lineas verticales y las dos horizontales.
        Color colorRejilla = Tema.conAlfa(Tema.LAVANDA, 150);
        for (int i = 1; i < 3; i++) {
            double p = inicio + i * tam;
            Dibujo.trazoNeon(g2, new Line2D.Double(p, MARGEN + 2, p, getHeight() - MARGEN - 2), colorRejilla, 1.5f, 0.4f);
            Dibujo.trazoNeon(g2, new Line2D.Double(MARGEN + 2, p, getWidth() - MARGEN - 2, p), colorRejilla, 1.5f, 0.4f);
        }

        // Fichas.
        float grosor = (float) Math.max(3, tam * 0.085);
        for (int fila = 0; fila < 3; fila++) {
            for (int columna = 0; columna < 3; columna++) {
                Dibujo.dibujarFicha(g2, fichas[fila][columna], centroX(columna), centroY(fila), tam * 0.56, grosor);
            }
        }

        // Ficha "fantasma" bajo el raton: muestra donde caeria la jugada.
        if (interactivo && filaEncima >= 0 && fichas[filaEncima][columnaEncima] == Tablero.VACIA
                && fichaFantasma != Tablero.VACIA) {
            g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, 0.28f));
            Dibujo.dibujarFicha(g2, fichaFantasma, centroX(columnaEncima), centroY(filaEncima), tam * 0.56, grosor);
            g2.setComposite(AlphaComposite.SrcOver);
        }

        // Raya sobre la linea ganadora, un poco mas larga que las fichas.
        if (lineaGanadora != null) {
            double x1 = centroX(lineaGanadora[1]);
            double y1 = centroY(lineaGanadora[0]);
            double x2 = centroX(lineaGanadora[3]);
            double y2 = centroY(lineaGanadora[2]);
            double largo = Math.hypot(x2 - x1, y2 - y1);
            double dx = (x2 - x1) / largo * tam * 0.38;
            double dy = (y2 - y1) / largo * tam * 0.38;
            Color color = Tema.colorDeFicha(fichas[lineaGanadora[0]][lineaGanadora[1]]);
            Dibujo.trazoNeon(g2, new Line2D.Double(x1 - dx, y1 - dy, x2 + dx, y2 + dy), color,
                    (float) Math.max(3, tam * 0.06), 1.4f);
        }
        g2.dispose();
    }
}
