package com.mycompany.calificador_notas;
import java.util.Scanner;
public class Calificador_notas {
    public static void main(String[] args) {
        //Variables
        Scanner input = new Scanner(System.in);
        int num_notas = 0;
        int contador_aprobados = 0;
        int contador_reprobados = 0;
        
        System.out.println("Ingrese la cantidad de notas que ingresara:");
        num_notas = input.nextInt();
        
        System.out.println("Ingrese"+num_notas+":");
        
        int []notas = new int[num_notas];
        for(int i = 0;i < num_notas;i++){
            System.out.println((i+1)+")Numero:");
            notas[i] = input.nextInt();
        }
        
        for(int u = 0;u < num_notas;u++){
            if(notas[u]>=60){
                contador_aprobados = contador_aprobados + 1;
            }
            else{
                contador_reprobados = contador_reprobados +1;
            }
        }
        System.out.println("Los alumnos aprobados son:"+contador_aprobados);
        System.out.println("Los alumnos reprobados son:"+contador_reprobados);
    }
}
