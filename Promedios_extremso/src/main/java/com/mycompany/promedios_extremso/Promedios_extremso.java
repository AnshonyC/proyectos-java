package com.mycompany.promedios_extremso;
import java.util.Scanner;
public class Promedios_extremso {
    public static void main(String[] args) {
        //Variables
        Scanner input = new Scanner(System.in);
        int []numbers = new int[10];
        int acumulador = 0;
        
        //Bucles de ingreso y lectura
        System.out.println("Ingrese 10 numeros:");
        for(int i = 0;i < 10;i++){
            System.out.println((i+1)+")Numero:");
            numbers[i]= input.nextInt();
        }
        for(int u = 0;u < 10;u++){
            acumulador = numbers[u]+acumulador;
        }
        
        //Sistema de dectector de numero menor o mayor 
        int mayor = numbers[0];
        int menor = numbers[0];

        for (int i = 1; i < numbers.length; i++) {
            if (numbers[i] > mayor) {
                mayor = numbers[i];
            }
            if (numbers[i] < menor) {
                menor = numbers[i];
            }
        }
        System.out.println("El numero mayor es: " + mayor);
        System.out.println("El numero menor es: " + menor);
        
        //sumatoria
        System.out.println("La sumatoria de los 10 numeros son:"+acumulador);
        
        //Promedio
        System.out.println("El promedio es:"+(acumulador/10));
        input.close();
    }
}
