import numpy as np
from myFile import myFile
from blurRules import blurRules


def nonlin(x,deriv=False):
    if(deriv==True):
          # return f(x)*(1-f(x))
        return x*(1-x)

    return 1/(1+np.exp(-x))
    
X = np.array([[0,0,1], #вход
            [0,1,1],
            [1,0,1],
            [1,1,1]])
                
y = np.array([[0], #выход
			[1],
			[1],
			[0]])

np.random.seed(1)

## exp start
#########################
linesCount = {}
myIn = {}
myOut = {}
br = blurRules()
f = myFile(br)
for i in f.candles: #количество обучающий строк. надо будет писать количество строк в отдельный конфиг
    linesCount[i] = 100
for i in f.candles: ###TODO: поразмышлять на предмет определить входящие и исходящие матрицы аки набор двумерных, дабы не влезать в дебри умножения трехмерных массивов
    #массив входных обучающих данных
    myIn[i] = np.empty((linesCount[i], br.IOcandles['in'][i],3))
    myOut[i] = np.empty((linesCount[i], br.IOcandles['out'][i],3))
    # случайно инициализируем веса, в среднем - 0
    syn0 = 2*np.random.random((linesCount[i], br.IOcandles['in'][i],3)) - 1
    syn1 = 2*np.random.random((linesCount[i], br.IOcandles['out'][i],3)) - 1
    for j in range(100000):
        	# проходим вперёд по слоям 0, 1 и 2
        layer0 = myIn[i]
        layer1 = nonlin(np.dot(layer0,syn0))
        layer2 = nonlin(np.dot(layer1,syn1))
        
        layer2_error = myOut[i] - layer2 #ouput error

        layer2_delta = layer2_error*nonlin(layer2,deriv=True) #turing machine ;)
        layer1_error = layer2_delta.dot(syn1.T) #turing machine - 2 ;)
        layer1_delta = layer1_error * nonlin(layer1,deriv=True) #tm-3
        syn1 += l1.T.dot(l2_delta) #подгонка весов. почти магина тьюринга ;)
        syn0 += l0.T.dot(l1_delta)
  
########################
## exp end ;)

# случайно инициализируем веса, в среднем - 0
syn0 = 2*np.random.random((3,4)) - 1
syn1 = 2*np.random.random((4,1)) - 1

for j in range(60000):

	# проходим вперёд по слоям 0, 1 и 2
    l0 = X
    l1 = nonlin(np.dot(l0,syn0))
    l2 = nonlin(np.dot(l1,syn1))

    # как сильно мы ошиблись относительно нужной величины?
    l2_error = y - l2
    
    if (j% 10000) == 0:
        print ("Error:" + str(np.mean(np.abs(l2_error))))
        
    # в какую сторону нужно двигаться?
    # если мы были уверены в предсказании, то сильно менять его не надо
    l2_delta = l2_error*nonlin(l2,deriv=True)

    # как сильно значения l1 влияют на ошибки в l2?
    l1_error = l2_delta.dot(syn1.T)
    
    # в каком направлении нужно двигаться, чтобы прийти к l1?
    # если мы были уверены в предсказании, то сильно менять его не надо
    l1_delta = l1_error * nonlin(l1,deriv=True)

    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)
