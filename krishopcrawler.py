import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tutorial.items import KrishItem
from itemloaders.processors import MapCompose
from scrapy.loader import ItemLoader

def get_num(string):
    return ''.join( i for i in string if i.isdigit() or i in ['.'])

# def get_prices(ls):
#     ls = [get_num(l) for l in ls]
#     return min(ls,default='0'),max(ls,default='0')

class WnsSpider(CrawlSpider):
    name = 'abc'
    allowed_domains = ['krisshop.com/en/']
    start_urls = ['https://www.krisshop.com/en/category/kso_online_wineSpirits/wine-%26-spirits.html?excludeBrandType=premium']

    box_xpath =  '//a[@class="productTile  productGridTilesItem"]'
    next_xpath = '//a[class="button buttonSizeRegular buttonStyleSecondary"]'


    rules = (
        Rule(LinkExtractor(restrict_xpaths=next_xpath),follow=True),
        Rule(LinkExtractor(restrict_xpaths=box_xpath),callback='parse')
            )

    def parse(self, response):
        l = ItemLoader(item = KrishItem(), response = response)
        l.add_value('url',response.url)
        l.add_xpath('name','//div[@class="productHeaderTitleText"]/text()',MapCompose(str.strip))
        # l.add_css('brand','a.productHeaderBrandLink::text',MapCompose(str.strip))
        # l.add_css('price','span.productPriceFinalPrice::text',MapCompose(str.strip))
        # l.add_css('description','string(div.productDescriptionInnerExpandable)',MapCompose(str.strip))
        # l.add_xpath('oos','//div[@class="addToCartButtonInnerHelper"]/div/text()',MapCompose(str.strip))


        #l.add_xpath('price','//div[@class="product-description-container"]//ul[@class="product-price"]//div[@class="new-prices"]',MapCompose(get_num))
        #l.add_xpath('price','//div[@class="product-description-container"]//ul[@class="product-price"][//div[@class="new-prices"] or //div[@class="new-prices special-prices"]]',MapCompose(get_num))

        # prices = response.xpath('//div[@class="product-description-container"]//ul[@class="product-price"]//li').getall()

        # prices = get_prices(prices)
        # l.add_value('regular_price',prices[0])
        # l.add_value('sale_price',prices[1])

        return l.load_item()
