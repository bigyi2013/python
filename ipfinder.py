import requests
import mysql.connector
from bs4 import  BeautifulSoup
url='http://www.data5u.com/'
# def pushmsg(ip):
#     conn = mysql.connector.connect(user='root', password='1q2wreader', database='iplist')
#     cursor = conn.cursor()
#     # 插入一行记录，注意MySQL的占位符是%s:
#     cursor.execute('insert into ip(ip,live) values (%s,%s)', [ip,0])
#     conn.commit()
#     cursor.close()
#     conn.close()
#     print("完成写入")
def push(ip,port):
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='iplist')
    cursor = conn.cursor()
    try:
        cursor.execute('select ip from ip where ip =%s and port=%s',[ip,port])
        values = cursor.fetchall()
        # 关闭Cursor和Connection:
        #print(values)
        t = values[0][0]#判断values是不是空集
        cursor.close()
        conn.close()
        print("重复ip")
    except:
        # 插入一行记录，注意MySQL的占位符是%s:
        cursor.execute('insert into ip (ip,port,live) values (%s,%s,%s)', [ip,port,0])
        conn.commit()
        print("更新ip")
        cursor.close()
        conn.close()
def changeip(ip):
    ip = ip.split('.')
    list=''
    for ip in ip:
        ip = "000" + ip
        ip=ip[-3:]
        list=list+ip
    return list
def kuaidaili(i):
    url='http://www.kuaidaili.com/proxylist/'+str(i)+'/'
    header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    r=requests.get(url,headers=header)
    soup=BeautifulSoup(r.text,"lxml")
    r=soup.select('tbody tr')
    for iplist in r:
        ip=iplist.select('td')[0].get_text()
        port=iplist.select('td')[1].get_text()
        #ip = changeip(ip)
        push(ip, port)
def data5u():
    url = 'http://www.data5u.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    r=requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,"lxml")
    for ull2 in soup.find_all('ul','l2'):
        ip=ull2.span.li.get_text()
        ports = ull2.contents[3]
        port=ports.li.get_text()
        #ip=changeip(ip)
        push(ip,port)
def xicidaili(a):
    url = 'http://www.xicidaili.com/'+str(a)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    re=requests.get(url,headers=headers)
    soup = BeautifulSoup(re.text,"lxml")
    r=soup.find_all(id="ip_list")[0]
    for tr in r.contents:
        if len(tr)!=1:
            try:
                ip=tr.find_all('td')[1].get_text()
                port = tr.find_all('td')[2].get_text()
                #ip = changeip(ip)
                push(ip,port)
            except:
                None
def main():
    try:
        print("从data5u 寻找ip")
        data5u()
    except:
        None
    try:
        print("从xicidaili 寻找ip")
        xicidaili('nn')
        xicidaili('nt')
        xicidaili('wn')
        xicidaili('wt')
    except:
        None
    try:
        for i in range(1,11):
            print("从kuaidaili第"+str(i)+"页寻找ip")
            kuaidaili(i)
    except:
        None
if __name__ == '__main__':
    main()
