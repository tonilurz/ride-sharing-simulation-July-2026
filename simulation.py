#This is the Simulation for the ride sharing Simulation Project
class Simulation:
    """
    Controls and stores the objects used in the rider_sharing simulation
    """

    def __init__(self):
        """
        Creates an empty simulation.
        """

        self.cars = {}
        self.riders ={}

    def __str__(self):
        """
        Returns a readable summary of the simulation
        """

        return(
            f"Simulation: \n"
            f"Cars: {len(self.cars)}\n"
            f"Riders: {len(self.riders)}"
        )