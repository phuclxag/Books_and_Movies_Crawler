import pandas as pd
data = pd.read_csv('output.csv')

url = []
for name in data['name'].values:
    search_link = "https://www.imdb.com/search/title/?title=" + name
    search_link = search_link.replace(" ","+")
    url.append(search_link)

from scrapy import Spider
from scrapy.crawler import CrawlerProcess
class MySpider(Spider):
    name = 'imdb'
    allowed_domains = ['https://www.imdb.com']
    start_urls = url
    def parse(self, response):
        table = response.xpath('//*[@id="main"]/div/div[3]')
        yield{
            'movie_name' : table.xpath('div/div[1]/div[3]/h3/a//text()').extract(), 
            'movie_link' : table.xpath('div/div[1]/div[3]/h3/a/@href').extract(),
        }
        
process = CrawlerProcess(settings={
    "FEEDS": {
        "imdb_link.csv": {"format": "csv"},
    },
})
process.crawl(MySpider)
process.start()



