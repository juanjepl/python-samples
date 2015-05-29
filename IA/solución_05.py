import math
import random

# Esta pr�ctica tiene dos partes:

# - En la primera parte vamos a implementar en Python el algoritmo de clustering
#   conocido como de K-medias

# - En la segunda parte experimentaremos la implementaci�n sobre un conjunto de
#   datos: el conocido como �iris�, una base de datos en la que cada instancia
#   refleja una serie de medidas sobre la flor del lirio, junto con una
#   clasificaci�n de la especie a la que pertenece la flor.


# ***********************************
# Parte I: Implementaci�n de K-medias
# ***********************************

# El algoritmo de K-medias es un algoritmo de clustering que sirve para
# clasificar en grupos o clusters una serie de ejemplos (vectores num�ricos) que
# constituyen el conjunto de datos de entrada. Adem�s del conjunto de datos,
# recibe como entrada el n�mero K de clusters de la clasificaci�n que se
# pretende hacer.

# B�sicamente, comienza escogiendo K centros y asignando cada elemento a la
# clase representada por el centro m�s cercano. Una vez asignado un cluster a
# cada ejemplo, la media aritm�tica de los ejemplos de cada cluster se toma como
# nuevo centro del cluster. Este proceso de asignaci�n de clusters y de
# rec�lculo de los centros se repite hasta que se cumple alguna condici�n de
# terminaci�n (estabilizaci�n de los centros, por ejemplo).

# El pseudoc�digo visto en clase es el siguiente:

# K-MEDIAS(K, DATOS)

# 1. Inicializar c_i (i=1, ..., K) (aleatoriamente o con alg�n criterio
#    heur�stico)
# 2. REPETIR hasta que los c_i no cambien:
#    2.1 PARA j=1, ..., N HACER:
#        Calcular el cluster correspondiente a x_j, escogiendo, de entre
#        todos los c_i, el c_h tal que distancia(x_j, c_h) sea m�nima
#    2.2 PARA i=1, ..., K HACER:
#        Asignar a c_i la media aritm�tica de los datos asignados al
#        cluster i-�simo
# 3. Devolver c_1, ..., c_K


# Los siguientes ejercicios tienen como objetivo final la implementaci�n en
# Python del algoritmo de K-medias. La funci�n distancia ser� un par�metro de
# entrada al algoritmo.

# Adem�s, en lugar de parar cuando se estabilizan los centros, haremos una
# versi�n m�s simple que realiza un n�mero prefijado de iteraciones.

# Para hacer pruebas a medida que se van definiendo las funciones, usaremos el
# siguiente conjunto de datos, en el que aparecen datos sobre los pesos de una
# poblaci�n (en forma de vector unidimensional). Es de suponer que estos datos
# corresponden a dos grupos (hombres y mujeres), y en principio desconocemos a
# qu� grupo pertenece cada peso. La distancia entre los datos ser� simplemente
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

# La asignaci�n de clusters a cada ejemplo durante cada iteraci�n del algoritmo
# la almacenaremos en una lista (que llamaremos "lista de clasificaci�n") cuyos
# elementos son a su vez listas con dos elementos: cada dato concreto y el
# n�mero de cluster que tiene asignado. Para comenzar, definir una funci�n
# "clasificacion_inicial_vacia(datos)" que recibe un conjunto de datos y crea
# una lista de clasificaci�n, en el que el n�mero de cluster de cada dato est�
# sin definir.
#
# Ejemplo:

# >>> clasificacion_inicial_vacia(pesos_poblacion)
# [[[51.0], None], [[43.0], None], [[62.0], None], [[64.0], None],
#  [[45.0], None], [[42.0], None], [[46.0], None], [[45.0], None],
#  [[45.0], None], [[62.0], None], [[47.0], None], [[52.0], None],
#  .......]

# ====== Soluci�n:

def clasificacion_inicial_vacia(datos):
    return [[x, None] for x in datos]

# =======


# ---------------------------------------------------------------
# Ejercicio 2

# Los centros que se vayan calculando durante el algoritmo los vamos a almacenar
# en un lista de K componentes (a la que llamaremos "lista de centros").

# Para definir los centros iniciales, vamos a elegir aleatoriamente K ejemplos
# distintos de entre los datos de entrada. Se pide definir una funci�n
# "centros_iniciales(ejemplos, num_clusters)" que recibiendo el conjunto de
# datos de entrada, y el n�mero total de clusters, genera una lista inicial de
# centros.

# Por ejemplo (el resultado puede variar):
# >>> centros_iniciales(pesos_poblacion, 2)
# [[65.0], [48.0]]

# Sugerencia: usar la funci�n random.sample

# ====== Soluci�n:

def centros_iniciales(ejemplos, num_clusters):
    return random.sample(ejemplos, num_clusters)

# =======


# ---------------------------------------------------------------
# Ejercicio 3

# Definir una funci�n "calcula_centro_mas_cercano(dato, centros,distancia)" que
# recibiendo como entrada un dato, una lista de centros de cada cluster y una
# funci�n distancia, devuelve el n�mero de cluster cuyo centro est� m�s cercano
# al dato (los clusters los numeraremos de 0 a K-1).

