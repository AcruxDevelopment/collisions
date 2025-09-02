from triangle_shape import *
from vector import *
from gobject import *
from game import *
from g_bullet import *
import shapes

mesh_player = shapes.circle(10, 20)
mesh_spearBlocker = [tri.offset(Vector2(50, 0)) for tri in shapes.rectangle(10, 70)] 
mesh_bullet = shapes.circle(8, 15)
mesh_bar = shapes.rectangle(80, 20)


player = GObject(0, 0, 0, mesh_player)
spearBlocker = GObject(0, 0, 0, mesh_spearBlocker)
bar = GObject(0, 0, 0, mesh_bar)

player_speed = 5

class TestGame(Game):
    def __init__(self, clock, screen):
        super().__init__(clock, screen)
        self.bullets = []
        self.spearBlockerDesiredAngle = 0

    def start(self):
        global player
        self.objects.append(player)
        player.add_child(spearBlocker)

    def logic(self, dt):
        super().logic(dt)
        deletingBullets = []
        if(self.key('w')): player.y += player_speed
        if(self.key('s')): player.y -= player_speed
        if(self.key('a')): player.x -= player_speed
        if(self.key('d')): player.x += player_speed

        if(self.key('i')): self.spearBlockerDesiredAngle = 270
        if(self.key('l')): self.spearBlockerDesiredAngle = 0
        if(self.key('k')): self.spearBlockerDesiredAngle = 90
        if(self.key('j')): self.spearBlockerDesiredAngle = 180


        spearBlocker.rotate_towards(self.spearBlockerDesiredAngle, 20)

        if self.isFamilyObjectOffScreen(player):
            player.x = 0
            player.y = 0
        
        if self.tick % 10 == 0:
            bullet = Bullet(0, 0, 0, mesh_bullet, 0.1)
            bullet.pointTo(player)
            self.bullets.append(bullet)
            self.objects.append(bullet)

        for bullet in self.bullets:
            if bullet.touches(spearBlocker):
                deletingBullets.append(bullet)
            else:
                bullet.update()

        bar.angle += 1

        self.bullets[:] = [
            bullet for bullet in self.bullets if not self.isFamilyObjectOffScreen(bullet) and bullet not in deletingBullets
        ]

    def draw(self, screen):
        global player
        player.drawMesh(screen, 2, (255, 0, 0))

        for bullet in self.bullets:
            bullet.drawMesh(screen, 2, (255, 255, 255))

        bar.drawMesh(screen, 2, (0, 0, 255))