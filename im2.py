# import json
# import pandas as pd
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from lazada.items import LiquorItem
# from itemloaders.processors import MapCompose
# from scrapy.loader import ItemLoader

# def get_num(string):
#     return ''.join( i for i in string if i.isdigit() or i in ['.'])

# def get_table_as_json(string):
#     table = pd.read_html(string)[0]
#     table.index = table.iloc[:,0]
#     table = table.iloc[:,1]
#     table = table.to_dict()
#     return json.dumps(table)

# # def get_prices(ls):
# #     ls = [get_num(l) for l in ls]
# #     return min(ls,default='0'),max(ls,default='0')

# class WnsSpider(CrawlSpider):
#     name = 'tlshop'
#     allowed_domains = ['theliquorshop.com.sg']
#     start_urls = ['https://www.theliquorshop.com.sg/collections/whisky-singapore']

#     box_xpath =  '//a[@class="product-grid-item"]'
#     next_xpath = '//a[@title="Next »"]'


#     rules = (
#         Rule(LinkExtractor(restrict_xpaths=next_xpath),follow=True),
#         Rule(LinkExtractor(restrict_xpaths=box_xpath),callback='parse')
#             )

#     def parse(self, response):
#         l = ItemLoader(item = LiquorItem(), response = response)
#         l.add_value('url',response.url)
#         l.add_xpath('name','//h1[@itemprop="name"]/text()',MapCompose(str.strip))
#         l.add_xpath('price','//span[@id="productPrice-product-template"]/span/text()',MapCompose(str.strip))
#         l.add_xpath('oos','//button[@id="addToCart-product-template"]/span[2]/text()',MapCompose(str.strip))
#         l.add_xpath('table','//div[@class="product-description rte"]/table',MapCompose(get_table_as_json))
        
#         # l.add_xpath('description','string(//div[@itemprop="description"]/table/tbody/tr/td[2]/text())',MapCompose(str.strip))
#         # l.add_xpath('volume','//div[@itemprop="description"]/table/tbody/tr[2]/td[2]/text()',MapCompose(str.strip))
#         # l.add_xpath('alcohol_percentage','//div[@itemprop="description"]/table/tbody/tr[3]/td[2]/text()',MapCompose(str.strip))
#         # # l.add_xpath('type','//div[@itemprop="description"]/table/tbody/tr[4]/td[2]/text()',MapCompose(str.strip))
#         # l.add_xpath('with_box','//div[@itemprop="description"]/table/tbody/tr[5]/td[2]/text()',MapCompose(str.strip))
        


#         #l.add_xpath('price','//div[@class="product-description-container"]//ul[@class="product-price"]//div[@class="new-prices"]',MapCompose(get_num))
#         #l.add_xpath('price','//div[@class="product-description-container"]//ul[@class="product-price"][//div[@class="new-prices"] or //div[@class="new-prices special-prices"]]',MapCompose(get_num))

#         # prices = response.xpath('//div[@class="product-description-container"]//ul[@class="product-price"]//li').getall()

#         # prices = get_prices(prices)
#         # l.add_value('regular_price',prices[0])
#         # l.add_value('sale_price',prices[1])

#         return l.load_item()