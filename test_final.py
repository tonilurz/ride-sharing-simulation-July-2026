"""
Final integration tests for the Ride-Sharing Simulator.

These tests verify the major correctness requirements
for Assignment 7.2.
"""

import heapq

import pytest

from car import Car
from rider import Rider
from simulation import Simulation

from quadtree import (
    Point,
    Rectangle,
    Quadtree
)

from pathfinder import find_the_shortest_path
from graph import Graph


# ============================================================
# HELPER FUNCTION
# ============================================================

def create_test_map(tmp_path):
    """
    Creates a small connected two-way map used
    by several integration tests.

    A -------- B

    Travel time:
    A <-> B = 1
    """

    map_file = tmp_path / "test_city_map.csv"

    map_file.write_text(
        "start_node_id,start_x,start_y,"
        "end_node_id,end_x,end_y,weight\n"
        "A,0,0,B,10,0,1\n"
        "B,10,0,A,0,0,1\n"
    )

    return str(map_file)


# ============================================================
# TEST 1
# TWO EVENTS AT THE SAME TIMESTAMP
# ============================================================

def test_same_timestamp_events_have_unique_sequence_numbers(
    tmp_path
):
    """
    Two events may occur at the same timestamp.

    The sequence number should preserve deterministic
    ordering and prevent heapq from comparing objects.
    """

    map_file = create_test_map(tmp_path)

    simulation = Simulation(
        map_filename=map_file,
        max_time=0,
        num_riders=0,
        candidate_count=1
    )

    simulation.schedule_event(
        10,
        "TEST_EVENT",
        "FIRST"
    )

    simulation.schedule_event(
        10,
        "TEST_EVENT",
        "SECOND"
    )

    first_event = heapq.heappop(
        simulation.events
    )

    second_event = heapq.heappop(
        simulation.events
    )

    # Same timestamp
    assert first_event[0] == 10
    assert second_event[0] == 10

    # Different sequence numbers
    assert first_event[1] != second_event[1]

    # First scheduled event should be first
    assert first_event[3] == "FIRST"
    assert second_event[3] == "SECOND"


# ============================================================
# TEST 2
# QUADTREE WITH FEWER THAN K CARS
# ============================================================

def test_find_k_nearest_with_fewer_than_k_points():
    """
    Asking for five cars should still work
    when only two cars exist.
    """

    boundary = Rectangle(
        0,
        0,
        100,
        100
    )

    quadtree = Quadtree(
        boundary,
        capacity=4
    )

    point_one = Point(
        10,
        10,
        "CAR001"
    )

    point_two = Point(
        20,
        20,
        "CAR002"
    )

    quadtree.insert(point_one)
    quadtree.insert(point_two)

    results = quadtree.find_k_nearest(
        Point(0, 0),
        k=5
    )

    assert len(results) == 2

    assert point_one in results
    assert point_two in results


# ============================================================
# TEST 3
# EMPTY QUADTREE
# ============================================================

def test_find_k_nearest_empty_quadtree():
    """
    An empty Quadtree should return an empty list,
    not crash.
    """

    quadtree = Quadtree(
        Rectangle(
            0,
            0,
            100,
            100
        )
    )

    results = quadtree.find_k_nearest(
        Point(50, 50),
        k=5
    )

    assert results == []


# ============================================================
# TEST 4
# INVALID K VALUE
# ============================================================

def test_find_k_nearest_rejects_zero_k():
    """
    k must be greater than zero.
    """

    quadtree = Quadtree(
        Rectangle(
            0,
            0,
            100,
            100
        )
    )

    with pytest.raises(ValueError):

        quadtree.find_k_nearest(
            Point(50, 50),
            k=0
        )


# ============================================================
# TEST 5
# IDENTICAL CAR COORDINATES
# ============================================================

