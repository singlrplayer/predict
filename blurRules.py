import itertools
from decimal import *

class blurRules:
    candleVal = [] #candle types. taken by class Files from config
    bodyRules = {} #bodyRules[candleVal[i]] = {} -> we'd have few bodyRules for every candle type. ihope
    shadowRules = {}#the same as body rules
    IOcandles = {'in':{},'out':{}} #input & ouput ANN candles. num
    learnArrayIn = [] #среднекрасивое решение для входов обучающей матрицы  : upShadow, body, DownShadow
    learnArrayOut = [] #среднекрасивое решение для выходов обучающей матрицы : upShadow, body, DownShadow

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
        UpShadowArr = []
        BodyArr = []
        DownShadowArr = []
        for i in range(len(self.learnArrayOut)):
            self.learnArrayOut.pop()
        for line in dataFile:
            s = line
            #self.learnArrayIn.append([])
            try:
                j = s.index('[',0,len(s)) #at first in row
                s = s[j + 1: len(s)]
                j = s.index(']',0,len(s))
                s_in = s[0:j]
                self.getvalsFromLine(s_in, UpShadowArr, BodyArr, DownShadowArr)
                self.learnArrayIn.append(UpShadowArr)
                self.learnArrayIn.append(BodyArr)
                self.learnArrayIn.append(DownShadowArr)
                j = s.index('[',0,len(s)) #at secont out row
                s = s[j + 1: len(s)]
                s_out = s[0:-1]
                self.getvalsFromLine(s_out, UpShadowArr, BodyArr, DownShadowArr)
                self.learnArrayOut.append(UpShadowArr)
                self.learnArrayOut.append(BodyArr)
                self.learnArrayOut.append(DownShadowArr)
            except Exception:
                print("wrong string format " + s)
            c += 1 #counter
            #if (c == count): return
        print(c)
        print("output array")
        #print(self.learnArrayOut)
        print(len(self.learnArrayOut))
        

    def getvalsFromLine(self, s, up, body, down):
        tmp = s.split(',')
        tmpCandle = '' #candle string temporary (shadow,body,shadow)
        for i in range(len(tmp)):
            tmpCandle = tmp[i][1:-1]
            try: #we have to clean row of '
                j = tmpCandle.index('\'',0,len(tmpCandle))
                tmpCandle = tmpCandle[j + 1: len(tmpCandle)]
                try: #кривая на обе ноги обработка апострофа в конце строки. надо будет обязательно сделать по-людски
                    j = tmpCandle.index('\'',0,len(tmpCandle))
                    tmpCandle = tmpCandle[0: j]
                except Exception:
                    #print("hehehe")
                    self.appendVals(tmpCandle, up, body, down)
            except Exception:
                tmpCandle = tmp[i][1:-1]
                self.appendVals(tmpCandle, up, body, down)
            #print (i)

    def appendVals(self, tmpCandle, up, body, down):
            try: #now we have to split candle values fom string to number
                #print(tmpCandle)
                j = tmpCandle.index(':',0,len(tmpCandle)) #TODO: проверить работоспособность и переписать все нахер по-нормальному. избавиться от говнокода
                t = Decimal(tmpCandle[0:j]) #upshadow
                up.append(t)
                tmpCandle = tmpCandle[j + 1:len(tmpCandle)]
                j = tmpCandle.index(':',0,len(tmpCandle)) #TODO: проверить работоспособность и переписать все нахер по-нормальному. избавиться от говнокода
                t = Decimal(tmpCandle[0:j]) #body
                body.append(t)
                tmpCandle = tmpCandle[j + 1:len(tmpCandle)]
                #print (tmpCandle)
                #j = tmpCandle.index(':',0,len(tmpCandle)) #TODO: проверить работоспособность и переписать все нахер по-нормальному. избавиться от говнокода
                t = Decimal(tmpCandle[0:j]) #downshadow
                down.append(t)
                #tmp = tmpCandle.split(':')
                """for k in range(len(tmp)):
                    try:
                        j = tmp[k].index('\'',0,len(tmp[k]))
                        tmp[k] = tmp[k][0:j] #if we have the ' -- we have it at the end. only. ever. TODO: make it more understandly ;)
                    except Exception:
                        print ("clean")"""
                    
                    
            except Exception:
                print ("exc")
        
