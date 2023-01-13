
"""@package docstring
Documentation for this module.

More details.
"""
import numpy as np

"""Documentation for this class.

More details.
"""


def sum_mod256(t1,t2):
    m=256
    assert len(t1)==len(t2)
    return tuple((t1[i]+t2[i])%m for i in range(len(t1)))

class Color:
    NONE = 0
    BLUE = 1
    RED = 2
    GREEN = 3
    PURPLE = 4
    YELLOW=5
    pygame_colors={
        NONE:(255,255,255),
        BLUE:(0,0,255),
        RED:(255,0,0),
        GREEN:(0,255,0),
        PURPLE:(255,0,255),
        YELLOW:(255,255,0)
    }
    @staticmethod
    def to_pygame(c):
        if not isinstance(c,int):
            return c
        return Color.pygame_colors[c]
    @staticmethod
    def combine(c1,c2):
        if c1==c2:
            return c1
        _c1=Color.to_pygame(c1)
        _c2=Color.to_pygame(c2)
        return sum_mod256(_c1,_c2)


class Point:
    def __init__(self, x, y, color=Color.NONE):
        self.x = x
        self.y = y
        self.color = color

    def getPoint(self):
        return self.x, self.y

    def setPoint_x(self, new_value):
        self.x = new_value

    def setPoint_y(self, new_value):
        self.y = new_value

    def __str__(self) -> str:
        return "Point["+str(self.x)+" "+str(self.y)+"]"

    def __gt__(self, other):
        if self.x==other.x:
            return self.y>other.y
        return self.x>other.x
    def __lt__(self, other):
        return not self>other

    def is_definite(self):
        d={
            None,np.inf,-np.inf
        }
        return self.x not in d and self.y not in d

#enum Side
class Side:
    LEFT = -1
    RIGHT = 1
    NONE = 0

"""Documentation for this class.

More details.
"""
class Segment:
    def __init__(self, A:Point, B:Point, color=Color.NONE):
        self.A = A
        self.B = B
        self.color = color

    def get_side(self, point:Point) -> int:
        return WhichSide(self,point)

    def __str__(self) -> str:
        return "Segment["+str(self.A)+" "+str(self.B)+"]"

# important! elementary_functions module imports should be called after
# the declaration of Segment and Point classes, to avoid circular module dependencies
from geometry_lib.elementary_functions import WhichSide,Intersection,IsIntersection

"""Documentation for this class.

More details.
"""
class Direct_Segment(Segment):
    #Notice: 'beginning' stands for starting point and 'end' stands for ending one. The segment is directed from 'beginning' to 'end'
    def __init__(self, beginning:Point, end:Point):
        super().__init__(beginning,end)

    def intersects(self, other: Segment):
        return IsIntersection(self,other)


"""Documentation for this class.

More details.
"""
class Intersection_Point:
    def __init__(self, seg1:Segment, seg2:Segment, point:Point):
        self.segment1 = seg1 
        self.segment2 = seg2
        self.intersection_point = point #function from elementary_functions.py
    def get_inter_point(self):
        return self.intersection_point


"""Documentation for this class.

More details.
"""
class Seg_Point_Side:
    def __init__(self, segment:Segment, point:Point, side:Side):
        self.segment = segment
        self.point = point
        self.side = side #function from elementary_functions.py
    def get_side(self):
        return self.side


"""Documentation for this class.

More details.
"""
class Polygon:
    def __init__(self, vertices, lazyInit=False):
        self.vertices = PolygonVertexList(vertices,lazyInit=lazyInit)

    def get_vertices(self):
        return self.vertices


"""Documentation for this class.

More details.
"""
class List(list):
    # todo test

    def __init__(self,*args):
        super().__init__(*args)
        self.data=self

    def Add(self, element):
        if not(element in self.data):
            self.data.append(element)

    def Del(self, element):
        try:
            self.data.remove(element)
        except:
            print(f"{element} is not in list")

    def Find(self, element):
        if element in self.data:
            return self.data.index(element)
        else:
            return None

    def IsEmpty(self):
        return len(self.data) == 0

    def Size(self):
        return len(self.data)


"""Documentation for this class.

More details.
"""
class PointList(List):
    def __init__(self, points):
        #todo test
        assert all(isinstance(x, Point) for x in points)
        super().__init__(points)
        point_list = [x for x in points]
        self.data=point_list

"""Documentation for this class.

More details.
"""
class SegmentList(List):
    def __init__(self, segments):
        #todo test
        assert all(isinstance(x, Segment) for x in segments)
        super().__init__(segments)
        seg_list = [x for x in segments]
        self.data=seg_list

"""Documentation for this class.

More details.
"""
class PolygonVertexList(List):

    def __init__(self, points, lazyInit=False):
        #todo test
        assert all(isinstance(x, Point) for x in points)
        assert len(points)>=3
        super().__init__(points)
        point_list = [x for x in points]
        self.data=point_list
        if not lazyInit:
            assert not self.has_self_intersections()

    def has_self_intersections(self):
        #O((n**2-n)/2) = O(n**2) (naive method)
        for i in range(0,len(self.data)):
            seg=Segment(self.data[i-1],self.data[i])
            for j in range(i-2):
                s1=Segment(self[j],self[j+1])
                if Intersection(seg,s1) is not None:
                    return True
        return False


"""Documentation for this class.

More details.
"""
class PolygonList(List):
    def __init__(self, polygons):
        #todo call __init__ of the superclass (List)
        assert all(isinstance(x, Polygon) for x in polygons)
        pol_list = [x for x in polygons]
        self.data=pol_list

"""Documentation for this class.

More details.
"""
class IntersectionPointList(List):
    def __init__(self, elements):
        #todo call __init__ of the superclass (List)
        assert all(isinstance(x, Intersection_Point) for x in elements)
        elem_list = [x for x in elements]
        self.data=elem_list

"""Documentation for this class.

More details.
"""
class SegPointSideList(List):
    def __init__(self, elements):
        #todo call __init__ of the superclass (List)
        assert all(isinstance(x, Seg_Point_Side) for x in elements)
        elem_list = [x for x in elements]
        self.data=elem_list

