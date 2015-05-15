# Práctica 1: Introducción a Python
# =================================

# En esta práctica veremos algunos ejercicios de Python, para ir
# familiarizándonos con el lenguaje.


# -----------
# EJERCICIO 1
# -----------

# Escribir una función cuadrados que recibiendo una secuencia l de números,
# devuelve la lista de los cuadrados de esos números, en el mismo orden.


# Por ejemplo:
# >>> cuadrados([4, 1, 5.2, 3, 8])
# [16, 1, 27.040000000000003, 9, 64]

# Hacer dos versiones: una usando un bucle explícito, y la otra mediante
# definición de listas por comprensión.
# ---------------------------------------------------------------------------

# ======= Solución:
# Iterando:
def cuadrados (l):
    res = []
    for x in l:
        res.append(x ** 2)
    return res

# Con listas por comprensión:
def cuadrados (l):
    return [x ** 2 for x in l]

# ======================================


# -----------
# EJERCICIO 2
# -----------

# Definir una función vocales_consonantes, que reciba una cadena de
# caracteres s (de letras mayúsculas) y escribe por pantalla, una a una, si
# sus letras son vocales o  consonantes.

# Ejemplo:
# >>> vocales_consonantes("INTELIGENCIA")
# I es vocal
# N es consonante
# T es consonante
# E es vocal
# L es consonante
# I es vocal
# G es consonante
# E es vocal
# N es consonante
# C es consonante
# I es vocal
# A es vocal
# ---------------------------------------------------------------------------

# ======= Solución:
def vocales_consonantes(s):
    for x in s:
        if x in "AEIOU":
            print("{} es vocal".format(x))
        else:
            print("{} es consonante".format(x))
# ==================================


# -----------
# EJERCICIO 3
# -----------

# Usando como técnica principal la definición de secuancias por comprensión,
# definir las siguientes funciones:

# a) Dada una lista de números naturales, la suma de los cuadrados de los
#    números pares de la lista.

# Ejemplo:
# >>> suma_cuadrados([9, 4, 2, 6, 8, 1])
# 120

# ======= Solución:
def suma_cuadrados (l):
    return sum(x ** 2 for x in l if x % 2 == 0)
# ==================================


# b) Dada una lista de números l=[a(1),...,a(n)], calcular el sumatorio desde i=1
#    hasta n de i*a(i).

# Ejemplo:
# >>> suma_fórmula([2, 4, 6, 8, 10])
# 110

# ======= Solución:
def suma_fórmula (l):
    return sum((i + 1) * x for i, x in enumerate(l))
# ==================================


# c) Dadas dos listas numéricas de la misma longitud, representado dos puntos
#    n-dimensionales, calcular la distancia euclídea entre ellos. 

# Ejemplo:
# >>> distancia([3, 1, 2], [1, 2, 1])
# 2.449489742783178

# ======= Solución:
import math

def distancia (p1, p2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(p1, p2)))
# ==================================


# d) Dada una lista y una función de un argumento, devolver la lista de los
#    resultados de aplicar la función a cada elemento de la lista.

# Ejemplo:
# >>> map_mío(abs, [-2, -3, -4, -1])
# [2, 3, 4, 1]

# ======= Solución:
def map_mío (f, l):
    return [f(x) for x in l]
# ==================================


# e) Dadas un par de listas (de la misma longitud) y una función de dos
#    argumentos, devolver la lista de los resultados de aplicar la función a
#    cada par de elementos que ocupan la misma posición en las listas de
#    entrada.

# Ejemplo:
# >>> map2_mío(lambda x, y: x + y, [1, 2, 3, 4], [5, 2, 7, 9])
# [6, 4, 10, 13]

# ======= Solución:
def map2_mío (f, l1, l2):
    return [f(x, y) for x, y in zip(l1, l2)]

# Nota: Python dispone de la función map que, aplicada a una función de n argumentos y
# a n iteradores, devuelve un iterador que proporciona los resultados de aplicar la función
# a los primeros elementos de los iteradores, los segundos elementos, etc.
list(map(abs, [-2, -3, -4, -1]))
from operator import add
list(map(add, range(10), range(0, 20, 2)))
# ==================================


