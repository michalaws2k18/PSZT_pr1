from sys import maxsize
from Genetic import Population
from random import shuffle
import time

"""
Wczytanie początkowych parametrów algorytmu z pliku "config.txt"
"""
variables = []
with open("config.txt", "r") as file1:
    for line in file1:
        word = line.split()
        v = word[0].strip()
        variables.append(float(v))

niu_rate = int(variables[0])  # krotność losowanych rodziców razme niu=niu_rate*N
initialPopParameter = int(variables[1])  # krotnosc wstepnego zwiekszenia poplacji poczatkowej
crossRate = variables[2]
mutateRate = variables[3]


def Run_Algorithm(N, max_iter):
    """
    Uruchamia algorytm genetyczny dla kwadratów o rozmiarze NxN
    algorytm będzie działał do chwili znalezienia szukanego osbnika 
    lub osiągnięcia maksymalnej liczby iteracji max_iter
    """
    print("Work in progress...")
    tic = time.perf_counter()
    family = Population(N, niu_rate, initialPopParameter, crossRate, mutateRate)
    family.take_the_best(family.niu)
    iter = 1
    old_error = maxsize
    curr_error = maxsize - 1
    repeat = 0
    while iter < max_iter:
        family.createChildren(family.parents, cuts=1)
        family.update_children_Matrix()
        family.calculate_children_Errors()
        family.update_parents()
        family.take_the_best(family.niu)
        if family.parents[0].error == 0:
            break
        old_error = curr_error
        curr_error = family.parents[0].error
        if old_error == curr_error:
            repeat += 1
            if repeat == 500:
                family.killHalfParents()
                repeat = 0
        else:
            repeat = 0
        shuffle(family.parents)
        iter += 1
    toc = time.perf_counter()
    print("\n\nFinal results")
    if family.parents[0].error == 0:
        print("Succes!!! Magic Square found!")
    else:
        print("Magic Square not found.\nCurrent best option:")
    print(family.parents[0].matrix)
    print(f"Iterations total: {iter}")
    print(f"Time total: {toc-tic:0.4f} seconds")
