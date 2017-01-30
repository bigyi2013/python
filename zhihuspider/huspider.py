#!/usr/bin/env python3
ian
'''
Required
- requests (必须)
- pillow (可选)
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.2.4"
Update
- name   : "wangmengcn"
- email  : "eclipse_sv@163.com"
- date   : "2016.4.21"
'''
import random
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
try:
    from PIL import Image
except:
    pass
import mysql.connector
#from bs4 import BeautifulSoup

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}
# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_xsrf():
    '''_xsrf 是一个动态变化的参数'''
    index_url = 'http://www.zhihu.com'
    # 获取登录时需要用到的_xsrf
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    pattern = r'name="_xsrf" value="(.*?)"'
    # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern, html)
    return _xsrf[0]


# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False


def login():
    # 通过输入的用户名判断是否是手机号
    if re.match(r"^1\d{10}$", "sun163@141.com"):
        print("手机号登录 \n")
        post_url = 'http://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': "1q2wspider",
            'remember_me': 'true',
            'phone_num': "asfagfsaga",
        }
    else:
        if "@" in "@ada":
            print("邮箱登录 \n")
        else:
            print("你的账号输入有问题，请重新登录")
            return 0
        post_url = 'http://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': "1q2wreader",
            'remember_me': 'true',
            'email': "bigyibigyi@163.com",
        }
    try:
        # 不需要验证码直接登录成功
        print("不需要验证码直接登录成功?")
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.text
        print(login_page.status_code)
        print(login_code['msg'])
    except:
        # 需要输入验证码后才能登录成功
        print("需要输入验证码后才能登录成功")
        postdata["captcha"] = get_captcha()
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.text
        print(login_code['msg'])
    session.cookies.save()

try:
    input = raw_input
except:
    pass
def gettopics(html):
    topic = r'"topic",.*?", "(\d{8})'
    topics = re.findall(topic, html)
    if len(topics)!=0:
        return topics[0]
    else:
        return None
def getloads(html):
    post_url1 = 'https://www.zhihu.com/topic/19776749/organize/entire?child=&parent='
    load = r'"load",.*?"", "(\d{8})"]'
    loads = re.findall(load, html)
    npus=set()
    for load in loads:
        newposturl = post_url1 + str(load)
        npus.add(newposturl)
    return npus
def getmore(html):
    more = r'"load",.*?", "(\d{8})", "\d{8}'
    getmores = re.findall(more, html)
    topic=gettopics(html)
    mpus=[]
    if topic==None:
        t=set()
        return t
    elif len(getmores)!=0:
        for getmore in getmores:
            moreposturl = 'https://www.zhihu.com/topic/19776749/organize/entire?child=' + str(
                    getmore) + '&parent=' + str(topic)
            mpus.append(moreposturl)
    return mpus
def gethtml(value):
    print(value)
    # 导入MySQL驱动:
    import mysql.connector
    # 注意把password设为你的root口令:
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='zhihu')
    cursor = conn.cursor()
    try:
        cursor.execute('select msg from urlmsg where url = %s  ', (value,))
        values = cursor.fetchall()
        # 关闭Cursor和Connection:
        t=values[0][0]
        print("找到url")
        return t
    except:
        print("访问网络")
        time.sleep(random.uniform(1,6))
        try:
             t= session.post(value, headers=headers, data=posts).text
        except:
            t = "aaa"
            print("网络错误")
        conn = mysql.connector.connect(user='root', password='1q2wreader', database='zhihu')
        cursor = conn.cursor()
        # 插入一行记录，注意MySQL的占位符是%s:
        cursor.execute('insert into urlmsg (url,msg) values (%s, %s)', [value,t])
        conn.commit()
        cursor.close()
        conn.close()
        print("conn.close()")
        return t
posts = {
                '_xsrf': get_xsrf(),
            }
def pushvalues(key,values):
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='zhihu')
    cursor = conn.cursor()
    cursor.execute('select url from urlmsg where url = %s  ', (key,))
    value = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    print(len(value))
    if len(value)==0:
        conn = mysql.connector.connect(user='root', password='1q2wreader', database='zhihu')
        cursor = conn.cursor()
        # 插入一行记录，注意MySQL的占位符是%s:
        cursor.execute('insert into urlmsg (url,msg) values (%s, %s)', [key, values])
        conn.commit()
        cursor.close()
        conn.close()
        print("conn.close()")
def t(i):
    t = "floor" + str(i+1) + ".txt"
    t2= "floor" + str(i) + ".txt"
    def getloadlists(url):
        html = gethtml(url)
        mores = getmore(html)
        loads = getloads(html)
        with open(t,'a', encoding='utf-8')as f:
            f.write("posturl:" + str(url) + "\n" + "html:" + str(html) + "\n" + "*_" * 9 + "\n" + "getlist:" + str(
                loads) + "\n" + "*_" * 10 + "\n")
        #pushvalues(url, html)
        if len(mores) != 0:
            getloadlists(mores[0])
    if __name__ == '__main__':
        if isLogin():
            print('您已经登录')
            with open(t2, 'r', encoding='utf-8')as f:
                fr=f.read()
            r=r'(https://.*?)\''
            urllist=re.findall(r,fr)
            for url in urllist:
                print(url)
                getloadlists(url)
        else:
            login()
for i in range(7,26):
    time.sleep(random.uniform(3, 5))
    print("floor"+str(i))
    t(i)

