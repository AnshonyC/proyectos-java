import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.awt.geom.RoundRectangle2D;
import javax.swing.BorderFactory;
import javax.swing.JTextField;
import javax.swing.text.AbstractDocument;
import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.DocumentFilter;

/**
 * Caja de texto redondeada con borde de neon, para escribir el nombre de
 * cada jugador. Cuando esta vacia muestra un texto de ayuda en gris
 * (placeholder) y no deja escribir mas de MAXIMO caracteres, para que el
 * nombre quepa en el marcador y en la pantalla de victoria.
 */
public class CampoTexto extends JTextField {

    public static final int MAXIMO = 14;
    /** Espacio para el halo del borde. */
    private static final int MARGEN = 5;

    private final Color color;
    private final String ayuda;

    public CampoTexto(String ayuda, Color color) {
        this.ayuda = ayuda;
        this.color = color;
        setOpaque(false);
        setForeground(Tema.TEXTO);
        setDisabledTextColor(Tema.TEXTO_SUAVE);
        setCaretColor(Tema.TEXTO);
        setSelectionColor(Tema.conAlfa(color, 120));
        setSelectedTextColor(Tema.TEXTO);
        setFont(Tema.fuente(Font.PLAIN, 17f));
        setBorder(BorderFactory.createEmptyBorder(MARGEN + 4, MARGEN + 14, MARGEN + 4, MARGEN + 10));
        ((AbstractDocument) getDocument()).setDocumentFilter(new LimiteDeLargo());
        // Al entrar o salir del campo cambia el brillo del borde.
        addFocusListener(new FocusAdapter() {
            @Override
            public void focusGained(FocusEvent e) {
                repaint();
            }

            @Override
            public void focusLost(FocusEvent e) {
                repaint();
            }
        });
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = Dibujo.preparar(g);
        RoundRectangle2D forma = new RoundRectangle2D.Double(MARGEN, MARGEN,
                getWidth() - 2.0 * MARGEN, getHeight() - 2.0 * MARGEN, 18, 18);
        g2.setColor(Tema.conAlfa(color, isEnabled() ? 26 : 12));
        g2.fill(forma);
        Dibujo.trazoNeon(g2, forma, color, 1.6f, hasFocus() ? 1.2f : 0.6f);

        if (getText().isEmpty() && !hasFocus()) {
            g2.setFont(getFont());
            g2.setColor(Tema.TEXTO_SUAVE);
            FontMetrics fm = g2.getFontMetrics();
            g2.drawString(ayuda, getInsets().left, Dibujo.lineaBaseCentrada(fm, getHeight() / 2f));
        }
        g2.dispose();
        super.paintComponent(g);   // el texto y el cursor los pinta Swing
    }

    /** Impide que el texto pase de MAXIMO caracteres. */
    private static class LimiteDeLargo extends DocumentFilter {
        @Override
        public void insertString(FilterBypass fb, int offset, String texto, AttributeSet attr)
                throws BadLocationException {
            replace(fb, offset, 0, texto, attr);
        }

        @Override
        public void replace(FilterBypass fb, int offset, int largo, String texto, AttributeSet attr)
                throws BadLocationException {
            if (texto == null) {
                texto = "";
            }
            int disponible = MAXIMO - (fb.getDocument().getLength() - largo);
            if (texto.length() > disponible) {
                texto = texto.substring(0, Math.max(0, disponible));
            }
            super.replace(fb, offset, largo, texto, attr);
        }
    }
}
