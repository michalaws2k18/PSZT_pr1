import numpy as np
from numpy import random
import copy 

niu = 200  # number of parents

initialPopParameter = 50 #krotnosc wstepnego zwiekszenia poplacji poczatkowej

N = 5
length = N*N
crossRate=0.5
mutateRate=0.5
Proper_sum=N*(1+N*N)/2

def referenceFunction():
    return N*(1+N*N)/2


def error(vector):
    return abs(np.sum(vector) - Proper_sum)  #funkcja obliczająca wielkość błędu
    # if sum(vector) == referenceFunction():
    #     return 0
    # return 1


def error2Prob(a):          # funkcja zmieniająca wielkość błędu na wagę bycia wybranym
    return np.exp(-a)       # TO NALEZY USTALIC !!! od tego zależy siła selekcji


class Subject:
    def __init__(self):
        self.array = [x for x in range(1, length+1)]
        random.shuffle(self.array)
        self.updateMatrix()
        self.calculateError()

    def updateMatrix(self):
        self.matrix = np.reshape(self.array, (-1, N))

    def calculateError(self):       # obliczenie błędu danego osobnika
        suma = 0
        for x in self.matrix:
            suma += error(x)
        for x in self.matrix.transpose():
            suma += error(x)
        diag1 = []
        diag2 = []
        i = 0
        for x in self.matrix:
            diag1.append(x[i])
            diag2.append(x[N-1-i])
            i += 1
        suma += error(diag1)
        suma += error(diag2)
        self.error = suma


class Population:
    def __init__(self):
        self.parents = []
        self.children = []*niu
        for i in range(niu*initialPopParameter):
            self.parents.append(Subject())
        # self.calculate_parents_Errors()

    def update_parents_Matrix(self):
        for x in self.parents:
            x.updateMatrix()

    def update_children_Matrix(self):
        for x in self.children:
            x.updateMatrix()

    def calculate_parents_Errors(self):
        for x in self.parents:
            x.calculateError()
    
    def calculate_children_Errors(self):
        for x in self.children:
            x.calculateError()

    def createChildren(self, rodzice, cuts=2, number_of_mutations=1):  # Krzyżowanie
        children = []
        for i in range(int(niu/2)):
            male = copy.deepcopy(rodzice[2*i])
            female = copy.deepcopy(rodzice[2*i+1])
            [boy, girl] = self.mycross(male, female, cuts=cuts)
            children.append(boy)
            children.append(girl)
        self.children = children
        for i in range(number_of_mutations):
            self.mutation()

    def mycross(self, male, female, cuts = 2):
        itsBoy = copy.deepcopy(male)
        itsGirl = copy.deepcopy(female)
        allCutPlaces = np.arange(start=1, stop=length-2)
        chosenCutPlaces = list(np.random.choice(allCutPlaces, size=cuts, replace=False))
        chosenCutPlaces.append(0)
        chosenCutPlaces.append(len(male.array)-1)
        chosenCutPlaces.sort()  # domyslnie rosnąco
        for i in range(len(chosenCutPlaces)-1):
            #do_i_change = random.randint(0, 2)
            do_i_change = random.choice([0,1], size= 1,p=[1-crossRate, crossRate])
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
        bufor = copy.deepcopy(sequence[pos1])
        sequence[pos1] = copy.deepcopy(sequence[pos2])
        sequence[pos2] = bufor

    def look_for(self, sequence, value):
        for i in range(len(sequence)):
            if sequence[i] == value:
                return i

    def take_the_best(self, number):
        # self.calculateAllErrors()
        self.parents.sort(key = lambda x: x.error, reverse=False)
        return copy.deepcopy(self.parents[0:number])
    
    def take_the_best_new(self, number):
        suma = 0
        for item in self.parents:
            suma += item.error
        prop=[]
        for item in self.parents:
            prop.append(item.error/suma)
        parents = copy.deepcopy(self.parents)
        wybrancy = random.choice(parents , size=number, replace=False, p=prop) 
        return wybrancy
        
    def mutation(self):
        for item in self.children:
            #if(random.randint(0, 1) == 0):
            if (random.choice([0,1], size= 1,p=[1-mutateRate, mutateRate]) == 1):
                first_to_change = random.randint(0, len(item.array))
                second_to_change = random.randint(0, len(item.array))
                self.swap(item.array, first_to_change, second_to_change)
            else:
                pass
    
    def update_parents(self):
        for item1 in self.children:
            yes_or_not = True
            for item2 in self.parents:
                if item1.array==item2.array:
                    yes_or_not=False
                # for iter in range(len(item1.array)):
                #     if item1.array[iter]!=item2.array[iter]:
                #         yes_or_not = False
                #         break
            if yes_or_not is True:
                self.parents.append(item1)
            else:
                pass
        #self.calculateAllErrors()
    
    def minimize_parents(self, chosen):
        self.parents = chosen
