from geometry_lib.io_operations import parse_file,TestOutputWriter
from geometry_lib.data_representation import Point,Side,Segment,WhichSide,Color
from collections import deque
from random import randint,random
from shapely.geometry import Polygon
import shapely

def _find_convex_hull_giftwrap(point_lst, sort=True):
    if sort:
        point_lst=sorted(point_lst, key=lambda p: p.x)
    left=deque()
    right=deque()
    def find_convex_side(deq:deque,point_list,side:Side):
        if side==Side.RIGHT:
            point_list=point_list[::-1]
        deq.append(point_list[0])
        for i in range(1,len(point_list)):
            if len(deq)<2:
                deq.append(point_list[i])
                continue
            p=point_list[i]
            seg=Segment(deq[len(deq)-2],
                        deq[len(deq)-1],
                        Color.NONE)
            if WhichSide(seg,p)!=Side.RIGHT:
                deq.pop()
            deq.append(p)
    find_convex_side(left,point_lst,Side.LEFT)
    find_convex_side(right,point_lst,Side.RIGHT)
    right.pop()
    left.pop()
    for x in right:
        left.append(x)
    return left

def find_convex_hull_giftwrap(point_lst, sort=True):
    return _find_convex_hull_giftwrap(_find_convex_hull_giftwrap(_find_convex_hull_giftwrap(point_lst,sort),sort),sort)


class TestCases:
    def __init__(self):
        self.rmin,self.rmax=-10000,10000
        self.buffer=1 # error = 1/20000 ~= 0.00005

    def generate_linear(self,maxpoints):
        #All points form a line
        k_list=[random()*maxpoints for i in range(maxpoints)]
        k_list=list(set(k_list))
        rmin,rmax=self.rmin,self.rmax
        b=randint(rmin,rmax)
        #k_list[i]*P + b
        initial_point=Point(randint(rmin,rmax),randint(rmin,rmax))
        _points=[Point(initial_point.x*k_list[i]+b,
                      initial_point.y*k_list[i]+b) for i in range(len(k_list))]
        return _points


    def generate_linear_with_repeating_points(self,maxpoints,reps=None):
        #All points form a line and some points repeat
        _points=self.generate_linear(maxpoints)
        if reps is None:
            reps=len(_points)//10+1
        assert reps>0
        _rep=[]
        for _ in range(reps):
            _rep.append(_points[randint(0,len(_points)-1)])
        _points+=_rep
        return _points

    def generate_normal(self,maxpoints):
        #No repeating points and points don't form a line
        rmin,rmax=self.rmin,self.rmax
        points=set((randint(rmin,rmax),randint(rmin,rmax)) for i in range(maxpoints))
        return [Point(x[0],x[1]) for x in points]


    def generate_with_repeating_points(self,maxpoints,reps=None):
        #The test contains are at least 2 points with the same coordinates
        _points = self.generate_normal(maxpoints)
        if reps is None:
            reps = len(_points) // 10 + 1
        assert reps > 0
        _rep = []
        for _ in range(reps):
            _rep.append(_points[randint(0, len(_points) - 1)])
        _points += _rep
        return _points

    def test_giftwrap_algorithm_correctness(self,points):
        #If algo is correct:
        #The convex hull contains all points
        #Convex hull of a convex polygon is equal to the polygon

        actual=find_convex_hull_giftwrap(points)
        actual1=find_convex_hull_giftwrap(actual)
        try:
            actual=Polygon([shapely.geometry.Point(p.x,p.y) for p in actual])
            actual1=Polygon([shapely.geometry.Point(p.x,p.y) for p in actual1])
        except:
            return None,False
        print("actual",actual)
        print("convex hull of 'actual'",actual1)
        print("'actual' = convex hull of 'actual':",actual==actual1)
        buffer=self.buffer

        res=False
        try:
            res=all([actual.buffer(buffer).contains(shapely.geometry.Point(p.x,p.y)) for p in points])
        except: pass
        return actual,res


if __name__ == '__main__':
    for i in range(10):
        print("Test %d"%(i+1))
        t=TestCases()
        t1=t.generate_linear(10)
        t2=t.generate_normal(100)
        t3=t.generate_linear_with_repeating_points(20)
        t4=t.generate_with_repeating_points(5)
        print("linear",t.test_giftwrap_algorithm_correctness(t1))
        print("normal",t.test_giftwrap_algorithm_correctness(t2))
        print("linear with repeating points",t.test_giftwrap_algorithm_correctness(t3))
        print("repeating points",t.test_giftwrap_algorithm_correctness(t4))
        print()