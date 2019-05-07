import os
import sqlite3
import requests
import win32crypt
from bs4 import BeautifulSoup
import re
import webbrowser

def get_chrome_cookies(url):
    cookiepath = os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data\Default\Cookies")
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
soup = BeautifulSoup(x.content, 'html.parser')

nonetop_torrents = soup.find_all('tbody', class_="")
free_torrents=[]
for i in nonetop_torrents:
    str_nonetop_torrents=str(i)
    free_torrent=re.findall(r'<img src="./static/image/bt/free.gif"/>', str_nonetop_torrents)
    if(free_torrent):
        download_tid=re.findall(r'tid=\d+', str_nonetop_torrents)
        download_link='http://rs.xidian.edu.cn/bt.php?mod=download&id='+download_tid[0][4:]
        free_torrents.append(download_link)
        #print(download_link)
for i in free_torrents:
    webbrowser.open(i)

