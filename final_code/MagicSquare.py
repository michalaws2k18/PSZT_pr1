from sys import argv
from Algorithm import Run_Algorithm

if __name__ == '__main__':
    if len(argv) < 3:
        raise Exception(f"too few arguments you give only {len(argv)}\
             Program requires 2 arguments: N-size of aquare and\
                  iter-max number of iteration")
    elif len(argv) > 3:
        raise Exception(f"You give too many arguments:{len(argv)}\
             Program requires 2 arguments: N-size of aquare and iter-max\
                  number of iteration")
    Run_Algorithm(int(argv[1]), int(argv[2]))
