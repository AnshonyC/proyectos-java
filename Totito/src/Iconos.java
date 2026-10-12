import java.awt.Color;
import java.awt.GradientPaint;
import java.awt.Graphics2D;
import java.awt.Shape;
import java.awt.geom.Arc2D;
import java.awt.geom.Area;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Path2D;
import java.awt.geom.Rectangle2D;
import java.awt.geom.RoundRectangle2D;

/**
 * Iconos de la interfaz, dibujados con figuras geometricas (sin archivos
 * de imagen). Cada icono se dibuja dentro de un cuadrado de lado "t" cuya
 * esquina superior izquierda es (x, y); todas las medidas son fracciones
 * de t, asi el mismo icono sirve a cualquier tamano.
 *
 * Para crear uno nuevo basta con agregar otra constante siguiendo el mismo
 * patron.
 */
public final class Iconos {

    /** Un icono sabe dibujarse en el cuadrado (x, y, tam, tam) con el color dado. */
    @FunctionalInterface
    public interface Icono {
        void dibujar(Graphics2D g, double x, double y, double tam, Color color);
    }

    private Iconos() {
    }

    /** Triangulo de "reproducir" (botones Jugar y Comenzar partida). */
    public static final Icono JUGAR = (g, x, y, t, c) -> {
        Path2D triangulo = new Path2D.Double();
        triangulo.moveTo(x + t * 0.24, y + t * 0.14);
        triangulo.lineTo(x + t * 0.86, y + t * 0.5);
        triangulo.lineTo(x + t * 0.24, y + t * 0.86);
        triangulo.closePath();
        Dibujo.trazoNeon(g, triangulo, c, (float) (t * 0.1), 0.6f);
        g.setPaint(new GradientPaint((float) x, (float) y, Tema.aclarar(c, 0.25f),
                (float) (x + t), (float) (y + t), c));
        g.fill(triangulo);
    };

    /** Libro abierto (Instrucciones / Como jugar). */
    public static final Icono LIBRO = (g, x, y, t, c) -> {
        double cx = x + t / 2;
        double arriba = y + t * 0.2;
        double abajo = y + t * 0.84;
        Path2D libro = new Path2D.Double();
        // Pagina izquierda
        libro.moveTo(cx, arriba + t * 0.06);
        libro.quadTo(cx - t * 0.2, arriba - t * 0.06, x + t * 0.06, arriba + t * 0.02);
        libro.lineTo(x + t * 0.06, abajo - t * 0.08);
        libro.quadTo(cx - t * 0.2, abajo - t * 0.14, cx, abajo);
        // Pagina derecha
        libro.moveTo(cx, arriba + t * 0.06);
        libro.quadTo(cx + t * 0.2, arriba - t * 0.06, x + t * 0.94, arriba + t * 0.02);
        libro.lineTo(x + t * 0.94, abajo - t * 0.08);
        libro.quadTo(cx + t * 0.2, abajo - t * 0.14, cx, abajo);
        // Lomo
        libro.moveTo(cx, arriba + t * 0.06);
        libro.lineTo(cx, abajo);
        Dibujo.trazoNeon(g, libro, c, (float) (t * 0.075));
    };

    /** Puerta con flecha saliendo (Salir). */
    public static final Icono SALIR = (g, x, y, t, c) -> {
        Path2D puerta = new Path2D.Double();
        puerta.moveTo(x + t * 0.55, y + t * 0.3);
        puerta.lineTo(x + t * 0.55, y + t * 0.12);
        puerta.lineTo(x + t * 0.14, y + t * 0.12);
        puerta.lineTo(x + t * 0.14, y + t * 0.88);
        puerta.lineTo(x + t * 0.55, y + t * 0.88);
        puerta.lineTo(x + t * 0.55, y + t * 0.7);
        puerta.moveTo(x + t * 0.36, y + t * 0.5);
        puerta.lineTo(x + t * 0.9, y + t * 0.5);
        puerta.moveTo(x + t * 0.74, y + t * 0.34);
        puerta.lineTo(x + t * 0.9, y + t * 0.5);
        puerta.lineTo(x + t * 0.74, y + t * 0.66);
        Dibujo.trazoNeon(g, puerta, c, (float) (t * 0.075));
    };

    /** Flechita "›" del lado derecho de los botones del menu. */
    public static final Icono CHEVRON = (g, x, y, t, c) -> {
        Path2D flecha = new Path2D.Double();
        flecha.moveTo(x + t * 0.32, y + t * 0.16);
        flecha.lineTo(x + t * 0.68, y + t * 0.5);
        flecha.lineTo(x + t * 0.32, y + t * 0.84);
        Dibujo.trazoNeon(g, flecha, c, (float) (t * 0.13), 0.7f);
    };

    /** Flecha hacia la izquierda (Volver / Regresar). */
    public static final Icono FLECHA_IZQUIERDA = (g, x, y, t, c) -> {
        Path2D flecha = new Path2D.Double();
        flecha.moveTo(x + t * 0.88, y + t * 0.5);
        flecha.lineTo(x + t * 0.14, y + t * 0.5);
        flecha.moveTo(x + t * 0.42, y + t * 0.22);
        flecha.lineTo(x + t * 0.14, y + t * 0.5);
        flecha.lineTo(x + t * 0.42, y + t * 0.78);
        Dibujo.trazo(g, flecha, c, (float) (t * 0.1));
    };

