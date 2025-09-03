from gobject import *
import random

class Bullet(GObject):
    def __init__(self, x, y, angle, normalMesh, yellowMesh, acceleration, maxVelocity = 1000):
        self.isYellow = random.randint(0, 7) == 0
        super().__init__(x, y, angle, normalMesh)
        self.rotated_mesh = normalMesh
        self.normalMesh = normalMesh
        self.yellowMesh = yellowMesh
        self.acceleration = acceleration
        self.velocity = 0
        self.maxVelocity = maxVelocity
        self.rotationLeft = 180
        self.origin = Vector2(x, y)
        self.tick = 0

    def update(self):
        self.velocity += self.acceleration
        self.velocity = min(self.velocity, self.maxVelocity)
        self.move_in_direction(self.angle, self.velocity)
        if self.tick == 0:
            self.setMesh(self.yellowMesh if self.isYellow else self.normalMesh)
            self.ignoreMeshRotation = self.isYellow
        self.tick += 1