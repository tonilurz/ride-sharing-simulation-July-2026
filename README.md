# Ride-Sharing Simulator

## MS549 Data Structures and Testing

This project is a Python-based ride-sharing simulation developed throughout the MS549 Data Structures and Testing course.

The project was built in milestones. Each milestone introduced a new data structure, algorithm, testing method, or simulation feature. The final version combines object-oriented programming, graphs, Dijkstra's shortest-path algorithm, Quadtrees, priority queues, discrete-event simulation, automated testing, performance metrics, and visualization.

The goal of the final project is to simulate a ride-sharing system in which riders request transportation, available cars are located efficiently, road-network travel times are calculated, and simulation events are processed chronologically.

---

# Project Overview

The final simulator models a simplified ride-sharing service.

The system contains:

- Cars
- Riders
- A city road network
- Graph node coordinates
- Dijkstra's shortest-path algorithm
- A Quadtree spatial index
- A min-heap event queue
- Dynamic rider generation
- Driver availability tracking
- Pickup and dropoff events
- Simulation performance metrics
- Automated testing with pytest
- Code coverage analysis
- A simulation summary visualization

The final matching process uses both geographic proximity and road-network travel time.

The Quadtree first identifies nearby available cars. Dijkstra's algorithm then evaluates those candidates using the road network. The available car with the lowest road travel time is selected for the rider.

---

# Project Structure

```text
ride_sharing_simulator/
│
├── car.py
├── rider.py
├── graph.py
├── pathfinder.py
├── quadtree.py
├── simulation.py
├── run_simulation.py
│
├── test_simulation.py
├── test_dijkstra.py
├── test_quadtree.py
├── test_final.py
│
├── city_map.csv
├── simulation_summary.png
├── README.md
└── .gitignore
```

---

# Car Class

The `Car` class represents an individual driver/car in the ride-sharing simulation.

Each car contains information including:

- Unique car ID
- Current physical `(x, y)` location
- Current status
- Assigned rider
- Current route
- Route travel time
- Busy start time
- Total busy time
- Number of completed trips

A car begins with the status:

```text
available
```

During the simulation, its status can change as it progresses through a trip.

For example:

```text
available
    ↓
en_route_to_pickup
    ↓
en_route_to_destination
    ↓
available
```

After completing a trip, the car's physical location becomes the rider's destination.

---

# Rider Class

The `Rider` class represents a passenger requesting transportation.

Each rider contains:

- Unique rider ID
- Pickup location
- Destination
- Current status
- Request time
- Pickup time
- Dropoff time

A rider begins with the status:

```text
waiting
```

A successful rider progresses through the simulation approximately as follows:

```text
waiting
    ↓
in_car
    ↓
completed
```

If a rider cannot be matched with a reachable car, the rider can be recorded as unsuccessful or unmatched.

The timestamps stored in the Rider object allow the simulation to calculate rider wait times and completed trip times.

---

# Graph and City Road Network

The city road network is represented using a weighted graph.

The graph uses an adjacency-list data structure.

Conceptually, the structure looks like:

```text
Node
  ↓
[(Neighbor, Weight), (Neighbor, Weight), ...]
```

For example:

```text
A -> [('B', 5.0), ('C', 3.0)]
B -> [('A', 5.0), ('D', 4.0)]
C -> [('A', 3.0), ('D', 1.0)]
D -> [('B', 4.0), ('C', 1.0)]
```

Each graph node also contains physical coordinates.

For example:

```text
A = (0.0, 0.0)
B = (100.0, 0.0)
C = (0.0, 100.0)
D = (100.0, 100.0)
```

This allows the simulator to translate a physical car or rider location into the nearest road-network vertex.

---

# City Map File

The city map is stored in `city_map.csv`.

The file contains:

```text
start_node_id,start_x,start_y,end_node_id,end_x,end_y,weight
```

Each row represents a road connection between two graph vertices.

The graph loader reads:

- Starting node ID
- Starting node X coordinate
- Starting node Y coordinate
- Ending node ID
- Ending node X coordinate
- Ending node Y coordinate
- Road weight

