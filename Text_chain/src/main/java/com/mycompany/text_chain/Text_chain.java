package com.mycompany.text_chain;
import java.util.Scanner;
public class Text_chain {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        System.out.print("Ingrese una palabra o cadena: ");
        String palabra = sc.nextLine();
        
        for (int i = 0; i < palabra.length(); i++) {
            System.out.println(palabra.charAt(i));
        }
    }
}
    

