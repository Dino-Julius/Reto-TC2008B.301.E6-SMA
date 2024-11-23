'''
Este archivo contiene funciones utilitarias para analizar la cuadrícula del entorno y los espacios de estacionamiento.
En Mesa, las celdas de la cuadrícula se indexan por [x, y], donde [0, 0] se asume que está en la esquina inferior izquierda y [width-1, height-1] en la esquina superior derecha.

Funciones incluidas:
- parse_environment: Analiza la cuadrícula del entorno y devuelve datos sobre carreteras, edificios, estacionamientos, semáforos y rotondas.
- find_parking_spots: Convierte un diccionario de espacios de estacionamiento en una lista de datos de espacios de estacionamiento.
'''

from enum import Enum


class Directions(Enum):
    '''
    Direcciones con un desplazamiento que funciona en un sistema de coordenadas natural
    '''

    UP = (0, 1)
    LF = (-1, 0)
    RH = (1, 0)
    DW = (0, -1)


class RawDirections(Enum):
    '''
    El desplazamiento ya está ajustado para funcionar con una matriz de la forma [fila][columna]
    '''

    UP = (-1, 0)
    LF = (0, -1)
    RH = (0, 1)
    DW = (1, 0)

def parse_environment(environment: list):
    '''
    Analiza la cuadrícula del entorno y devuelve datos sobre carreteras, edificios, espacios de estacionamiento, semáforos y rotondas.
    Args:
        environment (list): Una lista 2D que representa el entorno de la ciudad.
    Returns:
        tuple: Una tupla que contiene listas de datos de carreteras, edificios, estacionamientos, semáforos y rotondas.
    '''
    
    road_data = []
    building_data = []
    parking_data = []
    traffic_light_data = []
    roundabout_data = []
    n_rows = len(environment)
    n_cols = len(environment[0])

    for row_index in range(n_rows):
        for col_index in range(n_cols):
            cell = environment[row_index][col_index]
            # ! for vizualization of the original grid [starts on 1, 1]
            #  data = {"x": col_index + 1, "y": row_index + 1}
            data = {"x": col_index, "y": n_rows - row_index - 1}

            if cell in [direction.name for direction in Directions]:
                data["direction"] = cell
                road_data.append(data)

            elif cell == "BL":  # Building
                building_data.append(data)

            elif cell == "PK":  # Parking
                parking_data.append(data)

            elif cell == "TL":  # Traffic Light
                traffic_light_data.append(data)

            elif cell == "RD":
                roundabout_data.append(data)

    return road_data, building_data, parking_data, traffic_light_data, roundabout_data


def find_parking_spots(parking_spots: dict):
    '''
    Convierte un diccionario de espacios de estacionamiento en una lista de datos de espacios de estacionamiento.
    Args:
        parking_spots (dict): Un diccionario que contiene los IDs de los espacios de estacionamiento y sus correspondientes filas y columnas.
    Returns:
        list: Una lista de datos de espacios de estacionamiento con IDs, filas y columnas.
    '''

    parking_data = []
    for spot_id, (row, col) in parking_spots.items():
        data = {"id": spot_id, "x": row, "y": col}
        parking_data.append(data)
    return parking_data
