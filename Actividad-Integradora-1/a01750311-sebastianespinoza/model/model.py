import mesa
from mesa.datacollection import DataCollector

class CarAgent(mesa.Agent):  
    """
    An agent representing a car that might look for a parking spot.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

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


class CityModel(mesa.Model):
    """
    The model class manages the city grid with cars, parking spots, traffic lights and buildings.
    """
    def __init__(self, num_agents, parking_positions, building_positions, traffic_lights_positions, width, height):
        super().__init__()
        self.num_agents = num_agents
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width=width, height=height, torus=True)

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

        for pos in traffic_lights_positions:
            traffic_light_agent = TrafficLightAgent(self.next_id(), self)
            self.schedule.add(traffic_light_agent)
            self.grid.place_agent(traffic_light_agent, pos)


        # Crear y ubicar agentes de coches
        for i in range(self.num_agents):
            car_agent = CarAgent(self.next_id(), self)
            self.schedule.add(car_agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(car_agent, (x, y))

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