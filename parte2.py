import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
path_archivo = os.path.join(script_dir, "Instancias/costos_inventario30.txt")

with open (path_archivo) as file:
    linea = file.__next__()[1:-2]
    inter = linea.split(",") #lista
    print(inter)
