import traceback

import pygame.gfxdraw
from sys import exit
import os
from geometry_lib.data_representation import *
from pynput import keyboard
from threading import Lock,Thread
from Project5 import flat_map
pygame.font.init()



class DisplaySegmentIntersections:
    WINDOW_SIZE = (900, 600)
    WINDOW_POSITION = (500, 30)
    FONT_SIZE = 24
    FONT_BOLD = False
    FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE
    obj_offset=(WINDOW_SIZE[0]//2,WINDOW_SIZE[1]//2)
    offset=(5,5)
    _lock=Lock()
    font = pygame.font.SysFont('Comic Sans MS', 20)

    def __init__(self, segments, intersection_points, method, generator):
        self.segments = segments
        self.intersection_points = intersection_points
        self.draw_self = True
        self._cached_surface = None
        self.bbox = None
        self.scale = None
        self.method = method
        self.generator = generator
        self.screen = None
        self.init_bbox(segments)
        self.msg = "Q: re-generate input data"
        self.text_surf = self.font.render(self.msg,False,"white")

    def init_bbox(self,segments):
        points=flat_map(lambda seg: (seg.A,seg.B),segments)

        self.bbox = DisplaySegmentIntersections.bounding_box(points)
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
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % DisplaySegmentIntersections.WINDOW_POSITION
        return pygame.display.set_mode(DisplaySegmentIntersections.WINDOW_SIZE, DisplaySegmentIntersections.FLAGS)

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
        for s in self.segments:
            self.draw_line(surface,s.A,s.B,color=Color.to_pygame(s.color))
        for p in self.intersection_points:
            self.draw_point(surface,p,color=Color.to_pygame(p.color))

    def draw_point(self,surface:pygame.Surface,point,color="green"):
        radius=5
        scale=self.scale
        offset=self.obj_offset
        pygame.draw.circle(surface,color,(scale*(point.x+offset[0]),scale*(point.y+offset[1])),radius)

    def draw_line(self,surface: pygame.Surface, p1,p2,color="blue"):
        scale=self.scale
        offset=self.obj_offset
        pygame.draw.line(surface, color, (scale*(p1.x+offset[0]), scale*(p1.y+offset[1])),
                         (scale*(p2.x+offset[0]), scale*(p2.y+offset[1])),width=2)

    def exit(self):
        pygame.display.quit()
        pygame.quit()
        exit()

    def set_data(self,segments, intersection_points):
        self.segments=segments
        self.intersection_points=intersection_points
        self._cached_surface=None

    def _setup_hotkeys(self):
        def re_generate_data():
            try:
                self._cached_surface = None
                self.segments = self.generator()
                self.intersection_points = self.method(self.segments)
                self.init_bbox(self.segments)
            except:
                ex=traceback.format_exc()
                print(ex)
        def on_press(key):
            if hasattr(key, 'vk'):
                vk=key.vk
                if vk==81:
                    self._lock.acquire()
                    re_generate_data()
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
    from tests import Tests
    segs=Tests.generate_segments({
        Color.RED:23,
        Color.BLUE:15
    })

    segs=flat_map(lambda a:a,segs)

    print(segs)
    r=DisplaySegmentIntersections(segs,[
        Point(0, 10), Point(10, 10),
        Point(10, 0)
    ],method=None,generator=None)
    r.mainloop()