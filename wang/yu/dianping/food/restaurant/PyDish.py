class PyDish:
    def __init__(self, dish_name, dish_price, dish_img_src, dish_recommend_count=0):
        self.dish_name = dish_name
        self.dish_price = dish_price if dish_price != '' else 0
        self.dish_img_src = dish_img_src
        self.dish_recommend_count = dish_recommend_count if dish_recommend_count != '' else 0

    def __str__(self):
        return '\n'.join([self.dish_name, '￥' + str(self.dish_price), str(self.dish_recommend_count) + '人推荐'])
