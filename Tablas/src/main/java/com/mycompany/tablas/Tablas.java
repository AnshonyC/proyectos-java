package com.mycompany.tablas;
import java.util.Scanner;
public class Tablas {
    public static void main(String[] args) {
        Scanner out = new Scanner(System.in);
        System.out.println("Ingrese el numero de la tabla que desea");
        int Table = out.nextInt();
        for(int i=1 ;i<= 10;i++){
            System.out.println(Table+"x"+i+"="+(Table * i));   
        }
    }
}
