import itertools
from decimal import *

class blurRules:
    candleVal = [] #candle types. taken by class Files from config
    bodyRules = {} #bodyRules[candleVal[i]] = {} -> we'd have few bodyRules for every candle type. ihope
    shadowRules = {}#the same as body rules
    IOcandles = {'in':{},'out':{}} #input & ouput ANN candles. num
    learnArrayIn = [] #среднекрасивое решение для входов обучающей матрицы
    learnArrayOut = [] #среднекрасивое решение для выходов обучающей матрицы

    def getCandleRuleFromString(self, s):
        try:
            i = s.index(" ",0,len(s))
            candleType = s[0:i]
            s = s[i+1:len(s)]
            self.candleVal.append(candleType) #раз уж нашелся очередной свечей, то создаются все необходимые для правил словари
            self.IOcandles['in'][candleType] = {}
            self.IOcandles['out'][candleType] = {}
            self.bodyRules[candleType] = {}
            self.shadowRules[candleType] = {}
            try:
                i = s.index(" ",0,len(s))
                self.IOcandles['in'][candleType] = int(s[0:i])
                s = s[i+1:len(s)]
                try:
                    i = s.index(" ",0,len(s))
                    self.IOcandles['out'][candleType] = int(s[0:i])
                    s = s[i+1:len(s)]
                    try:
                        i = s.index("body",0,len(s))
                        j = s.index("{",0,len(s))
                        j1 = s.index("}",0,len(s))
                        bodyrules = s[j+1:j1]
                        self.parceRules(self.bodyRules[candleType],bodyrules)
                        s = s[j1 + 1:len(s)]
                        try:
                            i = s.index("shadow",0,len(s))
                            j = s.index("{",0,len(s))
                            j1 = s.index("}",0,len(s))
                            shadowrules = s[j+1:j1]
                            self.parceRules(self.shadowRules[candleType],shadowrules)
                        except Exception:
                            print ("ошибка чтения конфига. не найдены правила теней свечи в валютной паре  " + candleType)
                            return
                    except Exception:
                        print ("ошибка чтения конфига. не найдены правила тела свечи в валютной паре  " + candleType)
                        return 
                except Exception:
                    print ("ошибка чтения конфига. не найдено число выходных свечей для ANN в валютной паре (либо не отделено пробелом)  " + candleType)
                    return 
            except Exception:
                print ("ошибка чтения конфига. не найдено число входных свечей для ANN в валютной паре (либо не отделено пробелом) " + candleType)
                return 
        except Exception:
            print ("ошибка чтения конфига. не найден тип свечей (либо не отделен пробелом)" + s)
            return

    def parceRules(self, mydict, rulesSTR):
        tmp = rulesSTR.split(';')
        i = 0
        while i < len(tmp): #TODO разобраться почему работает только так
            try:
                j = tmp[i].index(':',0,len(tmp[i]))
                key = tmp[i][j + 1:len(tmp[i])]
                mydict[key] = []
                tmp[i] = tmp[i][0:j]
                if (',' in tmp[i]):
                    j = tmp[i].index(',',0,len(tmp[i]))
                    mydict[key].append(Decimal(tmp[i][1:j]))
                    mydict[key].append(Decimal(tmp[i][j + 1:len(tmp[i]) - 1]))
                else:
                    mydict[key].append(Decimal(tmp[i][1:len(tmp[i]) - 1]))
            except Exception:
                print("ошибка синтатксиса праввил свечей")
            i = i + 1

    def createLearnArray(self, sizeIn, sizeOut, dataFile, startPos = 0, count = 100):
        itertools.islice(dataFile,startPos) #on position
        c = 0
        for line in dataFile:
            c += 1 #counter
            s = line
            #print(line) ## <----- del it ;)
            try:
                j = s.index('[',0,len(s)) #at first in row
                s = s[j + 1: len(s)]
                j = s.index(']',0,len(s))
                s_in = s[0:j]
                self.getvalsFromLine(s_in)
                j = s.index('[',0,len(s)) #at secont out row
                s = s[j + 1: len(s)]
                s_out = s[0:-1]
                self.getvalsFromLine(s_out)
                #print(s_in)
                #print(s_out)
            except Exception:
                print("wrong string format " + s)
            if (c == count): return

    def getvalsFromLine(self, s):
        tmp = s.split(',')
        tmpCandle = '' #candle string temporary (shadow,body,shadow)
        i = 0
        for i in range(len(tmp)):
            tmpCandle = tmp[i][1:-1]
            print(tmpCandle)
            #print (i)
 

            

