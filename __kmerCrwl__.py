import requests as rq

class crwlframe:
    def __init__(self, url, agent):
        self.req = rq.Session()
        self.url = url
        self.agent = agent
        self.headers={'referer' : self.url,
                      'User-agent' : self.agent}

    def getDailyListURL(self, date):
        self.req.headers.update(self.headers)
        # print(self.url+date)
        return self.req.get(self.url+date)

    def getDailyArticle(self, url):
        return self.req.get(url)