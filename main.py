from collections import defaultdict
from personas import Persona
from simulation_parameters import simulation_parameters
from Codigo_Graficos import graficar_infectados
import os #https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
import re # https://stackoverflow.com/questions/1249388/removing-all-non-numeric-characters-from-string-in-python
import copy # copy deep copy
import time

VERBOSO = False

def crear_grafo ( personas, reuniones):
    """ Crea un default diccionario donde las llaves son los dias y los elemntos son una
    lista con los sets con los id de las personas que se juntaron """
    data_reuniones = defaultdict(list)
    with open (reuniones) as file:
        linea = file.__next__()
    inter = linea.split("({")

    for i in range(1,len(inter)):
        parcial = set(map(int,inter[i].split("}")[0].split(", ")))
        dia = int(re.sub("[^0-9]", "",inter[i].split("}")[1] ))
        data_reuniones[dia].append(parcial)
    #dia es el dia mas alto

    #cantidad de dia desde la infeccion que su estado de Enfermos con Sintomas
    """ Crea un diccionario donde se almacenan las persoans"""
    data_personas = dict()
    with open (personas) as file:
        linea = file.__next__().strip("{}")
    inter = linea.split(", ")
    for i in inter:
        persona = i.split(":")
        id = int(persona[0])
        data_personas[id]= Persona(id,float(persona[1]))
    return (data_personas,data_reuniones)




def determinar_contagiados(grafo, p0 ,delta_dias):
    #gafo es in grafo formado por la estructura de la funcion crear_grafo
    #p0 es in integer con el indice del paciente 0
    #dia_final número de días transcurridos
    posibles = set()
    posibles.add(p0)
    data_reuniones = grafo[1]
    for t in range (0,delta_dias+1):
        if VERBOSO:
            print(f"POSIBLES al principio del DIA {t}",posibles)
        for reunion in data_reuniones[t]:
            if posibles.intersection(reunion):
                if VERBOSO:
                    print(F"Reunion infectada DIA{t}:",reunion, "culpables:",posibles.intersection(reunion))
                posibles = posibles.union(reunion)
    if VERBOSO:
        print(F"POSIBLES al final del dia {t}",posibles)
    return posibles




def simular_contagio( grafo, p0, delta_dias, s):
    #vectores = infectados actuales
    data_personas = grafo[0]
    data_reuniones = grafo[1]
    "Se simulan los parametros necesarios para cada persona"
    parametros = simulation_parameters(len(data_personas),delta_dias,s)
    dias_recuperacion = parametros[0]
    #print(dias_recuperacion)
    dias_sintomas = parametros[1]
    #print(sintomas)
    contagios = parametros[2]
    vectores = set()
    vectores.add(p0)
    infectados = set()
    infectados.add(p0)
    recuperados = set()

    data_personas[p0].contacto(0,dias_recuperacion[p0] , dias_sintomas[p0])
    datos_infectados = []
    datos_recuperados = []
    datos_it = []
    dias = []

    for t in range (0,delta_dias+1):
        if VERBOSO:
            print(f"Comienza DIA {t}")
            print("Inf:",len(infectados),"-Vect:",len(vectores),"-Rec:",len(recuperados))
            datos_infectados.append(len(infectados))
            datos_recuperados.append(len(recuperados))
            datos_it.append(len(recuperados)+len(infectados))
            dias.append(t)
        for reunion in data_reuniones[t]:
            culpables = vectores.intersection(reunion) #son los que infectaron la reunion
            if culpables:
                if VERBOSO:
                    pass
                    #print("Reunion Infectada:",reunion , "Culpables:",culpables)
                for posible_contagiado in reunion - culpables:
                    #print(data_personas[posible_contagiado]._probabilidad_contagio,contagios[t][posible_contagiado])
                    id = posible_contagiado
                    if id not in recuperados and id not in infectados:
                        data_personas[id].contacto(contagios[t][id],dias_recuperacion[id] , dias_sintomas[id])
        infectados = set()
        vectores = set()
        recuperados = set()
        for i in range(0,len(data_personas)):
            data_personas[i].pasar_dia()
            if data_personas[i].estado == "A":
                vectores.add(i)
                infectados.add(i)
                #print(data_personas[i])

            elif data_personas[i].estado == "E":
                infectados.add(i)
                #(data_personas[i])
            elif data_personas[i].estado == "R":
                recuperados.add(i)
            elif data_personas[i].estado == "S":
                pass
            else:
                print(F"ERROR ESTADO ANOMALO")
    if VERBOSO:
        print(f"Fin del DIA {t}")
        print("Inf:",len(infectados),"-Vect:",len(vectores),"-Rec:",len(recuperados))
    return infectados,recuperados,{"t":dias,
            "i":datos_infectados,
            "it":datos_it,
            "r":datos_recuperados}



def probabilidad_contagio(grafo,p0,delta_dias):
    Cantidad = len(grafo[0].keys())
    SIMULACIONES = 10
    conteos = {i: 0 for i in range(Cantidad)}
    tiempo_simulaciones = 0
    for s in range (0,SIMULACIONES):
        copia_grafo = copy.deepcopy(grafo)
        print("-"*45,f"SIMUACION SEMILLA: {s}","-"*45)
        t_inicio=time.time()
        infectados = simular_contagio(copia_grafo, p0, delta_dias,s)[0]
        tiempo_simulacion = time.time()-t_inicio
        tiempo_simulaciones += tiempo_simulacion
        print(F"Tiempo de simulacion{tiempo_simulacion}")
        for i in range(Cantidad):
            if i in infectados:
                conteos[i] += 1
    for i in range (0, Cantidad):
        conteos[i]= float(conteos[i])/float(SIMULACIONES)
        if conteos[i] and VERBOSO:
            print(f"Pasinte{i}: probabilidad: {conteos[i]}")
    print(f"Con {Cantidad} personas y {delta_dias} dias se demora {tiempo_simulaciones}s en hacer {SIMULACIONES} simulaciones\nPromedio de simulacion{tiempo_simulaciones/SIMULACIONES} s")
    return conteos

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    CODIGO = 15000 #Cantidad de pacientes
    p0 = 33 #pacoente original
    delta_dias = 20 # Cantidad de dias
    personas = os.path.join(script_dir, f"Instancias/personas_{CODIGO}.txt")
    reuniones = os.path.join(script_dir, f"Instancias/reuniones_{CODIGO}.txt")
    grafo = crear_grafo(personas,reuniones)
    determinar_contagiados(grafo,p0,delta_dias)
    """ #Para hacer una sola simulacion
    SEED = 4
    resultados = simular_contagio( grafo, 33, delta_dias, SEED)
    grafico = graficar_infectados(resultados[2])
    """
    probabilidades = probabilidad_contagio(grafo,p0,delta_dias)
    #


#    posibles = determinar_contagiados(grafo,p0,delta_dias)
