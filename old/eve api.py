
from urllib import request
from bs4 import BeautifulSoup
#eve api 矿物价格
class evekuangwu:
    #地址列表
    def __init__(self,baseurl):
        self.baseurl = baseurl
        url = self.baseurl
        req = request.Request(url)
        try:
            response = request.urlopen(req)
            bean=response.read()
            soup=BeautifulSoup(bean,"lxml")
            # 分析soup
            print(soup)
        except  Exception as e:
            print(e.reason)
            return None
baseurl = 'http://www.ceve-market.org/api/market/type/34.xml'
evekuangwu(baseurl)
