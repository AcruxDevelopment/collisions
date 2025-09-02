from typing import Tuple, List
from vector import *
from triangle_shape import *



# -----------------------------
# COLLISION HELPERS
# -----------------------------
def overlap(interval1: Tuple[float, float], interval2: Tuple[float, float]) -> bool:
    return not (interval1[1] < interval2[0] or interval2[1] < interval1[0])


def triangles_collide(t1: TriangleShape, t2: TriangleShape) -> bool:
    """Check if two triangles overlap using the Separating Axis Theorem."""
    edges = t1.edges() + t2.edges()

    for edge in edges:
        axis = edge.perpendicular()
        proj1 = t1.project(axis)
        proj2 = t2.project(axis)

        if not overlap(proj1, proj2):
            return False
    return True