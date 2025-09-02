from sat import *
from triangle_shape import *
from vector import *
from gobject import *
from game import *
from test_game import TestGame
import shapes
# -----------------------------
# MAIN PYGAME LOOP
# -----------------------------

clock:pygame.time.Clock = None
screen:pygame.surface = None
running:bool = True
game:Game = None

def gameLogic():
    pass

def systemLogic():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def draw():
    global game
    screen.fill((0,0,0))
    game.draw(screen)
    pygame.display.flip()
        
def tick():
    global clock
    global game
    global screen
    systemLogic()
    game.logic(1)
    draw()
    clock.tick(60)

def main():
    global clock
    global screen
    global running
    global game

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Triangle Demo")
    game = TestGame(clock, screen)

    game.start()
    while running:
        tick()
    pygame.quit()

if __name__ == "__main__":
    main()