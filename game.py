import pygame
import shapes
from gobject import *

class Game:
    def __init__(self, clock, screen):
        self.screenObj = GObject(0, 0, 0, shapes.rectangle(screen.get_width(), screen.get_height()))
        self.objects = []
        self.clock = clock
        self.screen = screen
        self.keys = {}
        self.tick = -1

    def key(self, code):
        key_const = getattr(pygame, f"K_{code}")
        return self.keys[key_const]

    def start(self):
        pass

    def logic(self, dt):
        self.keys = pygame.key.get_pressed()
        self.tick += 1
        pass

    def draw(self, screen):
        pass

    def isSingleObjectOffScreen(self, object:GObject):
        return not object.touches(self.screenObj)
    
    def isFamilyObjectOffScreen(self, object:GObject):
        for child in object.children:
            if not self.isFamilyObjectOffScreen(child): return False

        return self.isSingleObjectOffScreen(object)