# En esta práctica se usan números aleatorios
import random

# Establecemos la semilla inicial para los números aleatorios
random.seed(123456)

# Para simplificar las soluciones usaremos utilidades proporcionadas por los siguientes módulos
import itertools
import collections


# Inferencia en redes bayesianas usando muestreo
# ==========================================================

# En esta práctica vamos a implementar métodos de inferencia probabilística en redes bayesianas,
# usando técnicas de muestreo.


# ***************************************************************
# Parte I: Estructura de datos para representar redes bayesianas.
# ****************************************************************

# Vamos a usar una estructura de datos prefijada, para representar redes
# bayesianas. Por ejemplo, la siguiente variable red_alarma contiene la
# representación de la red bayesiana del ejemplo de la alarma visto en clase:

red_alarma = [{'robo': [True, False],
               'terremoto': [True, False],
               'alarma': [True, False],
               'juanllama': [True, False],
               'mariallama': [True, False]},

              {'robo': [],
               'terremoto': [],
               'alarma': ['robo', 'terremoto'],
               'juanllama': ['alarma'],
               'mariallama': ['alarma']},

              {'robo': {(): [0.001, 0.999]},
               'terremoto': {(): [0.002, 0.998]},
               'alarma': {(True, True): [0.95, 0.05],
                          (True, False): [0.94, 0.06],
                          (False, True): [0.29, 0.71],
                          (False, False): [0.001, 0.999]},
               'juanllama': {(True,): [0.9, 0.1],
                             (False,): [0.05, 0.95]},
               'mariallama': {(True,): [0.7, 0.3],
                              (False,): [0.01, 0.99]}}]


# En general, una red bayesiana se representará mediante una lista de tres elementos. Cada uno de
# estos elementos representará:

# 1. Las variables aleatorias y sus posibles valores: un diccionario que asocia que asocia cada
#    nombre de variable con una lista de sus posible valores.

# 2. Los padres de cada variable en la red: un diccionario que asocia a cada nombre de variable con
#    una lista de sus padres.

# 3. Las tablas de probabilidad de cada nodo: un diccionario que asocia a cada nombre de variable
#    su tabla de probabilidad. A su vez, la tabla asociada a cada variable X es un diccionario que
#    asocia a cada combinación de valores de los padres, la distribución de probabilidad de X dada
#    esa combinación de valores.

#    Por ejemplo, si en la tabla de "alarma" hay una correspondencia (True, False): [0.94, 0.06],
#    quiere decir que:

#                         P(alarma=True | Robo=True, Terremoto=False)=0.94

#    y por tanto que

#                         P(alarma=False | Robo=True, Terremoto=False)=0.06.

#    Nótese que el orden implícito de los valores de una variable, y de sus padres, es el que está
#    definido en los correspondientes diccionarios.


# Lo que sigue son otras dos redes que también se han mostrado en clase de teoría:

red_infarto = [{'deportista': [True, False],
                'alimentación_equilibrada': [True, False],
                'hipertenso': [True, False],
                'fumador': [True, False],
                'infarto': [True, False]},

               {'deportista': [],
                'alimentación_equilibrada': [],
                'hipertenso': ['deportista', 'alimentación_equilibrada'],
                'fumador': [],
                'infarto': ['hipertenso', 'fumador']},

               {'deportista': {(): [0.1, 0.9]},
                'alimentación_equilibrada': {(): [0.4, 0.6]},
                'hipertenso': {(True, True): [0.01, 0.99],
                               (True, False): [0.25, 0.75],
                               (False, True): [0.2, 0.8],
                               (False, False): [0.7, 0.3]},
                'fumador': {(): [0.4, 0.6]},
                'infarto': {(True, True): [0.8, 0.2],
                            (True, False): [0.7, 0.3],
                            (False, True): [0.6, 0.4],
                            (False, False): [0.3, 0.7]}}]

