from graph import Graph

#This is the Simulation for the ride sharing Simulation Project
class Simulation:
    """
    Controls and stores the objects used in the rider_sharing simulation
    """

    def __init__(self, map_filename):
        """
        Creates the car and rider dictionaries and loads the map.
        """

        self.cars = {}
        self.riders ={}
    # Creat the Graph object

        self.map=Graph()
    # Load the map data from the CSV file
        self.map.load_from_file(map_filename)

    def __str__(self):
        """
        Returns a readable summary of the simulation
        """

        return(
            f"Simulation loaded successfully.\n"
            f"Cars: {len(self.cars)}\n"
            f"Riders: {len(self.riders)}"
            f"Map nodes: {len(self.map.adjacency_list)}"
        )