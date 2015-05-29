import math
import random

# Esta práctica tiene dos partes:

# - En la primera parte vamos a implementar en Python el algoritmo de clustering
#   conocido como de K-medias

# - En la segunda parte experimentaremos la implementación sobre un conjunto de
#   datos: el conocido como «iris», una base de datos en la que cada instancia
#   refleja una serie de medidas sobre la flor del lirio, junto con una
#   clasificación de la especie a la que pertenece la flor.


# ***********************************
# Parte I: Implementación de K-medias
# ***********************************

# El algoritmo de K-medias es un algoritmo de clustering que sirve para
# clasificar en grupos o clusters una serie de ejemplos (vectores numéricos) que
# constituyen el conjunto de datos de entrada. Además del conjunto de datos,
# recibe como entrada el número K de clusters de la clasificación que se
# pretende hacer.

# Básicamente, comienza escogiendo K centros y asignando cada elemento a la
# clase representada por el centro más cercano. Una vez asignado un cluster a
# cada ejemplo, la media aritmética de los ejemplos de cada cluster se toma como
# nuevo centro del cluster. Este proceso de asignación de clusters y de
# recálculo de los centros se repite hasta que se cumple alguna condición de
# terminación (estabilización de los centros, por ejemplo).

# El pseudocódigo visto en clase es el siguiente:

# K-MEDIAS(K, DATOS)

# 1. Inicializar c_i (i=1, ..., K) (aleatoriamente o con algún criterio
#    heurístico)
# 2. REPETIR hasta que los c_i no cambien:
#    2.1 PARA j=1, ..., N HACER:
#        Calcular el cluster correspondiente a x_j, escogiendo, de entre
#        todos los c_i, el c_h tal que distancia(x_j, c_h) sea mínima
#    2.2 PARA i=1, ..., K HACER:
#        Asignar a c_i la media aritmética de los datos asignados al
#        cluster i-ésimo
# 3. Devolver c_1, ..., c_K


# Los siguientes ejercicios tienen como objetivo final la implementación en
# Python del algoritmo de K-medias. La función distancia será un parámetro de
# entrada al algoritmo.

# Además, en lugar de parar cuando se estabilizan los centros, haremos una
# versión más simple que realiza un número prefijado de iteraciones.

# Para hacer pruebas a medida que se van definiendo las funciones, usaremos el
# siguiente conjunto de datos, en el que aparecen datos sobre los pesos de una
# población (en forma de vector unidimensional). Es de suponer que estos datos
# corresponden a dos grupos (hombres y mujeres), y en principio desconocemos a
# qué grupo pertenece cada peso. La distancia entre los datos será simplemente
# su diferencia en valor absoluto.

pesos_poblacion = [[51.0], [43.0], [62.0], [64.0], [45.0], [42.0], [46.0],
                   [45.0], [45.0], [62.0], [47.0], [52.0], [64.0], [51.0],
                   [65.0], [48.0], [49.0], [46.0], [64.0], [51.0], [52.0],
                   [62.0], [49.0], [48.0], [62.0], [43.0], [40.0], [48.0],
                   [64.0], [51.0], [63.0], [43.0], [65.0], [66.0], [65.0],
                   [46.0], [39.0], [62.0], [64.0], [52.0], [63.0], [64.0],
                   [48.0], [64.0], [48.0], [51.0], [48.0], [64.0], [42.0],
                   [48.0], [41.0]]


def distancia_abs(x, y):
    return abs(x[0] - y[0])


# ---------------------------------------------------------------
# Ejercicio 1

# La asignación de clusters a cada ejemplo durante cada iteración del algoritmo
# la almacenaremos en una lista (que llamaremos "lista de clasificación") cuyos
# elementos son a su vez listas con dos elementos: cada dato concreto y el
# número de cluster que tiene asignado. Para comenzar, definir una función
# "clasificacion_inicial_vacia(datos)" que recibe un conjunto de datos y crea
# una lista de clasificación, en el que el número de cluster de cada dato está
# sin definir.
#
# Ejemplo:

# >>> clasificacion_inicial_vacia(pesos_poblacion)
# [[[51.0], None], [[43.0], None], [[62.0], None], [[64.0], None],
#  [[45.0], None], [[42.0], None], [[46.0], None], [[45.0], None],
#  [[45.0], None], [[62.0], None], [[47.0], None], [[52.0], None],
#  .......]