def test_two_points_at_same_coordinates_are_separate():
    """
    Two cars may occupy the same coordinates.

    Removing one Point must not accidentally
    remove the other.
    """

    quadtree = Quadtree(
        Rectangle(
            0,
            0,
            100,
            100
        ),
        capacity=4
    )

    point_one = Point(
        50,
        50,
        "CAR001"
    )

    point_two = Point(
        50,
        50,
        "CAR002"
    )

    quadtree.insert(point_one)
    quadtree.insert(point_two)

    # Remove only the first exact object
    removed = quadtree.remove(
        point_one
    )

    assert removed is True

    # Second point must still exist
    remaining = quadtree.find_k_nearest(
        Point(50, 50),
        k=5
    )

    assert point_one not in remaining
    assert point_two in remaining


# ============================================================
# TEST 6
# NO EVENT MAY BE SCHEDULED AT INFINITY
# ============================================================

def test_simulation_rejects_infinite_event(tmp_path):
    """
    The simulation must never place an event at
    float('inf') on the event heap.
    """

    map_file = create_test_map(tmp_path)

    simulation = Simulation(
        map_filename=map_file,
        max_time=0,
        num_riders=0,
        candidate_count=1
    )

    with pytest.raises(ValueError):

        simulation.schedule_event(
            float("inf"),
            "PICKUP_ARRIVAL",
            None
        )


# ============================================================
# TEST 7
# CAR REMOVED FROM AVAILABILITY WHILE BUSY
# ============================================================

def test_busy_car_removed_from_quadtree(tmp_path):
    """
    When a car is dispatched it must disappear
    from all available-car structures.
    """

    map_file = create_test_map(tmp_path)

    simulation = Simulation(
        map_filename=map_file,
        max_time=0,
        num_riders=0,
        candidate_count=1
    )

    car = Car(
        "CAR001",
        (10, 0)
    )

    simulation.cars[
        car.id
    ] = car

    simulation.add_available_car(
        car
    )

    assert car.id in simulation.available_cars

    assert (
        car.id
        in simulation.available_car_points
    )

    # Save the exact old Point
    old_point = (
        simulation.available_car_points[
            car.id
        ]
    )

    simulation.remove_available_car(
        car
    )

    assert (
        car.id
        not in simulation.available_cars
    )

    assert (
        car.id
        not in simulation.available_car_points
    )

    nearby = (
        simulation.available_car_quadtree.find_k_nearest(
            Point(
                car.location[0],
                car.location[1]
            ),
            k=5
        )
    )

    assert old_point not in nearby


# ============================================================
# TEST 8
# CAR REINSERTED AT NEW LOCATION
# ============================================================

def test_car_reinserted_with_new_point(tmp_path):
    """
    After a trip finishes, an available car should
    receive a NEW Point at its new physical location.
    """

    map_file = create_test_map(tmp_path)

    simulation = Simulation(
        map_filename=map_file,
        max_time=0,
        num_riders=0,
        candidate_count=1
    )

    car = Car(
        "CAR001",
        (0, 0)
    )

    simulation.cars[
        car.id
    ] = car

    simulation.add_available_car(
        car
    )

    old_point = (
        simulation.available_car_points[
            car.id
        ]
    )

    simulation.remove_available_car(
        car
    )

    # Car moved during a trip
    car.location = (
        10,
        0
    )

    simulation.add_available_car(
        car
    )

    new_point = (
        simulation.available_car_points[
            car.id
        ]
    )

    # It must be a new Point object
    assert new_point is not old_point

    assert new_point.x == 10
    assert new_point.y == 0

    assert car.status == "available"


# ============================================================
# TEST 9
# DIJKSTRA NO-PATH CONTRACT
# ============================================================

def test_dijkstra_returns_infinity_when_unreachable():
    """
    Dijkstra must return:
        (None, float('inf'))
    when no path exists.
    """

    graph = Graph()

    graph.adjacency_list["A"] = [
        ("B", 1.0)
    ]

    graph.adjacency_list["B"] = []

    # C is disconnected
    graph.adjacency_list["C"] = []

    path, travel_time = (
        find_the_shortest_path(
            graph,
            "A",
            "C"
        )
    )

    assert path is None

    assert travel_time == float("inf")


