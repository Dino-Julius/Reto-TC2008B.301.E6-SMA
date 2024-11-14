import mesa
from .model import CityModel, CarAgent, ParkingAgent, TrafficLightAgent, BuildingAgent, RoundaboutAgent
from mesa.visualization.modules import TextElement

# Definir el TextElement para mostrar el mensaje de salida y destino de cada agente
class AgentMessageElement(mesa.visualization.TextElement):
    def __init__(self):
        super().__init__()

    def render(self, model):
        # Recupera y devuelve los mensajes de los agentes
        return model.get_agent_messages()

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
            "Color": "Green" if agent.state == "verde" else "Red"  # Cambiar color basado en el estado
        }
    elif isinstance(agent, RoundaboutAgent):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "w": 1.0,
            "h": 1.0,
            "Color": "Brown"
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
    (17, 21), #P12
    (17, 6), #P13
    (17, 4), #P14
    (20, 18), #P15
    (20, 15), #P16
    (20, 4) #P17
]

# Building spots
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
    (16, 21), (18, 21), (19, 21), (20, 21), (21, 21),
    (16, 20), (17, 20), (18, 20), (19, 20), (20, 20), (21, 20),
    (16, 19), (17, 19), (18, 19), (19, 19), (20, 19), (21, 19),
    (16, 18), (17, 18), (18, 18), (19, 18), (21, 18),

    # Edificio 9
    (16, 15), (17, 15), (18, 15), (19, 15), (21, 15),
    (16, 14), (17, 14), (18, 14), (19, 14), (20, 14), (21, 14),
    (16, 13), (17, 13), (18, 13), (19, 13), (20, 13), (21, 13),
    (16, 12), (17, 12), (18, 12), (19, 12), (20, 12), (21, 12),

    #Edificio 10
    (16, 7), (16, 6), (16, 5), (16, 4), (16, 3), (16, 2),
    (17, 7), (17, 5), (17, 3), (17, 2),

    #Edificio 11
    (20, 7), (20, 6), (20, 5), (20, 3), (20, 2),
    (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (21, 2),

]

traffic_lights_positions = [
    (6,2),(7,2), #Verde
    (2,5), (2,4), #Rojo
    (0,6),(1,6), #Verde
    (5,1), (5,0), #Rojo
    (6,16),(7,16), #Verde
    (17,9),(17,8), #Rojo
    (6,21),(7,21), #Verde
    (8,18),(8,17), #Rojo
    (18,7),(19,7), #Verde
    (8,23),(8,22) #Rojo
]

roundabout_positions = [
    (13, 9), (14, 9), (13,10), (14,10)

]

