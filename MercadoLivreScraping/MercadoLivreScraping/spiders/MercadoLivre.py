# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import FormRequest
from scrapy.selector import Selector
import unicodedata

class MercadolivreSpider(scrapy.Spider):
    name = 'MercadoLivre'
    allowed_domains = ['mercadolivre.com.br']
    start_urls = ['http://mercadolivre.com.br/']

    def remove_accents(self, input_str):
    	nfkd_form = unicodedata.normalize('NFKD', input_str)
    	only_ascii = nfkd_form.encode('ASCII', 'ignore')
    	return only_ascii

    def parse(self, response):
        search_string = 'celular'
        yield FormRequest.from_response(response, formxpath='//form[@class="nav-search"]', formdata={'as_word':search_string},callback=self.parseSearchPage)

    def parseSearchPage(self, response):
    	for product_elem in response.css('li.results-item'):
    		link = product_elem.css('div.item__info-container h2.item__title a::attr(href)').extract_first()
    		yield response.follow(link, self.parseProduct)

    def parseProduct(self, response):
    	url = response.url
    	name = response.xpath('//header[@class="item-title"]/h1/text()').extract_first().replace('\n','').replace('\t','')
    	description = '\n'.join(response.css('div.item-description__content div p::text').extract())

    	specs = response.css('section.vip-section-specs div.specs-wrapper section ul li').extract()
    	brand = None
    	features = {}
    	dimensions = {}
    	if specs is not None:
    		for li in specs:
    			li = Selector(text=li)
    			spec_name = li.css('Strong::text').extract_first().lower()
    			spec_name = self.remove_accents(spec_name).decode("utf-8") .replace(' ', '_')
    			feature = li.css('span::text').extract_first()
    			features[spec_name] = feature
    			if spec_name == "marca":
    				brand = feature
	    		'''if spec_name == "dimensoes":
	    			dimensoes = re.match(r'([0-9.]* [a-z ]*)x([0-9.]* [a-z ]*)x([0-9.]* [a-z ]*)', feature)
	    			if dimensoes is not None:
	    				dimensoes = dimensoes.groups()
	    			else:
	    				print("*************************************")
	    				print(url, feature)
	    				print("*************************************")
	    			if(len(dimensoes) >= 3):
	    				dimensions['largura'] = dimensoes[0]
	    				dimensions['altura'] = dimensoes[1]'''
	    		if spec_name == "peso":
	    			dimensions['peso'] = feature
	    		if spec_name == "largura":
	    			dimensions['largura'] = feature
	    		if spec_name == "altura":
	    			dimensions['altura'] = feature

    	yield None
