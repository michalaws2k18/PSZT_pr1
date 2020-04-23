from Algorithm import Run_Algorithm
import time

if __name__ == '__main__':
    N=3
    max_iter = 3000
    file2 = open('Time_info_N=3.txt', 'w')
    start = time.perf_counter()
    Run_Algorithm(N, max_iter)
    stop = time.perf_counter()
    file2.write(f"{stop-start :0.4f}; całkowity czas seconds\n")
    file2.close()