The road weight represents the travel cost or travel time used by Dijkstra's algorithm.

The city map used for development contains a small connected road network so that the simulation behavior can be inspected and tested.

---

# Dijkstra's Shortest-Path Algorithm

The simulator uses Dijkstra's algorithm to determine the shortest road-network path between two graph vertices.

The implementation is located in:

```text
pathfinder.py
```

The main pathfinding function is:

```python
find_the_shortest_path()
```

The function returns:

```text
(path, total_travel_time)
```

For example:

```text
(['A', 'C', 'D'], 4.0)
```

This means the shortest route travels:

```text
A
↓
C
↓
D
```

with a total road-network travel time of:

```text
4.0
```

The implementation uses Python's `heapq` module as a priority queue.

Dijkstra's algorithm provides more realistic routing than using only straight-line or Manhattan distance.

---

# Finding the Nearest Graph Vertex

Cars and riders exist at physical `(x, y)` coordinates, while Dijkstra's algorithm operates on graph node IDs.

The function:

```python
find_nearest_vertex()
```

bridges these two representations.

It determines which graph vertex is physically closest to a supplied `(x, y)` coordinate.

The simulation therefore follows this general process:

```text
Physical Location
      ↓
Nearest Graph Vertex
      ↓
Dijkstra
      ↓
Road Travel Time
```

---

# Quadtree Spatial Index

The project uses a Quadtree to efficiently locate nearby available cars.

The Quadtree is implemented in:

```text
quadtree.py
```

The main supporting classes are:

```text
Point
Rectangle
QuadtreeNode
Quadtree
```

Cars are represented inside the Quadtree using `Point` objects.

A Point stores:

```text
x coordinate
y coordinate
associated car
```

The Quadtree recursively divides the physical map into smaller geographic regions.

This allows the simulator to avoid searching every available car when looking for nearby drivers.

---

# K-Nearest Neighbor Search

The final project extends the Quadtree with:

```python
find_k_nearest()
```

Instead of finding only one geographically closest car, this method returns up to `k` nearby candidates.

The default candidate count is:

```text
k = 5
```

The Quadtree uses a heap to maintain the best candidates while recursively searching the tree.

Branches of the Quadtree that cannot contain a better candidate can be pruned from the search.

This reduces unnecessary searching.

---

# Removing Cars from the Quadtree

The Quadtree also supports:

```python
remove()
```

When a car is assigned to a rider, the exact Point object representing that car is removed from the Quadtree.

Object identity is important during removal.

The comparison uses:

```python
stored_point is point
```

rather than:

```python
stored_point == point
```

Two different cars may occupy exactly the same physical coordinates, but they are still different car objects.

---

# Available Car Management

The Simulation maintains three related availability structures:

```text
available_cars
available_car_points
available_car_quadtree
```

They serve different purposes.

### `available_cars`

Maps a car ID to the available Car object.

```text
car ID → Car
```

### `available_car_points`

Maps a car ID to the exact Point object stored in the Quadtree.

```text
car ID → Point
```

### `available_car_quadtree`

Provides spatial searching for nearby available cars.

These structures must remain synchronized.

When a car becomes unavailable, it is removed from all availability structures.

When a trip is completed, a new Point is created using the car's updated location and the car is reinserted into the availability structures.

---

# Adding an Available Car

The simulation uses:

```python
add_available_car()
```

to add a car to the availability system.

The method:

1. Creates a Point representing the car's current physical location.
2. Inserts the Point into the Quadtree.
3. Adds the car to the available-car dictionary.
4. Stores the exact Point object.
5. Sets the car's status to available.

The dictionaries are updated only after the Quadtree insertion succeeds.

This helps keep the availability structures synchronized.

---

# Removing an Available Car

The simulation uses:

```python
remove_available_car()
```

when a driver is assigned to a rider.

The method:

1. Retrieves the exact Point associated with the car.
2. Removes that Point from the Quadtree.
3. Removes the Point from the Point dictionary.
4. Removes the car from the available-car dictionary.

The car is therefore no longer considered during future rider matching while it is completing a trip.

---

# Quadtree and Dijkstra Driver Matching

