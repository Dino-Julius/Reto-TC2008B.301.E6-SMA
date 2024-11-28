"""
Este módulo define varias clases de agentes para un modelo de simulación de ciudad utilizando el framework Mesa. Los agentes incluyen:
1. `SimpleCar`: Representa un coche que se mueve desde un lugar de estacionamiento inicial hasta un lugar de estacionamiento de destino, respetando las direcciones de las carreteras, otros coches y semáforos.
2. `Pedestrian`: Representa un peatón que se mueve aleatoriamente en celdas de edificios o celdas con semáforos en rojo.
3. `Building`: Representa un edificio estático en la ciudad para fines de visualización.
4. `Roundabout`: Representa una glorieta estática en la ciudad para fines de visualización.
5. `TrafficLight`: Representa un semáforo que alterna entre los estados rojo y verde basado en un temporizador.
6. `Road`: Representa una carretera estática en la ciudad para fines de visualización.
7. `Parking`: Representa un estacionamiento estático en la ciudad para fines de visualización.
Cada clase de agente hereda de la clase Agent de Mesa e implementa los métodos requeridos para la simulación.
El agente SimpleCar incluye métodos para aplicar movimientos, moverse basado en direcciones válidas y avanzar en la simulación.
El agente TrafficLight incluye métodos para alternar su estado y avanzar en la simulación basado en un temporizador.
Los otros agentes son estáticos y no realizan ninguna acción durante los pasos de la simulación.
Además, el módulo incluye una función auxiliar `get_direction` para calcular la nueva posición de un agente basado en una dirección dada.
"""

from mesa import Agent

import networkx as nx

from model.environment import parking_spots
from model.utils import Directions, RawDirections, find_parking_number