red_aspersor = [{'hierba mojada': [True, False],
                 'lluvia': [True, False],
                 'nublado': [True, False],
                 'aspersor': [True, False]},

                {'nublado': [],
                 'aspersor': ['nublado'],
                 'lluvia': ['nublado'],
                 'hierba mojada': ['aspersor', 'lluvia']},

                {'nublado': {(): [0.5, 0.5]},
                 'aspersor': {(True,): [0.1, 0.9],
                              (False,): [0.5, 0.5]},
                 'lluvia': {(True,): [0.8, 0.2],
                            (False,): [0.2, 0.8]},
                 'hierba mojada': {(True, True): [0.99, 0.01],
                                   (True, False): [0.9, 0.1],
                                   (False, True): [0.9, 0.1],
                                   (False, False): [0.0, 1.0]}}]


# ******************************
# Parte II: Funciones auxiliares
# ******************************

# -----------
# Ejercicio 1
# -----------

# Definir una función "orden_compatible(red)", que recibiendo una red bayesiana, devuelva una
# ordenación topológica del grafo de la red. Es decir, una secuencia (una lista) de todas las
# variables de la red, cumpliendo que para toda variable X que sea padre de otra variable Y en la
# red, X va antes que Y en la secuencia.

# Ejemplos (hay otras posibilidades):

# >>> orden_compatible(red_alarma)
# ['terremoto', 'robo', 'alarma', 'mariallama', 'juanllama']
# >>> orden_compatible(red_infarto)
# ['alimentación_equilibrada', 'fumador', 'deportista', 'hipertenso', 'infarto']
# >>> orden_compatible(red_aspersor)
# ['nublado', 'lluvia', 'aspersor', 'hierba mojada']

# ========= Solución:

def orden_compatible(red):
    padres = red[1]

    def nivel(var):
        if not padres[var]:
            return 0
        else:
            return max(nivel(pvar) for pvar in padres[var]) + 1
    return list(sorted(padres.keys(), key=nivel))


# -----------
# Ejercicio 2
# -----------

# Definir una función "muestreo(valores, distr)" que recibiendo como entrada una lista de n valores
# de una variable aleatoria y una distribución de probabilidad (una lista de n probabilidades),
# devuelve aleatoriamente uno de los valores de la lista. La probabilidad de generar cada uno de
# los valores debe ser la correspondiente probabilidad en la distribución.

# ======== Solución:

def muestreo(valores, distr):
    r = random.random()
    for v, p in zip(valores, itertools.accumulate(distr)):
        if p > r:
            return v


# Una vez definida la función, comprobar con un número grande de muestreos que efectivamente son
# sucesos aleatorios con la probabilidad pretendida.

# >>> collections.Counter(muestreo(['v1', 'v2', 'v3'], [0.1, 0.8, 0.1]) for _ in range(int(1e6)))
# Counter({'v2': 799574, 'v3': 100368, 'v1': 100058})


# -----------
# Ejercicio 3
# -----------

# Definir la función "muestreo_a_priori(red)", que obtiene un evento aleatorio completo, siguiendo
# la distribución que define una red bayesiana que recibe como entrada.

# Ejemplos (téngase en cuenta que son resultados aleatorios):

# >>> muestreo_a_priori(red_alarma)
# {'alarma': False, 'juanllama': False, 'mariallama': False, 'robo': False, 'terremoto': False}
# >>> muestreo_a_priori(red_aspersor)
# {'aspersor': True, 'hierba mojada': True, 'lluvia': True, 'nublado': True}
# >>> muestreo_a_priori(red_infarto)
# {'alimentación_equilibrada': True, 'deportista': False, 'fumador': False, 'hipertenso': False,
# 'infarto': False}

# ======== Solución:

def muestreo_a_priori(red):
    valores = red[0]
    padres = red[1]
    tablas = red[2]
    variables = orden_compatible(red)
    muestra = {}
    for var in variables:
        padres_var = padres[var]
        valores_padres = tuple(muestra[vp] for vp in padres_var)
        valores_var = valores[var]
        distr_var = tablas[var][valores_padres]
        muestra[var] = muestreo(valores_var, distr_var)
    return muestra


# Función de normalización:
# -------------------------

# La siguiente función "normaliza(d)" normaliza una distribución de probabilidades, que viene dada
# mediante un diccionario d:

def normaliza(d):
    suma = sum(d.values())
    return {var: d[var] / suma for var in d}

# Ejemplos:

