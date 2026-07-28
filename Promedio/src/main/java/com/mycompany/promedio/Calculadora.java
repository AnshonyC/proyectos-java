package com.mycompany.promedio;

import java.util.Scanner;

public class Calculadora {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("¿Cuántas notas desea ingrSSSSesar?: ");
        int cantidad = sc.nextInt();

        double[] notas = new double[cantidad];

        for (int i = 0; i < cantidad; i++) {
            System.out.print("Ingrese la nota " + (i + 1) + ": ");
            notas[i] = sc.nextDouble();
        }

        // Se crea el objeto pasando el arreglo de notas por el constructor
        Promedio calc = new Promedio(notas);

        double promedio = calc.calculaPromedio();
        System.out.println("El promedio es: " + promedio);

        sc.close();
    }
}