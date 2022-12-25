import pygame.gfxdraw
from sys import exit
import os
from geometry_lib.data_representation import Point

class DisplayConvexHullResults:
    WINDOW_SIZE = (900, 600)
    WINDOW_POSITION = (500, 30)
    FONT_SIZE = 24
    FONT_BOLD = False
    FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE
    obj_offset=(WINDOW_SIZE[0]//2,WINDOW_SIZE[1]//2)
    offset=(5,5)
    scale=10

    def __init__(self, points, convex_hull):
        self.points = points
        self.convex_hull = convex_hull
        self.draw_self=True
        self._cached_surface=None
        self.screen=None

    @staticmethod
    def _pygame_screen_setup():
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % DisplayConvexHullResults.WINDOW_POSITION
        return pygame.display.set_mode(DisplayConvexHullResults.WINDOW_SIZE, DisplayConvexHullResults.FLAGS)

    def setup(self):
        self.screen = self._pygame_screen_setup()

    def draw(self):
        if self._cached_surface is None:
            self._cached_surface=pygame.Surface(self.WINDOW_SIZE)
            self._draw(self._cached_surface)
        self.screen.blit(self._cached_surface,self.offset)

    def _draw(self,surface):
        for p in self.points:
            self.draw_point(surface,p)
        for i in range(0,len(self.convex_hull)+2):
            self.draw_line(surface, self.convex_hull[i%len(self.convex_hull)], self.convex_hull[(i+1)%len(self.convex_hull)])

    @staticmethod
    def draw_point(surface:pygame.Surface,point):
        radius=3
        scale=DisplayConvexHullResults.scale
        offset=DisplayConvexHullResults.obj_offset
        pygame.draw.circle(surface,"green",(scale*point.x+offset[0],scale*point.y+offset[1]),radius)

    @staticmethod
    def draw_line(surface: pygame.Surface, p1,p2):
        scale=DisplayConvexHullResults.scale
        offset=DisplayConvexHullResults.obj_offset
        pygame.draw.line(surface, "blue", (scale*p1.x+offset[0], scale*p1.y+offset[1]),
                         (scale*p2.x+offset[0], scale*p2.y+offset[1]),width=2)

    def exit(self):
        pygame.display.quit()
        pygame.quit()
        exit()

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