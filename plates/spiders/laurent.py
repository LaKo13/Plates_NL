# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import csv
import logging
import time

def get_plates():
    plates = []
    line = 0
    with open('car_reg.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for plate in csv_reader:
            if line == 0:
                line += 1
            plates.append(plate[0])
    return plates


class DutchPlatesSpider(scrapy.Spider):
    name = 'dutch_plates'
    allowed_domains = ['ovi.rdw.nl']
    start_urls = ['http://ovi.rdw.nl/']

    plates = get_plates()

    def parse(self, response):
        view_state = response.xpath('//input[@id="__VIEWSTATE"]/@value').get()
        view_state_generator = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').get()
        event_validation = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').get()
        for plate in self.plates:
            yield FormRequest.from_response(
                response,
                formid='aspnetForm',
                formdata={
                    '__VIEWSTATE': view_state,
                    '__VIEWSTATEGENERATOR': view_state_generator,
                    '__EVENTVALIDATION': event_validation,
                    'ctl00$TopContent$txtKenteken': plate
                },
                callback=self.parse_plate,
                meta={
                    'plate': plate
                }
            )
        
        

    def parse_plate(self, response):
        yield {
            'plate': response.meta['plate'],
            'taxi': response.xpath("//div[@id='BijzonderheidTekst']/text()").get(),
            'brand': response.xpath("//div[@id='Merk']/text()").get(),
            'color': response.xpath("//div[@id='Kleur']/text()").get(),
            'model': response.xpath("//div[@id='Handelsbenaming']/text()").get(),
            'user-agent': response.request.headers.get('User-Agent').decode()
        }