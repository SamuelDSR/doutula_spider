import os
import requests
import scrapy
from urllib.parse import urlparse, urljoin, parse_qsl

from gifspider.items import GifspiderItem

class DoutulaSpider(scrapy.Spider):
    name = "doutula"
    allowed_domains = ["doutula.com", "sinaimg.cn"]
    start_urls = ["http://www.doutula.com/photo/list/?page=1"]

    #"www.doutula.com/photo/list?page=<page_num>", currently, max valid page_num is 1362
    max_page_num = 1500

    def parse(self, response):

        for img_selector in response.selector.css("a.col-xs-6.col-sm-3>img[data-original][alt]"):
            item = GifspiderItem()
            item["image_title"] = img_selector.css("::attr(alt)").extract_first()
            item["image_urls"]  = [img_selector.css("::attr(data-original)").extract_first()]
            yield item

        request_url = response.request.url
        query_param = parse_qsl(urlparse(request_url).query)
        next_page_num = int(query_param[0][1]) + 1
        if next_page_num < DoutulaSpider.max_page_num:
            next_page_url = "http://www.doutula.com/photo/list/?page=%d" % next_page_num
            yield  response.follow(next_page_url, callback=self.parse)
