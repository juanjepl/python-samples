# practica-02.py
# Inteligencia Artificial, tercer curso del Grado de Ingeniería Informática -

# Práctica 2: Búsqueda en espacios de estados
# ===========================================

# En esta práctica aplicaremos los algoritmos de búsqueda vistos en clase,
# viendo cómo se comportan con el problema del 8 puzzle.

# La práctica tiene tres partes bien diferenciadas:

# Parte I: Representación de problemas de espacios de estados. Veremos una
# técnica general para hacerlo, y en particular se implementará el problema del
# ocho puzzle.

# Parte II: Experimentación con los algoritmos implementados. Ejecución de los
# algoritmos implementados, para la búsqueda de soluciones a instancias
# concretas de los problemas.

# Parte III: Calcularemos algunos estadísticas sobre la ejecución de los
# algoritmos para resolución de problemas de ocho puzzle. Así, se comprobarán
# experimentalmente algunas propiedades de los algoritmos.

# El código que se usa en esta práctica está basado principalmente en el
# código Python que se proporciona con el libro "Artificial Intelligence: A
# Modern Approach" de S. Russell y P. Norvig
# (http://code.google.com/p/aima-python, módulo search.py). Las modificaciones
# al código y la traducción han realizadas por José Luis Ruiz Reina (Depto. de
# Ciencias de la Computación e Inteligencia Artificial de la Universidad de
# Sevilla).


# ATENCIÓN:
# =========
# Los dos siguientes "import" son necesarios para el modo python de emacs, que
# no actualiza bien el camino de carga de los módulos. Si no se usa emacs,
# dejarlo comentado. Si se usa, descomentar poner el camino absoluto donde
# están el fichero de la práctica y el auxiliar (algoritmos_de_búsqueda.py)

#import sys
#sys.path.append("/home/naranjo/IAIS_14/practicas/practica-1/")


#===============================================
# PARTE I. REPRESENTACIÓN DE ESPACIOS DE ESTADOS
#===============================================

# Recuérdese que según lo que se ha visto en clase, la implementación de la
# representación de un problema de espacio de estados consiste en:

# * Representar estados y acciones mediante una estructura de datos.
# * Definir: estado_inicial, es_estado_final(_), acciones(_), aplica(_,_) y
#   coste_de_aplicar_accion, si el problema tiene coste.

# La siguiente clase Problema representa este esquema general de cualquier
# problema de espacio de estados. Un problema concreto será una subclase de
# Problema, y requerirá implementar acciones, aplica y eventualmente __init__,
# es_estado_final y  coste_de_aplicar_accion.

class Problema(object):
    """Clase abstracta para un problema de espacio de estados. Los problemas
    concretos habría que definirlos como subclases de Problema, implementando
    acciones, aplica y eventualmente __init__, es_estado_final y
    coste_de_aplicar_accion. Una vez hecho esto, se han de crear instancias de
    dicha subclase, que serán la entrada a los distintos algoritmos de
    resolución mediante búsqueda."""

    def __init__(self, estado_inicial, estado_final=None):
        """El constructor de la clase especifica el estado inicial y
        puede que un estado_final, si es que es único. Las subclases podrían
        añadir otros argumentos"""

        self.estado_inicial = estado_inicial
        self.estado_final = estado_final

    def acciones(self, estado):
        """Devuelve las acciones aplicables a un estado dado. Lo normal es
        que aquí se devuelva una lista, pero si hay muchas se podría devolver
        un iterador, ya que sería más eficiente."""
        raise NotImplementedError

    def aplica(self, estado, accion):
        """Devuelve el estado resultante de aplicar accion a estado. Se
        supone que accion es aplicable a estado (es decir, debe ser una de las
        acciones de self.acciones(estado)."""
        raise NotImplementedError

    def es_estado_final(self, estado):
        """Devuelve True cuando estado es final. Por defecto, compara con el
        estado final, si éste se hubiera especificado al constructor. Si se da
        el caso de que no hubiera un único estado final, o se definiera
        mediante otro tipo de comprobación, habría que redefinir este método
        en la subclase."""
        return estado == self.estado_final

    def coste_de_aplicar_accion(self, estado, accion):
        """Devuelve el coste de aplicar accion a estado. Por defecto, este
        coste es 1. Reimplementar si el problema define otro coste"""
        return 1

