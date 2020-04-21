from Genetyczna import Population, Subject, niu

if __name__ == '__main__':
    family = Population()
    print(family.parents[0].error)
    # print(len(family.parents))
    # family.createChildren(family.take_the_best(10))
    # for item in family.parents:
    #     print(item.array)
    # for item in (family.children):
    #     print(item.array)
    # family.update_parents()
    # print(len(family.parents))


    """
    Piersza opcja wyboru najlepszych przez sortowanie
    """
    iter = 0
    family.updateAllMatrix()
    while iter < 1000:
        chosen = family.take_the_best(niu)
        family.createChildren(chosen)
        family.minimize_parents(chosen)
        family.update_parents()
        family.updateAllMatrix()
        candidate = family.take_the_best(1)
        if candidate[0].error == 0:
            break
        iter += 1
    print("Final results\n\n\n")
    print(candidate[0].matrix)
    print(candidate[0].error)
    print(f"zajelo to {iter} iteracji")
    """
    Druga opcja z wyborem najlepszych
    """

