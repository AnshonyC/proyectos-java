package com.mycompany.conversor;
import java.util.Scanner;
public class Conversor {
    public static void main(String[] args) {
        Scanner outs = new Scanner(System.in);
        System.out.println("Ingrese sus minutos:");
        int input_minutes = outs.nextInt();
        float minute = input_minutes;
        System.out.println("Minutos:"+minute);
        System.out.println("Horas:"+(minute/60));
        System.out.println("Dias:"+(minute/1440));     
    }
}
