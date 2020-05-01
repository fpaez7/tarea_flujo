from collections import defaultdict
import re



""" Crea un diccionario donde las llaves son los dias y los elemntos son una
lista con los sets con los id de las personas que se juntaron """

data_reuniones = defaultdict(list)
with open ("reuniones_1500.txt") as file:
    linea = file.__next__()
inter = linea.split("({")
for i in range(1,len(inter)):
    parcial = set(map(int,inter[i].split("}")[0].split(", ")))
    dia = int(re.sub("[^0-9]", "",inter[i].split("}")[1] ))
    data_reuniones[dia].append(parcial)
