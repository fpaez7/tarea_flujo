class Persona:
    def __init__(self,id,probabilidad_contagio):
        self._id = id
        self._probabilidad_contagio = probabilidad_contagio
        self.estado = "S" # S: sano; A asintomatico; E enfermo ; M muerto ; R recuperado
        self._dias_recuperacion = 0#cuenta regresiva a recuperacion
        self._dias_sintomas = 0 #cuenta regresiva a presentar sintomas
    @property
    def dias_recuperacion(self):
        return self._dias_recuperacion
    @dias_recuperacion.setter
    def dias_recuperacion(self, a):
        if(a <= 0):
            self._dias_recuperacion = 0
            self.estado = "R"
        self._dias_recuperacion = a

    @property
    def dias_sintomas(self):
        return self._dias_sintomas
    @dias_sintomas.setter
    def dias_sintomas(self, a):
        if(a <= 0):
            self._dias_sintomas = 0
            self.estado = "E"
        self._dias_sintomas = a
    def contacto(self,dado,dias_recuperacion,dias_sintomas):
        if self.estado == "S" and dado <= self._probabilidad_contagio:
            self.estado = "A"
            self._dias_recuperacion = dias_recuperacion
            self._dias_sintomas = min(dias_sintomas, dias_recuperacion)

    def pasar_dia (self):
        if self.estado in ["A","E"]:
            if self.estado == "A":
                self.dias_sintomas -= 1
            self.dias_recuperacion -= 1

    def __repr__(self):
        return self.estado+str(self._id)
    def __str__(self):
        if self.estado == "S":
            return f"Soy {self._id}, estoy Sano, P contagio {self._probabilidad_contagio}"
        if self.estado == "A":
            return f"Soy {self._id}, estoy Asintomatico,sintomas:{self._dias_sintomas}, recuperacion {self._dias_recuperacion}"
        if self.estado == "E":
            return f"Soy {self._id}, estoy Enfermo, recuperacion {self._dias_recuperacion}"
        if self.estado == "R":
            return f"Soy {self._id}, estoy Recuperado "


if __name__ == '__main__':
    SEED = 1

    # todos debieran sanarce a los 3 dias
    p1 = Persona(1,0.4,3,1) #pasiente presenta sintomas al dia
    p2 = Persona(2,0.4,3,2) #pasiente presenta sintomas al los 3
    p3 = Persona(3,0.4,3,3) #pasiente que siempre es asintomatico
    p4 = Persona(4,0.4,3,4) #pasiente que siempre es asintomatico
    p5 = Persona(5,0.4,0,0) #parte como inmune
    # todos debieran sanarce a los 0 dias
    personas = [p1,p2,p3,p4,p5]

    contagios = simulation_parameters(5,SEED)[2]

    for i in range (0, len(personas)):
        personas[i].contacto(contagios[i])# para testear esto cambiar estado default a A todos se enferman el dia 0



    delta_dias = 3
    for i in range (0,delta_dias+1):
        print( f"Dia {i}")
        for persona in personas:
            print(persona)
            persona.pasar_dia()
