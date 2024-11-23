'''
Este módulo define el modelo de movilidad urbana utilizando el framework Mesa. 
El modelo simula el comportamiento de diferentes agentes en un entorno urbano, 
incluyendo coches, edificios, rotondas, semáforos, carreteras y plazas de aparcamiento.

Clases:
    MovilityModel: Clase principal del modelo de movilidad urbana.
    AgentMessageElement: Clase para visualizar mensajes de los agentes en la interfaz de Mesa.
'''

import mesa
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from model.agents import SimpleCar, Building, Roundabout, TrafficLight, Road, Parking
from model.utils import parse_environment, find_parking_spots
from model.environment import parking_spots


class MovilityModel(Model):
    '''
    Clase del modelo para el Modelo de Movilidad.

    Este módulo define el modelo de movilidad urbana utilizando el framework Mesa. 
    El modelo simula el comportamiento de diferentes agentes en un entorno urbano, 
    incluyendo coches, edificios, rotondas, semáforos, carreteras y plazas de aparcamiento.

    Clases:
        MovilityModel: Clase principal del modelo de movilidad urbana.
        AgentMessageElement: Clase para visualizar mensajes de los agentes en la interfaz de Mesa.

    Agentes:
        SimpleCar: Representa un coche que se mueve desde un lugar de estacionamiento inicial hasta un lugar de estacionamiento de destino, respetando las direcciones de las carreteras, otros coches y semáforos.
        Building: Representa un edificio estático en la ciudad para fines de visualización.
        Roundabout: Representa una glorieta estática en la ciudad para fines de visualización.
        TrafficLight: Representa un semáforo que alterna entre los estados rojo y verde basado en un temporizador.
        Road: Representa una carretera estática en la ciudad para fines de visualización.
        Parking: Representa un estacionamiento estático en la ciudad para fines de visualización.

    Funciones:
        step: Avanza el modelo en un paso.
        get_agent_messages: Devuelve los mensajes de los agentes.
    '''

    def __init__(self, environment, valid_moves, simpleCar_agents_limit):
        '''
        Inicializa un nuevo modelo de movilidad urbana con el entorno, movimientos válidos y límite de agentes de coche simple.
        '''

        super().__init__()
        self.environment = environment
        self.width = len(environment)
        self.height = len(environment[0])
        self.grid = MultiGrid(self.width, self.height, False)
        self.schedule = RandomActivation(self)

        self.valid_moves = valid_moves

        self.simpleCar_agents_limit = simpleCar_agents_limit

        # Initialize other
        self.message = []
        self.step_count = 0

        # Parse the environment
        self.roads, self.buildings, _, self.traffic_lights, self.roundabouts = parse_environment(
            environment)

        # Parse the parking spots
        self.parsed_parking_spots = find_parking_spots(parking_spots)

        # Place the agents in the grid
        for road in self.roads:
            road_agent = Road(self.next_id(), self, road["direction"])
            self.schedule.add(road_agent)
            self.grid.place_agent(road_agent, (road["x"], road["y"]))

        # Place the buildings in the grid
        for building in self.buildings:
            building_agent = Building(self.next_id(), self)
            self.schedule.add(building_agent)
            self.grid.place_agent(building_agent, (building["x"], building["y"]))

        # Place the parking spots in the grid
        for parking in self.parsed_parking_spots:
            # print("parking values: ", parking)
            parking_agent = Parking(self.next_id(), self, direction=None, parking_id=parking["id"])
            self.schedule.add(parking_agent)
            self.grid.place_agent(parking_agent, (parking["x"], parking["y"]))
            # Determine the exit direction of the parking slot based on the neighboring road cells.
            neighbors = self.grid.get_neighborhood(
                parking_agent.pos, moore=False, include_center=False)
            for neighbor in neighbors:
                cell_contents = self.grid.get_cell_list_contents([neighbor])
                for agent in cell_contents:
                    if isinstance(agent, Road):
                        dx = neighbor[0] - parking_agent.pos[0]
                        dy = neighbor[1] - parking_agent.pos[1]
                        if dx == 1:
                            parking_agent.direction = 'RH'
                        elif dx == -1:
                            parking_agent.direction = 'LF'
                        elif dy == 1:
                            parking_agent.direction = 'UP'
                        elif dy == -1:
                            parking_agent.direction = 'DW'

        # Place the traffic lights in the grid
        for i, traffic_light in enumerate(self.traffic_lights):
            initial_state = "green" if i % 4 < 2 else "red"
            tl_agent = TrafficLight(self.next_id(), self, direction=None, initial_state=initial_state)
            self.schedule.add(tl_agent)
            self.grid.place_agent(tl_agent, (traffic_light["x"], traffic_light["y"]))

            possible_directions = self.grid.get_neighborhood(tl_agent.pos, moore=False, include_center=False)
            road_directions = []

            for possible_direction in possible_directions:
                cell_contents = self.grid.get_cell_list_contents([possible_direction])
                for agent in cell_contents:
                    if isinstance(agent, Road):
                        if tl_agent.direction is None:
                            tl_agent.direction = agent.direction
                        else:
                            # Verificar si hay un semáforo en la misma fila o columna
                            if tl_agent.pos[0] == possible_direction[0]:  # Mismo x
                                tl_agent.direction = 'y'
                            elif tl_agent.pos[1] == possible_direction[1]:  # Mismo y
                                tl_agent.direction = 'x'

                        # Agregar la dirección del agente Road a la lista
                        road_directions.append(agent.direction)

                    # Inicializar filtered_directions
                    filtered_directions = []
                    # Filtrar las direcciones de las carreteras para que coincidan con el eje del semáforo
                    if tl_agent.direction == 'y':
                        filtered_directions = [direction for direction in road_directions if direction in ['DW', 'UP']]
                    elif tl_agent.direction == 'x':
                        filtered_directions = [direction for direction in road_directions if direction in ['LF', 'RH']]

                    # Determinar la dirección real del semáforo
                    if filtered_directions:
                        if tl_agent.direction == 'y':
                            if 'DW' in filtered_directions:
                                tl_agent.direction = 'DW'
                            else:
                                tl_agent.direction = 'UP'
                        elif tl_agent.direction == 'x':
                            if 'RH' in filtered_directions:
                                tl_agent.direction = 'RH'
                            else:
                                tl_agent.direction = 'LF'

        # Place the roundabouts in the grid
        for roundabout in self.roundabouts:
            rd_agent = Roundabout(self.next_id(), self)
            self.schedule.add(rd_agent)
            self.grid.place_agent(rd_agent, (roundabout["x"], roundabout["y"]))

        # Place the cars in the grid
        for i in range(simpleCar_agents_limit):
            start_index = self.random.choice(range(len(self.parsed_parking_spots)))
            destination_index = self.random.choice(range(len(self.parsed_parking_spots)))

            start_parking = self.parsed_parking_spots[start_index - 1]
            destination_parking = self.parsed_parking_spots[destination_index - 1]

            start_coords = (start_parking["x"], start_parking["y"])
            destination_coords = (destination_parking["x"], destination_parking["y"])

            simpleCar_Agent = SimpleCar(self.next_id(), self, start_coords, destination_coords)

            self.schedule.add(simpleCar_Agent)
            self.message.append(f"Agente {simpleCar_Agent.unique_id} inicia en {start_index} y va a {destination_index}")

        # Agregar al datacollector
        self.datacollector = DataCollector(
            {
                "Car Count": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, SimpleCar)),
            }
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        '''
        Avanzar el modelo en un paso.
        '''

        self.schedule.step()
        self.datacollector.collect(self)

    def get_agent_messages(self):
        '''
        Devuelve los mensajes de los agentes.
        '''

        return "<br>".join(self.message)


class AgentMessageElement(mesa.visualization.TextElement):
    '''
    Clase para visualizar mensajes de los agentes en la interfaz de Mesa.
    '''

    def __init__(self):
        '''
        Constructor de la clase.
        '''

        super().__init__()

    def render(self, model):
        '''
        Renderiza los mensajes de los agentes en la interfaz de Mesa.
        '''

        # Recupera y devuelve los mensajes de los agentes
        return model.get_agent_messages()