# >>> normaliza({'v1': 0.21, 'v2': 0.11, 'v3': 0.37})
# {'v1': 0.30434782608695654, 'v2': 0.15942028985507248, 'v3': 0.5362318840579711}
# >>> normaliza({True: 0.012, False: 0.008})
# {False: 0.4, True: 0.6}


# *********************************
# Parte III:Inferencia por muestreo
# *********************************

# -----------
# Ejercicio 4
# -----------

# Definir la función muestreo_con_rechazo(consulta, observado, red, N), que hace un cálculo
# aproximado de la probabilidad P(consulta | observado), respecto de una red bayesiana dada, usando
# el método de muestreo con rechazo. El número N indica el número de muestreos que ha de realizar.

# Ejemplos:

# >>> muestreo_con_rechazo('robo', {'juanllama': True, 'mariallama': True}, red_alarma, 100000)
# {False: 0.7076271186440678, True: 0.2923728813559322}
# Nota: la probabilidad exacta es <False: 0.71583, True: 0.28417>

# >>> muestreo_con_rechazo('fumador', {'infarto': True, 'deportista': False}, red_infarto, 100000)
# {False: 0.5157322159647875, True: 0.4842677840352125}
# Nota: La probabilidad exacta es <False: 0.52, True: 0.48>

# ============ Solución:

def muestreo_con_rechazo(consulta, observado, red, N):
    def muestra_compatible(muestra):
        return all(muestra[var] == observado[var] for var in observado)
    valores = red[0]
    frecs = collections.Counter({valor: 0 for valor in valores[consulta]})
    muestras = filter(muestra_compatible,
                      (muestreo_a_priori(red) for _ in range(N)))
    frecs.update(muestra[consulta] for muestra in muestras)
    return normaliza(frecs)


# Experimentar con distintas probabilidades cuya respuesta exacta se conozca, para comprobar la
# calidad de la aproximación que el algoritmo realiza. Usar varios valores de N para comprobar cómo
# un mayor número de muestreos mejora la aproximación.

# * Experimento 1:

# Con la red de la alarma, aproximando la probabilidad:

#                 P(robo | juanllama=True, mariallama=True)
#
# Sabemos que la probabilidad exacta es <False: 0.71583, True: 0.28417>

# Distintos resultados obtenidos aumentando N:

# >>> muestreo_con_rechazo('robo', {'juanllama': True, 'mariallama': True}, red_alarma, int(1e3))
# {False: 1.0, True: 0.0}
# >>> muestreo_con_rechazo('robo', {'juanllama': True, 'mariallama': True}, red_alarma, int(1e4))
# {False: 0.6666666666666666, True: 0.3333333333333333}
# >>> muestreo_con_rechazo('robo', {'juanllama': True, 'mariallama': True}, red_alarma, int(1e5))
# {False: 0.7359307359307359, True: 0.26406926406926406}
# >>> muestreo_con_rechazo('robo', {'juanllama': True, 'mariallama': True}, red_alarma, int(1e6))
# {False: 0.7050799623706491, True: 0.2949200376293509}

# * Experimento 2:

# Experimentamos con la red del infarto, aproximando la probabilidad:

#                 P(fumador | infarto=True, deportista=False)
#
# Sabemos que la probabilidad exacta es <False: 0.52, True: 0.48>

# Distintos resultados obtenidos aumentando N:

# >>> muestreo_con_rechazo('fumador', {'infarto': True, 'deportista': False}, red_infarto, int(1e3))
# {False: 0.5374280230326296, True: 0.46257197696737046}
# >>> muestreo_con_rechazo('fumador', {'infarto': True, 'deportista': False}, red_infarto, int(1e4))
# {False: 0.512791141657121, True: 0.48720885834287897}
# >>> muestreo_con_rechazo('fumador', {'infarto': True, 'deportista': False}, red_infarto, int(1e5))
# {False: 0.5176075912968465, True: 0.4823924087031535}
# >>> muestreo_con_rechazo('fumador', {'infarto': True, 'deportista': False}, red_infarto, int(1e6))
# {False: 0.5172103482747439, True: 0.4827896517252561}


# -----------
# Ejercicio 5
# -----------

# El principal problema del algoritmo de muestreo con rechazo es que se pueden generar muchas
# muestras que se rechazan, cuando éstas no sean compatibles con los valores de las variables
# observadas.

