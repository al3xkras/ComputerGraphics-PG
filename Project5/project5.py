from collections import deque
from geometry_lib.data_representation import *
from tests import Tests

def seg_sort(seg_lst, sort):
    return sorted(seg_lst, key=sort)

def segments_intersection(s1,s2):
    if isinstance(s1,Segment) and isinstance(s2,Segment):
        p=Intersection(s1,s2)
        if not p.is_definite():
            return None
        return p
    else:
        #todo implement
        raise Exception

def seg_intersection_naive(iterable, collector, intersection_point_collector=None):
    ipc=intersection_point_collector
    for seg1 in iterable:
        s = iterable.__iter__()
        s.__next__()
        for seg2 in s:
            p = Intersection(seg1, seg2)
            if p is None or not p.is_definite():
                continue
            c=Color.combine(seg1.color,seg2.color)
            p.color=c
            if ipc is not None and not p in collector:
                ipc.add(Intersection_Point(seg1,seg2,p))
            collector.add(p)

def _bentley_ottman(segments,collector,step=None,seg_range=None,sort=None,intersection_point_collector=None):
    #O(n*log(n))
    intersections=collector
    seg_sorted=seg_sort(segments,sort)
    i=0
    status=deque()
    status_min,status_max=seg_range(seg_sorted[0])[0],seg_range(seg_sorted[len(seg_sorted)-1])[1]

    if step is None:
        step=abs(status_max-status_min)/1000
    for status_point in np.arange(status_min,status_max,step):
        if i>=len(seg_sorted):
            break
        status.clear()
        rng=seg_range(seg_sorted[i])
        while i<len(seg_sorted) and rng[0]<=status_point<=rng[1]:
            status.append(seg_sorted[i])
            i+=1
        if len(status)==0:
            continue
        seg_intersection_naive(status,intersections,intersection_point_collector)

def bentley_ottman(segments, step=None, intersection_point_collector=None):
    ipc=intersection_point_collector
    intersections=set()
    seg_x_range = lambda seg: (seg.A.x, seg.B.x)
    seg_y_range = lambda seg: (seg.A.y, seg.B.y)
    sort_x = lambda seg: seg.A.x
    sort_y = lambda seg: seg.A.y
    _bentley_ottman(segments,intersections,step,seg_x_range,sort_x,intersection_point_collector=ipc)
    _bentley_ottman(segments,intersections,step,seg_y_range,sort_y,intersection_point_collector=ipc)
    return intersections

def main():
    from Project5 import flat_map
    from Project5.gui import DisplaySegmentIntersections
    inp = True
    write_test_res=False
    if inp:
        generate = input("generate data and write to file? (y/n): ").lower()[:1]
        generate = len(generate) != 0 and generate[0] == 'y'
        postf=input("Path postfix")
        test_num = input("test number: ")
        test_num = None if len(test_num) == 0 else int(test_num)
        write_test_res = input("write test results to file? (y/n): ").lower()[:1]
        write_test_res = len(write_test_res) != 0 and write_test_res[0] == 'y'
    else:
        generate = False
        test_num = None
    data_def = {
        Color.RED: 73,
        Color.BLUE: 44
    }
    data_def1 = {
        Color.RED: 5,
        Color.BLUE: 5,
        Color.generic_from_tuple((0, 255, 0)): 5,
        Color.generic_from_tuple((12,54,2)):10,
        Color.generic_from_tuple((4,100,125)):15
    }
    data_def=data_def1
    from scipy.stats import norm, expon, uniform
    # X coordinate - exponentially distributed
    d_uni = lambda a, b: uniform.rvs(loc=0, scale=10000)
    d_exp = lambda a, b: expon.rvs(loc=b - a, scale=b)
    # Y coordinate: normally distributed
    d_norm = lambda a, b: norm.rvs(loc=b - a, scale=b)
    dist = (d_uni, d_uni)

    gen = lambda: flat_map(lambda _: _, Tests.generate_segments(data_def, dist=dist))
    IntersectionPts = type('IntersectionPts', (object,), {
        "write_test_res":write_test_res,
        "data":set(),
        "add":lambda self,obj: self.data.add(obj) if self.write_test_res else None
    })
    intersection_points=IntersectionPts()

    method = lambda segments: bentley_ottman(segments,intersection_point_collector=intersection_points)

    if generate:
        Tests.write_test_data(data_def, test_num=test_num)
    if test_num is not None:
        segs = read_test_segments(test_num,path_postf=postf)
    else:
        segs = gen()
    pts = method(segs)
    if write_test_res:
        if test_num is None:
            test_num=-1
        intersection_points=intersection_points.data
        Tests.write_test_results(segs,intersection_points,test_num)
    gui = DisplaySegmentIntersections(segs, pts, method=method, generator=gen)
    gui.mainloop()

def read_test_segments(test_num=0, path_postf=""):
    return Tests.read_test_data(test_num,path_postf)["segments"]

if __name__ == '__main__':
    main()



