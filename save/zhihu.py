import requests
import time
import random
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path

with open('list2.txt', 'r', encoding='utf-8')as f:
    a = re.findall(r',',f.read())
    print(len(a))