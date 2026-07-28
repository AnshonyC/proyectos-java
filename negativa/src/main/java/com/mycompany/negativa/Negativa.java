package com.mycompany.negativa;
import java.util.Scanner;
public class Negativa {
    public static void main(String[] args) {
        Scanner outs = new Scanner(System.in);
        System.out.println("Ingrese su numero:");
        int number = outs.nextInt();
        int Num_modificado = number-1;
        number=Num_modificado;
        if(number > 0){
            System.out.println(number);
        }
        else{
            System.out.println("valor invalido");
        }    
    }
}
