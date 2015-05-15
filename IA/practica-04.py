# practica-03.py
# Inteligencia Artificial 
# Universidad de Sevilla.

# Práctica 4: Inferencia en redes bayesianas usando muestreo
# ==========================================================

# Necesitamos el módulo random de la biblioteca estándar:

import random

# En esta práctica vamos a implementar métodos de inferencia probabilística en
# redes bayesianas, usando técnicas de muestreo. 


# ***************************************************************
# Parte I: Estructura de datos para representar redes bayesianas. 
# ****************************************************************

# Vamos a usar una estructura de datos prefijada, para representar redes
# bayesianas. Por ejemplo, la siguiente variable red_alarma contiene la
# representación de la red bayesiana del ejemplo de la alarma visto en clase:

red_alarma=[{"robo":[True,False],
             "terremoto":[True,False],
             "alarma":[True,False],
             "juanllama":[True,False],
             "mariallama":[True,False]},
             
             {"robo":[],
              "terremoto":[],
              "alarma":["robo","terremoto"],
              "juanllama":["alarma"],
              "mariallama":["alarma"]},
              
             {"robo":{():[0.001,0.999]},
              "terremoto":{():[0.002,0.998]},
              "alarma":{(True,True):[0.95,0.05],
                        (True,False):[0.94,0.06],
                        (False,True):[0.29,0.71],
                        (False,False):[0.001,0.999]},
              "juanllama":{(True,):[0.9,0.1],
                           (False,):[0.05,0.95]},
              "mariallama":{(True,):[0.7,0.3],
                            (False,):[0.01,0.99]}}]


# En general, una red bayesiana se representará mediante una lista de tres
# elementos. Cada uno de estos elementos representará:

# 1. Las variables aleatorias y sus posibles valores: un diccionario que asocia
#    que asocia cada nombre de variable con una lista de sus posible valores. 
# 2. Los padres de cada variable en la red: un diccionario que asocia a cada
#    nombre de variable con una lista de sus padres. 
# 3. Las tablas de probabilidad de cada nodo: un diccionario que asocia a cada
#    nombre de variable su tabla de probabilidad. A su vez, la tabla asociada
#    a cada variable X es un diccionario que asocia a cada combinación de
#    valores de los padres, la distribución de probabilidad de X dada esa
#    combinación de valores. 
#
#    Por ejemplo, si en la tabla de "alarma" hay una correspondencia  
#    (True,False):[0.94,0.06], 
#    quiere decir que:
#    P(alarma=True|Robo=True,Terremoto=False)=0.94, y que     
#    P(alarma=False|Robo=True,Terremoto=False)=0.06.
#
#    Nótese que el orden implícito de los valores de una variable, y de
#    sus padres, es el que está definido en los correspondientes
#    diccionarios. 

# Lo que sigue son otras dos redes que también se han mostrado en clase de
# teoría: 

red_infarto=[{"deportista":[True,False],
              "alimentación_equilibrada":[True,False],
              "hipertenso":[True,False],
              "fumador":[True,False],
              "infarto":[True,False]},
              
              {"deportista":[],
               "alimentación_equilibrada":[],
               "hipertenso":["deportista","alimentación_equilibrada"],
               "fumador":[],
               "infarto":["hipertenso","fumador"]},
               
               {"deportista":{():[0.1,0.9]},
                "alimentación_equilibrada":{():[0.4,0.6]},
                "hipertenso":{(True,True):[0.01,0.99],
                              (True,False):[0.25,0.75],
                              (False,True):[0.2,0.8],
                              (False,False):[0.7,0.3]},
                "fumador":{():[0.4,0.6]},
                "infarto":{(True,True):[0.8,0.2],
                           (True,False):[0.7,0.3],
                           (False,True):[0.6,0.4],
                           (False,False):[0.3,0.7]}}]

