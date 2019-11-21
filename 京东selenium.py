from selenium import webdriver
import time
import pymongo

class JdSpider(object):
    def __init__(self):
        self.url = 'https://www.jd.com/'
        # 设置无界面
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=self.options)
        # 计数变量
        self.i = 0
        # 存到mongodb
        self.conn = pymongo.MongoClient('localhost',27017)
        self.db = self.conn['jddb']
        self.myset = self.db['jdset']

    # 输入地址+输入内容+点击搜索按钮
    def get_html(self):
        self.browser.get(self.url)
        self.browser.find_element_by_xpath('//*[@id="key"]').send_keys('绝世好剑')
        self.browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
        time.sleep(1)

    # 抓取1页数据
    def parse_html(self):
        # 把进度条拉到最底部并预留时间加载
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        time.sleep(2)
        # 找节点抓数据
        li_list = self.browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')

        for li in li_list:
            item = {}
            try:
                item['name'] = li.find_element_by_xpath('.//div[@class="p-name p-name-type-2"]/a/em | .//div[@class="p-name"]/a/em').text.strip()
                item['price'] = li.find_element_by_xpath('.//div[@class="p-price"]').text.strip()
                item['commit'] = li.find_element_by_xpath('.//div[@class="p-commit"]/strong').text.strip()
                item['shop'] = li.find_element_by_xpath('.//div[@class="p-shopnum"]/a | .//div[@class="p-shopnum"]/span | .//div[@class="p-shop"]/span').text.strip()
                self.i += 1
                print(item)
                # 存入mongodb数据库
                self.myset.insert_one(item)
            except Exception as e:
                item = {}

    def run(self):
        self.get_html()
        while True:
            self.parse_html()
            if self.browser.page_source.find('pn-next disabled') == -1:
                self.browser.find_element_by_class_name('pn-next').click()
                time.sleep(0.5)
            else:
                self.browser.quit()
                break


        print('数量:',self.i)


if __name__ == '__main__':
    spider = JdSpider()
    spider.run()




























