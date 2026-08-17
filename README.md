# Ride-Sharing Simulator

## Project Overview

This project is an **Efficient, Analyzed Ride-Sharing Simulator** developed in Python. The project is being built through a series of milestones that introduce different data structures, algorithms, and simulation concepts.

The simulator currently includes:

* `Car` and `Rider` classes
* A `Simulation` controller
* A graph-based city map
* CSV map loading
* Dijkstra's shortest-path algorithm
* Quadtree spatial searching
* Brute-force nearest-car matching
* An event-driven simulation engine
* A min-heap priority queue for chronological event processing
* Placeholder Manhattan-distance navigation

The project demonstrates how data structures and algorithms can be combined to model the core functionality of a ride-sharing service.

---

# Milestone 1: Car, Rider, and Simulation Classes

The first milestone created the main objects used by the ride-sharing simulator.

## Car Class

The `Car` class represents a vehicle in the ride-sharing system.

Each car stores information such as:

* Car ID
* Current location
* Current status
* Assigned rider
* Planned route
* Route travel time

Beginning with the Simulation Engine Prototype, a car's location is represented using physical `(x, y)` coordinates.

Example:

```python
car = Car("CAR001", (0, 0))
```

A car can have statuses such as:

* `available`
* `en_route_to_pickup`
* `en_route_to_destination`

The `assigned_rider` attribute links a car to the rider it is currently serving.

---

## Rider Class

The `Rider` class represents a person requesting transportation.

Each rider stores:

* Rider ID
* Starting location
* Destination
* Current status

Example:

```python
rider = Rider(
    "RIDER_A",
    (10, 5),
    (40, 30)
)
```

Rider statuses include:

* `waiting`
* `in_car`
* `completed`

---

## Simulation Class

The `Simulation` class acts as the main controller for the project.

Cars and riders are stored in dictionaries using their IDs as keys.

Example:

```python
self.cars = {}
self.riders = {}
```

Using dictionaries allows cars and riders to be efficiently accessed by their unique IDs.

---

# Milestone 2: Graph Data Structure

The second milestone introduced the `Graph` class to represent the city road network.

The graph uses an **adjacency list** implemented with a Python dictionary.

Example:

```python
{
    "A": [("B", 5), ("C", 3)],
    "B": [("A", 5), ("D", 4)]
}
```

Each dictionary key represents a map node.

The value contains a list of tuples representing:

```text
(neighbor, travel_time)
```

An adjacency list is appropriate because road networks are generally sparse. Most intersections connect to only a small number of other intersections.

---

## Map File

The city map is stored in:

```text
map.csv
```

The map contains directed edges between locations.

Example:

```text
A,B,5
B,A,5
A,C,3
C,A,3
B,D,4
D,B,4
C,D,1
D,C,1
```

Two entries are used to represent a two-way road.

---

## Graph Methods

The Graph class includes methods such as:

```python
add_vertex()
```

Adds a node to the graph if it does not already exist.

```python
add_edge()
```

Creates a weighted connection between two nodes.

```python
load_from_file()
```

Reads the city map from `map.csv` and builds the adjacency list.

```python
__str__()
```

Returns a readable representation of the loaded graph for testing and debugging.

---

# Milestone 3: Dijkstra's Pathfinding Algorithm

The third milestone added intelligent navigation to the project using **Dijkstra's shortest-path algorithm**.

The algorithm determines the fastest route between two nodes in the weighted graph.

The pathfinding functionality is contained in:

```text
pathfinder.py
```

The primary function is:

```python
find_shortest_path(graph, start_node, end_node)
```

The function returns:

1. The shortest path as a list of nodes.
2. The total travel time.

Example:

```text
Shortest Path: ['A', 'C', 'D']
Total Travel Time: 4
```

---

## Priority Queue

Dijkstra's algorithm uses Python's `heapq` module to implement a **min-heap priority queue**.

The heap stores entries in the form:

```python
(distance, node)
```

This allows the algorithm to efficiently process the next node with the shortest known distance.

---

## Path Reconstruction

A predecessor dictionary records how each node was reached.

