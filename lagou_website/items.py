# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouWebsiteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 公司
    companyFullName = scrapy.Field()
    companyLabelList = scrapy.Field()
    # 公司规模
    companySize = scrapy.Field()
    # 地区
    district = scrapy.Field()
    # 融资情况
    financeStage = scrapy.Field()
    # 教育程度
    education = scrapy.Field()
    # 地点
    linestaion = scrapy.Field()
    # 招聘职务
    positionName = scrapy.Field()
    # 招聘要求
    jobNature = scrapy.Field()
    # 工资
    salary = scrapy.Field()
    # 工作经验
    workYear = scrapy.Field()
    # 岗位发布时间
    createTime = scrapy.Field()
    # 行业
    industryField = scrapy.Field()
    firstType = scrapy.Field()
    # 岗位发布
    positionLables = scrapy.Field()
    secondType = scrapy.Field()
    # 职位福利
    positionAdvantage = scrapy.Field()
