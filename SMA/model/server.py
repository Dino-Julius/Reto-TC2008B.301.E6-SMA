'''
Este módulo configura y lanza un servidor de visualización para el modelo de movilidad utilizando Mesa.

Clases:
    AgentMessageElement: Elemento de texto para mostrar mensajes de agentes en la visualización.
    
Funciones:
    agents_portrayal(agent: Agent): Determina cómo se muestra un agente en la cuadrícula del servidor de Mesa.

Variables:
    height (int): Altura de la cuadrícula de la ciudad.
    width (int): Ancho de la cuadrícula de la ciudad.
    city_grid (CanvasGrid): Configuración de la representación de los agentes en la cuadrícula.
    agent_message_element (AgentMessageElement): Elemento para mostrar mensajes iniciales de los agentes.
    model_kwargs (dict): Parámetros del modelo, incluyendo el límite de agentes SimpleCar.
    server (ModularServer): Servidor modular de Mesa configurado con el modelo de movilidad.
'''

import mesa

from mesa import Agent

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

from model.agents import SimpleCar, Building, Roundabout, TrafficLight, Road, Parking
from model.model import MovilityModel
from model.environment import CITY, street_directions
from model.utils import Directions


class AgentMessageElement(mesa.visualization.TextElement):
    '''
    Elemento de texto para mostrar mensajes de agentes en la visualización.
    '''

    def __init__(self):
        '''
        Inicializa el elemento de texto.
        '''
        super().__init__()

    def render(self, model):
        '''
        Renderiza el elemento de texto.
        '''

        # Recupera y devuelve los mensajes de los agentes
        return model.get_agent_messages()


def agents_portrayal(agent: Agent):
    '''
    Determina cómo se muestra un agente en la cuadrícula del servidor de mesa.

    :param agent: El agente que se va a representar.
    :type agent: Agent
    :return: Un diccionario que describe la representación visual del agente.
    :rtype: dict

    La función devuelve un diccionario con las siguientes claves:
    - "Shape": La forma del agente (por ejemplo, "circle", "rect", "arrowHead").
    - "Filled": Si la forma está llena o no ("true" o "false").
    - "Layer": La capa en la que se dibuja el agente.
    - "r": El radio del círculo (si la forma es un círculo).
    - "scale": La escala de la imagen (si la forma es una imagen).
    - "text": Texto adicional que se muestra con el agente.
    - "text_color": Color del texto adicional.
    - "w": Ancho del rectángulo (si la forma es un rectángulo).
    - "h": Altura del rectángulo (si la forma es un rectángulo).
    - "Color": Color de la forma.
    - "heading_x": Dirección en el eje x (si la forma es una flecha).
    - "heading_y": Dirección en el eje y (si la forma es una flecha).

    La representación visual varía según el tipo de agente:
    - SimpleCar: Se representa con una imagen de coche.
    - TrafficLight: Se representa con un rectángulo de color verde o rojo según su estado.
    - Road: Se representa con una flecha que indica la dirección de la carretera.
    - Parking: Se representa con un rectángulo amarillo.
    - Building: Se representa con un rectángulo azul.
    - Roundabout: Se representa con un rectángulo marrón.
    '''

    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": "0",
        "r": 0.5,
    }

    if isinstance(agent, SimpleCar):
        portrayal.update({
            "Shape": "assets/car.png",
            "Filled": "true",
            "Layer": 1,
            "scale": 1,
            "text": str(agent.unique_id),
            "text_color": "Black"
        })

    elif isinstance(agent, TrafficLight):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 1,
            "w": 1.0,
            "h": 1.0,
            "Color": "green" if agent.state == "green" else "red",
            # "text": str(agent.direction),
            # "text_color": "Black"
        }

    elif isinstance(agent, Road):
        portrayal = {
            "Shape": "arrowHead",
            "scale": 0.5,
            "heading_x": Directions[agent.direction].value[0],
            "heading_y": Directions[agent.direction].value[1],
            "Layer": 1,
            "Color": "lightgrey",
        }

    elif isinstance(agent, Parking):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "w": 1.0,
            "h": 1.0,
            "Color": "Yellow",
            "text": str(agent.parking_id),
            "text_color": "Black"
        }

    elif isinstance(agent, Building):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "w": 1.0,
            "h": 1.0,
            "Color": "Blue"
        }

    elif isinstance(agent, Roundabout):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "w": 1.0,
            "h": 1.0,
            "Color": "Brown"
        }

    return portrayal


# Configura la altura y anchura de la ciudad
height = len(CITY)
width = len(CITY[0])

# Configura la representación de los agentes
city_grid = CanvasGrid(agents_portrayal, width, height)

# Elemento para mostrar el mensaje inicial de cada agente
agent_message_element = AgentMessageElement()

# Define los parámetros del modelo
model_kwargs = {
    "environment": CITY,
    "valid_moves": street_directions,
    "simpleCar_agents_limit": Slider("Simple Car Agent Limit", value=1, min_value=2, max_value=100, step=2),
}

# Inicializa el servidor
server = ModularServer(
    MovilityModel,
    [city_grid, agent_message_element],
    "Movility Model",
    model_kwargs,
)

if __name__ == "__main__":
    server.port = 8521
    server.launch()
