import scrapy
from scrapy_splash import SplashRequest

class LaptopSpider(scrapy.Spider):
    name = 'kshop'
    def start_requests(self):
        url ='https://www.krisshop.com/en/product/16af9a9705dfedc3/akashi-blue-blended-whisky-0-7-l.html#readMore'
        yield SplashRequest(url)        

    def parse(self, response):
            yield {
                'name': response.css('div.productHeaderTitleText::text').get(),
                'brand': response.css('a.productHeaderBrandLink::text').get(),
                'price': response.css('span.productPriceFinalPrice::text').get(),
                'description': response.css('div.productDescriptionInnerExpandable').get(),
                #'Alcohol_percentage': response.xpath('//div[@class="productDescriptionText richtext"]/p[4]/text()').get(),
                #'Volume': response.xpath('//div[@class="productDescriptionText richtext"]/p[5]/text()').get(),
                #'Nose': response.xpath('//div[@class="productDescriptionText richtext"]/p[7]/text()').get(),
                #'Taste': response.xpath('//div[@class="productDescriptionText richtext"]/p[8]/text()').get(),
                #'Finish': response.xpath('//div[@class="productDescriptionText richtext"]/p[9]/text()').get(),
                'oos': response.xpath('//div[@class="addToCartButtonInnerHelper"]/div/text()').get(),
            }

            