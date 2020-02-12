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

    def createLearnArray(self, sizeIn, sizeOut, dataFile, startPos = 0, count = 3000):
        print(sizeIn)
        itertools.islice(dataFile,startPos) #on position
        c = 0
        UpShadowArr = []
        BodyArr = []
        DownShadowArr = []
        for line in dataFile:
            s = line
            self.learnArrayIn.append([])
            self.learnArrayOut.append([])
            try:
                j = s.index('[',0,len(s)) #at first in row
                s = s[j + 1: len(s)]
                j = s.index(']',0,len(s))
                s_in = s[0:j]
                self.getvalsFromLine(s_in, UpShadowArr, BodyArr, DownShadowArr)
                for k in range(sizeIn):
                    self.learnArrayIn[c].append(UpShadowArr[k])
                    self.learnArrayIn[c].append(BodyArr[k])
                    self.learnArrayIn[c].append(DownShadowArr[k])
                #if(sizeIn < 200):print(self.learnArrayIn[c])
                j = s.index('[',0,len(s)) #at secont out row
                s = s[j + 1: len(s)]
                s_out = s[0:-1]
                self.getvalsFromLine(s_out, UpShadowArr, BodyArr, DownShadowArr)
                for k in range(sizeOut):
                    self.learnArrayOut[c].append(UpShadowArr[k])
                    self.learnArrayOut[c].append(BodyArr[k])
                    self.learnArrayOut[c].append(DownShadowArr[k])
            except Exception:
                print("wrong string format " + s)
            #print ("line Num  " + str(c))            
            c += 1 #counter
            if (c == count):
                c = c + startPos
                print(" we got count :" + str(c))
                return c #next start position
        print("lines " + str(c))
        return -1 # we got end of file
        

    def getvalsFromLine(self, s, up, body, down):
        tmp = s.split(',')
        tmpCandle = '' #candle string temporary (shadow,body,shadow)
        for i in range(len(tmp)):
            tmpCandle = tmp[i][1:-1]
            try: #we have to clean row of ' IDEA:некорорые стринги имеют апострофы только спереди, некоторые -- с обеих сторон. да, этоможно сделать изящнее. и да, я это сделаю изящнее. потом.
                j = tmpCandle.index('\'',0,len(tmpCandle))
                tmpCandle = tmpCandle[j + 1: len(tmpCandle)]
                try: #кривая на обе ноги обработка апострофа в конце строки. надо будет обязательно сделать по-людски
                    j = tmpCandle.index('\'',0,len(tmpCandle))
                    tmpCandle = tmpCandle[0: j]
                    self.appendVals(tmpCandle, up, body, down) #все апострофы убрали -- обрабатываем
                except Exception: # если сзади апостофа не нашлось -- обрабатываем 
                    self.appendVals(tmpCandle, up, body, down)
            except Exception: # если спереди апостофа не нашлось -- обрабатываем
                self.appendVals(tmpCandle, up, body, down)

    def appendVals(self, tmpCandle, up, body, down):
            try: #now we have to split candle values fom string to number
                j = tmpCandle.index(':',0,len(tmpCandle)) #TODO: проверить работоспособность и переписать все нахер по-нормальному. избавиться от говнокода
                t = float(tmpCandle[0:j]) #upshadow
                up.append(t)
                tmpCandle = tmpCandle[j + 1:len(tmpCandle)]
                j = tmpCandle.index(':',0,len(tmpCandle)) #TODO: проверить работоспособность и переписать все нахер по-нормальному. избавиться от говнокода
                t = float(tmpCandle[0:j]) #body
                body.append(t)
                tmpCandle = tmpCandle[j + 1:len(tmpCandle)]
                t = float(tmpCandle[0:j]) #downshadow
                down.append(t)
            except Exception:
                print ("exc")
        
