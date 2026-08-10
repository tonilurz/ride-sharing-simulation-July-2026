from graph import Graph
from car import Car
from pathfinder import find_the_shortest_path

def main():
    """
    Test Dijkstra's algorithm implementation with a sample graph.
    """
    #Create the graph
    city_graph = Graph()

    #Load the graph from a CSV file
    city_graph.load_from_file("map.csv")

    car = Car("CAR001", ("A"))  # Example car starting at node "A"

    car.calculate_route(("D"), city_graph)  # Example destination node "D"

    

    #Choose a starting node and destination node for the test
    city_graph.load_from_file("map.csv")
    start_node = ("A")  # Example starting node
    end_node = ("D")    # Example destination node

    print("Adjacency List:")
    print(city_graph)

    #Find the shortest path using Dijkstra's algorithm
    path, travel_time = find_the_shortest_path(city_graph, start_node, end_node)

    #Display the results
    print("Car ID:", car.id)
    print("Current Location:", car.location)
    print("Destination:", car.destination)
    print("Route:", car.route)
    print("Travel Time:", car.route_time)
    print("\nDIJKSTRA TEST")
    print("------------------------")
    print(f"Start Node: {start_node}")
    print(f"Destination: {end_node}")
    print(f"Shortest Path: {path}")
    print(f"Total Travel Time: {travel_time}")


if __name__ == "__main__":
    main()