The final driver-matching algorithm combines two different algorithms.

The Quadtree answers:

```text
Which available cars are geographically close?
```

Dijkstra answers:

```text
Which of those cars can reach the rider fastest
using the road network?
```

The complete matching pipeline is:

```text
Rider Request
      │
      ▼
Create Rider Point
      │
      ▼
Quadtree
      │
      ▼
Find up to k nearby available cars
      │
      ▼
Convert rider location to graph vertex
      │
      ▼
Convert each candidate car location
to a graph vertex
      │
      ▼
Run Dijkstra for each candidate
      │
      ▼
Compare road travel times
      │
      ▼
Choose lowest reachable travel time
      │
      ▼
Dispatch selected car
```

This is an important design decision.

The geographically closest car is not always the car with the shortest road-network travel time.

The Quadtree reduces the candidate set, while Dijkstra makes the final road-based selection.

---

# Simulation Engine Prototype

The simulation engine was originally developed as a discrete-event simulation prototype.

Instead of updating every car continuously at every possible moment, the simulation jumps directly from one important event to the next.

The simulation uses a min-heap priority queue implemented with Python's:

```python
heapq
```

Events use the following structure:

```text
(
    timestamp,
    sequence_number,
    event_type,
    data
)
```

The timestamp determines when the event occurs.

The sequence number ensures events with the same timestamp can still be ordered safely.

The event type determines which handler processes the event.

The data field contains the object associated with the event.

---

# Final Event Queue

The final simulation uses three primary event types:

```text
RIDER_REQUEST
PICKUP_ARRIVAL
DROPOFF_ARRIVAL
```

The event queue operates as:

```text
Event Heap
    ↓
Pop earliest event
    ↓
Advance simulation clock
    ↓
Determine event type
    ↓
Call appropriate handler
    ↓
Handler may schedule future events
    ↓
Repeat until heap is empty
```

The simulation continues until the event heap is empty.

This is important because rider generation may stop while cars are still completing active trips.

Those pickup and dropoff events must still be processed before the simulation finishes.

---

# Dynamic Rider Generation

Riders are dynamically generated during the simulation.

Rider arrivals use Python's random exponential distribution:

```python
random.expovariate()
```

This provides variable intervals between rider requests.

The simulation can limit rider generation using:

- Maximum simulation generation time
- Maximum number of riders

The first rider request can be scheduled at simulation time:

```text
0
```

Each processed rider request schedules the next request when the configured limits allow it.

---

# Rider Request Event

When a:

```text
RIDER_REQUEST
```

event occurs, the simulation:

1. Records the rider request time.
2. Schedules the next rider request when allowed.
3. Creates a Point at the rider's pickup location.
4. Uses the Quadtree to retrieve nearby available-car candidates.
5. Converts the rider location to the nearest graph vertex.
6. Converts each candidate car location to its nearest graph vertex.
7. Runs Dijkstra for each candidate.
8. Ignores unreachable candidates.
9. Chooses the reachable candidate with the lowest road travel time.
10. Removes the selected car from the availability structures.
11. Links the car and rider.
12. Changes the car's status to `en_route_to_pickup`.
13. Schedules a `PICKUP_ARRIVAL` event.

If no available or reachable car can be found, the rider is recorded as unsuccessful or unmatched.

---

# Pickup Arrival Event

When:

```text
PICKUP_ARRIVAL
```

occurs, the simulation updates the physical and logical state of the system.

The car's physical location becomes:

```python
car.location = rider.start_location
```

The statuses are updated:

```text
Car:
en_route_to_pickup
        ↓
en_route_to_destination

Rider:
waiting
   ↓
in_car
```

The rider's pickup time is recorded.

The rider's wait time can then be calculated as:

```text
pickup time - request time
```

Dijkstra is then used again to calculate the passenger's route from the pickup location to the destination.

A future:

```text
DROPOFF_ARRIVAL
```

event is scheduled using the resulting road travel time.

---

# Dropoff Arrival Event

When:

```text
DROPOFF_ARRIVAL
```

occurs, the rider's trip is completed.

The car's physical location becomes:

