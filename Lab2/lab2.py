import math
from math import sqrt, sin, cos
import pygame.gfxdraw


class Manipulator:
    _hand_prefix = "/hand.png"
    _wrist_prefix = "/wrist.png"
    graphics_path = "./graphics/"
    arm_width=7
    hand_width=20

    def __init__(self, M, w3, w2, w1):
        self.hand = None
        self.arm2 = None
        self.arm1 = None
        self.vertices = (M, w3, w2, w1)
        self.S = tuple(
            Manipulator.distance(self.vertices[i], self.vertices[i + 1]) for i in range(len(self.vertices) - 1))
        self._scale = [1, 1, 1]
        self._rotate = [0, 0, 0, 0]
        try:
            self.loadAssets()
        except:
            pass

    def loadAssets(self):
        self.arm1 = pygame.image.load(Manipulator.graphics_path + "arm_1.png")
        self.arm2 = pygame.image.load(Manipulator.graphics_path + "arm_1.png")
        self.hand = pygame.image.load(Manipulator.graphics_path + "hand.png")

    @staticmethod
    def distance(p1, p2):
        return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    @staticmethod
    def angle(p1,p2):
        return math.atan2(p2[1]-p1[1],p2[0]-p1[0])-math.atan2(-p1[1],0)

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
        vertices = self._eval_vertices()
        pygame.draw.circle(surface,"black",vertices[0],Manipulator.arm_width*2,width=1)
        for i in range(1, len(vertices)):
            self._draw_arm(surface, vertices[i - 1], vertices[i], Manipulator.arm_width,self.arm1)

        v1=vertices[3]
        sc=[vertices[2][0]-v1[0],vertices[2][1]-v1[1]]
        sc=[-x*1.6 for x in sc]
        v2=[v1[i]+sc[i] for i in range(len(v1))]
        v2=Manipulator.rotate_around_point(v2,self._rotate[3]/180*math.pi,v1)

        self._draw_hand(surface,v1,v2,Manipulator.hand_width, self.hand)

    def _eval_vertices(self):
        return self._eval_scaled_points(self._eval_rotated_points())

    def rotate(self, vert_num, angle):
        self._rotate[vert_num] += angle
        self._rotate[vert_num] = self._rotate[vert_num] % 360

    @staticmethod
    def rotate_surface(surface, angle, pivot, offset):
        """Rotate the surface around the pivot point.
        Args:
            surface (pygame.Surface): The surface that is to be rotated.
            angle (float): Rotate by this angle.
            pivot (tuple, list, pygame.math.Vector2): The pivot point.
            offset (pygame.math.Vector2): This vector is added to the pivot.
        """
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
        rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect  # Return the rotated image and shifted rect.

    def scale(self, vert_num, coeff):
        self._scale[vert_num] = coeff

    def _eval_rotated_points(self):
        V = [x for x in self.vertices]
        for k in range(len(self._rotate)):
            r = self._rotate[k]
            for i in range(k + 1, len(V)):
                V[i] = Manipulator.rotate_around_point(V[i], r / 180 * math.pi, V[k])
        return V

    def _eval_scaled_points(self, V):
        for i in range(1, len(V)):
            vec_x = V[i][0] - V[i - 1][0]
            vec_y = V[i][1] - V[i - 1][1]
            vec_x = vec_x * self._scale[i - 1] - vec_x
            vec_y = vec_y * self._scale[i - 1] - vec_y
            for j in range(i, len(V)):
                V[j][0] += vec_x
                V[j][1] += vec_y
        return V

    def _draw_arm(self, surface: pygame.Surface, V1, V2, arm_width, arm=None,):
        if arm is None:
            pygame.draw.line(surface, "black", V1, V2)
        else:
            angle=Manipulator.angle(V1,V2)
            dist = Manipulator.distance(V1, V2)
            arm = pygame.transform.scale(arm, (arm_width, dist))
            surface.blit(*Manipulator.rotate_surface(arm, angle * 180 / math.pi,V1,pygame.math.Vector2(0,-dist/2)))

    def _draw_hand(self, surface: pygame.Surface, V, V1, hand_width, hand=None):
        if hand is None:
            pygame.draw.line(surface, "blue", V, V1)
        else:
            self._draw_arm(surface,V,V1,hand_width,hand)

    def translate(self, point):
        self.vertices = [(x[0] + point[0], x[1] + point[1]) for x in self.vertices]


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

    surf_size = (200, 200)
    m = Manipulator((0, 0), (0, 20), (0, 40), (0, 60))
    m.translate((100, 100))

    clock = pygame.time.Clock()
    i = 1
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

        s = pygame.Surface(surf_size)
        s.fill((0xff, 0xff, 0xff))
        m.rotate(0, 1)
        m.rotate(1, 2)
        m.rotate(2, 3)
        m.rotate(3, 5)
        i += 1
        i = i % 200
        m.scale(0,1.6)
        m.draw(s)
        screen.blit(pygame.transform.scale(s, WINDOW_SIZE), (0, 0))

        pygame.display.flip()
