from random import seed, random
from numpy.random import poisson, negative_binomial
from numpy.random import seed as npseed



def simulation_parameters(total, delta_t,s):
    seed(s)
    npseed(s)
    r_p = {i: poisson(15) for i in range(total)} # El tiempo de recuperacion
    c_p = {i: min(r_p[i], negative_binomial(6,0.5)) for i in range(total)} # Tiempo en que se da cuenta
    contagios = {t: {i: random() for i in range(total)} for t in range(delta_t + 1)}

    return r_p, c_p, contagios
