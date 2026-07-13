#This is the rider class for the Ride Sharing Simulation Project
class Rider:
    """
    Represents one rider requesting transportation
    """
    def __init__(self, rider_id, pickup_location, dropoff_location):
        """
        Creates a new Rider object.
        
        Args.
            rider_id (str): The uniquie ID for the rider.
            pickup_location (tuple): The rider's starting coordinates.
            dropoff_location (tuple): The rider's destination coordinates.
            """
        self.id = rider_id
        self.start_location = pickup_location
        self.destination = dropoff_location
        self.status = "waiting"

    def __str__(self):
        """
        Returns a readable description of a Rider
        """
        return (
            f"Rider {self.id} at {self.start_location}"
            f" waiting for ride to {self.destination}"
        ) 