import requests as rq

class crwlframe:
    def __init__(self, url, agent, accept):
        self.req = rq.Session()
        self.url = url
        self.headers={'referer' : self.url,
                      'User-Agent': agent,
                      'Accept' : accept,
                      'Connection' : 'close' }

    def getBoardURL(self, boardStem, boardName, pageNum):
        self.bUrl= self.url + boardStem
        self.bUrl=(self.bUrl).format(boardName, pageNum)
        self.req.headers.update(self.headers)
        return self.req.get(self.bUrl)

    def getPostURL(self, postNum):
        self.pURL = self.url+str(postNum)
        self.req.headers.update(self.headers)
        return self.req.get(self.pURL)

    def postBoardURL(self, boardStem, boardName, pageNum):
        self.url += boardStem
        self.url = (self.url).format(boardName, pageNum)
        self.req.headers.update(self.headers)
        return self.req.post(self.url)

    def postPostURL(self, postNum):
        self.pURL = self.url+str(postNum)
        self.req.headers.update(self.headers)
        return self.req.post(self.pURL)
