# ------------------------------------------------------------
# Ride-Sharing Simulator
# Final Simulation Engine
# ------------------------------------------------------------

import heapq
import random

from itertools import count

from graph import Graph
from car import Car
from rider import Rider

from quadtree import (
    Quadtree,
    Rectangle,
    Point
)

from pathfinder import (
    find_nearest_vertex,
    find_the_shortest_path
)


# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------

# Professor requires the default candidate count to be 5
DEFAULT_CANDIDATE_COUNT = 5

# Average time between randomly generated rider requests
MEAN_ARRIVAL_TIME = 10.0


class Simulation:
    """
    Main controller for the final ride-sharing simulation.

    The Simulation coordinates:
    - Cars
    - Riders
    - Graph
    - Quadtree
    - Dijkstra pathfinding
    - Event queue
    - Rider generation
    - Availability
    - Metrics
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        map_filename,
        max_time=500,
        num_riders=50,
        candidate_count=DEFAULT_CANDIDATE_COUNT
    ):
        """
        Initializes the final ride-sharing simulation.

        Args:
            map_filename:
                Name/path of the unified city map file.

            max_time:
                Latest simulation time at which a new
                rider request may be generated.

            num_riders:
                Maximum number of riders to generate.

            candidate_count:
                Number of geographically nearest cars
                requested from the Quadtree.
        """

        # --------------------------------------------------------
        # Validate configuration
        # --------------------------------------------------------

        if candidate_count <= 0:
            raise ValueError(
                "candidate_count must be greater than zero."
            )

        if num_riders is not None and num_riders < 0:
            raise ValueError(
                "num_riders cannot be negative."
            )

        if max_time is not None and max_time < 0:
            raise ValueError(
                "max_time cannot be negative."
            )

        # --------------------------------------------------------
        # General Simulation State
        # --------------------------------------------------------

        self.current_time = 0.0

        # Min-heap holding all future events
        self.events = []

        # Unique event sequence numbers
        # This prevents heapq from comparing Car/Rider objects
        # when two events have the same timestamp.
        self.event_sequence = count()

        # Chronological event log
        self.event_log = []

        # --------------------------------------------------------
        # Configuration
        # --------------------------------------------------------

        self.max_time = max_time

        self.num_riders = num_riders

        self.candidate_count = candidate_count

        # --------------------------------------------------------
        # Main Car and Rider Storage
        # --------------------------------------------------------

        self.cars = {}

        self.riders = {}

        # Rider ID generation
        self.rider_counter = 0

        self.riders_generated = 0

        # --------------------------------------------------------
        # Load Unified City Map
        # --------------------------------------------------------

        self.map = Graph()

        self.map.load_map_data(
            map_filename
        )
        
        # --------------------------------------------------------
        # Determine Quadtree Map Boundary
        # --------------------------------------------------------

        coordinates = list(
            self.map.node_coordinates.values()
        )

        if not coordinates:
            raise ValueError(
                "No graph-node coordinates were loaded."
            )

        min_x = min(
            x for x, y in coordinates
        )

        max_x = max(
            x for x, y in coordinates
        )

        min_y = min(
            y for x, y in coordinates
        )

        max_y = max(
            y for x, y in coordinates
        )

        # Add 1.0 because Rectangle.contains() normally
        # treats the upper boundary as exclusive.
        self.map_boundary = Rectangle(
            min_x,
            min_y,
            (max_x - min_x) + 1.0,
            (max_y - min_y) + 1.0
        )

        # --------------------------------------------------------
        # Available-Car Structures
        # --------------------------------------------------------

        # car_id -> Car object
        self.available_cars = {}

        # car_id -> exact Point object stored in Quadtree
        self.available_car_points = {}

        # Spatial index containing ONLY available cars
        self.available_car_quadtree = Quadtree(
            self.map_boundary,
            capacity=4
        )

    # ============================================================
    # LOGGING
    # ============================================================

    def log(self, message):
        """
        Prints and stores a chronological simulation message.
        """

        self.event_log.append(message)

        print(message)

    # ============================================================
    # EVENT QUEUE
    # ============================================================

    def schedule_event(
        self,
        timestamp,
        event_type,
        data
    ):
        """
        Adds a four-field event to the min-heap.

        Event format:
        (
            timestamp,
            sequence_number,
            event_type,
            data
        )
        """

        # Never allow an event at infinity
        if timestamp == float("inf"):
            raise ValueError(
                "Cannot schedule an event at infinity."
            )

        event = (
            timestamp,
            next(self.event_sequence),
            event_type,
            data
        )

        heapq.heappush(
            self.events,
            event
        )

    # ============================================================
    # AVAILABLE CAR MANAGEMENT
    # ============================================================

    def add_available_car(self, car):
        """
        Adds a car to all three availability structures.

        A NEW Point object is created using the car's
        CURRENT physical location.
        """

        # Make sure the car is not already listed
        if car.id in self.available_cars:
            raise ValueError(
                f"{car.id} is already in available_cars."
            )

        if car.id in self.available_car_points:
            raise ValueError(
                f"{car.id} already has an available-car Point."
            )

        # Create a new Point at the car's current position
        point = Point(
            x=car.location[0],
            y=car.location[1],
            data=car
        )

        # Insert into Quadtree FIRST
        inserted = (
            self.available_car_quadtree.insert(
                point
            )
        )

        # If insertion failed, do not modify the dictionaries
        if not inserted:
            raise ValueError(
                f"Could not insert {car.id} "
                f"at location {car.location} "
                f"into the available-car Quadtree."
            )

        # Only update dictionaries after Quadtree succeeds
        self.available_cars[
            car.id
        ] = car

        self.available_car_points[
            car.id
        ] = point

        # Available state is centralized here
        car.status = "available"

    def remove_available_car(self, car):
        """
        Removes a car from all availability structures.
        """

        # Make sure this car has a stored Point
        if car.id not in self.available_car_points:
            raise ValueError(
                f"No available Point for {car.id}"
            )

        # -------------------------------------------------
        # GET THE EXACT POINT FIRST
        # -------------------------------------------------

        point = self.available_car_points[car.id]

        # -------------------------------------------------
        # REMOVE FROM QUADTREE
        # -------------------------------------------------

        removed = (
            self.available_car_quadtree.remove(
                point
            )
        )

        print(
            "Removal result:",
            removed
        )

        # If the Quadtree cannot find the Point,
        # stop before changing the dictionaries.
        if not removed:

            raise RuntimeError(
                f"Quadtree removal failed for {car.id}"
            )

        # -------------------------------------------------
        # REMOVE FROM DICTIONARIES
        # -------------------------------------------------

        del self.available_car_points[
            car.id
        ]

        del self.available_cars[
            car.id
    ]
    # ============================================================
    # INITIAL CAR GENERATION
    # ============================================================

    def initialize_cars(
        self,
        number_of_cars
    ):
        """
        Creates the initial fleet of cars.

        Each car receives random physical coordinates
        inside the selected map boundary.
        """

        for i in range(number_of_cars):

            x = random.uniform(
                self.map_boundary.x,
                self.map_boundary.x
                + self.map_boundary.width
                - 0.001
            )

            y = random.uniform(
                self.map_boundary.y,
                self.map_boundary.y
                + self.map_boundary.height
                - 0.001
            )

            car = Car(
                f"CAR{i + 1:03d}",
                (x, y)
            )

            # Ensure final milestone attributes exist
            car.status = "available"
            car.assigned_rider = None
            car.busy_start_time = None
            car.total_busy_time = 0
            car.trips_completed = 0

            self.cars[
                car.id
            ] = car

            # All initial cars begin available
            self.add_available_car(
                car
            )

    # ============================================================
    # RIDER GENERATION
    # ============================================================

    def generate_rider_request(self):
        """
        Creates and stores one random Rider.

        Returns:
            Rider object
        """

        self.rider_counter += 1

        rider_id = (
            f"RIDER{self.rider_counter:04d}"
        )

        # Rider starting location
        start_location = (
            random.uniform(
                self.map_boundary.x,
                self.map_boundary.x
                + self.map_boundary.width
                - 0.001
            ),
            random.uniform(
                self.map_boundary.y,
                self.map_boundary.y
                + self.map_boundary.height
                - 0.001
            )
        )

        # Rider destination
        destination = (
            random.uniform(
                self.map_boundary.x,
                self.map_boundary.x
                + self.map_boundary.width
                - 0.001
            ),
            random.uniform(
                self.map_boundary.y,
                self.map_boundary.y
                + self.map_boundary.height
                - 0.001
            )
        )

        rider = Rider(
            rider_id,
            start_location,
            destination
        )

        # Ensure the final state model is initialized
        rider.status = "waiting"
        rider.request_time = None
        rider.pickup_time = None
        rider.dropoff_time = None

        # Store rider
        self.riders[
            rider.id
        ] = rider

        self.riders_generated += 1

        return rider

    def schedule_next_rider_request(self):
        """
        Generates and schedules the next rider request
        if both generation limits permit it.

        Rider generation may stop while active trips
        continue processing.
        """

        # --------------------------------------------------------
        # Rider-count limit
        # --------------------------------------------------------

        if (
            self.num_riders is not None
            and
            self.riders_generated >= self.num_riders
        ):
            return

        # --------------------------------------------------------
        # Generate the next arrival interval
        # --------------------------------------------------------

        interval = random.expovariate(
            1.0 / MEAN_ARRIVAL_TIME
        )

        next_time = (
            self.current_time
            +
            interval
        )

        # --------------------------------------------------------
        # Time-generation limit
        # --------------------------------------------------------

        if (
            self.max_time is not None
            and
            next_time > self.max_time
        ):
            return

        # Generate the next rider
        rider = (
            self.generate_rider_request()
        )

        # Schedule request
        self.schedule_event(
            next_time,
            "RIDER_REQUEST",
            rider
        )

    def start(self):
        """
        Schedules the first rider request at time 0.

        The first request is created only when the
        configured rider-generation limits permit it.
        """

        # Do not start twice
        if self.riders_generated > 0:
            return

        # num_riders = 0 means no rider generation
        if (
            self.num_riders is not None
            and
            self.num_riders <= 0
        ):
            return

        # max_time = 0 still allows an event at time 0
        if (
            self.max_time is not None
            and
            self.max_time < 0
        ):
            return

        first_rider = (
            self.generate_rider_request()
        )

        self.schedule_event(
            0.0,
            "RIDER_REQUEST",
            first_rider
        )

    # ============================================================
    # RIDER REQUEST HANDLER
    # ============================================================

    def handle_rider_request(
        self,
        rider
    ):
        """
        Matches a rider using:

        Quadtree
            -> up to k geographically nearest cars

        Dijkstra
            -> lowest reachable road-network travel time
        """

        # --------------------------------------------------------
        # Set request time
        # --------------------------------------------------------

        if rider.request_time is None:
            rider.request_time = (
                self.current_time
            )

        self.log(
            f"TIME {self.current_time:.2f}: "
            f"{rider.id} requested a ride"
        )

        # --------------------------------------------------------
        # IMPORTANT:
        # Schedule the next request regardless of whether
        # this rider is successfully matched.
        # --------------------------------------------------------

        self.schedule_next_rider_request()

        # --------------------------------------------------------
        # Ask Quadtree for geographically nearest candidates
        # --------------------------------------------------------

        query_point = Point(
            rider.start_location[0],
            rider.start_location[1]
        )

        candidate_points = (
            self.available_car_quadtree.find_k_nearest(
                query_point,
                k=self.candidate_count
            )
        )

        # --------------------------------------------------------
        # No available cars
        # --------------------------------------------------------

        if not candidate_points:

            rider.status = "unmatched"

            self.log(
                f"TIME {self.current_time:.2f}: "
                f"No available cars for {rider.id}"
            )

            return

        # --------------------------------------------------------
        # Snap rider location to graph ONCE
        # --------------------------------------------------------

        rider_vertex = find_nearest_vertex(
            rider.start_location,
            self.map.node_coordinates
        )

        # --------------------------------------------------------
        # Evaluate EVERY Quadtree candidate with Dijkstra
        # --------------------------------------------------------

        best_car = None

        best_route = None

        best_pickup_time = float("inf")

        for candidate_point in candidate_points:

            car = candidate_point.data

            # Convert physical car location to graph vertex
            car_vertex = find_nearest_vertex(
                car.location,
                self.map.node_coordinates
            )
           
            # Dijkstra determines actual road travel time
            route, travel_time = (
                find_the_shortest_path(
                    self.map,
                    car_vertex,
                    rider_vertex
                )
            )

           
            # Skip unreachable candidate
            if route is None:
                continue

            # Better route found
            if travel_time < best_pickup_time:

                best_car = car

                best_route = route

                best_pickup_time = travel_time

            # Deterministic tie-breaker by car ID
            elif (
                travel_time == best_pickup_time
                and
                best_car is not None
                and
                car.id < best_car.id
            ):

                best_car = car

                best_route = route

                best_pickup_time = travel_time

        # --------------------------------------------------------
        # All returned candidates were unreachable
        # --------------------------------------------------------

        if best_car is None:

            rider.status = "unmatched"

            self.log(
                f"TIME {self.current_time:.2f}: "
                f"No reachable car for {rider.id}"
            )

            return

        # --------------------------------------------------------
        # Remove selected car from availability immediately
        # --------------------------------------------------------

        self.remove_available_car(
            best_car
        )

        # --------------------------------------------------------
        # Dispatch State
        # --------------------------------------------------------

        best_car.status = (
            "en_route_to_pickup"
        )

        best_car.assigned_rider = rider

        best_car.route = best_route

        best_car.route_time = (
            best_pickup_time
        )

        best_car.busy_start_time = (
            self.current_time
        )

        rider.status = "waiting"

        # --------------------------------------------------------
        # Schedule pickup using DIJKSTRA travel time
        # --------------------------------------------------------

        pickup_time = (
            self.current_time
            +
            best_pickup_time
        )

        self.schedule_event(
            pickup_time,
            "PICKUP_ARRIVAL",
            best_car
        )

        self.log(
            f"TIME {self.current_time:.2f}: "
            f"{best_car.id} dispatched to {rider.id} "
            f"with pickup road time "
            f"{best_pickup_time:.2f}"
        )

    # ============================================================
    # PICKUP ARRIVAL
    # ============================================================

    def handle_pickup_arrival(
        self,
        car
    ):
        """
        Processes the selected car arriving
        at the rider's pickup location.
        """

        rider = car.assigned_rider

        if rider is None:
            raise RuntimeError(
                f"{car.id} reached pickup "
                f"without an assigned rider."
            )

        # --------------------------------------------------------
        # Update physical location
        # --------------------------------------------------------

        car.location = (
            rider.start_location
        )

        # --------------------------------------------------------
        # Update state
        # --------------------------------------------------------

        car.status = (
            "en_route_to_destination"
        )

        rider.status = "in_car"

        rider.pickup_time = (
            self.current_time
        )

        wait_time = (
            rider.pickup_time
            -
            rider.request_time
        )

        self.log(
            f"TIME {self.current_time:.2f}: "
            f"{car.id} picked up {rider.id} "
            f"after a wait of {wait_time:.2f}"
        )

        # --------------------------------------------------------
        # Snap pickup and destination to graph
        # --------------------------------------------------------

        pickup_vertex = find_nearest_vertex(
            rider.start_location,
            self.map.node_coordinates
        )

        destination_vertex = find_nearest_vertex(
            rider.destination,
            self.map.node_coordinates
        )

        # --------------------------------------------------------
        # Run Dijkstra for passenger trip
        # --------------------------------------------------------

        route, trip_time = (
            find_the_shortest_path(
                self.map,
                pickup_vertex,
                destination_vertex
            )
        )

        # --------------------------------------------------------
        # Destination unreachable
        # --------------------------------------------------------

        if route is None:

            rider.status = "unsuccessful"

            # Record busy time accumulated so far
            if car.busy_start_time is not None:

                car.total_busy_time += (
                    self.current_time
                    -
                    car.busy_start_time
                )

            car.busy_start_time = None

            car.assigned_rider = None

            # Return car to availability AT PICKUP LOCATION
            self.add_available_car(
                car
            )

            self.log(
                f"TIME {self.current_time:.2f}: "
                f"Trip for {rider.id} failed because "
                f"the destination was unreachable"
            )

            return

        # --------------------------------------------------------
        # Store passenger route
        # --------------------------------------------------------

        car.route = route

        car.route_time = trip_time

        # --------------------------------------------------------
        # Schedule dropoff using DIJKSTRA trip time
        # --------------------------------------------------------

        dropoff_time = (
            self.current_time
            +
            trip_time
        )

        self.schedule_event(
            dropoff_time,
            "DROPOFF_ARRIVAL",
            car
        )

    # ============================================================
    # DROPOFF ARRIVAL
    # ============================================================

    def handle_dropoff_arrival(
        self,
        car
    ):
        """
        Processes successful trip completion.
        """

        rider = car.assigned_rider

        if rider is None:
            raise RuntimeError(
                f"{car.id} reached dropoff "
                f"without an assigned rider."
            )

        # --------------------------------------------------------
        # Update physical car location
        # --------------------------------------------------------

        car.location = (
            rider.destination
        )

        # --------------------------------------------------------
        # Rider state
        # --------------------------------------------------------

        rider.status = "completed"

        rider.dropoff_time = (
            self.current_time
        )

        # --------------------------------------------------------
        # Driver Metrics
        # --------------------------------------------------------

        if car.busy_start_time is not None:

            car.total_busy_time += (
                self.current_time
                -
                car.busy_start_time
            )

        car.busy_start_time = None

        car.trips_completed += 1

        # --------------------------------------------------------
        # Unlink rider
        # --------------------------------------------------------

        car.assigned_rider = None

        # --------------------------------------------------------
        # Reinsert car using NEW Point at NEW location
        # --------------------------------------------------------

        self.add_available_car(
            car
        )

        self.log(
            f"TIME {self.current_time:.2f}: "
            f"{car.id} dropped off {rider.id} "
            f"at {car.location}"
        )

    # ============================================================
    # EVENT LOOP
    # ============================================================

    def run(self):
        """
        Runs the complete discrete-event simulation.

        New rider generation may stop at max_time or
        num_riders, but the event loop continues until
        all active pickup/dropoff events are finished.
        """

        # If nothing was scheduled manually,
        # begin with the first rider at time 0.
        if (
            not self.events
            and
            self.riders_generated == 0
        ):
            self.start()

        print()

        print(
            "STARTING FINAL RIDE-SHARING SIMULATION"
        )

        print(
            "---------------------------------------"
        )

        # IMPORTANT:
        # Do not include max_time in this while condition.
        # Active trips must be allowed to finish.
        while self.events:

            (
                timestamp,
                sequence_number,
                event_type,
                data
            ) = heapq.heappop(
                self.events
            )

            # Advance the simulation clock
            self.current_time = (
                timestamp
            )

            # --------------------------------------------
            # RIDER REQUEST
            # --------------------------------------------

            if event_type == "RIDER_REQUEST":

                self.handle_rider_request(
                    data
                )

            # --------------------------------------------
            # PICKUP
            # --------------------------------------------

            elif event_type == "PICKUP_ARRIVAL":

                self.handle_pickup_arrival(
                    data
                )

            # --------------------------------------------
            # DROPOFF
            # --------------------------------------------

            elif event_type == "DROPOFF_ARRIVAL":

                self.handle_dropoff_arrival(
                    data
                )

            # --------------------------------------------
            # UNKNOWN EVENT
            # --------------------------------------------

            else:

                raise ValueError(
                    f"Unknown event type: "
                    f"{event_type}"
                )

        print(
            "---------------------------------------"
        )

        print(
            "SIMULATION COMPLETE"
        )

    # ============================================================
    # METRICS
    # ============================================================

    def calculate_metrics(self):
        """
        Calculates final simulation performance metrics.
        """

        riders = list(
            self.riders.values()
        )

        completed = [
            rider
            for rider in riders
            if rider.status == "completed"
        ]

        unsuccessful = [
            rider
            for rider in riders
            if rider.status in (
                "unmatched",
                "unsuccessful"
            )
        ]

        # --------------------------------------------------------
        # Rider Wait Times
        # --------------------------------------------------------

        wait_times = [
            rider.pickup_time
            -
            rider.request_time

            for rider in completed

            if (
                rider.pickup_time is not None
                and
                rider.request_time is not None
            )
        ]

        # --------------------------------------------------------
        # Passenger Trip Times
        # --------------------------------------------------------

        trip_times = [
            rider.dropoff_time
            -
            rider.pickup_time

            for rider in completed

            if (
                rider.dropoff_time is not None
                and
                rider.pickup_time is not None
            )
        ]

        average_wait = (
            sum(wait_times)
            /
            len(wait_times)

            if wait_times

            else 0
        )

        average_trip = (
            sum(trip_times)
            /
            len(trip_times)

            if trip_times

            else 0
        )

        # Final processed event time
        simulation_span = (
            self.current_time
        )

        total_busy_time = sum(
            car.total_busy_time
            for car in self.cars.values()
        )

        # --------------------------------------------------------
        # Driver Utilization
        #
        # total busy time
        # ------------------------------
        # cars * simulation span
        # --------------------------------------------------------

        if (
            self.cars
            and
            simulation_span > 0
        ):

            utilization = (
                total_busy_time
                /
                (
                    len(self.cars)
                    *
                    simulation_span
                )
            )

        else:

            utilization = 0

        trips_per_car = {
            car.id: car.trips_completed
            for car in self.cars.values()
        }

        return {
            "total_riders": self.riders_generated,
            "completed": len(completed),
            "unsuccessful": len(unsuccessful),
            "average_wait": average_wait,
            "average_trip": average_trip,
            "utilization": utilization,
            "simulation_span": simulation_span,
            "trips_per_car": trips_per_car
        }

    def print_metrics(self):
        """
        Prints final simulation metrics.
        """

        metrics = (
            self.calculate_metrics()
        )

        print()

        print(
            "FINAL SIMULATION METRICS"
        )

        print(
            "--------------------------------"
        )

        print(
            f"Total Riders Generated: "
            f"{metrics['total_riders']}"
        )

        print(
            f"Completed Riders: "
            f"{metrics['completed']}"
        )

        print(
            f"Unmatched/Unsuccessful Riders: "
            f"{metrics['unsuccessful']}"
        )

        print(
            f"Average Rider Wait Time: "
            f"{metrics['average_wait']:.2f}"
        )

        print(
            f"Average Completed Trip Time: "
            f"{metrics['average_trip']:.2f}"
        )

        print(
            f"Driver Utilization: "
            f"{metrics['utilization'] * 100:.2f}%"
        )

        print()

        print(
            "TRIPS COMPLETED PER CAR"
        )

        for car_id, trips in (
            metrics["trips_per_car"].items()
        ):

            print(
                f"{car_id}: {trips}"
            )

    # ============================================================
    # ANALYTICAL VISUALIZATION
    # ============================================================

    def create_summary_visualization(
        self,
        filename="simulation_summary.png"
    ):
        """
        Creates the required PNG containing:

        - Final car-location map
        - Major simulation metrics
        - Trips-per-car chart
        """

        try:
            plt = __import__(
                "matplotlib.pyplot",
                fromlist=["pyplot"]
            )
        except ImportError as error:
            raise RuntimeError(
                "Creating visualizations requires matplotlib. "
                "Install it with: python -m pip install matplotlib"
            ) from error

        metrics = (
            self.calculate_metrics()
        )

        # --------------------------------------------------------
        # Create figure
        # --------------------------------------------------------

        figure = plt.figure(
            figsize=(14, 8)
        )

        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=[2, 1]
        )

        # ========================================================
        # LEFT SIDE: CITY MAP
        # ========================================================

        map_axis = figure.add_subplot(
            grid[:, 0]
        )

        # Draw graph roads
        for start_node, neighbors in (
            self.map.adjacency_list.items()
        ):

            if (
                start_node
                not in self.map.node_coordinates
            ):
                continue

            start_x, start_y = (
                self.map.node_coordinates[
                    start_node
                ]
            )

            for end_node, weight in neighbors:

                if (
                    end_node
                    not in self.map.node_coordinates
                ):
                    continue

                end_x, end_y = (
                    self.map.node_coordinates[
                        end_node
                    ]
                )

                map_axis.plot(
                    [start_x, end_x],
                    [start_y, end_y],
                    linewidth=0.5
                )

        # Final car coordinates
        car_x = [
            car.location[0]
            for car in self.cars.values()
        ]

        car_y = [
            car.location[1]
            for car in self.cars.values()
        ]

        map_axis.scatter(
            car_x,
            car_y
        )

        map_axis.set_title(
            "Final Car Locations"
        )

        map_axis.set_xlabel(
            "X Coordinate"
        )

        map_axis.set_ylabel(
            "Y Coordinate"
        )

        # ========================================================
        # TOP RIGHT: METRICS
        # ========================================================

        metrics_axis = figure.add_subplot(
            grid[0, 1]
        )

        metrics_axis.axis(
            "off"
        )

        metrics_text = (
            f"Total Riders: "
            f"{metrics['total_riders']}\n"
            f"Completed: "
            f"{metrics['completed']}\n"
            f"Unsuccessful: "
            f"{metrics['unsuccessful']}\n"
            f"Average Wait: "
            f"{metrics['average_wait']:.2f}\n"
            f"Average Trip: "
            f"{metrics['average_trip']:.2f}\n"
            f"Driver Utilization: "
            f"{metrics['utilization'] * 100:.2f}%\n"
            f"Simulation Span: "
            f"{metrics['simulation_span']:.2f}"
        )

        metrics_axis.text(
            0.05,
            0.95,
            metrics_text,
            va="top",
            fontsize=12
        )

        metrics_axis.set_title(
            "Simulation Metrics"
        )

        # ========================================================
        # BOTTOM RIGHT: TRIPS PER CAR
        # ========================================================

        chart_axis = figure.add_subplot(
            grid[1, 1]
        )

        car_ids = list(
            metrics[
                "trips_per_car"
            ].keys()
        )

        trip_counts = list(
            metrics[
                "trips_per_car"
            ].values()
        )

        chart_axis.bar(
            car_ids,
            trip_counts
        )

        chart_axis.set_title(
            "Trips Completed Per Car"
        )

        chart_axis.set_xlabel(
            "Car"
        )

        chart_axis.set_ylabel(
            "Trips Completed"
        )

        chart_axis.tick_params(
            axis="x",
            rotation=90
        )

        # --------------------------------------------------------
        # Save PNG
        # --------------------------------------------------------

        figure.tight_layout()

        figure.savefig(
            filename,
            dpi=150
        )

        plt.close(
            figure
        )

        print(
            f"Created {filename}"
        )

    # ============================================================
    # PRINTABLE SUMMARY
    # ============================================================

    def __str__(self):
        """
        Returns a readable summary of the simulation.
        """

        return (
            f"Cars: {len(self.cars)}\n"
            f"Riders: {len(self.riders)}\n"
            f"Available Cars: "
            f"{len(self.available_cars)}\n"
            f"Current Time: "
            f"{self.current_time:.2f}"
        )