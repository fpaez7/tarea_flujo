from collections import defaultdict          #para ordenarse en los momentos de reunion
from personas import Persona                #clase creada, mencionada en la celda anterior
from simulation_parameters import simulation_parameters    #para llamar a la funcion simulatio_parameters
from Codigo_Graficos import graficar_infectados            #para llamar a la funcion
import os  #https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
import re  #https://stackoverflow.com/questions/1249388/removing-all-non-numeric-characters-from-string-in-python
import copy  #https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/
import time  #medir los tiempos tiempos de simulacion, para medir la eficienci
VERBOSIDAD = 1 # 0 es no imprimir nada, 1 minimo (recomendado), 2 es imprimir lo basico  , 3 es imprimir los detalles


def crear_grafo ( personas, reuniones):
    """ Crea un default diccionario donde las llaves son los dias y los elemntos son una
    lista con los sets con los id de las personas que se juntaron """
    data_reuniones = defaultdict(list)
    with open (reuniones) as file:    #abrir archivo
        linea = file.__next__()       #nos da la unica linea del archivo
    inter = linea.split("({")         #lee la base de datos

    for i in range(1,len(inter)):
        parcial = set(map(int,inter[i].split("}")[0].split(", ")))    #usamos sets porque es mas eficiente la busqueda, facilita todo
        dia = int(re.sub("[^0-9]", "",inter[i].split("}")[1] ))
        data_reuniones[dia].append(parcial)
    #reuniones son los arcos
    #cantidad de dia desde la infeccion que su estado de Enfermos con Sintomas
    """ Crea un diccionario donde las llaves son las id y los elementos son instancias de la clase personas"""
    data_personas = dict()    #no es defaultdict porque no tiene sentido preguntar por personas que no existen (gigo)
    with open (personas) as file:   #fue un diccionario en vez de una lista, porque al principio estaba  desordenado y ahora no, pero ya esta hecho
        linea = file.__next__().strip("{}")
    inter = linea.split(", ")
    for i in inter:
        persona = i.split(":")
        id = int(persona[0])
        data_personas[id]= Persona(id,float(persona[1]))   #aca se guardo en cada nodo, una instancia para cada persona
    return (data_personas,data_reuniones)



#bastante efciciente creo que el por caso seria si todas las personas se juntaran todos los dias
def determinar_contagiados(grafo, p0 ,delta_dias):
    #grafo es un grafo formado por la estructura de la funcion crear_grafo
    #p0 es in integer con el indice del paciente 0
    #dia_final número de días transcurridos
    posibles = set()
    posibles.add(p0)
    data_reuniones = grafo[1]
    for t in range (0,delta_dias+1):
        if VERBOSIDAD>1:
            print(f"POSIBLES al principio del DIA {t}",posibles)
        for reunion in data_reuniones[t]:
            if posibles.intersection(reunion):
                posibles = posibles.union(reunion)
                if VERBOSIDAD > 3:
                    print(F"Reunion infectada DIA{t}:",reunion, "culpables:",posibles.intersection(reunion))
    if VERBOSIDAD > 1:
        print(F"\n POSIBLES al final del dia {t}",posibles)
    return posibles