# Lo que sigue es un ejemplo de cómo definir un problema como subclase
# de problema. En concreto, el problema de las jarras, visto en clase:


class Jarras(Problema):
    """Problema de las jarras:
    Representaremos los estados como tuplas (x, y) de dos números enteros,
    donde x es el número de litros contenidos en la jarra de capacidad 4 e
    y es el número de litros contenidos en la jarra de capacidad 3"""

    def __init__(self):
        super().__init__((0, 0))

    def acciones(self, estado):
        jarra_de_4 = estado[0]
        jarra_de_3 = estado[1]
        acciones_aplicables = []
        if jarra_de_4 > 0:
            acciones_aplicables.append('vaciar jarra de 4')
            if jarra_de_3 < 3:
                acciones_aplicables.append('trasvasar de jarra de 4 a jarra de 3')
        if jarra_de_4 < 4:
            acciones_aplicables.append('llenar jarra de 4')
            if jarra_de_3 > 0:
                acciones_aplicables.append('trasvasar de jarra de 3 a jarra de 4')
        if jarra_de_3 > 0:
            acciones_aplicables.append('vaciar jarra de 3')
        if jarra_de_3 < 3:
            acciones_aplicables.append('llenar jarra de 3')
        return acciones_aplicables

    def aplica(self, estado, accion):
        j4 = estado[0]
        j3 = estado[1]
        if accion == 'llenar jarra de 4':
            return (4, j3)
        elif accion == 'llenar jarra de 3':
            return (j4, 3)
        elif accion == 'vaciar jarra de 4':
            return (0, j3)
        elif accion == 'vaciar jarra de 3':
            return (j4, 0)
        elif accion == 'trasvasar de jarra de 4 a jarra de 3':
            return (j4 - (3 - j3), 3) if j3 + j4 >= 3 else (0, j3 + j4)
        else:  # "trasvasar de jarra de 3 a jarra de 4"
            return (j3 + j4, 0) if j3 + j4 <= 4 else (4, j3 - (4 - j4))

    def es_estado_final(self, estado):
        return estado[0] == 2


# Ejemplos:

# >>> pj = Jarras()
# >>> pj.estado_inicial
# (0, 0)
# >>> pj.acciones(pj.estado_inicial)
# ['llenar jarra de 4', 'llenar jarra de 3']
# >>> pj.aplica(pj.estado_inicial,"llenar jarra de 4")
# (4, 0)
# >>> pj.coste_de_aplicar_accion(pj.estado_inicial,"llenar jarra de 4")
# 1
# >>> pj.es_estado_final(pj.estado_inicial)
# False

# -----------
# Ejercicio 1
# -----------

# ---------------------------------------------------------------------------
# Definir la clase Ocho_Puzzle, que implementa la representación del
# problema del 8-puzzle visto en clase. Para ello, completar el código que se
# presenta a continuación, en los lugares marcados con interrogantes.
# ----------------------------------------------------------------------------


