#_____________Quadtree __________________________________________
class Point:
    """Represents a location on a 2D city map"""
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
        self.data = data # e.g., driver ID, car object, etc.

    def __repr__(self):
        """
        Returns a readable respresentation of the point.
        """
        return f"Point({self.x:.2f}, {self.y:.2f})"

class Rectangle:
    """Represents a rectangular boundary on the map."""
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
      
        """Check if a point is inside this rectangle."""
        return (self.x <= point.x < self.x + self.width and
                self.y <= point.y < self.y + self.height)

    def distance_sq_to_point(self,point):
        """Calcuates the squared shortest distance from a point to this rectangle."""
        dx = max(0, self.x - point.x, point.x - (self.x + self.width))
        dy = max(0, self.y - point.y, point.y -(self.y + self.height))
        return dx*dx + dy*dy

class QuadtreeNode:
    """Represents one rectangular region in the quadtree."""
    def __init__(self, boundary, capacity=4):
        """
        Creates on Quadtree node.
        """
        self.boundary = boundary
        self.capacity = capacity  # Max points a node can hold before subdividing
        self.points = []
        self.divided = False

        #Child nodes begin as None
        self.northeast = None
        self.northwest = None  
        self.southeast = None
        self.southwest = None

    def subdivide(self):
        """
        Divides the node into four child quadrants.
        """

        x = self.boundary.x
        y = self.boundary.y
        half_width = self.boundary.width / 2
        half_height = self.boundary.height / 2

        # Northwest
        nw_boundary = Rectangle(
            x,
            y,
            half_width,
            half_height
        )

        # Northeast
        ne_boundary = Rectangle(
            x + half_width,
            y,
            half_width,
            half_height
        )

        # Southwest
        sw_boundary = Rectangle(
            x,
            y + half_height,
            half_width,
            half_height
        )

        # Southeast
        se_boundary = Rectangle(
            x + half_width,
            y + half_height,
            half_width,
            half_height
        )

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

        self.divided = True
       


    def insert_into_children(self, point):
        """
        Attempts to insert a point into one of the four child nodes.
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

     

    def insert(self, point):
        """
        Recursively inserts a point into the Quadtree.
        """

        # Ignore points outside this node
        if not self.boundary.contains(point):
            return False

        # Store the point here if there is room
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True

        # If full and not yet divided, divide now
        if not self.divided:
            self.subdivide()

            old_points = self.points
            self.points = []

            for existing_point in old_points:
                self.insert_into_children(existing_point)

        # Insert the new point into the correct child
        return self.insert_into_children(point)
    
    def find_nearest_recursive(self, query_point, best_found):
        """
        Recursibely searches for the nearest point
        """
        #______________________
        #Pruning
        #______________________

        boundary_distance =(
            self.boundary.distance_sq_to_point(query_point)
        )

        if boundary_distance > best_found["dist_sq"]:
            return
        
        #__________________________
        #Checks Points in this Node
        #__________________________
    
        for point in self.points:
            dx = point.x - query_point.x
            dy = point.y - query_point.y

            distance_sq = dx * dx + dy * dy

            if distance_sq < best_found["dist_sq"]:

                best_found["dist_sq"]= distance_sq
                best_found["point"] = point

        #_______________________________________________
        # Search Children
        #_______________________________________________

        if self.divided:

            children =[
                self.northwest,
                self.northeast,
                self.southwest,
                self.southeast
            ]

            #Search closest quadrant first
            children.sort(
                key =lambda child:
                child.boundary.distance_sq_to_point(
                    query_point
                )
            )

            for child in children:
                child.find_nearest_recursive(
                    query_point,
                    best_found
                )

    def __str__(self, level=0):
        """
        Returns a readable representation of this node
        and its children.
        """

        ret = (
            "\t" * level
            + f"Level {level}, Boundary: "
            + f"{self.boundary.x, self.boundary.y, self.boundary.width, self.boundary.height}\n"
        )

        ret += "\t" * level + f"Points: {self.points}\n"

        if self.divided:
            ret += self.northwest.__str__(level + 1)
            ret += self.northeast.__str__(level + 1)
            ret += self.southwest.__str__(level + 1)
            ret += self.southeast.__str__(level + 1)

        return ret

class Quadtree:
    """
    Main Quadtree class used by the application
    """

    def __init__(self, boundary, capacity=4):
        """
        Creates the Quadtree and its root node.
        """
        self.boundary = boundary

        self.root = QuadtreeNode(
            boundary,
            capacity
        )

    def insert(self, point):
        """
        Inserts a point into the tree.
        """

        return self.root.insert(point)

    def find_nearest(self, query_point):
        """
        Finds the closest stored point.
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

    def __str__(self):
        return self.root.__str__()
    