def simular_contagio( grafo, p0, delta_dias, s):
    #vectores = infectados actuales
    data_personas = grafo[0]          #primer elemento del grafo (los nodos)
    data_reuniones = grafo[1]          # segundo
    "Se simulan los parametros necesarios para cada persona"
    parametros = simulation_parameters(len(data_personas),delta_dias,s)
    dias_recuperacion = parametros[0]
    dias_sintomas = parametros[1]
    contagios = parametros[2]
    vectores = set()        #los que pueden contagiar
    vectores.add(p0)
    infectados = set()
    infectados.add(p0)
    recuperados = set()

    data_personas[p0].contacto(0,dias_recuperacion[p0] , dias_sintomas[p0])  ##inicilizar el tiempo para p0 con sus contadores
    datos_infectados = []
    datos_recuperados = []
    datos_it = []
    dias = []

    for t in range (0,delta_dias+1):
        if VERBOSIDAD > 1:
            print(f"Comienza DIA {t}")
            print("Inf:",len(infectados),"-Vect:",len(vectores),"-Rec:",len(recuperados))
        datos_infectados.append(len(infectados))
        datos_recuperados.append(len(recuperados))
        datos_it.append(len(recuperados)+len(infectados))     #guardando los datos de cada dia para ponerlos en el grafico
        dias.append(t)
        for reunion in data_reuniones[t]:
            culpables = vectores.intersection(reunion) #son los que infectaron la reunion, que tiene complejidad (buscar)
            if culpables:                    #si es que existen culpables, que es lo mismo que decir len(culpables)>0
                for posible_contagiado in reunion - culpables:       # la resta es sacar los elementos iguales
                    id = posible_contagiado
                    if id not in recuperados and id not in infectados:   # si no esta en ninguno de los dos, esta sano
                        data_personas[id].contacto(contagios[t][id],dias_recuperacion[id] , dias_sintomas[id])  # ese contagios da el numero del dado,

        ##########################################################
        ##### VERDADERA FUENTE DE INEFICIENCIA DEL PROGRAMA ######
        ##########################################################
        # porque iteramos sobre todas las personas todos los dias O(m*n)   m:cantidad personas, n: cantidad de días
        # si queremos mejorar la eficiencia del codigo, esto es lo que hay que mejorar
        # podriamos llevar la cuenta de cambios de estado de las personas y asi tener el estado en cada momento del individuo, pero de esta forma,
        # perdemos la moldeabilidad y la escalabilidad del codigo (por ahora podría tener más caracteristicas el codigo(relaciones mas complejas,
        # mas enfermedades, muertes, entre otros factores) gracias a que los tratamos como objeto y no como una sola variable)
        infectados = set()
        vectores = set()
        recuperados = set()
        for i in range(0,len(data_personas)):
            data_personas[i].pasar_dia()
            if data_personas[i].estado == "A":
                vectores.add(i)
                infectados.add(i)
            elif data_personas[i].estado == "E":
                infectados.add(i)
            elif data_personas[i].estado == "R":
                recuperados.add(i)
            elif data_personas[i].estado == "S":
                pass
            else:
                print("ERROR ESTADO ANOMALO")
    if VERBOSIDAD:
        print(f"Fin del DIA {t}")
        print("Inf:",len(infectados),"-Vect:",len(vectores),"-Rec:",len(recuperados))
    return infectados,recuperados,{"t":dias,
            "i":datos_infectados,
            "it":datos_it,
            "r":datos_recuperados}


def probabilidad_contagio(grafo,p0,delta_dias):
    Cantidad = len(grafo[0])       #se obtiene la cantidad de personas
    SIMULACIONES = 1000
    conteos = {i: 0 for i in range(Cantidad)}      #esto crea un diccionario con las llaves siendo el id de la persona, y con todos los elementos en 0
    tiempo_simulaciones = 0                        #crea el tiempo para las simulaciones
    for s in range (0,SIMULACIONES):               #s es la semilla para poder hacer la cantidad de simulaciones requerida (1000), para tener diferentes semillas
        copia_grafo = copy.deepcopy(grafo)         # en vez de crear grafos para cada simulacion, los copiamos y los vamos sobreescribiendo
        if VERBOSIDAD:
            print("-"*45,f"SIMUACION SEMILLA: {s}","-"*45)
        t_inicio=time.time()
        infectados = simular_contagio(copia_grafo, p0, delta_dias,s)[0]   ##aca da la complejidad del algoritmo que es O(|s|*|Cantidad|)  (cada simulacion se demora lac antidad de dias asi que son lo mismo)
        tiempo_simulacion = time.time()-t_inicio
        tiempo_simulaciones += tiempo_simulacion        #autoexplicativo
        if VERBOSIDAD: # es lo mismo que if verbosidad >=1
            print(F"Tiempo de simulacion{tiempo_simulacion}")
        for i in range(Cantidad):
            if i in infectados:
                conteos[i] += 1       #en este for, se va actualizando el valor del diccionario, que nos dice cuantas veces se enfermo cada weon
    for i in range (0, Cantidad):
        conteos[i]= float(conteos[i])/float(SIMULACIONES) #ya esta hecha la division
        if conteos[i] and VERBOSIDAD > 1:
            print(f"Pasinte{i}: probabilidad: {conteos[i]}") #pos simplicidad solo printea los que son distintos de 0
    if VERBOSIDAD:
        print(f"Con {Cantidad} personas y {delta_dias} dias se demora {tiempo_simulaciones}s en hacer {SIMULACIONES} simulaciones\nPromedio de simulacion{tiempo_simulaciones/SIMULACIONES} s")
    return conteos


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    CODIGO = 1500 #Cantidad de pacientes
    p0 = 33 #pacoente original
    delta_dias = 20 # Cantidad de dias
    personas = os.path.join(script_dir, f"Instancias/personas_{CODIGO}.txt")
    reuniones = os.path.join(script_dir, f"Instancias/reuniones_{CODIGO}.txt")
    grafo = crear_grafo(personas,reuniones)
    posibles = determinar_contagiados(grafo,p0,delta_dias)
    SEED = 4
    resultados = simular_contagio( grafo, 33, delta_dias, SEED)
    grafico = graficar_infectados(resultados[2])
    print("INTENTAR CERRRAR EL GRAFICO PARA PODER PASASR A LAS MULTIPLES SIMULACIONES")
    time.sleep(0.5)
    probabilidades = probabilidad_contagio(grafo,p0,delta_dias)