class Ocho_Puzzle(Problema):
    """Problema a del 8-puzzle.  Los estados serán tuplas de nueve elementos,
    permutaciones de los números del 0 al 8 (el 0 es el hueco). Representan la
    disposición de las fichas en el tablero, leídas por filas de arriba a
    abajo, y dentro de cada fila, de izquierda a derecha. Por ejemplo, el
    estado final será la tupla (1, 2, 3, 8, 0, 4, 7, 6, 5). Las cuatro
    acciones del problema las representaremos mediante las cadenas:
    'Mover hueco arriba', 'Mover hueco abajo', 'Mover hueco izquierda' y
    'Mover hueco derecha', respectivamente."""

    def __init__(self, tablero_inicial):
        super().__init__(estado_inicial=tablero_inicial,
                         estado_final=(1, 2, 3, 8, 0, 4, 7, 6, 5))

    def acciones(self, estado):
        pos_hueco = estado.index(0)
        acciones_aplicables = []
        if pos_hueco not in [0, 1, 2]:
            acciones_aplicables.append('Mover hueco arriba')
        if pos_hueco not in [6, 7, 8]:
            acciones_aplicables.append('Mover hueco abajo')
        if pos_hueco not in [0, 3, 6]:
            acciones_aplicables.append('Mover hueco izquierda')
        if pos_hueco not in [2, 5, 8]:
            acciones_aplicables.append('Mover hueco derecha')
        return acciones_aplicables

    def aplica(self, estado, accion):
        pos_hueco = estado.index(0)
        if accion == 'Mover hueco arriba':
            nueva_pos = pos_hueco - 3
        elif accion == 'Mover hueco abajo':
            nueva_pos = pos_hueco + 3
        elif accion == 'Mover hueco izquierda':
            nueva_pos = pos_hueco - 1
        else:  # Mover hueco derecha
            nueva_pos = pos_hueco + 1
        ficha = estado[nueva_pos]
        estado_como_lista = list(estado)
        estado_como_lista[pos_hueco], estado_como_lista[nueva_pos] = ficha, 0
        return tuple(estado_como_lista)

# Ejemplos que se pueden ejecutar una vez se ha definido la clase:

# >>> p8p_1 = Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# >>> p8p_1.estado_inicial
# (2, 8, 3, 1, 6, 4, 7, 0, 5)
# >>> p8p_1.estado_final
# (1, 2, 3, 8, 0, 4, 7, 6, 5)
# >>> p8p_1.acciones(p8p_1.estado_inicial)
# ['Mover hueco arriba', 'Mover hueco izquierda', 'Mover hueco derecha']
# >>> p8p_1.aplica(p8p_1.estado_inicial,"Mover hueco arriba")
# (2, 8, 3, 1, 0, 4, 7, 6, 5)
# >>> p8p_1.coste_de_aplicar_accion(p8p_1.estado_inicial,"Mover hueco arriba")
# 1


#=========================
# PARTE II. Experimentando
#=========================

from algoritmos_de_búsqueda import *

# -----------
# Ejercicio 2
# -----------

# Usar búsqueda en anchura y en profundidad para encontrar soluciones tanto al
# problema de las jarras como al problema del ocho puzzle con distintos
# estados iniciales.

# Ejemplos de uso:

# >>> búsqueda_en_anchura(Jarras()).solucion()
# ['llenar jarra de 4', 'trasvasar de jarra de 4 a jarra de 3',
#  'vaciar jarra de 3', 'trasvasar de jarra de 4 a jarra de 3',
#  'llenar jarra de 4', 'trasvasar de jarra de 4 a jarra de 3']
# >>> búsqueda_en_profundidad(Jarras()).solucion()
# ['llenar jarra de 3', 'trasvasar de jarra de 3 a jarra de 4',
#  'llenar jarra de 3', 'trasvasar de jarra de 3 a jarra de 4',
#  'vaciar jarra de 4', 'trasvasar de jarra de 3 a jarra de 4']
# >>> búsqueda_en_anchura(Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))).solucion()
# ['Mover hueco arriba', 'Mover hueco arriba', 'Mover hueco izquierda',
#  'Mover hueco abajo', 'Mover hueco derecha']
# >>> búsqueda_en_profundidad(Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))).solucion()
# ['Mover hueco derecha', 'Mover hueco arriba', ... ] # ¡más de 3000 acciones!

# -----------
# Ejercicio 3
# -----------

# Definir las dos funciones heurísticas para el 8 puzzle que se han visto en
# clase. Es decir:
# - h1_ocho_puzzle(estado): cuenta el número de casillas mal colocadas respecto
#   del estado final.
# - h2_ocho_puzzle_estado(estado): suma la distancia Manhattan desde cada
#   casilla a la posición en la que debería estar en el estado final.

# Ejemplos:

# >>> h1_ocho_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# 4
# >>> h2_ocho_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# 5
# >>> h1_ocho_puzzle((5, 2, 3, 0, 4, 8, 7, 6, 1))
# 4
# >>> h2_ocho_puzzle((5, 2, 3, 0, 4, 8, 7, 6, 1))
# 11


