from pathfinder import find_the_shortest_path

#This is the Car Class for the Ride Sharing Simulation Project
class Car:
    """
    Represents one car in the rider-sharing simulation.
    """
    
    def __init__(self, car_id, initial_location):

        """
        Creates a new Car Object.
        
        Args:
            car_id(str): The unique ID for the car.
            initial_location(tuple): Current physical map corrdinates (x, y).
        """

        self.id = car_id

        #Physical location on the map
        self.location = initial_location

        #Car begins available 
        self.status = "available" 

        # Final Destination if one has been assigned 
        self.destination = None  

        # Rider currently assigned to this car
        self.assigned_rider = None

        # Attributes from the Djkstra
        self.route =[]
        self.route_time = 0

    def __str__(self):
        """
        returns a readable description of the car.
        """
        return (
            f"Car {self.id} at {self.location}"
            f" - Status: {self.status}"
        ) 

    def calculate_route(self, destination, graph):
        """
        Calculates the shortest route using Dijkstra's algorithm.
        """

        self.destination = destination

        self.route, self.route_time = find_the_shortest_path(
            graph,
            self.location,
            destination
        )