from collections import defaultdict
from personas import Persona
from simulation_parameters import simulation_parameters, simulation_contagios
import re # https://stackoverflow.com/questions/1249388/removing-all-non-numeric-characters-from-string-in-python

VERBOSO = True

def crear_grafo ( personas, reuniones ):
    "Se simulan los parametros necesarios para cada persona"
    parametros = simulation_parameters(CODIGO,SEED)
    recuperaciones = parametros [0] ##cantidad de dia desde la infeccion que su estado cambia a Inmune
    sintomas = parametros[1] #cantidad de dia desde la infeccion que su estado de Enfermos con Sintomas
    """ Crea un diccionario donde se almacenan las persoans"""
    data_personas = dict()
    with open (personas) as file:
        linea = file.__next__().strip("{}")
    inter = linea.split(", ")
    for i in inter:
        persona = i.split(":")
        id = int(persona[0])
        data_personas[id]= Persona(id,float(persona[1]),recuperaciones[id],sintomas[id])
    """ Crea un diccionario donde las llaves son los dias y los elemntos son una
    lista con los sets con los id de las personas que se juntaron """


    data_reuniones = defaultdict(list)
    with open (reuniones) as file:
        linea = file.__next__()
    inter = linea.split("({")
    for i in range(1,len(inter)):
        parcial = set(map(int,inter[i].split("}")[0].split(", ")))
        dia = int(re.sub("[^0-9]", "",inter[i].split("}")[1] ))
        data_reuniones[dia].append(parcial)
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

    data_reuniones = grafo[1]
    data_personas = grafo[0]
    contagios = simulation_contagios(len(data_personas),delta_dias,SEED)
    vectores = set()
    vectores.add(p0)
    infectados = set()
    infectados.add(p0)
    recuperados = set()

    # EL paciente P se enferma si o si
    data_personas[p0].contacto(0)
    print(data_personas[p0])
    datos_infectados = []

    for t in range (0,delta_dias+1):

        if VERBOSO:
            print(f"Comienza DIA {t}")
            print("Inf:",len(infectados),"-Vect:",len(vectores),"-Rec:",len(recuperados))
            datos_infectados.append([t,len(infectados)])
        for reunion in data_reuniones[t]:
            culpables = vectores.intersection(reunion) #son los que infectaron la reunion
            if culpables:
                if VERBOSO:
                    #print("Reunion Infectada:",reunion , "Culpables:",culpables)
                for posible_contagiado in reunion - culpables:
                    #print(data_personas[posible_contagiado]._probabilidad_contagio,contagios[t][posible_contagiado])
                    data_personas[posible_contagiado].contacto(contagios[t][posible_contagiado])
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










if __name__ == '__main__':
    CODIGO = 1500
    SEED = 4
    p0 = 33
    delta_dias = 3
    personas = f"personas_{CODIGO}.txt"
    reuniones = f"reuniones_{CODIGO}.txt"
    grafo = crear_grafo(personas,reuniones)
    simular_contagio( grafo, 33 , 4, SEED)
#    posibles = determinar_contagiados(grafo,p0,delta_dias)
