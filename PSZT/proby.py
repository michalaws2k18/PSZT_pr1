from Genetyczna import Population, Subject

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
    # candidate = family.take_the_best(1)
    while iter < 10000:
        chosen = family.take_the_best(20)
        family.createChildren(chosen)
        family.minimize_parents(chosen)
        family.update_parents()
        candidate = family.take_the_best(1)
        if candidate[0].error <= 2:
            break
        iter += 1
    print("Final results\n\n\n")
    candidate[0].updateMatrix
    print(candidate[0].matrix)
    print(candidate[0].error)
    print(f"zajelo to {iter} iteracji")
    """
    Druga opcja z wyborem najlepszych
    """
    # iter = 0
    # candidate = family.take_the_best(1)
    # while iter < 100:
    #     family.createChildren(family.findMales())
    #     chosen = family.take_the_best(20)
    #     family.minimize_parents(chosen)
    #     family.update_parents()
    #     candidate = family.take_the_best(1)
    #     if candidate[0].error == 0:
    #         break
    #     iter += 1
    # print("Final results\n\n\n")
    # candidate[0].updateMatrix
    # print(candidate[0].matrix)
    # print(candidate[0].error)
    # print(f"zajelo to {iter} iteracji")


    # for i in family.children:
    #     print("Kolejna macierz")
    #     print(i.matrix)
    # rodzice = family.findMales()
    # moje proby

    # macierz = Subject()
    # print(type(macierz.array))
    # print("\n\n\n")
    # print(macierz.matrix)
    # print(macierz.array)
    # print(macierz.error)
    # for i in range(1):
    #     print(i)
