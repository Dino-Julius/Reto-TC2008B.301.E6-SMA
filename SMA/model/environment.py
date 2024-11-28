"""
Esta es una representación de la ciudad donde el agente se moverá en una cuadrícula.

Abreviaciones de movimiento en CITY:
    DW: Abajo
    UP: Arriba
    LF: Izquierda
    RH: Derecha
    TL: Semáforo
    PK: Estacionamiento
    BL: Edificio
    RD: Rotonda

Descripción de parking_spots:
    La clave es el id del estacionamiento.
    El valor es una tupla con las coordenadas (fila, columna) del estacionamiento.
    Ya están ordenados en el sistema de ejes de mesa.

Descripción de street_directions:
    La clave es una tupla con las coordenadas (fila, columna) de la calle.
    El valor es una lista con los movimientos posibles que se pueden hacer desde esa calle.
    Los movimientos están representados por las abreviaciones usadas en CITY.
"""
CITY = [
    ["DW", "DW", "LF", "LF", "LF", "LF", "LF", "LF", "TL", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF"],
    ["DW", "DW", "LF", "LF", "LF", "LF", "LF", "LF", "TL", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF"],
    ["DW", "DW", "BL", "PK", "BL", "BL", "TL", "TL", "BL", "BL", "BL", "BL", "DW", "DW", "UP", "UP", "BL", "PK", "BL", "BL", "BL", "BL", "UP", "UP"],
    ["DW", "DW", "BL", "BL", "BL", "BL", "UP", "UP", "BL", "BL", "BL", "BL", "DW", "DW", "UP", "UP", "BL", "BL", "BL", "BL", "BL", "BL", "UP", "UP"],
    ["DW", "DW", "BL", "BL", "BL", "BL", "UP", "UP", "BL", "BL", "PK", "BL", "DW", "DW", "UP", "UP", "BL", "BL", "BL", "BL", "BL", "BL", "UP", "UP"],
    ["DW", "DW", "BL", "BL", "BL", "BL", "UP", "UP", "TL", "LF", "LF", "LF", "DW", "DW", "UP", "UP", "BL", "BL", "BL", "BL", "PK", "BL", "UP", "UP"],
    ["DW", "DW", "BL", "BL", "BL", "PK", "UP", "UP", "TL", "LF", "LF", "LF", "DW", "DW", "UP", "UP", "LF", "LF", "LF", "LF", "LF", "LF", "UP", "UP"],
    ["DW", "DW", "BL", "BL", "BL", "BL", "TL", "TL", "BL", "BL", "BL", "BL", "DW", "DW", "UP", "UP", "LF", "LF", "LF", "LF", "LF", "LF", "UP", "UP"],
    ["DW", "DW", "BL", "BL", "BL", "BL", "UP", "UP", "PK", "BL", "BL", "BL", "DW", "DW", "UP", "UP", "BL", "BL", "BL", "BL", "PK", "BL", "UP", "UP"],
    ["DW", "DW", "PK", "BL", "BL", "BL", "UP", "UP", "BL", "BL", "BL", "BL", "DW", "DW", "UP", "UP", "BL", "BL", "BL", "BL", "BL", "BL", "UP", "UP"],
    ["DW", "DW", "BL", "BL", "BL", "BL", "UP", "UP", "BL", "BL", "BL", "BL", "DW", "DW", "UP", "UP", "BL", "BL", "BL", "BL", "BL", "BL", "UP", "UP"],
    ["DW", "DW", "BL", "BL", "PK", "BL", "UP", "UP", "BL", "BL", "PK", "BL", "DW", "DW", "UP", "UP", "BL", "BL", "BL", "BL", "BL", "BL", "UP", "UP"],
    ["DW", "DW", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "DW", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "UP", "UP"],
    ["DW", "DW", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "LF", "DW", "RD", "RD", "UP", "LF", "LF", "LF", "LF", "LF", "LF", "UP", "UP"],
    ["DW", "DW", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "DW", "RD", "RD", "UP", "RH", "TL", "RH", "RH", "RH", "RH", "UP", "UP"],
    ["DW", "DW", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "UP", "RH", "TL", "RH", "RH", "RH", "RH", "UP", "UP"],
    ["DW", "DW", "BL", "BL", "BL", "BL", "DW", "DW", "BL", "BL", "PK", "BL", "DW", "DW", "UP", "UP", "BL", "BL", "TL", "TL", "BL", "BL", "UP", "UP"],
    ["TL", "TL", "BL", "PK", "BL", "BL", "DW", "DW", "BL", "BL", "BL", "BL", "DW", "DW", "UP", "UP", "BL", "PK", "UP", "UP", "BL", "BL", "UP", "UP"],
    ["DW", "DW", "TL", "LF", "LF", "LF", "DW", "DW", "RH", "RH", "RH", "RH", "DW", "DW", "UP", "UP", "BL", "BL", "UP", "UP", "BL", "BL", "UP", "UP"],
    ["DW", "DW", "TL", "LF", "LF", "LF", "DW", "DW", "RH", "RH", "RH", "RH", "DW", "DW", "UP", "UP", "BL", "PK", "UP", "UP", "PK", "BL", "UP", "UP"],
    ["DW", "DW", "BL", "BL", "PK", "BL", "DW", "DW", "BL", "BL", "BL", "BL", "DW", "DW", "UP", "UP", "BL", "BL", "UP", "UP", "BL", "BL", "UP", "UP"],
    ["DW", "DW", "BL", "BL", "BL", "BL", "TL", "TL", "BL", "PK", "BL", "BL", "DW", "DW", "UP", "UP", "BL", "BL", "UP", "UP", "BL", "BL", "UP", "UP"],
    ["RH", "RH", "RH", "RH", "RH", "TL", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "UP", "UP"],
    ["RH", "RH", "RH", "RH", "RH", "TL", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "RH", "UP", "UP"]
]

parking_spots = {
    1: (2, 14),
    2: (3, 21),
    3: (3, 6),
    4: (4, 12),
    5: (4, 3),
    6: (5, 17),
    7: (8, 15),
    8: (9, 2),
    9: (10, 19),
    10: (10, 12),
    11: (10, 7),
    12: (17, 21),
    13: (17, 6),
    14: (17, 4),
    15: (20, 18),
    16: (20, 15),
    17: (20, 4),
}

street_directions = {

    # Salida de estacionamientos
    (2, 14): ["LF"],  # P1
    (3, 21): ["UP"],  # P2
    (3, 6): ["DW"],  # P3
    (4, 12): ["DW"],  # P4
    (4, 3): ["UP"],  # P5
    (5, 17): ["RH"],  # P6
    (8, 15): ["LF"],  # P7
    (9, 2): ["DW"],  # P8
    (10, 19): ["DW"],  # P9
    (10, 12): ["DW"],  # P10
    (10, 7): ["UP"],  # P11
    (17, 21): ["UP"],  # P12
    (17, 6): ["RH"],  # P13
    (17, 4): ["RH"],  # P14
    (20, 18): ["DW"],  # P15
    (20, 15): ["UP"],  # P16
    (20, 4): ["LF"],  # P17


    # Calle de hasta abajo 1
    (0, 0): ["RH"], (1, 0): ["RH"], (2, 0): ["RH", "UP"], (3, 0): ["RH", "UP"],
    (4, 0): ["RH", "UP"], (5, 0): ["RH", "UP"], (6, 0): ["RH", "UP"], (7, 0): ["RH", "UP"],
    (8, 0): ["RH", "UP"], (9, 0): ["RH", "UP"], (10, 0): ["RH", "UP"], (11, 0): ["RH", "UP"],
    (12, 0): ["RH", "UP"], (13, 0): ["RH", "UP"], (14, 0): ["RH", "UP"], (15, 0): ["RH", "UP"],
    (16, 0): ["RH", "UP"], (17, 0): ["RH", "UP"], (18, 0): ["RH", "UP"], (19, 0): ["RH", "UP"],
    (20, 0): ["RH", "UP"], (21, 0): ["RH", "UP"], (22, 0): ["RH", "UP"], (23, 0): ["UP"],

    # Calle de hasta abajo 2
    (0, 1): ["RH", "DW"], (1, 1): ["RH", "DW"], (2, 1): ["RH", "DW"], (3, 1): ["RH", "DW"],
    (4, 1): ["RH", "DW"], (5, 1): ["RH", "DW"], (6, 1): ["RH", "DW"], (7, 1): ["RH", "DW"],
    (8, 1): ["RH", "DW"], (9, 1): ["RH", "UP", "DW"], (10, 1): ["RH", "DW"], (11, 1): ["RH", "DW"],
    (12, 1): ["RH", "DW"], (13, 1): ["RH", "DW"], (14, 1): ["RH", "UP"], (15, 1): ["RH", "UP"],
    (16, 1): ["RH", "DW"], (17, 1): ["RH", "DW"], (18, 1): ["RH", "UP"], (19, 1): ["RH", "UP"],
    (20, 1): ["RH", "DW"], (21, 1): ["RH", "DW"], (22, 1): ["RH", "UP"], (23, 1): ["UP"],

    # Calle de la izquierda 1
    (0, 2): ["DW", "RH"], (0, 3): ["DW", "RH"],
    (0, 4): ["DW"], (0, 5): ["DW"], (0, 6): ["DW", "RH"], (0, 7): ["DW", "RH"],
    (0, 8): ["DW", "RH"], (0, 9): ["DW", "RH"], (0, 10): ["DW"], (0, 11): ["DW"],
    (0, 12): ["DW", "RH"], (0, 13): ["DW", "RH"], (0, 14): ["DW", "RH"], (0, 15): ["DW", "RH"],
    (0, 16): ["DW", "RH"], (0, 17): ["DW", "RH"], (0, 18): ["DW", "RH"], (0, 19): ["DW", "RH"],
    (0, 20): ["DW", "RH"], (0, 21): ["DW", "RH"], (0, 22): ["DW"], (0, 23): ["DW"],

    # Calle izquierda 2
    (1, 2): ["DW", "LF"], (1, 3): ["DW", "LF"],
    (1, 4): ["DW", "LF"], (1, 5): ["DW", "LF"], (1, 6): ["DW", "LF"], (1, 7): ["DW", "LF"],
    (1, 8): ["DW", "RH"], (1, 9): ["DW", "RH"], (1, 10): ["DW", "LF"], (1, 11): ["DW", "LF"],
    (1, 12): ["DW", "LF"], (1, 13): ["DW", "LF"], (1, 14): ["DW", "RH", "LF"], (1, 15): ["DW", "LF"],
    (1, 16): ["DW", "LF"], (1, 17): ["DW", "LF"], (1, 18): ["DW", "LF"], (1, 19): ["DW", "LF"],
    (1, 20): ["DW", "LF"], (1, 21): ["DW", "LF"], (1, 22): ["DW", "LF"], (1, 23): ["DW", "LF"],

    # Calle Superior 1
    (2, 23): ["LF", "DW"], (3, 23): ["LF", "DW"], (4, 23): ["LF", "DW"], (5, 23): ["LF", "DW"],
    (6, 23): ["LF"], (7, 23): ["LF"], (8, 23): ["LF", "DW"], (9, 23): ["LF", "DW"],
    (10, 23): ["LF", "DW"], (11, 23): ["LF", "DW"], (12, 23): ["LF", "DW"], (13, 23): ["LF", "DW"],
    (14, 23): ["LF"], (15, 23): ["LF"], (16, 23): ["LF", "DW"], (17, 23): ["LF", "DW"], (18, 23): ["LF", "DW"],
    (19, 23): ["LF", "DW"], (20, 23): ["LF", "DW"], (21, 23): ["LF", "DW"], (22, 23): ["LF"], (23, 23): ["LF"],

    # Calle Superior 2
    (2, 22): ["LF", "UP"], (3, 22): ["LF", "DW", "UP"], (4, 22): ["LF", "UP"], (5, 22): ["LF", "UP"],
    (6, 22): ["LF", "UP"], (7, 22): ["LF", "UP"], (8, 22): ["LF", "UP"], (9, 22): ["LF", "UP"],
    (10, 22): ["LF", "UP"], (11, 22): ["LF", "UP"], (12, 22): ["LF", "DW", "UP"], (13, 22): ["LF", "DW", "UP"],
    (14, 22): ["LF", "UP"], (15, 22): ["LF", "UP"], (16, 22): ["LF", "UP"], (17, 22): ["LF", "DW", "UP"], (18, 22): ["LF", "UP"],
    (19, 22): ["LF", "UP"], (20, 22): ["LF", "UP"], (21, 22): ["LF", "UP"], (22, 22): ["LF", "UP"], (23, 22): ["LF", "UP"],

    # Calle derecha 1
    (23, 2): ["UP", "LF"], (23, 3): ["UP", "LF"], (23, 4): ["UP", "LF"], (23, 5): ["UP", "LF"],
    (23, 6): ["UP", "LF"], (23, 7): ["UP", "LF"], (23, 8): ["UP"], (23, 9): ["UP"], (23, 10): ["UP", "LF"], (23, 11): ["UP", "LF"],
    (23, 12): ["UP", "LF"], (23, 13): ["UP", "LF"], (23, 14): ["UP", "LF"], (23, 15): ["UP", "LF"], (23, 16): ["UP", "LF"], (23, 17): ["UP", "LF"], (23, 18): ["UP", "LF"],
    (23, 19): ["UP", "LF"], (23, 20): ["UP", "LF"], (23, 21): ["UP", "LF"],

    # Calle derecha 2
    (22, 2): ["UP", "RH"], (22, 3): ["UP", "RH"], (22, 4): ["UP", "RH"], (22, 5): ["UP", "RH"],
    (22, 6): ["UP", "RH"], (22, 7): ["UP", "RH"], (22, 8): ["UP", "RH"], (22, 9): ["UP", "RH"], (22, 10): ["UP", "LF"], (22, 11): ["UP", "LF"],
    (22, 12): ["UP", "RH"], (22, 13): ["UP", "RH"], (22, 14): ["UP", "RH"], (22, 15): ["UP", "RH"], (22, 16): ["UP", "LF"], (22, 17): ["UP", "LF"], (22, 18): ["UP", "RH"],
    (22, 19): ["UP", "RH"], (22, 20): ["UP", "RH"], (22, 21): ["UP", "RH"],

    # ! Faltan dobles direcciónes de aquí en adelante
    # Seccion 1
    (2, 5): ["LF"], (3, 5): ["LF", "UP"], (4, 5): ["LF"], (5, 5): ["LF"],
    (2, 4): ["LF"], (3, 4): ["LF"], (4, 4): ["LF", "DW"], (5, 4): ["LF"],

    # Seccion 2
    (6, 7): ["DW"], (6, 6): ["DW"], (6, 5): ["DW", "LF"], (6, 4): ["DW", "LF"], (6, 3): ["DW"], (6, 2): ["DW"],
    (7, 7): ["DW"], (7, 6): ["DW"], (7, 5): ["DW", "RH"], (7, 4): ["DW", "RH"], (7, 3): ["DW"], (7, 2): ["DW"],

    # Seccion 3
    (8, 5): ["RH"], (9, 5): ["RH"], (10, 5): ["RH"], (11, 5): ["RH"],
    (8, 4): ["RH"], (9, 4): ["RH"], (10, 4): ["RH"], (11, 4): ["RH"],

    # Seccion 4
    (12, 7): ["DW"], (12, 6): ["DW"], (12, 5): ["DW"], (12, 4): ["DW"], (12, 3): ["DW"], (12, 2): ["DW"],
    (13, 7): ["DW"], (13, 6): ["DW"], (13, 5): ["DW"], (13, 4): ["DW"], (13, 3): ["DW"], (13, 2): ["DW"],

    # Seccion 5
    (14, 7): ["UP"], (14, 6): ["UP"], (14, 5): ["UP"], (14, 4): ["UP"], (14, 3): ["UP"], (14, 2): ["UP"],
    (15, 7): ["UP"], (15, 6): ["UP"], (15, 5): ["UP"], (15, 4): ["UP"], (15, 3): ["UP"], (15, 2): ["UP"],

    # Seccion 6
    (18, 7): ["UP"], (18, 6): ["UP", "LF"], (18, 5): ["UP"], (18, 4): ["UP", "LF"], (18, 3): ["UP"], (18, 2): ["UP"],
    (19, 7): ["UP"], (19, 6): ["UP"], (19, 5): ["UP"], (19, 4): ["UP", "RH"], (19, 3): ["UP", "RH"], (19, 2): ["UP"],

    # Seccion 7
    (2, 9): ["RH"], (3, 9): ["RH"], (4, 9): ["RH"], (5, 9): ["RH"],
    (2, 8): ["RH"], (3, 8): ["RH"], (4, 8): ["RH"], (5, 8): ["RH"],

    # Seccion 8
    (2, 11): ["LF"], (3, 11): ["LF"], (4, 11): ["LF", "UP"], (5, 11): ["LF"],
    (2, 10): ["LF"], (3, 10): ["LF"], (4, 10): ["LF"], (5, 10): ["LF"],

    # Seccion 9
    (8, 9): ["RH"], (9, 9): ["RH"], (10, 9): ["RH"], (11, 9): ["RH"],
    (8, 8): ["RH"], (9, 8): ["RH"], (10, 8): ["RH", "DW"], (11, 8): ["RH"],

    # Seccion 10
    (8, 11): ["LF"], (9, 11): ["LF"], (10, 11): ["LF", "UP"], (11, 11): ["LF"],
    (8, 10): ["LF"], (9, 10): ["LF"], (10, 10): ["LF"], (11, 10): ["LF"],

    # Seccion 11
    (16, 9): ["RH"], (17, 9): ["RH"], (18, 9): ["RH"], (19, 9): ["RH"], (20, 9): ["RH"], (21, 9): ["RH"],
    (16, 8): ["RH"], (17, 8): ["RH"], (18, 8): ["RH"], (19, 8): ["RH"], (20, 8): ["RH"], (21, 8): ["RH"],

    # Seccion 12
    (16, 11): ["LF"], (17, 11): ["LF"], (18, 11): ["LF"], (19, 11): ["LF"], (20, 11): ["LF"], (21, 11): ["LF"],
    (16, 10): ["LF"], (17, 10): ["LF"], (18, 10): ["LF"], (19, 10): ["LF"], (20, 10): ["LF"], (21, 10): ["LF"],

    # Seccion 13
    (6, 21): ["UP"], (6, 20): ["UP"], (6, 19): ["UP"], (6, 18): ["UP"], (6, 17): ["UP", "LF"], (6, 16): ["UP"], (6, 15): ["UP"],
    (6, 14): ["UP"], (6, 13): ["UP"], (6, 12): ["UP"],
    (7, 21): ["UP"], (7, 20): ["UP"], (7, 19): ["UP"], (7, 18): ["UP"], (7, 17): ["UP"], (7, 16): ["UP"], (7, 15): ["UP", "RH"],
    (7, 14): ["UP"], (7, 13): ["UP"], (7, 12): ["UP"],

    # Seccion 14
    (8, 18): ["LF"], (9, 18): ["LF"], (10, 18): ["LF", "UP"], (11, 18): ["LF"],
    (8, 17): ["LF"], (9, 17): ["LF"], (10, 17): ["LF"], (11, 17): ["LF"],

    # Seccion 15
    (16, 17): ["LF"], (17, 17): ["LF"], (18, 17): ["LF"], (19, 17): ["LF", "DW"], (20, 17): ["LF", "UP"], (21, 17): ["LF"],
    (16, 16): ["LF"], (17, 16): ["LF"], (18, 16): ["LF"], (19, 16): ["LF"], (20, 16): ["LF", "DW"], (21, 16): ["LF"],

    # Seccion 16
    (12, 21): ["DW"], (12, 20): ["DW"], (12, 19): ["DW"],
    (13, 21): ["DW"], (13, 20): ["DW"], (13, 19): ["DW"],

    # Seccion 17
    (14, 21): ["UP"], (14, 20): ["UP"], (14, 19): ["UP"],
    (15, 21): ["UP"], (15, 20): ["UP"], (15, 19): ["UP"],

    # Seccion 18
    (12, 16): ["DW"], (12, 15): ["DW"], (12, 14): ["DW"], (12, 13): ["DW"], (12, 12): ["DW"],
    (13, 16): ["DW"], (13, 15): ["DW"], (13, 14): ["DW"], (13, 13): ["DW"], (13, 12): ["DW"],

    # Seccion 19
    (14, 18): ["UP"], (14, 17): ["UP"], (14, 16): ["UP"], (14, 15): ["UP"], (14, 14): ["UP"], (14, 13): ["UP"], (14, 12): ["UP"],
    (15, 18): ["UP"], (15, 17): ["UP"], (15, 16): ["UP"], (15, 15): ["UP"], (15, 14): ["UP"], (15, 13): ["UP"], (15, 12): ["UP"],

    # Seccion 20
    (12, 18): ["DW", "LF"], (13, 18): ["DW", "LF"],
    (12, 17): ["DW", "LF"], (13, 17): ["DW", "LF"],

    # Seccion 21
    (6, 9): ["RH", "DW"], (7, 9): ["RH", "DW"],
    (6, 8): ["RH", "DW"], (7, 8): ["RH", "DW"],

    # Seccion 22
    (6, 11): ["UP", "LF"], (7, 11): ["UP", "LF"],
    (6, 10): ["UP", "LF"], (7, 10): ["UP", "LF"],

    # Seccion 23 Rotonda
    (12, 11): ["LF", "DW"], (12, 10): ["LF", "DW"], (12, 9): ["DW"], (12, 8): ["RH", "DW"],
    (13, 8): ["RH", "DW"], (14, 8): ["RH"], (15, 8): ["UP", "RH"], (15, 9): ["UP", "RH"],
    (15, 10): ["UP"], (15, 11): ["UP", "LF"], (14, 11): ["UP", "LF"], (13, 11): ["LF"]

}
