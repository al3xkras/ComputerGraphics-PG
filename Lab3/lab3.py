import pygame.gfxdraw
from pynput import keyboard
from threading import Thread
from sys import exit
import os

from background import FalseDepthBackground
from spacecraft import Spacecraft


class Lab3:
    WINDOW_SIZE = (700, 700)
    WINDOW_POSITION = (500, 30)
    FONT_SIZE = 24
    FONT_BOLD = False
    FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE

    def __init__(self, initial_speed=0, bg_layer_count=15, bg_depth=200):
        self.screen = None
        self.background = None
        self.spacecraft = None
        self.hotkey_thread = None
        self.initial_speed=initial_speed
        self.bg_layer_count = bg_layer_count
        self.bg_depth = bg_depth
        self.warp = 0

    def setup(self, setup_hotkeys=True):
        self.background = FalseDepthBackground(self.bg_layer_count, self.initial_speed, self.bg_depth)
        self.spacecraft = Spacecraft()

        if setup_hotkeys:
            self.hotkey_thread = Thread(target=self._setup_hotkeys)
            self.hotkey_thread.daemon = True
            self.hotkey_thread.start()

        self.screen = self._pygame_screen_setup()

    def speed_up(self):
        self.background.speed_up(100)
        print("speed up")

    def slow_down(self):
        self.background.slow_down(100)
        print("slow down")

    def _setup_hotkeys(self):
        with keyboard.GlobalHotKeys({
            'a': self.speed_up,
            'b': self.slow_down,
            '<ctrl>+c': quit}) as h:
            h.join()

    def _pygame_screen_setup(self):
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % Lab3.WINDOW_POSITION
        return pygame.display.set_mode(Lab3.WINDOW_SIZE, Lab3.FLAGS)

    def stop(self):
        pygame.quit()
        exit()

    def mainloop(self):
        assert self.background is not None
        assert self.spacecraft is not None

        clock = pygame.time.Clock()
        while True:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

            screen = self.screen
            screen.fill((0x00, 0x00, 0x00))

            self.background.draw(screen)
            # self.spacecraft.draw(screen)

            pygame.display.flip()


if __name__ == '__main__':
    from pygame.locals import *

    lab3 = Lab3(bg_layer_count=15, initial_speed=0,bg_depth=200)
    lab3.setup()
    lab3.background.reverse()
    lab3.background.star_size=7
    lab3.mainloop()
