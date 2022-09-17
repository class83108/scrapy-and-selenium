import scrapy
from ..items import AiinfoItem


import datetime
import json


class AiSpider(scrapy.Spider):
    name = 'ai'
    allowed_domains = ['m.coa.gov.tw']
    headers = {
        'content-type':'application/x-www-form-urlencoded',
        'cookie':'_ga=GA1.3.1206352301.1655809566; _ga_GGFKGXEJ2S=GS1.1.1655809564.1.1.1655809580.0; G_ENABLED_IDPS=google; _gid=GA1.3.468272396.1658336359; .AspNetCore.Antiforgery.idCrnzStY7U=CfDJ8EbUqECCzu9PmB00eZlVJM_19KetzEhglU4PZ_B0YLszB1tL3JDKjPClF17K5qcCWxE2tXVPHLIjXgsayOY3Iwiik1KxMdqtNJ3Xgfj4p7Hxg4z05Vbb0Lt6oWheo7bcIKLliF--ys5ZqjCXXH1Ejy0; .AspNetCore.Session=CfDJ8EbUqECCzu9PmB00eZlVJM9n3hKteiJLj%2FqcggscHns%2FVN14veUvYn3Rskpc41wRdVNgEI%2BDGGcm3HQFjTHf4ndw0%2Bp2PJvlmxJw95vXQqk0BBNWFqbXGlWDrgLgOcndLtXTpkc6J9UHoLh2q5Is%2BlTS1iq9DVzg4mWUrNgeSNii; _gat_gtag_UA_154934224_1=1'
    }
    def get_StartDate(self):
        now = datetime.datetime.now()
        year = int(now.year)-1
        month = now.month
        day = now.day
        if month == 2 and day == 29:
            day = 28
        StartDate = str("%s/%s/%s"%(str(year),month,str(day)))
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
        form_data = {
            'StartDate':StartDate,
            'EndDate':EndDate,
            'InfoSearch.ByKeyword': '',
            'NowPage':'1',
            'SortAction':'DESC',
            'SortField':'PublishDate',
            'PageSize':'20',
            }
        yield scrapy.FormRequest('https://m.coa.gov.tw/Aigovinfo/Index#', formdata=form_data, callback=self.get_url, headers=self.headers,method='POST', dont_filter=True)
    def get_url(self, response):
        """抓取總數後將所有url入隊列"""
        html = json.loads(response.text)
        StartDate = self.get_StartDate()
        EndDate = self.get_EndDate()
        total = html['total']
        page_number = int(total) // 20 if total %20 ==0 else total //20 +1
        for i in range(1, page_number+1):
            form_data = {
                'StartDate': StartDate,
                'EndDate': EndDate,
                'InfoSearch.ByKeyword': '',
                'NowPage': str(i),
                'SortAction': 'DESC',
                'SortField': 'PublishDate',
                'PageSize': '20',
            }
            yield scrapy.FormRequest('https://m.coa.gov.tw/Aigovinfo/Index', formdata=form_data, callback=self.get_record_id,dont_filter=True,headers=self.headers,method='POST')
    def get_record_id(self, response):
        """從response中抓取record_id"""
        html = json.loads(response.text)
        item = AiinfoItem()
        for one in html['rows']:
            item['id'] = one['Record_ID']
            detail_url = 'https://m.coa.gov.tw/Aigovinfo/Detail/{}'.format(one['Record_ID'])
            item['url'] = detail_url
            yield scrapy.Request(url = detail_url,meta={'item':item}, callback=self.info)
    def info(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('/html/body/div/main/div[2]/section/div/div[2]/div[2]/table/tbody/tr[1]/td/text()').get().strip()
        item['date'] = response.xpath('/html/body/div/main/div[2]/section/div/div[2]/div[2]/table/tbody/tr[2]/td/text()').get().strip()

        yield item


