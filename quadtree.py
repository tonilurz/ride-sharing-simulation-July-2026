# _______________________________________________________________
# QUADTREE
# Ride-Sharing Simulator
# _______________________________________________________________

import heapq
from itertools import count


# _______________________________________________________________
# POINT CLASS
# _______________________________________________________________

class Point:
    """
    Represents a location on a 2D city map.
    """

    def __init__(self, x, y, data=None):
        """
        Creates a point with x and y coordinates.

        Args:
            x (float): Horizontal coordinate.
            y (float): Vertical coordinate.
            data: Optional information associated with the point,
                  such as a driver ID or Car object.
        """

        self.x = x
        self.y = y
        self.data = data

    def __repr__(self):
        """
        Returns a readable representation of the point.
        """

        return f"Point({self.x:.2f}, {self.y:.2f})"


# _______________________________________________________________
# RECTANGLE CLASS
# _______________________________________________________________

class Rectangle:
    """
    Represents a rectangular boundary on the map.
    """

    def __init__(self, x, y, width, height):
        """
        Creates a rectangular boundary.

        Args:
            x (float): Left edge of the rectangle.
            y (float): Top edge of the rectangle.
            width (float): Width of the rectangle.
            height (float): Height of the rectangle.
        """

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point):
        """
        Checks if a point is inside this rectangle.
        """

        return (
            self.x <= point.x < self.x + self.width
            and
            self.y <= point.y < self.y + self.height
        )

    def distance_sq_to_point(self, point):
        """
        Calculates the squared shortest distance
        from a point to this rectangle.
        """

        dx = max(
            0,
            self.x - point.x,
            point.x - (self.x + self.width)
        )

        dy = max(
            0,
            self.y - point.y,
            point.y - (self.y + self.height)
        )

        return dx * dx + dy * dy


# _______________________________________________________________
# QUADTREE NODE CLASS
# _______________________________________________________________

