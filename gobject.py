import pygame
import math
from vector import Vector2
from typing import List, Optional
import sat

class GObject:
    def __init__(self, x=0.0, y=0.0, angle=0.0, mesh: Optional[List] = None, ignoreMeshRotation=False):
        self._x = x
        self._y = y
        self._scaleX = 1
        self._scaleY = 1
        self._angle = angle  # degrees
        self.mesh: List = mesh if mesh else []  # list of unrotated meshes
        self.transformed_mesh: List = self.mesh.copy()      # list of rotated meshes
        self.children: List[GObject] = []
        self.ignoreMeshRotation = ignoreMeshRotation  # if true, mesh won't rotate with angle changes

    # -----------------------------
    # HIERARCHY MANAGEMENT
    # -----------------------------
    def add_child(self, child: "GObject"):
        self.children.append(child)

    # -----------------------------
    # PROPERTIES
    # -----------------------------
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        dx = value - self._x
        self._x = value
        for child in self.children:
            child.x += dx

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        dy = value - self._y
        self._y = value
        for child in self.children:
            child.y += dy

    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, value):
        delta_angle = (value - self._angle)
        self._angle = value  # _angle is CW-positive now
        # Rotate children around this object using CW-positive convention
        for child in self.children:
            child.rotate_around(self.x, self.y, delta_angle)
        # Rotate meshes: most geometry helpers use CCW-positive, so pass NEGATED angle
        if not self.ignoreMeshRotation:
            self.transformed_mesh = [m.rotate_around(Vector2(0, 0), -self._angle) for m in self.mesh]

    @property
    def scaleX(self):
        return self._scaleX
    @scaleX.setter
    def scaleX(self, value):
        if value == 0:
            raise ValueError("scaleX cannot be zero")
        factor = value / self._scaleX
        self._scaleX = value
        for child in self.children:
            child.scaleX *= factor
        # Scale meshes around origin
        self.mesh = [m.scaleX(Vector2(0, 0), factor) for m in self.mesh]
        if not self.ignoreMeshRotation:
            self.transformed_mesh = [m.rotate_around(Vector2(0, 0), -self._angle) for m in self.mesh]

    @property
    def scaleY(self):
        return self._scaleY
    @scaleY.setter
    def scaleY(self, value):
        if value == 0:
            raise ValueError("scaleY cannot be zero")
        factor = value / self._scaleY
        self._scaleY = value
        for child in self.children:
            child.scaleY *= factor
        # Scale meshes around origin
        self.mesh = [m.scaleY(Vector2(0, 0), factor) for m in self.mesh]
        if not self.ignoreMeshRotation:
            self.transformed_mesh = [m.rotate_around(Vector2(0, 0), -self._angle) for m in self.mesh]


    # -----------------------------
    # TRANSFORMATIONS
    # -----------------------------
    def position(self) -> Vector2:
        return Vector2(self.x, self.y)

    def move_in_direction(self, angle_deg: float, distance: float):
        # CW-positive: convert to CCW to use math cos/sin
        rad = math.radians(-angle_deg)
        self.x += math.cos(rad) * distance
        self.y += math.sin(rad) * distance  # y is math-up; you already flip on draw


    def pointTo(self, target:"GObject"):
        """
        Rotate this object so it points toward `target`.
        """
        self.pointToVector(target.position())

    def pointToVector(self, target: Vector2):
        direction = target - self.position()
        # atan2 is CCW-positive; convert to CW-positive
        angle_cw = (-math.degrees(math.atan2(direction.y, direction.x))) % 360
        self.angle = angle_cw


    def rotate_towards(self, desired_angle, step=5):
        """
        Rotate this object smoothly towards a target angle using the shortest path.

        :param desired_angle: target angle in degrees
        :param step: max step (degrees per frame) towards the target
        """
        # Normalize both angles to [0, 360)
        current = self.angle % 360
        target = desired_angle % 360

        # Compute shortest signed difference (-180, 180]
        diff = (target - current + 180) % 360 - 180

        # If the difference is small, snap to target
        if abs(diff) <= step:
            self.angle = target
        else:
            # Rotate by step in the shortest direction
            self.angle = (current + step * math.copysign(1, diff)) % 360

    def rotate_around(self, center_x: float, center_y: float, delta_angle: float):
        # Make +delta_angle = clockwise by negating for the math rotation
        rad = math.radians(-delta_angle)
        dx = self.x - center_x
        dy = self.y - center_y
        new_x = dx * math.cos(rad) - dy * math.sin(rad)
        new_y = dx * math.sin(rad) + dy * math.cos(rad)
        self._x = center_x + new_x
        self._y = center_y + new_y

        # Track angle in CW-positive
        self.angle = (self.angle + delta_angle) % 360

        # Rotate children recursively with the same CW-positive delta
        for child in self.children:
            child.rotate_around(center_x, center_y, delta_angle)



    # -----------------------------
    # COLLISION / DISTANCE
    # -----------------------------
    def distance(self, other: "GObject") -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.hypot(dx, dy)

    def touches(self, other: "GObject") -> bool:
        """
        Check collision using SAT with triangles offset by each object's position.
        """
        for myTri in self.transformed_mesh:
            # Offset my triangle by self position
            offset_myTri = myTri.offset(self.position())
            for theirTri in other.transformed_mesh:
                # Offset their triangle by their position
                offset_theirTri = theirTri.offset(other.position())
                if sat.triangles_collide(offset_myTri, offset_theirTri):
                    return True
        return False

    # -----------------------------
    # MESH
    # -----------------------------
    def setMesh(self, mesh: List):
        self.mesh = mesh
        if not self.ignoreMeshRotation:
            self.transformed_mesh = [m.rotate_around(Vector2(0, 0), -self._angle) for m in self.mesh]
        else:
            self.transformed_mesh = self.mesh.copy()

    # -----------------------------
    # DRAWING
    # -----------------------------
    def drawMesh(self, surface: pygame.Surface, width=1, color=(255, 0, 0), drawOrigin=False):
        centerizedPosition = self.position() + Vector2(0, 0); centerizedPosition.y *= -1
        centerizedPosition = centerizedPosition + Vector2(surface.get_width() / 2, surface.get_height() / 2)

        # Draw origin cross
        if drawOrigin:
            originSize = 10
            originStrokeSize = 2
            tl = centerizedPosition + Vector2(-originSize, -originSize)
            tr = centerizedPosition + Vector2(originSize, -originSize)
            bl = centerizedPosition + Vector2(-originSize, originSize)
            br = centerizedPosition + Vector2(originSize, originSize)
            pygame.draw.line(surface, color, (tl.x, tl.y), (br.x, br.y), originStrokeSize)
            pygame.draw.line(surface, color, (tr.x, tr.y), (bl.x, bl.y), originStrokeSize)

        # Draw all meshes
        for m in self.transformed_mesh:
            m.draw(surface, centerizedPosition, width, color)
        # Draw children
        for child in self.children:
            child.drawMesh(surface, width, color)
