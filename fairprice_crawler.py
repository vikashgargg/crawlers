import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tutorial.items import WnsItem
from itemloaders.processors import MapCompose
from scrapy.loader import ItemLoader

def get_num(string):
    return ''.join( i for i in string if i.isdigit() or i in ['.'])

# def get_prices(ls):
#     ls = [get_num(l) for l in ls]
#     return min(ls,default='0'),max(ls,default='0')

class WnsSpider(CrawlSpider):
    name = 'wns'
    allowed_domains = ['fairprice.com.sg']
    start_urls = ['https://www.fairprice.com.sg/category/whisky']

    box_xpath =  '//div[@class="sc-1plwklf-1 kXzSdT"]'
    next_xpath = '//ul[@class="pagination"]/li[last()]/a'


    rules = (
        Rule(LinkExtractor(restrict_xpaths=next_xpath),follow=True),
        Rule(LinkExtractor(restrict_xpaths=box_xpath),callback='parse')
            )

    def parse(self, response):
        l = ItemLoader(item = WnsItem(), response = response)
        l.add_value('url',response.url)
        l.add_css('name','span.sc-1bsd7ul-1.djlKtC::text',MapCompose(str.strip))
        l.add_css('brand','a.sc-13n2dsm-1.jLtMNk::text',MapCompose(str.strip))
        l.add_css('price','span.sc-1bsd7ul-1.sc-13n2dsm-5.kxEbZl.deQJPo::text',MapCompose(str.strip))
        l.add_css('key_information','string(span.sc-1bsd7ul-1.kmlJZt::text)',MapCompose(str.strip))
        l.add_css('volume','span.sc-1bsd7ul-1.LLmwF::text',MapCompose(str.strip))
        l.add_css('Country_of_origin','span.sc-1bsd7ul-1.sc-3zvnd-10.kmlJZt.hpuhl::text',MapCompose(str.strip))
        l.add_css('oos','span.sc-1bsd7ul-1.sc-1axwsmm-5.djlKtC.iKyLRU::text',MapCompose(str.strip))


        #l.add_xpath('price','//div[@class="product-description-container"]//ul[@class="product-price"]//div[@class="new-prices"]',MapCompose(get_num))
        #l.add_xpath('price','//div[@class="product-description-container"]//ul[@class="product-price"][//div[@class="new-prices"] or //div[@class="new-prices special-prices"]]',MapCompose(get_num))

        # prices = response.xpath('//div[@class="product-description-container"]//ul[@class="product-price"]//li').getall()

        # prices = get_prices(prices)
        # l.add_value('regular_price',prices[0])
        # l.add_value('sale_price',prices[1])

        return l.load_item()
