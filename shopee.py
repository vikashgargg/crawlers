import scrapy
from scrapy_splash import SplashRequest

class LaptopSpider(scrapy.Spider):
    name = 'shopee'
    def start_requests(self):
        url ='https://shopee.sg/Akashi-Tai-Daiginjo-Genshu-720ml-i.450865962.9960810031'
        yield SplashRequest(url)        

    def parse(self, response):
            yield {
                'name': response.xpath('//div[@class="attM6y"]/span/text()').get(),
                'price': response.css('div.class="_3e_UQT::text').get(),
                'description': response.xpath('//div[@class="_3yZnxJ"]/span/text()').get(),
                # 'Brand': response.css('.sc-13n2dsm-1.jLtMNk::text').get(),
            }