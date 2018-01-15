class PyRestaurant:
    def __init__(self, restaurant_id, restaurant_name, rate=0, comment_number=0, average=0.0):
        self.rate = rate
        self.restaurant_id = restaurant_id
        self.restaurant_name = restaurant_name
        self.restaurant_comments = []
        self.restaurant_images = []
        self.restaurant_dishlist = []
        self.address = ''
        self.phone = ''
        self.average = average
        self.comment_number = comment_number

    def construct_url(self):
        return 'https://www.dianping.com/shop/' + self.restaurant_id

    def construct_dishlist_url(self):
        return self.construct_url() + '/dishlist'

    def get_shop_detail(self):
        return '店名：' + self.restaurant_name + \
               '\n地址：' + self.address + \
               '\n电话：' + self.phone + \
               '\n评分：' + self.rate + \
               '\n人均：' + (self.average.__str__() + '元' if self.average > 0 else '-')

    def __str__(self):
        return self.restaurant_name

    def __repr__(self):
        return '[' + self.restaurant_id + ']' + self.restaurant_name
