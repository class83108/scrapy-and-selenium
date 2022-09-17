import sys

from fake_useragent import UserAgent
from selenium import webdriver
from hashlib import md5

import time
import redis
import pymysql
import csv


class NativeSpider:
    def __init__(self):
        self.ua = UserAgent().random
        #無頭模式
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        #解決無頭造成0*0時 xpath抓不到
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--start-maximized')
        self.options.add_argument("user-agent={}".format(self.ua))
        self.url = 'https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/ccd=TUzFwO/search?mode=basic'
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.driver.get(url = self.url)
        #redis去重
        self.r = redis.Redis(host = 'localhost', port =6379, db = 0)
        #mysql持久化
        self.db = pymysql.connect(host='localhost', user='root', password='a123456', database='scrapy_info', charset='utf8')
        self.cur = self.db.cursor()
        #打開檔案跟創建csv寫入對象
        self.f = open('native_zaki','w', newline='')
        self.writer = csv.writer(self.f)


    def get_html(self):
        """找到條件欄位點擊　輸入關鍵字後點擊"""
        time.sleep(10)
        print('get_html start')
        self.driver.find_element_by_xpath('//*[@id="ALLFIELD_不限欄位"]').click()
        self.driver.find_element_by_xpath('//*[@id="ysearchinput0"]').send_keys('石岐雞')
        self.driver.find_element_by_xpath('//*[@id="gs32search"]').click()
        #預留加載頁面時間
        time.sleep(3)
        print('get_html close')
    def arrangement(self):
        """再次調整搜尋順序"""
        time.sleep(10)
        print('arrangement start')
        self.driver.find_element_by_xpath('//*[@id="research"]').send_keys('石岐雞')
        self.driver.find_element_by_xpath('//*[@id="sortby"]').click()
        self.driver.find_element_by_xpath('//*[@id="sortby"]/option[14]').click()
        self.driver.find_element_by_xpath('//*[@id="researchdivid"]/input').click()
        # 預留加載頁面時間
        time.sleep(10)
        print('arrangement close')

    def md5_title(self, string):
        """功能函式-生成指紋"""
        s = md5()
        s.update(string.encode())
        return s.hexdigest()
    def parse_html(self):
        """解析頁面獲取數據"""
        print('parse start')
        tr_list = self.driver.find_elements_by_xpath('//*[@id="tablefmt1"]/tbody/tr')
        new_tr_list = tr_list[1:]
        for tr in new_tr_list:
            item = {}
            item['title'] = tr.find_element_by_xpath('.//tbody/tr[2]/td/a/span').text
            item['url'] = tr.find_element_by_xpath('.//tbody/tr[2]/td/a').get_attribute('href')
            item['number'] = tr.find_element_by_xpath('./td[2]').text.split('.')[0]
            finger = self.md5_title(item['title'])
            if self.r.sadd('paper_spider', finger) ==1:
                item['message'] = tr.find_element_by_xpath('.//tbody/tr[3]/td').text
                item['author'] = tr.find_element_by_xpath('.//tbody/tr[4]/td').text
                item['adviser'] = tr.find_element_by_xpath('.//tbody/tr[5]/td').text
                #確定資料是新的再進mysql
                self.save_into_mysql(item)
                self.write_csv(item)

            else:
                sys.exit('更新完成，程序退出')
    def save_into_mysql(self, item):
        """功能函式-存入mysql資料庫"""
        ins = 'insert into zaki_article values(%s, %s, %s, %s, %s, %s)'
        li = [
            item['number'],
            item['url'],
            item['title'],
            item['message'],
            item['author'],
            item['adviser'],
        ]
        self.cur.execute(ins, li)
        self.db.commit()
    def write_csv(self, item):
        li = [
            item['title'],
            item['url'],
            item['message'],
            item['author'],
            item['adviser'],
        ]
        self.writer.writerow(li)
        print(li)
    def run(self):
        self.get_html()
        self.arrangement()
        while True:
            self.parse_html()
            if self.driver.page_source.find('//*[@id="bodyid"]/form/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/div[1]/table/tbody/tr[6]/td/table[2]/tbody/tr/td/table/tbody/tr/td[4]/img') == -1:
                try:
                    self.driver.find_element_by_xpath('//*[@id="bodyid"]/form/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/div[1]/table/tbody/tr[6]/td/table[2]/tbody/tr/td/table/tbody/tr/td[4]/input').click()
                except Exception as e:
                    print('Last page')
                    self.driver.quit()
                    self.cur.close()
                    self.db.close()
                    self.f.close()
                    break
                time.sleep(10)
            else:
                self.driver.quit()
                self.cur.close()
                self.db.close()
                self.f.close()
                break
if __name__ == '__main__':
    spider = NativeSpider()
    spider.run()
