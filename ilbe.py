from __crwlframe__ import *
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool, freeze_support
import time, re, random

ILBE_URL = "http://www.ilbe.com/"
ILBE_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
ILBE_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
ILBE_STEM = "index.php?mid={}&page={}"
MAX_SLEEP_TIME = 4

class ilbeCrwl(crwlframe):
    def __init__(self, p16, p18, pnum, url = ILBE_URL, agent = ILBE_AGENT, accept = ILBE_ACCEPT):
        self.origin = url
        self.ilbe_16_18 = tuple(range(p16,p18-1,-1))
        self.yRange = ('2016', '2017', '2018')
        self.begPnum = 108
        self.postsCnt = pnum
        super(ilbeCrwl, self).__init__(self.origin, agent, accept)

    def _remove_tag(self,content):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr,'',content)
        specialr = re.compile('[\:\,\.\?\~\n\s+]', re.UNICODE)
        cleantext = re.sub(specialr,' ', cleantext)
        return cleantext

    def _getContents(self, pAddr):
        print("Writing... -> ", pAddr, type(pAddr))
        self.headers['referer'] = re.sub("document=[0-9]+", '', pAddr)
        self.req.headers.update(self.headers)
        post = bs(self.req.get(pAddr).text, 'html.parser')
        with open("ilbe_html_%s.txt" % (pAddr.replace("http://www.ilbe.com/index.php?document_srl=","")), "w", encoding='utf-8') as htmldoc:
            htmldoc.write(post.text)
        postDate = post.find_all("div", "date")
        postDate = list(map(self._remove_tag, list(map(str, postDate))))
        nickName = post.find_all("div", "author")
        nickName = list(map(self._remove_tag, list(map(str, nickName))))
        content = post.find_all("div", re.compile("document_[0-9]+ xe_content"))
        content = list(map(self._remove_tag, list(map(str, content))))
        try:
            if ((postDate[0].split())[0]) in self.yRange and len(nickName) > 0 and len(content) > 0:
                with open("ilbe_0%d.txt" % self.begPnum, "a", encoding='utf-8') as wf:
                    wf.write(nickName[0] + " _# " + content[0] + " $$\n")
        except IndexError:
            time.sleep(random.randint(0, MAX_SLEEP_TIME))
        time.sleep(random.randint(0, MAX_SLEEP_TIME))

    def getArticle(self):
        posts = []
        for i in self.ilbe_16_18:
            bURL = super(ilbeCrwl,self).getBoardURL(ILBE_STEM, "ilbe", str(i))
            if bURL.status_code == 200:
                bPage = bs(bURL.text, 'html.parser')
                bBoardP = bPage.tbody.find_all("a")
                del bBoardP[0]
                for j in bBoardP:
                    if len(posts) == self.postsCnt:
                        with Pool(processes=4) as pool:
                            pool.map(self._getContents, posts)
                        print("ilbe_%d.txt -> out!\n" % self.begPnum)
                        self.begPnum += 1
                        posts.clear()
                    if re.fullmatch("\/[0-9]+", j.get("href")) is not None or re.fullmatch("\/cdn-cgi\/l\/email-protection", j.get("href")) is not None:
                        print("Except -> ", j.get("href"))
                        continue
                    posts.append(j.get("href"))
                    print(j.get("href"),"-> get success!")
                    # time.sleep(random.randint(0, MAX_SLEEP_TIME))
        if len(posts) > 0:
            with Pool(processes=4) as pool:
                pool.map(self._getContents, posts)
        print("Complete!")

def main(): # for unit test
    beg = time.time()
    ex = ilbeCrwl(8528, 911, 1000)
    ex.getArticle()
    end = time.time()
    print(end-beg, "sec(s)")
    return

if __name__ == '__main__':
    freeze_support()
    main()