    /** Casa (Menu principal). */
    public static final Icono CASA = (g, x, y, t, c) -> {
        g.setColor(c);
        Path2D techo = new Path2D.Double();
        techo.moveTo(x + t * 0.5, y + t * 0.1);
        techo.lineTo(x + t * 0.92, y + t * 0.48);
        techo.lineTo(x + t * 0.08, y + t * 0.48);
        techo.closePath();
        g.setStroke(Dibujo.redondo((float) (t * 0.08)));
        g.draw(techo);
        g.fill(techo);
        Area cuerpo = new Area(new Rectangle2D.Double(x + t * 0.2, y + t * 0.44, t * 0.6, t * 0.46));
        cuerpo.subtract(new Area(new RoundRectangle2D.Double(
                x + t * 0.41, y + t * 0.6, t * 0.18, t * 0.32, t * 0.05, t * 0.05)));
        g.fill(cuerpo);
    };

    /** Dos flechas en circulo (Jugar de nuevo / Reiniciar). */
    public static final Icono REINICIAR = (g, x, y, t, c) -> {
        double cx = x + t / 2;
        double cy = y + t / 2;
        double r = t * 0.34;
        g.setColor(c);
        g.setStroke(Dibujo.redondo((float) (t * 0.1)));
        for (int inicio : new int[]{30, 210}) {
            g.draw(new Arc2D.Double(cx - r, cy - r, 2 * r, 2 * r, inicio, 120, Arc2D.OPEN));
            // Punta de flecha al final del arco, apuntando en el sentido del giro.
            double a = Math.toRadians(inicio + 120);
            double px = cx + r * Math.cos(a);
            double py = cy - r * Math.sin(a);
            double tx = -Math.sin(a);   // direccion tangente (sentido antihorario)
            double ty = -Math.cos(a);
            double nx = Math.cos(a);    // direccion radial
            double ny = -Math.sin(a);
            double largo = t * 0.17;
            double ancho = t * 0.14;
            Path2D punta = new Path2D.Double();
            punta.moveTo(px + tx * largo, py + ty * largo);
            punta.lineTo(px + nx * ancho, py + ny * ancho);
            punta.lineTo(px - nx * ancho, py - ny * ancho);
            punta.closePath();
            g.fill(punta);
        }
    };

    /** Silueta de persona (tarjetas de jugador). */
    public static final Icono PERSONA = Iconos::persona;

    /** Dos personas (modo 2 jugadores). */
    public static final Icono PERSONAS = (g, x, y, t, c) -> {
        persona(g, x + t * 0.42, y + t * 0.26, t * 0.52, Tema.conAlfa(c, 170));
        persona(g, x, y + t * 0.12, t * 0.66, c);
    };

    /** Chip de computadora (modo contra la IA). */
    public static final Icono COMPUTADORA = (g, x, y, t, c) -> {
        float grosor = (float) (t * 0.07);
        Dibujo.trazo(g, new RoundRectangle2D.Double(x + t * 0.2, y + t * 0.2, t * 0.6, t * 0.6, t * 0.16, t * 0.16),
                c, grosor);
        g.fill(new RoundRectangle2D.Double(x + t * 0.37, y + t * 0.37, t * 0.26, t * 0.26, t * 0.06, t * 0.06));
        Path2D patas = new Path2D.Double();
        for (int i = 0; i < 3; i++) {
            double p = t * (0.34 + 0.16 * i);
            patas.moveTo(x + p, y + t * 0.05);
            patas.lineTo(x + p, y + t * 0.19);
            patas.moveTo(x + p, y + t * 0.81);
            patas.lineTo(x + p, y + t * 0.95);
            patas.moveTo(x + t * 0.05, y + p);
            patas.lineTo(x + t * 0.19, y + p);
            patas.moveTo(x + t * 0.81, y + p);
            patas.lineTo(x + t * 0.95, y + p);
        }
        Dibujo.trazo(g, patas, c, grosor);
    };

