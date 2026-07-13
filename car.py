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
            initial_location(tuple): The initial location of the car as a tuple (x, y).
        """

        self.id = car_id
        self.location = initial_location
        self.status = "available"  # The status of the car, can be "available" or "unavailable" 
        self.destination = None  # The destination of the car, if it is currently on a trip

    def __str__(self):
        """
        returns a readable description of the car.
        """
        return (
            f"Car {self.id} at {self.location}"
            f" - Status: {self.status}"
        )
