#Importing
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
url = []
for i in range(1,93):
    a = 'https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century?page={}'.format(i)
    url.append(a)
class MySpider(Spider):
    name = 'book'
    allowed_domains = ['https://www.goodreads.com']
    start_urls = url

    def parse(self, response):
        table = response.xpath('//*[@id="all_votes"]')
        rows = table.xpath('//tr')
        for row in rows:
            yield{
            'name' : row.xpath('td[3]/a/span//text()').extract(),  
            'link' : row.xpath('td[3]/a//@href').extract()
            }


###CrawlerRunner can run mutiple times

# process = CrawlerProcess(settings={
#     "FEEDS": {
#         "output.csv": {"format": "csv"},
#     },
# })
# process.crawl(MySpider)
# process.start()

runner = CrawlerRunner(settings={
    "FEEDS": {
        "output.csv": {"format": "csv"},
    },
})

d = runner.crawl(MySpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()