def h1_ocho_puzzle(estado):
    """Cuenta el número de piezas descolocadas"""
    estado_final = (1, 2, 3, 8, 0, 4, 7, 6, 5)
    return sum(1 for f1, f2 in zip(estado, estado_final)
               if f1 != 0 and f1 != f2)


def h2_ocho_puzzle(estado):
    """Suma la distancia Manhattan de cada casilla a donde debería estar"""
    fichas = list(range(1, 9))
    estado_final = (1, 2, 3, 8, 0, 4, 7, 6, 5)
    pos_estado = (divmod(estado.index(f), 3) for f in fichas)
    pos_final = (divmod(estado_final.index(f), 3) for f in fichas)
    return sum(abs(x1 - x2) + abs(y1 - y2)
               for ((x1, y1), (x2, y2)) in zip(pos_estado, pos_final))


#============
# Ejercicio 4
#============

# Resolver usando búsqueda_óptima, búsqueda_primero_el_mejor y
# búsqueda_a_estrella (con las dos heurísticas), el problema del 8 puzzle para
# el siguiente estado inicial:

#              +---+---+---+
#              | 2 | 8 | 3 |
#              +---+---+---+
#              | 1 | 6 | 4 |
#              +---+---+---+
#              | 7 | H | 5 |
#              +---+---+---+

# >>> búsqueda_óptima(Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))).solucion()
# ['Mover hueco arriba', 'Mover hueco arriba', 'Mover hueco izquierda',
#  'Mover hueco abajo', 'Mover hueco derecha']

# >>> búsqueda_primero_el_mejor(Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5)),h1_ocho_puzzle).solucion()
# ['Mover hueco arriba', 'Mover hueco izquierda', 'Mover hueco arriba',
#  'Mover hueco derecha', 'Mover hueco abajo', 'Mover hueco izquierda',
#  'Mover hueco arriba', 'Mover hueco derecha', 'Mover hueco abajo']

# >>> búsqueda_primero_el_mejor(Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5)),h2_ocho_puzzle).solucion()
# ['Mover hueco arriba', 'Mover hueco arriba', 'Mover hueco izquierda',
#  'Mover hueco abajo', 'Mover hueco derecha']

# >>> búsqueda_a_estrella(Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5)),h1_ocho_puzzle).solucion()
# ['Mover hueco arriba', 'Mover hueco arriba', 'Mover hueco izquierda',
#  'Mover hueco abajo', 'Mover hueco derecha']

# >>> búsqueda_a_estrella(Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5)),h2_ocho_puzzle).solucion()
# ['Mover hueco arriba', 'Mover hueco arriba', 'Mover hueco izquierda',
#  'Mover hueco abajo', 'Mover hueco derecha']


#========================
# PARTE III. Estadísticas
#========================

# La siguientes definiciones nos van a permitir experimentar con distintos
# estados iniciales, algoritmos y heurísticas, para resolver el
# 8-puzzle. Además se van a contar el número de nodos analizados durante la
# búsqueda:


class Problema_con_Analizados(Problema):
    """Es un problema que se comporta exactamente igual que el que recibe al
       inicializarse, y además incorpora un atributos nuevos para almacenar el
       número de nodos analizados durante la búsqueda. De esta manera, no
       tenemos que modificar el código del algoritmo de búsqueda."""

    def __init__(self, problema):
        self.estado_inicial = problema.estado_inicial
        self.problema = problema
        self.analizados = 0

    def acciones(self, estado):
        return self.problema.acciones(estado)

    def aplica(self, estado, accion):
        return self.problema.aplica(estado, accion)

    def es_estado_final(self, estado):
        self.analizados += 1
        return self.problema.es_estado_final(estado)

    def coste_de_aplicar_accion(self, estado, accion):
        return self.problema.coste_de_aplicar_accion(estado, accion)


