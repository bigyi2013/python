import re
#导入MySQL驱动:
import mysql.connector

# 注意把password设为你的root口令:
def pushvalues(key,values):
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='zhihu')
    cursor = conn.cursor()
    cursor.execute('select msg from urlmsg where url = %s  ', (key,))
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
        print("conn.commit()")
for i in range(8,9):
    t="floor"+str(i)+".txt"
    print(t)
    with open(t, 'r', encoding='utf-8')as f:
        fr=f.read()
    lists=re.split('\*_\*_\*_\*_\*_\*_\*_\*_\*_\*_',fr)
    print(len(lists))
    post=r'posturl:(https.*?\n)'
    html=r'html:({"msg".*?})'
    for lista in lists:
        try:
            p = re.findall(post, lista)[0]
            h = re.findall(html, lista)[0]
            pushvalues(p, h)
        except:
            pass

# s="https://www.zhihu.com/topic/19776749/organize/entire?child=&parent=19586269"
# def gethtml(value):
#     # 导入MySQL驱动:
#     import mysql.connector
#     # 注意把password设为你的root口令:
#     conn = mysql.connector.connect(user='root', password='1q2wreader', database='zhihu')
#     cursor = conn.cursor()
#     try:
#         cursor.execute('select msg from urlmsg where url = %s  ', (value,))
#         values = cursor.fetchall()
#         # 关闭Cursor和Connection:
#         t=values[0]
#         print(t)
#         print("找到url")
#         return t
#     except:
#         pass
# gethtml(s)
# def gethtml(value):
#     # 导入MySQL驱动:
#     import mysql.connector
#     # 注意把password设为你的root口令:
#     conn = mysql.connector.connect(user='root', password='1q2wreader', database='zhihu')
#     cursor = conn.cursor()
#     try:
#
#         cursor.execute('select msg from urlmsg where moreurl = %s UNION select msg2 from urlmsg2 where moreurl2 = %s  ', (value,value))
#         values = cursor.fetchall()
#         # 关闭Cursor和Connection:
#         t=values[0][0]
#         print("找到more")
#         return t
#     except:
#         try:
#             cursor.execute('select msg from urlmsg where posturl = %s UNION select msg2 from urlmsg2 where posturl2 = %s  ', (value,value))
#             values = cursor.fetchall()
#             # 关闭Cursor和Connection:
#             cursor.close()
#             conn.close()
#             t= values[0][0]
#             print("找到post")
#             return t
#         except:
#             print("访问网络")
#             try:
#                 t= session.post(value, headers=headers, data=posts).text
#             except:
#                 t = "aaa"
#                 print("网络错误")
#             return t
# t="https://www.zhihu.com/topic/19776749/organize/entire?child=&parent=19636112"
# f=gethtml(t)
# print(f)
# import re
# r=r'posturl:'
# with open ('log5.txt','r') as f:
#     fr=f.read()
# t=re.findall(r,fr)
# print(len(t))