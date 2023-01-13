import Project4.project4 as pr4
from collections import deque
from geometry_lib.data_representation import *

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

def seg_intersection_naive(iterable, collector):
    for seg1 in iterable:
        s = iterable.__iter__()
        s.__next__()
        for seg2 in s:
            p = Intersection(seg1, seg2)
            if not p.is_definite():
                continue
            collector.add(p)


def _bentley_ottman(segments,collector,step=None,seg_range=None,sort=None):
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
        seg_intersection_naive(status,intersections)

def bentley_ottman(segments,step=None):
    intersections=set()
    seg_x_range = lambda seg: (seg.A.x, seg.B.x)
    seg_y_range = lambda seg: (seg.A.y, seg.B.y)
    sort_x = lambda seg: seg.A.x
    sort_y = lambda seg: seg.A.y
    _bentley_ottman(segments,intersections,step,seg_x_range,sort_x)
    _bentley_ottman(segments,intersections,step,seg_y_range,sort_y)
    return intersections

if __name__ == '__main__':
    from tests import Tests
    from Project5 import flat_map
    from Project5.gui import DisplaySegmentIntersections
    gen = lambda: Tests.generate_segments({
        Color.RED: 5,
        Color.BLUE: 5
    })
    method=lambda segments: bentley_ottman(segments)
    segs=gen()
    segs=flat_map(lambda a:a,segs)
    pts=bentley_ottman(segs)
    gui=DisplaySegmentIntersections(segs, pts, method=method, generator=gen)
    gui.mainloop()