# Por ejemplo:
# >>> calcula_centro_mas_cercano([41.0], [[39.0], [45.0]], distancia_abs)
# 0
# >>> calcula_centro_mas_cercano([64.0], [[39.0], [45.0]], distancia_abs)
# 1
# -----------------------------------------------------------------


# ======= Soluci�n:

def calcula_centro_mas_cercano(dato, centros, distancia):
    distancias = [distancia(dato, centro) for centro in centros]
    minima_distancia = min(distancias)
    return distancias.index(minima_distancia)

# ================


# ---------------------------------------------------------------
# Ejercicio 4

# Define la funci�n "asigna_cluster_a_cada_ejemplo(clasif, centros, distancia)"
# que recibiendo una lista de clasificaci�n "clasif" y una lista de centros
# "centros", actualice clasif de manera que en cada dato, el cluster asignado
# sea el del centro en "centros" m�s cercano al ejemplo.

# Por ejemplo:

# >>> clas = clasificacion_inicial_vacia(pesos_poblacion)
# >>> centr = [[65.0], [48.0]]
# >>> asigna_cluster_a_cada_ejemplo(clas, centr, distancia_abs)
# >>> clas
# [[[51.0], 1], [[43.0], 1], [[62.0], 0], [[64.0], 0], [[45.0], 1],
#  [[42.0], 1], [[46.0], 1], [[45.0], 1], [[45.0], 1], [[62.0], 0],
#  [[47.0], 1], [[52.0], 1], [[64.0], 0], [[51.0], 1], [[65.0], 0],
#  ...]

# ====== Soluci�n:

def asigna_cluster_a_cada_ejemplo(clasif, centros, distancia):
    for ejemplo in clasif:
        ejemplo[1] = calcula_centro_mas_cercano(ejemplo[0], centros, distancia)

# ===============


# ---------------------------------------------------------------
# Ejercicio 5

# Definir una funci�n "recalcula_centros(clasif, num_clusters)" que recibiendo
# una lista de clasificaci�n y el n�mero total de clusters, devuelve la lista
# con los nuevos centros calculados como media aritm�tica de los datos de cada
# cluster.

# Por ejemplo (si "clas" con el valor del ejemplo anterior):
# >>> recalcula_centros(clas, 2)
# [[63.63157894736842], [46.8125]]

# ====== Soluci�n:

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

# Usando las funciones definidas anteriormente, definir la funci�n "k-medias(k,
# datos, distancia)" que implementa la siguiente versi�n del algoritmo k-medias:

# K-MEDIAS(K, DATOS, distancia)

# 1. Inicializar c_i (i=1, ..., K) (aleatoriamente o con alg�n criterio
#    heur�stico)
# 2. REPETIR (hasta que los c_i no cambien):
#    2.1 PARA j=1, ..., N HACER:
#        Calcular el cluster correspondiente a x_j, escogiendo, de entre
#        todos los c_i, el c_h tal que distancia(x_j, c_h) sea m�nima
#    2.2 PARA i=1, ..., K HACER:
#        Asignar a c_i la media aritm�tica de los datos asignados al
#        cluster i-�simo
# 3. Devolver c_1,...,c_K y el cluster asignado a cada dato
# ---------------------------------------------------------------------


# El algoritmo debe devolver como salida una lista con los centros finalmente
# obtenidos y con la lista de clasificaci�n.

# Por ejemplo:
# >>> k_medias(2, pesos_poblacion, distancia_abs)
# [[[46.8125], [63.63157894736842]],
#  [[[51.0], 0], [[43.0], 0], [[62.0], 1], [[64.0], 1], [[45.0], 0],
#   [[42.0], 0], [[46.0], 0], [[45.0], 0], [[45.0], 0], [[62.0], 1],
#   [[47.0], 0], [[52.0], 0], [[64.0], 1], [[51.0], 0], [[65.0], 1],
#   ....]]

# =========Soluci�n:

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
# Parte II: experimentaci�n de k-medias sobre �iris�
# **************************************************