    /** Trofeo con estrella (pantalla de victoria). */
    public static final Icono TROFEO = (g, x, y, t, c) -> {
        Path2D copa = new Path2D.Double();
        copa.moveTo(x + t * 0.24, y + t * 0.08);
        copa.lineTo(x + t * 0.76, y + t * 0.08);
        copa.lineTo(x + t * 0.73, y + t * 0.36);
        copa.quadTo(x + t * 0.69, y + t * 0.58, x + t * 0.5, y + t * 0.6);
        copa.quadTo(x + t * 0.31, y + t * 0.58, x + t * 0.27, y + t * 0.36);
        copa.closePath();

        Path2D asas = new Path2D.Double();
        asas.moveTo(x + t * 0.25, y + t * 0.16);
        asas.lineTo(x + t * 0.1, y + t * 0.16);
        asas.quadTo(x + t * 0.08, y + t * 0.42, x + t * 0.31, y + t * 0.46);
        asas.moveTo(x + t * 0.75, y + t * 0.16);
        asas.lineTo(x + t * 0.9, y + t * 0.16);
        asas.quadTo(x + t * 0.92, y + t * 0.42, x + t * 0.69, y + t * 0.46);

        Area pie = new Area(new Rectangle2D.Double(x + t * 0.45, y + t * 0.58, t * 0.1, t * 0.16));
        pie.add(new Area(new RoundRectangle2D.Double(x + t * 0.33, y + t * 0.72, t * 0.34, t * 0.08, t * 0.04, t * 0.04)));
        pie.add(new Area(new RoundRectangle2D.Double(x + t * 0.26, y + t * 0.8, t * 0.48, t * 0.11, t * 0.05, t * 0.05)));

        Dibujo.trazoNeon(g, copa, c, 1.5f, 0.9f);
        Dibujo.trazoNeon(g, asas, c, (float) (t * 0.06));
        g.setPaint(new GradientPaint(0, (float) y, Tema.aclarar(c, 0.35f), 0, (float) (y + t), c));
        g.fill(copa);
        g.fill(pie);
        g.setColor(Tema.conAlfa(Tema.FONDO_ABAJO, 190));
        g.fill(estrella(x + t * 0.5, y + t * 0.32, t * 0.11, t * 0.045));
    };

    /** Logotipo del encabezado: la rejilla del totito con dos O y una X. */
    public static final Icono LOGO = (g, x, y, t, c) -> {
        float grosor = (float) (t * 0.045);
        Path2D rejilla = new Path2D.Double();
        rejilla.moveTo(x + t * 0.37, y + t * 0.04);
        rejilla.lineTo(x + t * 0.35, y + t * 0.96);
        rejilla.moveTo(x + t * 0.65, y + t * 0.04);
        rejilla.lineTo(x + t * 0.63, y + t * 0.96);
        rejilla.moveTo(x + t * 0.04, y + t * 0.36);
        rejilla.lineTo(x + t * 0.96, y + t * 0.34);
        rejilla.moveTo(x + t * 0.04, y + t * 0.66);
        rejilla.lineTo(x + t * 0.96, y + t * 0.64);
        Dibujo.trazoNeon(g, rejilla, c, grosor, 0.6f);
        Dibujo.trazoNeon(g, new Ellipse2D.Double(x + t * 0.08, y + t * 0.08, t * 0.18, t * 0.18), Tema.MORADO, grosor, 0.6f);
        Dibujo.trazoNeon(g, new Ellipse2D.Double(x + t * 0.74, y + t * 0.07, t * 0.18, t * 0.18), Tema.MORADO, grosor, 0.6f);
        Path2D equis = new Path2D.Double();
        equis.moveTo(x + t * 0.09, y + t * 0.75);
        equis.lineTo(x + t * 0.25, y + t * 0.91);
        equis.moveTo(x + t * 0.25, y + t * 0.75);
        equis.lineTo(x + t * 0.09, y + t * 0.91);
        Dibujo.trazoNeon(g, equis, Tema.MORADO, grosor, 0.6f);
    };

    /** X de cerrar (esquina del encabezado). */
    public static final Icono CERRAR = (g, x, y, t, c) -> {
        Path2D equis = new Path2D.Double();
        equis.moveTo(x + t * 0.22, y + t * 0.22);
        equis.lineTo(x + t * 0.78, y + t * 0.78);
        equis.moveTo(x + t * 0.78, y + t * 0.22);
        equis.lineTo(x + t * 0.22, y + t * 0.78);
        Dibujo.trazoNeon(g, equis, c, (float) (t * 0.11), 0.8f);
    };

    private static void persona(Graphics2D g, double x, double y, double t, Color c) {
        g.setPaint(new GradientPaint(0, (float) y, Tema.aclarar(c, 0.25f), 0, (float) (y + t), c));
        g.fill(new Ellipse2D.Double(x + t * 0.3, y + t * 0.04, t * 0.4, t * 0.4));
        Area cuerpo = new Area(new Ellipse2D.Double(x + t * 0.08, y + t * 0.5, t * 0.84, t * 0.84));
        cuerpo.intersect(new Area(new Rectangle2D.Double(x, y + t * 0.5, t, t * 0.46)));
        g.fill(cuerpo);
    }

    /** Estrella de cinco puntas centrada en (cx, cy). */
    private static Shape estrella(double cx, double cy, double radioExterior, double radioInterior) {
        Path2D estrella = new Path2D.Double();
        for (int i = 0; i < 10; i++) {
            double r = i % 2 == 0 ? radioExterior : radioInterior;
            double a = -Math.PI / 2 + i * Math.PI / 5;
            double px = cx + Math.cos(a) * r;
            double py = cy + Math.sin(a) * r;
            if (i == 0) {
                estrella.moveTo(px, py);
            } else {
                estrella.lineTo(px, py);
            }
        }
        estrella.closePath();
        return estrella;
    }
}
