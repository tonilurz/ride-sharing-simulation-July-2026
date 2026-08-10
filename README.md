# Ride-Sharing Simulator

## MS549 – Data Structures and Testing
### University of Advancing Technology

**Author:** Antoinette (Toni) Lurz

---

# Project Overview

The Ride-Sharing Simulator is a semester-long project designed to demonstrate object-oriented programming, data structures, algorithms, and software engineering principles using Python.

The simulator models a ride-sharing service by creating vehicles, riders, a road network, and intelligent pathfinding. Each milestone builds upon the previous one, gradually adding more sophisticated functionality while reinforcing efficient data structures and algorithm design.

---

# Technologies Used

- Python 3
- Visual Studio Code
- Git
- GitHub

Python Standard Libraries

- csv
- heapq

---

# Project Structure

```
ride_sharing_simulator/
│
├── car.py
├── rider.py
├── graph.py
├── simulation.py
├── pathfinder.py
│
├── test_simulation.py
├── test_dijkstra.py
│
├── map.csv
├── README.md
└── .gitignore
```

---

# Milestone 1
## Object-Oriented Design

### Objective

Create the core objects used by the simulator.

### Files

- car.py
- rider.py
- simulation.py
- test_simulation.py

### Features

#### Car Class

Stores information about each vehicle.

Attributes

- id
- location
- status
- destination

Methods

- __init__()
- __str__()

---

#### Rider Class

Represents customers requesting rides.

Attributes

- id
- start_location
- destination
- status

Methods

- __init__()
- __str__()

---

#### Simulation Class

Controls the ride-sharing simulation.

Stores

- Cars
- Riders

Both are stored using Python dictionaries for efficient O(1) lookups.

---

### Test

Run:

```bash
python test_simulation.py
```

---

# Milestone 2
## Graph Class

### Objective

Create a city road network using an adjacency list.

### Files Added

- graph.py
- map.csv

### Graph Design

The city map is stored using an adjacency list.

Example

```python
{
    "A": [("B", 5), ("C", 3)],
    "B": [("A", 5), ("D", 4)],
    "C": [("A", 3), ("D", 1)]
}
```

### Why an Adjacency List?

Road networks are sparse graphs.

Using an adjacency list provides

- efficient storage
- fast neighbor lookup
- ideal support for pathfinding algorithms

### Graph Methods

- __init__()
- add_vertex()
- add_edge()
- load_from_file()
- __str__()

---

### Simulation Update

The Simulation class now creates and stores a Graph object.

During initialization the simulation loads the road network directly from map.csv.

```python
self.map = Graph()
self.map.load_from_file(map_filename)
```

---

### Test

Run

```bash
python test_simulation.py
```

The test verifies

- Graph loads correctly
- Simulation initializes correctly
- Adjacency list prints successfully

---

# Milestone 3
## Dijkstra's Shortest Path Algorithm

### Objective

Allow vehicles to calculate the shortest route through the city.

### Files Added

- pathfinder.py
- test_dijkstra.py

### Dijkstra's Algorithm

The simulator now includes an implementation of Dijkstra's Shortest Path Algorithm.

Function

```python
find_the_shortest_path(graph, start_node, end_node)
```

Returns

```python
(path, total_travel_time)
```

Example

```python
(['A', 'C', 'D'], 4.0)
```

If no route exists

```python
(None, float("inf"))
```

---

### Priority Queue

Python's heapq module is used to implement a min-heap priority queue.

Items are stored as

```python
(distance, node)
```

The smallest distance is always processed first.

---

### Data Structures

The algorithm uses

- Distance Dictionary
- Predecessor Dictionary
- Priority Queue
- Adjacency List

These structures work together to efficiently calculate the shortest route.

---

### Big-O Performance

Using an adjacency list and priority queue gives Dijkstra's Algorithm a time complexity of

```
O((V + E) log V)
```

Where

V = Vertices

E = Edges

---

### Test

Run

```bash
python test_dijkstra.py
```

Example Output

```text
DIJKSTRA TEST

Start Node: A
Destination: D

Shortest Path:
['A', 'C', 'D']

Total Travel Time:
4.0
```

---

# Milestone 4
## Route Planning in the Car Class

### Objective

Allow each Car object to calculate and remember its own route.

### Updated File

- car.py

### New Method

```python
calculate_route(destination, graph)
```

The method

- Uses the car's current location
- Runs Dijkstra's Algorithm
- Calculates the shortest route
- Stores the results

New attributes

```python
self.route
self.route_time
```

Example

```python
Car ID:
CAR001

Route:
['A', 'C', 'D']

Travel Time:
4.0
```

Each car now remembers its planned route instead of recalculating it repeatedly.

---

# How to Run

## Test Milestone 1 & 2

```bash
python test_simulation.py
```

Tests

- Car
- Rider
- Graph
- Simulation

---

## Test Milestone 3

```bash
python test_dijkstra.py
```

Tests

- Graph loading
- Dijkstra's Algorithm
- Shortest path calculation

---

## Future Milestones

Future enhancements include

- Driver assignment
- Rider dispatch
- Multiple ride requests
- Vehicle movement
- Dynamic traffic
- Performance analysis
- Algorithm benchmarking

---

# GitHub Repository

The complete project, including source code, documentation, and test scripts, is maintained in a public GitHub repository and updated throughout the semester.

---

# Lessons Learned

Throughout this project I have gained experience with

- Object-Oriented Programming
- Graph Data Structures
- Adjacency Lists
- Dictionaries
- Priority Queues
- Dijkstra's Algorithm
- File Processing
- Git and GitHub
- Software Testing
- Algorithm Analysis
- Big-O Performance

Each milestone builds upon the previous one and demonstrates how data structures and algorithms work together to solve increasingly complex real-world problems.

---

# Author

**Antoinette (Toni) Lurz**

MS549 – Data Structures and Testing

University of Advancing Technology

2026