class SimpleCar(Agent):
    """
    Agente que representa un coche simple en la ciudad. Renderiza un coche en la cuadrícula.
    """
    def __init__(self, unique_id, model, num, start, destination):
        """
        Crear un nuevo agente de coche con un ID único, referencia al modelo, posición de inicio y posición de destino.
        """
        super().__init__(unique_id, model)
        self.id = num + 1
        self.start = start
        self.destination = destination

        self.model.grid.place_agent(self, self.start)
        self.movements = 0

        # Inicializar el grafo de la ciudad y calcular la mejor ruta
        self.graph = self.build_graph(self.model.valid_moves)
        self.now_direction = "XD"
        self.update_direction()

        self.determine_best_path()

    def determine_best_path(self):
        """
        Obtiene la mejor nueva ruta desde la posición actual hasta la posición de destino.
        """
        try:
            self.route = nx.shortest_path(self.graph, self.pos, self.destination)
            self.route_directions = self.get_directions_from_path(self.route)
            # print(f"Ruta recalculada desde {self.pos} hacia {self.destination}")
        except nx.NetworkXNoPath:
            self.route = None
            # pos_number = find_parking_number(self.pos, parking_spots)
            # dest_number = find_parking_number(self.destination, parking_spots)
            # print(f"No hay camino entre {pos_number}: {self.pos} y {dest_number}: {self.destination}")
        pass

    def apply_movement(self, next_direction: str):
        """
        Al aplicar la siguiente dirección, el coche se moverá a la siguiente celda en la cuadrícula.
        Esto utiliza el enum RawDirections para obtener el desplazamiento de la siguiente celda.
        Args:
            self: El agente coche.
            next_direction: La siguiente dirección a la que moverse.
        Returns:
            x_new, y_new: La nueva posición del coche.
        """
        disp = RawDirections[next_direction].value
        x_new, y_new = self.pos[0] + disp[0], self.pos[1] + disp[1]
        return x_new, y_new

    def random_move(self):
        """
        Mover el coche respetando las direcciones de las celdas de la carretera en la ruta, otros coches y semáforos para llegar al destino.
        """
        # Obtener direcciones permitidas desde la posición actual
        possible_directions = self.model.valid_moves.get(self.pos, [])
        # print(f'Possible directions: {possible_directions}')

        # Filtrar movimientos válidos
        valid_moves = []
        for direction in possible_directions:
            next_position = get_direction(self, direction)
            # print(next_position)

            # Permitir movimiento a la posición de destino sin restricciones
            if next_position == self.destination:
                valid_moves.append(next_position)
            else:
                # Verificar si hay semáforo en rojo en la próxima posición
                cell_contents = self.model.grid.get_cell_list_contents([next_position])
                if any(isinstance(agent, TrafficLight) and agent.state == "rojo" for agent in cell_contents):
                    continue  # Evitar moverse si el semáforo está en rojo

                # Verificar si la posición está libre de edificios, glorietas y otros coches
                if not any(isinstance(agent, (Building, Roundabout, SimpleCar)) for agent in cell_contents):
                    valid_moves.append(next_position)

        if valid_moves:
            # Elegir una posición válida al azar y moverse
            new_position = self.random.choice(valid_moves)
            self.model.grid.move_agent(self, new_position)

    def update_direction(self):
        """
        Obtener la dirección sobre la que se encuentra el vehículo
        """
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if isinstance(agent, Parking) or isinstance(agent, Road):
                self.now_direction = agent.direction

        # print("Dirección", self.direction, ", Pos: ", self.pos)

    @staticmethod
    def build_graph(valid_moves):
        """
        Construir un grafo dirigido de la ciudad basado en las direcciones válidas de movimiento. Usa la librería NetworkX.
        NetworkX es un paquete de Python para la creación, manipulación y estudio de la estructura, dinámica y funciones de redes complejas.
        Args:
            valid_moves (dict): Un diccionario que mapea las posiciones de la cuadrícula a las direcciones válidas.
        Returns:
            G: Un grafo de la ciudad con las conexiones de las direcciones válidas.
        """
        G = nx.DiGraph()
        for position, directions in valid_moves.items():
            for direction in directions:
                dx, dy = Directions[direction].value
                neighbor = (position[0] + dx, position[1] + dy)
                if neighbor in valid_moves:
                    G.add_edge(position, neighbor)
        return G

    @staticmethod
    def get_directions_from_path(route):
        """
        Obtener las direcciones de la ruta de un coche basado en los nodos de la ruta.
        Args:
            route (list): Una lista de nodos que representan la ruta del coche.
        Returns:
            directions (list): Una lista de direcciones que el coche debe seguir para llegar a su destino.
        """
        directions = []
        for i in range(len(route) - 1):
            current = route[i]
            next_node = route[i + 1]
            dx = next_node[0] - current[0]
            dy = next_node[1] - current[1]
            for direction, member in Directions.__members__.items():
                dir_dx, dir_dy = member.value
                if (dx, dy) == (dir_dx, dir_dy):
                    directions.append(direction)
                    break
        return directions

    def intelligent_move(self):
        """
        Movimeinto inteligente del coche basado en la dirección dada, ruta obtenida de la mejor ruta calculada.
        """
        if not self.route or len(self.route) < 2:
            return  # No hay ruta válida

        # Obtener la siguiente posición en la ruta
        next_position = self.route[1]

        # Verificar si la siguiente posición está libre
        cell_contents = self.model.grid.get_cell_list_contents([next_position])

        # Verificar si hay un semáforo en rojo
        traffic_light = any(isinstance(agent, TrafficLight) and agent.state == "red" for agent in cell_contents)

        # Verificar si hay otro coche en la siguiente posición
        other_car = any(isinstance(agent, SimpleCar) for agent in cell_contents)

        if not traffic_light and not other_car:
            # Mover al siguiente nodo en la ruta
            self.model.grid.move_agent(self, next_position)
            self.route.pop(0)  # Actualizar la ruta
        
        elif other_car or self.destination != self.pos:
            self.determine_best_path()

        elif other_car and self.destination == next_position:
            # Si el coche está en la posición de destino, pero hay otro coche, de todos formas ingresar al estacionamiento
            self.model.grid.move_agent(self, next_position)
            self.route.pop(0)
            pass

        else:
            # Esperar si hay un semáforo en rojo
            # print(f"Car {self.unique_id} is waiting at {self.pos}")
            pass

    def step(self):
        """
        Mientras el coche no haya llegado a su destino, seguirá moviéndose.
        """
        self.update_direction()
        if self.pos == self.destination:
            # print(f"Car {self.unique_id} has reached its destination.")
            return
        else:
            # print(f"Car {self.unique_id} is moving, now in {self.pos}")
            # self.random_move()
            self.intelligent_move()


class Pedestrian(Agent):
    """
    Agente que representa un peatón en la ciudad. Renderiza un peatón en la cuadrícula.
    """
    def __init__(self, unique_id, model, num):
        """
        Crear un nuevo agente de peatón con un ID único y referencia al modelo.
        """
        super().__init__(unique_id, model)
        self.id = num + 1

    def random_move(self):
        """
        Mover el peatón aleatoriamente solo en celdas de edificios (BL) o celdas con semáforos en rojo.
        """
        possible_moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        valid_moves = []

        for move in possible_moves:
            cell_contents = self.model.grid.get_cell_list_contents(move)
            if any(isinstance(agent, Building) for agent in cell_contents):
                valid_moves.append(move)
            elif any(isinstance(agent, TrafficLight) and agent.state == 'red' for agent in cell_contents):
                valid_moves.append(move)

        if valid_moves:
            new_position = self.random.choice(valid_moves)
            self.model.grid.move_agent(self, new_position)

    def step(self):
        """
        Realizar un movimiento aleatorio en cada paso.
        """
        self.random_move()


