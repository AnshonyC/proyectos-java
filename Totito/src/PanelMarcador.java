import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.RoundRectangle2D;
import javax.swing.JComponent;

/**
 * Marcador de la pantalla de juego: una "ficha" por jugador con su
 * simbolo, nombre y victorias, y los empates en el centro. La ficha del
 * jugador que tiene el turno brilla mas.
 */
public class PanelMarcador extends JComponent {

    private static final int ANCHO = 590;
    private static final int ALTO = 82;
    private static final int ANCHO_CENTRO = 104;

    private Partida partida;

    public PanelMarcador() {
        Dibujo.fijarTamano(this, ANCHO, ALTO);
        setAlignmentX(CENTER_ALIGNMENT);
    }

    public void mostrar(Partida partida) {
        this.partida = partida;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        if (partida == null) {
            return;
        }
        Graphics2D g2 = Dibujo.preparar(g);
        int anchoFicha = (getWidth() - ANCHO_CENTRO) / 2;
        boolean enCurso = partida.getEstado() == Partida.Estado.EN_CURSO;
        for (int i = 0; i < 2; i++) {
            Jugador jugador = partida.getJugador(i);
            boolean tieneTurno = enCurso && partida.getJugadorEnTurno() == jugador;
            int x = i == 0 ? 0 : getWidth() - anchoFicha;
            pintarJugador(g2, x, anchoFicha, jugador, partida.getVictorias(i), tieneTurno);
        }

        // Empates en el centro.
        float centro = getWidth() / 2f;
        g2.setFont(Tema.fuenteEspaciada(Font.BOLD, 11f, 0.2f));
        FontMetrics fm = g2.getFontMetrics();
        g2.setColor(Tema.TEXTO_SUAVE);
        g2.drawString("EMPATES", centro - fm.stringWidth("EMPATES") / 2f, 32);
        g2.setFont(Tema.fuente(Font.BOLD, 24f));
        fm = g2.getFontMetrics();
        String empates = String.valueOf(partida.getEmpates());
        g2.setColor(Tema.LAVANDA);
        g2.drawString(empates, centro - fm.stringWidth(empates) / 2f, 62);
        g2.dispose();
    }

    private void pintarJugador(Graphics2D g2, int x, int ancho, Jugador jugador, int victorias, boolean tieneTurno) {
        Color color = Tema.colorDeFicha(jugador.getFicha());
        RoundRectangle2D forma = new RoundRectangle2D.Double(x + 8, 8, ancho - 16, getHeight() - 16, 22, 22);
        g2.setColor(Tema.conAlfa(color, tieneTurno ? 45 : 14));
        g2.fill(forma);
        Dibujo.trazoNeon(g2, forma, color, 1.8f, tieneTurno ? 1.3f : 0.35f);

        double cy = getHeight() / 2.0;
        Dibujo.dibujarFicha(g2, jugador.getFicha(), x + 8 + 34, cy, 28, 4.5f);

        int xTexto = x + 8 + 64;
        g2.setFont(Tema.fuente(Font.BOLD, 17f));
        FontMetrics fm = g2.getFontMetrics();
        g2.setColor(Tema.TEXTO);
        g2.drawString(Dibujo.recortar(fm, jugador.getNombre(), ancho - 16 - 64 - 12), xTexto, (float) cy - 2);
        g2.setFont(Tema.fuente(Font.PLAIN, 13f));
        g2.setColor(Tema.TEXTO_SUAVE);
        g2.drawString("Victorias: " + victorias, xTexto, (float) cy + 17);
    }
}
