# -*- coding:utf-8 -*-
# @Date   : 2018/4/10 0023
# @Author : Dylan
# @File   : lagou_website.py
import random
import re
import time

import requests

from retrying import retry
class LaGouSpider():
    def __init__(self):
        self.FormData = {
            'first': 'true',
            'pn': 1,
            'kd': 'python',
        }
        # Request headers
        #         hd = """
        #         Accept: application/json, text/javascript, */*; q=0.01
        # Accept-Encoding: gzip, deflate, br
        # Accept-Language: zh-CN,zh;q=0.9
        # Cache-Control: no-cache
        # Connection: keep-alive
        # Content-Length: 25
        # Content-Type: application/x-www-form-urlencoded; charset=UTF-8
        # # Cookie: user_trace_token=20180418150202-393a30a1-6540-4bcb-acf0-da55102cbb0b; _ga=GA1.2.1241225647.1524034926; LGUID=20180418150208-68e1b7f6-42d6-11e8-89fd-525400f775ce; LG_LOGIN_USER_ID=377c5f6e6be86929b034e0b015cffbfcb615e561a3644632; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=3; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAACBHABBI298F961E3ACD99A1154481154DCE646A; _gid=GA1.2.1869587835.1524438157; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1524052619,1524056930,1524190222,1524438157; _putrc=F6032CE1971314B2; login=true; unick=%E6%88%B4%E7%BF%94%E5%AE%87; gate_login_token=7f891ff0a3a779816a3abdf7b81208646e37969d0cdc6d26; LGSID=20180423103004-3af9acab-469e-11e8-b986-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; TG-TRACK-CODE=search_code; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1524451274; LGRID=20180423104222-f2f321a9-469f-11e8-954f-525400f775ce; SEARCH_ID=a57e205676364152acc701fdb91ee796
        # Host: www.lagou.com
        # Origin: https://www.lagou.com
        # Pragma: no-cache
        # Referer: https://www.lagou.com/jobs/list_python?city=%E6%9D%AD%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=
        # User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36
        # X-Anit-Forge-Code: 0
        # X-Anit-Forge-Token: None
        # X-Requested-With: XMLHttpRequest
        # """
        #         hd = hd.strip().split('\n')
        #         self.headers = {x.split(':')[0]: x.split(':')[1] for x in hd}

        # 真实网址：
        "Request URL: https://www.lagou.com/jobs/positionAjax.json?city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false"
        self.start_url="https://www.lagou.com/jobs/positionAjax.json?city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false"
        # self.start_url="https://www.lagou.com/jobs/list_python?city=%E6%9D%AD%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput="
        self.headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Length': '25',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        #'Cookie': 'user_trace_token=20180418150202-393a30a1-6540-4bcb-acf0-da55102cbb0b; _ga=GA1.2.1241225647.1524034926; LGUID=20180418150208-68e1b7f6-42d6-11e8-89fd-525400f775ce; LG_LOGIN_USER_ID=377c5f6e6be86929b034e0b015cffbfcb615e561a3644632; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=3; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAACBHABBI298F961E3ACD99A1154481154DCE646A; _gid=GA1.2.1869587835.1524438157; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1524052619,1524056930,1524190222,1524438157; _putrc=F6032CE1971314B2; login=true; unick=%E6%88%B4%E7%BF%94%E5%AE%87; gate_login_token=7f891ff0a3a779816a3abdf7b81208646e37969d0cdc6d26; LGSID=20180423103004-3af9acab-469e-11e8-b986-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; TG-TRACK-CODE=search_code; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1524451274; LGRID=20180423104222-f2f321a9-469f-11e8-954f-525400f775ce; SEARCH_ID=a57e205676364152acc701fdb91ee796',
                        'Host': 'www.lagou.com',
                        'Origin': 'https',
                        'Pragma': 'no-cache',
                        'Referer': 'https://www.lagou.com/jobs/list_python?city=%E6%9D%AD%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
                        'X-Anit-Forge-Code': '0',
                        'X-Anit-Forge-Token': 'None',
                        'X-Requested-With': 'XMLHttpRequest'}
    def get_proxy(self):
        return requests.get("http://123.207.35.36:5010/get").text
    @retry(stop_max_attempt_number=3)
    def parse_url(self,get_proxy):

        html_str=requests.post(self.start_url,headers=self.headers,data=self.FormData,proxies={"http":"http:{}".format(get_proxy)}).text
        return html_str
    def get_content_list(self,html_str):
        print(html_str)
        content_list = re.findall('"companyId":.*?,"workYear":"(.*?)","education":"(.*?)","city":"(.*?)","positionName":"(.*?)","companyLogo":".*?","companyShortName":"(.*?)","positionLables":.*?,"industryLables":.*?,"businessZones":.*?,"score":.*?,"approve":.*?,"jobNature":".*?","companyLabelList":(.*?),"publisherId":.*?,"district":"(.*?)","companySize":".*?","createTime":".*?","positionAdvantage":".*?","salary":"(.*?)"',html_str)
        return content_list
    def to_csv(self,content_list):
        with open("lagoujob.csv",'a+',encoding="utf-8") as f:
            # f.write(content_list)   #argument must be str, not list
            f.write("".join(content_list))   #argument must be str, not list
    def main(self):
        for i in range(1,31):

            get_proxy=self.get_proxy()
            print(get_proxy)
            try:
                html_str=self.parse_url(get_proxy)
                content_list=self.get_content_list(html_str)

                self.to_csv(content_list)
                time.sleep(random.randint(2, 10))
            except Exception as e:
                print("html_str is %s",e)






if __name__ == '__main__':
    lagou = LaGouSpider()
    lagou.main()

