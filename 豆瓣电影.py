import requests
import time
import random
from fake_useragent import UserAgent
import json
import re


class DoubanSpider(object):
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'
        self.i = 0

    # 获取响应内容
    def get_html(self,url):
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url,headers=headers).text
        return html

    # 解析提取数据
    def parse_html(self,url):
        html = self.get_html(url)
        html = json.loads(html)
        item = {}
        for film in html:
            item['name'] = film['title']
            item['score'] = film['score']
            item['time'] = film['release_date']
            print(item)
            self.i += 1

    # 获取电影总数
    def get_total(self,types):
        url = 'https://movie.douban.com/j/chart/top_list_count?type={}&interval_id=100%3A90'.format(types)
        html = json.loads(self.get_html(url))
        total = html['total']
        return total

    # 获取所有类型的字典
    def get_types_dict(self):
        url = 'https://movie.douban.com/chart'
        html = self.get_html(url)
        p = re.compile('<span><a href=".*?type_name=(.*?)&type=(.*?)&interval_id=100:90&action=">.*?</span>',
                       re.S)
        r_list = p.findall(html)
        types_dict = {}
        for r in r_list:
            types_dict[r[0]] = r[1]
        return types_dict

    def run(self):
        types_dict = self.get_types_dict()
        menu = ''
        for key in types_dict:
            menu = menu + key + '|'
        print(menu)
        typ = input('请输入电影类型： ')
        types = types_dict[typ]
        total = self.get_total(types)
        for start in range(0,total,20):
            url = self.url.format(types,start)
            self.parse_html(url)
            time.sleep(random.uniform(0,1))
        print('总数： ',self.i)

if __name__ == '__main__':
    spider = DoubanSpider()
    spider.run() 



