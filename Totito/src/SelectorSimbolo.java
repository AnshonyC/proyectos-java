import java.awt.AlphaComposite;
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.geom.Ellipse2D;
import java.awt.geom.RoundRectangle2D;
import javax.swing.JComponent;

/**
 * Las dos cajas X / O de la pantalla de configuracion. La caja marcada es
 * el simbolo del Jugador 1; el Jugador 2 se queda con el otro. Debajo se
 * escribe una leyenda para que no haya dudas de quien juega con que.
 */
public class SelectorSimbolo extends JComponent {

    private static final int ANCHO_CAJA = 120;
    private static final int ALTO_CAJA = 98;
    private static final int HUECO = 34;
    private static final int ALTO_LEYENDA = 22;

    private char fichaJugador1 = 'X';

    public SelectorSimbolo() {
        Dibujo.fijarTamano(this, 2 * ANCHO_CAJA + HUECO + 160, ALTO_CAJA + ALTO_LEYENDA);
        setAlignmentX(CENTER_ALIGNMENT);
        setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                if (caja('X').contains(e.getPoint())) {
                    setFichaJugador1('X');
                } else if (caja('O').contains(e.getPoint())) {
                    setFichaJugador1('O');
                }
            }
        });
    }

    public char getFichaJugador1() {
        return fichaJugador1;
    }

    public void setFichaJugador1(char ficha) {
        fichaJugador1 = ficha;
        repaint();
    }

    /** Zona (en pixeles) de la caja de cada ficha. */
    private Rectangle caja(char ficha) {
        int x = (getWidth() - 2 * ANCHO_CAJA - HUECO) / 2;
        if (ficha == 'O') {
            x += ANCHO_CAJA + HUECO;
        }
        return new Rectangle(x, 0, ANCHO_CAJA, ALTO_CAJA);
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = Dibujo.preparar(g);
        for (char ficha : new char[]{'X', 'O'}) {
            pintarCaja(g2, ficha, ficha == fichaJugador1);
        }

        char fichaJugador2 = fichaJugador1 == 'X' ? 'O' : 'X';
        String leyenda = "Jugador 1 juega con " + fichaJugador1 + "   ·   Jugador 2 con " + fichaJugador2;
        g2.setFont(Tema.fuente(Font.PLAIN, 13f));
        FontMetrics fm = g2.getFontMetrics();
        g2.setColor(Tema.TEXTO_SUAVE);
        g2.drawString(leyenda, (getWidth() - fm.stringWidth(leyenda)) / 2f, getHeight() - 5);
        g2.dispose();
    }

    private void pintarCaja(Graphics2D g2, char ficha, boolean elegida) {
        Rectangle r = caja(ficha);
        Color color = Tema.colorDeFicha(ficha);
        RoundRectangle2D forma = new RoundRectangle2D.Double(r.x + 8, r.y + 8, r.width - 16, r.height - 16, 20, 20);
        g2.setColor(Tema.conAlfa(color, elegida ? 40 : 14));
        g2.fill(forma);
        Dibujo.trazoNeon(g2, forma, color, 2f, elegida ? 1.3f : 0.4f);

        // La ficha no elegida se ve apagada.
        if (!elegida) {
            g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, 0.5f));
        }
        double cx = r.getCenterX();
        double cy = r.y + 8 + (r.height - 16) * 0.4;
        Dibujo.dibujarFicha(g2, ficha, cx, cy, (r.height - 16) * 0.44, 6.5f);
        g2.setComposite(AlphaComposite.SrcOver);

        // Boton de radio debajo de la ficha.
        double cyRadio = r.y + r.height - 8 - 15;
        Ellipse2D aro = new Ellipse2D.Double(cx - 8, cyRadio - 8, 16, 16);
        if (elegida) {
            Dibujo.trazoNeon(g2, aro, color, 2f, 0.8f);
            g2.setColor(Tema.aclarar(color, 0.5f));
            g2.fill(new Ellipse2D.Double(cx - 4.5, cyRadio - 4.5, 9, 9));
        } else {
            Dibujo.trazo(g2, aro, Tema.conAlfa(Tema.LAVANDA, 120), 1.8f);
        }
    }
}
