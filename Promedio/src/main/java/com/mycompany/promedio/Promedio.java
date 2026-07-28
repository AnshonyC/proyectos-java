package com.mycompany.promedio;

public class Promedio {

    // Atributo: arreglo de notas
    private double[] notas;

    // Constructor que recibe el arreglo de notas
    public Promedio(double[] notas) {
        this.notas = notas;
    }

    // Método que calcula el promedio recorriendo el arreglo
    public double calculaPromedio() {
        if (notas == null || notas.length == 0) {
            System.out.println("Error: no hay notas para calcular el promedio.");
            return 0;
        }

        double acumulacionNotas = 0;
        for (int i = 0; i < notas.length; i++) {
            acumulacionNotas += notas[i];
        }

        int totalNotas = notas.length;
        return acumulacionNotas / totalNotas;
    }
}