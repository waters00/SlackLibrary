#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from ..items import DoubanbookItem


class DoubanBookSpider(scrapy.Spider):
    name = 'douban_book_spider'
    allowed_domains = ['book.douban.com']
    start_urls = [
        'https://book.douban.com/top250'
    ]

    def parse(self, response):
        if 'top250' in response.url:
            books = response.xpath('//a/@href').re('.*book.douban.com/subject/\d+')
            books = list(set(books))

            for book in books:
                yield scrapy.Request(url=book, callback=self.parse)

            next_page = response.xpath('//*[@id="content"]/div/div[1]/div/div/span[3]/a/@href')

            if next_page:
                next_page = next_page.extract()[0]
                yield scrapy.Request(url=next_page, callback=self.parse)

        elif 'subject' in response.url:
            title = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract()[0]
            author = response.xpath('//*[@id="info"]/a/text()').extract()[0].replace(' ', '').replace('\n', '')
            cover = response.xpath('//*[@id="mainpic"]/a/img/@src').extract()[0]

            _description = response.xpath('//*[@id="link-report"]/div[1]/div/p')
            if not _description:
                _description = response.xpath('//*[@id="link-report"]/span[2]/div/div/p')

            description = ''
            for d in _description:
                if d.xpath('text()').extract():
                    description += d.xpath('text()').extract()[0]

            item = DoubanbookItem()

            item['title'] = title
            item['author'] = author
            item['cover'] = cover
            item['description'] = description

            infos = response.xpath("//div[@id='info']//text()").extract()
            infos = [info.strip() for info in infos]
            infos = [info for info in infos if info != ""]

            for info in infos:
                if u"出版社:" in info:
                    item["press"] = infos[infos.index(info) + 1]
                elif u"定价:" in info:
                    item["price"] = infos[infos.index(info) + 1]
                elif u"ISBN:" in info:
                    item["ISBN"] = infos[infos.index(info) + 1]

            yield item
