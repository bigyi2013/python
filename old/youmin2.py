from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import re
def getlink(url,tag):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print("HTTPError")
        return None
    except URLError as e:
        print("URLError")
        return None
    bean = BeautifulSoup(html, 'lxml')
    links = set()
    list=bean.findAll("a", href=re.compile("^(http://www.gamersky.com/)(ent|new)((?!_).)*$"))
    num =0#记录有效link
    for link in list:
        if 'href'in link.attrs:#这个句子其实没什么用
            if 'title'in link.attrs:
                if link.attrs['href'] not in links:
                    newlink=link.attrs['href']
                    links.add(newlink)
                    print(newlink)
                    print(link.attrs['title'])
                    num=num+1
    if num == 0:
        return "empty"
    return url
for i in range(39,52,1):
    a=getlink("http://www.gamersky.com/ent/147/List_"+str(i)+".html","囧图")
    #print(a+"完成"+"*_"*20+"*")
    if a == None:
        break
    elif a =="empty":
        print("can not find linklist")
        break
    else:
        print(a + "完成" + "*_" * 20 + "*")