class Building(Agent):
    """
    Agente que representa un edificio en la ciudad. Renderiza un edificio en la cuadrícula.
    """
    def __init__(self, unique_id, model):
        """
        Crear un nuevo agente de edificio con un ID único y referencia al modelo.
        """
        super().__init__(unique_id, model)

    def step(self):
        """
        El agente Building no hace nada, es un agente estático para fines de visualización.
        """
        pass


class Roundabout(Agent):
    """
    Agente que representa una glorieta en la ciudad. Renderiza una glorieta en la cuadrícula.
    """
    def __init__(self, unique_id, model):
        """
        Crear un nuevo agente de glorieta con un ID único y referencia al modelo.
        """
        super().__init__(unique_id, model)

    def step(self):
        """
        El agente Roundabout no hace nada, es un agente estático para fines de visualización.
        """
        pass


class TrafficLight(Agent):
    """
    Agente que representa un semáforo en la ciudad. Renderiza un semáforo en la cuadrícula.
    """
    def __init__(self, unique_id, model, num, direction, initial_state="green", timer=5):
        """
        Crear un nuevo agente de semáforo con un ID único, referencia al modelo, dirección, estado inicial y temporizador.
        """
        super().__init__(unique_id, model)
        self.id = num + 1
        self.state = initial_state
        self.direction = direction
        self.timer = timer
        self.counter = 0

    def toggle_state(self):
        """
        Alternar el estado del semáforo.
        """
        self.state = "red" if self.state == "green" else "green"

    def count_waiting_cars(self):
        """
        Contar el número de coches esperando en la intersección del semáforo.
        """
        waiting_cars = 0
        neighbors = self.model.grid.get_neighbors(self.pos, moore=False, include_center=False)
        for neighbor in neighbors:
            if isinstance(neighbor, SimpleCar) and neighbor.route and neighbor.route[0] == self.pos:
                waiting_cars += 1
        return waiting_cars

    def step(self):
        """
        El agente TrafficLight no hace nada, es un agente estático para fines de visualización.
        """
        self.counter += 1
        if self.counter >= self.timer:
            self.toggle_state()
            self.counter = 0

        # Comunicación con el semáforo más cercano
        neighbors = self.model.grid.get_neighbors(self.pos, moore=False, include_center=False)
        for neighbor in neighbors:
            if isinstance(neighbor, TrafficLight) and neighbor.direction == self.direction:
                my_waiting_cars = self.count_waiting_cars()
                neighbor_waiting_cars = neighbor.count_waiting_cars()

                if my_waiting_cars > neighbor_waiting_cars:
                    # Reducir el temporizador mínimo a 3
                    self.timer = max(3, self.timer - 1)
                elif my_waiting_cars < neighbor_waiting_cars:
                    # Aumentar el temporizador máximo a 10
                    self.timer = min(10, self.timer + 1)


class Road(Agent):
    """
    Agente que representa una carretera en la ciudad. Renderiza una carretera en la cuadrícula.
    """
    def __init__(self, unique_id, model, direction):
        """
        Crear un nuevo agente de carretera con un ID único, referencia al modelo y dirección.
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        """
        El agente Road no hace nada, es un agente estático para fines de visualización.
        """
        pass


class Parking(Agent):
    """
    Agente que representa un estacionamiento en la ciudad. Renderiza un estacionamiento en la cuadrícula.
    """
    def __init__(self, unique_id, model, direction, parking_id):
        """
        Crear un nuevo agente de estacionamiento con un ID único, referencia al modelo, dirección y ID de estacionamiento
        """
        super().__init__(unique_id, model)
        self.parking_id = parking_id
        self.direction = direction

    def step(self):
        """
        El agente Parking no hace nada, es un agente estático para fines de visualización.
        """
        pass


def get_direction(Agent, direction):
    """
    Calcular la nueva posición de un agente basado en una dirección dada.
    Args:
        Agent: El agente que se moverá.
        direction: La dirección en la que moverse.
    Returns:
        x, y: Las nuevas coordenadas del agente.
    """
    x, y = Agent.pos
    if direction in Directions._member_names_:
        dx, dy = Directions[direction].value
        return x + dx, y + dy
