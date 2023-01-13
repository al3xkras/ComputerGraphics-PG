"""@package docstring
Documentation for this module.

More details.
"""

from geometry_lib.data_representation import *
import re

class Title:
    def __init__(self,val:str):
        self.val=val

class FilePrintStream:
    line_end='\n'
    def __init__(self,filename):
        self.fname=filename
        self._file=None

    def open(self):
        if not self._file:
            self._file=open(self.fname,'w+')

    def write_line(self,line):
        if self._file:
            self._file.write(line+self.line_end)

    def close(self):
        if self._file:
            self._file.close()

class TestOutputWriter:
    values='values'
    intersections='intersections'
    title='title'
    info='info'
    section_end= ''
    info_expr='#%s'
    str_expr= '%s'
    title_expr='[%s]'
    delim=chr(9)
    point_expr=delim.join(["%.3f","%.3f","%s"]) #x y color
    segment_expr=delim.join(["%.3f","%.3f","%.3f","%.3f","%s"]) #x1 y1 x2 y2 color
    intersection_point_expr=delim.join(["%.3f","%.3f","%.3f","%.3f","%s","%.3f","%.3f","%.3f","%.3f","%s","%.3f","%.3f","%s"])
    seg_point_side_expr=delim.join(["%.3f","%.3f","%.3f","%.3f","%.3f","%.3f","%d"]) #x1 y1 x2 y2 x3 y3
    float_expr="%.3f"
    val_type_formats={
        Point:point_expr,
        Segment:segment_expr,
        Intersection_Point:intersection_point_expr,
        Seg_Point_Side:seg_point_side_expr,
        str:str_expr,
        float:float_expr,
        Title:title_expr
    }
    val_to_params={
        Point: lambda p:(p.x,p.y,p.color),
        Segment: lambda s:(s.A.x,s.A.y,s.B.x,s.B.y,s.color),
        Intersection_Point: lambda ip: (ip.segment1.A.x,ip.segment1.A.y,ip.segment1.B.x,ip.segment1.B.y,ip.segment1.color,
                                        ip.segment2.A.x,ip.segment2.A.y,ip.segment2.B.x,ip.segment2.B.y,ip.segment2.color,
                                        ip.intersection_point.x,ip.intersection_point.y,ip.intersection_point.color),
        Seg_Point_Side: lambda sps: (sps.segment.A.x,sps.segment.A.y,sps.segment.B.x,sps.segment.B.y,
                                     sps.point.x,sps.point.y,
                                     sps.side),
        str: lambda s: TestOutputWriter.str_expr % s,
        float: lambda f: f,
        Title: lambda tl: tl.val
    }

    def __init__(self):
        self.sections=dict()
        self.header=None

    """
    def run_intersection_test(self):
        _type=self.intersections
        _tests=self.sections[_type]
        test_results=[]
        for i in range(0,len(_tests)):
            _t=_tests[i]
            p=_t.intersection_point
            _t=_t.segment1,_t.segment2
            if len(_t)<2: break
            test_results.append([_t[0],_t[1],p,Intersection(*_t)])
        #todo complete implementation
        for _x in test_results:
            for y in _x:
                print(y)
            print()"""

    def add_section(self,section_name):
        if section_name in self.sections:
            return
        self.sections[section_name]={
            self.title:Title(section_name),
            self.values:[]
        }

    def set_section_title(self,section,title):
        self.sections[section][self.title]=Title(title)

    def add_section_value(self,section,value):
        self.sections[section][self.values].append(value)

    def remove_section_value_by_index(self,section,i):
        del self.sections[section][self.values][i]

    def remove_section_value(self,section,value):
        self.sections[section][self.values].remove(value)

    def set_section_info(self, section, info):
        self.sections[section][self.info]=info

    def set_header(self,header):
        self.header=header

    def print_to_stream(self, print_stream):
        #todo implement
        if self.header:
            print_stream.write_line(self.info_expr%self.header)
            print_stream.write_line(self.section_end)
        for s in self.sections:
            s_val=self.sections[s]
            title=s_val[self.title]
            print_stream.write_line(self.title_expr % self.val_to_params[type(title)](title))
            for val in s_val[self.values]:
                vtype=type(val)
                print_stream.write_line(
                    self.val_type_formats[vtype]
                        %(self.val_to_params[vtype](val)))

            if self.info in s_val:
                print_stream.write_line(self.info_expr%s_val[self.info])
            print_stream.write_line(self.section_end)

    def print_to_file(self, filename):
        fs=FilePrintStream(filename)
        fs.open()
        self.print_to_stream(fs)
        fs.close()

    @staticmethod
    def from_dict(sections, header=None):
        w=TestOutputWriter()
        if header:
            w.set_header(header)
        for section_name in sections:
            w.add_section(section_name)
            for val in sections[section_name]:
                w.add_section_value(section_name,val)
        return w


def pointFromLine(line, color: Color):
    line_copy = line
    list = line_copy.split(chr(9))
    return Point(float(list[0]), float(list[1]), color)


