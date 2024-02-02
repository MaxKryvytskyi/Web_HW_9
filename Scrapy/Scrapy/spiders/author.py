import scrapy
# from scrapy.crawler import CrawlerProcess

class AuthorSpider(scrapy.Spider):
    name = "author"
    custom_settings = {"FEED_FORMAT" : "json", "FEED_URI" : "Load_mongoDB/author.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    author_url = []
    

    def parse(self, response):
        datas = response.xpath("/html//div[@class='quote']/span/a/@href").extract()
        self.author_url.extend(datas)
        next_page = response.xpath("/html//li[@class='next']/a/@href").get()
        if next_page:
            yield scrapy.Request(url=self.start_urls[0]+next_page)
        else:
            for url in self.author_url:
                yield scrapy.Request(url=self.start_urls[0]+url, callback=self.parse_author_info)

    def parse_author_info(self, response):
        yield {"fullname" : response.xpath("/html//h3[@class='author-title']/text()").extract(),             
               "born_date" : response.xpath("/html//span[@class='author-born-date']/text()").extract(),
               "born_location" : response.xpath("/html//span[@class='author-born-location']/text()").extract(),
               "description" : response.xpath("/html//div[@class='author-description']/text()").extract()}

# process = CrawlerProcess()
# process.crawl(AuthorSpider)
# process.start()