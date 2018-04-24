# -*- coding: utf-8 -*-
import json
import random
import time

import scrapy
from scrapy import FormRequest

from lagou_website.items import LagouWebsiteItem

import jsonpath


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    # position=input('请输入要搜索的职位')
    position = "python"
    # city_name=input("请输入要搜索的城市")
    # city_name = "杭州"
    allowed_domains = ['lagou.com']
    # start_urls = ['https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput='.format(position,city_name)]
    # 真实网址：
    # "Request URL: https://www.lagou.com/jobs/positionAjax.json?city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false"
    # city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false"
    start_urls = "https://www.lagou.com/jobs/positionAjax.json?"
    page = 1
    allpage = 0
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '25',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'user_trace_token=20180418150202-393a30a1-6540-4bcb-acf0-da55102cbb0b; _ga=GA1.2.1241225647.1524034926; LGUID=20180418150208-68e1b7f6-42d6-11e8-89fd-525400f775ce; LG_LOGIN_USER_ID=377c5f6e6be86929b034e0b015cffbfcb615e561a3644632; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=3; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAACBHABBI298F961E3ACD99A1154481154DCE646A; _gid=GA1.2.1869587835.1524438157; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1524052619,1524056930,1524190222,1524438157; _putrc=F6032CE1971314B2; login=true; unick=%E6%88%B4%E7%BF%94%E5%AE%87; gate_login_token=7f891ff0a3a779816a3abdf7b81208646e37969d0cdc6d26; LGSID=20180423103004-3af9acab-469e-11e8-b986-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; TG-TRACK-CODE=search_code; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1524451274; LGRID=20180423104222-f2f321a9-469f-11e8-954f-525400f775ce; SEARCH_ID=a57e205676364152acc701fdb91ee796',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.lagou.com/jobs/list_python?city=%E6%9D%AD%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def start_requests(self):

        yield FormRequest(
            # method='post',
            self.start_urls,
            headers=self.headers,
            formdata={
                'first': 'false',
                'pn': str(self.page),
                'kd': self.position,
                # 'city': self.city_name,
            },
            callback=self.parse

        )

    def parse(self, response):
        # item=LagouWebsiteItem()
        # print(response.body)
        # content_list = response.body.decode('utf-8')
        # data = json.loads(content_list)
        # print(data)

        # data = re.findall('"companyId":.*?,"workYear":"(.*?)","education":"(.*?)","city":"(.*?)","positionName":"(.*?)","companyLogo":".*?","companyShortName":"(.*?)","positionLables":.*?,"industryLables":.*?,"businessZones":.*?,"score":.*?,"approve":.*?,"jobNature":".*?","companyLabelList":(.*?),"publisherId":.*?,"district":"(.*?)","companySize":".*?","createTime":".*?","positionAdvantage":".*?","salary":"(.*?)"',data)
        # print(data)
        item = LagouWebsiteItem()

        data = json.loads(response.body.decode('utf-8'))
        result = data['content']['positionResult']['result']
        # result = jsonpath.jsonpath(data, '$..result')[0]
        totalCount = data['content']['positionResult']['totalCount']
        resultSize = data['content']['positionResult']['resultSize']
        for each in result:
            item['city'] = each['city']
            item['companyFullName'] = each['companyFullName']
            item['companyLabelList'] = each['companyLabelList']
            item['companySize'] = each['companySize']
            item['district'] = each['district']
            item['education'] = each['education']
            item['financeStage'] = each['financeStage']
            item['linestaion'] = each['linestaion']
            item['positionName'] = each['positionName']
            item['jobNature'] = each['jobNature']
            item['salary'] = each['salary']
            item['industryField'] = each['industryField']
            item['positionAdvantage'] = each['positionAdvantage']
            item['positionLables'] = each['positionLables']
            item['createTime'] = each['createTime']
            item['workYear'] = each['workYear']
            item['secondType'] = each['secondType']
            item['firstType'] = each['firstType']
            yield item

        time.sleep(random.randint(5, 20))

        if int(resultSize):
            self.allpage = int(totalCount) / int(resultSize) + 1
            if self.page < self.allpage:
                self.page += 1
                yield FormRequest(self.start_urls, headers=self.headers,
                                  formdata={
                                      'first': 'false',
                                      'pn': str(self.page),
                                      'kd': 'Python',
                                      # 'city': '杭州'
                                  }, callback=self.parse
                                  )
