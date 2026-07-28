package com.mycompany.vehiculos;

public class Carro extends Vehiculos{
    private int Numero_Puertas;
    
    public Carro(int numeroLlantas, String marca, int Numero_Puertas){
        super(numeroLlantas, marca);
        this.Numero_Puertas = Numero_Puertas;
    }
    
    public void tipo_vehiculo(){
        System.out.println("Posee un automovil");
    }
}
