from triangle_shape import TriangleShape
from vector import Vector2
import math
from typing import List

def circle(triangleCount: int, radius: float) -> List[TriangleShape]:
    """
    Generate `triangleCount` triangles forming a full circle of given radius.
    Each triangle is a sector of the circle.
    """
    triangles: List[TriangleShape] = []
    angle_step = 360 / triangleCount
    center = Vector2(0, 0)

    for i in range(triangleCount):
        angle1 = math.radians(i * angle_step)
        angle2 = math.radians((i + 1) * angle_step)

        # Two points on the circle edge
        p1 = Vector2(math.cos(angle1) * radius, math.sin(angle1) * radius)
        p2 = Vector2(math.cos(angle2) * radius, math.sin(angle2) * radius)

        # Triangle formed by center and the two points on the circumference
        triangles.append(TriangleShape(center, p1, p2))

    return triangles

def rectangle(width, height):
    center = Vector2(0, 0)
    tl = center + Vector2(-width/2, height/2)
    tr = center + Vector2(width/2, height/2)
    bl = center + Vector2(-width/2, -height/2)
    br = center + Vector2(width/2, -height/2)

    t1 = TriangleShape(tl, tr, bl)
    t2 = TriangleShape(br, bl, tr)
    return [t1, t2]