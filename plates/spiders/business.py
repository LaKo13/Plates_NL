import scrapy
from scrapy.http import FormRequest
import csv
import logging
import time


def get_business():
    businesses = []
    line = 0
    with open('company_reg.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for business in csv_reader:
            if line == 0:
                line += 1
            businesses.append(business[0])
    return businesses




class BusinessRegisterSpider(scrapy.Spider):
    name = 'register'
    allowed_domains = ['kvk.nl']

    start_urls = ['https://kvk.nl/zoeken/handelsregister/?handelsnaam=&kvknummer=&straat=&postcode=&huisnummer=&plaats=&hoofdvestiging=1&rechtspersoon=1&nevenvestiging=1&zoekvervallen=0&zoekuitgeschreven=1&start=0']

    businesses = get_business()
    print(businesses)


    def parse(self, response):
        for links in self.businesses:
            search = "http://kvk.nl/zoeken/handelsregister/?handelsnaam=&kvknummer="  + str(links) +  "&straat=&postcode=&huisnummer=&plaats=&hoofdvestiging=1&rechtspersoon=1&nevenvestiging=1&zoekvervallen=0&zoekuitgeschreven=1&start=0"
            yield scrapy.Request(url=search, callback=self.parse_item)

    def parse_item(self, response):
        yield {
            'Button': response.xpath("//button[@name='zoeken']/font/font/text()").extract(),
            'Title': response.xpath("//div[@class='more-search-info']/p/font/font/text()").get(),
            'Name': response.xpath("//div[@class='handelsnaamHeaderWrapper']/h3/a/font/font/text()").get()
        }


# scrapy crawl crawl-name --set HTTPCACHE_ENABLED=False