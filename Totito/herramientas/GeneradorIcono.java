import java.awt.GradientPaint;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.geom.RoundRectangle2D;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import javax.imageio.ImageIO;

/**
 * Crea el icono del programa a partir del logotipo del juego:
 *   recursos/totito.ico  (para el .exe de Windows)
 *   recursos/totito.png  (para otros sistemas y para mostrarlo)
 *
 * Un .ico es un paquete con el mismo dibujo en varios tamanos; Windows
 * elige el que necesita (16 px en la barra de titulo, 256 px en el
 * escritorio). Java no sabe escribir .ico, asi que se arma a mano: una
 * cabecera, una entrada por tamano y despues cada imagen como PNG.
 *
 * Ejecutar desde la carpeta Totito, despues de compilar el proyecto:
 *   java -cp target/classes herramientas/GeneradorIcono.java
 */
public class GeneradorIcono {

    private static final int[] TAMANOS = {16, 24, 32, 48, 64, 128, 256};

    public static void main(String[] args) throws IOException {
        File carpeta = new File("recursos");
        carpeta.mkdirs();

        BufferedImage grande = dibujar(1024);
        ImageIO.write(reducir(grande, 512), "png", new File(carpeta, "totito.png"));

        byte[][] pngs = new byte[TAMANOS.length][];
        for (int i = 0; i < TAMANOS.length; i++) {
            ByteArrayOutputStream bytes = new ByteArrayOutputStream();
            ImageIO.write(reducir(grande, TAMANOS[i]), "png", bytes);
            pngs[i] = bytes.toByteArray();
        }

        try (DataOutputStream ico = new DataOutputStream(
                new FileOutputStream(new File(carpeta, "totito.ico")))) {
            // Cabecera: reservado (0), tipo 1 = icono, cantidad de imagenes.
            corto(ico, 0);
            corto(ico, 1);
            corto(ico, TAMANOS.length);
            // Una entrada de 16 bytes por imagen. Los datos empiezan despues de todas.
            int posicion = 6 + 16 * TAMANOS.length;
            for (int i = 0; i < TAMANOS.length; i++) {
                int lado = TAMANOS[i] >= 256 ? 0 : TAMANOS[i];   // 0 significa 256
                ico.writeByte(lado);        // ancho
                ico.writeByte(lado);        // alto
                ico.writeByte(0);           // colores de paleta (0 = sin paleta)
                ico.writeByte(0);           // reservado
                corto(ico, 1);              // planos de color
                corto(ico, 32);             // bits por pixel
                entero(ico, pngs[i].length);
                entero(ico, posicion);
                posicion += pngs[i].length;
            }
            for (byte[] png : pngs) {
                ico.write(png);
            }
        }
        System.out.println("Listo: recursos/totito.ico y recursos/totito.png");
    }

    /** El icono: cuadrado redondeado oscuro con el logotipo de neon encima. */
    private static BufferedImage dibujar(int lado) {
        BufferedImage imagen = new BufferedImage(lado, lado, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = Dibujo.preparar(imagen.getGraphics());
        g2.setPaint(new GradientPaint(0, 0, Tema.FONDO_ARRIBA, 0, lado, Tema.FONDO_ABAJO));
        g2.fill(new RoundRectangle2D.Double(0, 0, lado, lado, lado * 0.42, lado * 0.42));
        double margen = lado * 0.17;
        g2.scale(lado / 256.0, lado / 256.0);   // el neon se dibuja pensado para 256 px
        double m = margen * 256.0 / lado;
        Iconos.LOGO.dibujar(g2, m, m, 256 - 2 * m, Tema.LAVANDA);
        g2.dispose();
        return imagen;
    }

    /** Achica la imagen a la mitad una y otra vez: asi queda nitida y no pixelada. */
    private static BufferedImage reducir(BufferedImage imagen, int lado) {
        BufferedImage actual = imagen;
        int tamano = imagen.getWidth();
        do {
            tamano = Math.max(lado, tamano / 2);
            BufferedImage menor = new BufferedImage(tamano, tamano, BufferedImage.TYPE_INT_ARGB);
            Graphics2D g2 = menor.createGraphics();
            g2.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BICUBIC);
            g2.drawImage(actual, 0, 0, tamano, tamano, null);
            g2.dispose();
            actual = menor;
        } while (tamano > lado);
        return actual;
    }

    /** El formato .ico guarda los numeros "al reves" (little-endian). */
    private static void corto(DataOutputStream salida, int valor) throws IOException {
        salida.writeByte(valor & 0xFF);
        salida.writeByte((valor >> 8) & 0xFF);
    }

    private static void entero(DataOutputStream salida, int valor) throws IOException {
        corto(salida, valor & 0xFFFF);
        corto(salida, (valor >> 16) & 0xFFFF);
    }
}
