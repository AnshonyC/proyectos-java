package com.mycompany.aniobisiesto;
import java.util.Scanner;
public class Aniobisiesto {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        System.out.print("Introduce un anio: ");
        int anio = input.nextInt();

        boolean esBisiesto = (anio % 4 == 0 && anio % 100 != 0) || (anio % 400 == 0);

        if (esBisiesto) {
            System.out.println("El anio " + anio + " es bisiesto.");
        } else {
            System.out.println("El anio " + anio + " no es bisiesto.");
        }

        input.close();
    }
}
