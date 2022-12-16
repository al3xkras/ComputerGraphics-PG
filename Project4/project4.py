from geometry_lib.data_representation import Side,Segment,WhichSide,Color
from collections import deque
from geometry_lib.io_operations import parse_file,TestOutputWriter

def _find_convex_hull_giftwrap(point_lst, sort=True):
    if sort:
        point_lst=sorted(point_lst, key=lambda p: p.x)
    left=deque()
    right=deque()
    def find_convex_side(deq:deque,point_list,side:Side):
        if side==Side.RIGHT:
            point_list.reverse()
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
    return _find_convex_hull_giftwrap(_find_convex_hull_giftwrap(_find_convex_hull_giftwrap(point_lst,sort),True),True)

if __name__ == '__main__':
    print(parse_file("./test_out.txt"))
    fname=input("Input filename: ").strip()
    data = parse_file(fname)
    section=input("Please input section to process: ").strip()
    print(data)
    points=data[section]
    ch=find_convex_hull_giftwrap(points)
    from project4_test import TestCases
    t=TestCases()
    writer=TestOutputWriter()
    t.test_giftwrap_algorithm_correctness(points, writer, section=section, info="User Input")
    writer.print_to_file(fname+"_convexhull.txt")

