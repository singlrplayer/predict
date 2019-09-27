import numpy as np
from myFile import myFile
from blurRules import blurRules

class ann:
    a = 0 # br.IOcandles['in'][i] * number_of_candle_properties (here we have 3pcs: shadow,body,shadow)
    b = 0 # len(br.learnArrayIn) --> matrix[learinig_lines x count_learning_candle_properties]
    c = 0 # IOcandles['out'][i] * number_of_candle_properties
    layers = 0 #количество слоёв сети
    layer = [] #сами слои
    syn = [] #синапсы
    layer_err = [] #ошибки
    layer_delta = [] #первая производная по ошибкам 

    def nonlin(x,deriv=False): #коррекция весов
        if(deriv==True):return x*(1-x)
        return 1/(1+np.exp(-x))

    def __init__(self, a,b,c,x): #пока так. трехслойная сеть(включая вход и выход) потом сделается универсальный конструктор на любое количество слоёв
        self.a = a; self.b = b; self.c = c
        self.syn.append(2*np.random.random((a,b)) - 1) #in
        self.syn.append(2*np.random.random((b,c)) - 1) #out
        self.layer.append(x) #то, что у нас на входе
        self.layer.append(self.nonlin(np.dot(self.layer[0],self.syn[0]))) #скрытый слой (можно долго и нудно рассуждать на тему его необходимости и значимости для текущей задачи, но я решила, шо он таки нужен)
        self.layer.append(self.nonlin(np.dot(self.layer[1],self.syn[1]))) #то, что получается на выходе
        for i in range (2):
            self.layer_err.append([])
            self.layer_delta.append([])

    def leancycle(self, count, check, x, y): #пока так. трехслойная сеть(включая вход и выход) потом сделается универсальная обучалка на любое количество слоёв
        for i in range(count):
            self.layer[0] = x
            self.layer[1] = self.nonlin(np.dot(self.layer[0],self.syn[0]))
            self.layer[2] = self.nonlin(np.dot(self.layer[1],self.syn[1]))
            self.layer_err[2] = np.array(y) - layer[2] #common output ERR
            if(i % check) == 0: #выводим промежуточный результат ошибки (пожалуй, это следует складывать в отдельный лог)
                #print("ANN predict forex error:" + str(np.mean(np.abs(self.layer_err[2]))))
                print("ANN predict forex error:" + str(self.layer_err[2]))
            self.layer_delta[2] = self.layer_err[2] * nonlin(self.layer[2],deriv=True) #Turing machine part
            self.layer_err[1] = self.layer_delta[2].dot(self.syn[1].T) #Turing machine part
            self.layer_delta[1] = self.layer_err[1] * nonlin(self.layer[1],deriv=True) #Turing machine part
            self.syn[1] += self.layer[1].T.dot(self.layer_delta[2]) #Turing machine part
            self.syn[0] += self.layer[0].T.dot(self.layer_delta[1]) #Turing machine part

    def writeSyn(self, f, f1):
        np.savetxt(f, self.syn[0])
        np.savetxt(f1, self.syn[1])

    def getSyn(self, f, f1):
        self.syn[0] = numpy.loadtxt(f).reshape((self.a, self.b))
        self.syn[1] = numpy.loadtxt(f1).reshape((self.b, self.c))


                

