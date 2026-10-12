import java.awt.Color;
import java.awt.Font;
import java.awt.GradientPaint;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.Line2D;

/**
 * Tarjeta de la pantalla de configuracion donde se escribe el nombre de un
 * jugador. En el modo "Contra la IA" la tarjeta del Jugador 2 se bloquea y
 * pasa a llamarse "Computadora" (ver setComputadora).
 */
public class TarjetaJugador extends Tarjeta {

    public static final int ANCHO = 290;
    public static final int ALTO = 150;
    public static final String NOMBRE_IA = "Computadora";

    private final String titulo;
    private final Color color;
    private final CampoTexto campo;
    private boolean esComputadora;
    /** Lo que el usuario habia escrito antes de pasar a modo IA, para devolverselo. */
    private String nombreGuardado = "";

    public TarjetaJugador(String titulo, Color color) {
        super(color, 26);
        this.titulo = titulo;
        this.color = color;
        setLayout(null);   // el campo se coloca a mano en doLayout()
        campo = new CampoTexto(titulo, color);
        add(campo);
        Dibujo.fijarTamano(this, ANCHO, ALTO);
    }

    @Override
    public void doLayout() {
        campo.setBounds(MARGEN + 12, getHeight() - MARGEN - 10 - 46, getWidth() - 2 * MARGEN - 24, 46);
    }

    /** El nombre escrito o, si se dejo vacio, el titulo ("Jugador 1"). */
    public String getNombre() {
        String nombre = campo.getText().trim();
        return nombre.isEmpty() ? titulo : nombre;
    }

    /** Convierte la tarjeta en la de la computadora (true) o la devuelve a humano (false). */
    public void setComputadora(boolean computadora) {
        if (computadora == esComputadora) {
            return;
        }
        esComputadora = computadora;
        if (computadora) {
            nombreGuardado = campo.getText();
            campo.setText(NOMBRE_IA);
        } else {
            campo.setText(nombreGuardado);
        }
        campo.setEnabled(!computadora);
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);   // la caja de cristal
        Graphics2D g2 = Dibujo.preparar(g);

        Iconos.Icono icono = esComputadora ? Iconos.COMPUTADORA : Iconos.PERSONA;
        icono.dibujar(g2, MARGEN + 22, MARGEN + 10, 42, color);

        g2.setFont(Tema.fuente(Font.BOLD, 21f));
        g2.setColor(Tema.TEXTO);
        float xTitulo = MARGEN + 88;
        float base = MARGEN + 36;
        g2.drawString(titulo, xTitulo, base);
        g2.setPaint(new GradientPaint(xTitulo, 0, color, xTitulo + 140, 0, Tema.conAlfa(color, 0)));
        g2.setStroke(Dibujo.redondo(3f));
        g2.draw(new Line2D.Float(xTitulo, base + 12, xTitulo + 140, base + 12));

        g2.setFont(Tema.fuente(Font.PLAIN, 13f));
        g2.setColor(Tema.TEXTO);
        g2.drawString("Nombre", MARGEN + 18, MARGEN + 70);
        g2.dispose();
    }
}
