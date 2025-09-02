from sat import *
from triangle_shape import *
from vector import *
from gobject import *
import shapes
# -----------------------------
# MAIN PYGAME LOOP
# -----------------------------
def main():
    width = 0
    rvel = 0
    racc = 0.5
    rfric = 0.99

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Triangle Demo")
    clock = pygame.time.Clock()

    # Create some triangles
    t1 = shapes.circle(20, 60)
    t1a = shapes.rectangle(200, 30)
    t1b = shapes.rectangle(30, 200)
    t1c = [x.rotate_around(Vector2(0, 0), 45) for x in shapes.rectangle(200, 30)]
    t1d = [x.rotate_around(Vector2(0, 0), 45) for x in shapes.rectangle(30, 200)]
    t2 = shapes.rectangle(100, 250)

    mine = [*t1, *t1a, *t1b, *t1c, *t1d]

    mine1 = mine.copy()
    mine2 = [x.offset(Vector2(200, 200)) for x in mine.copy()]
    o1 = GObject(200, 200, 0, [*mine1, *mine2])
    o2 = GObject(400, 180, 0, [*t2])

    frame = 0
    running = True
    while running:
        rvel *= rfric
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        vel = 5
        keys_hold = pygame.key.get_pressed()
        if keys_hold[pygame.K_w]:
            o2.y -= vel
        if keys_hold[pygame.K_s]:
            o2.y += vel
        if keys_hold[pygame.K_a]:
            o2.x -= vel
        if keys_hold[pygame.K_d]:
            o2.x += vel

        rotation_point = o2.mesh[0].points[0] + o2.position()
        if keys_hold[pygame.K_k]:
            rvel -= racc
        if keys_hold[pygame.K_l]:
            rvel += racc

        o2.rotate_around(rotation_point.x, rotation_point.y, rvel)

        screen.fill((30, 30, 30))  # dark background
        pygame.draw.circle(screen, (255, 0, 0), (rotation_point.x, rotation_point.y), 20)
        color =  (255, 0, 0 ) if o1.touches(o2) else (0, 255, 0)
 
        # Draw triangles
        #if frame % 100 == 0:
            #if width == 0: width = 2
            #else: width = 0

        o1.drawMesh(screen, color=color, width=width)
        o2.drawMesh(screen, color=color, width=width)

        o1.angle += 0.3
        o1.x = 300 + math.sin(frame * 0.01) * 300

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()