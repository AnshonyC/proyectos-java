/**
 * Representa al jugador humano: su nombre y la ficha que utiliza.
 * Es una clase simple de datos, sin logica de juego.
 */
public class Jugador {

    private final String nombre;
    private final char ficha;

    public Jugador(String nombre, char ficha) {
        this.nombre = nombre;
        this.ficha = ficha;
    }

    public String getNombre() {
        return nombre;
    }

    public char getFicha() {
        return ficha;
    }
}
