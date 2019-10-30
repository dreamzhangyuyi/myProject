# -*- coding: utf-8 -*-
import scrapy


class SnbookSpider(scrapy.Spider):
    name = 'snbook'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com//']

    def parse(self, response):
        categories = response.xpath("//div[@class='left-menu-container']//div[@class='menu-list']//div[@class='menu-item']")

        for category in categories:
            item = {}
            item['firstLevelName'] = category.xpath("./dl/dt/h3/a/text()").extract_first()
            secondLevelCategories = category.xpath("./dl/dd").extract_first()
            for secondLevelCategory in secondLevelCategories:
                item['secondLevelName'] = secondLevelCategory.xpath("./a/text()")
                href = secondLevelCategory.xpath("./a/@href")

                yield scrapy.Request(
                    href,
                    callback=
                )

        print(item)
        
    def parse_list(self, response):
        response
