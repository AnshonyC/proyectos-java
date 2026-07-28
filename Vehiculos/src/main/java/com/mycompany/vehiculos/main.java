package com.mycompany.vehiculos;
import java.util.Scanner;

public class main {
    public static void main(String[] args) {
        Scanner outs = new Scanner(System.in);
        
        System.out.println("""
         --Bienvenido Seleccione su Vehiculo--
         1.Automovil
         2.Motocicleta
         Opcion seleccionada:
        """);
        char option = outs.next().charAt(0);
        
        switch(option){
            case '1':
                menus menu = new menus();
                Carro miCarro = menu.crearCarro();
                miCarro.encender();       // heredado de Vehiculos
                miCarro.tipo_vehiculo();  // propio de Carro
                break;
                
            case '2':
                System.out.println("Opción Motocicleta (pendiente)");
                break;
                
            default:
                System.out.println("Opción inválida");
                break;
        }
    }
}