from vector import *
import pygame
from typing import List, Tuple
from triangle import Triangle

class Mesh(Triangle):
    def __init__(self, triangles: List[Triangle]):
        self.triangles = triangles

    def edges(self) -> List[Vector2]:
        edges = []
        for tri in self.triangles:
            edges.extend(tri.edges())
        return edges

    def edgeEndpoints(self) -> List[Tuple[Vector2, Vector2]]:
        endpoints = []
        for tri in self.triangles:
            endpoints.extend(tri.edgeEndpoints())
        return endpoints

    def project(self, axis: Vector2) -> Tuple[float, float]:
        min_proj = float("inf")
        max_proj = float("-inf")
        for tri in self.triangles:
            proj = tri.project(axis)
            min_proj = min(min_proj, proj[0])
            max_proj = max(max_proj, proj[1])
        return min_proj, max_proj

    def offset(self, vec: Vector2) -> "Mesh":
        """Return a new mesh with all triangles moved by vec."""
        new_triangles = [tri.offset(vec) for tri in self.triangles]
        return Mesh(new_triangles)

    def draw(self, surface: pygame.Surface, position: Vector2, width=0, color=(255, 0, 0)):
        for tri in self.triangles:
            tri.draw(surface, position, width, color)

    def scaleX(self, center: Vector2, factor: float) -> "Mesh":
        new_triangles = [tri.scaleX(center, factor) for tri in self.triangles]
        return Mesh(new_triangles)

    def scaleY(self, center: Vector2, factor: float) -> "Mesh":
        new_triangles = [tri.scaleY(center, factor) for tri in self.triangles]
        return Mesh(new_triangles)

    def scale(self, center: Vector2, factor: float) -> "Mesh":
        new_triangles = [tri.scale(center, factor) for tri in self.triangles]
        return Mesh(new_triangles)

    def rotate_around(self, center: Vector2, angle_deg: float) -> "Mesh":
        new_triangles = [tri.rotate_around(center, angle_deg) for tri in self.triangles]
        return Mesh(new_triangles)
    
    def copy(self) -> "Mesh":
        return Mesh(self.triangles.copy()) 

    def __iter__(self):
        return iter(self.triangles)
    
    def __len__(self):
        return len(self.triangles)
    
    def __getitem__(self, index):
        return self.triangles[index]