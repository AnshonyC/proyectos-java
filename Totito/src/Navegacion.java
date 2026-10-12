/**
 * Lo que las pantallas pueden pedir: cambiar a otra pantalla, empezar una
 * partida o cerrar el juego. Lo implementa PanelPrincipal.
 *
 * Gracias a esta interfaz ninguna pantalla conoce a las demas: solo dicen
 * "quiero ir al menu" y PanelPrincipal se encarga.
 */
public interface Navegacion {

    void irAlMenu();

    void irAInstrucciones();

    void irAConfiguracion();

    /** Crea una partida nueva (marcador en cero) y muestra el tablero. */
    void iniciarPartida(Jugador jugador1, Jugador jugador2, Partida.Modo modo);

    /** Muestra la pantalla de victoria o empate de la partida terminada. */
    void mostrarResultado(Partida partida);

    /** Otra partida con los mismos jugadores, conservando el marcador. */
    void jugarDeNuevo();

    void salir();
}
