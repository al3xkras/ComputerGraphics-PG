import pygame.gfxdraw
from pynput import keyboard
from threading import Thread
from sys import exit
import os

from background import FalseDepthBackground
from spacecraft import Spacecraft
import threading


class CountDownLatch(object):
    def __init__(self, count=1):
        self.count = count
        self.lock = threading.Condition()

    def count_down(self):
        self.lock.acquire()
        self.count -= 1
        if self.count <= 0:
            self.lock.notify_all()
        self.lock.release()

    def await_countdown(self):
        self.lock.acquire()
        while self.count > 0:
            self.lock.wait()
        self.lock.release()


class SpaceshipInfo:
    def __init__(self, warp_getter):
        self.warp_getter = warp_getter

    def draw(self, screen: pygame.Surface):
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text = my_font.render("warp: %d" % self.warp_getter(), False, (255, 255, 255))
        screen.blit(text, (15, 15))


class Lab3:
    WINDOW_SIZE = (900, 700)
    WINDOW_POSITION = (500, 30)
    FONT_SIZE = 24
    FONT_BOLD = False
    FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE
    warp_min = 0
    warp_max = 10
    contestant_spaceship_warp_speed = 5

    def __init__(self, initial_speed=0, bg_layer_count=15, bg_depth=200):
        self.screen = None
        self.background = None
        self.spacecraft = None
        self.contestant_spacecraft = None
        self.hotkey_thread = None
        self.spaceship_info = None
        self.initial_speed = initial_speed
        self.bg_layer_count = bg_layer_count
        self.bg_depth = bg_depth
        self.warp = 0
        self.distance_traveled = 0
        self.distance_traveled_spaceship1 = 0
        self.distance_traveled_spaceship2 = 0

        self.latch = CountDownLatch()
        self.draw = True

    def setup(self, setup_hotkeys=True):
        self.background = FalseDepthBackground(self.bg_layer_count, self.initial_speed, self.bg_depth)
        self.spacecraft = Spacecraft(displaySize=Lab3.WINDOW_SIZE)
        self.spaceship_info = SpaceshipInfo(lambda: self.warp)
        self.contestant_spacecraft = Spacecraft(displaySize=Lab3.WINDOW_SIZE, sprite="contestant_spaceship.png")
        if setup_hotkeys:
            self.hotkey_thread = Thread(target=self._setup_hotkeys)
            self.hotkey_thread.daemon = True
            self.hotkey_thread.start()

        self.screen = self._pygame_screen_setup()

    def speed_up(self):
        if self.warp >= Lab3.warp_max:
            return
        self.warp += 1
        self.background.speed_up(50)
        print("speed up")

    def slow_down(self):
        if self.warp <= Lab3.warp_min:
            return
        self.warp -= 1
        self.background.slow_down(50)
        print("slow down")

    def _setup_hotkeys(self):
        def on_press(key):
            if hasattr(key, 'vk') and key.vk == 12:
                self.stop()

            if hasattr(key, 'vk') and key.vk == 81:
                self.draw = False
                self.latch.await_countdown()
                exit()

            if hasattr(key, 'name'):
                if key.name == "left":
                    self.slow_down()
                elif key.name == "right":
                    self.speed_up()
                elif key.name == "up":
                    self.spacecraft.move(-Lab3.WINDOW_SIZE[1] / 10)
                elif key.name == "down":
                    self.spacecraft.move(Lab3.WINDOW_SIZE[1] / 10)
                elif key.name == "q" or key.name == "Q":
                    self.exit()

        with keyboard.Listener(on_press=on_press) as l:
            l.join()

    def _pygame_screen_setup(self):
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % Lab3.WINDOW_POSITION
        return pygame.display.set_mode(Lab3.WINDOW_SIZE, Lab3.FLAGS)

    def exit(self):
        pygame.display.quit()
        pygame.quit()
        exit()

    def stop(self):
        self.warp = 0
        self.spacecraft.stop()
        self.background.stop()

    def mainloop(self):

        self.spacecraft.move(Lab3.WINDOW_SIZE[1] / 2)
        clock = pygame.time.Clock()
        while self.draw:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

            screen = self.screen
            screen.fill((0x00, 0x00, 0x00))

            self.background.draw(screen)
            self.spaceship_info.draw(screen)

            self.distance_traveled += self.warp * 2
            self.distance_traveled_spaceship1 += self.warp * 2
            self.distance_traveled_spaceship2 += Lab3.contestant_spaceship_warp_speed * 2

            self.spacecraft.speed_up(self.distance_traveled_spaceship1 - self.distance_traveled)
            self.contestant_spacecraft.speed_up(self.distance_traveled_spaceship2 - self.distance_traveled)

            self.spacecraft.draw(screen)
            self.contestant_spacecraft.draw(screen)
            pygame.display.flip()

        self.latch.count_down()


if __name__ == '__main__':
    from pygame.locals import *

    lab3 = Lab3(bg_layer_count=15, initial_speed=0, bg_depth=200)
    lab3.setup()
    lab3.background.reverse()
    lab3.background.star_size = 7
    lab3.mainloop()
