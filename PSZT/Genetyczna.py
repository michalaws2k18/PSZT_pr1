import sys
print(sys.version)

import numpy as np
from numpy import random

niu = 10 # number of parents
lam = 20 # number of children

N = 5
length = N*N

def error(vector):
    return abs(np.sum(vector) - N*(1+N)/2)  #funkcja obliczająca wielkość błędu

def error2Prob(a):          #funkcja zmieniająca wielkość błędu na wagę bycia wybranym
    return np.exp(-a)       #TO NALEZY USTALIC !!! od tego zależy siła selekcji

def diff2Prob(a):
    return np.exp(-a)

class subject:
    def __init__(self):
        self.array = [0] * length
        self.array = [random.randint(9) for x in self.array]
        self.updateMatrix()
        self.calculateError()

    def updateMatrix(self):
        self.matrix = np.reshape(self.array, (-1,N))

    def calculateError(self):       #obliczenie błędu danego osobnika
        suma = 0
        for x in self.matrix:
            suma += error(x)
        for x in self.matrix.transpose():
            suma += error(x)
        diag1=[]
        diag2=[]
        i=0
        for x in self.matrix:
            diag1.append(x[i])
            diag2.append(x[N-1-i])
            i += 1
        suma += error(diag1)
        suma += error(diag2)
        self.error = suma

class population:
    def __init__(self):
        self.parents = []
        self.children = [] * lam
        for i in range(niu):
            self.parents.append(subject())
        self.calculateAllErrors()
    
    def calculateAllErrors(self):
        for x in self.parents:
            x.calculateError()
    
    def findMales(self):                #wybieramy meskich rodzicow dla dzieci, Stworzy lam Male'ów
        self.calculateAllErrors()
        probabilities = []
        prob_sum=0
        for x in self.parents:
            prob_sum += error2Prob(x.error)
        for x in self.parents:
            probabilities.append(error2Prob(x.error)/prob_sum)

        maleVector = np.random.choice(self.parents, size = lam, p=probabilities)  
        return maleVector
    
    def findFemales(self, maleVector):
        femaleVector=[]
        for x in maleVector:
            differenceMeasure=[]
            for y in self.parents:          #bedziemy wybierać 1 partnerke dla każego Male'a
                differenceMeasure.append(sum(np.absolute(x.array - y.array))
                weights = diff2Prob(differenceMeasure)
                probabilitiesOfFemale = weights/sum(weights)
            femaleVector.append(np.random.choice(self.parents, p=probabilitiesOfFemale))

        return femaleVector

    def cross(self, male, female):
        itsBoy = np.rint((male.array + female.array)/2)
        return itsBoy

    def createChildren(self):  #Krzyżowanie
        children=[]

        self.children = children


family = population()


#TESTOWANIE ROZNOSCI
ziomus = subject()
print(ziomus.array)
ziomus.updateMatrix()
print(ziomus.matrix)
ziomus.rotatedMatrix()
print(ziomus.transposedMatrix)
ziomus.calculateError()
print("Error ziomusia to:", ziomus.error)