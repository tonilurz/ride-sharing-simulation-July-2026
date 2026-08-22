from pathfinder import find_the_shortest_path, find_nearest_vertex


# This is the Car Class for the Ride Sharing Simulation Project
class Car:
    """
    Represents one car in the ride-sharing simulation.
    """

    def __init__(self, car_id, initial_location):
        """
        Creates a new Car object.

        Args:
            car_id (str): The unique ID for the car.
            initial_location (tuple): Current physical map coordinates (x, y).
        """

        self.id = car_id

        # Physical location on the map
        self.location = initial_location

        # Current car state
        self.status = "available"

        # Rider currently assigned to this car
        self.assigned_rider = None

        # Route information
        self.route = None
        self.route_time = 0

        # Final performance information
        self.busy_start_time = None
        self.total_busy_time = 0
        self.trips_completed = 0

    def calculate_route(self, destination, graph):
        """
        Calculates a route from the car's physical
        location to another physical location.
        """

        # Convert car coordinates to nearest graph vertex
        start_node = find_nearest_vertex(
            self.location,
            graph.node_coordinates
        )

        # Convert destination coordinates to nearest graph vertex
        end_node = find_nearest_vertex(
            destination,
            graph.node_coordinates
        )

        # Run Dijkstra
        self.route, self.route_time = (
            find_the_shortest_path(
                graph,
                start_node,
                end_node
            )
        )

        return self.route, self.route_time

    def __str__(self):
        """
        Returns a readable description of the car.
        """

        return (
            f"Car {self.id} at {self.location}"
            f" - Status: {self.status}"
        )