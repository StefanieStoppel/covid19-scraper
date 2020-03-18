import scrapy
from datetime import date
import json
from util.helpers import grouper

class RKISpider(scrapy.Spider):
    name = "rki"
    start_urls = [
        'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html',
    ]

    def parse(self, response):
        filename = 'rki-%s.json' % date.today()
        data = self.create_pandas_dict(response)
        self.create_json(data, filename)

    def create_pandas_dict(self, response):
        data = dict()
        header = self.parse_table_header(response)
        table_body = self.parse_table_body(response)
        data["columns"] = header
        data["index"] = list(table_body.keys())
        data["data"] = list(table_body.values())
        return data

    def create_json(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)
        self.log('Saved file %s' % filename)

    def parse_headings(self, response):
        return response.xpath('//h2[@class="null"]/text()').getall()

    def parse_table_header(self, response):
        table_header = [r.replace('\xad', '') for r in response.xpath('//table/thead/tr/th/text()').getall()]
        table_header.pop(1) # pop unneeded header 'Elektronisch übermittelte Fälle'
        table_header.append(table_header.pop(1)) # move header to end of list
        return table_header

    def parse_table_body(self, response):
        entries_per_row = 6

        counties = [td.xpath('text()').get(default='') for td in response.xpath('//table/tbody/tr/td')]
        table_content = {county_data[0]:county_data[1:] for county_data in grouper(counties, entries_per_row, '')[:-1]}

        totals = [td.xpath('strong/text()').get(default='') for td in response.xpath('//table/tbody/tr/td')][-entries_per_row:]
        table_content[totals[0]] = totals[1:]
        return table_content
