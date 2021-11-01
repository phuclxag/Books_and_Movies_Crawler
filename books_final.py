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
    start_urls = list(data['link'])

    def parse(self, response):
        table = response.xpath('/html/body/div[2]/div[3]/div[1]/div[2]')
        yield{
        'title' : table.xpath('div[2]/div[1]/div[2]/h1//text()').extract(),  
        }

process = CrawlerProcess(settings={
    "FEEDS": {
        "test.csv": {"format": "csv"},
    },
})
process.crawl(MySpider)
process.start()

