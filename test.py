# import scrapy
# from scrapy.crawler import CrawlerProcess
# import json
# import csv


# class Pharmeasy(scrapy.Spider):
#     name = 'pharmeasy'
    
#     base_url = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=whisky&experiments=recHome-Z%2CbsHome-B%2CpastPurchaseCategory-B%2CsearchVariant-B%2CUnappliedPromoVariant-C%2CtrendH-B%2CtimerVariant-A%2CsubstitutionVariant-B%2CsubstitutionVariant-B%2CsubstitutionVariant-B%2CsubstitutionVariant-B%2CsubstitutionVariant-B%2CsubstitutionVariant-A&includeTagDetails=true&orderType=DELIVERY&page=&pageType=category&slug=whisky&storeId=165&url=whisky'
    
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
#     }
    
#     # def __init__(self):
#     #     with open('pharmeasy.csv', 'w') as csv_file:
#     #         csv_file.write('name,slug,manufacturer,price,availability,images\n')
    
#     def start_requests(self):
#         # scrape data from infinite scroll
#         for page in range(0, 4):    # specify page range you would like to scrape data for
#             next_page = self.base_url + str(page)
#             yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)
    
#     def parse(self, res):
#         data = ''
#         with open('res.json', 'r') as json_file:
#             for line in json_file.read():
#                 data += line
        
#         data = json.loads(data)
        
#         # data extraction logic
#         for product in data['data']['product']:
#             items = {
#                 'name': product['name'],
#                 # 'slug': product['slug'],
#                 # 'manufacturer': product['manufacturer'],
#                 # 'price': product['salePriceDecimal'],
#                 # 'availability': product['productAvailabilityFlags']['isAvailable'],
#                 # 'images': ', '.join(product['images'])
#             }

#             # append results to CSV
#             # with open('pharmeasy.csv', 'a') as csv_file:
#             #     writer = csv.DictWriter(csv_file, fieldnames=items.keys())
#             #     writer.writerow(items)

# # run scraper
# # process = CrawlerProcess()
# # process.crawl(Pharmeasy)
# # process.start()

# # debug data extraction
# Pharmeasy.parse(Pharmeasy, '')