def segmentFromLine(line, color: Color):
    line_copy = line
    list = line_copy.split(chr(9))
    return Segment(Point(float(list[0]), float(list[1]), color), Point(float(list[2]), float(list[3]), color), color)


def intersectPointFromLine(line):
    line_copy = line
    list = line_copy.split(chr(9))
    seg1 = Segment(Point(float(list[0]), float(list[1]), int(list[4])),
                   Point(float(list[2]), float(list[3]), int(list[4])), int(list[4]))
    seg2 = Segment(Point(float(list[5]), float(list[6]), int(list[9])),
                   Point(float(list[7]), float(list[8]), int(list[9])), int(list[9]))
    point = Point(float(list[10]), float(list[11]), Color.NONE)
    return Intersection_Point(seg1, seg2, point)


def segPointSideFromLine(line):
    line_copy = line
    list = line_copy.split(chr(9))
    seg = Segment(Point(float(list[0]), float(list[1]), Color.NONE), Point(float(list[2]), float(list[3]), Color.NONE),
                  Color.NONE)
    point = Point(float(list[4]), float(list[5]), Color.NONE)
    if int(list[6]) == -1:
        side = Side.LEFT
    elif int(list[6]) == 1:
        side = Side.RIGHT
    else:
        side = Side.NONE
    return Seg_Point_Side(seg, point, side)


RE_SECTION_NAME = re.compile(r"\[(([a-zA-Z]+) ?([\d]*))\]\n")
"""
regex catching new sections and dividing it on 3 parts
f.e. "[points 1]\n" -> group(0) = "[points 1]\n"; group(1) = "points 1"; group(2) = "points"; group(3) = "1"
"""
RE_COMMENT = re.compile(r"\# ?([^\n]*)\n")
"""
regex catching comments and dividing it on 2 parts
f.e. "# Zestaw nr 3\n" -> group(0) = "# Zestaw nr 3\n"; group(1) = "Zestaw nr 3"
"""


def parse_file(dir_path):
    file = open(dir_path, 'r')

    section_name = ""
    sections_dictionary = {}
    start = False
    empty = True
    section_content = []
    flag = 0

    while True:
        # Get next line from file
        line = file.readline()

        # Checking if line is a new section or a comment
        match_section_name = RE_SECTION_NAME.match(line)
        match_comment = RE_COMMENT.match(line)

        # if line is empty
        # end of file is reached
        if not line:
            if start:
                sections_dictionary[section_name] = section_content
            break

        # If line is a new section
        if match_section_name:
            if empty:
                section_name = match_section_name.group(1)
                empty = False

            else:
                sections_dictionary[section_name] = section_content
                section_content = []
                section_name = match_section_name.group(1)
            start = True

            # If the section name is "info" then turn off start in order to skip adding its content to the dictionary
            if section_name == "info":
                start = False
                empty = True
            # If the section name contains "point" then set flag on 1, adding content of this section is in lines 137-147
            elif match_section_name.group(2) == "points":
                flag = 1
            # If the section name contains "segments" then set flag on 2, adding content of this section is in lines 137-147
            elif match_section_name.group(2) == "segments":
                flag = 2
            # If the section name contains "intersections" then set flag on 3, adding content of this section is in lines 137-147
            elif match_section_name.group(2) == "intersections":
                flag = 3
            # If the section name contains "polygon" then set flag on 4, adding content of this section is in lines 137-147
            elif match_section_name.group(2) == "polygon":
                flag = 4
            # If the section name contains "whichside" then set flag on 5, adding content of this section is in lines 137-147
            elif match_section_name.group(2) == "whichside":
                flag = 5
            # If the section name does not match any criterion given
            else:
                print("*********** ERROR ************\ninvalid section name")

        # Adding content of section
        elif start:
            if match_comment or line == "\n":
                pass
            else:
                color = line.rstrip()[-1]
                color=Color.parse_color(color)
                if flag == 1:
                    section_content.append(pointFromLine(line, color))
                elif flag == 2:
                    section_content.append(segmentFromLine(line, color))
                elif flag == 3:
                    section_content.append(intersectPointFromLine(line))
                elif flag == 4:
                    pass  # to implement
                elif flag == 5:
                    section_content.append(segPointSideFromLine(line))

        # Content of section "info" or empty line or comment -> pass
        else:
            pass


    file.close()
    return sections_dictionary


def test_cases():
    return parse_file("../../test_data_set/dane.txt")

# GIVE THE PATH OF FILE YOU WANT TO USE
if __name__ == '__main__':
    tests=test_cases()
    print(tests)
    t=TestOutputWriter.from_dict(test_cases())
    t.set_section_info("points 0","Additional info goes here")
    t.set_header("This is the title")
    t.print_to_file("./test_out.txt")

    t1=TestOutputWriter.from_dict(parse_file("./test_out.txt"))
    t1.print_to_file("./test_out1.txt")
    #t.run_intersection_test()
