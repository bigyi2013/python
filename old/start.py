from urllib import request
from bs4 import BeautifulSoup
import re
#瑞士文章爬虫0.1
class ruishi:
    #地址列表
    def __init__(self,baseurl,tag):
        self.baseurl = baseurl
        self.tag = str(tag)
        url=self.baseurl+self.tag
        req = request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)')
        try:
            response = request.urlopen(req)
            bean=response.read()
            soup=BeautifulSoup(bean,"lxml")
            # 寻找文章链接
            for main in soup.find(class_='content-left').find_all("a","cover"):
                   with open('list.txt','a')as f:
                       f.write(main.get('href')+'\n')
        except  Exception as e:
            print(e.reason)
            return None
class getpage:
    def __init__(self):
        with open('list.txt','r')as p:
            for i in range(10):
                page=str(p.readline())
                req = request.Request(page)
                req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)')
                response = request.urlopen(req)
                bean = response.read()
                soup = BeautifulSoup(bean, "lxml")
                print(soup.name)



baseurl = 'http://www.ellemen.com/'
ruishi(baseurl, 'gear/auto/')
getpage()
