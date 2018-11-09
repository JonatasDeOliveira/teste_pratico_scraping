# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
import unicodedata
import numpy as np
from MercadoLivreScraping.items import MercadoLivreItem

class MercadolivreSpider(scrapy.Spider):
	name = 'MercadoLivre'
	allowed_domains = ['mercadolivre.com.br']
	start_urls = ['http://mercadolivre.com.br/']

	def remove_accents(self, input_str):
		nfkd_form = unicodedata.normalize('NFKD', input_str)
		only_ascii = nfkd_form.encode('ASCII', 'ignore')
		return only_ascii

	def parse(self, response):
		return self.parseHomePage(response)

	def parseHomePage(self,response):
		search_strings = ['celular','geladeira','cubo']
		for search_string in search_strings:
			yield FormRequest.from_response(response, formxpath='//form[@class="nav-search"]', formdata={'as_word':search_string},callback=self.parseSearchPage)

	def parseSearchPage(self, response):
		for product_elem in response.css('li.results-item').extract():
			product_elem = Selector(text=product_elem)
			link = product_elem.css('div.item__info-container h2.item__title a::attr(href)').extract_first()
			yield response.follow(link, self.parseProduct)
		
		'''next_page = response.css('div.pagination__container ul.andes-pagination li.andes-pagination__button--next a::attr(href)').extract_first()
		if next_page is not None:
			yield response.follow(next_page, self.parseSearchPage)'''

	def parseProduct(self, response):
		url = response.url
		name = response.xpath('//header[@class="item-title"]/h1/text()').extract_first().replace('\n','').replace('\t','')
		description = '\n'.join(response.css('div.item-description__content div p::text').extract())
		
		navs = response.css('div.vip-navigation-breadcrumb ul.vip-navigation-breadcrumb-list li').extract()
		navigation = []
		for li in navs:
			li = Selector(text=li)
			nav = li.css('a::text').extract_first()
			if nav is not None:
				nav = nav.replace('\n','').replace('\t','')
				navigation.append(nav)

		seller_name = response.css('div.official-store-container div.official-store-info p.title::text').extract_first()

		item_price = response.css('fieldset.item-price span.price-tag').extract()
		price = None
		old_price = None
		if len(item_price) > 1:
			price = Selector(text=item_price[1]).css('span.price-tag span.price-tag-fraction::text').extract_first()
			price = float(price.replace('.','').replace(',','.'))
			old_price = Selector(text=item_price[0]).css('span.price-tag span.price-tag-fraction::text').extract_first()
			old_price = float(old_price.replace('.','').replace(',','.'))
		else:
			price = Selector(text=item_price[0]).css('span.price-tag span.price-tag-fraction::text').extract_first()
			price = float(price.replace('.','').replace(',','.'))

		main_image = None
		sec_images = []
		galery = response.css('div#gallery_dflt div label').extract()
		for i in range(len(galery)):
			label = Selector(text=galery[i])
			if i == 0:
				main_image = label.xpath('//img/@src').extract_first()
			else:
				sec_images.append(label.xpath('//img/@src').extract_first())

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
					dimensoes = re.match(r'([0-9.a-z ]*)x([0-9.a-z ]*)x([0-9.a-z ]*)', feature)
					if dimensoes is not None:
						dimensoes = dimensoes.groups()
					else:
						dimensoes = []
					if(len(dimensoes) >= 2):
						dimensions['largura'] = dimensoes[0]
						dimensions['altura'] = dimensoes[1]'''
				if spec_name == "peso":
					dimensions['peso'] = feature
				if spec_name == "largura":
					dimensions['largura'] = feature
				if spec_name == "altura":
					dimensions['altura'] = feature

		yield MercadoLivreItem(url=url,name=name,description=description,\
					brand=brand,navigation=navigation,seller_name=seller_name,price=price,\
					old_price=old_price, main_image=main_image, sec_images=sec_images,\
					features=features, dimensions=dimensions)
