import os
import sqlite3
import requests
import win32crypt
from bs4 import BeautifulSoup
import re

def get_chrome_cookies(url):
    cookiepath = os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome Dev\User Data\Default\Cookies")
    conn = sqlite3.connect(cookiepath)
    sql = 'select host_key, name, encrypted_value, path from cookies'
    if url:
        sql += ' where host_key like "%{}%"'.format(url)
    ret_list = []
    ret_dict = {}
    for row in conn.execute(sql):
        if row[0] != url:
            continue
        ret = win32crypt.CryptUnprotectData(row[2], None, None, None, 0)
        ret_list.append((row[1], ret[1]))
        ret_dict[row[1]] = ret[1].decode()
    conn.close()
    return ret_dict

url = 'http://rs.xidian.edu.cn/bt.php?mod=browse&t=all'
x = requests.session().get(url, cookies=get_chrome_cookies('rs.xidian.edu.cn'))
soup=BeautifulSoup(x.content, 'html.parser')
top_torrents=soup.find_all('tbody')
for i in
    print(i)
#print(top_torrents)