red_aspersor=[{"hierba mojada":[True,False],
               "lluvia":[True,False],
               "nublado":[True,False],
               "aspersor":[True,False]},

               {"nublado":[],
               "aspersor":["nublado"],
               "lluvia":["nublado"],
               "hierba mojada":["aspersor","lluvia"]},

               {"nublado":{():[0.5,0.5]},
                "aspersor":{(True,):[0.1,0.9],
                            (False,):[0.5,0.5]},
                "lluvia":{(True,):[0.8,0.2],
                          (False,):[0.2,0.8]},
                "hierba mojada":{(True,True):[0.99,0.01],
                                 (True,False):[0.9,0.1],
                                 (False,True):[0.9,0.1],
                                 (False,False):[0.0,1.0]}}]
                            
# ******************************
# Parte II: Funciones auxiliares
# ******************************



# -----------
# Ejercicio 1
# -----------

# Definir una función "orden_compatible(red)", que recibiendo una red
# bayesiana, devuelva una ordenación topológica del grafo de la red. Es decir,
# una secuencia (una lista) de todas las variables de la red, cumpliendo que
# para toda variable X que sea padre de otra variable Y en la red, X va antes
# que Y en la secuencia. 

# Ejemplos (hay otras posibilidades):

# >>> orden_compatible(red_alarma)
# ['robo', 'terremoto', 'alarma', 'juanllama', 'mariallama']
# >>> orden_compatible(red_infarto)
# ['deportista', 'fumador', 'alimentación_equilibrada', 'hipertenso', 'infarto']
# >>> orden_compatible(red_aspersor)
# ['nublado', 'aspersor', 'lluvia', 'hierba mojada']


# -----------
# Ejercicio 2
# -----------

# Definir una función "muestreo(valores,distr)" que recibiendo como entrada
# una lista de n valores de una variable aleatoria y una distribución de
# probabilidad (una lista de n probabilidades), devuelve aleatoriamente uno de
# los valores de la lista. La probabilidad de generar cada uno de los valores
# debe ser la correspondiente probabilidad en la distribución. 

# Ejemplos (téngase en cuenta que son valores aleatorios, por lo que los
# resultados no siempre son éstos):

# >>> muestreo(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v2'
# >>> muestreo(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v1'
# >>> muestreo(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v2'
# >>> muestreo(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v2'
# >>> muestreo(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v2'
# >>> muestreo(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v3'
# >>> muestreo(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v2'


# Una vez definida la función, comprobar con un número grande de muestreos
# que efectivamente son sucesos aleatorios con la probabilidad pretendida. 

# -----------
# Ejercicio 3
# -----------

# Definir la función "muestreo_a_priori(red)", que obtiene un evento aleatorio
# completo, siguiendo la distribución que define una red bayesiana que recibe
# como entrada (transparencias 95-97 del Tema 7 de teoría)

# Ejemplos (téngase en cuenta que son resultados aleatorios):

# >>> muestreo_a_priori(red_alarma)
# {'juanllama': False, 'terremoto': False, 'robo': False, 'alarma': False, 'mariallama': False}
# >>> muestreo_a_priori(red_alarma)
# {'juanllama': False, 'terremoto': False, 'robo': False, 'alarma': False, 'mariallama': False}
# >>> muestreo_a_priori(red_aspersor)
# {'nublado': True, 'lluvia': True, 'hierba mojada': False, 'aspersor': False}
# >>> muestreo_a_priori(red_aspersor)
# {'nublado': False, 'lluvia': False, 'hierba mojada': False, 'aspersor': False}
# >>> muestreo_a_priori(red_infarto)
# {'alimentación_equilibrada': False, 'fumador': True, 'infarto': True, 
#  'hipertenso': True, 'deportista': False}
# >>> muestreo_a_priori(red_infarto)
# {'alimentación_equilibrada': False, 'fumador': True, 'infarto': True, 
#  'hipertenso': False, 'deportista': False}

# Función de normalización:
# -------------------------

# La siguiente función "normaliza(d)" normaliza una distribución de
# probabilidades, que viene dada mediante un diccionario d:

def normaliza(d):
    suma=sum(d.values())
    return {var:d[var]/suma for var in d}

# Ejemplos:

# >>> normaliza({"v1":0.21,"v2":0.11,"v3":0.37})
# {'v1': 0.30434782608695654, 'v2': 0.15942028985507248, 'v3': 0.5362318840579711}
# >>> normaliza({True:0.012,False:0.008})
# {False: 0.4, True: 0.6}




