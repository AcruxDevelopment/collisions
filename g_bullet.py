from gobject import *
import random

class Bullet(GObject):
    def __init__(self, x, y, angle, mesh, acceleration, maxVelocity = 1000):
        super().__init__(x, y, angle, mesh)
        self.acceleration = acceleration
        self.velocity = 0
        self.maxVelocity = maxVelocity
        self.isYellow = random.randint(0, 5) == 0
        self.rotationLeft = 180
        self.origin = Vector2(x, y)

    def update(self):
        self.velocity += self.acceleration
        self.velocity = min(self.velocity, self.maxVelocity)
        self.move_in_direction(self.angle, self.velocity)