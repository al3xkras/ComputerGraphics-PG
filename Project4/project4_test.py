from geometry_lib.io_operations import TestOutputWriter
from project4 import TestCases

if __name__ == '__main__':
    writer=TestOutputWriter()
    for i in range(1):
        section="Test %d "%(i+1)
        print(section)
        t=TestCases()
        t1=t.generate_linear(10)
        t2=t.generate_normal(100)
        t3=t.generate_linear_with_repeating_points(20)
        #t4=t.generate_with_repeating_points(74)
        info=["linear","normal","linear with repeating points","repeating points"]
        #print(info[0],t.test_giftwrap_algorithm_correctness(t1,writer,section=section+info[0],info=info[0]))
        print(info[1],t.test_giftwrap_algorithm_correctness(t2,writer,section=section+info[1],info=info[1]))
        #print(info[2],t.test_giftwrap_algorithm_correctness(t3,writer,section=section+info[2],info=info[2]))
        #print(info[3],t.test_giftwrap_algorithm_correctness(t4,writer,section=section+info[3],info=info[3]))
        print()
    writer.print_to_file("./test5.txt")