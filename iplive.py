import requests
import mysql.connector
def iflive(ip,port):
    proxies = {
        "http": str(ip)+":"+str(port),
    }
    print(proxies)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    url="https://www.zhihu.com/"
    try:
        r=requests.get(url,headers=headers,proxies=proxies)
        print(r.status_code)
        return r.status_code
    except requests.exceptions.RequestException  as e:
        print(e)
        status_code=909
        return status_code
def getip(a):
        conn = mysql.connector.connect(user='root', password='1q2wreader', database='iplist')
        cursor = conn.cursor()
    #try:
        cursor.execute('select ip,port from ip where live =%s limit 1000', [a])
        values = cursor.fetchall()
        # 关闭Cursor和Connection:
        # print(values)
        cursor.close()
        conn.close()
        return values
def push(ip,port,status_code):
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='iplist')
    cursor = conn.cursor()
    if status_code==200:
        cursor.execute('update ip set live=%s where ip=%s and port=%s', [1,ip,port])
        conn.commit()
    else:
        cursor.execute('update ip set live=%s where ip=%s  and  port=%s', [2, ip, port])
        conn.commit()
    cursor.close()
    conn.close()
def main(a):
    ipa=getip(a)
    for iplist in ipa:
        ip=iplist[0]
        port=iplist[1]
        status_code=iflive(ip,port)
        push(ip,port,status_code)
if __name__ == '__main__':
    main(0)#0表示未知，main0 检测未知是否可用
    main(1)#1表示可用 2表示不可用 main1检测 可用是否可用