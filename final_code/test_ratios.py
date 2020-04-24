from sys import maxsize
from Genetic import Population
from random import shuffle
import time
import copy

"""
Wykonanie testów dla różnych współczynników krzyżowania i mutacji
oraz zapisanie wyników o błędzie oraz informacjach o realizacji (czas wykonania,
ilośći iteracji) w oddzoelnych plikach txt
"""
if __name__ == '__main__':
    N = 4
    max_iter = 10000
    niu_rate = 10
    initialPopParameter = 50
    crossRate = [0, 1, 0.5, 1, 1, 0.7]  # badane wartości współczynnika krzyżowania
    mutateRate = [1, 0, 0.5, 1, 0.7, 0.9]   # badane wartości współczynnika mutacji
    family = Population(N, niu_rate, initialPopParameter, crossRate[0], mutateRate[0])
    family.take_the_best(family.niu)
    error_file_name_base = f"Error_N={N}_"
    info_file_name_base = f"Info_N={N}_"
    for i in range(len(crossRate)):
        Myfamily = copy.deepcopy(family)
        Myfamily.edit_crossRate(crossRate[i])
        Myfamily.edit_mutateRate(mutateRate[i])
        error_file_name = error_file_name_base + f"Cross={Myfamily.crossRate}_Mutate={Myfamily.mutateRate}.txt"
        info_file_name = info_file_name_base + f"Cross={Myfamily.crossRate}_Mutate={Myfamily.mutateRate}.txt"
        file1 = open(error_file_name, "w")
        file1.write(f"{0};{Myfamily.parents[0].error}\n")
        print(f"Cross_rate:{Myfamily.crossRate}\t MutationRate:{Myfamily.mutateRate}")
        print("Work in progress...")
        tic = time.perf_counter()
        iter = 1
        old_error = maxsize
        curr_error = maxsize - 1
        repeat = 0
        while iter < max_iter:
            Myfamily.createChildren(Myfamily.parents, cuts=1)
            Myfamily.update_children_Matrix()
            Myfamily.calculate_children_Errors()
            Myfamily.update_parents()
            Myfamily.take_the_best(Myfamily.niu)
            file1.write(f"{iter};{Myfamily.parents[0].error}\n")
            if Myfamily.parents[0].error == 0:
                break
            old_error = curr_error
            curr_error = Myfamily.parents[0].error
            if old_error == curr_error:
                repeat += 1
                if repeat == 500:
                    Myfamily.killHalfParents()
                    repeat = 0
            else:
                repeat = 0
            shuffle(Myfamily.parents)
            iter += 1
        toc = time.perf_counter()
        file1.close()
        file2 = open(info_file_name, "w")
        file2.write(f"Iterations total: {iter}\n")
        file2.write(f"Time algorithm: {toc-tic:0.4f} seconds")
        file2.close()
        print("Final results")
        if Myfamily.parents[0].error == 0:
            print("Succes!!! Magic Square found!")
        else:
            print("Magic Square not found.\nCurrent best option:")
        print(Myfamily.parents[0].matrix)
        print(f"Iterations total: {iter}")
        print(f"Time algorithm: {toc-tic:0.4f} seconds\n\n\n\n")