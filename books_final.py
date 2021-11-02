import pandas as pd
data = pd.read_csv('output.csv')

for i in range(len(data['link'])):
    link = "https://www.goodreads.com" + data['link'][i]
    data['link'][i] = link

from scrapy.crawler import CrawlerProcess
from scrapy import Spider
class MySpider(Spider):
    name = 'book'
    allowed_domains = ['https://www.goodreads.com']
    start_urls = list(data['link'])[0:10]

    def parse(self, response):
        table = response.xpath('/html/body/div[2]/div[3]')
        link = response.request.url
        yield{
        'title' : (data[data['link'] == link])['name'].values[0],  
        'series' : table.xpath('//*[@id="bookSeries"]/a/text()').extract(),
        'author': table.xpath('//*[@id="bookAuthors"]/span[2]/div/a/span//text()').extract(),
        'book_link': response.request.url,
        'genre' : table.xpath('//*[@class="elementList "]/div/a/text()').extract(),
        'date_published' : table.xpath('//*[@id="details"]/div[2]/text()').extract(),
        'num_of_page' : table.xpath('//span[@itemprop="numberOfPages"]/text()').extract(),
        'lang' : table.xpath('//*[@itemprop="inLanguage"]/text()').extract(),
        'rating_count' : table.xpath('//*[@id="reviewControls"]/div[3]/text()').extract(),
        'rate' : table.xpath('//*[@itemprop="ratingValue"]/text()').extract(),
        'award' : table.xpath('//*[@itemprop="awards"]/a/text()').extract(),
        }

process = CrawlerProcess(settings={
    "FEEDS": {
        "test.csv": {"format": "csv"},
    },
})
process.crawl(MySpider)
process.start()
