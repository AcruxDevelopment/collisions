from typing import Tuple, List

# -----------------------------
# VECTOR CLASS
# -----------------------------
class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2":
        return Vector2(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    # Dot product
    def dot(self, other: "Vector2") -> float:
        return self.x * other.x + self.y * other.y

    # Perpendicular vector
    def perpendicular(self) -> "Vector2":
        return Vector2(-self.y, self.x)