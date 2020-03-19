from scrapy.crawler import CrawlerProcess
from src.scraper.scraper.spiders.rki_spider import RKISpider

process = CrawlerProcess()
process.crawl(RKISpider)
process.start()  # the script will block here until the crawling is finished
