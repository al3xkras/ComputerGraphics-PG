from geometry_lib.data_representation import Side,Segment,WhichSide,Color
from geometry_lib.io_operations import parse_file,TestOutputWriter
from shapely.geometry import Polygon,Point
from gui import DisplayConvexHullResults

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

def main():
    print(parse_file("./test_out.txt"))
    fname = input("Input filename: ").strip()
    data = parse_file(fname)
    section = input("Please input section to process: ").strip()
    print(data)
    points = data[section]
    ch = find_convex_hull_giftwrap(points)
    from project4_test import TestCases
    t = TestCases()
    writer = TestOutputWriter()
    t.test_giftwrap_algorithm_correctness(points, writer, section=section, info="User Input")
    t.test_naive_algorithm_correctness(points, writer, section=section, info="User Input")

    writer.print_to_file(fname + "_convexhull.txt")

def sub():
    data = parse_file("./test_out.txt")
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
    data = parse_file("./test_out.txt")
    points = data['points']
    ch = find_convex_hull_giftwrap(points)
    DisplayConvexHullResults.scale=1/50
    r = DisplayConvexHullResults(points,ch)

    r.scale=1/1000
    r.mainloop()
if __name__ == '__main__':
    sub_gui()

