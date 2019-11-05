import time, json
from collections import OrderedDict as od

class kormerDict:
    def __init__(self):
        self._1mer_ = {}
        self._2mer_ = {}
        self._3mer_ = {}

    def getData(self,fname):
        self.fname = fname
        with open(self.fname, "r") as rf :
            self._udict_ = json.load(rf)
        self.kl = list(self._udict_.keys())

    def dict1Mer(self):
        for word in self.kl :
            for chr in word:
                if chr not in self._1mer_ :
                    self._1mer_ [chr]=1
                else :
                    self._1mer_ [chr]+=1

    def dict2Mer(self):
        for word in self.kl :
            word = "_"+word+"_"
            for i in range(len(word)):
                e = i+1
                if e > len(word)-1:
                    break
                else :
                    if word[i:e+1] not in self._2mer_ :
                        self._2mer_ [word[i:e+1]]=1
                    else :
                        self._2mer_ [word[i:e+1]]+=1

    def dict3Mer(self):
        for word in self.kl :
            word = "_"+word+"_"
            for i in range(len(word)):
                e = i+2
                if e > len(word)-1:
                    break
                else :
                    if word[i:e+1] not in self._3mer_ :
                        self._3mer_ [word[i:e+1]]=1
                    else :
                        self._3mer_ [word[i:e+1]]+=1

    def colDict(self, dicName):
        self._1mer_ = dict(od(sorted(self._1mer_.items(), key=lambda t: t[0])))
        self._2mer_ = dict(od(sorted(self._2mer_.items(), key=lambda t: t[0])))
        self._3mer_ = dict(od(sorted(self._3mer_.items(), key=lambda t: t[0])))
        with open("Joongang"+ dicName + "Py.json", "a", encoding="utf-8") as jwf:
            if dicName == "1merDic":
                print("1merDic 제시어 수 :", len(self._1mer_))
                jwf.write(json.dumps(self._1mer_))

            elif dicName == "2merDic":
                print("2merDic 제시어 수 :", len(self._2mer_))
                jwf.write(json.dumps(self._2mer_))

            elif dicName == "3merDic":
                print("3merDic 제시어 수 :", len(self._3mer_))
                jwf.write(json.dumps(self._3mer_))

        with open("Joongang"+ dicName + ".txt", "a", encoding="utf-8") as twf:
            if dicName == "1merDic":
                for k, v in self._1mer_.items():
                    twf.write(f"{k:>1s} {v:<6d}\n")

            elif dicName == "2merDic":
                for k, v in self._2mer_.items():
                    twf.write(f"{k:>1s} {v:<6d}\n")

            elif dicName == "3merDic":
                for k,v in self._3mer_.items():
                    twf.write(f"{k:>1s} {v:<6d}\n")

def main():
    beg = time.time()
    ex = kormerDict()
    for i in range(1,29+1):
        ex.getData("중앙기사%dResPy.json" % i)
        ex.dict1Mer()
        ex.dict2Mer()
        ex.dict3Mer()
    ex.colDict("1merDic")
    ex.colDict("2merDic")
    ex.colDict("3merDic")
    end = time.time()
    print("exec time : %.6g sec(s)" % (end-beg))
    return

if __name__ == '__main__':
    main()