import numpy as np
from numpy import random

niu = 10  # number of parents

N = 4
length = N*N


def tossACoinToYourWitcher():
    return random.randint(2)


def referenceFunction():
    return N*(1+N*N)/2


def error(vector):
    # return abs(np.sum(vector) - N*(1+N*N)/2)  #funkcja obliczająca wielkość błędu
    if sum(vector) == referenceFunction():
        return 1
    return 0


def error2Prob(a):          # funkcja zmieniająca wielkość błędu na wagę bycia wybranym
    return np.exp(a)       # TO NALEZY USTALIC !!! od tego zależy siła selekcji


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
        for i in range(niu):
            self.parents.append(Subject())
        self.calculateAllErrors()

    def calculateAllErrors(self):
        for x in self.parents:
            x.calculateError()

    def findMales(self):                # wybieramy meskich rodzicow dla dzieci, Stworzy niu Male'ów
        self.calculateAllErrors()
        probabilities = []
        prob_sum = 0
        for x in self.parents:
            prob_sum += error2Prob(x.error)
        for x in self.parents:
            probabilities.append(error2Prob(x.error)/prob_sum)

        maleVector = np.random.choice(self.parents, size=niu, p=probabilities)
        return maleVector

    # def findFemales(self, maleVector):
    #     femaleVector = []
    #     for x in maleVector:
    #         differenceMeasure = []
    #         for y in self.parents:          #bedziemy wybierać 1 partnerke dla każdego Male'a
    #             differenceMeasure.append(sum(np.absolute(x.array - y.array))
    #             weights = diff2Prob(differenceMeasure)
    #             probabilitiesOfFemale = weights/sum(weights)
    #         femaleVector.append(np.random.choice(self.parents, p=probabilitiesOfFemale))

    #     return femaleVector

    def cross(self, male, female, cuts=2):  # Krzyżuje jedną parę
        itsGirl = []
        itsBoy = []
        allCutPlaces = np.arange(start=1, stop=length)
        chosenCutPlaces = np.random.choice(allCutPlaces, size=cuts, replace=False)
        chosenCutPlaces.sort()  # domyslnie rosnąco

        for i in range(cuts):
            if i == 0:
                if tossACoinToYourWitcher == 0:
                    itsGirl += female.array[0:chosenCutPlaces[i]]
                    itsBoy += male.array[0:chosenCutPlaces[i]]
                else:
                    itsGirl += male.array[0:chosenCutPlaces[i]]
                    itsBoy += female.array[0:chosenCutPlaces[i]]
            else:
                if tossACoinToYourWitcher == 0:
                    itsGirl += female.array[chosenCutPlaces[i-1]:chosenCutPlaces[i]]
                    itsBoy += male.array[chosenCutPlaces[i-1]:chosenCutPlaces[i]]
                else:
                    itsGirl += male.array[chosenCutPlaces[i-1]:chosenCutPlaces[i]]
                    itsBoy += female.array[chosenCutPlaces[i-1]:chosenCutPlaces[i]]

        male.array = itsBoy
        female.array = itsGirl
        return [male, female]  # zwróci subjecty ze zmieszanymi rodzicami

    def createChildren(self, rodzice, cuts=2):  # Krzyżowanie
        children = []
        for i in range(int(niu/2)):
            male = rodzice[2*i]
            female = rodzice[2*i+1]
            [boy, girl] = self.mycross(male, female, cuts=cuts)
            children.append(boy)
            children.append(girl)
        self.children = children
        self.mutation()

    def mycross(self, male, female, cuts):
        itsBoy = male
        itsGirl = female
        allCutPlaces = np.arange(start=1, stop=length-2)
        chosenCutPlaces = list(np.random.choice(allCutPlaces, size=cuts, replace=False))
        chosenCutPlaces.append(0)
        chosenCutPlaces.append(len(male.array)-1)
        chosenCutPlaces.sort()  # domyslnie rosnąco
        for i in range(len(chosenCutPlaces)-1):
            do_i_change = random.randint(0, 2)
            if (do_i_change == 1):
                bufor = itsBoy.array[chosenCutPlaces[i]:chosenCutPlaces[i+1]]
                for j in range(chosenCutPlaces[i], chosenCutPlaces[i+1]):
                    self.swap(itsBoy.array, j, self.look_for(itsBoy.array, itsGirl.array[j]))
                iter = 0
                for k in range(chosenCutPlaces[i], chosenCutPlaces[i+1]):
                    self.swap(itsGirl.array, k, self.look_for(itsGirl.array, bufor[iter]))
                    iter += 1
            else:
                pass
        return [itsBoy, itsGirl]

    def swap(self, sequence, pos1, pos2):
        bufor = sequence[pos1]
        sequence[pos1] = sequence[pos2]
        sequence[pos2] = bufor

    def look_for(self, sequence, value):
        for i in range(len(sequence)):
            if sequence[i] == value:
                return i

    def take_the_best(self, number):
        self.calculateAllErrors()
        self.parents.sort(key = lambda x: x.error, reverse=True)
        return self.parents[0:number]

    def mutation(self):
        for item in self.children:
            if(random.randint(0, 2) == 1):
                first_to_change = random.randint(0, len(item.array))
                second_to_change = random.randint(0, len(item.array))
                self.swap(item.array, first_to_change, second_to_change)
            else:
                pass
            
    def update_parents(self):
        for item1 in self.children:
            yes_or_not = True
            for item2 in self.parents:
                for iter in range(len(item1.array)):
                    if item1.array[iter]!=item2.array[iter]:
                        yes_or_not = False
                        break
            if yes_or_not is False:
                self.parents.append(item1)
            else:
                pass
        self.calculateAllErrors()
    
    def minimize_parents(self, chosen):
        self.parents = chosen


# for i in rodzice:
#     print("Kolejna macierz")
#     print(i.matrix)

# #TESTOWANIE ROZNOSCI
# ziomus = subject()
# print(ziomus.array)
# ziomus.updateMatrix()
# print(ziomus.matrix)
# ziomus.calculateError()
# print("Error ziomusia to:", ziomus.error)
