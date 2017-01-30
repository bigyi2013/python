import re
morelist=set()
def getmorelist():
    if len(morelist)==0:
        r=r'moreposturl:(https://www.zhihu.com/topic/19776749/organize/entire?child=\d{8}&parent=\d{8})'
        with open('posturl.txt', 'r', encoding='utf-8')as f:
            fr=f.read()
        list=re.findall(r,fr)
        print("morelist:"+str(len(list)))
        for li in list:
            print(li)
        for url in list:
           morelist.add(url)