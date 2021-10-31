import pandas as pd
data = pd.read_csv('output.csv')

for i in range(len(data['link'])):
    link = "https://goodreads.com" + data['link'][i]
    data['link'][i] = link

from scrapy.crawler import CrawlerProcess
from scrapy import Spider
class MySpider(Spider):
    name = 'book'
    allowed_domains = ['https://www.goodreads.com']
    def __init__(self, url):
        start_urls = url

    def parse(self, response):
        table = response.xpath('//*[@id="all_votes"]')
        rows = table.xpath('//tr')
        for row in rows:
            yield{
            'name' : row.xpath('td[3]/a/span//text()').extract(),  
            'link' : row.xpath('td[3]/a//@href').extract()
            }

process = CrawlerProcess(settings={
    "FEEDS": {
        "test.csv": {"format": "csv"},
    },
})
process.crawl(MySpider)
process.start()

