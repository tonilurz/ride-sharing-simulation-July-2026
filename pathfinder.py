import heapq


def find_the_shortest_path(graph, start_node, end_node):
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

    # Starting node has a distance of zero
    distances[start_node] = 0

    # Store how we reached each node
    predecessors = {
        node: None
        for node in graph.adjacency_list
    }

    # Priority queue format:
    # (distance, node)
    priority_queue = [(0, start_node)]

    while priority_queue:

        current_distance, current_node = heapq.heappop(
            priority_queue
        )

        # Ignore an outdated heap entry
        if current_distance > distances[current_node]:
            continue

        # Stop once destination is reached
        if current_node == end_node:
            break

        # Check each neighbor
        for neighbor, weight in graph.adjacency_list[current_node]:

            new_distance = current_distance + weight

            # Found a shorter route
            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    # IMPORTANT:
    # This is OUTSIDE the while loop
    if distances[end_node] == float("inf"):
        return None, float("inf")

    # Reconstruct the path
    path = []

    current = end_node

    while current is not None:
        path.append(current)
        current = predecessors[current]

    # Path was built backwards
    path.reverse()

    return path, distances[end_node]