# Comprobar esto experimentalmente. Para ello, modificar la función muestreo_con_rechazo del
# ejercicio anterior, para que además de calcular la probabilidad aproximada, escriba por pantalla
# el total de muestras que se han rechazado.

# Ejemplo:

# >>> muestreo_con_rechazo_bis('robo', {'juanllama': True, 'mariallama': True}, red_alarma, int(1e4))
# Rechazadas 9973 muestras de un total de 10000
# {False: 0.7777777777777778, True: 0.2222222222222222}

# ============ Solución:

def muestreo_con_rechazo_bis(consulta, observado, red, N):
    rechazadas = 0

    def muestra_compatible(muestra):
        nonlocal rechazadas
        if all(muestra[var] == observado[var] for var in observado):
            return True
        else:
            rechazadas += 1
            return False
    valores = red[0]
    frecs = collections.Counter({valor: 0 for valor in valores[consulta]})
    muestras = filter(muestra_compatible,
                      (muestreo_a_priori(red) for _ in range(N)))
    frecs.update(muestra[consulta] for muestra in muestras)
    print('Rechazadas {} muestras de un total de {}'.format(rechazadas, N))
    return normaliza(frecs)

# Algunos ejemplos, en los que se muestra que se rechaza un gran porcentaje de muestras:

# >>> muestreo_con_rechazo_bis('robo', {'juanllama': True, 'mariallama': True}, red_alarma, int(1e2))
# Rechazadas 100 muestras de un total de 100
# ...
# ZeroDivisionError: division by zero
# >>> muestreo_con_rechazo_bis('robo', {'juanllama': True, 'mariallama': True}, red_alarma, int(1e3))
# Rechazadas 998 muestras de un total de 1000
# {False: 1.0, True: 0.0}
# >>> muestreo_con_rechazo_bis('robo', {'juanllama': True, 'mariallama': True}, red_alarma, int(1e4))
# Rechazadas 9974 muestras de un total de 10000
# {False: 0.6538461538461539, True: 0.34615384615384615}
# >>> muestreo_con_rechazo_bis('robo', {'juanllama': True, 'mariallama': True}, red_alarma, int(1e5))
# Rechazadas 99791 muestras de un total de 100000
# {False: 0.6889952153110048, True: 0.31100478468899523}


# -----------
# Ejercicio 6
# -----------

# Para paliar este problema del muestreo con rechazo, se introduce el algoritmo de ponderación por
# verosimilitud, tal y como se ha visto en la teoría. Se trata de generar directamente muestras
# compatibles con las observaciones, forzando a que en las variables observadas se tomen los
# valores observados. Como consecuencia, cada muestra se genera con un "peso", que equivale a la
# probabilidad de que hubiera ocurrido aleatoriamente aquello que se ha forzado.

# El algoritmo de ponderación por verosimilitud nos permite abordar inferencia aproximada para
# redes de mayor tamaño. En nuestro caso, lo probaremos con las siguiente red (traducción al
# castellano de la red "Car Starting Problem" del "applet" de redes bayesianas de AISpace):

