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
