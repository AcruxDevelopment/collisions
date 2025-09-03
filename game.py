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
        self.sounds = []
        self.tick = -1
        self.sound_channels = {}  # {Sound: Channel}
        self.next_channel_id = 0

    def key(self, code):
        key_const = getattr(pygame, f"K_{code}")
        return self.keys[key_const]
    
    def queueSound(self, sound):
        self.sounds.append(sound)

    def _get_channel_for_sound(self, snd: pygame.mixer.Sound) -> pygame.mixer.Channel:
        """
        Return the dedicated channel for this sound.  
        If not assigned yet, auto-assign one.
        """
        if snd not in self.sound_channels:
            pygame.mixer.set_num_channels(max(self.next_channel_id + 1, pygame.mixer.get_num_channels()))
            self.sound_channels[snd] = pygame.mixer.Channel(self.next_channel_id)
            self.next_channel_id += 1
        return self.sound_channels[snd]

    def playSounds(self):
        for snd in set(self.sounds):
            ch = self._get_channel_for_sound(snd)
            ch.stop()      # cut off if already playing
            ch.play(snd)   # replay fresh
        self.sounds.clear()

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