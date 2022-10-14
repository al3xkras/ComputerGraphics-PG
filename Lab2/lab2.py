import math
from math import sqrt,sin,cos
import pygame.gfxdraw


class Manipulator:
    _hand_prefix = "/hand.png"
    _wrist_prefix = "/wrist.png"

    def __init__(self, M, w3, w2, w1):
        self.vertices = (M, w3, w2, w1)
        self.S = tuple(Manipulator.distance(self.vertices[i], self.vertices[i + 1]) for i in range(len(self.vertices) - 1))
        self._scale=[1,1,1]
        self._rotate=[0, 0, 0, 0]

    def loadAssets(self, location):
        with open(location + Manipulator._hand_prefix, "r") as f:
            pass
        with open(location + Manipulator._wrist_prefix, "r") as f:
            pass

    @staticmethod
    def distance(p1, p2):
        return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    @staticmethod
    def rotate_around_point(xy, radians, origin=(0, 0)):
        """Rotate a point around a given point.
        """
        x, y = xy
        offset_x, offset_y = origin
        adjusted_x = (x - offset_x)
        adjusted_y = (y - offset_y)
        cos_rad = cos(radians)
        sin_rad = sin(radians)
        qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
        qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
        return [qx, qy]

    def draw(self, surface: pygame.Surface):
        vertices=self._eval_vertices()
        for i in range(1,len(vertices)):
            self._draw_hand(surface,vertices[i-1],vertices[i])
        self._draw_wrist(surface,vertices[-1],0)

    def _eval_vertices(self):
        return self._eval_scaled_points(self._eval_rotated_points())

    def rotate(self, vert_num, angle):
        self._rotate[vert_num]+=angle
        self._rotate[vert_num]=self._rotate[vert_num]%360

    def scale(self,vert_num,coeff):
        self._scale[vert_num]=coeff

    def _eval_rotated_points(self):
        V=[x for x in self.vertices]
        for k in range(len(self._rotate)):
            r=self._rotate[k]
            for i in range(k+1,len(V)):
                V[i]=Manipulator.rotate_around_point(V[i],r/180*math.pi,V[k])
        return V

    def _eval_scaled_points(self,V):
        for i in range(1,len(V)):
            vec_x=V[i][0]-V[i-1][0]
            vec_y=V[i][1]-V[i-1][1]
            vec_x = vec_x*self._scale[i-1]-vec_x
            vec_y = vec_y*self._scale[i-1]-vec_y
            for j in range(i,len(V)):
                V[j][0]+=vec_x
                V[j][1]+=vec_y
        return V

    def _draw_hand(self,surface:pygame.Surface,V1,V2):
        pygame.draw.line(surface,"black",V1,V2)

    def _draw_wrist(self, surface:pygame.Surface,V, angle):
        V1 = [x+1 for x in V]
        V1=Manipulator.rotate_around_point(V1,angle/180*math.pi,V)
        pygame.draw.line(surface,"blue",V,V1)

    def translate(self, point):
        self.vertices=[(x[0]+point[0],x[1]+point[1]) for x in self.vertices]


if __name__ == '__main__':
    from pygame.locals import *
    import pygame.gfxdraw
    from math import sqrt
    from sys import exit
    import os

    pygame.init()

    WINDOW_SIZE = (600, 600)
    WINDOW_POSITION = (100, 100)

    FONT_SIZE = 24
    FONT_BOLD = False

    FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % WINDOW_POSITION

    screen = pygame.display.set_mode(WINDOW_SIZE, FLAGS)

    surf_size=(200,200)
    m = Manipulator((0,0),(0,20),(0,40),(0,60))
    m.translate((100,100))

    clock = pygame.time.Clock()
    i=1
    while True:
        clock.tick(30)
        # get events
        for event in pygame.event.get():
            # if QUIT
            if event.type == pygame.QUIT:
                # clean up
                pygame.quit()
                # bye bye
                exit()

        screen.fill((0xff, 0xff, 0xff))

        s=pygame.Surface(surf_size)
        s.fill((0xff, 0xff, 0xff))
        m.rotate(0, 3)
        m.rotate(1, -5)
        m.rotate(2, 1)
        i+=1
        i=i%200
        m.scale(2,i/60+1)
        m.scale(0,i/50+1)
        m.scale(1,i/70+1)


        m.draw(s)
        screen.blit(pygame.transform.scale(s,WINDOW_SIZE),(0,0))

        pygame.display.flip()