# ====== Solución:

def clasificacion_inicial_vacia(datos):
    return [[x, None] for x in datos]

# =======


# ---------------------------------------------------------------
# Ejercicio 2

# Los centros que se vayan calculando durante el algoritmo los vamos a almacenar
# en un lista de K componentes (a la que llamaremos "lista de centros").

# Para definir los centros iniciales, vamos a elegir aleatoriamente K ejemplos
# distintos de entre los datos de entrada. Se pide definir una función
# "centros_iniciales(ejemplos, num_clusters)" que recibiendo el conjunto de
# datos de entrada, y el número total de clusters, genera una lista inicial de
# centros.

# Por ejemplo (el resultado puede variar):
# >>> centros_iniciales(pesos_poblacion, 2)
# [[65.0], [48.0]]

# Sugerencia: usar la función random.sample

# ====== Solución:

def centros_iniciales(ejemplos, num_clusters):
    return random.sample(ejemplos, num_clusters)

# =======


# ---------------------------------------------------------------
# Ejercicio 3

# Definir una función "calcula_centro_mas_cercano(dato, centros,distancia)" que
# recibiendo como entrada un dato, una lista de centros de cada cluster y una
# función distancia, devuelve el número de cluster cuyo centro está más cercano
# al dato (los clusters los numeraremos de 0 a K-1).

# Por ejemplo:
# >>> calcula_centro_mas_cercano([41.0], [[39.0], [45.0]], distancia_abs)
# 0
# >>> calcula_centro_mas_cercano([64.0], [[39.0], [45.0]], distancia_abs)
# 1
# -----------------------------------------------------------------


# ======= Solución:

def calcula_centro_mas_cercano(dato, centros, distancia):
    distancias = [distancia(dato, centro) for centro in centros]
    minima_distancia = min(distancias)
    return distancias.index(minima_distancia)

# ================


# ---------------------------------------------------------------
# Ejercicio 4

# Define la función "asigna_cluster_a_cada_ejemplo(clasif, centros, distancia)"
# que recibiendo una lista de clasificación "clasif" y una lista de centros
# "centros", actualice clasif de manera que en cada dato, el cluster asignado
# sea el del centro en "centros" más cercano al ejemplo.

# Por ejemplo:

# >>> clas = clasificacion_inicial_vacia(pesos_poblacion)
# >>> centr = [[65.0], [48.0]]
# >>> asigna_cluster_a_cada_ejemplo(clas, centr, distancia_abs)
# >>> clas
# [[[51.0], 1], [[43.0], 1], [[62.0], 0], [[64.0], 0], [[45.0], 1],
#  [[42.0], 1], [[46.0], 1], [[45.0], 1], [[45.0], 1], [[62.0], 0],
#  [[47.0], 1], [[52.0], 1], [[64.0], 0], [[51.0], 1], [[65.0], 0],
#  ...]

# ====== Solución:

def asigna_cluster_a_cada_ejemplo(clasif, centros, distancia):
    for ejemplo in clasif:
        ejemplo[1] = calcula_centro_mas_cercano(ejemplo[0], centros, distancia)

# ===============


# ---------------------------------------------------------------
# Ejercicio 5

# Definir una función "recalcula_centros(clasif, num_clusters)" que recibiendo
# una lista de clasificación y el número total de clusters, devuelve la lista
# con los nuevos centros calculados como media aritmética de los datos de cada
# cluster.

# Por ejemplo (si "clas" con el valor del ejemplo anterior):
# >>> recalcula_centros(clas, 2)
# [[63.63157894736842], [46.8125]]

# ====== Solución:

def recalcula_centros(clasif, num_clusters):
    def media_ejemplos(ejemplos):
        num_ejemplos = len(ejemplos)
        tam_ejemplo = len(ejemplos[0])
        return [sum(ejemplo[i] for ejemplo in ejemplos) / num_ejemplos
                for i in range(tam_ejemplo)]
    return [media_ejemplos([ejemplo for ejemplo, cluster in clasif
                            if cluster == i])
            for i in range(num_clusters)]
# ================


# ------------------------------------------------------------------------------
# Ejercicio 6
# ------------------------------------------------------------------------------

