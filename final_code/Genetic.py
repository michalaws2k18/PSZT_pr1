import numpy as np
from numpy import random
import copy 


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
number_of_mutations = int(variables[4])


def referenceFunction(N):
    return N*(1+N*N)/2


def error(vector, proper_sum):
    return abs(np.sum(vector) - proper_sum)


class Subject:
    def __init__(self, N):
        length = N*N
        self.array = [x for x in range(1, length+1)]
        random.shuffle(self.array)
        self.updateMatrix(N)
        self.calculateError(N)

    def updateMatrix(self, N):
        self.matrix = np.reshape(self.array, (-1, N))

    def calculateError(self, N):
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
    def __init__(self, N):
        self.N = N
        self.niu = niu_rate * N
        self.parents = []
        self.children = []*(self.niu)
        for i in range(self.niu*initialPopParameter):
            self.parents.append(Subject(self.N))

    def killHalfParents(self):
        survivors = copy.deepcopy(self.parents[int(0.25*self.niu):int(0.75*self.niu)])
        self.parents = survivors
        for i in range(self.niu-len(survivors)):
            self.parents.append(Subject(self.N))
        self.parents.sort(key=lambda x: x.error, reverse=False)

    def update_parents_Matrix(self):
        for x in self.parents:
            x.updateMatrix(self.N)

    def update_children_Matrix(self):
        for x in self.children:
            x.updateMatrix(self.N)

    def calculate_parents_Errors(self):
        for x in self.parents:
            x.calculateError(self.N)

    def calculate_children_Errors(self):
        for x in self.children:
            x.calculateError(self.N)

    def createChildren(self, rodzice, cuts=2, number_of_mutations=1):  # Krzyżowanie
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
        itsBoy = copy.deepcopy(male)
        itsGirl = copy.deepcopy(female)
        allCutPlaces = np.arange(start=1, stop=self.N*self.N-2)
        chosenCutPlaces = list(np.random.choice(allCutPlaces, size=cuts, replace=False))
        chosenCutPlaces.append(0)
        chosenCutPlaces.append(len(male.array)-1)
        chosenCutPlaces.sort()
        for i in range(len(chosenCutPlaces)-1):
            do_i_change = random.choice([0, 1], size=1, p=[1-crossRate, crossRate])
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
        self.parents.sort(key=lambda x: x.error, reverse=False)
        self.parents = copy.deepcopy(self.parents[0:number])

    def mutation(self):
        for item in self.children:
            if (random.choice([0, 1], size=1, p=[1-mutateRate, mutateRate]) == 1):
                first_to_change = random.randint(0, len(item.array))
                second_to_change = random.randint(0, len(item.array))
                self.swap(item.array, first_to_change, second_to_change)
            else:
                pass

    def update_parents(self):
        for item1 in self.children:
            yes_or_not = True
            for item2 in self.parents:
                if item1.array == item2.array:
                    yes_or_not = False
            if yes_or_not:
                self.parents.append(item1)
            else:
                pass

    def minimize_parents(self, chosen):
        self.parents = chosen
