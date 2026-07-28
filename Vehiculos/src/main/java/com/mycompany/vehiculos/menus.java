package com.mycompany.vehiculos;
import java.util.Scanner;

public class menus {
    private Scanner outs = new Scanner(System.in);
    
    public Carro crearCarro(){
        System.out.println("Ingrese el numero de llantas: ");
        int llantas = outs.nextInt();
        
        System.out.println("Ingrese la marca: ");
        String marca = outs.next();
        
        System.out.println("Ingrese el numero de puertas: ");
        int puertas = outs.nextInt();
        
        return new Carro(llantas, marca, puertas);
    }
}