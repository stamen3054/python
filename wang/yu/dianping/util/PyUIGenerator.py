import tkinter
import tkinter.messagebox
from wang.yu.dianping.crawler.PyCrawler import PyCrawler
from wang.yu.dianping.util.PyXMLParser import PyXMLParser
import os
from io import BytesIO
from PIL import Image, ImageTk
import urllib
import urllib.request


class PyUIGenerator:
    def __init__(self):
        self.crawler = PyCrawler()
        self.xml_parser = PyXMLParser(os.path.dirname(os.path.dirname(__file__)) + '/properties/properties.xml')
        temp = self.xml_parser.do_parse()
        self.shop_info_selector = temp['websites']['selectors']['shop-info']
        self.shop_detail_selector = temp['websites']['selectors']['shop-detail']
        self.shop_dishlist_selector = temp['websites']['selectors']['shop-dishlist']
        self.base = tkinter.Tk('screen name', 'base name')
        self.base.geometry('400x600')
        self.frame = tkinter.Frame(self.base, width=400, height=600, bg='yellow')
        self.url_label = tkinter.Label(self.frame, text='输入网址')
        # self.url_input = tkinter.Entry(self.frame)
        self.url_input = tkinter.Entry(self.frame, textvariable=tkinter.StringVar(self.frame, value='https://www.dianping.com/search/category/10/10/r1651'))
        self.page_num_input = tkinter.Spinbox(self.frame, from_=1, to=7)
        self.main_button = tkinter.Button(self.frame, text='开始', command=self.click_main_btn)
        self.shop_list_box = tkinter.Listbox(self.frame, name="找到了以下店铺", selectmode='single')
        self.shop_detail_text = tkinter.Text(self.frame)
        self.status_label = tkinter.Label(self.frame)

    def get_page_number(self):
        return int(self.page_num_input.get())

    def get_user_input_url(self):
        return self.url_input.get()

    def click_main_btn(self):
        if self.get_user_input_url().startswith('http'):
            self.status_label.configure(text='爬取中...')
            self.main_button['state'] = 'disabled'
            self.base.update_idletasks()
            self.crawler.crawl_shop_info(self.get_user_input_url(), self.shop_info_selector, self.get_page_number())
            self.status_label.configure(text='完成')
            self.main_button['state'] = 'normal'
            self.draw_second_frame()
        else:
            self.draw_error_page()

    def draw_main_frame(self):
        self.url_label.pack()
        self.url_input.pack()
        self.main_button.pack()
        self.page_num_input.pack()
        self.status_label.pack(side='bottom')
        self.frame.pack()
        self.base.mainloop()

    def draw_second_frame(self):
        for count, res in enumerate(self.crawler.restaurants):
            self.shop_list_box.insert(count, res.__str__())
        self.shop_list_box.bind('<<ListboxSelect>>', self.update_second_frame)
        self.shop_list_box.pack()
        self.shop_detail_text.pack()

    def update_second_frame(self, event):
        index = int(event.widget.curselection()[0])
        self.status_label.configure(text='爬取中...')
        self.base.update_idletasks()
        restaurant = self.crawler.get_restaurant(index)
        self.crawler.crawl_shop_detail(restaurant, self.shop_detail_selector)
        self.shop_detail_text.delete(1.0, 'end')
        self.shop_detail_text.insert(1.0, restaurant.get_shop_detail())
        self.status_label.configure(text='完成')
        self.crawler.crawl_shop_dishlist(restaurant, self.shop_dishlist_selector)
        self.create_popup_window(restaurant)

    def create_popup_window(self, shop):
        top_window = tkinter.Toplevel()
        top_window.title('推荐菜单列表')
        top_window.geometry('1000x800')
        images = self.load_images(shop)
        line_counter = -1
        for i in range(0, len(images)):
            if i % 3 == 0:
                line_counter += 1
            label = tkinter.Label(top_window, image=images[i], text=shop.restaurant_dishlist[i], compound='left',
                                  borderwidth=4, relief='groove', width=300)
            label.grid(row=line_counter, column=i % 3)
        top_window_btn = tkinter.Button(top_window, text='关闭', command=top_window.destroy, compound='center')
        top_window_btn.grid(row=line_counter+1, column=1)
        top_window.mainloop()

    def load_images(self, shop):
        images = []
        for dish in shop.restaurant_dishlist:
            with urllib.request.urlopen(dish.dish_img_src) as u:
                raw_data = u.read()
            img = Image.open(BytesIO(raw_data))
            img.resize((200, 200))
            image = ImageTk.PhotoImage(img)
            images.append(image)
        return images
