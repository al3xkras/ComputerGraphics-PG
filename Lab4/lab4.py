import pygame.gfxdraw
from sys import exit
import os



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



class ProjectHexMap:
    def __init__(self):
        self.draw=True

    def start(self):
        pass

    def _pygame_screen_setup(self):
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % Lab3.WINDOW_POSITION
        return pygame.display.set_mode(Lab3.WINDOW_SIZE, Lab3.FLAGS)

    def exit(self):
        pygame.display.quit()
        pygame.quit()
        exit()

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
                    pass
                elif key.name == "right":
                    pass
                elif key.name == "up":
                    pass
                elif key.name == "down":
                    pass
                elif key.name == "q" or key.name == "Q":
                    pass

        with keyboard.Listener(on_press=on_press) as l:
            l.join()

    def _mainloop(self):
        clock = pygame.time.Clock()
        while self.draw:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
        self.latch.count_down()

if __name__ == '__main__':
    hmap = ProjectHexMap()
    hmap.start()