# f) Dada una lista de números, contar el número de elementos que sean múltiplos
#    de tres y distintos de cero. 

# Ejemplo:

# >>> m3_no_nulos([4, 0, 6, 7, 0, 9, 18])
# 3

# ======= Solución:
def m3_no_nulos (l):
    return sum(1 for _ in l if _ != 0 and _ % 3 == 0) 
# =========


# f) Dadas dos listas de la misma longitud, contar el número de posiciones en
#    las que coinciden los elementos de ambas listas.  

# Ejemplo:
# >>> cuenta_coincidentes([4, 2, 6, 8, 9, 3], [3, 2, 1, 8, 9, 6])
# 3

# ======= Solución:
def cuenta_coincidentes (l1, l2):
    return sum(1 for x, y in zip(l1, l2) if x == y)
# ==================================


# g) Dadas dos listas de la misma longitud, devolver un diccionario que tiene
# como claves las posiciones  en las que coinciden los elementos de ambas
# listas, y como valor de esas claves, el elemento coincidente. 

# Ejemplos:
# >>> dic_posiciones_coincidentes([4, 2, 6, 8, 9, 3], [3, 2, 1, 8, 9, 6])
# {1: 2, 3: 8, 4: 9}
# >>> dic_posiciones_coincidentes([2, 8, 1, 2, 1, 3], [1, 8, 1, 2, 1, 6])
# {1: 8, 2: 1, 3: 2, 4: 1}

# ======= Solución:
def dic_posiciones_coincidentes (l1, l2):
    return {i: x for i, (x, y) in enumerate(zip(l1, l2)) if x == y}
# ==================================


# -----------
# EJERCICIO 4
# -----------

# Un número es perfecto si es la suma de todos sus divisores (excepto él
# mismo). Definir una función filtra_perfectos(n, m, p) que imprime por pantalla
# todos los números perfectos entre n y m que cumplen la condición p. Se pide
# también que se indiquen los divisores de cada número perfecto que se
# imprima. 

# Ejemplo:

# >>> filtra_perfectos(3, 500, lambda x: True)
# El 6 es perfecto y sus divisores son [1, 2, 3]
# El 28 es perfecto y sus divisores son [1, 2, 4, 7, 14]
# El 496 es perfecto y sus divisores son [1, 2, 4, 8, 16, 31, 62, 124, 248]

# >>> filtra_perfectos(3, 500, lambda x: (x % 7 == 0))
# El 28 es perfecto y sus divisores son [1, 2, 4, 7, 14]
# ------------------------------------------------------------------------

