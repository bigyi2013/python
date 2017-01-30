import requests
import re
import re
import time
import os.path
from PIL import Image
import http.cookiejar as cookielib
import random
# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent,
    'Origin':'https://www.zhihu.com'
}
proxies = {
  #'http': 'http://61.174.10.22',
  'https': 'http://58.249.55.222',
#'https': 'http://58.252.73.14',
#'https': 'http://112.91.208.78',
}
# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
    print("加载cookie")
except:
    print("Cookie 未能加载")
def get_xsrf(html):
    '''_xsrf 是一个动态变化的参数'''
    pattern = r'name="_xsrf" value="(.*?)"'
    # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern, html)
    try:
        return _xsrf[0]
    except:
        print(html)
def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    time.sleep(2)
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False
def get_captcha():
    time.sleep(2)
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url,headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    im = Image.open('captcha.jpg')
    im.show()
    captcha = input("please input the captcha\n>")
    im.close()
    return captcha
def get_captchacn():
    time.sleep(2)
    t = str(int(time.time() * 1000))
    captchacn_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login&lang=cn"
    r = session.get(captchacn_url,headers=headers)
    with open('captchacn.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    im = Image.open('captchacn.jpg')
    im.show()
    captchacn = input("please input the captcha\n>")
    im.close()
    return captchacn
def login():
    post_url = 'http://www.zhihu.com/login/email'
    get_url='http://www.zhihu.com'
    postdata = {
        'password': "1q2wspider",
        'email':"zhispiderhu@163.com",
        'remember_me': 'true',
    }
    try:
        # 不需要验证码直接登录成功
        time.sleep(2)
        index_page = session.get(get_url, headers=headers)
        html = index_page.text
        postdata["_xsrf"] = get_xsrf(html)
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.text
        print(login_page.status_code)
        print(login_code)
        #print(login_code['msg'])
    except :
        # 需要输入验证码后才能登录成功
        #判断验证码类型
        try:
            print("判断验证码类型：")
            time.sleep(2)
            index_page = session.get(post_url, headers=headers)
            html = index_page.text
            print(html)
            postdata["_xsrf"] = get_xsrf(html)
            pattern = r'name="captcha" required data-rule-required="true" data-msg-required="(.*?)"'
            captcha = re.findall(pattern, html)
            if captcha[0]=="请点击图中倒立的文字":
                print("文字验证码：")
                postdata["captcha_type"] = "cn"
                i = get_captchacn()
                m_m = random.randint(-5, 5)+0.5
                n_n = random.randint(-5, 5)+0.5
                m = (int(i) // 10)*20-m_m
                n = (int(i) % 10)*20-n_n
                print(m, n, m_m, n_n)
                k = random.randint(23, 27)
                l = random.randint(23, 27)
                print(k, l)
                if int(i)<=10:
                    m=int(i)*20-m_m
                    postdata["captcha"] = '{"img_size":[200,44],"input_points":[[' + str(m) + ',' + str(k) + '.6094]]}'
                else:
                    postdata["captcha"] = '{"img_size":[200,44],"input_points":[[' + str(m) + ',' + str(k) + '.6094],[' + str(
                        n) + ',' + str(l) + '.6094]]}'
                time.sleep(2)
                print( postdata["captcha"])
                print(postdata)
                login_page = session.post(post_url, data=postdata, headers=headers)
                login_code = login_page.text
                print(login_code)
        except:
            print("字母验证码")
            time.sleep(2)
            postdata["captcha"] = get_captcha()
            time.sleep(2)
            print( postdata)
            login_page = session.post(post_url, data=postdata, headers=headers)
            login_code = login_page.text
            print(login_page.status_code)
            print(login_code)
            if login_page.status_code ==403:
                postdata["captcha"] = get_captcha()
                time.sleep(2)
                login_page = session.post(post_url, data=postdata, headers=headers)
                login_code = login_page.text
                print(login_page.status_code)
                print(login_code)
            #print(login_code)
            #print(login_code['msg'])
    session.cookies.save()

if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
    else:
        print("开始登陆：")
        login()
