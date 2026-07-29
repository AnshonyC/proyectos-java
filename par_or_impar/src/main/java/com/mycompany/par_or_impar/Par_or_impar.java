package com.mycompany.par_or_impar;
import java.util.Scanner;
public class Par_or_impar {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Introduce un numero: ");
        int numero = scanner.nextInt();
        String resultado = (numero % 2 == 0) ? "par" : "impar";
        System.out.println("El numero es " + resultado);
        scanner.close();
    }
}
