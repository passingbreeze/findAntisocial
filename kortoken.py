import time,json
from collections import OrderedDict as od

def isHangul(text): # codes come from Prof. Cho
    import sys, re, string

    pyVer3 =  sys.version_info >= (3, 0)

    if pyVer3 : # for Ver 3 or later
        encText = text
    else: # for Ver 2.x
        if type(text) is not unicode:
            encText = text.decode('utf-8')
        else:
            encText = text

    # '19.2.15 수정
    hanCount = len(re.findall(u'[\u3130-\u3163\uAC00-\uD7A3]+', encText))
    # 이전 코드 중 \u3130-\u318F => 옛한글을 포함합니다.
    # ㄱ ~ ㅎ : \u3130 ~ \u314E
    # ㅏ ~ ㅣ : \u314F ~ \u3163
    # 가 ~ 힣 : \uAC00 ~ \uD7A3

    return hanCount > 0

class korToken:
    def __init__(self, fname):
        self._countPh_ = {}
        self.fname = fname

    def colToken(self):
        kword = ""
        try :
            f = open(self.fname, "r", encoding="utf-8")
        except UnicodeDecodeError:
            f = open(self.fname, "r")
        with f as rf:
            for line in rf:
                if line == "":
                    continue
                else:
                    line = line.strip()
                    stmt = line.split()
                    for word in stmt:
                        for c in word:
                            if isHangul(c):
                                kword += c
                        if kword is not "" and kword not in self._countPh_:
                            self._countPh_[kword] = 1
                        elif kword is not "" and kword in self._countPh_:
                            self._countPh_[kword] += 1
                        kword = ""

    def getToken(self):
        res = dict(od(reversed(sorted(self._countPh_.items(), key = lambda t:t[1]))))
        with open((self.fname.replace(".txt","")+"Res.txt"), "w", encoding="cp949") as wf:
            for k,v in res.items():
                wf.write(f"{v:>6d} {k:<30s}\n")

        with open((self.fname.replace(".txt","")+"ResPy.json"), "w") as wf:
            wf.write(json.dumps(res))

        print(self.fname+"에서의 Token 갯수 :", len(res))

def main():
    beg = time.time()
    for i in range(1,29+1):
        ex = korToken("중앙기사%d.txt" % i)
        ex.colToken()
        ex.getToken()
    end = time.time()
    print("exec time : %.6g sec(s)" % (end - beg))
    return

if __name__ == '__main__':
    main()