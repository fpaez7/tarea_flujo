import os
import networkx as nx


script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
path_archivo_inventario = os.path.join(script_dir, "Instancias/costos_inventario30.txt")
path_archivo_transporte = os.path.join(script_dir, "Instancias/costos_transporte30x50.txt")
path_archivo_abastecimiento = os.path.join(script_dir, "Instancias/matriz_abastecimiento30x70.txt")
path_archivo_encuentro = os.path.join(script_dir, "Instancias/matriz_encuentro50x70.txt")

with open (path_archivo_inventario) as file:
    linea_inventario = file.__next__()[1:-2]

with open (path_archivo_transporte) as file:
    linea_transporte = file.__next__()[1:-2]

with open (path_archivo_abastecimiento) as file:
    linea_abastecimiento = file.__next__()[1:-2]

with open (path_archivo_encuentro) as file:
    linea_encuentro = file.__next__()[1:-2]

def json_a_dict(string):  #convierte en dicconario a costos_inventario30
    string = string.split("),")
    dict = {}
    for i in string:
        i = i.split(": (")
        j = i[1].split(",")
        dict[i[0]] = j
    return dict

def json_a_dict2(string):  #convierte en dicconario a costos_transporte30x50
    dict = {}
    string = string.split("},")
    for i in string:
        i = i.split(": {")
        #i[1] es otro json
        dict[i[0]] = json_a_dict(i[1])
    return dict

def json_a_dict4(string):  #convierte en dicconario a costos_inventario30
    string = string.split(", ")
    dict = {}
    for i in string:
        i = i.split(":")

        dict[i[0]] = i[1]
    return dict

def json_a_dict3(string):  #convierte en dicconario a costos_transporte30x50
    dict = {}
    string = string.split("},")
    for i in string:
        i = i.split(": {")
        #i[1] es otro json
        dict[i[0]] = json_a_dict4(i[1])
    return dict

dic_inventario = json_a_dict(linea_inventario)
dic_transporte = json_a_dict2(linea_transporte)
dic_abastecimiento = json_a_dict3(linea_abastecimiento)
dic_encuentro = json_a_dict3(linea_encuentro)

lista_tiempo = dic_abastecimiento["'a0'"].keys()

def crear_grafo():
    G = nx.Graph()
    oferta_total = 0
    demanda_total = 0
    #creamos todos los nodos de abastecimiento y retiro en el tiempo
    for nodo in dic_abastecimiento.keys(): #para cada punto de abastecimiento, oferta
        for tiempo in lista_tiempo: #para cada periodo de tiempo
            nombre = nodo + tiempo
            oferta_total += int(dic_abastecimiento[nodo][tiempo])
            G.add_node(nombre, demand = -1*int(dic_abastecimiento[nodo][tiempo])) #,demand = oferta
    for nodo in dic_encuentro.keys():
        for tiempo in lista_tiempo:
            nombre = nodo + tiempo
            demanda_total += int(dic_encuentro[nodo][tiempo])
            G.add_node(nombre, demand = int(dic_encuentro[nodo][tiempo]))

#crear nuestro nodo de sobreoferta para balancear el grafo
    G.add_node("sobreoferta", demand = oferta_total- demanda_total)
    for nodo in dic_abastecimiento:
        for tiempo in lista_tiempo:
            nombre = nodo + tiempo
            G.add_edge(nombre, "sobreoferta", weight = 0)
    #creamos los arcos que conectan los puntos de abastecimiento con los puntos de retiro
    for tiempo in lista_tiempo:
        for nodo in dic_abastecimiento.keys():
            for nodo2 in dic_encuentro.keys():
                nodo1 = nodo + tiempo
                nodo3 = nodo2 + tiempo
                cap = int(dic_transporte[nodo][nodo2][1].replace(")",""))
                G.add_edge(nodo1, nodo3, weight = int(dic_transporte[nodo][nodo2][0]), capacity = cap)
    #crear el arco de continuidad de inventario
    for i in range(0, len(lista_tiempo)-1):
        for nodo in dic_abastecimiento.keys():
            nodo1 = nodo + list(lista_tiempo)[i]
            nodo2 = nodo + list(lista_tiempo)[i+1]
            G.add_edge(nodo1, nodo2, weight = str(dic_inventario[nodo][0]), capacity = int(dic_inventario[nodo][1]))
    return G

G = crear_grafo()
#flowDict = nx.min_cost_flow(G)
#print(flowDict)
