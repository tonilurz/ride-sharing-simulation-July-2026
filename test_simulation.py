#This is the test simulation of the ride-sharing project
from car import Car
from rider import Rider
from simulation import Simulation

def main():
    """
    Creates and tests the main rider-sharing objects.
    """

    #Create one Car
    car_one = Car("CAR001", (10,5))

    #Create one rider
    rider_one = Rider("RIDER_A", (1,2),(20,15))

    #Create the simulation
    simulation = Simulation()

    #Add the car to the simulation's car dictionary
    simulation.cars[car_one.id] = car_one

    #Add the rider to the simulation's riders dictionary
    simulation.riders[rider_one.id] = rider_one

    #Print each object
    print(car_one)
    print(rider_one)
    print(simulation)

if __name__ == "__main__":
    main()
  
