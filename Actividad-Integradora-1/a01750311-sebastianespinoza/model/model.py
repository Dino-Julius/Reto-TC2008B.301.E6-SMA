import mesa
from mesa.datacollection import DataCollector

class CarAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.destination = None

    def step(self):
        if self.destination is None:
            # Elegir un estacionamiento aleatorio como destino
            self.destination = self.random.choice(self.model.parking_positions)

        if self.pos == self.destination:
            # Detenerse si se ha alcanzado el destino
            return

        # Obtener direcciones permitidas desde la posición actual
        possible_directions = self.model.street_directions.get(self.pos, [])

        # Filtrar movimientos válidos
        valid_moves = []
        for direction in possible_directions:
            next_position = self.get_next_position(direction)
        
            # Verificar si la posición está libre de edificios, glorietas, y otros coches
            cell_contents = self.model.grid.get_cell_list_contents([next_position])
            if not any(isinstance(agent, (BuildingAgent, RoundaboutAgent, CarAgent)) for agent in cell_contents):
                valid_moves.append(next_position)

        if valid_moves:
            # Elegir una posición válida al azar y moverse
            new_position = self.random.choice(valid_moves)
            self.model.grid.move_agent(self, new_position)

    def get_next_position(self, direction):
        x, y = self.pos
        if direction == "Norte":
            return (x, y + 1)
        elif direction == "Sur":
            return (x, y - 1)
        elif direction == "Este":
            return (x + 1, y)
        elif direction == "Oeste":
            return (x - 1, y)
        return self.pos

class TrafficLightAgent(mesa.Agent):
    """
    An agent representig a traffic light that changes colors between green, yellow and red. 
    It's purpose is to manage the traffic within the city
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class ParkingAgent(mesa.Agent):
    """
    An agent representing a parking spot.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.isOccupied = False

class BuildingAgent(mesa.Agent):
    """
    An agent representing a building.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class RoundaboutAgent(mesa.Agent):
    """
    An agent representing a roundabout (glorieta).
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class CityModel(mesa.Model):
    """
    The model class manages the city grid with cars, parking spots, traffic lights and buildings.
    """
    def __init__(self, num_agents, parking_positions, building_positions, roundabout_positions, traffic_lights_positions, width, height, street_directions):
        super().__init__()
        self.num_agents = num_agents
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width=width, height=height, torus=True)

        #Street directions
        self.street_directions = street_directions
        self.parking_positions = parking_positions  # Guardar las posiciones de los estacionamientos

        # Crear y ubicar plazas de aparcamiento en posiciones específicas
        for pos in parking_positions:
            parking_agent = ParkingAgent(self.next_id(), self)
            self.schedule.add(parking_agent)
            self.grid.place_agent(parking_agent, pos)

        # Crear y ubicar edificios en posiciones específicas
        for pos in building_positions:
            building_agent = BuildingAgent(self.next_id(), self)
            self.schedule.add(building_agent)
            self.grid.place_agent(building_agent, pos)

        for pos in roundabout_positions:
            roundabout_agent = RoundaboutAgent(self.next_id(), self)
            self.schedule.add(roundabout_agent)
            self.grid.place_agent(roundabout_agent, pos)

        #Crear y ubicar semaforos
        for pos in traffic_lights_positions:
            traffic_light_agent = TrafficLightAgent(self.next_id(), self)
            self.schedule.add(traffic_light_agent)
            self.grid.place_agent(traffic_light_agent, pos)


        # Crear y ubicar agentes de coches
        for i in range(self.num_agents):
            car_agent = CarAgent(self.next_id(), self)
            self.schedule.add(car_agent)
            start_parking = self.random.choice(parking_positions)
            self.grid.place_agent(car_agent, start_parking)

        # Agregar el DataCollector
        self.datacollector = DataCollector(
            {
                "Car Count": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, CarAgent)),
                "Parking Count": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, ParkingAgent)),
                "Building Count": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, BuildingAgent))
            }
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
        self.schedule.step()
        self.datacollector.collect(self)