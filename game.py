class Game:
    def __init__(self, clock, screen):
        self.objects = []
        self.clock = clock
        self.screen = screen

    def start(self):
        pass

    def logic(self, dt):
        pass

    def draw(self, screen):
        for i in self.objects:
            i.draw(screen)
        pass