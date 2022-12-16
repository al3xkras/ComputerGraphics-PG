from unittest import TestCase
from data_representation import *
from elementary_functions import *

class Test(TestCase):
    def test_intersection(self):
        s1=Segment(Point(0,0),Point(2,4))
        s2=Segment(Point(2,-1),Point(1,3))
        p = Intersection(
            s1,s2
        )
        self.assertIsNotNone(p)


    def test_which_side(self):
        test_segments=[
            Segment(Point(0,0),Point(0,1)),
            Segment(Point(0,0),Point(1,0)),
            Segment(Point(0,-1),Point(1,0)),
        ]
        test_points=[
            [Point(0,0),Point(-1,-1),Point(-10.4,100),Point(5,10)],
            [Point(0.5,0),Point(-1000,0),Point(10,10),Point(-0.0001,-0.1)],
            [Point(0,0),Point(-100,1000),Point(0.5,-0.5),Point(1,10)]
        ]
        test_sides=[
            [Side.NONE,Side.LEFT,Side.LEFT,Side.RIGHT],
            [Side.NONE,Side.NONE,Side.LEFT,Side.RIGHT],
            [Side.LEFT,Side.LEFT,Side.NONE,Side.LEFT]
        ]
        for i in range(len(test_segments)):
            seg=test_segments[i]
            points=test_points[i]
            sides=test_sides[i]
            for j in range(len(points)):
                p=points[j]
                s=sides[j]
                try:
                    self.assertEqual(WhichSide(seg,p),s)
                except AssertionError:
                    print(seg,p,"expected:",s)
                    print("Actual: ",WhichSide(seg,p))
                    self.fail()