# ======= Solución:
def filtra_perfectos (n, m, p):
    for x in range(n, m + 1):
        divisores_x = [d for d in range(1, x // 2 + 1) if x % d == 0]
        if x == sum(divisores_x) and p(x):
            print("El {} es perfecto y sus divisores son {}".format(x, divisores_x))
# ==================================


# -----------
# EJERCICIO 5
# -----------

# Supongamos que recibimos un diccionario cuyas claves son cadenas de
# caracteres de longitud uno y los valores asociados son números enteros 
# entre 0 y 50. 
# Definir una función histograma_horizontal(d), que recibiendo un diccionario 
# de ese tipo, escribe un histograma de barras horizontales asociado, 
# como se ilustra en el siguiente ejemplo:  

# >>> d1 = {'a': 5, 'b': 10, 'c': 12, 'd': 11, 'e': 15, 'f': 20,
#           'g': 15, 'h': 9, 'i': 7, 'j': 2}
# >>> histograma_horizontal(d1)
# a: *****
# b: **********
# c: ************
# d: ***********
# e: ***************
# f: ********************
# g: ***************
# h: *********
# i: *******
# j: **
#
# Nota: imprimir las barras, de arriba a abajo, en el orden que determina la
#         función "sorted" sobre las claves 
# ---------------------------------------------------------------------------

# ======= Solución:
def histograma_horizontal (d):
    for k, v in sorted(d.items()):
        print("{}: {}".format(k, '*' * v))
# ==================================


# -----------
# EJERCICIO 6
# -----------

# Con la misma entrada que el ejercicio anterior, definir una función
# histograma_vertical(d) que imprime el mismo histograma pero con las barras
# en vertical. 

# Ejemplo:
# >>> d2 = {'a': 5, 'b': 7, 'c': 9, 'd': 12, 'e': 15, 'f': 20,
#           'g': 15, 'h': 9, 'i': 7, 'j': 2}
# >>> histograma_vertical(d2)
#           *         
#           *         
#           *         
#           *         
#           *         
#         * * *       
#         * * *       
#         * * *       
#       * * * *       
#       * * * *       
#       * * * *       
#     * * * * * *     
#     * * * * * *     
#   * * * * * * * *   
#   * * * * * * * *   
# * * * * * * * * *   
# * * * * * * * * *   
# * * * * * * * * *   
# * * * * * * * * * * 
# * * * * * * * * * * 
# a b c d e f g h i j

# Nota: imprimir las barras, de izquierda a derecha, en el orden que determina la
#         función "sorted" sobre las claves 
# ---------------------------------------------------------------------------

# ======= Solución:
def histograma_vertical (d):
    altura_máxima = max(d.values())
    barras = ['{1:>{0}}{2}'.format(altura_máxima, '*' * v, k)
              for k, v in sorted(d.items())]
    for línea in zip(*barras):
        print(' '.join(línea))
# ================================


# -----------
# EJERCICIO 7
# -----------

#  (a) Definir la función compresion(l) que devuelva la lista resultante de
#  comprimir la lista l que recibe como entrada, en el siguiente sentido: 
#  * Si el elemento x aparece n (n > 1) veces de manera consecutiva en l
#    sustituimos esas n ocurrencias por la tupla (n, x)
#  * Si el elemento x es distinto de sus vecinos, entonces lo dejamos
#    igual

#  Ejemplo:
#  >>> compresión([1, 1, 1, 2, 1, 3, 2, 4, 4, 6, 8, 8, 8])
#  [[3, 1], 2, 1, 3, 2, [2, 4], 6, [3, 8]]
#  >>> compresión(['a', 'a', 'a', 'b', 'a', 'c', 'b', 'd', 'd', 'f', 'h', 'h', 'h'])
#  [[3, 'a'], 'b', 'a', 'c', 'b', [2, 'd'], 'f', [3, 'h']]

#  (b) Definir la función descompresión(l) que devuelva la lista l descomprimida,
#  suponiendo que ha sido comprimida con el método del apartado anterior.

#  Ejemplo:
#  >>> descompresión([[3, 1], 2, 1, 3, 2, [2, 4], 6, [3, 8]])
#  [1, 1, 1, 2, 1, 3, 2, 4, 4, 6, 8, 8, 8]
# ************************************************************************

# ======= Solución:
import itertools

def compresión (l):
    return [x if n == 1 else [n, x]
            for x, n in itertools.starmap(lambda x, grupo: (x, len(list(grupo))), itertools.groupby(l))]

def descompresión (l):
    return sum(([x[1]] * x[0] if isinstance(x, list) else [x] for x in l), [])
# ======================================


# -----------
# EJERCICIO 8
# -----------

# La profundidad de una lista anidada es el número máximo de anidamientos en
# la lista. Definir una función profundidad(l) que calcula la profundidad de
# una lista dada.

# Ejemplos:
# >>> profundidad(3)
# 0
# >>> profundidad([7, 5, 9, 5, 6])
# 1
# >>> profundidad([1, [1, [1, [1, 1], 1], [1, 1]], 1])
# 4

# Indicación: para saber si un dato es una lista, puede que sea útil la
# función "isinstance". En concreto, "isinstance(x, list)" comprueba si x es
# una lista.
# -------------------------------------------------------------------------

# ============= Solución:
def profundidad (l):
    if isinstance(l, list):
        return max(profundidad(m) for m in l) + 1
    else:
        return 0
# ============= 


# -----------
# EJERCICIO 9
# -----------

# Definir la función pertenece_prof(x, l), que comprueba la pertenencia de x a
# una lista l anidada

# Ejemplos:
# >>> pertenece_prof(1, [2, [3, [4, [1]]]])
# True
# >>> pertenece_prof('a', [['c', ['d', 'e', ['f', 'a'], 'g'], 'h'], ['i', ['j', 'k'], 'l'], 'b', ['x', 'y']])
# True
# >>> pertenece_prof('a', [['c', ['d', 'e', ['f', 'm'], 'g'], 'h'], ['i', ['j', 'k'], 'l'], 'b', ['x', 'y']])
# False
#
# Indicación: puede ser de utilidad la función "any" (consultar su
#    especificación en el manual)
# -----------------------------------------------------------------------

# =============== Solución:
def pertenece_prof (x, l):
    if isinstance(l, list):
        return any(pertenece_prof(x, m) for m in l)
    else:
        return x == l
# ===============================


# ------------
# EJERCICIO 10
# ------------

# Definir una función mi_grep(cadena, fichero) similar al comando grep de unix
# (sin uso de patrones). Es decir, escribe por pantalla las líneas de fichero
# en las que ocurre cadena (junto con el número de línea).

# Por ejemplo, si buscamos la cadena "función" en un fichero similar a éste,
# las prímeras líneas de la salida podría ser similar a esta: 

# >>> mi_grep("función","ejercicios.py")
# Línea 4: # Escribir una función cuadrados(l) que recibiendo una secuencia l de números,
#                         ^^^^^^^
# Línea 36: #  Definir la función compresion(l) que devuelva la lista resultante de
#                         ^^^^^^^
# Línea 50: #  Definir la función descompresion(l) que devuelva la lista l descomprimida,
#                         ^^^^^^^
# Línea 121: # Definir una función vocales_consonantes(s), que reciba una cadena de
#                          ^^^^^^^
# Línea 155: # Definir una función oculta_palabras(s) que reciba una cadena de caracteres
#                          ^^^^^^^
# Línea 180: # Definir, sin usar "slicing", una función es_palíndromo(s) que reconoce si
#                                               ^^^^^^^
# ---------------------------------------------------------------------------

# ======= Solución:
def mi_grep (cadena, fichero):
    tam_cadena = len(cadena)
    with open(fichero, 'r') as f:
        for i, línea in enumerate(f):
            if cadena in línea:
                salida = 'Línea {0}: {1}'.format(i, línea)
                posición = salida.find(cadena)
                marca = '{0:>{1}}'.format('^' * tam_cadena, posición + tam_cadena)
                print(salida, end = '')
                print(marca)
# =======================================================


# ------------
# EJERCICIO 11
# ------------

# Supongamos que queremos simular la trayectoria de un proyectil que se
# dispara en un punto dado a una determinada altura inicial. El disparo se
# realiza hacia adelante con una velocidad inicial y con un determinado ángulo. Inicialmente
# el proyectil avanzará subiendo pero por la fuerza de la gravedad en un
# momento dado empezará a bajar hasta que aterrice. Por simplificar,
# supondremos que no existe rozamiento ni resistencia del viento.

# Diseñar una clase Proyectil que sirva representar el estado del proyectil en
# un instante de tiempo dado. Para ello, necsitamos al menos los siguientes
# atributos de datos:
# - Distancia recorrida (en horizontal)
# - Altura
# - Velocidad horizontal
# - Velocidad vertical

# Además, incluir los siguientes tres métodos:
# - actualiza(t): actualiza la posición y la velocidad del proyectil tras t
#   segundos
# - obtén_posx(): devuelve la distancia horizontal recorrida 
# - obtén_posy(): devuelve la distancia vertical recorrida 

# Una vez definida la clase Proyectil, usarla para definir una función 
#    aterriza(altura, velocidad, ángulo, intervalo)
# que imprimirá por pantalla las distintas posiciones por las que pasa un
# proyectil que se ha disparado con una velocidad, un ángulo (en grados) 
# y una áltura inicial dada. Se mostrará la posición del proyectil 
# en cada intervalo de tiempo, hasta que aterriza.
# Además se mostrará la altura máxima que ha alcanzado, cuántos intervalos de
# tiempo ha tardado en aterrizar y el alcance que ha tenido.

# Indicaciones:
# - Si el proyectil tiene una velocidad inicial v y se lanza con un ángulo
#   theta, las componentes horizontal y vertical de la velocidad inicial son
#   v*cos(theta) y v*sen(theta), respectivamente.
# - La componente horizontal de la velocidad, en ausencia de rozamiento 
#   y viento, podemos suponer que permanece constante.
# - La componente vertical de la velocidad cambia de la siguiente manera
#   tras un instante t: si vy0 es la velocidad vertical al inicio del
#   intervalo, entonces al final del intervalo tiene una velocidad 
#   vy1=vy0-9.8*t, debido a la gravedad de la Tierra.
# - En ese caso, si el proyectil se encuentra a una altura h0, tras un
#   intervalo t de tiempo se encontrará a una altura h1=h0 - vm*t, donde vm 
#   es la media entre las anteriores vy0 y vy1. 
# - Será necesario importar la biblioteca "math"

# Ejemplo:
# >>> aterriza(30, 45, 20, 0.01)
# Proyectil en posición(0.0, 0.0)
# Proyectil en posición(0.4, 0.2)
# Proyectil en posición(0.8, 0.3)
# Proyectil en posición(1.3, 0.5)
# Proyectil en posición(1.7, 0.6)
# Proyectil en posición(2.1, 0.8)
# Proyectil en posición(2.5, 0.9)
# Proyectil en posición(3.0, 1.1)
# Proyectil en posición(3.4, 1.2)
#           ·······
# ·······SALIDA OMITIDA ·······
#           ·······
# Proyectil en posición(129.0, 1.4)
# Proyectil en posición(129.4, 1.2)
# Proyectil en posición(129.8, 1.1)
# Proyectil en posición(130.2, 0.9)
# Proyectil en posición(130.7, 0.8)
# Proyectil en posición(131.1, 0.6)
# Proyectil en posición(131.5, 0.5)
# Proyectil en posición(131.9, 0.3)
# Proyectil en posición(132.4, 0.2)
# Proyectil en posición(132.8, 0.0)
 
# Tras 315 intervalos de 0.01 segundos (3.15 segundos) el proyectil ha aterrizado.
# Ha recorrido una distancia de 133.2 metros
# Ha alcanzado una altura máxima de 12.1 metros
# -----------------------------------------------------------------------------


# ============== Solución

from math import sin, cos, radians

class Proyectil:
    def __init__(self, ángulo, velocidad, altura):
        self.posx = 0
        self.posy = altura
        theta = radians(ángulo)
        self.vx = velocidad * cos(theta)
        self.vy = velocidad * sin(theta)

    def actualiza (self, t):
        self.posx += t * self.vx
        vy1 = self.vy - 9.8 * t
        self.posy += t * (self.vy + vy1) / 2
        self.vy = vy1

    def obtén_posx (self):
        return self.posx

    def obtén_posy (self):
        return self.posy
    

def aterriza (altura, velocidad, ángulo, intervalo):
    proy = Proyectil(ángulo, velocidad, altura)
    n = 0
    hmax = -1
    while proy.obtén_posy() >= 0:
        print("Proyectil en posición({0:0.1f}, {1:0.1f})".format(proy.obtén_posx(), proy.obtén_posy()))
        if proy.obtén_posy() > hmax:
            hmax = proy.obtén_posy()
        proy.actualiza(intervalo)
        n += 1
    print("\nTras {} intervalos de {} segundos ({} segundos) el proyectil ha aterrizado.".format(
        n, intervalo, n * intervalo))
    print("Ha recorrido una distancia de {0:0.1f} metros".format(proy.obtén_posx()))
    print("Ha alcanzado una altura máxima de {0:0.1f} metros".format(hmax))
# ==========



