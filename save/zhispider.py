#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from bs4 import BeautifulSoup

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
        print(login_code)
        #print(login_code['msg'])
    session.cookies.save()

try:
    input = raw_input
except:
    pass

topic = r'"topic",.*?", "(\d+)'
posts = {
        '_xsrf': get_xsrf(),
    'num':1,
    }
getmore = r'"load",.*?", "(\d+)", "'
post_url1 = 'https://www.zhihu.com/topic/19776749/organize/entire?child=&parent='
retopics=[]
def geturl(posturl):
    load = r'"load",.*?", "(\d+)"]'
    i=random.uniform(2,5)
    time.sleep(i)
    try:
        html = session.post(posturl, headers=headers, data=posts).text
    except:
        print("网络错误")
        html="aaa"
    getmores= re.findall(getmore,html)
    loads = re.findall(load,html)
    topics = re.findall(topic, html)
    if len(getmores)==1:
        more1=r'(\d+)'
        morelink=re.findall(more1,getmores[0])
        moreposturl='https://www.zhihu.com/topic/19776749/organize/entire?child='+str(morelink[0])+'&parent='+ str(topics[0])
        print("加载")
        print(moreposturl)
        geturl(moreposturl)
    for getsurl in topics:
        t = posts['num']
        t = t+1
        print(t)
        posts['num'] = t
        print(getsurl)
        with open('list7.txt', 'a', encoding='utf-8')as f:
            f.write(getsurl+",")
    # if len(loads)==0:
    #     topics.pop(0)
    #     for getsurl in topics:
    #         print(getsurl)
    #         with open('list1.txt', 'a', encoding='utf-8')as f:
    #             f.write(getsurl+",")
    # else:
    #     for load in loads:
    #         posturl=post_url1+str(load)
    #         geturl(posturl)

def get_top():
    posturl = 'https://www.zhihu.com/topic/19776749/organize/entire'
    geturl(posturl)
if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
        get_top()
    else:
        login()
