import itertools
import os

class myFile:
    source = {'candlepath':'', 'logpath':'', 'pretext':'','f':False} #путь, название, и переменная исходного файла (здесь и везде: название исходного файла идентично с аббревиатурой валютной пары)
    QfilePath = {} #файлы со свечками
    Qfiles = {} #переменные файлов со свечками
    LearnfilePath = {} #файлы с обучающими цепочками
    Learniles = {} #переменные файлов с обучающими цепочками
    StatFilePath = {} #файлы статистики
    StatFiles = {} # переменные файлов статистики
    candles = ['minFile','min5File','min15File','min30File','hourFile','hour4File','dayFile','weekFile','monthFile'] #названия свечек. добавляется к названию файла

           
    def __init__(self, br, cfg = 'config.txt', currency = 'AUDJPY'):
        self.source['candlepath'] = self.source['pretext'] = currency
        try:
            f = open(cfg,'r')
            z = f.readline()
            z = z[0:len(z)-1] #некрасивое удаление знака конца строки. переделать
            self.source['candlepath'] = self.source['pretext'] = str(z)
            itertools.islice(f,1)
            for line in f:
                br.getCandleRuleFromString(line)
        except Exception:
            print ("ошибка конфига. убедитесь, что файл %s существует (и желательно не пуст).", cfg)
            self.myShutdowm()

    def getSourceLearnCandles(self, currency = 'AUDJPY'): #opens the learn files 
        path = os.getcwd()
        os.chdir(currency + 'learning')
        for i in self.candles:
            self.LearnfilePath[i] = self.source['pretext'] + currency + "_learn_" + i + ".txt" #здесь и везде: название файла строится по принцпу "валюта + "_learn_" + тип свечки + ".txt"
            try:
                self.Learniles[i] = open(self.LearnfilePath[i], 'a')
            except Exception:
                print ("ошибка открытия файл " + self.LearnfilePath[i])
                self.myShutdowm()
        os.chdir(path)
        

    def makeLearnFiles(self,currency):
        for i in self.candles:
            self.LearnfilePath[i] = self.fileCreate(self.source['pretext'] + "_learn_" + i + ".txt")
            try:
                self.Learniles[i] = open(self.LearnfilePath[i], 'a')
            except Exception:
                print ("ошибка открытия файл " + self.LearnfilePath[i])
                self.myShutdowm()
        

    def getSourceCandles(self, currency):
        path = os.getcwd()
        os.chdir(currency)
        for i in self.candles:
            self.QfilePath[i] = currency + "_" + i + ".txt"
            try:
                self.Qfiles[i] = open(self.QfilePath[i], 'r')
            except Exception:
                print("ошибка отрывания файла " + self.QfilePath[i])
                os.chdir(path)
        os.chdir(path)


    def myShutdowm(self):
        for i in self.candles:
            if(i in self.Qfiles): self.Qfiles[i].close()
            if(i in self.Learniles): self.Learniles[i].close()
            if(i in self.StatFiles): self.StatFiles[i].close()
            #self.QfilePath[i] = ''
            #self.LogfilePath[i] = ''
        #   self.source['f'].close()
        self.source['pretext'] = ''

    def dircreate(self, s,ind):
        path = os.getcwd()
        path = path + "\\" + s
        try:
            self.source[ind] = path
            os.makedirs(path)
            os.chdir(path)
        except OSError:
            if(os.path.isdir(path)):
                os.chdir(path)
                return
            print ("Создать директорию %s не удалось" % path)
        
    def takeFromCfg(self):
        try:
            f = open('config.txt','r')
            z = f.readline()
            print (z)
            z = z[0:len(z)-1] #некрасивое удаление знака конца строки. переделать
            self.source['candlepath'] = self.source['pretext'] = str(z)
            #self.dircreate(self.source['candlepath'], 'candlepath')
            return self
        except Exception:
            print ("ошибка конфига. убедитесь, что файл 'config.txt' существует (и желательно не пуст).")
            self.myShutdowm()
    
    def fileCreate(self, s):
        try:
            f = open(s,'w')
            f.close()
            return s
        except Exception:
            print ("ошибка попытки создания\перезаписи файла " + s)
            self.myShutdowm()

    def getStatFiles(self, candlefiles):
        for i in self.candles:
            try:
                self.Qfiles[i] = open(candlefiles.QfilePath[i], 'r') #теперь, когда уже все сделано, мы открываем файлы на чтение для сбора статистики значений свечей за весь период
            except Exception:
                print ("ошибка открытия файл " + candlefiles.QfilePath[i])
                self.myShutdowm()
                candlefiles.myShutdowm()
            try:
                self.StatFilePath[i] = self.fileCreate(candlefiles.source['pretext'] + "_stat_" + i + ".txt") #сюда складывать будем статистику значений
            except Exception:
                print ("создания файла статистики " + candlefiles.QfilePath[i])
                self.myShutdowm()
                candlefiles.myShutdowm()
            try:
                self.StatFiles[i] = open(self.StatFilePath[i], 'a') #и открываем на дозапись
            except Exception:
                print ("ошибка открытия файл " + self.StatFilePath[i])
                self.myShutdowm()
                candlefiles.myShutdowm()
        return self
                
        

