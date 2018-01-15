import requests
from bs4 import BeautifulSoup
from wang.yu.dianping.food.restaurant.PyRestaurant import PyRestaurant
from wang.yu.dianping.food.restaurant.PyDish import PyDish


class PyCrawler:

    def __init__(self, encoding='utf-8'):
        self.encoding = encoding
        self.children = []
        self.restaurants = []

    def crawl_shop_info(self, url, css_selector, page_number=5):
        shop_url = url
        for i in range(0, page_number):
            if i > 1:
                shop_url = url + 'p' + i.__str__()
            parent_soup = self.retrieve_page_info(shop_url)
            for item in parent_soup.select(css_selector):
                restaurant = PyRestaurant(
                    item.a.get('href').replace('http://www.dianping.com/shop/', ''),
                    item.select('a')[0].attrs['title'],
                    item.parent.select_one('.comment span')['class'][1][-2],
                    int(item.parent.select('.review-num b')[0].text),
                    float(
                        item.parent.select('.mean-price b')[0].text[1:])
                    if len(item.parent.select('.mean-price b')) > 0
                    else 0
                )
                self.restaurants.append(restaurant)

    def crawl_shop_detail(self, shop, css_selector):
        # goes inside each shop page and crawls comments, address, contact, and rating
        parent_soup = self.retrieve_page_info(shop.construct_url())
        for item in parent_soup.select(css_selector):
            shop.address = item.select_one('div.address span.item').attrs['title']
            shop.phone = item.select_one('p.tel span.item').text
        return None

    def crawl_shop_dishlist(self, shop, css_selector):
        # loop through the recommended food list
        parent_soup = self.retrieve_page_info(shop.construct_dishlist_url())
        for item in parent_soup.select(css_selector):
            shop.restaurant_dishlist.append(
                PyDish(item.select_one('img').attrs['alt'],
                       item.select_one('.shop-food-money').text.rstrip()[1:],
                       item.select_one('img').attrs['src'],
                       item.select_one('.recommend-count').text.rstrip()[:-3])
            )

    def retrieve_page_info(self, url):
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
        source_code = requests.get(url, headers=headers)
        source_code.encoding = self.encoding
        plain_text = source_code.text
        return BeautifulSoup(plain_text, 'html.parser')

    def get_restaurant(self, index):
        return self.restaurants[index]

