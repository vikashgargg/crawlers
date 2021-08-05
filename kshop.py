import time
import datetime
import csv
import base64
import json

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_splash import SplashRequest

from bs4 import BeautifulSoup

import pandas as pd


VISITED_URLS = set()


def convert_to_number(price, mode="min"):

    try:
        price = [''.join(j for j in i if j.isdigit() or j == ".")
                 for i in price]
        price = [float(i) for i in price if i]
        price = min(price)
    except BaseException:
        return ""
    return price


class SplashSpider(scrapy.Spider):
    name = "splash"

    def start_requests(self):

        df = pd.read_csv('all.csv')
        start = 0

        for i in df.iloc[start:, :].iterrows():
            url = i[1][2]
            splash_args = {
                'html': 1,
                'png': 1,
                # 'lua_source': 'splash:set_viewport_full()'
            }
            yield SplashRequest(url, self.parse_result, errback=self.errback_non_two, endpoint='render.json', args=splash_args, meta={'product_code': i[1][1], 'id_': i[1][0], 'timeout': 800, "retry": 0}, dont_filter=True)

    def parse_result(self, response):
        splash_args = {
            'html': 1,
            'png': 1,
            # 'lua_source': 'splash:set_viewport_full()'
        }

        id_ = response.meta['id_']
        product_code = response.meta['product_code']

        final = {}
        final['id_'] = id_
        retries = response.meta["retry"]

        description_xpath = '//span[@id="productTitle"]/text()'
        store_xpath = '//a[@id="bylineInfo"]/text()'
        price_xpath = '(//span[@id="priceblock_dealprice"]/text()|//span[@id="priceblock_ourprice"]/text())[1]|//div[@id="olp-new"]//span[@class="a-color-price"]/text()|//div[@id="olp-sl-new"]//span[@class="a-color-price"]/text()|//div[@class="a-section a-spacing-double-large"]//div[@class="a-column a-span2 olpPriceColumn"]/span["a-size-large a-color-price olpOfferPrice a-text-bold"]/text()|//span[@id="priceblock_saleprice"]/text()'

        # use pd to get brand
        table_xpath = '//table[@class="a-normal a-spacing-micro"]/text()'
        stars_xpath = '//span[@class="a-size-medium a-color-base"]/text()'
        rating_xpath = '//span[@class="a-size-base a-color-secondary"]/text()'
        #li_xpath = '//div[@id="detailBullets_feature_div"]/text()'
        li_xpath = '//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"]/text()'

        # no text()
        delivery_xpath = '//div[@id="dynamicDeliveryMessage"]'
        strike_xpath = '//span[@class="priceBlockStrikePriceString a-text-strike"]/text()'

        # instock
        instock_xpath = '(//span[@class="a-size-medium a-color-success"]/text())|//span[@class="a-size-medium a-color-state"]/text()'
        captch_xpath = """(//div[@class="a-box-inner"]//h4/text())[1]"""


        if response.xpath(captch_xpath).extract():
            print("The captcha was encountered", response.url, '---> ' ,  retries)
            print(response.xpath(captch_xpath).extract())

            if retries < 10:
                retries += 1

                if retries == 2:
                    filename = 'retries_9.csv'
                    with open(filename, 'a') as f:
                        txt = f"{product_code},{retries},{response.url},{response.status},{response.headers}"
                        f.write(txt)
                        print(txt)
                        f.write('\n')

                    filename = f"{str(product_code)}_{str(retries)}.html"
                    with open(filename, 'w') as f:
                        f.write(response.body_as_unicode())
                        f.write('\n')

                yield SplashRequest(response.url, self.parse_result, endpoint='render.json', args=splash_args, meta={'product_code': product_code, 'id_': id_, 'timeout': 800, "retry": retries}, dont_filter=True)


            else:

                print("Captcha retries max exceeded for url ", response.url)

        else:



            description_val = response.xpath(description_xpath).extract()
            if description_val:
                description_val = " ".join(description_val).strip()
                final["product_name_amazon"] = description_val
            else:
                final["product_name_amazon"] = ''

            price_val = response.xpath(price_xpath).extract()

            if price_val:
                price_val = convert_to_number(price_val)
                final["price_amazon"] = price_val
            else:
                final["price_amazon"] = ''
            strike_val = response.xpath(strike_xpath).extract()
            if strike_val:
                strike_val = convert_to_number(strike_val)
                final["mrp_on_amazon"] = strike_val
            else:
                final["mrp_on_amazon"] = ''

            stars_val = response.xpath(stars_xpath).extract()
            if stars_val:
                stars_val = " ".join(stars_val).strip()
                final["ratings_reviews_amazon"] = stars_val
            else:
                final["ratings_reviews_amazon"] = ''

            rating_val = response.xpath(rating_xpath).extract()
            if rating_val:
                rating_val = convert_to_number(rating_val)
                final["no_of_ratings"] = rating_val
            else:
                final["no_of_ratings"] = ''

            instock_val = response.xpath(instock_xpath).extract()
            print("---->", instock_val)
            if instock_val:
                instock_val = instock_val[-1].strip()
                #instock_val = " ".join(instock_val).strip()
                final["availability"] = instock_val
            else:
                final["availability"] = ''

            # try:
            #    instock_val = response.xpath(instock_xpath).extract()
            #    print(instock_val, response.url)
            #    if len(instock_val) > 0 :
            #        instock_bs4 = BeautifulSoup(instock_val,features="lxml")
            #        instock_raw = instock_bs4.text
            #        delivery_blacklist = ["\n", "Deal is claimed"]
            #        for i in delivery_blacklist:
            #            instock_raw = instock_raw.replace(i,'')

            #        final["availability"] = instock_raw.strip()

            #    else:
            #        final["availability"] = ''
            # except Exception as e:
            #    print(e)

            try:
                delivery_val = response.xpath(delivery_xpath).extract()[0]
                if len(delivery_val) > 0:
                    delivery_bs4 = BeautifulSoup(delivery_val, features="lxml")
                    delivery_raw = delivery_bs4.text
                    delivery_blacklist = ["\n", "Details"]
                    for i in delivery_blacklist:
                        delivery_raw = delivery_raw.replace(i, '')

                    final["delivery_info"] = delivery_raw.strip()

                else:
                    final["delivery_info"] = ''
            except Exception as e:
                print(e)

            try:
                # get_captcha_xpath()
                png_bytes = base64.b64decode(response.data['png'])
                filename = f'{product_code}.png'
                with open(filename, 'wb') as f:
                    f.write(png_bytes)
                final['screenshot_amazon'] = 'https://s3.ap-south-1.amazonaws.com/priceeye.1mg/screenshots/20210414/' + filename
            except Exception as e:
                print("There is some data error here")
                print(e)
            print(response.url, ' ---> ', response.status, '--> Price ', final['price_amazon'],
                    '--> Product Code ', product_code)

            final['amazon_links'] = response.url
            filename = 'results.json'
            with open(filename, 'a') as f:
                f.write(json.dumps(final))
                f.write('\n')

#            from scrapy.shell import inspect_response
#            inspect_response(response, self)

    def errback_non_two(self, failure):

        if failure.check(HttpError):
            response = failure.value.response

            filename = 'errback_500.csv'
            with open(filename, 'a') as f:
                txt = f"{response.url},{response.status},{response.headers}"
                f.write(txt)
                print(txt)
                f.write('\n')


                


def get_captcha_xpath():
    html = response.text
    fn = 'captcha.html'
    with open(fn, 'w') as f:
        f.write(html)
