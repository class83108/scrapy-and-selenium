import scrapy
import datetime
import json
from ..items import EggpriceItem

class MeatEggPriceSpider(scrapy.Spider):
    name = 'meat_egg_price'
    allowed_domains = ['m.coa.gov.tw']
    start_urls = 'https://m.coa.gov.tw/Transaction/PoultryTrans/Index'
    headers = {
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie':'_ga=GA1.3.1206352301.1655809566; _ga_GGFKGXEJ2S=GS1.1.1655809564.1.1.1655809580.0; G_ENABLED_IDPS=google; _gid=GA1.3.468272396.1658336359; .AspNetCore.Antiforgery.idCrnzStY7U=CfDJ8EbUqECCzu9PmB00eZlVJM_jvh3Csqa56RJCQLGU0jOlgVhWgwO5Fgtzt6nGG0vvGE0MT3tEtPF0do-tm4BskmWAs_IqU6t2ARVjreBXZHJn8BfZI-PCoCfLvALMaqowlNfGHHBbIKwI_NaDslrDfmQ; .AspNetCore.Session=CfDJ8EbUqECCzu9PmB00eZlVJM%2FPxzk1Z3BBbemHvTbiL9wh9oa%2FYq2dmjOjCa895A7hed57%2FWkpp31VVV6WrUayCdcDW64A3ITEPMkTiRIH4eM%2FzoLRl7sID7SLfQrfeCdIjrHYDG1V96pXjV%2F9jPQVLIMV8r4qIyaREqdCe62WPKE3; _gat_gtag_UA_154934224_1=1',
    }
    def get_StartDate(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        month = month -1
        day = now.day
        if month == 2 and day == 29:
            day = 28
        StartDate = str("%s/%s/%s"%(str(year),str(month),str(day)))
        return StartDate
    def get_EndDate(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        EndDate = str("%s/%s/%s" % (year, month, day))
        return EndDate
    def start_requests(self):
        StartDate = self.get_StartDate()
        EndDate = self.get_EndDate()
        formdata = {
            'StartDate': StartDate,
            'EndDate': EndDate,
            'DataSource': '1',
            'IsFirstLoad': 'True',
            'NoRest': 'false',
            'NowPage': '1',
            'SortAction': 'DESC',
            'SortField': 'TradeDateTime',
            'PageSize': '20'
        }
        yield scrapy.FormRequest(url=self.start_urls, callback=self.get_all_url, formdata=formdata,headers=self.headers, method='POST', dont_filter=True)
    def get_all_url(self, response):
        html = json.loads(response.text)
        total = html['total']
        StartDate = self.get_StartDate()
        EndDate = self.get_EndDate()
        page_num = total //20 if total %20 == 0 else total //20 +1
        for i in range(1, page_num+1):
            formdata = {
                'StartDate': StartDate,
                'EndDate': EndDate,
                'DataSource': '1',
                'IsFirstLoad': 'True',
                'NoRest': 'false',
                'NowPage': str(i),
                'SortAction': 'DESC',
                'SortField': 'TradeDateTime',
                'PageSize': '20'
            }
            yield scrapy.FormRequest(url=self.start_urls, callback=self.get_all_data, formdata=formdata,headers=self.headers, method='POST', dont_filter=True)
    def get_all_data(self, response):
        html = json.loads(response.text)
        for one in html['rows']:
            item = EggpriceItem()
            item['id'] = one['ID']
            item['date'] = one['TradeDate']
            item['meat_ab2'] = one['Column1Data']
            item['meat_l2'] = one['Column2Data']
            item['meat_south'] = one['Column3Data']
            item['egg'] = one['Column4Data']
            yield item