# *********************************
# Parte III:Inferencia por muestreo
# *********************************


# -----------
# Ejercicio 4
# -----------

# Definir la función "muestreo_con_rechazo(var,observado,red,N)", que hace un
# cálculo aproximado de la probabilidad P(var|observado), respecto de una red
# bayesiana dada, usando el método de muestreo con rechazo (transparencias
# 98-99 del tema 7). El número N indica el número de muestreos que ha de
# realizar.


# Experimentar con distintas probabilidades cuya respuesta exacta se conozca,
# para comprobar la calidad de la aproximación que el algoritmo realiza. Usar
# varios valores de N para comprobar cómo un mayor número de muestreos mejora
# la aproximación. 

# Ejemplos:

# >>> muestreo_con_rechazo("robo",{"juanllama":True,"mariallama":True},red_alarma,100000)
# {False: 0.6730769230769231, True: 0.3269230769230769}

# 
# Nota: la probabilidad exacta es <False:0.71583,True:0.28417> (ver transparencias)

# >>> muestreo_con_rechazo("fumador",{"infarto":True,"deportista":False},red_infarto,100000)
# {False: 0.5159282173461938, True: 0.48407178265380624}
#
# Nota: La probabilidad exacta es <False:0.52,True:0.48> (ver transparencias)
# 

# -----------
# Ejercicio 5
# -----------

# El principal problema del algoritmo de muestreo con rechazo es que se pueden
# generar muchas muestras que se rechazan, cuando éstas no sean compatibles
# con los valores de las variables observadas.

# Comprobar esto experimentalmente. Para ello, modificar la función
# muestreo_con_rechazo del ejercicio anterior, para que además de calcular la
# probabilidad aproximada, escriba por pantalla el total de muestras que se
# han rechazado.

# Ejemplo:

# >>> muestreo_con_rechazo_bis("robo",{"juanllama":True,"mariallama":True},red_alarma,10000)
# Rechazadas 9981 muestras de un total de 10000
# {False: 0.5263157894736842, True: 0.47368421052631576}

# -----------
# Ejercicio 6
# -----------

# Para paliar este problema del muestreo con rechazo, se introduce el
# algoritmo de ponderación por verosimilitud, tal y como se ha visto en la
# teoría. Se trata de generar directamente muestras compatibles con las
# observaciones, forzando a que en las variables observadas se tomen los
# valores observados. Como consecuencia, cada muestra se genera con un "peso",
# que equivale a la probabilidad de que hubiera ocurrido aleatoriamente
# aquello que se ha forzado.

# El algoritmo de ponderación por verosimilitud nos permite abordar inferencia
# aproximada para redes de mayor tamaño. En nuestro caso, lo probaremos con
# las siguiente red, traducción al castellano de la red "Car Starting Problem"
# del "applet" de redes bayesianas de AISpace):

