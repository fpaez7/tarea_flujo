import networkx as nx
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
import re #https://stackoverflow.com/questions/1249388/removing-all-non-numeric-characters-from-string-in-python

def abrir (nombre):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    path_archivo = os.path.join(script_dir, nombre)
    with open(path_archivo, 'r') as file:
        return eval(file.__next__())
    return y

def crear_grafo(dic_abastecimientos,dic_encuentros,dic_transportes, dic_inventarios):
    G = nx.DiGraph()
    oferta_total = 0
    demanda_total = 0
    # nodos de abastecimiento son los oferente
    for abastero in dic_abastecimientos:
        for tiempo in dic_abastecimientos[abastero]:
            oferta = dic_abastecimientos[abastero][tiempo]
            oferta_total += oferta
            G.add_node(f"{abastero}-{tiempo}", demand = -oferta)
    # nodos de encuentro son los demandantes
    for encuentro in dic_encuentros:
        for tiempo in dic_encuentros[encuentro]:
            demanda = dic_encuentros[encuentro][tiempo]
            demanda_total += demanda
            G.add_node(f"{encuentro}-{tiempo}", demand = demanda)
    G.add_node("sobreoferta", demand = oferta_total- demanda_total)
    for abastero in dic_abastecimientos:
        for tiempo in dic_abastecimientos[abastero]:
            G.add_edge(f"{abastero}-{tiempo}", "sobreoferta", weight = 0)


    #creamos los arcos que conectan los puntos de abastecimiento y retiro
    for abastero in dic_transportes:
        for encuentro in dic_transportes[abastero]:
            for tiempo in dic_abastecimientos[abastero]:
                costo = dic_transportes[abastero][encuentro][0]
                cap = dic_transportes[abastero][encuentro][1]
                G.add_edge(f"{abastero}-{tiempo}", f"{encuentro}-{tiempo}",
                            weight = costo, capacity = cap)

    #crear el arco de continuidad de inventario
    #uniendo todo punto abastero con su antesesor temporal
    for abastero in dic_abastecimientos:
        t_anterior = False
        for tiempo in dic_abastecimientos[abastero]:
            if t_anterior:
                costo = dic_inventarios[abastero][0]
                cap = dic_inventarios[abastero][1]
                G.add_edge(f"{abastero}-{t_anterior}", f"{abastero}-{tiempo}",
                        weight = costo, capacity = cap)
            t_anterior = tiempo
    return G
def coordenadas(nodo):
    tipo = nodo[0]
    nodo = nodo.split("-")
    if len (nodo) == 2:
        id   = int(re.sub("[^0-9]","",nodo[0] ))
        tiempo  = int(re.sub("[^0-9]","",nodo[1] ))
    else:
        id = 0
        tiempo = 0
    return id,tiempo,tipo

def Graficar(grafo, dict_flujos = False ):
    with plt.style.context("bmh"): #estilo del gráfico: por ejemplo probar 'dark_background'
        fig = plt.figure("Grafo", figsize=(100, 7)) #Genera una figura
        ax = Axes3D(fig) #genera un eje
        colores = {'s':'red','a':'magenta','e':"cyan"  }
        dict_zeta = {'s':2,'a':1,'e':0 }
        x_a=[]
        y_a=[]
        z_a=[]

        x_e=[]
        y_e=[]
        z_e=[]
        for i in grafo.nodes():
            coor = coordenadas(i)
            id = coor[0]
            tiempo = coor[1]
            tipo = coor[2]
            if tipo == "e":
                x_a.append(id)
                y_a.append(tiempo)
                z_a.append(dict_zeta[tipo])
            elif tipo == "a":
                x_e.append(id)
                y_e.append(tiempo)
                z_e.append(dict_zeta[tipo])
            elif tipo == "s":
                x_s =[ id ]
                y_s =[ tiempo]
                z_s = [dict_zeta[tipo]]
        ax.scatter3D(x_e, y_e, z_e,color= colores['e'])
        ax.scatter3D(x_a, y_a, z_a,color= colores['a'])
        ax.scatter3D(x_s, y_s, z_s,color= colores['s'])

        if not dict_flujos:
            flujos = dict(grafo.adjacency())
        else:
            flujos = dict_flujos

        for inicio in flujos:
            for fin in flujos[inicio]:
                print(coordenadas(inicio),coordenadas(fin))
                coor_in = coordenadas(inicio)
                coor_fn = coordenadas(fin)
                x = np.array((coor_in[0],coor_fn[0]))
                y = np.array((coor_in[1],coor_fn[1]))
                z = np.array((dict_zeta[coor_in[2]],dict_zeta[coor_fn[2]]))
                #ax.plot(x,y,z, alpha=0.7, marker= 8 ,c="g")


        ax.view_init(30, 210) #Es el ángulo en el que se muestra el gráfico: si están desde un editor, podrán girarlo
        ax.set_xlabel('Id')
        ax.set_ylabel('Tiempo')
        ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
        ax.set_zlabel('Tipo de punto')
        return plt



if __name__ != '__main__':
    encuentros = abrir("Instancias/matriz_encuentro50x70.txt")
    abastecimientos = abrir("Instancias/matriz_abastecimiento30x70.txt")
    transporte = abrir ("Instancias/costos_transporte30x50.txt")
    inventario = abrir ("Instancias/costos_inventario30.txt")

    G = crear_grafo(abastecimientos,encuentros,transporte,inventario)
    Graficar(G)
    #flowDict = nx.min_cost_flow(G)
    #with open('resultado.txt', 'w') as outfile:
    #    json.dump(flowDict, outfile)


if __name__ == '__main__':
    encuentros = {'e0': {'t0': 22, 't1': 16}, 'e1': {'t0': 34, 't1': 26}}
    abastecimientos = {'a0': {'t0': 720, 't1': 586}, 'a1': {'t0': 561, 't1': 985}}
    transporte = {'a0': {'e0': (5, 32), 'e1': (6, 43)},'a1': {'e0': (7, 67), 'e1': (8, 36)}}
    inventario = {'a0': (0, 427), 'a1': (0, 445)}
    G = crear_grafo(abastecimientos,encuentros,transporte,inventario)
    flowDict = nx.min_cost_flow(G)
    with open('resultado_simple.txt', 'w') as outfile:
        json.dump(flowDict, outfile)
    Graficar(G,flowDict).show()