red_arranque_coche = [{'Alternador OK': [True, False],
                       'Sistema de Carga OK': [True, False],
                       'Antigüedad Batería': ['nueva', 'vieja', 'muy_vieja'],
                       'Voltaje Batería': ['fuerte', 'débil', 'nada'],
                       'Fusible OK': [True, False],
                       'Distribuidor OK': [True, False],
                       'Voltaje en Conexión': ['fuerte', 'débil', 'nada'],
                       'Motor de Arranque OK': [True, False],
                       'Sistema de Arranque OK': [True, False],
                       'Faros': ['brillante', 'dim', 'apagado'],
                       'Bujías': ['okay', 'holgada', 'anulada'],
                       'Coche Maniobra': [True, False],
                       'Tiempo de Encendido': ['bien', 'mal', 'muy_mal'],
                       'Sistema Combustible OK': [True, False],
                       'Filtro de Aire Limpio': [True, False],
                       'Sistema de Aire OK': [True, False],
                       'Coche Arranca': [True, False],
                       'Calidad Bujías': ['bien', 'mal', 'muy_mal'],
                       'Bujías Adecuadas': [True, False]},

                      {'Alternador OK': [],
                       'Sistema de Carga OK': ['Alternador OK'],
                       'Antigüedad Batería': [],
                       'Voltaje Batería': ['Sistema de Carga OK', 'Antigüedad Batería'],
                       'Fusible OK': [],
                       'Distribuidor OK': [],
                       'Voltaje en Conexión': ['Voltaje Batería', 'Fusible OK', 'Distribuidor OK'],
                       'Motor de Arranque OK': [],
                       'Sistema de Arranque OK': ['Voltaje Batería', 'Fusible OK',
                                                  'Motor de Arranque OK'],
                       'Faros': ['Voltaje en Conexión'],
                       'Bujías': [],
                       'Coche Maniobra': ['Sistema de Arranque OK'],
                       'Tiempo de Encendido': ['Distribuidor OK'],
                       'Sistema Combustible OK': [],
                       'Filtro de Aire Limpio': [],
                       'Sistema de Aire OK': ['Filtro de Aire Limpio'],
                       'Coche Arranca': ['Coche Maniobra', 'Sistema Combustible OK',
                                         'Sistema de Aire OK', 'Bujías Adecuadas'],
                       'Calidad Bujías': ['Voltaje en Conexión', 'Bujías'],
                       'Bujías Adecuadas': ['Tiempo de Encendido', 'Calidad Bujías']},

                      {'Alternador OK': {(): [0.9997, 0.0003]},
                       'Sistema de Carga OK': {(True,): [0.995, 0.005],
                                               (False,):[0.0, 1.0]},
                       'Antigüedad Batería': {(): [0.4, 0.4, 0.2]},
                       'Voltaje Batería': {(True, 'nueva'): [0.999, 0.0008, 0.0002],
                                           (True, 'vieja'): [0.99, 0.008, 0.002],
                                           (True, 'muy_vieja'): [0.6, 0.3, 0.1],
                                           (False, 'nueva'): [0.8, 0.15, 0.05],
                                           (False, 'vieja'): [0.05, 0.3, 0.65],
                                           (False, 'muy_vieja'): [0.002, 0.1, 0.898]},
                       'Fusible OK': {(): [0.999, 0.001]},
                       'Distribuidor OK': {(): [0.99, 0.01]},
                       'Voltaje en Conexión': {('fuerte', True, True): [0.98, 0.015, 0.005],
                                               ('fuerte', True, False): [0.0, 0.0, 1.0],
                                               ('fuerte', False, True): [0.0, 0.0, 1.0],
                                               ('fuerte', False, False): [0.0, 0.0, 1.0],
                                               ('débil', True, True): [0.1, 0.8, 0.1],
                                               ('débil', True, False): [0.0, 0.0, 1.0],
                                               ('débil', False, True): [0.0, 0.0, 1.0],
                                               ('débil', False, False): [0.0, 0.0, 1.0],
                                               ('nada', True, True): [0.0, 0.0, 1.0],
                                               ('nada', True, False): [0.0, 0.0, 1.0],
                                               ('nada', False, True): [0.0, 0.0, 1.0],
                                               ('nada', False, False): [0.0, 0.0, 1.0]},
                       'Motor de Arranque OK': {(): [0.992, 0.008]},
                       'Sistema de Arranque OK': {('fuerte', True, True): [0.998, 0.002],
                                                  ('fuerte', True, False): [0.0, 1.0],
                                                  ('fuerte', False, True): [0.0, 1.0],
                                                  ('fuerte', False, False): [0.0, 1.0],
                                                  ('débil', True, True): [0.72, 0.28],
                                                  ('débil', True, False): [0.0, 1.0],
                                                  ('débil', False, True): [0.0, 1.0],
                                                  ('débil', False, False): [0.0, 1.0],
                                                  ('nada', True, True): [0.0, 1.0],
                                                  ('nada', True, False): [0.0, 1.0],
                                                  ('nada', False, True): [0.0, 1.0],
                                                  ('nada', False, False): [0.0, 1.0]},
                       'Faros': {('fuerte',): [0.98, 0.015, 0.005],
                                 ('débil',): [0.05, 0.9, 0.05],
                                 ('nada',): [0.0, 0.0, 1.0]},
                       'Bujías':{(): [0.99, 0.003, 0.007]},
                       'Coche Maniobra': {(True,): [0.98, 0.02],
                                          (False,): [0.0, 1.0]},
                       'Tiempo de Encendido': {(True,): [0.97, 0.02, 0.01],
                                               (False,): [0.2, 0.3, 0.5]},
                       'Sistema Combustible OK': {(): [0.9, 0.1]},
                       'Filtro de Aire Limpio': {(): [0.9, 0.1]},
                       'Sistema de Aire OK': {(True,): [0.9, 0.1],
                                              (False,): [0.3, 0.7]},
                       'Coche Arranca': {(True, True, True, True): [1.0, 0.0],
                                         (True, True, True, False): [0.0, 1.0],
                                         (True, True, False, True): [0.0, 1.0],
                                         (True, True, False, False): [0.0, 1.0],
                                         (True, False, True, True): [0.0, 1.0],
                                         (True, False, True, False): [0.0, 1.0],
                                         (True, False, False, True): [0.0, 1.0],
                                         (True, False, False, False): [0.0, 1.0],
                                         (False, True, True, True): [0.0, 1.0],
                                         (False, True, True, False): [0.0, 1.0],
                                         (False, True, False, True): [0.0, 1.0],
                                         (False, True, False, False): [0.0, 1.0],
                                         (False, False, True, True): [0.0, 1.0],
                                         (False, False, True, False): [0.0, 1.0],
                                         (False, False, False, True): [0.0, 1.0],
                                         (False, False, False, False): [0.0, 1.0]},
                       'Calidad Bujías':{('fuerte', 'okay'): [1.0, 0.0, 0.0],
                                         ('fuerte', 'holgada'): [0.0, 1.0, 0.0],
                                         ('fuerte', 'anulada'): [0.0, 0.0, 1.0],
                                         ('débil', 'okay'): [0.0, 1.0, 0.0],
                                         ('débil', 'holgada'): [0.0, 0.5, 0.5],
                                         ('débil', 'anulada'): [0.0, 0.2, 0.8],
                                         ('nada', 'okay'): [0.0, 0.0, 1.0],
                                         ('nada', 'holgada'): [0.0, 0.0, 1.0],
                                         ('nada', 'anulada'): [0.0, 0.0, 1.0]},
                       'Bujías Adecuadas': {('bien', 'bien'): [0.99, 0.01],
                                            ('bien', 'mal'): [0.5, 0.5],
                                            ('bien', 'muy_mal'): [0.1, 0.9],
                                            ('mal', 'bien'): [0.5, 0.5],
                                            ('mal', 'mal'): [0.05, 0.95],
                                            ('mal', 'muy_mal'): [0.01, 0.99],
                                            ('muy_mal', 'bien'): [0.1, 0.9],
                                            ('muy_mal', 'mal'): [0.01, 0.99],
                                            ('muy_mal', 'muy_mal'): [0.0, 1.0]}}]