# ============================================================
# TEST 10
# UNREACHABLE CANDIDATE IS SKIPPED
# ============================================================

def test_unreachable_candidate_is_skipped(tmp_path):
    """
    The Quadtree may return a geographically close car
    that cannot reach the rider through the road network.

    The simulator must skip it and choose a reachable car.
    """

    map_file = (
        tmp_path
        /
        "disconnected_map.csv"
    )

    map_file.write_text(
        "start_node_id,start_x,start_y,"
        "end_node_id,end_x,end_y,weight\n"

        # Connected component 1
        "A,0,0,B,10,0,1\n"
        "B,10,0,A,0,0,1\n"

        # Separate disconnected component
        "E,1,0,F,1,10,1\n"
        "F,1,10,E,1,0,1\n"
    )

    simulation = Simulation(
        map_filename=str(map_file),
        max_time=0,
        num_riders=0,
        candidate_count=2
    )

    # This car is geographically close,
    # but its graph component cannot reach A.
    unreachable_car = Car(
        "CAR001",
        (1, 0)
    )

    # This car is farther away physically,
    # but is connected to the rider's node.
    reachable_car = Car(
        "CAR002",
        (10, 0)
    )

    simulation.cars[
        unreachable_car.id
    ] = unreachable_car

    simulation.cars[
        reachable_car.id
    ] = reachable_car

    simulation.add_available_car(
        unreachable_car
    )

    simulation.add_available_car(
        reachable_car
    )

    rider = Rider(
        "RIDER001",
        (0, 0),
        (10, 0)
    )

    simulation.riders[
        rider.id
    ] = rider

    simulation.handle_rider_request(
        rider
    )

    # Reachable car should be selected
    assert (
        reachable_car.status
        ==
        "en_route_to_pickup"
    )

    # Unreachable car should remain available
    assert (
        unreachable_car.status
        ==
        "available"
    )

    assert (
        unreachable_car.id
        in simulation.available_cars
    )

    assert (
        reachable_car.id
        not in simulation.available_cars
    )


# ============================================================
# TEST 11
# ACTIVE TRIP FINISHES AFTER GENERATION TIME LIMIT
# ============================================================

def test_active_trip_finishes_after_max_time(tmp_path):
    """
    max_time controls new rider generation.

    It must NOT stop an already active trip.
    """

    map_file = create_test_map(
        tmp_path
    )

    simulation = Simulation(
        map_filename=map_file,

        # No new riders after time zero
        max_time=0,

        num_riders=1,

        candidate_count=1
    )

    car = Car(
        "CAR001",
        (10, 0)
    )

    simulation.cars[
        car.id
    ] = car

    simulation.add_available_car(
        car
    )

    rider = Rider(
        "RIDER001",

        # Pickup at A
        (0, 0),

        # Dropoff at B
        (10, 0)
    )

    simulation.riders[
        rider.id
    ] = rider

    # Tell generation logic this is our one rider
    simulation.riders_generated = 1

    simulation.schedule_event(
        0,
        "RIDER_REQUEST",
        rider
    )

    simulation.run()

    # Pickup requires one unit of time.
    # Dropoff requires another unit.
    # The trip therefore ends after max_time=0.
    assert simulation.current_time == 2

    assert rider.status == "completed"

    assert car.status == "available"

    assert car.location == (
        10,
        0
    )

    assert len(simulation.events) == 0

# ============================================================
# TEST 12
# Single Nearest Quadtree search
# ============================================================

def test_quadtree_find_nearest():
    """
    Verifies that the Quadtree finds the closest
    single Point correctly.
    """

    quadtree = Quadtree(
        Rectangle(
            0,
            0,
            100,
            100
        ),
        capacity=2
    )

    point_one = Point(
        10,
        10,
        "CAR001"
    )

    point_two = Point(
        80,
        80,
        "CAR002"
    )

    point_three = Point(
        45,
        45,
        "CAR003"
    )

    quadtree.insert(point_one)
    quadtree.insert(point_two)
    quadtree.insert(point_three)

    result = quadtree.find_nearest(
        Point(48, 48)
    )

    assert result is point_three

