import numpy as np
from numpy import random
import copy 


def referenceFunction(N):
    return N*(1+N*N)/2


def error(vector, proper_sum):
    return abs(np.sum(vector) - proper_sum)


class Subject:

    def __init__(self, N):
        """
        Osobnik będący jednym kwadratem NxN
        Osobnik rprezentowany jest przez atybuty:
        array - wartości w kolejnych wierszach kwadratu(genotyp)
        matrix -reprezentacja macierzowa osobnika
        error - bład osobnika
        """
        length = N*N
        self.array = [x for x in range(1, length+1)]
        random.shuffle(self.array)
        self.updateMatrix(N)
        self.calculateError(N)

    def updateMatrix(self, N):
        self.matrix = np.reshape(self.array, (-1, N))

    def calculateError(self, N):
        """
        Oblicza funkcję celu (błąd ) osobnika
        """
        suma = 0
        proper_sum = referenceFunction(N)
        for x in self.matrix:
            suma += error(x, proper_sum)
        for x in self.matrix.transpose():
            suma += error(x, proper_sum)
        diag1 = []
        diag2 = []
        i = 0
        for x in self.matrix:
            diag1.append(x[i])
            diag2.append(x[N-1-i])
            i += 1
        suma += error(diag1, proper_sum)
        suma += error(diag2, proper_sum)
        self.error = suma


class Population:

    def __init__(self, N, niu_rate, initialPopParameter, crossRate, mutateRate):
        """
    Populacja i zbiór osobników, przyjmuje prametry takie jak:
    niu_rate - współczynnik rozmiaru populacji
    initialPopParameter - współczynnik wielkości początkowej populacji
    crossRate - współczynnik krzyżowania
    mutateRate - współczynnik mutacji
    Populacja reprezentowana jest przez atrybuty:
    N- rozmiar kwadrtu, osobnika
    niu - ilość wybranych rodziców , utworzonych dzieci
    crossRate - współczynnik krzyżowania
    mutateRate- współczynnik mutacji
    parents - lista wybranch rodziców
    children - lista utworzonych dzieci
    """
        self.N = N
        self.niu = niu_rate * N
        self.crossRate = crossRate
        self.mutateRate = mutateRate
        self.parents = []
        self.children = []*(self.niu)
        for i in range(self.niu*initialPopParameter):
            self.parents.append(Subject(self.N))

    def killHalfParents(self):
        """
        Zabija połowę rodziców i zastępuje ich nowymi
        """
        survivors = copy.deepcopy(self.parents[0:int(self.niu/2)])
        self.parents = survivors
        for i in range(self.niu-len(survivors)):
            self.parents.append(Subject(self.N))
        self.parents.sort(key=lambda x: x.error, reverse=False)

    def update_parents_Matrix(self):
        """
        odświeża macierzową reprezentację rodzieców
        """
        for x in self.parents:
            x.updateMatrix(self.N)

    def update_children_Matrix(self):
        """
        odświeża macierzową reprezentację dzieci
        """
        for x in self.children:
            x.updateMatrix(self.N)

    def calculate_parents_Errors(self):
        """
        odświeża błąd rodziców
        """
        for x in self.parents:
            x.calculateError(self.N)

    def calculate_children_Errors(self):
        """
        odświeża bład dzieci
        """
        for x in self.children:
            x.calculateError(self.N)

    def edit_crossRate(self, new_crossRate):
        """
        edycja współczynnika krzyżowania
        """
        self.crossRate = new_crossRate

    def edit_mutateRate(self, new_mutateRate):
        """
        edycja współczynnika mutacji
        """
        self.mutateRate = new_mutateRate

    def createChildren(self, rodzice, cuts=2, number_of_mutations=1):
        """
        tworzenie nowych dzieci
        wejście:rodzice- wybrani do krzyżowania
        """
        children = []
        for i in range(int(self.niu/2)):
            male = copy.deepcopy(rodzice[2*i])
            female = copy.deepcopy(rodzice[2*i+1])
            [boy, girl] = self.mycross(male, female, cuts=cuts)
            children.append(boy)
            children.append(girl)
        self.children = children
        for i in range(number_of_mutations):
            self.mutation()

    def mycross(self, male, female, cuts=2):
        """
        Funkcja krzyżująca dwóch oosbników
        male- pierwszy osobnik
        female - drugi osobnik
        Dodatkowo przyjmuje parametr cuts- liczbę wylosowanych
        miejsc przeciecia genotypu osobnika(reprezentowanego przez wektor)
        """
        itsBoy = copy.deepcopy(male)
        itsGirl = copy.deepcopy(female)
        allCutPlaces = np.arange(start=1, stop=self.N*self.N-2)
        chosenCutPlaces = list(np.random.choice(allCutPlaces, size=cuts, replace=False))
        chosenCutPlaces.append(0)
        chosenCutPlaces.append(len(male.array)-1)
        chosenCutPlaces.sort()
        for i in range(len(chosenCutPlaces)-2):
            do_i_change = random.choice([0, 1], size=1, p=[1-self.crossRate, self.crossRate])
            if (do_i_change == 1):
                bufor = copy.deepcopy(itsBoy.array[chosenCutPlaces[i]:chosenCutPlaces[i+1]+1])
                for j in range(chosenCutPlaces[i], chosenCutPlaces[i+1]+1):
                    self.swap(itsBoy.array, j, self.look_for(itsBoy.array, itsGirl.array[j]))
                iter = 0
                for k in range(chosenCutPlaces[i], chosenCutPlaces[i+1]+1):
                    self.swap(itsGirl.array, k, self.look_for(itsGirl.array, bufor[iter]))
                    iter += 1
            else:
                pass
        return [itsBoy, itsGirl]

    def swap(self, sequence, pos1, pos2):
        """
        Zamienia elementy pod indekami pos1 i pos2 w sequence
        """
        bufor = copy.deepcopy(sequence[pos1])
        sequence[pos1] = copy.deepcopy(sequence[pos2])
        sequence[pos2] = bufor

    def look_for(self, sequence, value):
        """
        Zwraca indeks elementu o wartości value w sequence
        """
        for i in range(len(sequence)):
            if sequence[i] == value:
                return i

    def take_the_best(self, number):
        """
        Wybiera number rodziców o najmniejszym błedzie a reszte usuwa
        """
        self.parents.sort(key=lambda x: x.error, reverse=False)
        self.parents = copy.deepcopy(self.parents[0:number])

    def mutation(self):
        """
        Mutacja polega na zamianie miejscami wartośći pod dwoma wylsosowanymi
        indeksami dla nowo utworzonych dzieci z prawdopodobieństwem równym
        współczynnikow mutacji
        """
        for item in self.children:
            if (random.choice([0, 1], size=1, p=[1-self.mutateRate, self.mutateRate]) == 1):
                first_to_change = random.randint(0, len(item.array))
                second_to_change = random.randint(0, len(item.array))
                self.swap(item.array, first_to_change, second_to_change)
            else:
                pass

    def update_parents(self):
        """
        Do listy rodziców dodaje dzieci, sprawdzając czy takie osobniki
        nie występują jeszcze w liście rodziców
        """
        for item1 in self.children:
            yes_or_not = True
            for item2 in self.parents:
                if item1.array == item2.array:
                    yes_or_not = False
            if yes_or_not:
                self.parents.append(item1)
            else:
                pass
