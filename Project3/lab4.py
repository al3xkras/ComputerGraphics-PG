import pygame.gfxdraw
from sys import exit
import os
import threading
from hex_map import HexMap,Hex
from pynput import keyboard
from shapely.geometry import Polygon
from test.im_to_poly import FrameIterator,ImagePolygon

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
    WINDOW_SIZE = (900, 600)
    WINDOW_POSITION = (500, 30)
    FONT_SIZE = 24
    FONT_BOLD = False
    FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE
    def __init__(self):
        self.draw=True
        self.latch=CountDownLatch(1)
        self.screen=None

    def _pygame_screen_setup(self):
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ProjectHexMap.WINDOW_POSITION
        return pygame.display.set_mode(ProjectHexMap.WINDOW_SIZE, ProjectHexMap.FLAGS)

    def setup(self):
        self.screen=self._pygame_screen_setup()
        hotkey_thread = threading.Thread(target=self._setup_hotkeys)
        hotkey_thread.daemon = True
        hotkey_thread.start()

    def exit(self):
        pygame.display.quit()
        pygame.quit()
        exit()

    def _setup_hotkeys(self):
        def on_press(key):

            if hasattr(key, 'vk') and key.vk == 81:
                self.draw = False
                self.latch.await_countdown()
                exit()

            if hasattr(key, 'name'):
                print(key.name)
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

    def mainloop(self):
        self.setup()
        fr=FrameIterator("../test/test.mp4")
        hm = HexMap(ProjectHexMap.WINDOW_SIZE)
        rect=hm.map_poly
        clock = pygame.time.Clock()
        fps=pygame.time.Clock()

        im=None
        lock=threading.Lock()
        def draw_map():
            nonlocal im
            while self.draw:
                fps.tick(30)
                if not lock.locked():
                    im = fr.__next__()

        t=threading.Thread(target=draw_map,daemon=True)
        t.start()

        while self.draw:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
            self.screen.fill((0xff, 0xff, 0xff))
            hm.draw(self.screen)
            pygame.display.flip()

            lock.acquire()
            image=im
            lock.release()

            if not hm.is_preparing():
                try:
                    map_poly = ImagePolygon(image, 10, rect)
                except StopIteration:
                    map_poly = Polygon([(-100, 400), (400, -100), (300, 400), (400, 300)])

                hm.map_poly = map_poly
                hm.clear()
        self.latch.count_down()

if __name__ == '__main__':
    hmap = ProjectHexMap()
    hmap.mainloop()