# ============================================================
# TEST 13
# Make sure Quadtree sorts k-nearest correctly
# ============================================================

def test_find_k_nearest_returns_nearest_first():

    quadtree = Quadtree(
        Rectangle(
            0,
            0,
            100,
            100
        ),
        capacity=2
    )

    point_one = Point(10, 10, "CAR001")
    point_two = Point(20, 20, "CAR002")
    point_three = Point(30, 30, "CAR003")
    point_four = Point(90, 90, "CAR004")

    for point in (
        point_one,
        point_two,
        point_three,
        point_four
    ):
        quadtree.insert(point)

    results = quadtree.find_k_nearest(
        Point(0, 0),
        k=3
    )

    assert results == [
        point_one,
        point_two,
        point_three
    ]

# ============================================================
# TEST 14
# Successful full rider lifecycle
# ============================================================

def test_complete_rider_lifecycle(tmp_path):

    map_file = create_test_map(
        tmp_path
    )

    simulation = Simulation(
        map_filename=map_file,
        max_time=0,
        num_riders=1,
        candidate_count=1
    )

    car = Car(
        "CAR001",
        (10, 0)
    )

    simulation.cars[
        car.id
    ] = car

    simulation.add_available_car(
        car
    )

    rider = Rider(
        "RIDER001",
        (0, 0),
        (10, 0)
    )

    simulation.riders[
        rider.id
    ] = rider

    simulation.riders_generated = 1

    simulation.schedule_event(
        0,
        "RIDER_REQUEST",
        rider
    )

    simulation.run()

    assert rider.status == "completed"

    assert rider.request_time == 0

    assert rider.pickup_time is not None

    assert rider.dropoff_time is not None

    assert (
        rider.request_time
        <= rider.pickup_time
        <= rider.dropoff_time
    )

    assert car.status == "available"

    assert car.assigned_rider is None

    assert car.trips_completed == 1

# ============================================================
# TEST 15
# Final metrics
# ============================================================

def test_final_metrics_after_completed_trip(
    tmp_path
):

    map_file = create_test_map(
        tmp_path
    )

    simulation = Simulation(
        map_filename=map_file,
        max_time=0,
        num_riders=1,
        candidate_count=1
    )

    car = Car(
        "CAR001",
        (10, 0)
    )

    simulation.cars[
        car.id
    ] = car

    simulation.add_available_car(
        car
    )

    rider = Rider(
        "RIDER001",
        (0, 0),
        (10, 0)
    )

    simulation.riders[
        rider.id
    ] = rider

    simulation.riders_generated = 1

    simulation.schedule_event(
        0,
        "RIDER_REQUEST",
        rider
    )

    simulation.run()

    metrics = (
        simulation.calculate_metrics()
    )

    assert metrics["total_riders"] == 1
    assert metrics["completed"] == 1
    assert metrics["unsuccessful"] == 0

    assert metrics["average_wait"] >= 0
    assert metrics["average_trip"] >= 0

    assert (
        0
        <= metrics["utilization"]
        <= 1
    )

    assert (
        metrics["trips_per_car"]["CAR001"]
        == 1
    )
# ============================================================
# TEST 16
# No available car
# ============================================================

def test_rider_unmatched_when_no_cars_available(
    tmp_path
):

    map_file = create_test_map(
        tmp_path
    )

    simulation = Simulation(
        map_filename=map_file,
        max_time=0,
        num_riders=0,
        candidate_count=5
    )

    rider = Rider(
        "RIDER001",
        (0, 0),
        (10, 0)
    )

    simulation.riders[
        rider.id
    ] = rider

    simulation.handle_rider_request(
        rider
    )

    assert rider.status == "unmatched"

    assert len(simulation.events) == 0
