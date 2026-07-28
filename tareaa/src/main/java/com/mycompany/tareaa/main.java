package com.mycompany.tareaa;
import java.util.Scanner;
public class main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Ingrese su nombre: ");
        String nombre = sc.nextLine();
        System.out.println("Hola " + nombre);
        System.out.println("Escoge una opcion");
        System.out.println("1)Suma");
        System.out.println("2)Resta");
        System.out.println("3)Multiplicar");
        System.out.println("4)Dividir");
        System.out.println("Opcion:");
        char option_menu = sc.next().charAt(0);

        switch (option_menu) {
            case '1':
            case '2':
            case '3':
            case '4':
                System.out.println("Escriba sus numeros ");
                System.out.println("Numero 1:");
                int num1 = sc.nextInt();
                System.out.println("Numero 2:");
                int num2 = sc.nextInt();

                Operaciones op = new Operaciones(num1, num2);

                switch (option_menu) {
                    case '1':
                        System.out.println("La suma es: " + op.sumar());
                        break;
                    case '2':
                        System.out.println("La resta es: " + op.restar());
                        break;
                    case '3':
                        System.out.println("La multiplicación es: " + op.multiplicar());
                        break;
                    case '4':
                        try {
                            System.out.println("La división es: " + op.dividir());
                        } catch (ArithmeticException e) {
                            System.out.println("Error: " + e.getMessage());
                        }
                        break;
                }
                break;

            default:
                System.out.println("opcion no valida");
        }

        sc.close();
    }
}