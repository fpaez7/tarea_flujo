import matplotlib.pyplot as plt
import numpy as np


def graficar_infectados(diccionario):
    cantidad_casos_totales = diccionario["it"]
    cantidad_casos_recuperados = diccionario["r"]
    cantidad_casos_actuales = diccionario["i"]
    x = diccionario["t"]
    plt.plot(x, cantidad_casos_actuales,label= 'casos actuales')
    plt.plot(x, cantidad_casos_recuperados, label= 'casos recuperados')
    plt.plot(x, cantidad_casos_totales, label= 'casos totales')
    plt.ylabel('Cantidad de infectados')
    plt.xlabel('Días')
    plt.title("Infectados en función del tiempo")

    plt.legend(loc=0)
    plt.savefig("grafico.png")
    mostrar=plt.show()
    return mostrar

if __name__ == '__main__':
    dias=[]
    cantidad_casos_actuales=[]
    cantidad_casos_totales=[]
    cantidad_casos_recuperados=[]
    casos_acumulados=0
    casos_recuperados_acumulados=0
    for dia in dias:                                                  #dias seria como la lista de los dias con lo que pasaba en cada uno
        len(cantidad_casos_actuales).append(numero__casos__actuales[dia-1])       #esto es para tener una lista con los casos actuales de cada dia
        casos_acumulados+= numero__casos__nuevos[dia-1]          #esto es para ir teniendo los casos acumulados cada dia
        casos_recuperados_acumulados+= numero__recuperados__nuevos[dia-1]      #esto es para tener los recuperados
        cantidad_casos_totales.append(casos_acumulados)
        cantidad_casos_recuperados.append(casos_recuperados_acumulados)


    graficar_infectados(cantidad_casos_totales, cantidad_casos_recuperados, cantidad_casos_actuales, 7)
