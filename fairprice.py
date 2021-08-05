import scrapy
from scrapy_splash import SplashRequest

class LaptopSpider(scrapy.Spider):
    name = 'fprice'
    def start_requests(self):
        url ='https://www.fairprice.com.sg/product/sasanokawa-shuzo-cherry-ex-whisky-500ml-90016344'
        yield SplashRequest(url)        

    def parse(self, response):
            yield {
                'name': response.css('span.sc-1bsd7ul-1.djlKtC::text').get(),
                'brand': response.css('a.sc-13n2dsm-1.jLtMNk::text').get(),
                'price': response.css('span.sc-1bsd7ul-1.sc-13n2dsm-5.kxEbZl.deQJPo::text').get(),
                # 'description': response.css('div.productDescriptionInnerExpandable').get(),
                # 'Alcohol_percentage': response.xpath('//div[@class="productDescriptionText richtext"]/p[4]/text()').get(),
                'Volume': response.css('span.sc-1bsd7ul-1.LLmwF::text').get(),
                #'Ingredients': response.css('span.sc-1bsd7ul-1.sc-3zvnd-10.kmlJZt.hpuhl::text').get(),
                'Country_of_origin': response.css('span.sc-1bsd7ul-1.sc-3zvnd-10.kmlJZt.hpuhl::text').get(),
                'key_information': response.css('span.sc-1bsd7ul-1.kmlJZt::text').get(),
                'oos': response.css('span.sc-1bsd7ul-1.sc-1axwsmm-5.djlKtC.iKyLRU::text').get(),
            }

            