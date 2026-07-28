package com.mycompany.vehiculos;

public class Vehiculos {
    protected int numeroLlantas;
    protected String marca;
    
    public Vehiculos(int numeroLlantas, String marca){
        this.numeroLlantas = numeroLlantas;
        this.marca = marca;
    }
    
    public void encender(){
        System.out.println("El vehículo encendió");
    }
}
