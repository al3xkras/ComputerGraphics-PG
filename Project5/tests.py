import os
import shutil
from random import randint
from geometry_lib.data_representation import *
from geometry_lib.io_operations import parse_file,TestOutputWriter
from Project4.project4 import TestCases

class Tests:
    test_dir="./test_data/"
    test_fname_prefix= "test_"
    test_file_ext=".txt"
    x_bound=[-1000,1000]
    y_bound=[-1000,1000]
    load_factor=0.75
    
    @staticmethod
    def random_points(count=1,color=Color.RED,dist=None):
        t=TestCases()
        pts=t.generate_normal(maxpoints=count,dist=dist)
        for p in pts:
            p.color=color
        return pts

    @staticmethod
    def generate_points(kw:dict,dist=None):
        rmp=Tests.random_points
        points=[]
        for color in kw:
            count=kw[color]
            points.append(rmp(count,color,dist))
        return points

    @staticmethod
    def points_to_random_segments(pts: set):
        segments = []
        it = pts.__iter__()
        # todo remove hardcode
        count_mock = 1e4
        while True:
            if len(segments) > count_mock:
                return segments
            try:
                p1 = it.__next__()
                p2 = it.__next__()
                assert p1 != p2 and p1.color == p2.color
                segments.append(Segment(p1, p2, p1.color))
            except StopIteration:
                return segments

    @staticmethod
    def generate_segments(kw:dict,dist=None):
        #each segment contains 2 points
        kw=dict((k,kw[k]*2) for k in kw)
        #segment points: red, blue
        pts=Tests.generate_points(kw,dist)
        sg=Tests.points_to_random_segments
        return [sg(x) for x in pts]

    @staticmethod
    def write_test_data(kw,test_num=0):
        section_name= "segments"
        tw=TestOutputWriter()
        tw.add_section(section_name)
        for seg_lst in Tests.generate_segments(kw):
            for seg in seg_lst:
                tw.add_section_value(section_name,seg)
        fname=Tests.test_dir+Tests.test_fname_prefix+str(test_num)+Tests.test_file_ext
        tw.print_to_file(fname)

    @staticmethod
    def read_test_data(test_num=0):
        fname=Tests.test_dir+Tests.test_fname_prefix+str(test_num)+Tests.test_file_ext
        return parse_file(fname)

    @staticmethod
    def clear_tests():
        shutil.rmtree(Tests.test_dir)
        os.mkdir(Tests.test_dir)

if __name__ == '__main__':
    Tests.write_test_data({
        Color.RED:20,
        Color.BLUE:40
    },test_num=1)