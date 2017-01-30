#-*- coding: utf-8 -*-
import requests
import mysql.connector
import re
from bs4 import  BeautifulSoup
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    #"Host": "g.e-hentai.org",
    #"Referer": "http://g.e-hentai.org/",
    'User-Agent': agent
}
def get(url):
    try:
        t=requests.get(url, headers=headers)
        soup=BeautifulSoup(t.text.encode('utf-8'),'lxml')
        pages=soup.find(id='gdd').table.find_all('tr')
        pagesr=pages[5].get_text().encode('utf-8')
        faverr=pages[6].get_text().encode('utf-8')
        ranks = soup.find(id='gdr').table.tr.next_sibling
        ranksr=ranks.get_text().encode('utf-8')
        taglist=soup.find(id='taglist').table.select('div[id]')
        tags=[]
        tagr=r':(.*)'
        for tag in taglist:
            try:
                tag_=re.findall(tagr,str(tag["id"]))[0]
                tags.append(tag_)
            except:
                pass
        try:
            t = r'(\d+)'
            rankt=r'Average: (.*)\''
            pages = re.findall(t, str(pagesr))[0]
            faver = re.findall(t, str(faverr))[0]
            rank=re.findall(rankt, str(ranksr))[0]
            print("页面分析完成")
            return int(pages),int(faver),float(rank),tags
        except:
            print("页面分析错误")
            return 1, 1, 1, []
    except:
        print("页面分析错误")
        return 1, 1, 1, []
def gethref():
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='ehentai')
    cursor = conn.cursor()
    cursor.execute('SELECT href FROM msg where faver=1 or faver is null  ')
    values = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    print("有"+str(len(values))+"条数据需要爬取")
    for value in values:
        url=value[0]
        print("开始爬取" + str(url))
        t=get(url)
        pushmsg(t,url)
def pushmsg(t,url):
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='ehentai')
    cursor = conn.cursor()
    # 插入一行记录，注意MySQL的占位符是%s:
    cursor.execute('UPDATE msg SET pages=(%s),faver=(%s),rank=(%s),tag=(%s) WHERE href=(%s);',
                   ([t[0], t[1], t[2], str(t[3]), url]))
    conn.commit()
    cursor.close()
    conn.close()
    print("完成写入")
# url="http://g.e-hentai.org/g/975929/f2eba87d5e/"
# t=get("http://g.e-hentai.org/g/975929/f2eba87d5e/")
# push(t,url)
def upload(a):
    for i in range(1,a,1):
        url="http://g.e-hentai.org/?page="+str(i)+"&f_doujinshi=on&f_manga=on&f_artistcg=on&f_gamecg=on&f_western=on&f_non-h=on&f_imageset=on&f_cosplay=on&f_asianporn=on&f_misc=on&f_search=%E6%B1%89%E5%8C%96&f_apply=Apply+Filter"
        t=requests.get(url, headers=headers)
        soup=BeautifulSoup(t.text.encode('utf-8'),'lxml')
        try:
            pages = soup.find(class_='itg').find_all('tr')
            for page in pages:
                try:
                    title=page.div(class_='it5')[0].get_text()
                    href=page.div(class_='it5')[0].a.get('href')
                    cover = page.div(class_='it2')[0]
                    t=r'init~ehgt.org~(.*?)~'
                    cover = "http://ehgt.org/"+re.findall(t, str(cover))[0]
                    push(cover, href,title)
                except:
                    pass
        except:
            print("页面分析错误")
def push(cover, href,title):
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='ehentai')
    cursor = conn.cursor()
    try:
        cursor.execute('select href from msg where href = %s  ', (href,))
        values = cursor.fetchall()
        # 关闭Cursor和Connection:
        t = values[0][0]
        cursor.close()
        conn.close()
        print("重复title")
        print(href)
    except:
        # 插入一行记录，注意MySQL的占位符是%s:
        cursor.execute('insert into msg (cover, href,title) values (%s,%s, %s)', [cover, href,title])
        conn.commit()
        print("更新title")
        print(href)
        global num
        num=num+1
        cursor.close()
        conn.close()
#upload(310)
gethref()