# -*- coding: utf-8 -*-
import scrapy
import csv


class DutchPlatesSpider(scrapy.Spider):
    name = 'dutch_plates'
    allowed_domains = ['ovi.rdw.nl']
    start_urls = ['http://ovi.rdw.nl/']

    def start_requests(self):
        with open('car_reg.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            url = 'https://ovi.rdw.nl/'
            for plate in csv_reader: 
                yield FormRequest(url, callback=self.parse, formdata=row) ????? 



    def parse(self, response):        
        yield {
            'plate': plate,
            'taxi': response.xpath("//div[@id='BijzonderheidTekst']/text()").get(),
            'brand': response.xpath("//div[@id='Merk']/text()").get(),
            'color': response.xpath("//div[@id='Kleur']/text()").get(),
            'model': response.xpath("//div[@id='Handelsbenaming']/text()").get()
        }