# La siguiente lista �iris� contiene uno de los conjuntos de datos m�s conocido
# y usado como banco de pruebas en aprendizaje autom�tico. Se trata de una lista
# con 150 vectores de datos, cada uno de ellos con cuatro medidas num�ricas
# sobre longitud y anchura de s�palo y p�talo de la flor del lirio. Cada vector
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
        [6.3, 3.3, 6.0, 2.5, "Iris virg�nica"],
        [5.8, 2.7, 5.1, 1.9, "Iris virg�nica"],
        [7.1, 3.0, 5.9, 2.1, "Iris virg�nica"],
        [6.3, 2.9, 5.6, 1.8, "Iris virg�nica"],
        [6.5, 3.0, 5.8, 2.2, "Iris virg�nica"],
        [7.6, 3.0, 6.6, 2.1, "Iris virg�nica"],
        [4.9, 2.5, 4.5, 1.7, "Iris virg�nica"],
        [7.3, 2.9, 6.3, 1.8, "Iris virg�nica"],
        [6.7, 2.5, 5.8, 1.8, "Iris virg�nica"],
        [7.2, 3.6, 6.1, 2.5, "Iris virg�nica"],
        [6.5, 3.2, 5.1, 2.0, "Iris virg�nica"],
        [6.4, 2.7, 5.3, 1.9, "Iris virg�nica"],
        [6.8, 3.0, 5.5, 2.1, "Iris virg�nica"],
        [5.7, 2.5, 5.0, 2.0, "Iris virg�nica"],
        [5.8, 2.8, 5.1, 2.4, "Iris virg�nica"],
        [6.4, 3.2, 5.3, 2.3, "Iris virg�nica"],
        [6.5, 3.0, 5.5, 1.8, "Iris virg�nica"],
        [7.7, 3.8, 6.7, 2.2, "Iris virg�nica"],
        [7.7, 2.6, 6.9, 2.3, "Iris virg�nica"],
        [6.0, 2.2, 5.0, 1.5, "Iris virg�nica"],
        [6.9, 3.2, 5.7, 2.3, "Iris virg�nica"],
        [5.6, 2.8, 4.9, 2.0, "Iris virg�nica"],
        [7.7, 2.8, 6.7, 2.0, "Iris virg�nica"],
        [6.3, 2.7, 4.9, 1.8, "Iris virg�nica"],
        [6.7, 3.3, 5.7, 2.1, "Iris virg�nica"],
        [7.2, 3.2, 6.0, 1.8, "Iris virg�nica"],
        [6.2, 2.8, 4.8, 1.8, "Iris virg�nica"],
        [6.1, 3.0, 4.9, 1.8, "Iris virg�nica"],
        [6.4, 2.8, 5.6, 2.1, "Iris virg�nica"],
        [7.2, 3.0, 5.8, 1.6, "Iris virg�nica"],
        [7.4, 2.8, 6.1, 1.9, "Iris virg�nica"],
        [7.9, 3.8, 6.4, 2.0, "Iris virg�nica"],
        [6.4, 2.8, 5.6, 2.2, "Iris virg�nica"],
        [6.3, 2.8, 5.1, 1.5, "Iris virg�nica"],
        [6.1, 2.6, 5.6, 1.4, "Iris virg�nica"],
        [7.7, 3.0, 6.1, 2.3, "Iris virg�nica"],
        [6.3, 3.4, 5.6, 2.4, "Iris virg�nica"],
        [6.4, 3.1, 5.5, 1.8, "Iris virg�nica"],
        [6.0, 3.0, 4.8, 1.8, "Iris virg�nica"],
        [6.9, 3.1, 5.4, 2.1, "Iris virg�nica"],
        [6.7, 3.1, 5.6, 2.4, "Iris virg�nica"],
        [6.9, 3.1, 5.1, 2.3, "Iris virg�nica"],
        [5.8, 2.7, 5.1, 1.9, "Iris virg�nica"],
        [6.8, 3.2, 5.9, 2.3, "Iris virg�nica"],
        [6.7, 3.3, 5.7, 2.5, "Iris virg�nica"],
        [6.7, 3.0, 5.2, 2.3, "Iris virg�nica"],
        [6.3, 2.5, 5.0, 1.9, "Iris virg�nica"],
        [6.5, 3.0, 5.2, 2.0, "Iris virg�nica"],
        [6.2, 3.4, 5.4, 2.3, "Iris virg�nica"],
        [5.9, 3.0, 5.1, 1.8, "Iris virg�nica"]]

# ---------------------------------------------------------------
# Ejercicio 7

# La siguiente funci�n nos permite validar una clasificaci�n cualquiera de los
# 150 vectores num�ricos de la lista iris, compar�ndola con la clasificaci�n
# original que aparece en la base de datos. Para cada una de las tres
# clasificaciones originales, cuenta cu�ntos ejemplos hay en cada uno de los
# clusters asignados en la clasificaci�n que se le pasa como argumento de
# entrada.


def validacion_iris(clasificacion):
    posibles_valores = ["Iris setosa", "Iris versicolor", "Iris virg�nica"]
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
#   num�ricos, SIN el tipo de iris.
# - Aplicar el algoritmo de k-medias a esos datos (con la distancia eucl�dea)
# - Validar la clasificaci�n obtenida respecto de la clasificaci�n
#   original

# ======== Soluci�n:


def distancia_euclidea(v, w):
    return math.sqrt(sum((vi - wi) ** 2 for vi, wi in zip(v, w)))


# Sesi�n:

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



# Iris virg�nica
# ==============

# Cluster  0 :  0
# Cluster  1 :  14
# Cluster  2 :  36





# Comentarios: como se observa, el cluster 0 ha sido reconocido completamente
# como el cluster original de iris setosa. El cluster 1 casi al completo
# (excepto 2 ejemplos del 2) ha reconocido a iris versicolor. Sin embargo ha
# incluido tambi�n 14 ejemplos de iris virginica. El resto de iris virginica se
# ha asignado al cluster 2.

# Los resultados son bastante aceptables, aunque el algoritmo EM los mejora un
# poco.
