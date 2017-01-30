from bs4 import  BeautifulSoup
import requests
import random
import mysql.connector
import os
def insert(av):
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='toplist')
    cursor = conn.cursor()
    try:
        cursor.execute('select av from bilibili where av =%s ',[av])
        values = cursor.fetchall()
        # 关闭Cursor和Connection:
        #print(values)
        t = values[0][0]#判断values是不是空集
        cursor.close()
        conn.close()
    except:
        # 插入一行记录，注意MySQL的占位符是%s:
        cursor.execute('insert into bilibili (av) values (%s)', [av])
        conn.commit()
        cursor.close()
        conn.close()
def push(tag,info,av):
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='toplist')
    cursor = conn.cursor()
    cursor.execute('update bilibili set '+tag+'=%s where av=%s ', [info,av])
    conn.commit()
    cursor.close()
    conn.close()

def getip(a):
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='iplist')
    cursor = conn.cursor()
        # try:
    cursor.execute('select ip,port from ip where live =%s limit 1000', [a])
    values = cursor.fetchall()
        # 关闭Cursor和Connection:
        # print(values)
    cursor.close()
    conn.close()
    return values
def proxies():
    ip1=getip(1)
    i=random.randint(0,len(ip1))
    ip=ip1[i][0]
    port=ip1[i][1]
    proxies = {
        "http": str(ip) + ":" + str(port),
    }
    return proxies
def geturl(url):
    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) C hrome/54.0.2840.71 Safari/537.36'}
    r = requests.get(url,headers=headers,proxies=proxies())
    soup=BeautifulSoup(r.text,'lxml')
    title=soup.select('.title')
    info=soup.select('.v-info')
    upinfo = soup.select('.up-info')
    return  (info, title,upinfo)
def prints(tag,titlea,up,bofang,time):
    os.system('cls')
    #print("\n"*30)
    print("- - "*20)
    print("|   已经爬取到视频信息：                                      ")
    print("|   标签分类："+str(tag)+"                                              ")
    print("|   视频标题："+str(titlea)+"                                          ")
    print("|   up主："+str(up)+"                                          ")
    print("|   播放数："+str(bofang)+"                                          ")
    print("|   视频时间："+str(time)+"                                          ")
    print("- - " * 20)
def main(url,tag):
    (info, title, upinfo) = geturl(url)
    for i in range(len(info)):
        titlea=title[i].get_text()
        av=title[i]['href']
        bofang=info[i].select('span')[0].get_text()
        danmu=info[i].select('span')[1].get_text()
        pinglun=info[i].select('span')[2].get_text()
        up=upinfo[i].a.get_text()
        time=upinfo[i].span.get_text()
        insert(av)
        push('bofang',bofang,av)
        push('danmu', danmu, av)
        push('pinglun', pinglun, av)
        push('up', up, av)
        push('time', time, av)
        push('tag', tag, av)
        push('title',titlea, av)
        prints(tag,titlea,up,bofang,time)
def url(tag):
    for year in range(2012,2013):
        for mouth in range(1,3):
            mouth=("00"+str(mouth))[-2:]
            for i in range(1,6):
                url = "http://www.bilibili.com/list/hot-" + str(tag) + "-"+str(i)+"-" + str(year) + "-" + str(mouth) + "-01~" + str(
        year) + "-" + str((mouth )) + "-31.html"
                print("url:"+url)
                try:
                    main(url,tag)
                except:
                    print("todo")
#url(65)
for i in range(1,20):
    p=proxies()
    print(p)