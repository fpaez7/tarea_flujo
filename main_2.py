import networkx as nx
import os
import json


def abrir (nombre):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    path_archivo = os.path.join(script_dir, nombre)
    with open(path_archivo, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

if __name__ == '__main__':
    json_object = abrir ("Instancias/costos_inventario30.txt")


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


if __name__ == '__main__':
    encuentros = {'e0': {'t0': 22, 't1': 16}, 'e1': {'t0': 34, 't1': 26}}
    abastecimientos = {'a0': {'t0': 720, 't1': 586}, 'a1': {'t0': 561, 't1': 985}}
    transporte = {'a0': {'e0': (5, 32), 'e1': (6, 43)},'a1': {'e0': (7, 67), 'e1': (8, 36)}}
    inventario = {'a0': (0, 427), 'a1': (0, 445)}
    G = crear_grafo(abastecimientos,encuentros,transporte,inventario)
    flowDict = nx.min_cost_flow(G)
    print(flowDict)
