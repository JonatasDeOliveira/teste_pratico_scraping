# -*- coding: utf-8 -*-
import scrapy


class MercadolivrespiderSpider(scrapy.Spider):
    name = 'MercadoLivreSpider'
    allowed_domains = ['mercadolivre.com.br']
    start_urls = ['http://mercadolivre.com.br/']

    def parse(self, response):
    	search_string = 'celular'
    	yield FormRequest.from_response(response,
                                        formxpath='//form[@class="nav-search"]',
                                        formdata={"as_word": search_string},
                                        callback=self.parseSearchPage)

    def parseSearchPage(self, response):
    	for product_elem in response.css('li[class="results-item"]').extract():
    		print(product_elem.css('span[class="main-title"]::text').extract_first())

    	yield None

