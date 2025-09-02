from gobject import *

class Bullet(GObject):
    def __init__(self, x, y, angle, mesh, acceleration, maxVelocity = 1000):
        super().__init__(x, y, angle, mesh)
        self.acceleration = acceleration
        self.velocity = 0
        self.maxVelocity = maxVelocity

    def update(self):
        self.velocity += self.acceleration
        self.velocity = min(self.velocity, self.maxVelocity)
        self.move_in_direction(self.angle, self.velocity)