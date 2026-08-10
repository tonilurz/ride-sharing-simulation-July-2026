from graph import Graph
from pathfinder import find_the_shortest_path

def main():
    """
    Test Dijkstra's algorithm implementation with a sample graph.
    """
    #Create the graph
    city_graph = Graph()

    #Load the graph from a CSV file
    city_graph.load_from_file("map.csv")

    #Choose a starting node and destination node for the test
    city_graph.load_from_file("map.csv")
    start_node = ("A")  # Example starting node
    end_node = ("D")    # Example destination node

    print("Adjacency List:")
    print(city_graph)

    #Find the shortest path using Dijkstra's algorithm
    path, travel_time = find_the_shortest_path(city_graph, start_node, end_node)

    #Display the results
    print("\nDIJKSTRA TEST")
    print("------------------------")
    print(f"Start Node: {start_node}")
    print(f"Destination: {end_node}")
    print(f"Shortest Path: {path}")
    print(f"Total Travel Time: {travel_time}")


if __name__ == "__main__":
    main()