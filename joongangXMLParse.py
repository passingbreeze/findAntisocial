# -*- encoding:utf-8 -*-
from __kmerCrwl__ import *
import re
from bs4 import BeautifulSoup as bs

## Path Config in here
JAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
TargetURL = 'https://news.joins.com/sitemap/daily-articles/'
outTarget = 'joongang_conv_'
monthlyList = list(map(str,range(1,13)))

contentReg = r'<s n=\d+>(.*?)<\/s>'

def chkLeapyear(year):
    return year%4 == 0 and (year%400 == 0 or year%100 != 0)

class jarticle(crwlframe) :
    def __init__(self, year, url = TargetURL, agent = JAgent):
        self.origin = url
        self.year = str(year)
        self.yearMonth = []
        super(jarticle, self).__init__(self.origin, agent)
        for month in monthlyList:
            if month == "2":
                if chkLeapyear(year):
                    for i in range(1,30):
                        if i<10:
                            self.yearMonth.append(self.year + "0" + month + "0" + str(i))
                        else :
                            self.yearMonth.append(self.year + "0" + month + str(i))
                else :
                    for i in range(1,29):
                        if i<10:
                            self.yearMonth.append(self.year + "0" + month + "0" + str(i))
                        else :
                            self.yearMonth.append(self.year + "0" + month + str(i))
            elif month == "4" or month == "6" or month == "9" or month == "11":
                for i in range(1,31):
                    if len(month) == 1:
                        if i < 10:
                            self.yearMonth.append(self.year + "0" + month + "0" + str(i))
                        else:
                            self.yearMonth.append(self.year + "0" + month + str(i))
                    else :
                        if i<10:
                            self.yearMonth.append(self.year + month + "0" + str(i))
                        else :
                            self.yearMonth.append(self.year + month + str(i))
            else :
                for i in range(1,32):
                    if len(month) == 1:
                        if i < 10:
                            self.yearMonth.append(self.year + "0" + month + "0" + str(i))
                        else:
                            self.yearMonth.append(self.year + "0" + month + str(i))
                    else :
                        if i<10:
                            self.yearMonth.append(self.year + month + "0" + str(i))
                        else :
                            self.yearMonth.append(self.year + month + str(i))

    def _remove_tag(self,content):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, "",content)
        # specialr = re.compile('[\:\,\.\?\~]')
        # cleantext = re.sub(specialr,' ', cleantext)
        return cleantext

    def _getAList(self):
        # rx = re.compile(contentReg)
        articleList = []
        for date in self.yearMonth:
            dailyURL = super(jarticle, self).getDailyListURL(date)
            if dailyURL.status_code == 200:
                articles = bs(dailyURL.text,"lxml")
                tempList = re.split("https://",self._remove_tag(articles.text))
                del tempList[0]
                articleList += tempList
        print("%s년도 기사 갯수 : %d" % (self.year,len(articleList)))
        return articleList

    def getArticles(self):
        setList = self._getAList()
        for address in setList:
            articleURL = super(jarticle,self).getDailyArticle("https://"+address)
            article = bs(articleURL.text, "html.parser")
            with open("Joongang_%s_Articles.txt" % self.year, "w", encoding="utf-8") as wf:
                contents = article.find_all("div", "article_body")
                if len(contents) != 0 :
                    wf.write(self._remove_tag(str(contents[0]))+"\n")

        # try:
        #     rf = B
        #         # open(readTargetFolder + fileName, 'r', encoding='utf-8')
        #     wf = open(outTargetFolder + fileName, 'w', encoding='utf-8')
        #     lines = rf.readlines()
        #     cnt = 0
        #     for line in lines:
        #         cnt += 1
        #         m = rx.findall(line)
        #         for mm in m:
        #             curret = remove_tag(mm)
        #             if not curret:
        #                 continue
        #             result += curret + ' #\n'
        #
        #     wf.write(result)
        #     rf.close()
        #     wf.close()
        # except FileNotFoundError:
        #     print(fileName + ': FNF Error')
        #     pass


def main():
    ex = jarticle(2018)
    ex.getArticles()
    # print(dateList)
    # for headnumber in headNumber:
    #     for filecategory in fileCategory:
    #         for indexnumber in indexNumber:
    #             numberFormat = str(indexnumber).zfill(5)
    #             filename = str(headnumber) + filecategory + numberFormat + '.txt'
    #             parse(filename)


if __name__ == '__main__':
    main()