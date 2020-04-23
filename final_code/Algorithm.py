from sys import maxsize
from Genetic import Population


def Run_Algorithm(N, max_iter):
    family = Population(N)
    family.take_the_best(family.niu)
    iter = 1
    ncross = int(N/2)
    old_error = maxsize
    curr_error = maxsize
    repeat = 0
    while iter < max_iter:
        family.createChildren(family.parents, ncross)
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
        iter += 1
    print("\n\nFinal results")
    print(family.parents[0].matrix)
    print(family.parents[0].error)
    print(f"I take {iter} iterations")