# Usando las funciones definidas anteriormente, definir la función "k-medias(k,
# datos, distancia)" que implementa la siguiente versión del algoritmo k-medias:

# K-MEDIAS(K, DATOS, distancia)

# 1. Inicializar c_i (i=1, ..., K) (aleatoriamente o con algún criterio
#    heurístico)
# 2. REPETIR (hasta que los c_i no cambien):
#    2.1 PARA j=1, ..., N HACER:
#        Calcular el cluster correspondiente a x_j, escogiendo, de entre
#        todos los c_i, el c_h tal que distancia(x_j, c_h) sea mínima
#    2.2 PARA i=1, ..., K HACER:
#        Asignar a c_i la media aritmética de los datos asignados al
#        cluster i-ésimo
# 3. Devolver c_1,...,c_K y el cluster asignado a cada dato
# ---------------------------------------------------------------------


# El algoritmo debe devolver como salida una lista con los centros finalmente
# obtenidos y con la lista de clasificación.

# Por ejemplo:
# >>> k_medias(2, pesos_poblacion, distancia_abs)
# [[[46.8125], [63.63157894736842]],
#  [[[51.0], 0], [[43.0], 0], [[62.0], 1], [[64.0], 1], [[45.0], 0],
#   [[42.0], 0], [[46.0], 0], [[45.0], 0], [[45.0], 0], [[62.0], 1],
#   [[47.0], 0], [[52.0], 0], [[64.0], 1], [[51.0], 0], [[65.0], 1],
#   ....]]

# =========Solución:

def k_medias(k, datos, distancia):
    centros = centros_iniciales(datos, k)
    clasif = clasificacion_inicial_vacia(datos)
    while True:
        asigna_cluster_a_cada_ejemplo(clasif, centros, distancia)
        nuevos_centros = recalcula_centros(clasif, k)
        if nuevos_centros != centros:
            centros = nuevos_centros
        else:
            return [centros, clasif]

# ===============


# **************************************************
# Parte II: experimentación de k-medias sobre «iris»
# **************************************************

# La siguiente lista «iris» contiene uno de los conjuntos de datos más conocido
# y usado como banco de pruebas en aprendizaje automático. Se trata de una lista
# con 150 vectores de datos, cada uno de ellos con cuatro medidas numéricas
# sobre longitud y anchura de sépalo y pétalo de la flor del lirio. Cada vector
# tiene asignado una de las tres posibles clasificaciones: setosa, versicolor o
# virginica (que es la quinta componente).

