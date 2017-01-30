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
        print(login_code['msg'])
    session.cookies.save()

try:
    input = raw_input
except:
    pass

posts = {
        '_xsrf': get_xsrf(),
    }
nums={
    'num':1,
    'times':1
}

topiclist=set()
loadlist=set()
morelist=set()
def gettopiclist ():
    if len(topiclist)==0:
        r=r'(\d*?),'
        with open('topic.txt', 'r', encoding='utf-8')as f:
            fr=f.read()
        list=re.findall(r,fr)
        for url in list:
            topiclist.add(url)
def getloadlist():
    if len(loadlist)==0:
        r=r'newposturl.*19776749.*?(\d{8})'
        with open('posturl.txt', 'r', encoding='utf-8')as f:
            fr=f.read()
        list=re.findall(r,fr)
        print("loadlist:"+str(len(list)))
        for url in list:
           loadlist.add(url)
def getmorelist():
    if len(morelist)==0:
        r=r'moreposturl:(https://www.zhihu.com/topic/19776749/organize/entire?child=\d{8}&parent=\d{8})'
        with open('posturl.txt', 'r', encoding='utf-8')as f:
            fr=f.read()
        list=re.findall(r,fr)
        print("morelist:"+str(len(list)))
        for url in list:
           morelist.add(url)
def geturl(posturl):
    topic = r'"topic",.*?", "(\d{8})'
    getmore = r'"load",.*?", "(\d{8})", "\d{8}'
    post_url1 = 'https://www.zhihu.com/topic/19776749/organize/entire?child=&parent='
    load = r'"load",.*?"", "(\d{8})"]'
    gettopiclist()
    getloadlist()
    getmorelist()
    times = nums['times']
    print("times:" + str(times))
    if times == 50:
        print("休息中")
        time.sleep(30)
        nums['times']=1
    i=random.uniform(1,2)
    time.sleep(i)
    nums['times'] = nums['times'] + 1
    try:
        html = session.post(posturl, headers=headers, data=posts).text
    except:
        html="aaa"
        print("网络错误")
    with open('posturl.txt', 'a', encoding='utf-8')as f:
        f.write("html:"+ html +"\n")
        f.write("*_"*80+"\n")
    getmores= re.findall(getmore,html)
    loads = re.findall(load,html)
    topics = re.findall(topic, html)
    if len(topics)!=0:
        for getsurl in topics:
            if getsurl not in topiclist:
                t = nums['num']
                t = t + 1
                print("数量：" + str(t))
                nums['num'] = t
                print(getsurl)
                topiclist.add(getsurl)
                with open('topic.txt', 'a', encoding='utf-8')as f:
                    f.write(getsurl + ",")
            elif getsurl in topiclist:
                print("重复url:"+getsurl)
    else:
        t = nums['num']
        t = t + 1
        print("数量："+str(t))
        nums['num']=t
        print("400:" + posturl)
        with open('rtopics.txt', 'a', encoding='utf-8')as f:
            f.write("r:"+posturl+",")
    for load in loads:
        if load not in loadlist:
            loadlist.add(load)
            newposturl = post_url1 + str(load)
            print("from网址:"+posturl)
            print("访问load网址" + newposturl)
            with open('posturl.txt', 'a', encoding='utf-8')as f:
                f.write("fromposturl:"+posturl+"\n""newposturl:"+newposturl+"\n")
            geturl(newposturl)
        elif load in loadlist:
            print("重复load:" + load)
    for getmore in getmores:
        moreposturl = 'https://www.zhihu.com/topic/19776749/organize/entire?child=' + str(
               getmore) + '&parent=' + str(topics[0])
        if moreposturl not in morelist:
            morelist.add(moreposturl)
            print("加载")
            print("网址" + posturl)
            print("访问moreposturl网址" + moreposturl)
            with open('posturl.txt', 'a', encoding='utf-8')as f:
                 f.write("fromposturl:"+posturl+"\n"+"moreposturl:"+moreposturl+"\n")
            geturl(moreposturl)
        else:
            print("重复加载更多")
def get_top():
    r=r'r:(.*?),'
    with open('rtopics.txt', 'r', encoding='utf-8')as f:
        s=f.read()
    links = re.findall(r,s)
    for link in links:
        print("link:"+str(link))
        print("linklen:"+str(len(links)))
        geturl(link)
if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
        get_top()
    else:
        login()
