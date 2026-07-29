package com.mycompany.descuento;
public class Descuento {
    public static void main(String[] args) {
        double precio = 1000;
        int descuento = 30;
        double precio_descuento = precio*descuento/100;
        System.out.println("El precio original es:"+precio);
        System.out.println("El descuento es de:"+descuento+"%");
        System.out.println("Ahorro:"+ precio_descuento);
        System.out.println("El precio final es:"+(precio-precio_descuento));        
    }
}
