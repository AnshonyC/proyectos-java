import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.GradientPaint;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.Line2D;
import javax.swing.JComponent;

/**
 * Texto decorativo centrado. Hay dos variantes, que se crean con:
 *
 * - Rotulo.titulo(...): texto grande con degradado y halo, opcionalmente
 *   con icono a la izquierda y subrayado ("Cómo jugar", "¡Ganó Ana!").
 *   Si el texto no cabe, la letra se achica sola.
 * - Rotulo.seccion(...): texto entre dos lineas que se desvanecen, con un
 *   subtitulo opcional ("— JUGADORES —", "— Excelente jugada —").
 */
public class Rotulo extends JComponent {

    private enum Tipo { TITULO, SECCION }

    private final Tipo tipo;
    private final Font fuente;
    private String texto;
    private String subtitulo;
    private Color desde;
    private Color hasta;
    private Iconos.Icono icono;
    private Color colorIcono;
    private Color subrayadoDesde;
    private Color subrayadoHasta;

    private Rotulo(Tipo tipo, String texto, Font fuente, Color desde, Color hasta, int ancho, int alto) {
        this.tipo = tipo;
        this.texto = texto;
        this.fuente = fuente;
        this.desde = desde;
        this.hasta = hasta;
        setAlignmentX(CENTER_ALIGNMENT);
        Dibujo.fijarTamano(this, ancho, alto);
    }

    /** Titulo grande con degradado de color "desde" a "hasta". */
    public static Rotulo titulo(String texto, float tamano, Color desde, Color hasta, int ancho, int alto) {
        return new Rotulo(Tipo.TITULO, texto, Tema.fuente(Font.BOLD, tamano), desde, hasta, ancho, alto);
    }

    /** Titulo de seccion en mayusculas espaciadas, con subtitulo opcional (puede ser null). */
    public static Rotulo seccion(String texto, String subtitulo, int ancho) {
        Rotulo r = new Rotulo(Tipo.SECCION, texto, Tema.fuenteEspaciada(Font.BOLD, 17f, 0.3f),
                Tema.LAVANDA, Tema.LAVANDA, ancho, subtitulo == null ? 28 : 48);
        r.subtitulo = subtitulo;
        return r;
    }

    /** Frase corta entre lineas, sin mayusculas espaciadas ("Excelente jugada"). */
    public static Rotulo leyenda(String texto, int ancho) {
        return new Rotulo(Tipo.SECCION, texto, Tema.fuente(Font.BOLD, 19f),
                Tema.LAVANDA, Tema.LAVANDA, ancho, 32);
    }

    /** Agrega un icono a la izquierda del titulo. */
    public Rotulo conIcono(Iconos.Icono icono, Color color) {
        this.icono = icono;
        this.colorIcono = color;
        return this;
    }

    /** Agrega un subrayado con degradado bajo el titulo. */
    public Rotulo conSubrayado(Color desde, Color hasta) {
        this.subrayadoDesde = desde;
        this.subrayadoHasta = hasta;
        return this;
    }

    public void setTexto(String texto) {
        this.texto = texto;
        repaint();
    }

    public void setTexto(String texto, Color desde, Color hasta) {
        this.desde = desde;
        this.hasta = hasta;
        setTexto(texto);
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = Dibujo.preparar(g);
        if (tipo == Tipo.TITULO) {
            pintarTitulo(g2);
        } else {
            pintarSeccion(g2);
        }
        g2.dispose();
    }

    private void pintarTitulo(Graphics2D g2) {
        boolean conSubrayado = subrayadoDesde != null;
        Font f = fuente;
        g2.setFont(f);
        FontMetrics fm = g2.getFontMetrics();

        // Si no cabe, se reduce la letra hasta que quepa.
        double extraIcono = icono == null ? 0 : fm.getAscent() + 16;
        while (fm.stringWidth(texto) + extraIcono > getWidth() - 20 && f.getSize2D() > 12) {
            f = f.deriveFont(f.getSize2D() - 1);
            g2.setFont(f);
            fm = g2.getFontMetrics();
            extraIcono = icono == null ? 0 : fm.getAscent() + 16;
        }

        int anchoTexto = fm.stringWidth(texto);
        double tamIcono = icono == null ? 0 : fm.getAscent() * 1.05;
        double hueco = icono == null ? 0 : 16;
        double x = (getWidth() - (tamIcono + hueco + anchoTexto)) / 2;
        float base = Dibujo.lineaBaseCentrada(fm, getHeight() / 2f - (conSubrayado ? 6 : 0));

        if (icono != null) {
            icono.dibujar(g2, x, base - fm.getAscent() * 0.95, tamIcono, colorIcono);
        }
        float xTexto = (float) (x + tamIcono + hueco);
        Dibujo.textoNeon(g2, texto, xTexto, base, desde,
                new GradientPaint(xTexto, 0, desde, xTexto + anchoTexto, 0, hasta));

        if (conSubrayado) {
            float y = base + 14;
            g2.setPaint(new GradientPaint(xTexto, 0, subrayadoDesde, xTexto + anchoTexto, 0, subrayadoHasta));
            g2.setStroke(Dibujo.redondo(3f));
            g2.draw(new Line2D.Float(xTexto, y, xTexto + anchoTexto, y));
        }
    }

    private void pintarSeccion(Graphics2D g2) {
        g2.setFont(fuente);
        FontMetrics fm = g2.getFontMetrics();
        int anchoTexto = fm.stringWidth(texto);
        float x = (getWidth() - anchoTexto) / 2f;
        float base = subtitulo == null ? Dibujo.lineaBaseCentrada(fm, getHeight() / 2f) : 21;
        Dibujo.textoNeon(g2, texto, x, base, Tema.MORADO, desde);

        // Lineas a los lados que se desvanecen hacia afuera.
        float yLinea = base - fm.getAscent() * 0.35f;
        float separacion = 24;
        // 140 px, o menos si no caben dentro del componente.
        float largo = Math.min(140, (getWidth() - anchoTexto) / 2f - separacion - 16);
        Color linea = Tema.conAlfa(Tema.MORADO, 170);
        Color nada = Tema.conAlfa(Tema.MORADO, 0);
        g2.setStroke(new BasicStroke(1.6f));
        float finIzquierda = x - separacion;
        g2.setPaint(new GradientPaint(finIzquierda - largo, 0, nada, finIzquierda, 0, linea));
        g2.draw(new Line2D.Float(finIzquierda - largo, yLinea, finIzquierda, yLinea));
        float inicioDerecha = x + anchoTexto + separacion;
        g2.setPaint(new GradientPaint(inicioDerecha, 0, linea, inicioDerecha + largo, 0, nada));
        g2.draw(new Line2D.Float(inicioDerecha, yLinea, inicioDerecha + largo, yLinea));

        if (subtitulo != null) {
            g2.setFont(Tema.fuente(Font.PLAIN, 14f));
            fm = g2.getFontMetrics();
            g2.setColor(Tema.TEXTO_SUAVE);
            g2.drawString(subtitulo, (getWidth() - fm.stringWidth(subtitulo)) / 2f, base + 22);
        }
    }
}
