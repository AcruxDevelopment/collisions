from triangle import *
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
mesh_spearBlocker = Mesh(
    [shapes.rectangle(10, 70).offset(Vector2(spearBlockerDistance, 0))] +
    [Triangle(Vector2(0, 0), Vector2(20, 20), Vector2(20, -20)).offset(Vector2(spearBlockerDistance, 35))]
)

#mesh_bullet = shapes.circle(5, 15)
mesh_bullet = Mesh([Triangle(Vector2(0, 10), Vector2(0, -10), Vector2(25, 0)).offset(Vector2(-7, 0))])
mesh_bullet_yellow = mesh_bullet.rotate_around(Vector2(0, 0), 180)
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
        self.spearBlockerDesiredAngle = -1
        self.mode = 'g'
        self.spawnCooldown = 0
        self.maxHurtTimeCooldown = 10
        self.hurtTimeCooldown = 0
        self.bot = False
        #self.record = eval("[(Vector2(0, 600), 41), (Vector2(600, 0), 58), (Vector2(0, 600), 75), (Vector2(600, 0), 94), (Vector2(0, 600), 109), (Vector2(600, 0), 121), (Vector2(0, 600), 133), (Vector2(600, 0), 150), (Vector2(600, 0), 167), (Vector2(0, 600), 185), (Vector2(0, 600), 200), (Vector2(600, 0), 213)]")
        #self.record = [(Vector2(0, 600), 0), (Vector2(0, -600), 0), (Vector2(0, 0), 150)] + [(Vector2(0, 1000), 0), (Vector2(0, 1000), 0), (Vector2(0, 0), 150)]
        #self.record = [(Vector2(0, 600), 0), (Vector2(600, 0), 15), (Vector2(0, 600), 32), (Vector2(600, 0), 52), (Vector2(600, 0), 68), (Vector2(600, 0), 81), (Vector2(600, 0), 94), (Vector2(0, 600), 114), (Vector2(0, 600), 132), (Vector2(600, 0), 150), (Vector2(0, 600), 165)]
        #self.record = [(Vector2(0, 600), 0), (Vector2(600, 0), 15)]
        #self.record = []
        self.recording = False
        self._record = []
        if not self.recording:
            with open("record.txt", "r") as f:
                self._record = eval(f.read())
        else:
            self._record = []
        self.record = [(i[0], i[1]-self._record[0][1]) for i in self._record]
        self.recordCopy = self.record.copy()
        self.useRandomPattern = False
        self.delay = 0
        self.bulletIdx = 0

    def start(self):
        global player
        global snd_spearBlocked
        global snd_hurt
        self.objects.append(player)
        player.add_child(spearBlocker)
        self.objects.append(spearBlocker)
        snd_spearBlocked = pygame.mixer.Sound("assets/spear_blocked.wav"); snd_spearBlocked.set_volume(0.5)
        snd_hurt = pygame.mixer.Sound("assets/hurt.wav"); snd_hurt.set_volume(0.5)
        self.spawntick = 0
        pygame.mixer.music.load("assets/battle_theme.wav")
        pygame.mixer.music.set_volume(0)
        

    def logic(self, dt):
        super().logic(dt)
        
        #spearBlocker.scaleX = 1 + (math.sin(self.tick * 0.05)+1) * 3
        spearBlocker.scaleY += 0.005
        if(self.hurtTimeCooldown): self.hurtTimeCooldown -= 1

        deletingBullets = []

        if self.mode != 'g':
            if(self.key('w')): player.y += player_speed
            if(self.key('s')): player.y -= player_speed
            if(self.key('a')): player.x -= player_speed
            if(self.key('d')): player.x += player_speed
            

        recordedThisFrame = False
        if self.mode == 'g':
            # Up + Left
            if self.key('w') and self.key('a'):
                if not (self.prevKey('w') or self.prevKey('a')) and self.recording:
                    self.record.append((Vector2(-600, 600), self.tick))
                    self.hurtTimeCooldown = 10
                self.spearBlockerDesiredAngle = -90-45  # diagonal up-left

            # Up + Right
            elif self.key('w') and self.key('d'):
                if not (self.prevKey('w') or self.prevKey('d')) and self.recording:
                    self.record.append((Vector2(600, 600), self.tick))
                    self.hurtTimeCooldown = 10
                self.spearBlockerDesiredAngle = -45  # diagonal up-right

            # Down + Left
            elif self.key('s') and self.key('a'):
                if not (self.prevKey('s') or self.prevKey('a')) and self.recording:
                    self.record.append((Vector2(-600, -600), self.tick))
                    self.hurtTimeCooldown = 10
                self.spearBlockerDesiredAngle = 90+45  # diagonal down-left

            # Down + Right
            elif self.key('s') and self.key('d'):
                if not (self.prevKey('s') or self.prevKey('d')) and self.recording:
                    self.record.append((Vector2(600, -600), self.tick))
                    self.hurtTimeCooldown = 10
                self.spearBlockerDesiredAngle = 45  # diagonal down-right

            # Single directions (original logic)
            elif self.key('w') and not self.key('a') and not self.key('d'):
                if not self.prevKey('w') and self.recording:
                    self.record.append((Vector2(0, 600), self.tick))
                    self.hurtTimeCooldown = 10
                self.spearBlockerDesiredAngle = 270  # up

            elif self.key('s') and not self.key('a') and not self.key('d'):
                if not self.prevKey('s') and self.recording:
                    self.record.append((Vector2(0, -600), self.tick))
                    self.hurtTimeCooldown = 10
                self.spearBlockerDesiredAngle = 90  # down

            elif self.key('d') and not self.key('w') and not self.key('s'):
                if not self.prevKey('d') and self.recording:
                    self.record.append((Vector2(600, 0), self.tick))
                    self.hurtTimeCooldown = 10
                self.spearBlockerDesiredAngle = 0  # right

            elif self.key('a') and not self.key('w') and not self.key('s'):
                if not self.prevKey('a') and self.recording:
                    self.record.append((Vector2(-600, 0), self.tick))
                    self.hurtTimeCooldown = 10
                self.spearBlockerDesiredAngle = 180  # left

            if self.spearBlockerDesiredAngle != -1 and not pygame.mixer.music.get_busy() and self.recording:
                pygame.mixer.music.play(-1)

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

        if spearBlocker.angle != self.spearBlockerDesiredAngle:
            spearBlocker.rotate_towards(self.spearBlockerDesiredAngle, 30)

        if self.isFamilyObjectOffScreen(player):
            player.x = 0
            player.y = 0
        
        bulletvel = 7 #5 #5 # 7
        interval = 10 #15 #20 #15
        interval += random.randint(0, 20) # 30
        dist = 600
        self.spawntick += 1
        if self.spawnCooldown <= 0 and not self.recording and self.useRandomPattern:
            poss = [Vector2(dist, 0), Vector2(-dist, 0), Vector2(0, dist), Vector2(0, -dist)]
            dirs = [180, 0, 90, -90]
            idx = random.randint(0, 3)
            pos = poss[idx]

            bullet = Bullet(pos.x, pos.y, dirs[idx], mesh_bullet, mesh_bullet_yellow, bulletvel, bulletvel)
            bullet.pointTo(player)
            self.bullets.append(bullet)
            self.objects.append(bullet)

            self.spawnCooldown = interval
            if bullet.isYellow: self.spawnCooldown = max(self.spawnCooldown, 30)
        elif not self.useRandomPattern and len(self.record) > 0 and not self.recording:
            incomingSpear = self.record[0]

            if self.spawntick - self.delay >= incomingSpear[1]:
                pos = incomingSpear[0]
                dir = 0
                if pos.x > 0: dir = 180
                if pos.x < 0: dir = 0
                if pos.y > 0: dir = 90
                if pos.y < 0: dir = -90

                #pos = [Vector2(dist, 0), Vector2(-dist, 0), Vector2(0, dist), Vector2(0, -dist)]
                #pos = pos[random.randint(0, 3)]
                bullet = Bullet(pos.x, pos.y, dir, mesh_bullet, mesh_bullet_yellow, bulletvel, bulletvel)
                #bullet.isYellow = self.bulletIdx == 0
                #bullet.isYellow = False
                bullet.pointTo(player)
                self.bullets.append(bullet)
                if bullet.isYellow:
                    #self.delay += 5
                    bullet.move_in_direction(bullet.angle, 120)
                self.objects.append(bullet)
                self.objects.append(bullet)
                self.spawntick = incomingSpear[1]
                self.bulletIdx += 1

                self.record.pop(0)
        elif len(self.record) == 0 and not self.recording and not self.useRandomPattern:
            toAdd = self.recordCopy
            #toAdd = []
            for i in toAdd:
                self.record.append(i)
            self.spawntick = -100
            self.delay = 0
            self.bulletIdx = 0
        else:
            self.spawnCooldown -= 1

        for bullet in self.bullets:
            if bullet.touches(spearBlocker):
                deletingBullets.append(bullet)
                self.queueSound(snd_spearBlocked)
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
                    self.spawntick += 5

            elif bullet.touches(player):
                deletingBullets.append(bullet)
                self.queueSound(snd_hurt)
                self.hurtTimeCooldown = self.maxHurtTimeCooldown
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
                    self.spawntick += 5
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
        self.afterLogic()

    def draw(self, screen):
        global player
        width = 0
        player.drawMesh(screen, width, (0, 190, 0) if self.hurtTimeCooldown == 0 else (0, 50, 10))

        bulletIdx = 0
        for bullet in self.bullets:
            color = (170, 190, 255) if bulletIdx > 0 else (255, 0, 0)
            color = (255 ,255, 0) if bullet.isYellow else color
            bullet.drawMesh(screen, width, color)
            bulletIdx += 1

        for i in self.objects:
            i.recomputeTransformedMesh()

        box.drawMesh(screen, 5, (0, 190, 8))
        #bar.drawMesh(screen, 2, (0, 0, 255))