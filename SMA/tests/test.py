"""
Código para realizar pruebas de las funciones de parseo de datos y búsqueda de estacionamientos.
"""

import sys
import os

# Agregar la ruta al directorio raíz del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import networkx as nx
import matplotlib.pyplot as plt
from model.environment import CITY, parking_spots, street_directions
from model.model import parse_environment, find_parking_spots
from model.utils import Directions, RawDirections

# Parse the environment
# road_data, building_data, parking_data, traffic_light_data, roundabout_data = parse_environment(CITY)

# Parse the parking spots
# parsed_parking_spots = find_parking_spots(parking_spots)

# print("Road Data:", road_data)
# print()
# print("Building Data:", building_data)
# print()
# print("Parking Data:", parking_data)
# print()
# print("Traffic Light Data:", traffic_light_data)
# print()
# print("Roundabout Data:", roundabout_data)
# print()
# print("Parsed Parking Spots:", parsed_parking_spots)
# print()
# print("Parking Spots:", parking_spots)
# print()

# for i, traffic_light in enumerate(traffic_light_data):
#     initial_state = "green" if i % 4 < 2 else "red"
#     print(f"Traffic Light {i}: {(traffic_light["x"], traffic_light["y"])} -> {initial_state}")
#     print()


# def get_direction(pos, direction):
#     x, y = pos
#     if direction in Directions._member_names_:
#         dx, dy = Directions[direction].value
#         return x + dx, y + dy

# # if "DW" in [direction.name for direction in Directions]:
# #     print(Directions.DW.value[0], Directions.DW.value[1])

# print(get_direction((0, 0), "DW"))
# print(get_direction((1, 1), "RH"))


def build_graph(street_directions):
    G = nx.DiGraph()
    for position, directions in street_directions.items():
        for direction in directions:
            dx, dy = Directions[direction].value
            neighbor = (position[0] + dx, position[1] + dy)
            if neighbor in street_directions:
                G.add_edge(position, neighbor, direction=direction)
    return G


def get_directions_from_path(path):
    directions = []
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        dx = next_node[0] - current[0]
        dy = next_node[1] - current[1]
        for direction, member in Directions.__members__.items():
            dir_dx, dir_dy = member.value
            if (dx, dy) == (dir_dx, dir_dy):
                directions.append(direction)
                break
    return directions

# Construye el grafo
G = build_graph(street_directions)

source = (17, 21)
target = (9, 2)
try:
    shortest_path = nx.shortest_path(G, source=source, target=target)
    print("Camino más corto:", shortest_path)
    directions = get_directions_from_path(shortest_path)
    print("Direcciones del camino más corto:", directions)
except nx.NetworkXNoPath:
    print(f"No hay camino entre {source} y {target}")

# Ajusta el tamaño de la figura
plt.figure(figsize=(12, 12))  # Cambia los valores según sea necesario

# Posiciones de los nodos
pos = {node: node for node in G.nodes()}

# Dibuja los nodos
nx.draw_networkx_nodes(G, pos, node_size=12, node_color='green')

# Dibuja las aristas con flechas
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=15)

# Dibuja las etiquetas con un tamaño de fuente más pequeño
# nx.draw_networkx_labels(G, pos, font_size=8)

# # Ajusta los textos para evitar sobreposición
# texts = []
# for nodo, (x, y) in pos.items():
#     texts.append(plt.text(x, y, str(nodo), fontsize=8))
# adjust_text(texts, arrowprops=dict(arrowstyle='->', color='black'))

# Resalta el camino más corto
if 'shortest_path' in locals():
    path_edges = list(zip(shortest_path, shortest_path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='red', node_size=20)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', arrowsize=12)

# Configuraciones adicionales
plt.gca()
plt.axis('equal')
plt.show()


# # Supongamos que ya has construido el grafo G
# G = build_graph(street_directions)

# # Calcula el camino más corto entre los dos puntos
# shortest_path = nx.shortest_path(G, source=(2, 14), target=(20, 4))

# print("Camino más corto:", shortest_path)

# # Posiciones de los nodos para el plot
# pos = {node: node for node in G.nodes()}

# # Dibuja todos los nodos
# nx.draw_networkx_nodes(G, pos, node_size=20, node_color='lightblue')

# # Dibuja todas las aristas
# nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10, edge_color='gray')

# # Prepara las aristas del camino más corto
# path_edges = list(zip(shortest_path, shortest_path[1:]))

# # Dibuja las aristas del camino más corto en rojo
# nx.draw_networkx_edges(G, pos, edgelist=path_edges, arrowstyle='->', arrowsize=15, edge_color='red', width=2)

# # Dibuja los nodos del camino más corto en rojo
# nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_size=50, node_color='red')

# # Agrega etiquetas con las coordenadas de los nodos
# labels = {node: str(node) for node in G.nodes()}
# nx.draw_networkx_labels(G, pos, labels, font_size=8)

# # Ajusta la visualización
# plt.gca()
# plt.axis('equal')
# plt.show()