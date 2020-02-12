import numpy as np
from myFile import myFile
from blurRules import blurRules

from ann import ann


def nonlin(x,deriv=False):
    if(deriv==True):
          # return f(x)*(1-f(x))
        return x*(1-x)

    return 1/(1+np.exp(-x))
    
X = np.array([[0,0,1], #вход
            [0,1,1],
            [1,0,1],
            [1,1,1]])
                
y = np.array([[0,0], #выход
			[1,1],
			[1,1],
			[0,1]])

np.random.seed(1)

## exp start
#########################
linesCount = {} #количество обучающих строк на каждый тип свечи. надо будет писать количество строк в отдельный конфиг
br = blurRules()
f = myFile(br)
f.getMeSourceCandles()
for i in f.candles: 
    linesCount[i] = 3000
learnCount = {'minFile':30,'min5File':50,'min15File':70,'min30File':120,'hourFile':250,'hour4File':300,'dayFile':400,'weekFile':500,'monthFile':1000} #количество циклов обучения в пачке данных linesCount[i] для каждой свечки 
for i in f.candles:
    ######## вынести к херам это отсюда в одельное место 
    startpos = 0
    startpos = br.createLearnArray(br.IOcandles['in'][i], br.IOcandles['out'][i], f.Learniles[i], startpos, linesCount[i])
    f.LearnLogF.write(str(i) + '\n')
    print(i)
    print(len(br.learnArrayIn))
    print(len(br.learnArrayIn[0]))
    print(br.IOcandles['in'][i] * 3)
    print(br.IOcandles['out'][i] * 3)
    layer0 = np.array(br.learnArrayIn)
    print(layer0.shape)
    #MyAnn = ann(br.IOcandles['in'][i] * 3, len(br.learnArrayIn), br.IOcandles['out'][i] * 3, np.array(br.learnArrayIn)) #TODO: сделать шо, блядь, работало
    syn0 = 2*np.random.random((br.IOcandles['in'][i] * 3,len(br.learnArrayIn))) - 1 #in
    syn1 = 2*np.random.random((len(br.learnArrayIn),br.IOcandles['out'][i] * 3)) - 1 #out   
    for learncycle in range(learnCount[i]):
        if (len(br.learnArrayIn)>0):
            layer0 = np.array(br.learnArrayIn)
            #print(layer0.shape)
            layer1 = nonlin(np.dot(layer0,syn0))
            layer2 = nonlin(np.dot(layer1,syn1))
            layer2_error = np.array(br.learnArrayOut) - layer2 #common output ERR
            if (learncycle% 10) == 0:
                print ("ANN predict forex error:" + str(np.mean(np.abs(layer2_error))))
                f.LearnLogF.write(str(np.mean(np.abs(layer2_error))) + '\n')
                f.LearnLogF.write(str(layer2_error) + '\n')
            layer2_delta = layer2_error*nonlin(layer2,deriv=True)
            layer1_error = layer2_delta.dot(syn1.T)
            layer1_delta = layer1_error * nonlin(layer1,deriv=True)
            syn1 += layer1.T.dot(layer2_delta)
            syn0 += layer0.T.dot(layer1_delta)
    
    #######
    while (startpos != -1):
        for j in range(len(br.learnArrayIn)):
            br.learnArrayIn.pop()# input ANN array cleaning
            br.learnArrayOut.pop()# output ANN array cleaning
        startpos = br.createLearnArray(br.IOcandles['in'][i], br.IOcandles['out'][i], f.Learniles[i], startpos, linesCount[i])
        f.LearnLogF.write(str(i) + '\n')
        print (i)
        #MyAnn = ann(br.IOcandles['in'][i] * 3, len(br.learnArrayIn), br.IOcandles['out'][i] * 3, np.array(br.learnArrayIn)) #TODO: сделать шо, блядь, работало
        #syn0 = 2*np.random.random((br.IOcandles['in'][i] * 3,len(br.learnArrayIn))) - 1 #in
        #syn1 = 2*np.random.random((len(br.learnArrayIn),br.IOcandles['out'][i] * 3)) - 1 #out   
        for learncycle in range(learnCount[i]):
            if (len(br.learnArrayIn)>0):
                layer0 = np.array(br.learnArrayIn)
                layer1 = nonlin(np.dot(layer0,syn0))
                layer2 = nonlin(np.dot(layer1,syn1))
                layer2_error = np.array(br.learnArrayOut) - layer2 #common output ERR
                if (learncycle% 10) == 0:
                    print ("ANN predict forex error:" + str(np.mean(np.abs(layer2_error))))
                    f.LearnLogF.write(str(np.mean(np.abs(layer2_error))) + '\n')
                    f.LearnLogF.write(str(layer2_error) + '\n')
                layer2_delta = layer2_error*nonlin(layer2,deriv=True)
                layer1_error = layer2_delta.dot(syn1.T)
                layer1_delta = layer1_error * nonlin(layer1,deriv=True)
                syn1 += layer1.T.dot(layer2_delta)
                syn0 += layer0.T.dot(layer1_delta)
    """upsh = layer2[0].pop()
    bod = layer2[1].pop()
    dsh = layer2[2].pop()
    print("After learning ")"""
    f.LearnLogF.write('\n') #after every candle
    for k in range (len(br.learnArrayIn)):
        br.learnArrayIn.pop()
    for k in range (len(br.learnArrayOut)):
        br.learnArrayOut.pop()
                    

            
########################
## exp end ;)

# случайно инициализируем веса, в среднем - 0
syn0 = 2*np.random.random((3,4)) - 1
syn1 = 2*np.random.random((4,2)) - 1

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
print ("finish ;)")
