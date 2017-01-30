from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re
pages = set()
def getlinks(url):
    global pages
    try:
        html = urlopen(url)
    except HTTPError as e:
        print("HTTPError")
        return None
    bean=BeautifulSoup(html,'lxml')
    for link in bean.findAll("a",href=re.compile("^(http://www.gamersky.com/ent)((?!_).)*$"),title=re.compile(".*(囧图)")):
        if 'href'in link.attrs:#这个句子其实没什么用
            if 'title'in link.attrs:#这个句子其实没什么用
                    if link.attrs['href'] not in pages:
                        newpage=link.attrs['href']
                        #print(link)
                        print(newpage)
                        print(link.attrs['title'])
                        pages.add(newpage)
                        getlinks(newpage)
getlinks("http://www.gamersky.com/ent/201608/796289.shtml")