iris = [[5.1, 3.5, 1.4, 0.2, "Iris setosa"],
        [4.9, 3.0, 1.4, 0.2, "Iris setosa"],
        [4.7, 3.2, 1.3, 0.2, "Iris setosa"],
        [4.6, 3.1, 1.5, 0.2, "Iris setosa"],
        [5.0, 3.6, 1.4, 0.2, "Iris setosa"],
        [5.4, 3.9, 1.7, 0.4, "Iris setosa"],
        [4.6, 3.4, 1.4, 0.3, "Iris setosa"],
        [5.0, 3.4, 1.5, 0.2, "Iris setosa"],
        [4.4, 2.9, 1.4, 0.2, "Iris setosa"],
        [4.9, 3.1, 1.5, 0.1, "Iris setosa"],
        [5.4, 3.7, 1.5, 0.2, "Iris setosa"],
        [4.8, 3.4, 1.6, 0.2, "Iris setosa"],
        [4.8, 3.0, 1.4, 0.1, "Iris setosa"],
        [4.3, 3.0, 1.1, 0.1, "Iris setosa"],
        [5.8, 4.0, 1.2, 0.2, "Iris setosa"],
        [5.7, 4.4, 1.5, 0.4, "Iris setosa"],
        [5.4, 3.9, 1.3, 0.4, "Iris setosa"],
        [5.1, 3.5, 1.4, 0.3, "Iris setosa"],
        [5.7, 3.8, 1.7, 0.3, "Iris setosa"],
        [5.1, 3.8, 1.5, 0.3, "Iris setosa"],
        [5.4, 3.4, 1.7, 0.2, "Iris setosa"],
        [5.1, 3.7, 1.5, 0.4, "Iris setosa"],
        [4.6, 3.6, 1.0, 0.2, "Iris setosa"],
        [5.1, 3.3, 1.7, 0.5, "Iris setosa"],
        [4.8, 3.4, 1.9, 0.2, "Iris setosa"],
        [5.0, 3.0, 1.6, 0.2, "Iris setosa"],
        [5.0, 3.4, 1.6, 0.4, "Iris setosa"],
        [5.2, 3.5, 1.5, 0.2, "Iris setosa"],
        [5.2, 3.4, 1.4, 0.2, "Iris setosa"],
        [4.7, 3.2, 1.6, 0.2, "Iris setosa"],
        [4.8, 3.1, 1.6, 0.2, "Iris setosa"],
        [5.4, 3.4, 1.5, 0.4, "Iris setosa"],
        [5.2, 4.1, 1.5, 0.1, "Iris setosa"],
        [5.5, 4.2, 1.4, 0.2, "Iris setosa"],
        [4.9, 3.1, 1.5, 0.1, "Iris setosa"],
        [5.0, 3.2, 1.2, 0.2, "Iris setosa"],
        [5.5, 3.5, 1.3, 0.2, "Iris setosa"],
        [4.9, 3.1, 1.5, 0.1, "Iris setosa"],
        [4.4, 3.0, 1.3, 0.2, "Iris setosa"],
        [5.1, 3.4, 1.5, 0.2, "Iris setosa"],
        [5.0, 3.5, 1.3, 0.3, "Iris setosa"],
        [4.5, 2.3, 1.3, 0.3, "Iris setosa"],
        [4.4, 3.2, 1.3, 0.2, "Iris setosa"],
        [5.0, 3.5, 1.6, 0.6, "Iris setosa"],
        [5.1, 3.8, 1.9, 0.4, "Iris setosa"],
        [4.8, 3.0, 1.4, 0.3, "Iris setosa"],
        [5.1, 3.8, 1.6, 0.2, "Iris setosa"],
        [4.6, 3.2, 1.4, 0.2, "Iris setosa"],
        [5.3, 3.7, 1.5, 0.2, "Iris setosa"],
        [5.0, 3.3, 1.4, 0.2, "Iris setosa"],
        [7.0, 3.2, 4.7, 1.4, "Iris versicolor"],
        [6.4, 3.2, 4.5, 1.5, "Iris versicolor"],
        [6.9, 3.1, 4.9, 1.5, "Iris versicolor"],
        [5.5, 2.3, 4.0, 1.3, "Iris versicolor"],
        [6.5, 2.8, 4.6, 1.5, "Iris versicolor"],
        [5.7, 2.8, 4.5, 1.3, "Iris versicolor"],
        [6.3, 3.3, 4.7, 1.6, "Iris versicolor"],
        [4.9, 2.4, 3.3, 1.0, "Iris versicolor"],
        [6.6, 2.9, 4.6, 1.3, "Iris versicolor"],
        [5.2, 2.7, 3.9, 1.4, "Iris versicolor"],
        [5.0, 2.0, 3.5, 1.0, "Iris versicolor"],
        [5.9, 3.0, 4.2, 1.5, "Iris versicolor"],
        [6.0, 2.2, 4.0, 1.0, "Iris versicolor"],
        [6.1, 2.9, 4.7, 1.4, "Iris versicolor"],
        [5.6, 2.9, 3.6, 1.3, "Iris versicolor"],
        [6.7, 3.1, 4.4, 1.4, "Iris versicolor"],
        [5.6, 3.0, 4.5, 1.5, "Iris versicolor"],
        [5.8, 2.7, 4.1, 1.0, "Iris versicolor"],
        [6.2, 2.2, 4.5, 1.5, "Iris versicolor"],
        [5.6, 2.5, 3.9, 1.1, "Iris versicolor"],
        [5.9, 3.2, 4.8, 1.8, "Iris versicolor"],
        [6.1, 2.8, 4.0, 1.3, "Iris versicolor"],
        [6.3, 2.5, 4.9, 1.5, "Iris versicolor"],
        [6.1, 2.8, 4.7, 1.2, "Iris versicolor"],
        [6.4, 2.9, 4.3, 1.3, "Iris versicolor"],
        [6.6, 3.0, 4.4, 1.4, "Iris versicolor"],
        [6.8, 2.8, 4.8, 1.4, "Iris versicolor"],
        [6.7, 3.0, 5.0, 1.7, "Iris versicolor"],
        [6.0, 2.9, 4.5, 1.5, "Iris versicolor"],
        [5.7, 2.6, 3.5, 1.0, "Iris versicolor"],
        [5.5, 2.4, 3.8, 1.1, "Iris versicolor"],
        [5.5, 2.4, 3.7, 1.0, "Iris versicolor"],
        [5.8, 2.7, 3.9, 1.2, "Iris versicolor"],
        [6.0, 2.7, 5.1, 1.6, "Iris versicolor"],
        [5.4, 3.0, 4.5, 1.5, "Iris versicolor"],
        [6.0, 3.4, 4.5, 1.6, "Iris versicolor"],
        [6.7, 3.1, 4.7, 1.5, "Iris versicolor"],
        [6.3, 2.3, 4.4, 1.3, "Iris versicolor"],
        [5.6, 3.0, 4.1, 1.3, "Iris versicolor"],
        [5.5, 2.5, 4.0, 1.3, "Iris versicolor"],
        [5.5, 2.6, 4.4, 1.2, "Iris versicolor"],
        [6.1, 3.0, 4.6, 1.4, "Iris versicolor"],
        [5.8, 2.6, 4.0, 1.2, "Iris versicolor"],
        [5.0, 2.3, 3.3, 1.0, "Iris versicolor"],
        [5.6, 2.7, 4.2, 1.3, "Iris versicolor"],
        [5.7, 3.0, 4.2, 1.2, "Iris versicolor"],
        [5.7, 2.9, 4.2, 1.3, "Iris versicolor"],
        [6.2, 2.9, 4.3, 1.3, "Iris versicolor"],
        [5.1, 2.5, 3.0, 1.1, "Iris versicolor"],
        [5.7, 2.8, 4.1, 1.3, "Iris versicolor"],
        [6.3, 3.3, 6.0, 2.5, "Iris virgínica"],
        [5.8, 2.7, 5.1, 1.9, "Iris virgínica"],
        [7.1, 3.0, 5.9, 2.1, "Iris virgínica"],
        [6.3, 2.9, 5.6, 1.8, "Iris virgínica"],
        [6.5, 3.0, 5.8, 2.2, "Iris virgínica"],
        [7.6, 3.0, 6.6, 2.1, "Iris virgínica"],
        [4.9, 2.5, 4.5, 1.7, "Iris virgínica"],
        [7.3, 2.9, 6.3, 1.8, "Iris virgínica"],
        [6.7, 2.5, 5.8, 1.8, "Iris virgínica"],
        [7.2, 3.6, 6.1, 2.5, "Iris virgínica"],
        [6.5, 3.2, 5.1, 2.0, "Iris virgínica"],
        [6.4, 2.7, 5.3, 1.9, "Iris virgínica"],
        [6.8, 3.0, 5.5, 2.1, "Iris virgínica"],
        [5.7, 2.5, 5.0, 2.0, "Iris virgínica"],
        [5.8, 2.8, 5.1, 2.4, "Iris virgínica"],
        [6.4, 3.2, 5.3, 2.3, "Iris virgínica"],
        [6.5, 3.0, 5.5, 1.8, "Iris virgínica"],
        [7.7, 3.8, 6.7, 2.2, "Iris virgínica"],
        [7.7, 2.6, 6.9, 2.3, "Iris virgínica"],
        [6.0, 2.2, 5.0, 1.5, "Iris virgínica"],
        [6.9, 3.2, 5.7, 2.3, "Iris virgínica"],
        [5.6, 2.8, 4.9, 2.0, "Iris virgínica"],
        [7.7, 2.8, 6.7, 2.0, "Iris virgínica"],
        [6.3, 2.7, 4.9, 1.8, "Iris virgínica"],
        [6.7, 3.3, 5.7, 2.1, "Iris virgínica"],
        [7.2, 3.2, 6.0, 1.8, "Iris virgínica"],
        [6.2, 2.8, 4.8, 1.8, "Iris virgínica"],
        [6.1, 3.0, 4.9, 1.8, "Iris virgínica"],
        [6.4, 2.8, 5.6, 2.1, "Iris virgínica"],
        [7.2, 3.0, 5.8, 1.6, "Iris virgínica"],
        [7.4, 2.8, 6.1, 1.9, "Iris virgínica"],
        [7.9, 3.8, 6.4, 2.0, "Iris virgínica"],
        [6.4, 2.8, 5.6, 2.2, "Iris virgínica"],
        [6.3, 2.8, 5.1, 1.5, "Iris virgínica"],
        [6.1, 2.6, 5.6, 1.4, "Iris virgínica"],
        [7.7, 3.0, 6.1, 2.3, "Iris virgínica"],
        [6.3, 3.4, 5.6, 2.4, "Iris virgínica"],
        [6.4, 3.1, 5.5, 1.8, "Iris virgínica"],
        [6.0, 3.0, 4.8, 1.8, "Iris virgínica"],
        [6.9, 3.1, 5.4, 2.1, "Iris virgínica"],
        [6.7, 3.1, 5.6, 2.4, "Iris virgínica"],
        [6.9, 3.1, 5.1, 2.3, "Iris virgínica"],
        [5.8, 2.7, 5.1, 1.9, "Iris virgínica"],
        [6.8, 3.2, 5.9, 2.3, "Iris virgínica"],
        [6.7, 3.3, 5.7, 2.5, "Iris virgínica"],
        [6.7, 3.0, 5.2, 2.3, "Iris virgínica"],
        [6.3, 2.5, 5.0, 1.9, "Iris virgínica"],
        [6.5, 3.0, 5.2, 2.0, "Iris virgínica"],
        [6.2, 3.4, 5.4, 2.3, "Iris virgínica"],
        [5.9, 3.0, 5.1, 1.8, "Iris virgínica"]]

