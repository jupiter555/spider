import time
import random
import requests
from lxml import etree

class XiceHost(object):
    def __init__(self):
        self.url = 'https://www.kuaidaili.com/free/inha/{}'
        self.headers = {'Uers-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}

    def get_html(self,url):
        html = requests.get(url=url,headers=self.headers).content.decode('utf-8','ignore')
        self.parse_html(html)

    def parse_html(self,html):
        bds = '//tr/td[@data-title="IP"]/text() | //tr/td[@data-title="PORT"]/text()'
        p = etree.HTML(html)
        host_list = p.xpath(bds)
        print(host_list)
        i = 0
        for host in host_list:
            with open('host.txt','a+') as f:
                f.write(host + ',')
            i += 1
            if i == 2:
                with open('host.txt', 'a+') as f:
                    f.write('\r\n')
                i = 0
            print(host,' 写入成功')

    def run(self):
        for pn in range(1,100):
            url = self.url.format(pn)
            print(url)
            self.get_html(url)
            time.sleep(random.randint(0,1))

if __name__ == '__main__':
    spider = XiceHost()
    spider.run()