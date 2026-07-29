package com.mycompany.numayor;
import java.util.Scanner;
public class Numayor {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int[] numbers = new int[3];
        
        System.out.println("Ingrese 3 numeros");
        
        for(int i = 0;i < 3;i++){     
        System.out.println((i+1)+")numero:");
        numbers[i]= input.nextInt();        
      } 
        
        if(numbers[0]>numbers[1] && numbers[0]>numbers[2]){
            System.out.println("El numero mayor es:"+numbers[0]);
        }
        else if(numbers[1]>numbers[0] && numbers[1]>numbers[2]){
            System.out.println("El numero mayor es:"+numbers[1]);
        }
        else{
            System.out.println("El numero mayor es:"+numbers[2]);
        }
        input.close();
    }
}



        