red_arranque_coche=[{"Alternador OK":[True,False],
                     "Sistema de Carga OK":[True,False],	
                     "Antigüedad Batería":["nueva", "vieja", "muy_vieja"],	
                     "Voltaje Batería":["fuerte", "débil", "nada"],	
                     "Fusible OK":[True,False],
                     "Distribuidor OK":[True,False],
                     "Voltaje en Conexión":["fuerte", "débil", "nada"],
                     "Motor de Arranque OK":[True,False],
                     "Sistema de Arranque OK":[True,False],
                     "Faros":["brillante", "dim", "apagado"],
                     "Bujías":["okay", "holgada", "anulada"],
                     "Coche Maniobra":[True,False],
                     "Tiempo de Encendido":["bien", "mal", "muy_mal"],
                     "Sistema Combustible OK":[True,False],
                     "Filtro de Aire Limpio":[True,False],
                     "Sistema de Aire OK":[True,False],
                     "Coche Arranca":[True,False],
                     "Calidad Bujías":["bien", "mal", "muy_mal"],
                     "Bujías Adecuadas":[True,False]},
                     
			   {"Alternador OK":[],
			   "Sistema de Carga OK":["Alternador OK"],	
             		   "Antigüedad Batería":[],	
             		   "Voltaje Batería":["Sistema de Carga OK", "Antigüedad Batería"],	
             		   "Fusible OK":[],
             		   "Distribuidor OK":[],
             		   "Voltaje en Conexión":["Voltaje Batería", "Fusible OK", "Distribuidor OK"],
             		   "Motor de Arranque OK":[],
             		   "Sistema de Arranque OK":["Voltaje Batería", "Fusible OK", "Motor de Arranque OK"],
             		   "Faros":["Voltaje en Conexión"],
             		   "Bujías":[],
             		   "Coche Maniobra":["Sistema de Arranque OK"],
             		   "Tiempo de Encendido":["Distribuidor OK"],
             		   "Sistema Combustible OK":[],
             		   "Filtro de Aire Limpio":[],
             		   "Sistema de Aire OK":["Filtro de Aire Limpio"],
             		   "Coche Arranca":["Coche Maniobra", "Sistema Combustible OK", 
                                        "Sistema de Aire OK", "Bujías Adecuadas"],
             		   "Calidad Bujías":["Voltaje en Conexión", "Bujías"],
             		   "Bujías Adecuadas":["Tiempo de Encendido", "Calidad Bujías"]},


			   {"Alternador OK":{():[0.9997,0.0003]},
			   "Sistema de Carga OK":{(True,):[0.995, 0.005],
                                      (False,):[0.0, 1.0]},	
             		   "Antigüedad Batería":{():[0.4, 0.4, 0.2]},	
             		   "Voltaje Batería":{(True,"nueva"):[0.999, 0.0008, 0.0002],
                                          (True,"vieja"):[0.99, 0.008, 0.002],
                                          (True,"muy_vieja"):[0.6, 0.3, 0.1],		      
                                          (False,"nueva"):[0.8, 0.15, 0.05],
                                          (False,"vieja"):[0.05, 0.3, 0.65],
                                          (False,"muy_vieja"):[0.002, 0.1, 0.898]},	
             		   "Fusible OK":{():[0.999, 0.001]}, 
             		   "Distribuidor OK":{():[0.99, 0.01]},
             		   "Voltaje en Conexión":{("fuerte", True, True):[0.98, 0.015, 0.005],
                                              ("fuerte", True, False):[0.0, 0.0, 1.0],
                                              ("fuerte", False, True):[0.0, 0.0, 1.0],
                                              ("fuerte", False, False):[0.0, 0.0, 1.0],
                                              ("débil", True, True):[0.1, 0.8, 0.1],
                                              ("débil", True, False):[0.0, 0.0, 1.0],
                                              ("débil", False, True):[0.0, 0.0, 1.0],
                                              ("débil", False, False):[0.0, 0.0, 1.0],
                                              ("nada", True, True):[0.0, 0.0, 1.0],
                                              ("nada", True, False):[0.0, 0.0, 1.0],
                                              ("nada", False, True):[0.0, 0.0, 1.0],
                                              ("nada", False, False):[0.0, 0.0, 1.0]},
             		   "Motor de Arranque OK":{():[0.992, 0.008]},
             		   "Sistema de Arranque OK":{("fuerte", True, True):[ 0.998, 0.002],
                                                 ("fuerte", True, False):[ 0.0, 1.0],
                                                 ("fuerte", False, True):[ 0.0, 1.0],
                                                 ("fuerte", False, False):[ 0.0, 1.0],
                                                 ("débil", True, True):[ 0.72, 0.28],
                                                 ("débil", True, False):[ 0.0, 1.0],
                                                 ("débil", False, True):[ 0.0, 1.0],
                                                 ("débil", False, False):[ 0.0, 1.0],
                                                 ("nada", True, True):[ 0.0, 1.0],
                                                 ("nada", True, False):[ 0.0, 1.0],
                                                 ("nada", False, True):[ 0.0, 1.0],
                                                 ("nada", False, False):[ 0.0, 1.0]},
             		   "Faros":{("fuerte",):[0.98, 0.015, 0.005],
                                ("débil",):[0.05, 0.9, 0.05],
                                ("nada",):[0.0, 0.0, 1.0]},
             		   "Bujías":{():[0.99, 0.003, 0.007]},
             		   "Coche Maniobra":{(True,):[0.98, 0.02],
                                         (False,):[0.0, 1.0]},
             		   "Tiempo de Encendido":{(True,):[0.97, 0.02, 0.01],
                                              (False,):[0.2, 0.3, 0.5]},
             		   "Sistema Combustible OK":{():[0.9, 0.1]},
             		   "Filtro de Aire Limpio":{():[0.9, 0.1]},
             		   "Sistema de Aire OK":{(True,):[0.9, 0.1],
                                             (False,):[0.3, 0.7]},
             		   "Coche Arranca":{  (True, True, True, True):[ 1.0, 0.0],
                                          (True, True, True, False):[ 0.0, 1.0],
                                          (True, True, False, True):[ 0.0, 1.0],
                                          (True, True, False, False):[ 0.0, 1.0],
                                          (True, False, True, True):[ 0.0, 1.0],
                                          (True, False, True, False):[ 0.0, 1.0],
                                          (True, False, False, True):[ 0.0, 1.0],
                                          (True, False, False, False):[ 0.0, 1.0],
                                          (False, True, True, True):[ 0.0, 1.0],
                                          (False, True, True, False):[ 0.0, 1.0],
                                          (False, True, False, True):[ 0.0, 1.0],
                                          (False, True, False, False):[ 0.0, 1.0],
                                          (False, False, True, True):[ 0.0, 1.0],
                                          (False, False, True, False):[ 0.0, 1.0],
                                          (False, False, False, True):[ 0.0, 1.0],
                                          (False, False, False, False):[ 0.0, 1.0]},
             		   "Calidad Bujías":{("fuerte", "okay"):[ 1.0, 0.0, 0.0],
                                         ("fuerte", "holgada"):[ 0.0, 1.0, 0.0],
                                         ("fuerte", "anulada"):[ 0.0, 0.0, 1.0],
                                         ("débil", "okay"):[ 0.0, 1.0, 0.0],
                                         ("débil", "holgada"):[ 0.0, 0.5, 0.5],
                                         ("débil", "anulada"):[ 0.0, 0.2, 0.8],
                                         ("nada", "okay"):[ 0.0, 0.0, 1.0],
                                         ("nada", "holgada"):[ 0.0, 0.0, 1.0],
                                         ("nada", "anulada"):[ 0.0, 0.0, 1.0]},
             		   "Bujías Adecuadas":{("bien", "bien"):[ 0.99, 0.01],
                                           ("bien", "mal"):[ 0.5, 0.5],
                                           ("bien", "muy_mal"):[ 0.1, 0.9],
                                           ("mal", "bien"):[ 0.5, 0.5],
                                           ("mal", "mal"):[ 0.05, 0.95],
                                           ("mal", "muy_mal"):[ 0.01, 0.99],
                                           ("muy_mal", "bien"):[ 0.1, 0.9],
                                           ("muy_mal", "mal"):[ 0.01, 0.99],
                                           ("muy_mal", "muy_mal"):[ 0.0, 1.0]}}]



# Definir una función "ponderacion_por_verosimilitud(var,observado,red,N)" que
# implemente un cálculo aproximado de la probabilidad P(var|observado),
# respecto de una red bayesiana dada, usando el método de ponderación por
# verosimilitus (transparencias 100-103 del tema 7). El número N indica el
# número de muestreos que ha de realizar.

# Ejemplos:

# >>> ponderacion_por_verosimilitud("robo",{"juanllama":True,"mariallama":True},red_alarma,100000)
# {False: 0.7143990444003082, True: 0.2856009555996919}
# 
# Nota: la probabilidad exacta es <False:0.71583,True:0.28417>

# >>> ponderacion_por_verosimilitud("Sistema Combustible OK",
#                                   {"Antigüedad Batería":"vieja",
#                                    "Alternador OK":True, 
#                                    "Filtro de Aire Limpio":False,
#                                    "Coche Arranca":False},
#                                   red_arranque_coche,1000)
# {False: 0.11749347258485594, True: 0.8825065274151441}
#
# Nota: la probabilidda exacta (calculada en el applet AISpace) 
#       es <False:0.13227,True:0.86773>
