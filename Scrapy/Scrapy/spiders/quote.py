import scrapy
# from scrapy.crawler import CrawlerProcess

class QuoteSpider(scrapy.Spider):
    name = "quote"
    custom_settings = {"FEED_FORMAT" : "json", "FEED_URI" : "Load_mongoDB/quote.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]


    def parse(self, response):
        datas = response.xpath("/html//div[@class='col-md-8']/div")
        for data in datas:
            yield { "tags": [data.xpath("div[@class='tags']/a/text()").extract()],
                    "author": data.xpath("span/small[@class='author']/text()").extract()[0],
                    "quote": data.xpath("span[@class='text']/text()").extract()}

        next_page = response.xpath("/html//li[@class='next']/a/@href").extract()[0]
        if next_page:
            yield scrapy.Request(url=self.start_urls[0]+next_page)

# process = CrawlerProcess()
# process.crawl(QuoteSpider)
# process.start()