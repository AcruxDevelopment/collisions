from vector import *
import pygame
from typing import List, Tuple

class Polygon:
    def __init__(self, points: List[Vector2]):
        self.points = points

    def edges(self) -> List[Vector2]: pass
    def edgeEndpoints(self) -> List[Tuple[Vector2, Vector2]]: pass
    def project(self, axis: Vector2) -> Tuple[float, float]: pass
    def offset(self, vec: Vector2) -> "Polygon": pass
    def draw(self, surface: pygame.Surface, position: Vector2, width=0, color=(255, 0, 0)): pass
    def scaleX(self, center: Vector2, factor: float) -> "Polygon": pass
    def scaleY(self, center: Vector2, factor: float) -> "Polygon": pass
    def scale(self, center: Vector2, factor: float) -> "Polygon": pass
    def rotate_around(self, center: Vector2, angle_deg: float) -> "Polygon": pass
    def copy(self) -> "Polygon": pass