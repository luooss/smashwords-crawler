# coding:utf-8
 
import queue
import threading
 
import requests
from bs4 import BeautifulSoup
 
 
class ProxyGetter:
    def __init__(self, num=300):
        # num 代表爬取代理地址的数目，默认为全部爬取，也就是300.
        self.num = num
        self.url = "https://free-proxy-list.net/"
        # 伪装response的header
        self.header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        self.q = queue.Queue()
        self.Lock = threading.Lock()
 
    def get_ips(self):
        # 把爬取的代理地址存储在当前文件夹list.txt文件中。
        with open("list.txt", "w") as l:
            res = requests.get(self.url, headers=self.header)
            soup = BeautifulSoup(res.text, 'lxml')
            a = soup.find_all('tbody')[0].find_all('tr')
            count = 0
            for element in a:
                if count < self.num:
                    ips = element.find_all('td')
                    if ips[6].getText() == 'yes':
                        # 合并爬取到的ip和端口，写成 https://xxx.xxx.xxx.xxx:xxxx 的形式。
                        ip_temp = "https://" + ips[0].contents[0] + ":" + ips[1].contents[0]
                    else:
                        ip_temp = "http://" + ips[0].contents[0] + ":" + ips[1].contents[0]
                    self.q.put(str(ip_temp))
                    l.write(ip_temp + "\n")
                    count += 1
        l.close()
 
    
 
if __name__ == '__main__':
    ProxyGetter().get_ips()