# -----------
# Ejercicio 6
# -----------

# Definir una función ponderación_por_verosimilitud(consulta, observado, red, N) que implemente un
# cálculo aproximado de la probabilidad P(consulta | observado), respecto de una red bayesiana
# dada, usando el método de ponderación por verosimilitud. El número N indica el número de
# muestreos que ha de realizar.

# Ejemplos:

# >>> ponderación_por_verosimilitud('robo', {'juanllama': True, 'mariallama': True},
#                                   red_alarma, int(1e5))
# {False: 0.7074398233577173, True: 0.29256017664228273}
# Nota: la probabilidad exacta es <False: 0.71583; True: 0.28417>

# >>> ponderación_por_verosimilitud('Sistema Combustible OK',
#                                   {'Antigüedad Batería': 'vieja',
#                                    'Alternador OK': True,
#                                    'Filtro de Aire Limpio': False,
#                                    'Coche Arranca': False},
#                                   red_arranque_coche, int(1e3))
# {False: 0.15072083879423287, True: 0.8492791612057671}
# Nota: la probabilidad exacta (calculada en el applet AISpace) es <False: 0.13227; True: 0.86773>

# =========== Solución:

def muestreo_ponderado(red, observado):
    valores = red[0]
    padres = red[1]
    tablas = red[2]
    variables = orden_compatible(red)
    muestra = {}
    peso = 1
    for var in variables:
        padres_var = padres[var]
        valores_padres = tuple(muestra[vp] for vp in padres_var)
        valores_var = valores[var]
        distr_var = tablas[var][valores_padres]
        if var in observado:
            valor_observado = observado[var]
            muestra[var] = valor_observado
            prob_valor_observado = distr_var[valores_var.index(valor_observado)]
            peso *= prob_valor_observado
        else:
            muestra[var] = muestreo(valores_var, distr_var)
    return (muestra, peso)