class QuadtreeNode:
    """
    Represents one rectangular region in the Quadtree.
    """

    def __init__(self, boundary, capacity=4):
        """
        Creates one Quadtree node.

        Args:
            boundary (Rectangle):
                The rectangular area covered by this node.

            capacity (int):
                Maximum number of points this node can hold
                before subdividing.
        """

        self.boundary = boundary
        self.capacity = capacity

        # Points stored in this node
        self.points = []

        # Tracks whether this node has been divided
        self.divided = False

        # Child nodes begin as None
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None


    # ___________________________________________________________
    # SUBDIVIDE
    # ___________________________________________________________

    def subdivide(self):
        """
        Divides the node into four child quadrants.
        """

        x = self.boundary.x
        y = self.boundary.y

        half_width = self.boundary.width / 2
        half_height = self.boundary.height / 2


        # Northwest quadrant
        nw_boundary = Rectangle(
            x,
            y,
            half_width,
            half_height
        )


        # Northeast quadrant
        ne_boundary = Rectangle(
            x + half_width,
            y,
            half_width,
            half_height
        )


        # Southwest quadrant
        sw_boundary = Rectangle(
            x,
            y + half_height,
            half_width,
            half_height
        )


        # Southeast quadrant
        se_boundary = Rectangle(
            x + half_width,
            y + half_height,
            half_width,
            half_height
        )


        # Create the four child nodes
        self.northwest = QuadtreeNode(
            nw_boundary,
            self.capacity
        )

        self.northeast = QuadtreeNode(
            ne_boundary,
            self.capacity
        )

        self.southwest = QuadtreeNode(
            sw_boundary,
            self.capacity
        )

        self.southeast = QuadtreeNode(
            se_boundary,
            self.capacity
        )


        # Mark this node as divided
        self.divided = True


    # ___________________________________________________________
    # INSERT INTO CHILDREN
    # ___________________________________________________________

    def insert_into_children(self, point):
        """
        Attempts to insert a point into one
        of the four child nodes.
        """

        if self.northwest.insert(point):
            return True

        if self.northeast.insert(point):
            return True

        if self.southwest.insert(point):
            return True

        if self.southeast.insert(point):
            return True

        return False


    # ___________________________________________________________
    # INSERT
    # ___________________________________________________________

    def insert(self, point):
        """
        Recursively inserts a point into the Quadtree.
        """

        # STEP 1
        # Ignore points outside this node's boundary
        if not self.boundary.contains(point):
            return False


        # STEP 2
        # If there is room and this node has not divided,
        # store the point here.
        if (
            len(self.points) < self.capacity
            and
            not self.divided
        ):

            self.points.append(point)

            return True


        # STEP 3
        # If the node is full, subdivide it.
        if not self.divided:

            self.subdivide()

            # Save the existing points
            old_points = self.points

            # Clear this parent node
            self.points = []

            # Move existing points into the children
            for existing_point in old_points:

                inserted = self.insert_into_children(
                    existing_point
                )

                if not inserted:
                    raise RuntimeError(
                        "Existing point could not be "
                        "reinserted after subdivision."
                    )


        # STEP 4
        # Insert the new point into the correct child
        return self.insert_into_children(point)


    # ___________________________________________________________
    # FIND ONE NEAREST POINT
    # Original Milestone Quadtree Search
    # ___________________________________________________________

    def find_nearest_recursive(
        self,
        query_point,
        best_found
    ):
        """
        Recursively searches for the single
        nearest Point to the query point.
        """

        # Calculate the shortest possible distance
        # between the query point and this boundary.
        boundary_distance_sq = (
            self.boundary.distance_sq_to_point(
                query_point
            )
        )


        # PRUNING
        # If this entire region is farther away
        # than our current best point, skip it.
        if (
            boundary_distance_sq
            >
            best_found["dist_sq"]
        ):

            return


        # Check points stored in this node
        for point in self.points:

            dx = point.x - query_point.x
            dy = point.y - query_point.y

            distance_sq = (
                dx * dx
                +
                dy * dy
            )


            # Found a closer point
            if (
                distance_sq
                <
                best_found["dist_sq"]
            ):

                best_found["dist_sq"] = distance_sq
                best_found["point"] = point


        # Search children if this node is divided
        if self.divided:

            children = [
                self.northwest,
                self.northeast,
                self.southwest,
                self.southeast
            ]


            # Search the closest quadrant first
            children.sort(
                key=lambda child:
                child.boundary.distance_sq_to_point(
                    query_point
                )
            )


            for child in children:

                child.find_nearest_recursive(
                    query_point,
                    best_found
                )


    # ___________________________________________________________
    # FIND K NEAREST POINTS
    # Final Project Addition
    # ___________________________________________________________

    def find_k_nearest_recursive(
        self,
        query_point,
        k,
        candidate_heap,
        tie_counter
    ):
        """
        Recursively searches for up to k nearest points.

        A heap stores the best candidates found so far.

        The Quadtree can prune branches that cannot
        contain a closer candidate.
        """


        # -------------------------------------------------------
        # PRUNING
        # -------------------------------------------------------

        # Once we already have k candidates,
        # determine the farthest candidate currently stored.
        if len(candidate_heap) == k:

            farthest_distance_sq = (
                -candidate_heap[0][0]
            )

            boundary_distance_sq = (
                self.boundary.distance_sq_to_point(
                    query_point
                )
            )


            # If this entire region is farther away
            # than our current farthest candidate,
            # there is no reason to search this branch.
            if (
                boundary_distance_sq
                >
                farthest_distance_sq
            ):

                return


        # -------------------------------------------------------
        # CHECK POINTS IN THIS NODE
        # -------------------------------------------------------

        for point in self.points:

            dx = point.x - query_point.x
            dy = point.y - query_point.y

            distance_sq = (
                dx * dx
                +
                dy * dy
            )


            # Negative distance lets Python's min-heap
            # act like a max-heap for our candidates.
            #
            # The sequence number prevents Python from
            # comparing Point objects when distances tie.
            entry = (
                -distance_sq,
                next(tie_counter),
                point
            )


            # We do not have k candidates yet
            if len(candidate_heap) < k:

                heapq.heappush(
                    candidate_heap,
                    entry
                )


            # We already have k candidates
            else:

                farthest_distance_sq = (
                    -candidate_heap[0][0]
                )


                # Replace the farthest candidate
                # if this point is closer.
                if (
                    distance_sq
                    <
                    farthest_distance_sq
                ):

                    heapq.heapreplace(
                        candidate_heap,
                        entry
                    )


        # -------------------------------------------------------
        # SEARCH CHILDREN
        # -------------------------------------------------------

        if self.divided:

            children = [
                self.northwest,
                self.northeast,
                self.southwest,
                self.southeast
            ]


            # Search closest quadrant first.
            # This helps us find good candidates sooner,
            # which improves pruning.
            children.sort(
                key=lambda child:
                child.boundary.distance_sq_to_point(
                    query_point
                )
            )


            for child in children:

                child.find_k_nearest_recursive(
                    query_point,
                    k,
                    candidate_heap,
                    tie_counter
                )


    # ___________________________________________________________
    # REMOVE POINT
    # Final Project Addition
    # ___________________________________________________________

    def remove(self, point):
        """
        Removes the exact Point object from the Quadtree.

        Uses object identity so different cars at the
        same coordinates can still be removed separately.
        """

        if not self.boundary.contains(point):
            return False

        # Check points stored directly in this node
        for index, stored_point in enumerate(self.points):

            if stored_point is point:

                del self.points[index]

                return True

        # Search child nodes
        if self.divided:

            children = [
                self.northwest,
                self.northeast,
                self.southwest,
                self.southeast
            ]

            for child in children:

                # Let each child decide whether the point
                # belongs inside its boundary.
                if child.remove(point):
                    return True

        return False


    # ___________________________________________________________
    # STRING REPRESENTATION
    # ___________________________________________________________

    def __str__(self, level=0):
        """
        Returns a readable representation of this node
        and all of its children.
        """

        boundary = (
            self.boundary.x,
            self.boundary.y,
            self.boundary.width,
            self.boundary.height
        )

        ret = (
            "\t" * level
            + f"Level {level}, Boundary: {boundary}\n"
        )

        ret += (
            "\t" * level
            + f"Points: {self.points}\n"
        )

        if self.divided:
            ret += self.northwest.__str__(level + 1)
            ret += self.northeast.__str__(level + 1)
            ret += self.southwest.__str__(level + 1)
            ret += self.southeast.__str__(level + 1)

        return ret


