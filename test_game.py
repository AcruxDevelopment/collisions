from triangle_shape import *
from vector import *
from gobject import *
from game import *
from g_bullet import *
import shapes
import random

box_size = 250
spearBlockerDistance = 40

snd_spearBlocked = None
snd_hurt = None

mesh_player = shapes.circle(10, 20)
mesh_spearBlocker = [tri.offset(Vector2(spearBlockerDistance, 0)) for tri in shapes.rectangle(10, 70)] + [
    TriangleShape(Vector2(0, 0), Vector2(20, 20), Vector2(20, -20)).offset(Vector2(spearBlockerDistance, 35))
]

#mesh_bullet = shapes.circle(5, 15)
mesh_bullet = [TriangleShape(Vector2(0, 15), Vector2(0, -15), Vector2(25, 0))]
mesh_bar = shapes.rectangle(80, 20)
mesh_box = shapes.rectangle(box_size, box_size)

player = GObject(0, 0, 0, mesh_player)
spearBlocker = GObject(0, 0, 0, mesh_spearBlocker)
bar = GObject(0, 0, 0, mesh_bar)
box = GObject(0, 0, 0, mesh_box)
rotators = []

player_speed = 5

class TestGame(Game):
    def __init__(self, clock, screen):
        super().__init__(clock, screen)
        self.bullets = []
        self.spearBlockerDesiredAngle = 0
        self.mode = 'g'

    def start(self):
        global player
        global snd_spearBlocked
        global snd_hurt
        self.objects.append(player)
        player.add_child(spearBlocker)
        snd_spearBlocked = pygame.mixer.Sound("assets/spear_blocked.wav"); snd_spearBlocked.set_volume(0.3)
        snd_hurt = pygame.mixer.Sound("assets/hurt.wav"); snd_hurt.set_volume(0.3)

    def logic(self, dt):
        super().logic(dt)
        soundsToPlay = []
        deletingBullets = []

        if self.mode != 'g':
            if(self.key('w')): player.y += player_speed
            if(self.key('s')): player.y -= player_speed
            if(self.key('a')): player.x -= player_speed
            if(self.key('d')): player.x += player_speed
            

        if self.mode == 'g':
            if(self.key('w')): self.spearBlockerDesiredAngle = 270
            if(self.key('d')): self.spearBlockerDesiredAngle = 0
            if(self.key('s')): self.spearBlockerDesiredAngle = 90
            if(self.key('a')): self.spearBlockerDesiredAngle = 180

            if(self.key('i')): player.y += player_speed
            if(self.key('k')): player.y -= player_speed
            if(self.key('j')): player.x -= player_speed
            if(self.key('l')): player.x += player_speed


        spearBlocker.rotate_towards(self.spearBlockerDesiredAngle, 30)

        if self.isFamilyObjectOffScreen(player):
            player.x = 0
            player.y = 0
        
        bulletvel = 5 #5 #5
        interval = 20 #20 #15
        if self.tick % interval == 0:
            dist = 600
            poss = [Vector2(dist, 0), Vector2(-dist, 0), Vector2(0, dist), Vector2(0, -dist)]
            dirs = [180, 0, 90, -90]
            idx = random.randint(0, 3)
            pos = poss[idx]

            bullet = Bullet(pos.x, pos.y, dirs[idx], mesh_bullet, bulletvel, bulletvel)
            bullet.pointTo(player)
            self.bullets.append(bullet)
            self.objects.append(bullet)

        for bullet in self.bullets:
            if bullet.touches(spearBlocker):
                deletingBullets.append(bullet)
                self.queueSound(snd_spearBlocked)
            elif bullet.touches(player):
                deletingBullets.append(bullet)
                self.queueSound(snd_hurt)
            else:
                if bullet.isYellow and bullet.distance(player) < 200 and bullet.rotationLeft > 0:
                    dd = min(bullet.rotationLeft, 10)
                    bullet.rotate_around(0, 0, dd)
                    bullet.rotationLeft -= dd
                    bullet.pointTo(player)
                    bullet.move_in_direction(bullet.angle, bullet.velocity)
                else:
                    bullet.update()

        bar.angle += 1

        self.bullets[:] = [
            ##bullet for bullet in self.bullets if not self.isFamilyObjectOffScreen(bullet) and bullet not in deletingBullets
            bullet for bullet in self.bullets if bullet not in deletingBullets
        ]

        self.playSounds()

    def draw(self, screen):
        global player
        width = 0
        player.drawMesh(screen, width, (0, 190, 0))

        bulletIdx = 0
        for bullet in self.bullets:
            color = (255, 255, 255) if bulletIdx > 0 else (255, 0, 0)
            color = (255 ,255, 0) if bullet.isYellow else color
            bullet.drawMesh(screen, width, color)
            bulletIdx += 1

        box.drawMesh(screen, 5, (0, 190, 8))
        #bar.drawMesh(screen, 2, (0, 0, 255))