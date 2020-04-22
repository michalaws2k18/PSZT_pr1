from Genetyczna import Population, Subject, niu
import time

if __name__ == '__main__':
    family = Population()

    """
    Piersza opcja wyboru najlepszych przez sortowanie
    """
    start = time.perf_counter()
    iter = 0
    family.updateAllMatrix()
    suma_1 = 0
    suma_2 = 0
    suma_3 = 0
    suma_4 = 0
    suma_5 = 0
    suma_6 = 0
    suma_7 = 0
    
    family.parents = family.take_the_best(niu)
    print(f"Poczatkowy blad wynosi {family.parents[0].error}")
    while iter < 3000:
        # tic=time.perf_counter()
        # chosen = family.parents
        # toc=time.perf_counter()
        # suma_1 += (toc-tic)
        
        tic=time.perf_counter()
        family.createChildren(family.parents)
        toc=time.perf_counter()
        suma_2 += (toc-tic)

        # tic=time.perf_counter()
        # family.minimize_parents(family.parents)
        # toc=time.perf_counter()
        # suma_3 += (toc-tic)

        tic=time.perf_counter()
        family.update_parents()
        toc=time.perf_counter()
        suma_4 += (toc-tic)

        tic=time.perf_counter()
        family.updateAllMatrix()
        toc=time.perf_counter()
        suma_5 += (toc-tic)

        tic=time.perf_counter()
        #candidate = family.take_the_best(1)
        family.parents = family.take_the_best(niu)
        toc=time.perf_counter()
        suma_6 += (toc-tic)

        tic=time.perf_counter()
        if family.parents[0].error == 0:
            break
        toc=time.perf_counter()
        suma_7 += (toc-tic)
        if iter % 100 == 0:
            print(f"Po {iter} iteracjach:")
            print(f"czas wykonania take_the_best({niu}) wynosi {suma_1:0.4f} seconds")
            print(f"czas wykonania createChildren wynosi {suma_2:0.4f} seconds")
            print(f"czas wykonania minimize_parents wynosi {suma_3:0.4f} seconds")
            print(f"czas wykonania update_parents() wynosi {suma_4:0.4f} seconds")
            print(f"czas wykonania upadateAllMatrix wynosi {suma_5:0.4f} seconds")
            print(f"czas wykonania take_the_best(1) wynosi {suma_6:0.4f} seconds")
            print(f"czas wykonania sprawdzenia czy najlepszy jest ostateczny wynosi {suma_7:0.4f} seconds")
            print(f"Aktualny blad wynosi {family.parents[0].error}")
            print(f"\n\n")
        iter += 1
        
    stop = time.perf_counter()
    print(f"\n\n\n")
    print(f"Całkowity czas : {stop-start :0.4f} sec")
    print(f"W tym:")
    print(f"czas wykonania take_the_best({niu}) wynosi {suma_1:0.4f} seconds")
    print(f"czas wykonania createChildren wynosi {suma_2:0.4f} seconds")
    print(f"czas wykonania minimize_parents wynosi {suma_3:0.4f} seconds")
    print(f"czas wykonania update_parents() wynosi {suma_4:0.4f} seconds")
    print(f"czas wykonania upadateAllMatrix wynosi {suma_5:0.4f} seconds")
    print(f"czas wykonania take_the_best(1) wynosi {suma_6:0.4f} seconds")
    print(f"czas wykonania sprawdzenia czy najlepszy jest ostateczny wynosi {suma_7:0.4f} seconds")
    print("Final results\n\n\n")
    print(family.parents[0].matrix)
    print(family.parents[0].error)
    print(f"zajelo to {iter} iteracji")
    """
    Druga opcja z wyborem najlepszych
    """
