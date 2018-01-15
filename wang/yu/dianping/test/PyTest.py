from wang.yu.crawler.PyCrawler import PyCrawler
from wang.yu.util.PyXMLParser import PyXMLParser
from tkinter import font
import tkinter
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# # xml parser
# parser = PyXMLParser('../properties/properties.xml')
# temp = parser.do_parse()
# shop_info_str = temp['websites']['selectors']['shop-info']
# shop_detail_str = temp['websites']['selectors']['shop-detail']
# shop_menu_str = temp['websites']['selectors']['shop-menu']
#
# # crawler processing
# crawler = PyCrawler()
# # fetch shop basic info
# crawler.crawl_shop_info('https://www.dianping.com/search/category/10/10/r1651', shop_info_str, page_number=1)
# print('\n'.join([(counter+1).__str__()+' - '+res.__str__() for counter, res in enumerate(crawler.restaurants)]))
# # user select shop
# user_input = int(input('要看哪个?\n'))
# # go into shop page and get the detail
# restaurant = crawler.get_restaurant(user_input-1)
# crawler.crawl_shop_detail(restaurant, shop_detail_str)
# crawler.crawl_shop_menu(restaurant, shop_menu_str)
# print(restaurant.restaurant_menus)

import requests
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/61.0.3163.91 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cookie': '_hc.v=31ef5053-154c-ea0e-ca96-92eb521f544e.1501521356; _'
                      'lxsdk_cuid=15dadd29676c8-0a0335a3635a27-791238-1fa400-15dadd29676c8; _'
                      'lxsdk=15dadd29676c8-0a0335a3635a27-791238-1fa400-15dadd29676c8; __'
                      'mta=204780847.1501859868869.1505335822694.1505336503268.16; '
                      's_ViewType=10; aburl=1; cy=10; cye=tianjin; _'
                      'hc.s="\"31ef5053-154c-ea0e-ca96-92eb521f544e.1501521356.1505335526.1505336589\""; _'
                      'lxsdk_s=15e7cfd40f9-8d0-8fc-1ac%7C%7C86'
        }
temp = requests.get('http://www.dianping.com/shop/93957731/dishlist')

x = 1







