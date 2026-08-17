import heapq
from graph import Graph


# Placeholder travel-time multiplier
TRAVEL_SPEED_FACTOR = 1.0


# This is the Simulation for the ride-sharing Simulation Project
class Simulation:
    """
    Main controller for the ride-sharing simulation.
    """

    def __init__(self, map_filename):
        """
        Initializes the simulation state.
        """

        # Stores cars and riders
        self.cars = {}
        self.riders = {}

        # Create the Graph object
        self.map = None

        if map_filename is not None:
            self.map = Graph()
            self.map.load_from_file(map_filename)

        # Current simulation time
        self.current_time = 0

        # Min-heap containing future events
        self.events = []

        # Unique sequence number for each event
        self.event_sequence = 0


    def schedule_event(self, timestamp, event_type, data):
        """
        Adds an event to the min-heap.
        """

        self.event_sequence += 1

        event = (
            timestamp,
            self.event_sequence,
            event_type,
            data
        )

        heapq.heappush(self.events, event)


    def calculate_travel_time(self, start_location, end_location):
        """
        Calculates placeholder travel time using Manhattan distance.
        """

        x1, y1 = start_location
        x2, y2 = end_location

        distance = (
            abs(x1 - x2)
            +
            abs(y1 - y2)
        )

        return distance * TRAVEL_SPEED_FACTOR


    def find_closest_car_brute_force(self, rider_location):
        """
        Finds the closest available car using an O(N) brute-force search.
        """

        closest_car = None
        minimum_distance = float("inf")

        for car in self.cars.values():

            if car.status != "available":
                continue

            x1, y1 = car.location
            x2, y2 = rider_location

            distance = (
                abs(x1 - x2)
                +
                abs(y1 - y2)
            )

            if distance < minimum_distance:
                minimum_distance = distance
                closest_car = car

        return closest_car


    def handle_rider_request(self, rider):
        """
        Handles a new rider request.
        """

        print(
            f"TIME {self.current_time}: "
            f"RIDER {rider.id} requested a ride"
        )

        # Find nearest available car
        car = self.find_closest_car_brute_force(
            rider.start_location
        )

        if car is None:
            print(
                f"TIME {self.current_time}: "
                f"No available car for RIDER {rider.id}"
            )
            return

        # Link rider and car
        car.assigned_rider = rider

        # Car is no longer available
        car.status = "en_route_to_pickup"

        # Calculate time to rider
        pickup_duration = self.calculate_travel_time(
            car.location,
            rider.start_location
        )

        pickup_time = (
            self.current_time
            + pickup_duration
        )

        # Schedule pickup
        self.schedule_event(
            pickup_time,
            "ARRIVAL",
            car
        )

        print(
            f"TIME {self.current_time}: "
            f"CAR {car.id} dispatched to RIDER {rider.id}"
        )


    def handle_arrival(self, car):
        """
        Handles pickup and dropoff arrival events.
        """

        rider = car.assigned_rider

        if rider is None:
            return

        # ---------------------------------
        # PICKUP
        # ---------------------------------

        if car.status == "en_route_to_pickup":

            print(
                f"TIME {self.current_time}: "
                f"CAR {car.id} picked up RIDER {rider.id}"
            )

            # Update car physical location
            car.location = rider.start_location

            # Update statuses
            car.status = "en_route_to_destination"
            rider.status = "in_car"

            dropoff_duration = self.calculate_travel_time(
                car.location,
                rider.destination
            )

            dropoff_time = (
                self.current_time
                +
                dropoff_duration
            )

            self.schedule_event(
                dropoff_time,
                "ARRIVAL",
                car
            )

        # ---------------------------------
        # DROPOFF
        # ---------------------------------

        elif car.status == "en_route_to_destination":

            print(
                f"TIME {self.current_time}: "
                f"CAR {car.id} dropped off RIDER {rider.id}"
            )

            # Update car physical location
            car.location = rider.destination

            # Update statuses
            car.status = "available"
            rider.status = "completed"

            # Remove rider assignment
            car.assigned_rider = None


    def run(self):
        """
        Processes all events in chronological order.
        """

        print()
        print("STARTING RIDE-SHARING SIMULATION")
        print("-----------------------------------")

        while self.events:

            (
                timestamp,
                sequence_number,
                event_type,
                data
            ) = heapq.heappop(self.events)

            # Move simulation clock forward
            self.current_time = timestamp

            if event_type == "RIDER_REQUEST":

                self.handle_rider_request(data)

            elif event_type == "ARRIVAL":

                self.handle_arrival(data)

            else:

                print(
                    f"Unknown event type: {event_type}"
                )

        print("-----------------------------------")
        print("SIMULATION COMPLETE")


    def __str__(self):
        """
        Returns a readable summary of the simulation.
        """

        return (
            f"Cars: {len(self.cars)}\n"
            f"Riders: {len(self.riders)}"
        )