def resuelve_ocho_puzzle(estado_inicial, algoritmo, h=None):
    """Función para aplicar un algoritmo de búsqueda dado al problema del ocho
       puzzle, con un estado inicial dado y (cuando el algoritmo lo necesite)
       una heurística dada.
       Ejemplo de uso:

       >>> resuelve_ocho_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5),búsqueda_a_estrella,h2_ocho_puzzle)
       Solución: ['Mover hueco arriba', 'Mover hueco arriba', 'Mover hueco izquierda',
                  'Mover hueco abajo', 'Mover hueco derecha']
       Algoritmo: búsqueda_a_estrella
       Heurística: h2_ocho_puzzle
       Longitud de la solución: 5. Nodos analizados: 7
       """

    p8p = Problema_con_Analizados(Ocho_Puzzle(estado_inicial))
    sol = algoritmo(p8p, h).solucion() if h else algoritmo(p8p).solucion()
    print("Solución: {0}".format(sol))
    print("Algoritmo: {0}".format(algoritmo.__name__))
    if h:
        print("Heurística: {0}".format(h.__name__))
    print("Longitud de la solución: {0}. Nodos analizados: {1}".format(
        len(sol), p8p.analizados))


#============
# Ejercicio 5
#============

# Intentar resolver usando las distintas búsquedas y en su caso, las distintas
# heurísticas, el problema del 8 puzzle para los siguientes estados iniciales:

#           E1              E2              E3              E4
#
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
#     | 2 | 8 | 3 |   | 4 | 8 | 1 |   | 2 | 1 | 6 |   | 5 | 2 | 3 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
#     | 1 | 6 | 4 |   | 3 | H | 2 |   | 4 | H | 8 |   | H | 4 | 8 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
#     | 7 | H | 5 |   | 7 | 6 | 5 |   | 7 | 5 | 3 |   | 7 | 6 | 1 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+

# Se pide, en cada caso, hacerlo con la función resuelve_ocho_puzzle, para
# obtener, además de la solución, la longitud (el coste) de la solución
# obtenida y el número de nodos analizados. Anotar los resultados en la
# siguiente tabla (L, longitud de la solución, NA, nodos analizados), y
# justificarlos con las distintas propiedades teóricas estudiadas.

# -----------------------------------------------------------------------------------------
#                                       E1           E2           E3          E4

# Anchura                             L=5           L=12         L=-         L=-
#                                     NA=35         NA=2032      NA=-        NA=-

# Profundidad                         L=3437        L=-          L=-         L=-
#                                     NA=3528       NA=-         NA=-        NA=-

# Óptima                              L=5           L=12         L=-         L=-
#                                     NA=53         NA=2049      NA=-        NA=-

# Primero el mejor (h1)               L=9           L=20         L=134       L=105
#                                     NA=11         NA=24        NA=575      NA=1002

# Primero el mejor (h2)               L=5           L=12         L=28        L=37
#                                     NA=7          NA=15        NA=196      NA=177

# A* (h1)                             L=5           L=12         L=18        L=25
#                                     NA=8          NA=91        NA=1290     NA=23209

# A* (h2)                             L=5           L=12         L=18        L=25
#                                     NA=7          NA=15        NA=138      NA=1273
# -----------------------------------------------------------------------------------------

# Comentarios:
# * La búsqueda en profundidad, en este caso, no resulta práctica incluso para
#   problemas sencillos. En muchos casos, la búsqueda en profundidad se
#   prefiere a la de anchura, debido a su menor gasto de espacio. Es
#   especialmente indicada cuando todas las soluciones están a una misma
#   profundidad. Sin embargo, en este caso, al existir soluciones muy largas,
#   no es mejor que la búsqueda en anchura.
# * En este caso, la búsqueda en anchura y la óptima, prácticamente coinciden,
#   ya que el coste de aplicar una acción es 1.
# * La búsqueda ciega va siendo cada vez más ineficiente a medida que aumenta
#   la complejidad del problema (en este caso, los estados iniciales que se
#   consideran están cada vez más lejos, en número de movimientos, del estado
#   final). En los dos últimos casos, es impracticable.
# * La búsqueda primero el mejor es bastante rápida. Sin embargo, la «calidad»
#   de las soluciones que encuentra es mala (no se asegura que encuentre una
#   solución óptima).
# * Ambas heurísticas usadas son admisibles (¡razonar por qué!). Por tanto, la
#   solución que encuentra A* es óptima, como se puede corroborar en los casos
#   en los que sabemos la solución óptima, que ha encontrado la búsqueda
#   óptima. Además, la eficiencia de A* en todos los casos es bastante buena en
#   los cuatro ejemplos.
# * La heurística h2 está más informada que h1. Esto se traduce en que A* con
#   h2 analiza menos nodos que h1, en todos los casos probados. Como las dos
#   heurísticas son admisibles, la calidad de la solución que encuantran en la
#   misma en ambos casos.