```python
car.location = rider.destination
```

The rider's status becomes:

```text
completed
```

The rider's dropoff time is recorded.

The car's:

- Total busy time is updated
- Completed trip count is increased
- Assigned rider is removed

The car is then made available again.

Importantly, the old Quadtree Point is not reused.

Instead:

```text
Old Point removed at dispatch
          ↓
Trip occurs
          ↓
Car reaches new destination
          ↓
Car location changes
          ↓
New Point created
          ↓
New Point inserted into Quadtree
```

This ensures the Quadtree always represents the current physical locations of available cars.

---

# Performance Metrics

The final simulator calculates performance metrics after the event queue finishes processing.

Metrics include:

- Total riders generated
- Completed riders
- Unmatched or unsuccessful riders
- Average rider wait time
- Average completed trip time
- Driver utilization
- Trips completed by each car

### Average Wait Time

Average wait time measures how long successfully served riders waited between requesting a ride and being picked up.

```text
pickup_time - request_time
```

### Average Trip Time

Trip time measures the time between pickup and dropoff.

```text
dropoff_time - pickup_time
```

### Driver Utilization

Driver utilization compares the total amount of time drivers were busy with the total simulation time available across all drivers.

This helps evaluate how heavily the simulated fleet was being used.

---

# Simulation Summary Visualization

The final simulation creates:

```text
simulation_summary.png
```

using Matplotlib.

The summary visualization provides a graphical representation of the completed simulation.

It includes simulation information such as:

- The city/map representation
- Simulation performance metrics
- Rider outcome information

This provides a visual summary in addition to the console-based event log.

---

# Command-Line Controls

The simulation is launched through:

```text
run_simulation.py
```

Command-line arguments allow different simulation configurations to be tested without modifying the Python source code.

Available controls include:

```text
--max-time
--num-riders
--num-cars
--candidate-count
--random-seed
--map-file
```

The candidate count controls the number of geographically nearby cars returned by the Quadtree before Dijkstra evaluates road travel times.

The default candidate count is:

```text
5
```

The random seed allows a simulation run to be reproduced.

---

# How to Run

## 1. Open the Project

Open the `ride_sharing_simulator` project folder in Visual Studio Code.

Open a PowerShell terminal.

Make sure the terminal is located in the project folder.

For example:

```powershell
cd "C:\Users\YourName\Desktop\ride_sharing_simulator"
```

---

## 2. Activate the Virtual Environment

If the project uses a virtual environment named `venv`, activate it with:

```powershell
.\venv\Scripts\Activate.ps1
```

Your terminal should then show the virtual environment as active.

---

## 3. Install Required Packages

The project uses Matplotlib for the final visualization:

```powershell
python -m pip install matplotlib
```

The automated testing environment uses pytest:

```powershell
python -m pip install pytest
```

For coverage analysis:

```powershell
python -m pip install pytest-cov
```

---

## 4. Run the Final Simulation

Run:

```powershell
python run_simulation.py
```

The program will:

1. Load the city map.
2. Create the initial fleet.
3. Add available cars to the Quadtree.
4. Generate rider requests.
5. Process events chronologically.
6. Match riders using Quadtree and Dijkstra.
7. Process pickup events.
8. Process dropoff events.
9. Calculate final performance metrics.
10. Create `simulation_summary.png`.

---

# Running With Custom Settings

The simulation can also be run using command-line arguments.

Example:

```powershell
python run_simulation.py --num-riders 100 --num-cars 20 --max-time 1000
```

To change the number of Quadtree candidates evaluated by Dijkstra:

```powershell
python run_simulation.py --candidate-count 10
```

To reproduce a simulation using a specific random seed:

```powershell
python run_simulation.py --random-seed 42
```

The default candidate count remains:

```text
k = 5
```

---

# Testing Strategy

Automated testing is performed using:

```text
pytest
```

The final test suite verifies the major data structures, algorithms, state transitions, and integration points of the ride-sharing simulator.

Testing includes areas such as:

