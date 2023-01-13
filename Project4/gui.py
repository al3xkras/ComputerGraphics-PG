import pygame.gfxdraw
from sys import exit
import os
from geometry_lib.data_representation import Point
from pynput import keyboard
from threading import Lock,Thread
pygame.font.init()

class DisplayConvexHullResults:
    WINDOW_SIZE = (900, 600)
    WINDOW_POSITION = (500, 30)
    FONT_SIZE = 24
    FONT_BOLD = False
    FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE
    obj_offset=(WINDOW_SIZE[0]//2,WINDOW_SIZE[1]//2)
    offset=(5,5)
    _lock=Lock()
    font = pygame.font.SysFont('Comic Sans MS', 20)

    def __init__(self, points, convex_hull, method, generator):
        self.points = points
        self.convex_hull = convex_hull
        self.draw_self=True
        self._cached_surface=None
        self.bbox=None
        self.scale=None
        self.method=method
        self.generator=generator
        self.screen=None
        self.init_bbox(points)
        self.msg="Q: re-generate input data"
        self.text_surf=self.font.render(self.msg,False,"white")

    def init_bbox(self,points):
        self.bbox = DisplayConvexHullResults.bounding_box(points)
        msize = min(self.WINDOW_SIZE)
        s1 = abs(self.bbox[1][0] - self.bbox[0][0] + self.offset[0])
        s2 = abs(self.bbox[1][1] - self.bbox[0][1] + self.offset[1])
        self.scale = msize / max(s1, s2)*0.95
        self.obj_offset = -self.bbox[0][0], -self.bbox[0][1]
    @staticmethod
    def bounding_box(points):
        x, y = [p.x for p in points], [p.y for p in points]
        return [(min(x), min(y)),
                (max(x), max(y))]

    @staticmethod
    def _pygame_screen_setup():
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % DisplayConvexHullResults.WINDOW_POSITION
        return pygame.display.set_mode(DisplayConvexHullResults.WINDOW_SIZE, DisplayConvexHullResults.FLAGS)

    def setup(self):
        self.screen = self._pygame_screen_setup()
        hotkey_thread = Thread(target=self._setup_hotkeys,daemon=True)
        hotkey_thread.start()

    def draw(self):
        self._lock.acquire()
        if self._cached_surface is None:
            self._cached_surface=pygame.Surface(self.WINDOW_SIZE)
            self._draw(self._cached_surface)
        self.screen.blit(self._cached_surface,self.offset)
        self.screen.blit(self.text_surf,(self.WINDOW_SIZE[0]-self.font.size(self.msg)[0]-self.offset[0],self.offset[1]))
        self._lock.release()

    def _draw(self,surface):
        for p in self.points:
            self.draw_point(surface,p)
        for i in range(0,len(self.convex_hull)+2):
            self.draw_line(surface, self.convex_hull[i%len(self.convex_hull)], self.convex_hull[(i+1)%len(self.convex_hull)])

    def draw_point(self,surface:pygame.Surface,point):
        radius=3
        scale=self.scale
        offset=self.obj_offset
        pygame.draw.circle(surface,"green",(scale*(point.x+offset[0]),scale*(point.y+offset[1])),radius)

    def draw_line(self,surface: pygame.Surface, p1,p2):
        scale=self.scale
        offset=self.obj_offset
        pygame.draw.line(surface, "blue", (scale*(p1.x+offset[0]), scale*(p1.y+offset[1])),
                         (scale*(p2.x+offset[0]), scale*(p2.y+offset[1])),width=2)

    def exit(self):
        pygame.display.quit()
        pygame.quit()
        exit()

    def set_data(self,points,conv_hull):
        self.points=points
        self.convex_hull=conv_hull
        self._cached_surface=None

    def _setup_hotkeys(self):

        def on_press(key):
            if hasattr(key, 'vk'):
                vk=key.vk
                if vk==81:
                    self._lock.acquire()
                    self._cached_surface=None
                    self.points=self.generator()
                    self.convex_hull=self.method(self.points)
                    self.init_bbox(self.points)
                    self._lock.release()


        with keyboard.Listener(on_press=on_press) as l:
            l.join()

    def mainloop(self):
        self.setup()
        clock = pygame.time.Clock()
        while self.draw_self:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
            self.screen.fill((0x00, 0x00, 0x00))
            self.draw()
            pygame.display.flip()

if __name__ == '__main__':
    r=DisplayConvexHullResults([
        Point(0, 0), Point(10, 10),
        Point(0, 10), Point(10, 10),
        Point(10, 0), Point(5, 5),
    ],[
        Point(0, 10), Point(10, 10),
        Point(10, 0)
    ])
    r.mainloop()