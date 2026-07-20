import csv

class Graph:
    """
    Represents the city map using an adjacency list.
    """

    def __init__(self):
        """
        Initializes the graph with an empty adjacency list.
        The adjacency list is a dictionary where keys are vertex IDs
        and values are lists of (neighbor, weight) tuples.
        """
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        """ Adds a vertex to the graph if it;s not already there
        """
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] =[]
            print(f"Vertex '[vertex]' added.")

    def add_edge(self, start_node, end_node, weight):
        """
        Adds a directed edge to the graph
        """
        self.add_vertex(start_node)
        self.add_vertex(end_node)
        self.adjacency_list[start_node].append((end_node, float(weight)))

    #Load from a csv file 
    def load_from_file(self, filename):
        with open(filename, newline="") as file:
            reader = csv.reader(file)
            next (reader)
            for row in reader:
                if len(row) != 3: #Ensures row has 3 elements
                    print(f"Invalid row skipped: {row}")
                    continue

                start, end, weight = row

                try:
                    self.add_edge(
                        start.strip(), 
                        end.strip(), 
                        int(weight.strip())
                    )
                except ValueError:
                    print(f"Invalid weight skipped; {row}")      
        print("Map loaded successfully")

    def __str__(self):
        output = "Adjacency List\n"
        for node, neighbors in self.adjacency_list.items():
            output += f"{node} -> {neighbors}\n"
        return output
