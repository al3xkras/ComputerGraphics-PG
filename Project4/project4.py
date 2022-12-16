from geometry_lib.io_operations import parse_file,TestOutputWriter
from geometry_lib.data_representation import Point,Side,Segment,WhichSide,Color
from collections import deque

def find_convex_full_giftwrap(point_lst, sort=False):
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
    left.pop()
    right.pop()
    for x in right:
        left.append(x)
    return left




if __name__ == '__main__':
    points=[
        Point(0,0),
        Point(0,1),
        Point(20,-1),
        Point(-2,-1),
        Point(5,-1),
    ]
    ch=find_convex_full_giftwrap(points)
    s=Segment(Point(-2,-1),Point(0,0),Color.NONE)
    for x in ch:
        print(x)
    print(WhichSide(s,Point(5,-1)))