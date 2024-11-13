import mesa
from .model import CityModel, CarAgent, ParkingAgent, TrafficLightAgent, BuildingAgent

def circle_portrayal_example(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
    }

    if isinstance(agent, CarAgent):
        portrayal["Color"] = "Pink"
    elif isinstance(agent, ParkingAgent):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "w": 1.0,
            "h": 1.0,
            "Color": "Yellow",
            "text": str(agent.unique_id),
            "text_color": "Black"
        }
    elif isinstance(agent, BuildingAgent):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "w": 1.0,
            "h": 1.0,
            "Color": "Blue"  
        }
    elif isinstance(agent, TrafficLightAgent):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "w": 1.0,
            "h": 1.0,
            "Color": "Green"

        }

    return portrayal

# Parking spots
parking_positions = [
    (2, 14), # P1 
    (3, 21), # P2
    (3, 6),  #P3
    (4, 12), #P4
    (4, 3), #P5
    (5, 17), #P6
    (8, 15), #P7
    (9, 2), #P8
    (10, 19), #P9 
    (10, 12), #P10
    (10, 7), #P11
    (18, 21), #P12
    (18, 6), #P13
    (18, 4), #P14
    (21, 18), #P15
    (21, 15), #P16
    (21, 4) #P17
]

# Building spot
building_positions = [
    # Edificio 1
    (2 , 12), (3, 12), (5,12),
    (2 , 13), (3, 13), (4,13), (5,13),
    (3, 14), (4,14), (5,14),
    (2, 15), (3, 15), (4,15), (5, 15),
    (2, 16), (3, 16), (4,16), (5, 16),
    (2, 16), (3, 16), (4,16),
    (2, 17), (3, 17), (4,17),
    (2, 18), (3, 18), (4, 18), (5,18),
    (2, 19), (3, 19), (4, 19), (5,19),
    (2, 20), (3, 20), (4,20), (5, 20),
    (2, 21), (4, 21), (5, 21),

    #Edificio 2
    (8, 19),(9, 19), (11, 19),
    (8, 20),(9,20), (10,20), (11,20),
    (8, 21), (9, 21),(10, 21), (11,21),

    #Edificio 3
    (8, 16), (9, 16), (10, 16), (11,16),
    (9, 15), (10,15), (11, 15),
    (8, 14), (9, 14), (10, 14), (11,14),
    (8, 13), (9, 13), (10, 13), (11,13),
    (8, 12), (9, 12), (11,12),

    # Edificio 4
    (2, 2), (3, 2), (4, 2), (5, 2),
    (2, 3), (3, 3), (5, 3),

    # Edificio 5
    (2, 6), (4, 6), (5, 6),
    (2, 7), (3, 7), (4, 7), (5, 7),

    #Edificio 6
    (8, 2), (10, 2), (11, 2),
    (8, 3), (9, 3), (10, 3), (11, 3),

    # Edificio 7
    (8, 6), (9, 6), (10, 6), (11, 6),
    (8, 7), (9, 7), (11, 7),

    # Edifcio 8 
    (17, 21), (19, 21), (20, 21), (21, 21), (22, 21),
    (17, 20), (18, 20), (19, 20), (20, 20), (21, 20), (22, 20),
    (17, 19), (18, 19), (19, 19), (20, 19), (21, 19), (22, 19),
    (17, 18), (18, 18), (19, 18), (20, 18), (22, 18),

    # Edificio 9
    (17, 15), (18, 15), (19, 15), (20, 15), (22, 15),
    (17, 14), (18, 14), (19, 14), (20, 14), (21, 14), (22, 14),
    (17, 13), (18, 13), (19, 13), (20, 13), (21, 13), (22, 13),
    (17, 12), (18, 12), (19, 12), (20, 12), (21, 12), (22, 12),

    #Edificio 10
    (17, 7), (17, 6), (17, 5), (17, 4), (17, 3), (17, 2),
    (18, 7), (18, 5), (18, 3), (18, 2),

    #Edificio 11
    (21, 7), (21, 6), (21, 5), (21, 3), (21, 2),
    (22, 7), (22, 6), (22, 5), (22, 4), (22, 3), (22, 2),

]

traffic_lights_positions = [
    (1,1),
]

# Configurar los elementos de la visualización
canvas_element = mesa.visualization.CanvasGrid(
    circle_portrayal_example, 24, 24, 500, 500
)
chart_element = mesa.visualization.ChartModule([
    {"Label": "Car Count", "Color": "Pink"},
    {"Label": "Parking Count", "Color": "Yellow"},
    {"Label": "Building Count", "Color": "Blue"}
])

# Parámetros del modelo, incluyendo las posiciones de los estacionamientos y edificios
model_kwargs = {
    "num_agents": 1,
    "parking_positions": parking_positions,
    "building_positions": building_positions,
    "traffic_lights_positions": traffic_lights_positions,
    "width": 24,
    "height": 24
}

# Inicialización del servidor
server = mesa.visualization.ModularServer(
    CityModel,
    [canvas_element, chart_element],
    "Cityprojecta01750311",
    model_kwargs,
)
