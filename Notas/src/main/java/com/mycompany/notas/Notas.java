package com.mycompany.notas;

import java.util.Scanner;

public class Notas {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        System.out.print("¿Cuántas notas desea ingresar? ");
        int cantidadNotas = sc.nextInt();
        
        double suma = 0;
        
        for (int i = 1; i <= cantidadNotas; i++) {
            System.out.print("Ingrese la nota " + i + ": ");
            double nota = sc.nextDouble();
            suma += nota;
        }
        
        double promedio = suma / cantidadNotas;
        
        System.out.println("El promedio del alumno es: " + promedio);
        
        sc.close();
    }
}