street_directions = {

    #Salida de estacionamientos
    (2, 14): ["Oeste"], # P1 
    (3, 21): ["Norte"], # P2
    (3, 6): ["Sur"],  #P3
    (4, 12): ["Sur"], #P4
    (4, 3): ["Norte"], #P5
    (5, 17): ["Este"], #P6
    (8, 15): ["Oeste"], #P7
    (9, 2): ["Sur"], #P8
    (10, 19): ["Sur"], #P9 
    (10, 12): ["Sur"], #P10
    (10, 7): ["Norte"], #P11
    (17, 21): ["Norte"], #P12
    (17, 6): ["Este"], #P13
    (17, 4): ["Este"], #P14
    (20, 18): ["Sur"], #P15
    (20, 15): ["Norte"], #P16
    (20, 4): ["Oeste"], #P17


    # Calle de hasta abajo 1
    (0, 0): ["Este"], (1, 0): ["Este"], (2, 0): ["Este"], (3, 0): ["Este"], 
    (4, 0): ["Este"], (5, 0): ["Este"], (6, 0): ["Este"], (7, 0): ["Este"],
    (8, 0): ["Este"], (9, 0): ["Este"], (10, 0): ["Este"], (11, 0): ["Este"],
    (12, 0): ["Este"], (13, 0): ["Este"], (14, 0): ["Este", "Norte"], (15, 0): ["Este", "Norte"],
    (16, 0): ["Este"], (17, 0): ["Este"], (18, 0): ["Este", "Norte"], (19, 0): ["Este", "Norte"],
    (20, 0): ["Este"], (21, 0): ["Este"], (22, 0): ["Este", "Norte"], (23, 0): ["Norte"],

    # Calle de hasta abajo 2
    (0, 1): ["Este", "Sur"], (1, 1): ["Este", "Sur"], (2, 1): ["Este"], (3, 1): ["Este"], 
    (4, 1): ["Este"], (5, 1): ["Este"], (6, 1): ["Este"], (7, 1): ["Este"],
    (8, 1): ["Este"], (9, 1): ["Este", "Norte"], (10, 1): ["Este"], (11, 1): ["Este"],
    (12, 1): ["Este"], (13, 1): ["Este"], (14, 1): ["Este", "Norte"], (15, 1): ["Este", "Norte"],
    (16, 1): ["Este"], (17, 1): ["Este"], (18, 1): ["Este", "Norte"], (19, 1): ["Este", "Norte"],
    (20, 1): ["Este"], (21, 1): ["Este"], (22, 1): ["Este", "Norte"], (23, 1): ["Norte"],

    # Calle de la izquierda 1
    (0, 2): ["Sur"], (0, 3): ["Sur"],
    (0, 4): ["Sur"], (0, 5): ["Sur"], (0, 6): ["Sur"], (0, 7): ["Sur"],
    (0, 8): ["Sur"], (0, 9): ["Sur"], (0, 10): ["Sur"], (0, 11): ["Sur"],
    (0, 12): ["Sur"], (0, 13): ["Sur"], (0, 14): ["Sur"], (0, 15): ["Sur"],
    (0, 16): ["Sur"], (0, 17): ["Sur"], (0, 18): ["Sur"], (0, 19): ["Sur"],
    (0, 20): ["Sur"], (0, 21): ["Sur"], (0, 22): ["Sur"], (0, 23): ["Sur"],

    # Calle izquierda 2
    (1, 2): ["Sur"], (1, 3): ["Sur"],
    (1, 4): ["Sur"], (1, 5): ["Sur"], (1, 6): ["Sur"], (1, 7): ["Sur"],
    (1, 8): ["Sur", "Este"], (1, 9): ["Sur", "Este"], (1, 10): ["Sur"], (1, 11): ["Sur"],
    (1, 12): ["Sur"], (1, 13): ["Sur"], (1, 14): ["Sur", "Este"], (1, 15): ["Sur"],
    (1, 16): ["Sur"], (1, 17): ["Sur"], (1, 18): ["Sur"], (1, 19): ["Sur"],
    (1, 20): ["Sur"], (1, 21): ["Sur"], (1, 22): ["Sur", "Oeste"], (1, 23): ["Sur", "Oeste"],

    #Calle Superior 1
    (2,23): ["Oeste"], (3,23): ["Oeste"], (4,23): ["Oeste"], (5,23): ["Oeste"],
    (6,23): ["Oeste"], (7,23): ["Oeste"], (8,23): ["Oeste"], (9,23): ["Oeste"],
    (10,23): ["Oeste"], (11,23): ["Oeste"], (12, 23): ["Oeste", "Sur"], (13,23): ["Oeste", "Sur"],
    (14,23): ["Oeste"], (15,23): ["Oeste"], (16,23): ["Oeste"], (17,23): ["Oeste"], (18,23): ["Oeste"],
    (19,23): ["Oeste"], (20,23): ["Oeste"], (21,23): ["Oeste"], (22,23): ["Oeste"], (23,23): ["Oeste"],

    #Calle Superior 2
    (2,22): ["Oeste"], (3,22): ["Oeste", "Sur"], (4,22): ["Oeste"], (5,22): ["Oeste"],
    (6,22): ["Oeste"], (7,22): ["Oeste"], (8,22): ["Oeste"], (9,22): ["Oeste"],
    (10,22): ["Oeste"], (11,22): ["Oeste"], (12, 22): ["Oeste", "Sur"], (13,22): ["Oeste", "Sur"],
    (14,22): ["Oeste"], (15,22): ["Oeste"], (16,22): ["Oeste"], (17,22): ["Oeste", "Sur"], (18,22): ["Oeste"],
    (19,22): ["Oeste"], (20,22): ["Oeste"], (21,22): ["Oeste"], (22,22): ["Oeste", "Norte"], (23,22): ["Oeste", "Norte"],

    #Calle derecha 1
    (23,2): ["Norte"], (23,3): ["Norte"], (23,4): ["Norte"], (23,5): ["Norte"],
    (23,6): ["Norte"], (23,7): ["Norte"], (23,8): ["Norte"], (23,9): ["Norte"], (23,10): ["Norte", "Oeste"],(23,11): ["Norte", "Oeste"],
    (23,12): ["Norte"],(23,13): ["Norte"], (23,14): ["Norte"], (23,15): ["Norte"], (23,16): ["Norte", "Oeste"], (23,17): ["Norte", "Oeste"], (23,18): ["Norte"],
    (23,19): ["Norte"], (23,20): ["Norte"], (23,21): ["Norte"],

    #Calle derecha 2
    (22,2): ["Norte"], (22,3): ["Norte"], (22,4): ["Norte"], (22,5): ["Norte"],
    (22,6): ["Norte"], (22,7): ["Norte"], (22,8): ["Norte"], (22,9): ["Norte"], (22,10): ["Norte", "Oeste"],(22,11): ["Norte", "Oeste"],
    (22,12): ["Norte"],(22,13): ["Norte"], (22,14): ["Norte"], (22,15): ["Norte"], (22,16): ["Norte", "Oeste"], (22,17): ["Norte", "Oeste"], (22,18): ["Norte"],
    (22,19): ["Norte"], (22,20): ["Norte"], (22,21): ["Norte"],

    #Seccion 1
    (2,5): ["Oeste"], (3,5): ["Oeste", "Norte"], (4,5): ["Oeste"], (5,5): ["Oeste"],
    (2,4): ["Oeste"], (3,4): ["Oeste"], (4,4): ["Oeste", "Sur"], (5,4): ["Oeste"],

    #Seccion 2
    (6,7): ["Sur"], (6,6): ["Sur"], (6,5): ["Sur", "Oeste"], (6,4): ["Sur", "Oeste"], (6,3): ["Sur"], (6,2): ["Sur"],
    (7,7): ["Sur"], (7,6): ["Sur"], (7,5): ["Sur", "Este"], (7,4): ["Sur", "Este"], (7,3): ["Sur"], (7,2): ["Sur"],

    #Seccion 3
    (8,5): ["Este"], (9,5): ["Este"], (10,5): ["Este"], (11,5): ["Este"],
    (8,4): ["Este"], (9,4): ["Este"], (10,4): ["Este"], (11,4): ["Este"],

    #Seccion 4 
    (12, 7): ["Sur"], (12, 6): ["Sur"], (12, 5): ["Sur"], (12, 4): ["Sur"], (12, 3): ["Sur"], (12, 2): ["Sur"],
    (13, 7): ["Sur"], (13, 6): ["Sur"], (13, 5): ["Sur"], (13, 4): ["Sur"], (13, 3): ["Sur"], (13, 2): ["Sur"],

    #Seccion 5
    (14, 7): ["Norte"], (14, 6): ["Norte"], (14, 5): ["Norte"], (14, 4): ["Norte"], (14, 3): ["Norte"], (14, 2): ["Norte"],
    (15, 7): ["Norte"], (15, 6): ["Norte"], (15, 5): ["Norte"], (15, 4): ["Norte"], (15, 3): ["Norte"], (15, 2): ["Norte"],

    #Seccion 6
    (18, 7): ["Norte"], (18, 6): ["Norte", "Oeste"], (18, 5): ["Norte"], (18, 4): ["Norte", "Oeste"], (18, 3): ["Norte"], (18, 2): ["Norte"],
    (19, 7): ["Norte"], (19, 6): ["Norte"], (19, 5): ["Norte"], (19, 4): ["Norte"], (19, 3): ["Norte", "Este"], (19, 2): ["Norte"],

    #Seccion 7
    (2, 9): ["Este"], (3, 9): ["Este"], (4, 9): ["Este"], (5, 9): ["Este"],
    (2, 8): ["Este"], (3, 8): ["Este"], (4, 8): ["Este"], (5, 8): ["Este"],

    #Seccion 8
    (2,11): ["Oeste"], (3,11): ["Oeste"], (4,11): ["Oeste", "Norte"], (5,11): ["Oeste"],
    (2,10): ["Oeste"], (3,10): ["Oeste"], (4,10): ["Oeste"], (5,10): ["Oeste"],

    #Seccion 9
    (8, 9): ["Este"], (9, 9): ["Este"], (10, 9): ["Este"], (11, 9): ["Este"],
    (8, 8): ["Este"], (9, 8): ["Este"], (10, 8): ["Este", "Sur"], (11, 8): ["Este"],

    #Seccion 10
    (8,11): ["Oeste"], (9,11): ["Oeste"], (10,11): ["Oeste", "Norte"], (11,11): ["Oeste"],
    (8,10): ["Oeste"], (9,10): ["Oeste"], (10,10): ["Oeste"], (11,10): ["Oeste"],

    #Seccion 11
    (16, 9): ["Este"], (17, 9): ["Este"], (18, 9): ["Este"], (19, 9): ["Este"], (20, 9): ["Este"], (21, 9): ["Este"],
    (16, 8): ["Este"], (17, 8): ["Este"], (18, 8): ["Este"], (19, 8): ["Este"], (20, 8): ["Este"], (21, 8): ["Este"],

    #Seccion 12
    (16,11): ["Oeste"], (17,11): ["Oeste"], (18,11): ["Oeste"], (19,11): ["Oeste"],(20,11): ["Oeste"],(21,11): ["Oeste"],
    (16,10): ["Oeste"], (17,10): ["Oeste"], (18,10): ["Oeste"], (19,10): ["Oeste"],(20,10): ["Oeste"],(21,10): ["Oeste"],

    #Seccion 13
    (6,21): ["Norte"], (6,20): ["Norte"], (6,19): ["Norte"], (6,18): ["Norte"], (6,17): ["Norte", "Oeste"], (6,16): ["Norte"],(6,15): ["Norte"],
    (6,14): ["Norte"], (6,13): ["Norte"], (6,12): ["Norte"],
    (7,21): ["Norte"], (7,20): ["Norte"], (7,19): ["Norte"], (7,18): ["Norte"], (7,17): ["Norte"], (7,16): ["Norte"],(7,15): ["Norte", "Este"],
    (7,14): ["Norte"], (7,13): ["Norte"], (7,12): ["Norte"],

    #Seccion 14
    (8,18): ["Oeste"], (9,18): ["Oeste"], (10,18): ["Oeste", "Norte"], (11,18): ["Oeste"],
    (8,17): ["Oeste"], (9,17): ["Oeste"], (10,17): ["Oeste"], (11,17): ["Oeste"],

    #Seccion 15
    (16,17): ["Oeste"], (17,17): ["Oeste"], (18,17): ["Oeste"], (19,17): ["Oeste", "Sur"],(20,17): ["Oeste", "Norte"],(21,17): ["Oeste"],
    (16,16): ["Oeste"], (17,16): ["Oeste"], (18,16): ["Oeste"], (19,16): ["Oeste"],(20,16): ["Oeste"],(21,16): ["Oeste"],

    #Seccion 16
    (12,21): ["Sur"], (12,20): ["Sur"], (12,19): ["Sur"],
    (13,21): ["Sur"], (13,20): ["Sur"], (13,19): ["Sur"],

    #Seccion 17
    (14,21): ["Norte"], (14,20): ["Norte"], (14,19): ["Norte"],
    (15,21): ["Norte"], (15,20): ["Norte"], (15,19): ["Norte"],

    #Seccion 18
    (12, 16): ["Sur"], (12, 15): ["Sur"], (12, 14): ["Sur"], (12, 13): ["Sur"], (12, 12): ["Sur"],
    (13, 16): ["Sur"], (13, 15): ["Sur"], (13, 14): ["Sur"], (13, 13): ["Sur"], (13, 12): ["Sur"],

    #Seccion 19
    (14, 18): ["Norte"], (14, 17): ["Norte"], (14, 16): ["Norte"], (14, 15): ["Norte"], (14, 14): ["Norte"], (14, 13): ["Norte"], (14, 12): ["Norte"],
    (15, 18): ["Norte"], (15, 17): ["Norte"], (15, 16): ["Norte"], (15, 15): ["Norte"], (15, 14): ["Norte"], (15, 13): ["Norte"], (15, 12): ["Norte"],

    #Seccion 20
    (12,18): ["Sur", "Oeste"], (13,18): ["Sur", "Oeste"],
    (12,17): ["Sur", "Oeste"], (13,17): ["Sur", "Oeste"],

    #Seccion 21
    (6,9): ["Este", "Sur"], (7,9): ["Este", "Sur"],
    (6,8): ["Este", "Sur"], (7,8): ["Este", "Sur"],

    #Seccion 22
    (6, 11): ["Norte", "Oeste"], (7, 11): ["Norte", "Oeste"],
    (6, 10): ["Norte", "Oeste"], (7, 10): ["Norte", "Oeste"],

    #Seccion 23 Rotonda
    (12, 11): ["Oeste", "Sur"], (12, 10): ["Oeste", "Sur"], (12,9): ["Sur"], (12,8): ["Este", "Sur"],
    (13, 8): ["Este", "Sur"], (14, 8): ["Este"], (15, 8): ["Norte", "Este"], (15, 9): ["Norte", "Este"],
    (15, 10): ["Norte"], (15,11): ["Norte", "Oeste"], (14,11): ["Norte", "Oeste"], (13,11): ["Oeste"]

}



# Configurar los elementos de la visualización
canvas_element = mesa.visualization.CanvasGrid(
    circle_portrayal_example, 24, 24, 500, 500
)

agent_message_element = AgentMessageElement()  # Elemento para mostrar el mensaje inicial de cada agente

# Parámetros del modelo, incluyendo las posiciones de los estacionamientos y edificios
model_kwargs = {
    "num_agents": 1,
    "parking_positions": parking_positions,
    "building_positions": building_positions,
    "traffic_lights_positions": traffic_lights_positions,
    "roundabout_positions": roundabout_positions,
    "street_directions": street_directions,
    "width": 24,
    "height": 24
}

# Inicialización del servidor
server = mesa.visualization.ModularServer(
    CityModel,
    [canvas_element, agent_message_element],
    "Cityprojecta01750311",
    model_kwargs,
)