After reaching the destination, the algorithm follows these predecessors backward to reconstruct the complete route.

If no route exists, the function returns:

```python
(None, float("inf"))
```

---

## Car Route Calculation

The `Car` class also includes a `calculate_route()` method.

The calculated results can be stored in:

```python
self.route
self.route_time
```

This allows a car to remember its planned route and estimated travel time.

The Simulation Engine Prototype uses placeholder coordinate-based navigation instead of Dijkstra's algorithm. Full integration of physical coordinates with the graph-based pathfinding system will occur in the final project milestone.

---

# Milestone 4: Quadtree Data Structure

The fourth milestone introduced a **Quadtree** for efficient two-dimensional spatial searching.

The Quadtree will eventually allow the ride-sharing simulator to quickly locate cars near a rider.

The implementation is contained in:

```text
quadtree.py
```

The main classes include:

* `Point`
* `Rectangle`
* `QuadtreeNode`
* `Quadtree`

---

## Point

The `Point` class represents a location on the two-dimensional city map.

A point contains:

* X coordinate
* Y coordinate
* Optional associated data

The associated data can represent information such as a driver ID or `Car` object.

---

## Rectangle

The `Rectangle` class represents the boundaries used by Quadtree nodes.

It determines:

* Whether a point falls inside a region.
* The minimum squared distance between a query point and the rectangular region.

This distance calculation is important for pruning unnecessary branches during nearest-neighbor searches.

---

## QuadtreeNode

Each `QuadtreeNode` represents one rectangular section of the map.

A node contains:

* Boundary
* Capacity
* Stored points
* Divided status
* Northwest child
* Northeast child
* Southwest child
* Southeast child

When a node reaches capacity, it subdivides into four smaller regions.

---

## Recursive Insertion

Points are inserted recursively.

If a node has available capacity, the point is stored there.

When the node becomes full, it subdivides and its points are moved into the appropriate child quadrants.

---

## Nearest-Neighbor Search

The Quadtree implements:

```python
find_nearest()
```

to locate the point closest to a query location.

The recursive search uses **pruning** to avoid searching regions that cannot contain a closer point.

If the minimum possible distance to a region is already greater than the best distance found, that entire branch can be skipped.

This provides a significant performance improvement over checking every point.

A brute-force nearest-neighbor search requires:

```text
O(N)
```

comparisons.

A well-balanced Quadtree can provide approximately:

```text
O(log N)
```

average search performance.

---

## Quadtree Testing

The file:

```text
test_quadtree.py
```

creates 5,000 random driver points and inserts them into the Quadtree.

A random rider location is then generated.

The test compares:

1. The Quadtree nearest-neighbor result.
2. A brute-force search through all 5,000 points.

An assertion confirms that both methods locate the same point.

Example result:

```text
TEST PASSED

The Quadtree and brute-force search found the same nearest driver.
```

The test also compares the execution time of the two methods.

---

# Milestone 5: Simulation Engine Prototype

The **Simulation Engine Prototype** combines the project's objects into an event-driven ride-sharing simulation.

The purpose of this milestone is to create the central event-processing engine before integrating the advanced Quadtree matching and Dijkstra pathfinding systems.

This milestone uses simplified placeholder algorithms so the focus remains on event handling and state management.

---

## Discrete-Event Simulation

The project now uses a **Discrete-Event Simulation** model.

Instead of updating every car continuously, the simulation jumps from one important event to the next.

Examples of events include:

```text
RIDER_REQUEST
ARRIVAL
```

An `ARRIVAL` event can represent either:

* Arrival at the rider's pickup location.
* Arrival at the rider's destination.

---

## Event Priority Queue

Future events are stored using Python's `heapq` module.

The event queue is a **min-heap**, which automatically allows the simulation to process the event with the earliest timestamp first.

Each event uses the following structure:

```python
(
    timestamp,
    sequence_number,
    event_type,
    data
)
```

The sequence number ensures events remain uniquely ordered even when multiple events have the same timestamp.

---

## Simulation Clock

The Simulation class maintains an internal clock:

```python
self.current_time
```

