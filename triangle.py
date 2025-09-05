from polygon import Polygon
from vector import *
import pygame
import math
from typing import List, Tuple

class Triangle(Polygon):
    def __init__(self, p1: Vector2, p2: Vector2, p3: Vector2):
        self.points = [p1, p2, p3]

    def edges(self) -> List[Vector2]:
        return [self.points[(i+1) % 3] - self.points[i] for i in range(3)]

    def edgeEndpoints(self) -> List[Tuple[Vector2, Vector2]]:
        return [(self.points[i], self.points[(i+1) % 3]) for i in range(3)]

    def project(self, axis: Vector2) -> Tuple[float, float]:
        projections = [p.dot(axis) for p in self.points]
        return min(projections), max(projections)

    def offset(self, vec: Vector2) -> "Triangle":
        """Return a new triangle with all points moved by vec."""
        return Triangle(
            self.points[0] + vec,
            self.points[1] + vec,
            self.points[2] + vec
        )

    def draw(self, surface: pygame.Surface, position: Vector2, width=0, color=(255, 0, 0)):
        height = surface.get_height()
        points = [
            (p.x + position.x, -p.y + position.y)
            for p in self.points
        ]
        pygame.draw.polygon(surface, color, points, width)

    def scaleX(self, center: Vector2, factor: float) -> "Triangle":
        """Scale only horizontally relative to a center point."""
        new_points = []
        for p in self.points:
            new_x = center.x + (p.x - center.x) * factor
            new_points.append(Vector2(new_x, p.y))
        return Triangle(*new_points)

    def scaleY(self, center: Vector2, factor: float) -> "Triangle":
        """Scale only vertically relative to a center point."""
        new_points = []
        for p in self.points:
            new_y = center.y + (p.y - center.y) * factor
            new_points.append(Vector2(p.x, new_y))
        return Triangle(*new_points)

    def scale(self, center: Vector2, factor: float) -> "Triangle":
        """Uniformly scale horizontally and vertically using scaleX and scaleY."""
        return self.scaleX(center, factor).scaleY(center, factor)

    def rotate_around(self, center: Vector2, angle_deg: float) -> "Triangle":
        """Return a new TriangleShape rotated around a given center by angle_deg (standard math, CW)."""
        rad = -math.radians(angle_deg)
        cos_r = math.cos(rad)
        sin_r = math.sin(rad)
        new_points = []
        for p in self.points:
            dx = p.x - center.x
            dy = p.y + center.y
            # Standard math: CW rotation
            new_x = center.x + dx * cos_r + dy * sin_r
            new_y = center.y - dx * sin_r + dy * cos_r
            new_points.append(Vector2(new_x, new_y))
        return Triangle(*new_points)

    def copy(self) -> "Triangle":
        return Triangle(*[p.copy() for p in self.points])