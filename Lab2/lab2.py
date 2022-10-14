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
        pass

    def _eval_vertices(self):
        return self._eval_rotated_points()

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
        #todo test
        for i in range(1,len(V)):
            vec_x=V[i][0]-V[i-1][0]
            vec_y=V[i][1]-V[i-1][1]
            vec_x *= self._scale[i-1]
            vec_y *= self._scale[i-1]
            for j in range(i,len(V)):
                V[j][0]+=vec_x
                V[j][1]+=vec_y
        return V

    def _draw_hand(self,V1,V2):
        pass

    def _draw_wrist(self, V, angle):
        pass

if __name__ == '__main__':
    m = Manipulator((0,0),(0,2),(0,4),(0,6))
    m.rotate(0,90)
    m.rotate(1,-90)
    m.rotate(2,60)
    print(m._eval_vertices())

    m = Manipulator((0,0),(0,2),(0,4),(0,6))
    m.scale(0,2)
    print(m._eval_scaled_points(m._eval_rotated_points()))
