import random

class Persona:

    def __init__(self,id,probabilidad_contagio):
        self.id = id
        self.probabilidad_contagio = probabilidad_contagio
        self.estado = "S" # S: sano; A asintomatico; E enfermo ; M muerto ; R recuperado
        self.dia_de_contagio = 0 #Lleva la cuenta de la cantidad de dias desde que se enfermo
    def __repr__(self):
        return self.id
    def __str__(self):
        if self.estado == "S":
            return f"Soy {self.id}, estoy Sano y mi probabilidad de infectarme es {self.probabilidad_contagio}"
        if self.estado == "A":
            return f"Soy {self.id}, soy asintomatico  y me enfeme el dia  {self.dia_de_contagio}"
        if self.estado == "E":
            return f"Soy {self.id}, estoy enfermo y me enfeme el dia  {self.dia_de_contagio}"
        if self.estado == "E":
            return f"Soy {self.id}, estoy sano"


if __name__ == '__main__':
    Persona(1,3)
