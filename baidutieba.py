from urllib import request
import urllib
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
def gettextfromtieba(name,page):
    filename = name+".txt"
    with open(filename, 'w', encoding='utf-8')as qingkong:
            qingkong.write('清空')
    def gettext(url):
        try:
            html = urlopen(url)
        except HTTPError as e:
            return None
        try:
            bean=BeautifulSoup(html.read(),'lxml')
            try:
                testtext=bean.find("li",{"class":" j_thread_list clearfix"})
                if testtext == None:
                    return "[]"
            except AttributeError as e:
                return None
            textlist=bean.findAll("li",{"class":" j_thread_list clearfix"})
        except AttributeError as e:
            return None
        return textlist
    def printtext(textlist):
        for text in textlist :
            with open(filename, 'a',encoding='utf-8')as f:
                f.write('{"title":"'+  text.a["title"] +'","href":"' "http://tieba.baidu.com"+ text.a["href"] + "?see_lz=1"+'"},')
    for i in range(0,page*50,50):
        url="http://tieba.baidu.com/f?kw="+urllib.parse.quote(name)+"&ie=utf-8&tab=good&cid=0&pn="+str(i)
        textlist=gettext(url)
        if textlist == None:
            print("找不到textlist")
        elif textlist == "[]":
            print("精品贴共"+str(i/50)+"页")
            break
        else:
            printtext(textlist)
            print("第"+str(i/50+1)+"页 done")
gettextfromtieba("南笙",100)
