import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.Ellipse2D;
import javax.swing.JLabel;
import javax.swing.JPanel;

/**
 * Un paso numerado de "Cómo jugar": circulo de neon con el numero y el
 * texto a la derecha. El texto es HTML de JLabel, asi se pueden pintar de
 * color la X y la O dentro de la frase y partir la linea con &lt;br&gt;.
 */
public class PasoInstruccion extends JPanel {

    private static final int ALTO = 54;
    private static final int DIAMETRO = 38;

    private final int numero;
    private final Color color;

    public PasoInstruccion(int numero, Color color, String html, int ancho) {
        super(null);
        this.numero = numero;
        this.color = color;
        setOpaque(false);
        setAlignmentX(CENTER_ALIGNMENT);
        Dibujo.fijarTamano(this, ancho, ALTO);

        JLabel texto = new JLabel("<html>" + html + "</html>");
        texto.setFont(Tema.fuente(Font.PLAIN, 17f));
        texto.setForeground(Tema.TEXTO);
        texto.setBounds(DIAMETRO + 30, 0, ancho - DIAMETRO - 30, ALTO);
        add(texto);
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = Dibujo.preparar(g);
        double y = (getHeight() - DIAMETRO) / 2.0;
        Dibujo.trazoNeon(g2, new Ellipse2D.Double(8, y, DIAMETRO, DIAMETRO), color, 2f, 0.9f);
        g2.setFont(Tema.fuente(Font.BOLD, 18f));
        FontMetrics fm = g2.getFontMetrics();
        String n = String.valueOf(numero);
        g2.setColor(Tema.TEXTO);
        g2.drawString(n, 8 + (DIAMETRO - fm.stringWidth(n)) / 2f, Dibujo.lineaBaseCentrada(fm, getHeight() / 2f));
        g2.dispose();
    }
}
