t=b'{"msg": [["topic", "\u300c\u6839\u8bdd\u9898\u300d", "19776749"], [[["topic", "\u751f\u6d3b\u3001\u827a\u672f\u3001\u6587\u5316\u4e0e\u6d3b\u52a8", "19778317"], [[["load", "\u663e\u793a\u5b50\u8bdd\u9898", "", "19778317"], []]]], [["topic", "\u5b9e\u4f53", "19778287"], [[["load", "\u663e\u793a\u5b50\u8bdd\u9898", "", "19778287"], []]]], [["topic", "\u4ea7\u4e1a", "19560891"], [[["load", "\u663e\u793a\u5b50\u8bdd\u9898", "", "19560891"], []]]], [["topic", "\u5b66\u79d1", "19618774"], [[["load", "\u663e\u793a\u5b50\u8bdd\u9898", "", "19618774"], []]]], [["topic", "\u300c\u672a\u5f52\u7c7b\u300d\u8bdd\u9898", "19776751"], [[["load", "\u663e\u793a\u5b50\u8bdd\u9898", "", "19776751"], []]]], [["topic", "\u300c\u5f62\u800c\u4e0a\u300d\u8bdd\u9898", "19778298"], [[["load", "\u663e\u793a\u5b50\u8bdd\u9898", "", "19778298"], []]]]]], "r": 0}'
print(type(t))
print(t)
td=t.decode('utf-8')
print(type(td))
print(td)
tde=td.encode('utf-8')
print(type(tde))
print(tde)
import re
#导入MySQL驱动:
import mysql.connector
def pushvalues(key):
    conn = mysql.connector.connect(user='root', password='1q2wreader', database='zhihu')
    cursor = conn.cursor()
    cursor.execute('select msg from urlmsg where id = %s  ', (key,))
    value = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    print(len(value))
    f=str(value[0][0])
    print(f)
    # t = []
    # for i in range(0,90000):
    #     try:
    #         t.append(f[i])
    #     except:
    #         pass
    # print(t)
    # f=''.join(t)
    # print(type(f))
    # print(f)
pushvalues(1)