Whenever an event is removed from the priority queue, the simulation clock advances to that event's timestamp.

This allows the simulation to move directly from event to event rather than processing every individual unit of time.

---

## Event Loop

The `run()` method is the heart of the simulation engine.

It continues processing events while the event heap contains scheduled events.

The next event is retrieved using:

```python
heapq.heappop(self.events)
```

The simulation then determines which handler should process the event.

For example:

```python
if event_type == "RIDER_REQUEST":
    self.handle_rider_request(data)

elif event_type == "ARRIVAL":
    self.handle_arrival(data)
```

This structure allows new event types to be added as the simulation becomes more advanced.

---

## Placeholder Car Matching

The prototype uses:

```python
find_closest_car_brute_force()
```

to locate the closest available car.

The method checks every available car and calculates its distance from the rider.

This is an:

```text
O(N)
```

search.

The brute-force method is intentionally being used as placeholder logic for this milestone. The final simulation will replace this with the previously developed Quadtree nearest-neighbor search.

---

## Placeholder Navigation

The prototype calculates travel time using **Manhattan distance**.

The distance between two locations is calculated as:

```python
abs(x1 - x2) + abs(y1 - y2)
```

Travel time is then calculated using:

```python
travel_time = distance * TRAVEL_SPEED_FACTOR
```

This provides simple navigation for testing the event engine.

The final simulation will replace this placeholder navigation with graph-based routing using Dijkstra's algorithm.

---

## Rider Request Event

When a rider requests a ride, the simulation:

1. Searches for the closest available car.
2. Assigns the rider to that car.
3. Changes the car's status to `en_route_to_pickup`.
4. Calculates the travel time to the rider.
5. Schedules a future `ARRIVAL` event.
6. Logs the dispatch to the console.

The rider and car are linked using:

```python
car.assigned_rider = rider
```

---

## Pickup Event

When an `ARRIVAL` event occurs and the car has the status:

```python
en_route_to_pickup
```

the event represents a pickup.

The simulation:

1. Retrieves the assigned rider.
2. Updates the car's location to the rider's starting location.
3. Changes the car status to `en_route_to_destination`.
4. Changes the rider status to `in_car`.
5. Calculates the travel time to the destination.
6. Schedules another `ARRIVAL` event for the dropoff.

The car's physical location is updated with:

```python
car.location = rider.start_location
```

---

## Dropoff Event

When an `ARRIVAL` event occurs and the car has the status:

```python
en_route_to_destination
```

the event represents a dropoff.

The simulation:

1. Updates the car's location to the rider's destination.
2. Changes the car status back to `available`.
3. Changes the rider status to `completed`.
4. Removes the rider assignment from the car.

The location update is:

```python
car.location = rider.destination
```

The rider is then unlinked:

```python
car.assigned_rider = None
```

---

## Simulation Prototype Test

The `test_simulation.py` file creates:

* Two cars
* Two riders
* Two rider request events

Example starting cars:

```python
car_one = Car("CAR001", (0, 0))
car_two = Car("CAR002", (80, 80))
```

Example riders:

```python
rider_one = Rider(
    "RIDER_A",
    (10, 5),
    (40, 30)
)

rider_two = Rider(
    "RIDER_B",
    (75, 70),
    (20, 60)
)
```

The rider requests are scheduled at different simulation times:

```python
simulation.schedule_event(
    10,
    "RIDER_REQUEST",
    rider_one
)

simulation.schedule_event(
    20,
    "RIDER_REQUEST",
    rider_two
)
```

The event engine then processes the requests, dispatches the cars, performs pickups, and completes the dropoffs in chronological order.

A successful run produces an event sequence similar to:

```text
TIME 10: RIDER RIDER_A requested a ride
TIME 10: CAR CAR001 dispatched to RIDER RIDER_A
TIME 20: RIDER RIDER_B requested a ride
TIME 20: CAR CAR002 dispatched to RIDER RIDER_B
TIME 25.0: CAR CAR001 picked up RIDER RIDER_A
TIME 35.0: CAR CAR002 picked up RIDER RIDER_B
TIME 80.0: CAR CAR001 dropped off RIDER RIDER_A
TIME 100.0: CAR CAR002 dropped off RIDER RIDER_B
```

