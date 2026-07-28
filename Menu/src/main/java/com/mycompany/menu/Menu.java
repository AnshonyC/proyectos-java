package com.mycompany.menu;

import java.util.Scanner;

public class Menu {
    public static void main(String[] args) {
        int salida = 0;
        Scanner out = new Scanner(System.in);
        
        do {
            System.out.println("---MENU---");
            System.out.println("1)Nuevo");
            System.out.println("2)Eliminar");
            System.out.println("3)Modificar");
            System.out.println("4)Salir");
            int option = out.nextInt();
            switch (option) {
                case 1:
                    System.out.println("selecciono nuevo");
                    break;
                case 2:
                    System.out.println("selecciono eliminar");
                    break;
                case 3:
                    System.out.println("Selecciono Modificar");
                    break;
                case 4:
                    salida = 1;
                    break;
                default:
                    System.out.println("Opción no válida");
            }
        } while (salida == 0);
        
        System.out.println("Finalizo la sesion");
        out.close();
    }
}