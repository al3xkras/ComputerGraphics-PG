
from scipy.stats import norm

from geometry_lib.data_representation import Side,Segment,WhichSide,Color
from geometry_lib.io_operations import parse_file,TestOutputWriter
from shapely.geometry import Polygon,Point
from geometry_lib.data_representation import Point as Point1
from gui import DisplayConvexHullResults
from random import random,randint
from time import time
import shapely
def find_convex_hull_naive(point_lst):
    print("[WARN] naive convex hull algorithm complicity is O(n^3)")
    chull=set()
    for p1 in point_lst:
        for p2 in point_lst:
            if p1==p2:
                continue
            sides=set()
            for p3 in point_lst:
                if p3==p1 or p3==p2:
                    continue
                seg=Segment(p1,p2,Color.NONE)
                sides.add(WhichSide(seg,p3))
            if len(sides)==1 or (len(sides)==2 and Side.NONE in sides):
                chull.add(p1)
                chull.add(p2)
    return sorted(list(chull))

#0: Collinear points
#1: Clockwise angle
#2: Counterclockwise angle
def orientation(p, q, r):
  val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
  if val == 0:
      return 0
  elif val > 0:
      return 1
  return 2

def find_convex_hull_giftwrap(points):
  points=sorted(list(set(points)))
  result = [points[0]]
  current_point = 0
  while True:
    next_point = (current_point + 1) % len(points)
    for i in range(len(points)):
        if orientation(points[current_point], points[i], points[next_point]) == 2:
            next_point = i
    current_point = next_point
    if current_point == 0:
      break
    result.append(points[current_point])
  return result

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
        initial_point=Point1(randint(rmin,rmax),randint(rmin,rmax))
        _points=[Point1(initial_point.x*k_list[i]+b,
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
    @staticmethod
    def _rand(a,b):
        return norm.rvs(loc=b-a,scale=b)
    def generate_normal(self,maxpoints, dist=None):
        if dist is None:
            dist=(TestCases._rand,TestCases._rand)
        #No repeating points and points don't form a line
        rmin,rmax=self.rmin,self.rmax
        points=set((dist[0](rmin,rmax),dist[1](rmin,rmax)) for i in range(maxpoints))
        return [Point1(x[0],x[1]) for x in points]


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

    @staticmethod
    def log_exec_time(writer:TestOutputWriter,fun,section,*args,**kwargs):
        delta=time()
        res=fun(*args,**kwargs)
        delta=time()-delta
        exec_time_postfix=" execution time"
        section+=exec_time_postfix
        writer.add_section(section)
        writer.add_section_value(section,delta)
        return res

    def test_algorithm_correctness(self, points, writer:TestOutputWriter, section="test", info="",method=find_convex_hull_giftwrap,
                                   log_exec_time=True):
        #If algo is correct:
        #The convex hull contains all points
        #Convex hull of a convex polygon is equal to the polygon
        if log_exec_time:
            log=TestCases.log_exec_time
        else:
            log=lambda _,fun,__,args: fun(*args)

        _actual=list(log(writer,method,str(method),points))
        _actual1=list(method(_actual))
        section+=str(method)
        try:
            actual=Polygon([shapely.geometry.Point(p.x,p.y) for p in _actual])
            actual1=Polygon([shapely.geometry.Point(p.x,p.y) for p in _actual1])
        except:
            return None,False
        print("actual",actual)
        print("convex hull of 'actual'",actual1)
        print("'actual' = convex hull of 'actual':",actual==actual1)
        buffer=self.buffer
        s_name_input=section+" input data"
        s_name_actual = section + " convex hull"
        s_name_actual1 = section + " convex hull of the output convex hull"

        writer.add_section(section)
        writer.set_section_info(section,info)
        writer.add_section(s_name_input)
        for p in points:
            writer.add_section_value(s_name_input,p)
        writer.set_section_info(s_name_input,"Input points")
        writer.add_section(s_name_actual)
        writer.add_section(s_name_actual1)
        for i in range(len(_actual)):
            val=_actual[i]
            writer.add_section_value(s_name_actual,val)
        for i in range(len(_actual1)):
            val1=_actual1[i]
            writer.add_section_value(s_name_actual1,val1)
            writer.set_section_info(s_name_actual1,"must be equal to '%s' for non-linear cases"%s_name_actual)

        res=False
        try:
            res=all([actual.buffer(buffer).contains(shapely.geometry.Point(p.x,p.y)) for p in points])
        except: pass
        return actual,res

    def test_giftwrap_algorithm_correctness(self, points, writer: TestOutputWriter, section="test", info=""):
        self.test_algorithm_correctness(points, writer, section, info,method=find_convex_hull_giftwrap)
    def test_naive_algorithm_correctness(self, points, writer:TestOutputWriter, section="test", info=""):
        self.test_algorithm_correctness(points, writer, section, info,method=find_convex_hull_naive)


def main():
    def_fname="./test_data/test5.txt"
    def_section="points"
    fname = input("Input filename: ").strip()
    fname = fname if fname else def_fname
    data = parse_file(fname)
    section = input("Please input section to process: ").strip()
    section=section if section else def_section
    print(data)
    points = data[section]
    ch = find_convex_hull_giftwrap(points)
    ch1 = find_convex_hull_naive(points)
    t = TestCases()
    writer = TestOutputWriter()

    dta = "data"
    writer.add_section(dta)

    writer.add_section_value(dta, "points count: %d" % len(points))
    writer.add_section_value(dta, "naive algorithm: convex hull points count: %d" % len(ch1))
    writer.add_section_value(dta, "giftwrap algorithm: convex hull points count: %d" % len(ch))

    t.test_giftwrap_algorithm_correctness(points, writer, section=section, info="User Input")
    t.test_naive_algorithm_correctness(points, writer, section=section, info="User Input")

    writer.print_to_file(fname + "_convexhull.txt")

def sub():
    data = parse_file("./test_data/test1.txt")
    points = data['points']
    for x in find_convex_hull_naive(points):
      print(x)
    print()
    ch = find_convex_hull_giftwrap(points)
    for x in ch:
        print(x)
    ch = Polygon([Point(s.x, s.y) for s in points]).convex_hull
    print(ch)

def sub_gui():
    from scipy.stats import expon,norm
    #data = parse_file("./test_out.txt")
    #points = data['points']
    t=TestCases()
    points=t.generate_normal(5000)
    #points=parse_file("./test_data/test5.txt")['points']
    ch = find_convex_hull_giftwrap(points)
    d1=lambda a,b: expon.rvs(loc=b-a,scale=b)
    d2=lambda a,b: norm.rvs(loc=b-a,scale=b)
    gen=lambda: t.generate_normal(1000,dist=(d1,d2))
    r = DisplayConvexHullResults(points,ch,method=find_convex_hull_giftwrap,generator=gen)
    r.mainloop()
if __name__ == '__main__':
    action="gui" #input("Choose action (test/gui): ").strip().lower()
    if action=="test":
        main()
    elif action=="gui":
        sub_gui()
    else:
        t=TestCases()
        points=t.generate_normal(100000)
        tm=time()
        find_convex_hull_giftwrap(points)
        delta=time()-tm
        print(delta)

