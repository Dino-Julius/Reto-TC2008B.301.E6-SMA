import mesa
from mesa.datacollection import DataCollector

class CarAgent(mesa.Agent):
    def __init__(self, unique_id, model, start_parking, destination_parking):
        super().__init__(unique_id, model)
        self.start_parking = start_parking
        self.destination_parking = destination_parking
        # Colocar el agente en su lugar de salida al inicio
        self.model.grid.place_agent(self, self.start_parking)

    def step(self):
        if self.pos == self.destination_parking:
            # Si el agente ha llegado a su destino, permanece allí
            return

        # Obtener direcciones permitidas desde la posición actual
        possible_directions = self.model.street_directions.get(self.pos, [])

        # Filtrar movimientos válidos
        valid_moves = []
        for direction in possible_directions:
            next_position = self.get_next_position(direction)
            
            # Permitir movimiento a la posición de destino sin restricciones
            if next_position == self.destination_parking:
                valid_moves.append(next_position)
            else:
                # Verificar si hay semáforo en rojo en la próxima posición
                cell_contents = self.model.grid.get_cell_list_contents([next_position])
                if any(isinstance(agent, TrafficLightAgent) and agent.state == "rojo" for agent in cell_contents):
                    continue  # Evitar moverse si el semáforo está en rojo

                # Verificar si la posición está libre de edificios, glorietas y otros coches
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
    An agent representing a traffic light that changes colors between green and red.
    """
    def __init__(self, unique_id, model, initial_state="verde"):
        super().__init__(unique_id, model)
        self.state = initial_state  # Inicialmente en verde

    def toggle_state(self):
        """
        Change the traffic light state between green and red.
        """
        self.state = "rojo" if self.state == "verde" else "verde"


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
        self.step_count = 0 # Contador para semaforo
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width=width, height=height, torus=True)

        #Street directions
        self.street_directions = street_directions
        self.parking_positions = parking_positions  # Guardar las posiciones de los estacionamientos
        self.agent_messages = []  # Lista para almacenar los mensajes de cada agente

        # Crear y ubicar plazas de aparcamiento en posiciones específicas
        for pos in parking_positions:
            parking_agent = ParkingAgent(self.next_id(), self)
            self.schedule.add(parking_agent)
            self.grid.place_agent(parking_agent, pos)

        # Crear y ubicar edificios 
        for pos in building_positions:
            building_agent = BuildingAgent(self.next_id(), self)
            self.schedule.add(building_agent)
            self.grid.place_agent(building_agent, pos)
        
        #Crear y ubicar rotonda
        for pos in roundabout_positions:
            roundabout_agent = RoundaboutAgent(self.next_id(), self)
            self.schedule.add(roundabout_agent)
            self.grid.place_agent(roundabout_agent, pos)

        #Crear y ubicar semaforos
        for i,pos in enumerate(traffic_lights_positions):
            #Si el indice es par verde, impar rojo
            initial_state = "verde" if i % 4 < 2 else "rojo"
            traffic_light_agent = TrafficLightAgent(self.next_id(), self, initial_state=initial_state)
            self.schedule.add(traffic_light_agent)
            self.grid.place_agent(traffic_light_agent, pos)


        # Crear y ubicar agentes de coches en estacionamientos
        for i in range(self.num_agents):
            start_index = self.random.choice(range(len(parking_positions)))  # Índice de salida
            destination_index = self.random.choice(range(len(parking_positions)))  # Índice de destino

            start_parking = parking_positions[start_index]
            destination_parking = parking_positions[destination_index]

            car_agent = CarAgent(self.next_id(), self, start_parking, destination_parking)
            self.schedule.add(car_agent)
            self.agent_messages.append(f"Agente {car_agent.unique_id - 203} salió de estacionamiento {start_index + 1} y se dirige a {destination_index + 1}")

        # Agregar el DataCollector
        self.datacollector = DataCollector(
            {
                "Car Count": lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, CarAgent)),
            }
        )

        self.running = True
        self.datacollector.collect(self)

    def get_agent_messages(self):
        return "<br>".join(self.agent_messages)


    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
        # Incrementar el contador de pasos y cambiar el estado del semáforo cada 30 pasos
        self.step_count += 1
        if self.step_count >= 30:
            for agent in self.schedule.agents:
                if isinstance(agent, TrafficLightAgent):
                    agent.toggle_state()
            self.step_count = 0  # Reiniciar el contador
        self.schedule.step()
        self.datacollector.collect(self)