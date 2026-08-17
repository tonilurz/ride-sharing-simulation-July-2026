#This is the test simulation of the ride-sharing project
from car import Car
from rider import Rider
from simulation import Simulation

def main():
    """
    Tests the event-driven ride-sharing simulation
    """

    print("Creating simulation and loading map...\n")

    #Create the simulation object
    #The Simulation automatically creates and loads its Graph
    simulation = Simulation("map.csv") 

     #Create one Car
    car_one = Car("CAR001", (0,0))
    car_two = Car("CAR002", (80, 80))

    simulation.cars[car_one.id] = car_one
    simulation.cars[car_two.id] = car_two

    #______________________________
    # Create Riders
    #______________________________

    #Create one rider
    rider_one = Rider("RIDER_A", (10,5),(40,30))
    rider_two = Rider("RIDER_B", (75,70), (20, 60))

    #Add riders to the simulation dictionary
    simulation.riders[rider_one.id] = rider_one
    simulation.riders[rider_two.id] = rider_two 


    #________________________________________________-
    # Schedule Rider Request Events
    #________________________________________________

    simulation.schedule_event(
        10,"RIDER_REQUEST", rider_one
    )
    simulation.schedule_event(
        20, "RIDER_REQUEST", rider_two
    )

    #Temporary debugging line
    print("Events waiting before run:")
    print(simulation.events)
    print()
    #_________________________________________________
    # Run the Simulation
    #________________________________________________

    simulation.run()
   #_________________________________________________
   # Print Final States
   #_________________________________________________
    print()
    print("FINAL SIMULATION STATE")
    print("----------------------------")

    print(
        f"{car_one.id}:"
        f"Location = {car_one.location},"
        f"Status = {car_one.status}"
    )
    print(
            f"{car_two.id}:"
            f"Location = {car_two.location},"
            f"Status = {car_two.status}"
        )
    print()

    print(
        f"{rider_one.id}:"
        f"Status = {rider_one.status}"
    )

    print(
        f"{rider_two.id}:"
        f"Status = {rider_two.status}"
    )

if __name__ == "__main__":
    main()                                                                                                                                                                                                                                                                                                                      
  
