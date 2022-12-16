"""@package docstring
Documentation for this module.

More details.
"""
from geometry_lib.data_representation import Segment
from geometry_lib.data_representation import Point,Side,Color
from numpy import inf,nan
infinity=inf
"""Documentation for this function.

More details.
"""
def VectorProduct(A:Point, B:Point, C:Point, D:Point):
    return (B.x - A.x)*(D.y - C.y) - (D.x - C.x)*(B.y - A.y)

def IsIntersection(seg1:Segment, seg2:Segment):
    if (seg1.A == seg1.B) and (seg2.A == seg2.B):
        if seg1.A == seg2.A:
            return True
        else:
            return False
    elif seg1.A == seg1.B:
        if IfPointIsOnSegment(seg2.A, seg2.B, seg1.A):
            return True
        else:
            return False
    elif seg2.A == seg2.B:
        if IfPointIsOnSegment(seg1.A, seg1.B, seg2.A):
            return True
        else:
            return False
    else:
        vecprod1 = VectorProduct(seg1.A, seg1.B, seg2.A, seg2.B)
        vecprod2 = VectorProduct(seg1.A, seg2.A, seg2.A, seg2.B)
        if vecprod1 == 0 and vecprod2 == 0:
            return True
        elif vecprod1 == 0:
            return False
        else:
            t = vecprod2/vecprod1
            vecprod3 = VectorProduct(seg1.A, seg2.A, seg1.A, seg1.B)
            u = vecprod3/vecprod1
            if t >= 0 and t <= 1 and u <= 1 and u >= 0:
                return True
            else:
                return False


"""Documentation for this function.

More details.
"""
def orientation(ax,ay,bx,by,cx,cy):
    # todo test
    return (bx-ax)*(cy-ay)-(cx-ax)*(by-ay)

def Orientation(A:Point, B:Point, P:Point):
    return orientation(A.x,A.y,B.x,B.y,P.x,P.y)

def BoundingBox(A:Point, B:Point, P:Point):
    # todo test
    return (P.x >= A.x and P.x <= B.x) and (P.y >= A.y and P.y <= B.y)

def IfPointIsOnSegment(A:Point, B:Point, P:Point):
    # todo test
    if not BoundingBox(A, B, P):
        return False
    elif Orientation(A, B, P) == 0:
        return True
    return False


def Intersection(seg1:Segment, seg2:Segment):
    #todo test
    if (seg1.A == seg1.B) and (seg2.A == seg2.B):
        if seg1.A == seg2.A:
            return seg1.A
        else:
            return None
    elif seg1.A == seg1.B:
        if IfPointIsOnSegment(seg2.A, seg2.B, seg1.A):
            return seg1.A
        else:
            return None
    elif seg2.A == seg2.B:
        if IfPointIsOnSegment(seg1.A, seg1.B, seg2.A):
            return seg2.A
        else:
            return None
    else:
        vecprod1 = VectorProduct(seg1.A, seg1.B, seg2.A, seg2.B)
        vecprod2 = VectorProduct(seg1.A, seg2.A, seg2.A, seg2.B)
        if vecprod1 == 0 and vecprod2 == 0:
            return Point(infinity,infinity,Color.NONE)
        elif vecprod1 == 0:
            return Point(nan,nan,Color.NONE)
        else:
            t = vecprod2/vecprod1
            vecprod3 = VectorProduct(seg1.A, seg2.A, seg1.A, seg1.B)
            u = vecprod3/vecprod1
            if t >= 0 and t <= 1 and u <= 1 and u >= 0:
                return Point(seg1.A.x + t*(seg1.B.x - seg1.A.x),
                          seg1.A.y + t*(seg1.B.y - seg1.A.y),Color.NONE)
            else:
                return Point(nan,nan,Color.NONE)


"""Documentation for this function.

More details.
"""
def WhichSide(seg:Segment, point:Point):
    aX = seg.A.x
    aY = seg.A.y
    bX = seg.B.x
    bY = seg.B.y
    cX = point.x
    cY = point.y
    value=orientation(aX,aY,bX,bY,cX,cY)
    thresh = 1e-9
    if value >= thresh:
        return Side.LEFT
    elif value <= -thresh:
        return Side.RIGHT
    return Side.NONE

def CCW(p1:Point, p2:Point, p3:Point):
    value = Orientation(p1,p2,p3)
    thresh = 1e-9
    return value <= -thresh

if __name__ == '__main__':
    pass


