from triangle_shape import *
from vector import *
from gobject import *
from game import *
import shapes

mesh_player = shapes.circle(10, 20)
player = GObject(0, 0, 0, mesh_player)

class TestGame(Game):
    def __init__(self, clock, screen):
        super().__init__(clock, screen)
        pass

    def start(self):
        global player
        self.objects.append(player)

    def logic(self, dt):
        player.y += 1
        pass

    def draw(self, screen):
        global player
        player.drawMesh(screen, 0, (255, 255, 255))
        pass