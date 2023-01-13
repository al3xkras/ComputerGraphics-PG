import os
import shutil
from geometry_lib.data_representation import *
from geometry_lib.io_operations import parse_file,TestOutputWriter
from Project4.project4 import TestCases
import webcolors

class Tests:
    test_dir="./test_data/"
    test_fname_prefix= "test_"
    test_file_ext=".txt"
    x_bound=[-1000,1000]
    y_bound=[-1000,1000]
    load_factor=0.75

    @staticmethod
    def file_name_from_test_num(num):
        return Tests.test_dir+Tests.test_fname_prefix+str(num)+Tests.test_file_ext

    @staticmethod
    def closest_colour(requested_colour):
        min_colours = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]
    @staticmethod
    def colour_name(rgb):
        try:
            return webcolors.rgb_to_name(rgb)
        except:
            return Tests.closest_colour(rgb)
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
        fname=Tests.file_name_from_test_num(test_num)
        tw.print_to_file(fname)

    @staticmethod
    def read_test_data(test_num=0):
        fname=Tests.file_name_from_test_num(test_num)
        return parse_file(fname)

    @staticmethod
    def clear_tests():
        shutil.rmtree(Tests.test_dir)
        os.mkdir(Tests.test_dir)

    @staticmethod
    def write_test_results(segments,intersection_pts,test_num):
        postf="_intersections.txt"
        fname=Tests.file_name_from_test_num(test_num)+postf
        t=TestOutputWriter()
        sec="intersections"
        t.add_section(sec)
        for x in intersection_pts:
            t.add_section_value(sec,x)

        points_by_color=dict()
        segments_by_color=dict()
        for x in intersection_pts:
            p=x.point
            if p.color in points_by_color:
                points_by_color[p.color]+=1
            else:
                points_by_color[p.color]=1
        for x in segments:
            if x.color in segments_by_color:
                segments_by_color[x.color]+=1
            else:
                segments_by_color[x.color]=1
        info="info"
        t.add_section(info)
        t.add_section_value(info,"segments count by color: ")
        format="%s: %d"
        for c in segments_by_color:
            color_name=Tests.colour_name(Color.to_pygame(c))
            val=format%(color_name,segments_by_color[c])
            t.add_section_value(info,val)

        t.add_section_value(info,"\nintersection points count by color: ")
        for c in points_by_color:
            color_name = Tests.colour_name(Color.to_pygame(c))
            val = format%(color_name, points_by_color[c])
            t.add_section_value(info, val)

        t.print_to_file(fname)


if __name__ == '__main__':
    Tests.write_test_data({
        Color.RED:20,
        Color.BLUE:40
    },test_num=1)