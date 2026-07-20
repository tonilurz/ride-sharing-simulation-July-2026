# Ride-Sharing Simulator

## Project Title

Ride-Sharing Simulator

## Purpose / Design

This project is the foundation of a ride-sharing simulation developed in Python using object-oriented programming principles. The first milestone focuses on creating the core classes that represent the vehicles, riders, and the simulation environment. These classes will serve as the building blocks for future milestones, where additional algorithms, data structures, and event-driven simulation features will be added.

The project is designed with modularity in mind by separating each class into its own Python file. Cars and riders are stored in dictionaries using their unique IDs as keys, allowing efficient object lookup and preparing the system for future performance analysis using Big O notation.

## Project Structure

```text
ride_sharing_simulator/
│
├── car.py
├── rider.py
├── simulation.py
├── test_simulation.py
├── README.md
└── .gitignore
```

### Files

* **car.py** - Contains the `Car` class, which represents a vehicle in the ride-sharing fleet.
* **rider.py** - Contains the `Rider` class, which represents a customer requesting transportation.
* **simulation.py** - Contains the `Simulation` class, which manages collections of cars and riders.
* **test_simulation.py** - Creates sample objects and verifies that the classes function correctly.
* **README.md** - Project documentation.

## Object Design

### Car Class

Each `Car` object contains:

* Unique car ID
* Current location as an `(x, y)` tuple
* Current status
* Destination

The default status is **"available"**, and the destination is initialized to **None**.

### Rider Class

Each `Rider` object contains:

* Unique rider ID
* Pickup location
* Destination location
* Current status

The default rider status is **"waiting"**.

### Simulation

The `Simulation` class maintains two dictionaries:

* `cars` – stores `Car` objects using the car ID as the key.
* `riders` – stores `Rider` objects using the rider ID as the key.

Using dictionaries allows efficient retrieval of objects by their unique IDs and supports future algorithm development.

## How to Run

1. Download or clone this repository.
2. Open the project folder in Visual Studio Code.
3. (Optional but recommended) Create and activate a Python virtual environment.

### Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv venv
venv\Scripts\activate
```

4. Run the test script:

```bash
python test_simulation.py
```
If your system uses the Python launcher instead of `python`, run:

```bash
py test_simulation.py
```

## Sample Output
```text
Car CAR001 at (10, 5) - Status: available
Rider RIDER_A at (1, 2) waiting for ride to (20, 15)
Simulation with 1 car(s) and 1 rider(s)
```

## Dependencies
This milestone uses only the Python Standard Library.
No external libraries are required.

## Future Enhancements

Future milestones will expand this project by adding:

* Driver assignment algorithms
* Ride request processing
* Pathfinding algorithms
* Event-driven simulation
* Performance analysis using Big O notation
* Additional data structures for efficient searching and scheduling
* Automated testing and benchmarking

## Author
**Antoinette (Toni) Lurz**
Master of Science Student
University of Advancing Technology (UAT)


Milestone 2: Graph Integration
Overview

In this milestone, the Ride-Sharing Simulator was expanded by adding a Graph class that represents the city road network. The graph uses an adjacency list to efficiently store intersections and the roads that connect them. The graph is automatically loaded from a CSV file when the simulation begins.

# New Files
graph.py

The Graph class represents the city map.

It includes the following methods:

* __init__()
Creates an empty adjacency list using a  Python dictionary.
* add_vertex()
Adds a vertex to the graph if it does not already exist.
* add_edge()
Creates a directed, weighted connection between two vertices.
* load_from_file()
Reads the road network from a CSV file and builds the graph.
* __str__()
Displays the adjacency list in a readable format for testing and debugging.

# Data Structure Selection

The Graph class stores the city map as an adjacency list.

{
    "A": [("B", 5), ("C", 3)],
    "B": [("D", 4)]
}

An adjacency list was selected because road networks are considered sparse graphs, meaning each intersection connects to only a few nearby intersections instead of every location in the city.

Using an adjacency list provides:

* Efficient storage
* Fast neighbor lookups
* Excellent support for graph algorithms  * such as Dijkstra's algorithm

# Map File

The road network is stored in a CSV file named:

city_map.csv

Example:

Start,End,Weight
A,B,5
B,A,5
A,C,3
C,A,3
B,D,4
D,B,4
C,D,1
D,C,1

Each row contains:

Starting intersection
Destination intersection
Road weight or distance

# Simulation Updates

The Simulation class has been updated to automatically create and load the Graph object during initialization.

self.map = Graph()
self.map.load_from_file(map_filename)

This ensures the city map is available whenever the simulation begins.

The Simulation class continues to maintain dictionaries for Cars and Riders, allowing objects to be located quickly using their unique IDs.

# Testing

The project is tested using:

test_simulation.py

The test program performs the following actions:

Creates a Simulation object
Loads the city map from the CSV file
Creates one Car object
Creates one Rider object
Stores both objects in the Simulation dictionaries
Prints the Car, Rider, Simulation, and Graph objects

Example output:

Creating simulation and loading map...

Map loaded successfully.

Car CAR001 at (10, 5) - Status: available

Rider RIDER_A at (1, 2) waiting for ride to (20, 15)

Simulation loaded successfully.
Cars: 1
Riders: 1
Map nodes: 4

Adjacency List
A -> [('B', 5), ('C', 3)]
B -> [('A', 5), ('D', 4)]
C -> [('A', 3), ('D', 1)]
D -> [('B', 4), ('C', 1)]
# Future Enhancements

The Graph class establishes the foundation for future milestones, which may include:

Implementing Dijkstra's Shortest Path Algorithm
Finding the nearest available driver
Calculating optimal routes between riders and destinations
Simulating vehicle movement through the road network
Measuring algorithm performance and efficiency using Big-O analysis

I would also recommend updating the Project Structure section of your README to reflect the new files:

ride_sharing_simulator/
│
├── car.py              # Car class
├── rider.py            # Rider class
├── graph.py            # City map stored as an adjacency list
├── simulation.py       # Main simulation controller
├── test_simulation.py  # Test program
├── city_map.csv        # Sample road network
├── README.md           # Project documentation
└── .gitignore

This gives your README a polished, professional feel and clearly documents the additions made in this milestone.