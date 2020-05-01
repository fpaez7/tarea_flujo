import random

class Persona:

    def __init__(self,id,probabilidad_contagio,dias_recuperacion,dias_sintomas):
        self._id = id
        self._probabilidad_contagio = probabilidad_contagio
        self._estado = "S" # S: sano; A asintomatico; E enfermo ; M muerto ; R recuperado
        self._dias_recuperacion = dias_recuperacion #cuenta regresiva a recuperacion
        self._dias_sintomas = dias_sintomas #cuenta regresiva a presentar sintomas
    def contacto(self):
        pass
    def __repr__(self):
        return self._estado+str(self._id)
    def __str__(self):
        if self.estado == "S":
            return f"Soy {self._id}, estoy Sano, P contagio {self._probabilidad_contagio}"
        if self.estado == "A":
            return f"Soy {self._id}, estoy Asintomatico,sintomas:{self._dias_sintomas}, recuperacion {self.dias_recuperacion}"
        if self.estado == "E":
            return f"Soy {self._id}, estoy Enfermo, recuperacion {self.dias_recuperacion}"
        if self.estado == "I":
            return f"Soy {self._id}, estoy Inmune "


if __name__ == '__main__':
    Persona(1,3)
