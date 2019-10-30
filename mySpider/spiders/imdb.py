# -*- coding: utf-8 -*-
import scrapy
import re

# from lxml import etree
# import logging

# logger = logging.getLogger(__name__)


class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['imdb.cn']
    start_urls = ['http://www.imdb.cn/IMDB250/']

    def parse(self, response):
        with open('./imdb.html','wb') as f:
            f.write(response.text.encode('utf-8'))
        # endurls = re.findall('<a href="(/p/.*?)" title=',response.text)
        
        # html = etree.HTML(str(response.text))
        # logger.warning(response)
        film_list = response.xpath("//div[@class='ss-3 clear']//a")
        for film in film_list:
            item = {}
            item["href"] = film.xpath("@href").extract_first()
            item["file_name"] = film.xpath("./div[@class='honghe']/div[@class='honghe-1']/div[@class='honghe-2']/div[@class='honghe-3']/p[@class='bb']/text()").extract_first()
            item["rate"] = film.xpath("./div[@class='honghe']/div[@class='honghe-1']/div[@class='honghe-2']/span/i/text()").extract_first()
            item["other_name"] = film.xpath("./div[@class='honghe']/div[@class='honghe-1']/div[@class='honghe-4 clear']/p[1]/i/text()").extract_first()
            item["en_name"] = film.xpath("./div[@class='honghe']/div[@class='honghe-1']/div[@class='honghe-4 clear']/p[2]/text()").extract_first()
            item["director_name"] = film.xpath("./div[@class='honghe']/div[@class='honghe-1']/div[@class='honghe-4 clear']/p[3]/span/text()").extract_first()

            yield scrapy.Request(
                "http://www.imdb.cn{}".format(item["href"]),
                callback=self.parse_detail,
                meta= {"item": item}
            )
        next_url = response.xpath("//div[@class='page-1 clear']/a[1]/@href").extract_first()
        next_tag = response.xpath("//div[@class='page-1 clear']/a[1]/text()").extract_first()
        if next_tag == "下一页":
            yield scrapy.Request(
                "http://www.imdb.cn{}".format(next_url),
                callback=self.parse
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["content"] = response.xpath("//div[@class='fk-4 clear']//div[@class='bdd clear']").extract_first()
        yield item

        