At the end of the simulation:

```text
CAR001: Location = (40, 30), Status = available
CAR002: Location = (20, 60), Status = available

RIDER_A: Status = completed
RIDER_B: Status = completed
```

This demonstrates that the event engine is correctly scheduling events, processing them chronologically, updating locations, and managing car and rider states.

---

# Project Files

The project currently contains files including:

```text
ride_sharing_simulator/
│
├── car.py
├── rider.py
├── simulation.py
├── graph.py
├── pathfinder.py
├── quadtree.py
├── map.csv
│
├── test_simulation.py
├── test_dijkstra.py
├── test_quadtree.py
│
├── README.md
└── .gitignore
```

---

# How to Run

## Requirements

The project requires:

* Python 3
* No external packages are currently required.

The project uses Python standard-library modules including:

```python
heapq
csv
random
math
time
```

---

## Open the Project

Open a terminal in the project directory.

Example:

```powershell
cd "C:\Users\Toni Lurz\Desktop\MS549 Data Structures and Testing\ride_sharing_simulator"
```

---

## Test the Graph and Original Simulation Components

Run:

```powershell
python test_simulation.py
```

The current version of this test also runs the **Simulation Engine Prototype**.

---

## Test Dijkstra's Algorithm

Run:

```powershell
python test_dijkstra.py
```

This tests the graph-based shortest-path functionality and displays the calculated route and total travel time.

---

## Test the Quadtree

Run:

```powershell
python test_quadtree.py
```

This:

1. Creates a Quadtree.
2. Generates 5,000 random driver locations.
3. Searches for the nearest driver.
4. Performs the same search using brute force.
5. Compares the results.
6. Uses an assertion to verify that both searches found the same driver.
7. Displays the execution times for comparison.

A successful test displays:

```text
TEST PASSED
The Quadtree and brute-force search found the same nearest driver.
```

---

## Run the Simulation Engine Prototype

Run:

```powershell
python test_simulation.py
```

The prototype will:

1. Load the city map from `map.csv`.
2. Create the Simulation object.
3. Create two cars with physical `(x, y)` locations.
4. Create two riders.
5. Add the cars and riders to the Simulation dictionaries.
6. Schedule the rider request events.
7. Run the event-processing loop.
8. Dispatch the closest available cars.
9. Process pickup events.
10. Update the cars' locations at pickup.
11. Process dropoff events.
12. Update the cars' locations at dropoff.
13. Return the cars to `available`.
14. Mark the riders as `completed`.
15. Print the final state of the simulation.

A successful simulation should finish with both cars available and both riders completed.

---

# Current Project Architecture

The project currently demonstrates several different data structures and algorithms:

| Component            | Purpose                        | Data Structure / Algorithm |
| -------------------- | ------------------------------ | -------------------------- |
| Cars                 | Store vehicle objects          | Dictionary                 |
| Riders               | Store rider objects            | Dictionary                 |
| City Map             | Represent roads                | Graph / Adjacency List     |
| Pathfinding          | Find fastest routes            | Dijkstra's Algorithm       |
| Pathfinding Queue    | Select next closest graph node | Min-Heap                   |
| Spatial Search       | Find nearby drivers            | Quadtree                   |
| Prototype Matching   | Find closest available car     | Brute-Force Search         |
| Event Queue          | Process future events          | Min-Heap                   |
| Prototype Navigation | Estimate travel time           | Manhattan Distance         |

---

# Next Steps

The Simulation Engine Prototype proves that the event-driven architecture works correctly using simplified matching and navigation.

The next stage of the project will integrate the advanced components developed in earlier milestones.

The final simulator will replace:

```text
Brute-Force Matching
        ↓
Quadtree Matching
```

and:

```text
Manhattan-Distance Navigation
        ↓
Graph + Dijkstra Pathfinding
```

This will combine the project's individual data structures and algorithms into a complete and efficient ride-sharing simulation.