# ---------------------------------------------------------------
# Ejercicio 7

# La siguiente función nos permite validar una clasificación cualquiera de los
# 150 vectores numéricos de la lista iris, comparándola con la clasificación
# original que aparece en la base de datos. Para cada una de las tres
# clasificaciones originales, cuenta cuántos ejemplos hay en cada uno de los
# clusters asignados en la clasificación que se le pasa como argumento de
# entrada.


def validacion_iris(clasificacion):
    posibles_valores = ["Iris setosa", "Iris versicolor", "Iris virgínica"]
    contadores = dict()
    for val in posibles_valores:
        for x in range(3):
            contadores[val, x] = 0
    for i in range(len(clasificacion)):
        contadores[iris[i][4], clasificacion[i][1]] += 1
    for val in posibles_valores:
        print(val + "\n" + "==============\n")
        for x in range(3):
            print("Cluster ", x, ": ", contadores[val, x])
        print("\n\n")

# Se pide:
# - Obtener, a partir de los datos de iris la lista de vectores
#   numéricos, SIN el tipo de iris.
# - Aplicar el algoritmo de k-medias a esos datos (con la distancia euclídea)
# - Validar la clasificación obtenida respecto de la clasificación
#   original

# ======== Solución:


def distancia_euclidea(v, w):
    return math.sqrt(sum((vi - wi) ** 2 for vi, wi in zip(v, w)))


# Sesión:

# >>> iris_sin_clasificar = [x[:-1] for x in iris]
# >>> iris_k_medias = k_medias(3, iris_sin_clasificar, distancia_euclidea)[1]
# >>> validacion_iris(iris_k_medias)
# Iris setosa
# ==============

# Cluster  0 :  50
# Cluster  1 :  0
# Cluster  2 :  0



# Iris versicolor
# ==============

# Cluster  0 :  0
# Cluster  1 :  48
# Cluster  2 :  2



# Iris virgínica
# ==============

# Cluster  0 :  0
# Cluster  1 :  14
# Cluster  2 :  36





# Comentarios: como se observa, el cluster 0 ha sido reconocido completamente
# como el cluster original de iris setosa. El cluster 1 casi al completo
# (excepto 2 ejemplos del 2) ha reconocido a iris versicolor. Sin embargo ha
# incluido también 14 ejemplos de iris virginica. El resto de iris virginica se
# ha asignado al cluster 2.

# Los resultados son bastante aceptables, aunque el algoritmo EM los mejora un
# poco.
