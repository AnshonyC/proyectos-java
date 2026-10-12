import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics2D;
import java.awt.geom.AffineTransform;
import java.awt.geom.RoundRectangle2D;
import java.util.Random;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;

/**
 * Pantalla 4 del diseno: "¡Ganó Jugador 2!" con trofeo, confeti y el
 * tablero final con la raya ganadora. Tambien sirve para el empate
 * (sin trofeo ni confeti).
 */
public class PantallaResultado extends PantallaBase {

    private static final int ANCHO_INTERIOR = 440;

    private final IconoResultado icono = new IconoResultado();
    private final Rotulo titulo = Rotulo.titulo("", 40f, Tema.CIAN, Tema.AZUL, ANCHO_INTERIOR, 54);
    private final Rotulo frase = Rotulo.leyenda("", ANCHO_INTERIOR);
    private final PanelTablero tablero = new PanelTablero(66);
    private final TarjetaConConfeti tarjeta = new TarjetaConConfeti();

    public PantallaResultado(Navegacion navegacion) {
        super(navegacion);

        tarjeta.setLayout(new BoxLayout(tarjeta, BoxLayout.Y_AXIS));
        tarjeta.setBorder(BorderFactory.createEmptyBorder(14, 20, 18, 20));
        tarjeta.add(icono);
        tarjeta.add(titulo);
        tarjeta.add(frase);
        tarjeta.add(Box.createRigidArea(new Dimension(0, 6)));
        tarjeta.add(tablero);

        BotonNeon jugarDeNuevo = BotonNeon.pildora("Jugar de nuevo", Iconos.REINICIAR,
                Tema.ROSA, Tema.MORADO, 290, 72);
        jugarDeNuevo.addActionListener(e -> navegacion.jugarDeNuevo());
        BotonNeon menu = BotonNeon.pildora("Menú principal", Iconos.CASA,
                Tema.AZUL, new Color(0x3A, 0x3F, 0xC8), 290, 72);
        menu.addActionListener(e -> navegacion.irAlMenu());

        relleno();
        agregar(tarjeta);
        espacio(6);
        agregar(fila(6, jugarDeNuevo, menu));
        relleno();
    }

    /** Prepara la pantalla con el resultado de la partida que acaba de terminar. */
    public void mostrar(Partida partida) {
        tablero.mostrar(partida.getTablero());
        boolean empate = partida.getEstado() == Partida.Estado.EMPATE;
        icono.setEmpate(empate);
        tarjeta.setConConfeti(!empate);

        if (empate) {
            titulo.setTexto("¡Empate!", Tema.LAVANDA, Tema.MORADO);
            frase.setTexto("Nadie cedió ni una casilla");
            return;
        }
        Jugador ganador = partida.getGanador();
        Color color = Tema.colorDeFicha(ganador.getFicha());
        titulo.setTexto("¡Ganó " + ganador.getNombre() + "!", Tema.aclarar(color, 0.35f), color);
        if (partida.esComputadora(ganador)) {
            frase.setTexto("La máquina no perdona");
        } else if (partida.getModo() == Partida.Modo.CONTRA_IA) {
            frase.setTexto("¡Le ganaste a la máquina!");
        } else {
            frase.setTexto("Excelente jugada");
        }
    }

    /**
     * Tarjeta con papelitos de colores. Las posiciones salen de un Random
     * con semilla fija: siempre son las mismas y no "bailan" al repintar.
     */
    private static class TarjetaConConfeti extends Tarjeta {

        private static final Color[] COLORES = {Tema.ROSA, Tema.CIAN, Tema.MORADO};
        private boolean conConfeti = true;

        TarjetaConConfeti() {
            super(Tema.MORADO);
        }

        void setConConfeti(boolean conConfeti) {
            this.conConfeti = conConfeti;
            repaint();
        }

        @Override
        protected void pintarDecoracion(Graphics2D g2, RoundRectangle2D forma) {
            if (!conConfeti) {
                return;
            }
            Random azar = new Random(11);
            double centro = forma.getCenterX();
            int colocados = 0;
            while (colocados < 22) {
                double x = forma.getX() + 18 + azar.nextDouble() * (forma.getWidth() - 36);
                double y = forma.getY() + 16 + azar.nextDouble() * (forma.getHeight() - 32);
                // Solo arriba (alrededor del trofeo) o a los lados del tablero.
                boolean libre = y < forma.getY() + 100 || Math.abs(x - centro) > 135;
                boolean sobreTrofeo = y < forma.getY() + 120 && Math.abs(x - centro) < 60;
                double angulo = azar.nextDouble() * Math.PI;
                Color color = COLORES[azar.nextInt(COLORES.length)];
                if (!libre || sobreTrofeo) {
                    continue;
                }
                AffineTransform previo = g2.getTransform();
                g2.translate(x, y);
                g2.rotate(angulo);
                RoundRectangle2D papel = new RoundRectangle2D.Double(-3.5, -7, 7, 14, 3, 3);
                g2.setColor(Tema.conAlfa(color, 45));
                g2.fill(new RoundRectangle2D.Double(-6, -9.5, 12, 19, 6, 6));
                g2.setColor(Tema.conAlfa(color, 220));
                g2.fill(papel);
                g2.setTransform(previo);
                colocados++;
            }
        }
    }
}
