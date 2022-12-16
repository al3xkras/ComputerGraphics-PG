from unittest import TestCase
from data_representation import *

fail = False
def assertThrows(test,fun):
    global fail
    fail=False
    try:
        fun()
        fail = True
    except AssertionError:
        pass
    if fail:
        test.fail()

class TestPolygonVertexList(TestCase):
    def test_has_self_intersections(self):
        def f():
            Polygon([
                Point(0, 0),
            ])
        assertThrows(self,f)
        Polygon([
            Point(0,0),Point(2,4),Point(-1,2)
        ])
        def f1():
            Polygon([
                Point(0, 0), Point(2, 4), Point(2, -1),
                Point(1,3)
            ])
        assertThrows(self,f1)
        #No exception, lazy init
        Polygon([
            Point(0, 0), Point(2, 4), Point(-1, 2),
            Point(1, 3)
        ],lazyInit=True)
        Polygon([
            Point(0, 0), Point(2, 4), Point(2, -1),
            Point(1, 0), Point(1,-3), Point(-4,2)
        ])
        def f3():
            Polygon([
                Point(0, 0), Point(2, 4), Point(2, -1),
                Point(1, 0), Point(1, -3), Point(-4, 20)
            ])
        assertThrows(self,f3)
