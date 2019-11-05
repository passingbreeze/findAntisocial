from __crwlframe__ import *
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool,freeze_support
import time, re, random, os

WOMAD_URL = "https://womad.life/"
WOMAD_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
WOMAD_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
WOMAD_STEM = "index.php?mid={}&page={}"
MAX_SLEEP_TIME = 5

class womadCrwl(crwlframe):
    def __init__(self, b16, e18, postcnt, url = WOMAD_URL, agent = WOMAD_AGENT, accept = WOMAD_ACCEPT):
        self.origin = url
        self.womad_16_18 = list(range(b16, e18+1))
        self.textNum = 40
        self.postsCnt = postcnt
        super(womadCrwl, self).__init__(self.origin, agent, accept)

    def _remove_tag(self,content):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr,'',content)
        specialr = re.compile('[\:\,\.\?\~\n\s+]', re.UNICODE)
        cleantext = re.sub(specialr,' ', cleantext)
        return cleantext

    def _getContents(self, num):
        print("Writing... -> %d | proc ID : " % num, os.getpid())
        pURL = super(womadCrwl, self).getPostURL(num)
        if pURL.status_code == 200:
            post = bs(pURL.text, 'html.parser')
            with open("womad_html_%d.txt"%num, "w", encoding='utf-8') as htmldoc:
                htmldoc.write(pURL.text)
            nickName = post.find_all("div", re.compile("clear top-padding"))
            nickName = list(map(self._remove_tag, list(map(str, nickName))))
            nickName = nickName[0].replace("작성자","")
            content = post.find_all("div", re.compile("content content-box post-content"))
            content = list(map(self._remove_tag, list(map(str, content))))
            if len(content) > 0:
                with open("womad_0%d.txt" % self.textNum, "a", encoding='utf-8') as wf:
                    wf.write(nickName + " _# "+ content[0] + "$$\n")
        time.sleep(random.randint(0, MAX_SLEEP_TIME))

    def getArticle(self):
        while len(self.womad_16_18) > 0:
            temp = self.womad_16_18[:self.postsCnt]
            del self.womad_16_18[:self.postsCnt]
            with open("womadRec.txt", "w", encoding='utf-8') as rf:
                rf.write(str(self.womad_16_18[0])+" "+str(self.womad_16_18[len(self.womad_16_18)-1])+"\n")
            with Pool(processes=4) as pool:
                pool.map(self._getContents, temp)
            print("womad_0%d.txt -> out!" % self.textNum)
            self.textNum+=1
        print("Complete!\n")


def main(): # for unit test
    beg = time.time()
    begRng, endRng = 0,0
    with open("womadRec.txt", "r", encoding='utf-8') as rec:
        begRng, endRng = list(map(int, rec.readline().split()))
    if begRng == 0:
        ex = womadCrwl(91, 267956, 5000)
    else :
        ex = womadCrwl(begRng, endRng, 5000)
    ex.getArticle()
    print("---%.3f sec(s)---" % (time.time()-beg))
    return

if __name__ == '__main__':
    freeze_support()
    main()
