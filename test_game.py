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
mesh_bullet = [TriangleShape(Vector2(0, 10), Vector2(0, -10), Vector2(25, 0)).offset(Vector2(-7, 0))]
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
        self.spawnCooldown = 0
        self.maxHurtTimeCooldown = 10
        self.hurtTimeCooldown = 0
        self.bot = True
        self.record = eval("[(Vector2(0, 600), 41), (Vector2(600, 0), 58), (Vector2(0, 600), 75), (Vector2(600, 0), 94), (Vector2(0, 600), 109), (Vector2(600, 0), 121), (Vector2(0, 600), 133), (Vector2(600, 0), 150), (Vector2(600, 0), 167), (Vector2(0, 600), 185), (Vector2(0, 600), 200), (Vector2(600, 0), 213)]")
        self.recording = False
        self.useRandomPattern = False
        self.delay = 0

    def start(self):
        global player
        global snd_spearBlocked
        global snd_hurt
        self.objects.append(player)
        player.add_child(spearBlocker)
        snd_spearBlocked = pygame.mixer.Sound("assets/spear_blocked.wav"); snd_spearBlocked.set_volume(0.5)
        snd_hurt = pygame.mixer.Sound("assets/hurt.wav"); snd_hurt.set_volume(0.5)
        pygame.mixer.music.load("assets/battle_theme.wav")
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

    def logic(self, dt):
        super().logic(dt)

        if(self.hurtTimeCooldown): self.hurtTimeCooldown -= 1

        soundsToPlay = []
        deletingBullets = []

        if self.mode != 'g':
            if(self.key('w')): player.y += player_speed
            if(self.key('s')): player.y -= player_speed
            if(self.key('a')): player.x -= player_speed
            if(self.key('d')): player.x += player_speed
            

        if self.mode == 'g':
            if(self.key('w')): 
                if self.spearBlockerDesiredAngle != 270 and self.recording:
                    self.record.append((Vector2(0, 600), self.tick))
                self.spearBlockerDesiredAngle = 270
            if(self.key('d')):
                if self.spearBlockerDesiredAngle != 0 and self.recording:
                    self.record.append((Vector2(600, 0), self.tick))
                self.spearBlockerDesiredAngle = 0
            if(self.key('s')):
                if self.spearBlockerDesiredAngle != 90 and self.recording:
                    self.record.append((Vector2(0, 600), self.tick))
                self.spearBlockerDesiredAngle = 90
            if(self.key('a')):
                if self.spearBlockerDesiredAngle != 180 and self.recording:
                    self.record.append((Vector2(600, 0), self.tick))
                self.spearBlockerDesiredAngle = 180

            if(self.key('i')): player.y += player_speed
            if(self.key('k')): player.y -= player_speed
            if(self.key('j')): player.x -= player_speed
            if(self.key('l')): player.x += player_speed

        if self.bot and len(self.bullets) > 0:
            bullet = self.bullets[0]
            if bullet.origin.y > player.y + 10: self.spearBlockerDesiredAngle = 270 if not bullet.isYellow else 90
            if bullet.origin.y < player.y - 10: self.spearBlockerDesiredAngle = 90 if not bullet.isYellow else 270
            if bullet.origin.x > player.x + 10: self.spearBlockerDesiredAngle = 0 if not bullet.isYellow else 180
            if bullet.origin.x < player.x - 10: self.spearBlockerDesiredAngle = 180 if not bullet.isYellow else 0


        spearBlocker.rotate_towards(self.spearBlockerDesiredAngle, 30)

        if self.isFamilyObjectOffScreen(player):
            player.x = 0
            player.y = 0
        
        bulletvel = 10 #5 #5
        interval = 10 #15 #20 #15
        interval += random.randint(0, 20) # 30
        if self.spawnCooldown <= 0 and not self.recording and self.useRandomPattern:
            dist = 600
            poss = [Vector2(dist, 0), Vector2(-dist, 0), Vector2(0, dist), Vector2(0, -dist)]
            dirs = [180, 0, 90, -90]
            idx = random.randint(0, 3)
            pos = poss[idx]

            bullet = Bullet(pos.x, pos.y, dirs[idx], mesh_bullet, bulletvel, bulletvel)
            bullet.pointTo(player)
            self.bullets.append(bullet)
            self.objects.append(bullet)

            self.spawnCooldown = interval
            if bullet.isYellow: self.spawnCooldown = max(self.spawnCooldown, 30)
        elif not self.useRandomPattern and len(self.record) > 0 and not self.recording:
            incomingSpear = self.record[0]
            if len(self.record) < 5:
                toAdd = eval("[(Vector2(0, 600), 41), (Vector2(600, 0), 58), (Vector2(0, 600), 75), (Vector2(600, 0), 94), (Vector2(0, 600), 109), (Vector2(600, 0), 121), (Vector2(0, 600), 133), (Vector2(600, 0), 150), (Vector2(600, 0), 167), (Vector2(0, 600), 185), (Vector2(0, 600), 200), (Vector2(600, 0), 213)]")
                for i in toAdd:
                        self.record.append(i)

            if self.tick - self.delay > incomingSpear[1]:
                pos = incomingSpear[0]
                dir = 0
                if pos.x > 0: dir = 180
                if pos.x < 0: dir = 0
                if pos.y > 0: dir = 90
                if pos.y < 0: dir = -90

                bullet = Bullet(pos.x, pos.y, dir, mesh_bullet, bulletvel, bulletvel)
                bullet.pointTo(player)
                self.bullets.append(bullet)
                if bullet.isYellow:
                    self.delay += 5
                    bullet.move_in_direction(bullet.angle, 150)
                self.objects.append(bullet)

                self.record.pop(0)
        else:
            self.spawnCooldown -= 1

        for bullet in self.bullets:
            if bullet.touches(spearBlocker):
                deletingBullets.append(bullet)
                self.queueSound(snd_spearBlocked)
            elif bullet.touches(player):
                deletingBullets.append(bullet)
                self.queueSound(snd_hurt)
                self.hurtTimeCooldown = self.maxHurtTimeCooldown
            else:
                if bullet.isYellow and bullet.distance(player) < 200 and bullet.rotationLeft > 0:
                    dd = min(bullet.rotationLeft, 10)
                    bullet.rotate_around(0, 0, dd)
                    bullet.rotationLeft -= dd
                    bullet.pointTo(player)
                    #bullet.move_in_direction(bullet.angle, bullet.velocity)
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
        player.drawMesh(screen, width, (0, 190, 0) if self.hurtTimeCooldown == 0 else (0, 50, 10))

        bulletIdx = 0
        for bullet in self.bullets:
            color = (100, 100, 255) if bulletIdx > 0 else (255, 0, 0)
            color = (255 ,255, 0) if bullet.isYellow else color
            bullet.drawMesh(screen, width, color)
            bulletIdx += 1

        box.drawMesh(screen, 5, (0, 190, 8))
        #bar.drawMesh(screen, 2, (0, 0, 255))