from geometry_lib.io_operations import parse_file,TestOutputWriter
from geometry_lib.data_representation import Point,Side,Segment,WhichSide,Color
from time import time
from random import randint,random
from shapely.geometry import Polygon
import shapely
from project4 import find_convex_hull_giftwrap,find_convex_hull_naive

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
        _actual1=list(log(writer,method,str(method),_actual))
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
        s_name_actual = section + " CH"
        s_name_actual1 = section + " CH of the output CH"

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

if __name__ == '__main__':
    writer=TestOutputWriter()
    for i in range(10):
        section="Test %d "%(i+1)
        print(section)
        t=TestCases()
        t1=t.generate_linear(10)
        t2=t.generate_normal(100)
        t3=t.generate_linear_with_repeating_points(20)
        t4=t.generate_with_repeating_points(5)
        info=["linear","normal","linear with repeating points","repeating points"]
        #print(info[0],t.test_giftwrap_algorithm_correctness(t1,writer,section=section+info[0],info=info[0]))
        print(info[1],t.test_giftwrap_algorithm_correctness(t2,writer,section=section+info[1],info=info[1]))
        #print(info[2],t.test_giftwrap_algorithm_correctness(t3,writer,section=section+info[2],info=info[2]))
        print(info[3],t.test_giftwrap_algorithm_correctness(t4,writer,section=section+info[3],info=info[3]))
        print()
    writer.print_to_file("./test_out1.txt")