# _______________________________________________________________
# MAIN QUADTREE CLASS
# _______________________________________________________________

class Quadtree:
    """
    Main Quadtree class used by the ride-sharing simulation.

    The Quadtree provides the public methods used by
    the rest of the program.
    """

    def __init__(self, boundary, capacity=4):
        """
        Creates the Quadtree and its root node.

        Args:
            boundary (Rectangle):
                Boundary of the entire map.

            capacity (int):
                Maximum points per node before subdivision.
        """

        self.boundary = boundary

        self.root = QuadtreeNode(
            boundary,
            capacity
        )


    # ___________________________________________________________
    # PUBLIC INSERT METHOD
    # ___________________________________________________________

    def insert(self, point):
        """
        Inserts a Point into the Quadtree.
        """

        return self.root.insert(point)

    def get_all_points(self):
        """
        Returns every Point object currently stored
        in the Quadtree.
        """

        points = []

        def collect(node):

            points.extend(node.points)

            if node.divided:
                collect(node.northwest)
                collect(node.northeast)
                collect(node.southwest)
                collect(node.southeast)

        collect(self.root)

        return points


    # ___________________________________________________________
    # PUBLIC FIND NEAREST METHOD
    # ___________________________________________________________

    def find_nearest(self, query_point):
        """
        Finds and returns the single nearest Point.

        Returns:
            Point object or None if the tree is empty.
        """

        best_found = {
            "point": None,
            "dist_sq": float("inf")
        }


        self.root.find_nearest_recursive(
            query_point,
            best_found
        )


        return best_found["point"]


    # ___________________________________________________________
    # PUBLIC FIND K NEAREST METHOD
    # ___________________________________________________________

    def find_k_nearest(
        self,
        query_point,
        k=5
    ):
        """
        Returns up to k nearest Point objects.

        The default value of k is 5 for the
        ride-sharing candidate search.

        Args:
            query_point (Point):
                Location to search around.

            k (int):
                Maximum number of nearest points
                to return.

        Returns:
            List of Point objects ordered from
            nearest to farthest.
        """


        # k must be positive
        if k <= 0:

            raise ValueError(
                "k must be greater than zero."
            )


        # Heap containing our best candidates
        candidate_heap = []


        # Used to break ties when two points
        # have exactly the same distance.
        tie_counter = count()


        # Perform recursive search
        self.root.find_k_nearest_recursive(
            query_point,
            k,
            candidate_heap,
            tie_counter
        )


        # -------------------------------------------------------
        # CONVERT RESULTS
        # -------------------------------------------------------

        results = []


        for (
            negative_distance,
            sequence,
            point
        ) in candidate_heap:

            results.append(
                (
                    -negative_distance,
                    sequence,
                    point
                )
            )


        # Sort from nearest to farthest
        results.sort(
            key=lambda item: (
                item[0],
                item[1]
            )
        )


        # Return only the Point objects
        return [
            item[2]
            for item in results
        ]


    # ___________________________________________________________
    # PUBLIC REMOVE METHOD
    # ___________________________________________________________

    def remove(self, point):
        """
        Removes the exact Point object
        from the Quadtree.

        Returns:
            True if removed.
            False if not found.
        """

        return self.root.remove(point)


    # ___________________________________________________________
    # STRING REPRESENTATION
    # ___________________________________________________________

    def __str__(self):
        """
        Returns a readable representation
        of the entire Quadtree.
        """

        return self.root.__str__()