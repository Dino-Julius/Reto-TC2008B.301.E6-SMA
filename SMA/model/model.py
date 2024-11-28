"""
Este módulo define el modelo de movilidad urbana utilizando el framework Mesa.
El modelo simula el comportamiento de diferentes agentes en un entorno urbano,
incluyendo coches, edificios, rotondas, semáforos, carreteras y plazas de aparcamiento.

Clases:
    MovilityModel: Clase principal del modelo de movilidad urbana.
    AgentMessageElement: Clase para visualizar mensajes de los agentes en la interfaz de Mesa.
"""

import mesa
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from model.agents import SimpleCar, Pedestrian, Building, Roundabout, TrafficLight, Road, Parking
from model.environment import parking_spots
from model.utils import parse_environment, find_parking_spots, unity_pos


class MovilityModel(Model):
    """
    Clase del modelo para el Modelo de Movilidad.

    Este módulo define el modelo de movilidad urbana utilizando el framework Mesa.
    El modelo simula el comportamiento de diferentes agentes en un entorno urbano,
    incluyendo coches, edificios, rotondas, semáforos, carreteras y plazas de aparcamiento.

    Clases:
        MovilityModel: Clase principal del modelo de movilidad urbana.
        AgentMessageElement: Clase para visualizar mensajes de los agentes en la interfaz de Mesa.

    Agentes:
        SimpleCar: Representa un coche que se mueve desde un lugar de estacionamiento inicial hasta un lugar de estacionamiento de destino, respetando las direcciones de las carreteras, otros coches y semáforos.
        Pedestrian: Representa un peatón que se mueve de un edificio a otro, evitando los coches y las carreteras.
        Building: Representa un edificio estático en la ciudad para fines de visualización.
        Roundabout: Representa una glorieta estática en la ciudad para fines de visualización.
        TrafficLight: Representa un semáforo que alterna entre los estados rojo y verde basado en un temporizador.
        Road: Representa una carretera estática en la ciudad para fines de visualización.
        Parking: Representa un estacionamiento estático en la ciudad para fines de visualización.

    Funciones:
        step: Avanza el modelo en un paso.
        get_agent_messages: Devuelve los mensajes de los agentes.
    """
    def __init__(self, environment, valid_moves, simplecar_agents_limit, pedestrian_agents_limit=5):
        """
        Inicializa un nuevo modelo de movilidad urbana con el entorno, movimientos válidos y límite de agentes de coche simple.
        """
        super().__init__()
        self.environment = environment
        self.width = len(environment)
        self.height = len(environment[0])
        self.grid = MultiGrid(self.width, self.height, False)
        self.schedule = RandomActivation(self)

        self.valid_moves = valid_moves

        self.simpleCar_agents_limit = simplecar_agents_limit

        self.message = []
        self.step_count = 0

        # Parserear el entorno
        self.roads, self.buildings, _, self.traffic_lights, self.roundabouts = parse_environment(environment)

        # Parsrear los lugares de estacionamiento
        self.parsed_parking_spots = find_parking_spots(parking_spots)

        # Colocar las carreteras en la cuadrícula
        for road in self.roads:
            road_agent = Road(self.next_id(), self, road["direction"])
            self.schedule.add(road_agent)
            self.grid.place_agent(road_agent, (road["x"], road["y"]))

        # Coloca los edificios en la cuadrícula
        for building in self.buildings:
            building_agent = Building(self.next_id(), self)
            self.schedule.add(building_agent)
            self.grid.place_agent(building_agent, (building["x"], building["y"]))

        # Coloca los lugares de estacionamiento en la cuadrícula
        for parking in self.parsed_parking_spots:
            # print("parking values: ", parking)
            parking_agent = Parking(self.next_id(), self, direction=None, parking_id=parking["id"])
            self.schedule.add(parking_agent)
            self.grid.place_agent(parking_agent, (parking["x"], parking["y"]))
            # Determina la dirección de salida del lugar de estacionamiento basándose en las celdas de carretera vecinas.
            neighbors = self.grid.get_neighborhood(parking_agent.pos, moore=False, include_center=False)
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

        # Coloca los semáforos en la cuadrícula
        for i, traffic_light in enumerate(self.traffic_lights):
            initial_state = "green" if i % 4 < 2 else "red"
            tl_agent = TrafficLight(self.next_id(), self, i, direction=None, initial_state=initial_state)
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

        # Coloca las rotondas en la cuadrícula
        for roundabout in self.roundabouts:
            rd_agent = Roundabout(self.next_id(), self)
            self.schedule.add(rd_agent)
            self.grid.place_agent(rd_agent, (roundabout["x"], roundabout["y"]))

        # Conjunto de lugares utilizados
        self.used_start_spots = set()
        self.used_destination_spots = set()
        # Salidas peligrosas: 3, 7, 13
        self.dangerous_exits = [2, 6, 12]  # Índices peligrosos (restados 1)

        # Coloca los coches en la cuadrícula
        for i in range(simplecar_agents_limit):

            start_index = i

            # Asegurarse de que el índice de inicio no sea peligroso y no esté ya utilizado
            while start_index in self.dangerous_exits or start_index in self.used_start_spots:
                start_index += 1

            # Asegurarse de que el índice de inicio no exceda el número de estacionamientos disponibles
            if start_index >= len(self.parsed_parking_spots):
                break

            self.used_start_spots.add(start_index)  # Marcar el spot como utilizado

            destination_index = self.random.choice(range(len(self.parsed_parking_spots)))

            # Asegurarse de que el destino no sea el mismo que el inicio y no esté ya utilizado
            while destination_index == start_index or destination_index in self.used_destination_spots or destination_index in self.dangerous_exits:
                destination_index = self.random.choice(range(len(self.parsed_parking_spots)))

            self.used_destination_spots.add(destination_index)  # Marcar el destino como utilizado

            start_parking = self.parsed_parking_spots[start_index]
            destination_parking = self.parsed_parking_spots[destination_index]

            start_coords = (start_parking["x"], start_parking["y"])
            destination_coords = (destination_parking["x"], destination_parking["y"])

            car_agent = SimpleCar(self.next_id(), self, i, start_coords, destination_coords)

            self.schedule.add(car_agent)
            self.message.append(f"Vehículo {car_agent.id} inicia en {start_index + 1} y va a {destination_index + 1}")

        
        # Obtener todas las posiciones de celdas BL
        bl_positions = [(x, y) for x in range(self.width) for y in range(self.height) if any(isinstance(agent, Building) for agent in self.grid.get_cell_list_contents((x, y)))]
        
        # Coloca los peatones en la cuadrícula
        for i in range(pedestrian_agents_limit):
            if bl_positions:
                pos = self.random.choice(bl_positions)
                pedestrian_agent = Pedestrian(self.next_id(), self, i)
                self.schedule.add(pedestrian_agent)
                self.grid.place_agent(pedestrian_agent, pos)


        # Agregar al datacollector
        self.datacollector = DataCollector(
            {
                "Car Count": lambda m: sum(1 for car in m.schedule.agents if isinstance(car, SimpleCar)),
            }
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Avanzar el modelo en un paso.
        """
        self.schedule.step()
        self.step_count += 1
        self.datacollector.collect(self)

        # Verificar si todos los coches han llegado a su destino
        all_arrived = all(agent.pos == agent.destination for agent in self.schedule.agents if isinstance(agent, SimpleCar))

        if all_arrived:
            # Reset de los destinos disponibles
            self.used_destination_spots = set()
            
            if self.step_count >= 5:  # Esperar 5 pasos
                for agent in self.schedule.agents:
                    if isinstance(agent, SimpleCar):
                        agent.start = agent.destination  # Cambiar el start al destino

                        destination_index = self.random.choice(range(len(self.parsed_parking_spots)))

                        # Asegurarse de que el destino no sea el mismo que el inicio y no esté ya utilizado
                        while destination_index == agent.start or destination_index in self.used_destination_spots or destination_index in self.dangerous_exits:
                            destination_index = self.random.choice(range(len(self.parsed_parking_spots)))

                        self.used_destination_spots.add(destination_index)  # Marcar el destino como utilizado
                        
                        destination_parking = self.parsed_parking_spots[destination_index]
                        destination_coords = (destination_parking["x"], destination_parking["y"])

                        agent.destination = destination_coords  # Cambiar el destino
                        
                        # print(f"Vehículo {agent.id} inicia en {agent.start} y va a {destination_index}")
                        # Buscar el id del coche dado el punto
                        start_index = [index for index, parking in enumerate(self.parsed_parking_spots) if parking["x"] == agent.start[0] and parking["y"] == agent.start[1]][0] + 1    

                        # Actualizar el mensaje
                        self.message[agent.id - 1] = (f"Vehículo {agent.id} inicia en {start_index + 1} y va a {destination_index + 1}")
                        agent.determine_best_path()

                print(f"Todos los coches han llegado a su destino en el tiempo {self.step_count}. Reiniciando...")
                self.step_count = 0  # Reiniciar el contador de pasos

    def get_agent_messages(self):
        """
        Devuelve los mensajes de los agentes.
        """
        return "<br>".join(self.message)

    def start_data(self):
        """
        Obitene la instancia inicial de cada agente importante del modelo
        """
        result = {"Cars": [], "TrafficLights": [], "Pedestrians": []}
        for agent in self.agents:
            if isinstance(agent, SimpleCar):
                unity_x, unity_z = unity_pos(agent.start[0], agent.start[1])
                result["Cars"].append({"id": agent.unique_id, "pos": {"x": unity_x, "z": unity_z, "dir": agent.now_direction}})
            if isinstance(agent, TrafficLight):
                result["TrafficLights"].append(({"id": agent.id, "pos": agent.pos, "state": agent.state}))
            if isinstance(agent, Pedestrian):
                unity_x, unity_z = unity_pos(agent.pos[0], agent.pos[1])
                result["Pedestrians"].append({"id": agent.unique_id, "pos": {"x": unity_x, "z": unity_z}})
                
        return result

    def update_data(self):
        """
        Obtiene la información importante de cada agente para serializarla y enviarla al servidor.
        """
        result = {"Cars": [], "TrafficLights": [], "Pedestrians": []}
        for agent in self.agents:
            if isinstance(agent, SimpleCar):
                unity_x, unity_z = unity_pos(agent.pos[0], agent.pos[1])
                result["Cars"].append({"id": agent.unique_id, "pos": {"x": unity_x, "z": unity_z, "dir": agent.now_direction}})
            if isinstance(agent, TrafficLight):
                result["TrafficLights"].append(({"id": agent.id, "pos": agent.pos, "state": agent.state}))
            if isinstance(agent, Pedestrian):
                unity_x, unity_z = unity_pos(agent.pos[0], agent.pos[1])
                result["Pedestrians"].append({"id": agent.unique_id, "pos": {"x": unity_x, "z": unity_z}})
                
        return result


class AgentMessageElement(mesa.visualization.TextElement):
    """
    Clase para visualizar mensajes de los agentes en la interfaz de Mesa.
    """
    def __init__(self):
        """
        Constructor de la clase.
        """
        super().__init__()

    def render(self, model):
        """
        Renderiza los mensajes de los agentes en la interfaz de Mesa.
        """
        # Recupera y devuelve los mensajes de los agentes
        return model.get_agent_messages()