- Graph behavior
- Dijkstra shortest-path calculations
- Nearest graph-vertex calculations
- Quadtree insertion
- Quadtree nearest-neighbor searching
- K-nearest neighbor searching
- Quadtree removal
- Car availability management
- Event scheduling
- Rider matching
- Pickup processing
- Dropoff processing
- Complete rider lifecycle
- Unmatched rider behavior
- Simulation metrics

The testing strategy focuses on both individual components and integration between the components.

---

# Running the Automated Tests

To run the final automated test suite:

```powershell
python -m pytest test_final.py -v
```

The completed final test suite successfully passes all tests.

Current result:

```text
16 tests passed
```

---

# Code Coverage

Code coverage is measured using:

```text
pytest-cov
```

Run the application-focused coverage test with:

```powershell
python -m pytest test_final.py -v --cov=car --cov=rider --cov=graph --cov=pathfinder --cov=quadtree --cov=simulation --cov-report=term-missing
```

Current coverage results:

| Module | Coverage |
|---|---:|
| `car.py` | 74% |
| `graph.py` | 72% |
| `pathfinder.py` | 91% |
| `quadtree.py` | 78% |
| `rider.py` | 91% |
| `simulation.py` | 58% |
| **Overall** | **69%** |

All final automated tests passed during this coverage run.

Coverage is used as one part of the testing strategy. The project also focuses on meaningful functional tests rather than attempting to execute every line solely to achieve a higher coverage percentage.

---

# Data Structures Used

Several important data structures are used throughout the project.

## Dictionaries

Dictionaries provide efficient access to cars and riders by their unique IDs.

Examples include:

```text
cars
riders
available_cars
available_car_points
```

Typical dictionary lookup is approximately:

```text
O(1)
```

average-case time complexity.

---

## Adjacency List

The road network is represented using an adjacency list.

This is efficient for representing a road network where each graph vertex connects to only a limited number of neighboring vertices.

Graph storage is approximately:

```text
O(V + E)
```

where:

```text
V = vertices
E = edges
```

---

## Min-Heap / Priority Queue

The discrete-event simulation uses a min-heap.

Python's:

```python
heapq
```

allows the earliest event to be efficiently retrieved.

Event insertion and removal are approximately:

```text
O(log N)
```

where `N` is the number of events currently in the queue.

---

## Quadtree

The Quadtree provides a spatial index for available cars.

Instead of performing a brute-force scan of the entire fleet for every rider, the Quadtree can eliminate geographic regions that cannot contain better candidates.

This makes the structure valuable as the number of available cars increases.

---

# Algorithm Design

The final system deliberately separates geographic searching from road-network routing.

A simple brute-force matching approach would compare every available driver for every request.

Instead, the final simulator uses:

```text
Quadtree
    ↓
Small geographic candidate set
    ↓
Dijkstra
    ↓
Road-based comparison
```

This combines the strengths of both algorithms.

The Quadtree reduces the search space.

Dijkstra determines the actual road-network travel cost.

The result is a more efficient and realistic driver-matching strategy than using either simple straight-line distance or a full Dijkstra search for every available driver.

---

# Final Simulation Architecture

The central workflow of the completed system is:

```text
Generate Rider
      │
      ▼
RIDER_REQUEST
      │
      ▼
Quadtree
      │
      ▼
Find k geographically close
available cars
      │
      ▼
Dijkstra
      │
      ▼
Evaluate road travel time
for each candidate
      │
      ▼
Select best reachable car
      │
      ▼
Remove car from availability
and Quadtree
      │
      ▼
PICKUP_ARRIVAL
      │
      ▼
Update car location
      │
      ▼
Dijkstra passenger route
      │
      ▼
DROPOFF_ARRIVAL
      │
      ▼
Update car to rider destination
      │
      ▼
Create new Quadtree Point
      │
      ▼
Return car to availability
      │
      ▼
Calculate final metrics
      │
      ▼
Create simulation_summary.png
```

---

# Development Milestones

The project was developed incrementally throughout the course.

## Milestone 1: Object-Oriented Foundation

Created the initial:

- `Car` class
- `Rider` class
- `Simulation` class

Cars and riders were stored in dictionaries using their unique IDs.

This established the object-oriented foundation for the simulator.