#============
# Ejercicio 6
#============

# La siguiente heurística h3_ocho_puzzle se obtiene sumando a la heurística
# h2_ocho_puzzle una componente que cuantifica la "secuencialidad" en las
# casillas de un tablero, al recorrerlo en el sentido de las aguas del reloj
# ¿Es h3 admisible? Comprobar cómo se comporta esta heurística cuando se usa en
# A*, con cada uno de los estados anteriores. Comentar los resultados.


def h3_ocho_puzzle(estado):
    suc_ocho_puzzle = {0: 1, 1: 2, 2: 5, 3: 0, 4: 4, 5: 8, 6: 3, 7: 6, 8: 7}

    def secuencialidad_aux(estado, i):
        val = estado[i]
        if val == 0:
            return 0
        elif i == 4:
            return 1
        else:
            i_sig = suc_ocho_puzzle[i]
            val_sig = (val + 1 if val < 8 else 1)
            return 0 if val_sig == estado[i_sig] else 2

    def secuencialidad(estado):
        res = 0
        for i in range(8):
            res += secuencialidad_aux(estado, i)
        return res

    return h2_ocho_puzzle(estado) + 3 * secuencialidad(estado)


# ***********
# Solución:
# ************


# Con E1, L=5, NA=7
# Con E2, L=12, NA=38
# Con E3, L=30, NA=78
# Con E4, L=33, NA=395

# Con E1:
# >>> resuelve_ocho_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5),búsqueda_a_estrella,h3_ocho_puzzle)
# Solución: ['Mover hueco arriba', 'Mover hueco arriba', 'Mover hueco izquierda',
#            'Mover hueco abajo', 'Mover hueco derecha']
# Algoritmo: búsqueda_a_estrella
# Heurística: h3_ocho_puzzle
# Longitud de la solución: 5. Nodos analizados: 7

# Con E2:
# >>> resuelve_ocho_puzzle((4,8,1,3,0,2,7,6,5),búsqueda_a_estrella,h3_ocho_puzzle)
# Solución: ['Mover hueco izquierda', 'Mover hueco arriba', 'Mover hueco derecha',
#            'Mover hueco derecha', 'Mover hueco abajo', 'Mover hueco izquierda',
#            'Mover hueco izquierda', 'Mover hueco arriba', 'Mover hueco derecha',
#            'Mover hueco derecha', 'Mover hueco abajo', 'Mover hueco izquierda']
# Algoritmo: búsqueda_a_estrella
# Heurística: h3_ocho_puzzle
# Longitud de la solución: 12. Nodos analizados: 38

# Con E3:
# resuelve_ocho_puzzle((2,1,6,4,0,8,7,5,3),búsqueda_a_estrella,h3_ocho_puzzle)
# Solución: ['Mover hueco arriba', 'Mover hueco derecha', 'Mover hueco abajo',
#            ... 'Mover hueco abajo']
# Algoritmo: búsqueda_a_estrella
# Heurística: h3_ocho_puzzle
# Longitud de la solución: 30. Nodos analizados: 78

# Con E4:
#  resuelve_ocho_puzzle((5,2,3,0,4,8,7,6,1),búsqueda_a_estrella,h3_ocho_puzzle)
# Solución: ['Mover hueco arriba', 'Mover hueco derecha',
#            ... 'Mover hueco derecha']
# Algoritmo: búsqueda_a_estrella
# Heurística: h3_ocho_puzzle
# Longitud de la solución: 33. Nodos analizados: 395

# La heurística es buena, pero no es admisible. Como se ve, no ha encontrado
# la solución óptima en los últimos dos casos.