def ponderación_por_verosimilitud(consulta, observado, red, N):
    valores = red[0]
    frecs = collections.Counter({valor: 0 for valor in valores[consulta]})
    for _ in range(N):
        muestra, peso = muestreo_ponderado(red, observado)
        frecs[muestra[consulta]] += peso
    return normaliza(frecs)

# Experimentos:
# ·············

# Experimentamos con el cálculo de la probabilidad
#    P(Sistema Combustible OK | Antigüedad Batería=vieja,
#                               Alternador OK=True,
#                               Filtro de Aire Limpio=False,
#                               Coche Arranca=False)
#
# Calculando con AISpace, esta probabilidad es exactamente: <False: 0.13227; True: 0.86773>


# Comparamos también con muestreo_con_rechazo, a igualdad de muestras:

# N=1000
# ------

# >>> muestreo_con_rechazo('Sistema Combustible OK', {'Antigüedad Batería': 'vieja', 'Alternador OK': True, 'Filtro de Aire Limpio': False, 'Coche Arranca': False}, red_arranque_coche, int(1e3))
# {False: 0.14814814814814814, True: 0.8518518518518519}
# >>> ponderación_por_verosimilitud('Sistema Combustible OK', {'Antigüedad Batería': 'vieja', 'Alternador OK': True, 'Filtro de Aire Limpio': False, 'Coche Arranca': False}, red_arranque_coche, int(1e3))
# {False: 0.13856209150326754, True: 0.8614379084967325}

# N=10000
# -------

# >>> muestreo_con_rechazo('Sistema Combustible OK', {'Antigüedad Batería': 'vieja', 'Alternador OK': True, 'Filtro de Aire Limpio': False, 'Coche Arranca': False}, red_arranque_coche, int(1e4))
# {False: 0.1342281879194631, True: 0.8657718120805369}
# >>> ponderación_por_verosimilitud('Sistema Combustible OK', {'Antigüedad Batería': 'vieja', 'Alternador OK': True, 'Filtro de Aire Limpio': False, 'Coche Arranca': False}, red_arranque_coche, int(1e4))
# {False: 0.13041738898521185, True: 0.8695826110147881}

# N=100000
# --------

# >>> muestreo_con_rechazo('Sistema Combustible OK', {'Antigüedad Batería': 'vieja', 'Alternador OK': True, 'Filtro de Aire Limpio': False, 'Coche Arranca': False}, red_arranque_coche, int(1e5))
# {False: 0.13303049967553537, True: 0.8669695003244646}
# >>> ponderación_por_verosimilitud('Sistema Combustible OK', {'Antigüedad Batería': 'vieja', 'Alternador OK': True, 'Filtro de Aire Limpio': False, 'Coche Arranca': False}, red_arranque_coche, int(1e5))
# {False: 0.13381092998927657, True: 0.8661890700107234}

# N=1000000
# ---------

# >>> muestreo_con_rechazo('Sistema Combustible OK', {'Antigüedad Batería': 'vieja', 'Alternador OK': True, 'Filtro de Aire Limpio': False, 'Coche Arranca': False}, red_arranque_coche, int(1e6))
# {False: 0.1364010130579219, True: 0.863598986942078}
# >>> ponderación_por_verosimilitud('Sistema Combustible OK', {'Antigüedad Batería': 'vieja', 'Alternador OK': True, 'Filtro de Aire Limpio': False, 'Coche Arranca': False}, red_arranque_coche, int(1e6))
# {False: 0.13260590279734755, True: 0.8673940972026525}


# Conclusión: ponderación_por_verosimilitud obtiene resultados aceptables con menos iteraciones que
# muestreo_con_rechazo
