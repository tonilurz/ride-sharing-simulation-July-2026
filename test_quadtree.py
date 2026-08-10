import random
import time
import math

from quadtree import Point, Rectangle, Quadtree


def find_closest_brute_force(query_point, all_points):
    """
    Finds the nearest point by checking every point.
    This is the simple O(N) comparison search.
    """

    best_point = None
    min_dist_sq = float("inf")

    for point in all_points:

        # Calculate the x and y distance
        dx = point.x - query_point.x
        dy = point.y - query_point.y

        # Calculate squared distance
        distance_sq = dx * dx + dy * dy

        # If this point is closer, save it
        if distance_sq < min_dist_sq:
            min_dist_sq = distance_sq
            best_point = point

    return best_point, min_dist_sq


def main():
    """
    Tests the Quadtree nearest-neighbor search
    against a brute-force search.
    """

    # Use the same random numbers each time
    # This makes the test repeatable
    random.seed(42)

    # -----------------------------------------
    # STEP 1: CREATE THE MAP BOUNDARY
    # -----------------------------------------

    map_boundary = Rectangle(
        0,
        0,
        1000,
        1000
    )

    # -----------------------------------------
    # STEP 2: CREATE THE QUADTREE
    # -----------------------------------------

    quadtree = Quadtree(
        map_boundary,
        capacity=4
    )

    # -----------------------------------------
    # STEP 3: CREATE 5,000 RANDOM DRIVER POINTS
    # -----------------------------------------

    number_of_points = 5000
    points = []

    for i in range(number_of_points):

        point = Point(
            random.uniform(0, 1000),
            random.uniform(0, 1000),
            f"Driver-{i}"
        )

        # Save point for brute-force testing
        points.append(point)

        # Insert point into Quadtree
        quadtree.insert(point)

    # -----------------------------------------
    # STEP 4: CREATE A RANDOM RIDER LOCATION
    # -----------------------------------------

    query_point = Point(
        random.uniform(0, 1000),
        random.uniform(0, 1000),
        "Rider"
    )

    print("QUADTREE NEAREST-NEIGHBOR TEST")
    print("-----------------------------------")
    print(f"Number of Driver Points: {number_of_points}")
    print(f"Rider Location: {query_point}")
    print()

    # -----------------------------------------
    # STEP 5: QUADTREE SEARCH
    # -----------------------------------------

    start_time_qt = time.perf_counter()

    quadtree_result = quadtree.find_nearest(
        query_point
    )

    end_time_qt = time.perf_counter()

    quadtree_time = (
        end_time_qt - start_time_qt
    ) * 1000

    # Make sure the Quadtree found something
    if quadtree_result is None:
        print("ERROR: Quadtree did not find a nearest point.")
        return

    # Calculate actual distance for display
    qt_dx = quadtree_result.x - query_point.x
    qt_dy = quadtree_result.y - query_point.y

    quadtree_distance = math.sqrt(
        qt_dx * qt_dx + qt_dy * qt_dy
    )

    # -----------------------------------------
    # STEP 6: BRUTE-FORCE SEARCH
    # -----------------------------------------

    start_time_bf = time.perf_counter()

    brute_result, brute_distance_sq = (
        find_closest_brute_force(
            query_point,
            points
        )
    )

    end_time_bf = time.perf_counter()

    brute_force_time = (
        end_time_bf - start_time_bf
    ) * 1000

    brute_force_distance = math.sqrt(
        brute_distance_sq
    )

    # -----------------------------------------
    # STEP 7: DISPLAY RESULTS
    # -----------------------------------------

    print("QUADTREE RESULT")
    print("-----------------------------------")
    print(f"Nearest Point: {quadtree_result}")
    print(f"Driver: {quadtree_result.data}")
    print(f"Distance: {quadtree_distance:.4f}")
    print(f"Search Time: {quadtree_time:.6f} ms")

    print()

    print("BRUTE-FORCE RESULT")
    print("-----------------------------------")
    print(f"Nearest Point: {brute_result}")
    print(f"Driver: {brute_result.data}")
    print(f"Distance: {brute_force_distance:.4f}")
    print(f"Search Time: {brute_force_time:.6f} ms")

    print()

    # -----------------------------------------
    # STEP 8: VERIFY THE RESULTS MATCH
    # -----------------------------------------

    assert quadtree_result is brute_result

    print("TEST PASSED")
    print(
        "The Quadtree and brute-force search "
        "found the same nearest driver."
    )

    # -----------------------------------------
    # STEP 9: PERFORMANCE COMPARISON
    # -----------------------------------------

    if quadtree_time > 0:

        speed_difference = (
            brute_force_time / quadtree_time
        )

        print(
            f"The Quadtree search was approximately "
            f"{speed_difference:.2f}x the speed "
            f"of the brute-force search."
        )


if __name__ == "__main__":
    main()