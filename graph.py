import collections


class Graph:
    """
    Represents the city road network.

    The graph stores:
    1. Road connections using an adjacency list.
    2. Physical (x, y) coordinates for each graph node.
    """

    def __init__(self):
        """
        Creates an empty graph.
        """

        # Graph connections
        #
        # Example:
        # {
        #     "A": [("B", 5.0), ("C", 3.0)],
        #     "B": [("A", 5.0)]
        # }
        self.adjacency_list = collections.defaultdict(list)

        # Physical coordinates of each graph node
        #
        # Example:
        # {
        #     "A": (0.0, 0.0),
        #     "B": (25.0, 10.0)
        # }
        self.node_coordinates = {}


    def load_map_data(self, filename):
        """
        Loads graph edges and node coordinates
        from the unified city map.

        Expected CSV format:

        start_node_id,start_x,start_y,end_id,end_x,end_y,weight
        """

        with open(filename, "r") as file:

            for line in file:

                # Remove whitespace and newline
                line = line.strip()

                # Skip blank lines
                if not line:
                    continue

                # Skip comment lines
                if line.startswith("#"):
                    continue

                # Split the CSV row
                parts = line.split(",")

                # Skip the CSV header
                if parts[0].strip().lower() == "start_node_id":
                    continue

                # Each valid row must contain 7 values
                if len(parts) != 7:
                    print(
                        f"Invalid map row skipped: {parts}"
                    )
                    continue

                (
                    start_id,
                    start_x,
                    start_y,
                    end_id,
                    end_x,
                    end_y,
                    weight
                ) = parts


                # Clean IDs
                start_id = start_id.strip()
                end_id = end_id.strip()


                # Convert coordinate and weight values
                try:

                    start_x = float(start_x.strip())
                    start_y = float(start_y.strip())

                    end_x = float(end_x.strip())
                    end_y = float(end_y.strip())

                    weight = float(weight.strip())

                except ValueError:

                    print(
                        f"Invalid numeric value skipped: {parts}"
                    )

                    continue


                # Save node coordinates
                self.node_coordinates[start_id] = (
                    start_x,
                    start_y
                )

                self.node_coordinates[end_id] = (
                    end_x,
                    end_y
                )


                # Add directed road
                self.adjacency_list[start_id].append(
                    (end_id, weight)
                )


                # Make sure the destination node exists
                # even if it has no outgoing road yet
                if end_id not in self.adjacency_list:
                    self.adjacency_list[end_id] = []


        print("Unified city map loaded successfully.")


    def __str__(self):
        """
        Returns a readable representation
        of the city graph.
        """

        output = "Adjacency List\n"

        for node, neighbors in self.adjacency_list.items():

            coordinates = self.node_coordinates.get(
                node,
                None
            )

            output += (
                f"{node} {coordinates}"
                f" -> {neighbors}\n"
            )

        return output