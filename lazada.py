import scrapy
from scrapy_splash import SplashRequest

class LaptopSpider(scrapy.Spider):
    name = 'lazada'
    def start_requests(self):
        url ='https://www.lazada.sg/products/akashi-red-blended-whisky-500ml-i114930551-s123533794.html?spm=a2o42.searchlist.list.28.5ecce4cc4klkP6&search=1'
        yield SplashRequest(url)        

    def parse(self, response):
            yield {
                'name': response.css('h1.pdp-mod-product-badge-title::text').get(),
                'price': response.css('span.pdp-price.pdp-price_type_normal.pdp-price_color_orange.pdp-price_size_xl::text').get(),
                'Brand': response.css('a.pdp-link.pdp-link_size_s.pdp-link_theme_blue.pdp-product-brand__brand-link::text').get(),
                # 'oos': response.css('button[data-spm-anchor-id="a2o42.pdp_revamp.0.i1.5ca27bdcMNM2F4"]::text').get(),
                # 'description': response.css('div.pdp-product-desc::text').get(),
            }