---

## Milestone 2: Graph Data Structure

Created the Graph class and adjacency-list representation of the road network.

This provided the data structure needed for later pathfinding.

---

## Milestone 3: Graph Integration

Expanded the graph implementation and map-loading functionality.

The simulation could load road connections from a map file and represent the road network in memory.

---

## Milestone 4: Dijkstra Pathfinding

Implemented Dijkstra's shortest-path algorithm.

Cars could calculate routes through the graph and determine the total cost of a route.

This milestone introduced priority-queue-based pathfinding using `heapq`.

---

## Milestone 5: Quadtree Spatial Searching

Implemented the Quadtree spatial data structure.

The Quadtree stores Point objects and supports efficient geographic searching.

Nearest-neighbor searching was tested against brute-force searching to verify correctness and compare performance.

---

## Milestone 6: Simulation Engine Prototype

Implemented the discrete-event simulation engine.

This milestone introduced:

- Min-heap event scheduling
- Simulation timestamps
- Rider request events
- Placeholder driver matching
- Pickup arrivals
- Dropoff arrivals
- Car/rider state management

This prototype proved that the event engine could correctly process an entire ride from request through completion.

---

## Milestone 7: Final Integrated Ride-Sharing Simulator

The final milestone replaces the placeholder algorithms with the advanced components created during earlier milestones.

The final simulator integrates:

- Graph road-network representation
- Physical graph-node coordinates
- Dijkstra pathfinding
- Quadtree spatial searching
- K-nearest candidate searching
- Exact Point removal
- Dynamic rider generation
- Event-driven simulation
- Driver availability management
- Pickup and dropoff events
- Performance metrics
- Command-line configuration
- Automated pytest testing
- Code coverage analysis
- Final visualization

The result is a cohesive multi-component ride-sharing simulation.

---

# Final Results

The final simulator successfully demonstrates the complete ride-sharing lifecycle.

A typical successful trip follows:

```text
Rider generated
      ↓
Rider requests ride
      ↓
Nearby drivers found
      ↓
Road routes evaluated
      ↓
Driver selected
      ↓
Driver removed from availability
      ↓
Driver reaches pickup
      ↓
Rider enters car
      ↓
Passenger route calculated
      ↓
Driver reaches destination
      ↓
Rider completed
      ↓
Driver returned to availability
```

The simulation also produces final performance metrics and a graphical summary of the run.

Automated testing verifies the important components of the final system.

Current automated testing result:

```text
16 tests passed
69% overall application code coverage
91% pathfinder coverage
78% Quadtree coverage
91% Rider coverage
```

---

# Technologies Used

- Python 3.10
- Visual Studio Code
- Git
- GitHub
- `heapq`
- `collections`
- `itertools`
- `random`
- `argparse`
- Matplotlib
- pytest
- pytest-cov

---

# Key Concepts Demonstrated

This project demonstrates the practical use and integration of:

- Object-oriented programming
- Encapsulation
- Dictionaries
- Tuples
- Graphs
- Adjacency lists
- Weighted graphs
- Priority queues
- Min-heaps
- Dijkstra's algorithm
- Quadtrees
- Spatial searching
- K-nearest neighbor searching
- Discrete-event simulation
- Event-driven programming
- State management
- Random event generation
- Command-line interfaces
- Performance measurement
- Automated unit and integration testing
- Code coverage analysis
- Data visualization
- Big O analysis

---

# Conclusion

This project demonstrates how multiple data structures and algorithms can be combined to solve a larger computational problem.

The project began with basic Car and Rider objects and progressively added a graph, Dijkstra's shortest-path algorithm, a Quadtree, a priority-queue-based event engine, automated testing, and performance analysis.

The final simulator uses the Quadtree to efficiently identify geographically close available cars and Dijkstra's algorithm to determine which candidate has the best road-network travel time.

The discrete-event simulation then manages rider requests, driver dispatches, pickups, dropoffs, state changes, and driver availability until all scheduled events have been processed.

The final result demonstrates how selecting appropriate data structures and algorithms can improve the organization, efficiency, testability, and performance of a multi-component software system.