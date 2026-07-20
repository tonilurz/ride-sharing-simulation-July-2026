#This is the test simulation of the ride-sharing project
from car import Car
from rider import Rider
from simulation import Simulation

def main():
    """
    Tests the Car, Rider, and Simulation classes.
    """

    print("Creating simulation and loading map...\n")

    #Create the simulation object
    #The Simulation automatically creates and loads its Graph
    simulation = Simulation("map.csv")

     #Create one Car
    car_one = Car("CAR001", (10,5))

    #Create one rider
    rider_one = Rider("RIDER_A", (1,2),(20,15))



    #Store the objects in the Simulation dictionaries
    simulation.cars[car_one.id] = car_one
    simulation.riders[rider_one.id] = rider_one
   


    #Print each object
    print(car_one)
    print(rider_one)
    print(simulation)

    # Print the dictionaries to prove the objects are stored
    print("\nCars dictionary:")
    for car_id, car in simulation.cars.items():
        print(car_id, ":", car)

    print("\nRiders dictionary:")
    for rider_id, rider in simulation.riders.items():
        print(rider_id, ":", rider)

        print("\nLoaded City Map")
        print(simulation.map)

if __name__ == "__main__":
    main()                                                                                                                                                                                                                                                                                                                      
  
