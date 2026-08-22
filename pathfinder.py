import heapq


def find_nearest_vertex(point, node_coordinates):
    """
    Finds the graph vertex physically closest
    to an (x, y) coordinate.

    Args:
        point (tuple): Physical (x, y) coordinates.
        node_coordinates (dict):
            Dictionary mapping graph-node IDs
            to physical coordinates.

    Returns:
        The ID of the closest graph vertex.
    """

    if not node_coordinates:
        raise ValueError(
            "No graph vertices have been loaded."
        )

    point_x, point_y = point

    nearest_node = None
    minimum_distance_sq = float("inf")

    for node_id, coordinates in node_coordinates.items():

        node_x, node_y = coordinates

        distance_sq = (
            (node_x - point_x) ** 2
            +
            (node_y - point_y) ** 2
        )

        if distance_sq < minimum_distance_sq:

            minimum_distance_sq = distance_sq
            nearest_node = node_id

    return nearest_node


def find_the_shortest_path(
    graph,
    start_node,
    end_node
):
    """
    Finds the shortest path between two nodes
    using Dijkstra's algorithm.

    Returns:
        (path, total_travel_time)

    If no path exists:
        (None, float("inf"))
    """

    # Make sure both nodes exist
    if start_node not in graph.adjacency_list:
        return None, float("inf")

    if end_node not in graph.adjacency_list:
        return None, float("inf")

    # Set all distances to infinity
    distances = {
        node: float("inf")
        for node in graph.adjacency_list
    }

    # Starting node has distance zero
    distances[start_node] = 0

    # Stores the previous node
    # used to reach each graph node
    predecessors = {
        node: None
        for node in graph.adjacency_list
    }

    # Priority queue format:
    # (distance, node)
    priority_queue = [
        (0, start_node)
    ]

    while priority_queue:

        current_distance, current_node = (
            heapq.heappop(
                priority_queue
            )
        )

        # Ignore outdated heap entries
        if (
            current_distance
            >
            distances[current_node]
        ):
            continue

        # Stop once destination is reached
        if current_node == end_node:
            break

        # Examine neighboring nodes
        for neighbor, weight in (
            graph.adjacency_list[
                current_node
            ]
        ):

            new_distance = (
                current_distance
                +
                weight
            )

            # Found a shorter route
            if (
                new_distance
                <
                distances[neighbor]
            ):

                distances[neighbor] = (
                    new_distance
                )

                predecessors[neighbor] = (
                    current_node
                )

                heapq.heappush(
                    priority_queue,
                    (
                        new_distance,
                        neighbor
                    )
                )

    # Destination cannot be reached
    if (
        distances[end_node]
        ==
        float("inf")
    ):
        return None, float("inf")

    # Reconstruct the path
    path = []

    current = end_node

    while current is not None:

        path.append(
            current
        )

        current = (
            predecessors[current]
        )

    # Path was constructed backwards
    path.reverse()

    return (
        path,
        distances[end_node]
    )