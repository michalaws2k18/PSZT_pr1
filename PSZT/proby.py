from Genetyczna import Population, niu, N
import time

if __name__ == '__main__':

    # print(len(family.parents))
    # family.createChildren(family.take_the_best(10))
    # for item in family.parents:
    #     print(item.array)
    # for item in (family.children):
    #     print(item.array)
    # family.update_parents()
    # print(len(family.parents))

    file = open('Error_function-N=6.txt', 'w')
    
    """
    Piersza opcja wyboru najlepszych przez sortowanie
    """
    ncross = int(N/2)+1
    number_of_mutations = 1
    iter = 1
    suma_1 = 0
    suma_2 = 0
    suma_3 = 0
    suma_4 = 0
    suma_5 = 0
    suma_6 = 0
    suma_7 = 0
    suma_8 = 0

    last_error = 0
    same_error = 1
    multi = 1
    start = time.perf_counter()
    tic = time.perf_counter()
    family = Population()
    family.parents = family.take_the_best(niu)
    print(family.parents[0].error)
    toc = time.perf_counter()
    suma_0 = toc-tic

    while iter < 3000:
        # tic=time.perf_counter()
        # chosen = family.parents
        # toc=time.perf_counter()
        # suma_1 += (toc-tic)
    
        tic=time.perf_counter()
        family.createChildren(family.parents, 1, 1)
        toc=time.perf_counter()
        suma_1 += (toc-tic)

        tic=time.perf_counter()
        family.update_children_Matrix()
        toc=time.perf_counter()
        suma_2 += (toc-tic)
        tic = time.perf_counter()
        family.calculate_children_Errors()
        toc = time.perf_counter()
        suma_3 += (toc-tic)
        # tic=time.perf_counter()
        # family.minimize_parents(family.parents)
        # toc=time.perf_counter()
        # suma_3 += (toc-tic)

        tic = time.perf_counter()
        family.update_parents()
        toc=time.perf_counter()
        suma_4 += (toc-tic)

        # tic=time.perf_counter()
        # family.updateAllMatrix()
        # toc=time.perf_counter()
        # suma_5 += (toc-tic)

        # tic=time.perf_counter()
        # family.calculateAllErrors()
        # toc=time.perf_counter()
        # suma_8+=(toc-tic)

        tic=time.perf_counter()
        #candidate = family.take_the_best(1)
        family.parents = family.take_the_best(niu)
        toc=time.perf_counter()
        suma_6 += (toc-tic)

        tic=time.perf_counter()
        if family.parents[0].error == 0:
            break
        # else:
        #     if family.parents[0].error == last_error:
        #         same_error += 1
        #     else:
        #         same_error = 1
        #         last_error=family.parents[0].error
        #         number_of_mutations = 1
        #     if(same_error %10==0):
        #         number_of_mutations += N

        toc = time.perf_counter()
        suma_7 += (toc-tic)
        file.write(f"{iter};{family.parents[0].error}\n")
        if iter % 100 == 0:
            print(f"Po {iter} iteracjach error:{family.parents[0].error}:")
            print(f"czas wykonania createChildren() wynosi {suma_1:0.4f} seconds")
            print(f"czas wykonania upadate_children_Matrix() wynosi {suma_2:0.4f} seconds")
            print(f"czas wykonania calculate_children_Errors() wynosi {suma_3:0.4f} seconds")
            print(f"czas wykonania update_parents() wynosi {suma_4:0.4f} seconds")
            print(f"czas wykonania take_the_best({niu}) wynosi {suma_6:0.4f} seconds")
            print(f"czas wykonania sprawdzenia czy najlepszy jest ostateczny wynosi {suma_7:0.4f} seconds")
            print(f"\n\n")
        iter += 1
        
    stop = time.perf_counter()
    print(f"\n\n\n")
    print(f"Calkowity czas : {stop-start :0.4f} sec")
    print(f"W tym:")
    print(f"czas wylosowania {4*niu} rodzicow i wybranie {niu} najlepszych wynosi {suma_1:0.4f} seconds")
    print(f"czas wykonania createChildren() wynosi {suma_1:0.4f} seconds")
    print(f"czas wykonania upadate_children_Matrix() wynosi {suma_2:0.4f} seconds")
    print(f"czas wykonania calculate_children_Errors() wynosi {suma_3:0.4f} seconds")
    print(f"czas wykonania update_parents() wynosi {suma_4:0.4f} seconds")
    print(f"czas wykonania take_the_best({niu}) wynosi {suma_6:0.4f} seconds")
    print(f"czas wykonania sprawdzenia czy najlepszy jest ostateczny wynosi {suma_7:0.4f} seconds")
    print("Final results\n\n\n")
    print(family.parents[0].matrix)
    print(family.parents[0].error)
    print(f"zajelo to {iter} iteracji")
    file.close()
    """
    Druga opcja z wyborem najlepszych
    """
