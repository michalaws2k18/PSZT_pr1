from Genetic import Population
import time

if __name__ == '__main__':
    file = open('Error_function-N=8.txt', 'w')
    file2 = open('Time_info_N=8.txt', 'w')

    N = 4
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
    old_error = 1000000
    curr_error = 999999
    powtorka = 0
    maxIterations = 100000

    last_error = 0
    same_error = 1
    multi = 1
    start = time.perf_counter()
    tic = time.perf_counter()
    family = Population(N)
    ncross = int(family.N/2)
    family.take_the_best(family.niu)
    print(f"Aktualny blad = {family.parents[0].error}\n")
    toc = time.perf_counter()
    suma_0 = toc-tic

    while iter < maxIterations:
    
        tic = time.perf_counter()
        family.createChildren(family.parents, ncross)
        toc = time.perf_counter()
        suma_1 += (toc-tic)

        tic = time.perf_counter()
        family.update_children_Matrix()
        toc = time.perf_counter()
        suma_2 += (toc-tic)

        tic = time.perf_counter()
        family.calculate_children_Errors()
        toc = time.perf_counter()
        suma_3 += (toc-tic)
  
        tic = time.perf_counter()
        family.update_parents()
        toc = time.perf_counter()
        suma_4 += (toc-tic)

        tic = time.perf_counter()
        family.take_the_best(family.niu)
        toc = time.perf_counter()
        suma_6 += (toc-tic)

        tic = time.perf_counter()
        if family.parents[0].error == 0:
            break
      
        toc = time.perf_counter()
        suma_7 += (toc-tic)
        file.write(f"{iter};{family.parents[0].error}\n")
        if iter % 100 == 0:
            print(f"Po {iter} iteracjach:")
            print(f"czas wykonania createChildren() wynosi: {suma_1:0.4f} seconds")
            print(f"czas wykonania upadate_children_Matrix() wynosi: {suma_2:0.4f} seconds")
            print(f"czas wykonania calculate_children_Errors() wynosi: {suma_3:0.4f} seconds")
            print(f"czas wykonania update_parents() wynosi: {suma_4:0.4f} seconds")
            print(f"czas wykonania take_the_best({family.niu}) wynosi: {suma_6:0.4f} seconds")
            print(f"czas wykonania sprawdzenia czy najlepszy jest ostateczny wynosi: {suma_7:0.4f} seconds")
            old_error = curr_error
            curr_error = family.parents[0].error
            if old_error == curr_error:
                powtorka +=1
                if powtorka == 5:
                    family.killHalfParents()
                    print("zabilem polowe rodzicow :D")
                    powtorka = 0
            else:
                powtorka = 0
            print(f"blad wynosi: {family.parents[0].error}")
            print(f"\n\n")
        iter += 1
        
    stop = time.perf_counter()
    print(f"\n\n\n")
    print(f"Calkowity czas : {stop-start :0.4f} sec")
    print(f"W tym:")
    print(f"czas wylosowania szerszych rodzicow i wybranie {family.niu} najlepszych wynosi {suma_1:0.4f} seconds")
    print(f"czas wykonania createChildren() wynosi {suma_1:0.4f} seconds")
    print(f"czas wykonania upadate_children_Matrix() wynosi {suma_2:0.4f} seconds")
    print(f"czas wykonania calculate_children_Errors() wynosi {suma_3:0.4f} seconds")
    print(f"czas wykonania update_parents() wynosi {suma_4:0.4f} seconds")
    print(f"czas wykonania take_the_best({family.niu}) wynosi {suma_6:0.4f} seconds")
    print(f"czas wykonania sprawdzenia czy najlepszy jest ostateczny wynosi {suma_7:0.4f} seconds")
    print("Final results\n\n\n")
    print(family.parents[0].matrix)
    print(family.parents[0].error)
    print(f"zajelo to {iter} iteracji")
    file.close()

    file2.write(f"{iter};ilość iteracji\n ")
    file2.write(f"{stop-start :0.4f}; całkowity czas seconds\n")
    file2.close()
